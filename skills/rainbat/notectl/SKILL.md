---
name: notectl
description: 通过 AppleScript CLI 管理 Apple Notes
---

# notectl - Apple Notes 命令行工具

使用 AppleScript 通过命令行管理 Apple Notes。

## 命令

| 命令 | 描述 |
|---------|-------------|
| `notectl folders` | 列出所有包含笔记的文件夹 |
| `notectl list [folder]` | 列出指定文件夹中的笔记（默认文件夹：Notes） |
| `notectl show <title>` | 按标题显示笔记内容 |
| `notectl add <title>` | 创建新笔记 |
| `notectl search <query>` | 按标题或内容搜索笔记 |
| `notectl append <title>` | 向现有笔记中添加文本 |

## 示例

```bash
# List all folders
notectl folders

# List notes in default folder
notectl list

# List notes in specific folder
notectl list "rainbat-projects"
notectl list Papi

# Show a note
notectl show "Meeting Notes"

# Create a note
notectl add "New Idea"
notectl add "Project Plan" --folder research --body "Initial thoughts..."

# Search all notes
notectl search "clawdbot"
notectl search "API"

# Append to a note (daily log style)
notectl append "Daily Log" --text "- Completed feature X"
```

## `add` 命令的选项

| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `-f, --folder <name>` | 创建笔记的文件夹 | Notes |
| `-b, --body <text>` | 笔记内容 | 空 |

## `append` 命令的选项

| 选项 | 描述 | |
|--------|-------------|---------|
| `-t, --text <text>` | 要添加到笔记中的文本 |

## 可用的文件夹

本系统上的可用文件夹：
- Notes（默认文件夹）
- research
- rainbat-projects
- Papi
- renova-roll
- Journal
- CheatSheets
- pet-projects