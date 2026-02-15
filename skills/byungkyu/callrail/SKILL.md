---
name: callrail
description: |
  CallRail API integration with managed OAuth. Track and analyze phone calls, manage tracking numbers, companies, and tags.
  Use this skill when users want to access call data, manage tracking numbers, view call analytics, or organize calls with tags.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# CallRail

使用托管的 OAuth 认证来访问 CallRail API。您可以跟踪通话记录、管理跟踪号码、分析通话数据，并通过标签对数据进行分类。

## 快速入门

```bash
# List all calls
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/callrail/v3/a/{account_id}/calls.json')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/callrail/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 CallRail API 端点路径。该网关会将请求代理到 `api.callrail.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 标头中包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的 CallRail OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=callrail&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'callrail'}).encode()
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
    "connection_id": "75364cb9-7116-4367-a707-1113d426f17d",
    "status": "ACTIVE",
    "creation_time": "2026-02-10T09:55:17.574212Z",
    "last_updated_time": "2026-02-10T09:55:34.693801Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "callrail",
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

如果您有多个 CallRail 连接，请使用 `Maton-Connection` 标头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/callrail/v3/a.json')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '75364cb9-7116-4367-a707-1113d426f17d')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，网关将使用默认的（最旧的）活动连接。

## API 参考

### URL 构造

所有 CallRail API 端点都遵循以下格式：

```
/callrail/v3/a/{account_id}/{resource}.json
```

账户 ID 以 `ACC` 开头，公司 ID 以 `COM` 开头，通话 ID 以 `CAL` 开头，跟踪器 ID 以 `TRK` 开头，用户 ID 以 `USR` 开头。

---

## 账户

### 列出账户

```bash
GET /callrail/v3/a.json
```

**响应：**
```json
{
  "page": 1,
  "per_page": 100,
  "total_pages": 1,
  "total_records": 1,
  "accounts": [
    {
      "id": "ACC019c46b8a0807fbdb81c8bf12af91cb3",
      "name": "My Account",
      "numeric_id": 518664017,
      "inbound_recording_enabled": false,
      "outbound_recording_enabled": false,
      "hipaa_account": false,
      "created_at": "2026-02-10 03:43:50 -0500"
    }
  ]
}
```

### 获取账户信息

```bash
GET /callrail/v3/a/{account_id}.json
```

---

## 公司

### 列出公司

```bash
GET /callrail/v3/a/{account_id}/companies.json
```

**响应：**
```json
{
  "page": 1,
  "per_page": 100,
  "total_pages": 1,
  "total_records": 1,
  "companies": [
    {
      "id": "COM019c46b8a26376a9a4f29671dcdd49e9",
      "name": "My Company",
      "status": "active",
      "time_zone": "America/Los_Angeles",
      "created_at": "2026-02-10T08:43:51.280Z",
      "callscore_enabled": false,
      "lead_scoring_enabled": true,
      "callscribe_enabled": true
    }
  ]
}
```

### 获取公司信息

```bash
GET /callrail/v3/a/{account_id}/companies/{company_id}.json
```

---

## 通话记录

### 列出通话记录

```bash
GET /callrail/v3/a/{account_id}/calls.json
```

**查询参数：**

| 参数 | 描述 |
|-----------|-------------|
| `page` | 页码（默认：1） |
| `per_page` | 每页显示的结果数量（默认：100，最大：250） |
| `date_range` | 预设值：`recent`、`today`、`yesterday`、`last_7_days`、`last_30_days`、`this_month`、`last_month` |
| `start_date` | ISO 8601 格式的日期（例如：`2026-02-01T00:00:00-08:00`） |
| `end_date` | ISO 8601 格式的日期 |
| `company_id` | 按公司过滤 |
| `tracker_id` | 按跟踪器过滤 |
| `search` | 搜索词 |
| `fields` | 要返回的字段名称（用逗号分隔） |
| `sort` | 排序字段 |
| `order` | 排序方式：`asc` 或 `desc` |

**响应：**
```json
{
  "page": 1,
  "per_page": 100,
  "total_pages": 1,
  "total_records": 1,
  "calls": [
    {
      "id": "CAL019c46b9fc277a7881e3728fea20869b",
      "answered": false,
      "customer_name": "John Doe",
      "customer_phone_number": "+18886757190",
      "direction": "inbound",
      "duration": 36,
      "recording": "https://api.callrail.com/v3/a/.../recording",
      "recording_duration": 36,
      "start_time": "2026-02-10T00:45:19.781-08:00",
      "tracking_phone_number": "+18017846712",
      "voicemail": true
    }
  ]
}
```

