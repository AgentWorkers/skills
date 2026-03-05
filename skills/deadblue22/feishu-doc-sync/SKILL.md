---
name: feishu-doc-sync
description: >
  飞书文档增量同步与表格操作指南。涵盖以下内容：  
  - 表格更新策略（包括删除（delete）和插入（insert）操作）  
  - header_row 的设置方法  
  - 插入数据的操作（insert action）  
  - 列宽的计算与调整算法  
  - 三阶段差异（diff）同步机制  
  本指南适用于需要将本地文档同步到飞书、对飞书中的表格进行操作或进行增量编辑的场景。
---
# Feishu 文档工具

`feishu_doc` 是一个单一的工具，通过提供不同的操作参数来执行所有的文档操作，包括创建 Docx 格式的文档。

## 令牌提取

从 URL `https://xxx.feishu.cn/docx/ABC123def` 中提取令牌 → `doc_token` = `ABC123def`

## 操作

### 读取文档

```json
{ "action": "read", "doc_token": "ABC123def" }
```

返回：文档标题、纯文本内容以及各块的信息统计。如果 `hint` 字段存在，说明文档中包含需要使用 `list_blocks` 方法处理的结构化内容（如表格、图片等）。

### 写入文档（替换全部内容）

```json
{ "action": "write", "doc_token": "ABC123def", "content": "# Title\n\nMarkdown content..." }
```

用 Markdown 内容替换整个文档。支持以下内容类型：标题、列表、代码块、引文、链接、图片（`![](url)` 会自动上传）、粗体/斜体/删除线，以及 Markdown 表格。

### 添加内容

```json
{ "action": "append", "doc_token": "ABC123def", "content": "Additional content" }
```

将 Markdown 内容添加到文档末尾。支持与 `write` 相同的内容类型，包括 Markdown 表格。

### 插入内容（指定位置）

```json
{
  "action": "insert",
  "doc_token": "ABC123def",
  "after_block_id": "doxcnXXX",
  "content": "Markdown content including tables..."
}
```

在指定位置插入内容。内部使用 Descendant API，支持所有类型的块，包括表格。

**关键用法：** 这是精确插入内容的主要方法。首先使用 `list_blocks` 找到目标块的位置（`after_block_id`）。

### 创建文档

```json
{ "action": "create", "title": "New Document", "owner_open_id": "ou_xxx" }
```

如果需要使用文件夹，请按照以下步骤操作：

```json
{
  "action": "create",
  "title": "New Document",
  "folder_token": "fldcnXXX",
  "owner_open_id": "ou_xxx"
}
```

**重要提示：** 在调用创建文档的 API 时，必须传递请求用户的 `open_id`（来自传入元数据的 `sender_id`），这样用户才能自动获得对创建文档的 `full_access` 权限。否则，只有机器人应用程序才能访问该文档。

### 列出所有块

```json
{ "action": "list_blocks", "doc_token": "ABC123def" }
```

返回所有块的数据，包括表格和图片。可以使用这些数据来读取结构化内容并获取块的 ID 以便进行后续操作。

### 获取单个块

```json
{ "action": "get_block", "doc_token": "ABC123def", "block_id": "doxcnXXX" }
```

### 更新块内容

```json
{
  "action": "update_block",
  "doc_token": "ABC123def",
  "block_id": "doxcnXXX",
  "content": "New text with **bold** and `code`"
}
```

