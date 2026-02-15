---
name: mailerlite
description: |
  MailerLite API integration with managed OAuth. Manage email subscribers, groups, campaigns, automations, and forms.
  Use this skill when users want to add subscribers, create email campaigns, manage groups, or work with MailerLite automations.
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

# MailerLite

通过管理的OAuth认证来访问MailerLite API。可以管理订阅者、组、活动、自动化脚本、表单、字段、细分受众和Webhook。

## 快速入门

```bash
# List subscribers
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/mailerlite/api/subscribers?limit=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/mailerlite/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的MailerLite API端点路径。该网关会将请求代理到 `connect.mailerlite.com` 并自动插入您的OAuth令牌。

## 认证

所有请求都需要在 `Authorization` 头中包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的MailerLite OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=mailerlite&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'mailerlite'}).encode()
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
    "app": "mailerlite",
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

如果您有多个MailerLite连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/mailerlite/api/subscribers')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## API参考

### 订阅者操作

#### 列出订阅者

```bash
GET /mailerlite/api/subscribers
```

查询参数：
- `filter[status]` - 按状态筛选：`active`（活动中的）、`unsubscribed`（已取消订阅的）、`unconfirmed`（未确认的）、`bounced`（被退回的）、`junk`（垃圾邮件）
- `limit` - 每页显示的结果数量（默认：25）
- `cursor` - 分页游标
- `include` - 是否包含相关数据：`groups`（包含组信息）

#### 获取订阅者信息

```bash
GET /mailerlite/api/subscribers/{subscriber_id_or_email}
```

#### 创建/更新订阅者

```bash
POST /mailerlite/api/subscribers
Content-Type: application/json

{
  "email": "subscriber@example.com",
  "fields": {
    "name": "John Doe",
    "company": "Acme Inc"
  },
  "groups": ["12345678901234567"],
  "status": "active"
}
```

创建新订阅者时返回 201 状态码，更新订阅者信息时返回 200 状态码。

#### 更新订阅者信息

```bash
PUT /mailerlite/api/subscribers/{subscriber_id}
Content-Type: application/json

{
  "fields": {
    "name": "Jane Doe"
  },
  "status": "active"
}
```

#### 删除订阅者

```bash
DELETE /mailerlite/api/subscribers/{subscriber_id}
```

#### 获取订阅者活动记录

```bash
GET /mailerlite/api/subscribers/{subscriber_id}/activity-log
```

查询参数：
- `filter[log_name]` - 按活动类型筛选：`campaign_send`（活动发送）、`automation_email_sent`（自动化邮件发送）、`email_open`（邮件打开）、`link_click`（链接点击）、`email_bounce`（邮件退回）、`spam_complaint`（垃圾邮件投诉）、`unsubscribed`（取消订阅）
- `limit` - 每页显示的结果数量（默认：100）
- `page` - 页码（从1开始）

#### 忘记订阅者（符合GDPR要求）

```bash
POST /mailerlite/api/subscribers/{subscriber_id}/forget
```

### 组操作

#### 列出组

```bash
GET /mailerlite/api/groups
```

查询参数：
- `limit` - 每页显示的结果数量
- `page` - 页码（从1开始）
- `filter[name]` - 按名称筛选（部分匹配）
- `sort` - 排序方式：`name`（名称）、`total`（总数）、`open_rate`（打开率）、`click_rate`（点击率）、`created_at`（按创建时间降序排序）

#### 创建组

```bash
POST /mailerlite/api/groups
Content-Type: application/json

{
  "name": "Newsletter Subscribers"
}
```

#### 更新组

```bash
PUT /mailerlite/api/groups/{group_id}
Content-Type: application/json

{
  "name": "Updated Group Name"
}
```

#### 删除组

```bash
DELETE /mailerlite/api/groups/{group_id}
```

#### 获取组内的订阅者

```bash
GET /mailerlite/api/groups/{group_id}/subscribers
```

查询参数：
- `filter[status]` - 按状态筛选：`active`（活动中的）、`unsubscribed`（已取消订阅的）、`unconfirmed`（未确认的）、`bounced`（被退回的）、`junk`（垃圾邮件）
- `limit` - 每页显示的结果数量（1-1000，默认：50）
- `cursor` - 分页游标

#### 将订阅者分配到组

```bash
POST /mailerlite/api/subscribers/{subscriber_id}/groups/{group_id}
```

#### 从组中移除订阅者

```bash
DELETE /mailerlite/api/subscribers/{subscriber_id}/groups/{group_id}
```

### 活动操作

#### 列出活动

```bash
GET /mailerlite/api/campaigns
```

查询参数：
- `filter[status]` - 按状态筛选：`sent`（已发送的）、`draft`（草稿）、`ready`（准备好的）
- `filter[type]` - 按类型筛选：`regular`（常规的）、`ab`（自动回复的）、`resend`（重新发送的）、`rss`（RSS邮件）
- `limit` - 每页显示的结果数量：10、25、50或100（默认：25）
- `page` - 页码（从1开始）

#### 获取活动信息

```bash
GET /mailerlite/api/campaigns/{campaign_id}
```

#### 创建活动

```bash
POST /mailerlite/api/campaigns
Content-Type: application/json

