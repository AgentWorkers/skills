---
name: "stripe-integration-expert"
description: "**Stripe集成专家**  
**职责概述：**  
作为Stripe集成专家，您将负责协助企业或开发团队将他们的产品或服务与Stripe支付平台进行无缝集成。您的核心任务包括：  
1. **技术设计：** 为项目制定详细的集成方案，确保支付流程的安全性、稳定性和用户体验。  
2. **代码实现：** 编写或修改相关代码，以实现与Stripe API的交互，处理支付请求、响应以及异常处理。  
3. **文档编写：** 撰写技术文档，详细说明集成过程、配置步骤和最佳实践。  
4. **测试与调试：** 进行全面的测试，确保集成功能按预期工作，并解决可能出现的问题。  
5. **客户支持：** 为团队和客户提供技术支持，解答关于Stripe集成的疑问。  
**技能要求：**  
- 熟练掌握Python、JavaScript（或其他用于Web开发的编程语言）  
- 熟悉Stripe API及其相关文档  
- 具备良好的问题解决能力和团队协作精神  
- 熟悉支付行业的相关法规和最佳实践  
**工作经验：**  
- 至少2年Stripe集成相关工作经验  
- 有成功实现复杂支付集成项目的经验  
**职位优势：**  
- 获得Stripe官方认证的集成专家认证（如Stripe Certified Integration Specialist）  
- 了解最新的支付技术和行业趋势  
**加入我们，成为支付解决方案的领导者！**"
---
# Stripe 集成专家

**等级：** 高级  
**类别：** 工程团队  
**领域：** 支付/计费基础设施  

---

## 概述  

实现生产级的 Stripe 集成功能，包括：带试用期的订阅服务、按比例计费的订阅服务、一次性支付、基于使用量的计费、结账流程、幂等性的 Webhook 处理程序、客户门户以及发票生成。支持 Next.js、Express 和 Django 开发框架。  

---

## 核心功能  

- 订阅生命周期管理（创建、升级、降级、取消、暂停）  
- 试用期处理及转化跟踪  
- 按比例计费及信用额度申请  
- 基于使用量的计费（采用计量定价方式）  
- 带签名验证的幂等性 Webhook 处理程序  
- 客户门户集成  
- 发票生成及 PDF 文件下载  
- 完整的 Stripe CLI（命令行工具）本地测试环境  

---

## 适用场景  

- 为任何 Web 应用程序添加订阅计费功能  
- 实现按比例计算的订阅计划升级/降级  
- 构建基于使用量或座位数的计费系统  
- 调试 Webhook 发送失败的问题  
- 从一种计费模式迁移到另一种计费模式  

---

## 订阅生命周期状态机  

```
FREE_TRIAL ──paid──► ACTIVE ──cancel──► CANCEL_PENDING ──period_end──► CANCELED
     │                  │                                                    │
     │               downgrade                                            reactivate
     │                  ▼                                                    │
     │             DOWNGRADING ──period_end──► ACTIVE (lower plan)           │
     │                                                                        │
     └──trial_end without payment──► PAST_DUE ──payment_failed 3x──► CANCELED
                                          │
                                     payment_success
                                          │
                                          ▼
                                        ACTIVE
```  

### 数据库中的订阅状态值：  
`trialing | active | past_due | canceled | cancel_pending | paused | unpaid`  

---

## Stripe 客户端配置  

```typescript
// lib/stripe.ts
import Stripe from "stripe"

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: "2024-04-10",
  typescript: true,
  appInfo: {
    name: "myapp",
    version: "1.0.0",
  },
})

// Price IDs by plan (set in env)
export const PLANS = {
  starter: {
    monthly: process.env.STRIPE_STARTER_MONTHLY_PRICE_ID!,
    yearly: process.env.STRIPE_STARTER_YEARLY_PRICE_ID!,
    features: ["5 projects", "10k events"],
  },
  pro: {
    monthly: process.env.STRIPE_PRO_MONTHLY_PRICE_ID!,
    yearly: process.env.STRIPE_PRO_YEARLY_PRICE_ID!,
    features: ["Unlimited projects", "1M events"],
  },
} as const
```  

