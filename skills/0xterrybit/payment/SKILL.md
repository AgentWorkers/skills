---
name: payment
description: 支付处理与管理：负责处理发票、交易以及与支付网关的集成。
metadata: {"clawdbot":{"emoji":"💳","always":true,"requires":{"bins":["curl","jq"]}}}
---

# 支付 💳

处理支付和交易管理。

## 功能

- 创建并发送发票
- 处理付款
- 跟踪支付状态
- 退款管理
- 支付历史记录

## 支持的支付网关

- Stripe
- PayPal
- Square
- 加密货币支付

## 使用示例

```
"Create an invoice for $100"
"Check payment status for order #123"
"Show recent transactions"
```

## 安全规则

1. **务必** 在处理支付前核实支付金额。
2. **绝不要** 以明文形式存储敏感的支付凭据。