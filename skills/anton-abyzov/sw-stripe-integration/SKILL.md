---
name: stripe-integration
description: **Stripe支付集成**  
适用于结账、订阅服务、Webhook通知以及Connect市场模式的场景。适用于实现Stripe支付功能、处理支付相关的Webhook通知，或构建订阅计费系统。内容包括：双重确认机制（Webhook + 前端验证）、移动支付验证、100%促销代码的处理方式，以及幂等性（idempotent）的支付操作。
---

# Stripe集成

掌握Stripe支付处理集成技术，以实现强大且符合PCI标准的支付流程，包括结账、订阅、Webhook、Stripe Connect市场支付以及移动/网页支付验证等功能。

## 何时使用此技能

- 在Web/移动应用程序中实现支付处理
- 设置订阅计费系统
- 处理一次性支付和定期收费
- 处理退款和争议
- 管理客户的支付方式
- 为欧洲地区的支付实现SCA（强客户认证）
- 使用Stripe Connect构建市场支付流程
- 实现直接收费（Direct Charge）或目标账户收费（Destination Charge）模式
- 处理促销代码和100%折扣场景
- 实现双重确认机制（Webhook + 前端验证）
- 管理库存/预订资源，确保操作的原子性

## 核心概念

### 1. 支付流程
**结账会话（托管式）**
- 由Stripe托管的支付页面
- PCI合规要求较低
- 实现速度最快
- 支持一次性支付和定期支付

**支付意图（自定义用户界面）**
- 对支付用户界面有完全控制权
- 需要Stripe.js来满足PCI合规要求
- 实现难度较高
- 提供更多的定制选项

**设置意图（保存支付方式）**
- 收集支付方式信息，但不进行扣费
- 用于订阅和未来的支付
- 需要客户确认

### 2. Webhook
**关键事件：**
- `payment_intent.succeeded`：支付完成
- `payment_intent.payment_failed`：支付失败
- `checkout.session_completed`：结账会话结束（对于Stripe Connect至关重要！）
- `checkout.session.expired`：结账会话超时
- `customer.subscription.updated`：订阅信息更新
- `customer.subscriptiondeleted`：订阅取消
- `charge.refunded`：退款处理完成
- `invoice.payment_succeeded`：订阅付款成功
- `account.updated`：Connect账户状态更新
- `payout.paid` / `payout_FAILED`：Connect账户的支付状态

### 3. 订阅
**组成部分：**
- **产品**：你销售的商品或服务
- **价格**：价格及支付频率
- **订阅**：客户的定期付款
- **发票**：每个计费周期生成的账单

### 4. 客户管理
- 创建和管理客户记录
- 存储多种支付方式
- 跟踪客户元数据
- 管理账单详情

### 5. Stripe Connect（市场/平台支付）

**收费类型：**

| 类型 | 创建方 | Webhook位置 | 使用场景 |
|------|-------------|------------------|----------|
| **直接收费（Direct Charge）** | 连接的账户（Connected Account） | Connect端点 | 卖家拥有控制权的市场平台 |
| **目标账户收费（Destination Charge）** | 平台（Platform） | 平台端点 | 平台控制支付体验 |
| **单独收费与转账（Separate Charges & Transfers）** | 平台 | 平台端点 | 最高的灵活性 |

**⚠️ 重要提示：直接收费的Webhook设置**  
使用直接收费时，结账会话是在连接的账户上创建的，而不是在平台上。Webhook应发送到Connect端点，而不是平台端点！

```
Platform endpoint:  /webhooks/stripe        → Has general events ✓
Connect endpoint:   /webhooks/stripe/connect → MUST have checkout.session.completed! ✓
```

**Connect端点必须处理的事件：**
- `checkout.session_completed`（对于直接收费至关重要）
- `checkout.session.expired`
- `account.updated`
- `payout.paid` / `payout_FAILED`

## 快速入门

```python
import stripe

stripe.api_key = "sk_test_..."

# Create a checkout session
session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': 'Premium Subscription',
            },
            'unit_amount': 2000,  # $20.00
            'recurring': {
                'interval': 'month',
            },
        },
        'quantity': 1,
    }],
    mode='subscription',
    success_url='https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url='https://yourdomain.com/cancel',
)

# Redirect user to session.url
print(session.url)
```

