---
name: linear
description: |
  Linear API integration with managed OAuth. Query and manage issues, projects, teams, cycles, and labels using GraphQL.
  Use this skill when users want to create, update, or query Linear issues, search for tasks, manage projects, or track work.
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

# Linear

您可以使用受管理的 OAuth 认证来访问 Linear API。通过 GraphQL 查询和管理问题（Issues）、项目（Projects）、团队（Teams）、周期（Cycles）、标签（Labels）以及评论（Comments）。

## 快速入门

```bash
# Get current user
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': '{ viewer { id name email } }'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/linear/graphql', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/linear/graphql
```

所有请求都使用 POST 方法发送到 GraphQL 端点。网关会将请求代理到 `api.linear.app`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头部包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Linear OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=linear&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'linear'}).encode()
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
    "connection_id": "fda4dabb-9d62-47e3-9503-a2f29d0995df",
    "status": "ACTIVE",
    "creation_time": "2026-02-04T23:03:22.676001Z",
    "last_updated_time": "2026-02-04T23:03:51.239577Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "linear",
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

如果您有多个 Linear 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': '{ viewer { id name } }'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/linear/graphql', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', 'fda4dabb-9d62-47e3-9503-a2f29d0995df')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头部，网关将使用默认的（最旧的）活动连接。

## API 参考

Linear 使用 GraphQL API。所有操作都以 POST 请求的形式发送，请求体中包含 `query` 字段。

### 查看器（当前用户）

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ viewer { id name email } }"}
```

**响应：**
```json
{
  "data": {
    "viewer": {
      "id": "4933b394-c42f-4623-904f-355fc40a4858",
      "name": "Byungkyu Park",
      "email": "byungkyujpark@gmail.com"
    }
  }
}
```

### 组织（Organization）

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ organization { id name urlKey } }"}
```

### 团队（Teams）

#### 列出团队

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ teams { nodes { id name key } } }"}
```

**响应：**
```json
{
  "data": {
    "teams": {
      "nodes": [
        {
          "id": "70c49a0d-6973-4563-a743-8504f1a5171b",
          "name": "Maton",
          "key": "MTN"
        }
      ]
    }
  }
}
```

#### 获取团队信息

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ team(id: \"TEAM_ID\") { id name key issues { nodes { id identifier title } } } }"}
```

### 问题（Issues）

#### 列出问题

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ issues(first: 10) { nodes { id identifier title state { name } priority createdAt } pageInfo { hasNextPage endCursor } } }"}
```

**响应：**
```json
{
  "data": {
    "issues": {
      "nodes": [
        {
          "id": "565e2ee9-2552-48d8-bbf9-a8b79ca1baec",
          "identifier": "MTN-527",
          "title": "Shopify app verification",
          "state": { "name": "In Progress" },
          "priority": 0,
          "createdAt": "2026-02-03T07:49:31.675Z"
        }
      ],
      "pageInfo": {
        "hasNextPage": true,
        "endCursor": "4c7b33c8-dabf-47ce-9d30-7f286f9463be"
      }
    }
  }
}
```

#### 通过 ID 或标识符获取问题

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ issue(id: \"MTN-527\") { id identifier title description state { name } priority assignee { name } team { key name } createdAt updatedAt } }"}
```

#### 过滤问题

- 按状态类型过滤：
```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ issues(first: 10, filter: { state: { type: { eq: \"started\" } } }) { nodes { id identifier title state { name type } } } }"}
```

- 按标题过滤：
```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ issues(first: 10, filter: { title: { containsIgnoreCase: \"bug\" } }) { nodes { id identifier title } } }"}
```

#### 搜索问题

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ searchIssues(first: 10, term: \"shopify\") { nodes { id identifier title } } }"}
```

#### 创建问题

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "mutation { issueCreate(input: { teamId: \"TEAM_ID\", title: \"New issue title\", description: \"Issue description\" }) { success issue { id identifier title state { name } } } }"}
```

**响应：**
```json
{
  "data": {
    "issueCreate": {
      "success": true,
      "issue": {
        "id": "9dff693f-27d2-4656-9b2d-baa4a828dc83",
        "identifier": "MTN-528",
        "title": "New issue title",
        "state": { "name": "Backlog" }
      }
    }
  }
}
```

#### 更新问题

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "mutation { issueUpdate(id: \"ISSUE_ID\", input: { title: \"Updated title\", priority: 2 }) { success issue { id identifier title priority } } }"}
```

### 项目（Projects）

#### 列出项目

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ projects(first: 10) { nodes { id name state createdAt } } }"}
```

### 周期（Cycles）

#### 列出周期

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ cycles(first: 10) { nodes { id name number startsAt endsAt } } }"}
```

### 标签（Labels）

#### 列出标签

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ issueLabels(first: 20) { nodes { id name color } } }"}
```

