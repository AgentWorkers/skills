---
name: nb
description: 使用 `nb CLI` 管理笔记、书签和笔记本。支持在多个笔记本中创建、列出、搜索和整理笔记，并具备基于 Git 的版本控制功能。
author: Benjamin Jesuiter <bjesuiter@gmail.com>
homepage: https://github.com/xwmx/nb
metadata:
  clawdbot:
    emoji: "📓"
    os: ["darwin", "linux"]
    requires:
      bins: ["nb"]
---

# nb – 命令行笔记工具

> ⚠️ **重要提示：** **切勿** 手动编辑 `nb` Git 仓库中的文件（`~/.nb/*`）！请始终使用 `nb` 命令行工具（CLI），以确保文件索引正确且能够通过 Git 进行版本控制。

nb 是一个命令行工具，支持本地笔记的创建、编辑、搜索、归档等功能。它使用纯文本格式存储数据，并通过 Git 进行版本控制，同时提供类似维基的链接功能。

## 快速参考

### 笔记本（Notebooks）

```bash
# List all notebooks
nb notebooks

# Switch to a notebook
nb use <notebook>

# Create a new notebook
nb notebooks add <name>

# Show current notebook
nb notebooks current
```

### 添加笔记（Adding Notes）

```bash
# Add a note with title
nb add -t "Title" -c "Content here"

# Add note to specific notebook
nb <notebook>: add -t "Title" -c "Content"

# Add note with tags
nb add -t "Title" --tags tag1,tag2

# Add note from file content
nb add <notebook>:filename.md
```

### 列出笔记（Listing Notes）

```bash
# List notes in current notebook
nb list

# List all notes (no limit)
nb list -a

# List notes in specific notebook
nb <notebook>: list

# List with excerpts
nb list -e

# List with tags shown
nb list --tags
```

### 查看笔记（Showing Notes）

```bash
# Show note by ID or title
nb show <id>
nb show "<title>"

# Show note from specific notebook
nb show <notebook>:<id>

# Print content (for piping)
nb show <id> --print
```

### 搜索笔记（Searching Notes）

```bash
# Search across all notebooks
nb search "query"

# Search in specific notebook
nb <notebook>: search "query"

# Search with AND/OR/NOT
nb search "term1" --and "term2"
nb search "term1" --or "term2"
nb search "term1" --not "exclude"

# Search by tag
nb search --tag "tagname"
```

### 编辑笔记（Editing Notes）

```bash
# Edit by ID
nb edit <id>

# Edit by title
nb edit "<title>"

# Append content
nb edit <id> -c "New content to append"

# Prepend content
nb edit <id> -c "Content at top" --prepend

# Overwrite content
nb edit <id> -c "Replace all" --overwrite
```

### 删除笔记（Deleting Notes）

```bash
# Delete by ID (will prompt)
nb delete <id>

# Force delete without prompt
nb delete <id> -f
```

### 移动/重命名笔记（Moving/Renaming Notes）

```bash
# Move note to another notebook
nb move <id> <notebook>:

# Rename a note
nb move <id> new-filename.md
```

### 待办事项（Todos）

```bash
# Add a todo
nb todo add "Task title"

# Add todo with due date
nb todo add "Task" --due "2026-01-15"

# List open todos
nb todos open

# List closed todos
nb todos closed

# Mark todo as done
nb todo do <id>

# Mark todo as not done
nb todo undo <id>
```

### 书签（Bookmarks）

```bash
# Add a bookmark
nb bookmark <url>

# Add with comment
nb bookmark <url> -c "My comment"

# Add with tags
nb bookmark <url> --tags reference,dev

# List bookmarks
nb bookmark list

# Search bookmarks
nb bookmark search "query"
```

### Git 操作（Git Operations）

```bash
# Sync with remote
nb sync

# Create checkpoint (commit)
nb git checkpoint "Message"

# Check dirty status
nb git dirty

# Run any git command
nb git status
nb git log --oneline -5
```

### 文件夹（Folders）

```bash
# Add folder to notebook
nb folders add <folder-name>

# List folders
nb folders

# Add note to folder
nb add <folder>/<filename>.md
```

## 常见用法

### 添加包含完整内容的笔记

对于较长的笔记，可以先创建一个临时文件，然后再导入到笔记本中：

```bash
# Write content to temp file first, then copy to nb
cp /tmp/note.md ~/.nb/<notebook>/
cd ~/.nb/<notebook> && git add . && git commit -m "Add note"
nb <notebook>: index rebuild
```

### 在所有笔记中搜索

```bash
# Search everything
nb search "term" --all

# Search by type
nb search "term" --type bookmark
nb search "term" --type todo
```

## 数据存储位置

笔记以 markdown 格式存储在 `~/.nb/<notebook>/` 目录下，并通过 Git 进行版本控制。

```
~/.nb/
├── notebook-name-1/ # Your first notebook
├── notebook-name-2/ # Your second notebook
└── ...
```

## 使用技巧

1. 使用前缀 `nb <notebook>` 来操作特定的笔记本。
2. 笔记的 ID 是数字形式，可以在 `nb list` 命令中查看。
3. 也可以使用笔记的标题作为 ID（如果标题中包含空格，请使用引号）。
4. 所有更改都会自动被提交到 Git 仓库。
5. 使用 `nb sync` 命令从远程仓库同步数据。