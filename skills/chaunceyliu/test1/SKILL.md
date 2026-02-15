---
name: trello
description: 通过 Trello REST API 管理 Trello 的看板、列表和卡片。
homepage: https://developer.atlassian.com/cloud/trello/rest/
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":["jq"],"env":["TRELLO_API_KEY","TRELLO_TOKEN"]}}}
---

# Trello 技能

可以直接通过 Clawdbot 管理 Trello 的看板、列表和卡片。

## 设置

1. 获取您的 API 密钥：https://trello.com/app-key
2. 生成一个令牌（点击该页面上的 “Token” 链接）
3. 设置环境变量：
   ```bash
   export TRELLO_API_KEY="your-api-key"
   export TRELLO_TOKEN="your-token"
   ```

## 使用方法

所有命令都使用 `curl` 来调用 Trello 的 REST API。

### 列出所有看板
```bash
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
```

### 列出某个看板中的所有列表
```bash
curl -s "https://api.trello.com/1/boards/{boardId}/lists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
```

### 列出某个列表中的所有卡片
```bash
curl -s "https://api.trello.com/1/lists/{listId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id, desc}'
```

### 创建一张卡片
```bash
curl -s -X POST "https://api.trello.com/1/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idList={listId}" \
  -d "name=Card Title" \
  -d "desc=Card description"
```

### 将卡片移动到另一个列表
```bash
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idList={newListId}"
```

### 为卡片添加评论
```bash
curl -s -X POST "https://api.trello.com/1/cards/{cardId}/actions/comments?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "text=Your comment here"
```

### 将卡片归档
```bash
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "closed=true"
```

## 注意事项

- 看板/列表/卡片的 ID 可以在 Trello 的 URL 中找到，或者通过相应的列表命令获取
- API 密钥和令牌可以完全访问您的 Trello 账户，请务必保密！
- 请求限制：每个 API 密钥每 10 秒内最多 300 次请求；每个令牌每 10 秒内最多 100 次请求；`/1/members` 端点每 900 秒内最多 100 次请求

## 示例

```bash
# Get all boards
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id" | jq

# Find a specific board by name
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | select(.name | contains("Work"))'

# Get all cards on a board
curl -s "https://api.trello.com/1/boards/{boardId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, list: .idList}'
```