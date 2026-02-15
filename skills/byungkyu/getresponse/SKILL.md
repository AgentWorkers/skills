---
name: getresponse
description: |
  GetResponse API integration with managed OAuth. Manage email marketing campaigns, contacts, newsletters, autoresponders, and segments.
  Use this skill when users want to manage email lists, send newsletters, create campaigns, or work with contacts in GetResponse.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
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

# GetResponse

通过管理的OAuth认证访问GetResponse API。该API用于管理电子邮件营销活动、联系人信息、新闻通讯、自动回复系统、用户分组以及表单。

## 快速入门

```bash
# List campaigns
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/getresponse/v3/campaigns')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/getresponse/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的GetResponse API端点路径。该网关会将请求代理到 `api.getresponse.com`，并自动插入您的OAuth令牌。

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

您可以在 `https://ctrl.maton.ai` 上管理您的GetResponse OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=getresponse&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'getresponse'}).encode()
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
    "app": "getresponse",
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

如果您有多个GetResponse连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/getresponse/v3/campaigns')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头部，网关将使用默认的（最旧的）活动连接。

## API参考

### 账户操作

#### 获取账户详情

```bash
GET /getresponse/v3/accounts
```

#### 获取账单信息

```bash
GET /getresponse/v3/accounts/billing
```

### 活动操作

GetResponse中的活动相当于电子邮件列表/受众群体。

#### 列出活动

```bash
GET /getresponse/v3/campaigns
```

支持分页：

```bash
GET /getresponse/v3/campaigns?page=1&perPage=100
```

#### 获取活动详情

```bash
GET /getresponse/v3/campaigns/{campaignId}
```

#### 创建活动

```bash
POST /getresponse/v3/campaigns
Content-Type: application/json

{
  "name": "My Campaign"
}
```

### 联系人操作

#### 列出联系人

```bash
GET /getresponse/v3/contacts
```

支持按活动筛选：

```bash
GET /getresponse/v3/contacts?query[campaignId]={campaignId}
```

支持分页：

```bash
GET /getresponse/v3/contacts?page=1&perPage=100
```

支持排序：

```bash
GET /getresponse/v3/contacts?sort[createdOn]=desc
```

#### 获取联系人信息

```bash
GET /getresponse/v3/contacts/{contactId}
```

#### 创建联系人

```bash
POST /getresponse/v3/contacts
Content-Type: application/json

{
  "email": "john@example.com",
  "name": "John Doe",
  "campaign": {
    "campaignId": "abc123"
  },
  "customFieldValues": [
    {
      "customFieldId": "xyz789",
      "value": ["Custom Value"]
    }
  ]
}
```

#### 更新联系人信息

```bash
POST /getresponse/v3/contacts/{contactId}
Content-Type: application/json

{
  "name": "John Smith",
  "customFieldValues": [
    {
      "customFieldId": "xyz789",
      "value": ["Updated Value"]
    }
  ]
}
```

#### 删除联系人

```bash
DELETE /getresponse/v3/contacts/{contactId}
```

#### 获取联系人活动记录

```bash
GET /getresponse/v3/contacts/{contactId}/activities
```

### 自定义字段

#### 列出自定义字段

```bash
GET /getresponse/v3/custom-fields
```

#### 获取自定义字段信息

```bash
GET /getresponse/v3/custom-fields/{customFieldId}
```

#### 创建自定义字段

```bash
POST /getresponse/v3/custom-fields
Content-Type: application/json

{
  "name": "company",
  "type": "text",
  "hidden": false,
  "values": []
}
```

### 新闻通讯操作

#### 列出新闻通讯

```bash
GET /getresponse/v3/newsletters
```

#### 发送新闻通讯

```bash
POST /getresponse/v3/newsletters
Content-Type: application/json

{
  "subject": "Newsletter Subject",
  "name": "Internal Newsletter Name",
  "campaign": {
    "campaignId": "abc123"
  },
  "content": {
    "html": "<html><body>Newsletter content</body></html>",
    "plain": "Newsletter content"
  },
  "sendOn": "2026-02-15T10:00:00Z"
}
```

#### 发送新闻通讯草稿

```bash
POST /getresponse/v3/newsletters/send-draft
Content-Type: application/json

{
  "messageId": "newsletter123",
  "sendOn": "2026-02-15T10:00:00Z"
}
```

#### 列出RSS新闻通讯

```bash
GET /getresponse/v3/rss-newsletters
```

### 标签

#### 列出标签

```bash
GET /getresponse/v3/tags
```

#### 获取标签信息

```bash
GET /getresponse/v3/tags/{tagId}
```

#### 创建标签

```bash
POST /getresponse/v3/tags
Content-Type: application/json

{
  "name": "VIP Customer"
}
```

