---
name: keap
description: |
  Keap API integration with managed OAuth. Manage contacts, companies, tags, tasks, orders, opportunities, and campaigns for CRM and marketing automation.
  Use this skill when users want to create and manage contacts, apply tags, track opportunities, or automate marketing workflows in Keap.
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

# Keap

使用受管理的OAuth认证来访问Keap API。您可以管理联系人、公司、标签、任务、订单、机会等数据，以实现CRM和营销自动化功能。

## 快速入门

```bash
# List contacts
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/keap/crm/rest/v2/contacts?page_size=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/keap/crm/rest/{api-path}
```

该网关会将请求代理到`api.infusionsoft.com/crm/rest`，并自动插入您的OAuth令牌。

## 认证

所有请求都需要在`Authorization`头部包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为`MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在[maton.ai](https://maton.ai)登录或创建账户。
2. 转到[maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在`https://ctrl.maton.ai`管理您的Keap OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=keap&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'keap'}).encode()
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
    "connection_id": "d5242090-02ae-4195-83e3-8deca823eb9a",
    "status": "ACTIVE",
    "creation_time": "2026-02-08T01:34:44.738374Z",
    "last_updated_time": "2026-02-08T01:35:20.106942Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "keap",
    "metadata": {}
  }
}
```

在浏览器中打开返回的`url`以完成OAuth认证。

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

如果您有多个Keap连接，请使用`Maton-Connection`头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/keap/crm/rest/v2/contacts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'd5242090-02ae-4195-83e3-8deca823eb9a')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API参考

### 用户信息

#### 获取当前用户

```bash
GET /keap/crm/rest/v2/oauth/connect/userinfo
```

**响应：**
```json
{
  "email": "user@example.com",
  "sub": "1",
  "id": "4236128",
  "keap_id": "user@example.com",
  "family_name": "Doe",
  "given_name": "John",
  "is_admin": true
}
```

### 联系人操作

#### 列出联系人

```bash
GET /keap/crm/rest/v2/contacts
```

查询参数：
- `page_size` - 每页显示的结果数量（默认为50，最大为1000）
- `page_token` - 下一页的令牌
- `filter` - 过滤条件
- `order_by` - 排序方式
- `fields` - 响应中包含的字段

**响应：**
```json
{
  "contacts": [
    {
      "id": "9",
      "family_name": "Park",
      "given_name": "John"
    }
  ],
  "next_page_token": ""
}
```

#### 获取联系人信息

```bash
GET /keap/crm/rest/v2/contacts/{contact_id}
```

#### 创建联系人

```bash
POST /keap/crm/rest/v2/contacts
Content-Type: application/json

{
  "given_name": "John",
  "family_name": "Doe",
  "email_addresses": [
    {"email": "john@example.com", "field": "EMAIL1"}
  ],
  "phone_numbers": [
    {"number": "555-1234", "field": "PHONE1"}
  ]
}
```

**响应：**
```json
{
  "id": "13",
  "family_name": "Doe",
  "given_name": "John"
}
```

#### 更新联系人信息

```bash
PATCH /keap/crm/rest/v2/contacts/{contact_id}
Content-Type: application/json

{
  "given_name": "Jane"
}
```

#### 删除联系人

```bash
DELETE /keap/crm/rest/v2/contacts/{contact_id}
```

成功时返回204状态码。

#### 获取联系人备注

```bash
GET /keap/crm/rest/v2/contacts/{contact_id}/notes
```

#### 创建联系人备注

```bash
POST /keap/crm/rest/v2/contacts/{contact_id}/notes
Content-Type: application/json

{
  "body": "Note content here",
  "title": "Note Title"
}
```

### 公司操作

#### 列出公司

```bash
GET /keap/crm/rest/v2/companies
```

#### 获取公司信息

```bash
GET /keap/crm/rest/v2/companies/{company_id}
```

#### 创建公司

```bash
POST /keap/crm/rest/v2/companies
Content-Type: application/json

{
  "company_name": "Acme Corp",
  "phone_number": {"number": "555-1234", "type": "MAIN"},
  "website": "https://acme.com"
}
```

#### 更新公司信息

```bash
PATCH /keap/crm/rest/v2/companies/{company_id}
Content-Type: application/json