### 获取通话记录详情

```bash
GET /callrail/v3/a/{account_id}/calls/{call_id}.json
```

### 更新通话记录

```bash
PUT /callrail/v3/a/{account_id}/calls/{call_id}.json
Content-Type: application/json

{
  "customer_name": "John Smith",
  "note": "Follow up scheduled",
  "lead_status": "good_lead",
  "spam": false
}
```

**可更新的字段：**

| 字段 | 描述 |
|-------|-------------|
| `customer_name` | 客户名称 |
| `note` | 通话备注 |
| `lead_status` | `good_lead`、`not_a_lead`、`previously_marked_good_lead` |
| `spam` | 标记为垃圾邮件（布尔值） |
| `tag_list` | 要应用的标签名称数组 |
| `value` | 通话价值（数值） |
| `append_tags` | 添加标签（不会删除现有标签） |

### 通话统计

```bash
GET /callrail/v3/a/{account_id}/calls/summary.json
```

获取指定日期范围内的通话统计信息。

**查询参数：**

| 参数 | 描述 |
|-----------|-------------|
| `date_range` | 预设的日期范围 |
| `start_date` | 开始日期（ISO 8601 格式） |
| `end_date` | 结束日期（ISO 8601 格式） |
| `group_by` | 分组方式：`company`、`tracker`、`source` 等 |

**响应：**
```json
{
  "start_date": "2026-02-03T00:00:00-0800",
  "end_date": "2026-02-10T23:59:59-0800",
  "time_zone": "Pacific Time (US & Canada)",
  "total_results": {
    "total_calls": 42
  }
}
```

### 通话时间序列数据

```bash
GET /callrail/v3/a/{account_id}/calls/timeseries.json
```

获取用于图表显示的通话数据。

**响应：**
```json
{
  "start_date": "2026-02-03T00:00:00-0800",
  "end_date": "2026-02-10T23:59:59-0800",
  "data": [
    {"key": "2026-02-03", "date": "2026-02-03", "total_calls": 5},
    {"key": "2026-02-04", "date": "2026-02-04", "total_calls": 8}
  ]
}
```

---

## 跟踪器（跟踪号码）

### 列出跟踪器

```bash
GET /callrail/v3/a/{account_id}/trackers.json
```

**响应：**
```json
{
  "page": 1,
  "per_page": 100,
  "total_records": 1,
  "trackers": [
    {
      "id": "TRK019c46b9f18174d68bb8d7985260a11f",
      "name": "Google My Business",
      "type": "source",
      "status": "active",
      "destination_number": "+18019234886",
      "tracking_numbers": ["+18017846712"],
      "sms_supported": true,
      "sms_enabled": true,
      "company": {
        "id": "COM019c46b8a26376a9a4f29671dcdd49e9",
        "name": "My Company"
      },
      "source": {"type": "google_my_business"},
      "call_flow": {
        "type": "basic",
        "recording_enabled": true,
        "destination_number": "+18019234886"
      }
    }
  ]
}
```

### 获取跟踪器信息

```bash
GET /callrail/v3/a/{account_id}/trackers/{tracker_id}.json
```

---

## 标签

### 列出标签

```bash
GET /callrail/v3/a/{account_id}/tags.json
```

**响应：**
```json
{
  "page": 1,
  "per_page": 100,
  "total_records": 6,
  "tags": [
    {
      "id": 7886733,
      "name": "Schedule requested",
      "tag_level": "account",
      "color": "orange3",
      "background_color": "gray1",
      "company_id": null,
      "status": "enabled"
    },
    {
      "id": 7886728,
      "name": "Opportunity",
      "tag_level": "company",
      "color": "gray1",
      "company_id": "COM019c46b8a26376a9a4f29671dcdd49e9",
      "status": "enabled"
    }
  ]
}
```

### 创建标签

```bash
POST /callrail/v3/a/{account_id}/tags.json
Content-Type: application/json

{
  "name": "New Tag",
  "tag_level": "account",
  "color": "blue1"
}
```

**标签级别：**
- `account` - 对账户内的所有公司可用 |
- `company` - 仅针对特定公司（需要 `company_id`）

