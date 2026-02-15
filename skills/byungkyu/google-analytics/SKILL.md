---
name: google-analytics
description: |
  Google Analytics API integration with managed OAuth. Manage accounts, properties, and data streams (Admin API). Run reports on sessions, users, page views, and conversions (Data API). Use this skill when users want to configure or query Google Analytics. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Google Analytics

您可以使用托管的 OAuth 认证来访问 Google Analytics。本文档涵盖了 Admin API（用于管理账户、属性和数据流）和 Data API（用于运行报告）的相关内容。

## 快速入门

```bash
# List account summaries (Admin API)
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-analytics-admin/v1beta/accountSummaries')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF

# Run a report (Data API)
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}], 'dimensions': [{'name': 'city'}], 'metrics': [{'name': 'activeUsers'}]}).encode()
req = urllib.request.Request('https://gateway.maton.ai/google-analytics-data/v1beta/properties/{propertyId}:runReport', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

**Admin API**（用于管理账户、属性和数据流）：
```
https://gateway.maton.ai/google-analytics-admin/{native-api-path}
```

**Data API**（用于运行报告）：
```
https://gateway.maton.ai/google-analytics-data/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Google Analytics API 端点路径。Maton 代理会将请求转发到 `analyticsadmin.googleapis.com` 和 `analyticsdata.googleapis.com`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头中包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Google OAuth 连接。

**注意：** Admin API 和 Data API 使用不同的连接：
- `google-analytics-admin`：用于 Admin API 端点（管理账户、属性和数据流）。
- `google-analytics-data`：用于 Data API 端点（运行报告）。
根据您要使用的 API 创建相应的连接。

### 列出连接

```bash
# List Admin API connections
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-analytics-admin&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF

# List Data API connections
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-analytics-data&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
# Create Admin API connection (for managing accounts, properties, data streams)
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-analytics-admin'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF

# Create Data API connection (for running reports)
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-analytics-data'}).encode()
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
    "app": "google-analytics-admin",
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

如果您有多个 Google Analytics 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-analytics-admin/v1beta/accountSummaries')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头，Maton 代理将使用默认的（最旧的）活动连接。

## Admin API 参考

### 账户

```bash
GET /google-analytics-admin/v1beta/accounts
GET /google-analytics-admin/v1beta/accounts/{accountId}
GET /google-analytics-admin/v1beta/accountSummaries
```

### 属性

```bash
GET /google-analytics-admin/v1beta/properties?filter=parent:accounts/{accountId}
GET /google-analytics-admin/v1beta/properties/{propertyId}
```

#### 创建属性

```bash
POST /google-analytics-admin/v1beta/properties
Content-Type: application/json

{
  "parent": "accounts/{accountId}",
  "displayName": "My New Property",
  "timeZone": "America/Los_Angeles",
  "currencyCode": "USD"
}
```

### 数据流

```bash
GET /google-analytics-admin/v1beta/properties/{propertyId}/dataStreams
```

#### 创建 Web 数据流

```bash
POST /google-analytics-admin/v1beta/properties/{propertyId}/dataStreams
Content-Type: application/json

{
  "type": "WEB_DATA_STREAM",
  "displayName": "My Website",
  "webStreamData": {"defaultUri": "https://example.com"}
}
```

### 自定义维度

```bash
GET /google-analytics-admin/v1beta/properties/{propertyId}/customDimensions
```

#### 创建自定义维度

```bash
POST /google-analytics-admin/v1beta/properties/{propertyId}/customDimensions
Content-Type: application/json

{
  "parameterName": "user_type",
  "displayName": "User Type",
  "scope": "USER"
}
```

### 转换事件

```bash
GET /google-analytics-admin/v1beta/properties/{propertyId}/conversionEvents
POST /google-analytics-admin/v1beta/properties/{propertyId}/conversionEvents
```

## Data API 参考

### 运行报告

```bash
POST /google-analytics-data/v1beta/properties/{propertyId}:runReport
Content-Type: application/json

{
  "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
  "dimensions": [{"name": "city"}],
  "metrics": [{"name": "activeUsers"}]
}
```

### 运行实时报告

```bash
POST /google-analytics-data/v1beta/properties/{propertyId}:runRealtimeReport
Content-Type: application/json

