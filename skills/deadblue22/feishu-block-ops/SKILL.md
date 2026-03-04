---
name: feishu-block-ops
description: 通过 REST API 进行低级别的 Feishu 文档块操作。当 Feishu-doc 的内置功能不足以满足需求时，可以使用这些 API：批量更新单元格、精确插入内容、遍历文档块树、操作表格的行或列、替换图片，或任何需要直接控制文档块级别的操作。这些 API 是对 Feishu-doc 的补充，而非替代品。
---
# Feishu 块操作

当 `feishu_doc` 工具的内置功能无法满足您的需求时，可以使用这些直接的 REST API 操作来对 Feishu 云文档进行操作。

## 何时使用这些操作（相对于 `feishu_doc`）

| 需求 | 使用方法 |
|------|-----|
| 读取/写入/追加文档内容 | `feishu_doc` |
| 创建简单表格 | `feishu_doc` `create_table_with_values` |
| 上传图片/文件 | `feishu_doc` `upload_image`/`upload_file` |
| **批量更新 200 个单元格** | **使用这些操作** |
| **在指定位置插入内容** | **使用这些操作**（或 `feishu-md2blocks`） |
| **遍历块树** | **使用这些操作** |
| **插入/删除表格行/列** | **使用这些操作** |
| **合并/拆分表格单元格** | **使用这些操作** |
| **替换图片** | **使用这些操作** |
| **按索引范围删除块** | **使用这些操作** |

## 认证

从 OpenClaw 配置中获取租户访问令牌：

```python
import json, urllib.request

def get_feishu_token():
    with open(os.path.expanduser("~/.openclaw/openclaw.json")) as f:
        c = json.load(f)["channels"]["feishu"]
    payload = json.dumps({"app_id": c["appId"], "app_secret": c["appSecret"]}).encode()
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=payload, headers={"Content-Type": "application/json"}, method="POST")
    return json.loads(urllib.request.urlopen(req).read())["tenant_access_token"]
```

所有 API 调用都需要在请求头中添加以下字段：`Authorization: Bearer {token}`

## 速率限制

| 操作 | 限制 |
|-----------|-------|
| 读取（GET） | 每个应用每秒 5 次请求 |
| 写入（POST/PATCH/DELETE） | 每个应用每秒 3 次请求，每个文档每秒 3 次请求 |

写入操作之间请使用 `time.sleep(0.35)` 进行延迟。读取操作之间请使用 `time.sleep(0.25)` 进行延迟。

## API 参考

基础 URL：`https://open.feishu.cn/open-apis/docx/v1/documents`

### 1. 获取块

```
GET /docx/v1/documents/{doc}/blocks/{block_id}
```

返回包含完整内容的单个块（类型、元素、子块 ID、样式）。

### 2. 获取子块（可选包含整个块树）

```
GET /docx/v1/documents/{doc}/blocks/{block_id}/children
    ?with_descendants=true    # get ALL descendants, not just direct children
    &page_size=500            # max 500
    &document_revision_id=-1  # latest revision
```

**提示：** 对于表格块，使用 `with_descendants=true` 可以一次性获取所有单元格及其内容。

### 3. 创建块（仅支持简单结构）

```
POST /docx/v1/documents/{doc}/blocks/{parent_id}/children
Body: {"children": [...blocks], "index": 0}
```

- 每次调用最多创建 50 个块。
- **无法** 创建嵌套结构（例如包含单元格内容的表格）。
- 请求体中的 `index` 参数：0 表示开始，-1 表示结束（默认值）。

### 4. 创建嵌套块（表格、网格等）

```
POST /docx/v1/documents/{doc}/blocks/{parent_id}/descendant
Body: {
    "children_id": ["temp_id_1", "temp_id_2"],
    "descendants": [...all_blocks_with_parent_child_relations],
    "index": 0
}
```

- 每次调用最多创建 1000 个块。
- `children_id`：仅包含一级子块的 ID（包含孙子块会导致错误 1770006）。
- `descendants`：一个包含所有块（包括嵌套块）的扁平数组，每个块包含 `block_id`、`block_type` 和 `children`（子块 ID 的列表）。
- ⚠️ **`index` 必须在请求体中指定，不能作为 URL 查询参数** —— `?index=N` 会被忽略。

### 5. 批量更新块

```
PATCH /docx/v1/documents/{doc}/blocks/batch_update
Body: {"requests": [...update_requests]}
```

每次调用最多更新 200 个块。每个请求对象包含 `block_id` 和一个操作类型：

| 操作 | 功能 |
|-----------|---------|
| `update_text_elements` | 更改文本内容和内联元素 |
| `update_text_style` | 更改对齐方式、折叠方式、语言设置、换行设置、背景颜色 |
| `update_table_property` | 修改列宽、表头行/列 |
| `insert_table_row` | 在指定索引处插入行 |
| `insert_table_column` | 在指定索引处插入列 |
| `delete_table_rows` | 按索引和数量删除行 |
| `delete_table_columns` | 按索引和数量删除列 |
| `merge_table_cells` | 合并单元格（指定起始行/列和结束行/列） |
| `unmerge_table_cells` | 拆分之前合并的单元格 |
| `replace_image` | 用新的文件令牌替换图片块的内容 |

#### 示例：批量更新多个单元格中的文本

```python
requests = []
for block_id, new_text in updates.items():
    requests.append({
        "block_id": block_id,
        "update_text_elements": {
            "elements": [{"text_run": {"content": new_text}}]
        }
    })

api_call(token, "PATCH",
    f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc}/blocks/batch_update",
    {"requests": requests})
```

