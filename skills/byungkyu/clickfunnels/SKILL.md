---
name: clickfunnels
description: |
  ClickFunnels API integration with managed OAuth. Manage contacts, products, orders, courses, forms, and webhooks.
  Use this skill when users want to create sales funnels, manage contacts, process orders, or build marketing automation.
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

# ClickFunnels

通过管理的OAuth认证来访问ClickFunnels 2.0 API。您可以管理联系人、产品、订单、课程、表单、Webhook等资源。

## 快速入门

```bash
# List teams
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clickfunnels/api/v2/teams')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('User-Agent', 'Maton/1.0')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基础URL

```
https://gateway.maton.ai/clickfunnels/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的ClickFunnels API端点路径。该网关会将请求代理到 `{subdomain}.myclickfunnels.com` 并自动插入您的OAuth令牌。

## 认证

所有请求都需要在 `Authorization` 头中包含 Maton API 密钥，以及 `User-Agent` 头：

```
Authorization: Bearer $MATON_API_KEY
User-Agent: Maton/1.0
```

**环境变量：** 将您的API密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的ClickFunnels OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=clickfunnels&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'clickfunnels'}).encode()
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
    "app": "clickfunnels",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成OAuth认证。

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

如果您有多个ClickFunnels连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clickfunnels/api/v2/teams')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('User-Agent', 'Maton/1.0')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略该头，网关将使用默认的（最旧的）活动连接。

## API参考

### 团队

#### 列出团队

```bash
GET /clickfunnels/api/v2/teams
```

**响应：**
```json
[
  {
    "id": 412840,
    "public_id": "vPNqAp",
    "name": "My Team",
    "time_zone": "Pacific Time (US & Canada)",
    "locale": "en",
    "created_at": "2026-02-07T09:28:29.709Z",
    "updated_at": "2026-02-07T11:14:32.118Z"
  }
]
```

#### 获取团队信息

```bash
GET /clickfunnels/api/v2/teams/{team_id}
```

### 工作空间

#### 列出工作空间

```bash
GET /clickfunnels/api/v2/teams/{team_id}/workspaces
```

**响应：**
```json
[
  {
    "id": 435231,
    "public_id": "JZqWGb",
    "team_id": 412840,
    "name": "My Workspace",
    "subdomain": "myworkspace",
    "created_at": "2026-02-07T09:28:31.268Z",
    "updated_at": "2026-02-07T09:28:34.498Z"
  }
]
```

#### 获取工作空间信息

```bash
GET /clickfunnels/api/v2/workspaces/{workspace_id}
```

### 联系人

#### 列出联系人

```bash
GET /clickfunnels/api/v2/workspaces/{workspace_id}/contacts
```

支持过滤：

```bash
GET /clickfunnels/api/v2/workspaces/{workspace_id}/contacts?filter[email_address]=user@example.com
```

**响应：**
```json
[
  {
    "id": 1087091674,
    "public_id": "PWzmxEx",
    "workspace_id": 435231,
    "email_address": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": null,
    "time_zone": null,
    "uuid": "eb7a970c-727d-4c82-9209-bd8f7457a801",
    "tags": [],
    "custom_attributes": {},
    "created_at": "2026-02-07T09:28:52.713Z",
    "updated_at": "2026-02-07T09:28:52.777Z"
  }
]
```

#### 获取联系人信息

```bash
GET /clickfunnels/api/v2/contacts/{contact_id}
```

#### 创建联系人

```bash
POST /clickfunnels/api/v2/workspaces/{workspace_id}/contacts
Content-Type: application/json

{
  "contact": {
    "email_address": "newuser@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "phone_number": "+1234567890"
  }
}
```

#### 更新联系人信息

```bash
PUT /clickfunnels/api/v2/contacts/{contact_id}
Content-Type: application/json

{
  "contact": {
    "first_name": "Updated Name",
    "phone_number": "+1987654321"
  }
}
```

#### 删除联系人

```bash
DELETE /clickfunnels/api/v2/contacts/{contact_id}
```

成功时返回HTTP 204状态码。

#### 更新联系人信息（根据电子邮件地址）

```bash
POST /clickfunnels/api/v2/workspaces/{workspace_id}/contacts/upsert
Content-Type: application/json

{
  "contact": {
    "email_address": "user@example.com",
    "first_name": "Updated"
  }
}
```

#### 遵守GDPR规定（隐藏联系人信息）

```bash
DELETE /clickfunnels/api/v2/workspaces/{workspace_id}/contacts/{contact_id}/gdpr_destroy
```

### 产品

#### 列出产品

```bash
GET /clickfunnels/api/v2/workspaces/{workspace_id}/products
```