## 支付实现模式

### 模式1：一次性支付（托管式结账）
```python
def create_checkout_session(amount, currency='usd'):
    """Create a one-time payment checkout session."""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': 'Purchase',
                        'images': ['https://example.com/product.jpg'],
                    },
                    'unit_amount': amount,  # Amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://yourdomain.com/cancel',
            metadata={
                'order_id': 'order_123',
                'user_id': 'user_456'
            }
        )
        return session
    except stripe.error.StripeError as e:
        # Handle error
        print(f"Stripe error: {e.user_message}")
        raise
```

### 模式2：自定义支付意图流程
```python
def create_payment_intent(amount, currency='usd', customer_id=None):
    """Create a payment intent for custom checkout UI."""
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        customer=customer_id,
        automatic_payment_methods={
            'enabled': True,
        },
        metadata={
            'integration_check': 'accept_a_payment'
        }
    )
    return intent.client_secret  # Send to frontend

# Frontend (JavaScript)
"""
const stripe = Stripe('pk_test_...');
const elements = stripe.elements();
const cardElement = elements.create('card');
cardElement.mount('#card-element');

const {error, paymentIntent} = await stripe.confirmCardPayment(
    clientSecret,
    {
        payment_method: {
            card: cardElement,
            billing_details: {
                name: 'Customer Name'
            }
        }
    }
);

if (error) {
    // Handle error
} else if (paymentIntent.status === 'succeeded') {
    // Payment successful
}
"""
```

### 模式3：订阅创建
```python
def create_subscription(customer_id, price_id):
    """Create a subscription for a customer."""
    try:
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{'price': price_id}],
            payment_behavior='default_incomplete',
            payment_settings={'save_default_payment_method': 'on_subscription'},
            expand=['latest_invoice.payment_intent'],
        )

        return {
            'subscription_id': subscription.id,
            'client_secret': subscription.latest_invoice.payment_intent.client_secret
        }
    except stripe.error.StripeError as e:
        print(f"Subscription creation failed: {e}")
        raise
```

### 模式4：客户门户
```python
def create_customer_portal_session(customer_id):
    """Create a portal session for customers to manage subscriptions."""
    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url='https://yourdomain.com/account',
    )
    return session.url  # Redirect customer here
```

## Webhook处理

### 安全的Webhook端点
```python
from flask import Flask, request
import stripe

app = Flask(__name__)

endpoint_secret = 'whsec_...'

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return 'Invalid signature', 400

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_successful_payment(payment_intent)
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_failed_payment(payment_intent)
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_canceled(subscription)

    return 'Success', 200

def handle_successful_payment(payment_intent):
    """Process successful payment."""
    customer_id = payment_intent.get('customer')
    amount = payment_intent['amount']
    metadata = payment_intent.get('metadata', {})

    # Update your database
    # Send confirmation email
    # Fulfill order
    print(f"Payment succeeded: {payment_intent['id']}")

def handle_failed_payment(payment_intent):
    """Handle failed payment."""
    error = payment_intent.get('last_payment_error', {})
    print(f"Payment failed: {error.get('message')}")
    # Notify customer
    # Update order status

def handle_subscription_canceled(subscription):
    """Handle subscription cancellation."""
    customer_id = subscription['customer']
    # Update user access
    # Send cancellation email
    print(f"Subscription canceled: {subscription['id']}")
```

### Webhook最佳实践
```python
import hashlib
import hmac

def verify_webhook_signature(payload, signature, secret):
    """Manually verify webhook signature."""
    expected_sig = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_sig)

def handle_webhook_idempotently(event_id, handler):
    """Ensure webhook is processed exactly once."""
    # Check if event already processed
    if is_event_processed(event_id):
        return

    # Process event
    try:
        handler()
        mark_event_processed(event_id)
    except Exception as e:
        log_error(e)
        # Stripe will retry failed webhooks
        raise
```

