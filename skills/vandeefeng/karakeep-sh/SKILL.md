---
name: karakeep
description: Karakeep书签管理器支持完整的原生RESTful API，包括添加书签、更新书签以及删除书签的功能。
---
# Karakeep 技能

提供高级的 Karakeep 书签管理功能，并全面支持 REST API。

请将 `KARAKEEP_SERVER_URL` 和 `KARAKEEP_API_KEY` 设置为环境变量，并使用 `jq` 来美化 JSON 响应的输出。

如果这些变量缺失，请为用户提供明确的指导。

**重要提示：** 在删除书签之前，务必先获得用户的确认。

## 完整的函数参考

使用以下脚本 [karakeep-script.sh](scripts/karakeep-script.sh)：

我们提供了以下函数：

| 函数 | 描述 |
|----------|-------------|
| `kb-create` | 创建书签（支持添加笔记） |
| `kb-update-note` | 更新书签笔记 |
| `kb-delete` | 删除书签 |
| `kb-get` | 获取书签详情 |
| `kb-list` | 列出所有书签（可设置限制） |
| `kb-content` | 获取书签的 Markdown 内容 |
| `kb-search` | 根据条件进行搜索 |
| `kb-lists` | 列出所有列表 |
| `kb-create-list` | 创建新列表 |
| `kb-add-to-list` | 将书签添加到列表中 |
| `kb-remove-from-list` | 从列表中删除书签 |
| `kb-attach-tags` | 为书签添加标签 |
| `kb-detach-tags` | 从书签中删除标签 |

## 可用的操作

### 创建带有笔记的书签

```bash
# Link bookmark with note
kb-create link "https://example.com" "Example Site" "My analysis and notes here..."

# Text bookmark with note
kb-create text "Text content here" "My Note" "Additional notes..."
```

### 更新书签笔记

```bash
kb-update-note "bookmark_id" "Updated note content..."
```

### 删除书签

```bash
kb-delete "bookmark_id"
```

### 获取书签信息

```bash
kb-get "bookmark_id"
```

### 搜索操作

```bash
# Search with qualifiers (uses MeiliSearch backend)
kb-search "is:fav after:2023-01-01 #important"
kb-search "machine learning is:tagged"
kb-search "list:reading #work"

# Search with custom limit and sort order
kb-search "python" 50 "desc"  # 50 results, descending order

# Available qualifiers:
# - is:fav, is:archived, is:tagged, is:inlist
# - is:link, is:text, is:media
# - url:<value>, #<tag>, list:<name>
# - after:<YYYY-MM-DD>, before:<YYYY-MM-DD>

# Sort options: relevance (default), asc, desc
```

**API 参数：**
- `q`（必填）：包含搜索条件的查询字符串 |
- `limit`（可选）：每页显示的结果数量（默认由服务器控制） |
- `sortOrder`（可选）：`asc` | `desc` | `relevance`（默认值） |
- `cursor`（可选）：分页游标 |
- `includeContent`（可选）：是否包含完整内容（默认值为 `true`）

### 列表管理

```bash
# List all lists
kb-lists

# Create new list
kb-create-list "Reading List" "📚"

# Add bookmark to list
kb-add-to-list "bookmark_id" "list_id"

# Remove bookmark from list
kb-remove-from-list "bookmark_id" "list_id"
```

### 标签管理

```bash
# Attach tags
kb-attach-tags "bookmark_id" "important" "todo" "work"

# Detach tags
kb-detach-tags "bookmark_id" "oldtag" "anotherold"
```

**注意事项：**
- 所有响应均以 JSON 格式返回 |
- 创建书签时，会返回书签的 ID |
- 使用 `jq` 来美化 JSON 响应的输出 |
- 可能会应用 API 的速率限制。