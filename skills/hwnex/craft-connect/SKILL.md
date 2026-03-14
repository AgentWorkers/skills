---
name: craft
description: 通过 Craft Connect API 读取和写入 Craft 文档。当用户需要创建、读取、更新或搜索 Craft 文档、管理任务、编写每日笔记、组织文件夹、处理集合（结构化数据库）或格式化富文本内容时，可以使用该 API。该 API 支持所有类型的文档块，包括切换按钮（toggles）、标注（callouts）、表格（tables）、代码块（code）、高亮显示（highlights）、数学公式（math formulas）、图片（images）、卡片（cards）以及带样式的文本（styled text）。**不适用于将笔记保存到本地文件或使用其他无关的文档编辑器**。**所需配置：** CRAFT_API_URL（包含链接令牌的 Craft Connect API 基础 URL，存储在 TOOLS.md 文件中）。所有 HTTP 请求均使用 curl 工具进行。
---
# Craft 文档管理

通过 Craft Connect REST API 对 Craft 空间进行操作。支持对文档、块、文件夹、任务、集合和评论进行完整的创建（Create）、读取（Read）、更新（Update）和删除（Delete, CRUD）操作。

## 所需工具

- **curl**：用于所有 API 请求
- **CRAFT_API_URL**：您的 Craft Connect API 基本 URL（其中包含用于身份验证的链接令牌）

## 设置

1. 在您的 Craft 空间中创建一个 Craft Connect 链接（设置 → 连接 → 创建链接）
2. 复制 API 基本 URL 并将其保存在 `TOOLS.md` 文件的 `Craft` 部分中：

```
CRAFT_API_URL=https://connect.craft.do/links/<LINK_ID>/api/v1
```

3. 在进行任何调用之前，请先阅读 `TOOLS.md` 文件以获取正确的 URL。

所有请求都使用 `curl`，写入操作时设置 `-H "Content-Type: application/json"`，读取操作时设置 `-H "Accept: application/json"`。

**重要提示：** 对查询参数中的非 ASCII 字符（如中文字符）进行 URL 编码。

---

## API 参考

### 连接信息

```bash
curl -s "$CRAFT_API_URL/connection"
```

返回空间 ID、时区、当前时间以及深度链接模板。

### 发现（Discovery）

```bash
# List all folders and locations
curl -s "$CRAFT_API_URL/folders"

# List documents in a location (unsorted | trash | templates | daily_notes)
curl -s "$CRAFT_API_URL/documents?location=unsorted"

# List documents in a folder
curl -s "$CRAFT_API_URL/documents?folderId=<FOLDER_ID>"

# With metadata (creation/modification dates, deep links)
curl -s "$CRAFT_API_URL/documents?location=unsorted&fetchMetadata=true"

# Date filters (ISO YYYY-MM-DD or: today, yesterday, tomorrow)
curl -s "$CRAFT_API_URL/documents?createdDateGte=2025-01-01&lastModifiedDateLte=today"
```

### 搜索（Search）

```bash
# Search across ALL documents (URL-encode non-ASCII!)
curl -s "$CRAFT_API_URL/documents/search?include=<TERM>&fetchMetadata=true"

# Search within a specific document (with context blocks)
curl -s "$CRAFT_API_URL/blocks/search?blockId=<DOC_ID>&pattern=<REGEX>&beforeBlockCount=2&afterBlockCount=2"

# Filter search by folder or location
curl -s "$CRAFT_API_URL/documents/search?include=<TERM>&folderIds=<FOLDER_ID>"
curl -s "$CRAFT_API_URL/documents/search?include=<TERM>&location=daily_notes"
```

### 文档（Documents）

