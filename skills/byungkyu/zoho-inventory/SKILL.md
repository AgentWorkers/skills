---
name: zoho-inventory
description: |
  Zoho Inventory API integration with managed OAuth. Manage items, sales orders, invoices, purchase orders, bills, contacts, and shipments.
  Use this skill when users want to read, create, update, or delete inventory items, sales orders, invoices, purchase orders, bills, or other inventory records in Zoho Inventory.
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

# Zoho Inventory

您可以使用受管理的 OAuth 认证来访问 Zoho Inventory API。通过该 API，您可以执行创建（Create）、读取（Read）、更新（Update）和删除（Delete，简称 CRUD）操作，以管理商品、销售订单、发票、采购订单、账单、联系人、发货订单以及商品组。

## 快速入门

```bash
# List items
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-inventory/inventory/v1/items')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/zoho-inventory/inventory/v1/{endpoint}
```

该网关会将请求代理到 `www.zohoapis.com/inventory/v1`，并自动插入您的 OAuth 令牌。

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

1. 在 [maton.ai](https://maton.ai) 上登录或创建帐户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的 Zoho Inventory OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=zoho-inventory&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'zoho-inventory'}).encode()
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
    "app": "zoho-inventory",
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

如果您有多个 Zoho Inventory 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-inventory/inventory/v1/items')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 可用模块

| 模块 | 端点 | 描述 |
|--------|----------|-------------|
| 商品 | `/items` | 产品和服务 |
| 商品组 | `/itemgroups` | 分组的产品变体 |
| 联系人 | `/contacts` | 客户和供应商 |
| 销售订单 | `/salesorders` | 销售订单 |
| 发票 | `/invoices` | 销售发票 |
| 采购订单 | `/purchaseorders` | 采购订单 |
| 账单 | `/bills` | 供应商账单 |
| 发货订单 | `/shipmentorders` | 发货跟踪 |

### 商品

#### 列出商品

```bash
GET /zoho-inventory/inventory/v1/items
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-inventory/inventory/v1/items')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "code": 0,
  "message": "success",
  "items": [
    {
      "item_id": "1234567890000",
      "name": "Widget",
      "status": "active",
      "sku": "WDG-001",
      "rate": 25.00,
      "purchase_rate": 10.00,
      "is_taxable": true
    }
  ],
  "page_context": {
    "page": 1,
    "per_page": 200,
    "has_more_page": false
  }
}
```

#### 获取商品信息

```bash
GET /zoho-inventory/inventory/v1/items/{item_id}
```

#### 创建商品

```bash
POST /zoho-inventory/inventory/v1/items
Content-Type: application/json

{
  "name": "Widget",
  "rate": 25.00,
  "purchase_rate": 10.00,
  "sku": "WDG-001",
  "item_type": "inventory",
  "product_type": "goods",
  "unit": "pcs",
  "is_taxable": true
}
```

**必填字段：**
- `name` - 商品名称

**可选字段：**
- `rate` - 销售价格
- `purchase_rate` - 采购成本
- `sku` - 库存单位（唯一）
- `item_type` - `inventory`、`sales`、`purchases` 或 `sales_and_purchases`
- `product_type` - `goods` 或 `service`
- `unit` - 计量单位
- `is_taxable` - 是否征税
- `tax_id` - 税务标识符
- `description` - 商品描述
- `reorder_level` - 重新订购点
- `vendor_id` - 首选供应商

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "name": "Widget",
    "rate": 25.00,
    "purchase_rate": 10.00,
    "sku": "WDG-001",
    "item_type": "inventory",
    "product_type": "goods",
    "unit": "pcs"
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-inventory/inventory/v1/items', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "code": 0,
  "message": "The item has been added.",
  "item": {
    "item_id": "1234567890000",
    "name": "Widget",
    "status": "active",
    "rate": 25.00,
    "purchase_rate": 10.00,
    "sku": "WDG-001"
  }
}
```

#### 更新商品信息

```bash
PUT /zoho-inventory/inventory/v1/items/{item_id}
Content-Type: application/json

