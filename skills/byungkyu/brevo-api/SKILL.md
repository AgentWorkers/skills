---
name: brevo
description: |
  Brevo API integration with managed OAuth. Email marketing, transactional emails, SMS, contacts, and CRM.
  Use this skill when users want to send emails, manage contacts, create campaigns, or work with Brevo lists and templates.
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

# Brevo

您可以使用受管理的 OAuth 认证来访问 Brevo API。该 API 支持发送交易性电子邮件、管理联系人和列表、创建电子邮件活动以及使用模板等功能。

## 快速入门

```bash
# Get account info
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/brevo/v3/account')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/brevo/v3/{resource}
```

该网关会将请求代理到 `api.brevo.com`，并自动插入您的 OAuth 令牌。

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
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Brevo OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=brevo&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'brevo'}).encode()
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
    "connection_id": "b04dd695-d056-433b-baf9-0fb4eb3bde9e",
    "status": "ACTIVE",
    "creation_time": "2026-02-09T19:51:00.932629Z",
    "last_updated_time": "2026-02-09T19:51:30.123456Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "brevo",
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

如果您有多个 Brevo 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/brevo/v3/account')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'b04dd695-d056-433b-baf9-0fb4eb3bde9e')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，网关将使用默认的（最旧的）活动连接。

## API 参考

### 账户

#### 获取账户信息

```bash
GET /brevo/v3/account
```

**响应：**
```json
{
  "email": "user@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "companyName": "Acme Inc",
  "relay": {
    "enabled": true,
    "data": {
      "userName": "user@smtp-brevo.com",
      "relay": "smtp-relay.brevo.com",
      "port": 587
    }
  }
}
```

### 联系人

#### 列出联系人

```bash
GET /brevo/v3/contacts
```

**查询参数：**
- `limit` - 每页显示的结果数量（默认：50，最大：500）
- `offset` - 第一个结果的索引（从 0 开始）
- `modifiedSince` - 按修改日期过滤（ISO 8601 格式）

**响应：**
```json
{
  "contacts": [
    {
      "id": 1,
      "email": "contact@example.com",
      "emailBlacklisted": false,
      "smsBlacklisted": false,
      "createdAt": "2026-02-09T20:33:59.705+01:00",
      "modifiedAt": "2026-02-09T20:35:19.529+01:00",
      "listIds": [2],
      "attributes": {
        "FIRSTNAME": "John",
        "LASTNAME": "Doe"
      }
    }
  ],
  "count": 1
}
```

#### 获取联系人信息

```bash
GET /brevo/v3/contacts/{identifier}
```

联系人标识符可以是电子邮件地址、电话号码或联系人 ID。

**查询参数：**
- `identifierType` - 标识符类型：`email_id`、`phone_id`、`contact_id`、`ext_id`

#### 创建联系人

```bash
POST /brevo/v3/contacts
Content-Type: application/json

{
  "email": "newcontact@example.com",
  "attributes": {
    "FIRSTNAME": "Jane",
    "LASTNAME": "Smith"
  },
  "listIds": [2],
  "updateEnabled": false
}
```

**响应：**
```json
{
  "id": 2
}
```

如果联系人已存在，请设置 `updateEnabled: true` 以更新其信息。

#### 更新联系人信息

```bash
PUT /brevo/v3/contacts/{identifier}
Content-Type: application/json

{
  "attributes": {
    "FIRSTNAME": "Updated",
    "LASTNAME": "Name"
  }
}
```

成功时返回 204（表示内容无变化）。

#### 删除联系人

```bash
DELETE /brevo/v3/contacts/{identifier}
```

成功时返回 204（表示内容无变化）。

#### 获取联系人活动统计信息

```bash
GET /brevo/v3/contacts/{identifier}/campaignStats
```

### 列表

#### 列出所有列表

```bash
GET /brevo/v3/contacts/lists
```

**响应：**
```json
{
  "lists": [
    {
      "id": 2,
      "name": "Newsletter Subscribers",
      "folderId": 1,
      "uniqueSubscribers": 150,
      "totalBlacklisted": 2,
      "totalSubscribers": 148
    }
  ],
  "count": 1
}
```

#### 获取列表信息

```bash
GET /brevo/v3/contacts/lists/{listId}
```

#### 创建列表

```bash
POST /brevo/v3/contacts/lists
Content-Type: application/json

{
  "name": "New List",
  "folderId": 1
}
```

**响应：**
```json
{
  "id": 3
}
```

#### 更新列表信息