**响应：**
```json
[
  {
    "id": 962732,
    "public_id": "jAvBEA",
    "workspace_id": 435231,
    "name": "My Product",
    "current_path": "/my-product",
    "archived": false,
    "visible_in_store": true,
    "visible_in_customer_center": true,
    "default_variant_id": 5361073,
    "variant_ids": [5361073],
    "price_ids": [],
    "tag_ids": [],
    "created_at": "2026-02-09T07:23:02.158Z",
    "updated_at": "2026-02-09T07:23:02.163Z"
  }
]
```

#### 获取产品信息

```bash
GET /clickfunnels/api/v2/products/{product_id}
```

#### 创建产品

```bash
POST /clickfunnels/api/v2/workspaces/{workspace_id}/products
Content-Type: application/json

{
  "product": {
    "name": "New Product",
    "visible_in_store": true,
    "visible_in_customer_center": true
  }
}
```

#### 更新产品信息

```bash
PUT /clickfunnels/api/v2/products/{product_id}
Content-Type: application/json

{
  "product": {
    "name": "Updated Product Name"
  }
}
```

#### 将产品归档

```bash
POST /clickfunnels/api/v2/products/{product_id}/archive
```

#### 取消产品归档

```bash
POST /clickfunnels/api/v2/products/{product_id}/unarchive
```

### 订单

#### 列出订单

```bash
GET /clickfunnels/api/v2/workspaces/{workspace_id}/orders
```

#### 获取订单信息

```bash
GET /clickfunnels/api/v2/orders/{order_id}
```

#### 更新订单信息

```bash
PUT /clickfunnels/api/v2/orders/{order_id}
Content-Type: application/json

{
  "order": {
    "notes": "Updated order notes"
  }
}
```

### 履行情况

#### 列出订单履行情况

```bash
GET /clickfunnels/api/v2/workspaces/{workspace_id}/fulfillments
```

#### 获取订单履行信息

```bash
GET /clickfunnels/api/v2/fulfillments/{fulfillment_id}
```

#### 创建订单履行记录

```bash
POST /clickfunnels/api/v2/workspaces/{workspace_id}/fulfillments
Content-Type: application/json

{
  "fulfillment": {
    "contact_id": 1087091674,
    "location_id": 12345,
    "tracking_url": "https://tracking.example.com/123",
    "shipping_provider": "ups",
    "tracking_code": "1Z999AA10123456784",
    "notify_customer": true
  }
}
```

#### 取消订单履行

```bash
POST /clickfunnels/api/v2/fulfillments/{fulfillment_id}/cancel
```

### 课程

#### 列出课程

```bash
GET /clickfunnels/api/v2/workspaces/{workspace_id}/courses
```

#### 获取课程信息

```bash
GET /clickfunnels/api/v2/courses/{course_id}
```

### 注册信息

#### 列出注册记录

```bash
GET /clickfunnels/api/v2/courses/{course_id}/enrollments
```

#### 创建注册记录

```bash
POST /clickfunnels/api/v2/courses/{course_id}/enrollments
Content-Type: application/json

{
  "courses_enrollment": {
    "contact_id": 1087091674
  }
}
```

#### 更新注册记录

```bash
PUT /clickfunnels/api/v2/courses/{course_id}/enrollments/{enrollment_id}
Content-Type: application/json

{
  "courses_enrollment": {
    "suspended": true,
    "suspension_reason": "Payment failed"
  }
}
```

### 表单

#### 列出表单

```bash
GET /clickfunnels/api/v2/workspaces/{workspace_id}/forms
```

**响应：**
```json
[
  {
    "id": 442896,
    "public_id": "NdOxzL",
    "workspace_id": 435231,
    "name": "Contact Form",
    "created_at": "2026-02-07T09:28:33.316Z",
    "updated_at": "2026-02-07T09:28:33.316Z"
  }
]
```

#### 获取表单信息

```bash
GET /clickfunnels/api/v2/forms/{form_id}
```

#### 列出表单提交记录

```bash
GET /clickfunnels/api/v2/forms/{form_id}/submissions
```

### 图片

#### 列出图片

```bash
GET /clickfunnels/api/v2/workspaces/{workspace_id}/images
```

**响应：**
```json
[
  {
    "id": 20670308,
    "public_id": "mvvWWM",
    "url": "https://statics.myclickfunnels.com/workspace/JZqWGb/image/20670308/file/image.png",
    "workspace_id": 435231,
    "alt_text": null,
    "name": null,
    "created_at": "2026-02-07T09:28:40.102Z",
    "updated_at": "2026-02-07T09:29:01.697Z"
  }
]
```

#### 通过URL创建图片

```bash
POST /clickfunnels/api/v2/workspaces/{workspace_id}/images
Content-Type: application/json

{
  "image": {
    "upload_source_url": "https://example.com/image.png"
  }
}
```

### Webhook

#### 列出Webhook端点

```bash
GET /clickfunnels/api/v2/workspaces/{workspace_id}/webhooks/outgoing/endpoints
```

