---
name: posthog
description: >
  **PostHog API集成与托管式身份验证**  
  支持产品分析、功能开关管理、会话记录查看、实验设计等功能。  
  当用户需要查询分析事件、管理功能开关、分析用户行为、查看会话记录或进行A/B测试时，可使用此功能。  
  对于其他第三方应用程序，请使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🦔
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# PostHog

您可以使用托管的身份验证方式访问 PostHog API。通过 HogQL 查询产品分析事件、管理功能标志、分析用户行为、查看会话记录以及运行 A/B 实验。

## 快速入门

```bash
# List projects
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/posthog/api/projects/')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/posthog/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 PostHog API 端点路径。网关会将请求代理到 `{subdomain}.posthog.com` 并自动插入您的凭据。

## 身份验证

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
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的 PostHog OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=posthog&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'posthog'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接

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
    "connection_id": "ce2b0840-4e39-4b58-b607-7290fa7a3595",
    "status": "ACTIVE",
    "creation_time": "2026-02-23T09:37:57.686121Z",
    "last_updated_time": "2026-02-23T09:39:11.851118Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "posthog",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成 OAuth 授权。

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

如果您有多个 PostHog 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/posthog/api/projects/')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'ce2b0840-4e39-4b58-b607-7290fa7a3595')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略该头部，网关将使用默认的（最旧的）活动连接。

## API 参考

### 组织

#### 获取当前组织

```bash
GET /posthog/api/organizations/@current/
```

### 项目

#### 列出项目

```bash
GET /posthog/api/projects/
```

**响应：**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 136209,
      "uuid": "019583c6-377c-0000-e55c-8696cbc33595",
      "organization": "019583c6-3635-0000-5798-c18f20963b3b",
      "api_token": "phc_XXX",
      "name": "Default project",
      "timezone": "UTC"
    }
  ]
}
```

#### 获取当前项目

```bash
GET /posthog/api/projects/@current/
```

### 用户

#### 获取当前用户

```bash
GET /posthog/api/users/@me/
```

### 查询（HogQL）

查询端点是检索事件和运行分析查询的推荐方式。

#### 运行 HogQL 查询

```bash
POST /posthog/api/projects/{project_id}/query/
Content-Type: application/json

{
  "query": {
    "kind": "HogQLQuery",
    "query": "SELECT event, count() FROM events GROUP BY event ORDER BY count() DESC LIMIT 10"
  }
}
```

**响应：**
```json
{
  "columns": ["event", "count()"],
  "results": [
    ["$pageview", 140504],
    ["$autocapture", 108691],
    ["$identify", 5455]
  ],
  "types": [
    ["event", "String"],
    ["count()", "UInt64"]
  ]
}
```

### 人员

#### 列出人员

```bash
GET /posthog/api/projects/{project_id}/persons/?limit=10
```

**响应：**
```json
{
  "results": [
    {
      "id": "5d79eecb-93e6-5c8b-90f9-8510ba4040b8",
      "uuid": "5d79eecb-93e6-5c8b-90f9-8510ba4040b8",
      "name": "user@example.com",
      "is_identified": true,
      "distinct_ids": ["user-uuid", "anon-uuid"],
      "properties": {
        "email": "user@example.com",
        "name": "John Doe"
      }
    }
  ],
  "next": "https://us.posthog.com/api/projects/{project_id}/persons/?limit=10&offset=10"
}
```

#### 获取人员信息

```bash
GET /posthog/api/projects/{project_id}/persons/{person_uuid}/
```

### 仪表板

#### 列出仪表板

```bash
GET /posthog/api/projects/{project_id}/dashboards/
```

#### 获取仪表板

```bash
GET /posthog/api/projects/{project_id}/dashboards/{dashboard_id}/
```

#### 创建仪表板

```bash
POST /posthog/api/projects/{project_id}/dashboards/
Content-Type: application/json

{
  "name": "My Dashboard",
  "description": "Analytics overview"
}
```

#### 更新仪表板

```bash
PATCH /posthog/api/projects/{project_id}/dashboards/{dashboard_id}/
Content-Type: application/json

{
  "name": "Updated Dashboard Name"
}
```

### 洞察

#### 列出洞察数据

```bash
GET /posthog/api/projects/{project_id}/insights/?limit=10
```

#### 获取洞察数据

```bash
GET /posthog/api/projects/{project_id}/insights/{insight_id}/
```

#### 创建洞察数据

```bash
POST /posthog/api/projects/{project_id}/insights/
Content-Type: application/json

{
  "name": "Daily Active Users",
  "query": {
    "kind": "InsightVizNode",
    "source": {
      "kind": "TrendsQuery",
      "series": [{"kind": "EventsNode", "event": "$pageview", "math": "dau"}],
      "interval": "day",
      "dateRange": {"date_from": "-30d"}
    }
  }
}
```

### 功能标志

#### 列出功能标志

```bash
GET /posthog/api/projects/{project_id}/feature_flags/
```

#### 获取功能标志信息

```bash
GET /posthog/api/projects/{project_id}/feature_flags/{flag_id}/
```

#### 创建功能标志

```bash
POST /posthog/api/projects/{project_id}/feature_flags/
Content-Type: application/json

{
  "key": "my-feature-flag",
  "name": "My Feature Flag",
  "active": true,
  "filters": {
    "groups": [{"rollout_percentage": 100}]
  }
}
```

#### 更新功能标志

#### 删除功能标志

