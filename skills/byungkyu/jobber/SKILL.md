---
name: jobber
description: |
  Jobber API integration with managed OAuth. Manage clients, jobs, invoices, quotes, properties, and team members for field service businesses.
  Use this skill when users want to create and manage service jobs, clients, quotes, invoices, or access scheduling data.
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

# Jobber

通过管理的OAuth认证访问Jobber API，该API用于管理现场服务企业的客户、任务、发票、报价单、属性和团队成员。

## 快速入门

```bash
# Get account information
python <<'EOF'
import urllib.request, os, json
query = '{"query": "{ account { id name } }"}'
req = urllib.request.Request('https://gateway.maton.ai/jobber/graphql', data=query.encode(), method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## API类型

Jobber仅使用**GraphQL API**。所有请求均为POST请求，目标端点为`/graphql`，请求体中包含`query`字段（以JSON格式）。

## 基本URL

```
https://gateway.maton.ai/jobber/graphql
```

代理服务器会将请求转发到`api.getjobber.com/apigraphql`，并自动插入您的OAuth令牌和API版本头。

## 认证

所有请求都必须在`Authorization`头部包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

代理服务器还会自动插入`X-JOBBER-GRAPHQL-VERSION`头部（当前版本为`2025-04-16`）。

**环境变量：** 将您的API密钥设置为`MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在[maton.ai](https://maton.ai)登录或创建账户。
2. 访问[maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在`https://ctrl.maton.ai`管理您的Jobber OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=jobber&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'jobber'}).encode()
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
    "connection_id": "cc61da85-8bf7-4fbc-896b-4e4eb9a5aafd",
    "status": "ACTIVE",
    "creation_time": "2026-02-07T09:29:19.946291Z",
    "last_updated_time": "2026-02-07T09:30:59.990084Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "jobber",
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