## 客户管理
```python
def create_customer(email, name, payment_method_id=None):
    """Create a Stripe customer."""
    customer = stripe.Customer.create(
        email=email,
        name=name,
        payment_method=payment_method_id,
        invoice_settings={
            'default_payment_method': payment_method_id
        } if payment_method_id else None,
        metadata={
            'user_id': '12345'
        }
    )
    return customer

def attach_payment_method(customer_id, payment_method_id):
    """Attach a payment method to a customer."""
    stripe.PaymentMethod.attach(
        payment_method_id,
        customer=customer_id
    )

    # Set as default
    stripe.Customer.modify(
        customer_id,
        invoice_settings={
            'default_payment_method': payment_method_id
        }
    )

def list_customer_payment_methods(customer_id):
    """List all payment methods for a customer."""
    payment_methods = stripe.PaymentMethod.list(
        customer=customer_id,
        type='card'
    )
    return payment_methods.data
```

## 退款处理
```python
def create_refund(payment_intent_id, amount=None, reason=None):
    """Create a refund."""
    refund_params = {
        'payment_intent': payment_intent_id
    }

    if amount:
        refund_params['amount'] = amount  # Partial refund

    if reason:
        refund_params['reason'] = reason  # 'duplicate', 'fraudulent', 'requested_by_customer'

    refund = stripe.Refund.create(**refund_params)
    return refund

def handle_dispute(charge_id, evidence):
    """Update dispute with evidence."""
    stripe.Dispute.modify(
        charge_id,
        evidence={
            'customer_name': evidence.get('customer_name'),
            'customer_email_address': evidence.get('customer_email'),
            'shipping_documentation': evidence.get('shipping_proof'),
            'customer_communication': evidence.get('communication'),
        }
    )
```

## 测试
```python
# Use test mode keys
stripe.api_key = "sk_test_..."

# Test card numbers
TEST_CARDS = {
    'success': '4242424242424242',
    'declined': '4000000000000002',
    '3d_secure': '4000002500003155',
    'insufficient_funds': '4000000000009995'
}

def test_payment_flow():
    """Test complete payment flow."""
    # Create test customer
    customer = stripe.Customer.create(
        email="test@example.com"
    )

    # Create payment intent
    intent = stripe.PaymentIntent.create(
        amount=1000,
        currency='usd',
        customer=customer.id,
        payment_method_types=['card']
    )

    # Confirm with test card
    confirmed = stripe.PaymentIntent.confirm(
        intent.id,
        payment_method='pm_card_visa'  # Test payment method
    )

    assert confirmed.status == 'succeeded'
```

## ⚠️ 生产环境中的关键注意事项

### 1. 100%促销代码检测（错误与正确处理方式）

**常见错误：**
```python
# ❌ WRONG - no_payment_required is for different scenarios!
if session.payment_status == 'no_payment_required':
    handle_free_checkout()
```

**正确处理方式：**
```python
# ✅ CORRECT - 100% promo codes have: status=complete, payment_status=paid, amount_total=0
def is_100_percent_promo(session):
    """Detect 100% discount promo code checkout."""
    return (
        session.payment_status == 'paid' and
        session.amount_total == 0 and
        session.payment_intent is None  # No payment intent when $0
    )

# In webhook handler
if session.status == 'complete':
    if is_100_percent_promo(session):
        # Handle free checkout from promo code
        fulfill_order(session)
    else:
        # Normal paid checkout
        fulfill_order(session)
```

**关键提示：** 即使使用促销代码支付金额为0，Stripe也会显示“已支付”。`no_payment_required`状态适用于其他场景（例如按使用量计费的0美元账单）。

---

### 2. 双重确认机制（Webhook + 前端）

**问题：** 仅依赖前端验证时可能出现的问题：**
- 用户在跳转前关闭浏览器
- 验证过程中发生网络错误
- 支付发生在单独标签页中

**解决方案：** 双重确认架构
```
Payment Complete
      ↓
 ┌────┴────┐
 ↓         ↓
Webhook   Frontend
(async)   (polling)
 ↓         ↓
 └────┬────┘
      ↓
First one wins (idempotent)
```

