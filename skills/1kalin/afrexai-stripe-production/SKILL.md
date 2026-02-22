# Stripe 生产环境工程

这是一套完整的开发方法论，用于构建、扩展和运营生产环境的 Stripe 支付系统，涵盖了从首次购物到大规模企业计费的整个流程。

## 快速健康检查

请检查以下 8 项指标，每项得 1 分。总分低于 5 分时，需要立即停止并修复问题：

1. ✅ Webhook 端点已验证且具有幂等性
2. ✅ 所有 API 调用都使用了幂等性键
3. ✅ 客户门户已启用，支持自助服务
4. ✅ 已配置 Stripe 税务处理或手动税务收集功能
5. ✅ 具备失败支付的重试逻辑，并会发送催款邮件
6. ✅ 已完成 PCI 合规性问卷（至少满足 SAQ-A 的要求）
7. ✅ 从测试模式切换到生产模式
8. ✅ 能够监控支付失败和 webhook 错误

**得分：/8** — 如果得分低于 5 分，请在添加新功能之前先修复存在的问题。

---

## 第 1 阶段：架构策略

### 集成模式选择

| 集成模式 | 适用场景 | 复杂度 | PCI 合规性要求 |
|---------|----------|------------|-----------|
| **Stripe Checkout（托管式）** | MVP 项目、快速启动 | 低 | 最低满足 SAQ-A 的要求 |
| **Payment Element（嵌入式）** | 自定义用户界面、品牌控制 | 中等 | 最低满足 SAQ-A 的要求 |
| **Card Element（传统方式）** | 适用于现有集成系统 | 中等 | 需满足 SAQ-A-EP 的要求 |
| **Direct API** | 适用于平台/市场places | 高 | 需满足 SAQ-D 的要求（建议避免使用） |

**决策规则：** 首先选择 Checkout 模式。只有在有特定用户界面需求且 Checkout 无法满足时，再考虑使用 Payment Element 模式。

### 计费模型选择

| 计费模型 | 对应的 Stripe 产品 | 适用场景 |
|-------|---------------|----------|
| 一次性支付 | Payment Links / Checkout | 单次购买、终身订阅 |
| 循环计费 | 订阅服务 | 固定的月度/年度费用 |
| 按使用量计费 | 根据 API 调用次数、计算资源使用量等计费 |
| 按用户数量计费 | 订阅服务 + 用户数量 | 根据团队/用户数量定价 |
| 分层定价 | 分层定价 | 根据使用量提供折扣 |
| 混合计费 | 订阅服务 + 使用量记录 | 基础费用 + 超量使用额外收费 |

### 项目结构

```
src/
  payments/
    stripe.config.ts        # Stripe client initialization
    webhooks.handler.ts     # Webhook endpoint + event routing
    checkout.service.ts     # Checkout session creation
    subscription.service.ts # Subscription lifecycle
    customer.service.ts     # Customer CRUD + portal
    invoice.service.ts      # Invoice customization
    tax.service.ts          # Tax calculation
    types.ts                # Shared types
  middleware/
    webhook-verify.ts       # Signature verification middleware
```

### 7 条架构规则

1. **切勿完全信任客户端** — 必须通过服务器端的 webhook 验证支付状态，切勿依赖重定向 URL。
2. **Webhook 是数据来源** — 数据库更新应基于 webhook 事件，而非 API 调用响应。
3. **所有 API 调用都必须具有幂等性** — 每次修改数据的 API 调用都必须使用幂等性键。
4. **每个用户只能对应一个 Stripe 客户** — 注册时创建客户账户，并在数据库中存储 `stripe_customer_id`。
5. **元数据非常重要** — 为每个数据对象附加 `user_id`、`plan`、`source` 等元数据，便于调试。
6. **测试模式应与生产环境一致** — 测试环境应使用与生产环境完全相同的代码路径。
7. **切勿存储信用卡号码** — 使用 Stripe.js/Elements 工具，切勿直接处理原始信用卡数据。

---

## 第 2 阶段：核心集成模式

### Stripe 客户端设置

```typescript
// stripe.config.ts
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-12-18.acacia',  // Pin API version!
  maxNetworkRetries: 2,
  timeout: 10_000,
  telemetry: false,
});

export { stripe };
```

