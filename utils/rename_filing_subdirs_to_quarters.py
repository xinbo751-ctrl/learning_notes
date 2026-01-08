#!/usr/bin/env python3
"""Rename SEC filing subdirectories to `YYYYQn` (e.g., 2022Q1).

Designed for cases like `filings/CME_copy/*` where subdirs are named:
  10-Q_2024-05-01_report_2024-03-31_0001156375-24-000072/

It reads `meta.json` (preferred) to get `reportDate`, then derives quarter from
that date.

By default this script only renames filings whose `reportDate` is a standard
quarter/year-end (03-31/06-30/09-30/12-31). This avoids mislabeling foreign
issuer 6-K filings where `reportDate` is often the event/filing date.

Default is dry-run; pass `--apply` to actually rename.

Examples:
  python utils/rename_filing_subdirs_to_quarters.py --base filings/CME_copy
  python utils/rename_filing_subdirs_to_quarters.py --base filings/CME_copy --apply

Notes:
- 10-K typically maps to Q4 via reportDate (often 12-31).
- If multiple filings map to the same quarter, suffixes are added: 2022Q1_2.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional


_QUARTER_DIR_RE = re.compile(r"^(?P<year>\d{4})Q(?P<q>[1-4])(?:_\d+)?$")


@dataclass(frozen=True)
class FilingInfo:
    path: Path
    report_end: date
    form: Optional[str]
    accession: Optional[str]


def _parse_iso_date(s: str) -> date:
    # s is expected like '2024-03-31'
    y, m, d = s.split("-")
    return date(int(y), int(m), int(d))


def _infer_quarter(d: date) -> int:
    return ((d.month - 1) // 3) + 1


def _is_standard_quarter_end(d: date) -> bool:
    # SEC meta.json `reportDate` is usually the period end for 10-Q/10-K/20-F,
    # but for many 6-K filings it's just the event/filing date.
    return (d.month, d.day) in {(3, 31), (6, 30), (9, 30), (12, 31)}


def _read_meta(filing_dir: Path) -> Optional[dict]:
    mp = filing_dir / "meta.json"
    if not mp.exists():
        return None
    try:
        return json.loads(mp.read_text(encoding="utf-8"))
    except Exception:
        return None


def _infer_report_end_from_dirname(name: str) -> Optional[date]:
    # Fallback: parse ..._report_YYYY-MM-DD_...
    m = re.search(r"_report_(\d{4}-\d{2}-\d{2})_", name)
    if not m:
        return None
    try:
        return _parse_iso_date(m.group(1))
    except Exception:
        return None


def _load_filing_info(*, filing_dir: Path, only_standard_period_ends: bool) -> Optional[FilingInfo]:
    if not filing_dir.is_dir():
        return None

    # Skip already-renamed quarter dirs.
    if _QUARTER_DIR_RE.match(filing_dir.name):
        return None

    meta = _read_meta(filing_dir)
    report_end: Optional[date] = None
    form: Optional[str] = None
    accession: Optional[str] = None

    if meta:
        rd = meta.get("reportDate") or meta.get("report_end") or meta.get("reportEnd")
        if isinstance(rd, str):
            try:
                report_end = _parse_iso_date(rd)
            except Exception:
                report_end = None
        form = meta.get("form") if isinstance(meta.get("form"), str) else None
        accession = meta.get("accessionNumber") if isinstance(meta.get("accessionNumber"), str) else None

    if report_end is None:
        report_end = _infer_report_end_from_dirname(filing_dir.name)

    if report_end is None:
        return None

    if only_standard_period_ends and not _is_standard_quarter_end(report_end):
        # Common for foreign issuers: 6-K reportDate == filing date.
        # Renaming those to YYYYQn would be misleading, so we skip them by default.
        return None

    return FilingInfo(path=filing_dir, report_end=report_end, form=form, accession=accession)


def _pick_unique_target_name(base: Path, desired: str) -> str:
    # Avoid collisions with existing dirs.
    if not (base / desired).exists():
        return desired
    i = 2
    while True:
        cand = f"{desired}_{i}"
        if not (base / cand).exists():
            return cand
        i += 1


def main() -> None:
    ap = argparse.ArgumentParser(description="Rename filing subdirs to YYYYQn format")
    ap.add_argument(
        "--base",
        required=True,
        help="Base directory whose immediate subdirectories will be renamed (e.g., filings/CME_copy)",
    )
    ap.add_argument(
        "--apply",
        action="store_true",
        help="Actually perform renames (default is dry-run)",
    )
    ap.add_argument(
        "--include-nonstandard-period-ends",
        dest="only_standard_period_ends",
        action="store_false",
        help=(
            "Include filings whose reportDate is NOT a standard period end (03-31/06-30/09-30/12-31). "
            "This is usually NOT what you want for foreign issuer 6-K event filings."
        ),
    )
    ap.set_defaults(only_standard_period_ends=True)
    args = ap.parse_args()

    base = Path(args.base)
    if not base.exists() or not base.is_dir():
        raise SystemExit(f"Base directory not found or not a directory: {base}")

    infos: list[FilingInfo] = []
    for p in sorted(base.iterdir(), key=lambda x: x.name):
        info = _load_filing_info(filing_dir=p, only_standard_period_ends=bool(args.only_standard_period_ends))
        if info is not None:
            infos.append(info)

    if not infos:
        print("No eligible filing subdirectories found (already renamed or missing meta/reportDate).")
        return

    # Deterministic order: by report_end then accession then name.
    infos.sort(key=lambda i: (i.report_end, i.accession or "", i.path.name))

    # Build rename plan with collision-safe targets.
    plan: list[tuple[Path, Path]] = []
    used_targets: set[str] = set()

    for info in infos:
        y = info.report_end.year
        q = _infer_quarter(info.report_end)
        desired = f"{y}Q{q}"

        # If multiple filings map to same quarter, ensure uniqueness.
        target_name = desired
        if target_name in used_targets or (base / target_name).exists():
            target_name = _pick_unique_target_name(base, desired)
        used_targets.add(target_name)

        plan.append((info.path, base / target_name))

    # Print plan.
    print(f"Base: {base}")
    print(f"Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    for src, dst in plan:
        print(f"{src.name}  ->  {dst.name}")

    if not args.apply:
        print("\nDry-run only. Re-run with --apply to perform the renames.")
        return

    # Two-phase rename to avoid accidental collisions.
    tmp_pairs: list[tuple[Path, Path]] = []
    for idx, (src, dst) in enumerate(plan, start=1):
        tmp = base / f"__tmp_rename__{idx:04d}__{src.name}"
        if tmp.exists():
            raise SystemExit(f"Temp path already exists; aborting: {tmp}")
        tmp_pairs.append((src, tmp))

    for src, tmp in tmp_pairs:
        src.rename(tmp)

    for (_src, tmp), (_orig_src, final_dst) in zip(tmp_pairs, plan):
        if final_dst.exists():
            raise SystemExit(f"Target already exists after temp rename; aborting: {final_dst}")
        tmp.rename(final_dst)

    print(f"\nRenamed {len(plan)} directories.")


if __name__ == "__main__":
    main()
