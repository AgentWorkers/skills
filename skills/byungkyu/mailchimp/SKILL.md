---
name: mailchimp
description: |
  Mailchimp Marketing API integration with managed OAuth. Access audiences, campaigns, templates, automations, reports, and manage subscribers. Use this skill when users want to manage email marketing, subscriber lists, or automate email campaigns. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Mailchimp

通过管理的OAuth认证来访问Mailchimp营销API。您可以管理受众群体、营销活动、模板、自动化脚本、报告以及电子邮件营销的订阅者信息。

## 快速入门

```bash
# List all audiences
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/mailchimp/3.0/lists')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/mailchimp/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的Mailchimp API端点路径（例如 `3.0/lists`）。该网关会将请求代理到您的Mailchimp数据中心，并自动插入您的OAuth令牌。

## 认证

所有请求都需要在 `Authorization` 头部包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的Mailchimp OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=mailchimp&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'mailchimp'}).encode()
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
    "app": "mailchimp",
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

如果您有多个Mailchimp连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/mailchimp/3.0/lists')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API参考

### 列表（受众群体）

在Mailchimp应用程序中，“audience”是常用术语，但API中使用“lists”作为端点名称。

#### 获取所有列表

```bash
GET /mailchimp/3.0/lists
```

查询参数：
- `count` - 返回的记录数（默认为10，最大为1000）
- `offset` - 跳过的记录数（用于分页）
- `fields` - 需要包含的字段列表（用逗号分隔）
- `exclude_fields` - 需要排除的字段列表（用逗号分隔）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/mailchimp/3.0/lists?count=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "lists": [
    {
      "id": "abc123def4",
      "name": "Newsletter Subscribers",
      "contact": {
        "company": "Acme Corp",
        "address1": "123 Main St"
      },
      "stats": {
        "member_count": 5000,
        "unsubscribe_count": 100,
        "open_rate": 0.25
      }
    }
  ],
  "total_items": 1
}
```

#### 获取单个列表

```bash
GET /mailchimp/3.0/lists/{list_id}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/mailchimp/3.0/lists/abc123def4')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建列表

```bash
POST /mailchimp/3.0/lists
Content-Type: application/json

{
  "name": "Newsletter",
  "contact": {
    "company": "Acme Corp",
    "address1": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip": "10001",
    "country": "US"
  },
  "permission_reminder": "You signed up for our newsletter",
  "campaign_defaults": {
    "from_name": "Acme Corp",
    "from_email": "newsletter@acme.com",
    "subject": "",
    "language": "en"
  },
  "email_type_option": true
}
```

#### 更新列表

```bash
PATCH /mailchimp/3.0/lists/{list_id}
```

#### 删除列表

```bash
DELETE /mailchimp/3.0/lists/{list_id}
```

### 列表成员（订阅者）

成员是指受众群体中的联系人。API使用电子邮件地址的小写形式的MD5哈希值作为订阅者标识符。

#### 获取列表成员

```bash
GET /mailchimp/3.0/lists/{list_id}/members
```

查询参数：
- `status` - 按订阅状态过滤（已订阅、已取消订阅、待处理、交易中）
- `count` - 返回的记录数
- `offset` - 跳过的记录数

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/mailchimp/3.0/lists/abc123def4/members?status=subscribed&count=50')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "members": [
    {
      "id": "f4b7c8d9e0",
      "email_address": "john@example.com",
      "status": "subscribed",
      "merge_fields": {
        "FNAME": "John",
        "LNAME": "Doe"
      },
      "tags": [
        {"id": 1, "name": "VIP"}
      ]
    }
  ],
  "total_items": 500
}
```

#### 获取单个成员信息

```bash
GET /mailchimp/3.0/lists/{list_id}/members/{subscriber_hash}
```

`subscriber_hash` 是电子邮件地址的小写形式的MD5哈希值。

**示例：**

```bash
# For email "john@example.com", subscriber_hash = md5("john@example.com")
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/mailchimp/3.0/lists/abc123def4/members/b4c9a0d1e2f3g4h5')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 添加成员

```bash
POST /mailchimp/3.0/lists/{list_id}/members
Content-Type: application/json

