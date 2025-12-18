#!/bin/zsh

set -euo pipefail

SCRIPT_DIR=${0:A:h}
cd "$SCRIPT_DIR"

if (( $# < 1 )); then
	echo "Usage: $0 <input_markdown> [output_html]" >&2
	exit 1
fi

INPUT_MD=${1:A}
INPUT_FILENAME=${INPUT_MD:t}
INPUT_STEM=${INPUT_FILENAME%.*}
if [[ -z "$INPUT_STEM" ]]; then
	INPUT_STEM="$INPUT_FILENAME"
fi

if (( $# >= 2 )); then
	OUTPUT_HTML_RAW=$2
else
	OUTPUT_HTML_RAW="output/${INPUT_STEM}.html"
fi
OUTPUT_HTML=${OUTPUT_HTML_RAW:A}

mkdir -p "$(dirname "$OUTPUT_HTML")"
mkdir -p output/media

pushd output > /dev/null
pandoc "$INPUT_MD" \
	--lua-filter=../render/diagram.lua \
	--extract-media=media \
	-f gfm -t html5 -s \
	--css=../render/github-markdown.css \
	--include-before-body=../render/before.html \
	--include-after-body=../render/after.html \
	-o "$OUTPUT_HTML"
popd > /dev/null

open "$OUTPUT_HTML"
