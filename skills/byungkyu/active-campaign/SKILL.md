---
name: active-campaign
description: |
  ActiveCampaign API integration with managed OAuth. Marketing automation, CRM, contacts, deals, and email campaigns.
  Use this skill when users want to manage contacts, deals, tags, lists, automations, or campaigns in ActiveCampaign.
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

# ActiveCampaign

您可以使用托管的 OAuth 认证来访问 ActiveCampaign API，从而管理联系人、交易、标签、列表、自动化规则和电子邮件活动。

## 快速入门

```bash
# List all contacts
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/active-campaign/api/3/contacts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/active-campaign/api/3/{resource}
```

该网关代理会将请求转发到您的 ActiveCampaign 账户 API，并自动插入您的 OAuth 令牌。

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

您可以在 `https://ctrl.maton.ai` 上管理您的 ActiveCampaign OAuth 连接。

### 查看连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=active-campaign&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'active-campaign'}).encode()
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
    "connection_id": "9e8ba2aa-25ec-4ba0-8815-3068be304dca",
    "status": "ACTIVE",
    "creation_time": "2026-02-09T20:03:16.595823Z",
    "last_updated_time": "2026-02-09T20:04:09.550767Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "active-campaign",
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

如果您有多个 ActiveCampaign 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/active-campaign/api/3/contacts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '9e8ba2aa-25ec-4ba0-8815-3068be304dca')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 联系人

#### 查看联系人列表

```bash
GET /active-campaign/api/3/contacts
```

**查询参数：**
- `limit` - 每页显示的结果数量（默认：20）
- `offset` - 开始索引
- `search` - 按电子邮件搜索
- `filters[email]` - 按电子邮件过滤
- `filters[listid]` - 按列表 ID 过滤

**响应：**
```json
{
  "contacts": [
    {
      "id": "1",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "phone": "",
      "cdate": "2026-02-09T14:03:19-06:00",
      "udate": "2026-02-09T14:03:19-06:00"
    }
  ],
  "meta": {
    "total": "1"
  }
}
```

#### 获取联系人信息

```bash
GET /active-campaign/api/3/contacts/{contactId}
```

返回包含相关数据（如列表、标签、交易和字段值）的联系人信息。

#### 创建联系人

```bash
POST /active-campaign/api/3/contacts
Content-Type: application/json

{
  "contact": {
    "email": "newcontact@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "phone": "555-1234"
  }
}
```

**响应：**
```json
{
  "contact": {
    "id": "2",
    "email": "newcontact@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "cdate": "2026-02-09T17:51:39-06:00",
    "udate": "2026-02-09T17:51:39-06:00"
  }
}
```

#### 更新联系人信息

```bash
PUT /active-campaign/api/3/contacts/{contactId}
Content-Type: application/json

{
  "contact": {
    "firstName": "Updated",
    "lastName": "Name"
  }
}
```

#### 删除联系人

```bash
DELETE /active-campaign/api/3/contacts/{contactId}
```

成功时返回 200 OK。

#### 同步联系人信息（创建或更新）

```bash
POST /active-campaign/api/3/contact/sync
Content-Type: application/json

{
  "contact": {
    "email": "user@example.com",
    "firstName": "Updated Name"
  }
}
```

如果联系人不存在，则创建；如果存在，则更新。

### 标签

#### 查看标签列表

```bash
GET /active-campaign/api/3/tags
```

**响应：**
```json
{
  "tags": [
    {
      "id": "1",
      "tag": "VIP Customer",
      "tagType": "contact",
      "description": "High-value customers",
      "cdate": "2026-02-09T17:51:39-06:00"
    }
  ],
  "meta": {
    "total": "1"
  }
}
```

#### 获取标签信息

```bash
GET /active-campaign/api/3/tags/{tagId}
```

#### 创建标签

```bash
POST /active-campaign/api/3/tags
Content-Type: application/json

{
  "tag": {
    "tag": "New Tag",
    "tagType": "contact",
    "description": "Tag description"
  }
}
```

#### 更新标签信息

```bash
PUT /active-campaign/api/3/tags/{tagId}
Content-Type: application/json

{
  "tag": {
    "tag": "Updated Tag Name"
  }
}
```

#### 删除标签

```bash
DELETE /active-campaign/api/3/tags/{tagId}
```

### 为联系人添加标签

```bash
POST /active-campaign/api/3/contactTags
Content-Type: application/json

{
  "contactTag": {
    "contact": "2",
    "tag": "1"
  }
}
```

#### 从联系人中删除标签

```bash
DELETE /active-campaign/api/3/contactTags/{contactTagId}
```

#### 获取联系人的标签信息