#### 更新标签信息

```bash
POST /getresponse/v3/tags/{tagId}
Content-Type: application/json

{
  "name": "Premium Customer"
}
```

#### 删除标签

```bash
DELETE /getresponse/v3/tags/{tagId}
```

#### 为联系人分配标签

```bash
POST /getresponse/v3/contacts/{contactId}/tags
Content-Type: application/json

{
  "tags": [
    {"tagId": "abc123"},
    {"tagId": "xyz789"}
  ]
}
```

### 自动回复系统

#### 列出自动回复系统

```bash
GET /getresponse/v3/autoresponders
```

#### 获取自动回复系统信息

```bash
GET /getresponse/v3/autoresponders/{autoresponderId}
```

#### 创建自动回复系统

```bash
POST /getresponse/v3/autoresponders
Content-Type: application/json

{
  "name": "Welcome Email",
  "subject": "Welcome to our list!",
  "campaign": {
    "campaignId": "abc123"
  },
  "triggerSettings": {
    "dayOfCycle": 0
  },
  "content": {
    "html": "<html><body>Welcome!</body></html>",
    "plain": "Welcome!"
  }
}
```

#### 更新自动回复系统

```bash
POST /getresponse/v3/autoresponders/{autoresponderId}
Content-Type: application/json

{
  "subject": "Updated Welcome Email"
}
```

#### 删除自动回复系统

```bash
DELETE /getresponse/v3/autoresponders/{autoresponderId}
```

#### 获取自动回复系统统计信息

```bash
GET /getresponse/v3/autoresponders/{autoresponderId}/statistics
```

#### 获取所有自动回复系统统计信息

```bash
GET /getresponse/v3/autoresponders/statistics
```

### 发件人字段

#### 列出发件人字段

```bash
GET /getresponse/v3/from-fields
```

#### 获取发件人字段信息

```bash
GET /getresponse/v3/from-fields/{fromFieldId}
```

### 交易邮件

**注意：** 交易邮件相关的API可能需要额外的OAuth权限范围，这些权限范围不在默认授权范围内。

#### 列出交易邮件

```bash
GET /getresponse/v3/transactional-emails
```

#### 发送交易邮件

```bash
POST /getresponse/v3/transactional-emails
Content-Type: application/json

{
  "fromField": {
    "fromFieldId": "abc123"
  },
  "subject": "Your Order Confirmation",
  "recipients": {
    "to": "customer@example.com"
  },
  "content": {
    "html": "<html><body>Order confirmed!</body></html>",
    "plain": "Order confirmed!"
  }
}
```

#### 获取交易邮件信息

```bash
GET /getresponse/v3/transactional-emails/{transactionalEmailId}
```

#### 获取交易邮件统计信息

```bash
GET /getresponse/v3/transactional-emails/statistics
```

### 导入功能

#### 列出导入数据

```bash
GET /getresponse/v3/imports
```

#### 创建导入数据

```bash
POST /getresponse/v3/imports
Content-Type: application/json

{
  "campaign": {
    "campaignId": "abc123"
  },
  "contacts": [
    {
      "email": "user1@example.com",
      "name": "User One"
    },
    {
      "email": "user2@example.com",
      "name": "User Two"
    }
  ]
}
```

#### 获取导入数据信息

```bash
GET /getresponse/v3/imports/{importId}
```

### 工作流（自动化）

#### 列出工作流

```bash
GET /getresponse/v3/workflow
```

#### 获取工作流信息

```bash
GET /getresponse/v3/workflow/{workflowId}
```

#### 更新工作流

```bash
POST /getresponse/v3/workflow/{workflowId}
Content-Type: application/json

{
  "status": "enabled"
}
```

### 用户分组（搜索联系人）

#### 列出用户分组

```bash
GET /getresponse/v3/search-contacts
```

#### 创建用户分组

```bash
POST /getresponse/v3/search-contacts
Content-Type: application/json

{
  "name": "Active Subscribers",
  "subscribersType": ["subscribed"],
  "sectionLogicOperator": "or",
  "section": []
}
```

#### 获取用户分组信息

```bash
GET /getresponse/v3/search-contacts/{searchContactId}
```

#### 更新用户分组

```bash
POST /getresponse/v3/search-contacts/{searchContactId}
Content-Type: application/json

{
  "name": "Updated Segment Name"
}
```

#### 删除用户分组

```bash
DELETE /getresponse/v3/search-contacts/{searchContactId}
```

#### 从用户分组中获取联系人

```bash
GET /getresponse/v3/search-contacts/{searchContactId}/contacts
```

#### 不保存地搜索联系人

