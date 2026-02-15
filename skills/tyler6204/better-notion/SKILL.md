---
name: better-notion
description: Notion页面、数据库和区块支持完整的CRUD（创建、读取、更新、删除）操作。用户可以执行创建、读取、更新、删除、搜索和查询等操作。
metadata: {"clawdbot":{"emoji":"📝"}}
---

# Notion

您可以使用 Notion API 来创建页面、数据源（数据库）以及各种内容块。

## 设置

```bash
mkdir -p ~/.config/notion
echo "ntn_your_key_here" > ~/.config/notion/api_key
```

在 Notion 用户界面中，将目标页面或数据库共享给您的集成系统。

## API 基础知识

```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
curl -X POST "https://api.notion.com/v1/..." \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json"
```

## 常见操作

```bash
# Search
curl -X POST "https://api.notion.com/v1/search" -d '{"query": "title"}'

# Get page
curl "https://api.notion.com/v1/pages/{page_id}"

# Get page blocks
curl "https://api.notion.com/v1/blocks/{page_id}/children"

# Create page in database
curl -X POST "https://api.notion.com/v1/pages" -d '{
  "parent": {"data_source_id": "xxx"},
  "properties": {"Name": {"title": [{"text": {"content": "Item"}}]}}
}'

# Query database
curl -X POST "https://api.notion.com/v1/data_sources/{id}/query" -d '{
  "filter": {"property": "Status", "select": {"equals": "Active"}}
}'

# Update page
curl -X PATCH "https://api.notion.com/v1/pages/{page_id}" -d '{
  "properties": {"Status": {"select": {"name": "Done"}}}
}'

# Add blocks
curl -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children" -d '{
  "children": [{"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Text"}}]}}]
}'

# Delete page or block (moves to trash)
curl -X DELETE "https://api.notion.com/v1/blocks/{block_id}"

# Restore from trash (set archived to false)
curl -X PATCH "https://api.notion.com/v1/blocks/{block_id}" -d '{"archived": false}'
```

## 属性类型

| 类型 | 格式 |
|------|--------|
| 标题 | `{"title": [{"text": {"content": "..."}}]}` |
| 文本 | `{"rich_text": [{"text": {"content": "..."}}]}` |
| 单选 | `{"select": {"name": "选项"}}` |
| 多选 | `{"multi_select": [{"name": "选项A"}]}` |
| 日期 | `{"date": {"start": "2024-01-15"}}` |
| 复选框 | `{"checkbox": true}` |
| 数字 | `{"number": 42}` |
| URL | `{"url": "https://..."}` |

## 2025-09-03 的 API 更新说明

- 在 API 中，`Databases` 现在被称为“数据源”（data sources）。
- 创建页面或查询数据源时，都需要使用 `data_source_id`。
- 可以从搜索结果中获取 `data_source_id`（该字段名为 `id`）。
- API 的请求速率限制为：约 3 次请求/秒。