{
  "company_name": "Acme Corporation"
}
```

#### 删除公司

```bash
DELETE /keap/crm/rest/v2/companies/{company_id}
```

### 标签操作

#### 列出标签

```bash
GET /keap/crm/rest/v2/tags
```

**响应：**
```json
{
  "tags": [
    {
      "id": "91",
      "name": "Nurture Subscriber",
      "description": "",
      "category": {"id": "10"},
      "create_time": "2017-04-24T17:26:26Z",
      "update_time": "2017-04-24T17:26:26Z"
    }
  ],
  "next_page_token": ""
}
```

#### 获取标签信息

```bash
GET /keap/crm/rest/v2/tags/{tag_id}
```

#### 创建标签

```bash
POST /keap/crm/rest/v2/tags
Content-Type: application/json

{
  "name": "VIP Customer",
  "description": "High value customers"
}
```

#### 更新标签信息

```bash
PATCH /keap/crm/rest/v2/tags/{tag_id}
Content-Type: application/json

{
  "name": "Premium Customer"
}
```

#### 删除标签

```bash
DELETE /keap/crm/rest/v2/tags/{tag_id}
```

#### 列出带有标签的联系人

```bash
GET /keap/crm/rest/v2/tags/{tag_id}/contacts
```

#### 为联系人添加标签

```bash
POST /keap/crm/rest/v2/tags/{tag_id}/contacts:applyTags
Content-Type: application/json

{
  "contact_ids": ["1", "2", "3"]
}
```

#### 从联系人中移除标签

```bash
POST /keap/crm/rest/v2/tags/{tag_id}/contacts:removeTags
Content-Type: application/json

{
  "contact_ids": ["1", "2", "3"]
}
```

### 标签类别操作

#### 列出标签类别

```bash
GET /keap/crm/rest/v2/tags/categories
```

#### 创建标签类别

```bash
POST /keap/crm/rest/v2/tags/categories
Content-Type: application/json

{
  "name": "Customer Segments"
}
```

### 任务操作

#### 列出任务

```bash
GET /keap/crm/rest/v2/tasks
```

#### 获取任务信息

```bash
GET /keap/crm/rest/v2/tasks/{task_id}
```

#### 创建任务

```bash
POST /keap/crm/rest/v2/tasks
Content-Type: application/json

{
  "title": "Follow up call",
  "description": "Call to discuss proposal",
  "due_date": "2026-02-15T10:00:00Z",
  "contact": {"id": "9"}
}
```

#### 更新任务信息

```bash
PATCH /keap/crm/rest/v2/tasks/{task_id}
Content-Type: application/json

{
  "completed": true
}
```

#### 删除任务

```bash
DELETE /keap/crm/rest/v2/tasks/{task_id}
```

### 机会操作

#### 列出机会

```bash
GET /keap/crm/rest/v2/opportunities
```

#### 获取机会信息

```bash
GET /keap/crm/rest/v2/opportunities/{opportunity_id}
```

#### 创建机会

```bash
POST /keap/crm/rest/v2/opportunities
Content-Type: application/json

{
  "opportunity_title": "New Deal",
  "contact": {"id": "9"},
  "stage": {"id": "1"},
  "estimated_close_date": "2026-03-01"
}
```

#### 更新机会信息

```bash
PATCH /keap/crm/rest/v2/opportunities/{opportunity_id}
Content-Type: application/json

{
  "stage": {"id": "2"}
}
```

#### 删除机会

```bash
DELETE /keap/crm/rest/v2/opportunities/{opportunity_id}
```

#### 列出机会阶段

```bash
GET /keap/crm/rest/v2/opportunities/stages
```

### 订单操作

#### 列出订单

```bash
GET /keap/crm/rest/v2/orders
```

#### 获取订单信息

```bash
GET /keap/crm/rest/v2/orders/{order_id}
```

#### 创建订单

```bash
POST /keap/crm/rest/v2/orders
Content-Type: application/json

{
  "contact": {"id": "9"},
  "order_date": "2026-02-08",
  "order_title": "Product Order"
}
```

#### 添加订单项

```bash
POST /keap/crm/rest/v2/orders/{order_id}/items
Content-Type: application/json

{
  "product": {"id": "1"},
  "quantity": 2
}
```

### 产品操作

#### 列出产品

```bash
GET /keap/crm/rest/v2/products
```

#### 获取产品信息

```bash
GET /keap/crm/rest/v2/products/{product_id}
```

#### 创建产品

```bash
POST /keap/crm/rest/v2/products
Content-Type: application/json