{
  "name": "Updated Widget",
  "rate": 30.00
}
```

#### 删除商品

```bash
DELETE /zoho-inventory/inventory/v1/items/{item_id}
```

#### 商品状态操作

```bash
# Mark as active
POST /zoho-inventory/inventory/v1/items/{item_id}/active

# Mark as inactive
POST /zoho-inventory/inventory/v1/items/{item_id}/inactive
```

### 联系人

#### 列出联系人

```bash
GET /zoho-inventory/inventory/v1/contacts
```

**查询参数：**
- `filter_by` - `Status.All`、`Status.Active`、`Status.Inactive`、`Status.Duplicate`、`Status.Crm`
- `search_text` - 在联系人字段中搜索
- `sort_column` - `contact_name`、`first_name`、`last_name`、`email`、`created_time`、`last_modified_time`
- `contact_name`、`company_name`、`email`、`phone` - 特定字段的过滤器

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-inventory/inventory/v1/contacts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取联系人信息

```bash
GET /zoho-inventory/inventory/v1/contacts/{contact_id}
```

#### 创建联系人

```bash
POST /zoho-inventory/inventory/v1/contacts
Content-Type: application/json

{
  "contact_name": "Acme Corporation",
  "contact_type": "customer",
  "company_name": "Acme Corp",
  "email": "billing@acme.com",
  "phone": "+1-555-1234"
}
```

**必填字段：**
- `contact_name` - 显示名称

**可选字段：**
- `contact_type` - `customer` 或 `vendor`
- `company_name` - 法人实体名称
- `email` - 电子邮件地址
- `phone` - 电话号码
- `billing_address` - 收货地址
- `shipping_address` - 发货地址
- `payment_terms` - 支付期限
- `currency_id` - 货币标识符
- `website` - 网站地址

#### 更新联系人信息

```bash
PUT /zoho-inventory/inventory/v1/contacts/{contact_id}
```

#### 删除联系人

```bash
DELETE /zoho-inventory/inventory/v1/contacts/{contact_id}
```

#### 联系人状态操作

```bash
# Mark as active
POST /zoho-inventory/inventory/v1/contacts/{contact_id}/active

# Mark as inactive
POST /zoho-inventory/inventory/v1/contacts/{contact_id}/inactive
```

### 销售订单

#### 列出销售订单

```bash
GET /zoho-inventory/inventory/v1/salesorders
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-inventory/inventory/v1/salesorders')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取销售订单信息

```bash
GET /zoho-inventory/inventory/v1/salesorders/{salesorder_id}
```

#### 创建销售订单

```bash
POST /zoho-inventory/inventory/v1/salesorders
Content-Type: application/json

{
  "customer_id": "1234567890000",
  "date": "2026-02-06",
  "line_items": [
    {
      "item_id": "1234567890001",
      "quantity": 5,
      "rate": 25.00
    }
  ]
}
```

**必填字段：**
- `customer_id` - 客户标识符
- `line_items` - 包含 `item_id`、`quantity`、`rate` 的商品数组

**可选字段：**
- `salesorder_number` - 如果未指定，则自动生成（如果启用了自动生成功能，请勿指定）
- `date` - 订单日期（格式为 yyyy-mm-dd）
- `shipment_date` - 预计发货日期
- `reference_number` - 外部参考编号
- `notes` - 内部备注
- `terms` - 条款和条件
- `discount` - 折扣百分比或金额
- `shipping_charge` - 运费
- `adjustment` - 价格调整

#### 更新销售订单信息

```bash
PUT /zoho-inventory/inventory/v1/salesorders/{salesorder_id}
```

#### 删除销售订单

```bash
DELETE /zoho-inventory/inventory/v1/salesorders/{salesorder_id}
```

#### 销售订单状态操作

```bash
# Mark as confirmed
POST /zoho-inventory/inventory/v1/salesorders/{salesorder_id}/status/confirmed

# Mark as void
POST /zoho-inventory/inventory/v1/salesorders/{salesorder_id}/status/void
```

### 发票

