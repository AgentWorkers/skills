---
name: PayPal
slug: paypal
version: 1.0.0
description: 将 PayPal 支付功能与适当的 Webhook 验证、OAuth 处理以及安全验证集成到结账流程和订阅服务中。
metadata: {"clawdbot":{"emoji":"💳","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 使用场景

用户需要集成 PayPal 的 REST API 来处理支付、订阅或退款操作。代理负责处理结账流程、Webhook 验证、OAuth 令牌管理以及争议处理工作流程。

## 快速参考

| 主题 | 文件名 |
|-------|------|
| 代码模式 | `patterns.md` |
| Webhook 事件 | `webhooks.md` |

## 核心规则

### 1. 环境 URL 不同
- 沙盒环境：`api.sandbox.paypal.com`
- 生产环境：`api.paypal.com`
- 在生成代码之前，请先确认使用的是哪个环境。
- 凭据是特定于环境的——切勿混用。

### 2. OAuth 令牌管理
```javascript
// Token expires ~8 hours — handle refresh
const getToken = async () => {
  const res = await fetch('https://api.paypal.com/v1/oauth2/token', {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${Buffer.from(`${clientId}:${secret}`).toString('base64')}`,
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: 'grant_type=client_credentials'
  });
  return res.json(); // { access_token, expires_in }
};
```
切勿将 OAuth 令牌硬编码在代码中。必须实现令牌的刷新逻辑。

### 3. Webhook 验证是强制性的
PayPal 的 Webhook 必须通过 API 调用进行验证——不能使用简单的 HMAC 签名方式：
```javascript
// POST /v1/notifications/verify-webhook-signature
const verification = await fetch('https://api.paypal.com/v1/notifications/verify-webhook-signature', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
  body: JSON.stringify({
    auth_algo: headers['paypal-auth-algo'],
    cert_url: headers['paypal-cert-url'],
    transmission_id: headers['paypal-transmission-id'],
    transmission_sig: headers['paypal-transmission-sig'],
    transmission_time: headers['paypal-transmission-time'],
    webhook_id: WEBHOOK_ID,
    webhook_event: body
  })
});
// verification_status === 'SUCCESS'
```

### 4. 使用 `CAPTURE` 还是 `AUTHORIZE` —— 需要先确认用户意图
| 意图 | 行为 |
|--------|----------|
| `CAPTURE` | 在用户批准后立即扣款 |
| `AUTHORIZE` | 预先冻结资金，稍后扣款（最长延迟 29 天） |

在集成完成后更改意图会导致整个流程失败。

### 5. 服务器端验证——切勿信任客户端提供的信息
```javascript
// After client approves, VERIFY on server before fulfillment
const order = await fetch(`https://api.paypal.com/v2/checkout/orders/${orderId}`, {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());

// Validate ALL of these:
if (order.status !== 'APPROVED') throw new Error('Not approved');
if (order.purchase_units[0].amount.value !== expectedAmount) throw new Error('Amount mismatch');
if (order.purchase_units[0].amount.currency_code !== expectedCurrency) throw new Error('Currency mismatch');
if (order.purchase_units[0].payee.merchant_id !== YOUR_MERCHANT_ID) throw new Error('Wrong merchant');
```

### 6. Webhook 的幂等性
PayPal 可能会多次发送相同的 Webhook 请求：
```javascript
const processed = await db.webhooks.findOne({ eventId: body.id });
if (processed) return res.status(200).send('Already processed');
await db.webhooks.insert({ eventId: body.id, processedAt: new Date() });
// Now process the event
```

### 7. 货币的小数规则
某些货币没有小数位：
| 货币 | 小数位数 | 例子 |
|----------|----------|---------|
| USD, EUR | 2 | “10.50” |
| JPY, TWD | 0 | “1050”（而不是 “1050.00”） |

如果为 JPY 发送 “10.50” 这样的金额，会导致 API 错误。

## 常见错误

- **IPN 与 Webhook 的区别** —— IPN 是旧有的通信方式。新集成应使用 Webhook，切勿混用。
- **订单状态** —— 订单状态包括：CREATED → APPROVED → COMPLETED（或 VOIDED）。需要处理所有状态，而不仅仅是成功的路径。
- **小数位问题** —— PayPal 使用字符串表示金额（例如 “10.50”），而不是浮点数。某些货币不允许使用小数位。
- **沙盒环境的限制** —— 沙盒环境的 API 调用频率限制通常低于生产环境。不要假设生产环境的限制也会相同。
- **退款与支付** —— 退款相关的 API 是独立的。不要将资金发送（Payout）与接收订单（Payment）混淆。