```bash
PUT /brevo/v3/contacts/lists/{listId}
Content-Type: application/json

{
  "name": "Updated List Name"
}
```

成功时返回 204（表示内容无变化）。

#### 删除列表

```bash
DELETE /brevo/v3/contacts/lists/{listId}
```

成功时返回 204（表示内容无变化）。

#### 获取列表中的联系人

```bash
GET /brevo/v3/contacts/lists/{listId}/contacts
```

#### 将联系人添加到列表中

```bash
POST /brevo/v3/contacts/lists/{listId}/contacts/add
Content-Type: application/json

{
  "emails": ["contact1@example.com", "contact2@example.com"]
}
```

#### 从列表中删除联系人

```bash
POST /brevo/v3/contacts/lists/{listId}/contacts/remove
Content-Type: application/json

{
  "emails": ["contact1@example.com"]
}
```

### 文件夹

#### 列出文件夹

```bash
GET /brevo/v3/contacts/folders
```

**响应：**
```json
{
  "folders": [
    {
      "id": 1,
      "name": "Marketing",
      "uniqueSubscribers": 500,
      "totalSubscribers": 480,
      "totalBlacklisted": 20
    }
  ],
  "count": 1
}
```

#### 获取文件夹信息

```bash
GET /brevo/v3/contacts/folders/{folderId}
```

#### 创建文件夹

```bash
POST /brevo/v3/contacts/folders
Content-Type: application/json

{
  "name": "New Folder"
}
```

**响应：**
```json
{
  "id": 4
}
```

#### 更新文件夹信息

```bash
PUT /brevo/v3/contacts/folders/{folderId}
Content-Type: application/json

{
  "name": "Renamed Folder"
}
```

成功时返回 204（表示内容无变化）。

#### 删除文件夹

```bash
DELETE /brevo/v3/contacts/folders/{folderId}
```

删除文件夹及其内的所有列表。成功时返回 204（表示内容无变化）。

#### 获取文件夹中的列表

```bash
GET /brevo/v3/contacts/folders/{folderId}/lists
```

### 属性

#### 列出属性

```bash
GET /brevo/v3/contacts/attributes
```

**响应：**
```json
{
  "attributes": [
    {
      "name": "FIRSTNAME",
      "category": "normal",
      "type": "text"
    },
    {
      "name": "LASTNAME",
      "category": "normal",
      "type": "text"
    }
  ]
}
```

#### 创建属性

```bash
POST /brevo/v3/contacts/attributes/{category}/{attributeName}
Content-Type: application/json

{
  "type": "text"
}
```

属性类别：`normal`、`transactional`、`category`、`calculated`、`global`

#### 更新属性

```bash
PUT /brevo/v3/contacts/attributes/{category}/{attributeName}
Content-Type: application/json

{
  "value": "new value"
}
```

#### 删除属性

```bash
DELETE /brevo/v3/contacts/attributes/{category}/{attributeName}
```

### 交易性电子邮件

#### 发送电子邮件

```bash
POST /brevo/v3/smtp/email
Content-Type: application/json

{
  "sender": {
    "name": "John Doe",
    "email": "john@example.com"
  },
  "to": [
    {
      "email": "recipient@example.com",
      "name": "Jane Smith"
    }
  ],
  "subject": "Welcome!",
  "htmlContent": "<html><body><h1>Hello!</h1><p>Welcome to our service.</p></body></html>"
}
```

**响应：**
```json
{
  "messageId": "<202602092329.12910305853@smtp-relay.mailin.fr>"
}
```

**可选参数：**
- `cc` - 抄送收件人
- `bcc` - 密件抄送收件人
- `replyTo` - 回复地址
- `textContent` - 纯文本版本
- `templateId` - 使用模板而不是 `htmlContent`
- `params` - 模板参数
- `attachment` - 文件附件
- `headers` - 自定义邮件头
- `tags` - 用于跟踪的邮件标签
- `scheduledAt` - 安排发送时间（ISO 8601 格式）

#### 获取交易性电子邮件

```bash
GET /brevo/v3/smtp/emails
```

**查询参数：**
- `email` - 按收件人电子邮件地址过滤
- `templateId` - 按模板过滤
- `messageId` - 按消息 ID 过滤
- `startDate` - 开始日期（YYYY-MM-DD 格式）
- `endDate` - 结束日期（YYYY-MM-DD 格式）
- `limit` - 每页显示的结果数量
- `offset` - 开始索引

#### 删除已安排的电子邮件

```bash
DELETE /brevo/v3/smtp/email/{identifier}
```

