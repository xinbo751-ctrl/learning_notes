#!/usr/bin/env python3
"""Render Markdown to HTML/PDF/Word using pandoc + Chrome.

Usage:
  python utils/render.py <input_markdown> [output_path]
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _copy_render_assets(repo_root: Path, output_root: Path) -> None:
    media_dir = output_root / "media"
    _ensure_dir(media_dir)
    shutil.copyfile(repo_root / "render" / "github-markdown.css", media_dir / "github-markdown.css")
    shutil.copyfile(repo_root / "render" / "before.html", media_dir / "before.html")
    shutil.copyfile(repo_root / "render" / "after.html", media_dir / "after.html")


def _inline_css(target_html: Path, media_dir: Path, *, add_img_style: bool = False) -> None:
    inline_start = "<!-- INLINE_GITHUB_MARKDOWN_CSS_START -->"
    inline_end = "<!-- INLINE_GITHUB_MARKDOWN_CSS_END -->"
    img_style_block = "<style>img{max-width:100%;height:auto;}</style>"

    html = target_html.read_text(encoding="utf-8")
    css = (media_dir / "github-markdown.css").read_text(encoding="utf-8")
    inline_css_block = f"{inline_start}\n<style>\n{css}\n</style>\n{inline_end}"

    if inline_start in html and inline_end in html:
        start = html.index(inline_start)
        end = html.index(inline_end) + len(inline_end)
        html = html[:start] + inline_css_block + html[end:]
    else:
        link_patterns = [
            '<link rel="stylesheet" href="media/github-markdown.css" />',
            '<link rel="stylesheet" href="media/github-markdown.css"/>',
            '<link rel="stylesheet" href="./media/github-markdown.css" />',
            '<link rel="stylesheet" href="./media/github-markdown.css"/>',
        ]
        replaced = False
        for pattern in link_patterns:
            if pattern in html:
                html = html.replace(pattern, inline_css_block, 1)
                replaced = True
                break
        if not replaced:
            if "</head>" in html:
                html = html.replace("</head>", f"{inline_css_block}\n</head>", 1)
            else:
                html = inline_css_block + "\n" + html

    if add_img_style and img_style_block not in html:
        if "</head>" in html:
            html = html.replace("</head>", f"  {img_style_block}\n</head>", 1)
        else:
            html += "\n" + img_style_block + "\n"

    target_html.write_text(html, encoding="utf-8")


def _run_pandoc(args: list[str], *, cwd: Path) -> None:
    subprocess.run(["pandoc", *args], check=True, cwd=str(cwd))


def _generate_html(input_md: Path, target_html: Path, repo_root: Path) -> None:
    output_root = repo_root / "output"
    _copy_render_assets(repo_root, output_root)

    _run_pandoc(
        [
            str(input_md),
            "--lua-filter=../render/diagram.lua",
            "--extract-media=./media",
            "-f",
            "gfm",
            "-t",
            "html5",
            "-s",
            "--css=./media/github-markdown.css",
            "--include-before-body=./media/before.html",
            "--include-after-body=./media/after.html",
            "--embed-resources",
            "-o",
            str(target_html),
        ],
        cwd=output_root,
    )

    _inline_css(target_html, output_root / "media")


def _generate_word(input_md: Path, target_path: Path, repo_root: Path) -> None:
    output_root = repo_root / "output"
    _copy_render_assets(repo_root, output_root)

    _run_pandoc(
        [
            str(input_md),
            "--lua-filter=../render/diagram.lua",
            "--extract-media=./media",
            "-f",
            "gfm",
            "-s",
            "--embed-resources",
            "--reference-doc=../render/reference.docx",
            "-o",
            str(target_path),
        ],
        cwd=output_root,
    )


def _generate_generic(input_md: Path, target_path: Path, repo_root: Path) -> None:
    output_root = repo_root / "output"
    _copy_render_assets(repo_root, output_root)

    _run_pandoc(
        [
            str(input_md),
            "--lua-filter=../render/diagram.lua",
            "--extract-media=./media",
            "-f",
            "gfm",
            "-s",
            "--embed-resources",
            "--css=./media/github-markdown.css",
            "-o",
            str(target_path),
        ],
        cwd=output_root,
    )


def _find_chrome_binary() -> str:
    chrome_bin = os.environ.get("PUPPETEER_EXECUTABLE_PATH", "").strip()
    if not chrome_bin:
        if shutil.which("google-chrome"):
            chrome_bin = shutil.which("google-chrome") or ""
        elif Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome").is_file():
            chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    if not chrome_bin or not Path(chrome_bin).is_file():
        raise SystemExit(
            "Chrome binary not found. Set PUPPETEER_EXECUTABLE_PATH or install Google Chrome."
        )
    return chrome_bin


def _convert_html_to_pdf(html_path: Path, pdf_path: Path) -> None:
    chrome_bin = _find_chrome_binary()
    html_uri = html_path.resolve().as_uri()
    chrome_args = [
        "--headless",
        "--disable-gpu",
        "--disable-background-networking",
        "--disable-default-apps",
        "--disable-component-update",
        "--disable-client-side-phishing-detection",
        "--disable-features=TranslateUI",
        "--disable-sync",
        "--disable-extensions",
        "--metrics-recording-only",
        "--password-store=basic",
        "--use-mock-keychain",
        "--no-first-run",
        "--no-default-browser-check",
        "--incognito",
        "--bwsi",
        "--disable-logging",
        "--log-level=3",
        "--disable-popup-blocking",
        "--disable-notifications",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=10000",
        f"--print-to-pdf={pdf_path}",
        "--print-to-pdf-no-header",
        "--no-pdf-header-footer",
        html_uri,
    ]

    subprocess.run([chrome_bin, *chrome_args], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _open_file(path: Path) -> None:
    try:
        if sys.platform.startswith("darwin"):
            subprocess.run(["open", str(path)], check=False)
        elif sys.platform.startswith("linux"):
            subprocess.run(["xdg-open", str(path)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sys.platform.startswith("win"):
            os.startfile(str(path))  # type: ignore[attr-defined]
        else:
            print(f"Generated file: {path}", file=sys.stderr)
    except Exception:
        print(f"Generated file: {path}", file=sys.stderr)


def _normalize_ext(path: Path) -> str:
    return path.suffix.lower().lstrip(".")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python utils/render.py <input_markdown> [output_html]", file=sys.stderr)
        return 1

    script_dir = Path(__file__).resolve().parent
    repo_root = (script_dir / "..").resolve()
    if not (repo_root / "render").is_dir():
        raise SystemExit(f"render directory not found: {repo_root / 'render'}")
    os.chdir(repo_root)

    input_md_raw = Path(sys.argv[1])
    input_md = input_md_raw.expanduser().resolve()
    if not input_md.is_file():
        print(f"Input markdown not found: {input_md}", file=sys.stderr)
        return 1

    if len(sys.argv) >= 3:
        output_path_raw = Path(sys.argv[2])
    else:
        output_path_raw = Path("output") / f"{input_md.stem}.html"

    output_dir = output_path_raw.expanduser().parent
    _ensure_dir(output_dir)
    output_path = output_path_raw.expanduser().resolve()

    ext = _normalize_ext(output_path)
    is_html = ext in {"html", "htm"}
    is_pdf = ext == "pdf"
    is_word = ext in {"docx", "doc"}

    html_target = output_path
    if is_pdf:
        html_target = output_path.with_suffix(".html")
        _ensure_dir(html_target.parent)

    _ensure_dir(repo_root / "output" / "media")

    if is_pdf:
        _generate_html(input_md, html_target, repo_root)
        _convert_html_to_pdf(html_target, output_path)
    elif is_html:
        _generate_html(input_md, output_path, repo_root)
    elif is_word:
        _generate_word(input_md, output_path, repo_root)
    else:
        _generate_generic(input_md, output_path, repo_root)

    _open_file(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
