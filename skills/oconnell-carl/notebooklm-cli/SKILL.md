---
name: notebooklm-cli
description: 这是一个针对 Google NotebookLM 的全面命令行界面（CLI）工具，支持管理笔记本、数据源、音频播客、报告、测验、闪卡、思维导图、幻灯片、信息图、视频以及数据表等功能。在通过编程方式使用 NotebookLM 时，该工具非常实用：可以用于管理笔记本和数据源、生成音频概要（如播客）、创建学习材料（测验、闪卡）、制作演示文稿（幻灯片、信息图），或通过聊天功能查询数据源。
---

# NotebookLM CLI

## 概述

本技能通过命令行界面提供对 Google NotebookLM 的完整访问权限。您可以管理笔记本、数据源，并生成多种类型的内容，包括音频播客、报告、测验、闪卡、思维导图、幻灯片、信息图、视频和数据表。

## 适用场景

- 以编程方式管理 NotebookLM 的笔记本和数据源
- 从笔记本数据源生成音频内容（如播客）
- 创建学习材料（如测验、闪卡、报告）
- 制作视觉内容（如幻灯片、信息图、思维导图、视频）
- 通过聊天或一次性问题查询数据源
- 自动搜索和导入新的数据源

## 快速入门

### 认证

```bash
nlm login
```

1. 启动 Chrome 浏览器，导航至 NotebookLM 网站，并获取会话 cookie。需要安装 Google Chrome 浏览器。

### 列出笔记本

```bash
nlm notebook list
```

### 创建笔记本并添加数据源

```bash
nlm notebook create "My Research"
nlm source add <notebook-id> --url "https://example.com/article"
nlm source add <notebook-id> --text "Your content here" --title "My Notes"
```

### 生成内容（所有类型）

所有生成内容的命令都需要使用 `--confirm` 或 `-y` 选项：

```bash
nlm audio create <id> --confirm          # Podcast
nlm report create <id> --confirm         # Briefing doc or study guide
nlm quiz create <id> --confirm           # Quiz questions
nlm flashcards create <id> --confirm     # Flashcards
nlm mindmap create <id> --confirm        # Mind map
nlm slides create <id> --confirm         # Slide deck
nlm infographic create <id> --confirm    # Infographic
nlm video create <id> --confirm          # Video overview
nlm data-table create <id> "description" --confirm  # Data table
```

## 认证

| 命令 | 功能 |
|---------|-------------|
| `nlm login` | 使用 NotebookLM 进行登录（会打开 Chrome 浏览器） |
| `nlm login --check` | 验证当前登录凭证 |
| `nlm auth status` | 检查会话状态 |
| `nlm auth list` | 列出所有登录账号 |
| `nlm auth delete <profile> --confirm` | 删除指定登录账号 |
| `nlm login --profile <name>` | 登录到指定账号 |

会话有效期约为 20 分钟。如果命令执行失败，请使用 `nlm login` 重新登录。

## 笔记本管理

| 命令 | 功能 |
|---------|-------------|
| `nlm notebook list` | 列出所有笔记本 |
| `nlm notebook create "标题"` | 创建新的笔记本 |
| `nlm notebook get <id>` | 获取笔记本详细信息 |
| `nlm notebook describe <id>` | 查看笔记本的 AI 生成摘要 |
| `nlm notebook query <id> "问题"` | 与笔记本中的数据源进行交互式问答 |
| `nlm notebook delete <id> --confirm` | 删除笔记本 |

## 数据源管理

| 命令 | 功能 |
|---------|-------------|
| `nlm source list <notebook-id>` | 列出笔记本中的数据源 |
| `nlm source list <notebook-id> --drive` | 显示 Google Drive 中的数据源及其更新状态 |
| `nlm source add <id> --url "..."` | 添加 URL 或 YouTube 视频作为数据源 |
| `nlm source add <id> --text "..." --title "..."` | 添加文本作为数据源 |
| `nlm source add <id> --drive <doc-id>` | 添加 Google Drive 文档作为数据源 |
| `nlm source describe <source-id>` | 查看数据源的 AI 生成摘要 |
| `nlm source content <source-id>` | 获取数据源的原始文本内容 |
| `nlm source stale <notebook-id>` | 列出过时的 Google Drive 数据源 |
| `nlm source sync <notebook-id> --confirm` | 同步 Google Drive 数据源 |

