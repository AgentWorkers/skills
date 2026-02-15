---
name: fathom
description: |
  Fathom API integration with managed OAuth. Access meeting recordings, transcripts, summaries, and manage webhooks. Use this skill when users want to retrieve meeting content, search recordings, or set up webhook notifications for new meetings. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Fathom

您可以使用托管的 OAuth 认证来访问 Fathom API。该 API 允许您检索会议记录、会议转录文本、会议摘要、待办事项，并管理用于通知的 Webhook。

## 快速入门

```bash
# List recent meetings
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/fathom/external/v1/meetings')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/fathom/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Fathom API 端点路径。该网关会将请求代理到 `api.fathom.ai`，并自动插入您的 OAuth 令牌。

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
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Fathom OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=fathom&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'fathom'}).encode()
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
    "app": "fathom",
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

如果您有多个 Fathom 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/fathom/external/v1/meetings')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 会议

#### 列出会议

```bash
GET /fathom/external/v1/meetings
```

查询参数：
- `cursor` - 用于分页的游标
- `created_after` - 筛选在此时间戳之后创建的会议（例如：`2025-01-01T00:00:00Z`）
- `created_before` - 筛选在此时间戳之前创建的会议
- `calendarInviteesDomains[]` - 按公司域名筛选（每个值传递一次）
- `calendarInviteesDomainsType` - 按受邀者类型筛选：`all`、`only_internal`、`one_or_more_external`
- `recorded_by[]` - 按录制会议的用户的电子邮件地址筛选
- `teams[]` - 按团队名称筛选

**注意：** 使用 OAuth 认证的用户无法在此端点使用 `include_transcript`、`include_summary`、`include_action_items` 或 `include_crm_matches` 参数。请使用 `/recordings/{recording_id}/summary` 和 `/recordings/{recording_id}/transcript` 端点。

**带筛选条件的示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/fathom/external/v1/meetings?created_after=2025-01-01T00:00:00Z&teams[]=Sales')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "limit": 10,
  "next_cursor": "eyJwYWdlX251bSI6Mn0=",
  "items": [
    {
      "title": "Quarterly Business Review",
      "meeting_title": "QBR 2025 Q1",
      "recording_id": 123456789,
      "url": "https://fathom.video/xyz123",
      "share_url": "https://fathom.video/share/xyz123",
      "created_at": "2025-03-01T17:01:30Z",
      "scheduled_start_time": "2025-03-01T16:00:00Z",
      "scheduled_end_time": "2025-03-01T17:00:00Z",
      "recording_start_time": "2025-03-01T16:01:12Z",
      "recording_end_time": "2025-03-01T17:00:55Z",
      "calendar_invitees_domains_type": "one_or_more_external",
      "transcript_language": "en",
      "transcript": null,
      "default_summary": null,
      "action_items": null,
      "crm_matches": null,
      "recorded_by": {
        "name": "Alice Johnson",
        "email": "alice.johnson@acme.com",
        "email_domain": "acme.com",
        "team": "Marketing"
      },
      "calendar_invitees": [
        {
          "name": "Alice Johnson",
          "email": "alice.johnson@acme.com",
          "email_domain": "acme.com",
          "is_external": false,
          "matched_speaker_display_name": null
        }
      ]
    }
  ]
}
```

### 会议记录

#### 获取会议摘要

```bash
GET /fathom/external/v1/recordings/{recording_id}/summary
```

查询参数：
- `destination_url` - 可选的异步回调 URL。如果提供了此 URL，摘要将被发送到该地址。

**同步示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/fathom/external/v1/recordings/123456789/summary')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "summary": {
    "template_name": "general",
    "markdown_formatted": "## Summary\n\nWe reviewed Q1 OKRs, identified budget risks, and agreed to revisit projections next month."
  }
}
```

**异步示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/fathom/external/v1/recordings/123456789/summary?destination_url=https://example.com/webhook')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取会议转录文本

```bash
GET /fathom/external/v1/recordings/{recording_id}/transcript
```

查询参数：
- `destination_url` - 可选的异步回调 URL。如果提供了此 URL，转录文本将被发送到该地址。

**同步示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/fathom/external/v1/recordings/123456789/transcript')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "transcript": [
    {
      "speaker": {
        "display_name": "Alice Johnson",
        "matched_calendar_invitee_email": "alice.johnson@acme.com"
      },
      "text": "Let's revisit the budget allocations.",
      "timestamp": "00:05:32"
    }
  ]
}
```