**后端实现：**
```typescript
// Idempotent order confirmation - BOTH webhook and frontend call this
async function confirmPayment(sessionId: string): Promise<boolean> {
  // Atomic conditional update - only updates if still pending
  const result = await db
    .update(orders)
    .set({
      status: 'paid',
      paidAt: new Date(),
      updatedAt: new Date()
    })
    .where(
      and(
        eq(orders.stripeSessionId, sessionId),
        eq(orders.status, 'pending')  // CRITICAL: Only if still pending!
      )
    );

  if (result.changes === 0) {
    // Already processed by other path - that's OK!
    return false;
  }

  // We just confirmed it - now do post-payment work
  await decrementInventory(sessionId);
  await sendConfirmationEmail(sessionId);
  return true;
}

// Webhook endpoint
app.post('/webhooks/stripe', async (req, res) => {
  const event = stripe.webhooks.constructEvent(...);

  if (event.type === 'checkout.session.completed') {
    await confirmPayment(event.data.object.id);
  }

  res.json({ received: true });
});

// Frontend verify endpoint
app.get('/api/verify-payment/:sessionId', async (req, res) => {
  const session = await stripe.checkout.sessions.retrieve(req.params.sessionId);

  if (session.status === 'complete') {
    await confirmPayment(session.id);
    return res.json({ success: true });
  }

  res.json({ success: false, status: session.status });
});
```

**前端实现（React Native/Web）：**
```typescript
async function verifyPaymentWithRetry(
  sessionId: string,
  attempts = 3,
  initialDelay = 1500
): Promise<boolean> {
  let delay = initialDelay;

  for (let i = 0; i < attempts; i++) {
    await sleep(delay);

    try {
      const result = await api.verifyPayment(sessionId);

      if (result.success) return true;

      if (result.status === 'pending') {
        // Still processing - increase delay and retry
        delay = Math.min(delay * 1.5, 5000);
        continue;
      }

      // Failed or expired
      return false;
    } catch (error) {
      // Network error - retry
      delay = Math.min(delay * 1.5, 5000);
    }
  }

  return false;
}
```

---

### 3. 所有支付操作的可重试性

**问题：** Webhook和前端操作可能同时执行，导致：**
- 库存/预订资源被重复减少
- 通知重复发送
- 状态不一致

**解决方案：** 条件更新机制
```sql
-- Only update if still in expected state
UPDATE orders
SET status = 'paid', updated_at = NOW()
WHERE id = $1 AND status = 'pending';

-- Check affected rows
-- If 0 rows affected → another process already handled it → skip side effects
```

**TypeScript/Drizzle实现示例：**
```typescript
async function processPaymentIdempotently(orderId: string) {
  const result = await db
    .update(orders)
    .set({ status: 'paid', updatedAt: new Date() })
    .where(and(
      eq(orders.id, orderId),
      eq(orders.status, 'pending')
    ));

  if (result.changes === 0) {
    // Already processed - safe to skip
    console.log(`Order ${orderId} already processed`);
    return { alreadyProcessed: true };
  }

  // We just confirmed - NOW do side effects
  await decrementInventory(orderId);
  await sendEmail(orderId);

  return { alreadyProcessed: false };
}
```

---

### 4. Web浏览器支付流程（React Native/Expo）

**问题：** `WebBrowser.openBrowserAsync` 在Web和原生环境中的行为不同！**

| 平台 | 返回时间 | `result.type` | 用户状态 |
|----------|---------------|---------------|------------|
| **iOS/Android** | 浏览器关闭后 | `'dismiss'` 或 `'cancel'` | 用户返回应用 |
| **Web** | 立即返回 | `'opened'` | 用户仍在查看Stripe结账页面！ |

**⚠️ 重要提示：** 在Web环境中，不能立即验证支付状态，因为用户可能仍在另一个标签页中查看Stripe结账页面！**

