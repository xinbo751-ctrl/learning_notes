#!/bin/bash

set -euo pipefail

SCRIPT_PATH="${BASH_SOURCE[0]:-$0}"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"

REPO_ROOT=""
if command -v git >/dev/null 2>&1; then
	REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || true)"
fi

if [ -z "$REPO_ROOT" ]; then
	REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

cd "$REPO_ROOT"

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
# 先创建目录，避免路径解析时失败
OUTPUT_DIR="$(dirname "$OUTPUT_PATH_RAW")"
mkdir -p "$OUTPUT_DIR"
OUTPUT_PATH="$(cd "$OUTPUT_DIR" && pwd)/$(basename "$OUTPUT_PATH_RAW")"
OUTPUT_EXT="${OUTPUT_PATH##*.}"
OUTPUT_EXT_LOWER=$(printf '%s' "$OUTPUT_EXT" | tr '[:upper:]' '[:lower:]')

IS_HTML_OUTPUT=false
IS_PDF_OUTPUT=false
IS_WORD_OUTPUT=false
case "$OUTPUT_EXT_LOWER" in
	html|htm)
		IS_HTML_OUTPUT=true
		;;
	pdf)
		IS_PDF_OUTPUT=true
		;;
	docx|doc)
		IS_WORD_OUTPUT=true
		;;
esac

HTML_TARGET="$OUTPUT_PATH"
if [ "$IS_PDF_OUTPUT" = true ] ; then
	HTML_TARGET="${OUTPUT_PATH%.*}.html"
	if [ "$HTML_TARGET" = "$OUTPUT_PATH" ]; then
		HTML_TARGET="${OUTPUT_PATH}.html"
	fi
fi

# 确保HTML_TARGET的目录存在
if [ "$IS_PDF_OUTPUT" = true ]; then
	mkdir -p "$(dirname "$HTML_TARGET")"
fi
mkdir -p output/media

generate_html_output() {
	local target_html=$1
	local add_img_style=${2:-false}
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

		python3 - <<PY
import sys
from pathlib import Path

target_html = """$target_html"""
add_img_style = "$add_img_style" == "true"

html_path = Path(target_html)
css_path = Path("media/github-markdown.css")
img_style_block = "<style>img{max-width:100%;height:auto;}</style>"
inline_start = "<!-- INLINE_GITHUB_MARKDOWN_CSS_START -->"
inline_end = "<!-- INLINE_GITHUB_MARKDOWN_CSS_END -->"

html = html_path.read_text(encoding='utf-8')
css = css_path.read_text(encoding='utf-8')
inline_css_block = f"{inline_start}\n<style>\n{css}\n</style>\n{inline_end}"

# 内联CSS
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

# 可选：添加图片样式限制
if add_img_style and img_style_block not in html:
	if "</head>" in html:
		html = html.replace("</head>", f"  {img_style_block}\n</head>", 1)
	else:
		html += "\n" + img_style_block + "\n"

html_path.write_text(html, encoding='utf-8')
PY
	)
}

generate_word_output() {
	local target_path=$1
	(
		cd output
		pandoc "$INPUT_MD" \
			--lua-filter=../render/diagram.lua \
			--extract-media=./media \
			-f gfm \
			-s \
			--embed-resources \
			--reference-doc=../render/reference.docx \
			-o "$target_path"
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
			--embed-resources \
			--css=./media/github-markdown.css \
			-o "$target_path"
	)
}

find_chrome_binary() {
	local chrome_bin=${PUPPETEER_EXECUTABLE_PATH:-}
	
	# 如果未设置环境变量，尝试查找 Chrome
	if [ -z "$chrome_bin" ]; then
		if command -v google-chrome >/dev/null 2>&1; then
			chrome_bin=$(command -v google-chrome)
		elif [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
			chrome_bin="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
		fi
	fi
	
	# 验证 Chrome 是否可执行
	if [ -z "$chrome_bin" ] || [ ! -x "$chrome_bin" ]; then
		echo "Chrome binary not found. Set PUPPETEER_EXECUTABLE_PATH or install Google Chrome." >&2
		return 1
	fi
	
	echo "$chrome_bin"
	return 0
}

convert_html_to_pdf() {
	local html_path=$1
	local pdf_path=$2
	local chrome_bin
	
	# 查找 Chrome 二进制文件
	if ! chrome_bin=$(find_chrome_binary); then
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

open_file() {
	local file_path=$1
	
	# 根据操作系统选择合适的打开命令
	if [[ "$OSTYPE" == "darwin"* ]]; then
		# macOS
		open "$file_path"
	elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
		# Linux
		xdg-open "$file_path" 2>/dev/null
	elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
		# Windows (Git Bash / Cygwin)
		start "$file_path"
	else
		echo "Generated file: $file_path" >&2
	fi
}

if [ "$IS_PDF_OUTPUT" = true ]; then
	generate_html_output "$HTML_TARGET"
	convert_html_to_pdf "$HTML_TARGET" "$OUTPUT_PATH"
elif [ "$IS_HTML_OUTPUT" = true ]; then
	generate_html_output "$OUTPUT_PATH"
elif [ "$IS_WORD_OUTPUT" = true ]; then
	generate_word_output "$OUTPUT_PATH"
else
	generate_generic_output "$OUTPUT_PATH"
fi

open_file "$OUTPUT_PATH"
