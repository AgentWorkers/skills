---
name: checkout
description: 使用 Credpay Checkout API 在任何在线商店完成购物交易，支持 x402 支付方式。该功能会在用户想要购买、下单或结账时被触发。
---
# Credpay 结账技能

**API 基本 URL:** `https://checkout-agent.credpay.xyz`

每当用户想要从任何在线商店购买、下单或结账时，触发此技能。

## 需要用户提供的信息

在开始之前，请收集以下信息（如果缺少，请询问用户）：

| 字段 | 示例 |
|---|---|
| 产品 URL | `https://example.com/products/tee` |
| 数量 | `1` |
| 尺寸/颜色（如适用） | `"Size": "M", "Color": "Black"` |
| 电子邮件 | `customer@example.com` |
| 商品总价（美元） | `"49.99"` — 以美元字符串形式表示商品价格，不包含货币符号 |
| 运输地址 | 名字, 姓氏, 街道1号, 城市, 州, 邮政编码, 国家, 电话 |

## 第一步 — 获取报价（无需支付）

```http
POST https://checkout-agent.credpay.xyz/v1/quote
Content-Type: application/json

{
  "items": [
    {
      "url": "<product URL>",
      "quantity": 1,
      "options": { "Size": "M", "Color": "Black" }
    }
  ],
  "email": "<email>",
  "shippingAddress": {
    "firstName": "Jane",
    "lastName": "Doe",
    "line1": "123 Main St",
    "city": "Austin",
    "state": "TX",
    "postalCode": "78701",
    "country": "United States",
    "countryCode": "US",
    "phone": "+15125551234"
  },
  "goodsTotal": "<item price in USD as string, e.g. \"49.99\">"
}
```

→ 从响应中保存 `maxAmount`。这是您将通过 x402 支付的 USDC 金额。

## 第二步 — 提交结账请求（需要 x402 支付）

```http
POST https://checkout-agent.credpay.xyz/v1/checkout
Content-Type: application/json
X-PAYMENT: <x402 payment payload for maxAmount on Base chainId 8453>

<same body as Step 1>
```

→ 当收到 `202` 状态码时，保存 `requestId` 并进入第三步。
→ 当收到 `402` 状态码时，重新读取响应中的支付要求，并使用正确的 `X-PAYMENT` 标头重新尝试支付。

## 第三步 — 监控支付完成情况

```http
GET https://checkout-agent.credpay.xyz/v1/checkout/{requestId}
```

每 5 秒检查一次支付进度。当状态变为 `completed` 或 `failed` 时停止检查。超时时间为 10 分钟。

| 状态 | 操作 |
|---|---|
| `processing` | 继续检查 |
| `authorization_required` | 转到第四步 |
| `completed` | 结束操作 — 将结果返回给用户 |
| `failed` | 向用户报告 `errorCode` 和 `errorMessage` |

## 第四步 — 处理额外支付（如有必要）

如果状态为 `authorization_required`，说明订单总金额超过了报价金额：

```http
POST https://checkout-agent.credpay.xyz/v1/checkout/{requestId}/authorize
X-PAYMENT: <x402 payment for extraOwed amount>
```

然后从第三步重新开始检查支付进度。

## 规则

- 适用于任何在线商店 — 只需传递产品页面的 URL 即可。
- 在 `requestId` 仍然有效的情况下，切勿为同一笔订单创建第二次结账请求。
- 对于短暂的网络错误，采用指数级退避策略进行重试。切勿对 `failed` 状态进行盲目重试。
- 默认的 `chainId` 为 `8453`（基础值）。

## 成功响应

```json
{
  "requestId": "req_abc123",
  "status": "completed",
  "success": true,
  "orderNumber": "1234"
}
```

## 失败响应

```json
{
  "requestId": "req_abc123",
  "status": "failed",
  "success": false,
  "errorCode": "payment_failed",
  "errorMessage": "Card declined"
}
```