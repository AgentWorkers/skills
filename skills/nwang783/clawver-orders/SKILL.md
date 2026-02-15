---
name: clawver-orders
description: 管理 Clawver 订单：列出订单、追踪订单状态、处理退款、生成下载链接。当需要查询客户订单、订单履行情况、退款信息或订单历史记录时，请使用此功能。
version: 1.3.0
homepage: https://clawver.store
metadata: {"openclaw":{"emoji":"📦","homepage":"https://clawver.store","requires":{"env":["CLAW_API_KEY"]},"primaryEnv":"CLAW_API_KEY"}}
---

# Clawver 订单管理

在您的 Clawver 商店中管理订单——查看订单历史记录、追踪订单状态、处理退款以及生成下载链接。

## 先决条件

- 需要设置 `CLAW_API_KEY` 环境变量
- 商店中必须有已生成的订单

有关 `claw-social` 提供的特定平台上的优秀及不良 API 设计范例，请参考 `references/api-examples.md`。

## 列出订单

### 获取所有订单

```bash
curl https://api.clawver.store/v1/orders \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

### 按状态筛选

```bash
# Confirmed (paid) orders
curl "https://api.clawver.store/v1/orders?status=confirmed" \
  -H "Authorization: Bearer $CLAW_API_KEY"

# In-progress POD orders
curl "https://api.clawver.store/v1/orders?status=processing" \
  -H "Authorization: Bearer $CLAW_API_KEY"

# Shipped orders
curl "https://api.clawver.store/v1/orders?status=shipped" \
  -H "Authorization: Bearer $CLAW_API_KEY"

# Delivered orders
curl "https://api.clawver.store/v1/orders?status=delivered" \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

**订单状态：**

| 状态 | 描述 |
|--------|-------------|
| `pending` | 订单已创建，付款待处理 |
| `confirmed` | 付款已确认 |
| `processing` | 订单正在处理中 |
| `shipped` | 商品已发货（仅限 POD 服务） |
| `delivered` | 订单已送达 |
| `cancelled` | 订单已取消 |

`paymentStatus` 会单独显示，可能为 `pending`、`paid`、`failed`、`partially_refunded` 或 `refunded`。

### 分页

```bash
curl "https://api.clawver.store/v1/orders?limit=20" \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

该接口支持分页功能。目前不支持基于游标的分页方式。

## 获取订单详情

```bash
curl https://api.clawver.store/v1/orders/{orderId} \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

对于按需打印的商品，订单数据中包含以下信息：
- `variantId`（必填项——订单对应的商品变体标识符，必须与产品变体匹配）
- `variantName`（用户可读的尺寸/变体名称）

注意：自 2026 年 2 月起，所有 POD 类型的订单都必须提供 `variantId`；缺货的变体将无法被处理。

## 生成下载链接

### 所有者下载链接（数字商品）

```bash
curl "https://api.clawver.store/v1/orders/{orderId}/download/{itemId}" \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

当客户报告下载问题或请求新的下载链接时，可以使用此功能。

### 客户下载链接（数字商品）

```bash
curl "https://api.clawver.store/v1/orders/{orderId}/download/{itemId}/public?token={downloadToken}"
```

每个订单商品都会生成一个下载链接，该链接可以在结账收据中获取（通过 `GET /v1/checkout/{checkoutId}/receipt` 获取）。

### 客户订单状态（公开可见）

```bash
curl "https://api.clawver.store/v1/orders/{orderId}/public?token={orderStatusToken}"
```

### 结账收据（成功页面/支持页面）

```bash
curl "https://api.clawver.store/v1/checkout/{checkoutId}/receipt"
```

## 处理退款

### 全额退款

```bash
curl -X POST https://api.clawver.store/v1/orders/{orderId}/refund \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "amountInCents": 2499,
    "reason": "Customer requested refund"
  }'
```

### 部分退款

```bash
curl -X POST https://api.clawver.store/v1/orders/{orderId}/refund \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "amountInCents": 500,
    "reason": "Partial refund for missing item"
  }'
```

**注意事项：**
- `amountInCents` 是必填项，且必须为正整数。
- `reason` 是必填项。
- `amountInCents` 不能超过订单剩余的可退款金额。
- 退款通过 Stripe 平台处理，客户通常在 1-5 个工作日内收到退款。
- 订单的 `paymentStatus` 必须为 `paid` 或 `partially_refunded`。

## POD 订单追踪

对于按需打印的订单，发货后可以获取追踪信息：

```bash
curl https://api.clawver.store/v1/orders/{orderId} \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

请查看响应中的 `trackingUrl`、`trackingNumber` 和 `carrier` 字段。

### 发货更新的通知钩子

```bash
curl -X POST https://api.clawver.store/v1/webhooks \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-server.com/webhook",
    "events": ["order.shipped", "order.fulfilled"],
    "secret": "your-secret-min-16-chars"
  }'
```

## 订单通知钩子

接收实时订单更新通知：

```bash
curl -X POST https://api.clawver.store/v1/webhooks \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-server.com/webhook",
    "events": ["order.created", "order.paid", "order.refunded"],
    "secret": "your-webhook-secret-16chars"
  }'
```

**签名格式：**
```
X-Claw-Signature: sha256=abc123...
```

**验证（Node.js）：**
```javascript
const crypto = require('crypto');

function verifyWebhook(body, signature, secret) {
  const expected = 'sha256=' + crypto
    .createHmac('sha256', secret)
    .update(body)
    .digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  );
}
```

## 常见工作流程

### 每日订单检查

```python
# Get newly paid/confirmed orders
response = api.get("/v1/orders?status=confirmed")
orders = response["data"]["orders"]
print(f"New orders: {len(orders)}")

for order in orders:
    print(f"  - {order['id']}: ${order['totalInCents']/100:.2f}")
```

### 处理退款请求

```python
def process_refund(order_id, amount_cents, reason):
    # Get order details
    response = api.get(f"/v1/orders/{order_id}")
    order = response["data"]["order"]
    
    # Check if refundable
    if order["paymentStatus"] not in ["paid", "partially_refunded"]:
        return "Order cannot be refunded"
    
    # Process refund
    result = api.post(f"/v1/orders/{order_id}/refund", {
        "amountInCents": amount_cents,
        "reason": reason
    })
    
    return f"Refunded ${amount_cents/100:.2f}"
```

### 处理尺寸错误的情况

```python
def handle_wrong_size(order_id):
    response = api.get(f"/v1/orders/{order_id}")
    order = response["data"]["order"]

    for item in order["items"]:
        if item.get("productType") == "print_on_demand":
            print("Variant ID:", item.get("variantId"))
            print("Variant Name:", item.get("variantName"))

    # Confirm selected variant before issuing a refund/replacement workflow.
```

### 重新发送下载链接

```python
def resend_download(order_id, item_id):
    # Generate new download link
    response = api.get(f"/v1/orders/{order_id}/download/{item_id}")
    
    return response["data"]["downloadUrl"]
```

## 订单生命周期

**数字产品：** `confirmed` → `delivered`（立即完成交付）
**POD 产品：** `confirmed` → `processing` → `shipped` → `delivered`