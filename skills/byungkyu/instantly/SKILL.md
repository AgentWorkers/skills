---
name: instantly
description: |
  Instantly API integration with managed OAuth. Cold email outreach platform for managing campaigns, leads, accounts, and analytics.
  Use this skill when users want to create campaigns, manage leads, send emails, or view analytics.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Instantly

通过管理认证方式访问 Instantly API v2。您可以管理冷邮件活动（cold email campaigns）、潜在客户信息（leads）、发送账户（sending accounts），并查看分析数据（analytics）。

## 快速入门

```bash
# List campaigns
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/instantly/api/v2/campaigns?limit=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/instantly/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Instantly API 端点路径。该网关会将请求代理到 `api.instantly.ai` 并自动插入您的 API 密钥。

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
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的 Instantly 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=instantly&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'instantly'}).encode()
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
    "connection_id": "e4dca622-b9cf-4ed6-b52e-fa681345f5ac",
    "status": "ACTIVE",
    "creation_time": "2026-02-11T22:19:35.798712Z",
    "last_updated_time": "2026-02-11T22:20:15.702846Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "instantly",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成授权过程。

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

如果您有多个 Instantly 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/instantly/api/v2/campaigns')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'e4dca622-b9cf-4ed6-b52e-fa681345f5ac')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 活动管理

#### 列出活动

```bash
GET /instantly/api/v2/campaigns?limit=10&status=1&search=keyword
```

查询参数：
- `limit` - 结果数量（默认值：10）
- `status` - 活动状态过滤器（0=草稿，1=活动中，2=暂停，3=已完成）
- `search` - 按活动名称搜索
- `starting_after` - 分页的起始位置

#### 获取活动信息

```bash
GET /instantly/api/v2/campaigns/{campaign_id}
```

#### 创建活动

```bash
POST /instantly/api/v2/campaigns
Content-Type: application/json

{
  "name": "My Campaign",
  "campaign_schedule": {
    "schedules": [
      {
        "name": "My Schedule",
        "timing": {
          "from": "09:00",
          "to": "17:00"
        },
        "days": {
          "0": true,
          "1": true,
          "2": true,
          "3": true,
          "4": true
        },
        "timezone": "Etc/GMT+5"
      }
    ]
  }
}
```

注意：时区必须使用 Etc/GMT 格式（例如：“Etc/GMT+5”、“Etc/GMT-8”、“Etc/GMT+12”）。

```

#### Activate Campaign

```bash
POST /instantly/api/v2/campaigns/{campaign_id}/activate
```

#### Pause Campaign

```bash
POST /instantly/api/v2/campaigns/{campaign_id}/pause
```

#### Delete Campaign

```bash
DELETE /instantly/api/v2/campaigns/{campaign_id}
```

#### Search Campaigns by Lead Email

```bash
GET /instantly/api/v2/campaigns/search-by-contact?search=lead@example.com
```

### Leads

#### Create Lead

```bash
POST /instantly/api/v2/leads
Content-Type: application/json

{
  "campaign_id": "019bb3bd-9963-789e-b776-6c6927ef3f79",
  "email": "lead@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "company_name": "Acme Inc",
  "variables": {
    "custom_field": "custom_value"
  }
}
```

#### Bulk Add Leads

```bash
POST /instantly/api/v2/leads
Content-Type: application/json

{
  "campaign_id": "019bb3bd-9963-789e-b776-6c6927ef3f79",
  "leads": [
    {
      "email": "lead1@example.com",
      "first_name": "John"
    },
    {
      "email": "lead2@example.com",
      "first_name": "Jane"
    }
  ]
}
```

#### List Leads

Note: This is a POST endpoint due to complex filtering requirements.

```bash
POST /instantly/api/v2/leads/list
Content-Type: application/json

{
  "campaign_id": "019bb3bd-9963-789e-b776-6c6927ef3f79",
  "limit": 100
}
```

#### Get Lead

```bash
GET /instantly/api/v2/leads/{lead_id}
```

#### Delete Lead

```bash
DELETE /instantly/api/v2/leads/{lead_id}
```

#### Move Leads

```bash
POST /instantly/api/v2/leads/move
Content-Type: application/json

{
  "lead_ids": ["lead_id_1", "lead_id_2"],
  "to_campaign_id": "target_campaign_id"
}
```

### Lead Lists

#### List Lead Lists

```bash
GET /instantly/api/v2/lead-lists?limit=10
```

#### Create Lead List

```bash
POST /instantly/api/v2/lead-lists
Content-Type: application/json

{
  "name": "My Lead List"
}
```

#### Get Lead List

```bash
GET /instantly/api/v2/lead-lists/{list_id}
```

#### Update Lead List

```bash
PATCH /instantly/api/v2/lead-lists/{list_id}
Content-Type: application/json

{
  "name": "Updated List Name"
}
```

#### Delete Lead List

```bash
DELETE /instantly/api/v2/lead-lists/{list_id}
```

### Accounts (Sending Email Accounts)

#### List Accounts

```bash
GET /instantly/api/v2/accounts?limit=10
```

#### Get Account

```bash
GET /instantly/api/v2/accounts/{email}
```

#### Create Account

```bash
POST /instantly/api/v2/accounts
Content-Type: application/json

{
  "email": "sender@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "provider_code": "google",
  "smtp_host": "smtp.gmail.com",
  "smtp_port": 587,
  "smtp_username": "sender@example.com",
  "smtp_password": "app_password",
  "imap_host": "imap.gmail.com",
  "imap_port": 993,
  "imap_username": "sender@example.com",
  "imap_password": "app_password"
}
```

#### Update Account

```bash
PATCH /instantly/api/v2/accounts/{email}
Content-Type: application/json

{
  "first_name": "Jane"
}
```

