---
name: constant-contact
description: |
  Constant Contact API integration with managed OAuth. Manage contacts, email campaigns, lists, segments, and marketing automation.
  Use this skill when users want to manage email marketing campaigns, contact lists, or analyze campaign performance.
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

# Constant Contact

您可以使用管理的OAuth身份验证来访问Constant Contact V3 API，该API支持联系人管理、电子邮件活动管理、联系人列表管理、客户群体管理以及营销数据分析等功能。

## 快速入门

```bash
# List contacts
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/constant-contact/v3/contacts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/constant-contact/v3/{resource}
```

该API通过`api.cc.email/v3`接口接收请求，并自动插入您的OAuth令牌。

## 身份验证

所有请求都必须在`Authorization`头部包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为`MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在[maton.ai](https://maton.ai)登录或创建账户。
2. 访问[maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在`https://ctrl.maton.ai`管理您的Constant Contact OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=constant-contact&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'constant-contact'}).encode()
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
    "connection_id": "4314bd0f-fd56-40ab-8c65-2676dd2c23c4",
    "status": "ACTIVE",
    "creation_time": "2026-02-07T07:41:05.859244Z",
    "last_updated_time": "2026-02-07T07:41:32.658230Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "constant-contact",
    "metadata": {}
  }
}
```

在浏览器中打开返回的`url`以完成OAuth身份验证。

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

如果您有多个Constant Contact连接，请使用`Maton-Connection`头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/constant-contact/v3/contacts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '4314bd0f-fd56-40ab-8c65-2676dd2c23c4')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略该头部，系统将使用默认的（最旧的）活跃连接。

## API参考

### 账户

#### 获取账户信息

```bash
GET /constant-contact/v3/account/summary
```

#### 获取账户中的电子邮件地址

```bash
GET /constant-contact/v3/account/emails
```

#### 获取用户权限

```bash
GET /constant-contact/v3/account/user/privileges
```

### 联系人

#### 列出联系人

```bash
GET /constant-contact/v3/contacts
```

查询参数：
- `status` - 按状态过滤：`all`、`active`、`deleted`、`not_set`、`pending_confirmation`、`temp_hold`、`unsubscribed`
- `email` - 按电子邮件地址过滤
- `lists` - 按联系人列表ID过滤
- `segment_id` - 按客户群体ID过滤
- `tags` - 按标签ID过滤
- `updated_after` - ISO-8601日期格式的过滤条件
- `include` - 包含子资源：`custom_fields`、`list_memberships`、`taggings`、`notes`
- `limit` - 每页显示的结果数量（默认50条，最多500条）

#### 获取联系人信息

```bash
GET /constant-contact/v3/contacts/{contact_id}
```

#### 创建联系人

```bash
POST /constant-contact/v3/contacts
Content-Type: application/json

{
  "email_address": {
    "address": "john@example.com",
    "permission_to_send": "implicit"
  },
  "first_name": "John",
  "last_name": "Doe",
  "job_title": "Developer",
  "company_name": "Acme Inc",
  "list_memberships": ["list-uuid-here"]
}
```

#### 更新联系人信息

```bash
PUT /constant-contact/v3/contacts/{contact_id}
Content-Type: application/json

{
  "email_address": {
    "address": "john@example.com"
  },
  "first_name": "John",
  "last_name": "Smith"
}
```

#### 删除联系人

```bash
DELETE /constant-contact/v3/contacts/{contact_id}
```

#### 创建或更新联系人（注册表单）

使用此接口可以创建新联系人或更新现有联系人，无需先检查其是否存在：

```bash
POST /constant-contact/v3/contacts/sign_up_form
Content-Type: application/json

{
  "email_address": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "list_memberships": ["list-uuid-here"]
}
```

#### 获取联系人数量

```bash
GET /constant-contact/v3/contacts/counts
```

### 联系人列表

#### 列出联系人列表

```bash
GET /constant-contact/v3/contact_lists
```

查询参数：
- `include_count` - 包含每个列表中的联系人数量
- `includemembership_count` - 包含每个列表中的成员数量
- `limit` - 每页显示的结果数量

#### 获取联系人列表信息

```bash
GET /constant-contact/v3/contact_lists/{list_id}
```

#### 创建联系人列表

```bash
POST /constant-contact/v3/contact_lists
Content-Type: application/json