{
  "email_address": "newuser@example.com",
  "status": "subscribed",
  "merge_fields": {
    "FNAME": "Jane",
    "LNAME": "Smith"
  },
  "tags": ["Newsletter", "Premium"]
}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'email_address': 'newuser@example.com', 'status': 'subscribed', 'merge_fields': {'FNAME': 'Jane', 'LNAME': 'Smith'}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/mailchimp/3.0/lists/abc123def4/members', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 更新成员信息

```bash
PATCH /mailchimp/3.0/lists/{list_id}/members/{subscriber_hash}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'merge_fields': {'FNAME': 'Jane', 'LNAME': 'Doe'}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/mailchimp/3.0/lists/abc123def4/members/b4c9a0d1e2f3g4h5', data=data, method='PATCH')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 添加或更新成员信息（更新操作）

```bash
PUT /mailchimp/3.0/lists/{list_id}/members/{subscriber_hash}
Content-Type: application/json

{
  "email_address": "user@example.com",
  "status_if_new": "subscribed",
  "merge_fields": {
    "FNAME": "Jane",
    "LNAME": "Smith"
  }
}
```

根据电子邮件哈希值创建新成员或更新现有成员。使用 `status_if_new` 参数来设置新成员的状态。

#### 删除成员

将成员标记为已存档（以后可以重新添加）：

```bash
DELETE /mailchimp/3.0/lists/{list_id}/members/{subscriber_hash}
```

成功时返回 `204 No Content`。

**永久删除成员（符合GDPR规定）：**

```bash
POST /mailchimp/3.0/lists/{list_id}/members/{subscriber_hash}/actions/delete-permanent
```

### 成员标签

#### 获取成员标签

```bash
GET /mailchimp/3.0/lists/{list_id}/members/{subscriber_hash}/tags
```

#### 添加或删除标签

```bash
POST /mailchimp/3.0/lists/{list_id}/members/{subscriber_hash}/tags
Content-Type: application/json

{
  "tags": [
    {"name": "VIP", "status": "active"},
    {"name": "Old Tag", "status": "inactive"}
  ]
}
```

成功时返回 `204 No Content`。

### 分段

#### 获取分段信息

```bash
GET /mailchimp/3.0/lists/{list_id}/segments
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/mailchimp/3.0/lists/abc123def4/segments')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建分段

```bash
POST /mailchimp/3.0/lists/{list_id}/segments
Content-Type: application/json

{
  "name": "Active Subscribers",
  "options": {
    "match": "all",
    "conditions": [
      {
        "condition_type": "EmailActivity",
        "field": "opened",
        "op": "date_within",
        "value": "30"
      }
    ]
  }
}
```

#### 更新分段

```bash
PATCH /mailchimp/3.0/lists/{list_id}/segments/{segment_id}
```

#### 获取分段成员

```bash
GET /mailchimp/3.0/lists/{list_id}/segments/{segment_id}/members
```

#### 删除分段

```bash
DELETE /mailchimp/3.0/lists/{list_id}/segments/{segment_id}
```

成功时返回 `204 No Content`。

### 营销活动

#### 获取所有营销活动

```bash
GET /mailchimp/3.0/campaigns
```

查询参数：
- `type` - 营销活动类型（常规、纯文本、absplit、rss、variate）
- `status` - 营销活动状态（保存中、暂停、计划中、已发送、已发送）
- `list_id` - 按列表ID过滤
- `count` - 返回的记录数
- `offset` - 跳过的记录数

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/mailchimp/3.0/campaigns?status=sent&count=20')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "campaigns": [
    {
      "id": "campaign123",
      "type": "regular",
      "status": "sent",
      "settings": {
        "subject_line": "Monthly Newsletter",
        "from_name": "Acme Corp"
      },
      "send_time": "2025-02-01T10:00:00Z",
      "report_summary": {
        "opens": 1500,
        "clicks": 300,
        "open_rate": 0.30,
        "click_rate": 0.06
      }
    }
  ],
  "total_items": 50
}
```

#### 获取单个营销活动信息

```bash
GET /mailchimp/3.0/campaigns/{campaign_id}
```

#### 创建营销活动

```bash
POST /mailchimp/3.0/campaigns
Content-Type: application/json

{
  "type": "regular",
  "recipients": {
    "list_id": "abc123def4"
  },
  "settings": {
    "subject_line": "Your Monthly Update",
    "from_name": "Acme Corp",
    "reply_to": "hello@acme.com"
  }
}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'type': 'regular', 'recipients': {'list_id': 'abc123def4'}, 'settings': {'subject_line': 'February Newsletter', 'from_name': 'Acme Corp', 'reply_to': 'newsletter@acme.com'}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/mailchimp/3.0/campaigns', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 更新营销活动

