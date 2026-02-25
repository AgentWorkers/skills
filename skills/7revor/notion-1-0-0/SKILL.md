---
name: notion
description: Notion API 用于创建和管理页面、数据库以及各种内容块（blocks）。
homepage: https://developers.notion.com
metadata: {"clawdbot":{"emoji":"📝"}}
---

# Notion API

使用 Notion API 可以创建/读取/更新页面、数据源（数据库）以及页面中的区块。

## 设置

1. 在 https://notion.so/my-integrations 创建一个集成。
2. 复制 API 密钥（以 `ntn_` 或 `secret_` 开头）。
3. 将密钥存储起来：
```bash
mkdir -p ~/.config/notion
echo "ntn_your_key_here" > ~/.config/notion/api_key
```
4. 将目标页面/数据库共享给你的集成（点击 “...” → “连接到” → 你的集成名称）。

## API 基础知识

所有请求都需要：
```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
curl -X GET "https://api.notion.com/v1/..." \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json"
```

> **注意：** 必须包含 `Notion-Version` 标头。本技能使用的是 `2025-09-03` 版本。在该版本中，API 中将数据库称为 “data sources”（数据源）。

## 常见操作

**搜索页面和数据源：**
```bash
curl -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "page title"}'
```

**获取页面：**
```bash
curl "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03"
```

**获取页面内容（区块）：**
```bash
curl "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03"
```

**在数据源中创建页面：**
```bash
curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "xxx"},
    "properties": {
      "Name": {"title": [{"text": {"content": "New Item"}}]},
      "Status": {"select": {"name": "Todo"}}
    }
  }'
```

**查询数据源（数据库）：**
```bash
curl -X POST "https://api.notion.com/v1/data_sources/{data_source_id}/query" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"property": "Status", "select": {"equals": "Active"}},
    "sorts": [{"property": "Date", "direction": "descending"}]
  }'
```

**创建数据源（数据库）：**
```bash
curl -X POST "https://api.notion.com/v1/data_sources" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"page_id": "xxx"},
    "title": [{"text": {"content": "My Database"}}],
    "properties": {
      "Name": {"title": {}},
      "Status": {"select": {"options": [{"name": "Todo"}, {"name": "Done"}]}},
      "Date": {"date": {}}
    }
  }'
```

**更新页面属性：**
```bash
curl -X PATCH "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"Status": {"select": {"name": "Done"}}}}'
```

**向页面添加区块：**
```bash
curl -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Hello"}}]}}
    ]
  }'
```

## 属性类型

数据源项的常见属性格式：
- **标题：** `{"title": [{"text": {"content": "..."}}]}`
- **富文本：** `{"rich_text": [{"text": {"content": "..."}}]}`
- **单选：** `{"select": {"name": "选项"}}`
- **多选：** `{"multi_select": [{"name": "A"}, {"name": "B"}]}`
- **日期：** `{"date": {"start": "2024-01-15", "end": "2024-01-16"}}`
- **复选框：** `{"checkbox": true}`
- **数字：** `{"number": 42}`
- **URL：** `{"url": "https://..."}`
- **电子邮件：** `{"email": "a@b.com"}`
- **关联：** `{"relation": [{"id": "page_id"}]}`

## 2025-09-03 版本的主要变化

- **数据库 → 数据源：** 使用 `/data_sources/` 端点进行查询和检索。
- **两个 ID：** 每个数据库现在都有 `database_id` 和 `data_source_id`。
  - 创建页面时使用 `database_id`（例如：`parent: {"database_id": "..."}`）。
  - 查询时使用 `data_source_id`（例如：`POST /v1/data_sources/{id}/query`）。
- **搜索结果：** 数据源以 `"object": "data_source"` 的形式返回，并包含其 `data_source_id`。
- **响应中的父级信息：** 页面会显示 `parent.data_source_id` 和 `parent.database_id`。
- **查找 data_source_id：** 可以搜索数据库，或者调用 `GET /v1/data_sources/{data_source_id}`。

## 注意事项

- 页面/数据库的 ID 是 UUID（可能包含或不包含破折号）。
- API 无法设置数据库的显示过滤器——这些设置仅通过用户界面进行。
- 请求速率限制：平均每秒约 3 次请求。
- 在创建数据源时，设置 `is_inline: true` 可以将其嵌入到页面中。