{
  "name": "Newsletter Subscribers",
  "description": "Main newsletter list",
  "favorite": false
}
```

#### 更新联系人列表

```bash
PUT /constant-contact/v3/contact_lists/{list_id}
Content-Type: application/json

{
  "name": "Updated List Name",
  "description": "Updated description",
  "favorite": true
}
```

#### 删除联系人列表

```bash
DELETE /constant-contact/v3/contact_lists/{list_id}
```

### 标签

#### 列出标签

```bash
GET /constant-contact/v3/contact_tags
```

#### 创建标签

```bash
POST /constant-contact/v3/contact_tags
Content-Type: application/json

{
  "name": "VIP Customer"
}
```

#### 更新标签

```bash
PUT /constant-contact/v3/contact_tags/{tag_id}
Content-Type: application/json

{
  "name": "Premium Customer"
}
```

#### 删除标签

```bash
DELETE /constant-contact/v3/contact_tags/{tag_id}
```

### 自定义字段

#### 列出自定义字段

```bash
GET /constant-contact/v3/contact_custom_fields
```

#### 创建自定义字段

```bash
POST /constant-contact/v3/contact_custom_fields
Content-Type: application/json

{
  "label": "Customer ID",
  "type": "string"
}
```

#### 删除自定义字段

```bash
DELETE /constant-contact/v3/contact_custom_fields/{custom_field_id}
```

### 电子邮件活动

#### 列出电子邮件活动

```bash
GET /constant-contact/v3/emails
```

查询参数：
- `limit` - 每页显示的结果数量（默认50条）

#### 获取电子邮件活动信息

```bash
GET /constant-contact/v3/emails/{campaign_id}
```

#### 创建电子邮件活动

```bash
POST /constant-contact/v3/emails
Content-Type: application/json

{
  "name": "March Newsletter",
  "email_campaign_activities": [
    {
      "format_type": 5,
      "from_name": "Company Name",
      "from_email": "marketing@example.com",
      "reply_to_email": "reply@example.com",
      "subject": "March Newsletter",
      "html_content": "<html><body><h1>Hello!</h1></body></html>"
    }
  ]
}
```

#### 更新电子邮件活动信息

```bash
PUT /constant-contact/v3/emails/activities/{campaign_activity_id}
Content-Type: application/json

{
  "contact_list_ids": ["list-uuid-here"],
  "from_name": "Updated Name",
  "subject": "Updated Subject"
}
```

#### 发送测试邮件

```bash
POST /constant-contact/v3/emails/activities/{campaign_activity_id}/tests
Content-Type: application/json

{
  "email_addresses": ["test@example.com"]
}
```

#### 安排电子邮件活动

```bash
POST /constant-contact/v3/emails/activities/{campaign_activity_id}/schedules
Content-Type: application/json

{
  "scheduled_date": "2026-03-01T10:00:00Z"
}
```

### 客户群体

#### 列出客户群体

```bash
GET /constant-contact/v3/segments
```

#### 获取客户群体信息

```bash
GET /constant-contact/v3/segments/{segment_id}
```

#### 创建客户群体

```bash
POST /constant-contact/v3/segments
Content-Type: application/json

{
  "name": "Engaged Subscribers",
  "segment_criteria": "..."
}
```

#### 删除客户群体

```bash
DELETE /constant-contact/v3/segments/{segment_id}
```

### 批量操作

#### 导入联系人

```bash
POST /constant-contact/v3/activities/contacts_file_import
Content-Type: multipart/form-data

{file: contacts.csv, list_ids: ["list-uuid"]}
```

#### 将联系人添加到列表中

```bash
POST /constant-contact/v3/activities/add_list_memberships
Content-Type: application/json