```bash
# Create document (defaults to unsorted)
curl -s -X POST "$CRAFT_API_URL/documents" \
  -H "Content-Type: application/json" \
  -d '{"documents": [{"title": "My Document"}]}'

# Create in a specific folder
curl -s -X POST "$CRAFT_API_URL/documents" \
  -H "Content-Type: application/json" \
  -d '{"documents": [{"title": "Doc"}], "destination": {"folderId": "<ID>"}}'

# Create as template
curl -s -X POST "$CRAFT_API_URL/documents" \
  -H "Content-Type: application/json" \
  -d '{"documents": [{"title": "Template"}], "destination": {"destination": "templates"}}'

# Delete (soft-delete to trash, recoverable)
curl -s -X DELETE "$CRAFT_API_URL/documents" \
  -H "Content-Type: application/json" \
  -d '{"documentIds": ["<DOC_ID>"]}'

# Move between locations
curl -s -X PUT "$CRAFT_API_URL/documents/move" \
  -H "Content-Type: application/json" \
  -d '{"documentIds": ["<ID>"], "destination": {"folderId": "<FOLDER_ID>"}}'

# Restore from trash
curl -s -X PUT "$CRAFT_API_URL/documents/move" \
  -H "Content-Type: application/json" \
  -d '{"documentIds": ["<ID>"], "destination": {"destination": "unsorted"}}'
```

### 读取内容（Reading Content）

```bash
# Get document content (JSON)
curl -s "$CRAFT_API_URL/blocks?id=<DOC_ID>" -H "Accept: application/json"

# Get daily note
curl -s "$CRAFT_API_URL/blocks?date=today" -H "Accept: application/json"

# Control depth (0=block only, 1=direct children, -1=all)
curl -s "$CRAFT_API_URL/blocks?id=<ID>&maxDepth=1"

# With metadata (comments, authors, timestamps)
curl -s "$CRAFT_API_URL/blocks?id=<ID>&fetchMetadata=true"
```

### 写入内容（Writing Content）

有两种方法：**Markdown**（推荐）和 **Blocks JSON**。

#### 方法 1：Markdown（推荐）

适用于大多数内容。Craft 会自动解析 Markdown 并生成正确的块类型、缩进级别和列表样式。

```bash
curl -s -X POST "$CRAFT_API_URL/blocks" \
  -H "Content-Type: application/json" \
  -d '{
    "markdown": "## Heading\n\nParagraph\n\n- bullet 1\n- bullet 2",
    "position": {"position": "end", "pageId": "<DOC_ID>"}
  }'
```

#### 方法 2：Blocks JSON

当您需要对 `color`、`font`、`textStyle` 等属性进行显式控制时使用（这些属性在纯 Markdown 中无法表示）。

```bash
curl -s -X POST "$CRAFT_API_URL/blocks" \
  -H "Content-Type: application/json" \
  -d '{
    "blocks": [
      {"type": "text", "textStyle": "h2", "markdown": "## Title"},
      {"type": "text", "color": "#00A3CB", "markdown": "<callout>💡 Info</callout>"}
    ],
    "position": {"position": "end", "pageId": "<DOC_ID>"}
  }'
```

#### 位置选项（Position Options）

| 位置 | 语法 |
|------|--------|
| 添加到文档末尾 | `{"position": "end", "pageId": "<DOC_ID>"}` |
| 添加到文档开头 | `{"position": "start", "pageId": "<DOC_ID>"}` |
| 添加到特定块之后 | `{"position": "after", "siblingId": "<BLOCK_ID>"}` |
| 添加到特定块之前 | `{"position": "before", "siblingId": "<BLOCK_ID>"}` |
| 添加到每日笔记中 | `{"position": "end", "date": "today"}` |

### 更新和删除块（Updating & Deleting Blocks）

```bash
# Update (only provided fields change; others preserved)
curl -s -X PUT "$CRAFT_API_URL/blocks" \
  -H "Content-Type: application/json" \
  -d '{"blocks": [{"id": "<BLOCK_ID>", "markdown": "Updated", "font": "serif"}]}'

# Delete blocks (permanent!)
curl -s -X DELETE "$CRAFT_API_URL/blocks" \
  -H "Content-Type: application/json" \
  -d '{"blockIds": ["<ID1>", "<ID2>"]}'

# Move blocks between documents
curl -s -X PUT "$CRAFT_API_URL/blocks/move" \
  -H "Content-Type: application/json" \
  -d '{"blockIds": ["<ID>"], "position": {"position": "end", "pageId": "<DOC_ID>"}}'
```

