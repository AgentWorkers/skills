---
name: zoho-books
description: |
  Zoho Books API integration with managed OAuth. Manage invoices, contacts, bills, expenses, and other accounting data.
  Use this skill when users want to read, create, update, or delete invoices, contacts, bills, expenses, or other financial records in Zoho Books.
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

# Zoho Books

您可以使用托管的 OAuth 认证来访问 Zoho Books API。该 API 支持对发票、联系人、账单、费用、销售订单、采购订单以及其他会计数据进行完整的 CRUD 操作（创建、读取、更新、删除）。

## 快速入门

```bash
# List contacts
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-books/books/v3/contacts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/zoho-books/books/v3/{endpoint}
```

该网关会将请求代理到 `www.zohoapis.com/books/v3`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取您的 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的 Zoho Books OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=zoho-books&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'zoho-books'}).encode()
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
    "app": "zoho-books",
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

如果您有多个 Zoho Books 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-books/books/v3/contacts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 可用模块

Zoho Books 将数据组织成多个模块。主要模块包括：

| 模块 | 端点 | 描述 |
|--------|----------|-------------|
| 联系人 | `/contacts` | 客户和供应商信息 |
| 发票 | `/invoices` | 销售发票 |
| 账单 | `/bills` | 供应商账单 |
| 费用 | `/expenses` | 商业费用 |
| 销售订单 | `/salesorders` | 销售订单 |
| 采购订单 | `/purchaseorders` | 采购订单 |
| 信用票据 | `/creditnotes` | 客户信用票据 |
| 定期发票 | `/recurringinvoices` | 自动生成的定期发票 |
| 定期账单 | `/recurringbills` | 自动生成的定期账单 |

### 联系人

#### 列出联系人

```bash
GET /zoho-books/books/v3/contacts
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-books/books/v3/contacts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "code": 0,
  "message": "success",
  "contacts": [...],
  "page_context": {
    "page": 1,
    "per_page": 200,
    "has_more_page": false,
    "sort_column": "contact_name",
    "sort_order": "A"
  }
}
```

#### 获取联系人信息

```bash
GET /zoho-books/books/v3/contacts/{contact_id}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-books/books/v3/contacts/8527119000000099001')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建联系人

```bash
POST /zoho-books/books/v3/contacts
Content-Type: application/json

{
  "contact_name": "Customer Name",
  "contact_type": "customer"
}
```

**必填字段：**
- `contact_name` - 联系人的显示名称
- `contact_type` - `customer` 或 `vendor`（客户或供应商）

**可选字段：**
- `company_name` - 法定实体名称
- `email` - 电子邮件地址
- `phone` - 电话号码
- `billing_address` - 支付地址
- `payment_terms` - 支付期限

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "contact_name": "Acme Corporation",
    "contact_type": "customer",
    "company_name": "Acme Corp",
    "email": "billing@acme.com",
    "phone": "+1-555-1234"
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-books/books/v3/contacts', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "code": 0,
  "message": "The contact has been added.",
  "contact": {
    "contact_id": "8527119000000099001",
    "contact_name": "Acme Corporation",
    "company_name": "Acme Corp",
    "contact_type": "customer",
    ...
  }
}
```

#### 更新联系人信息

```bash
PUT /zoho-books/books/v3/contacts/{contact_id}
Content-Type: application/json

{
  "contact_name": "Updated Name",
  "phone": "+1-555-9999"
}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "contact_name": "Acme Corporation Updated",
    "phone": "+1-555-9999"
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-books/books/v3/contacts/8527119000000099001', data=data, method='PUT')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 删除联系人

```bash
DELETE /zoho-books/books/v3/contacts/{contact_id}
```

**示例：**

**响应：**
```json
{
  "code": 0,
  "message": "The customer has been deleted."
}
```

### 发票

#### 列出发票

```bash
GET /zoho-books/books/v3/invoices
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-books/books/v3/invoices')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取发票信息

```bash
GET /zoho-books/books/v3/invoices/{invoice_id}
```

#### 创建发票

```bash
POST /zoho-books/books/v3/invoices
Content-Type: application/json

{
  "customer_id": "8527119000000099001",
  "line_items": [
    {
      "item_id": "8527119000000100001",
      "quantity": 1,
      "rate": 100.00
    }
  ]
}
```

**必填字段：**
- `customer_id` - 客户标识符
- `line_items` - 包含 `item_id` 的项目数组或手动输入的项目

**可选字段：**
- `invoice_number` - 如果未指定，则自动生成
- `date` - 发票日期（格式为 yyyy-mm-dd）
- `due_date` - 应付款日期
- `discount` - 折扣百分比或固定金额
- `payment_terms` - 到期付款天数

#### 更新发票

```bash
PUT /zoho-books/books/v3/invoices/{invoice_id}
```

#### 删除发票

```bash
DELETE /zoho-books/books/v3/invoices/{invoice_id}
```

#### 发票操作

```bash
# Mark as sent
POST /zoho-books/books/v3/invoices/{invoice_id}/status/sent

# Void invoice
POST /zoho-books/books/v3/invoices/{invoice_id}/status/void

# Email invoice
POST /zoho-books/books/v3/invoices/{invoice_id}/email
```

### 账单

#### 列出账单

```bash
GET /zoho-books/books/v3/bills
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-books/books/v3/bills')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建账单

```bash
POST /zoho-books/books/v3/bills
Content-Type: application/json