支持 Markdown 的内联样式：`**粗体**、````、`code`、`[link](url)`、`~~strike~~`。

**支持的块类型：** 文本、标题、项目符号列表、有序列表、代码块、引文、待办事项列表。

**⚠️ 注意：** 对于表格，使用 `update_block` 会将其内容替换为纯文本，导致所有内联格式（如内联代码、粗体等）丢失。

### 删除块

```json
{ "action": "delete_block", "doc_token": "ABC123def", "block_id": "doxcnXXX" }
```

### 创建表格

```json
{
  "action": "create_table",
  "doc_token": "ABC123def",
  "row_size": 2,
  "column_size": 2,
  "column_width": [200, 200]
}
```

**⚠️ 注意：** 对于表格，`parent_block_id` 和 `index` 参数的定位方式不可靠——表格总是会被插入到文档的末尾。建议使用 `insert` 操作并指定 `after_block_id` 来定位表格。

### 写入表格单元格

```json
{
  "action": "write_table_cells",
  "doc_token": "ABC123def",
  "table_block_id": "doxcnTABLE",
  "values": [
    ["A1", "B1"],
    ["A2", "B2"]
  ]
}
```

将纯文本写入表格单元格。支持在单元格值中使用 Markdown 内联样式。

**注意：** 这个操作会清除并重新构建单元格内的所有内容。适用于填充表格或完全替换单元格内容，但不适用于部分编辑。

### 一步创建带内容的表格

```json
{
  "action": "create_table_with_values",
  "doc_token": "ABC123def",
  "row_size": 2,
  "column_size": 2,
  "column_width": [200, 200],
  "values": [["A1", "B1"], ["A2", "B2"]]
}
```

**⚠️ 与 `create_table` 一样，位置定位不可靠**——建议使用 `insert` 操作来定位表格。

### 表格行/列操作

```json
{ "action": "insert_table_row", "doc_token": "...", "table_block_id": "...", "row_index": -1 }
{ "action": "insert_table_column", "doc_token": "...", "table_block_id": "...", "column_index": -1 }
{ "action": "delete_table_rows", "doc_token": "...", "block_id": "...", "row_start": 1, "row_count": 1 }
{ "action": "delete_table_columns", "doc_token": "...", "block_id": "...", "column_start": 0, "column_count": 1 }
{ "action": "merge_table_cells", "doc_token": "...", "table_block_id": "...", "row_start": 0, "row_end": 2, "column_start": 0, "column_end": 2 }
```

**注意：** 在使用 `delete_table_rows` 时，请使用 `block_id`（而不是 `table_block_id`）和 `row_start`（而不是 `row_index`）。

### 上传图片

```json
{ "action": "upload_image", "doc_token": "ABC123def", "url": "https://example.com/image.png" }
```

可以使用本地路径或指定位置来上传图片：

```json
{
  "action": "upload_image",
  "doc_token": "ABC123def",
  "file_path": "/tmp/image.png",
  "parent_block_id": "doxcnParent",
  "index": 5
}
```

也可以使用 Base64 数据 URI 上传图片：

```json
{
  "action": "upload_image",
  "doc_token": "ABC123def",
  "image": "data:image/png;base64,iVBOR..."
}
```

**注意：** 图片的显示大小由上传的图片像素尺寸决定。对于小图片（例如 480x270），建议在上传前将其缩放至 800px 以上。

### 上传文件附件

```json
{ "action": "upload_file", "doc_token": "ABC123def", "url": "https://example.com/report.pdf" }
```

可以使用本地路径或指定路径来上传文件附件：

```json
{ "action": "upload_file", "doc_token": "ABC123def", "file_path": "/tmp/report.pdf", "filename": "Q1-report.pdf" }
```

### 更改文本颜色

```json
{
  "action": "color_text",
  "doc_token": "ABC123def",
  "block_id": "doxcnXXX",
  "content": "colored text",
  "color": "red"
}
```

## 阅读文档的工作流程

1. 首先使用 `action: "read"` 来获取纯文本内容和统计信息。
2. 检查响应中的 `block_types`，判断文档中是否包含表格、图片、代码块等结构化内容。
3. 如果存在结构化内容，使用 `action: "list_blocks"` 来获取完整的数据。

---

## 增量同步的最佳实践

### 何时使用增量同步与全量同步

- **如果只有不到 5 个块发生变化** → 使用增量同步（删除和插入单个块）。
- **如果超过 80% 的块发生变化** → 使用全量同步（通过 `write` 操作替换全部内容）。
- **如果只有单个表格发生变化** → 删除旧表格并插入新表格。

### 表格更新策略：删除 + 插入

表格绝对不能直接在原地编辑。始终使用以下方法：

```
1. list_blocks → find the block before the table (anchor_block_id)
2. delete_block(block_id = old_table_id)
3. insert(after_block_id = anchor_block_id, content = "| new | table |...")
```

**为什么不能直接编辑表格？**
- 对表格单元格使用 `update_block` 会删除所有内联格式（如内联代码、粗体、链接等）。
- 使用 `write_table_cells` 会清除并重新构建单元格内容，同样会导致格式丢失。
- 使用 `create_table` 或 `create_table_with_values` 会导致表格位置定位不准确。

### 多块批量替换

当多个连续的块发生变化时：

1. 找到未发生变化的最后一个块作为基准块。
2. 以相反的顺序删除发生变化的块（以避免索引错位）。
3. 使用一次 `insert` 操作插入所有新的内容（支持不同类型的块）。

### 差异同步策略（来自 feishu-doc-sync）

1. 通过块签名（类型和内容）进行匹配，通过哈希值来检测变化。
2. 对比本地和远程块的文本内容。
3. 分三步执行同步操作：**更新**（文本块）→ **删除**（按相反顺序）→ **插入**（按顺序）。
4. 对于表格，如果结构相同，可以只更新单元格内容；如果结构不同，则需要替换整个表格。
5. 如果变化率超过 80%，则进行全量同步。

---

## 表格标题行（深色背景）

`header_row: true` 属性可以为表格设置深色标题背景。这是一个常见的需求。

### ⚠️ 重要提示：** `header_row` 只能在创建表格时设置

**PATCH API (`update_table_property`) 不支持设置 `header_row` —— 它会返回 `code: 0` 表示操作成功，但实际上不会应用该属性。这适用于单个块的更新和批量更新操作。**

### 如何创建带有标题行的表格

由于 `insert` 操作（Descendant API）和 `create_table` 操作不支持设置 `header_row`，因此必须使用原始的 Feishu API：

```bash
# Step 1: Get tenant_access_token
TOKEN=$(curl -s https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{"app_id":"'$APP_ID'","app_secret":"'$APP_SECRET'"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")

# Step 2: Create empty table with header_row via document_block_children.create
curl -s -X POST \
  "https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{doc_token}/children?document_revision_id=-1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [{
      "block_type": 31,
      "table": {
        "property": {
          "row_size": 3,
          "column_size": 2,
          "header_row": true,
          "column_width": [300, 400]
        }
      }
    }],
    "index": 5
  }'