{
  "name": "My Newsletter",
  "type": "regular",
  "emails": [
    {
      "subject": "Weekly Update",
      "from_name": "Newsletter",
      "from": "newsletter@example.com"
    }
  ],
  "groups": ["12345678901234567"]
}
```

#### 更新活动

```bash
PUT /mailerlite/api/campaigns/{campaign_id}
Content-Type: application/json

{
  "name": "Updated Campaign Name",
  "emails": [
    {
      "subject": "New Subject Line",
      "from_name": "Newsletter",
      "from": "newsletter@example.com"
    }
  ]
}
```

**注意：** 只有草稿活动可以更新。

#### 安排活动发送

```bash
POST /mailerlite/api/campaigns/{campaign_id}/schedule
Content-Type: application/json

{
  "delivery": "instant"
}
```

#### 取消活动

```json
{
  "delivery": "scheduled",
  "schedule": {
    "date": "2026-03-15",
    "hours": "10",
    "minutes": "30"
  }
}
```

将已准备好的活动恢复为草稿状态。

#### 删除活动

```bash
DELETE /mailerlite/api/campaigns/{campaign_id}
```

#### 获取活动中的订阅者活动记录

```bash
GET /mailerlite/api/campaigns/{campaign_id}/reports/subscriber-activity
```

查询参数：
- `filter[type]` - 按活动类型筛选：`opened`（已打开的）、`unopened`（未打开的）、`clicked`（点击的）、`unsubscribed`（取消订阅的）、`forwarded`（转发的）、`hardbounced`（硬退回的）、`softbounced`（软退回的）、`junk`（垃圾邮件）
- `filter[search]` - 按电子邮件地址搜索
- `limit` - 每页显示的结果数量（10、25、50或100）
- `page` - 页码（从1开始）

### 自动化脚本操作

#### 列出自动化脚本

```bash
GET /mailerlite/api/automations
```

查询参数：
- `filter[enabled]` - 按状态筛选：`true`（启用）或 `false`（禁用）
- `filter[name]` - 按名称筛选
- `filter[group]` - 按组ID筛选
- `page` - 页码（从1开始）
- `limit` - 每页显示的结果数量（默认：10）

#### 获取自动化脚本信息

```bash
GET /mailerlite/api/automations/{automation_id}
```

#### 创建自动化脚本

```bash
POST /mailerlite/api/automations
Content-Type: application/json

{
  "name": "Welcome Series"
}
```

创建一个草稿自动化脚本。

#### 获取自动化脚本活动记录

```bash
GET /mailerlite/api/automations/{automation_id}/activity
```

查询参数：
- `filter[status]` - 必填：`completed`（已完成）、`active`（活动中的）、`canceled`（已取消的）、`failed`（失败的）
- `filter[date_from]` - 开始日期（格式：Y-m-d）
- `filter[date_to]` - 结束日期（格式：Y-m-d）
- `filter[search]` - 按电子邮件地址搜索
- `page` - 页码（从1开始）
- `limit` - 每页显示的结果数量（默认：10）

#### 删除自动化脚本

```bash
DELETE /mailerlite/api/automations/{automation_id}
```

### 字段操作

#### 列出字段

```bash
GET /mailerlite/api/fields
```

查询参数：
- `limit` - 每页显示的结果数量（最多100个）
- `page` - 页码（从1开始）
- `filter[keyword]` - 按关键词筛选（部分匹配）
- `filter[type]` - 按类型筛选：`text`（文本）、`number`（数字）、`date`（日期）
- `sort` - 排序方式：`name`（名称）、`type`（类型）（按降序排序）

#### 创建字段

```bash
POST /mailerlite/api/fields
Content-Type: application/json

{
  "name": "Company",
  "type": "text"
}
```

#### 更新字段

```bash
PUT /mailerlite/api/fields/{field_id}
Content-Type: application/json

{
  "name": "Organization"
}
```

#### 删除字段

```bash
DELETE /mailerlite/api/fields/{field_id}
```

### 细分受众操作

#### 列出细分受众

```bash
GET /mailerlite/api/segments
```

查询参数：
- `limit` - 每页显示的结果数量（最多250个）
- `page` - 页码（从1开始）

#### 获取细分受众中的订阅者

```bash
GET /mailerlite/api/segments/{segment_id}/subscribers
```

查询参数：
- `filter[status]` - 按状态筛选：`active`（活动中的）、`unsubscribed`（已取消订阅的）、`unconfirmed`（未确认的）、`bounced`（被退回的）、`junk`（垃圾邮件）
- `limit` - 每页显示的结果数量
- `cursor` - 分页游标

#### 更新细分受众

```bash
PUT /mailerlite/api/segments/{segment_id}
Content-Type: application/json

