---
name: squareup
description: |
  Square API integration with managed OAuth. Process payments, manage customers, orders, catalog, inventory, and invoices.
  Use this skill when users want to accept payments, manage point-of-sale operations, track inventory, or handle invoicing through Square.
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

# Square

通过管理的OAuth认证来访问Square API。您可以处理支付、管理客户、订单、商品目录、库存和发票等信息。

## 快速入门

```bash
# List locations
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/squareup/v2/locations')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/squareup/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的Square API端点路径。该网关会将请求代理到 `connect_square.com` 并自动插入您的OAuth令牌。

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
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的Square OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=squareup&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'squareup'}).encode()
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
    "app": "squareup",
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

如果您有多个Square连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/squareup/v2/locations')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API参考

### 地点

#### 列出地点

```bash
GET /squareup/v2/locations
```

#### 获取地点信息

```bash
GET /squareup/v2/locations/{location_id}
```

#### 创建地点

```bash
POST /squareup/v2/locations
Content-Type: application/json

{
  "location": {
    "name": "New Location",
    "address": {
      "address_line_1": "123 Main St",
      "locality": "San Francisco",
      "administrative_district_level_1": "CA",
      "postal_code": "94102",
      "country": "US"
    }
  }
}
```

#### 更新地点信息

```bash
PUT /squareup/v2/locations/{location_id}
Content-Type: application/json

{
  "location": {
    "name": "Updated Location Name"
  }
}
```

### 商户

#### 获取商户信息

```bash
GET /squareup/v2/merchants/me
```

#### 列出商户

```bash
GET /squareup/v2/merchants
```

### 支付

#### 列出支付记录

```bash
GET /squareup/v2/payments
```

支持过滤：

```bash
GET /squareup/v2/payments?location_id={location_id}&begin_time=2026-01-01T00:00:00Z&end_time=2026-02-01T00:00:00Z
```

#### 获取支付信息

```bash
GET /squareup/v2/payments/{payment_id}
```

#### 创建支付记录

```bash
POST /squareup/v2/payments
Content-Type: application/json

{
  "source_id": "cnon:card-nonce-ok",
  "idempotency_key": "unique-key-12345",
  "amount_money": {
    "amount": 1000,
    "currency": "USD"
  },
  "location_id": "{location_id}"
}
```

#### 更新支付记录

```bash
PUT /squareup/v2/payments/{payment_id}
Content-Type: application/json

{
  "payment": {
    "tip_money": {
      "amount": 200,
      "currency": "USD"
    }
  },
  "idempotency_key": "unique-key-67890"
}
```

#### 完成支付

```bash
POST /squareup/v2/payments/{payment_id}/complete
Content-Type: application/json

{}
```

#### 取消支付

```bash
POST /squareup/v2/payments/{payment_id}/cancel
Content-Type: application/json

{}
```

### 退款

#### 列出退款记录

```bash
GET /squareup/v2/refunds
```

#### 获取退款信息

```bash
GET /squareup/v2/refunds/{refund_id}
```

#### 创建退款记录

```bash
POST /squareup/v2/refunds
Content-Type: application/json

{
  "idempotency_key": "unique-refund-key",
  "payment_id": "{payment_id}",
  "amount_money": {
    "amount": 500,
    "currency": "USD"
  },
  "reason": "Customer requested refund"
}
```

### 客户

#### 列出客户信息

```bash
GET /squareup/v2/customers
```

#### 获取客户信息

```bash
GET /squareup/v2/customers/{customer_id}
```

#### 创建客户

```bash
POST /squareup/v2/customers
Content-Type: application/json

{
  "given_name": "John",
  "family_name": "Doe",
  "email_address": "john.doe@example.com",
  "phone_number": "+15551234567"
}
```

#### 更新客户信息

```bash
PUT /squareup/v2/customers/{customer_id}
Content-Type: application/json

{
  "email_address": "john.updated@example.com"
}
```

#### 删除客户

```bash
DELETE /squareup/v2/customers/{customer_id}
```

#### 搜索客户

```bash
POST /squareup/v2/customers/search
Content-Type: application/json

{
  "query": {
    "filter": {
      "email_address": {
        "exact": "john.doe@example.com"
      }
    }
  }
}
```

### 订单

#### 创建订单

```bash
POST /squareup/v2/orders
Content-Type: application/json

