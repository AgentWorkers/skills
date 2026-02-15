---
name: apollo
description: |
  Apollo.io API integration with managed OAuth. Search and enrich people and companies, manage contacts and accounts. Use this skill when users want to prospect, enrich leads, or manage sales data. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Apollo

您可以使用托管的 OAuth 认证来访问 Apollo.io API。该 API 可用于搜索人员和组织、丰富联系人信息以及管理销售流程。

## 快速入门

```bash
# Search for people at a company
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'q_organization_name': 'Google', 'per_page': 10}).encode()
req = urllib.request.Request('https://gateway.maton.ai/apollo/v1/mixed_people/api_search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/apollo/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Apollo API 端点路径。该网关会将请求代理到 `api.apollo.io` 并自动插入您的 API 密钥。

## 认证

所有请求都必须在 `Authorization` 标头中包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 管理您的 Apollo 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=apollo&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'apollo'}).encode()
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
    "app": "apollo",
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

如果您有多个 Apollo 连接，请使用 `Maton-Connection` 标头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'q_organization_name': 'Google', 'per_page': 10}).encode()
req = urllib.request.Request('https://gateway.maton.ai/apollo/v1/mixed_people/api_search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略该字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 人员

#### 搜索人员

```bash
POST /apollo/v1/mixed_people/api_search
Content-Type: application/json

{
  "q_organization_name": "Google",
  "page": 1,
  "per_page": 25
}
```

#### 通过电子邮件丰富人员信息

```bash
POST /apollo/v1/people/match
Content-Type: application/json

{
  "email": "john@example.com"
}
```

#### 通过 LinkedIn 丰富人员信息

```bash
POST /apollo/v1/people/match
Content-Type: application/json

{
  "linkedin_url": "https://linkedin.com/in/johndoe"
}
```

### 组织

#### 搜索组织

```bash
POST /apollo/v1/organizations/search
Content-Type: application/json

{
  "q_organization_name": "Google",
  "page": 1,
  "per_page": 25
}
```

#### 丰富组织信息

```bash
POST /apollo/v1/organizations/enrich
Content-Type: application/json

{
  "domain": "google.com"
}
```

### 联系人

#### 搜索联系人

```bash
POST /apollo/v1/contacts/search
Content-Type: application/json

{
  "page": 1,
  "per_page": 25
}
```

#### 创建联系人

```bash
POST /apollo/v1/contacts
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "organization_name": "Acme Corp"
}
```

#### 更新联系人信息

```bash
PUT /apollo/v1/contacts/{contactId}
Content-Type: application/json

{
  "first_name": "Jane"
}
```

### 账户

#### 搜索账户

```bash
POST /apollo/v1/accounts/search
Content-Type: application/json

{
  "page": 1,
  "per_page": 25
}
```

#### 创建账户

```bash
POST /apollo/v1/accounts
Content-Type: application/json

{
  "name": "Acme Corp",
  "domain": "acme.com"
}
```

### 序列

#### 搜索序列

```bash
POST /apollo/v1/emailer_campaigns/search
Content-Type: application/json

{
  "page": 1,
  "per_page": 25
}
```

#### 将联系人添加到序列中

```bash
POST /apollo/v1/emailer_campaigns/{campaignId}/add_contact_ids
Content-Type: application/json

{
  "contact_ids": ["contact_id_1", "contact_id_2"]
}
```

### 标签

#### 列出标签

```bash
GET /apollo/v1/labels
```

## 搜索过滤器

常见的搜索参数：
- `q_organization_name` - 公司名称
- `q_person_title` - 职位
- `person_locations` - 地点数组
- `organization_num_employees_ranges` - 员工数量范围
- `q_keywords` - 通用关键词搜索

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/apollo/v1/mixed_people/api_search',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({
      q_organization_name: 'Google',
      per_page: 10
    })
  }
);
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/apollo/v1/mixed_people/api_search',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={'q_organization_name': 'Google', 'per_page': 10}
)
```

## 注意事项

- 分页使用 POST 请求中的 `page` 和 `per_page` 参数。
- 大多数列表端点使用带有 `/search` 后缀的 POST 请求。
- 通过电子邮件丰富联系人信息会消耗信用额度。
- `people/search` 和 `mixed_people/search` 已被弃用，请使用 `mixed_people/api_search`。
- 重要提示：当 URL 中包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 可以避免全局解析问题。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境可能无法正确解析环境变量 `$MATON_API_KEY`，这可能导致 “无效 API 密钥” 错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Apollo 连接 |
| 401 | API 密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（每秒 10 次） |
| 4xx/5xx | 来自 Apollo API 的传递错误 |

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

1. 确保您的 URL 路径以 `apollo` 开头。例如：
- 正确：`https://gateway.maton.ai/apollo/v1/mixed_people/api_search`
- 错误：`https://gateway.maton.ai/v1/mixed_people/api_search`

## 资源

- [Apollo API 概述](https://docs.apollo.io/reference/introduction)
- [搜索人员](https://docs.apollo.io/reference/people-api-search.md)
- [丰富人员信息](https://docs.apollo.io/reference/people-enrichment.md)
- [搜索组织](https://docs.apollo.io/reference/organization-search.md)
- [丰富组织信息](https://docs.apollo.io/reference/organization-enrichment.md)
- [创建联系人](https://docs.apollo.io/reference/create-a-contact.md)
- [LLM 参考](https://docs.apollo.io/llms.txt)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)