**规则：**
- 固定 API 版本，避免使用最新版本。
- 设置明确的超时时间（默认 10 秒即可）。
- 如果涉及隐私敏感信息，请在生产环境中禁用数据收集功能。
- 使用具有最小权限的受限 API 密钥。

### 客户生命周期管理

```typescript
// customer.service.ts
async function getOrCreateCustomer(userId: string, email: string, name?: string) {
  // Check DB first
  const existing = await db.users.findOne({ id: userId });
  if (existing?.stripeCustomerId) {
    return existing.stripeCustomerId;
  }

  // Create in Stripe
  const customer = await stripe.customers.create({
    email,
    name,
    metadata: {
      user_id: userId,
      created_via: 'signup',
    },
  });

  // Store mapping
  await db.users.update({ id: userId }, { stripeCustomerId: customer.id });
  return customer.id;
}
```

**客户相关规则：**
- 在用户注册时创建客户账户，而非在首次购买时。
- 为后续查询设置 `metadata.user_id`。
- 将 `stripe_customer_id` 存储在用户数据库中。
- 通过监听 `customer.updated` 事件来更新客户信息。

### 结账流程（推荐起点）

```typescript
// checkout.service.ts
async function createCheckoutSession(params: {
  customerId: string;
  priceId: string;
  mode: 'payment' | 'subscription';
  successUrl: string;
  cancelUrl: string;
  metadata?: Record<string, string>;
}) {
  const session = await stripe.checkout.sessions.create({
    customer: params.customerId,
    mode: params.mode,
    line_items: [{ price: params.priceId, quantity: 1 }],
    success_url: `${params.successUrl}?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: params.cancelUrl,
    metadata: params.metadata ?? {},

    // Recommended defaults
    allow_promotion_codes: true,
    billing_address_collection: 'auto',
    tax_id_collection: { enabled: true },
    customer_update: { address: 'auto', name: 'auto' },
    payment_method_types: ['card'],
    
    // For subscriptions
    ...(params.mode === 'subscription' && {
      subscription_data: {
        metadata: params.metadata ?? {},
        trial_period_days: 14,
      },
    }),
  }, {
    idempotencyKey: `checkout_${params.customerId}_${params.priceId}_${Date.now()}`,
  });

  return session;
}
```

### 自定义支付界面（Payment Element）

```typescript
// Server: create PaymentIntent
async function createPaymentIntent(params: {
  customerId: string;
  amount: number;      // in cents!
  currency: string;
  metadata?: Record<string, string>;
}) {
  return stripe.paymentIntents.create({
    customer: params.customerId,
    amount: params.amount,
    currency: params.currency,
    automatic_payment_methods: { enabled: true },
    metadata: {
      ...params.metadata,
      created_at: new Date().toISOString(),
    },
  }, {
    idempotencyKey: `pi_${params.customerId}_${params.amount}_${Date.now()}`,
  });
}

// Client: React Payment Element
// <PaymentElement /> handles all payment method rendering
// Use confirmPayment() on form submit
```

---

## 第 3 阶段：订阅管理

### 订阅生命周期事件处理

```
Created → Active → Past Due → Canceled → (optionally) Unpaid
                ↓
            Trialing → Active
                ↓
            Paused → Resumed → Active
```

### 订阅相关的关键 webhook 事件

| 事件 | 对应操作 |
|-------|--------|
| `customer.subscription.created` | 授权用户访问，更新数据库中的订阅计划 |
| `customer.subscription.updated` | 处理计划变更或数量调整 |
| `customer.subscriptiondeleted` | 取消用户访问权限，清理相关数据 |
| `customer.subscription.trial_will_end` | 在试用期结束前发送提醒邮件 |
| `invoice.payment_succeeded` | 确认订阅续费 |
| `invoice.payment_failed` | 启动催款流程 |
| `customer.subscriptionpaused` | 限制用户访问权限，保留相关数据 |
| `customer.subscription.resumed` | 恢复用户访问权限 |

### 订阅计划变更处理

```typescript
// Upgrade (immediate)
async function upgradePlan(subscriptionId: string, newPriceId: string) {
  const sub = await stripe.subscriptions.retrieve(subscriptionId);
  return stripe.subscriptions.update(subscriptionId, {
    items: [{
      id: sub.items.data[0].id,
      price: newPriceId,
    }],
    proration_behavior: 'create_prorations',  // charge difference immediately
    payment_behavior: 'error_if_incomplete',
  });
}

