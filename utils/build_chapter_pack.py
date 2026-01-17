#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Build a per-chapter materials pack (bundle.md) from a manifest + toc.

This is the writing-side counterpart of `build_mineru_manifest.py`.

Inputs
------
- index_dir/manifest.jsonl : rows emitted by build_mineru_manifest (kind=mineru_chunk)
- index_dir/toc.md         : lightweight retrieval config, chapter -> queries/top_k

Outputs
-------
- <output>/bundle.md       : concatenated chunks for one chapter
- <output>/selected.jsonl  : selected chunk metadata + score

The selection intentionally uses simple lexical matching (no external deps),
so it's deterministic and easy to debug.

Example
-------
python utils/build_chapter_pack.py \
  --index-dir output/0883/index \
  --chapter "公司介绍与沿革" \
  --output Reports/0883/_materials_packs/公司介绍与沿革

"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


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


def _sanitize_filename(name: str) -> str:
    replacements = {
        "/": "／",
        "\\": "＼",
        ":": "：",
        "*": "＊",
        "?": "？",
        '"': "＂",
        "<": "＜",
        ">": "＞",
        "|": "｜",
    }
    out = "".join(replacements.get(ch, ch) for ch in name)
    out = out.strip().strip(".")
    return out or "untitled"


def _expand_s2t_variants(items: List[str]) -> List[str]:
    # Minimal Simplified -> Traditional mapping for common report terms.
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

    out: List[str] = []
    for it in items:
        it = it.strip()
        if not it:
            continue
        out.append(it)
        trad = "".join(s2t.get(ch, ch) for ch in it)
        if trad != it:
            out.append(trad)
    # De-dup while preserving order
    seen = set()
    uniq: List[str] = []
    for it in out:
        if it in seen:
            continue
        seen.add(it)
        uniq.append(it)
    return uniq


def default_queries_for_chapter(title: str) -> List[str]:
    q: List[str] = []
    t = title

    # Very generic anchors (high recall)
    q.extend(["本公司", "我們", "公司", "集团", "集團"])

    if any(k in t for k in ["介绍", "沿革", "概况", "简介", "历史"]):
        q.extend(["公司简介", "公司概况", "概覽", "公司簡介", "發展歷程", "发展历程", "沿革", "成立", "上市"])
    if any(k in t for k in ["业务", "商业模式", "经营", "产品", "服务"]):
        q.extend(["业务", "商業模式", "商业模式", "主营", "產品", "产品", "服务", "服務", "客户", "客戶", "市场", "市場", "竞争", "競爭"])
    if any(k in t for k in ["财务", "经营数据", "业绩", "业务数据", "分部"]):
        q.extend(["财务", "財務", "收入", "毛利", "利润", "利潤", "现金流", "現金流", "资产负债", "資產負債", "分部"])
    if any(k in t for k in ["风险"]):
        q.extend(["风险", "風險", "风险因素", "風險因素", "不确定", "不確定", "可能", "监管", "監管", "合规", "合規"])
    if any(k in t for k in ["治理", "管理层", "董事会", "薪酬", "激励"]):
        q.extend(["董事会", "董事會", "管理层", "管理層", "公司治理", "薪酬", "高管"])
    if any(k in t for k in ["股东", "回报", "资本结构", "分红", "回购", "债务", "融资", "股权"]):
        q.extend(["股东", "股東", "股息", "分红", "分紅", "回购", "回購", "债务", "債務", "融资", "融資", "股权", "股權"])

    # Also include the title itself.
    q.append(t)
    return _expand_s2t_variants(q)


@dataclass(frozen=True)
class TocEntry:
    chapter: str
    queries: List[str]
    must_include: List[str]
    top_k: int
    neighbor_window: int


_TOC_CHAPTER_RE = re.compile(r"^##\s+(.+?)\s*$")
_TOC_FIELD_RE = re.compile(r"^-\s*(\w+)\s*:\s*(.*?)\s*$")


