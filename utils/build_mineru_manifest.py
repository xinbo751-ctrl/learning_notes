#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Build a searchable manifest from MinerU-extracted output.

Why
----
MinerU extraction produces many files (images/layout/json/etc). For LLM writing,
we usually want a small, structured index over *textual* content.

This script scans a MinerU output root (e.g. output/0883/), finds each document
folder (identified by a meta.json), reads its primary text (prefer artifacts/full.md),
chunks it, and writes:

- manifest.jsonl  (machine-friendly; includes chunk text)
- manifest.tsv    (human-friendly; no full text)
- toc.md (skeleton; created by default if missing)

The output schema is designed so a future build_marker_manifest.py can emit a
compatible manifest.

Example
-------
python utils/build_mineru_manifest.py --base output/0883

python utils/build_mineru_manifest.py --base output/0883 --output output/0883/index

"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHUNK_CHARS = int(os.environ.get("MINERU_CHUNK_CHARS", "1800") or "1800")


def _sha256_8(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    return n


def _safe_rel_posix(path: Path) -> str:
    return path.as_posix()


_META_RE = re.compile(r"^\s*\{")
_DATE_RE = re.compile(r"(20\d{2})[-/\.]?(0[1-9]|1[0-2])[-/\.]?(0[1-9]|[12]\d|3[01])")


def _load_meta(meta_path: Path) -> Optional[Dict[str, Any]]:
    try:
        text = meta_path.read_text(encoding="utf-8")
    except Exception:
        return None
    if not _META_RE.search(text):
        return None
    try:
        obj = json.loads(text)
    except Exception:
        return None
    return obj if isinstance(obj, dict) else None


def _extract_meta_date(meta: Dict[str, Any]) -> Tuple[int, int, int]:
    # Try a few common metadata fields first; then scan all string values.
    candidates: List[Tuple[int, int, int]] = []
    keys = [
        "report_date",
        "filed_date",
        "filing_date",
        "publish_date",
        "announcement_date",
        "period_end",
        "fiscal_year_end",
        "date",
        "reportDate",
        "period",
        "end_date",
    ]

    def _scan_value(val: Any) -> None:
        if val is None:
            return
        if isinstance(val, (dict, list, tuple)):
            return
        s = str(val)
        m = _DATE_RE.search(s)
        if not m:
            return
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        candidates.append((y, mo, d))

    for k in keys:
        if k in meta:
            _scan_value(meta.get(k))

    if not candidates:
        for v in meta.values():
            _scan_value(v)

    if not candidates:
        return (0, 0, 0)
    return max(candidates)


def _find_primary_text(doc_dir: Path) -> Optional[Path]:
    # Prefer MinerU's consolidated markdown.
    preferred = [
        doc_dir / "artifacts" / "full.md",
        doc_dir / "document.md",
        doc_dir / "document.txt",
        doc_dir / "artifacts" / "full.txt",
    ]
    for p in preferred:
        if p.exists() and p.is_file() and p.stat().st_size > 0:
            return p

    # Fallback: any .md/.txt under artifacts.
    artifacts = doc_dir / "artifacts"
    if artifacts.exists() and artifacts.is_dir():
        for ext in (".md", ".txt"):
            cand = sorted([x for x in artifacts.rglob(f"*{ext}") if x.is_file()])
            for p in cand:
                if p.stat().st_size > 0:
                    return p

    return None


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


@dataclass(frozen=True)
class Paragraph:
    heading: str
    text: str


def _split_paragraphs_with_heading(text: str) -> List[Paragraph]:
    # Track a simple heading stack for markdown headings.
    heading_stack: List[str] = []

    def set_heading(level: int, title: str) -> None:
        nonlocal heading_stack
        if level <= 0:
            heading_stack = [title]
            return
        if len(heading_stack) >= level:
            heading_stack = heading_stack[: level - 1]
        while len(heading_stack) < level - 1:
            heading_stack.append("")
        heading_stack.append(title)

    def current_heading() -> str:
        items = [h.strip() for h in heading_stack if h and h.strip()]
        return " > ".join(items)

    lines = [ln.rstrip() for ln in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]

    paras: List[Paragraph] = []
    buf: List[str] = []

    def flush_buf() -> None:
        nonlocal buf
        if not buf:
            return
        para_text = "\n".join(buf).strip()
        buf = []
        if para_text:
            paras.append(Paragraph(heading=current_heading(), text=para_text))

    for ln in lines:
        m = _HEADING_RE.match(ln)
        if m:
            flush_buf()
            level = len(m.group(1))
            title = m.group(2).strip()
            set_heading(level, title)
            continue

        if not ln.strip():
            flush_buf()
            continue

        buf.append(ln)

    flush_buf()
    return paras


def _chunk_paragraphs(paras: List[Paragraph], max_chars: int) -> List[Dict[str, Any]]:
    chunks: List[Dict[str, Any]] = []
    cur: List[Paragraph] = []
    cur_len = 0

    def flush() -> None:
        nonlocal cur, cur_len
        if not cur:
            return
        chunk_text = "\n\n".join(p.text for p in cur).strip()
        if chunk_text:
            heading = cur[0].heading
            chunks.append(
                {
                    "index": len(chunks),
                    "heading": heading,
                    "text": chunk_text,
                    "char_len": len(chunk_text),
                }
            )
        cur = []
        cur_len = 0

    for p in paras:
        if not p.text:
            continue
        if len(p.text) > max_chars:
            # Hard split oversized paragraphs.
            start = 0
            while start < len(p.text):
                part = p.text[start : start + max_chars]
                if cur_len + len(part) + (2 if cur else 0) > max_chars:
                    flush()
                cur.append(Paragraph(heading=p.heading, text=part))
                cur_len += len(part)
                flush()
                start += max_chars
            continue

        projected = cur_len + len(p.text) + (2 if cur else 0)
        if projected > max_chars:
            flush()
        cur.append(p)
        cur_len += len(p.text)

    flush()
    return chunks


def _preview(text: str, limit: int = 180) -> str:
    s = re.sub(r"\s+", " ", text.strip())
    if len(s) <= limit:
        return s
    return s[: limit - 1] + "…"


def _iter_doc_meta_paths(base_dir: Path) -> List[Path]:
    # We treat each directory that contains a top-level meta.json as one document.
    out: List[Path] = []
    for p in base_dir.rglob("meta.json"):
        if not p.is_file():
            continue
        # Exclude nested meta.json that might appear in artifacts or other tools.
        if p.parent.name == "artifacts":
            continue
        out.append(p)
    return sorted(out)


def _parse_template_titles(template_path: Path) -> List[str]:
    if not template_path.exists():
        return []
    text = _read_text(template_path)
    titles = []
    for m in re.finditer(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE):
        t = m.group(1).strip()
        if t:
            titles.append(t)
    return titles


def build_toc_skeleton(*, out_path: Path) -> None:
    titles = _parse_template_titles(ROOT / "定性分析模板.md")
    if not titles:
        titles = ["公司介绍与沿革", "业务与商业模式", "财务与经营数据", "风险因素"]

    lines: List[str] = []
    lines.append("# toc\n")
    lines.append("\n")
    lines.append("<!--\n")
    lines.append("This is a lightweight retrieval config. Fill queries/must_include/top_k.\n")
    lines.append("A later build_chapter_pack.py can read this file to select Top-K chunks.\n")
    lines.append("-->\n")
    lines.append("\n")

    def default_queries_for(title: str) -> List[str]:
        # Very small Simplified -> Traditional mapping for common finance/report terms.
        # This avoids adding heavy dependencies while improving match rate on HK filings.
        s2t = {
            "简": "簡",
            "绍": "紹",
            "体": "體",
            "发": "發",
            "历": "歷",
            "财": "財",
            "务": "務",
            "风": "風",
            "险": "險",
            "们": "們",
            "东": "東",
            "营": "營",
            "业": "業",
            "净": "淨",
            "资": "資",
            "负": "負",
            "债": "債",
            "现": "現",
            "节": "節",
        }

        def expand_variants(items: List[str]) -> List[str]:
            out_items: List[str] = []
            for it in items:
                out_items.append(it)
                # naive char-wise replace
                trad = "".join(s2t.get(ch, ch) for ch in it)
                if trad != it:
                    out_items.append(trad)
            return out_items

        q: List[str] = []
        t = title
        q.append(t)

        if any(k in t for k in ["介绍", "沿革", "概况", "简介", "历史"]):
            q.extend(["公司简介", "公司概况", "发展历程", "沿革", "成立", "上市", "本公司", "我们"])
        if any(k in t for k in ["业务", "商业模式", "经营", "产品", "服务"]):
            q.extend(["业务", "商业模式", "主营", "产品", "服务", "客户", "市场", "竞争"])
        if any(k in t for k in ["财务", "经营数据", "业绩", "业务数据", "分部"]):
            q.extend(["财务", "收入", "毛利", "利润", "现金流", "资产负债", "分部", "主要财务数据"])
        if any(k in t for k in ["风险"]):
            q.extend(["风险", "风险因素", "不确定", "可能", "监管", "合规"])
        if any(k in t for k in ["治理", "管理层", "董事会", "薪酬"]):
            q.extend(["董事会", "管理层", "公司治理", "薪酬", "高管"])
        if any(k in t for k in ["股东", "回报", "资本结构", "分红", "回购", "债务", "融资"]):
            q.extend(["股息", "分红", "回购", "债务", "融资", "资本"])

        q = expand_variants(q)

        # De-dup while preserving order
        seen = set()
        out: List[str] = []
        for item in q:
            item = item.strip()
            if not item or item in seen:
                continue
            seen.add(item)
            out.append(item)
        return out

    for title in titles:
        queries = ", ".join(default_queries_for(title))
        lines.append(f"## {title}\n")
        lines.append(f"- queries: {queries}\n")
        lines.append("- must_include: \n")
        lines.append("- top_k: 40\n")
        lines.append("- neighbor_window: 1\n")
        lines.append("\n")

    _write_text(out_path, "".join(lines))


def build_manifest(
    *,
    base_dir: Path,
    out_dir: Path,
    chunk_chars: int,
    include_doc_records: bool,
    max_docs: Optional[int],
) -> Tuple[int, int]:
    meta_paths = _iter_doc_meta_paths(base_dir)
    meta_with_date: List[Tuple[Path, Tuple[int, int, int], str]] = []
    for p in meta_paths:
        meta = _load_meta(p) or {}
        date_key = _extract_meta_date(meta)
        meta_with_date.append((p, date_key, p.parent.name))
    meta_with_date.sort(key=lambda x: (x[1], x[2]), reverse=True)
    meta_paths = [p for (p, _, _) in meta_with_date]
    if max_docs is not None:
        meta_paths = meta_paths[: max_docs]

    manifest_jsonl = out_dir / "manifest.jsonl"
    manifest_tsv = out_dir / "manifest.tsv"

    rows_jsonl: List[Dict[str, Any]] = []
    rows_tsv: List[Dict[str, Any]] = []

    doc_count = 0
    chunk_count = 0

    for meta_path in meta_paths:
        meta = _load_meta(meta_path) or {}
        state = str(meta.get("state") or "").lower()
        if state and state != "done":
            continue

        doc_dir = meta_path.parent
        doc_rel_dir = doc_dir.relative_to(base_dir)
        doc_id = _safe_rel_posix(doc_rel_dir)

        source_pdf = str(meta.get("input_pdf") or "")
        source_pdf_name = Path(source_pdf).name if source_pdf else ""

        text_path = _find_primary_text(doc_dir)
        if not text_path:
            continue

        text_rel_path = text_path.relative_to(base_dir)
        text = _read_text(text_path)
        paras = _split_paragraphs_with_heading(text)
        chunks = _chunk_paragraphs(paras, max_chars=chunk_chars)

        if include_doc_records:
            rows_jsonl.append(
                {
                    "kind": "mineru_doc",
                    "doc_id": doc_id,
                    "doc_rel_dir": _safe_rel_posix(doc_rel_dir),
                    "source_pdf": source_pdf,
                    "source_pdf_name": source_pdf_name,
                    "text_rel_path": _safe_rel_posix(text_rel_path),
                    "chunk_chars": chunk_chars,
                    "chunk_count": len(chunks),
                }
            )

        doc_count += 1

        for c in chunks:
            chunk_index = int(c["index"])
            chunk_id = f"{doc_id}#{chunk_index:05d}"
            heading = str(c.get("heading") or "")
            chunk_text = str(c.get("text") or "")
            preview = _preview(chunk_text)

            row = {
                "kind": "mineru_chunk",
                "chunk_id": chunk_id,
                "doc_id": doc_id,
                "chunk_index": chunk_index,
                "heading": heading,
                "char_len": int(c.get("char_len") or len(chunk_text)),
                "preview": preview,
                "text": chunk_text,
                "source_pdf": source_pdf,
                "source_pdf_name": source_pdf_name,
                "doc_rel_dir": _safe_rel_posix(doc_rel_dir),
                "text_rel_path": _safe_rel_posix(text_rel_path),
            }
            rows_jsonl.append(row)

            rows_tsv.append(
                {
                    "chunk_id": chunk_id,
                    "doc_id": doc_id,
                    "chunk_index": chunk_index,
                    "heading": heading,
                    "char_len": int(row["char_len"]),
                    "source_pdf_name": source_pdf_name,
                    "doc_rel_dir": row["doc_rel_dir"],
                    "text_rel_path": row["text_rel_path"],
                    "preview": preview,
                }
            )
            chunk_count += 1

    _write_jsonl(manifest_jsonl, rows_jsonl)

    manifest_tsv.parent.mkdir(parents=True, exist_ok=True)
    with manifest_tsv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "chunk_id",
                "doc_id",
                "chunk_index",
                "heading",
                "char_len",
                "source_pdf_name",
                "doc_rel_dir",
                "text_rel_path",
                "preview",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        for r in rows_tsv:
            writer.writerow(r)

    return doc_count, chunk_count


def build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Build manifest.jsonl/tsv from MinerU output")
    ap.add_argument("--base", required=True, type=str, help="MinerU output root (e.g. output/0883)")
    ap.add_argument(
        "--output",
        type=str,
        default="",
        help="Directory to write manifest files (default: <base>/index)",
    )
    ap.add_argument(
        "--chunk-chars",
        type=int,
        default=DEFAULT_CHUNK_CHARS,
        help=f"Chunk size in chars (default: {DEFAULT_CHUNK_CHARS})",
    )
    ap.add_argument(
        "--include-doc-records",
        action="store_true",
        help="Include doc-level rows (kind=mineru_doc) in manifest.jsonl",
    )
    ap.add_argument(
        "--max-docs",
        type=int,
        default=0,
        help="Limit number of docs processed (0 = no limit)",
    )
    ap.add_argument(
        "--write-toc",
        action="store_true",
        default=True,
        help="Write a toc.md skeleton (based on 定性分析模板.md) into output dir if missing (default: true)",
    )
    ap.add_argument(
        "--no-write-toc",
        dest="write_toc",
        action="store_false",
        help="Do not create toc.md",
    )
    return ap


def main(argv: Optional[List[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)

    base_dir = Path(args.base).expanduser().resolve()
    if not base_dir.exists() or not base_dir.is_dir():
        raise SystemExit(f"--base is not a directory: {base_dir}")

    out_dir = Path(args.output).expanduser().resolve() if args.output else (base_dir / "index")
    out_dir.mkdir(parents=True, exist_ok=True)

    max_docs = int(args.max_docs)
    if max_docs <= 0:
        max_docs = None

    doc_count, chunk_count = build_manifest(
        base_dir=base_dir,
        out_dir=out_dir,
        chunk_chars=int(args.chunk_chars),
        include_doc_records=bool(args.include_doc_records),
        max_docs=max_docs,
    )

    if args.write_toc:
        toc_path = out_dir / "toc.md"
        if not toc_path.exists():
            build_toc_skeleton(out_path=toc_path)

    print(f"Wrote: {out_dir / 'manifest.jsonl'}")
    print(f"Wrote: {out_dir / 'manifest.tsv'}")
    if args.write_toc:
        print(f"toc.md: {(out_dir / 'toc.md')}")
    print(f"Docs indexed: {doc_count} | Chunks: {chunk_count} | chunk_chars={args.chunk_chars}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