## 内容生成

所有内容生成命令都需要使用 `--confirm` 或 `-y` 选项：

### 媒体类型

| 命令 | 生成内容 |
|---------|--------|
| `nlm audio create <id> --confirm` | 生成音频播客 |
| `nlm report create <id> --confirm` | 生成简报或学习指南 |
| `nlm quiz create <id> --confirm` | 生成测验题目 |
| `nlm flashcards create <id> --confirm` | 生成闪卡 |
| `nlm mindmap create <id> --confirm` | 生成思维导图 |
| `nlm slides create <id> --confirm` | 生成幻灯片 |
| `nlm infographic create <id> --confirm` | 生成信息图 |
| `nlm video create <id> --confirm` | 生成视频 |
| `nlm data-table create <id> "描述" --confirm` | 从笔记本中提取数据并生成数据表 |

## 文档管理

| 命令 | 功能 |
|---------|-------------|
| `nlm studio status <notebook-id>` | 列出所有生成的文档 |
| `nlm studio delete <notebook-id> <artifact-id> --confirm` | 删除指定的文档 |

## 聊天功能

| 命令 | 功能 |
|---------|-------------|
| `nlm chat start <notebook-id>` | 启动与笔记本的交互式聊天会话 |
| `nlm chat configure <notebook-id>` | 配置聊天目标和响应样式 |
| `nlm notebook query <id> "问题"` | 提出一次性问题（无需会话支持） |

聊天会话支持的命令：`/sources`, `/clear`, `/help`, `/exit`

## 搜索功能

| 命令 | 功能 |
|---------|-------------|
| `nlm research start "查询" --notebook-id <id>` | 在网页上搜索（约 30 秒） |
| `nlm research start "查询" --notebook-id <id> --mode deep` | 进行深度搜索（约 5 分钟） |
| `nlm research start "查询" --notebook-id <id> --source drive` | 在 Google Drive 中搜索 |
| `nlm research status <notebook-id>` | 查看搜索进度 |
| `nlm research import <notebook-id> <task-id>` | 导入搜索到的数据源 |

## 别名（UUID 快捷键）

```bash
nlm alias set myproject <uuid>           # Create alias
nlm notebook get myproject               # Use alias
nlm alias list                           # List all aliases
nlm alias get myproject                  # Resolve to UUID
nlm alias delete myproject               # Remove alias
```

## 输出格式

大多数列表命令支持多种输出格式：

```bash
nlm notebook list                # Rich table (default)
nlm notebook list --json         # JSON output
nlm notebook list --quiet        # IDs only (for scripting)
nlm notebook list --title        # "ID: Title" format
nlm notebook list --full         # All columns
```

## 多个账号管理

```bash
nlm login --profile work         # Login to profile
nlm notebook list --profile work # Use profile
nlm auth list                    # List all profiles
nlm auth delete work --confirm   # Delete profile
```

## 配置设置

```bash
nlm config show                  # Show current configuration
nlm config get <key>             # Get specific setting
nlm config set <key> <value>     # Update setting
```

## AI 文档生成

对于 AI 助手，本技能可生成详细的文档：

```bash
nlm --ai
```

生成的文档包含超过 400 行内容，涵盖所有命令、认证流程、错误处理方式、任务执行顺序以及自动化使用技巧。

## 参考资料

- [命令参考](references/commands.md) - 完整的命令格式说明
- [故障排除](references/troubleshooting.md) - 错误诊断与解决方法
- [工作流程](references/workflows.md) - 任务执行的完整步骤