def parse_toc(toc_text: str) -> Dict[str, TocEntry]:
    current: Optional[str] = None
    buf: Dict[str, Dict[str, str]] = {}

    for raw_line in toc_text.splitlines():
        line = raw_line.rstrip()
        m = _TOC_CHAPTER_RE.match(line)
        if m:
            current = m.group(1).strip()
            buf.setdefault(current, {})
            continue
        m2 = _TOC_FIELD_RE.match(line)
        if m2 and current:
            key = m2.group(1).strip()
            val = m2.group(2).strip()
            buf[current][key] = val

    out: Dict[str, TocEntry] = {}
    for chapter, fields in buf.items():
        queries = [x.strip() for x in fields.get("queries", "").split(",") if x.strip()]
        must = [x.strip() for x in fields.get("must_include", "").split(",") if x.strip()]

        def as_int(name: str, default: int) -> int:
            raw = fields.get(name, "").strip()
            if not raw:
                return default
            try:
                return int(raw)
            except Exception:
                return default

        top_k = as_int("top_k", 40)
        neighbor = as_int("neighbor_window", 1)

        out[chapter] = TocEntry(
            chapter=chapter,
            queries=queries,
            must_include=must,
            top_k=top_k,
            neighbor_window=neighbor,
        )

    return out


def _score_text(haystack: str, query: str) -> int:
    if not query:
        return 0
    return haystack.count(query)


def _combined_haystack(row: Dict[str, Any]) -> str:
    parts = [
        str(row.get("heading") or ""),
        str(row.get("preview") or ""),
        str(row.get("text") or ""),
        str(row.get("source_pdf_name") or ""),
        str(row.get("doc_id") or ""),
    ]
    return "\n".join(p for p in parts if p)


