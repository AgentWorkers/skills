---
name: trello
description: |
  Trello API integration with managed OAuth. Manage boards, lists, cards, members, and labels. Use this skill when users want to interact with Trello for project management. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Trello

通过管理的 OAuth 认证来访问 Trello API。您可以管理项目和工作任务中的看板（boards）、列表（lists）、卡片（cards）、待办事项列表（checklists）、标签（labels）以及成员（members）。

## 快速入门

```bash
# Get boards for current user
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/trello/1/members/me/boards')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/trello/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Trello API 端点路径。该网关会将请求代理到 `api.trello.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的 Trello OAuth 连接。

### 查看连接信息

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=trello&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'trello'}).encode()
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
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "trello",
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

如果您有多个 Trello 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/trello/1/members/me/boards')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## API 参考

### 成员（Members）

#### 获取当前成员信息

```bash
GET /trello/1/members/me
```

#### 获取成员的看板信息

```bash
GET /trello/1/members/me/boards
```

查询参数：
- `filter` - 筛选看板：`all`、`open`、`closed`、`members`、`organization`、`starred`
- `fields` - 要包含的字段（用逗号分隔）

### 看板（Boards）

#### 获取看板信息

```bash
GET /trello/1/boards/{id}
```

查询参数：
- `fields` - 要包含的字段（用逗号分隔）
- `lists` - 是否包含列表：`all`、`open`、`closed`、`none`
- `cards` - 是否包含卡片：`all`、`open`、`closed`、`none`
- `members` - 是否包含成员：`all`、`none`

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/trello/1/boards/BOARD_ID?lists=open&cards=open')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建看板

```bash
POST /trello/1/boards
Content-Type: application/json

{
  "name": "Project Alpha",
  "desc": "Main project board",
  "defaultLists": false,
  "prefs_permissionLevel": "private"
}
```

#### 更新看板信息

```bash
PUT /trello/1/boards/{id}
Content-Type: application/json

{
  "name": "Project Alpha - Updated",
  "desc": "Updated description"
}
```

#### 删除看板

```bash
DELETE /trello/1/boards/{id}
```

#### 获取看板的列表信息

```bash
GET /trello/1/boards/{id}/lists
```

查询参数：
- `filter` - 筛选：`all`、`open`、`closed`、`none`

#### 获取看板中的卡片信息

```bash
GET /trello/1/boards/{id}/cards
```

#### 获取看板的成员信息

```bash
GET /trello/1/boards/{id}/members
```

### 列表（Lists）

#### 获取列表信息

```bash
GET /trello/1/lists/{id}
```

#### 创建列表

```bash
POST /trello/1/lists
Content-Type: application/json

{
  "name": "To Do",
  "idBoard": "BOARD_ID",
  "pos": "top"
}
```

#### 更新列表信息

```bash
PUT /trello/1/lists/{id}
Content-Type: application/json

{
  "name": "In Progress"
}
```

#### 将列表归档

```bash
PUT /trello/1/lists/{id}/closed
Content-Type: application/json

{
  "value": true
}
```

#### 获取列表中的卡片信息

```bash
GET /trello/1/lists/{id}/cards
```

#### 将列表中的所有卡片移动到其他位置

```bash
POST /trello/1/lists/{id}/moveAllCards
Content-Type: application/json

{
  "idBoard": "BOARD_ID",
  "idList": "TARGET_LIST_ID"
}
```

### 卡片（Cards）

#### 获取卡片信息

```bash
GET /trello/1/cards/{id}
```

查询参数：
- `fields` - 要包含的字段（用逗号分隔）
- `members` - 是否包含成员（true/false）
- `checklists` - 是否包含待办事项列表：`all`、`none`
- `attachments` - 是否包含附件：`true/false`

#### 创建卡片

```bash
POST /trello/1/cards
Content-Type: application/json

{
  "name": "Implement feature X",
  "desc": "Description of the task",
  "idList": "LIST_ID",
  "pos": "bottom",
  "due": "2025-03-30T12:00:00.000Z",
  "idMembers": ["MEMBER_ID"],
  "idLabels": ["LABEL_ID"]
}
```

#### 更新卡片信息

```bash
PUT /trello/1/cards/{id}
Content-Type: application/json

{
  "name": "Updated card name",
  "desc": "Updated description",
  "due": "2025-04-15T12:00:00.000Z",
  "dueComplete": false
}
```

#### 将卡片移动到其他列表

```bash
PUT /trello/1/cards/{id}
Content-Type: application/json

{
  "idList": "NEW_LIST_ID",
  "pos": "top"
}
```

#### 删除卡片

```bash
DELETE /trello/1/cards/{id}
```

#### 为卡片添加评论

```bash
POST /trello/1/cards/{id}/actions/comments
Content-Type: application/json

{
  "text": "This is a comment"
}
```

#### 为卡片添加成员

```bash
POST /trello/1/cards/{id}/idMembers
Content-Type: application/json

{
  "value": "MEMBER_ID"
}
```