### 团队

#### 列出团队

```bash
GET /fathom/external/v1/teams
```

查询参数：
- `cursor` - 用于分页的游标

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/fathom/external/v1/teams')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "limit": 25,
  "next_cursor": null,
  "items": [
    {
      "name": "Sales",
      "created_at": "2023-11-10T12:00:00Z"
    }
  ]
}
```

### 团队成员

#### 列出团队成员

```bash
GET /fathom/external/v1/team_members
```

查询参数：
- `cursor` - 用于分页的游标
- `team` - 要筛选的团队名称

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/fathom/external/v1/team_members?team=Sales')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "limit": 25,
  "next_cursor": null,
  "items": [
    {
      "name": "Bob Lee",
      "email": "bob.lee@acme.com",
      "created_at": "2024-06-01T08:30:00Z"
    }
  ]
}
```

### Webhook

#### 创建 Webhook

```bash
POST /fathom/external/v1/webhooks
Content-Type: application/json

{
  "destination_url": "https://example.com/webhook",
  "triggered_for": ["my_recordings", "my_shared_with_team_recordings"],
  "include_transcript": true,
  "include_summary": true,
  "include_action_items": true,
  "include_crm_matches": false
}
```

**triggered_for** 选项：
- `my_recordings` - 您私有的会议记录（不包括通过 Team Plans 与团队共享的记录）
- `shared_external_recordings` - 其他用户与您共享的会议记录
- `my_shared_with_team_recordings` - 您与团队共享的会议记录
- `shared_team_recordings` - （Team Plans）来自您团队计划的其他用户的会议记录

必须至少选择 `include_transcript`、`include_summary`、`include_action_items` 或 `include_crm_matches` 中的一个选项。

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'destination_url': 'https://example.com/webhook', 'triggered_for': ['my_recordings'], 'include_summary': True}).encode()
req = urllib.request.Request('https://gateway.maton.ai/fathom/external/v1/webhooks', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "id": "ikEoQ4bVoq4JYUmc",
  "url": "https://example.com/webhook",
  "secret": "whsec_x6EV6NIAAz3ldclszNJTwrow",
  "created_at": "2025-06-30T10:40:46Z",
  "include_transcript": false,
  "include_crm_matches": false,
  "include_summary": true,
  "include_action_items": false,
  "triggered_for": ["my_recordings"]
}
```

#### 删除 Webhook

```bash
DELETE /fathom/external/v1/webhooks/{id}
```

**示例：**

**响应：**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/fathom/external/v1/webhooks/ikEoQ4bVoq4JYUmc', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

成功时返回 `204 No Content`。

## 分页

使用 `cursor` 进行分页。如果存在更多结果，响应中会包含 `next_cursor`：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/fathom/external/v1/meetings?cursor=eyJwYWdlX251bSI6Mn0=')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/fathom/external/v1/meetings?created_after=2025-01-01T00:00:00Z',
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
    'https://gateway.maton.ai/fathom/external/v1/meetings',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'created_after': '2025-01-01T00:00:00Z'}
)
data = response.json()
```

## 注意事项

- 会议记录的 ID 是整数。
- 时间戳采用 ISO 8601 格式。
- 转录文本和会议摘要为英文。
- Webhook 密钥用于验证 Webhook 签名。
- CRM 匹配仅返回来自您或您团队关联的 CRM 的数据。
- **重要提示：** 当 URL 包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 可以避免全局解析问题。
- **重要提示：** 当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确展开，这可能导致 “Invalid API key” 错误。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 请求错误或未建立 Fathom 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 资源未找到 |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自 Fathom API 的传递错误 |

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

1. 确保您的 URL 路径以 `fathom` 开头。例如：
- 正确：`https://gateway.maton.ai/fathom/external/v1/meetings`
- 错误：`https://gateway.maton.ai/external/v1/meetings`

## 资源

- [Fathom API 文档](https://developers.fathom.ai)
- [LLM 参考](https://developers.fathom.ai/llms.txt)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)