{
  "order": {
    "location_id": "{location_id}",
    "line_items": [
      {
        "name": "Item 1",
        "quantity": "1",
        "base_price_money": {
          "amount": 1000,
          "currency": "USD"
        }
      }
    ]
  },
  "idempotency_key": "unique-order-key"
}
```

#### 获取订单信息

```bash
GET /squareup/v2/orders/{order_id}
```

#### 更新订单信息

```bash
PUT /squareup/v2/orders/{order_id}
Content-Type: application/json

{
  "order": {
    "location_id": "{location_id}",
    "version": 1
  },
  "fields_to_clear": ["line_items"]
}
```

#### 搜索订单

```bash
POST /squareup/v2/orders/search
Content-Type: application/json

{
  "location_ids": ["{location_id}"],
  "query": {
    "filter": {
      "state_filter": {
        "states": ["OPEN"]
      }
    }
  }
}
```

#### 批量获取订单信息

```bash
POST /squareup/v2/orders/batch-retrieve
Content-Type: application/json

{
  "location_id": "{location_id}",
  "order_ids": ["{order_id_1}", "{order_id_2}"]
}
```

### 商品目录

#### 列出商品目录

```bash
GET /squareup/v2/catalog/list
```

支持类型过滤：

```bash
GET /squareup/v2/catalog/list?types=ITEM,CATEGORY
```

#### 获取商品目录信息

```bash
GET /squareup/v2/catalog/object/{object_id}
```

#### 更新商品目录信息

```bash
POST /squareup/v2/catalog/object
Content-Type: application/json

{
  "idempotency_key": "unique-catalog-key",
  "object": {
    "type": "ITEM",
    "id": "#new-item",
    "item_data": {
      "name": "Coffee",
      "description": "Hot brewed coffee",
      "variations": [
        {
          "type": "ITEM_VARIATION",
          "id": "#small-coffee",
          "item_variation_data": {
            "name": "Small",
            "pricing_type": "FIXED_PRICING",
            "price_money": {
              "amount": 300,
              "currency": "USD"
            }
          }
        }
      ]
    }
  }
}
```

#### 删除商品目录信息

```bash
DELETE /squareup/v2/catalog/object/{object_id}
```

#### 批量更新商品目录信息

```bash
POST /squareup/v2/catalog/batch-upsert
Content-Type: application/json

{
  "idempotency_key": "unique-batch-key",
  "batches": [
    {
      "objects": [...]
    }
  ]
}
```

#### 搜索商品目录信息

```bash
POST /squareup/v2/catalog/search
Content-Type: application/json

{
  "object_types": ["ITEM"],
  "query": {
    "text_query": {
      "keywords": ["coffee"]
    }
  }
}
```

#### 获取商品目录详情

```bash
GET /squareup/v2/catalog/info
```

### 库存

#### 获取库存数量

```bash
GET /squareup/v2/inventory/{catalog_object_id}
```

#### 批量获取库存数量

```bash
POST /squareup/v2/inventory/counts/batch-retrieve
Content-Type: application/json

{
  "catalog_object_ids": ["{object_id_1}", "{object_id_2}"],
  "location_ids": ["{location_id}"]
}
```

#### 批量修改库存信息

```bash
POST /squareup/v2/inventory/changes/batch-create
Content-Type: application/json

{
  "idempotency_key": "unique-inventory-key",
  "changes": [
    {
      "type": "ADJUSTMENT",
      "adjustment": {
        "catalog_object_id": "{object_id}",
        "location_id": "{location_id}",
        "quantity": "10",
        "from_state": "NONE",
        "to_state": "IN_STOCK"
      }
    }
  ]
}
```

#### 获取库存调整信息

```bash
GET /squareup/v2/inventory/adjustments/{adjustment_id}
```

### 发票

#### 列出发票记录

```bash
GET /squareup/v2/invoices?location_id={location_id}
```

#### 获取发票信息

```bash
GET /squareup/v2/invoices/{invoice_id}
```

#### 创建发票

```bash
POST /squareup/v2/invoices
Content-Type: application/json

