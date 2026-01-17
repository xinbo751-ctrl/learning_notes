#!/usr/bin/env python3
"""marker_extract.py
Convert single or batch PDFs via marker-pdf into LLM-ready outputs (chunks + html).
"""

from __future__ import annotations

import argparse
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List


def _log(message: str) -> None:
    print(message)


def _safe_slug(name: str) -> str:
    name = name.strip()
    name = re.sub(r"\s+", " ", name)
    name = re.sub(r"[\\/]+", "_", name)
    name = re.sub(r"[^\w\s.-]+", "_", name)
    name = name.strip(" ._-")
    return name or "pdf"


def _ensure_marker_single() -> None:
    if shutil.which("marker_single") is None:
        raise SystemExit(
            "Error: marker_single not found in PATH.\nInstall: pip install marker-pdf"
        )


def _parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Convert single or batch PDFs via marker-pdf (chunks + html)."
    )
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--filing", type=str, help="Single PDF file path")
    g.add_argument("--base", type=str, help="Directory containing PDF files")
    ap.add_argument("--output", type=str, default="./output", help="Output directory (default: ./output)")
    ap.add_argument("--ollama", action="store_true", help="Enable local Ollama via marker's OllamaService")
    ap.add_argument("--model", type=str, default="deepseek-r1:8b", help="Ollama model name (default: deepseek-r1:8b)")
    return ap.parse_args()


def _validate_inputs(args: argparse.Namespace) -> None:
    if args.filing:
        pdf_path = Path(args.filing).expanduser()
        if not pdf_path.is_file():
            raise SystemExit(f"Error: --filing file does not exist: {pdf_path}")
        if pdf_path.suffix.lower() != ".pdf":
            raise SystemExit(f"Error: --filing must be a .pdf file: {pdf_path}")
    if args.base:
        base_dir = Path(args.base).expanduser()
        if not base_dir.is_dir():
            raise SystemExit(f"Error: --base directory does not exist: {base_dir}")


def _build_llm_args(use_llm: bool, model: str, ollama_base_url: str) -> List[str]:
    if not use_llm:
        return []
    return [
        "--use_llm",
        "--llm_service",
        "marker.services.ollama.OllamaService",
        "--ollama_base_url",
        ollama_base_url,
        "--ollama_model",
        model,
    ]


def _run_marker_single(
    pdf: Path,
    output_dir: Path,
    output_format: str,
    llm_args: List[str],
    force_ocr: bool,
    extra_args: List[str],
) -> None:
    cmd = [
        "marker_single",
        str(pdf),
        "--output_dir",
        str(output_dir),
        "--output_format",
        output_format,
    ]
    if llm_args:
        cmd.extend(llm_args)
    if force_ocr:
        cmd.append("--force_ocr")
    if extra_args:
        cmd.extend(extra_args)

    subprocess.run(cmd, check=True)


def _process_one_pdf(
    pdf: Path,
    out_dir: Path,
    llm_args: List[str],
    force_ocr: bool,
    extra_args: List[str],
) -> None:
    filename = pdf.name
    out_dir.mkdir(parents=True, exist_ok=True)

    _log(f"=== Processing: {filename}")
    _log(f"-> Source:      {pdf}")
    _log(f"-> Output to:   {out_dir}")

    _run_marker_single(pdf, out_dir, "chunks", llm_args, force_ocr, extra_args)
    _run_marker_single(pdf, out_dir, "html", llm_args, force_ocr, extra_args)

    _log(f"Done: {filename}\n")


def main() -> int:
    args = _parse_args()
    _validate_inputs(args)
    _ensure_marker_single()

    output_root = Path(args.output).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    torch_device = os.environ.get("TORCH_DEVICE", "mps")
    os.environ["TORCH_DEVICE"] = torch_device

    ollama_base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    force_ocr = os.environ.get("MARKER_FORCE_OCR", "0") == "1"
    extra_args = shlex.split(os.environ.get("MARKER_EXTRA_ARGS", ""))

    llm_args = _build_llm_args(args.ollama, args.model, ollama_base_url)

    _log(f"Output root       : {output_root}")
    _log(f"TORCH_DEVICE      : {torch_device}")
    _log(f"OLLAMA_BASE_URL   : {ollama_base_url}")
    _log(f"Use LLM           : {1 if args.ollama else 0}")
    _log(f"Model             : {args.model if args.ollama else '<disabled>'}")
    _log(f"MARKER_FORCE_OCR  : {1 if force_ocr else 0}")
    _log("")

    if args.filing:
        pdf = Path(args.filing).expanduser().resolve()
        out_dir = output_root / _safe_slug(pdf.stem)
        _process_one_pdf(pdf, out_dir, llm_args, force_ocr, extra_args)
        _log(f"All done. Outputs in: {out_dir}")
        return 0

    base_dir = Path(args.base).expanduser().resolve()
    if args.output == "./output":
        out_root = output_root / _safe_slug(base_dir.name)
    else:
        out_root = output_root
    out_root.mkdir(parents=True, exist_ok=True)
    pdfs = sorted([p for p in base_dir.glob("*.pdf")] + [p for p in base_dir.glob("*.PDF")])
    if not pdfs:
        print(f"No PDF files found in: {base_dir}", file=sys.stderr)
        return 2

    _log(f"Base dir          : {base_dir}")
    _log(f"PDF count         : {len(pdfs)}")
    _log("")

    for pdf in pdfs:
        out_dir = out_root / _safe_slug(pdf.stem)
        _process_one_pdf(pdf, out_dir, llm_args, force_ocr, extra_args)

    _log(f"All done. Outputs in: {out_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