```bash
POST /getresponse/v3/search-contacts/contacts
Content-Type: application/json

{
  "subscribersType": ["subscribed"],
  "sectionLogicOperator": "or",
  "section": []
}
```

### 表单操作

**注意：** 表单相关的API可能需要额外的OAuth权限范围（如 `form_view`、`form_design`、`form_select`），这些权限范围不在默认授权范围内。

#### 列出表单

```bash
GET /getresponse/v3/forms
```

#### 获取表单信息

```bash
GET /getresponse/v3/forms/{formId}
```

### Web表单

#### 列出Web表单

```bash
GET /getresponse/v3/webforms
```

#### 获取Web表单信息

```bash
GET /getresponse/v3/webforms/{webformId}
```

### SMS消息

#### 列出SMS消息

```bash
GET /getresponse/v3/sms
```

#### 发送SMS消息

```bash
POST /getresponse/v3/sms
Content-Type: application/json

{
  "recipients": {
    "campaignId": "abc123"
  },
  "content": {
    "message": "Your SMS message content"
  },
  "sendOn": "2026-02-15T10:00:00Z"
}
```

#### 获取SMS消息信息

```bash
GET /getresponse/v3/sms/{smsId}
```

#### 获取SMS消息统计信息

```bash
GET /getresponse/v3/statistics/sms/{smsId}
```

### 商店（电子商务）

#### 列出商店

```bash
GET /getresponse/v3/shops
```

#### 创建商店

```bash
POST /getresponse/v3/shops
Content-Type: application/json

{
  "name": "My Store",
  "locale": "en_US",
  "currency": "USD"
}
```

#### 获取商店信息

```bash
GET /getresponse/v3/shops/{shopId}
```

#### 列出产品

```bash
GET /getresponse/v3/shops/{shopId}/products
```

#### 创建产品

```bash
POST /getresponse/v3/shops/{shopId}/products
Content-Type: application/json

{
  "name": "Product Name",
  "url": "https://example.com/product",
  "variants": [
    {
      "name": "Default",
      "price": 29.99,
      "priceTax": 32.99
    }
  ]
}
```

#### 列出订单

```bash
GET /getresponse/v3/shops/{shopId}/orders
```

#### 创建订单

```bash
POST /getresponse/v3/shops/{shopId}/orders
Content-Type: application/json

{
  "contactId": "abc123",
  "totalPrice": 99.99,
  "currency": "USD",
  "status": "completed"
}
```

### 网络研讨会

#### 列出网络研讨会

```bash
GET /getresponse/v3/webinars
```

#### 获取网络研讨会信息

```bash
GET /getresponse/v3/webinars/{webinarId}
```

### 登陆页

#### 列出登录页

```bash
GET /getresponse/v3/lps
```

#### 获取登录页信息

```bash
GET /getresponse/v3/lps/{lpsId}
```

#### 获取登录页统计信息

```bash
GET /getresponse/v3/statistics/lps/{lpsId}/performance
```

## 分页

使用 `page` 和 `perPage` 查询参数进行分页：

```bash
GET /getresponse/v3/contacts?page=1&perPage=100
```

- `page` - 页码（从1开始）
- `perPage` - 每页显示的记录数（最多1000条）

响应头中包含分页信息：
- `TotalCount` - 总记录数
- `TotalPages` - 总页数
- `CurrentPage` - 当前页码

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/getresponse/v3/contacts?perPage=10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const contacts = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/getresponse/v3/contacts',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'perPage': 10}
)
contacts = response.json()
```

## 注意事项

- 活动ID和联系人ID是字母数字字符串。
- 所有时间戳均采用ISO 8601格式（例如：`2026-02-15T10:00:00Z`）。
- 字段名称采用驼峰命名法（CamelCase）。
- 请求速率限制：每10分钟30,000次请求，每秒80次请求。
- 重要提示：当URL包含括号时，使用 `curl -g` 命令以避免全局解析问题。
- 重要提示：当将curl输出传递给 `jq` 或其他命令时，在某些shell环境中 `$MATON_API_KEY` 环境变量可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 无法找到GetResponse连接或请求无效 |
| 401 | Maton API密钥无效或缺失 |
| 404 | 资源未找到 |
| 409 | 冲突（例如，联系人已存在） |
| 429 | 请求速率受限 |
| 4xx/5xx | 来自GetResponse API的传递错误 |

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

### 故障排除：应用名称错误

1. 确保您的URL路径以 `getresponse` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/getresponse/v3/contacts`
- 错误的路径：`https://gateway.maton.ai/v3/contacts`

## 资源

- [GetResponse API文档](https://apidocs.getresponse.com/v3)
- [GetResponse OpenAPI规范](https://apireference.getresponse.com/open-api.json)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)