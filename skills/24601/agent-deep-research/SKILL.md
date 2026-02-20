---
name: deep-research
description: >
  **通过 Gemini Interactions API 进行异步深度研究（无需依赖 Gemini CLI）**  
  支持对本地文件进行基于 RAG（Retrieval, Augmentation, and Generation）的查询（使用 `--context` 参数）；提供查询成本的预览功能（`--dry-run`）；输出结构化的 JSON 数据；支持自适应的轮询机制。该技能适用于 30 多种 AI 代理，包括 Claude Code、Amp、Codex 和 Gemini CLI。
license: MIT
metadata:
  version: "1.3.1"
  author: "24601"
---
# 深度研究技能

该技能利用 Google Gemini 的深度研究功能进行深入研究。用户可以将文档上传到文件搜索存储库中，以获取基于 RAG（Retrieval, Augmentation, and Generation）的答案，并通过持久的工作区状态来管理研究会话。

## 适用于 AI 代理

获取完整的技能功能列表、决策树和输出格式：

```bash
uv run {baseDir}/scripts/onboard.py --agent
```

请参阅 [AGENTS.md]({baseDir}/AGENTS.md) 以获取完整的结构化说明。

| 命令 | 功能 |
|---------|-------------|
| `uv run {baseDir}/scripts/research.py start "问题"` | 启动深度研究 |
| `uv run {baseDir}/scripts/research.py start "问题" --context ./路径 --dry-run` | 估算成本 |
| `uv run {baseDir}/scripts/research.py start "问题" --context ./路径 --output report.md` | 基于 RAG 的研究 |
| `uv run {baseDir}/scripts/store.py query <名称> "问题"` | 根据上传的文档快速问答 |

## 先决条件

