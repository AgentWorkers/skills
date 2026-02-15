---
name: paypal
description: PayPal支付集成：支持发送款项、创建发票以及管理PayPal交易。
metadata: {"clawdbot":{"emoji":"🅿️","always":true,"requires":{"bins":["curl","jq"]},"primaryEnv":"PAYPAL_CLIENT_ID"}}
---

# PayPal 🅿️

PayPal支付平台集成。

## 设置

```bash
export PAYPAL_CLIENT_ID="your_client_id"
export PAYPAL_SECRET="your_secret"
```

## 功能

- 发送付款
- 创建发票
- 请求退款
- 交易历史记录
- 退款功能

## 使用示例

```
"Send $25 to user@email.com via PayPal"
"Create PayPal invoice for $100"
"Show my PayPal balance"
```