**正确处理方式：** 根据平台进行差异化处理
```typescript
import * as WebBrowser from 'expo-web-browser';
import { Platform, Alert } from 'react-native';

async function handlePayment(checkoutUrl: string, sessionId: string) {
  const result = await WebBrowser.openBrowserAsync(checkoutUrl);

  // Platform-specific handling based on result.type
  switch (result.type) {
    case 'cancel':
      // Native only: User explicitly cancelled (X button)
      // Don't verify - they cancelled intentionally
      Alert.alert('Payment Cancelled', 'You cancelled the payment.');
      break;

    case 'dismiss':
      // Native only: Browser was closed (could be success or cancel)
      // NOW it's safe to verify - user is back in the app
      const success = await verifyPaymentWithRetry(sessionId);
      if (success) {
        navigation.navigate('PaymentSuccess');
      } else {
        navigation.navigate('PaymentPending');
      }
      break;

    case 'opened':
      // WEB ONLY: Browser opened but user is STILL VIEWING STRIPE!
      // Do NOT verify immediately - show dialog instead
      Alert.alert(
        'Complete Your Payment',
        'Please complete your payment in the browser tab, then return here.',
        [
          {
            text: 'I\'ve Completed Payment',
            onPress: async () => {
              const success = await verifyPaymentWithRetry(sessionId);
              if (success) {
                navigation.navigate('PaymentSuccess');
              } else {
                Alert.alert('Payment Not Found', 'We couldn\'t confirm your payment. Please try again or contact support.');
              }
            }
          },
          {
            text: 'Cancel',
            style: 'cancel'
          }
        ]
      );
      break;
  }
}
```

**Web环境的替代方案：** 使用`Window Focus Event`事件
```typescript
// Web-specific: Listen for when user returns to tab
if (Platform.OS === 'web') {
  const handleFocus = async () => {
    window.removeEventListener('focus', handleFocus);
    // User returned to our tab - now verify
    const success = await verifyPaymentWithRetry(sessionId);
    // Handle result...
  };
  window.addEventListener('focus', handleFocus);
}
```

**带有指数退避机制的验证：**
```typescript
async function verifyPaymentWithRetry(
  sessionId: string,
  attempts = 3,
  initialDelay = 1500
): Promise<boolean> {
  let delay = initialDelay;

  for (let i = 0; i < attempts; i++) {
    await sleep(delay);

    try {
      const result = await api.verifyPayment(sessionId);

      if (result.success) return true;

      if (result.status === 'pending') {
        // Still processing - increase delay and retry
        delay = Math.min(delay * 1.5, 5000);
        continue;
      }

      // Failed or expired
      return false;
    } catch (error) {
      // Network error - retry
      delay = Math.min(delay * 1.5, 5000);
    }
  }

  return false;
}

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));
```

---

### 5. 库存/预订资源的管理与原子性

**规则：** 仅在支付确认后修改库存，并确保操作的原子性。

**错误做法：**
```typescript
// ❌ WRONG - Decrementing before payment confirmation
await reserveSlot(slotId);  // Slot decremented
const session = await createCheckoutSession();  // Payment might fail!
// If user abandons → slot is stuck as reserved
```

**正确做法：**
```typescript
// ✅ CORRECT - Only decrement AFTER payment confirmed
async function confirmBookingPayment(sessionId: string) {
  // Atomic update with inventory in single transaction
  const result = await db.transaction(async (tx) => {
    // 1. Mark order as paid (only if pending)
    const orderUpdate = await tx
      .update(orders)
      .set({ status: 'paid' })
      .where(and(
        eq(orders.stripeSessionId, sessionId),
        eq(orders.status, 'pending')
      ));

    if (orderUpdate.changes === 0) {
      return { success: false, reason: 'already_processed' };
    }

    // 2. Get order details
    const order = await tx.query.orders.findFirst({
      where: eq(orders.stripeSessionId, sessionId)
    });

    // 3. Decrement inventory atomically
    const slotUpdate = await tx
      .update(slots)
      .set({
        availableCount: sql`available_count - 1`,
        updatedAt: new Date()
      })
      .where(and(
        eq(slots.id, order.slotId),
        gt(slots.availableCount, 0)  // Prevent negative
      ));

    if (slotUpdate.changes === 0) {
      // Slot became unavailable - need to refund
      throw new Error('SLOT_UNAVAILABLE');
    }

    return { success: true };
  });

  return result;
}
```

---

### 6. Stripe Connect直接收费的Webhook设置