// Downgrade (at period end)
async function downgradePlan(subscriptionId: string, newPriceId: string) {
  const sub = await stripe.subscriptions.retrieve(subscriptionId);
  return stripe.subscriptions.update(subscriptionId, {
    items: [{
      id: sub.items.data[0].id,
      price: newPriceId,
    }],
    proration_behavior: 'none',               // no refund, change at renewal
    billing_cycle_anchor: 'unchanged',
  });
}

// Cancel (at period end — always prefer this)
async function cancelSubscription(subscriptionId: string) {
  return stripe.subscriptions.update(subscriptionId, {
    cancel_at_period_end: true,
  });
  // User keeps access until period ends
  // Handle `customer.subscription.deleted` to revoke
}
```

### 催款（处理失败支付）

```yaml
# Stripe Dashboard → Settings → Subscriptions → Smart Retries
retry_schedule:
  attempt_1: 1 day after failure    # Smart timing
  attempt_2: 3 days after failure
  attempt_3: 5 days after failure
  attempt_4: 7 days after failure   # Final attempt

# Custom dunning emails (supplement Stripe's built-in)
dunning_sequence:
  - day: 0
    action: "Email: payment failed, update card link"
    template: "Your payment of {amount} failed. Update → {portal_url}"
  - day: 3
    action: "Email: second notice, urgency"
    template: "Still unable to charge. Update payment to avoid interruption."
  - day: 5
    action: "Email: final warning"
    template: "Last chance to update. Access pauses in 48 hours."
  - day: 7
    action: "Pause or cancel subscription"
    note: "Automatic via Stripe if all retries fail"
```

### 按使用量计费

```typescript
// Report usage for metered billing
async function reportUsage(subscriptionItemId: string, quantity: number) {
  return stripe.subscriptionItems.createUsageRecord(subscriptionItemId, {
    quantity,
    timestamp: Math.floor(Date.now() / 1000),
    action: 'increment',  // or 'set' for absolute value
  }, {
    idempotencyKey: `usage_${subscriptionItemId}_${Date.now()}`,
  });
}

// Best practice: batch usage reports
// Don't report every API call individually — aggregate per hour/day
// Report at least daily to avoid surprise bills at period end
```

---

## 第 4 阶段：Webhook（最关键的部分）

### Webhook 处理器模板

```typescript
// webhooks.handler.ts
import { stripe } from './stripe.config';
import type { Request, Response } from 'express';

const WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET!;

// Event handlers map
const handlers: Record<string, (event: Stripe.Event) => Promise<void>> = {
  'checkout.session.completed': handleCheckoutCompleted,
  'customer.subscription.created': handleSubscriptionCreated,
  'customer.subscription.updated': handleSubscriptionUpdated,
  'customer.subscription.deleted': handleSubscriptionDeleted,
  'invoice.payment_succeeded': handleInvoicePaymentSucceeded,
  'invoice.payment_failed': handleInvoicePaymentFailed,
  'customer.subscription.trial_will_end': handleTrialEnding,
  'payment_intent.succeeded': handlePaymentSucceeded,
  'payment_intent.payment_failed': handlePaymentFailed,
};

