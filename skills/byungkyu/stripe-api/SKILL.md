---
name: stripe
description: |
  Stripe API integration with managed OAuth. Manage customers, subscriptions, invoices, products, prices, and payments.
  Use this skill when users want to process payments, manage billing, or handle subscriptions with Stripe.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
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

# Stripe

通过管理的OAuth身份验证来访问Stripe API。您可以管理客户、订阅、发票、产品、价格，并处理支付。

## 快速入门

```bash
# List customers
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/stripe/v1/customers?limit=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/stripe/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的Stripe API端点路径。该网关会将请求代理到 `api.stripe.com`，并自动插入您的OAuth令牌。

## 身份验证

所有请求都需要在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取您的API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的Stripe OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=stripe&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'stripe'}).encode()
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
    "connection_id": "c3c82a73-4c86-4c73-8ebd-1f325212fde6",
    "status": "ACTIVE",
    "creation_time": "2026-02-01T06:04:02.431819Z",
    "last_updated_time": "2026-02-10T22:40:01.061825Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "stripe",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成OAuth授权。

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

如果您有多个Stripe连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/stripe/v1/customers')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'c3c82a73-4c86-4c73-8ebd-1f325212fde6')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API参考

所有Stripe API端点都遵循以下格式：

```
/stripe/v1/{resource}
```

---

## 账户余额

### 获取账户余额

```bash
GET /stripe/v1/balance
```

**响应：**
```json
{
  "object": "balance",
  "available": [
    {
      "amount": 0,
      "currency": "usd",
      "source_types": {"card": 0}
    }
  ],
  "pending": [
    {
      "amount": 5000,
      "currency": "usd",
      "source_types": {"card": 5000}
    }
  ]
}
```

### 列出账户余额交易记录

```bash
GET /stripe/v1/balance_transactions?limit=10
```

---

## 客户

### 列出客户

```bash
GET /stripe/v1/customers?limit=10
```

**查询参数：**

| 参数 | 描述 |
|-----------|-------------|
| `limit` | 结果数量（1-100，默认：10） |
| `starting_after` | 分页的起始位置 |
| `ending_before` | 分页的结束位置 |
| `email` | 按电子邮件过滤 |
| `created` | 按创建日期过滤 |

**响应：**
```json
{
  "object": "list",
  "data": [
    {
      "id": "cus_TxKtN8Irvzx9BQ",
      "object": "customer",
      "email": "customer@example.com",
      "name": null,
      "balance": 0,
      "currency": "usd",
      "created": 1770765579,
      "metadata": {}
    }
  ],
  "has_more": true,
  "url": "/v1/customers"
}
```

### 获取客户信息

```bash
GET /stripe/v1/customers/{customer_id}
```

### 创建客户

```bash
POST /stripe/v1/customers
Content-Type: application/x-www-form-urlencoded

email=customer@example.com&name=John%20Doe&metadata[user_id]=123
```

### 更新客户信息

```bash
POST /stripe/v1/customers/{customer_id}
Content-Type: application/x-www-form-urlencoded

name=Jane%20Doe&email=jane@example.com
```

### 删除客户

```bash
DELETE /stripe/v1/customers/{customer_id}
```

---

## 产品

### 列出产品

```bash
GET /stripe/v1/products?limit=10
```

**查询参数：**

| 参数 | 描述 |
|-----------|-------------|
| `active` | 按活动状态过滤 |
| `type` | 按类型过滤：`good` 或 `service` |

**响应：**
```json
{
  "object": "list",
  "data": [
    {
      "id": "prod_TthCLBwTIXuzEw",
      "object": "product",
      "active": true,
      "name": "Premium Plan",
      "description": "Premium subscription",
      "type": "service",
      "created": 1769926024,
      "metadata": {}
    }
  ],
  "has_more": true
}
```

### 获取产品信息

```bash
GET /stripe/v1/products/{product_id}
```

### 创建产品

```bash
POST /stripe/v1/products
Content-Type: application/x-www-form-urlencoded

name=Premium%20Plan&description=Premium%20subscription&type=service
```

### 更新产品信息

```bash
POST /stripe/v1/products/{product_id}
Content-Type: application/x-www-form-urlencoded

name=Updated%20Plan&active=true
```

### 删除产品

```bash
DELETE /stripe/v1/products/{product_id}
```

---

## 价格

### 列出价格

```bash
GET /stripe/v1/prices?limit=10
```

**查询参数：**

| 参数 | 描述 |
|-----------|-------------|
| `active` | 按活动状态过滤 |
| `product` | 按产品ID过滤 |
| `type` | 按类型过滤：`one_time` 或 `recurring` |
| `currency` | 按货币过滤 |

**响应：**
```json
{
  "object": "list",
  "data": [
    {
      "id": "price_1SvtoVDfFKJhF88gKJv2eSmO",
      "object": "price",
      "active": true,
      "currency": "usd",
      "product": "prod_TthCLBwTIXuzEw",
      "unit_amount": 1999,
      "recurring": {
        "interval": "month",
        "interval_count": 1
      },
      "type": "recurring"
    }
  ],
  "has_more": true
}
```

### 获取价格信息

```bash
GET /stripe/v1/prices/{price_id}
```

### 创建价格

```bash
POST /stripe/v1/prices
Content-Type: application/x-www-form-urlencoded

