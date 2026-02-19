---
name: dnote
description: 使用 Dnote CLI 来保存、检索和管理笔记。当用户需要记录信息、搜索现有笔记、查阅已保存的知识内容，或将笔记整理成“知识库”时，这款工具非常实用。它支持添加新笔记、进行全文搜索、查看笔记内容、编辑笔记以及删除笔记。是构建个人知识库的理想选择。
metadata:
  openclaw:
    emoji: '📝'
    homepage: https://www.getdnote.com/docs/cli/
    requires:
      bins:
        - dnote
    primaryEnv: DNOTE_API_KEY
---
# Dnote 笔记

使用 Dnote CLI 管理个人知识库。

## 设置

### 安装

```bash
# macOS/Linux auto-install
curl -s https://www.getdnote.com/install | sh

# Or Homebrew
brew install dnote

# Or download from: https://github.com/dnote/dnote/releases
```

### 配置

Dnote 遵循 XDG 目录结构：
- **配置文件**：`~/.config/dnote/dnoterc`
- **数据库**：`~/.local/share/dnote/dnote.db`

```bash
# Example config file (~/.config/dnote/dnoterc)
editor: vim
apiEndpoint: https://api.dnote.io
enableUpgradeCheck: true

# Or use local-only (no sync)
# No config needed - works offline by default
```

### 同步设置（可选）

```bash
# To sync across devices
dnote login

# Or local-only mode (no setup required)
```

## 快速入门

```bash
# Add a note to a book
{baseDir}/scripts/dnote.sh add cli "git rebase -i HEAD~3"

# Pipe content to a note
echo "docker system prune" | {baseDir}/scripts/dnote.sh add docker

# Search all notes
{baseDir}/scripts/dnote.sh find "docker compose"

# View recent notes
{baseDir}/scripts/dnote.sh recent

# List all books
{baseDir}/scripts/dnote.sh books

# View notes in a book
{baseDir}/scripts/dnote.sh view cli

# Get a specific note
{baseDir}/scripts/dnote.sh get cli 1
```

## 命令

### 添加笔记

| 命令 | 描述 |
|---------|-------------|
| `add <书名> <内容>` | 向指定书籍中添加笔记 |
| `add-stdin <书名>` | 从标准输入（stdin）添加笔记 |
| `quick <内容>` | 快速将内容添加到“收件箱”书籍中 |

### 查阅笔记

| 命令 | 描述 |
|---------|-------------|
| `view [书名]` | 列出书籍或书籍中的笔记 |
| `get <书名> <索引>` | 通过索引获取特定笔记 |
| `find <查询>` | 全文搜索（使用 `-b <书名>` 进行过滤） |
| `recent [数量]` | 显示最近的数量条笔记（默认：10 条） |
| `books` | 列出所有书籍 |
| `export [书名]` | 将笔记导出为 JSON 格式 |
| `config` | 显示配置信息和文件路径 |

### 管理笔记

| 命令 | 描述 |
|---------|-------------|
| `edit <ID> <内容>` | 通过 ID 编辑笔记 |
| `move <ID> <书名>` | 将笔记移动到其他书籍 |
| `remove <ID>` | 删除笔记 |
| `remove-book <书名>` | 删除整个书籍 |

### 同步与信息

| 命令 | 描述 |
|---------|-------------|
| `sync` | 与 Dnote 服务器同步 |
| `status` | 显示状态和统计信息 |
| `config` | 显示配置文件的位置 |
| `login` | 通过 CLI 登录服务器 |
| `logout` | 退出登录状态 |

## 收集 ID/书籍

- 可以使用任意书名（首次使用时会自动生成）
- 常见的书名示例：`cli`、`docker`、`git`、`ideas`、`snippets`、`journal`、`inbox`
- 添加第一条笔记时，系统会自动创建相应的书籍。

## 示例

```bash
# Capture a shell one-liner
{baseDir}/scripts/dnote.sh add cli "grep -r pattern . --include='*.py'"

# Save from command output
git log --oneline -10 | {baseDir}/scripts/dnote.sh add git

# Quick capture to inbox
{baseDir}/scripts/dnote.sh quick "Remember to update README"

# Search for docker commands
{baseDir}/scripts/dnote.sh find "docker compose"

# Search within a specific book
{baseDir}/scripts/dnote.sh find "config" -b cli

# Get formatted note for AI context
{baseDir}/scripts/dnote.sh get cli 1 --format raw

# Export book for processing
{baseDir}/scripts/dnote.sh export cli --json | jq '.notes[].content'

# Recent notes across all books
{baseDir}/scripts/dnote.sh recent 20

# Search and export results
{baseDir}/scripts/dnote.sh find "postgres" --json
```

## 在 AI 环境中使用 Dnote

### 为当前任务检索相关笔记：

```bash
# Search for related knowledge
{baseDir}/scripts/dnote.sh find "python argparse"

# Get full content of a specific note
{baseDir}/scripts/dnote.sh get cli 5

# Export entire book for context
{baseDir}/scripts/dnote.sh export python
```

### 自动捕获有用信息：

```bash
# Save a discovered solution
{baseDir}/scripts/dnote.sh add docker "Multi-stage builds reduce image size"

# Save with timestamp
{baseDir}/scripts/dnote.sh add journal "$(date): Deployed v2.3 to production"
```

## 模式化使用

### 日记

```bash
# Create dated entry
{baseDir}/scripts/dnote.sh add journal "$(date +%Y-%m-%d): Started work on feature X"

# Review recent entries
{baseDir}/scripts/dnote.sh view journal | head -20
```

### 代码片段

```bash
# Save with description
{baseDir}/scripts/dnote.sh add python "List comprehension: [x for x in items if x > 0]"

# Search when needed
{baseDir}/scripts/dnote.sh find "list comprehension"
```

### 命令参考

```bash
# Build a CLI reference
curl -s https://api.example.com | {baseDir}/scripts/dnote.sh add api

# Quick lookup
{baseDir}/scripts/dnote.sh view api
```

## 与工作流程集成

Dnote 提供了一些辅助功能，用于处理常见的使用场景：

| 功能 | 使用场景 |
|----------|----------|
| `dnote:search <查询>` | 在回答问题前查找相关内容 |
| `dnote:capture <书名> <内容>` | 保存任务中发现的有用信息 |
| `dnote:recent [数量]` | 查看最近捕获的笔记 |
| `dnote:export-book <书名>` | 将整本书的内容导入到当前上下文中 |

## 配置文件

创建 `~/.config/dnote/dnoterc` 文件：

```yaml
editor: code --wait      # or vim, nano, subl -w
apiEndpoint: https://api.dnote.io
enableUpgradeCheck: true
```

## 提示

- **使用具体的书名**：例如 `python`、`bash`、`docker`、`kubernetes`、`ideas` 等 |
- **全文搜索**：支持对所有笔记内容进行搜索 |
- **索引从 1 开始**：第一条笔记的索引是 1，而不是 0 |
- **支持管道操作**：可以直接将命令输出捕获到笔记中 |
- **同步是可选的**：可以离线使用，需要时再同步到服务器

## 直接使用 Dnote CLI

对于未在上述文档中涵盖的操作，请参考 Dnote 的官方文档：

```bash
# Interactive edit
dnote edit 5

# Rename book
dnote edit oldname -n newname

# Full sync
dnote sync --full

# Custom DB path
dnote --dbPath /path/to/custom.db view
```

更多文档：https://www.getdnote.com/docs/cli/