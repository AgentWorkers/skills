---
name: stripe-connect
description: **Stripe Connect集成：适用于市场平台和平台支付，支持“直接收费”（Direct Charge）及“目标账户收费”（Destination Charge）模式。**  
适用于以下场景：  
- 构建需要向卖家支付款项的市场平台；  
- 实施平台费用收取机制；  
- 让供应商接入以接收付款。  

**涵盖内容：**  
- Stripe Connect Webhook的配置与设置；  
- 账户验证流程；  
- 关键的“直接收费”（Direct Charge）Webhook功能实现。
---

# Stripe Connect 集成

掌握 Stripe Connect，以实现市场交易和平台支付功能，包括正确的 Webhook 处理、收费模式以及 Connect 账户管理。

## 适用场景

- 构建允许卖家接收支付的市场平台
- 实现带有费用的平台支付功能
- 将供应商/卖家引入您的平台
- 设置多方支付流程
- 处理向关联账户的付款
- 管理 Connect Webhook（尤其是 Direct Charge 功能）

## ⚠️ 重要提示：收费类型选择

| 收费模式 | 费用创建方 | Webhook 所在位置 | 适用场景 |
|---------|-------------------|------------------|----------|
| **Direct Charge** | 关联账户 | Connect 端点 | 卖家拥有客户关系的市场平台 |
| **Destination Charge** | 平台 | 平台端点 | 平台控制支付流程，并收取费用 |
| **Separate Charges & Transfers** | 平台 | 平台端点 | 最高的灵活性，支持复杂的费用分摊 |

### #1 Connect 使用误区：Direct Charge 的 Webhook 问题

**使用 Direct Charge 时，结账会话是在关联账户上创建的，** **而非在平台上！**

```
❌ Platform webhook only - PAYMENTS WILL BE MISSED!
   /webhooks/stripe → Does NOT receive Direct Charge checkout.session.completed

✅ Both webhooks required:
   /webhooks/stripe         → Platform events (account.updated, etc.)
   /webhooks/stripe/connect → checkout.session.completed for Direct Charges!
```

## 快速入门：使用正确的 Webhook 实现 Direct Charge

### 1. 创建结账会话（Direct Charge）

```typescript
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

async function createDirectChargeCheckout(
  connectedAccountId: string,
  amount: number,
  platformFee: number,
  metadata: Record<string, string>
) {
  const session = await stripe.checkout.sessions.create(
    {
      mode: 'payment',
      line_items: [{
        price_data: {
          currency: 'usd',
          product_data: { name: 'Service Booking' },
          unit_amount: amount,
        },
        quantity: 1,
      }],
      payment_intent_data: {
        application_fee_amount: platformFee, // Platform takes this
        metadata,
      },
      success_url: `${process.env.APP_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.APP_URL}/cancel`,
      metadata,
    },
    {
      stripeAccount: connectedAccountId, // CRITICAL: Creates on connected account!
    }
  );

  return session;
}
```

### 2. 平台 Webhook 端点

```typescript
// /webhooks/stripe - Platform events only
app.post('/webhooks/stripe',
  express.raw({ type: 'application/json' }),
  async (req, res) => {
    const sig = req.headers['stripe-signature']!;
    const event = stripe.webhooks.constructEvent(
      req.body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET!
    );

    switch (event.type) {
      case 'account.updated':
        await handleAccountUpdated(event.data.object);
        break;
      // Note: checkout.session.completed does NOT come here for Direct Charge!
    }

    res.json({ received: true });
  }
);
```

### 3. Connect Webhook 端点（Direct Charge 的关键步骤！）

```typescript
// /webhooks/stripe/connect - Connected account events
app.post('/webhooks/stripe/connect',
  express.raw({ type: 'application/json' }),
  async (req, res) => {
    const sig = req.headers['stripe-signature']!;
    const event = stripe.webhooks.constructEvent(
      req.body,
      sig,
      process.env.STRIPE_CONNECT_WEBHOOK_SECRET! // Different secret!
    );

    const connectedAccountId = event.account;

    switch (event.type) {
      case 'checkout.session.completed':
        // THIS is where Direct Charge payments complete!
        await handleConnectCheckoutComplete(event.data.object, connectedAccountId);
        break;

      case 'checkout.session.expired':
        await handleConnectCheckoutExpired(event.data.object, connectedAccountId);
        break;

      case 'payout.paid':
        await handlePayoutPaid(event.data.object, connectedAccountId);
        break;

      case 'payout.failed':
        await handlePayoutFailed(event.data.object, connectedAccountId);
        break;
    }

    res.json({ received: true });
  }
);

async function handleConnectCheckoutComplete(
  session: Stripe.Checkout.Session,
  connectedAccountId: string
) {
  // Retrieve full session from the connected account
  const fullSession = await stripe.checkout.sessions.retrieve(
    session.id,
    { expand: ['line_items', 'payment_intent'] },
    { stripeAccount: connectedAccountId } // CRITICAL!
  );

  // Idempotent confirmation
  await confirmPayment(fullSession.id);
}
```

### 4. Stripe 控制台设置

1. **平台 Webhook**：
   - 开发者 → Webhooks → 添加端点
   - URL：`https://yourdomain.com/webhooks/stripe`
   - 选择事件类型：`account.updated`
   - 监听事件：`account.updated`

