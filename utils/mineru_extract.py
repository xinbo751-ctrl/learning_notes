#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Convert PDF(s) into LLM-ready artifacts via MinerU API (v4 batch upload).

CLI
    --filing   Single PDF file path
    --base     Directory containing PDF files (recursively searches *.pdf)
    --output   Output directory (default: ./output)
    --ocr      Enable OCR (default: false)
    --html     Export HTML format (extra_formats=["html"]) when set

Environment variables (required)
    MINERU_TOKEN
        API token from MinerU console. Sent as Authorization: Bearer <token>

Environment variables (optional)
    MINERU_API_BASE (default "https://mineru.net/api/v4")
        Base URL for MinerU v4 API.

    MINERU_MODEL_VERSION (default "pipeline")
        "pipeline" or "vlm".

    MINERU_LANGUAGE (optional)
        Language code for OCR (pipeline only). Default: "ch".

    MINERU_ENABLE_FORMULA (optional)
        "true" or "false" (pipeline only). Default: true.

    MINERU_ENABLE_TABLE (optional)
        "true" or "false" (pipeline only). Default: true.

    MINERU_IS_OCR (optional)
        "true" or "false" (pipeline only, per-file). Default: false.


    MINERU_EXTRA_FORMATS (optional)
        Comma-separated list of extra export formats: docx, html, latex.

    MINERU_BATCH_SIZE (optional, default 50)
        Max files per batch request (doc limit is 200).

    MINERU_POLL_INTERVAL_SEC (optional, default 5.0)
    MINERU_POLL_TIMEOUT_SEC (optional, default 1800)

    MINERU_CHUNK_CHARS (optional, default 1800)
        Chunk size used when generating chunks.json / chunks.jsonl.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import requests
from requests.exceptions import Timeout


MAX_TIMEOUT_RETRIES = 3
RETRY_BACKOFF_BASE_SEC = 0.8


def _sleep_backoff(attempt_idx: int) -> None:
    time.sleep(RETRY_BACKOFF_BASE_SEC * (2 ** attempt_idx))


def _sha256_8(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:8]


def _safe_slug(name: str) -> str:
    name = name.strip()
    name = re.sub(r"\s+", " ", name)
    name = re.sub(r"[\\/]+", "_", name)
    name = re.sub(r"[^\w\s.-]+", "_", name)
    name = name.strip(" ._-")
    return name or "pdf"


def _read_env_float(name: str, default: float) -> float:
    v = os.environ.get(name)
    if v is None or not v.strip():
        return default
    try:
        return float(v)
    except Exception:
        return default


def _read_env_int(name: str, default: int) -> int:
    v = os.environ.get(name)
    if v is None or not v.strip():
        return default
    try:
        return int(v)
    except Exception:
        return default


def _read_env_str(name: str, default: str) -> str:
    v = os.environ.get(name)
    if v is None:
        return default
    v = v.strip()
    return v if v else default


def _read_env_list(name: str) -> Optional[List[str]]:
    v = os.environ.get(name)
    if v is None or not v.strip():
        return None
    items = [x.strip() for x in v.split(",") if x.strip()]
    return items or None


def _parse_bool_env(name: str) -> Optional[bool]:
    v = os.environ.get(name)
    if v is None or not v.strip():
        return None
    s = v.strip().lower()
    if s in {"1", "true", "yes", "y"}:
        return True
    if s in {"0", "false", "no", "n"}:
        return False
    return None