{
  "vendor_id": "8527119000000099002",
  "bill_number": "BILL-001",
  "date": "2026-02-06",
  "line_items": [
    {
      "account_id": "8527119000000100002",
      "description": "Office Supplies",
      "amount": 150.00
    }
  ]
}
```

**必填字段：**
- `vendor_id` - 供应商标识符
- `bill_number` - 独立的账单编号
- `date` - 账单日期（格式为 yyyy-mm-dd）

#### 更新账单

```bash
PUT /zoho-books/books/v3/bills/{bill_id}
```

#### 删除账单

```bash
DELETE /zoho-books/books/v3/bills/{bill_id}
```

### 费用

#### 列出费用

```bash
GET /zoho-books/books/v3/expenses
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-books/books/v3/expenses')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建费用记录

```bash
POST /zoho-books/books/v3/expenses
Content-Type: application/json

{
  "account_id": "8527119000000100003",
  "date": "2026-02-06",
  "amount": 75.50,
  "paid_through_account_id": "8527119000000100004",
  "description": "Business lunch"
}
```

**必填字段：**
- `account_id` - 费用账户 ID
- `date` - 费用发生日期（格式为 yyyy-mm-dd）
- `amount` - 费用金额
- `paid_through_account_id` - 支付账户 ID

**可选字段：**
- `description` - 费用详情
- `customer_id` - 可计费的客户 ID
- `is_billable` - 是否可计费的费用
- `project_id` - 关联的项目

#### 更新费用记录

```bash
PUT /zoho-books/books/v3/expenses/{expense_id}
```

#### 删除费用记录

```bash
DELETE /zoho-books/books/v3/expenses/{expense_id}
```

### 销售订单

#### 列出销售订单

```bash
GET /zoho-books/books/v3/salesorders
```

#### 创建销售订单

```bash
POST /zoho-books/books/v3/salesorders
```

### 采购订单

#### 列出采购订单

```bash
GET /zoho-books/books/v3/purchaseorders
```

#### 创建采购订单

```bash
POST /zoho-books/books/v3/purchaseorders
```

### 信用票据

#### 列出信用票据

```bash
GET /zoho-books/books/v3/creditnotes
```

### 定期发票

#### 列出定期发票

```bash
GET /zoho-books/books/v3/recurringinvoices
```

### 定期账单

#### 列出定期账单

```bash
GET /zoho-books/books/v3/recurringbills
```

## 分页

Zoho Books 使用基于页面的分页机制：

```bash
GET /zoho-books/books/v3/contacts?page=1&per_page=50
```

响应中包含 `page_context` 中的分页信息：

```json
{
  "code": 0,
  "message": "success",
  "contacts": [...],
  "page_context": {
    "page": 1,
    "per_page": 50,
    "has_more_page": true,
    "sort_column": "contact_name",
    "sort_order": "A"
  }
}
```

当 `has_more_page` 为 `true` 时，继续获取数据，并每次迭代时递增 `page` 的值。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/zoho-books/books/v3/contacts',
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
    'https://gateway.maton.ai/zoho-books/books/v3/contacts',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

## 注意事项：

- 所有成功的响应都会包含 `code: 0` 和 `message` 字段。
- 日期应采用 `yyyy-mm-dd` 的格式。
- 联系人类型可以是 `customer` 或 `vendor`。
- 某些模块（如项目、银行账户等）可能需要额外的 OAuth 权限范围。如果您收到权限范围错误，请通过 support@maton.ai 联系 Maton 支持团队，提供所需的操作/API 以及您的使用场景。
- 请求速率限制：每个组织每分钟 100 次请求。
- 每日的请求限制因套餐而异：免费套餐（1,000 次）、标准套餐（2,000 次）、专业套餐（5,000 次）、高级套餐（10,000 次）。
- 重要提示：当 URL 中包含括号时，使用 `curl -g` 选项来禁用全局解析。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Zoho Books 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失，或者 OAuth 权限范围不匹配 |
| 404 | 资源未找到 |
| 429 | 请求超出速率限制 |
| 4xx/5xx | 来自 Zoho Books API 的传递错误 |

### 常见错误代码

| 代码 | 描述 |
|------|-------------|
| 0 | 操作成功 |
| 57 | 未授权（OAuth 权限范围不匹配） |
| 1 | 输入的值无效 |
| 2 | 必填字段缺失 |
| 3 | 资源不存在 |
| 5 | URL 错误 |

### 故障排除：

- **API 密钥问题：**
  1. 确保设置了 `MATON_API_KEY` 环境变量。
  2. 通过列出连接来验证 API 密钥是否有效。

- **应用程序名称错误：**
  1. 确保您的 URL 路径以 `zoho-books` 开头。例如：
    - 正确的路径：`https://gateway.maton.ai/zoho-books/books/v3/contacts`
    - 错误的路径：`https://gateway.maton.ai/books/v3/contacts`

## 资源：

- [Zoho Books API v3 介绍](https://www.zoho.com/books/api/v3/introduction/)
- [Zoho Books 发票 API](https://www.zoho.com/books/api/v3/invoices/)
- [Zoho Books 联系人 API](https://www.zoho.com/books/api/v3/contacts/)
- [Zoho Books 账单 API](https://www.zoho.com/books/api/v3/bills/)
- [Zoho Books 费用 API](https://www.zoho.com/books/api/v3/expenses/)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持团队](mailto:support@maton.ai)