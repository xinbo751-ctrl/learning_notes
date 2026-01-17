# 公司全貌分析加工流程（端到端）

目标：从 **股票代码** 或 “**原始披露材料**（EDGAR filings / PDF 财报）”加工成一份可追溯的公司全貌梳理 Markdown，并最终一键导出成 HTML / PDF / Word。

两套写作工具：
1) 网页版（GUIDE 手写）：按 [GUIDE.md](GUIDE.md) 逐章写作 → 用 `render` 导出 HTML/PDF/Word。
2) Codex CLI 自动写作：准备 filings 或 PDF（可选用 Marker/MinerU 处理成 LLM ready）→ 自动写作 → 用 `render` 导出 HTML/PDF/Word。

> ***Markdown（.md文件）可以用Chrome（需安装Markdown Viewer扩展程序）打开查看，然后用打印成PDF，`render`脚本可不用。***

---

## 快速开始（推荐）

### 路线 A：网页版（GUIDE 手写）

> ***也可不用准备材料，给TICKER就能写作。***

- 获取材料（可选）（任选其一）

  - 美股/SEC：下载 filings  
  
  ```bash
  python utils/fetch_sec_edgar.py --ticker AAPL --form 10-K 10-Q --start 2015 --end 2025
  ```

  - PDF（财报、公告、电话会议）  
  可自己从公司IR网站下载PDF。

- 按 [GUIDE.md](GUIDE.md) 逐章写作  

- 用 `render` 导出 HTML/PDF/Word  

```bash
python utils/render.py Reports/<TICKER>/<公司名>全貌梳理.md
```

### 路线 B：Codex CLI 自动写作

#### 获取材料（可选）（任选其一）

> ***也可不下载任何资料直接用TICKER开始写作，但是速度理论上比下载好材料写作慢*** 

- 美股/SEC：下载 filings
```bash
python utils/fetch_sec_edgar.py --ticker AAPL --form 10-K 10-Q --start 2015 --end 2025
```

- PDF：可直接用原 PDF，也可用 Marker/MinerU 处理成 LLM ready，建议处理。

#### 自动写作（Codex CLI）

从[GUIDE.md](GUIDE.md) 生成prompts：
```bash
python utils/sync_codex_from_guide.py
```

用TICKER自动写作：
```bash
python utils/run_qual_report_codex.py --ticker <TICKER>
```

用本机材料自动写作：
```bash
python utils/run_qual_report_codex.py --base filings/<TICKER>
```

#### 用 `render` 导出 HTML/PDF/Word  

```bash
python utils/render.py Reports/<TICKER>/<公司名>全貌梳理.md
```

---

## 目录约定（你会看到的产物在哪里）

- `filings/`：SEC EDGAR 下载的原始 filing（iXBRL HTML + XBRL 实例与 taxonomy）。
- `output/`：各类脚本的输出目录（渲染后的 HTML/PDF/Word、marker 输出、媒体资源等）。
- `render/`：Pandoc 渲染模板资源（CSS、before/after 片段、Lua filter）。
- `Reports/`：你写作/自动化生成的最终产物（建议用股票代码做目录名：`Reports/<TICKER>/...`）。

---

## 路径 A：网页版（GUIDE 手写）

### 获取材料

可选两类材料来源：
- 美股/SEC：下载 filings（见【脚本参数说明】`fetch_sec_edgar`）
- PDF：可直接用原 PDF 作为材料

### 按 GUIDE 逐章写作

写作流程与“对话协议”在 [GUIDE.md](GUIDE.md)。推荐顺序：
1) 新对话中粘贴 [GUIDE.md](GUIDE.md) 的“开场必发：协议注入 + 全局硬约束”。
2) 上传《定性分析模板.md》与材料。
3) 用 `#WRITE` 从“公司介绍与沿革”开始线性推进；跳章用 `#JUMP`。
4) 中间章节写完后再 `#FIX`；最后 `#FILL` 回填“投资要点概览”和“来源清单”。
5) 用 `#CHECK` 做一致性检查。

### 用 render 导出 HTML / PDF / Word（可选）

> ***Markdown（.md文件）可以用Chrome（需安装Markdown Viewer扩展程序）打开查看，然后用打印成PDF，`render`脚本可不用。***

```bash
python utils/render.py Reports/<TICKER>/<公司名>全貌梳理.md
```

---

## 路径 B：Codex CLI 自动写作

### 可直接用TICKER自动写作：
```bash
python utils/run_qual_report_codex.py --ticker <TICKER>
```

也可获取材料到本机后用材料写作，理论上速度会更快。  

### 获取材料

可选两类材料来源：
- 美股/SEC：下载 filings（见【脚本参数说明】 `fetch_sec_edgar`）
- PDF：可直接用原 PDF，或先处理成 LLM ready，建议处理。

### 可选：PDF 处理成 LLM ready（Marker / MinerU）

适合：PDF 规模大、结构复杂、需要更稳定的章节检索与引用。

输入：PDF  
输出：LLM ready的材料库  
示例（MinerU）：
```bash
python utils/mineru_extract.py --base /path/to/pdfs --output output/<base目录名>
```

### 可选：构建材料索引（manifest/toc）