product=prod_XXX&unit_amount=1999&currency=usd&recurring[interval]=month
```

### 更新价格

```bash
POST /stripe/v1/prices/{price_id}
Content-Type: application/x-www-form-urlencoded

active=false
```

---

## 订阅

### 列出订阅信息

```bash
GET /stripe/v1/subscriptions?limit=10
```

**查询参数：**

| 参数 | 描述 |
|-----------|-------------|
| `customer` | 按客户ID过滤 |
| `price` | 按价格ID过滤 |
| `status` | 按状态过滤：`active`, `canceled`, `past_due` 等 |

**响应：**
```json
{
  "object": "list",
  "data": [
    {
      "id": "sub_1SzQDXDfFKJhF88gf72x6tDh",
      "object": "subscription",
      "customer": "cus_TxKtN8Irvzx9BQ",
      "status": "active",
      "current_period_start": 1770765579,
      "current_period_end": 1773184779,
      "items": {
        "data": [
          {
            "id": "si_TxKtFWxlUW50cR",
            "price": {
              "id": "price_1RGbXsDfFKJhF88gMIShAq9m",
              "unit_amount": 0
            },
            "quantity": 1
          }
        ]
      }
    }
  ],
  "has_more": true
}
```

### 获取订阅信息

```bash
GET /stripe/v1/subscriptions/{subscription_id}
```

### 创建订阅

```bash
POST /stripe/v1/subscriptions
Content-Type: application/x-www-form-urlencoded

customer=cus_XXX&items[0][price]=price_XXX
```

### 更新订阅

```bash
POST /stripe/v1/subscriptions/{subscription_id}
Content-Type: application/x-www-form-urlencoded

items[0][id]=si_XXX&items[0][price]=price_YYY
```

### 取消订阅

```bash
DELETE /stripe/v1/subscriptions/{subscription_id}
```

---

## 发票

### 列出发票

```bash
GET /stripe/v1/invoices?limit=10
```

**查询参数：**

| 参数 | 描述 |
|-----------|-------------|
| `customer` | 按客户ID过滤 |
| `subscription` | 按订阅ID过滤 |
| `status` | 按状态过滤：`draft`, `open`, `paid`, `void`, `uncollectible` |

**响应：**
```json
{
  "object": "list",
  "data": [
    {
      "id": "in_1SzQDXDfFKJhF88g3nh4u2GS",
      "object": "invoice",
      "customer": "cus_TxKtN8Irvzx9BQ",
      "amount_due": 0,
      "amount_paid": 0,
      "currency": "usd",
      "status": "paid",
      "subscription": "sub_1SzQDXDfFKJhF88gf72x6tDh",
      "hosted_invoice_url": "https://invoice.stripe.com/...",
      "invoice_pdf": "https://pay.stripe.com/invoice/.../pdf"
    }
  ],
  "has_more": true
}
```

### 获取发票信息

```bash
GET /stripe/v1/invoices/{invoice_id}
```

### 创建发票

```bash
POST /stripe/v1/invoices
Content-Type: application/x-www-form-urlencoded

customer=cus_XXX
```

### 完成发票处理

```bash
POST /stripe/v1/invoices/{invoice_id}/finalize
```

### 支付发票

```bash
POST /stripe/v1/invoices/{invoice_id}/pay
```

### 废除发票

```bash
POST /stripe/v1/invoices/{invoice_id}/void
```

---

## 费用

### 列出费用信息

```bash
GET /stripe/v1/charges?limit=10
```

**查询参数：**

| 参数 | 描述 |
|-----------|-------------|
| `customer` | 按客户ID过滤 |
| `payment_intent` | 按支付意图过滤 |

**响应：**
```json
{
  "object": "list",
  "data": [
    {
      "id": "ch_3SyXBvDfFKJhF88g1MHtT45f",
      "object": "charge",
      "amount": 5000,
      "currency": "usd",
      "customer": "cus_TuZ7GIjeZQOQ2m",
      "paid": true,
      "status": "succeeded",
      "payment_method_details": {
        "card": {
          "brand": "mastercard",
          "last4": "0833"
        },
        "type": "card"
      }
    }
  ],
  "has_more": true
}
```

### 获取费用信息

```bash
GET /stripe/v1/charges/{charge_id}
```

### 创建费用记录

```bash
POST /stripe/v1/charges
Content-Type: application/x-www-form-urlencoded

