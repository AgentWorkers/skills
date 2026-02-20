---
name: active-campaign
description: >
  **ActiveCampaign API集成（支持OAuth认证）**  
  该功能支持与ActiveCampaign的自动化营销系统（Marketing Automation）、客户关系管理（CRM）、联系人管理（Contacts）、交易管理（Deals）以及电子邮件营销（Email Campaigns）进行集成。  
  当用户需要管理ActiveCampaign中的联系人、交易、标签、列表、自动化流程或营销活动时，可使用此功能。  
  对于其他第三方应用程序，建议使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。  
  使用此功能需要网络连接以及有效的Maton API密钥。
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
# ActiveCampaign

通过管理的OAuth认证来访问ActiveCampaign API。您可以管理联系人、交易、标签、列表、自动化规则以及电子邮件活动。

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

## 基本URL

```
https://gateway.maton.ai/active-campaign/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的ActiveCampaign API端点路径。该网关会将请求代理到 `{account}.api-us1.com` 并自动插入您的OAuth令牌。

## 认证

所有请求都需要在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
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

您可以在 `https://ctrl.maton.ai` 上管理您的ActiveCampaign OAuth连接。

### 列出连接

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

如果您有多个ActiveCampaign连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/active-campaign/api/3/contacts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '9e8ba2aa-25ec-4ba0-8815-3068be304dca')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略该头部，网关将使用默认的（最旧的）活动连接。

## API参考

### 联系人

#### 列出联系人

```bash
GET /active-campaign/api/3/contacts
```

**查询参数：**
- `limit` - 结果数量（默认：20）
- `offset` - 开始索引
- `search` - 按电子邮件搜索
- `filters[email]` - 按电子邮件过滤
- `filters[listid]` - 按列表ID过滤

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

#### 列出标签

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

#### 列出所有列表

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

#### 列出交易

```bash
GET /active-campaign/api/3/deals
```

**查询参数：**
- `search` - 按标题、联系人或组织搜索
- `filters[stage]` - 按阶段ID过滤
- `filters[owner]` - 按所有者ID过滤

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

#### 列出交易阶段

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

#### 列出交易组

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

#### 列出自动化规则

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

#### 列出活动

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

#### 列出用户

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

#### 列出账户

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

#### 列出字段

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

#### 列出备注

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

#### 列出Webhook

```bash
GET /active-campaign/api/3/webhooks
```

#### 创建Webhook

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

ActiveCampaign使用基于偏移量的分页机制：

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

对于大型数据集，使用 `orders[id]=ASC` 和 `id_greater` 参数以提高性能：
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

### Python（创建带有标签的联系人）

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

- 所有端点都需要加上 `/api/3/` 前缀。
- 请求体使用对象格式来表示资源（例如：`{"contact": {...}}`）。
- ID 以字符串形式返回。
- 时间戳采用ISO 8601格式，并包含时区信息。
- 每个账户每秒的请求限制为5次。
- DELETE操作返回200 OK（而不是204）。
- **重要提示：** 当将curl输出传递给 `jq` 或其他命令时，在某些shell环境中环境变量（如 `$MATON_API_KEY`）可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立ActiveCampaign连接或请求无效 |
| 401 | Maton API密钥无效或缺失 |
| 404 | 资源未找到 |
| 422 | 验证错误 |
| 429 | 请求速率限制（每秒5次） |
| 4xx/5xx | 来自ActiveCampaign API的传递错误 |

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

### 故障排除：API密钥无效

**当收到“API密钥无效”的错误时，请务必按照以下步骤操作，再判断是否存在问题：**

1. 确保 `MATON_API_KEY` 环境变量已设置：

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

## 资源

- [ActiveCampaign API概述](https://developers.activecampaign.com/reference/overview)
- [ActiveCampaign开发者门户](https://developers.activecampaign.com/)
- [API基本URL](https://developers.activecampaign.com/reference/url)
- [联系人API](https://developers.activecampaign.com/reference/list-all-contacts)
- [标签API](https://developers.activecampaign.com/reference/contact-tags)
- [交易API](https://developers.activecampaign.com/reference/list-all-deals)