#### 列出发票

```bash
GET /zoho-inventory/inventory/v1/invoices
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-inventory/inventory/v1/invoices')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取发票信息

```bash
GET /zoho-inventory/inventory/v1/invoices/{invoice_id}
```

#### 创建发票

```bash
POST /zoho-inventory/inventory/v1/invoices
Content-Type: application/json

{
  "customer_id": "1234567890000",
  "line_items": [
    {
      "item_id": "1234567890001",
      "quantity": 5,
      "rate": 25.00
    }
  ]
}
```

**必填字段：**
- `customer_id` - 客户标识符
- `line_items` - 商品数组

**可选字段：**
- `invoice_number` - 如果未指定，则自动生成
- `date` - 发票日期（格式为 yyyy-mm-dd）
- `due_date` - 应付日期
- `payment_terms` - 截止付款日期
- `discount` - 折扣百分比或金额
- `shipping_charge` - 运费
- `notes` - 内部备注
- `terms` - 条款和条件

#### 更新发票信息

```bash
PUT /zoho-inventory/inventory/v1/invoices/{invoice_id}
```

#### 删除发票

```bash
DELETE /zoho-inventory/inventory/v1/invoices/{invoice_id}
```

#### 发票状态操作

```bash
# Mark as sent
POST /zoho-inventory/inventory/v1/invoices/{invoice_id}/status/sent

# Mark as draft
POST /zoho-inventory/inventory/v1/invoices/{invoice_id}/status/draft

# Void invoice
POST /zoho-inventory/inventory/v1/invoices/{invoice_id}/status/void
```

#### 发票电子邮件

```bash
# Email invoice to customer
POST /zoho-inventory/inventory/v1/invoices/{invoice_id}/email

# Get email content template
GET /zoho-inventory/inventory/v1/invoices/{invoice_id}/email
```

#### 发票付款

```bash
# List payments applied
GET /zoho-inventory/inventory/v1/invoices/{invoice_id}/payments

# Delete a payment
DELETE /zoho-inventory/inventory/v1/invoices/{invoice_id}/payments/{invoice_payment_id}
```

#### 发票退款

```bash
# List credits applied
GET /zoho-inventory/inventory/v1/invoices/{invoice_id}/creditsapplied

# Apply credits
POST /zoho-inventory/inventory/v1/invoices/{invoice_id}/credits

# Delete applied credit
DELETE /zoho-inventory/inventory/v1/invoices/{invoice_id}/creditsapplied/{creditnotes_invoice_id}
```

#### 发票备注

```bash
# List comments
GET /zoho-inventory/inventory/v1/invoices/{invoice_id}/comments

# Add comment
POST /zoho-inventory/inventory/v1/invoices/{invoice_id}/comments

# Update comment
PUT /zoho-inventory/inventory/v1/invoices/{invoice_id}/comments/{comment_id}

# Delete comment
DELETE /zoho-inventory/inventory/v1/invoices/{invoice_id}/comments/{comment_id}
```

### 采购订单

#### 列出采购订单

```bash
GET /zoho-inventory/inventory/v1/purchaseorders
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-inventory/inventory/v1/purchaseorders')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取采购订单信息

```bash
GET /zoho-inventory/inventory/v1/purchaseorders/{purchaseorder_id}
```

#### 创建采购订单

```bash
POST /zoho-inventory/inventory/v1/purchaseorders
Content-Type: application/json

{
  "vendor_id": "1234567890000",
  "line_items": [
    {
      "item_id": "1234567890001",
      "quantity": 100,
      "rate": 10.00
    }
  ]
}
```

**必填字段：**
- `vendor_id` - 供应商标识符
- `line_items` - 商品数组

**可选字段：**
- `purchaseorder_number` - 如果未指定，则自动生成（如果启用了自动生成功能，请勿指定）
- `date` - 订单日期（格式为 yyyy-mm-dd）
- `delivery_date` - 预计交货日期
- `reference_number` - 外部参考编号
- `ship_via` - 运输方式
- `notes` - 内部备注
- `terms` - 条款和条件

