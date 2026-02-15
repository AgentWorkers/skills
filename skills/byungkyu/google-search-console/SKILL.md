---
name: google-search-console
description: |
  Google Search Console API integration with managed OAuth. Query search analytics, manage sitemaps, and monitor site performance. Use this skill when users want to access Search Console data. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Google Search Console

您可以使用托管的 OAuth 认证来访问 Google Search Console API。该 API 允许您查询搜索分析数据、管理站点地图，并监控网站在 Google 搜索中的表现。

## 快速入门

```bash
# List sites
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-search-console/webmasters/v3/sites')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/google-search-console/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Google Search Console API 端点路径。该网关会将请求代理到 `www.googleapis.com` 并自动插入您的 OAuth 令牌。

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Google OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-search-console&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-search-console'}).encode()
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
    "app": "google-search-console",
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

如果您有多个 Google Search Console 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-search-console/webmasters/v3/sites')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 站点

```bash
GET /google-search-console/webmasters/v3/sites
GET /google-search-console/webmasters/v3/sites/{siteUrl}
```

注意：站点 URL 必须进行 URL 编码（例如：`https%3A%2F%2Fexample.com%2F`）。

### 搜索分析

```bash
POST /google-search-console/webmasters/v3/sites/{siteUrl}/searchAnalytics/query
Content-Type: application/json

{
  "startDate": "2024-01-01",
  "endDate": "2024-01-31",
  "dimensions": ["query"],
  "rowLimit": 100
}
```

### 站点地图

```bash
GET /google-search-console/webmasters/v3/sites/{siteUrl}/sitemaps
PUT /google-search-console/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}
DELETE /google-search-console/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}
```

## 搜索分析示例

### 热门查询

```json
{
  "startDate": "2024-01-01",
  "endDate": "2024-01-31",
  "dimensions": ["query"],
  "rowLimit": 25
}
```

### 热门页面

```json
{
  "startDate": "2024-01-01",
  "endDate": "2024-01-31",
  "dimensions": ["page"],
  "rowLimit": 25
}
```

### 设备分布

```json
{
  "startDate": "2024-01-01",
  "endDate": "2024-01-31",
  "dimensions": ["device"],
  "rowLimit": 10
}
```

### 日常性能

```json
{
  "startDate": "2024-01-01",
  "endDate": "2024-01-31",
  "dimensions": ["date"],
  "rowLimit": 31
}
```

### 过滤查询

```json
{
  "startDate": "2024-01-01",
  "endDate": "2024-01-31",
  "dimensions": ["query"],
  "dimensionFilterGroups": [{
    "filters": [{
      "dimension": "query",
      "operator": "contains",
      "expression": "keyword"
    }]
  }],
  "rowLimit": 100
}
```

## 维度

- `query` - 搜索查询
- `page` - 页面 URL
- `country` - 国家代码
- `device` - 桌面、移动设备、平板电脑
- `date` - 日期

## 自动返回的指标

- `clicks` - 点击次数
- `impressions` - 展示次数
- `ctr` - 点击率
- `position` - 平均排名

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/google-search-console/webmasters/v3/sites/https%3A%2F%2Fexample.com/searchAnalytics/query',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({
      startDate: '2024-01-01',
      endDate: '2024-01-31',
      dimensions: ['query'],
      rowLimit: 25
    })
  }
);
```

### Python

```python
import os
import requests
from urllib.parse import quote

site_url = quote('https://example.com', safe='')
response = requests.post(
    f'https://gateway.maton.ai/google-search-console/webmasters/v3/sites/{site_url}/searchAnalytics/query',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={
        'startDate': '2024-01-01',
        'endDate': '2024-01-31',
        'dimensions': ['query'],
        'rowLimit': 25
    }
)
```

## 注意事项

- 站点 URL 必须在路径中进行 URL 编码。
- 日期范围限制为 16 个月。
- 每次请求最多返回 25,000 行数据。
- 使用 `startRow` 进行分页。
- 数据可能存在 2-3 天的延迟。
- 重要提示：当使用 `curl` 命令时，如果 URL 包含方括号（如 `fields[]`、`sort[]`、`records[]`），请使用 `curl -g` 以禁用全局解析。
- 重要提示：当将 `curl` 的输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确展开，这可能导致“无效 API 密钥”错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Google Search Console 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（10 次/秒） |
| 4xx/5xx | 来自 Google Search Console API 的传递错误 |

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

1. 确保您的 URL 路径以 `google-search-console` 开头。例如：
- 正确：`https://gateway.maton.ai/google-search-console/webmasters/v3/sites`
- 错误：`https://gateway.maton.ai/webmasters/v3/sites`

## 资源

- [Search Console API 参考](https://developers.google.com/webmaster-tools/v1/api_reference_index)
- [列出站点](https://developers.google.com/webmaster-tools/v1/sites/list)
- [搜索分析](https://developers.google.com/webmaster-tools/v1/searchanalytics/query)
- [站点地图](https://developers.google.com/webmaster-tools/v1/sitemaps)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)