{
  "name": "High Engagement Subscribers"
}
```

#### 删除细分受众

```bash
DELETE /mailerlite/api/segments/{segment_id}
```

### 表单操作

#### 列出表单

```bash
GET /mailerlite/api/forms/{type}
```

路径参数：
- `type` - 表单类型：`popup`（弹出式）、`embedded`（嵌入式的）、`promotion`（促销用的）

查询参数：
- `limit` - 每页显示的结果数量
- `page` - 页码（从1开始）
- `filter[name]` - 按名称筛选（部分匹配）
- `sort` - 排序方式：`created_at`（创建时间）、`name`（名称）、`conversions_count`（转化次数）、`opens_count`（打开次数）、`visitors`（访问者数量）、`conversion_rate`（转化率）、`last_registration_at`（最后注册时间）（按降序排序）

#### 获取表单信息

```bash
GET /mailerlite/api/forms/{form_id}
```

#### 更新表单

```bash
PUT /mailerlite/api/forms/{form_id}
Content-Type: application/json

{
  "name": "Newsletter Signup"
}
```

#### 删除表单

```bash
DELETE /mailerlite/api/forms/{form_id}
```

#### 获取表单中的订阅者

```bash
GET /mailerlite/api/forms/{form_id}/subscribers
```

查询参数：
- `filter[status]` - 按状态筛选：`active`（活动中的）、`unsubscribed`（已取消订阅的）、`unconfirmed`（未确认的）、`bounced`（被退回的）、`junk`（垃圾邮件）
- `limit` - 每页显示的结果数量（默认：25）
- `cursor` - 分页游标

### Webhook操作

#### 列出Webhook

```bash
GET /mailerlite/api/webhooks
```

#### 获取Webhook信息

```bash
GET /mailerlite/api/webhooks/{webhook_id}
```

#### 创建Webhook

```bash
POST /mailerlite/api/webhooks
Content-Type: application/json

{
  "name": "Subscriber Updates",
  "events": ["subscriber.created", "subscriber.updated"],
  "url": "https://example.com/webhook"
}
```

#### 更新Webhook

```bash
PUT /mailerlite/api/webhooks/{webhook_id}
Content-Type: application/json

{
  "name": "Updated Webhook",
  "enabled": true
}
```

#### 删除Webhook

```bash
DELETE /mailerlite/api/webhooks/{webhook_id}
```

## 分页

MailerLite对大多数端点使用基于游标的分页方式，对某些端点使用基于页面的分页方式。

### 基于游标的分页

```bash
GET /mailerlite/api/subscribers?limit=25&cursor=eyJpZCI6MTIzNDU2fQ
```

响应中包含分页链接：
```json
{
  "data": [...],
  "links": {
    "first": "https://connect.mailerlite.com/api/subscribers?cursor=...",
    "last": null,
    "prev": null,
    "next": "https://connect.mailerlite.com/api/subscribers?cursor=eyJpZCI6MTIzNDU2fQ"
  },
  "meta": {
    "path": "https://connect.mailerlite.com/api/subscribers",
    "per_page": 25,
    "next_cursor": "eyJpZCI6MTIzNDU2fQ",
    "prev_cursor": null
  }
}
```

### 基于页面的分页

```bash
GET /mailerlite/api/groups?limit=25&page=2
```

响应中包含页面元数据：
```json
{
  "data": [...],
  "meta": {
    "current_page": 2,
    "from": 26,
    "last_page": 4,
    "per_page": 25,
    "to": 50,
    "total": 100
  }
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/mailerlite/api/subscribers?limit=10',
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
    'https://gateway.maton.ai/mailerlite/api/subscribers',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'limit': 10}
)
data = response.json()
```

### 创建订阅者的示例

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/mailerlite/api/subscribers',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'email': 'newuser@example.com',
        'fields': {'name': 'John Doe'},
        'status': 'active'
    }
)
data = response.json()
```

## 注意事项

- 请求速率限制：每分钟120次请求。
- 订阅者的电子邮件地址用作唯一标识符（POST请求用于创建或更新订阅者信息）。
- 组的名称最长为255个字符。
- 只有草稿活动可以更新。
- 可以通过 `X-Version: YYYY-MM-DD` 头来覆盖API版本。
- **重要提示：** 当URL包含括号时，使用 `curl -g` 选项来禁用glob解析。
- **重要提示：** 当将curl输出传递给 `jq` 或其他命令时，在某些shell环境中环境变量（如 `$MATON_API_KEY`）可能无法正确解析。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 未找到MailerLite连接 |
| 401 | Maton API密钥无效或缺失 |
| 403 | 禁止访问 - 权限不足 |
| 404 | 资源未找到 |
| 422 | 验证错误 |
| 429 | 请求速率限制（每分钟120次） |
| 4xx/5xx | 来自MailerLite API的传递错误 |

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

1. 确保您的URL路径以 `mailerlite` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/mailerlite/api/subscribers`
- 错误的路径：`https://gateway.maton.ai/api/subscribers`

## 资源

- [MailerLite API文档](https://developers.mailerlite.com/docs/)
- [MailerLite 订阅者API](https://developers.mailerlite.com/docs/subscribers.html)
- [MailerLite 组API](https://developers.mailerlite.com/docs/groups.html)
- [MailerLite 活动API](https://developers.mailerlite.com/docs/campaigns.html)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)