**完整的Connect Webhook处理流程：**
```typescript
// /webhooks/stripe/connect - For Direct Charge events
app.post('/webhooks/stripe/connect',
  express.raw({ type: 'application/json' }),
  async (req, res) => {
    const sig = req.headers['stripe-signature'];
    const connectWebhookSecret = process.env.STRIPE_CONNECT_WEBHOOK_SECRET!;

    let event;
    try {
      event = stripe.webhooks.constructEvent(
        req.body,
        sig!,
        connectWebhookSecret  // Different secret from platform webhook!
      );
    } catch (err) {
      return res.status(400).send(`Webhook Error: ${err.message}`);
    }

    // Get the connected account ID
    const connectedAccountId = event.account;

    switch (event.type) {
      case 'checkout.session.completed':
        // CRITICAL: This is where Direct Charge sessions complete!
        await handleConnectCheckoutComplete(event.data.object, connectedAccountId);
        break;

      case 'checkout.session.expired':
        await handleConnectCheckoutExpired(event.data.object, connectedAccountId);
        break;

      case 'account.updated':
        await handleAccountUpdated(event.data.object);
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

async function handleConnectCheckoutComplete(session, connectedAccountId: string) {
  // Retrieve full session with line items
  const fullSession = await stripe.checkout.sessions.retrieve(
    session.id,
    { expand: ['line_items'] },
    { stripeAccount: connectedAccountId }  // CRITICAL: Specify account!
  );

  // Confirm payment in your system
  await confirmPayment(fullSession.id);
}
```

**Stripe控制台设置步骤：**
1. 登录Stripe控制台 → 开发者 → Webhooks
2. 为Connect添加端点：`https://yourdomain.com/webhooks/stripe/connect`
3. 选择“连接的账户”（Connected Accounts），而非“账户”（Account）
4. 添加事件监听：`checkout.session_completed`、`checkout.session.expired`、`account.updated`、`payout.paid`、`payout.failed`

---

## 预实施检查清单

### Webhook设置
- [ ] 平台端点能够正确处理平台相关事件
- [ ] 如果使用直接收费，Connect端点能够处理`checkout.session_completed`事件
- [ ] Stripe控制台的Connect Webhook设置正确
- [ ] 两个端点的Webhook密钥均已配置（密钥不同！）

### 支付验证
- [ ] Webhook处理函数已实现（主要依赖异步处理，确保可靠性）
- [ ] 前端验证功能已实现（辅助功能，提供即时用户体验）
- [ ] 两者都使用条件更新机制来保证操作的原子性
- [ ] 通过`amount_total === 0`来检测是否为100%折扣（而非依赖`no_payment_required`状态）
- **Web与原生浏览器处理差异**：根据`result.type`判断（Web为`'opened'`，原生为`'dismiss'/'cancel'`），切勿在Web环境中立即验证支付状态！

### 库存/预订资源管理
- [ ] 仅在支付确认后修改库存
- [ ] 确保操作原子性，防止重复计数
- [ ] 如果预订资源不可用，需妥善处理退款流程

### 测试
- [ ] 使用常规支付场景进行测试
- [ ] 使用100%折扣代码进行测试
- [ ] 测试用户在支付过程中关闭浏览器的情况
- [ ] 测试网络故障对支付验证的影响
- [ ] 确保Webhook能接收到来自连接账户的事件（如适用）

## 最佳实践

1. **始终使用Webhook**：不要仅依赖客户端验证
2. **确保操作的原子性**：正确处理Webhook事件
3. **错误处理**：优雅地处理所有Stripe相关的错误
4. **测试模式**：在生产环境前使用测试密钥进行全面测试
5. **元数据管理**：使用元数据将Stripe数据与数据库关联
6. **监控**：跟踪支付成功率和错误情况
7. **PCI合规**：切勿在服务器端处理原始卡信息
8. **支持SCA**：为欧洲地区的支付实现3D安全认证

## 常见问题

- **未验证Webhook**：务必验证Webhook签名
- **遗漏Webhook事件**：确保处理所有相关的Webhook事件
- **硬编码金额**：使用分或最小货币单位进行支付金额处理
- **缺乏重试机制**：为API调用实现重试逻辑
- **忽略测试模式**：使用测试卡片测试所有边缘情况