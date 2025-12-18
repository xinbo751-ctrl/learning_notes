#!/bin/bash

set -euo pipefail

SCRIPT_PATH="$0"
if [ "${SCRIPT_PATH%/*}" != "$SCRIPT_PATH" ]; then
	SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
else
	SCRIPT_DIR="$PWD"
fi
cd "$SCRIPT_DIR"

if [ $# -lt 1 ]; then
	echo "Usage: $0 <input_markdown> [output_html]" >&2
	exit 1
fi

INPUT_MD_RAW=$1
INPUT_MD="$(cd "$(dirname "$INPUT_MD_RAW")" && pwd)/$(basename "$INPUT_MD_RAW")"
INPUT_FILENAME=$(basename "$INPUT_MD")
INPUT_STEM=${INPUT_FILENAME%.*}
if [ -z "$INPUT_STEM" ]; then
	INPUT_STEM="$INPUT_FILENAME"
fi

if [ $# -ge 2 ]; then
	OUTPUT_PATH_RAW=$2
else
	OUTPUT_PATH_RAW="output/${INPUT_STEM}.html"
fi
OUTPUT_PATH="$(cd "$(dirname "$OUTPUT_PATH_RAW")" && pwd)/$(basename "$OUTPUT_PATH_RAW")"
OUTPUT_EXT="${OUTPUT_PATH##*.}"
OUTPUT_EXT_LOWER=$(printf '%s' "$OUTPUT_EXT" | tr '[:upper:]' '[:lower:]')

IS_HTML_OUTPUT=false
IS_PDF_OUTPUT=false
case "$OUTPUT_EXT_LOWER" in
	html|htm)
		IS_HTML_OUTPUT=true
		;;
	pdf)
		IS_PDF_OUTPUT=true
		;;
esac

HTML_TARGET="$OUTPUT_PATH"
if [ "$IS_PDF_OUTPUT" = true ] ; then
	HTML_TARGET="${OUTPUT_PATH%.*}.html"
	if [ "$HTML_TARGET" = "$OUTPUT_PATH" ]; then
		HTML_TARGET="${OUTPUT_PATH}.html"
	fi
fi

mkdir -p "$(dirname "$OUTPUT_PATH")"
mkdir -p "$(dirname "$HTML_TARGET")"
mkdir -p output/media

generate_html_output() {
	local target_html=$1
	(
		cd output
		cp "../render/github-markdown.css" ./media/github-markdown.css
		cp "../render/before.html" ./media/before.html
		cp "../render/after.html" ./media/after.html
		pandoc "$INPUT_MD" \
			--lua-filter=../render/diagram.lua \
			--extract-media=./media \
			-f gfm \
			-t html5 \
			-s \
			--css=./media/github-markdown.css \
			--include-before-body=./media/before.html \
			--include-after-body=./media/after.html \
			--embed-resources \
			-o "$target_html"

		python3 <<PY
from pathlib import Path

html_path = Path("$target_html")
css_path = Path("media/github-markdown.css")
# img_style_block = "<style>img{max-width:100%;height:auto;}</style>"
inline_start = "<!-- INLINE_GITHUB_MARKDOWN_CSS_START -->"
inline_end = "<!-- INLINE_GITHUB_MARKDOWN_CSS_END -->"

html = html_path.read_text()
css = css_path.read_text()
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
		'<link rel="stylesheet" href="./media/github-markdown.css"/>'
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

# if img_style_block not in html:
# 	if "</head>" in html:
# 		html = html.replace("</head>", f"  {img_style_block}\n</head>", 1)
# 	else:
# 		html += "\n" + img_style_block + "\n"

html_path.write_text(html)
PY
	)
}

generate_generic_output() {
	local target_path=$1
	(
		cd output
		pandoc "$INPUT_MD" \
			--lua-filter=../render/diagram.lua \
			--extract-media=./media \
			-f gfm \
			-s \
			--css=./media/github-markdown.css \
			-o "$target_path"
	)
}

convert_html_to_pdf() {
	local html_path=$1
	local pdf_path=$2
	local chrome_bin=${PUPPETEER_EXECUTABLE_PATH:-}
	if [ -z "$chrome_bin" ]; then
		if command -v google-chrome >/dev/null 2>&1; then
			chrome_bin=$(command -v google-chrome)
		elif [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
			chrome_bin="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
		fi
	fi
	if [ -z "$chrome_bin" ] || [ ! -x "$chrome_bin" ]; then
		echo "Chrome binary not found. Set PUPPETEER_EXECUTABLE_PATH or install Google Chrome." >&2
		exit 1
	fi
	local html_uri
	html_uri=$(python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).resolve().as_uri())' "$html_path")
	local chrome_args=(
		--headless
		--disable-gpu
		--disable-background-networking
		--disable-default-apps
		--disable-component-update
		--disable-client-side-phishing-detection
		--disable-features=TranslateUI
		--disable-sync
		--disable-extensions
		--metrics-recording-only
		--password-store=basic
		--use-mock-keychain
		--no-first-run
		--no-default-browser-check
		--incognito
		--bwsi
		--disable-logging
		--log-level=3
		--disable-popup-blocking
		--disable-notifications
		--run-all-compositor-stages-before-draw
		--virtual-time-budget=10000
		--print-to-pdf="$pdf_path"
		--print-to-pdf-no-header
		--no-pdf-header-footer
		"$html_uri"
	)
	if ! "$chrome_bin" "${chrome_args[@]}" >/dev/null 2>&1; then
		echo "Chrome headless PDF conversion failed." >&2
		exit 1
	fi
}

if [ "$IS_PDF_OUTPUT" = true ]; then
	generate_html_output "$HTML_TARGET"
	convert_html_to_pdf "$HTML_TARGET" "$OUTPUT_PATH"
elif [ "$IS_HTML_OUTPUT" = true ]; then
	generate_html_output "$OUTPUT_PATH"
else
	generate_generic_output "$OUTPUT_PATH"
fi

open "$OUTPUT_PATH"
