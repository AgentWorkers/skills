---
name: monday
description: 通过 GraphQL API 管理 monday.com 的看板、项目和工作流程。创建任务、更新状态，并实现工作的自动化。
metadata: {"clawdbot":{"emoji":"📋","requires":{"env":["MONDAY_API_TOKEN"]}}}
---

# Monday.com

这是一个工作管理平台。

## 环境配置

```bash
export MONDAY_API_TOKEN="xxxxxxxxxx"
```

## 列表板管理

```bash
curl "https://api.monday.com/v2" \
  -H "Authorization: $MONDAY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ boards(limit:10) { id name } }"}'
```

## 获取列表板项目

```bash
curl "https://api.monday.com/v2" \
  -H "Authorization: $MONDAY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ boards(ids: [BOARD_ID]) { items_page { items { id name column_values { id text } } } } }"}'
```

## 创建项目

```bash
curl "https://api.monday.com/v2" \
  -H "Authorization: $MONDAY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { create_item(board_id: BOARD_ID, item_name: \"New Task\") { id } }"}'
```

## 更新项目信息

```bash
curl "https://api.monday.com/v2" \
  -H "Authorization: $MONDAY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { change_column_value(board_id: BOARD_ID, item_id: ITEM_ID, column_id: \"status\", value: \"{\\\"label\\\":\\\"Done\\\"}\") { id } }"}'
```

## 添加/更新项目备注（评论）

```bash
curl "https://api.monday.com/v2" \
  -H "Authorization: $MONDAY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { create_update(item_id: ITEM_ID, body: \"Task completed!\") { id } }"}'
```

## 获取用户信息

```bash
curl "https://api.monday.com/v2" \
  -H "Authorization: $MONDAY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ me { id name email } }"}'
```

## 链接：
- 仪表盘：https://monday.com
- 文档：https://developer.monday.com/api-reference