如果您有多个Jobber连接，请使用`Maton-Connection`头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
query = '{"query": "{ account { id name } }"}'
req = urllib.request.Request('https://gateway.maton.ai/jobber/graphql', data=query.encode(), method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', 'cc61da85-8bf7-4fbc-896b-4e4eb9a5aafd')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果未指定，代理服务器将使用默认的（最旧的）活动连接。

## API参考

### 账户操作

#### 获取账户信息

```bash
POST /jobber/graphql
Content-Type: application/json

{
  "query": "{ account { id name } }"
}
```

### 客户操作

#### 列出客户

```bash
POST /jobber/graphql
Content-Type: application/json

{
  "query": "{ clients(first: 20) { nodes { id name emails { primary address } phones { primary number } } pageInfo { hasNextPage endCursor } } }"
}
```

#### 根据ID获取客户

```bash
POST /jobber/graphql
Content-Type: application/json

{
  "query": "query($id: EncodedId!) { client(id: $id) { id name emails { primary address } phones { primary number } billingAddress { street city } } }",
  "variables": { "id": "CLIENT_ID" }
}
```

#### 创建客户

```bash
POST /jobber/graphql
Content-Type: application/json

{
  "query": "mutation($input: ClientCreateInput!) { clientCreate(input: $input) { client { id name } userErrors { message path } } }",
  "variables": {
    "input": {
      "firstName": "John",
      "lastName": "Doe",
      "email": "john@example.com",
      "phone": "555-1234"
    }
  }
}
```

#### 更新客户信息

```bash
POST /jobber/graphql
Content-Type: application/json

{
  "query": "mutation($id: EncodedId!, $input: ClientUpdateInput!) { clientUpdate(clientId: $id, input: $input) { client { id name } userErrors { message path } } }",
  "variables": {
    "id": "CLIENT_ID",
    "input": {
      "email": "newemail@example.com"
    }
  }
}
```

### 任务操作

#### 列出任务

```bash
POST /jobber/graphql
Content-Type: application/json

{
  "query": "{ jobs(first: 20) { nodes { id title jobNumber jobStatus client { name } } pageInfo { hasNextPage endCursor } } }"
}
```

#### 根据ID获取任务

```bash
POST /jobber/graphql
Content-Type: application/json

{
  "query": "query($id: EncodedId!) { job(id: $id) { id title jobNumber jobStatus instructions client { name } property { address { street city } } } }",
  "variables": { "id": "JOB_ID" }
}
```

#### 创建任务

```bash
POST /jobber/graphql
Content-Type: application/json

{
  "query": "mutation($input: JobCreateInput!) { jobCreate(input: $input) { job { id jobNumber title } userErrors { message path } } }",
  "variables": {
    "input": {
      "clientId": "CLIENT_ID",
      "title": "Lawn Maintenance",
      "instructions": "Weekly lawn care service"
    }
  }
}
```

### 发票操作

#### 列出发票

```bash
POST /jobber/graphql
Content-Type: application/json

{
  "query": "{ invoices(first: 20) { nodes { id invoiceNumber subject total invoiceStatus client { name } } pageInfo { hasNextPage endCursor } } }"
}
```

#### 根据ID获取发票

```bash
POST /jobber/graphql
Content-Type: application/json

{
  "query": "query($id: EncodedId!) { invoice(id: $id) { id invoiceNumber subject total amountDue invoiceStatus lineItems { nodes { name quantity unitPrice } } } }",
  "variables": { "id": "INVOICE_ID" }
}
```

#### 创建发票

```bash
POST /jobber/graphql
Content-Type: application/json

{
  "query": "mutation($input: InvoiceCreateInput!) { invoiceCreate(input: $input) { invoice { id invoiceNumber } userErrors { message path } } }",
  "variables": {
    "input": {
      "clientId": "CLIENT_ID",
      "subject": "Service Invoice",
      "lineItems": [
        {
          "name": "Lawn Care",
          "quantity": 1,
          "unitPrice": 75.00
        }
      ]
    }
  }
}
```

### 报价单操作

#### 列出报价单

```bash
POST /jobber/graphql
Content-Type: application/json

{
  "query": "{ quotes(first: 20) { nodes { id quoteNumber title quoteStatus client { name } } pageInfo { hasNextPage endCursor } } }"
}
```

#### 创建报价单

```bash
POST /jobber/graphql
Content-Type: application/json

{
  "query": "mutation($input: QuoteCreateInput!) { quoteCreate(input: $input) { quote { id quoteNumber } userErrors { message path } } }",
  "variables": {
    "input": {
      "clientId": "CLIENT_ID",
      "title": "Landscaping Quote",
      "lineItems": [
        {
          "name": "Garden Design",
          "quantity": 1,
          "unitPrice": 500.00
        }
      ]
    }
  }
}
```

### 属性操作

#### 列出属性

```bash
POST /jobber/graphql
Content-Type: application/json

{
  "query": "{ properties(first: 20) { nodes { id address { street city state postalCode } client { name } } pageInfo { hasNextPage endCursor } } }"
}
```

### 请求操作

#### 列出请求

```bash
POST /jobber/graphql
Content-Type: application/json

{
  "query": "{ requests(first: 20) { nodes { id title requestStatus client { name } } pageInfo { hasNextPage endCursor } } }"
}
```

### 用户/团队操作

#### 列出用户

```bash
POST /jobber/graphql
Content-Type: application/json

{
  "query": "{ users(first: 50) { nodes { id name { full } email { raw } } } }"
}
```

### 自定义字段操作

#### 列出自定义字段

```bash
POST /jobber/graphql
Content-Type: application/json

{
  "query": "{ customFields(first: 50) { nodes { id name fieldType } } }"
}
```

## 分页

Jobber使用基于游标的分页机制（Relay风格）：

```bash
# First page
POST /jobber/graphql
{
  "query": "{ clients(first: 20) { nodes { id name } pageInfo { hasNextPage endCursor } } }"
}

# Next page using cursor
POST /jobber/graphql
{
  "query": "{ clients(first: 20, after: \"CURSOR_VALUE\") { nodes { id name } pageInfo { hasNextPage endCursor } } }"
}
```

响应中包含`pageInfo`信息：
```json
{
  "data": {
    "clients": {
      "nodes": [...],
      "pageInfo": {
        "hasNextPage": true,
        "endCursor": "abc123"
      }
    }
  }
}
```

## Webhooks

Jobber支持Webhooks以实现实时事件通知：

- `CLIENT_CREATE` - 新客户创建
- `JOB_COMPLETE` - 任务完成
- `QUOTE_CREATE` - 新报价单创建
- `QUOTE_APPROVAL` - 报价单被批准
- `REQUEST_CREATE` - 新请求创建
- `INVOICE_CREATE` - 新发票创建
- `APP_CONNECT` - 应用程序连接

Webhooks包含HMAC-SHA256签名以进行验证。

## 代码示例

### JavaScript

```javascript
const query = `{ clients(first: 10) { nodes { id name emails { address } } } }`;

const response = await fetch('https://gateway.maton.ai/jobber/graphql', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ query })
});

const data = await response.json();
```

### Python

```python
import os
import requests

query = '''
{
  clients(first: 10) {
    nodes { id name emails { address } }
  }
}
'''

response = requests.post(
    'https://gateway.maton.ai/jobber/graphql',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={'query': query}
)
data = response.json()
```

## 注意事项

- Jobber仅使用GraphQL API（不支持REST API）。
- 代理服务器会自动插入`X-JOBBER-GRAPHQL-VERSION`头部。
- 当前API版本为`2025-04-16`（最新版本）。
- 旧版本的API在发布后仍支持12至18个月。
- 可在Jobber的开发者中心使用GraphiQL浏览器来查看API架构。
- ID使用`EncodedId`类型（Base64编码），需以字符串形式传递。
- 字段命名规则：使用`emails`/`phones`（数组类型），`jobStatus`/`invoiceStatus`/`quoteStatus`/`requestStatus`等。
- 速率限制：
  - 防DDoS保护：每个应用程序/账户每5分钟最多2,500次请求。
  - 查询费用：基于“漏桶算法”计算（最多10,000点，每秒恢复500点）。
- 请避免使用深度嵌套的查询以降低查询成本。
- 重要提示：当将curl输出传递给`jq`或其他命令时，在某些shell环境中环境变量（如`$MATON_API_KEY`）可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立Jobber连接或查询格式错误 |
| 401 | Maton API密钥无效或缺失 |
| 403 | 未授权（请检查OAuth权限范围） |
| 429 | 超过速率限制 |
| 4xx/5xx | 来自Jobber API的传递错误 |

GraphQL错误会显示在响应体中：
```json
{
  "errors": [
    {
      "message": "Error description",
      "locations": [...],
      "path": [...]
    }
  ]
}
```

mutation错误会显示在`userErrors`字段中：
```json
{
  "data": {
    "clientCreate": {
      "client": null,
      "userErrors": [
        {
          "message": "Email is required",
          "path": ["input", "email"]
        }
      ]
    }
  }
}
```

### 故障排除：API密钥问题

1. 确保`MATON_API_KEY`环境变量已设置：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证API密钥的有效性：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用程序名称错误

1. 确保您的URL路径以`jobber`开头。例如：
  - 正确格式：`https://gateway.maton.ai/jobberGraphQL`
  - 错误格式：`https://gateway.maton.aigraphql`

## 资源

- [Jobber开发者文档](https://developer.getjobber.com/docs/)
- [快速入门指南](https://developer.getjobber.com/docs/getting_started/)
- [API支持](mailto:api-support@getjobber.com)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)