{
  "dimensions": [{"name": "country"}],
  "metrics": [{"name": "activeUsers"}]
}
```

### 批量运行报告

```bash
POST /google-analytics-data/v1beta/properties/{propertyId}:batchRunReports
Content-Type: application/json

{
  "requests": [
    {
      "dateRanges": [{"startDate": "7daysAgo", "endDate": "today"}],
      "dimensions": [{"name": "country"}],
      "metrics": [{"name": "sessions"}]
    }
  ]
}
```

### 获取元数据

```bash
GET /google-analytics-data/v1beta/properties/{propertyId}/metadata
```

## 常见报告示例

### 按页面查看页面浏览量

```json
{
  "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
  "dimensions": [{"name": "pagePath"}],
  "metrics": [{"name": "screenPageViews"}],
  "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": true}],
  "limit": 10
}
```

### 按国家查看用户

```json
{
  "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
  "dimensions": [{"name": "country"}],
  "metrics": [{"name": "activeUsers"}, {"name": "sessions"}]
}
```

### 流量来源

```json
{
  "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
  "dimensions": [{"name": "sessionSource"}, {"name": "sessionMedium"}],
  "metrics": [{"name": "sessions"}, {"name": "conversions"}]
}
```

## 常见维度

- `date`、`country`、`city`、`deviceCategory`
- `pagePath`、`pageTitle`、`landingPage`
- `sessionSource`、`sessionMedium`、`sessionCampaignName`

## 常见指标

- `activeUsers`、`newUsers`、`sessions`
- `screenPageViews`、`bounceRate`、`averageSessionDuration`
- `conversions`、`eventCount`

## 日期格式

- 相对日期：`today`、`yesterday`、`7daysAgo`、`30daysAgo`
- 绝对日期：`2026-01-01`

## 代码示例

### JavaScript

```javascript
// List account summaries (Admin API)
const accounts = await fetch(
  'https://gateway.maton.ai/google-analytics-admin/v1beta/accountSummaries',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);

// Run a report (Data API)
const report = await fetch(
  'https://gateway.maton.ai/google-analytics-data/v1beta/properties/123456:runReport',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({
      dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
      dimensions: [{ name: 'country' }],
      metrics: [{ name: 'activeUsers' }]
    })
  }
);
```

### Python

```python
import os
import requests

# List account summaries (Admin API)
accounts = requests.get(
    'https://gateway.maton.ai/google-analytics-admin/v1beta/accountSummaries',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)

# Run a report (Data API)
report = requests.post(
    'https://gateway.maton.ai/google-analytics-data/v1beta/properties/123456:runReport',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={
        'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
        'dimensions': [{'name': 'country'}],
        'metrics': [{'name': 'activeUsers'}]
    }
)
```

## 注意事项

- 仅支持 GA4 属性（不支持 Universal Analytics）。
- 属性 ID 为数字格式（例如：`properties/521310447`）。
- 使用 `accountSummaries` 快速列出所有可访问的属性。
- 在 Admin API 中使用 `updateMask` 进行 PATCH 请求。
- 使用元数据端点来查看可用的维度/指标。
- **重要提示：** 当 URL 包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 可以避免全局解析问题。
- **重要提示：** 在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中 `$MATON_API_KEY` 可能无法正确解析，可能会导致 “Invalid API key” 错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 缺少 Google Analytics 连接 |
| 401 | API 密钥无效或缺失 |
| 429 | 每账户每秒请求次数限制（10 次） |
| 4xx/5xx | 来自 Google Analytics API 的传递错误 |

### 故障排除：API 密钥无效

**当收到 “Invalid API key” 错误时，请务必按照以下步骤进行排查：**

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

1. 确保您的 URL 路径以正确的应用名称开头：
   - 对于 Admin API：使用 `google-analytics-admin`
   - 对于 Data API：使用 `google-analytics-data`
   - 正确示例：`https://gateway.maton.ai/google-analytics-admin/v1beta/accountSummaries`
   - 错误示例：`https://gateway.maton.ai/analytics/v1beta/accountSummaries`

## 资源

- [Admin API 概述](https://developers.google.com/analytics/devguides/config/admin/v1)
- [账户](https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1betaaccounts)
- [属性](https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1beta/properties)
- [数据流](https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1beta/properties.dataStreams)
- [Data API 概述](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [运行报告](https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport)
- [实时报告](https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runRealtimeReport)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)