def _batched(items: List[Path], batch_size: int) -> Iterable[List[Path]]:
    if batch_size <= 0:
        batch_size = 1
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def _log(message: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {message}")


def _iter_pdfs_from_base(base_dir: Path) -> List[Path]:
    if not base_dir.exists() or not base_dir.is_dir():
        raise SystemExit(f"--base is not a directory: {base_dir}")
    pdfs = sorted(p for p in base_dir.rglob("*.pdf") if p.is_file())
    return pdfs


def _collect_files_recursive(root: Path) -> List[Path]:
    if not root.exists():
        return []
    return sorted([p for p in root.rglob("*") if p.is_file()])


def _find_mineru_primary_md(pdf_stem: str, files: List[Path]) -> Optional[Path]:
    # Official MinerU CLI typically emits: {原文件名}.md
    stem = pdf_stem.lower()
    exact = [p for p in files if p.suffix.lower() == ".md" and p.stem.lower() == stem]
    if exact:
        return exact[0]
    any_md = [p for p in files if p.suffix.lower() in {".md", ".markdown"}]
    if any_md:
        return any_md[0]
    return None


def _find_content_list_json(pdf_stem: str, files: List[Path]) -> Optional[Path]:
    # {原文件名}_content_list.json
    target = f"{pdf_stem}_content_list".lower()
    cand = [p for p in files if p.suffix.lower() == ".json" and p.stem.lower() == target]
    if cand:
        return cand[0]
    # fallback: any file ending with _content_list.json
    cand2 = [p for p in files if p.name.lower().endswith("_content_list.json")]
    if cand2:
        return cand2[0]
    return None


def _find_model_json(pdf_stem: str, files: List[Path]) -> Optional[Path]:
    # {原文件名}_model.json (VLM/pipeline)
    target = f"{pdf_stem}_model".lower()
    cand = [p for p in files if p.suffix.lower() == ".json" and p.stem.lower() == target]
    if cand:
        return cand[0]
    # fallback: any file ending with _model.json
    cand2 = [p for p in files if p.name.lower().endswith("_model.json")]
    if cand2:
        return cand2[0]
    return None


def _content_list_to_text(content_list: Any) -> str:
    # Best-effort: flatten readable parts.
    if not isinstance(content_list, list):
        return ""
    parts: List[str] = []
    for item in content_list:
        if not isinstance(item, dict):
            continue
        t = item.get("type")
        if t in {"text", "title", "header", "footer", "page_number", "page_footnote", "aside_text"}:
            s = item.get("text")
            if isinstance(s, str) and s.strip():
                parts.append(s.strip())
        elif t == "equation":
            s = item.get("text")
            if isinstance(s, str) and s.strip():
                parts.append(s.strip())
        elif t == "table":
            caps = item.get("table_caption")
            if isinstance(caps, list):
                parts.extend([str(x).strip() for x in caps if str(x).strip()])
            body = item.get("table_body")
            if isinstance(body, str) and body.strip():
                parts.append(body.strip())
        elif t == "image":
            caps = item.get("image_caption")
            if isinstance(caps, list):
                parts.extend([str(x).strip() for x in caps if str(x).strip()])
        elif t == "code":
            cap = item.get("code_caption")
            if isinstance(cap, list):
                parts.extend([str(x).strip() for x in cap if str(x).strip()])
            body = item.get("code_body")
            if isinstance(body, str) and body.strip():
                parts.append(body.strip())
        elif t == "list":
            items = item.get("list_items")
            if isinstance(items, list):
                parts.extend([str(x).strip() for x in items if str(x).strip()])
    return "\n\n".join([p for p in parts if p])


def _model_json_to_text(model: Any) -> str:
    # VLM model.json: list[page] -> list[block]
    if not isinstance(model, list):
        return ""
    parts: List[str] = []
    for page in model:
        if not isinstance(page, list):
            continue
        for block in page:
            if not isinstance(block, dict):
                continue
            t = block.get("type")
            content = block.get("content")
            if isinstance(content, str) and content.strip():
                # keep textual content types; for unknown types still keep content to avoid loss
                if t in {
                    "text",
                    "title",
                    "equation",
                    "image_caption",
                    "image_footnote",
                    "table_caption",
                    "table_footnote",
                    "code",
                    "code_caption",
                    "ref_text",
                    "algorithm",
                    "list",
                    "header",
                    "footer",
                    "page_number",
                    "aside_text",
                    "page_footnote",
                } or t is None:
                    parts.append(content.strip())
                else:
                    parts.append(content.strip())
    return "\n\n".join([p for p in parts if p])


def _is_error_status(data: Any) -> Optional[str]:
    if not isinstance(data, dict):
        return None
    code = data.get("code")
    if isinstance(code, int) and code != 0:
        msg = data.get("msg") or data.get("message") or str(code)
        return str(msg)
    return None


def _chunk_text(text: str, max_chars: int) -> List[Dict[str, Any]]:
    lines = [ln.rstrip() for ln in text.splitlines()]
    paras: List[str] = []
    buf: List[str] = []
    for ln in lines:
        if not ln.strip():
            if buf:
                paras.append("\n".join(buf).strip())
                buf = []
            continue
        buf.append(ln)
    if buf:
        paras.append("\n".join(buf).strip())

    chunks: List[Dict[str, Any]] = []
    cur: List[str] = []
    cur_len = 0

    def flush() -> None:
        nonlocal cur, cur_len
        if not cur:
            return
        chunk_text = "\n\n".join(cur).strip()
        if chunk_text:
            chunks.append(
                {
                    "index": len(chunks),
                    "text": chunk_text,
                    "char_len": len(chunk_text),
                }
            )
        cur = []
        cur_len = 0

    for p in paras:
        if not p:
            continue
        if len(p) > max_chars:
            # hard split long paragraph
            start = 0
            while start < len(p):
                part = p[start : start + max_chars]
                if cur_len + len(part) + (2 if cur else 0) > max_chars:
                    flush()
                cur.append(part)
                cur_len += len(part)
                flush()
                start += max_chars
            continue

        projected = cur_len + len(p) + (2 if cur else 0)
        if projected > max_chars:
            flush()
        cur.append(p)
        cur_len += len(p)

    flush()
    return chunks


@dataclass
class MinerUConfig:
    api_base: str
    token: str
    model_version: str
    language: Optional[str]
    enable_formula: bool
    enable_table: bool
    is_ocr: bool
    extra_formats: Optional[List[str]]
    batch_size: int
    poll_interval_sec: float
    poll_timeout_sec: float


class MinerUClient:
    def __init__(self, cfg: MinerUConfig):
        self.cfg = cfg

    def _headers(self) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.cfg.token}",
        }

    def apply_upload_urls(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        url = f"{self.cfg.api_base}/file-urls/batch"
        payload: Dict[str, Any] = {
            "files": files,
            "model_version": self.cfg.model_version,
        }
        if self.cfg.enable_formula is not None:
            payload["enable_formula"] = self.cfg.enable_formula
        if self.cfg.enable_table is not None:
            payload["enable_table"] = self.cfg.enable_table
        if self.cfg.language:
            payload["language"] = self.cfg.language
        if self.cfg.extra_formats:
            payload["extra_formats"] = self.cfg.extra_formats

        last_err: Optional[Exception] = None
        for attempt in range(MAX_TIMEOUT_RETRIES):
            try:
                r = requests.post(url, headers=self._headers(), json=payload, timeout=60)
                r.raise_for_status()
                return r.json()
            except Timeout as e:
                last_err = e
                if attempt < MAX_TIMEOUT_RETRIES - 1:
                    _sleep_backoff(attempt)
                    continue
                raise
            except Exception as e:
                last_err = e
                raise
        raise last_err  # type: ignore[misc]

    def upload_file(self, upload_url: str, file_path: Path) -> None:
        last_err: Optional[Exception] = None
        for attempt in range(MAX_TIMEOUT_RETRIES):
            try:
                with open(file_path, "rb") as f:
                    r = requests.put(upload_url, data=f, timeout=120)
                r.raise_for_status()
                return
            except Timeout as e:
                last_err = e
                if attempt < MAX_TIMEOUT_RETRIES - 1:
                    _sleep_backoff(attempt)
                    continue
                raise
            except Exception as e:
                last_err = e
                raise
        raise last_err  # type: ignore[misc]

    def poll_batch_results(self, batch_id: str) -> Dict[str, Any]:
        url = f"{self.cfg.api_base}/extract-results/batch/{batch_id}"
        deadline = time.time() + self.cfg.poll_timeout_sec
        last_json: Dict[str, Any] = {}

        while True:
            if time.time() > deadline:
                raise SystemExit(f"Polling timed out after {self.cfg.poll_timeout_sec}s: batch_id={batch_id}")

            r = requests.get(url, headers=self._headers(), timeout=60)
            r.raise_for_status()
            try:
                data = r.json()
            except Exception:
                data = {"raw": r.text}

            if isinstance(data, dict):
                last_json = data

            err = _is_error_status(data)
            if err:
                raise SystemExit(f"MinerU batch failed: batch_id={batch_id} error={err}")

            extract_result = ((data or {}).get("data") or {}).get("extract_result")
            if isinstance(extract_result, list) and extract_result:
                states = [str(x.get("state", "")).lower() for x in extract_result if isinstance(x, dict)]
                done = sum(1 for s in states if s == "done")
                failed = sum(1 for s in states if s == "failed")
                running = sum(1 for s in states if s == "running")
                pending = sum(1 for s in states if s == "pending")
                waiting = sum(1 for s in states if s == "waiting-file")
                converting = sum(1 for s in states if s == "converting")
                total = len(states)
                _log(
                    f"Polling batch {batch_id}: total={total} done={done} failed={failed} "
                    f"running={running} pending={pending} waiting-file={waiting} converting={converting}"
                )
                if states and all(s in {"done", "failed"} for s in states):
                    return last_json

            time.sleep(self.cfg.poll_interval_sec)


def _save_zip_and_extract(zip_bytes: bytes, out_dir: Path) -> List[Path]:
    import zipfile

    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / "result.zip"
    zip_path.write_bytes(zip_bytes)

    artifacts_dir = out_dir / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    extracted: List[Path] = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        for name in zf.namelist():
            # Basic zip-slip protection
            p = Path(name)
            if p.is_absolute() or ".." in p.parts:
                continue
            target = artifacts_dir / p
            target.parent.mkdir(parents=True, exist_ok=True)
            if name.endswith("/"):
                target.mkdir(parents=True, exist_ok=True)
                continue
            with zf.open(name, "r") as src:
                target.write_bytes(src.read())
            extracted.append(target)

    try:
        zip_path.unlink(missing_ok=True)
    except Exception:
        pass

    return extracted


def _download_files_list(files_list: Any, out_dir: Path, headers: Dict[str, str]) -> List[Path]:
    artifacts_dir = out_dir / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    saved: List[Path] = []
    if not isinstance(files_list, list):
        return saved

    for item in files_list:
        if not isinstance(item, dict):
            continue
        url = item.get("url") or item.get("download_url")
        name = item.get("name") or item.get("filename")
        if not isinstance(url, str) or not url.strip():
            continue
        if not isinstance(name, str) or not name.strip():
            name = _sha256_8(url)
        name = _safe_slug(name)
        out_path = artifacts_dir / name

        r = requests.get(url, headers=headers, timeout=120)
        r.raise_for_status()
        out_path.write_bytes(r.content)
        saved.append(out_path)

    return saved


def _normalize_outputs(
    out_dir: Path,
    extracted_paths: List[Path],
    pdf_stem: Optional[str] = None,
) -> None:

    if not (out_dir / "document.md").exists():
        stem = pdf_stem or out_dir.name.split("_")[0]
        primary_md = _find_mineru_primary_md(stem, extracted_paths)
        if primary_md:
            try:
                _write_text(out_dir / "document.md", primary_md.read_text(encoding="utf-8"))
            except Exception:
                pass

    if not (out_dir / "document.txt").exists():
        txt_candidates = [p for p in extracted_paths if p.suffix.lower() in {".txt"}]
        if txt_candidates:
            try:
                _write_text(out_dir / "document.txt", txt_candidates[0].read_text(encoding="utf-8"))
            except Exception:
                pass

    if not (out_dir / "document.txt").exists():
        stem = pdf_stem or out_dir.name.split("_")[0]
        content_list_path = _find_content_list_json(stem, extracted_paths)
        if content_list_path:
            try:
                obj = json.loads(content_list_path.read_text(encoding="utf-8"))
                txt = _content_list_to_text(obj)
                if txt.strip():
                    _write_text(out_dir / "document.txt", txt)
            except Exception:
                pass

    if not (out_dir / "document.txt").exists():
        stem = pdf_stem or out_dir.name.split("_")[0]
        model_path = _find_model_json(stem, extracted_paths)
        if model_path:
            try:
                obj = json.loads(model_path.read_text(encoding="utf-8"))
                txt = _model_json_to_text(obj)
                if txt.strip():
                    _write_text(out_dir / "document.txt", txt)
            except Exception:
                pass


def _load_for_chunking(out_dir: Path) -> Optional[str]:
    txt = out_dir / "document.txt"
    md = out_dir / "document.md"
    if txt.exists():
        try:
            return txt.read_text(encoding="utf-8")
        except Exception:
            return None
    if md.exists():
        try:
            return md.read_text(encoding="utf-8")
        except Exception:
            return None
    return None


def _download_and_extract_zip(url: str, out_dir: Path) -> List[Path]:
    r = requests.get(url, timeout=180)
    r.raise_for_status()
    return _save_zip_and_extract(r.content, out_dir)


def _handle_single_result(
    result: Dict[str, Any],
    pdf_path: Path,
    out_root: Path,
    *,
    single_mode: bool,
) -> Optional[tuple[Path, str]]:
    file_name = result.get("file_name")
    state = str(result.get("state", "")).lower()
    if file_name and file_name != pdf_path.name:
        return None

    if single_mode:
        out_dir = out_root
    else:
        out_dir = out_root / _safe_slug(pdf_path.stem)
    out_dir.mkdir(parents=True, exist_ok=True)

    meta = {
        "input_pdf": str(pdf_path.resolve()),
        "output_dir": str(out_dir),
        "state": state,
    }

    if state == "failed":
        meta["error"] = result.get("err_msg")
        _write_json(out_dir / "meta.json", meta)
        return out_dir, state

    if state == "done":
        zip_url = result.get("full_zip_url")
        if isinstance(zip_url, str) and zip_url.strip():
            _download_and_extract_zip(zip_url, out_dir)

    _write_json(out_dir / "meta.json", meta)
    return out_dir, state

def process_batch_pdfs(
    client: MinerUClient,
    pdf_paths: List[Path],
    out_root: Path,
    *,
    single_mode: bool,
) -> tuple[List[Path], List[tuple[Path, str]]]:
    files_payload: List[Dict[str, Any]] = []
    for p in pdf_paths:
        item: Dict[str, Any] = {
            "name": p.name,
            "data_id": _sha256_8(str(p.resolve())),
            "is_ocr": client.cfg.is_ocr
        }
        files_payload.append(item)

    resp = client.apply_upload_urls(files_payload)
    err = _is_error_status(resp)
    if err:
        raise SystemExit(f"Apply upload urls failed: {err}")

    batch_id = ((resp.get("data") or {}).get("batch_id") or "").strip()
    file_urls = (resp.get("data") or {}).get("file_urls") or (resp.get("data") or {}).get("files")
    if not batch_id or not isinstance(file_urls, list) or len(file_urls) != len(pdf_paths):
        raise SystemExit("Invalid response: missing batch_id or file_urls")

    for i, url in enumerate(file_urls):
        client.upload_file(str(url), pdf_paths[i])

    results = client.poll_batch_results(batch_id)
    extract_results = ((results.get("data") or {}).get("extract_result") or [])

    out_dirs: List[Path] = []
    failed_items: List[tuple[Path, str]] = []
    if isinstance(extract_results, list):
        for p in pdf_paths:
            matched = None
            for r in extract_results:
                if not isinstance(r, dict):
                    continue
                if r.get("file_name") == p.name:
                    matched = r
                    break
            if matched:
                handled = _handle_single_result(matched, p, out_root, single_mode=single_mode)
                if handled:
                    out_dir, state = handled
                    if state == "done":
                        out_dirs.append(out_dir)
                    else:
                        failed_items.append((p, str(matched.get("err_msg") or "failed")))
            else:
                failed_items.append((p, "missing result"))
    return out_dirs, failed_items


def build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Convert PDF(s) into LLM-ready artifacts via MinerU API")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--filing", type=str, help="Single PDF file path")
    g.add_argument("--base", type=str, help="Directory containing PDF files (recursively searches *.pdf)")
    ap.add_argument("--output", type=str, default="./output", help="Output directory (default: ./output)")
    ap.add_argument("--ocr", action="store_true", help="Enable OCR (default: false)")
    ap.add_argument("--html", action="store_true", help="Export HTML (extra_formats=[\"html\"]) ")
    ap.add_argument("--sleep", type=float, default=30.0, help="Polling interval in seconds (default: 30)")
    ap.add_argument("--timeout", type=float, default=1200.0, help="Polling timeout in seconds (default: 1200)")
    return ap