**响应：**
```json
{
  "data": {
    "issueLabels": {
      "nodes": [
        { "id": "510edbdf-9f6e-43a0-80e5-c3b3bd82e26f", "name": "Blocked", "color": "#eb5757" },
        { "id": "cb7a7ef2-d2d3-4da2-ad4e-7cea0f8a72c7", "name": "Feature", "color": "#BB87FC" },
        { "id": "c795d04c-24d2-4d20-b3c1-9f9f1ce7b017", "name": "Improvement", "color": "#4EA7FC" },
        { "id": "40ff69f9-4a93-40a2-b143-f3b94aa594b7", "name": "Bug", "color": "#EB5757" }
      ]
    }
  }
}
```

### 工作流程状态（Workflow States）

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ workflowStates(first: 20) { nodes { id name type team { key } } } }"}
```

**响应：**
```json
{
  "data": {
    "workflowStates": {
      "nodes": [
        { "id": "f21dfa65-7951-4742-a202-00ceb0ff6e9f", "name": "Backlog", "type": "backlog", "team": { "key": "MTN" } },
        { "id": "1ab9475f-eb91-4207-a5a3-1176e38b85be", "name": "Todo", "type": "unstarted", "team": { "key": "MTN" } },
        { "id": "ee724a62-0212-4b53-af67-08297a5ae132", "name": "In Progress", "type": "started", "team": { "key": "MTN" } },
        { "id": "427a9916-3849-4303-b982-f00f1d79c5ee", "name": "Done", "type": "completed", "team": { "key": "MTN" } },
        { "id": "363df32a-f22d-4083-8efb-b3615c019925", "name": "Canceled", "type": "canceled", "team": { "key": "MTN" } }
      ]
    }
  }
}
```

### 用户（Users）

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ users(first: 20) { nodes { id name email active } } }"}
```

### 评论（Comments）

#### 列出评论

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ comments(first: 10) { nodes { id body createdAt issue { identifier } user { name } } } }"}
```

#### 创建评论

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "mutation { commentCreate(input: { issueId: \"ISSUE_ID\", body: \"Comment text here\" }) { success comment { id body } } }"}
```

## 分页

Linear 使用基于游标的分页机制，支持 `first/after` 和 `last/before` 参数。

```bash
# First page
POST /linear/graphql
{"query": "{ issues(first: 10) { nodes { id identifier title } pageInfo { hasNextPage endCursor } } }"}

# Next page using endCursor
POST /linear/graphql
{"query": "{ issues(first: 10, after: \"CURSOR_VALUE\") { nodes { id identifier title } pageInfo { hasNextPage endCursor } } }"}
```

响应中包含 `pageInfo`：

```json
{
  "data": {
    "issues": {
      "nodes": [...],
      "pageInfo": {
        "hasNextPage": true,
        "endCursor": "4c7b33c8-dabf-47ce-9d30-7f286f9463be"
      }
    }
  }
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch('https://gateway.maton.ai/linear/graphql', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: `{ issues(first: 10) { nodes { id identifier title state { name } } } }`
  })
});
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/linear/graphql',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'query': '{ issues(first: 10) { nodes { id identifier title state { name } } } }'
    }
)
data = response.json()
```

## 注意事项

- Linear 仅使用 GraphQL（不提供 REST API）。
- 可以使用问题标识符（如 `MTN-527`）代替 UUID 作为 `id` 参数。
- 优先级值：0 = 无优先级，1 = 紧急，2 = 高，3 = 中等，4 = 低。
- 工作流程状态类型：`backlog`、`unstarted`、`started`、`completed`、`canceled`。
- GraphQL 架构可以在 `https://api.linear.appgraphql` 上查看。
- 使用 `searchIssues(term: "...")` 进行全文搜索问题。
- 某些操作（如删除、创建标签/项目）可能需要额外的 OAuth 权限范围。如果您收到权限范围错误，请通过 support@maton.ai 联系 Maton 支持团队，提供具体的操作/API 和您的使用场景。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 缺少 Linear 连接或 GraphQL 验证错误 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 操作所需的 OAuth 权限范围不足 |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自 Linear API 的传递错误 |

GraphQL 错误会包含在 `errors` 数组中：

```json
{
  "errors": [
    {
      "message": "Invalid scope: `write` required",
      "extensions": {
        "type": "forbidden",
        "code": "FORBIDDEN",
        "statusCode": 403
      }
    }
  ]
}
```

### 故障排除：API 密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

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

1. 确保您的 URL 路径以 `linear` 开头。例如：
- 正确：`https://gateway.maton.ai/lineargraphql`
- 错误：`https://gateway.maton.aigraphql`

## 资源

- [Linear API 概述](https://linear.app/developers)
- [Linear GraphQL 快速入门](https://linear.app/developersgraphql)
- [Linear GraphQL 架构（Apollo Studio）](https://studio.apollographql.com/public/Linear-API/schema/reference?variant=current)
- [Linear API 和 Webhooks](https://linear.app/docs/api-and-webhooks)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)