### 任务（Tasks）

```bash
# List tasks (scopes: inbox, active, upcoming, logbook, document)
curl -s "$CRAFT_API_URL/tasks?scope=active"
curl -s "$CRAFT_API_URL/tasks?scope=document&documentId=<DOC_ID>"

# Create task in inbox
curl -s -X POST "$CRAFT_API_URL/tasks" \
  -H "Content-Type: application/json" \
  -d '{"tasks": [{"markdown": "Task text", "taskInfo": {"scheduleDate": "tomorrow"}, "location": {"type": "inbox"}}]}'

# Create task in daily note
curl -s -X POST "$CRAFT_API_URL/tasks" \
  -H "Content-Type: application/json" \
  -d '{"tasks": [{"markdown": "Task", "taskInfo": {"scheduleDate": "2025-01-20", "deadlineDate": "2025-01-22"}, "location": {"type": "dailyNote", "date": "today"}}]}'

# Create task in a document
curl -s -X POST "$CRAFT_API_URL/tasks" \
  -H "Content-Type: application/json" \
  -d '{"tasks": [{"markdown": "Task", "location": {"type": "document", "documentId": "<DOC_ID>"}}]}'

# Complete task
curl -s -X PUT "$CRAFT_API_URL/tasks" \
  -H "Content-Type: application/json" \
  -d '{"tasksToUpdate": [{"id": "<TASK_ID>", "taskInfo": {"state": "done"}}]}'

# Delete task
curl -s -X DELETE "$CRAFT_API_URL/tasks" \
  -H "Content-Type: application/json" \
  -d '{"idsToDelete": ["<TASK_ID>"]}'
```

### 文件夹（Folders）

```bash
# Create folder (root level)
curl -s -X POST "$CRAFT_API_URL/folders" \
  -H "Content-Type: application/json" \
  -d '{"folders": [{"name": "New Folder"}]}'

# Create nested folder
curl -s -X POST "$CRAFT_API_URL/folders" \
  -H "Content-Type: application/json" \
  -d '{"folders": [{"name": "Sub", "parentFolderId": "<PARENT_ID>"}]}'

# Delete folder (docs move to parent or Unsorted)
curl -s -X DELETE "$CRAFT_API_URL/folders" \
  -H "Content-Type: application/json" \
  -d '{"folderIds": ["<FOLDER_ID>"]}'

# Move folder
curl -s -X PUT "$CRAFT_API_URL/folders/move" \
  -H "Content-Type: application/json" \
  -d '{"folderIds": ["<ID>"], "destination": "root"}'
# or: "destination": {"parentFolderId": "<ID>"}
```

### 集合（Collections）

集合类似于 Notion 数据库——具有类型化的列的结构化表格。

```bash
# List all collections
curl -s "$CRAFT_API_URL/collections"

# Create collection in a document
curl -s -X POST "$CRAFT_API_URL/collections" \
  -H "Content-Type: application/json" \
  -d '{
    "schema": {
      "name": "Tasks",
      "contentPropDetails": {"name": "Title"},
      "properties": [
        {"name": "Status", "type": "singleSelect", "options": [{"name": "Todo"}, {"name": "In Progress"}, {"name": "Done"}]},
        {"name": "Priority", "type": "singleSelect", "options": [{"name": "High"}, {"name": "Medium"}, {"name": "Low"}]},
        {"name": "Due Date", "type": "date"}
      ]
    },
    "position": {"position": "end", "pageId": "<DOC_ID>"}
  }'

# Get schema (use json-schema-items format to learn the property keys!)
curl -s "$CRAFT_API_URL/collections/<COL_ID>/schema?format=json-schema-items"
# ⚠️ IMPORTANT: schema returns auto-generated keys like "", "_2", "_3", "_4"
# You MUST read the schema first to know the correct keys for items

# Get items
curl -s "$CRAFT_API_URL/collections/<COL_ID>/items"

# Add items (use schema keys, NOT "title"!)
# First GET the schema to find the contentProp key (e.g. "_4" for title)
curl -s -X POST "$CRAFT_API_URL/collections/<COL_ID>/items" \
  -H "Content-Type: application/json" \
  -d '{"items": [{"<CONTENT_KEY>": "Item Title", "properties": {"<STATUS_KEY>": "Todo", "<PRIORITY_KEY>": "High"}}]}'

# Update items
curl -s -X PUT "$CRAFT_API_URL/collections/<COL_ID>/items" \
  -H "Content-Type: application/json" \
  -d '{"itemsToUpdate": [{"id": "<ITEM_ID>", "properties": {"<STATUS_KEY>": "Done"}}]}'

# Delete items
curl -s -X DELETE "$CRAFT_API_URL/collections/<COL_ID>/items" \
  -H "Content-Type: application/json" \
  -d '{"idsToDelete": ["<ITEM_ID>"]}'

# Update schema (replaces entirely — include ALL fields you want to keep)
curl -s -X PUT "$CRAFT_API_URL/collections/<COL_ID>/schema" \
  -H "Content-Type: application/json" \
  -d '{"schema": { ... }}'
```