def main(argv: Optional[List[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)

    token = (os.environ.get("MINERU_TOKEN") or "YOUR_API_TOKEN").strip()

    api_base = _read_env_str("MINERU_API_BASE", "https://mineru.net/api/v4")
    model_version = _read_env_str("MINERU_MODEL_VERSION", "pipeline")

    extra_formats = ["html"] if args.html else _read_env_list("MINERU_EXTRA_FORMATS")

    cfg = MinerUConfig(
        api_base=api_base.rstrip("/"),
        token=token,
        model_version=model_version,
        language=_read_env_str("MINERU_LANGUAGE", "ch").strip() or "ch",
        enable_formula=_parse_bool_env("MINERU_ENABLE_FORMULA") if _parse_bool_env("MINERU_ENABLE_FORMULA") is not None else True,
        enable_table=_parse_bool_env("MINERU_ENABLE_TABLE") if _parse_bool_env("MINERU_ENABLE_TABLE") is not None else True,
        is_ocr=args.ocr,
        extra_formats=extra_formats,
        batch_size=_read_env_int("MINERU_BATCH_SIZE", 50),
        poll_interval_sec=args.sleep,
        poll_timeout_sec=0.0,
    )

    output_root = Path(args.output).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    client = MinerUClient(cfg)

    single_mode = bool(args.filing)
    if args.filing:
        pdf_path = Path(args.filing).expanduser()
        pdfs = [pdf_path]
        out_root = output_root / _safe_slug(pdf_path.stem)
    else:
        base_dir = Path(args.base).expanduser()
        pdfs = _iter_pdfs_from_base(base_dir)
        out_root = output_root / _safe_slug(base_dir.name)
    out_root.mkdir(parents=True, exist_ok=True)

    if not pdfs:
        print("No PDFs found.", file=sys.stderr)
        return 1

    cfg.poll_timeout_sec = args.timeout * len(pdfs)

    _log(f"Found {len(pdfs)} PDF(s). Output root: {out_root}")

    ok = 0
    failed = 0

    for batch in _batched(pdfs, cfg.batch_size):
        _log(f"Submitting batch of {len(batch)} file(s)...")
        try:
            out_dirs, failed_items = process_batch_pdfs(client, batch, out_root, single_mode=single_mode)
            for d in out_dirs:
                _log(f"  -> {d}")
            for p, err in failed_items:
                _log(f"  !! failed: {p.name} | {err}")
            ok += len(out_dirs)
            failed += len(failed_items)
        except Exception as e:
            failed += len(batch)
            print(f"Batch failed: {e}", file=sys.stderr)

    _log(f"Done. ok={ok} failed={failed}")
    return 0 if failed == 0 else 3


if __name__ == "__main__":
    raise SystemExit(main())