**响应：**
```json
[
  {
    "id": 96677,
    "public_id": "vBZlEl",
    "workspace_id": 435231,
    "url": "https://example.com/webhook",
    "name": "My Webhook",
    "event_type_ids": ["contact.created"],
    "api_version": 2,
    "webhook_secret": "e779d4b2faa7d986...",
    "created_at": "2026-02-09T07:23:22.295Z",
    "updated_at": "2026-02-09T07:23:22.295Z"
  }
]
```

#### 创建Webhook端点

```bash
POST /clickfunnels/api/v2/workspaces/{workspace_id}/webhooks/outgoing/endpoints
Content-Type: application/json

{
  "webhooks_outgoing_endpoint": {
    "url": "https://example.com/webhook",
    "name": "New Webhook",
    "event_type_ids": ["contact.created", "order.created"]
  }
}
```

#### 获取Webhook端点信息

```bash
GET /clickfunnels/api/v2/webhooks/outgoing/endpoints/{endpoint_id}
```

#### 更新Webhook端点信息

```bash
PUT /clickfunnels/api/v2/webhooks/outgoing/endpoints/{endpoint_id}
Content-Type: application/json

{
  "webhooks_outgoing_endpoint": {
    "name": "Updated Webhook",
    "event_type_ids": ["contact.created", "contact.updated"]
  }
}
```

#### 删除Webhook端点

```bash
DELETE /clickfunnels/api/v2/webhooks/outgoing/endpoints/{endpoint_id}
```

成功时返回HTTP 204状态码。

## 分页

ClickFunnels使用基于游标的分页机制。每个列表端点最多返回20个条目。

可以使用 `after` 参数和最后一个条目的ID来获取下一页：

```bash
GET /clickfunnels/api/v2/workspaces/{workspace_id}/contacts?after=1087091674
```

**响应头：**

- `Pagination-Next`：最后一个条目的ID（用于获取下一页）
- `Link`：下一页的完整URL

分页示例流程：

```bash
# First page
GET /clickfunnels/api/v2/workspaces/{workspace_id}/images

# Response header: Pagination-Next: 20670327

# Next page
GET /clickfunnels/api/v2/workspaces/{workspace_id}/images?after=20670327
```

## 过滤

使用 `filter` 查询参数来过滤列表结果：

```bash
# Filter by email
GET /clickfunnels/api/v2/workspaces/{workspace_id}/contacts?filter[email_address]=user@example.com

# Filter by multiple emails (OR)
GET /clickfunnels/api/v2/workspaces/{workspace_id}/contacts?filter[email_address]=user1@example.com,user2@example.com

# Multiple filters (AND)
GET /clickfunnels/api/v2/workspaces/{workspace_id}/contacts?filter[email_address]=user@example.com&filter[id]=1087091674
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/clickfunnels/api/v2/teams',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'User-Agent': 'Maton/1.0'
    }
  }
);
const teams = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/clickfunnels/api/v2/teams',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'User-Agent': 'Maton/1.0'
    }
)
teams = response.json()
```

### 创建联系人的示例

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/clickfunnels/api/v2/workspaces/435231/contacts',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json',
        'User-Agent': 'Maton/1.0'
    },
    json={
        'contact': {
            'email_address': 'newuser@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith'
        }
    }
)
contact = response.json()
```

## 注意事项

- 团队ID、工作空间ID和资源ID都是整数。
- 每个资源都有一个 `public_id`（字符串），用于生成公开访问的URL。
- 列表端点默认每页返回最多20个条目。
- 使用 `after` 参数进行分页。
- 删除操作会返回HTTP 204状态码，并且响应内容为空。
- 请求体使用嵌套的资源键（例如：`{"contact": {...}}`）。
- 图片的最大大小为10MB，最大尺寸为10,000 x 10,000像素。
- 支持的图片格式：JPEG、PNG、WebP、GIF、SVG。
- 重要提示：当使用curl命令时，如果URL包含括号，请使用 `curl -g` 以避免glob解析。
- 重要提示：当将curl输出传递给 `jq` 或其他命令时，在某些shell环境中环境变量（如 `$MATON_API_KEY`）可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立ClickFunnels连接 |
| 401 | Maton API密钥无效或缺失 |
| 404 | 资源未找到 |
| 422 | 验证错误（请检查响应内容） |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自ClickFunnels API的传递错误 |

### 故障排除：API密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证API密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称无效

1. 确保您的URL路径以 `clickfunnels` 开头。例如：
- 正确：`https://gateway.maton.ai/clickfunnels/api/v2/teams`
- 错误：`https://gateway.maton.ai/api/v2/teams`

## 资源

- [ClickFunnels API简介](https://developers.myclickfunnels.com/docs/intro)
- [ClickFunnels API参考](https://developers.myclickfunnels.com/reference)
- [分页指南](https://developers.myclickfunnels.com/docs/pagination)
- [过滤指南](https://developers.myclickfunnels.com/docs/filtering)
- [Webhook概述](https://developers.myclickfunnels.com/docs/webhooks-overview)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)