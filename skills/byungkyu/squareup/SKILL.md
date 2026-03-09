---
name: squareup
description: >
  **Square API集成与托管型OAuth**  
  支持处理支付、管理客户信息、订单、商品目录、库存、发票、会员积分计划以及团队成员等数据。  
  当用户需要通过Square接受支付、管理销售点操作、追踪库存、处理发票或创建支付链接时，可使用此功能。  
  对于其他第三方应用程序，建议使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。  
  该功能需要网络连接以及有效的Maton API密钥。
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

您可以使用管理的 OAuth 认证来访问 Square API，从而处理支付、管理客户、订单、商品目录、库存和发票等操作。

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

## 基本 URL

```
https://gateway.maton.ai/squareup/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Square API 端点路径。该网关会将请求代理到 `connect.squareup.com` 并自动插入您的 OAuth 令牌。

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Square OAuth 连接。

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

如果您有多个 Square 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

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

## API 参考

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

#### 获取支付详情

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

#### 获取客户详情

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

#### 更新订单

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

#### 支付订单

```bash
POST /squareup/v2/orders/{order_id}/pay
Content-Type: application/json

{
  "idempotency_key": "unique-key",
  "payment_ids": ["{payment_id}"]
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

### 团队成员

#### 搜索团队成员

```bash
POST /squareup/v2/team-members/search
Content-Type: application/json

{
  "query": {
    "filter": {
      "location_ids": ["{location_id}"],
      "status": "ACTIVE"
    }
  }
}
```

#### 获取团队成员信息

```bash
GET /squareup/v2/team-members/{team_member_id}
```

#### 更新团队成员信息

```bash
PUT /squareup/v2/team-members/{team_member_id}
Content-Type: application/json

{
  "team_member": {
    "given_name": "Updated Name"
  }
}
```

### 会员福利

#### 列出会员福利计划

```bash
GET /squareup/v2/loyalty/programs
```

#### 获取会员福利计划信息

```bash
GET /squareup/v2/loyalty/programs/{program_id}
```

#### 搜索会员账户

```bash
POST /squareup/v2/loyalty/accounts/search
Content-Type: application/json

{
  "query": {
    "customer_ids": ["{customer_id}"]
  }
}
```

#### 创建会员账户

```bash
POST /squareup/v2/loyalty/accounts
Content-Type: application/json

{
  "loyalty_account": {
    "program_id": "{program_id}",
    "mapping": {
      "phone_number": "+15551234567"
    }
  },
  "idempotency_key": "unique-key"
}
```

#### 积累会员积分

```bash
POST /squareup/v2/loyalty/accounts/{account_id}/accumulate
Content-Type: application/json

{
  "accumulate_points": {
    "order_id": "{order_id}"
  },
  "location_id": "{location_id}",
  "idempotency_key": "unique-key"
}
```

### 支付链接（在线结算）

#### 列出支付链接

```bash
GET /squareup/v2/online-checkout/payment-links
```

#### 获取支付链接信息

```bash
GET /squareup/v2/online-checkout/payment-links/{id}
```

#### 创建支付链接

```bash
POST /squareup/v2/online-checkout/payment-links
Content-Type: application/json

{
  "idempotency_key": "unique-key",
  "quick_pay": {
    "name": "Payment for Service",
    "price_money": {
      "amount": 1000,
      "currency": "USD"
    },
    "location_id": "{location_id}"
  }
}
```

#### 更新支付链接信息

```bash
PUT /squareup/v2/online-checkout/payment-links/{id}
Content-Type: application/json

{
  "payment_link": {
    "version": 1,
    "description": "Updated description"
  }
}
```

#### 删除支付链接

```bash
DELETE /squareup/v2/online-checkout/payment-links/{id}
```

### 卡片

#### 列出卡片信息

```bash
GET /squareup/v2/cards
GET /squareup/v2/cards?customer_id={customer_id}
```

#### 获取卡片信息

```bash
GET /squareup/v2/cards/{card_id}
```

#### 创建卡片

```bash
POST /squareup/v2/cards
Content-Type: application/json

{
  "idempotency_key": "unique-key",
  "source_id": "cnon:card-nonce-ok",
  "card": {
    "customer_id": "{customer_id}"
  }
}
```

#### 禁用卡片

```bash
POST /squareup/v2/cards/{card_id}/disable
```

### 支付结算

#### 列出支付结算记录

```bash
GET /squareup/v2/payouts
GET /squareup/v2/payouts?location_id={location_id}
```

#### 获取支付结算信息

```bash
GET /squareup/v2/payouts/{payout_id}
```

#### 列出支付结算条目

```bash
GET /squareup/v2/payouts/{payout_id}/payout-entries
```

### 银行账户

#### 列出银行账户信息

```bash
GET /squareup/v2/bank-accounts
```

#### 获取银行账户信息

```bash
GET /squareup/v2/bank-accounts/{bank_account_id}
```

### 终端

#### 列出终端结算信息

```bash
GET /squareup/v2/terminals/checkouts
```

#### 创建终端结算记录

```bash
POST /squareup/v2/terminals/checkouts
Content-Type: application/json

{
  "idempotency_key": "unique-key",
  "checkout": {
    "amount_money": {
      "amount": 1000,
      "currency": "USD"
    },
    "device_options": {
      "device_id": "{device_id}"
    }
  }
}
```

#### 获取终端结算信息

```bash
GET /squareup/v2/terminals/checkouts/{checkout_id}
```

#### 搜索终端结算记录

```bash
POST /squareup/v2/terminals/checkouts/search
Content-Type: application/json

{
  "query": {
    "filter": {
      "status": "COMPLETED"
    }
  }
}
```

#### 取消终端结算

```bash
POST /squareup/v2/terminals/checkouts/{checkout_id}/cancel
```

## 分页

Square 使用基于游标的分页机制。当存在更多结果时，列表端点会返回一个 `cursor` 字段：

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

- 所有金额均以最小货币单位表示（例如，美元的 cent 表示为 1000 = $10.00）。
- ID 为字母数字字符串。
- 时间戳采用 ISO 8601 格式（例如，`2026-02-07T01:59:28.459Z`）。
- 大多数写入操作需要 `idempotency_key` 以防止重复操作。
- 某些端点需要特定的 OAuth 权限范围（如 `CUSTOMERS_READ`、`ORDERS_READ`、`ITEMS_READ`、`INVOICES_READ` 等）。
- 重要提示：当使用 `curl` 命令时，如果 URL 中包含括号，请使用 `curl -g` 以防止全局解析。
- 重要提示：当将 `curl` 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立 Square 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | OAuth 权限范围不足 |
| 404 | 资源未找到 |
| 429 | 请求次数受限 |
| 4xx/5xx | 来自 Square API 的传递错误 |

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

### 故障排除：应用名称无效

1. 确保您的 URL 路径以 `squareup` 开头。例如：
  - 正确：`https://gateway.maton.ai/squareup/v2/locations`
  - 错误：`https://gateway.maton.ai/v2/locations`

### 故障排除：权限范围不足

如果收到 `INSUFFICIENT_SCOPES` 错误，表示 OAuth 连接没有所需的权限。请创建新的连接，并在 OAuth 认证过程中授予所有必要的权限。

## 资源

- [Square API 概述](https://developer.square.com/docs)
- [Square API 参考](https://developer.square.com/reference/square)
- [支付 API](https://developer.square.com/reference/square/payments-api)
- [客户 API](https://developer.square.com/reference/square/customers-api)
- [订单 API](https://developer.square.com/reference/square/orders-api)
- [商品目录 API](https://developer.square.com/reference/square/catalog-api)
- [库存 API](https://developer.square.com/reference/square/inventory-api)
- [发票 API](https://developer.square.com/reference/square/invoices-api)
- [地点 API](https://developer.square.com/reference/square/locations-api)
- [团队成员 API](https://developer.square.com/reference/square/team-api)
- [会员福利 API](https://developer.square.com/reference/square/loyalty-api)
- [在线结算 API](https://developer.square.com/reference/square/online-checkout-api)
- [卡片 API](https://developer.square.com/reference/square/cards-api)
- [支付结算 API](https://developer.square.com/reference/square/payouts-api)
- [银行账户 API](https://developer.square.com/reference/square/bank-accounts-api)
- [终端 API](https://developer.square.com/reference/square/terminal-api)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)