{
  "source": {
    "contact_ids": ["contact-uuid-1", "contact-uuid-2"]
  },
  "list_ids": ["list-uuid"]
}
```

#### 从列表中移除联系人

```bash
POST /constant-contact/v3/activities/remove_list_memberships
Content-Type: application/json

{
  "source": {
    "list_ids": ["source-list-uuid"]
  },
  "list_ids": ["target-list-uuid"]
}
```

#### 批量删除联系人

```bash
POST /constant-contact/v3/activities/contact_delete
Content-Type: application/json

{
  "contact_ids": ["contact-uuid-1", "contact-uuid-2"]
}
```

#### 获取活动状态

```bash
GET /constant-contact/v3/activities/{activity_id}
```

#### 列出活动记录

```bash
GET /constant-contact/v3/activities
```

### 报告

#### 电子邮件活动摘要

```bash
GET /constant-contact/v3/reports/summary_reports/email_campaign_summaries
```

查询参数：
- `start` - 开始日期（ISO-8601格式）
- `end` - 结束日期（ISO-8601格式）

#### 获取电子邮件活动报告

```bash
GET /constant-contact/v3/reports/email_reports/{campaign_activity_id}
```

#### 联系人活动摘要

```bash
GET /constant-contact/v3/reports/contact_reports/{contact_id}/activity_summary
```

## 分页

该API使用基于游标的分页机制，通过`limit`参数进行分页：

```bash
GET /constant-contact/v3/contacts?limit=50
```

响应中包含分页链接：

```json
{
  "contacts": [...],
  "_links": {
    "next": {
      "href": "/v3/contacts?cursor=abc123"
    }
  }
}
```

使用“next”链接可以查看后续页面：

```bash
GET /constant-contact/v3/contacts?cursor=abc123
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/constant-contact/v3/contacts?limit=50',
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
    'https://gateway.maton.ai/constant-contact/v3/contacts',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'limit': 50}
)
data = response.json()
```

## 注意事项

- 资源ID采用UUID格式（36个字符，包含连字符）。
- 所有日期均采用ISO-8601格式（例如：`YYYY-MM-DDThh:mm:ss.sZ`）。
- 每个账户最多可以拥有1,000个联系人列表。
- 一个联系人最多可以属于50个列表。
- 批量操作是异步的，请检查活动状态以确认操作是否完成。
- 电子邮件活动要求发送者的电子邮件地址经过验证。
- `format_type: 5`表示自定义HTML格式的邮件。
- **重要提示：** 当使用curl命令时，如果URL中包含括号，请使用`curl -g`来禁用全局解析。
- **重要提示：** 当将curl的输出传递给`jq`或其他命令时，在某些shell环境中环境变量`$MATON_API_KEY`可能无法正确解析。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 缺少Constant Contact连接或请求无效 |
| 401 | Maton API密钥无效或缺失，或者OAuth令牌已过期 |
| 403 | 没有足够的权限执行请求的操作 |
| 404 | 资源未找到 |
| 409 | 发生冲突（例如，电子邮件地址重复） |
| 429 | 操作频率超出限制 |
| 4xx/5xx | 来自Constant Contact API的传递错误 |

### 错误响应格式

```json
{
  "error_key": "unauthorized",
  "error_message": "Unauthorized"
}
```

### 故障排除：API密钥问题

1. 确保`MATON_API_KEY`环境变量已设置：

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

1. 确保您的URL路径以`constant-contact`开头。例如：
- 正确的路径：`https://gateway.maton.ai/constant-contact/v3/contacts`
- 错误的路径：`https://gateway.maton.ai/v3/contacts`

## 资源链接

- [Constant Contact V3 API概述](https://developer.constantcontact.com/api_guide/getting_started.html)
- [API参考](https://developer.constantcontact.com/api_reference/index.html)
- [技术概述](https://developer.constantcontact.com/api_guide/v3_technical_overview.html)
- [联系人概述](https://developer.constantcontact.com/api_guide/contacts_overview.html)
- [电子邮件活动指南](https://developer.constantcontact.com/api_guide/email_campaigns_get_started.html)
- [联系人列表概述](https://v3.developer.constantcontact.com/api_guide/lists_overview.html)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)