amount=2000&currency=usd&source=tok_XXX
```

---

## 支付意图

### 列出支付意图

```bash
GET /stripe/v1/payment_intents?limit=10
```

**响应：**
```json
{
  "object": "list",
  "data": [
    {
      "id": "pi_3SyXBvDfFKJhF88g17PeHdpE",
      "object": "payment_intent",
      "amount": 5000,
      "currency": "usd",
      "customer": "cus_TuZ7GIjeZQOQ2m",
      "status": "succeeded",
      "payment_method": "pm_1SyXBpDfFKJhF88gmP3IjC8C"
    }
  ],
  "has_more": true
}
```

### 获取支付意图

```bash
GET /stripe/v1/payment_intents/{payment_intent_id}
```

### 创建支付意图

```bash
POST /stripe/v1/payment_intents
Content-Type: application/x-www-form-urlencoded

amount=2000&currency=usd&customer=cus_XXX&payment_method_types[]=card
```

### 确认支付意图

```bash
POST /stripe/v1/payment_intents/{payment_intent_id}/confirm
```

### 取消支付意图

```bash
POST /stripe/v1/payment_intents/{payment_intent_id}/cancel
```

---

## 支付方式

### 列出支付方式

```bash
GET /stripe/v1/payment_methods?customer=cus_XXX&type=card
```

### 获取支付方式信息

```bash
GET /stripe/v1/payment_methods/{payment_method_id}
```

### 附加支付方式

```bash
POST /stripe/v1/payment_methods/{payment_method_id}/attach
Content-Type: application/x-www-form-urlencoded

customer=cus_XXX
```

### 移除支付方式

```bash
POST /stripe/v1/payment_methods/{payment_method_id}/detach
```

---

## 优惠券

### 列出优惠券

```bash
GET /stripe/v1/coupons?limit=10
```

### 获取优惠券信息

```bash
GET /stripe/v1/coupons/{coupon_id}
```

### 创建优惠券

```bash
POST /stripe/v1/coupons
Content-Type: application/x-www-form-urlencoded

percent_off=25&duration=once
```

### 删除优惠券

```bash
DELETE /stripe/v1/coupons/{coupon_id}
```

---

## 退款

### 列出退款记录

```bash
GET /stripe/v1/refunds?limit=10
```

### 获取退款信息

```bash
GET /stripe/v1/refunds/{refund_id}
```

### 创建退款

```bash
POST /stripe/v1/refunds
Content-Type: application/x-www-form-urlencoded

charge=ch_XXX&amount=1000
```

---

## 分页

Stripe使用基于游标的分页方式，通过 `starting_after` 和 `ending_before` 参数进行分页：

```bash
GET /stripe/v1/customers?limit=10&starting_after=cus_XXX
```

**响应包含：**
```json
{
  "object": "list",
  "data": [...],
  "has_more": true,
  "url": "/v1/customers"
}
```

使用上一页的最后一个项目的ID作为 `starting_after` 参数来获取下一页的数据。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/stripe/v1/customers?limit=10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.data);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/stripe/v1/customers',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'limit': 10}
)
data = response.json()
for customer in data['data']:
    print(f"{customer['id']}: {customer['email']}")
```

## 注意事项

- Stripe API 对POST请求使用 `application/x-www-form-urlencoded` 格式（而非JSON）。
- 金额以最小货币单位表示（例如，USD的金额为分）。
- ID以特定前缀开头：`cus_`（客户）、`prod_`（产品）、`price_`（价格）、`sub_`（订阅）、`in_`（发票）、`ch_`（费用）、`pi_`（支付意图）。
- 时间戳为Unix时间戳。
- 重要提示：当使用 `curl` 命令时，如果URL包含括号，请使用 `curl -g` 以避免全局解析问题。
- 重要提示：当将 `curl` 的输出传递给 `jq` 或其他命令时，在某些shell环境中环境变量（如 `$MATON_API_KEY`）可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求错误或参数无效 |
| 401 | Maton API密钥无效或缺失 |
| 402 | 卡片被拒绝或需要支付 |
| 404 | 资源未找到 |
| 429 | 日志限制 |
| 500 | Stripe内部错误 |

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

### 故障排除：应用程序名称错误

1. 确保您的URL路径以 `stripe` 开头。例如：

- 正确：`https://gateway.maton.ai/stripe/v1/customers`
- 错误：`https://gateway.maton.ai/v1/customers`

## 资源

- [Stripe API参考文档](https://docs.stripe.com/api)
- [Stripe控制面板](https://dashboard.stripe.com/)
- [Stripe测试工具](https://docs.stripe.com/testing)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)