---

## 结账流程（Next.js 应用程序路由器）  

```typescript
// app/api/billing/checkout/route.ts
import { NextResponse } from "next/server"
import { stripe } from "@/lib/stripe"
import { getAuthUser } from "@/lib/auth"
import { db } from "@/lib/db"

export async function POST(req: Request) {
  const user = await getAuthUser()
  if (!user) return NextResponse.json({ error: "Unauthorized" }, { status: 401 })

  const { priceId, interval = "monthly" } = await req.json()

  // Get or create Stripe customer
  let stripeCustomerId = user.stripeCustomerId
  if (!stripeCustomerId) {
    const customer = await stripe.customers.create({
      email: user.email,
      name: "username-undefined"
      metadata: { userId: user.id },
    })
    stripeCustomerId = customer.id
    await db.user.update({ where: { id: user.id }, data: { stripeCustomerId } })
  }

  const session = await stripe.checkout.sessions.create({
    customer: stripeCustomerId,
    mode: "subscription",
    payment_method_types: ["card"],
    line_items: [{ price: priceId, quantity: 1 }],
    allow_promotion_codes: true,
    subscription_data: {
      trial_period_days: user.hasHadTrial ? undefined : 14,
      metadata: { userId: user.id },
    },
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
    metadata: { userId: user.id },
  })

  return NextResponse.json({ url: session.url })
}
```  

---

## 订阅升级/降级  

```typescript
// lib/billing.ts
export async function changeSubscriptionPlan(
  subscriptionId: string,
  newPriceId: string,
  immediate = false
) {
  const subscription = await stripe.subscriptions.retrieve(subscriptionId)
  const currentItem = subscription.items.data[0]

  if (immediate) {
    // Upgrade: apply immediately with proration
    return stripe.subscriptions.update(subscriptionId, {
      items: [{ id: currentItem.id, price: newPriceId }],
      proration_behavior: "always_invoice",
      billing_cycle_anchor: "unchanged",
    })
  } else {
    // Downgrade: apply at period end, no proration
    return stripe.subscriptions.update(subscriptionId, {
      items: [{ id: currentItem.id, price: newPriceId }],
      proration_behavior: "none",
      billing_cycle_anchor: "unchanged",
    })
  }
}

// Preview proration before confirming upgrade
export async function previewProration(subscriptionId: string, newPriceId: string) {
  const subscription = await stripe.subscriptions.retrieve(subscriptionId)
  const prorationDate = Math.floor(Date.now() / 1000)

  const invoice = await stripe.invoices.retrieveUpcoming({
    customer: subscription.customer as string,
    subscription: subscriptionId,
    subscription_items: [{ id: subscription.items.data[0].id, price: newPriceId }],
    subscription_proration_date: prorationDate,
  })

  return {
    amountDue: invoice.amount_due,
    prorationDate,
    lineItems: invoice.lines.data,
  }
}
```  

---

## 完整的 Webhook 处理程序（幂等性设计）  