2. **Connect Webhook**：
   - 开发者 → Webhooks → 添加端点
   - URL：`https://yourdomain.com/webhooks/stripe/connect`
   - 选择事件类型：`connectedaccounts`（而非 `account`！
   - 监听事件：`checkout.session_completed`, `checkout.session.expired`, `payout.paid`, `payout.failed`

## 账户注册流程

### Express 账户（大多数情况下推荐使用）

```typescript
async function createConnectAccount(email: string, businessType: string) {
  const account = await stripe.accounts.create({
    type: 'express',
    email,
    business_type: businessType,
    capabilities: {
      card_payments: { requested: true },
      transfers: { requested: true },
    },
    metadata: {
      internal_user_id: 'user_123',
    },
  });

  return account;
}

async function createOnboardingLink(accountId: string) {
  const accountLink = await stripe.accountLinks.create({
    account: accountId,
    refresh_url: `${process.env.APP_URL}/onboarding/refresh`,
    return_url: `${process.env.APP_URL}/onboarding/complete`,
    type: 'account_onboarding',
  });

  return accountLink.url; // Redirect user here
}
```

### 检查账户状态

```typescript
async function isAccountReady(accountId: string): Promise<boolean> {
  const account = await stripe.accounts.retrieve(accountId);

  return (
    account.charges_enabled &&
    account.payouts_enabled &&
    !account.requirements?.currently_due?.length
  );
}
```

## Destination Charge 模式

**适用于平台控制客户关系的场景：**

```typescript
async function createDestinationCharge(
  amount: number,
  destinationAccountId: string,
  platformFee: number
) {
  const paymentIntent = await stripe.paymentIntents.create({
    amount,
    currency: 'usd',
    transfer_data: {
      destination: destinationAccountId,
    },
    application_fee_amount: platformFee,
    metadata: {
      booking_id: 'booking_123',
    },
  });

  return paymentIntent;
}
```

## Separate Charges & Transfers

**适用于需要高度灵活的费用分摊场景（例如，将款项分摊给多个卖家）：**

```typescript
async function chargeAndTransfer(
  amount: number,
  transfers: Array<{ accountId: string; amount: number }>
) {
  // 1. Create charge on platform
  const paymentIntent = await stripe.paymentIntents.create({
    amount,
    currency: 'usd',
    metadata: { type: 'multi_transfer' },
  });

  // 2. After payment succeeds, create transfers
  // (Usually in webhook handler)
  for (const transfer of transfers) {
    await stripe.transfers.create({
      amount: transfer.amount,
      currency: 'usd',
      destination: transfer.accountId,
      source_transaction: paymentIntent.latest_charge as string,
    });
  }
}
```

## 使用 Connect 处理退款

```typescript
async function refundDirectCharge(
  paymentIntentId: string,
  connectedAccountId: string,
  refundApplicationFee: boolean = false
) {
  const refund = await stripe.refunds.create(
    {
      payment_intent: paymentIntentId,
      refund_application_fee: refundApplicationFee, // Return platform fee too?
    },
    {
      stripeAccount: connectedAccountId, // CRITICAL for Direct Charge!
    }
  );

  return refund;
}
```

## 预实施检查清单

### Webhook 设置
- [ ] 平台 Webhook 已配置为监听 `account.updated` 事件
- [ ] Connect Webhook 已配置为监听 `checkout.session_completed` 事件
- [ ] Connect Webhook 已配置为监听 `checkout.session.expired` 事件
- [ ] Connect Webhook 已配置为监听 `payout.paid` 和 `payout.failed` 事件
- [ ] 两个 Webhook 密钥已分别存储在环境变量中
- [ ] Stripe 控制台显示 Connect Webhook 与关联账户的关联状态

### 账户注册流程
- [ ] 账户创建流程正确（Express/Standard/Custom 类型）
- [ ] 生成账户注册链接
- [ ] 处理返回/刷新页面的逻辑
- [ ] 在允许收费前检查账户状态

### 收费流程
- [ ] 确定收费模式（Direct Charge/Destination Charge/Separate Charges）
- [ ] 实现平台费用计算
- [ ] 确保支付确认操作的幂等性
- [ ] 正确处理促销代码（如适用）

### 测试
- [ ] 使用测试账户进行注册流程测试
- [ ] 使用 Stripe CLI 测试结账流程
- [ ] 测试 Connect Webhook 是否能接收到 `checkout.session_completed` 事件
- [ ] 测试退款流程
- [ ] 测试付款事件的处理

## 常见错误

1. **缺少 Direct Charge 的 Connect Webhook** —— 这是导致支付失败的最常见原因
2. **两个端点使用相同的 Webhook 密钥** —— 必须使用不同的密钥
3. **在获取会话信息时未指定 `stripeAccount` —— 会导致数据错误
4. **未检查账户是否已准备好就直接开始收费** —— 必须始终验证 `charges_enabled` 状态
5. **硬编码平台费用** —— 应根据每笔交易进行配置

## 参考资源

- [Stripe Connect 概述](https://stripe.com/docs/connect)
- [Direct Charge](https://stripe.com/docs/connect/direct-charges)
- [Destination Charge](https://stripe.com/docs/connect/destination-charges)
- [Connect Webhooks](https://stripe.com/docs/connect/webhooks)