# Step 3: Fill cells via feishu_doc write_table_cells
# (use the new table's block_id from step 2 response)
```

**凭据：** 从 `/root/.openclaw/openclaw.json` 中读取 `channels.feishu.appId` 和 `channels.feishu.appSecret`。

### 创建带有标题行的表格的工作流程

1. 使用 `list_blocks` 找到基准块和目标位置。
2. （如果需要替换表格）使用 `delete_block` 删除旧表格。
3. 使用原始 API `document_block_children.create` 在正确的位置创建一个带有 `header_row: true` 的空表格。
4. 使用 `feishu_doc.write_table_cells` 填充表格内容。
5. 使用 `get_block` 验证表格是否具有标题行。

### 列宽计算算法

使用 `insert` 操作（Descendant API）时，列宽会自动计算：
- 总宽度约为 730px。
- 中文和日文字符的宽度会被计算为正常宽度的两倍。
- 列宽会按比例分配，范围在 50–400px 之间。
- 如果使用原始 API，需要手动指定 `column_width`。

---

## 同步前的准备工作

- **在读取本地仓库文件之前，请务必执行 `git pull` —— 以确保获取最新内容。**
- **在写入数据之前，请先进行比较** —— 使用 `read` 或 `list_blocks` 来检查当前文档的状态。
- **注意格式的保留** —— 表格单元格中的内联代码、粗体、链接等格式需要特别处理。

## 配置设置

```yaml
channels:
  feishu:
    tools:
      doc: true  # default: true
```

**注意：** `feishu_wiki` 依赖于这个工具 —— 维基页面的内容是通过 `feishu_doc` 来读写的。

## 权限要求

需要以下权限：`docx:document`、`docx:document:readonly`、`docx:document:block:convert`、`drive:drive`