#### 更新采购订单信息

```bash
PUT /zoho-inventory/inventory/v1/purchaseorders/{purchaseorder_id}
```

#### 删除采购订单

```bash
DELETE /zoho-inventory/inventory/v1/purchaseorders/{purchaseorder_id}
```

#### 采购订单状态操作

```bash
# Mark as issued
POST /zoho-inventory/inventory/v1/purchaseorders/{purchaseorder_id}/status/issued

# Mark as cancelled
POST /zoho-inventory/inventory/v1/purchaseorders/{purchaseorder_id}/status/cancelled
```

### 账单

#### 列出账单

```bash
GET /zoho-inventory/inventory/v1/bills
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-inventory/inventory/v1/bills')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取账单信息

```bash
GET /zoho-inventory/inventory/v1/bills/{bill_id}
```

#### 创建账单

```bash
POST /zoho-inventory/inventory/v1/bills
Content-Type: application/json

{
  "vendor_id": "1234567890000",
  "bill_number": "BILL-001",
  "date": "2026-02-06",
  "due_date": "2026-03-06",
  "line_items": [
    {
      "item_id": "1234567890001",
      "quantity": 100,
      "rate": 10.00
    }
  ]
}
```

**必填字段：**
- `vendor_id` - 供应商标识符
- `bill_number` - 唯一的账单编号（必填，不会自动生成）
- `date` - 账单日期（格式为 yyyy-mm-dd）
- `due_date` - 应付日期
- `line_items` - 商品数组

**可选字段：**
- `reference_number` - 外部参考编号
- `notes` - 内部备注
- `terms` - 条款和条件
- `currency_id` - 货币标识符
- `exchange_rate` - 外币汇率

#### 更新账单信息

```bash
PUT /zoho-inventory/inventory/v1/bills/{bill_id}
```

#### 删除账单

```bash
DELETE /zoho-inventory/inventory/v1/bills/{bill_id}
```

#### 账单状态操作

```bash
# Mark as open
POST /zoho-inventory/inventory/v1/bills/{bill_id}/status/open

# Mark as void
POST /zoho-inventory/inventory/v1/bills/{bill_id}/status/void
```

### 发货订单

#### 创建发货订单

```bash
POST /zoho-inventory/inventory/v1/shipmentorders
Content-Type: application/json

{
  "shipment_number": "SHP-001",
  "date": "2026-02-06",
  "delivery_method": "FedEx",
  "tracking_number": "1234567890"
}
```

**必填字段：**
- `shipment_number` - 唯一的发货订单编号
- `date` - 发货日期
- `delivery_method` - 运输方式

**可选字段：**
- `tracking_number` - 运输公司的跟踪编号
- `shipping_charge` - 运费
- `notes` - 内部备注
- `reference_number` - 外部参考编号

#### 获取发货订单信息

```bash
GET /zoho-inventory/inventory/v1/shipmentorders/{shipmentorder_id}
```

#### 更新发货订单信息

```bash
PUT /zoho-inventory/inventory/v1/shipmentorders/{shipmentorder_id}
```

#### 删除发货订单

```bash
DELETE /zoho-inventory/inventory/v1/shipmentorders/{shipmentorder_id}
```

#### 标记为已交付

```bash
POST /zoho-inventory/inventory/v1/shipmentorders/{shipmentorder_id}/status/delivered
```

### 商品组

#### 列出商品组

```bash
GET /zoho-inventory/inventory/v1/itemgroups
```

#### 获取商品组信息

```bash
GET /zoho-inventory/inventory/v1/itemgroups/{itemgroup_id}
```

#### 创建商品组

```bash
POST /zoho-inventory/inventory/v1/itemgroups
Content-Type: application/json

