---
name: inkdrop
description: 通过 Inkdrop 的本地 HTTP 服务器 API，您可以执行以下操作：读取、创建、更新、搜索和删除笔记。当用户需要记笔记、保存想法、管理项目笔记、阅读笔记或以任何方式与 Inkdrop 交互时，都可以使用这些 API。此外，这些 API 还可用于整理思路、项目待办事项或需要长期保存在 Inkdrop 中的任务列表。
env:
  INKDROP_AUTH:
    required: true
    description: "Basic auth credentials (user:password) from Inkdrop preferences"
  INKDROP_URL:
    required: false
    description: "Inkdrop local server URL (default: http://localhost:19840)"
---
# Inkdrop Notes

您可以通过与 Inkdrop 的本地 HTTP 服务器交互来管理笔记、笔记本和标签。

## 先决条件

1. 已安装并运行 [Inkdrop](https://inkdrop.app) 桌面应用程序。
2. 在 Inkdrop 的设置中启用了本地 HTTP 服务器（设置 → API → 启用本地 HTTP 服务器）。
3. 记下从 Inkdrop 设置中获取的端口、用户名和密码。

## 设置

设置环境变量：

```bash
export INKDROP_URL="http://localhost:19840"   # default port
export INKDROP_AUTH="username:password"        # from Inkdrop preferences
```

对于 OpenClaw，将凭据存储在 secrets 文件中（例如，工作区中的 `secrets.md` 文件），并在运行时加载这些凭据。避免将明文凭据保存在 shell 配置文件中。

## 连接

```
Base URL: http://localhost:19840 (or INKDROP_URL env var)
Auth: Basic auth via INKDROP_AUTH env var (user:password)
```

验证连接：

```bash
curl -s -u "$INKDROP_AUTH" "${INKDROP_URL:-http://localhost:19840}/"
# Returns: {"version":"5.x.x","ok":true}
```

## API 参考

所有端点都使用基本身份验证（Basic Auth）。请将 `USER:PASS` 替换为您的 `$INKDROP_AUTH` 值。

### 列出笔记

```bash
curl -s -u $INKDROP_AUTH http://localhost:19840/notes
```

查询参数：
- `keyword` — 搜索文本（与 Inkdrop 的搜索功能相同）
- `limit` — 最大结果数量（默认：全部）
- `skip` — 分页的偏移量
- `sort` — `updatedAt`、`createdAt` 或 `title`（排序依据）
- `descending` — 是否按降序显示（布尔值）

### 获取单个文档

```bash
curl -s -u $INKDROP_AUTH "http://localhost:19840/<docid>"
```

`docid` 是完整的 `_id`（例如，`note:abc123`、`book:xyz`）。适用于笔记、书籍、标签和文件。

可选参数：
- `rev` — 获取特定版本
- `attachments` — 是否包含附件数据（布尔值，适用于文件文档）

### 创建笔记

```bash
curl -s -u $INKDROP_AUTH -X POST http://localhost:19840/notes \
  -H "Content-Type: application/json" \
  -d '{
    "doctype": "markdown",
    "title": "Note Title",
    "body": "Markdown content here",
    "bookId": "book:inbox",
    "status": "none",
    "tags": []
  }'
```

 `_id` 会自动生成。`bookId` 是必填项——默认使用 `book:inbox`，或者可以先查找相应的笔记本。

### 更新笔记

使用 `_id` 和 `_rev` 发送 POST 请求（避免冲突）：

```bash
# 1. Get current _rev
REV=$(curl -s -u $INKDROP_AUTH "http://localhost:19840/note:abc123" | python3 -c "import sys,json; print(json.load(sys.stdin)['_rev'])")

# 2. Update with _rev
curl -s -u $INKDROP_AUTH -X POST http://localhost:19840/notes \
  -H "Content-Type: application/json" \
  -d '{
    "_id": "note:abc123",
    "_rev": "'"$REV"'",
    "doctype": "markdown",
    "title": "Updated Title",
    "body": "Updated content",
    "bookId": "book:inbox",
    "status": "none"
  }'
```

### 删除文档

```bash
curl -s -u $INKDROP_AUTH -X DELETE "http://localhost:19840/<docid>"
```

### 列出笔记本

```bash
curl -s -u $INKDROP_AUTH http://localhost:19840/books
```

### 创建笔记本

```bash
curl -s -u $INKDROP_AUTH -X POST http://localhost:19840/books \
  -H "Content-Type: application/json" \
  -d '{"name": "My Notebook"}'
```

### 列出标签

```bash
curl -s -u $INKDROP_AUTH http://localhost:19840/tags
```

### 创建标签

```bash
curl -s -u $INKDROP_AUTH -X POST http://localhost:19840/tags \
  -H "Content-Type: application/json" \
  -d '{"_id": "tag:mytag", "name": "mytag", "color": "blue"}'
```

### 列出/创建文件（包含附件）

```bash
curl -s -u $INKDROP_AUTH http://localhost:19840/files
```

通过向 `/files` 发送 POST 请求来创建文件。文件主要是用于笔记的图片附件。

### 变更通知

```bash
curl -s -u $INKDROP_AUTH "http://localhost:19840/_changes?since=0&limit=50&include_docs=true"
```

参数：`since`（序列号）、`limit`、`descending`、`include_docs`、`conflicts`、`attachments`。

按更改的顺序返回变更信息。这对于同步或监控更新非常有用。

## 辅助脚本

随附的 `scripts/inkdrop.sh` 脚本可以封装常见的操作：

```bash
export INKDROP_AUTH="username:password"

# List all notes
./scripts/inkdrop.sh notes

# Search notes
./scripts/inkdrop.sh search "project ideas"

# Get a specific note
./scripts/inkdrop.sh get "note:abc123"

# Create a note (title, bookId, body)
./scripts/inkdrop.sh create "My Note" "book:inbox" "Note content here"

# List notebooks
./scripts/inkdrop.sh books

# List tags
./scripts/inkdrop.sh tags

# Delete a document
./scripts/inkdrop.sh delete "note:abc123"
```

## 笔记模型

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `_id` | 字符串 | `note:<id>`（自动生成） |
| `_rev` | 字符串 | 版本令牌（更新时必需） |
| `title` | 字符串 | 笔记标题 |
| `body` | 字符串 | Markdown 内容 |
| `doctype` | 字符串 | 始终为 `"markdown"` |
| `bookId` | 字符串 | 笔记本 ID（例如，`book:inbox`） |
| `tags` | 字符串[] | 标签 ID 的数组 |
| `status` | 字符串 | `none`、`active`、`onHold`、`completed`、`dropped` |
| `pinned` | 布尔值 | 是否固定显示在顶部 |
| `share` | 字符串 | `private` 或 `public` |
| `createdAt` | 数字 | Unix 时间戳（毫秒） |
| `updatedAt` | 数字 | Unix 时间戳（毫秒） |

## 状态值

- `none` — 默认值
- `active` — 进行中
- `onHold` — 暂停
- `completed` — 完成
- `dropped` — 被放弃

## 规范

- 用于快速记录的默认笔记本：`book:inbox`
- 当上下文明确时，使用现有的笔记本（通过 `GET /books` 按名称查找）
- 在笔记正文中使用 Markdown 格式
- 在更新前始终获取 `_rev` 以避免冲突
- 标签 ID 使用 `tag:<name>` 格式