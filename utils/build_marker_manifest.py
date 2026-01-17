#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Build a searchable manifest from Marker-extracted output.

Why
----
Marker output is JSON-heavy and not optimized for chapter-level retrieval.
This script converts Marker folders (e.g. output/0300/<doc>/) into a
manifest.jsonl/tsv + toc.md that are compatible with build_chapter_pack.py.

Output schema mirrors build_mineru_manifest so run_qual_report_codex can
use the same Materials packs logic.

Example
-------
python utils/build_marker_manifest.py --base output/0300
python utils/build_marker_manifest.py --base output/0300 --output output/0300/index

"""

from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHUNK_CHARS = int(os.environ.get("MARKER_CHUNK_CHARS", "2200") or "2200")


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


_DATE_RE = re.compile(r"(20\d{2})[-/\.]?(0[1-9]|1[0-2])[-/\.]?(0[1-9]|[12]\d|3[01])")


def _extract_name_date(name: str) -> Tuple[int, int, int]:
    """Best-effort date extraction from folder name (YYYY + quarter/period)."""
    year = 0
    period = 0
    m = re.search(r"(20\d{2})", name)
    if m:
        year = int(m.group(1))
    mq = re.search(r"(?i)Q([1-4])", name)
    if mq:
        period = int(mq.group(1))
    elif "一季度" in name:
        period = 1
    elif "中报" in name or "半年" in name or "二季度" in name:
        period = 2
    elif "三季度" in name:
        period = 3
    elif "年报" in name or "年度" in name or "四季度" in name:
        period = 4
    return (year, period, 0)


def _strip_html_tags(text: str) -> str:
    # Remove tags and unescape entities.
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _preview(text: str, limit: int = 180) -> str:
    s = re.sub(r"\s+", " ", text.strip())
    if len(s) <= limit:
        return s
    return s[: limit - 1] + "…"


@dataclass(frozen=True)
class TocItem:
    title: str
    page_id: Optional[int]


def _load_meta(meta_path: Path) -> Optional[Dict[str, Any]]:
    try:
        text = meta_path.read_text(encoding="utf-8")
    except Exception:
        return None
    if not text.strip().startswith("{"):
        return None
    try:
        obj = json.loads(text)
    except Exception:
        return None
    return obj if isinstance(obj, dict) else None


def _iter_marker_docs(base_dir: Path) -> List[Tuple[Path, Path]]:
    """Return list of (doc_dir, meta_path) sorted by date/name desc."""
    docs: List[Tuple[Path, Path]] = []
    for d in base_dir.iterdir():
        if not d.is_dir():
            continue
        meta = d / f"{d.name}_meta.json"
        main = d / f"{d.name}.json"
        if meta.exists() and main.exists():
            docs.append((d, meta))
    docs.sort(key=lambda x: (_extract_name_date(x[0].name), x[0].name), reverse=True)
    return docs


def _parse_toc(meta: Dict[str, Any]) -> List[TocItem]:
    toc = meta.get("table_of_contents") if isinstance(meta, dict) else None
    items: List[TocItem] = []
    if isinstance(toc, list):
        for it in toc:
            if not isinstance(it, dict):
                continue
            title = str(it.get("title") or "").strip()
            if not title:
                continue
            page_id = it.get("page_id")
            try:
                page_id_int = int(page_id) if page_id is not None else None
            except Exception:
                page_id_int = None
            items.append(TocItem(title=title, page_id=page_id_int))
    return items


def _load_blocks(main_json: Path) -> List[Dict[str, Any]]:
    try:
        with main_json.open("r", encoding="utf-8", errors="replace") as f:
            obj = json.load(f)
    except Exception:
        return []
    blocks = obj.get("blocks") if isinstance(obj, dict) else None
    return blocks if isinstance(blocks, list) else []


def _collect_page_text(blocks: List[Dict[str, Any]]) -> Tuple[List[int], Dict[int, List[str]]]:
    pages: Dict[int, List[str]] = {}
    for b in blocks:
        if not isinstance(b, dict):
            continue
        html_text = str(b.get("html") or "")
        if not html_text.strip():
            continue
        text = _strip_html_tags(html_text)
        if not text:
            continue
        page_val = b.get("page")
        try:
            page = int(page_val)
        except Exception:
            continue
        pages.setdefault(page, []).append(text)
    page_list = sorted(pages.keys())
    return page_list, pages


def _map_toc_pages(toc_items: List[TocItem], pages: List[int]) -> List[Tuple[int, str]]:
    if not pages or not toc_items:
        return []
    mapped: List[Tuple[int, str]] = []
    for it in toc_items:
        if it.page_id is None:
            continue
        idx = it.page_id
        if idx < 0:
            continue
        if idx >= len(pages):
            actual_page = pages[-1]
        else:
            actual_page = pages[idx]
        mapped.append((actual_page, it.title))
    mapped.sort(key=lambda x: x[0])
    return mapped


def _iter_page_chunks(
    *,
    pages: List[int],
    page_texts: Dict[int, List[str]],
    toc_mapped: List[Tuple[int, str]],
    fallback_heading: str,
    max_chars: int,
) -> List[Dict[str, Any]]:
    chunks: List[Dict[str, Any]] = []
    cur_heading = ""
    cur_texts: List[str] = []
    cur_len = 0

    toc_idx = 0
    current_heading = fallback_heading

    def flush() -> None:
        nonlocal cur_heading, cur_texts, cur_len
        if not cur_texts:
            return
        chunk_text = "\n\n".join(cur_texts).strip()
        if chunk_text:
            chunks.append(
                {
                    "index": len(chunks),
                    "heading": cur_heading or fallback_heading,
                    "text": chunk_text,
                    "char_len": len(chunk_text),
                }
            )
        cur_heading = ""
        cur_texts = []
        cur_len = 0

    for page in pages:
        while toc_idx < len(toc_mapped) and toc_mapped[toc_idx][0] <= page:
            current_heading = toc_mapped[toc_idx][1] or fallback_heading
            toc_idx += 1

        text = "\n".join(page_texts.get(page, [])).strip()
        if not text:
            continue

        if cur_heading and current_heading != cur_heading:
            flush()

        if not cur_heading:
            cur_heading = current_heading or fallback_heading

        if max_chars > 0 and cur_len + len(text) > max_chars and cur_texts:
            flush()
            cur_heading = current_heading or fallback_heading

        cur_texts.append(text)
        cur_len += len(text)

    flush()
    return chunks


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
        if any(k in t for k in ["治理", "管理层", "董事会", "薪酬", "激励"]):
            q.extend(["董事会", "管理层", "公司治理", "薪酬", "高管"])
        if any(k in t for k in ["股东", "回报", "资本结构", "分红", "回购", "债务", "融资", "股权"]):
            q.extend(["股东", "股息", "分红", "回购", "债务", "融资", "股权"])

        return expand_variants(q)

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
    docs = _iter_marker_docs(base_dir)
    if max_docs is not None:
        docs = docs[: max_docs]

    manifest_jsonl = out_dir / "manifest.jsonl"
    manifest_tsv = out_dir / "manifest.tsv"

    rows_jsonl: List[Dict[str, Any]] = []
    rows_tsv: List[Dict[str, Any]] = []

    doc_count = 0
    chunk_count = 0

    for doc_dir, meta_path in docs:
        meta = _load_meta(meta_path) or {}
        toc_items = _parse_toc(meta)

        main_json = doc_dir / f"{doc_dir.name}.json"
        blocks = _load_blocks(main_json)
        pages, page_texts = _collect_page_text(blocks)
        if not pages:
            continue

        toc_mapped = _map_toc_pages(toc_items, pages)
        fallback_heading = toc_items[0].title if toc_items else doc_dir.name

        chunks = _iter_page_chunks(
            pages=pages,
            page_texts=page_texts,
            toc_mapped=toc_mapped,
            fallback_heading=fallback_heading,
            max_chars=chunk_chars,
        )

        doc_rel_dir = doc_dir.relative_to(base_dir)
        doc_id = _safe_rel_posix(doc_rel_dir)
        text_rel_path = main_json.relative_to(base_dir)

        source_html = doc_dir / f"{doc_dir.name}.html"
        source_html_rel = source_html.relative_to(base_dir) if source_html.exists() else None
        source_pdf = _safe_rel_posix(source_html_rel) if source_html_rel else ""
        source_pdf_name = source_html.name if source_html.exists() else ""

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
                    "source_type": "marker",
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
                "source_type": "marker",
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
    ap = argparse.ArgumentParser(description="Build manifest.jsonl/tsv from Marker output")
    ap.add_argument("--base", required=True, type=str, help="Marker output root (e.g. output/0300)")
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