### 评论（Comments）

```bash
curl -s -X POST "$CRAFT_API_URL/comments" \
  -H "Content-Type: application/json" \
  -d '{"comments": [{"blockId": "<BLOCK_ID>", "content": "Comment text"}]}'
```

### 上传文件（File Upload）

```bash
curl -s -X POST "$CRAFT_API_URL/upload?position=end&pageId=<DOC_ID>" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @file.png
```

位置参数：`position`（start|end|before|after）+ `pageId`/`date`/`siblingId`。

---

## 块类型与格式（Block Types & Formatting）

### 标题（Headings）

```markdown
# H1 Title          → textStyle: "h1"
## H2 Subtitle      → textStyle: "h2"
### H3 Heading      → textStyle: "h3"
#### H4 Strong      → textStyle: "h4"
```

### 内联样式（Inline Styles）

```markdown
**bold**, *italic*, ~strikethrough~, `inline code`
[link text](https://url)
$(a+b)^2$                    ← inline equation
```

### 高亮显示（Highlight Styles, 9 种纯色 + 5 种渐变）

#### 纯色：`yellow`, `blue`, `red`, `green`, `purple`, `pink`, `mint`, `cyan`, `gray`
#### 渐变：`gradient-blue`, `gradient-purple`, `gradient-red`, `gradient-yellow`, `gradient-brown`

### 列表（Lists）

```markdown
- bullet item           → listStyle: "bullet"
1. numbered item        → listStyle: "numbered"
- [ ] todo task         → listStyle: "task", taskInfo.state: "todo"
- [x] completed task    → listStyle: "task", taskInfo.state: "done"
+ toggle (collapsible)  → listStyle: "toggle"
```

### 可折叠列表（Toggle (Collapsible Lists) — 非常重要**

子列表必须缩进 2 个空格才能正确嵌套在可折叠列表中：

```markdown
+ Parent toggle
  - Child 1 (hidden when collapsed)
  - Child 2
  + Nested toggle
    - Deep child
```

**仅使用 Markdown 模式。** 在使用 Blocks JSON 时，`indentationLevel` 参数会被忽略。

### 引用（Blockquote）

```markdown
> Quoted text
```

生成带有 `decorations: ["quote"]` 标签的引用块。

### 分隔符/行（Dividers / Lines）

使用 Blocks JSON 时设置 `lineStyle`：

```json
{"type": "line", "lineStyle": "extraLight", "markdown": "***"}
{"type": "line", "lineStyle": "light", "markdown": "****"}
{"type": "line", "lineStyle": "regular", "markdown": "*****"}
{"type": "line", "lineStyle": "strong", "markdown": "******"}
```

在 Markdown 模式下，`---` 会默认生成 `extraLight` 样式的文本。

### 代码块（Code Blocks）

#### Markdown 模式：

```markdown
def hello():
    print("Hello")
```

#### Blocks JSON 模式：