export async function handleWebhook(req: Request, res: Response) {
  // 1. Verify signature (NEVER skip this)
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(
      req.body,        // raw body, not parsed JSON!
      req.headers['stripe-signature']!,
      WEBHOOK_SECRET,
    );
  } catch (err) {
    console.error('Webhook signature verification failed:', err);
    return res.status(400).send('Invalid signature');
  }

  // 2. Idempotency check
  const alreadyProcessed = await db.webhookEvents.findOne({ eventId: event.id });
  if (alreadyProcessed) {
    return res.status(200).json({ received: true, duplicate: true });
  }

  // 3. Route to handler
  const handler = handlers[event.type];
  if (handler) {
    try {
      await handler(event);
      await db.webhookEvents.insert({ eventId: event.id, type: event.type, processedAt: new Date() });
    } catch (err) {
      console.error(`Webhook handler failed for ${event.type}:`, err);
      return res.status(500).send('Handler error');  // Stripe will retry
    }
  }

  // 4. Always return 200 quickly
  res.status(200).json({ received: true });
}
```

### 10 条 webhook 规则

1. **验证每个 webhook 事件的签名** — 仅处理经过验证的事件。
2. **直接处理原始数据** — 在验证之前不要解析 JSON 数据（Express 中使用 `express.raw({type: 'application/json'})`）。
3. **确保幂等性** — 存储已处理的事件 ID，并妥善处理重复事件。
4. **快速返回 200 状态码** — 重处理逻辑应在后台异步执行。
5. **处理事件顺序混乱的情况** — 事件可能以随机顺序到达，处理前请检查当前状态。
6. **不要仅依赖事件数据** — 对于关键操作，需要从 API 重新获取相关数据。
7. **详细记录所有事件** — 包括事件 ID、类型、相关对象 ID 和处理结果。
8. **监控错误情况** — 对于频繁出现的 500 状态码或未处理的事件类型，及时发出警报。
9. **使用 CLI 进行本地开发** — 使用 `stripe listen --forward-to localhost:3000/webhooks` 命令进行测试。
10. **仅订阅需要处理的事件** — 避免无谓地订阅所有 webhook 事件。

### 根据使用场景划分的必备事件

| 使用场景 | 必需处理的 webhook 事件 |
|----------|-----------------|
| 一次性支付 | `checkout.session_completed`, `payment_intent.succeeded`, `payment_intent.payment_failed` |
| 订阅服务 | 所有与订阅相关的事件 + `invoice.payment_succeeded`, `invoice.payment_failed`, `invoice.upcoming` |
| 市场places/Connect | `account.updated`, `payout.paid`, `payout_failed`, `transfer.created` |
| 开票 | `invoice.created`, `invoice.finalized`, `invoice.payment_failed` |

---

## 第 5 阶段：客户门户与自助服务

```typescript
// Customer portal — saves you building billing UI
async function createPortalSession(customerId: string, returnUrl: string) {
  return stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: returnUrl,
  });
}

// Configure in Dashboard → Settings → Customer portal
// Enable: Update payment method, Cancel subscription, View invoices
// Optional: Plan switching, Invoice history download
```

### 客户门户配置检查项

- [ ] 已启用支付方式更新功能
- [ ] 支持取消订阅并记录取消原因
- [ ] 支持切换订阅计划并显示费用分摊情况
- [ ] 可查看发票历史记录
- [ ] 已设置企业信息（名称、Logo）
- [ ] 已配置退货链接
- [ ] 已链接服务条款/隐私政策

---

## 第 6 阶段：税务处理

### 税务处理策略

```
Do you sell to EU customers?
  YES → Need VAT collection
    Use Stripe Tax (automatic) OR manual tax rates
  NO → 
Do you sell to US customers in multiple states?
  YES → Need sales tax (nexus rules)
    Use Stripe Tax (automatic) — manual is nightmare
  NO →
Do you exceed $100K revenue or 200 transactions in any US state?
  YES → You have economic nexus — collect tax
  NO → May not need to collect, but verify with accountant
```

### Stripe 税务配置

```typescript
// Enable automatic tax on Checkout
const session = await stripe.checkout.sessions.create({
  // ... other config
  automatic_tax: { enabled: true },
  customer_update: { address: 'auto' },  // Required for tax calculation
});

// For subscriptions via API
const subscription = await stripe.subscriptions.create({
  customer: customerId,
  items: [{ price: priceId }],
  automatic_tax: { enabled: true },
});
```

**税务相关规则：**
- Stripe 负责自动计算和收取税款。
- 你仍需自行申报或通过 Stripe 提供的税务服务进行税款缴纳（仅适用于支持的区域）。
- 为 B2B 交易务必收集正确的账单地址信息。

---

## 第 7 阶段：Stripe Connect（适用于市场places 和平台）

### 连接账户类型

| 连接类型 | 控制权限 | 上线流程 | 适用场景 |
|------|---------|------------|----------|
| **Standard** | 权限较低（由 Stripe 提供托管的仪表盘） | 适用于卖家自行管理 Stripe 账户的市场places |
| **Express** | 权限中等（仪表盘功能有限） | 适用于需要管理支付流程的平台 |
| **Custom** | 权限最高（完全自定义） | 适用于需要全面控制支付流程的企业平台 |

**决策规则：** 除非有特殊原因，否则建议使用 Express 类型。

### 支付流程设计

```typescript
// Direct charge (platform takes cut)
const paymentIntent = await stripe.paymentIntents.create({
  amount: 10000,  // $100
  currency: 'usd',
  application_fee_amount: 1500,  // $15 platform fee
  transfer_data: {
    destination: 'acct_seller123',
  },
});

