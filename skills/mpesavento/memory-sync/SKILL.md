---
name: memory-sync
description: >
  Scrape and analyze OpenClaw JSONL session logs to reconstruct and backfill
  agent memory files. Use when: (1) Memory appears incomplete after model
  switches, (2) Verifying memory coverage, (3) Reconstructing lost memory,
  (4) Automated daily memory sync via cron/heartbeat. Supports simple
  extraction and LLM-based narrative summaries with automatic secret
  sanitization.
---

# 内存同步

该工具用于在模型切换时保持代理内存的连续性，并自动清理敏感信息。

## 安装

需要 Python 3.11 及 `click` 工具：

```bash
pip install click

# Optional: for direct API summarization (only if not using OpenClaw backend)
pip install openai
```

## 快速入门

```bash
# Run directly from skill directory
python ~/.openclaw/skills/memory-sync/memory_sync.py compare

# Or create an alias for convenience
alias memory-sync="python ~/.openclaw/skills/memory-sync/memory_sync.py"

# Check for gaps
memory-sync compare

# Backfill today's memory (simple extraction - fast, no LLM)
memory-sync backfill --today

# Backfill with LLM narrative (uses OpenClaw's native model - no API key needed)
memory-sync backfill --today --summarize

# Backfill all missing
memory-sync backfill --all
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `compare` | 检查会话日志与内存文件之间的差异 |
| `backfill --today` | 生成当前日期的内存数据 |
| `backfill --since YYYY-MM-DD` | 从指定日期至今补全数据 |
| `backfill --all` | 补全所有缺失的日期 |
| `backfill --incremental` | 仅补全自上次运行以来发生变化的日期 |
| `extract` | 提取符合条件的对话内容 |
| `summarize --date YYYY-MM-DD` | 生成指定日期的 LLM 摘要 |
| `transitions` | 列出模型切换情况 |
| `validate` | 检查内存文件的一致性 |
| `stats` | 显示覆盖统计信息 |

## 简单提取模式与 LLM 摘要模式

`backfill` 命令支持两种模式：

**简单提取模式（默认，未使用 `--summarize`）：**
- 速度快，无需调用 LLM 或 API
- 通过关键词频率分析提取主题
- 识别关键用户问题和助手的回答
- 从文本模式中检测决策点
- 生成包含主题、关键交流和决策部分的结构化输出
- 使用 `--preserve` 选项时：手写内容会 **附加** 到新文件的末尾
- 适用于：快速补全数据、初始设置、无法访问 LLM 的系统

**LLM 摘要模式（使用 `--summarize`） - 推荐使用：**
- 使用 LLM 生成连贯的摘要
- 生成 2-4 段落的文本
- 提供更好的上下文和洞察力提取
- 使用 `--preserve` 选项时：现有内容会 **传递给 LLM**，并指示其将其整合到新摘要中，同时保持时间顺序和主题结构
- 适用于：日常自动化、需要高质量内存文件的情况

**建议常规使用以下模式：**
```bash
# Best quality: LLM summary that incorporates any existing notes
memory-sync backfill --today --summarize --preserve
```

两种模式在写入数据前都会自动清理敏感信息。

## 常见工作流程

### 初始设置

```bash
# Check what's missing
memory-sync compare

# Backfill everything (may take time)
memory-sync backfill --all
```

### 每晚自动化（推荐）

```bash
# Best: LLM summary that incorporates any existing notes
memory-sync backfill --today --summarize --preserve

# Smart: Process only days changed since last run
memory-sync backfill --incremental --summarize --preserve

# Or use a specific backend if preferred
memory-sync backfill --today --summarize --preserve --summarize-backend anthropic
```

### 补充缺失的数据

```bash
# Backfill from last week to present
memory-sync backfill --since 2026-01-28 --summarize
```

### 保留原有内容重新生成

```bash
# Keep hand-written notes when regenerating
memory-sync backfill --date 2026-02-05 --force --preserve --summarize
```

## 敏感信息清理

所有内容都会自动清理以防止信息泄露：

- **30 多种明确识别模式**：OpenAI、Anthropic、GitHub、AWS、Stripe、Discord、Slack、Notion、Google、Brave、Tavily、SerpAPI 等
- **结构化数据**：JWT 令牌、SSH 密钥、数据库连接字符串、高熵 Base64 编码的数据
- **通用模式**：API 密钥、令牌、密码、环境变量
- **深度防护**：在提取、LLM 处理、文件写入、CLI 显示的每个阶段都会对敏感信息进行隐藏

敏感信息会被替换为 `[REDACTED-TYPE]` 占位符。

请参阅 `SECRET_PATTERNS.md` 以获取完整的模式列表。

## 摘要后端

`--summarize` 选项支持通过 `--summarize-backend` 参数选择多种后端：

| 后端 | 描述 | 是否需要 API 密钥 |
|---------|-------------|------------------|
| `openclaw`（默认） | 使用您配置的 OpenClaw 和模型 | 不需要 |
| `anthropic` | 通过 openai 包直接调用 Anthropic API | `ANTHROPIC_API_KEY` |
| `openai` | 通过 openai 包直接调用 OpenAI API | `OPENAI_API_KEY` |

### 示例

```bash
# Default: use OpenClaw's native model (no API key needed)
memory-sync backfill --today --summarize