标识符可以是 `messageId` 或 `batchId`。

#### 获取电子邮件统计信息

```bash
GET /brevo/v3/smtp/statistics/events
```

**查询参数：**
- `limit` - 每页显示的结果数量
- `offset` - 开始索引
- `startDate` - 开始日期
- `endDate` - 结束日期
- `email` - 按收件人过滤
- `event` - 按事件类型过滤：`delivered`、`opened`、`clicked`、`bounced` 等

### 电子邮件模板

#### 列出模板

```bash
GET /brevo/v3/smtp/templates
```

**响应：**
```json
{
  "count": 1,
  "templates": [
    {
      "id": 1,
      "name": "Welcome Email",
      "subject": "Welcome {{params.name}}!",
      "isActive": true,
      "sender": {
        "name": "Company",
        "email": "noreply@company.com"
      },
      "htmlContent": "<html>...</html>",
      "createdAt": "2026-02-09 23:29:38",
      "modifiedAt": "2026-02-09 23:29:38"
    }
  ]
}
```

#### 获取模板信息

```bash
GET /brevo/v3/smtp/templates/{templateId}
```

#### 创建模板

```bash
POST /brevo/v3/smtp/templates
Content-Type: application/json

{
  "sender": {
    "name": "Company",
    "email": "noreply@company.com"
  },
  "templateName": "Welcome Email",
  "subject": "Welcome {{params.name}}!",
  "htmlContent": "<html><body><h1>Hello {{params.name}}!</h1></body></html>"
}
```

**响应：**
```json
{
  "id": 1
}
```

#### 更新模板

```bash
PUT /brevo/v3/smtp/templates/{templateId}
Content-Type: application/json

{
  "templateName": "Updated Template Name",
  "subject": "New Subject"
}
```

成功时返回 204（表示内容无变化）。

#### 删除模板

```bash
DELETE /brevo/v3/smtp/templates/{templateId}
```

成功时返回 204（表示内容无变化）。

#### 发送测试邮件

```bash
POST /brevo/v3/smtp/templates/{templateId}/sendTest
Content-Type: application/json

{
  "emailTo": ["test@example.com"]
}
```

### 电子邮件活动

#### 列出活动

```bash
GET /brevo/v3/emailCampaigns
```

**查询参数：**
- `type` - 按类型过滤：`classic`、`trigger`
- `status` - 按状态过滤：`draft`、`sent`、`archive`、`queued`、`suspended`、`in_process`
- `limit` - 每页显示的结果数量
- `offset` - 开始索引

**响应：**
```json
{
  "count": 1,
  "campaigns": [
    {
      "id": 2,
      "name": "Monthly Newsletter",
      "subject": "Our March Update",
      "type": "classic",
      "status": "draft",
      "sender": {
        "name": "Company",
        "email": "news@company.com"
      },
      "createdAt": "2026-02-09T23:29:39.000Z"
    }
  ]
}
```

#### 获取活动信息

```bash
GET /brevo/v3/emailCampaigns/{campaignId}
```

#### 创建活动

```bash
POST /brevo/v3/emailCampaigns
Content-Type: application/json

{
  "name": "March Newsletter",
  "subject": "Our March Update",
  "sender": {
    "name": "Company",
    "email": "news@company.com"
  },
  "htmlContent": "<html><body><h1>March News</h1></body></html>",
  "recipients": {
    "listIds": [2]
  }
}
```

**响应：**
```json
{
  "id": 2
}
```

#### 更新活动信息

```bash
PUT /brevo/v3/emailCampaigns/{campaignId}
Content-Type: application/json

{
  "name": "Updated Campaign Name",
  "subject": "Updated Subject"
}
```

成功时返回 204（表示内容无变化）。

#### 删除活动

```bash
DELETE /brevo/v3/emailCampaigns/{campaignId}
```

成功时返回 204（表示内容无变化）。

#### 立即发送活动

```bash
POST /brevo/v3/emailCampaigns/{campaignId}/sendNow
```

#### 发送测试邮件

```bash
POST /brevo/v3/emailCampaigns/{campaignId}/sendTest
Content-Type: application/json

{
  "emailTo": ["test@example.com"]
}
```

#### 更新活动状态

```bash
PUT /brevo/v3/emailCampaigns/{campaignId}/status
Content-Type: application/json

{
  "status": "suspended"
}
```

### 发件人

#### 列出发件人

```bash
GET /brevo/v3/senders
```

**响应：**
```json
{
  "senders": [
    {
      "id": 1,
      "name": "Company",
      "email": "noreply@company.com",
      "active": true,
      "ips": []
    }
  ]
}
```