// Destination charge (seller's Stripe processes)
// Same as above but payment appears on seller's statement

// Separate charges and transfers (most flexible)
const charge = await stripe.paymentIntents.create({
  amount: 10000,
  currency: 'usd',
});
// Then transfer to seller
const transfer = await stripe.transfers.create({
  amount: 8500,
  currency: 'usd',
  destination: 'acct_seller123',
  transfer_group: 'order_123',
});
```

---

## 第 8 阶段：测试策略

### 测试模式检查项

| 测试内容 | 测试方法 | 通过标准 |
|------|-----|--------------|
| 成功支付 | 使用测试卡号（例如 42424242424242424）完成支付流程，验证 webhook 是否触发，检查数据库是否更新 |
| 卡号被拒绝 | 使用测试卡号（例如 4000000000000002），检查是否显示错误信息，数据库是否更新 |
| 需要 3D Secure 验证 | 使用测试卡号（例如 4000002500003155），验证认证流程是否正常 |
| 账户余额不足 | 使用测试卡号（例如 4000000000009995），检查系统是否能优雅地处理失败情况 |
| 新订阅创建 | 使用测试价格完成支付流程，确认订阅是否生效 |
| 支付失败并尝试重试 | 使用测试卡号（例如 4000000000000341），触发催款流程 |
| Webhook 重放 | 使用 `stripe events resendevt_xxx` 命令重新发送 webhook 事件，确保处理过程不会重复 |
| 退款 | 通过 API 或客户门户处理退款操作 |
| 升级/降级订阅 | 在订阅周期结束时处理升级/降级操作，确保费用分摊正确 |

### Stripe CLI 在本地开发中的使用

```bash
# Install
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Trigger specific events for testing
stripe trigger checkout.session.completed
stripe trigger invoice.payment_failed
stripe trigger customer.subscription.deleted
```

---

## 第 9 阶段：安全性与 PCI 合规性

### PCI 合规性要求

| 合规性级别 | 相关要求 |
|-------|----------|-------------|
| **SAQ-A** | 推荐使用 Checkout 或 Payment Element 功能，每年提交一次问卷 |
| **SAQ-A-EP** | 需在客户端进行令牌化处理，每年提交一次问卷并定期进行安全扫描 |
| **SAQ-D** | 避免直接使用 Direct API 处理信用卡信息，需进行全面审计和定期安全扫描 |

### 安全性检查项（P0 — 强制要求）

- **API 密钥必须存储在环境变量中，切勿写入代码**。
- **每次请求时都要验证 webhook 签名**。
- **仅允许使用具有最小权限的受限 API 密钥**。
- **所有接口都必须使用 HTTPS 协议**（Stripe 有此要求）。
- **严禁存储、传输或记录信用卡号码**。
- **在支付接口上实施 CSRF 防护**。
- **对每次 API 调用实施速率限制**。
- **所有会修改数据的 API 调用都必须使用幂等性键**。

### API 密钥管理策略

```
Live mode:
  sk_live_xxx    → Server only, env var, restricted permissions
  pk_live_xxx    → Client-side (public, safe to expose)
  whsec_xxx      → Webhook secret, server only

Test mode:
  sk_test_xxx    → Same restrictions as live
  pk_test_xxx    → Client-side
  whsec_test_xxx → Webhook secret (different from live!)