```bash
GET /active-campaign/api/3/contacts/{contactId}/contactTags
```

### 列表

#### 查看所有列表

```bash
GET /active-campaign/api/3/lists
```

**响应：**
```json
{
  "lists": [
    {
      "id": "1",
      "stringid": "master-contact-list",
      "name": "Master Contact List",
      "cdate": "2026-02-09T14:03:20-06:00"
    }
  ],
  "meta": {
    "total": "1"
  }
}
```

#### 获取列表信息

```bash
GET /active-campaign/api/3/lists/{listId}
```

#### 创建列表

```bash
POST /active-campaign/api/3/lists
Content-Type: application/json

{
  "list": {
    "name": "New List",
    "stringid": "new-list",
    "sender_url": "https://example.com",
    "sender_reminder": "You signed up on our website"
  }
}
```

#### 更新列表

```bash
PUT /active-campaign/api/3/lists/{listId}
Content-Type: application/json

{
  "list": {
    "name": "Updated List Name"
  }
}
```

#### 删除列表

```bash
DELETE /active-campaign/api/3/lists/{listId}
```

### 联系人与列表的关联

#### 让联系人订阅列表

```bash
POST /active-campaign/api/3/contactLists
Content-Type: application/json

{
  "contactList": {
    "contact": "2",
    "list": "1",
    "status": "1"
  }
}
```

状态值：`1` = 已订阅，`2` = 未订阅

### 交易

#### 查看交易列表

```bash
GET /active-campaign/api/3/deals
```

**查询参数：**
- `search` - 按标题、联系人或组织搜索
- `filters[stage]` - 按阶段 ID 过滤
- `filters[owner]` - 按所有者 ID 过滤

**响应：**
```json
{
  "deals": [
    {
      "id": "1",
      "title": "New Deal",
      "value": "10000",
      "currency": "usd",
      "stage": "1",
      "owner": "1"
    }
  ],
  "meta": {
    "total": 0,
    "currencies": []
  }
}
```

#### 获取交易信息

```bash
GET /active-campaign/api/3/deals/{dealId}
```

#### 创建交易

```bash
POST /active-campaign/api/3/deals
Content-Type: application/json

{
  "deal": {
    "title": "New Deal",
    "value": "10000",
    "currency": "usd",
    "contact": "2",
    "stage": "1",
    "owner": "1"
  }
}
```

#### 更新交易信息

```bash
PUT /active-campaign/api/3/deals/{dealId}
Content-Type: application/json

{
  "deal": {
    "title": "Updated Deal",
    "value": "15000"
  }
}
```

#### 删除交易

```bash
DELETE /active-campaign/api/3/deals/{dealId}
```

### 交易阶段

#### 查看交易阶段列表

```bash
GET /active-campaign/api/3/dealStages
```

#### 创建交易阶段

```bash
POST /active-campaign/api/3/dealStages
Content-Type: application/json

{
  "dealStage": {
    "title": "New Stage",
    "group": "1",
    "order": "1"
  }
}
```

### 交易组（Pipeline）

#### 查看交易组列表

```bash
GET /active-campaign/api/3/dealGroups
```

#### 创建交易组

```bash
POST /active-campaign/api/3/dealGroups
Content-Type: application/json

{
  "dealGroup": {
    "title": "Sales Pipeline",
    "currency": "usd"
  }
}
```

### 自动化规则

#### 查看自动化规则列表

```bash
GET /active-campaign/api/3/automations
```

**响应：**
```json
{
  "automations": [
    {
      "id": "1",
      "name": "Welcome Series",
      "cdate": "2026-02-09T14:00:00-06:00",
      "mdate": "2026-02-09T14:00:00-06:00",
      "status": "1"
    }
  ],
  "meta": {
    "total": "1"
  }
}
```

#### 获取自动化规则信息

```bash
GET /active-campaign/api/3/automations/{automationId}
```

### 活动

#### 查看活动列表

```bash
GET /active-campaign/api/3/campaigns
```

**响应：**
```json
{
  "campaigns": [
    {
      "id": "1",
      "name": "Newsletter",
      "type": "single",
      "status": "0"
    }
  ],
  "meta": {
    "total": "1"
  }
}
```

#### 获取活动信息

```bash
GET /active-campaign/api/3/campaigns/{campaignId}
```

### 用户

#### 查看用户列表

```bash
GET /active-campaign/api/3/users
```

**响应：**
```json
{
  "users": [
    {
      "id": "1",
      "username": "admin",
      "firstName": "John",
      "lastName": "Doe",
      "email": "admin@example.com"
    }
  ]
}
```

#### 获取用户信息

```bash
GET /active-campaign/api/3/users/{userId}
```

### 账户

#### 查看账户列表

