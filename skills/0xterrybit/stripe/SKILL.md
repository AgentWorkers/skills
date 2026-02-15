---
name: stripe
description: **Stripe支付平台集成**：通过Stripe API管理支付、订阅、发票和客户信息。
metadata: {"clawdbot":{"emoji":"💵","always":true,"requires":{"bins":["curl","jq"]},"primaryEnv":"STRIPE_API_KEY"}}
---

# Stripe 💵

Stripe 是一个流行的在线支付平台，支持多种支付方式。以下是关于如何将您的应用程序与 Stripe 集成的指南。

## 设置

```bash
export STRIPE_API_KEY="sk_live_..."
```

## 主要功能

- 创建支付请求（Payment Intents）
- 管理订阅服务
- 发送发票
- 客户管理
- 退款处理
- Webhook 功能（用于接收支付状态更新）

## 使用示例

```
"Create a $50 payment link"
"List recent Stripe payments"
"Refund payment pi_xxx"
"Show subscription for customer@email.com"
```

## API 参考文档

```bash
# List recent charges
curl -s https://api.stripe.com/v1/charges?limit=10 \
  -u "$STRIPE_API_KEY:"
```