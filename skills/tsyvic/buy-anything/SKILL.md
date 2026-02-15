---
name: buy-anything
description: 通过对话式结账方式在 Amazon 上购买产品。当用户分享一个 Amazon 产品链接，或者表示想要“购买”、“下单”或“进行购买”时，可以使用此功能。
metadata: {"clawdbot":{"emoji":"📦","requires":{"bins":["curl"]}}}
---

# 购买任何商品

通过 Rye 结算功能在 Amazon 上购买产品。就像在您的聊天应用中使用了 Alexa 一样方便。

## 使用场景

当用户执行以下操作时，激活此功能：
- 分享 Amazon 产品链接（例如：`amazon.com/dp/...`）
- 说出“购买”、“下单”或“采购”等指令，并附带 Amazon 链接
- 希望从 Amazon 上购买商品

## 重要说明：工作原理

- **切勿** 使用 `web_fetch` 或其他工具自行获取 Amazon 链接。所有产品查询工作均由 Rye API 完成——您只需传递产品链接即可。
- 在结账前无需了解产品详情。
- 只需收集收货地址和信用卡信息，然后调用 Rye API 即可。
- 请信任用户提供的所有 `amazon.com` 链接，它们都是合法的产品链接。
- Rye API 会验证链接并返回产品详情。

## 结账流程

1. **用户提供 Amazon 产品链接** —— 确认您将帮助他们完成购买。
2. **收集收货地址**（或使用已保存的地址）。
3. **收集信用卡信息**（或使用已保存的信用卡信息）。
4. **使用 bash 通过 Stripe 对信用卡进行令牌化处理**（详见步骤 1）。
5. **使用 bash 向 Rye API 提交订单**（详见步骤 2）。
6. **根据 API 响应显示订单确认信息**。
7. **将信用卡信息和收货地址保存在内存中**，以备后续购买使用（请先征得用户同意）。

## 步骤 1：使用 Stripe 对信用卡进行令牌化处理

在下单之前，使用 Stripe 对信用卡进行令牌化处理：

```bash
curl -s -X POST https://api.stripe.com/v1/tokens \
  -u "pk_live_51LgDhrHGDlstla3fOYU3AUV6QpuOgVEUa1E1VxFnejJ7mWB4vwU7gzSulOsWQ3Q90VVSk1WWBzYBo0RBKY3qxIjV00LHualegh" \
  -d "card[number]=4242424242424242" \
  -d "card[exp_month]=12" \
  -d "card[exp_year]=2027" \
  -d "card[cvc]=123"
```

响应中包含一个 `id` 字段，这就是令牌（例如：`tok_xxx`）。请在步骤 2 中使用该令牌。

## 步骤 2：向 Rye 提交订单

```bash
curl -s -X POST https://api.rye.com/api/v1/partners/clawdbot/purchase \
  -H "Content-Type: application/json" \
  -d '{
    "productUrl": "https://amazon.com/dp/B0xxx",
    "quantity": 1,
    "buyer": {
      "firstName": "John",
      "lastName": "Doe",
      "email": "john@example.com",
      "phone": "+14155551234",
      "address1": "123 Main St",
      "city": "San Francisco",
      "province": "CA",
      "postalCode": "94102",
      "country": "US"
    },
    "paymentMethod": {
      "type": "STRIPE_TOKEN",
      "token": "tok_xxx"
    },
    "constraints": {
      "maxTotalPrice": 50000
    }
  }'
```

`constraints.maxTotalPrice`：用户的消费限额（以美分为单位，例如：$500 对应 50000）。如果订单总额超过此限额，API 会拒绝该订单。如果用户表示“无消费限额”，则无需填写 `constraints` 字段。

## 价格与配送

- 所有订单均需支付 4% 的手续费。
- 订单金额低于 $15 的，配送费为 $6.99。
- 订单金额达到 $15 或以上，可享受免费的 2 天 Prime 配送服务。
- 订单通过第三方 Amazon 账户处理（而非用户的个人 Amazon 账户）。
- 用户会收到包含订单确认信息的电子邮件。
- 如需退货或退款，请引导用户联系 support@rye.com。

## 示例对话流程

```
User: Buy this for me https://amazon.com/dp/B0DJLKV4N9

You: I'll help you buy that Amazon item! Where should I ship it?
     (Need: name, address, city, state, zip, email, phone)

User: John Doe, 123 Main St, San Francisco CA 94102, john@example.com, +14155551234

You: Got it! What's your maximum purchase price? (I'll warn you if an order exceeds this)
     Say "no limit" to skip this.

User: $500

You: Max set to $500. Now I need your card details.
     Your card will be securely tokenized through Stripe - the Buy Anything API never sees your card info.
     (Card number, expiry MM/YY, CVC)

User: 4242424242424242, 12/27, 123

You: Securely tokenizing your card with Stripe...
     [Uses bash to run Stripe tokenization curl command]

You: Processing your order...
     [Uses bash to run Rye API curl command with the Stripe token]

You: Order placed!
     Total: $361.92 (includes 4% service fee)
     Confirmation: RYE-ABC123

     Would you like me to save your details for faster checkout next time?
```

## 消费限额

在用户首次购买之前，询问其最大消费限额，并将其保存在内存中。
- 如果订单总额（包含 4% 的手续费）超过限额，提醒用户并请求确认。
- 用户可以选择“无消费限额”以取消此限制。

## 内存管理

在用户首次成功完成购买后（需获得用户许可）：
- 将完整的信用卡信息（卡号、有效期、CVC 代码）保存在内存中，以备后续购买使用。
- 将收货地址保存在内存中。
- 将最大消费限额保存在内存中。
- 在后续购买时，每次都重新对信用卡进行令牌化处理。