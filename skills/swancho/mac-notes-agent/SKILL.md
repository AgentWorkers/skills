---
name: mac-notes-agent
description: |
  Integrate with the macOS Notes app (Apple Notes).
  Supports creating, listing, reading, updating, deleting, and searching notes
  via a simple Node.js CLI that bridges to AppleScript.
version: 1.1.0
author: swancho
license: CC-BY-NC-4.0
repository: https://github.com/swancho/mac-memo-agent
metadata:
  openclaw:
    emoji: "📝"
---

# Mac Notes Agent

## 概述

该工具允许代理程序通过 AppleScript（`osascript`）与 macOS 上的 **Apple Notes** 应用程序进行交互。它被实现为一个简单的 Node.js 命令行工具（CLI）：

```bash
node skills/mac-notes-agent/cli.js <command> [options]
```

> 该工具要求使用内置了 **Notes** 应用程序且支持 `osascript` 的 macOS 系统。

所有操作都针对 **默认的 Notes 账户** 进行。您也可以选择指定要使用的文件夹。

---

## 命令

### 1) 添加新笔记

```bash
node skills/mac-notes-agent/cli.js add \
  --title "Meeting notes" \
  --body "First line\nSecond line\nThird line" \
  [--folder "Jarvis"]
```

- `--title`（必填）：笔记标题
- `--body`（必填）：笔记正文。使用 `\n` 表示换行。
- `--folder`（可选）：文件夹名称。如果省略，则使用系统默认文件夹。如果文件夹不存在，系统会创建该文件夹。

> 换行符（`\n`）会在内部被转换为 `<br>` 标签，以便在 Notes 中正确显示。

**返回结果（JSON 格式）：**

```json
{
  "status": "ok",
  "id": "Jarvis::2026-02-09T08:40:00::Meeting notes",
  "title": "Meeting notes",
  "folder": "Jarvis"
}
```

---

### 2) 列出笔记

```bash
node skills/mac-notes-agent/cli.js list [--folder "Jarvis"] [--limit 50]
```

- 列出指定文件夹中的所有笔记（如果省略，则列出所有文件夹中的笔记）。
- 返回一个 JSON 数组，其中包含笔记的 `title`、`folder`、`creationDate` 和一个生成的 `id`。

---

### 3) 读取笔记内容

```bash
# By folder + title
node skills/mac-notes-agent/cli.js get \
  --folder "Jarvis" \
  --title "Meeting notes"

# By synthetic id
node skills/mac-notes-agent/cli.js get --id "Jarvis::2026-02-09T08:40:00::Meeting notes"
```

---

### 4) 更新笔记内容（替换正文）

```bash
node skills/mac-notes-agent/cli.js update \
  --folder "Jarvis" \
  --title "Meeting notes" \
  --body "New content\nReplaces everything"
```

- 替换匹配笔记的正文内容。
- 可以使用 `--id` 来指定要更新的笔记。

---

### 5) 向笔记中添加内容

```bash
node skills/mac-notes-agent/cli.js append \
  --folder "Jarvis" \
  --title "Meeting notes" \
  --body "\n---\nAdditional notes here"
```

- 在现有笔记的末尾添加新内容。

---

### 6) 删除笔记

```bash
node skills/mac-notes-agent/cli.js delete \
  --folder "Jarvis" \
  --title "Meeting notes"
```

---

### 7) 搜索笔记

```bash
node skills/mac-notes-agent/cli.js search \
  --query "keyword" \
  [--folder "Jarvis"] \
  [--limit 20]
```

- 根据关键词搜索笔记的标题和正文。

---

## 识别模型

Apple Notes 并不提供稳定的笔记 ID。该 CLI 使用以下方式来识别笔记：

- 主键：`(folderName, title)`
- 生成 ID：`folderName::creationDate::title`

如果有多个笔记具有相同的标题，该 CLI 会操作最新创建的笔记。

---

## 环境要求

- **仅支持 macOS**：通过 `osascript` 使用 AppleScript。
- **无需 npm 依赖**：仅使用 Node.js 的内置模块（如 `child_process`）。