```

**API 密钥的权限设置（在 Dashboard 中配置）：**
- **Checkout 会话相关操作**：写入权限
- **客户信息相关操作**：写入权限
- **订阅相关操作**：读取/写入权限
- **Webhook 端点相关操作**：仅允许读取权限
- **其他所有操作**：无写入权限

---

## 第 10 阶段：上线准备（P0 — 强制要求）

- **Webhook 端点已注册并在生产环境中验证**。
- **所有需要的 webhook 事件均已订阅**（与测试阶段相同）。
- **生产环境中的 API 密钥已配置**。
- **客户门户已配置并显示正确的品牌信息**。
- **进行真实的支付测试（金额为 1 美元），然后进行退款操作**。
- **针对所有支付状态（成功、失败、待处理等）设置错误处理逻辑**。
- **记录每次交易的支付 ID、客户 ID、金额和状态**。
- **确保在 Stripe 仪表板中完成 PCI 合规性问卷的填写**。

### 上线准备（P1 — 在上线前一周内完成）

- **监控支付失败率（超过 5% 时发出警报）**。
- **监控 webhook 发送失败的情况**。
- **配置好退款邮件**（Stripe 可自动发送或手动设置）。
- **完善退款流程**。
- **设置好争议/退款响应机制**。
- **为订阅服务启用税务处理功能（如适用）**。

### 上线准备（P2 — 在上线后一个月内完成）

- **配置收入分析仪表盘**。
- **跟踪月度收入（MRR）和客户流失情况**。
- **制定优惠券/促销代码策略**。
- **允许用户切换年度/月度定价模式**。
- **验证客户门户的自助服务功能**。

---

## 第 11 阶段：监控与运营维护

### 关键指标监控仪表盘

```yaml
metrics:
  payment_success_rate:
    calculation: "successful_payments / total_attempts × 100"
    healthy: ">= 95%"
    warning: "90-95%"
    critical: "< 90%"
    
  webhook_delivery_rate:
    calculation: "successful_deliveries / total_events × 100"  
    healthy: ">= 99.5%"
    critical: "< 99%"
    
  average_revenue_per_user:
    calculation: "total_revenue / active_customers"
    track: "weekly trend"
    
  monthly_recurring_revenue:
    calculation: "sum(active_subscription_amounts)"
    track: "monthly growth rate"
    
  churn_rate:
    calculation: "canceled_subscriptions / total_active × 100"
    healthy: "< 5% monthly"
    warning: "5-10%"
    critical: "> 10%"
    
  involuntary_churn:
    calculation: "failed_payment_cancellations / total_churn × 100"
    note: "Should be < 30% of total churn — fix with better dunning"
```

### 周度监控检查项

- **支付成功率与上周相比的情况**。
- **支付失败的情况（分析卡类型、地区和金额等）。
- **Webhook 失败的情况（检查是否有接口超时）**。
- **新产生的争议/退款请求（需在 7 天内响应）**。
- **订阅相关的指标（新订阅、流失用户、升级/降级用户等）**。
- **收入相关指标（月度收入、新增订阅收入、扩张/收缩带来的收入变化）**。

---

## 第 12 阶段：高级功能

### 具有年度定价切换功能的定价页面

```typescript
// Create both monthly and annual prices for each plan
const prices = {
  starter: {
    monthly: 'price_starter_monthly',   // $29/mo
    annual: 'price_starter_annual',     // $290/yr (save ~17%)
  },
  pro: {
    monthly: 'price_pro_monthly',       // $79/mo
    annual: 'price_pro_annual',         // $790/yr
  },
};

// Client toggles monthly/annual → creates checkout with correct priceId
```

### 旧版本数据的处理与价格调整

```typescript
// New price, existing customers keep old price
// 1. Create new price object (don't modify existing)
// 2. New signups use new price
// 3. Existing subs stay on old price until they change plans
// 4. Optional: scheduled price migration with notice

async function schedulePriceIncrease(subscriptionId: string, newPriceId: string, effectiveDate: Date) {
  // Create a subscription schedule
  const schedule = await stripe.subscriptionSchedules.create({
    from_subscription: subscriptionId,
  });
  
  // Add phase with new price
  await stripe.subscriptionSchedules.update(schedule.id, {
    phases: [
      { items: [{ price: currentPriceId }], end_date: Math.floor(effectiveDate.getTime() / 1000) },
      { items: [{ price: newPriceId }] },
    ],
  });
}
```

### 优惠券与促销代码的管理

```typescript
// Create coupon (reusable)
const coupon = await stripe.coupons.create({
  percent_off: 20,
  duration: 'repeating',
  duration_in_months: 3,
  max_redemptions: 100,
  metadata: { campaign: 'launch_2024' },
});

