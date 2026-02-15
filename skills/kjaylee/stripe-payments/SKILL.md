---
name: stripe-payments
description: Stripe支付集成的最佳实践。适用于在游戏或Web应用中实现支付、订阅、结账流程或任何货币化功能时使用。内容涵盖了CheckoutSessions、Payment Element、订阅服务以及Connect接口的相关用法。
metadata:
  author: misskim
  version: "1.0"
  origin: Concept from Stripe official best practices, adapted for our game/app monetization
---

# Stripe支付集成

本指南介绍了如何将Stripe支付集成到您的游戏或Web应用程序中，以实现收入化。

## 核心原则

### 必须使用的功能：
- **CheckoutSessions API**：用于处理一次性支付和订阅功能。
- **Stripe提供的主机式结账（Hosted Checkout）**或**嵌入式结账（Embedded Checkout）**方式优先选择。
- **动态支付方式**：需在控制台中进行配置（禁止直接在代码中硬编码`payment_method_types`）。
- 使用最新版本的API和SDK。

### 绝对禁止的功能：
- ❌ `Charges API`（已过时，建议迁移到`PaymentIntents`）。
- ❌ `Card Element`/`Payment Element`的卡片支付方式（已过时）。
- ❌ `Sources API`（已被弃用）。
- ❌ `Tokens API`（建议使用`SetupIntents`）。
- ❌ 禁止在代码中硬编码`payment_method_types`（应使用动态支付方式）。

## 如何应用于我们的游戏/应用程序

### 根据不同场景的选择方案

```
수익화 유형 → 무엇을 파는가?
├─ 일회성 게임 구매 → CheckoutSessions (one-time)
├─ 인앱 구매/아이템 → CheckoutSessions + metadata
├─ 월정액 구독 → Billing API + CheckoutSessions
├─ 기부/후원 → Payment Links (가장 간단)
└─ 마켓플레이스 → Stripe Connect (destination charges)
```

### 基本实现模式

```javascript
// 서버 (Node.js)
const session = await stripe.checkout.sessions.create({
  mode: 'payment',  // 또는 'subscription'
  line_items: [{
    price_data: {
      currency: 'usd',
      product_data: { name: 'Game Premium' },
      unit_amount: 999,  // $9.99 (센트 단위!)
    },
    quantity: 1,
  }],
  success_url: 'https://eastsea.monster/thanks?session_id={CHECKOUT_SESSION_ID}',
  cancel_url: 'https://eastsea.monster/games/',
});
// session.url로 리다이렉트
```

### 订阅模式（SaaS/游戏高级会员）
- 使用`Billing API`来设计订阅功能：[参考文档](docs.stripe.com/billing/subscriptions/designing-integration)。
- 优先选择`CheckoutSessions`与`Billing`的组合。
- 通过Webhook实时检测订阅状态的变化。

### 多个游戏开发者共享的解决方案（使用Stripe Connect）：
- **责任承担方（Liability）**：由我们负责处理相关费用。
- 使用`on_behalf_of`参数来指定交易的商户信息。
- 禁止混合使用不同的支付类型。

## 安全性检查清单：
- [ ] 仅在使用服务器端时才使用Secret Key。
- [ ] 对Webhook签名进行验证。
- [ ] 禁止在客户端代码中硬编码金额或价格信息（金额应在服务器端生成）。
- [ ] 完成上线前的检查清单：[参考文档](docs.stripe.com/get-started/checklist/go-live)。
- [ ] 必须使用HTTPS协议。

## 参考文档：
- 集成选项：[查看文档](docs.stripe.com/payments/payment-methods/integration-options)。
- API使用指南：[查看文档](docs.stripe.com/payments-api/tour)。
- 上线前的检查清单：[查看文档](docs.stripe.com/get-started/checklist/go-live)。