通过设置 `deleted: true` 来实现软删除：

```bash
PATCH /posthog/api/projects/{project_id}/feature_flags/{flag_id}/
Content-Type: application/json

{
  "deleted": true
}
```

### 分组

#### 列出分组

```bash
GET /posthog/api/projects/{project_id}/cohorts/
```

#### 获取分组信息

```bash
GET /posthog/api/projects/{project_id}/cohorts/{cohort_id}/
```

#### 创建分组

```bash
POST /posthog/api/projects/{project_id}/cohorts/
Content-Type: application/json

{
  "name": "Active Users",
  "groups": [
    {
      "properties": [
        {"key": "$pageview", "type": "event", "value": "performed_event"}
      ]
    }
  ]
}
```

### 操作

#### 列出操作记录

```bash
GET /posthog/api/projects/{project_id}/actions/
```

#### 创建操作记录

```bash
POST /posthog/api/projects/{project_id}/actions/
Content-Type: application/json

{
  "name": "Signed Up",
  "steps": [{"event": "$identify"}]
}
```

### 会话记录

#### 列出会话记录

```bash
GET /posthog/api/projects/{project_id}/session_recordings/?limit=10
```

**响应：**
```json
{
  "results": [
    {
      "id": "019c8795-79e3-7a05-ac56-597b102f1960",
      "distinct_id": "user-uuid",
      "recording_duration": 1807,
      "start_time": "2026-02-22T23:00:46.389000Z",
      "end_time": "2026-02-22T23:30:53.297000Z",
      "click_count": 0,
      "keypress_count": 0,
      "start_url": "https://example.com/register"
    }
  ],
  "has_next": false
}
```

#### 获取会话记录

```bash
GET /posthog/api/projects/{project_id}/session_recordings/{recording_id}/
```

### 注释

#### 列出注释

```bash
GET /posthog/api/projects/{project_id}/annotations/
```

#### 创建注释

```bash
POST /posthog/api/projects/{project_id}/annotations/
Content-Type: application/json

{
  "content": "New feature launched",
  "date_marker": "2026-02-23T00:00:00Z",
  "scope": "project"
}
```

### 调查

#### 列出调查

```bash
GET /posthog/api/projects/{project_id}/surveys/
```

#### 创建调查

```bash
POST /posthog/api/projects/{project_id}/surveys/
Content-Type: application/json

{
  "name": "NPS Survey",
  "type": "popover",
  "questions": [
    {
      "type": "rating",
      "question": "How likely are you to recommend us?"
    }
  ]
}
```

### 实验

#### 列出实验

```bash
GET /posthog/api/projects/{project_id}/experiments/
```

#### 创建实验

```bash
POST /posthog/api/projects/{project_id}/experiments/
Content-Type: application/json

{
  "name": "Button Color Test",
  "feature_flag_key": "button-color-test"
}
```

### 事件定义

#### 列出事件定义

```bash
GET /posthog/api/projects/{project_id}/event_definitions/?limit=10
```

### 属性定义

#### 列出属性定义

```bash
GET /posthog/api/projects/{project_id}/property_definitions/?limit=10
```

## 分页

PostHog 使用基于偏移量的分页机制：

```bash
GET /posthog/api/projects/{project_id}/persons/?limit=10&offset=20
```

响应中包含分页信息：

```json
{
  "count": 100,
  "next": "https://us.posthog.com/api/projects/{project_id}/persons/?limit=10&offset=30",
  "previous": "https://us.posthog.com/api/projects/{project_id}/persons/?limit=10&offset=10",
  "results": [...]
}
```

对于会话记录，可以使用 `has_next` 布尔值来判断是否还有更多记录：

```json
{
  "results": [...],
  "has_next": true
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/posthog/api/projects/',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/posthog/api/projects/',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

### Python - 使用 HogQL 查询

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/posthog/api/projects/@current/query/',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'query': {
            'kind': 'HogQLQuery',
            'query': 'SELECT event, count() FROM events GROUP BY event LIMIT 10'
        }
    }
)
data = response.json()
```

## 注意事项

- 使用 `@current` 作为当前项目 ID 的快捷方式（例如：`/api/projects/@current/dashboards/`）。
- 项目 ID 是整数（例如：`136209`）。
- 人员 UUID 采用标准 UUID 格式。
- `Events` 端点已弃用；请改用带有 HogQL 的查询端点。
- 会话记录包含活动指标（如 `click_count`、`keypress_count`）。
- PostHog 使用软删除机制：请使用 `PATCH` 请求并设置 `{"deleted": true}` 而不是 HTTP DELETE。
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中可能无法正确解析环境变量 `$MATON_API_KEY`。建议使用 Python 代码示例。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 PostHog 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 请求频率受限 |
| 4xx/5xx | 来自 PostHog API 的传递错误 |

### 请求频率限制

- 分析相关端点（洞察数据、人员信息、会话记录）：每分钟 240 次请求，每小时 1200 次请求。
- HogQL 查询端点：每小时 120 次请求。
- 创建/读取/更新/删除相关端点：每分钟 480 次请求，每小时 4800 次请求。

## 资源

- [PostHog API 概述](https://posthog.com/docs/api)
- [HogQL 文档](https://posthog.com/docs/hogql)
- [功能标志](https://posthog.com/docs/feature-flags)
- [会话回放](https://posthog.com/docs/session-replay)
- [实验](https://posthog.com/docs/experiments)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)