**颜色：** `gray1`、`blue1`、`blue2`、`green1`、`green2`、`orange1`、`orange2`、`orange3`、`red1` 等。

### 更新标签

```bash
PUT /callrail/v3/a/{account_id}/tags/{tag_id}.json
Content-Type: application/json

{
  "name": "Updated Tag Name",
  "color": "green1"
}
```

### 删除标签

```bash
DELETE /callrail/v3/a/{account_id}/tags/{tag_id}.json
```

---

## 用户

### 列出用户

```bash
GET /callrail/v3/a/{account_id}/users.json
```

**响应：**
```json
{
  "page": 1,
  "per_page": 100,
  "total_records": 1,
  "users": [
    {
      "id": "USR019c46b8a0557b2e85e5e1c651452509",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "name": "John Doe",
      "role": "admin",
      "accepted": true,
      "created_at": "2026-02-10T03:43:50.798-05:00",
      "companies": [
        {"id": "COM...", "name": "My Company"}
      ]
    }
  ]
}
```

### 获取用户信息

```bash
GET /callrail/v3/a/{account_id}/users/{user_id}.json
```

---

## 集成

### 列出集成信息

```bash
GET /callrail/v3/a/{account_id}/integrations.json?company_id={company_id}
```

**注意：** 需要提供 `company_id`。

---

## 通知

### 列出通知信息

```bash
GET /callrail/v3/a/{account_id}/notifications.json
```

---

## 分页

CallRail 使用基于偏移量的分页机制：

```bash
GET /callrail/v3/a/{account_id}/calls.json?page=2&per_page=50
```

**响应包含：**
```json
{
  "page": 2,
  "per_page": 50,
  "total_pages": 10,
  "total_records": 487,
  "calls": [...]
}
```

**参数：**
- `page` | 页码（默认：1）
- `per_page` | 每页显示的结果数量（默认：100，最大：250）

对于通话记录端点，您还可以使用相对分页：

```bash
GET /callrail/v3/a/{account_id}/calls.json?relative_pagination=true
```

这会返回 `next_page` URL 和 `has_next_page` 布尔值，以便高效地对大量数据进行分页。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/callrail/v3/a/{account_id}/calls.json',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.calls);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/callrail/v3/a/{account_id}/calls.json',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'per_page': 50, 'date_range': 'last_30_days'}
)
data = response.json()
for call in data['calls']:
    print(f"{call['customer_name']}: {call['duration']}s")
```

## 速率限制

| 端点类型 | 每小时限制 | 每天限制 |
|--------------|--------------|-------------|
| 通用 API | 1,000 | 10,000 |
| 发送短信 | 150 | 1,000 |
| 外拨电话 | 100 | 2,000 |

超出限制会导致 HTTP 429 错误。请实施指数退避策略进行重试。

## 注意事项

- 账户 ID 以 `ACC` 开头 |
- 公司 ID 以 `COM` 开头 |
- 通话 ID 以 `CAL` 开头 |
- 跟踪器 ID 以 `TRK` 开头 |
- 用户 ID 以 `USR` 开头 |
- 所有端点的结尾都是 `.json` |
- 通信记录会保留 25 个月 |
- 日期/时间值使用带有时区的 ISO 8601 格式 |
- 重要提示：当 URL 中包含括号时，使用 `curl -g` 命令来禁用全局解析 |
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中可能无法正确解析环境变量 `$MATON_API_KEY` |

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求错误或缺少必要参数 |
| 401 | 无效或缺失的 Maton API 密钥 |
| 403 | 禁止访问 - 权限不足 |
| 404 | 资源未找到 |
| 422 | 实体无法处理 |
| 429 | 速率限制 |
| 500 | 服务器内部错误 |
| 503 | 服务不可用 |

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

### 故障排除：应用程序名称无效

1. 确保您的 URL 路径以 `callrail` 开头。例如：
- 正确的格式：`https://gateway.maton.ai/callrail/v3/a.json`
- 错误的格式：`https://gateway.maton.ai/v3/a.json`

## 资源

- [CallRail API 文档](https://apidocs.callrail.com/)
- [CallRail 帮助中心 - API](https://support.callrail.com/hc/en-us/sections/4426797289229-API)
- [CallRail API 速率限制](https://apidocs.callrail.com/#rate-limiting)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)