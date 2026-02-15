---
name: kit
description: |
  Kit (formerly ConvertKit) API integration with managed OAuth. Manage email subscribers, forms, tags, sequences, broadcasts, and custom fields.
  Use this skill when users want to manage their email marketing lists, create or update subscribers, manage tags, or work with email sequences and broadcasts.
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

# 套件（Kit）  

通过管理的 OAuth 认证方式访问套件（Kit，前身为 ConvertKit）API。您可以管理订阅者、标签、表单、序列（sequences）、广播（broadcasts）、自定义字段（custom fields）以及 Webhook。  

## 快速入门  

```bash
# List subscribers
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/kit/v4/subscribers?per_page=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```  

## 基本 URL  

```
https://gateway.maton.ai/kit/{native-api-path}
```  

请将 `{native-api-path}` 替换为实际的套件 API 端点路径。该网关会将请求代理到 `api.kit.com` 并自动插入您的 OAuth 令牌。  

## 认证  

所有请求都需要在 `Authorization` 头中包含 Maton API 密钥：  

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

您可以在 `https://ctrl.maton.ai` 管理您的套件 OAuth 连接。  

### 列出连接（List Connections）  

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=kit&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```  

### 创建连接（Create Connection）  

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'kit'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```  

### 获取连接（Get Connection）  

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
    "connection_id": "cb2025b3-706f-4b5d-87a5-c6809c0c7ec4",
    "status": "ACTIVE",
    "creation_time": "2026-02-07T00:04:08.476727Z",
    "last_updated_time": "2026-02-07T00:05:58.001964Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "kit",
    "metadata": {}
  }
}
```  

在浏览器中打开返回的 `url` 以完成 OAuth 认证。  

### 删除连接（Delete Connection）  

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```  

### 指定连接（Specify Connection）  

如果您有多个套件连接，请使用 `Maton-Connection` 头来指定要使用的连接：  

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/kit/v4/subscribers')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'cb2025b3-706f-4b5d-87a5-c6809c0c7ec4')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```  

如果省略此头，网关将使用默认的（最旧的）活动连接。  

## API 参考  

### 订阅者（Subscribers）  

#### 列出订阅者（List Subscribers）  

**查询参数：**  
- `per_page` - 每页显示的结果数量（默认：500，最大：1000）  
- `after` - 下一页的游标  
- `before` - 上一页的游标  
- `status` - 过滤条件：`active`（活动）、`inactive`（非活动）、`bounced`（被拒绝）、`complained`（投诉）、`cancelled`（已取消）或 `all`  
- `email_address` - 按特定电子邮件地址过滤  
- `created_after` / `created_before` - 按创建日期过滤（格式：yyyy-mm-dd）  
- `updated_after` / `updated_before` - 按更新日期过滤（格式：yyyy-mm-dd）  
- `include_total_count` - 是否包含总数（此操作较慢）  

**响应：**  
```json
{
  "subscribers": [
    {
      "id": 3914682852,
      "first_name": "Test User",
      "email_address": "test@example.com",
      "state": "active",
      "created_at": "2026-02-07T00:42:54Z",
      "fields": {"company": null}
    }
  ],
  "pagination": {
    "has_previous_page": false,
    "has_next_page": false,
    "start_cursor": "WzE0OV0=",
    "end_cursor": "WzE0OV0=",
    "per_page": 500
  }
}
```  

#### 获取订阅者信息（Get Subscriber Information）  

```bash
GET /kit/v4/subscribers/{id}
```  

#### 创建订阅者（Create Subscriber）  

```bash
POST /kit/v4/subscribers
Content-Type: application/json

{
  "email_address": "user@example.com",
  "first_name": "John"
}
```  

#### 更新订阅者信息（Update Subscriber Information）  

```bash
PUT /kit/v4/subscribers/{id}
Content-Type: application/json

{
  "first_name": "Updated Name"
}
```  

### 标签（Tags）  

