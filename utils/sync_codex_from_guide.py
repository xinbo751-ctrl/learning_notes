#!/usr/bin/env python3
"""Sync Codex instruction assets from GUIDE.md.

Why this exists
--------------
You want GUIDE.md to be the single source of truth. When GUIDE changes, run:

    python utils/sync_codex_from_guide.py

This script extracts the "4. 开场必发：协议注入 + 全局硬约束" code block from GUIDE.md
and updates:
- Codex/prompts/_protocol_from_guide.txt (raw protocol text)
- AGENTS.md (project instructions Codex will load)
- Codex/prompts/* (all prompt templates used by the driver)

Prompt templates reference {{PROTOCOL_RESTATEMENT}} and should be filled by the
caller (or you can paste the protocol manually). Keeping the protocol in a
separate file makes drift recovery consistent.
"""

from __future__ import annotations

import hashlib
import re
import textwrap
from pathlib import Path
from string import Template


ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "GUIDE.md"
OUT_AGENTS_ROOT = ROOT / "AGENTS.md"

OUT_PROMPTS_DIR = ROOT / "Codex/prompts"
TEMPLATES_DIR = ROOT / "Codex/template"

OUT_PROTOCOL = OUT_PROMPTS_DIR / "_protocol_from_guide.txt"
OUT_PROTOCOL_RESTATEMENT = OUT_PROMPTS_DIR / "_protocol_restatement.txt"
OUT_AUDIT_PROMPT = OUT_PROMPTS_DIR / "audit_facts_tone_json.txt"
OUT_AGENTS_SELF_CHECK = OUT_PROMPTS_DIR / "agents_self_check.txt"
OUT_INFER_IDENTITY = OUT_PROMPTS_DIR / "infer_identity_json.txt"
OUT_INFER_IDENTITY_TICKER = OUT_PROMPTS_DIR / "infer_identity_from_ticker_json.txt"
OUT_WRITE_CHAPTER = OUT_PROMPTS_DIR / "write_chapter.txt"
OUT_FIX_PLACEHOLDERS = OUT_PROMPTS_DIR / "fix_placeholders.txt"
OUT_FILL_OVERVIEW = OUT_PROMPTS_DIR / "fill_overview.txt"
OUT_CHECK_FULL_REPORT = OUT_PROMPTS_DIR / "check_full_report_json.txt"