#### 获取发件人信息

```bash
GET /brevo/v3/senders/{senderId}
```

#### 创建发件人

```bash
POST /brevo/v3/senders
Content-Type: application/json

{
  "name": "Marketing",
  "email": "marketing@company.com"
}
```

#### 更新发件人信息

```bash
PUT /brevo/v3/senders/{senderId}
Content-Type: application/json

{
  "name": "Updated Name"
}
```

#### 删除发件人

```bash
DELETE /brevo/v3/senders/{senderId}
```

### 被阻止的联系人

#### 列出被阻止的联系人

```bash
GET /brevo/v3/smtp/blockedContacts
```

#### 解封联系人

```bash
DELETE /brevo/v3/smtp/blockedContacts/{email}
```

### 被阻止的域名

#### 列出被阻止的域名

```bash
GET /brevo/v3/smtp/blockedDomains
```

#### 添加被阻止的域名

```bash
POST /brevo/v3/smtp/blockedDomains
Content-Type: application/json

{
  "domain": "spam-domain.com"
}
```

#### 删除被阻止的域名

```bash
DELETE /brevo/v3/smtp/blockedDomains/{domain}
```

## 分页

Brevo 使用基于偏移量的分页机制：

```bash
GET /brevo/v3/contacts?limit=50&offset=0
```

**参数：**
- `limit` - 每页显示的结果数量（因端点而异，通常最大为 500）
- `offset` - 开始索引（从 0 开始）

**响应中包含总数：**
```json
{
  "contacts": [...],
  "count": 150
}
```

要获取下一页，请将 `offset` 增加 `limit` 的值：
- 第 1 页：`offset=0&limit=50`
- 第 2 页：`offset=50&limit=50`
- 第 3 页：`offset=100&limit=50`

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/brevo/v3/contacts',
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
    'https://gateway.maton.ai/brevo/v3/contacts',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
print(data['contacts'])
```

### Python（发送电子邮件）

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/brevo/v3/smtp/email',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'sender': {'name': 'John', 'email': 'john@example.com'},
        'to': [{'email': 'recipient@example.com', 'name': 'Jane'}],
        'subject': 'Hello!',
        'htmlContent': '<html><body><h1>Hi Jane!</h1></body></html>'
    }
)
result = response.json()
print(f"Sent! Message ID: {result['messageId']}")
```

### Python（创建联系人并将其添加到列表中）

```python
import os
import requests

headers = {
    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
    'Content-Type': 'application/json'
}

# Create contact
response = requests.post(
    'https://gateway.maton.ai/brevo/v3/contacts',
    headers=headers,
    json={
        'email': 'newuser@example.com',
        'attributes': {'FIRSTNAME': 'New', 'LASTNAME': 'User'},
        'listIds': [2]
    }
)
contact = response.json()
print(f"Created contact ID: {contact['id']}")
```

## 注意事项

- 所有端点的路径前缀都必须加上 `/v3/`。
- 属性名称必须使用大写字母。
- 联系人标识符可以是电子邮件地址、电话号码或 ID。
- 发件人电子邮件地址必须在 Brevo 中经过验证。
- 模板参数使用 `{{params.name}}` 语法。
- PUT 和 DELETE 操作成功时返回 204（表示内容无变化）。
- 资源限制：免费计划每分钟 300 次请求；付费计划的限制更高。
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，环境变量（如 `$MATON_API_KEY`）在某些 shell 环境中可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立 Brevo 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 资源未找到 |
| 429 | 超过请求限制 |
| 4xx/5xx | 来自 Brevo API 的传递错误 |

响应中的速率限制相关头信息：
- `x-sib-ratelimit-limit` - 请求限制
- `x-sib-ratelimit-remaining` - 剩余请求次数
- `x-sib-ratelimit-reset` - 重置时间

### 故障排除：API 密钥无效

**当您收到“API 密钥无效”的错误时，请务必按照以下步骤操作，再判断是否存在问题：**

1. 确保已设置 `MATON_API_KEY` 环境变量：

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

## 资源

- [Brevo API 概述](https://developers.brevo.com/)
- [Brevo API 密钥概念](https://developers.brevo.com/docs/how-it-works)
- [Brevo OAuth 2.0](https://developers.brevo.com/docs/integrating-oauth-20-to-your-solution)
- [管理联系人](https://developers.brevo.com/docs/synchronise-contact-lists)
- [发送交易性电子邮件](https://developers.brevo.com/docs/send-a-transactional-email)