{
  "group_name": "T-Shirts",
  "unit": "pcs",
  "items": [
    {
      "name": "T-Shirt - Small",
      "rate": 20.00,
      "purchase_rate": 8.00,
      "sku": "TS-S"
    },
    {
      "name": "T-Shirt - Medium",
      "rate": 20.00,
      "purchase_rate": 8.00,
      "sku": "TS-M"
    }
  ]
}
```

**必填字段：**
- `group_name` - 组名称
- `unit` - 计量单位

#### 更新商品组信息

```bash
PUT /zoho-inventory/inventory/v1/itemgroups/{itemgroup_id}
```

#### 删除商品组

```bash
DELETE /zoho-inventory/inventory/v1/itemgroups/{itemgroup_id}
```

#### 商品组状态操作

```bash
# Mark as active
POST /zoho-inventory/inventory/v1/itemgroups/{itemgroup_id}/active

# Mark as inactive
POST /zoho-inventory/inventory/v1/itemgroups/{itemgroup_id}/inactive
```

## 分页

Zoho Inventory 使用基于页面的分页机制：

```bash
GET /zoho-inventory/inventory/v1/items?page=1&per_page=50
```

响应中包含 `page_context` 中的分页信息：

```json
{
  "code": 0,
  "message": "success",
  "items": [...],
  "page_context": {
    "page": 1,
    "per_page": 50,
    "has_more_page": true,
    "sort_column": "name",
    "sort_order": "A"
  }
}
```

当 `has_more_page` 为 `true` 时，继续获取更多数据，并每次递增 `page` 的值。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/zoho-inventory/inventory/v1/items',
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
    'https://gateway.maton.ai/zoho-inventory/inventory/v1/items',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

## 注意事项

- 所有成功的响应都会包含 `code: 0` 和 `message` 字段。
- 日期应采用 `yyyy-mm-dd` 的格式。
- 联系人类型为 `customer` 或 `vendor`。
- 商品类型包括 `inventory`、`sales`、`purchases`、`sales_and_purchases`。
- 产品类型包括 `goods` 或 `service`。
- `organization_id` 参数由网关自动处理，您无需手动指定。
- 销售订单和采购订单编号会自动生成——除非在设置中禁用了自动生成功能，否则无需指定 `salesorder_number` 或 `purchaseorder_number`。
- 状态操作端点使用 POST 方法（例如 `/status/confirmed`、`/status/void`）。
- 每个组织的请求速率限制为每分钟 100 次。
- 每日的请求限制因计划而异：免费计划（1,000 次）、标准计划（2,500 次）、专业计划（5,000 次）、高级计划（7,500 次）、企业计划（10,000 次）。
- 重要提示：当使用 `curl` 命令时，如果 URL 中包含括号，请使用 `curl -g` 以禁用全局解析。
- 重要提示：当将 `curl` 的输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Zoho Inventory 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失，或者 OAuth 范围不匹配 |
| 404 | 资源未找到 |
| 429 | 请求次数达到限制 |
| 4xx/5xx | 来自 Zoho Inventory API 的传递错误 |

### 常见错误代码

| 代码 | 描述 |
|------|-------------|
| 0 | 操作成功 |
| 1 | 值无效 |
| 2 | 必填字段缺失 |
| 3 | 资源不存在 |
| 5 | URL 无效 |

### 故障排除：API 密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

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

### 故障排除：应用程序名称无效

1. 确保您的 URL 路径以 `zoho-inventory` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/zoho-inventory/inventory/v1/items`
- 错误的路径：`https://gateway.maton.ai/inventory/v1/items`

## 资源

- [Zoho Inventory API v1 简介](https://www.zoho.com/inventory/api/v1/introduction/)
- [Zoho Inventory 商品 API](https://www.zoho.com/inventory/api/v1/items/)
- [Zoho Inventory 联系人 API](https://www.zoho.com/inventory/api/v1/contacts/)
- [Zoho Inventory 销售订单 API](https://www.zoho.com/inventory/api/v1/salesorders/)
- [Zoho Inventory 发票 API](https://www.zoho.com/inventory/api/v1/invoices/)
- [Zoho Inventory 采购订单 API](https://www.zoho.com/inventory/api/v1/purchaseorders/)
- [Zoho Inventory 账单 API](https://www.zoho.com/inventory/api/v1/bills/)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)