```typescript
// app/api/webhooks/stripe/route.ts
import { NextResponse } from "next/server"
import { headers } from "next/headers"
import { stripe } from "@/lib/stripe"
import { db } from "@/lib/db"
import Stripe from "stripe"

// Processed events table to ensure idempotency
async function hasProcessedEvent(eventId: string): Promise<boolean> {
  const existing = await db.stripeEvent.findUnique({ where: { id: eventId } })
  return !!existing
}

async function markEventProcessed(eventId: string, type: string) {
  await db.stripeEvent.create({ data: { id: eventId, type, processedAt: new Date() } })
}

export async function POST(req: Request) {
  const body = await req.text()
  const signature = headers().get("stripe-signature")!

  let event: Stripe.Event
  try {
    event = stripe.webhooks.constructEvent(body, signature, process.env.STRIPE_WEBHOOK_SECRET!)
  } catch (err) {
    console.error("Webhook signature verification failed:", err)
    return NextResponse.json({ error: "Invalid signature" }, { status: 400 })
  }

  // Idempotency check
  if (await hasProcessedEvent(event.id)) {
    return NextResponse.json({ received: true, skipped: true })
  }

  try {
    switch (event.type) {
      case "checkout.session.completed":
        await handleCheckoutCompleted(event.data.object as Stripe.Checkout.Session)
        break

      case "customer.subscription.created":
      case "customer.subscription.updated":
        await handleSubscriptionUpdated(event.data.object as Stripe.Subscription)
        break

      case "customer.subscription.deleted":
        await handleSubscriptionDeleted(event.data.object as Stripe.Subscription)
        break

      case "invoice.payment_succeeded":
        await handleInvoicePaymentSucceeded(event.data.object as Stripe.Invoice)
        break

      case "invoice.payment_failed":
        await handleInvoicePaymentFailed(event.data.object as Stripe.Invoice)
        break

      default:
        console.log(`Unhandled event type: ${event.type}`)
    }

    await markEventProcessed(event.id, event.type)
    return NextResponse.json({ received: true })
  } catch (err) {
    console.error(`Error processing webhook ${event.type}:`, err)
    // Return 500 so Stripe retries — don't mark as processed
    return NextResponse.json({ error: "Processing failed" }, { status: 500 })
  }
}

async function handleCheckoutCompleted(session: Stripe.Checkout.Session) {
  if (session.mode !== "subscription") return
  
  const userId = session.metadata?.userId
  if (!userId) throw new Error("No userId in checkout session metadata")

  const subscription = await stripe.subscriptions.retrieve(session.subscription as string)
  
  await db.user.update({
    where: { id: userId },
    data: {
      stripeCustomerId: session.customer as string,
      stripeSubscriptionId: subscription.id,
      stripePriceId: subscription.items.data[0].price.id,
      stripeCurrentPeriodEnd: new Date(subscription.current_period_end * 1000),
      subscriptionStatus: subscription.status,
      hasHadTrial: true,
    },
  })
}

async function handleSubscriptionUpdated(subscription: Stripe.Subscription) {
  const user = await db.user.findUnique({
    where: { stripeSubscriptionId: subscription.id },
  })
  if (!user) {
    // Look up by customer ID as fallback
    const customer = await db.user.findUnique({
      where: { stripeCustomerId: subscription.customer as string },
    })
    if (!customer) throw new Error(`No user found for subscription ${subscription.id}`)
  }

  await db.user.update({
    where: { stripeSubscriptionId: subscription.id },
    data: {
      stripePriceId: subscription.items.data[0].price.id,
      stripeCurrentPeriodEnd: new Date(subscription.current_period_end * 1000),
      subscriptionStatus: subscription.status,
      cancelAtPeriodEnd: subscription.cancel_at_period_end,
    },
  })
}

async function handleSubscriptionDeleted(subscription: Stripe.Subscription) {
  await db.user.update({
    where: { stripeSubscriptionId: subscription.id },
    data: {
      stripeSubscriptionId: null,
      stripePriceId: null,
      stripeCurrentPeriodEnd: null,
      subscriptionStatus: "canceled",
    },
  })
}

async function handleInvoicePaymentFailed(invoice: Stripe.Invoice) {
  if (!invoice.subscription) return
  const attemptCount = invoice.attempt_count
  
  await db.user.update({
    where: { stripeSubscriptionId: invoice.subscription as string },
    data: { subscriptionStatus: "past_due" },
  })

  if (attemptCount >= 3) {
    // Send final dunning email
    await sendDunningEmail(invoice.customer_email!, "final")
  } else {
    await sendDunningEmail(invoice.customer_email!, "retry")
  }
}

async function handleInvoicePaymentSucceeded(invoice: Stripe.Invoice) {
  if (!invoice.subscription) return

  await db.user.update({
    where: { stripeSubscriptionId: invoice.subscription as string },
    data: {
      subscriptionStatus: "active",
      stripeCurrentPeriodEnd: new Date(invoice.period_end * 1000),
    },
  })
}
```  