# Explicit backend selection
memory-sync backfill --today --summarize --summarize-backend openclaw
memory-sync backfill --today --summarize --summarize-backend anthropic
memory-sync backfill --today --summarize --summarize-backend openai

# Override model for any backend
memory-sync backfill --today --summarize --model claude-sonnet-4-20250514
memory-sync backfill --today --summarize --summarize-backend openai --model gpt-4o
```

推荐使用 `openclaw` 后端，因为它：
- 使用您现有的 OpenClaw 配置
- 不需要额外的 API 密钥
- 可以使用您在 OpenClaw 中配置的任何模型

## 自动化使用示例

### 每晚 3 点自动执行

使用 LLM 生成摘要，并保留现有的笔记：

```bash
0 3 * * * cd ~/.openclaw/skills/memory-sync && python memory_sync.py backfill --today --summarize --preserve >> ~/.memory-sync/cron.log 2>&1
```

### 智能增量模式

自动检测自上次运行以来的变化：

```bash
# Initial backfill (run once, simple extraction for speed)
python memory_sync.py backfill --all

# Then set up nightly incremental with LLM summaries
0 3 * * * cd ~/.openclaw/skills/memory-sync && python memory_sync.py backfill --incremental --summarize --preserve >> ~/.memory-sync/cron.log 2>&1
```

状态信息记录在 `~/.memory-sync/state.json` 文件中。

## 配置

**默认路径：**
- 会话日志：`~/.openclaw/agents/main/sessions/*.jsonl`
- 内存文件：`~/.openclaw/workspace/memory/`

**可通过 CLI 参数进行覆盖：**
- `--sessions-dir /path/to/sessions` - 会话日志路径
- `--memory-dir /path/to/memory` - 内存文件路径

**仅针对直接使用 API 的后端的环境变量：**
- `ANTHROPIC_API_KEY` - 使用 `--summarize-backend anthropic` 时需要
- `OPENAI_API_KEY` - 使用 `--summarize-backend openai` 时需要

默认的 `openclaw` 后端不需要 API 密钥，它直接使用您的 OpenClaw 配置。

```bash
# Only needed if using direct API backends
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
```

## 内容保留规则

`--preserve` 选项的行为取决于是否使用了 `--summarize`：

**未使用 `--summarize`（简单提取模式）：**
- 手写内容（位于文件末尾的标记之后）会 **原样** 附加到新生成的文件末尾
- 新提取的内容会替换自动生成的部分，您的笔记会保留在文件末尾

**使用 `--summarize`（LLM 模式）：**
- 现有的手写内容会作为上下文传递给 LLM
- LLM 会被指示将您的笔记整合到新摘要中
- 结果：您的见解会被融入到连贯的叙述中，而不仅仅是简单添加

**示例：**
```bash
# Regenerate with LLM, incorporating existing notes into the summary
memory-sync backfill --date 2026-02-05 --force --preserve --summarize
```

自动生成的标记：
- 标题：*根据 N 段会话消息自动生成*
- 页脚：*请审阅并编辑此草稿，以记录真正重要的内容*

页脚标记之后的内容被视为手写内容，将会被保留。

## 补全数据选项

**日期选择（请选择一个）：**
- `--date YYYY-MM-DD` - 指定单一日期
- `--today` - 仅当前日期（适用于每晚自动化）
- `--since YYYY-MM-DD` - 从指定日期至今（用于补全数据）
- `--all` - 所有缺失的日期（适用于初始设置）
- `--incremental` - 仅补全自上次运行以来发生变化的日期（智能自动化）

**其他选项：**
- `--dry-run` - 显示不生成文件时的结果
- `--force` - 覆盖现有文件（重新生成时需要）
- `--preserve` - 重新生成时保留手写内容
- `--summarize` - 使用 LLM 生成摘要
- `--summarize-backend BACKEND` - 摘要后端：`openclaw`（默认）、`anthropic`、`openai`
- `--model MODEL` - 摘要使用的模型（默认值因后端而异）

## 性能

| 模式 | 每天所需时间 | 适用场景 |
|------|-------------|----------|
| `--all` | 5-10 分钟 × N 天 | 仅适用于初始设置 |
| `--since` | 5-10 分钟 × N 天 | 用于补全缺失的数据 |
| `--today` | 30-60 秒 | 适用于每晚自动化 |
| `--incremental` | 30-60 秒 | 适用于智能自动化场景 |