```bash
GET /active-campaign/api/3/accounts
```

#### 创建账户

```bash
POST /active-campaign/api/3/accounts
Content-Type: application/json

{
  "account": {
    "name": "Acme Inc"
  }
}
```

### 自定义字段

#### 查看字段列表

```bash
GET /active-campaign/api/3/fields
```

#### 创建自定义字段

```bash
POST /active-campaign/api/3/fields
Content-Type: application/json

{
  "field": {
    "type": "text",
    "title": "Custom Field",
    "descript": "A custom field"
  }
}
```

### 更新联系人字段值

```bash
PUT /active-campaign/api/3/fieldValues/{fieldValueId}
Content-Type: application/json

{
  "fieldValue": {
    "value": "New Value"
  }
}
```

### 备注

#### 查看备注列表

```bash
GET /active-campaign/api/3/notes
```

#### 创建备注

```bash
POST /active-campaign/api/3/notes
Content-Type: application/json

{
  "note": {
    "note": "This is a note",
    "relid": "2",
    "reltype": "Subscriber"
  }
}
```

### Webhook

#### 查看 Webhook 列表

```bash
GET /active-campaign/api/3/webhooks
```

#### 创建 Webhook

```bash
POST /active-campaign/api/3/webhooks
Content-Type: application/json

{
  "webhook": {
    "name": "My Webhook",
    "url": "https://example.com/webhook",
    "events": ["subscribe", "unsubscribe"],
    "sources": ["public", "admin"]
  }
}
```

## 分页

ActiveCampaign 使用基于偏移量的分页机制：

```bash
GET /active-campaign/api/3/contacts?limit=20&offset=0
```

**参数：**
- `limit` - 每页显示的结果数量（默认：20）
- `offset` - 开始索引

**响应包含元数据：**
```json
{
  "contacts": [...],
  "meta": {
    "total": "150"
  }
}
```

对于大型数据集，使用 `orders[id]=ASC` 和 `id_greater` 参数可提高性能：
```bash
GET /active-campaign/api/3/contacts?orders[id]=ASC&id_greater=100
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/active-campaign/api/3/contacts',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.contacts);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/active-campaign/api/3/contacts',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
print(data['contacts'])
```

### 使用 Python 创建带有标签的联系人

```python
import os
import requests

headers = {
    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
    'Content-Type': 'application/json'
}

# Create contact
contact_response = requests.post(
    'https://gateway.maton.ai/active-campaign/api/3/contacts',
    headers=headers,
    json={
        'contact': {
            'email': 'newuser@example.com',
            'firstName': 'New',
            'lastName': 'User'
        }
    }
)
contact = contact_response.json()['contact']
print(f"Created contact ID: {contact['id']}")

# Add tag to contact
tag_response = requests.post(
    'https://gateway.maton.ai/active-campaign/api/3/contactTags',
    headers=headers,
    json={
        'contactTag': {
            'contact': contact['id'],
            'tag': '1'
        }
    }
)
print("Tag added to contact")
```

## 注意事项

- 所有 API 端点都需要前缀 `/api/3/`。
- 请求体应使用对象格式表示资源（例如：`{"contact": {...}}`）。
- ID 以字符串形式返回。
- 时间戳采用 ISO 8601 格式，并包含时区信息。
- 每个账户每秒的请求限制为 5 次。
- 删除操作返回 200 OK（而非 204）。
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，环境变量（如 `$MATON_API_KEY`）在某些 shell 环境中可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立 ActiveCampaign 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 资源未找到 |
| 422 | 验证错误 |
| 429 | 请求速率限制（每秒 5 次） |
| 4xx/5xx | 来自 ActiveCampaign API 的传递错误 |

错误响应会包含详细信息：
```json
{
  "errors": [
    {
      "title": "The contact email is required",
      "source": {
        "pointer": "/data/attributes/email"
      }
    }
  ]
}
```

### 故障排除：API 密钥无效

**当收到“API 密钥无效”的错误时，请务必按照以下步骤操作，再判断是否存在问题：**

1. 确保 `MATON_API_KEY` 环境变量已设置：

```bash
echo $MATON_API_KEY
```

2. 通过查看连接信息来验证 API 密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 资源

- [ActiveCampaign API 概述](https://developers.activecampaign.com/reference/overview)
- [ActiveCampaign 开发者门户](https://developers.activecampaign.com/)
- [API 基本 URL](https://developers.activecampaign.com/reference/url)
- [联系人 API](https://developers.activecampaign.com/reference/list-all-contacts)
- [标签 API](https://developers.activecampaign.com/reference/contact-tags)
- [交易 API](https://developers.activecampaign.com/reference/list-all-deals)