// Create promotion code (shareable link)
const promoCode = await stripe.promotionCodes.create({
  coupon: coupon.id,
  code: 'LAUNCH20',
  max_redemptions: 50,
  expires_at: Math.floor(new Date('2024-12-31').getTime() / 1000),
});
```

### 争议处理（退款流程）

```yaml
dispute_response_process:
  when_received:
    - Log dispute details: amount, reason, deadline
    - Alert team immediately
    - Begin evidence collection within 24 hours
    
  evidence_to_collect:
    - Customer communication (emails, chat logs)
    - Delivery proof (access logs, download records)
    - Terms of service acceptance timestamp
    - Refund policy shown at checkout
    - IP address and device fingerprint
    - Prior successful transactions from same customer
    
  submit:
    - Within 7 days (Stripe deadline is usually 21 days, but act fast)
    - Use Stripe Dashboard evidence submission form
    - Include written rebuttal addressing specific reason code
    
  prevention:
    - Clear billing descriptor (customer recognizes charge)
    - Send receipt emails immediately
    - Offer easy refunds before disputes escalate
    - Use Radar for fraud detection
```

---

## 10 个常见错误

| 编号 | 错误内容 | 修复方法 |
|---|---------|-----|
| 1 | 仅依赖客户端重定向来确认支付完成 | 必须通过 webhook 进行验证 |
| 2 | 在验证 webhook 签名之前解析 JSON 数据 | 应直接使用原始数据 |
| 3 | API 调用时未使用幂等性键 | 必须为所有会修改数据的 API 调用添加幂等性键 |
| 4 | 在订阅周期结束前立即取消订阅 | 除非需要退款，否则应在周期结束时取消订阅 |
| 5 | 金额单位使用美元而非分 | Stripe 使用最小的货币单位（分） |
| 6 | 未处理 3D Secure 验证或支付状态确认 | 必须检查 `payment_intent.status` 并处理相应的认证逻辑 |
| 7 | 在测试环境和生产环境中使用相同的 webhook 密钥 | 应为不同环境设置不同的 webhook 密钥 |
| 8 | 未使用 Stripe CLI 进行本地测试 | 必须在开发环境中设置 `stripe listen` 命令 |
| 9 | 硬编码价格信息 | 应使用配置文件或环境变量来动态设置价格信息 |
| 10 | 未为失败订阅设置退款机制 | 必须配置自动重试机制并发送相应的退款邮件 |

---

## 质量评估标准（0-100 分）

| 评估维度 | 权重 | 评估标准 |
|-----------|--------|----------|
| Webhook 可靠性 | 25% | 签名验证、幂等性处理、错误处理、事件覆盖范围 |
| 安全性与 PCI 合规性 | 20% | 是否满足 SAQ-A 合规性要求、密钥管理是否正确、是否避免泄露信用卡信息 |
| 订阅服务管理 | 15% | 订阅的创建/升级/降级/取消等操作是否正确处理 |
| 客户体验 | 15% | 客户门户、退款通知、错误信息的清晰度 |
| 测试覆盖范围 | 10% | 是否覆盖了所有支付场景、CLI 设置是否正确、边缘情况是否得到处理 |
| 监控机制 | 10% | 是否能及时发现错误、监控收入相关指标 |
| 代码质量 | 5% | 代码类型、错误处理逻辑、幂等性键的使用等 |

---

## 命令说明

代理可以执行以下自然语言指令：

1. “Set up Stripe checkout”：配置完整的 Checkout 集成，并设置 webhook 处理器。
2. “Add subscriptions”：实现订阅服务的生命周期管理，包括计划变更和催款功能。
3. “Configure webhooks”：配置 webhook 处理器，并确保签名验证和幂等性处理正确。
4. “Set up customer portal”：配置客户门户的相关功能。
5. “Add usage-based billing”：实现按使用量计费的订阅服务，并提供使用量报告功能。
6. “Stripe security audit”：检查系统的 PCI 合规性并加强系统安全性。
7. “Go-live checklist”：进行上线前的全面验证。
8. “Set up Stripe Connect”：配置适用于市场places 和平台的支付流程。
9. “Add coupons and promos”：设置优惠券和促销代码系统。
10. “Review payment metrics”：查看收入和相关支付指标。

---