---

## 基于使用量的计费  

```typescript
// Report usage for metered subscriptions
export async function reportUsage(subscriptionItemId: string, quantity: number) {
  await stripe.subscriptionItems.createUsageRecord(subscriptionItemId, {
    quantity,
    timestamp: Math.floor(Date.now() / 1000),
    action: "increment",
  })
}

// Example: report API calls in middleware
export async function trackApiCall(userId: string) {
  const user = await db.user.findUnique({ where: { id: userId } })
  if (user?.stripeSubscriptionId) {
    const subscription = await stripe.subscriptions.retrieve(user.stripeSubscriptionId)
    const meteredItem = subscription.items.data.find(
      (item) => item.price.recurring?.usage_type === "metered"
    )
    if (meteredItem) {
      await reportUsage(meteredItem.id, 1)
    }
  }
}
```  

---

## 客户门户  

```typescript
// app/api/billing/portal/route.ts
import { NextResponse } from "next/server"
import { stripe } from "@/lib/stripe"
import { getAuthUser } from "@/lib/auth"

export async function POST() {
  const user = await getAuthUser()
  if (!user?.stripeCustomerId) {
    return NextResponse.json({ error: "No billing account" }, { status: 400 })
  }

  const portalSession = await stripe.billingPortal.sessions.create({
    customer: user.stripeCustomerId,
    return_url: `${process.env.NEXT_PUBLIC_APP_URL}/settings/billing`,
  })

  return NextResponse.json({ url: portalSession.url })
}
```  

---

## 使用 Stripe CLI 进行测试  

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to local dev
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Trigger specific events for testing
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
stripe trigger invoice.payment_failed

# Test with specific customer
stripe trigger customer.subscription.updated \
  --override subscription:customer=cus_xxx

# View recent events
stripe events list --limit 10

# Test cards
# Success: 4242 4242 4242 4242
# Requires auth: 4000 0025 0000 3155
# Decline: 4000 0000 0000 9995
# Insufficient funds: 4000 0000 0000 9995
```  

---

## 功能开关辅助工具  

```typescript
// lib/subscription.ts
export function isSubscriptionActive(user: { subscriptionStatus: string | null, stripeCurrentPeriodEnd: Date | null }) {
  if (!user.subscriptionStatus) return false
  if (user.subscriptionStatus === "active" || user.subscriptionStatus === "trialing") return true
  // Grace period: past_due but not yet expired
  if (user.subscriptionStatus === "past_due" && user.stripeCurrentPeriodEnd) {
    return user.stripeCurrentPeriodEnd > new Date()
  }
  return false
}

// Middleware usage
export async function requireActiveSubscription() {
  const user = await getAuthUser()
  if (!isSubscriptionActive(user)) {
    redirect("/billing?reason=subscription_required")
  }
}
```  

---

## 常见问题  

- **Webhook 发送顺序不可保证** — 必须始终从 Stripe API 重新获取数据，切勿仅依赖事件数据来更新数据库  
- **Webhook 可能被重复处理** — Stripe 会在收到 500 错误时重试；务必使用幂等性机制  
- **试用期转化跟踪** — 在数据库中存储 `hasHadTrial: true` 字段以防止滥用试用期  
- **按比例计费可能带来意外** — 升级前务必预览费用详情；确认前向用户展示费用金额  
- **客户门户未配置** — 必须在 Stripe 仪表板的“计费” → “客户门户设置”中启用相关功能  
- **结账时缺少元数据** — 必须在元数据中传递 `userId`；否则无法将订阅信息与用户关联  

---