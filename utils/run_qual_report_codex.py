#!/usr/bin/env python3
"""Automate the GUIDE.md qualitative-report workflow using Codex CLI.

Key ideas (v1)
-------------
- `GUIDE.md` is the single source of truth for the protocol.
- `python utils/sync_codex_from_guide.py` keeps `AGENTS.md` in sync.
- This driver script:
  - Parses `定性分析模板.md` into chapter skeletons.
    - Calls `codex exec` from the repo root (where `AGENTS.md` lives) to generate each chapter Markdown.
    - Audits each chapter via `#ASK` JSON-only (facts & tone 2 + 2.1–2.6).
  - Retries chapter generation up to N times when the audit fails.
  - Assembles a full report and generates a de-duplicated Sources chapter.

Notes
-----
- This script deliberately keeps Codex in read-only sandbox mode.
- Materials for ONE company should live under `--base`.
    - If `--base` is omitted, the script runs without local materials and relies on SEC/EDGAR retrieval (when applicable).

Example
-------
python utils/run_qual_report_codex.py \
  --base filings/V \
  --company "Visa公司" \
  --only-chapters "公司介绍与沿革" \
  --max-attempts 3
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import textwrap
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Iterable, List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "定性分析模板.md"
PROMPTS_DIR = ROOT / "Codex" / "prompts"
IDENTITY_INDEX_EVIDENCE_MAX_ITEMS = 12
IDENTITY_INDEX_EVIDENCE_MAX_PREVIEW_CHARS = 160


@dataclass(frozen=True)
class Chapter:
    title: str
    skeleton: str


@dataclass(frozen=True)
class CodexProfile:
    name: str
    model: str
    reasoning_effort: str


def resolve_codex_profile(name: str) -> CodexProfile:
    # NOTE:
    # - On this environment/account, `model_reasoning_effort="minimal"` is rejected for gpt-5.2.
    # - Supported values observed: none | low | medium | high | xhigh.
    if name == "fast":
        return CodexProfile(name="fast", model="gpt-5.2", reasoning_effort="low")
    if name == "balanced":
        return CodexProfile(name="balanced", model="gpt-5.2", reasoning_effort="medium")
    if name == "high":
        return CodexProfile(name="high", model="gpt-5.2", reasoning_effort="high")
    if name == "deep":
        return CodexProfile(name="deep", model="gpt-5.2", reasoning_effort="xhigh")
    raise ValueError(f"Unknown profile: {name}")


def validate_project_layout(*, required_prompt_paths: List[Path]) -> None:
    if not PROMPTS_DIR.exists() or not PROMPTS_DIR.is_dir():
        raise SystemExit(f"Missing prompts directory: {PROMPTS_DIR}. Run: python utils/sync_codex_from_guide.py")

    agents_path = ROOT / "AGENTS.md"
    if not agents_path.exists() or not agents_path.is_file():
        raise SystemExit(
            f"Missing AGENTS.md at repo root: {agents_path}. Run: python utils/sync_codex_from_guide.py"
        )
    try:
        if agents_path.stat().st_size <= 0:
            raise SystemExit(f"AGENTS.md is empty: {agents_path}")
    except OSError as e:
        raise SystemExit(f"Cannot stat AGENTS.md: {agents_path} ({e})")

    for p in required_prompt_paths:
        if not p.exists() or not p.is_file():
            raise SystemExit(f"Missing required prompt file: {p}")


_AGENTS_SENTINEL_RE = re.compile(r"^AGENTS_SENTINEL:\s*(?P<token>\S+)\s*$", re.MULTILINE)


def read_agents_sentinel() -> str:
    # AGENTS.md is intentionally at repo root so Codex can be run without --cd.
    agents_path = ROOT / "AGENTS.md"
    text = _read_text(agents_path)
    match = _AGENTS_SENTINEL_RE.search(text)
    if not match:
        raise SystemExit(
            f"AGENTS.md missing sentinel line. Re-run: python utils/sync_codex_from_guide.py | path={agents_path}"
        )
    token = match.group("token").strip()
    if not token:
        raise SystemExit(f"AGENTS.md sentinel token is empty: {agents_path}")
    return token


def validate_agents_self_check_output(text: str, *, expected_sentinel: str) -> None:
    out = text.strip()

    if out == "SENTINEL_NOT_FOUND":
        raise SystemExit("agents_self_check failed: SENTINEL_NOT_FOUND")

    # Require the model to print the full sentinel line. This is robust against
    # formatting drift and effectively proves AGENTS.md was loaded.
    match = re.fullmatch(r"AGENTS_SENTINEL:\s*(\S+)\s*", out)
    if not match:
        snippet = out.replace("\n", " ")
        if len(snippet) > 300:
            snippet = snippet[:300] + "…"
        raise SystemExit(
            "agents_self_check returned unexpected output (expected a single line: "
            "'AGENTS_SENTINEL: <token>' or 'SENTINEL_NOT_FOUND') | "
            f"snippet={snippet}"
        )

    got = match.group(1).strip()
    if got != expected_sentinel:
        raise SystemExit(f"agents_self_check failed: sentinel mismatch | expected={expected_sentinel} got={got}")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _log_step(message: str) -> None:
    # Intentionally simple and always-on progress logs.
    # Keep these stable so users can grep them.
    ts = datetime.now().strftime("%H:%M:%S")
    if message.lstrip().startswith("Step "):
        print("")
    print(f"[{ts}] {message}")


def _sanitize_filename(name: str) -> str:
    # Keep it visually close to the chapter title, but filesystem-safe.
    # macOS forbids '/'. Also avoid ':' for portability.
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
    if not out:
        out = "untitled"
    return out


_CHAPTER_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)

_HTML_COMMENT_RE = re.compile(r"<!--([\s\S]*?)-->")
_WRITE_BLOCKED_RE = re.compile(
    r"缺口清单.*?未满足[“\"']?\s*最小\s*输入\s*条件[”\"']?.*?#WRITE",
    re.IGNORECASE | re.DOTALL,
)
AUDIT_CLASS_WRITE_BLOCKED = "write_blocked"


def strip_html_comments(markdown: str) -> str:
    return _HTML_COMMENT_RE.sub("", markdown)


def is_write_blocked(markdown: str) -> bool:
    return bool(_WRITE_BLOCKED_RE.search(markdown))


def extract_template_disclaimers(template_text: str) -> tuple[str, str]:
    """Extract (preamble, footer) disclaimer blocks from the template.

    - Preamble: everything before the first '##' chapter heading (minus the first '# ...' title line).
    - Footer: from the last '**免责声明**' heading to end of file.
    """
    matches = list(_CHAPTER_HEADING_RE.finditer(template_text))
    if not matches:
        return "", ""

    pre_raw = template_text[: matches[0].start()].strip() + "\n"
    pre_lines = pre_raw.splitlines()
    if pre_lines and pre_lines[0].lstrip().startswith("#"):
        pre_lines = pre_lines[1:]
    pre = "\n".join(pre_lines).strip() + "\n"
    pre = strip_html_comments(pre).strip() + "\n\n" if pre.strip() else ""

    footer_match_iter = list(re.finditer(r"^\*\*免责声明\*\*\s*$", template_text, flags=re.MULTILINE))
    if footer_match_iter:
        start = footer_match_iter[-1].start()
        footer = template_text[start:].strip() + "\n"
        footer = strip_html_comments(footer).strip() + "\n" if footer.strip() else ""
    else:
        footer = ""

    return pre, footer


def fill_disclaimer_placeholders(text: str, *, company: str, ticker: str) -> str:
    out = text
    out = out.replace("[公司名称]", company)
    out = out.replace("(TICKER)", f"({ticker})")
    out = out.replace(" TICKER ", f" {ticker} ")
    return out


def parse_template_chapters(template_text: str) -> List[Chapter]:
    matches = list(_CHAPTER_HEADING_RE.finditer(template_text))
    if not matches:
        raise SystemExit("No chapters found in template: expected '## <章节标题>' headings.")

    chapters: List[Chapter] = []
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(template_text)
        chunk = template_text[start:end].rstrip() + "\n"
        title = match.group(1).strip()
        chapters.append(Chapter(title=title, skeleton=chunk))
    return chapters


_SKIP_NON_MIDDLE_CHAPTERS = {"投资要点概览", "来源清单"}


def normalize_only_chapters_arg(values: List[str]) -> List[str]:
    # Accept repeatable args and comma-separated lists.
    out: List[str] = []
    for v in values:
        parts = [p.strip() for p in v.split(",")]
        out.extend([p for p in parts if p])
    # De-dup while preserving order.
    seen = set()
    uniq: List[str] = []
    for c in out:
        if c not in seen:
            seen.add(c)
            uniq.append(c)
    return uniq


def select_chapters(all_chapters: List[Chapter], only_titles: Optional[List[str]]) -> List[Chapter]:
    if not only_titles:
        return all_chapters

    index = {c.title: c for c in all_chapters}
    missing = [t for t in only_titles if t not in index]
    if missing:
        available = "\n".join([f"- {c.title}" for c in all_chapters])
        raise SystemExit(
            "Unknown chapter title(s):\n"
            + "\n".join([f"- {m}" for m in missing])
            + "\n\nAvailable chapters:\n"
            + available
        )

    return [index[t] for t in only_titles]


def build_materials_manifest(base_dir: Path, max_items: int = 6) -> str:
    if not base_dir.exists():
        raise SystemExit(f"--base does not exist: {base_dir}")

    # User-facing manifest focus: "main" content-like files.
    # Keep this intentionally small and readable.
    visible_exts = {
        ".json",
        ".jsonl",
        ".htm",
        ".html",
        ".pdf",
        ".md",
        ".yml",
        ".yaml",
    }

    def _is_manifest_excluded(path: Path) -> bool:
        if path.name in {".DS_Store", "Thumbs.db"}:
            return True
        return False

    def _is_manifest_visible(path: Path) -> bool:
        if _is_manifest_excluded(path):
            return False
        return path.suffix.lower() in visible_exts

    all_files: List[Path] = [p for p in base_dir.rglob("*") if p.is_file()]
    excluded_junk_count = sum(1 for p in all_files if _is_manifest_excluded(p))
    visible_files: List[Path] = [p for p in all_files if _is_manifest_visible(p)]
    excluded_other_count = len(all_files) - excluded_junk_count - len(visible_files)
    files: List[Path] = visible_files

    # Heuristic: detect common material base layouts and only list "main documents".
    # This keeps the prompt compact and increases the chance the model starts with the newest primary report.
    #
    # Supported layouts:
    # - SEC filings downloaded by fetch_sec_edgar: base/<FORM>_<FILED>_report_<REPORT>_<ACCESSION>/... .htm
    # - MinerU output: base/<doc_name>/artifacts/full.md + *_origin.pdf
    # - Marker output: base/<doc_name>/<doc_name>.json (+ <doc_name>_meta.json)

    sec_dir_re = re.compile(
        r"^(?P<form>[^_]+)_(?P<filed>\d{4}-\d{2}-\d{2})_report_(?P<report>\d{4}-\d{2}-\d{2})_(?P<acc>\d{10}-\d{2}-\d{6})$"
    )

    def _try_parse_date(s: str) -> Optional[datetime]:
        try:
            return datetime.strptime(s, "%Y-%m-%d")
        except Exception:
            return None

    def _sec_form_bucket(form: str) -> str:
        # Normalize common SEC form spellings so we can apply per-form quotas.
        f = re.sub(r"\s+", "", form.upper())
        if re.fullmatch(r"10-?K", f):
            return "10-K"
        if re.fullmatch(r"10-?Q", f):
            return "10-Q"
        if re.fullmatch(r"8-?K", f):
            return "8-K"
        if "DEF14A" in f:
            return "DEF 14A"
        if re.fullmatch(r"20-?F", f):
            return "20-F"
        if re.fullmatch(r"6-?K", f):
            return "6-K"
        return form.upper().strip() or "(unknown)"

    def _select_sec_dirs(
        rows: List[tuple[datetime, str, str, str, Path]],
        *,
        total_cap: int,
    ) -> List[tuple[datetime, str, str, str, Path]]:
        # Prefer the newest primary periodic reports first, but keep a few others as fill.
        quotas = {
            "10-K": 2,
            "20-F": 2,
            "10-Q": 4,
            "6-K": 4,
            "DEF 14A": 1,
        }

        picked: List[tuple[datetime, str, str, str, Path]] = []
        remaining = dict(quotas)
        used_dirs: set[Path] = set()

        for filed_dt, form, report_date, acc, d in rows:
            if len(picked) >= total_cap:
                break
            bucket = _sec_form_bucket(form)
            if bucket in remaining and remaining[bucket] > 0:
                remaining[bucket] -= 1
                picked.append((filed_dt, form, report_date, acc, d))
                used_dirs.add(d)

        if len(picked) < total_cap:
            for filed_dt, form, report_date, acc, d in rows:
                if len(picked) >= total_cap:
                    break
                if d in used_dirs:
                    continue
                picked.append((filed_dt, form, report_date, acc, d))
                used_dirs.add(d)

        return picked

    def _pick_main_html(filing_dir: Path, form: str) -> Optional[Path]:
        htmls = [p for p in filing_dir.glob("*.htm")] + [p for p in filing_dir.glob("*.html")]
        if not htmls:
            return None
        form_key = re.sub(r"[^a-z0-9]", "", form.lower())

        def score(p: Path) -> tuple[int, int]:
            name = p.name.lower()
            name_key = re.sub(r"[^a-z0-9]", "", name)
            bonus = 0
            if form_key and form_key in name_key:
                bonus += 2
            if re.search(r"\b10k\b|10-k", name) and "10k" in form_key:
                bonus += 1
            if re.search(r"\b10q\b|10-q", name) and "10q" in form_key:
                bonus += 1
            if re.search(r"\b20f\b|20-f", name) and "20f" in form_key:
                bonus += 1
            if re.search(r"\b6k\b|6-k", name) and "6k" in form_key:
                bonus += 1
            if "def14a" in name_key and "def14a" in form_key:
                bonus += 1
            try:
                size = p.stat().st_size
            except OSError:
                size = -1
            return (bonus, size)

        return max(htmls, key=score)

    def _mineru_period_key(name: str) -> tuple[int, int]:
        # Rough ordering for Chinese report folders.
        # Higher means newer.
        m = re.search(r"(\d{4})", name)
        year = int(m.group(1)) if m else 0
        period = 0
        if "一季度" in name:
            period = 1
        elif "中报" in name or "半年" in name or "二季度" in name:
            period = 2
        elif "三季度" in name:
            period = 3
        elif "年报" in name or "年度" in name or "四季度" in name:
            period = 4
        return (year, period)

    lines: List[str] = []
    lines.append(f"Location: {base_dir}")
    lines.append(f"Total files under location: {len(all_files)}")
    lines.append(f"Manifest-visible files (json/html/pdf/md/yml/yaml): {len(files)}")
    lines.append("Note: This list is intentionally partial; traverse location as needed.")
    lines.append("")

    # 1) SEC filings layout
    sec_dirs: List[tuple[datetime, str, str, str, Path]] = []
    for p in base_dir.iterdir():
        if not p.is_dir():
            continue
        m = sec_dir_re.match(p.name)
        if not m:
            continue
        filed_dt = _try_parse_date(m.group("filed"))
        if not filed_dt:
            continue
        sec_dirs.append((filed_dt, m.group("form"), m.group("report"), m.group("acc"), p))

    if sec_dirs:
        sec_dirs.sort(key=lambda x: x[0], reverse=True)
        lines.append("Detected materials type: SEC filings (fetch_sec_edgar layout)")
        lines.append("Hint: Prefer latest 10-K/20-F for annual baseline; use newer 10-Q/6-K for interim updates.")
        lines.append("")
        # Even when the base contains only dozens of filings, listing them all wastes prompt tokens.
        # Keep a short, newest-first list with per-form quotas to anchor the model.
        shown = _select_sec_dirs(sec_dirs, total_cap=max(1, max_items))
        for filed_dt, form, report_date, acc, d in shown:
            main = _pick_main_html(d, form)
            if main is None:
                continue
            rel = main.relative_to(base_dir)
            lines.append(f"- {filed_dt.date().isoformat()} | Form {form} | Report {report_date} | Accession {acc} | {rel}")
        remaining = len(sec_dirs) - len(shown)
        if remaining > 0:
            lines.append(f"- … ({remaining} more filings not listed)")
        lines.append("")
        lines.append(f"Template (required): {TEMPLATE_PATH}")
        return "\n".join(lines) + "\n"

    # 2) MinerU layout
    # Goal: keep year coverage stable (similar to other sources that tend to have one anchor per year).
    # For each year, pick the "best" doc (prefer higher period, e.g., 年报 > Q3 > 中报 > Q1).
    mineru_docs: List[tuple[int, int, int, Path]] = []
    mineru_unknown_seq = 0
    for d in base_dir.iterdir():
        if not d.is_dir():
            continue
        full_md = d / "artifacts" / "full.md"
        content_lists = list((d / "artifacts").glob("*_content_list.json")) if (d / "artifacts").exists() else []
        if full_md.exists() or content_lists:
            year, period = _mineru_period_key(d.name)
            if year <= 0:
                mineru_unknown_seq += 1
                # Avoid collapsing multiple unknown-year docs into one bucket.
                year = -mineru_unknown_seq
            mineru_docs.append((year, period, _mineru_period_key(d.name)[1], d))

    if mineru_docs:
        # Pick one doc per year (best period; tie-breaker by name).
        best_by_year: dict[int, tuple[int, str, Path]] = {}
        for year, period, _period_dup, d in mineru_docs:
            cand = (period, d.name, d)
            prev = best_by_year.get(year)
            if prev is None or cand > prev:
                best_by_year[year] = cand

        years_sorted = sorted(best_by_year.keys(), reverse=True)
        shown_years = years_sorted[:max_items]

        lines.append("Detected materials type: MinerU output")
        lines.append("Hint: Read artifacts/full.md first; use *_content_list.json for page/heading lookup.")
        lines.append("")
        for year in shown_years:
            _, _, d = best_by_year[year]
            rel_dir = d.relative_to(base_dir)
            full_md = d / "artifacts" / "full.md"
            if full_md.exists():
                lines.append(f"- {rel_dir}/artifacts/full.md")
            # Scheme A: list content_list.json for finer-grained page/heading lookup.
            artifacts_dir = d / "artifacts"
            if artifacts_dir.exists():
                content_lists = list(artifacts_dir.glob("*_content_list.json"))
                if content_lists:
                    content_lists.sort(key=lambda p: p.name)
                    lines.append(f"- {content_lists[0].relative_to(base_dir)}")

        remaining_years = len(years_sorted) - len(shown_years)
        if remaining_years > 0:
            lines.append(f"- … ({remaining_years} more documents not listed)")
        lines.append("")
        lines.append(f"Template (required): {TEMPLATE_PATH}")
        return "\n".join(lines) + "\n"

    # 3) Marker layout (simple: <dir>/<dir>.json + <dir>_meta.json)
    marker_docs: List[Path] = []
    for d in base_dir.iterdir():
        if not d.is_dir():
            continue
        main_json = d / f"{d.name}.json"
        meta_json = d / f"{d.name}_meta.json"
        if main_json.exists() or meta_json.exists():
            marker_docs.append(d)

    def _marker_sort_key(path: Path) -> tuple[int, int, str]:
        name = path.name
        m = re.search(r"(?i)(\d{4})\s*Q([1-4])", name)
        if m:
            return (int(m.group(1)), int(m.group(2)), name)
        m = re.search(r"(?i)(\d{4})", name)
        if m:
            return (int(m.group(1)), 0, name)
        return (0, 0, name)

    if marker_docs:
        marker_docs.sort(key=_marker_sort_key, reverse=True)
        lines.append("Detected materials type: Marker output")
        lines.append("")
        shown = marker_docs[:max_items]
        for d in shown:
            main_json = d / f"{d.name}.json"
            meta_json = d / f"{d.name}_meta.json"
            # Keep marker manifests compact: anchor on ONE primary file per document.
            if main_json.exists():
                lines.append(f"- {main_json.relative_to(base_dir)}")
            elif meta_json.exists():
                lines.append(f"- {meta_json.relative_to(base_dir)}")
        if len(marker_docs) > max_items:
            lines.append(f"- … ({len(marker_docs) - max_items} more documents not listed)")
        lines.append("")
        lines.append(f"Template (required): {TEMPLATE_PATH}")
        return "\n".join(lines) + "\n"

    # 4) Fallback: list first max_items non-excluded files in sorted order
    files.sort(key=lambda p: str(p).lower())

    shown = files[:max_items]
    for p in shown:
        rel = p.relative_to(base_dir)
        lines.append(f"- {rel}")

    if len(files) > max_items:
        lines.append(f"- … ({len(files) - max_items} more files not listed)")

    lines.append("")
    lines.append(f"Template (required): {TEMPLATE_PATH}")
    return "\n".join(lines) + "\n"


def build_pack_manifest(bundle_path: Path) -> str:
    if not bundle_path.exists():
        raise SystemExit(f"Missing bundle file: {bundle_path}")

    lines: List[str] = []
    lines.append(f"Location: {bundle_path.parent}")
    lines.append("Total files under location: 1")
    lines.append("")
    lines.append(f"- {bundle_path.name}")
    lines.append("")
    lines.append(f"Template (required): {TEMPLATE_PATH}")
    return "\n".join(lines) + "\n"


def build_combined_materials_manifest(*, packs_manifest: Optional[str], base_manifest: str) -> str:
    """Build a single manifest string that includes both packs (preferred) and base (fallback).

    We deliberately keep this as a single string because the Codex prompt templates
    use a single {{MATERIALS_MANIFEST}} placeholder.
    """

    _BASE_LINE_RE = re.compile(r"^Location:\s*(?P<base>.*)\s*$")
    _TEMPLATE_LINE_RE = re.compile(r"^\s*Template\s*\(required\)\s*:\s*")

    def _parse_manifest(manifest: Optional[str]) -> tuple[Optional[str], str]:
        """Parse a manifest into (base_value, body_without_base_or_template).

        - Accepts None/empty.
        - Removes the first-line 'Base: ...' if present.
        - Removes any 'Template (required): ...' lines.
        """

        if not manifest or not manifest.strip():
            return None, ""

        raw_lines = manifest.strip("\n").splitlines()
        if not raw_lines:
            return None, ""

        base_value: Optional[str] = None
        start_idx = 0
        m = _BASE_LINE_RE.match(raw_lines[0])
        if m:
            base_value = m.group("base").strip() or None
            start_idx = 1

        body_lines: List[str] = []
        for line in raw_lines[start_idx:]:
            if _TEMPLATE_LINE_RE.match(line):
                continue
            body_lines.append(line.rstrip())
        body = "\n".join(body_lines).strip()
        return base_value, body

    parts: List[str] = []

    packs_base, packs_body = _parse_manifest(packs_manifest)
    if packs_manifest and packs_manifest.strip():
        if packs_base:
            parts.append(f"Materials packs (preferred) | Location: {packs_base}")
        else:
            parts.append("Materials packs (preferred):")
        parts.append(packs_body if packs_body else "(empty)")
    else:
        parts.append("Materials packs (preferred):")
        parts.append("(none)")

    parts.append("")


    base_base, base_body = _parse_manifest(base_manifest)
    if base_base and base_base != "(none)":
        parts.append(f"Base packs (fallback) | Location: {base_base} | Traverse: allowed")
    elif base_base == "(none)":
        parts.append("Base packs (fallback) | Location: (none)")
    else:
        parts.append("Base packs (fallback):")
    parts.append(base_body if base_body else "(empty)")

    parts.append("")
    parts.append(f"Template (required): {TEMPLATE_PATH}")

    return "\n".join(parts).rstrip() + "\n"


def build_base_materials_manifest(*, base_dir: Optional[Path], manifest_max_items: int) -> str:
    if base_dir:
        return build_materials_manifest(base_dir, max_items=max(1, int(manifest_max_items)))
    return (
        "Location: (none)\n"
        "Total files under location: 0\n"
        "Manifest-visible files (json/html/pdf/md/yml/yaml): 0\n"
        "Note: Base packs is (none); no local materials to traverse.\n\n"
        f"Template (required): {TEMPLATE_PATH}\n"
    )


def resolve_materials_index_dir(*, base_dir: Optional[Path], materials_index_arg: Optional[str]) -> Optional[Path]:
    if materials_index_arg:
        materials_index_dir = (
            (ROOT / materials_index_arg).resolve()
            if not os.path.isabs(materials_index_arg)
            else Path(materials_index_arg).resolve()
        )
        if not materials_index_dir.exists() or not materials_index_dir.is_dir():
            raise SystemExit(f"--materials-index is not a directory: {materials_index_dir}")
        if not (materials_index_dir / "manifest.jsonl").exists():
            raise SystemExit(f"--materials-index missing manifest.jsonl: {materials_index_dir / 'manifest.jsonl'}")
        if not (materials_index_dir / "toc.md").exists():
            raise SystemExit(f"--materials-index missing toc.md: {materials_index_dir / 'toc.md'}")
        return materials_index_dir

    if base_dir is not None:
        candidate = base_dir / "index"
        if candidate.exists() and candidate.is_dir():
            if (candidate / "manifest.jsonl").exists() and (candidate / "toc.md").exists():
                return candidate
    return None


def resolve_identity_materials(
    *,
    base_dir: Optional[Path],
    materials_index_dir: Optional[Path],
    materials_manifest: str,
    manifest_max_items: int,
) -> tuple[Optional[Path], str, Optional[Path]]:
    if base_dir is None:
        return None, materials_manifest, None
    evidence_dir = materials_index_dir if materials_index_dir else base_dir
    return base_dir, materials_manifest, evidence_dir


def pack_params_for_attempt(
    *,
    attempt: int,
    base_top_k: int,
    base_max_total_chars: int,
    expand_for_evidence: bool,
) -> tuple[int, int]:
    """Compute chapter-pack sizing for a given write attempt.

    Attempt 1 uses the base sizes.
    Attempt 2+ expands top_k/max_total_chars to reduce the chance of missing materials.
    """

    if attempt <= 1 or not expand_for_evidence:
        return base_top_k, base_max_total_chars
    if attempt == 2:
        return max(base_top_k, 120), max(base_max_total_chars, 450_000)
    return max(base_top_k, 200), max(base_max_total_chars, 800_000)


def fill_template(template_text: str, mapping: dict) -> str:
    out = template_text
    for k, v in mapping.items():
        out = out.replace("{{" + k + "}}", v)
    return out


def gen_infer_identity_prompt(
    *,
    infer_template_text: str,
    expected_ticker: Optional[str],
    base_dir_name_hint: str,
    materials_manifest_text: str,
    evidence_text: str,
) -> str:
    return fill_template(
        infer_template_text,
        {
            "EXPECTED_TICKER": (expected_ticker or "null"),
            "BASE_DIR_NAME_HINT": base_dir_name_hint,
            "MATERIALS_MANIFEST": materials_manifest_text,
            "EVIDENCE_TEXT": evidence_text,
        },
    )


def gen_infer_identity_from_ticker_only_prompt(
    *,
    infer_template_text: str,
    expected_ticker: str,
    materials_manifest_text: str,
    evidence_text: str,
) -> str:
    return fill_template(
        infer_template_text,
        {
            "EXPECTED_TICKER": expected_ticker,
            "BASE_DIR_NAME_HINT": "(none)",
            "MATERIALS_MANIFEST": materials_manifest_text,
            "EVIDENCE_TEXT": evidence_text,
        },
    )


def gen_agents_self_check_prompt(*, self_check_template_text: str) -> str:
    # Keep as a function so prompt iteration can be unit-tested/dumped consistently.
    return self_check_template_text


def gen_protocol_restatement_prompt(*, protocol_restatement_text: str) -> str:
    # Keep as a function so prompt iteration can be unit-tested/dumped consistently.
    return protocol_restatement_text


def gen_write_chapter_prompt(
    *,
    write_template_text: str,
    attempt: int,
    chapter_title: str,
    chapter_skeleton: str,
    materials_manifest: str,
    company: str,
    ticker: str,
    last_audit: Optional[dict],
) -> str:
    if attempt <= 1:
        preface = ""
    else:
        preface = (
            "上一版章节审计未通过。你必须严格按协议与硬约束重写该章节，修复所有违规点。\n"
            "注意：不得引入新事实；条件项缺失必须删除；不得输出模板注释；不要用数字编号列表。\n"
        )
        if last_audit is not None:
            preface += "\n审计违规信息（供你逐条修复）：\n" + json.dumps(last_audit, ensure_ascii=False, indent=2)
            preface += "\n\n"

    write_prompt_body = fill_template(
        write_template_text,
        {
            "CHAPTER_TITLE": chapter_title,
            "CHAPTER_SKELETON": chapter_skeleton,
            "MATERIALS_MANIFEST": materials_manifest,
            "COMPANY": company,
            "TICKER": ticker,
        },
    )

    return preface + write_prompt_body


def gen_audit_prompt(*, audit_template_text: str, chapter_markdown: str) -> str:
    return fill_template(
        audit_template_text,
        {
            "CHAPTER_MARKDOWN": chapter_markdown,
        },
    )


def gen_fill_overview_prompt(
    *,
    fill_overview_template_text: str,
    overview_input_text: str,
) -> str:
    fill_body = fill_template(
        fill_overview_template_text,
        {"FULL_REPORT_MARKDOWN": overview_input_text},
    )
    return fill_body


def build_overview_input_text(
    *,
    overview_input: str,
    full_body: str,
    written: List[Tuple[Chapter, Path]],
) -> str:
    if overview_input == "full":
        return full_body

    chunks: List[str] = []
    for c, p in written:
        md = _read_text(p)
        md_strip = md.lstrip()
        if not md_strip.startswith(f"## {c.title}"):
            chunks.append(f"## {c.title}\n")
        chunks.append(md[:1200] + ("\n…\n" if len(md) > 1200 else "\n"))
    return "\n".join(chunks)


def dump_prompts_to_dir(
    *,
    dump_dir: Path,
    base_dir: Optional[Path],
    materials_manifest: str,
    materials_index_dir: Optional[Path],
    protocol_restatement: str,
    expected_agents_sentinel: str,
    ticker: str,
    company: str,
    chapters: List[Chapter],
    write_template_text: str,
    audit_template_text: str,
    fill_overview_template_text: str,
    self_check_template_text: str,
    infer_template_text: str,
    infer_ticker_template_text: str,
    pack_top_k: int,
    pack_neighbor_window: int,
    pack_max_total_chars: int,
    max_attempts: int,
    overview_input: str,
    manifest_max_items: int,
    identity_index_max_items: int,
) -> None:
    dump_dir.mkdir(parents=True, exist_ok=True)

    _write_text(dump_dir / "_protocol_restatement.txt", protocol_restatement.rstrip() + "\n")

    logs_dir = dump_dir
    chapters_dir = dump_dir
    report_dir = dump_dir.parent
    logs_dir.mkdir(parents=True, exist_ok=True)

    def _extract_title_from_label(label: str) -> Optional[str]:
        m = re.search(r"write_chapter:(.+?):attempt\d+$", label)
        return m.group(1) if m else None

    def run_codex_dump_stub(
        prompt_text: str,
        output_last_message_path: Path,
        *,
        model: Optional[str] = None,
        reasoning_effort: Optional[str] = None,
        verbose: bool = False,
        label: str = "",
    ) -> str:
        # NOTE: dump stub writes PROMPT to output_last_message_path (not model output).
        output_last_message_path.parent.mkdir(parents=True, exist_ok=True)
        _write_text(output_last_message_path, prompt_text.rstrip() + "\n")

        if label == "agents_self_check":
            return f"AGENTS_SENTINEL: {expected_agents_sentinel}\n"
        if label == "infer_identity":
            return json.dumps(
                {
                    "ticker": ticker,
                    "company": company,
                    "base_matches_ticker": True,
                    "mismatch_reason": None,
                },
                ensure_ascii=False,
                indent=2,
            )
        if label.startswith("audit:"):
            return json.dumps(
                {
                    "pass": True,
                    "class": "ok",
                    "violations": [],
                    "notes": [],
                },
                ensure_ascii=False,
                indent=2,
            )
        if label.startswith("write_chapter:"):
            title = _extract_title_from_label(label) or "(unknown)"
            return (
                f"## {title}\n\n"
                "【占位符】\n"
                "- 缺口：dump-prompts 模式未运行 Codex，因此这里没有真实章节输出。\n"
                "- 需要：去掉 --dump-prompts 运行一次 write，再基于真实输出审计。\n"
                "- 已检索范围：N/A（dump-prompts）\n"
                "- 下一步：执行正常流程生成章节后回填。\n"
            )
        if label == "fill_overview":
            return (
                "## 投资要点概览\n\n"
                "【占位符】\n"
                "- 缺口：dump-prompts 模式未运行 Codex。\n"
                "- 需要：去掉 --dump-prompts 运行一次 fill overview。\n"
            )
        return ""

    # Step 0: infer identity prompt
    if base_dir is not None:
        identity_base_dir, identity_manifest, identity_evidence_dir = resolve_identity_materials(
            base_dir=base_dir,
            materials_index_dir=materials_index_dir,
            materials_manifest=materials_manifest,
            manifest_max_items=manifest_max_items,
        )
        step_infer_identity_from_materials(
            base_dir=identity_base_dir,
            materials_manifest=identity_manifest,
            evidence_dir=identity_evidence_dir,
            expected_ticker=ticker,
            logs_dir=logs_dir,
            infer_template_text=infer_template_text,
            model=None,
            reasoning_effort=None,
            verbose=False,
            identity_index_max_items=max(1, int(identity_index_max_items)),
            run_codex_fn=run_codex_dump_stub,
        )
    else:
        step_infer_identity_from_ticker_only(
            expected_ticker=ticker,
            logs_dir=logs_dir,
            infer_template_text=infer_ticker_template_text,
            model=None,
            reasoning_effort=None,
            verbose=False,
            run_codex_fn=run_codex_dump_stub,
        )

    # Step 1: agents self-check prompt
    step_agents_self_check(
        self_check_template_text=self_check_template_text,
        logs_dir=logs_dir,
        expected_sentinel=expected_agents_sentinel,
        model=None,
        reasoning_effort=None,
        verbose=False,
        run_codex_fn=run_codex_dump_stub,
    )

    # Step 2: write+audit prompts
    written: List[Tuple[Chapter, Path]] = []
    for chapter in chapters:
        safe_name = _sanitize_filename(chapter.title)
        chapter_path = chapters_dir / f"{safe_name}.md"
        step_write_and_audit_chapter(
            chapter=chapter,
            chapter_path=chapter_path,
            report_dir=report_dir,
            logs_dir=logs_dir,
            max_attempts=int(max_attempts),
            materials_index_dir=materials_index_dir,
            materials_manifest=materials_manifest,
            pack_top_k=int(pack_top_k),
            pack_neighbor_window=int(pack_neighbor_window),
            pack_max_total_chars=int(pack_max_total_chars),
            company=company,
            ticker=ticker,
            write_template_text=write_template_text,
            audit_template_text=audit_template_text,
            model=None,
            reasoning_effort=None,
            verbose=False,
            on_audit_fail=None,
            run_codex_fn=run_codex_dump_stub,
        )
        written.append((chapter, chapter_path))

    # Step 4: fill overview prompt
    assembled_parts: List[str] = []
    for c, p in written:
        if p.exists():
            assembled_parts.append(_read_text(p).rstrip() + "\n\n")
    full_body = "".join(assembled_parts).strip() + "\n"

    overview_input_text = build_overview_input_text(
        overview_input=overview_input,
        full_body=full_body,
        written=written,
    )

    _write_text(dump_dir / "_step4_overview_input_text.txt", overview_input_text.rstrip() + "\n")

    step_fill_overview(
        overview_input=str(overview_input),
        full_body=full_body,
        written=written,
        chapters_dir=chapters_dir,
        logs_dir=logs_dir,
        fill_overview_template_text=fill_overview_template_text,
        model=None,
        reasoning_effort=None,
        verbose=False,
        run_codex_fn=run_codex_dump_stub,
    )


def run_codex(
    prompt_text: str,
    output_last_message_path: Path,
    *,
    model: Optional[str] = None,
    reasoning_effort: Optional[str] = None,
    verbose: bool = False,
    label: str = "",
) -> str:
    output_last_message_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "codex",
        "exec",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
        "--output-last-message",
        str(output_last_message_path),
        "-",  # read prompt from stdin
    ]
    if model:
        cmd[1:1] = ["--model", model]
    if reasoning_effort:
        # Use config override because Codex CLI does not expose a direct flag.
        cmd[1:1] = ["--config", f"model_reasoning_effort=\"{reasoning_effort}\""]

    if verbose:
        # Print the exact CLI invocation for observability/debugging.
        # Prompt content is sent via stdin, so it won't show here.
        _log_step(f"Run codex cmd (cwd={ROOT}): {shlex.join(cmd)}")
        banner = f"\n===== CODEX PROMPT{': ' + label if label else ''} =====\n"
        sys.stdout.write(banner)
        sys.stdout.write(prompt_text.rstrip() + "\n")
        sys.stdout.write("===== END CODEX PROMPT =====\n")
        sys.stdout.flush()

    proc = subprocess.run(
        cmd,
        input=prompt_text,
        text=True,
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            "Codex exec failed:\n"
            f"Command: {' '.join(cmd)}\n"
            f"STDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}\n"
        )

    if not output_last_message_path.exists():
        raise RuntimeError("Codex reported success but did not write --output-last-message")

    final = _read_text(output_last_message_path)
    if verbose:
        banner = f"\n===== CODEX OUTPUT{': ' + label if label else ''} =====\n"
        sys.stdout.write(banner)
        sys.stdout.write(final.rstrip() + "\n")
        sys.stdout.write("===== END CODEX OUTPUT =====\n")
        sys.stdout.flush()

    return final


def _strip_code_fences_if_any(text: str) -> str:
    t = text.strip()
    if t.startswith("```") and t.endswith("```"):
        lines = t.splitlines()
        if len(lines) >= 3:
            return "\n".join(lines[1:-1]).strip() + "\n"
    return text


def _strip_json_code_fences_if_any(text: str) -> str:
    t = text.strip()
    if t.startswith("```") and t.endswith("```"):
        lines = t.splitlines()
        if len(lines) >= 3:
            # drop first and last fence line
            return "\n".join(lines[1:-1]).strip()
    return text.strip()


def parse_audit_json(text: str) -> dict:
    raw = _strip_code_fences_if_any(text).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Try to salvage the first JSON object.
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(raw[start : end + 1])
        raise


def parse_identity_json(text: str) -> dict:
    raw = _strip_json_code_fences_if_any(text)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(raw[start : end + 1])
        raise


def step_infer_identity_from_materials(
    *,
    base_dir: Path,
    materials_manifest: str,
    evidence_dir: Optional[Path],
    expected_ticker: Optional[str],
    logs_dir: Path,
    infer_template_text: str,
    model: Optional[str],
    reasoning_effort: Optional[str],
    verbose: bool,
    identity_index_max_items: int,
    run_codex_fn=run_codex,
) -> dict:
    evidence_source_dir = evidence_dir or base_dir
    if (evidence_source_dir / "manifest.jsonl").exists() and (evidence_source_dir / "toc.md").exists():
        evidence = collect_identity_evidence_from_index(evidence_source_dir, max_items=identity_index_max_items)
    else:
        evidence = collect_identity_evidence(evidence_source_dir)
    materials_manifest_block = materials_manifest
    if materials_manifest_block.strip():
        lines = materials_manifest_block.splitlines()
        if lines and lines[0].startswith("Location:"):
            location = lines[0].replace("Location:", "", 1).strip() or "(none)"
            header = f"Base packs | Location: {location}"
            materials_manifest_block = "\n".join([header] + lines[1:])
    evidence_text = evidence.strip()

    prompt = gen_infer_identity_prompt(
        infer_template_text=infer_template_text,
        expected_ticker=expected_ticker,
        base_dir_name_hint=str(base_dir),
        materials_manifest_text=materials_manifest_block.strip(),
        evidence_text=evidence_text,
    )

    out_path = logs_dir / "infer_identity_last_message.txt"
    text = run_codex_fn(
        prompt,
        out_path,
        model=model,
        reasoning_effort=reasoning_effort,
        verbose=verbose,
        label="infer_identity",
    )
    return parse_identity_json(text)


def step_infer_identity_from_ticker_only(
    *,
    expected_ticker: str,
    logs_dir: Path,
    infer_template_text: str,
    model: Optional[str],
    reasoning_effort: Optional[str],
    verbose: bool,
    run_codex_fn=run_codex,
) -> dict:
    materials_manifest_text = "Base packs | Location: (none)\nNote: no local materials."
    evidence_text = "(none)"
    prompt = gen_infer_identity_from_ticker_only_prompt(
        infer_template_text=infer_template_text,
        expected_ticker=expected_ticker,
        materials_manifest_text=materials_manifest_text,
        evidence_text=evidence_text,
    )

    out_path = logs_dir / "infer_identity_last_message.txt"
    text = run_codex_fn(
        prompt,
        out_path,
        model=model,
        reasoning_effort=reasoning_effort,
        verbose=verbose,
        label="infer_identity",
    )
    return parse_identity_json(text)


def step_agents_self_check(
    *,
    self_check_template_text: str,
    logs_dir: Path,
    expected_sentinel: str,
    model: Optional[str],
    reasoning_effort: Optional[str],
    verbose: bool,
    run_codex_fn=run_codex,
) -> str:
    # Important: do NOT prefix protocol restatement here, otherwise the self-check cannot
    # meaningfully demonstrate that AGENTS.md was loaded as project instructions.
    prompt = gen_agents_self_check_prompt(self_check_template_text=self_check_template_text)
    out = run_codex_fn(
        prompt,
        logs_dir / "agents_self_check_last_message.txt",
        model=model,
        reasoning_effort=reasoning_effort,
        verbose=verbose,
        label="agents_self_check",
    )
    validate_agents_self_check_output(out, expected_sentinel=expected_sentinel)
    _write_text(logs_dir / "_agents_self_check.txt", out)
    return out


def step_protocol_restatement(
    *,
    protocol_restatement_text: str,
    logs_dir: Path,
    model: Optional[str],
    reasoning_effort: Optional[str],
    verbose: bool,
    run_codex_fn=run_codex,
) -> None:
    prompt = gen_protocol_restatement_prompt(protocol_restatement_text=protocol_restatement_text)
    run_codex_fn(
        prompt,
        logs_dir / "protocol_restatement_last_message.txt",
        model=model,
        reasoning_effort=reasoning_effort,
        verbose=verbose,
        label="protocol_restatement",
    )


def step_write_and_audit_chapter(
    *,
    chapter: Chapter,
    chapter_path: Path,
    report_dir: Path,
    logs_dir: Path,
    max_attempts: int,
    materials_index_dir: Optional[Path],
    materials_manifest: str,
    pack_top_k: int,
    pack_neighbor_window: int,
    pack_max_total_chars: int,
    company: str,
    ticker: str,
    write_template_text: str,
    audit_template_text: str,
    model: Optional[str],
    reasoning_effort: Optional[str],
    verbose: bool,
    on_audit_fail: Optional[Callable[[Optional[str]], None]] = None,
    run_codex_fn=run_codex,
) -> tuple[bool, Optional[dict]]:
    safe_name = _sanitize_filename(chapter.title)

    last_audit: Optional[dict] = None
    last_audit_class: Optional[str] = None

    for attempt in range(1, max_attempts + 1):
        _log_step(f"- attempt {attempt}/{max_attempts}: write chapter")

        chapter_packs_manifest: Optional[str] = None
        if materials_index_dir is not None:
            packs_root = report_dir / "_materials_packs"
            pack_dir = packs_root / safe_name / f"attempt{attempt}"
            pack_dir.mkdir(parents=True, exist_ok=True)

            base_top_k = pack_top_k if pack_top_k > 0 else 0
            base_max_chars = pack_max_total_chars
            expand_for_evidence = attempt > 1 and last_audit_class == "evidence_insufficient"
            pack_k, pack_chars = pack_params_for_attempt(
                attempt=attempt,
                base_top_k=base_top_k,
                base_max_total_chars=base_max_chars,
                expand_for_evidence=expand_for_evidence,
            )

            bundle_path = pack_dir / "bundle.md"
            pack_cmd = [
                sys.executable,
                str(ROOT / "utils" / "build_chapter_pack.py"),
                "--index-dir",
                str(materials_index_dir),
                "--chapter",
                chapter.title,
                "--output",
                str(pack_dir),
                "--max-total-chars",
                str(pack_chars),
            ]

            # Attempt 1: only override top_k if explicitly provided.
            # Attempt 2+: always override to expanded sizes.
            if attempt == 1:
                if base_top_k > 0:
                    pack_cmd.extend(["--top-k", str(base_top_k)])
            else:
                pack_cmd.extend(["--top-k", str(pack_k)])

            if pack_neighbor_window >= 0:
                pack_cmd.extend(["--neighbor-window", str(pack_neighbor_window)])

            _log_step(
                "  build chapter pack | "
                f"chapter={chapter.title} attempt={attempt} top_k={pack_k or '(toc)'} max_chars={pack_chars}"
            )
            proc = subprocess.run(
                pack_cmd,
                cwd=str(ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if proc.returncode != 0:
                raise SystemExit(
                    "build_chapter_pack failed\n"
                    f"Command: {shlex.join(pack_cmd)}\n"
                    f"STDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}\n"
                )
            if verbose and proc.stdout.strip():
                sys.stdout.write(proc.stdout)
                sys.stdout.flush()

            chapter_packs_manifest = build_pack_manifest(bundle_path)

        chapter_materials_manifest = build_combined_materials_manifest(
            packs_manifest=chapter_packs_manifest,
            base_manifest=materials_manifest,
        )

        write_prompt = gen_write_chapter_prompt(
            write_template_text=write_template_text,
            attempt=attempt,
            chapter_title=chapter.title,
            chapter_skeleton=chapter.skeleton,
            materials_manifest=chapter_materials_manifest,
            company=company,
            ticker=ticker,
            last_audit=last_audit,
        )

        out_path = logs_dir / f"write_{safe_name}_attempt{attempt}_last_message.txt"
        _log_step(
            f"  codex(write) start | title={chapter.title} attempt={attempt}/{max_attempts} | "
            f"last_message={out_path}"
        )
        chapter_md = run_codex_fn(
            write_prompt,
            out_path,
            model=model,
            reasoning_effort=reasoning_effort,
            verbose=verbose,
            label=f"write_chapter:{chapter.title}:attempt{attempt}",
        )
        chapter_md = _strip_code_fences_if_any(chapter_md)
        _write_text(chapter_path, chapter_md)
        _log_step(f"  wrote chapter file: {chapter_path}")

        if is_write_blocked(chapter_md):
            _log_step("  write blocked: missing minimum inputs (will retry if attempts remain)")
            last_audit = {
                "pass": False,
                "class": AUDIT_CLASS_WRITE_BLOCKED,
                "violations": [
                    {
                        "rule": "0.2",
                        "severity": "high",
                        "excerpt": "【缺口清单（未满足最小输入条件，无法进入 #WRITE）】",
                        "reason": "模型判定最小输入条件未满足，未进入写作流程。",
                        "rewrite_hint": "补齐材料或改用可检索来源后再写作。",
                    }
                ],
                "notes": [],
            }
            last_audit_class = last_audit.get("class")
            if on_audit_fail is not None:
                on_audit_fail(last_audit_class)
            continue

        _log_step("  audit prep | rules=facts&tone 2 + 2.1–2.6")
        audit_prompt = gen_audit_prompt(audit_template_text=audit_template_text, chapter_markdown=chapter_md)
        audit_out_path = logs_dir / f"audit_{safe_name}_attempt{attempt}_last_message.txt"
        _log_step(
            f"  codex(audit) start | title={chapter.title} attempt={attempt}/{max_attempts} | "
            f"last_message={audit_out_path}"
        )
        audit_text = run_codex_fn(
            audit_prompt,
            audit_out_path,
            model=model,
            reasoning_effort=reasoning_effort,
            verbose=verbose,
            label=f"audit:{chapter.title}:attempt{attempt}",
        )
        try:
            audit = parse_audit_json(audit_text)
        except Exception as e:  # noqa: BLE001
            _log_step(f"  audit parse failed (will retry): {e}")
            last_audit = {
                "pass": False,
                "class": "unknown",
                "violations": [
                    {
                        "rule": "2.8",
                        "severity": "high",
                        "excerpt": "(audit JSON parse error)",
                        "reason": f"审计输出不是合法 JSON: {e}",
                        "rewrite_hint": "严格按模板输出 JSON-only。",
                    }
                ],
                "notes": [],
            }
            last_audit_class = last_audit.get("class")
            continue

        last_audit = audit
        last_audit_class = audit.get("class")
        if audit.get("pass") is True:
            vcount = len(audit.get("violations") or [])
            _log_step(f"  audit PASS | violations={vcount}")
            return True, audit

        vcount = len(audit.get("violations") or [])
        _log_step(f"  audit FAIL | violations={vcount} (will retry if attempts remain)")
        if on_audit_fail is not None:
            on_audit_fail(last_audit_class)

    # Non-fatal: keep the last attempt's chapter output and continue.
    _log_step(
        f"  audit still FAIL after {max_attempts} attempts; continue with last output (non-fatal) | title={chapter.title}"
    )
    if last_audit is not None:
        audit_final_path = logs_dir / f"_audit_{safe_name}_final.json"
        _write_text(audit_final_path, json.dumps(last_audit, ensure_ascii=False, indent=2) + "\n")
        _log_step(f"  saved final failing audit: {audit_final_path}")
    return False, last_audit


def step_fill_overview(
    *,
    overview_input: str,
    full_body: str,
    written: List[Tuple[Chapter, Path]],
    chapters_dir: Path,
    logs_dir: Path,
    fill_overview_template_text: str,
    model: Optional[str],
    reasoning_effort: Optional[str],
    verbose: bool,
    run_codex_fn=run_codex,
) -> tuple[str, Path]:
    overview_input_text = build_overview_input_text(
        overview_input=overview_input,
        full_body=full_body,
        written=written,
    )

    fill_prompt = gen_fill_overview_prompt(
        fill_overview_template_text=fill_overview_template_text,
        overview_input_text=overview_input_text,
    )
    fill_out_path = logs_dir / "fill_overview_last_message.txt"
    overview_md = run_codex_fn(
        fill_prompt,
        fill_out_path,
        model=model,
        reasoning_effort=reasoning_effort,
        verbose=verbose,
        label="fill_overview",
    )
    overview_md = _strip_code_fences_if_any(overview_md)
    overview_path = chapters_dir / f"{_sanitize_filename('投资要点概览')}.md"
    _write_text(overview_path, overview_md)
    _log_step(f"Overview saved: {overview_path}")
    return overview_md, overview_path


def _read_text_head(path: Path, max_chars: int = 200_000) -> str:
    # Many SEC .htm files are huge; only read the beginning.
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        return f.read(max_chars)


def _read_text_head_lines(path: Path, max_lines: int) -> str:
    lines: List[str] = []
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            for idx, line in enumerate(f):
                if idx >= max_lines:
                    break
                lines.append(line.rstrip("\n"))
    except OSError:
        return ""
    return "\n".join(lines).strip() + ("\n" if lines else "")


def collect_identity_evidence(base_dir: Path, *, max_files: int = 5) -> str:
    def _marker_sort_key(path: Path) -> tuple[int, int, str]:
        name = path.name
        m = re.search(r"(?i)(\d{4})\s*Q([1-4])", name)
        if m:
            return (int(m.group(1)), int(m.group(2)), name)
        m = re.search(r"(?i)(\d{4})", name)
        if m:
            return (int(m.group(1)), 0, name)
        return (0, 0, name)

    marker_meta_files: List[Path] = []
    for d in base_dir.iterdir():
        if not d.is_dir():
            continue
        meta_json = d / f"{d.name}_meta.json"
        if meta_json.exists():
            marker_meta_files.append(meta_json)

    lines: List[str] = []
    if marker_meta_files:
        marker_meta_files.sort(key=lambda p: _marker_sort_key(p.parent), reverse=True)
        picked = marker_meta_files[:max_files]
        for p in picked:
            rel = p.relative_to(base_dir)
            lines.append(f"file: {rel}")
            toc_titles: List[str] = []
            try:
                with p.open("r", encoding="utf-8", errors="ignore") as f:
                    obj = json.load(f)
                toc = obj.get("table_of_contents") if isinstance(obj, dict) else None
                if isinstance(toc, list):
                    for item in toc:
                        if isinstance(item, dict):
                            title = str(item.get("title") or "").strip()
                            if title:
                                toc_titles.append(title)
                        if len(toc_titles) >= 3:
                            break
            except Exception:
                toc_titles = []

            if toc_titles:
                for title in toc_titles:
                    lines.append(f"- toc: {title}")
            else:
                lines.append("- (no toc entries found)")
            lines.append("")

        return "\n".join(lines).strip() + "\n"

    patterns = [
        re.compile(r"Exact name of registrant", re.IGNORECASE),
        re.compile(r"Trading\s+Symbol", re.IGNORECASE),
        re.compile(r"Trading\s+symbol\(s\)", re.IGNORECASE),
        re.compile(r"Commission\s+File\s+Number", re.IGNORECASE),
        re.compile(r"\bCIK\b", re.IGNORECASE),
    ]

    files = [p for p in base_dir.rglob("*") if p.is_file() and p.suffix.lower() in {".htm", ".html", ".txt"}]
    files.sort(key=lambda p: str(p).lower())
    picked = files[:max_files]

    for p in picked:
        rel = p.relative_to(base_dir)
        head = _read_text_head(p)
        hits: List[str] = []
        for pat in patterns:
            m = pat.search(head)
            if not m:
                continue
            start = max(0, m.start() - 120)
            end = min(len(head), m.end() + 220)
            snippet = head[start:end]
            snippet = re.sub(r"\s+", " ", snippet).strip()
            hits.append(f"- hit: {pat.pattern} | snippet: {snippet}")

        lines.append(f"file: {rel}")
        if hits:
            lines.extend(hits)
        else:
            lines.append("- (no obvious identity markers found in head)")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def collect_identity_evidence_from_index(
    index_dir: Path,
    *,
    max_items: int = IDENTITY_INDEX_EVIDENCE_MAX_ITEMS,
    max_preview_chars: int = IDENTITY_INDEX_EVIDENCE_MAX_PREVIEW_CHARS,
) -> str:
    manifest_path = index_dir / "manifest.jsonl"
    lines: List[str] = []
    lines.append(f"index_dir: {index_dir}")
    lines.append("")

    if manifest_path.exists():
        rows: List[str] = []
        with manifest_path.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if len(rows) >= max_items:
                    break
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
                source = str(obj.get("source_pdf_name") or "")
                doc_id = str(obj.get("doc_id") or "")
                heading = str(obj.get("heading") or "")
                preview = str(obj.get("preview") or obj.get("text") or "")
                preview = re.sub(r"\s+", " ", preview).strip()
                if max_preview_chars > 0 and len(preview) > max_preview_chars:
                    preview = preview[:max_preview_chars] + "…"
                rows.append(
                    "- row: "
                    + " | ".join(
                        [
                            f"doc_id={doc_id}" if doc_id else "doc_id=(none)",
                            f"source={source}" if source else "source=(none)",
                            f"heading={heading}" if heading else "heading=(none)",
                            f"preview={preview}" if preview else "preview=(empty)",
                        ]
                    )
                )
        lines.append(f"manifest_head (first {max_items} rows):")
        lines.extend(rows if rows else ["- (no mineru_chunk rows found)"])
        lines.append("")
    else:
        lines.append("manifest_head: (missing manifest.jsonl)")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


_HEADING_RE = re.compile(r"^(#{2,6})\s+(.+?)\s*$", re.MULTILINE)
_URL_RE = re.compile(r"https?://\S+")
_SEC_FILE_LEVEL_RE = re.compile(
    r"^(?P<prefix>.*?\|\s*SEC\s+EDGAR\s*\|\s*Form\s*[^|]+\|\s*Filed\s*[^|]+\|\s*Accession\s*[^|]+)",
    re.IGNORECASE,
)


def extract_sources_block(chapter_markdown: str) -> List[str]:
    lines = chapter_markdown.splitlines()
    # Find a heading that equals "证据与出处".
    start_idx = None
    start_level = None
    for i, line in enumerate(lines):
        m = _HEADING_RE.match(line)
        if m and m.group(2).strip() == "证据与出处":
            start_idx = i + 1
            start_level = len(m.group(1))
            break
    if start_idx is None:
        return []

    out: List[str] = []
    for j in range(start_idx, len(lines)):
        m = _HEADING_RE.match(lines[j])
        if m and len(m.group(1)) <= (start_level or 3):
            break
        if lines[j].strip().startswith("-"):
            out.append(lines[j].rstrip())
    # Strip empty / placeholder bullets
    out = [l for l in out if l.strip() not in {"-", "- "}]
    return out


def normalize_source_bullet_to_file_or_url_level(line: str) -> Optional[str]:
    raw = line.strip()
    if not raw:
        return None

    # Drop the bullet marker if present.
    if raw.startswith("-"):
        raw = raw.lstrip("-").strip()
    if not raw:
        return None

    # SEC EDGAR: keep up to accession (file-level), drop trailing section/item.
    m = _SEC_FILE_LEVEL_RE.match(raw)
    if m:
        normalized = " | ".join([p.strip() for p in m.group("prefix").split("|")])
        return "- " + normalized

    # Web: keep up to the URL (URL-level), drop anything after the URL.
    um = _URL_RE.search(raw)
    if um:
        kept = raw[: um.end()].rstrip(").,;]")
        return "- " + kept.strip()

    # Uploaded reports / other docs: keep file-level (first 2 pipe-separated fields).
    if "|" in raw:
        parts = [p.strip() for p in raw.split("|") if p.strip()]
        if len(parts) >= 2:
            return "- " + " | ".join(parts[:2])

    return "- " + raw


def build_sources_chapter_from_evidence_blocks(source_bullets: Iterable[str]) -> str:
    normalized: List[str] = []
    for line in source_bullets:
        n = normalize_source_bullet_to_file_or_url_level(line)
        if n:
            normalized.append(n)

    normalized = dedupe_preserve_order(normalized)

    sec: List[str] = []
    web: List[str] = []
    other: List[str] = []
    for l in normalized:
        body = l.lstrip("-").strip()
        if re.search(r"\bSEC\s+EDGAR\b", body, flags=re.IGNORECASE):
            sec.append(l)
        elif _URL_RE.search(body):
            web.append(l)
        else:
            other.append(l)

    parts: List[str] = ["## 来源清单\n"]
    if sec:
        parts.append("### SEC filings\n")
        parts.append("\n".join(sec) + "\n\n")
    if other:
        parts.append("### 上传财报/公告（及其它文件）\n")
        parts.append("\n".join(other) + "\n\n")
    if web:
        parts.append("### 网页资料\n")
        parts.append("\n".join(web) + "\n\n")

    # Never output a bare placeholder bullet here; empty sources list is still allowed.
    if len(parts) == 1:
        parts.append("- (no sources extracted)\n")

    return "".join(parts).rstrip() + "\n"


def dedupe_preserve_order(items: Iterable[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for it in items:
        key = it.strip()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--base",
        default=None,
        help="Materials directory for ONE company (filings/PDF/etc). Optional if --ticker is provided.",
    )
    ap.add_argument(
        "--ticker",
        default=None,
        help="Stock ticker. If provided, used as output folder name and to validate base; also enables default base.",
    )
    ap.add_argument(
        "--materials-index",
        default=None,
        help=(
            "Optional index dir containing manifest.jsonl + toc.md (e.g. output/0883/index). "
            "When set, the script builds a per-chapter bundle.md and only feeds that bundle as local materials."
        ),
    )
    ap.add_argument(
        "--pack-top-k",
        type=int,
        default=0,
        help="Override toc top_k when building a chapter pack (0 = use toc).",
    )
    ap.add_argument(
        "--pack-neighbor-window",
        type=int,
        default=-1,
        help="Override toc neighbor_window when building a chapter pack (-1 = use toc).",
    )
    ap.add_argument(
        "--pack-max-total-chars",
        type=int,
        default=220_000,
        help="Max total chars in bundle.md when building a chapter pack.",
    )
    ap.add_argument(
        "--manifest-max-items",
        type=int,
        default=6,
        help="Max number of items to list in the base materials manifest (prompt anchor list).",
    )
    ap.add_argument(
        "--identity-index-top-n",
        type=int,
        default=IDENTITY_INDEX_EVIDENCE_MAX_ITEMS,
        help="Number of manifest/toc entries to use for identity inference when using materials index.",
    )
    ap.add_argument(
        "--protocol-restate-after",
        type=int,
        default=10,
        help="Send protocol restatement after this many cumulative audit failures (default: 10).",
    )
    ap.add_argument(
        "--write-blocked-max",
        type=int,
        default=10,
        help="Max consecutive write_blocked failures before aborting (default: 10).",
    )
    ap.add_argument("--company", default=None, help="Override inferred company name (used for report header/file name).")
    ap.add_argument(
        "--only-chapters",
        action="append",
        default=[],
        help="Only write these chapter titles (exact match). Repeatable or comma-separated.",
    )
    ap.add_argument("--max-attempts", type=int, default=2, help="Max attempts per chapter (initial + retries).")
    ap.add_argument(
        "--profile",
        default="balanced",
        choices=["fast", "balanced", "high", "deep"],
        help=(
            "Codex execution profile. "
            "fast: gpt-5.2 + low; "
            "balanced: gpt-5.2 + medium; "
            "high: gpt-5.2 + high; "
            "deep: gpt-5.2 + xhigh"
        ),
    )
    ap.add_argument(
        "--verbose",
        action="store_true",
        help="Echo Codex outputs (the final message for each step) to stdout.",
    )
    ap.add_argument("--dry-run", action="store_true", help="Print plan and exit.")
    ap.add_argument(
        "--dump-prompts",
        action="store_true",
        help=(
            "Generate and write Step0/1/2/4 prompts to disk, without calling Codex. "
            "Useful for prompt iteration/testing. Requires --ticker."
        ),
    )
    ap.add_argument(
        "--dump-prompts-dir",
        default=None,
        help=(
            "Optional output dir for --dump-prompts. "
            "Default: Reports/<TICKER>/_codex_logs/_dump_prompts/<timestamp>"
        ),
    )
    ap.add_argument(
        "--overview-input",
        choices=["condensed", "full"],
        default="condensed",
        help="What to feed into overview fill: condensed (default) or full report (may be very large).",
    )
    ap.add_argument(
        "--check",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "Run a full-report consistency check after assembling the final Markdown. "
            "Enabled by default; pass --no-check to disable."
        ),
    )

    args = ap.parse_args()

    prompt_self_check = PROMPTS_DIR / "agents_self_check.txt"
    prompt_write_chapter = PROMPTS_DIR / "write_chapter.txt"
    prompt_audit = PROMPTS_DIR / "audit_facts_tone_json.txt"
    prompt_fill_overview = PROMPTS_DIR / "fill_overview.txt"
    prompt_check_full_report = PROMPTS_DIR / "check_full_report_json.txt"
    prompt_protocol_restatement = PROMPTS_DIR / "_protocol_restatement.txt"
    prompt_infer_identity = PROMPTS_DIR / "infer_identity_json.txt"
    prompt_infer_identity_ticker = PROMPTS_DIR / "infer_identity_from_ticker_json.txt"

    required_prompts = [
        prompt_self_check,
        prompt_write_chapter,
        prompt_audit,
        prompt_fill_overview,
        prompt_protocol_restatement,
        prompt_infer_identity,
        prompt_infer_identity_ticker,
    ]
    if args.check:
        required_prompts.append(prompt_check_full_report)

    validate_project_layout(required_prompt_paths=required_prompts)

    expected_agents_sentinel = read_agents_sentinel()

    expected_ticker = args.ticker.strip().upper() if args.ticker else None

    if args.base:
        base_dir = (ROOT / args.base).resolve() if not os.path.isabs(args.base) else Path(args.base).resolve()
    else:
        base_dir = None
        if not expected_ticker:
            raise SystemExit("Missing --base (or provide --ticker to run without local materials).")

    _log_step(f"Resolve base dir: {base_dir if base_dir else '(none)'}")

    effective_profile = args.profile
    # if base_dir is None and expected_ticker and args.profile == "fast":
    #     effective_profile = "balanced"
    #     _log_step("Profile override: ticker-only run -> profile=balanced (reasoning_effort=medium)")

    codex_profile = resolve_codex_profile(effective_profile)

    _log_step(
        "Start run | "
        f"profile={codex_profile.name} model={codex_profile.model} reasoning_effort={codex_profile.reasoning_effort} "
        f"max_attempts={args.max_attempts}"
    )

    _log_step(f"Prompts dir: {PROMPTS_DIR}")
    if not TEMPLATE_PATH.exists():
        raise SystemExit(f"Missing template file: {TEMPLATE_PATH}")
    if not prompt_protocol_restatement.exists():
        raise SystemExit(
            f"Missing {prompt_protocol_restatement}. Run: python utils/sync_codex_from_guide.py"
        )

    if not prompt_infer_identity.exists():
        raise SystemExit(f"Missing {prompt_infer_identity}")

    # Pre-compute selection plan (no Codex calls).

    template_text = _read_text(TEMPLATE_PATH)
    template_preamble, template_footer = extract_template_disclaimers(template_text)
    all_chapters = [c for c in parse_template_chapters(template_text) if c.title not in _SKIP_NON_MIDDLE_CHAPTERS]
    only = normalize_only_chapters_arg(args.only_chapters)
    target_chapters = select_chapters(all_chapters, only)
    stop_after_chapters = bool(only)

    _log_step(f"Chapters selected: {len(target_chapters)}")
    for c in target_chapters:
        _log_step(f"- chapter: {c.title}")

    if args.dump_prompts:
        if not expected_ticker:
            raise SystemExit("--dump-prompts requires --ticker (no Codex inference is performed in dump mode).")

        ticker = expected_ticker
        company = args.company.strip() if args.company else ticker

        # Load prompt templates and protocol restatement.
        protocol_restatement = gen_protocol_restatement_prompt(
            protocol_restatement_text=_read_text(prompt_protocol_restatement)
        )
        write_template_text = _read_text(prompt_write_chapter)
        audit_template_text = _read_text(prompt_audit)
        fill_overview_template_text = _read_text(prompt_fill_overview)
        self_check_template_text = _read_text(prompt_self_check)
        infer_template_text = _read_text(prompt_infer_identity)
        infer_ticker_template_text = _read_text(prompt_infer_identity_ticker)

        # Build materials manifest (same logic as normal run, but no Codex calls).
        materials_manifest = build_base_materials_manifest(
            base_dir=base_dir,
            manifest_max_items=int(args.manifest_max_items),
        )

        # Resolve optional materials index (same auto-detect behavior).
        materials_index_dir = resolve_materials_index_dir(
            base_dir=base_dir,
            materials_index_arg=args.materials_index,
        )
        if materials_index_dir is not None and args.materials_index is None:
            _log_step(f"Auto-detected materials index: {materials_index_dir}")

        if args.dump_prompts_dir:
            dump_dir = (ROOT / args.dump_prompts_dir).resolve() if not os.path.isabs(args.dump_prompts_dir) else Path(args.dump_prompts_dir).resolve()
        else:
            dump_dir = ROOT / "Reports" / ticker / "_dump_prompts"

        _log_step(f"Dump prompts (no Codex) -> {dump_dir}")
        dump_prompts_to_dir(
            dump_dir=dump_dir,
            base_dir=base_dir,
            materials_manifest=materials_manifest,
            materials_index_dir=materials_index_dir,
            protocol_restatement=protocol_restatement,
            expected_agents_sentinel=expected_agents_sentinel,
            ticker=ticker,
            company=company,
            chapters=target_chapters,
            write_template_text=write_template_text,
            audit_template_text=audit_template_text,
            fill_overview_template_text=fill_overview_template_text,
            self_check_template_text=self_check_template_text,
            infer_template_text=infer_template_text,
            infer_ticker_template_text=infer_ticker_template_text,
            pack_top_k=int(args.pack_top_k),
            pack_neighbor_window=int(args.pack_neighbor_window),
            pack_max_total_chars=int(args.pack_max_total_chars),
            max_attempts=int(args.max_attempts),
            overview_input=str(args.overview_input),
            manifest_max_items=max(1, int(args.manifest_max_items)),
            identity_index_max_items=max(1, int(args.identity_index_top_n)),
        )

        print(f"Dumped prompts dir: {dump_dir}")
        return

    if args.dry_run:
        planned_ticker = expected_ticker or "(will infer)"
        planned_company = args.company.strip() if args.company else "(will infer)"
        planned_report_dir = ROOT / "Reports" / (expected_ticker or "_infer")
        _log_step("Dry-run: no Codex calls will be executed")
        print(f"Base: {base_dir if base_dir else '(none)'}")
        print(f"Ticker: {planned_ticker}")
        print(f"Company: {planned_company}")
        print(f"Report dir: {planned_report_dir}")
        print("Chapters:")
        for c in target_chapters:
            print(f"- {c.title}")
        return

    _log_step("Load protocol restatement + build materials manifest")
    protocol_restatement = gen_protocol_restatement_prompt(
        protocol_restatement_text=_read_text(prompt_protocol_restatement)
    )
    materials_manifest = build_base_materials_manifest(
        base_dir=base_dir,
        manifest_max_items=int(args.manifest_max_items),
    )

    materials_index_dir = resolve_materials_index_dir(
        base_dir=base_dir,
        materials_index_arg=args.materials_index,
    )
    if materials_index_dir is not None and args.materials_index is None:
        _log_step(f"Auto-detected materials index: {materials_index_dir}")

    identity_base_dir, identity_manifest, identity_evidence_dir = resolve_identity_materials(
        base_dir=base_dir,
        materials_index_dir=materials_index_dir,
        materials_manifest=materials_manifest,
        manifest_max_items=int(args.manifest_max_items),
    )
    if base_dir and materials_index_dir:
        _log_step(f"Identity inference will use materials index: {identity_evidence_dir}")

    # Create a temporary logs dir until we have the final ticker.
    temp_report_dir = ROOT / "Reports" / (expected_ticker or "_infer")
    temp_logs_dir = temp_report_dir / "_codex_logs"
    temp_logs_dir.mkdir(parents=True, exist_ok=True)

    if base_dir:
        _log_step(
            "Step 0: infer identity (ticker/company) from local materials"
            + (f" | expected_ticker={expected_ticker}" if expected_ticker else "")
        )
        infer_template_text = _read_text(prompt_infer_identity)
        identity = step_infer_identity_from_materials(
            base_dir=identity_base_dir,
            materials_manifest=identity_manifest,
            evidence_dir=identity_evidence_dir,
            expected_ticker=expected_ticker,
            logs_dir=temp_logs_dir,
            infer_template_text=infer_template_text,
            model=codex_profile.model,
            reasoning_effort=codex_profile.reasoning_effort,
            verbose=args.verbose,
            identity_index_max_items=max(1, int(args.identity_index_top_n)),
        )
    else:
        if not expected_ticker:
            raise SystemExit("Missing --ticker when no --base is provided.")
        _log_step("Step 0: infer identity (ticker/company) from ticker only")
        try:
            infer_template_text = _read_text(prompt_infer_identity_ticker)
            identity = step_infer_identity_from_ticker_only(
                expected_ticker=expected_ticker,
                logs_dir=temp_logs_dir,
                infer_template_text=infer_template_text,
                model=codex_profile.model,
                reasoning_effort=codex_profile.reasoning_effort,
                verbose=args.verbose,
            )
        except Exception:
            identity = {
                "ticker": expected_ticker,
                "company": args.company.strip() if args.company else expected_ticker,
                "base_matches_ticker": True,
                "mismatch_reason": None,
            }

    inferred_ticker = str(identity.get("ticker") or "").strip().upper()
    inferred_company = str(identity.get("company") or "").strip()

    _log_step(
        "Identity inference done | "
        f"inferred_ticker={inferred_ticker or '(empty)'} "
        f"inferred_company={inferred_company or '(empty)'}"
    )

    if expected_ticker and base_dir:
        matches = identity.get("base_matches_ticker")
        if matches is not True:
            reason = identity.get("mismatch_reason") or "(no reason)"
            raise SystemExit(
                f"--base materials do not appear to match --ticker={expected_ticker}.\n"
                f"Reason: {reason}\n"
                f"Inference: {json.dumps(identity, ensure_ascii=False, indent=2)}"
            )
        ticker = expected_ticker
    elif expected_ticker:
        ticker = expected_ticker
    else:
        if not inferred_ticker:
            raise SystemExit(
                "Could not infer ticker from --base materials. "
                "Pass --ticker explicitly or add clearer filings under --base.\n"
                f"Inference: {json.dumps(identity, ensure_ascii=False, indent=2)}"
            )
        ticker = inferred_ticker

    company = args.company.strip() if args.company else inferred_company
    if not company:
        company = ticker

    _log_step(f"Resolved identity | ticker={ticker} company={company}")

    report_dir = ROOT / "Reports" / ticker
    chapters_dir = report_dir / "chapters"
    logs_dir = report_dir / "_codex_logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    _log_step(f"Output dirs | report_dir={report_dir} | chapters_dir={chapters_dir} | logs_dir={logs_dir}")

    # Save identity decision for traceability.
    _write_text(logs_dir / "_identity.json", json.dumps(identity, ensure_ascii=False, indent=2) + "\n")
    _log_step(f"Wrote identity trace: {logs_dir / '_identity.json'}")

    _log_step("Step 1: agents self-check")
    self_check_template_text = _read_text(prompt_self_check)
    step_agents_self_check(
        self_check_template_text=self_check_template_text,
        logs_dir=logs_dir,
        expected_sentinel=expected_agents_sentinel,
        model=codex_profile.model,
        reasoning_effort=codex_profile.reasoning_effort,
        verbose=args.verbose,
    )
    _log_step(f"Self-check saved: {logs_dir / '_agents_self_check.txt'}")

    # 1) Write + audit chapters
    written: List[Tuple[Chapter, Path]] = []
    failed_audit_titles: List[str] = []
    audit_fail_count = 0
    write_blocked_count = 0
    protocol_restate_after = int(args.protocol_restate_after)
    write_blocked_max = int(args.write_blocked_max)

    def _on_audit_fail(audit_class: Optional[str]) -> None:
        nonlocal audit_fail_count
        nonlocal write_blocked_count
        audit_fail_count += 1
        if audit_class == AUDIT_CLASS_WRITE_BLOCKED:
            write_blocked_count += 1
            if write_blocked_max > 0 and write_blocked_count >= write_blocked_max:
                raise SystemExit(
                    f"write_blocked reached max attempts ({write_blocked_max}). "
                    "Aborting to avoid infinite retries; please provide required materials."
                )
            _log_step("Write blocked; sending protocol restatement to Codex immediately")
            audit_fail_count = 0  # reset counter after immediate restate
            step_protocol_restatement(
                protocol_restatement_text=protocol_restatement,
                logs_dir=logs_dir,
                model=codex_profile.model,
                reasoning_effort=codex_profile.reasoning_effort,
                verbose=args.verbose,
            )
            return
        if protocol_restate_after > 0 and audit_fail_count % protocol_restate_after == 0:
            _log_step(
                f"Audit failures reached {audit_fail_count}; sending protocol restatement to Codex"
            )
            step_protocol_restatement(
                protocol_restatement_text=protocol_restatement,
                logs_dir=logs_dir,
                model=codex_profile.model,
                reasoning_effort=codex_profile.reasoning_effort,
                verbose=args.verbose,
            )

    write_template_text = _read_text(prompt_write_chapter)
    audit_template_text = _read_text(prompt_audit)

    for chapter in target_chapters:
        safe_name = _sanitize_filename(chapter.title)
        chapter_path = chapters_dir / f"{safe_name}.md"

        _log_step(f"Step 2: write+audit chapter | title={chapter.title} | out={chapter_path}")

        passed, last_audit = step_write_and_audit_chapter(
            chapter=chapter,
            chapter_path=chapter_path,
            report_dir=report_dir,
            logs_dir=logs_dir,
            max_attempts=int(args.max_attempts),
            materials_index_dir=materials_index_dir,
            materials_manifest=materials_manifest,
            pack_top_k=int(args.pack_top_k),
            pack_neighbor_window=int(args.pack_neighbor_window),
            pack_max_total_chars=int(args.pack_max_total_chars),
            company=company,
            ticker=ticker,
            write_template_text=write_template_text,
            audit_template_text=audit_template_text,
            model=codex_profile.model,
            reasoning_effort=codex_profile.reasoning_effort,
            verbose=args.verbose,
            on_audit_fail=_on_audit_fail,
        )
        written.append((chapter, chapter_path))
        if not passed:
            failed_audit_titles.append(chapter.title)

    if stop_after_chapters:
        _log_step("Only-chapters mode: stopping after chapter outputs (skip assemble/fill/sources/final report)")
        print(f"Chapters dir: {chapters_dir}")
        print(f"Logs dir: {logs_dir}")
        for chapter, chapter_path in written:
            print(f"Wrote chapter: {chapter.title} | {chapter_path}")
        _log_step(f"write_blocked count: {write_blocked_count} (max={write_blocked_max})")
        return

    # 2) Assemble full report in template order (use latest written if present; else skip)
    _log_step("Step 3: assemble full report (template order)")
    chapter_by_title = {c.title: p for c, p in written}
    assembled_parts: List[str] = []
    for c in all_chapters:
        p = chapter_by_title.get(c.title)
        if p and p.exists():
            assembled_parts.append(_read_text(p).rstrip() + "\n\n")

    full_body = "".join(assembled_parts).strip() + "\n"

    _log_step(f"Assembled chapters included: {len(assembled_parts)}")

    # 3) Fill overview (run after middle chapters are written)
    _log_step(f"Step 4: fill overview | input={args.overview_input}")
    if args.overview_input == "full":
        overview_input_text = full_body
    else:
        # Condensed: keep just each chapter title + 结论要点 section + 证据 headings.
        chunks: List[str] = []
        for c, p in written:
            md = _read_text(p)
            chunks.append(f"## {c.title}\n")
            # Keep the first ~1200 chars as a cheap "conclusion-ish" proxy.
            chunks.append(md[:1200] + ("\n…\n" if len(md) > 1200 else "\n"))
        overview_input_text = "\n".join(chunks)

    fill_template_text = _read_text(prompt_fill_overview)
    overview_md, _overview_path = step_fill_overview(
        overview_input=str(args.overview_input),
        full_body=full_body,
        written=written,
        chapters_dir=chapters_dir,
        logs_dir=logs_dir,
        fill_overview_template_text=fill_template_text,
        model=codex_profile.model,
        reasoning_effort=codex_profile.reasoning_effort,
        verbose=args.verbose,
    )
    # Ensure it is included in assembled output (put it first)
    full_body = overview_md.rstrip() + "\n\n" + full_body

    # 4) Generate sources list from chapters' 证据与出处
    _log_step("Step 5: build de-duplicated sources list")
    source_bullets: List[str] = []
    for _, p in written:
        source_bullets.extend(extract_sources_block(_read_text(p)))
    sources_md = build_sources_chapter_from_evidence_blocks(source_bullets)
    extracted_count = len([l for l in sources_md.splitlines() if l.strip().startswith("-")])
    _log_step(f"Sources entries (file/URL-level): {extracted_count}")

    # 5) Write final report
    _log_step("Step 6: write final report")
    report_path = report_dir / f"{_sanitize_filename(company)}全貌梳理.md"
    header = f"# {company} 全貌梳理\n\n"
    meta = (
        f"<!-- Generated: {datetime.now().isoformat(timespec='seconds')} -->\n"
        f"<!-- Base: {base_dir if base_dir else '(none)'} -->\n\n"
    )
    pre = fill_disclaimer_placeholders(template_preamble, company=company, ticker=ticker)
    footer = fill_disclaimer_placeholders(template_footer, company=company, ticker=ticker)

    final_md = header + meta + (pre if pre else "") + full_body.strip() + "\n\n" + sources_md
    if footer:
        final_md = final_md.rstrip() + "\n\n" + footer.strip() + "\n"
    else:
        final_md = final_md.rstrip() + "\n"

    # Always persist the report, regardless of any later check outcome.
    _write_text(report_path, final_md)

    if args.check:
        _log_step("Step 7: full-report consistency check")
        try:
            check_template = _read_text(prompt_check_full_report)
            check_body = fill_template(check_template, {"FULL_REPORT_MARKDOWN": final_md})
            check_prompt = check_body
            check_out_path = logs_dir / "check_full_report_last_message.txt"
            check_text = run_codex(
                check_prompt,
                check_out_path,
                model=codex_profile.model,
                reasoning_effort=codex_profile.reasoning_effort,
                verbose=args.verbose,
                label="check_full_report",
            )
            _write_text(logs_dir / "_check_full_report_raw.txt", check_text)
            try:
                check_json = parse_audit_json(check_text)
            except Exception as e:  # noqa: BLE001
                _log_step(f"Check parse failed: {e}")
                check_json = {"pass": False, "issues": [], "notes": [f"check output not valid JSON: {e}"]}
            _write_text(
                logs_dir / "_check_full_report.json", json.dumps(check_json, ensure_ascii=False, indent=2) + "\n"
            )
            if check_json.get("pass") is True:
                _log_step("Check PASS")
            else:
                _log_step("Check FAIL (see _check_full_report.json)")
        except Exception as e:  # noqa: BLE001
            _log_step(f"Check failed to run (non-fatal): {e}")

    print(f"Wrote report: {report_path}")
    print(f"Chapters dir: {chapters_dir}")
    print(f"Logs dir: {logs_dir}")
    if failed_audit_titles:
        _log_step("Chapters still failing audit after retries:")
        for title in failed_audit_titles:
            print(f"- {title}")
    _log_step(f"write_blocked count: {write_blocked_count} (max={write_blocked_max})")
    _log_step("Done")


if __name__ == "__main__":
    main()
