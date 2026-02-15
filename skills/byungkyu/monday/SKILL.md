---
name: monday
description: |
  Monday.com API integration with managed OAuth. Manage boards, items, columns, groups, and workspaces using GraphQL.
  Use this skill when users want to create, update, or query Monday.com boards and items, manage tasks, or automate workflows.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Monday.com

您可以使用托管的 OAuth 认证来访问 Monday.com 的 API。通过 GraphQL 可以管理看板（boards）、项目（items）、列（columns）、组（groups）、用户（users）和工作空间（workspaces）。

## 快速入门

```bash
# Get current user
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': '{ me { id name email } }'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/monday/v2', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/monday/v2
```

所有请求都使用 POST 方法发送到 GraphQL 端点。该网关会将请求代理到 `api.monday.com`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取您的 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Monday.com OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=monday&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'monday'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接信息

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection": {
    "connection_id": "ca93f2c5-5126-4360-b293-4f05f7bb6c8c",
    "status": "ACTIVE",
    "creation_time": "2026-02-05T20:10:47.585047Z",
    "last_updated_time": "2026-02-05T20:11:12.357011Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "monday",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成 OAuth 认证。

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您有多个 Monday.com 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': '{ me { id name } }'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/monday/v2', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', 'ca93f2c5-5126-4360-b293-4f05f7bb6c8c')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头部，网关将使用默认的（最旧的）活动连接。

## API 参考

Monday.com 使用 GraphQL API。所有操作都以 POST 请求的形式发送，请求体中包含 `query` 字段。

### 当前用户（me）

```bash
POST /monday/v2
Content-Type: application/json

{"query": "{ me { id name email } }"}
```

**响应：**
```json
{
  "data": {
    "me": {
      "id": "72989582",
      "name": "Chris",
      "email": "chris.kim.2332@gmail.com"
    }
  }
}
```

### 用户

```bash
POST /monday/v2
Content-Type: application/json

{"query": "{ users(limit: 20) { id name email } }"}
```

### 工作空间

```bash
POST /monday/v2
Content-Type: application/json

{"query": "{ workspaces(limit: 10) { id name kind } }"}
```

**响应：**
```json
{
  "data": {
    "workspaces": [
      { "id": "10136488", "name": "Main workspace", "kind": "open" }
    ]
  }
}
```

### 看板

#### 列出看板

```bash
POST /monday/v2
Content-Type: application/json

{"query": "{ boards(limit: 10) { id name state board_kind workspace { id name } } }"}
```

**响应：**
```json
{
  "data": {
    "boards": [
      {
        "id": "8614733398",
        "name": "Welcome to your developer account",
        "state": "active",
        "board_kind": "public",
        "workspace": { "id": "10136488", "name": "Main workspace" }
      }
    ]
  }
}
```

#### 获取包含列、组和项目的看板信息

```bash
POST /monday/v2
Content-Type: application/json

{"query": "{ boards(ids: [BOARD_ID]) { id name columns { id title type } groups { id title } items_page(limit: 20) { cursor items { id name state } } } }"}
```

#### 创建看板

```bash
POST /monday/v2
Content-Type: application/json

{"query": "mutation { create_board(board_name: \"New Board\", board_kind: public) { id name } }"}
```

**响应：**
```json
{
  "data": {
    "create_board": {
      "id": "18398921201",
      "name": "New Board"
    }
  }
}
```

#### 更新看板

```bash
POST /monday/v2
Content-Type: application/json

{"query": "mutation { update_board(board_id: BOARD_ID, board_attribute: description, new_value: \"Board description\") }"}
```

#### 删除看板

```bash
POST /monday/v2
Content-Type: application/json

{"query": "mutation { delete_board(board_id: BOARD_ID) { id } }"}
```

### 项目

#### 根据 ID 获取项目信息

```bash
POST /monday/v2
Content-Type: application/json

{"query": "{ items(ids: [ITEM_ID]) { id name created_at updated_at state board { id name } group { id title } column_values { id text value } } }"}
```

**响应：**
```json
{
  "data": {
    "items": [
      {
        "id": "11200791874",
        "name": "Test item",
        "created_at": "2026-02-05T20:12:42Z",
        "updated_at": "2026-02-05T20:12:42Z",
        "state": "active",
        "board": { "id": "8614733398", "name": "Welcome to your developer account" },
        "group": { "id": "topics", "title": "Group Title" }
      }
    ]
  }
}
```

#### 创建项目

```bash
POST /monday/v2
Content-Type: application/json

{"query": "mutation { create_item(board_id: BOARD_ID, group_id: \"GROUP_ID\", item_name: \"New item\") { id name } }"}
```

#### 创建包含列值的项目

```bash
POST /monday/v2
Content-Type: application/json

{"query": "mutation { create_item(board_id: BOARD_ID, group_id: \"GROUP_ID\", item_name: \"New task\", column_values: \"{\\\"status\\\": {\\\"label\\\": \\\"Working on it\\\"}}\") { id name column_values { id text } } }"}
```

