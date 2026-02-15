---
name: drafts
description: 在 macOS 上，可以通过 CLI（命令行接口）来管理 Drafts 应用中的笔记。支持创建、查看、列出、编辑、追加、前置以及执行其他操作。当用户需要创建笔记、列出所有草稿、搜索草稿或管理自己的草稿收件箱时，可以使用此功能。**重要提示**：必须确保 Drafts 应用已在 macOS 上运行，才能使用这些 CLI 命令。
homepage: https://github.com/nerveband/drafts
metadata: {"clawdbot":{"emoji":"📋","os":["darwin"],"requires":{"bins":["drafts"]}}}
---

# Drafts CLI

通过终端在 macOS 上管理 [Drafts](https://getdrafts.com) 的笔记。

## 重要要求

> **此 CLI 仅适用于运行了 Drafts 应用的 macOS 系统。**

- **仅支持 macOS** - 该工具基于 AppleScript，无法在 Linux 或 Windows 上使用。
- **Drafts 必须处于运行状态** - 所有命令只有在 Drafts 应用运行时才能生效。
- **需要 Drafts Pro 订阅** - 自动化功能需要 Pro 订阅。

如果命令执行失败或卡住，请首先检查：`open -a Drafts`

## 安装

通过 Go 安装：
```bash
go install github.com/nerveband/drafts/cmd/drafts@latest
```

或从源代码编译：
```bash
git clone https://github.com/nerveband/drafts
cd drafts && go build ./cmd/drafts
```

## 命令

### 创建笔记

```bash
# Simple draft
drafts create "Meeting notes for Monday"

# With tags
drafts create "Shopping list" -t groceries -t todo

# Flagged draft
drafts create "Urgent reminder" -f

# Create in archive
drafts create "Reference note" -a
```

### 列出笔记

```bash
# List inbox (default)
drafts list

# List archived drafts
drafts list -f archive

# List trashed drafts
drafts list -f trash

# List all drafts
drafts list -f all

# Filter by tag
drafts list -t mytag
```

### 获取笔记内容

```bash
# Get specific draft
drafts get <uuid>

# Get active draft (currently open in Drafts)
drafts get
```

### 修改笔记内容

```bash
# Prepend text
drafts prepend "New first line" -u <uuid>

# Append text
drafts append "Added at the end" -u <uuid>

# Replace entire content
drafts replace "Completely new content" -u <uuid>
```

### 在编辑器中编辑笔记

```bash
drafts edit <uuid>
```

### 运行自定义操作

```bash
# Run action on text
drafts run "Copy" "Text to copy to clipboard"

# Run action on existing draft
drafts run "Copy" -u <uuid>
```

### 获取笔记的元数据（schema）

```bash
# Full schema for LLM integration
drafts schema

# Schema for specific command
drafts schema create
```

## 输出格式

- **JSON（默认）**：所有命令返回结构化的 JSON 数据。
- **纯文本**：以人类可读的形式输出结果。

## 常见使用场景

- **快速记录**  
- **每日日志**  
- **搜索与审阅**

## 故障排除

- **命令执行失败或返回空结果**：
  1. Drafts 是否正在运行？ → `open -a Drafts`
  2. 是否使用了 Drafts Pro？ → 自动化功能需要 Pro 订阅。
  3. 是否获得了必要的系统权限？ → 查看系统设置 > 隐私 > 自动化。

- **命令卡住**：
  - 检查 Drafts 是否显示了任何对话框或警告信息。

## 注意事项

- **仅支持 macOS（基于 AppleScript）**
- **Drafts 应用必须处于运行状态**
- **需要 Drafts Pro 订阅**
- 所有的 UUID 都是由 Drafts 生成的唯一标识符。
- 标签区分大小写。

## 版本

最新版本（通过 Go 安装获得）