{
  "invoice": {
    "location_id": "{location_id}",
    "order_id": "{order_id}",
    "primary_recipient": {
      "customer_id": "{customer_id}"
    },
    "payment_requests": [
      {
        "request_type": "BALANCE",
        "due_date": "2026-02-15"
      }
    ],
    "delivery_method": "EMAIL"
  },
  "idempotency_key": "unique-invoice-key"
}
```

#### 更新发票信息

```bash
PUT /squareup/v2/invoices/{invoice_id}
Content-Type: application/json

{
  "invoice": {
    "version": 1,
    "payment_requests": [
      {
        "uid": "{payment_request_uid}",
        "due_date": "2026-02-20"
      }
    ]
  },
  "idempotency_key": "unique-update-key"
}
```

#### 发布发票

```bash
POST /squareup/v2/invoices/{invoice_id}/publish
Content-Type: application/json

{
  "version": 1,
  "idempotency_key": "unique-publish-key"
}
```

#### 取消发票

```bash
POST /squareup/v2/invoices/{invoice_id}/cancel
Content-Type: application/json

{
  "version": 1
}
```

#### 删除发票

```bash
DELETE /squareup/v2/invoices/{invoice_id}?version=1
```

#### 搜索发票记录

```bash
POST /squareup/v2/invoices/search
Content-Type: application/json

{
  "query": {
    "filter": {
      "location_ids": ["{location_id}"],
      "customer_ids": ["{customer_id}"]
    }
  }
}
```

## 分页

Square使用基于游标的分页机制。当存在更多结果时，列表端点会返回一个 `cursor` 字段：

```bash
GET /squareup/v2/payments?cursor={cursor_value}
```

响应中包含分页信息：

```json
{
  "payments": [...],
  "cursor": "next_page_cursor_value"
}
```

通过在后续请求中传递 `cursor` 值来继续获取数据，直到不再返回 `cursor`。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/squareup/v2/locations',
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
    'https://gateway.maton.ai/squareup/v2/locations',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

## 注意事项

- 所有金额均以最小货币单位表示（例如，USD的1000表示$10.00）。
- ID为字母数字字符串。
- 时间戳采用ISO 8601格式（例如：`2026-02-07T01:59:28.459Z`）。
- 大多数写入操作需要 `idempotency_key` 以防止重复操作。
- 某些端点需要特定的OAuth权限范围（如 `CUSTOMERS_READ`、`ORDERS_READ`、`ITEMS_READ`、`INVOICES_READ`等）。
- 重要提示：当URL包含括号时，使用 `curl -g` 可以防止全局解析。
- 重要提示：在将curl输出传递给 `jq` 或其他命令时，环境变量（如 `$MATON_API_KEY`）可能在某些shell环境中无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立Square连接或请求无效 |
| 401 | Maton API密钥无效或缺失 |
| 403 | OAuth权限范围不足 |
| 404 | 资源未找到 |
| 429 | 请求次数限制 |
| 4xx/5xx | 来自Square API的传递错误 |

### 错误响应格式

```json
{
  "errors": [
    {
      "category": "INVALID_REQUEST_ERROR",
      "code": "NOT_FOUND",
      "detail": "Could not find payment with id: {payment_id}"
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

### 故障排除：应用名称无效

1. 确保您的URL路径以 `squareup` 开头。例如：
   - 正确：`https://gateway.maton.ai/squareup/v2/locations`
   - 错误：`https://gateway.maton.ai/v2/locations`

### 故障排除：权限范围不足

如果收到 `INSUFFICIENT_SCOPES` 的错误，说明OAuth连接没有所需的权限。请创建新的连接并在OAuth认证过程中授予所有必要的权限。

## 资源

- [Square API概述](https://developer.square.com/docs)
- [Square API参考](https://developer.square.com/reference/square)
- [支付API](https://developer.square.com/reference/square/payments-api)
- [客户API](https://developer.square.com/reference/square/customers-api)
- [订单API](https://developer.square.com/reference/square/orders-api)
- [商品目录API](https://developer.square.com/reference/square/catalog-api)
- [库存API](https://developer.square.com/reference/square/inventory-api)
- [发票API](https://developer.square.com/reference/square/invoices-api)
- [地点API](https://developer.square.com/reference/square/locations-api)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)