---
name: beehiiv
description: |
  beehiiv API integration with managed OAuth. Manage newsletter publications, subscriptions, posts, custom fields, segments, and automations.
  Use this skill when users want to manage newsletter subscribers, create posts, organize segments, or integrate with beehiiv publications.
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

# beehiiv

通过管理的OAuth认证来访问beehiiv API。您可以管理新闻通讯的发布、订阅、帖子、自定义字段、用户群体（segments）、订阅层级（tiers）以及自动化流程（automations）。

## 快速入门

```bash
# List publications
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/beehiiv/v2/publications')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/beehiiv/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 beehiiv API 端点路径。该网关会将请求代理到 `api.beehiiv.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取您的 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的 beehiiv OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=beehiiv&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'beehiiv'}).encode()
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
    "connection_id": "8bfe17f4-0038-4cbd-afb4-907b1ffa9d66",
    "status": "ACTIVE",
    "creation_time": "2026-02-11T00:25:10.464852Z",
    "last_updated_time": "2026-02-11T00:27:00.816431Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "beehiiv",
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

如果您有多个 beehiiv 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/beehiiv/v2/publications')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '8bfe17f4-0038-4cbd-afb4-907b1ffa9d66')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

所有 beehiiv API 端点都遵循以下格式：

```
/beehiiv/v2/{resource}
```

---

## 新闻通讯（Publications）

### 列出新闻通讯

```bash
GET /beehiiv/v2/publications
```

**查询参数：**

| 参数 | 描述 |
|-----------|-------------|
| `limit` | 每页显示的结果数量（1-100，默认：10） |
| `page` | 页码（默认：1） |
| `expand[]` | 可扩展字段：`stats`, `stat_active_subscriptions`, `stat_average_open_rate` 等 |
| `order_by` | 排序方式：`created` 或 `name` |
| `direction` | 排序方向：`asc` 或 `desc` |

**响应：**
```json
{
  "data": [
    {
      "id": "pub_c6c521e4-91ac-4c14-8a52-06987b7e32f2",
      "name": "My Newsletter",
      "organization_name": "My Organization",
      "referral_program_enabled": true,
      "created": 1770767522
    }
  ],
  "page": 1,
  "limit": 10,
  "total_results": 1,
  "total_pages": 1
}
```

### 获取新闻通讯详情

```bash
GET /beehiiv/v2/publications/{publication_id}
```

---

## 订阅（Subscriptions）

### 列出订阅信息

```bash
GET /beehiiv/v2/publications/{publication_id}/subscriptions
```

**查询参数：**

| 参数 | 描述 |
|-----------|-------------|
| `limit` | 每页显示的结果数量（1-100，默认：10） |
| `cursor` | 分页游标（推荐使用） |
| `page` | 页码（已弃用，最多支持 100 页） |
| `email` | 按电子邮件过滤（不区分大小写） |
| `status` | 过滤状态：`validating`, `invalid`, `pending`, `active`, `inactive`, `all` |
| `tier` | 过滤层级：`free`, `premium`, `all` |
| `expand[]` | 可扩展字段：`stats`, `custom_fields`, `referrals` |
| `order_by` | 排序字段（默认：`created`） |
| `direction` | 排序方向：`asc` 或 `desc` |

**响应：**
```json
{
  "data": [
    {
      "id": "sub_c27d9640-f418-43a8-a0f9-528c20a05002",
      "email": "subscriber@example.com",
      "status": "active",
      "created": 1770767524,
      "subscription_tier": "free",
      "subscription_premium_tier_names": [],
      "utm_source": "direct",
      "utm_medium": "",
      "utm_channel": "website",
      "utm_campaign": "",
      "referring_site": "",
      "referral_code": "gBZbSVal1X",
      "stripe_customer_id": ""
    }
  ],
  "limit": 10,
  "has_more": false,
  "next_cursor": null
}
```

### 根据 ID 获取订阅信息

```bash
GET /beehiiv/v2/publications/{publication_id}/subscriptions/{subscription_id}
```