#### 更新项目名称

```bash
POST /monday/v2
Content-Type: application/json

{"query": "mutation { change_simple_column_value(board_id: BOARD_ID, item_id: ITEM_ID, column_id: \"name\", value: \"Updated name\") { id name } }"}
```

#### 更新列值

```bash
POST /monday/v2
Content-Type: application/json

{"query": "mutation { change_column_value(board_id: BOARD_ID, item_id: ITEM_ID, column_id: \"status\", value: \"{\\\"label\\\": \\\"Done\\\"}\") { id name } }"}
```

#### 删除项目

```bash
POST /monday/v2
Content-Type: application/json

{"query": "mutation { delete_item(item_id: ITEM_ID) { id } }"}
```

### 列

#### 创建列

```bash
POST /monday/v2
Content-Type: application/json

{"query": "mutation { create_column(board_id: BOARD_ID, title: \"Status\", column_type: status) { id title type } }"}
```

**响应：**
```json
{
  "data": {
    "create_column": {
      "id": "color_mm09e48w",
      "title": "Status",
      "type": "status"
    }
  }
}
```

**列类型**

常见的列类型：`status`、`text`、`numbers`、`date`、`people`、`dropdown`、`checkbox`、`email`、`phone`、`link`、`timeline`、`tags`、`rating`

### 组

#### 创建组

```bash
POST /monday/v2
Content-Type: application/json

{"query": "mutation { create_group(board_id: BOARD_ID, group_name: \"New Group\") { id title } }"}
```

**响应：**
```json
{
  "data": {
    "create_group": {
      "id": "group_mm0939df",
      "title": "New Group"
    }
  }
}
```

## 分页

Monday.com 对项目使用基于游标的分页机制，通过 `items_page` 和 `next_items_page` 参数实现分页。

```bash
# First page
POST /monday/v2
{"query": "{ boards(ids: [BOARD_ID]) { items_page(limit: 50) { cursor items { id name } } } }"}

# Next page using cursor
POST /monday/v2
{"query": "{ next_items_page(cursor: \"CURSOR_VALUE\", limit: 50) { cursor items { id name } } }"}
```

当还有更多项目时，响应中会包含 `cursor`（如果没有更多页面，则 `cursor` 为 `null`）：

```json
{
  "data": {
    "boards": [{
      "items_page": {
        "cursor": "MSw5NzI4...",
        "items": [...]
      }
    }]
  }
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch('https://gateway.maton.ai/monday/v2', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: `{ boards(limit: 10) { id name items_page(limit: 20) { items { id name } } } }`
  })
});
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/monday/v2',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'query': '{ boards(limit: 10) { id name items_page(limit: 20) { items { id name } } } }'
    }
)
data = response.json()
```

## 注意事项

- Monday.com 仅支持 GraphQL，不支持 REST API。
- 看板 ID、项目 ID 和用户 ID 都是数字字符串。
- 列 ID 是字母数字字符串（例如：`color_mm09e48w`）。
- 组 ID 也是字母数字字符串（例如：`group_mm0939df`、`topics`）。
- 在创建或更新项目时，列值必须以 JSON 字符串的形式传递。
- `account` 查询可能需要额外的 OAuth 权限范围。如果您收到权限范围错误，请通过 support@maton.ai 联系 Maton 支持团队，并提供具体的操作、API 和使用场景。
- 看板类型：`public`、`private`、`share`。
- 看板状态：`active`、`archived`、`deleted`、`all`。
- 每个游标在初始请求后的 60 分钟内有效。
- 大多数查询的默认限制为 25 个结果，最大限制为 100 个结果。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 未建立 Monday.com 连接或 GraphQL 验证错误 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 操作所需的 OAuth 权限范围不足 |
| 429 | 请求次数达到限制 |
| 4xx/5xx | 来自 Monday.com API 的传递错误 |

GraphQL 错误会通过 `errors` 数组返回：

```json
{
  "data": {},
  "errors": [
    {
      "message": "Unauthorized field or type",
      "path": ["account"],
      "extensions": { "code": "UNAUTHORIZED_FIELD_OR_TYPE" }
    }
  ]
}
```

### 故障排除：API 密钥问题

1. 确保 `MATON_API_KEY` 环境变量已设置：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证 API 密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称无效

1. 确保您的 URL 路径以 `monday` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/monday/v2`
- 错误的路径：`https://gateway.maton.ai/v2`

## 资源

- [Monday.com API 基础知识](https://developer.monday.com/api-reference/docs/basics)
- [GraphQL 概述](https://developer.monday.com/api-reference/docs/introduction-to-graphql)
- [看板参考](https://developer.monday.com/api-reference/reference/boards)
- [项目参考](https://developer.monday.com/api-reference/reference/items)
- [列参考](https://developer.monday.com/api-reference/reference/columns)
- [API 更新日志](https://developer.monday.com/api-reference/changelog)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)