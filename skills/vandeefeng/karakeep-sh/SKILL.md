---
name: karakeep
description: Karakeep 是一个书签管理工具，支持完整的 API 功能，包括添加书签、更新书签以及删除书签。使用该工具需要设置 `KARAKEEP_SERVER_URL` 和 `KARAKEEP_API_KEY` 两个环境变量。
---

# Karakeep Skill

这是一个高级的Karakeep书签管理工具，支持完整的REST API接口。

## 完整功能参考

请使用以下脚本 [karakeep-script.sh](scripts/karakeep-script.sh) 进行操作：

我们提供了以下功能：

| 功能 | 描述 |
|----------|-------------|
| `kb-create` | 创建书签（支持添加笔记） |
| `kb-update-note` | 更新书签中的笔记内容 |
| `kb-delete` | 删除书签 |
| `kb-get` | 获取书签详情 |
| `kb-list` | 列出所有书签（可设置限制） |
| `kb-content` | 获取书签的Markdown内容 |
| `kb-search` | 根据指定条件搜索书签 |
| `kb-lists` | 列出所有列表 |
| `kb-create-list` | 创建新列表 |
| `kb-add-to-list` | 将书签添加到列表中 |
| `kb-remove-from-list` | 从列表中删除书签 |
| `kb-attach-tags` | 为书签添加标签 |
| `kb-detach-tags` | 从书签中删除标签 |

## 可用的操作

### 创建带笔记的书签

```bash
# Link bookmark with note
kb-create link "https://example.com" "Example Site" "My analysis and notes here..."

# Text bookmark with note
kb-create text "Text content here" "My Note" "Additional notes..."
```

### 更新书签中的笔记内容

```bash
kb-update-note "bookmark_id" "Updated note content..."
```

### 删除书签

```bash
kb-delete "bookmark_id"
```

### 获取书签详情

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

**API参数：**
- `q` (必填)：包含搜索条件的查询字符串 |
- `limit` (可选)：每页显示的结果数量（默认由服务器控制） |
- `sortOrder` (可选)：排序方式（`asc` | `desc` | `relevance`，默认为`relevance`） |
- `cursor` (可选)：分页游标 |
- `includeContent` (可选)：是否包含书签的完整内容（默认为`true`）

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

## 注意事项：
- 所有响应均以JSON格式返回 |
- 创建书签时，会返回书签的ID |
- 可使用`jq`工具来美化JSON响应的显示效果 |
- API可能受到使用频率的限制（即存在速率限制）。