**查询参数：**

| 参数 | 描述 |
|-----------|-------------|
| `expand[]` | 可扩展字段：`stats`, `custom_fields`, `referrals`, `tags` |

### 根据电子邮件获取订阅信息

```bash
GET /beehiiv/v2/publications/{publication_id}/subscriptions/by_email/{email}
```

### 创建订阅

```bash
POST /beehiiv/v2/publications/{publication_id}/subscriptions
Content-Type: application/json

{
  "email": "newsubscriber@example.com",
  "utm_source": "api",
  "send_welcome_email": false,
  "reactivate_existing": false
}
```

**请求体：**

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `email` | string | 是 | 订阅者的电子邮件地址 |
| `reactivate_existing` | boolean | 否 | 是否重新激活已取消的订阅 |
| `send_welcome_email` | boolean | 否 | 是否发送欢迎邮件 |
| `utm_source` | string | 否 | UTM 来源（用于跟踪） |
| `utm_medium` | string | 否 | UTM 渠道 |
| `referring_site` | string | 否 | 推荐者的引用代码 |
| `custom_fields` | object | 否 | 自定义字段值（这些字段必须存在） |
| `double_opt_override` | string | 否 | 是否覆盖双重确认设置（`on` 或 `off`） |
| `tier` | string | 否 | 订阅层级 |
| `premium_tier_names` | array | 否 | 要分配的高级订阅层级名称 |

### 更新订阅信息

```bash
PATCH /beehiiv/v2/publications/{publication_id}/subscriptions/{subscription_id}
Content-Type: application/json

{
  "utm_source": "updated-source",
  "custom_fields": [
    {"name": "First Name", "value": "John"}
  ]
}
```

### 删除订阅

```bash
DELETE /beehiiv/v2/publications/{publication_id}/subscriptions/{subscription_id}
```

---

## 帖子（Posts）

### 列出帖子

```bash
GET /beehiiv/v2/publications/{publication_id}/posts
```

**查询参数：**

| 参数 | 描述 |
|-----------|-------------|
| `limit` | 每页显示的结果数量（1-100，默认：10） |
| `page` | 页码 |
| `status` | 按状态过滤 |
| `expand[]` | 可扩展字段 |

**响应：**
```json
{
  "data": [],
  "page": 1,
  "limit": 10,
  "total_results": 0,
  "total_pages": 0
}
```

### 获取帖子详情

```bash
GET /beehiiv/v2/publications/{publication_id}/posts/{post_id}
```

### 删除帖子

```bash
DELETE /beehiiv/v2/publications/{publication_id}/posts/{post_id}
```

---

## 自定义字段（Custom Fields）

### 列出自定义字段

```bash
GET /beehiiv/v2/publications/{publication_id}/custom_fields
```

**响应：**
```json
{
  "data": [
    {
      "id": "95c9653f-a1cf-45f0-a140-97feef19057b",
      "kind": "string",
      "display": "Last Name",
      "created": 1770767523
    },
    {
      "id": "4cfe081e-c89b-4da5-9c1a-52a4fb8ba69e",
      "kind": "string",
      "display": "First Name",
      "created": 1770767523
    }
  ],
  "page": 1,
  "limit": 10,
  "total_results": 2,
  "total_pages": 1
}
```

**字段类型：** `string`, `integer`, `boolean`, `date`, `datetime`, `list`, `double`

### 创建自定义字段

```bash
POST /beehiiv/v2/publications/{publication_id}/custom_fields
Content-Type: application/json

{
  "display": "Company",
  "kind": "string"
}
```

### 更新自定义字段

```bash
PATCH /beehiiv/v2/publications/{publication_id}/custom_fields/{custom_field_id}
Content-Type: application/json

{
  "display": "Company Name"
}
```

### 删除自定义字段

```bash
DELETE /beehiiv/v2/publications/{publication_id}/custom_fields/{custom_field_id}
```

---

## 用户群体（Segments）

### 列出用户群体