```bash
PATCH /mailchimp/3.0/campaigns/{campaign_id}
```

#### 删除营销活动

**成功时返回 `204 No Content`。**

#### 获取营销活动内容

```bash
GET /mailchimp/3.0/campaigns/{campaign_id}/content
```

#### 设置营销活动内容

```bash
PUT /mailchimp/3.0/campaigns/{campaign_id}/content
Content-Type: application/json

{
  "html": "<html><body><h1>Hello!</h1><p>Newsletter content here.</p></body></html>",
  "plain_text": "Hello! Newsletter content here."
}
```

**或使用模板：**

```bash
PUT /mailchimp/3.0/campaigns/{campaign_id}/content
Content-Type: application/json

{
  "template": {
    "id": 12345,
    "sections": {
      "body": "<p>Custom content for the template section</p>"
    }
  }
}
```

#### 获取营销活动发送检查清单

检查营销活动是否准备好发送：

```bash
GET /mailchimp/3.0/campaigns/{campaign_id}/send-checklist
```

#### 发送营销活动

```bash
POST /mailchimp/3.0/campaigns/{campaign_id}/actions/send
```

#### 计划营销活动

```bash
POST /mailchimp/3.0/campaigns/{campaign_id}/actions/schedule
Content-Type: application/json

{
  "schedule_time": "2025-03-01T10:00:00+00:00"
}
```

#### 取消已计划的营销活动

```bash
POST /mailchimp/3.0/campaigns/{campaign_id}/actions/cancel-send
```

### 模板

#### 获取所有模板

```bash
GET /mailchimp/3.0/templates
```

查询参数：
- `type` - 模板类型（用户自定义、基础模板、图库模板）
- `count` - 返回的记录数
- `offset` - 跳过的记录数

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/mailchimp/3.0/templates?type=user')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取单个模板信息

```bash
GET /mailchimp/3.0/templates/{template_id}
```

#### 获取模板的默认内容

```bash
GET /mailchimp/3.0/templates/{template_id}/default-content
```

#### 创建模板

```bash
POST /mailchimp/3.0/templates
Content-Type: application/json

{
  "name": "Newsletter Template",
  "html": "<html><body mc:edit=\"body\"><h1>Title</h1><p>Content here</p></body></html>"
}
```

#### 更新模板

```bash
PATCH /mailchimp/3.0/templates/{template_id}
```

#### 删除模板

**成功时返回 `204 No Content`。**

### 自动化脚本

Mailchimp的经典自动化脚本允许您根据日期、活动或事件触发电子邮件系列。

#### 获取所有自动化脚本

```bash
GET /mailchimp/3.0/automations
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/mailchimp/3.0/automations')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取单个自动化脚本

```bash
GET /mailchimp/3.0/automations/{workflow_id}
```

#### 启动自动化脚本

```bash
POST /mailchimp/3.0/automations/{workflow_id}/actions/start-all-emails
```

#### 暂停自动化脚本

```bash
POST /mailchimp/3.0/automations/{workflow_id}/actions/pause-all-emails
```

#### 获取自动化脚本执行的电子邮件

```bash
GET /mailchimp/3.0/automations/{workflow_id}/emails
```

#### 将订阅者添加到自动化脚本队列

手动将订阅者添加到自动化脚本工作流程中：

```bash
POST /mailchimp/3.0/automations/{workflow_id}/emails/{workflow_email_id}/queue
Content-Type: application/json

{
  "email_address": "subscriber@example.com"
}
```

### 报告

#### 获取营销活动报告

```bash
GET /mailchimp/3.0/reports
```

查询参数：
- `count` - 返回的记录数
- `offset` - 跳过的记录数
- `type` - 营销活动类型

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/mailchimp/3.0/reports?count=20')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "reports": [
    {
      "id": "campaign123",
      "campaign_title": "Monthly Newsletter",
      "emails_sent": 5000,
      "opens": {
        "opens_total": 1500,
        "unique_opens": 1200,
        "open_rate": 0.24
      },
      "clicks": {
        "clicks_total": 450,
        "unique_clicks": 300,
        "click_rate": 0.06
      },
      "unsubscribed": 10,
      "bounce_rate": 0.02
    }
  ]
}
```

#### 获取单个营销活动报告