当材料库规模很大（例如上千文件）时，建议构建索引并按章拼包。
输入：LLM ready的材料库  
输出：材料库  索引  
示例（MinerU）：
```bash
python utils/build_mineru_manifest.py --base output/<base目录名>
```

### 运行 Codex CLI 自动写作

从[GUIDE.md](GUIDE.md) 生成prompts：
```bash
python utils/sync_codex_from_guide.py
```

直接从filings或PDF开始写作：  
```bash
python utils/run_qual_report_codex.py --base filings/<TICKER> --ticker <TICKER>
```

从材料库开始写作：  
> 如果未显式传 `--materials-index`，脚本会自动检查 `--base/index` 是否存在索引并使用它。
```bash
python utils/run_qual_report_codex.py --base output/<base目录名>
```

从材料库 + 索引开始写作：  
```bash
python utils/run_qual_report_codex.py --base output/<base目录名> --materials-index output/<base目录名>/index
```


当章节审计失败触发重试时，脚本会自动扩大该章材料包（提高 `top_k` 与 `max_total_chars`）并重写。

产物与日志：
- 报告：`Reports/<TICKER>/<公司名>全貌梳理.md`
- 章节：`Reports/<TICKER>/chapters/`
- 日志：`Reports/<TICKER>/_codex_logs/`

### 用 render 导出 HTML / PDF / Word

```bash
python utils/render.py Reports/<TICKER>/<公司名>全貌梳理.md
```

---

## 脚本参数说明

### fetch_sec_edgar
脚本：`utils/fetch_sec_edgar.py`

常用参数：
- `--ticker`：股票代码（必填）
- `--form`：表单类型（可多填，如 `10-K 10-Q`）
- `--start`：起始日期（必填；支持 YYYY / YYYY-MM / YYYY-MM-DD）
- `--end`：结束日期（可选；支持 YYYY / YYYY-MM / YYYY-MM-DD；默认今天）
- `--output`：输出目录（可选，默认 `./filings`）

重要说明：
- SEC 要求 User-Agent 标识身份，请在环境变量中设置：
	```bash
	export SEC_USER_AGENT="Your Name your@email.com"
	```
- 输出目录结构形如：`filings/<TICKER>/<FORM>_<DATE>_report_<REPORT_DATE>_<ACCESSION>/`。

### mineru_extract
脚本：`utils/mineru_extract.py`

参数：
- `--filing`：单个 PDF 文件路径（与 `--base` 互斥）
- `--base`：PDF 目录（递归扫描 .pdf，与 `--filing` 互斥）
- `--output`：输出目录（默认 `./output`）
- `--ocr`：启用 OCR（默认关闭）
- `--html`：导出 HTML（`extra_formats=["html"]`）
- `--sleep`：轮询间隔秒数（默认 30）
- `--timeout`：轮询超时秒数（默认 1200；实际总超时 = `timeout * 文件数`）

### build_mineru_manifest
脚本：`utils/build_mineru_manifest.py`

用途：把 MinerU 输出目录（大量文件）构建成可检索的 `manifest.jsonl/manifest.tsv`，供后续按章节选 Top-K chunks。

参数：
- `--base`：MinerU 输出根目录（例如 `output/0883`）
- `--output`：索引输出目录（可选；默认 `<base>/index`）
- `--chunk-chars`：chunk 大小（字符数；默认取环境变量 `MINERU_CHUNK_CHARS`，否则 1800）
- `--include-doc-records`：在 `manifest.jsonl` 中额外写入 doc 级记录（可选）
- `--max-docs`：仅处理前 N 份文档（调试用；0 表示不限制）
- `--write-toc`：生成一个 `toc.md` 骨架（默认开启；仅当 `toc.md` 不存在时写入）
- `--no-write-toc`：关闭 `toc.md` 生成

### marker_extract
脚本：`utils/marker_extract.py`

参数：
- `--filing`：单个 PDF 文件路径（与 `--base` 互斥）
- `--base`：PDF 目录（仅当前目录下 .pdf）
- `--output`：输出目录（默认 `./output`）
- `--ollama`：启用本地 Ollama
- `--model`：Ollama 模型名（默认 `deepseek-r1:8b`）

### run_qual_report_codex
脚本：`utils/run_qual_report_codex.py`

参数：
- `--base`：材料目录（单一公司；可选，不提供则表示不使用本地材料）
- `--ticker`：股票代码（可选但推荐；用于默认 base 与校验）
- `--company`：公司名（可选，覆盖自动识别）
- `--only-chapters`：只写指定章节（可重复或逗号分隔）
- `--max-attempts`：每章最大尝试次数（默认 2）
- `--profile`：执行档位（fast/balanced/high/deep）
- `--verbose`：打印 Codex 最终输出
- `--dry-run`：只打印计划不执行
- `--overview-input`：overview 输入范围（condensed/full）
- `--no-check`：关闭最终一致性检查

### render
脚本：`utils/render.py`

参数：
- `<input_markdown>`：输入 Markdown（必填）
- `[output_path]`：输出路径（可选；扩展名决定格式：html/pdf/docx）

运行时依赖：
- `pandoc`（带 Lua filter 支持）
- `python3`（用于 HTML 后处理：CSS 内联、图片宽度限制）
- Google Chrome（PDF 导出时 headless 打印）

macOS 通常需要配置：
```bash
export PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