```bash
GET /beehiiv/v2/publications/{publication_id}/segments
```

**响应：**
```json
{
  "data": [],
  "page": 1,
  "limit": 10,
  "total_results": 0,
  "total_pages": 0
}
```

### 获取用户群体详情

```bash
GET /beehiiv/v2/publications/{publication_id}/segments/{segment_id}
```

### 删除用户群体

```bash
DELETE /beehiiv/v2/publications/{publication_id}/segments/{segment_id}
```

---

## 订阅层级（Tiers）

### 列出订阅层级

```bash
GET /beehiiv/v2/publications/{publication_id}/tiers
```

### 获取订阅层级详情

```bash
GET /beehiiv/v2/publications/{publication_id}/tiers/{tier_id}
```

### 创建订阅层级

```bash
POST /beehiiv/v2/publications/{publication_id}/tiers
Content-Type: application/json

{
  "name": "Premium",
  "description": "Premium tier with exclusive content"
}
```

### 更新订阅层级

```bash
PATCH /beehiiv/v2/publications/{publication_id}/tiers/{tier_id}
Content-Type: application/json

{
  "name": "Updated Tier Name"
}
```

---

## 自动化流程（Automations）

### 列出自动化流程

```bash
GET /beehiiv/v2/publications/{publication_id}/automations
```

### 获取自动化流程详情

```bash
GET /beehiiv/v2/publications/{publication_id}/automations/{automation_id}
```

---

## 推荐计划（Referral Program）

### 获取推荐计划信息

```bash
GET /beehiiv/v2/publications/{publication_id}/referral_program
```

---

## 分页

beehiiv 支持两种分页方式：

### 基于游标的分页（推荐使用）

```bash
GET /beehiiv/v2/publications/{publication_id}/subscriptions?limit=10&cursor={next_cursor}
```

**响应包含：**
```json
{
  "data": [...],
  "limit": 10,
  "has_more": true,
  "next_cursor": "eyJ0aW1lc3RhbXAiOiIyMDI0LTA3LTAyVDE3OjMwOjAwLjAwMDAwMFoifQ=="
}
```

使用 `next_cursor` 值进行后续请求。

### 基于页码的分页（已弃用）

```bash
GET /beehiiv/v2/publications?page=2&limit=10
```

**响应包含：**
```json
{
  "data": [...],
  "page": 2,
  "limit": 10,
  "total_results": 50,
  "total_pages": 5
}
```

**注意：** 基于页码的分页最多支持 100 页。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/beehiiv/v2/publications',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.data);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/beehiiv/v2/publications',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
for pub in data['data']:
    print(f"{pub['id']}: {pub['name']}")
```

## 注意事项

- 新闻通讯的 ID 以 `pub_` 开头。
- 订阅的 ID 以 `sub_` 开头。
- 时间戳为 Unix 时间戳（自纪元以来的秒数）。
- 在使用自定义字段之前，必须先创建它们。
- 建议使用基于游标的分页方式以获得更好的性能。
- 基于页码的分页已弃用，且最多支持 100 页。
- 重要提示：当 URL 中包含括号时，使用 `curl -g` 命令可以禁用全局解析。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中可能无法正确解析环境变量 `$MATON_API_KEY`。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求错误或参数无效 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 禁止访问 - 权限不足或计划限制 |
| 404 | 资源未找到 |
| 429 | 请求次数限制 |
| 500 | 服务器内部错误 |

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

### 故障排除：应用名称错误

1. 确保您的 URL 路径以 `beehiiv` 开头。例如：
- 正确格式：`https://gateway.maton.ai/beehiiv/v2/publications`
- 错误格式：`https://gateway.maton.ai/v2/publications`

## 资源

- [beehiiv 开发者文档](https://developers.beehiiv.com/)
- [beehiiv API 参考](https://developers.beehiiv.com/api-reference)
- [beehiiv 帮助中心](https://beehiivhelp.zendesk.com/)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持团队](mailto:support@maton.ai)