- Google API 密钥（环境变量 `GOOGLE_API_KEY` 或 `GEMINI_API_KEY`）
- 已安装 [uv](https://docs.astral.sh/uv/)（通过 `curl -LsSf https://astral.sh/uv/install.sh | sh` 安装）

## 快速入门

```bash
# Run a deep research query
uv run {baseDir}/scripts/research.py "What are the latest advances in quantum computing?"

# Check research status
uv run {baseDir}/scripts/research.py status <interaction-id>

# Save a completed report
uv run {baseDir}/scripts/research.py report <interaction-id> --output report.md

# Research grounded in local files (auto-creates store, uploads, cleans up)
uv run {baseDir}/scripts/research.py start "How does auth work?" --context ./src --output report.md

# Export as HTML or PDF
uv run {baseDir}/scripts/research.py start "Analyze the API" --context ./src --format html --output report.html

# Auto-detect prompt template based on context files
uv run {baseDir}/scripts/research.py start "How does auth work?" --context ./src --prompt-template auto --output report.md
```

## 环境变量

设置以下其中一个变量（按优先级顺序）：

| 变量 | 描述 |
|----------|-------------|
| `GEMINI_DEEP_RESEARCH_API_KEY` | 专用于此技能的密钥（最高优先级） |
| `GOOGLE_API_KEY` | 标准的 Google AI 密钥 |
| `GEMINI_API_KEY` | Gemini 专用密钥 |

可选的模型配置：

| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| `GEMINI_DEEP_RESEARCH_MODEL` | 用于文件搜索查询的模型 | `gemini-3.1-pro-preview` |
| `GEMINI_MODEL` | 备用模型名称 | `gemini-3.1-pro-preview` |
| `GEMINI_DEEP_RESEARCH_AGENT` | 深度研究代理标识符 | `deep-research-pro-preview-12-2025` |

## 研究命令

### 启动研究

```bash
uv run {baseDir}/scripts/research.py start "your research question"
```

| 标志 | 描述 |
|------|-------------|
| `--report-format FORMAT` | 输出格式：`executive_summary`、`detailed_report`、`comprehensive` |
| `--store STORE_NAME` | 将研究结果保存到文件搜索存储库中（显示名称或资源 ID） |
| `--no-thoughts` | 隐藏中间思考步骤 |
| `--follow-up ID` | 继续之前的研究会话 |
| `--output FILE` | 等待研究完成后将报告保存到单个文件中 |
| `--output-dir DIR` | 等待研究完成后将结构化结果保存到指定目录中 |
| `--timeout SECONDS` | 轮询的最大等待时间（默认：1800 秒 = 30 分钟） |
| `--no-adaptive-poll` | 禁用自适应轮询；使用固定间隔轮询 |
| `--context PATH` | 从文件或目录自动创建临时存储库以进行基于 RAG 的研究 |
| `--context-extensions EXT` | 根据文件扩展名过滤上传的上下文（例如 `py,md` 或 `.py .md`） |
| `--keep-context` | 研究完成后保留临时上下文存储库（默认：自动删除） |
| `--dry-run` | 估算成本而不启动研究（打印 JSON 成本估算） |
| `--format {md,html,pdf}` | 报告的输出格式（默认：md；pdf 需要 weasyprint） |
| `--prompt-template {typescript,python,general,auto}` | 领域特定的提示前缀；根据上下文文件扩展名自动检测 |

`start` 子命令是默认命令，因此 `research.py "问题"` 和 `research.py start "问题"` 是等效的。

### 检查状态

```bash
uv run {baseDir}/scripts/research.py status <interaction-id>
```

返回当前状态（`in_progress`、`completed`、`failed`），并在可用时输出相关信息。

### 保存报告

```bash
uv run {baseDir}/scripts/research.py report <interaction-id>
```

| 标志 | 描述 |
|------|-------------|
| `--output FILE` | 将报告保存到指定文件路径（默认：`report-<id>.md`） |
| `--output-dir DIR` | 将结构化结果保存到指定目录 |

## 结构化输出（`--output-dir`）

当使用 `--output-dir` 时，结果会被保存到一个结构化的目录中：

```
<output-dir>/
  research-<id>/
    report.md          # Full final report
    metadata.json      # Timing, status, output count, sizes
    interaction.json   # Full interaction data (all outputs, thinking steps)
    sources.json       # Extracted source URLs/citations
```

会向标准输出打印一个简洁的 JSON 总结（少于 500 个字符）：

```json
{
  "id": "interaction-123",
  "status": "completed",
  "output_dir": "research-output/research-interaction-1/",
  "report_file": "research-output/research-interaction-1/report.md",
  "report_size_bytes": 45000,
  "duration_seconds": 154,
  "summary": "First 200 chars of the report..."
}
```

这是推荐的人工智能代理集成模式——代理接收一个简短的 JSON 数据包，而完整的报告会写入磁盘。

## 自适应轮询

当使用 `--output` 或 `--output-dir` 时，脚本会轮询 Gemini API 直到研究完成。默认情况下，它使用 **自适应轮询**，该机制会根据之前的研究完成时间进行调整：

- 完成时间记录在 `.gemini-research.json` 文件的 `researchHistory` 中（最近 50 条记录，基于 RAG 的研究和非基于 RAG 的研究分别记录）。
- 当存在 3 个或更多匹配的数据点时，轮询间隔会根据历史数据分布进行调整：
  - 在任何研究完成之前：轮询间隔较慢（30 秒）
  - 在可能的完成时间范围内（中间 25% 到 75%）：轮询间隔较快（5 秒）
  - 在完成时间较晚的部分（超过平均完成时间的 75%）：轮询间隔适中（15-30 秒）
  - 完成时间异常长的研究（超过平均完成时间的 1.5 倍）：轮询间隔较慢（60 秒）
- 所有轮询间隔都被限制在 [2 秒到 120 秒] 之间，作为安全措施。

当历史数据不足（少于 3 个数据点）或使用了 `--no-adaptive-poll` 时，将使用固定的轮询间隔：前 30 秒为 5 秒，30 秒到 2 分钟为 10 秒，2 分钟到 10 分钟为 30 秒，10 分钟以上为 60 秒。

## 成本估算（`--dry-run`）

在开始研究之前预览成本估算：

```bash
uv run {baseDir}/scripts/research.py start "Analyze security architecture" --context ./src --dry-run
```

向标准输出输出一个 JSON 成本估算，其中包含上下文上传成本、研究查询成本和总成本。这些估算基于启发式方法（Gemini API 不返回令牌计数或计费数据），并且会明确标注。

当使用 `--output-dir` 完成研究后，`metadata.json` 文件会包含一个 `usage` 键，其中包含基于实际输出大小和持续时间的运行后成本估算。

## 文件搜索存储库命令

用于管理基于 RAG 的研究和问答的文件搜索存储库。

### 创建存储库

```bash
uv run {baseDir}/scripts/store.py create "My Project Docs"
```

### 列出存储库

```bash
uv run {baseDir}/scripts/store.py list
```

### 查询存储库

```bash
uv run {baseDir}/scripts/store.py query <store-name> "What does the auth module do?"
```

| 标志 | 描述 |
|------|-------------|
| `--output-dir DIR` | 将响应和元数据保存到指定目录 |

### 删除存储库

```bash
uv run {baseDir}/scripts/store.py delete <store-name>
```

使用 `--force` 可以跳过确认提示。当标准输入不是终端（例如，由 AI 代理调用时）时，会自动跳过确认提示。

## 文件上传

将文件或整个目录上传到文件搜索存储库。

```bash
uv run {baseDir}/scripts/upload.py ./src fileSearchStores/abc123
```

| 标志 | 描述 |
|------|-------------|
| `--smart-sync` | 跳过未更改的文件（通过哈希比较） |
| `--extensions EXT [EXT ...]` | 要包含的文件扩展名（用逗号或空格分隔，例如 `py,ts,md` 或 `.py .ts .md`） |

成功上传后总会保存哈希缓存，因此后续的 `--smart-sync` 运行会正确跳过未更改的文件，即使第一次上传没有使用 `--smart-sync`。

### MIME 类型支持

Gemini 文件搜索 API 支持 36 种文件扩展名。常见的编程文件（JS、TS、JSON、CSS、YAML 等）会通过回退机制自动上传为 `text/plain` 格式。二进制文件会被拒绝。详细列表请参见 `references/file_search_guide.md`。

**文件大小限制**：每个文件最大 100 MB。

## 会话管理

研究 ID 和存储库映射会缓存在当前工作目录下的 `.gemini-research.json` 文件中。

### 显示会话状态

```bash
uv run {baseDir}/scripts/state.py show
```

### 仅显示研究会话

```bash
uv run {baseDir}/scripts/state.py research
```

### 仅显示存储库

```bash
uv run {baseDir}/scripts/state.py stores
```

### 为代理提供 JSON 输出

在任何状态子命令后添加 `--json`，可以将结构化 JSON 输出到标准输出：

```bash
uv run {baseDir}/scripts/state.py --json show
uv run {baseDir}/scripts/state.py --json research
uv run {baseDir}/scripts/state.py --json stores
```

### 清除会话状态

```bash
uv run {baseDir}/scripts/state.py clear
```

使用 `-y` 可以跳过确认提示。当标准输入不是终端（例如，由 AI 代理调用时）时，会自动跳过确认提示。

## 非交互式模式

当标准输入不是终端时，所有确认提示（`store.py delete`、`state.py clear`）都会自动跳过。这允许 AI 代理和持续集成管道在不需要交互式提示的情况下调用这些命令。

## 工作流程示例

典型的基于 RAG 的研究工作流程：

```bash
# 1. Create a file search store
STORE_JSON=$(uv run {baseDir}/scripts/store.py create "Project Codebase")
STORE_NAME=$(echo "$STORE_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['name'])")

# 2. Upload your documents
uv run {baseDir}/scripts/upload.py ./docs "$STORE_NAME" --smart-sync

# 3. Query the store directly
uv run {baseDir}/scripts/store.py query "$STORE_NAME" "How is authentication handled?"

# 4. Start grounded deep research (blocking, saves to directory)
uv run {baseDir}/scripts/research.py start "Analyze the security architecture" \
  --store "$STORE_NAME" --output-dir ./research-output --timeout 3600

# 5. Or start non-blocking and check later
RESEARCH_JSON=$(uv run {baseDir}/scripts/research.py start "Analyze the security architecture" --store "$STORE_NAME")
RESEARCH_ID=$(echo "$RESEARCH_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 6. Check progress
uv run {baseDir}/scripts/research.py status "$RESEARCH_ID"

# 7. Save the report when completed
uv run {baseDir}/scripts/research.py report "$RESEARCH_ID" --output-dir ./research-output
```

## 输出规范

所有脚本都遵循双重输出模式：
- **stderr**：格式丰富的、人类可读的输出（表格、面板、进度条）
- **stdout**：程序可读的 JSON 格式，用于程序化处理

这意味着 `2>/dev/null` 可以隐藏人类可读的输出，而将标准输出重定向到 `/dev/null` 可以得到干净的 JSON 输出。