{
  "product_name": "Consulting Package",
  "product_price": 500.00,
  "product_short_description": "1 hour consulting"
}
```

### 活动操作

#### 列出活动

```bash
GET /keap/crm/rest/v2/campaigns
```

#### 获取活动信息

```bash
GET /keap/crm/rest/v2/campaigns/{campaign_id}
```

#### 列出活动序列

```bash
GET /keap/crm/rest/v2/campaigns/{campaign_id}/sequences
```

#### 将联系人添加到活动序列中

```bash
POST /keap/crm/rest/v2/campaigns/{campaign_id}/sequences/{sequence_id}:addContacts
Content-Type: application/json

{
  "contact_ids": ["1", "2"]
}
```

#### 从活动序列中移除联系人

```bash
POST /keap/crm/rest/v2/campaigns/{campaign_id}/sequences/{sequence_id}:removeContacts
Content-Type: application/json

{
  "contact_ids": ["1", "2"]
}
```

### 邮件操作

#### 列出邮件

```bash
GET /keap/crm/rest/v2/emails
```

#### 获取邮件信息

```bash
GET /keap/crm/rest/v2/emails/{email_id}
```

#### 发送邮件

```bash
POST /keap/crm/rest/v2/emails:send
Content-Type: application/json

{
  "contacts": [{"id": "9"}],
  "subject": "Hello",
  "html_content": "<p>Email body</p>"
}
```

### 用户操作

#### 列出用户

```bash
GET /keap/crm/rest/v2/users
```

#### 获取用户信息

```bash
GET /keap/crm/rest/v2/users/{user_id}
```

### 订阅操作

#### 列出订阅信息

```bash
GET /keap/crm/rest/v2/subscriptions
```

#### 获取订阅信息

```bash
GET /keap/crm/rest/v2/subscriptions/{subscription_id}
```

### 代理商操作

#### 列出代理商

```bash
GET /keap/crm/rest/v2/affiliates
```

#### 获取代理商信息

```bash
GET /keap/crm/rest/v2/affiliates/{affiliate_id}
```

### 自动化操作

#### 列出自动化规则

```bash
GET /keap/crm/rest/v2/automations
```

#### 获取自动化规则信息

```bash
GET /keap/crm/rest/v2/automations/{automation_id}
```

## 分页

Keap使用基于令牌的分页机制：

```bash
GET /keap/crm/rest/v2/contacts?page_size=50
```

**响应：**
```json
{
  "contacts": [...],
  "next_page_token": "abc123"
}
```

对于后续页面，请使用`page_token`参数：

```bash
GET /keap/crm/rest/v2/contacts?page_size=50&page_token=abc123
```

当`next_page_token`为空时，表示没有更多页面。

## 过滤

使用`filter`参数对结果进行过滤：

```bash
GET /keap/crm/rest/v2/contacts?filter=given_name==John
GET /keap/crm/rest/v2/contacts?filter=email_addresses.email==john@example.com
GET /keap/crm/rest/v2/tasks?filter=completed==false
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/keap/crm/rest/v2/contacts?page_size=10',
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
    'https://gateway.maton.ai/keap/crm/rest/v2/contacts',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'page_size': 10}
)
data = response.json()
```

## 注意事项

- 所有API路径都必须包含`/crm/rest`前缀（例如：`/keap/crm/rest/v2/contacts`）
- Keap使用v2 REST API（之前的v1 API已弃用）
- 时间戳采用ISO 8601格式
- ID以字符串形式返回
- 分页使用`page_size`和`page_token`（而非基于偏移量）
- 最大`page_size`为1000
- 重要提示：当将curl输出传递给`jq`或其他命令时，在某些shell环境中环境变量`$MATON_API_KEY`可能无法正确解析

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立Keap连接或请求无效 |
| 401 | Maton API密钥无效或缺失 |
| 403 | 未授权（请检查OAuth权限） |
| 404 | 资源未找到 |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自Keap API的错误 |

### 故障排除：API密钥问题

1. 确保设置了`MATON_API_KEY`环境变量：

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

### 故障排除：应用程序名称错误

1. 确保您的URL路径以`keap`开头。例如：
- 正确的路径：`https://gateway.maton.ai/keap/crm/rest/v2/contacts`
- 错误的路径：`https://gateway.maton.ai/crm/rest/v2/contacts`

## 资源

- [Keap开发者门户](https://developer.infusionsoft.com/)
- [Keap REST API V2文档](https://developer.infusionsoft.com/docs/restv2/)
- [入门指南](https://developer.infusionsoft.com/getting-started/)
- [OAuth 2.0认证](https://developer.infusionsoft.com/authentication/)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)