# NOTE:
# GUIDE.md contains multiple ```text blocks (write templates, examples, etc).
# Per repo protocol, we ONLY sync from section 4: "开场必发：协议注入 + 全局硬约束".
_OPENING_PROTOCOL_RE = re.compile(
    r"##\s*4\.\s*开场必发：协议注入\s*\+\s*全局硬约束[\s\S]*?\n```text\n(?P<body>[\s\S]*?)\n```",
    re.MULTILINE,
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _read_template(name: str) -> str:
    path = TEMPLATES_DIR / name
    if not path.exists():
        raise SystemExit(
            f"Missing template file: {path}. "
            "Create it under Codex/template/ (source templates) then rerun sync."
        )
    return _read_text(path)


def _render_template(template: str, /, **mapping: str) -> str:
    """Render a large template string.

    We use string.Template ($NAME) to avoid conflicts with the prompt placeholders
    like {{CHAPTER_MARKDOWN}} which must remain verbatim for later filling.
    """
    body = textwrap.dedent(template).lstrip("\n")
    return Template(body).safe_substitute(**mapping)


def extract_protocol_from_guide(guide_text: str) -> str:
    match = _OPENING_PROTOCOL_RE.search(guide_text)
    if not match:
        raise SystemExit(
            "Could not find the protocol block in GUIDE.md. "
            "Expected the opening section '## 4. 开场必发：协议注入 + 全局硬约束' "
            "followed by a ```text fenced block."
        )
    body = match.group("body").strip("\n")
    if not body.strip():
        raise SystemExit("Found opening protocol block, but it is empty.")
    return body + "\n"


def build_agents_md(protocol_text: str) -> str:
    # Keep this file short and stable; the authoritative protocol is embedded below.
    protocol_hash = hashlib.sha256(protocol_text.encode("utf-8")).hexdigest()[:12]
    sentinel_line = f"AGENTS_SENTINEL: {protocol_hash}"
    template = _read_template("agents_md.tmpl")
    return _render_template(template, SENTINEL_LINE=sentinel_line, PROTOCOL_TEXT=protocol_text)


def build_protocol_restatement(protocol_text: str) -> str:
    template = _read_template("protocol_restatement.tmpl")
    return _render_template(template, PROTOCOL_TEXT=protocol_text)


def build_agents_self_check_prompt() -> str:
    # Plain-text output on purpose: robust and machine-checkable.
    return _read_template("agents_self_check.txt")


def build_infer_identity_prompt() -> str:
    return _read_template("infer_identity_json.tmpl")


def build_infer_identity_from_ticker_prompt() -> str:
    return _read_template("infer_identity_from_ticker_json.tmpl")


def build_write_chapter_prompt() -> str:
    return _read_template("write_chapter.tmpl")


def build_fix_placeholders_prompt() -> str:
    return _read_template("fix_placeholders.tmpl")


def build_fill_overview_prompt() -> str:
    return _read_template("fill_overview.tmpl")


def build_check_full_report_prompt() -> str:
    return _read_template("check_full_report_json.tmpl")


def _extract_section(protocol_text: str, start_marker: str, end_marker: str) -> str:
    start = protocol_text.find(start_marker)
    if start < 0:
        raise SystemExit(f"Could not find section start marker in protocol: {start_marker!r}")
    end = protocol_text.find(end_marker, start)
    if end < 0:
        raise SystemExit(f"Could not find section end marker in protocol: {end_marker!r}")
    return protocol_text[start:end]


_RULE_LINE_RE = re.compile(r"^\s*(?P<id>\d+(?:\.\d+)*)\)\s*(?P<rest>.*)\s*$")


def _normalize_rule_text(lines: list[str]) -> str:
    joined = " ".join(line.strip() for line in lines if line.strip())
    joined = re.sub(r"\s+", " ", joined).strip()
    return joined


def extract_facts_tone_rules(protocol_text: str) -> dict[str, str]:
    section = _extract_section(protocol_text, "【事实与语气】", "【证据规则】")
    lines = section.splitlines()

    rules: dict[str, list[str]] = {}
    current_id: str | None = None

    for line in lines:
        match = _RULE_LINE_RE.match(line)
        if match:
            current_id = match.group("id")
            rules[current_id] = [match.group("rest")]
            continue

        if current_id is None:
            continue

        # Continuation lines for the current rule (including indented sub-bullets).
        # Stop conditions are handled implicitly by the next rule header match.
        if line.strip():
            rules[current_id].append(line)

    return {rule_id: _normalize_rule_text(text_lines) for rule_id, text_lines in rules.items()}


def build_audit_facts_tone_prompt(protocol_text: str) -> str:
    # Audit scope is intentionally narrower than the full protocol.
    audited_rule_ids = ["2", "2.1", "2.2", "2.3", "2.4", "2.5", "2.6"]
    rules = extract_facts_tone_rules(protocol_text)

    missing = [rule_id for rule_id in audited_rule_ids if rule_id not in rules]
    if missing:
        raise SystemExit(
            "Protocol facts/tone rules missing in GUIDE.md protocol block: "
            + ", ".join(missing)
            + ". Please ensure those rule headers exist as 'X)' lines under '【事实与语气】'."
        )

    rules_joined = "|".join(audited_rule_ids)
    audit_lines = [f"- {rule_id}) {rules[rule_id]}（命中则列出片段）" for rule_id in audited_rule_ids]
    audit_block = "\n".join(audit_lines)

    template = _read_template("audit_facts_tone_json.tmpl")
    return _render_template(template, RULES_JOINED=rules_joined, AUDIT_BLOCK=audit_block)


def main() -> None:
    guide_text = _read_text(GUIDE)
    protocol = extract_protocol_from_guide(guide_text)

    protocol_restatement = build_protocol_restatement(protocol)
    audit_prompt = build_audit_facts_tone_prompt(protocol)
    agents_md = build_agents_md(protocol)
    agents_self_check = build_agents_self_check_prompt()
    infer_identity = build_infer_identity_prompt()
    infer_identity_ticker = build_infer_identity_from_ticker_prompt()
    write_chapter = build_write_chapter_prompt()
    fix_placeholders = build_fix_placeholders_prompt()
    fill_overview = build_fill_overview_prompt()
    check_full_report = build_check_full_report_prompt()

    # Single source of truth: only write the raw protocol under Codex/.
    _write_text(OUT_PROTOCOL, protocol)
    _write_text(OUT_PROTOCOL_RESTATEMENT, protocol_restatement)
    _write_text(OUT_AUDIT_PROMPT, audit_prompt)
    _write_text(OUT_AGENTS_ROOT, agents_md)
    _write_text(OUT_AGENTS_SELF_CHECK, agents_self_check)
    _write_text(OUT_INFER_IDENTITY, infer_identity)
    _write_text(OUT_INFER_IDENTITY_TICKER, infer_identity_ticker)
    _write_text(OUT_WRITE_CHAPTER, write_chapter)
    _write_text(OUT_FIX_PLACEHOLDERS, fix_placeholders)
    _write_text(OUT_FILL_OVERVIEW, fill_overview)
    _write_text(OUT_CHECK_FULL_REPORT, check_full_report)

    print("Synced:")
    print(f"- {OUT_PROTOCOL.relative_to(ROOT)}")
    print(f"- {OUT_PROTOCOL_RESTATEMENT.relative_to(ROOT)}")
    print(f"- {OUT_AUDIT_PROMPT.relative_to(ROOT)}")
    print(f"- {OUT_AGENTS_ROOT.relative_to(ROOT)}")
    print(f"- {OUT_AGENTS_SELF_CHECK.relative_to(ROOT)}")
    print(f"- {OUT_INFER_IDENTITY.relative_to(ROOT)}")
    print(f"- {OUT_INFER_IDENTITY_TICKER.relative_to(ROOT)}")
    print(f"- {OUT_WRITE_CHAPTER.relative_to(ROOT)}")
    print(f"- {OUT_FIX_PLACEHOLDERS.relative_to(ROOT)}")
    print(f"- {OUT_FILL_OVERVIEW.relative_to(ROOT)}")
    print(f"- {OUT_CHECK_FULL_REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
