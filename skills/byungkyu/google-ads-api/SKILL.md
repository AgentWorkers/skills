---
name: google-ads
description: |
  Google Ads API integration with managed OAuth. Query campaigns, ad groups, keywords, and performance metrics with GAQL. Use this skill when users want to interact with Google Ads data. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# 谷歌广告（Google Ads）

通过管理的 OAuth 认证来访问谷歌广告 API。可以使用 GAQL 查询广告活动（campaigns）、广告组（ad groups）、关键词（keywords）以及性能指标（performance metrics）。

## 快速入门

```bash
# List accessible customers
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-ads/v23/customers:listAccessibleCustomers')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/google-ads/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的谷歌广告 API 端点路径。该网关会将请求代理到 `googleads.googleapis.com`，并自动插入 OAuth 令牌和开发者令牌。

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

您可以在 `https://ctrl.maton.ai` 管理您的谷歌广告 OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-ads&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-ads'}).encode()
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
    "app": "google-ads",
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

如果您有多个谷歌广告连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': 'SELECT campaign.id, campaign.name FROM campaign'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/google-ads/v23/customers/1234567890/googleAds:search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 列出可访问的客户

```bash
GET /google-ads/v23/customers:listAccessibleCustomers
```

### 搜索（GAQL 查询）

```bash
POST /google-ads/v23/customers/{customerId}/googleAds:search
Content-Type: application/json

{
  "query": "SELECT campaign.id, campaign.name, campaign.status FROM campaign ORDER BY campaign.id"
}
```

### 搜索流（用于处理大量结果）

```bash
POST /google-ads/v23/customers/{customerId}/googleAds:searchStream
Content-Type: application/json

{
  "query": "SELECT campaign.id, campaign.name FROM campaign"
}
```

## 常用 GAQL 查询

### 列出广告活动

```sql
SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type
FROM campaign
WHERE campaign.status != 'REMOVED'
ORDER BY campaign.name
```

### 广告活动性能

```sql
SELECT campaign.id, campaign.name, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.impressions DESC
```

### 列出广告组

```sql
SELECT ad_group.id, ad_group.name, ad_group.status, campaign.id, campaign.name
FROM ad_group
WHERE ad_group.status != 'REMOVED'
```

### 列出关键词

```sql
SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, metrics.impressions, metrics.clicks
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS
```

## 代码示例

### JavaScript

```javascript
// Get customer IDs
const customers = await fetch(
  'https://gateway.maton.ai/google-ads/v23/customers:listAccessibleCustomers',
  { headers: { 'Authorization': `Bearer ${process.env.MATON_API_KEY}` } }
).then(r => r.json());

// Query campaigns
const campaigns = await fetch(
  `https://gateway.maton.ai/google-ads/v23/customers/${customerId}/googleAds:search`,
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({
      query: 'SELECT campaign.id, campaign.name FROM campaign'
    })
  }
).then(r => r.json());
```

### Python

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}

# Query campaigns
response = requests.post(
    f'https://gateway.maton.ai/google-ads/v23/customers/{customer_id}/googleAds:search',
    headers=headers,
    json={'query': 'SELECT campaign.id, campaign.name FROM campaign'}
)
```

## 注意事项

- 首先使用 `listAccessibleCustomers` 获取客户 ID。
- 客户 ID 是 10 位数字（请删除破折号）。
- 货币值以微秒（micros）为单位（需除以 1,000,000）。
- 日期范围：`LAST_7_DAYS`、`LAST_30_days`、`THIS_MONTH`。
- 状态值：`ENABLED`、`PAUSED`、`REMOVED`。
- 重要提示：当 URL 包含方括号（`fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 可以避免全局解析问题。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境可能无法正确解析环境变量 `$MATON_API_KEY`，这可能导致 “无效 API 密钥” 错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 缺少谷歌广告连接 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（每秒 10 次） |
| 4xx/5xx | 来自谷歌广告 API 的传递错误 |

### 故障排除：API 密钥问题

1. 确保已设置 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证 API 密钥的有效性：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用程序名称无效

1. 确保您的 URL 路径以 `google-ads` 开头。例如：
- 正确格式：`https://gateway.maton.ai/google-ads/v23/customers:listAccessibleCustomers`
- 错误格式：`https://gateway.maton.ai/v23/customers:listAccessibleCustomers`

## 资源

- [谷歌广告 API 概述](https://developers.google.com/google-ads/api/docs/start)
- [GAQL 参考](https://developers.google.com/google-ads/api/docs/query/overview)
- [指标参考](https://developers.google.com/google-ads/api/fields/v23/metrics)
- [搜索功能](https://developers.google.com/google-ads/api/reference/rpc/v23/GoogleAdsService/Search)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)