### 6. 更新单个块

```
PATCH /docx/v1/documents/{doc}/blocks/{block_id}
Body: {same operations as batch_update, without block_id wrapper}
```

### 7. 删除块

```
DELETE /docx/v1/documents/{doc}/blocks/{parent_id}/children/batch_delete
Body: {"start_index": 0, "end_index": 5}
```

- ⚠️ 使用 `start_index`/`end_index`（半开区间 `[start, end)`，**不能** 使用 `block_ids`。
- 索引是相对于父块的子块列表的。

## 块类型

| 类型 | ID | 说明 |
|------|---:|-------|
| Page | 1 | 文档的根块，始终只有一个 |
| Text | 2 | 普通段落 |
| Heading1–9 | 3–11 | 标题 1–9 |
| Bullet | 12 | 无序列表项 |
| Ordered | 13 | 有序列表项 |
| Code | 14 | 代码块 |
| Quote | 15 | 引用块 |
| Todo | 17 | 待办事项项 |
| Callout | 19 | 高亮显示的块 |
| Divider | 22 | 水平分隔线（内容：`{}`） |
| Grid | 24 | 多列布局 |
| GridColumn | 25 | 网格中的列 |
| Image | 27 | 图片块 |
| Table | 31 | 表格容器 |
| TableCell | 32 | 表格中的单元格 |
| QuoteContainer | 34 | 引用框（内容：`{}`） |

## 文本元素

文本块包含一个 `elements` 数组。每个元素可以是以下类型之一：

```python
# Plain text
{"text_run": {"content": "hello", "text_element_style": {"bold": True, "link": {"url": "..."}}}}

# Mention user
{"mention_user": {"user_id": "ou_xxx", "text_element_style": {}}}

# Mention document
{"mention_doc": {"token": "xxx", "obj_type": 22, "text_element_style": {}}}

# Equation (LaTeX)
{"equation": {"content": "E=mc^2"}}

# Reminder
{"reminder": {"expire_time": 1234567890, "is_whole_day": True}}
```

## 常见用法模式

### 模式 1：读取表格内容

```python
# 1. Get table's descendants in one call
url = f".../blocks/{table_block_id}/children?with_descendants=true&page_size=500&document_revision_id=-1"
items = api_call(token, "GET", url)["data"]["items"]

# 2. Extract text from cells
for item in items:
    if item["block_type"] == 2 and "text" in item:
        text = "".join(e.get("text_run", {}).get("content", "") for e in item["text"]["elements"])
```

### 模式 2：在指定位置插入 Markdown 内容

使用 `feishu-md2blocks` 的 `md2blocks.py` 脚本，并加上 `--after <block_id>` 参数。

或者手动操作：
```python
# 1. Convert markdown
convert_resp = api_call(token, "POST", ".../blocks/convert",
    {"content_type": "markdown", "content": md_text})

# 2. Clean table blocks (remove merge_info)
for block in convert_resp["data"]["blocks"]:
    if block.get("block_type") == 31 and "table" in block:
        block["table"]["property"].pop("merge_info", None)

# 3. Insert at position (index IN BODY)
api_call(token, "POST", f".../blocks/{parent_id}/descendant", {
    "children_id": convert_resp["data"]["first_level_block_ids"],
    "descendants": convert_resp["data"]["blocks"],
    "index": target_index
})
```

### 模式 3：批量编辑表格单元格

```python
# 1. Get all descendants of table
items = get_descendants(table_id)

# 2. Build update map
updates = []
for item in items:
    if needs_update(item):
        updates.append({
            "block_id": item["block_id"],
            "update_text_elements": {
                "elements": [{"text_run": {"content": new_value}}]
            }
        })

# 3. Batch update (max 200 per call)
for i in range(0, len(updates), 200):
    api_call(token, "PATCH", f".../blocks/batch_update",
        {"requests": updates[i:i+200]})
    time.sleep(0.35)
```

### 模式 4：先删除再插入（用于处理特定位置的修改）

当需要在指定位置替换内容时：

```python
# 1. Find the index range to replace
children = get_doc_children(doc)
start_idx = children.index(first_block_to_replace)
end_idx = children.index(last_block_to_replace) + 1

# 2. Delete old blocks
api_call(token, "DELETE", f".../children/batch_delete",
    {"start_index": start_idx, "end_index": end_idx})

# 3. Insert new content at same position
api_call(token, "POST", f".../blocks/{doc}/descendant", {
    "children_id": new_ids,
    "descendants": new_blocks,
    "index": start_idx
})
```

## 注意事项与经验总结

1. **`index` 参数必须在请求体中指定，不能作为 URL 查询参数** —— `?index=N` 会被忽略。
2. **`batch_delete` 操作使用索引范围** —— 例如 `{"start_index": 0, "end_index": 5}` 会删除从索引 0 到索引 4 的所有子块。**不要** 提供 `block_ids` 参数。
3. **表格的 `merge_info` 属性是只读的** —— 在插入前必须将其从块数据中删除，否则会导致错误。
4. **`children_id` 仅包含一级子块的 ID** —— 如果包含孙子块的 ID 会导致错误 1770006。
5. **速率限制是针对每个文档的** —— 对同一文档的多次并发编辑操作共享每秒 3 次的请求限制。
6. **使用 `with_descendants=true` 可以减少请求次数** —— 读取表格内容时只需一次请求，而不是多次请求。
7. **API 返回的临时 ID 与实际使用的 ID 不同** —— 插入后，块的 ID 会与请求时使用的临时 ID 不一致。