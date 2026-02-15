---
name: upnote
description: 通过 `x-callback-url` 自动化功能来管理 UpNote 的笔记和笔记本。当用户请求创建笔记、打开笔记、创建笔记本、查看标签或管理 UpNote 中的内容时，可以使用此功能。
---

# UpNote

使用 x-callback-url 自动化功能来管理 UpNote 的笔记和笔记本。

## 概述

UpNote 已安装并支持 x-callback-url 端点以实现自动化操作。请使用随附的 `upnote.sh` 脚本来执行所有 UpNote 操作。

## 快速入门

- 创建笔记：
  ```bash
scripts/upnote.sh new --title "My Note" --text "Note content here"
```

- 使用 Markdown 创建笔记：
  ```bash
scripts/upnote.sh new --title "Meeting Notes" --text "# Agenda\n- Item 1" --markdown
```

- 在特定笔记本中创建笔记：
  ```bash
scripts/upnote.sh new --title "Project Ideas" --text "Ideas..." --notebook "Work"
```

## 常用操作

### 创建笔记
```bash
scripts/upnote.sh new \
  --title "Note Title" \
  --text "Content here" \
  [--notebook "Notebook Name"] \
  [--markdown] \
  [--new-window]
```

### 创建笔记本
```bash
scripts/upnote.sh notebook new "Notebook Name"
```

### 打开笔记（需要笔记 ID）
```bash
scripts/upnote.sh open <noteId> [true|false]
```

要获取笔记 ID，请在 UpNote 中右键点击笔记 → 选择“复制链接”，然后从链接中提取 ID。

### 打开笔记本（需要笔记本 ID）
```bash
scripts/upnote.sh notebook open <notebookId>
```

### 查看标签
```bash
scripts/upnote.sh tag "tag-name"
```

### 搜索笔记
```bash
scripts/upnote.sh view all_notes --query "search term"
```

### 查看模式
```bash
scripts/upnote.sh view <mode>
```

可用模式：
- `all_notes` - 所有笔记
- `quick_access` - 快速访问笔记
- `templates` - 所有模板
- `trash` - 垃圾箱
- `notebooks` - 笔记本（需使用 `--notebook-id` 参数）
- `tags` - 标签（需使用 `--tag-id` 参数）
- `filters` - 过滤器（需使用 `--filter-id` 参数）
- `all_notebooks` - 所有笔记本
- `all_tags` - 所有标签

## 注意事项

- 所有 UpNote 操作都需要通过打开 UpNote 应用程序来执行。
- 可以通过右键点击笔记并选择“复制链接”来获取笔记和笔记本的 ID。
- 该脚本会自动处理 URL 编码。
- 对于多行内容，请使用 `\n` 来表示换行，或者使用 heredoc 格式传递内容。

## 资源

### scripts/upnote.sh

这是一个用于处理 UpNote x-callback-url 操作的 Shell 脚本。它负责处理 URL 编码，并提供简洁的命令行界面。