```json
{
  "type": "code",
  "language": "math_formula",
  "rawCode": "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
  "markdown": "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}"
```

#### 使用 Blocks JSON 时需要指定 `rawCode` 字段：

```json
{
  "type": "code",
  "language": "math_formula",
  "rawCode": "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
  "markdown": "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}"
}
```

#### 表格（Tables）

```markdown
| 列 A | 列 B |
| --- | --- |
| val 1 | val 2 |
```

#### 图片（Images）

```json
{
  "type": "image",
  "url": "https://example.com/photo.jpg",
  "markdown": "![图片说明](https://example.com/photo.jpg)"
}
```

#### 富文本链接（Rich Urls）

```json
{
  "type": "richUrl",
  "url": "https://www.youtube.com/watch?v=..."
}
```

#### 页面（Pages）

```json
{
  "type": "page",
  "textStyle": "page",
  "markdown": "子页面标题"
}
```

#### 卡片（Cards）

```json
{
  "type": "page",
  "textStyle": "card",
  "markdown": "卡片标题"
}
```

#### 文本（Text）

```json
{
  "type": "text",
  "color": "#00A3CB",
  "markdown": "<callout>💡 信息</callout>"
}
```

#### 注释（Comments）

```json
{
  "type": "text",
  "textStyle": "caption",
  "markdown": "<caption>小注释"</caption>
}
```

#### 任务（Tasks）

```json
{
  "type": "text",
  "listStyle": "task",
  "taskInfo": {"state": "todo"},
  "markdown": "- [ ] 任务"
}
```

---

## 选择插入方法（Choosing Insert Method）

| 需要插入的内容 | 使用的方法 | 原因 |
|------------|------------|---------|
| 文本、列表、标题 | Markdown | 更简洁，能自动识别内容类型 |
| 带有子列表的可折叠元素 | Markdown | 是确保正确缩进的唯一方法 |
| 代码块、表格 | 两者均可 | Markdown 更简单；JSON 需要指定 `rawCode` |
| 带颜色的注释 | Blocks JSON | 需要 `color` 属性 |
| 自定义字体 | Blocks JSON | 需要 `font` 属性 |
| 图片、富文本链接、页面 | Blocks JSON | 需要指定 `type` 属性 |
| 行样式 | Blocks JSON | 需要 `lineStyle` 属性 |
| 数学公式 | Blocks JSON | 需要指定 `language: "math_formula"` 和 `rawCode` |
| 混合内容 | 分别使用 Markdown 和 Blocks JSON |

---

## 注意事项与经验总结

1. **可折叠列表的缩进**：必须使用 2 个空格进行缩进。
   在使用 Blocks JSON 时，`indentationLevel` 参数会被忽略。

2. **任务状态**：使用 `todo`、`done` 或 `canceled`，而不是 `completed`。

3. 使用 `siblingId` 而不是 `blockId` 来指定块的位置。

4. 使用 `pageId` 或 `date` 来指定位置的开始或结束。

5. 在使用 Blocks JSON 时，代码块需要包含 `rawCode` 字段；否则会导致验证错误。

6. **集合项的键**：API 文档中可能写的是 `title`，但实际上使用的键是自动生成的 `contentProp`（例如 `_4`）。在写入集合项之前，务必先使用 `GET /collections/<id>/schema?format=json-schema-items` 来获取正确的键。

7. 对查询参数中的中文字符和特殊字符进行 URL 编码；否则 `curl` 会返回 400 错误。

8. 请求头：读取操作时使用 `application/json`；使用 `text/markdown` 会导致 502 错误。

9. 文档的删除操作是“软删除”：文档会被移至回收站，可以通过移动操作恢复。块的删除操作是不可逆的。

10. 大量内容插入：一次 POST 请求可以插入多个块。为避免达到速率限制，建议分多次插入。

11. 图片会被重新托管：Craft 会下载外部图片并将其重新托管在 `https://r.craft.do/`。原始图片链接会被替换。

12. 集合功能仍处于实验阶段：API 可能会发生变化。在写入数据之前，请务必查看相关规范。