def _load_manifest_rows(manifest_path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with manifest_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if not isinstance(obj, dict):
                continue
            if obj.get("kind") != "mineru_chunk":
                continue
            rows.append(obj)
    return rows


def select_chunks(
    *,
    rows: List[Dict[str, Any]],
    entry: TocEntry,
    top_k_override: Optional[int],
    neighbor_window_override: Optional[int],
) -> List[Dict[str, Any]]:
    queries = entry.queries or default_queries_for_chapter(entry.chapter)
    top_k = top_k_override if top_k_override is not None else entry.top_k
    neighbor_window = neighbor_window_override if neighbor_window_override is not None else entry.neighbor_window

    scored: List[Tuple[int, Dict[str, Any]]] = []
    for row in rows:
        hay = _combined_haystack(row)
        score = 0
        for q in queries:
            if not q:
                continue
            # Heading matches matter more.
            score += 3 * _score_text(str(row.get("heading") or ""), q)
            score += 1 * _score_text(hay, q)

        # must_include as soft boost (not hard filter)
        for m in entry.must_include:
            if m and m in hay:
                score += 5

        if score > 0:
            scored.append((score, row))

    scored.sort(key=lambda t: (-t[0], str(t[1].get("chunk_id") or "")))
    picked = [r for _, r in scored[: max(1, top_k)]]

    if neighbor_window <= 0:
        return picked

    # Neighbor expansion based on (doc_id, chunk_index)
    by_doc: Dict[str, Dict[int, Dict[str, Any]]] = {}
    for row in rows:
        doc_id = str(row.get("doc_id") or "")
        try:
            idx = int(row.get("chunk_index"))
        except Exception:
            continue
        by_doc.setdefault(doc_id, {})[idx] = row

    expanded: Dict[str, Dict[str, Any]] = {str(r.get("chunk_id")): r for r in picked}
    for r in picked:
        doc_id = str(r.get("doc_id") or "")
        try:
            idx = int(r.get("chunk_index"))
        except Exception:
            continue
        for d in range(-neighbor_window, neighbor_window + 1):
            if d == 0:
                continue
            nb = by_doc.get(doc_id, {}).get(idx + d)
            if nb is None:
                continue
            expanded[str(nb.get("chunk_id"))] = nb

    # Keep stable ordering by doc_id then chunk_index.
    def sort_key(row: Dict[str, Any]) -> Tuple[str, int]:
        doc_id = str(row.get("doc_id") or "")
        try:
            idx = int(row.get("chunk_index"))
        except Exception:
            idx = 0
        return (doc_id, idx)

    return sorted(expanded.values(), key=sort_key)


def build_bundle(
    *,
    selected: List[Dict[str, Any]],
    chapter: str,
    max_total_chars: int,
) -> str:
    total = 0
    parts: List[str] = []
    parts.append(f"# Materials Pack\n\n")
    parts.append(f"Chapter: {chapter}\n\n")

    for row in selected:
        text = str(row.get("text") or "").strip()
        if not text:
            continue
        chunk_id = str(row.get("chunk_id") or "")
        source_pdf = str(row.get("source_pdf_name") or "")
        heading = str(row.get("heading") or "")

        block = []
        block.append("---\n")
        block.append(f"chunk_id: {chunk_id}\n")
        if source_pdf:
            block.append(f"source: {source_pdf}\n")
        if heading:
            block.append(f"heading: {heading}\n")
        block.append("\n")
        block.append(text)
        block.append("\n\n")
        block_text = "".join(block)

        if total + len(block_text) > max_total_chars:
            break
        parts.append(block_text)
        total += len(block_text)

    return "".join(parts).rstrip() + "\n"


def build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Build per-chapter bundle.md from manifest.jsonl + toc.md")
    ap.add_argument("--index-dir", required=True, help="Directory containing manifest.jsonl and toc.md")
    ap.add_argument("--chapter", required=True, help="Chapter title (must match a toc.md '## <title>')")
    ap.add_argument("--output", required=True, help="Output directory for this chapter pack")
    ap.add_argument("--top-k", type=int, default=0, help="Override toc top_k (0 = use toc)")
    ap.add_argument("--neighbor-window", type=int, default=-1, help="Override toc neighbor_window (-1 = use toc)")
    ap.add_argument(
        "--max-total-chars",
        type=int,
        default=220_000,
        help="Max total chars in bundle.md (default: 220000)",
    )
    return ap


def main(argv: Optional[List[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)

    index_dir = Path(args.index_dir).expanduser().resolve()
    manifest_path = index_dir / "manifest.jsonl"
    toc_path = index_dir / "toc.md"
    if not manifest_path.exists():
        raise SystemExit(f"Missing manifest.jsonl: {manifest_path}")
    if not toc_path.exists():
        raise SystemExit(f"Missing toc.md: {toc_path}")

    toc_map = parse_toc(_read_text(toc_path))
    if args.chapter not in toc_map:
        known = "\n".join([f"- {k}" for k in sorted(toc_map.keys())])
        raise SystemExit(f"Unknown chapter in toc.md: {args.chapter}\nKnown:\n{known}")

    entry = toc_map[args.chapter]
    rows = _load_manifest_rows(manifest_path)

    top_k_override = int(args.top_k) if int(args.top_k) > 0 else None
    neighbor_override = int(args.neighbor_window) if int(args.neighbor_window) >= 0 else None

    selected = select_chunks(
        rows=rows,
        entry=entry,
        top_k_override=top_k_override,
        neighbor_window_override=neighbor_override,
    )

    if not selected:
        print(
            "WARNING: selected 0 chunks. Fill queries in toc.md for this chapter to improve retrieval.",
        )

    out_dir = Path(args.output).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    bundle = build_bundle(selected=selected, chapter=entry.chapter, max_total_chars=int(args.max_total_chars))
    _write_text(out_dir / "bundle.md", bundle)

    # Store selected rows (without full text to keep it smaller)
    selected_rows: List[Dict[str, Any]] = []
    for r in selected:
        selected_rows.append(
            {
                "chunk_id": r.get("chunk_id"),
                "doc_id": r.get("doc_id"),
                "chunk_index": r.get("chunk_index"),
                "heading": r.get("heading"),
                "char_len": r.get("char_len"),
                "preview": r.get("preview"),
                "source_pdf_name": r.get("source_pdf_name"),
            }
        )
    _write_jsonl(out_dir / "selected.jsonl", selected_rows)

    print(f"Wrote: {out_dir / 'bundle.md'}")
    print(f"Wrote: {out_dir / 'selected.jsonl'}")
    print(f"Selected chunks: {len(selected)} | top_k={top_k_override or entry.top_k} | neighbor_window={neighbor_override if neighbor_override is not None else entry.neighbor_window}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