#### Delete Account

```bash
DELETE /instantly/api/v2/accounts/{email}
```

#### Enable Warmup

```bash
POST /instantly/api/v2/accounts/warmup/enable
Content-Type: application/json

{
  "emails": ["account1@example.com", "account2@example.com"]
}
```

#### Disable Warmup

```bash
POST /instantly/api/v2/accounts/warmup/disable
Content-Type: application/json

{
  "emails": ["account1@example.com"]
}
```

### Emails (Unibox)

#### List Emails

```bash
GET /instantly/api/v2/emails?limit=20
```

#### Get Email

```bash
GET /instantly/api/v2/emails/{email_id}
```

#### Reply to Email

```bash
POST /instantly/api/v2/emails/reply
Content-Type: application/json

{
  "reply_to_uuid": "email_uuid",
  "body": "Thank you for your response!"
}
```

#### Forward Email

```bash
POST /instantly/api/v2/emails/forward
Content-Type: application/json

{
  "email_uuid": "email_uuid",
  "to": "forward@example.com"
}
```

#### Mark Thread as Read

```bash
POST /instantly/api/v2/emails/threads/{thread_id}/mark-as-read
```

#### Get Unread Count

```bash
GET /instantly/api/v2/emails/unread/count
```

#### Update Email

```bash
PATCH /instantly/api/v2/emails/{email_id}
Content-Type: application/json

{
  "is_read": true
}
```

#### Delete Email

```bash
DELETE /instantly/api/v2/emails/{email_id}
```

### Analytics

#### Get Campaign Analytics

```bash
GET /instantly/api/v2/campaigns/analytics?id={campaign_id}
```

Query parameters:
- `id` - Campaign ID (leave empty for all campaigns)
- `start_date` - Filter start date (YYYY-MM-DD)
- `end_date` - Filter end date (YYYY-MM-DD)
- `exclude_total_leads_count` - Set to true for faster response

#### Get Campaign Analytics Overview

```bash
GET /instantly/api/v2/campaigns/analytics/overview?id={campaign_id}
```

#### Get Daily Campaign Analytics

```bash
GET /instantly/api/v2/campaigns/analytics/daily?id={campaign_id}
```

#### Get Campaign Step Analytics

```bash
GET /instantly/api/v2/campaigns/analytics/steps?id={campaign_id}
```

#### Get Warmup Analytics

```bash
POST /instantly/api/v2/accounts/warmup/analytics
Content-Type: application/json

{
  "emails": ["account@example.com"]
}
```

### Block List

#### List Block List Entries

```bash
GET /instantly/api/v2/block-lists-entries?limit=100
```

Query parameters:
- `domains_only` - Filter to domain entries only
- `search` - Search entries

#### Create Block List Entry

```bash
POST /instantly/api/v2/block-lists-entries
Content-Type: application/json

{
  "bl_value": "blocked@example.com"
}
```

Or block a domain:

```bash
POST /instantly/api/v2/block-lists-entries
Content-Type: application/json

{
  "bl_value": "blockeddomain.com"
}
```

#### Delete Block List Entry

```bash
DELETE /instantly/api/v2/block-lists-entries/{entry_id}
```

### Email Verification

#### Verify Email

```bash
GET /instantly/api/v2/email-verification/{email}
```

If verification takes longer than 10 seconds, status will be `pending`. Poll this endpoint to check status.

Response fields:
- `verification_status` - Use this field (not `status`) to determine verification result

### Background Jobs

#### Get Background Job Status

```bash
GET /instantly/api/v2/background-jobs/{job_id}
```

Query parameters:
- `data_fields` - Comma-separated fields (e.g., `success_count,failed_count,total_to_process`)

### Workspace

#### Get Current Workspace

```bash
GET /instantly/api/v2/workspaces/current
```

### Custom Tags

#### Toggle Tag on Resource

```bash
POST /instantly/api/v2/custom-tags/toggle-resource
Content-Type: application/json

{
  "tag_id": "tag_uuid",
  "resource_id": "campaign_or_account_id",
  "resource_type": "campaign"
}
```

## Pagination

Instantly uses cursor-based pagination with `limit` and `starting_after`:

```bash
GET /instantly/api/v2/campaigns?limit=10&starting_after=cursor_value
```

Response includes pagination info:

```json
{
  "items": [...],
  "next_starting_after": "cursor_for_next_page"
}
```

Use `next_starting_after` value in the next request's `starting_after` parameter.

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/instantly/api/v2/campaigns?limit=10',
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
    'https://gateway.maton.ai/instantly/api/v2/campaigns',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'limit': 10}
)
data = response.json()
```

## Notes

- Instantly API v2 uses snake_case for all field names
- Lead custom variables must be string, number, boolean, or null (no objects/arrays)
- The List Leads endpoint is POST (not GET) due to complex filtering requirements
- Campaign status values: 0=draft, 1=active, 2=paused, 3=completed
- Email verification may return `pending` status if it takes longer than 10 seconds
- Warmup operations return background job IDs - poll the background jobs endpoint for status
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq`, environment variables may not expand correctly. Use Python examples instead.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Instantly connection or invalid request |
| 401 | Invalid or missing Maton API key |
| 403 | Insufficient API key scopes |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Instantly API |

### Troubleshooting: API Key Issues

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF

### 故障排除：应用程序名称无效

1. 确保您的 URL 路径以 `instantly` 开头。例如：
- 正确：`https://gateway.maton.ai/instantly/api/v2/campaigns`
- 错误：`https://gateway.maton.ai/api/v2/campaigns`

## 资源

- [Instantly API V2 文档](https://developer.instantly.ai/api/v2)
- [Instantly API 介绍](https://developer.instantly.ai/)
- [Instantly 帮助中心](https://help.instantly.ai/)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)