```bash
GET /mailchimp/3.0/reports/{campaign_id}
```

#### 获取营销活动打开详情

```bash
GET /mailchimp/3.0/reports/{campaign_id}/open-details
```

#### 获取营销活动点击详情

```bash
GET /mailchimp/3.0/reports/{campaign_id}/click-details
```

#### 获取列表活动信息

```bash
GET /mailchimp/3.0/lists/{list_id}/activity
```

返回过去180天的每日聚合活动统计信息（取消订阅、新注册、打开邮件、点击次数）。

### 批量操作

在一次调用中处理多个操作。

#### 创建批量操作

```bash
POST /mailchimp/3.0/batches
Content-Type: application/json

{
  "operations": [
    {
      "method": "POST",
      "path": "/lists/abc123def4/members",
      "body": "{\"email_address\":\"user1@example.com\",\"status\":\"subscribed\"}"
    },
    {
      "method": "POST",
      "path": "/lists/abc123def4/members",
      "body": "{\"email_address\":\"user2@example.com\",\"status\":\"subscribed\"}"
    }
  ]
}
```

#### 获取批量操作状态

```bash
GET /mailchimp/3.0/batches/{batch_id}
```

#### 列出所有批量操作

```bash
GET /mailchimp/3.0/batches
```

#### 删除批量操作

```bash
DELETE /mailchimp/3.0/batches/{batch_id}
```

成功时返回 `204 No Content`。

## 分页

Mailchimp使用基于偏移量的分页机制：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/mailchimp/3.0/lists?count=50&offset=100')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

响应中包含 `total_items`，用于计算总页数：

```json
{
  "lists": [...],
  "total_items": 250
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/mailchimp/3.0/lists',
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
import hashlib

# Get lists
response = requests.get(
    'https://gateway.maton.ai/mailchimp/3.0/lists',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()

# Add a subscriber
list_id = 'abc123def4'
email = 'newuser@example.com'

response = requests.post(
    f'https://gateway.maton.ai/mailchimp/3.0/lists/{list_id}/members',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'email_address': email,
        'status': 'subscribed'
    }
)

# Get subscriber hash for updates
subscriber_hash = hashlib.md5(email.lower().encode()).hexdigest()
```

## 注意事项

- 列表ID是10个字符的字母数字字符串。
- 订阅者哈希值是电子邮件地址的小写形式的MD5哈希值。
- 时间戳采用ISO 8601格式。
- API的调用有120秒的超时限制。
- 每个列表端点的请求最多返回1000条记录。
- “Audience”和“list”在应用程序和API中的术语可以互换使用。
- “Contact”和“member”在应用程序和API中的术语可以互换使用。
- 重要提示：当URL包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 选项来禁用全局解析。
- 重要提示：当将curl输出传递给 `jq` 或其他命令时，在某些Shell环境中环境变量 `$MATON_API_KEY` 可能无法正确解析，可能会导致“Invalid API key”错误。

## 响应代码

| 状态 | 含义 |
|--------|---------|
| 200 | 请求成功，返回响应体 |
| 204 | 请求成功，但没有返回内容（DELETE、某些POST操作） |
| 400 | 请求错误或未建立Mailchimp连接 |
| 401 | Maton API密钥无效或缺失 |
| 403 | 权限不足 |
| 404 | 资源未找到 |
| 405 | 方法不允许 |
| 429 | 超过请求频率限制 |
| 4xx/5xx | 来自Mailchimp API的传递错误 |

Mailchimp的错误响应包含详细信息：

```json
{
  "type": "https://mailchimp.com/developer/marketing/docs/errors/",
  "title": "Invalid Resource",
  "status": 400,
  "detail": "The resource submitted could not be validated.",
  "instance": "abc123-def456",
  "errors": [
    {
      "field": "email_address",
      "message": "This value should be a valid email."
    }
  ]
}
```

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

### 故障排除：应用程序名称无效

1. 确保您的URL路径以 `mailchimp` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/mailchimp/3.0/lists`
- 错误的路径：`https://gateway.maton.ai/3.0/lists`

## 资源

- [Mailchimp营销API文档](https://mailchimp.com/developer/marketing/)
- [API参考](https://mailchimp.com/developer/marketing/api/)
- [快速入门指南](https://mailchimp.com/developer/marketing/guides/quick-start/)
- [版本说明](https://mailchimp.com/developer/release-notes/)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)