#### 列出标签（List Tags）  

**查询参数：**  
- `per_page`、`after`、`before`、`include_total_count`  

#### 创建标签（Create Tag）  

```bash
POST /kit/v4/tags
Content-Type: application/json

{
  "name": "new-tag"
}
```  

**响应：**  
```json
{
  "tag": {
    "id": 15690016,
    "name": "new-tag",
    "created_at": "2026-02-07T00:42:53Z"
  }
}
```  

#### 更新标签信息（Update Tag Information）  

```bash
PUT /kit/v4/tags/{id}
Content-Type: application/json

{
  "name": "updated-tag-name"
}
```  

#### 删除标签（Delete Tag）  

**响应：**  
成功时返回 204（No Content）。  

#### 为订阅者添加标签（Tag a Subscriber）  

```bash
POST /kit/v4/tags/{tag_id}/subscribers
Content-Type: application/json

{
  "email_address": "user@example.com"
}
```  

#### 从订阅者中移除标签（Remove Tag from Subscriber）  

**响应：**  
成功时返回 204（No Content）。  

#### 列出带有标签的订阅者（List Subscribers with Tag）  

```bash
GET /kit/v4/tags/{tag_id}/subscribers
```  

### 表单（Forms）  

#### 列出表单（List Forms）  

**查询参数：**  
- `per_page`、`after`、`before`、`include_total_count`  
- `status` - 过滤条件：`active`（活动）、`archived`（已归档）、`trashed`（已删除）或 `all`  
- `type` - `embed`（嵌入式表单）或 `hosted`（ landing 页面使用的表单）  

**响应：**  
```json
{
  "forms": [
    {
      "id": 9061198,
      "name": "Creator Profile",
      "created_at": "2026-02-07T00:00:32Z",
      "type": "embed",
      "format": null,
      "embed_js": "https://chris-kim-2.kit.com/c682763b07/index.js",
      "embed_url": "https://chris-kim-2.kit.com/c682763b07",
      "archived": false,
      "uid": "c682763b07"
    }
  ],
  "pagination": {...}
}
```  

#### 将订阅者添加到表单（Add Subscriber to Form）  

```bash
POST /kit/v4/forms/{form_id}/subscribers
Content-Type: application/json

{
  "email_address": "user@example.com"
}
```  

#### 列出表单的订阅者（List Form Subscribers）  

```bash
GET /kit/v4/forms/{form_id}/subscribers
```  

### 序列（Sequences）  

#### 列出序列（List Sequences）  

**响应：**  
```bash
GET /kit/v4/sequences
```  

#### 将订阅者添加到序列（Add Subscriber to Sequence）  

```bash
POST /kit/v4/sequences/{sequence_id}/subscribers
Content-Type: application/json

{
  "email_address": "user@example.com"
}
```  

#### 列出序列的订阅者（List Sequence Subscribers）  

```bash
GET /kit/v4/sequences/{sequence_id}/subscribers
```  

### 广播（Broadcasts）  

#### 列出广播（List Broadcasts）  

**查询参数：**  
- `per_page`、`after`、`before`、`include_total_count`  

**响应：**  
```json
{
  "broadcasts": [
    {
      "id": 123,
      "publication_id": 456,
      "created_at": "2026-02-07T00:00:00Z",
      "subject": "My Broadcast",
      "preview_text": "Preview...",
      "content": "<p>Content</p>",
      "public": false,
      "published_at": null,
      "send_at": null,
      "email_template": {"id": 123, "name": "Text only"}
    }
  ],
  "pagination": {...}
}
```  

### 分段（Segments）  

#### 列出分段（List Segments）  

**查询参数：**  
- `per_page`、`after`、`before`、`include_total_count`  

### 自定义字段（Custom Fields）  

#### 列出自定义字段（List Custom Fields）  

**响应：**  
```bash
GET /kit/v4/custom_fields
```  