#### 从卡片中移除成员

```bash
DELETE /trello/1/cards/{id}/idMembers/{idMember}
```

#### 为卡片添加标签

```bash
POST /trello/1/cards/{id}/idLabels
Content-Type: application/json

{
  "value": "LABEL_ID"
}
```

### 待办事项列表（Checklists）

#### 获取待办事项列表信息

```bash
GET /trello/1/checklists/{id}
```

#### 创建待办事项列表

```bash
POST /trello/1/checklists
Content-Type: application/json

{
  "idCard": "CARD_ID",
  "name": "Task Checklist"
}
```

#### 创建待办事项列表项

```bash
POST /trello/1/checklists/{id}/checkItems
Content-Type: application/json

{
  "name": "Subtask 1",
  "pos": "bottom",
  "checked": false
}
```

#### 更新待办事项列表项

```bash
PUT /trello/1/cards/{cardId}/checkItem/{checkItemId}
Content-Type: application/json

{
  "state": "complete"
}
```

#### 删除待办事项列表

```bash
DELETE /trello/1/checklists/{id}
```

### 标签（Labels）

#### 获取看板的标签信息

```bash
GET /trello/1/boards/{id}/labels
```

#### 创建标签

```bash
POST /trello/1/labels
Content-Type: application/json

{
  "name": "High Priority",
  "color": "red",
  "idBoard": "BOARD_ID"
}
```

可用颜色：`yellow`、`purple`、`blue`、`red`、`green`、`orange`、`black`、`sky`、`pink`、`lime`、`null`（无颜色）

#### 更新标签信息

```bash
PUT /trello/1/labels/{id}
Content-Type: application/json

{
  "name": "Critical",
  "color": "red"
}
```

#### 删除标签

```bash
DELETE /trello/1/labels/{id}
```

### 搜索

#### 全部搜索

```bash
GET /trello/1/search?query=keyword&modelTypes=cards,boards
```

查询参数：
- `query` - 搜索查询（必填）
- `modelTypes` - 用逗号分隔的搜索类型：`actions`、`boards`、`cards`、`members`、`organizations`
- `board_fields` - 要返回的看板字段
- `card_fields` - 要返回的卡片字段
- `cards_limit` - 返回的最大卡片数量（1-1000）

## 代码示例

### JavaScript

```javascript
const headers = {
  'Authorization': `Bearer ${process.env.MATON_API_KEY}`
};

// Get boards
const boards = await fetch(
  'https://gateway.maton.ai/trello/1/members/me/boards',
  { headers }
).then(r => r.json());

// Create card
await fetch(
  'https://gateway.maton.ai/trello/1/cards',
  {
    method: 'POST',
    headers: { ...headers, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: 'New Task',
      idList: 'LIST_ID',
      desc: 'Task description'
    })
  }
);
```

### Python

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}

# Get boards
boards = requests.get(
    'https://gateway.maton.ai/trello/1/members/me/boards',
    headers=headers
).json()

# Create card
response = requests.post(
    'https://gateway.maton.ai/trello/1/cards',
    headers=headers,
    json={
        'name': 'New Task',
        'idList': 'LIST_ID',
        'desc': 'Task description'
    }
)
```

## 注意事项

- ID 是由 24 个字母和数字组成的字符串。
- 使用 `me` 来引用已认证的用户。
- 日期采用 ISO 8601 格式。
- `pos` 可以是 `top`、`bottom` 或一个正数，表示卡片在列表中的位置。
- 使用 `fields` 参数可以限制返回的数据量并提高性能。
- 可以通过 `filter=closed` 来检索已归档的卡片。
- 重要提示：当 URL 包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 可以避免全局解析问题。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确解析，可能会导致“无效 API 密钥”错误。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 未找到 Trello 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 未找到看板、列表或卡片 |
| 429 | 每个账户的请求速率限制（10 次/秒） |
| 4xx/5xx | 来自 Trello API 的传递错误 |

### 故障排除：API 密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接信息来验证 API 密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称无效

1. 确保您的 URL 路径以 `trello` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/trello/1/members/me/boards`
- 错误的路径：`https://gateway.maton.ai/1/members/me/boards`

## 资源

- [Trello API 概述](https://developer.atlassian.com/cloud/trello/rest/api-group-actions/)
- [看板](https://developer.atlassian.com/cloud/trello/rest/api-group-boards/)
- [列表](https://developer.atlassian.com/cloud/trello/rest/api-group-lists/)
- [卡片](https://developer.atlassian.com/cloud/trello/rest/api-group-cards/)
- [待办事项列表](https://developer.atlassian.com/cloud/trello/rest/api-group-checklists/)
- [标签](https://developer.atlassian.com/cloud/trello/rest/api-group-labels/)
- [成员](https://developer.atlassian.com/cloud/trello/rest/api-group-members/)
- [搜索](https://developer.atlassian.com/cloud/trello/rest/api-group-search/)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)