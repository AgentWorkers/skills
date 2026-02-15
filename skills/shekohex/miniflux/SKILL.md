---
name: miniflux
description: "浏览、阅读和管理 Miniflux 提供的文章。当 Claude 需要通过 Miniflux 处理 RSS/Atom 源时，可以使用此功能：列出未读或新发布的文章、阅读文章内容、将文章标记为已读，以及管理源和分类。该功能支持命令行界面（CLI），并提供灵活的输出格式（标题、摘要或全文）。"
metadata: {"clawdbot":{"emoji":"📣","requires":{"bins":["uv"]}}}
---

# Miniflux 技能

通过命令行界面（CLI）浏览、阅读和管理 Miniflux 的 RSS/Atom 订阅源文章。

## 快速入门

```bash
# List unread articles (brief format)
uv run scripts/miniflux-cli.py list --status=unread --brief

# Get article details
uv run scripts/miniflux-cli.py get 123

# Mark articles as read
uv run scripts/miniflux-cli.py mark-read 123 456

# Show article statistics (word count, reading time)
uv run scripts/miniflux-cli.py stats --entry-id=123
```

## 配置

配置的优先级（从高到低）：
1. **CLI 参数**：`--url`, `--api-key`
2. **环境变量**：`MINIFLUX_URL`, `MINIFLUX_API_KEY`
3. **配置文件**：`~/.local/share/miniflux/config.json`（首次运行时自动生成）

### 设置

```bash
# Option 1: Environment variables (recommended for agents)
export MINIFLUX_URL="https://miniflux.example.org"
export MINIFLUX_API_KEY="your-api-key"

# Option 2: CLI flags (one-time, saves to config)
uv run scripts/miniflux-cli.py --url="https://miniflux.example.org" --api-key="xxx" list
```

## 子命令

### list - 列出文章

列出文章，支持可选的过滤条件。

```bash
# Unread articles (brief)
uv run scripts/miniflux-cli.py list --status=unread --brief

# From specific feed with summary
uv run scripts/miniflux-cli.py list --feed=42 --summary

# Search with limit
uv run scripts/miniflux-cli.py list --search="python" --limit=10

# Starred articles
uv run scripts/miniflux-cli.py list --starred
```

**参数：**
- `--status={read,unread,removed}` - 按状态过滤
- `--feed=ID` - 按订阅源 ID 过滤
- `--category=ID` - 按类别 ID 过滤
- `--starred` - 仅显示已标记为星号的文章
- `--search=QUERY` - 搜索文章
- `--limit=N` - 最大显示条数
- `--offset=N` - 跳过内容的前 N 个字符
- `--content-limit=N` - 每篇文章的最大显示字符数
- `-b, --brief` - 仅显示标题
- `-s, --summary` - 标题 + 摘要
- `-f, --full` - 完整文章内容（默认）
- `--json` - JSON 格式输出
- `--plain` - 每条记录占用一行

### get - 根据 ID 获取文章

根据 ID 获取单篇文章，并可控制是否显示内容。

```bash
# Full article
uv run scripts/miniflux-cli.py get 123

# First 2000 characters
uv run scripts/miniflux-cli.py get 123 --limit=2000

# Read from character 1000 to 2000 (pagination)
uv run scripts/miniflux-cli.py get 123 --offset=1000 --limit=1000
```

如果文章内容被截断，会显示：`[...truncated, total: N chars]`

### mark-read - 标记为已读

将一个或多个文章标记为已读。

```bash
# Single article
uv run scripts/miniflux-cli.py mark-read 123

# Multiple articles
uv run scripts/miniflux-cli.py mark-read 123 456 789
```

### mark-unread - 标记为未读

将一个或多个文章标记为未读。

```bash
uv run scripts/miniflux-cli.py mark-unread 123
```

### feeds - 列出所有订阅源

列出所有已配置的订阅源。

```bash
# Human-readable
uv run scripts/miniflux-cli.py feeds

# JSON format
uv run scripts/miniflux-cli.py feeds --json
```

### categories - 列出所有类别

列出所有类别。

```bash
uv run scripts/miniflux-cli.py categories
```

### stats - 统计信息

显示未读文章的数量或文章的统计信息。

```bash
# Article statistics (word count, character count, reading time)
uv run scripts/miniflux-cli.py stats --entry-id=123

# Global unread counts per feed
uv run scripts/miniflux-cli.py stats
```

### refresh - 刷新订阅源

触发订阅源的更新。

```bash
# Refresh all feeds
uv run scripts/miniflux-cli.py refresh --all

# Refresh specific feed
uv run scripts/miniflux-cli.py refresh --feed=42
```

### search - 搜索文章

`list --search` 的便捷别名。

```bash
uv run scripts/miniflux-cli.py search "rust"
uv run scripts/miniflux-cli.py search "ai" --status=unread --brief
```

## 输出格式

- `--brief` / `-b` - 快速概览（标题 + 订阅源 + 日期）
- `--summary` / `-s` - 标题 + 内容预览（200 个字符）
- `--full` / `-f` - 完整文章内容（默认）
- `--json` - 用于机器处理的原始 JSON 格式输出
- `--plain` - 每条记录占用一行（以制表符分隔）

## 大篇幅文章的处理

对于内容较长的文章（例如超过 5000 字）：
1. **先查看统计信息：**
   ```bash
   uv run scripts/miniflux-cli.py stats --entry-id=123
   ```
   显示字数、字符数和阅读所需时间。
2. **使用分页功能分块阅读：**
   ```bash
   # First 5000 chars
   uv run scripts/miniflux-cli.py get 123 --limit=5000

   # Next 5000 chars (chars 5000-10000)
   uv run scripts/miniflux-cli.py get 123 --offset=5000 --limit=5000
   ```

3. **对于摘要：** 如果文章超过 5000 字，可以使用子代理来读取并生成摘要：
   ```bash
   # Get stats to determine word count
   uv run scripts/miniflux-cli.py stats --entry-id=123

   # If >5000 words, delegate to subagent for summarization
   ```

## 错误处理

CLI 提供了有用的错误信息：
- **无效的凭据** → 请检查 `MINIFLUX_API_KEY`
- **未找到文章** → 建议使用 `list` 命令进行浏览
- **配置文件缺失** → 显示配置文件的位置
- **没有结果** → 显示相应提示信息

## 标准参数

- `-v, --version` - 显示版本信息
- `-q, --quiet` - 抑制非错误信息的输出
- `-d, --debug` - 启用调试输出
- `--no-color` - 禁用彩色输出
- `--url=URL` - Miniflux 服务器地址
- `--api-key=KEY` - Miniflux API 密钥

## 示例

### 日常工作流程

```bash
# Check what's unread
uv run scripts/miniflux-cli.py list --status=unread --brief

# Read interesting articles
uv run scripts/miniflux-cli.py get 456

# Mark as read
uv run scripts/miniflux-cli.py mark-read 456
```

### 研究模式

```bash
# Search for specific topics
uv run scripts/miniflux-cli.py search "machine learning" --summary

# Get full article content
uv run scripts/miniflux-cli.py get 789
```

### 批量处理

```bash
# Get all unread as JSON for processing
uv run scripts/miniflux-cli.py list --status=unread --json

# Mark multiple as read
uv run scripts/miniflux-cli.py mark-read 123 456 789
```

有关任何子命令的完整帮助信息，请参阅：
```bash
uv run scripts/miniflux-cli.py <subcommand> --help
```