#### 创建自定义字段（Create Custom Field）  

```bash
POST /kit/v4/custom_fields
Content-Type: application/json

{
  "label": "Company"
}
```  

#### 更新自定义字段（Update Custom Field）  

```bash
PUT /kit/v4/custom_fields/{id}
Content-Type: application/json

{
  "label": "Company Name"
}
```  

#### 删除自定义字段（Delete Custom Field）  

**响应：**  
成功时返回 204（No Content）。  

### 购买记录（Purchases）  

#### 列出购买记录（List Purchases）  

**查询参数：**  
- `per_page`、`after`、`before`、`include_total_count`  

### 电子邮件模板（Email Templates）  

#### 列出电子邮件模板（List Email Templates）  

**响应：**  
```json
{
  "email_templates": [
    {
      "id": 4956167,
      "name": "Text only",
      "is_default": true,
      "category": "Classic"
    }
  ],
  "pagination": {...}
}
```  

### Webhook  

#### 列出 Webhook（List Webhooks）  

**响应：**  
```bash
GET /kit/v4/webhooks
```  

#### 创建 Webhook（Create Webhook）  

**响应：**  
```json
{
  "webhook": {
    "id": 5291560,
    "account_id": 2596262,
    "event": {
      "name": "subscriber_activate",
      "initiator_value": null
    },
    "target_url": "https://example.com/webhook"
  }
}
```  

#### 删除 Webhook（Delete Webhook）  

**响应：**  
成功时返回 204（No Content）。  

## 分页（Pagination）  

套件使用基于游标的分页机制。请使用 `after` 和 `before` 查询参数，并使用响应中的游标值进行分页。  

```bash
GET /kit/v4/subscribers?per_page=100&after=WzE0OV0=
```  

**响应中包含分页信息：**  
```json
{
  "subscribers": [...],
  "pagination": {
    "has_previous_page": false,
    "has_next_page": true,
    "start_cursor": "WzE0OV0=",
    "end_cursor": "WzI0OV0=",
    "per_page": 100
  }
}
```  

## 代码示例  

### JavaScript  

```javascript
const response = await fetch(
  'https://gateway.maton.ai/kit/v4/subscribers?per_page=10',
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
    'https://gateway.maton.ai/kit/v4/subscribers',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'per_page': 10}
)
data = response.json()
```  

## 注意事项：**  
- 套件 API 使用 V4（V3 已弃用）  
- 订阅者 ID 为整数  
- 自定义字段的键是根据标签自动生成的  
- 大量操作（超过 100 个条目）会异步处理  
- 删除操作成功时返回 204（No Content）且响应体为空  
- 重要提示：当使用 `curl` 命令时，如果 URL 中包含括号，请使用 `curl -g` 以禁用全局解析  
- 重要提示：当将 `curl` 的输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确解析  

## 错误处理（Error Handling）  

| 状态码 | 含义 |  
|--------|---------|  
| 400 | 未建立套件连接  
| 401 | Maton API 密钥无效或缺失  
| 403 | 权限不足（请检查 OAuth 权限范围）  
| 404 | 资源未找到  
| 429 | 请求频率受限  
| 4xx/5xx | 来自套件 API 的传递错误  

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

### 故障排除：应用名称无效（Invalid App Name）  

1. 确保您的 URL 路径以 `kit` 开头。例如：  
- 正确：`https://gateway.maton.ai/kit/v4/subscribers`  
- 错误：`https://gateway.maton.ai/v4/subscribers`  

## 资源（Resources）：**  
- [套件 API 概述](https://developers.kit.com/api-reference/overview)  
- [套件 API 订阅者](https://developers.kit.com/api-reference/subscribers/list-subscribers)  
- [套件 API 标签](https://developers.kit.com/api-reference/tags/list-tags)  
- [套件 API 表单](https://developers.kit.com/api-reference/forms/list-forms)  
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)  
- [Maton 支持](mailto:support@maton.ai)