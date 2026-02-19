---
name: macos-notes
description: 通过 AppleScript 创建、读取、搜索和管理 macOS 上的 Notes（便签）。适用于用户需要记录信息、保存想法、创建会议记录、阅读便签或执行与 macOS Notes 相关的任何操作的场景。可响应如下指令：“将此内容记下来”、“将其保存为便签”、“创建关于 X 的便签”、“显示我的便签”、“在便签中搜索 X”、“我之前写了关于 X 的什么内容”等。仅支持 macOS 系统。
license: MIT
compatibility: Requires macOS with Notes.app. Uses osascript (AppleScript) and python3 for JSON parsing.
metadata:
  author: lucaperret
  version: "1.0.0"
  openclaw:
    os: macos
    emoji: "\U0001F4DD"
    homepage: https://github.com/lucaperret/agent-skills
    requires:
      bins:
        - osascript
        - python3
---
# macOS 使用说明

您可以通过 `$SKILL_DIR/scripts/notes.sh` 脚本来管理 Apple Notes。Notes 的内容以 HTML 格式存储在系统中；该脚本支持接收纯文本或 HTML 格式的笔记内容，并在读取时返回纯文本格式的结果。

## 快速入门

### 列出文件夹

在操作之前，请务必先列出所有文件夹，以便识别账户和文件夹名称：

```bash
"$SKILL_DIR/scripts/notes.sh" list-folders
```

输出格式：`account → folder`（每行一个记录）。

### 创建笔记

```bash
echo '<json>' | "$SKILL_DIR/scripts/notes.sh" create-note
```

所需 JSON 字段：

| 字段 | 是否必填 | 默认值 | 说明 |
|---|---|---|---|
| `title` | 是 | - | 笔记标题（将成为笔记的第一行/标题） |
| `body` | 否 | "" | 笔记内容（纯文本，会自动转换为 HTML） |
| `html` | 否 | "" | 原始 HTML 内容（如果同时提供了 `title` 和 `html`，则 `html` 会覆盖 `body`） |
| `folder` | 否 | 默认文件夹 | 从文件夹列表中选择的文件夹名称 |
| `account` | 否 | 默认账户 | 从文件夹列表中选择的账户名称 |

### 阅读笔记

```bash
echo '<json>' | "$SKILL_DIR/scripts/notes.sh" read-note
```

所需 JSON 字段：

| 字段 | 是否必填 | 默认值 | 说明 |
|---|---|---|---|
| `name` | 是 | - | 笔记标题（需与笔记名称完全匹配） |
| `folder` | 否 | 所有文件夹 | 需要搜索的文件夹 |
| `account` | 否 | 默认账户 | 需要搜索的账户 |

### 列出所有笔记

```bash
echo '<json>' | "$SKILL_DIR/scripts/notes.sh" list-notes
```

所需 JSON 字段：

| 字段 | 是否必填 | 默认值 | 说明 |
| `folder` | 否 | 默认文件夹 | 从文件夹列表中选择的文件夹名称 |
| `account` | 否 | 默认账户 | 从文件夹列表中选择的账户名称 |
| `limit` | 否 | 20 | 最多返回的笔记数量 |

### 搜索笔记

```bash
echo '<json>' | "$SKILL_DIR/scripts/notes.sh" search-notes
```

所需 JSON 字段：

| 字段 | 是否必填 | 默认值 | 说明 |
| `query` | 是 | - | 需要在笔记标题中搜索的文本 |
| `account` | 否 | 默认账户 | 需要搜索的账户 |
| `limit` | 否 | 10 | 最多返回的结果数量 |

## 自然语言处理

将用户输入的指令转换为相应的脚本命令：

| 用户输入 | 对应命令 | 关键参数 |
|---|---|---|
| “记下这个信息：...” | `create-note` | `title`, `body` |
| “保存会议笔记” | `create-note` | `title: "会议笔记 — <日期>"`, `body` |
| “我写了关于 X 的什么内容？” | `search-notes` | `query: "X"` |
| “显示我的笔记” | `list-notes` | （默认操作） |
| “阅读我关于 X 的笔记” | `read-note` | `name: "X"` |
| “将这个内容保存到我的工作笔记中” | `create-note` | 从文件夹列表中选择最匹配的账户/文件夹 |

## 示例指令

**“记下 API 密钥的格式：prefix_xxxx”**  
```bash
echo '{"title":"API key format","body":"Format: prefix_xxxx"}' | "$SKILL_DIR/scripts/notes.sh" create-note
```

**“显示我最近的笔记”**  
```bash
echo '{}' | "$SKILL_DIR/scripts/notes.sh" list-notes
```

**“我写了关于密码的什么内容？”**  
```bash
echo '{"query":"password"}' | "$SKILL_DIR/scripts/notes.sh" search-notes
```

**“阅读我关于 Hinge 的笔记”**  
```bash
echo '{"name":"Hinge"}' | "$SKILL_DIR/scripts/notes.sh" read-note
```

**“在我的 iCloud 笔记中创建会议总结”**  
```bash
"$SKILL_DIR/scripts/notes.sh" list-folders
```  
之后执行：  
```bash
echo '{"title":"Meeting summary — 2026-02-17","body":"Discussed roadmap.\n- Q1: launch MVP\n- Q2: iterate","account":"iCloud","folder":"Notes"}' | "$SKILL_DIR/scripts/notes.sh" create-note
```

## 重要规则：

1. 如果用户没有指定账户或文件夹，请**始终先列出所有文件夹**——因为文件夹名称在多个账户之间是共享的。
2. 当需要访问特定位置的笔记时，请**同时指定账户和文件夹**——仅指定 `folder` 会导致命令含义不明确。
3. 被密码保护的笔记会被忽略——脚本无法读取或修改这些笔记。
4. 请通过标准输入（stdin）传递 JSON 数据——切勿通过命令行参数传递，以避免数据泄露。
5. 脚本会对所有输入进行验证（类型转换、范围检查）——无效的输入会被拒绝并显示错误信息。
6. 所有操作都会被记录到 `logs/notes.log` 文件中，包括时间戳、命令和笔记标题。
7. 笔记内容使用纯文本格式——`body` 中的换行符会自动转换为 `<br>`；如需富文本格式，请使用 `html` 参数。
8. 笔记的标题就是笔记的第一行——Notes.app 会将 `body` 的第一行视为笔记的名称。