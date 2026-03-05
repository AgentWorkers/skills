---
name: buy-anything
description: 通过对话式结账功能从 Amazon 和 Shopify 商店购买产品。当用户分享产品链接或说出“购买”、“下单”或“采购”等指令时，可以使用该功能。
metadata: {"clawdbot":{"emoji":"📦","requires":{"bins":["curl"]}}}
---
# 购买任何商品

您可以通过 Rye 结算功能从 Amazon 和 Shopify 商店购买商品，就像在聊天应用中拥有一个私人购物助手一样。

## 适用场景

当用户出现以下情况时，激活此功能：
- 分享 Amazon 产品链接（例如：`amazon.com/dp/...`）
- 分享 Shopify 商店产品链接（任何以 `.myshopify.com` 结尾的链接或自定义域名的 Shopify 商店）
- 提到“购买”、“下单”或“采购”并附有产品链接
- 希望从在线商店购买商品

## 重要说明：工作原理

- **切勿** 使用 `web_fetch` 或其他工具自行获取产品链接。Rye API 负责处理所有产品信息查询——您只需传递产品链接即可。
- 在结账前无需了解产品详情。
- 只需收集收货地址并设置支付卡信息，然后调用 API 即可。
- Rye API 会验证链接的有效性；如果链接无效或不受支持，API 会返回错误信息。

## 结账流程

1. **用户提供产品链接**——确认您将帮助他们完成购买。
2. **收集收货地址**（或使用用户记忆中保存的地址）。
3. **通过 BasisTheory 设置支付卡信息**（或使用用户记忆中保存的 BT 令牌）。
4. **使用 bash 命令向 Rye API 提交订单**（详见步骤 2）。
5. **根据 API 响应显示订单确认信息**。
6. **将 BT 令牌和收货地址保存在用户记忆中**，以备后续购买使用（请先征得用户同意）。

## 步骤 1：通过 BasisTheory 安全地获取用户支付卡信息

如果用户记忆中不存在 BT 令牌，请通过浏览器安全地获取他们的支付卡信息：

```bash
open "https://mcp.rye.com/bt-card-capture" 2>/dev/null || xdg-open "https://mcp.rye.com/bt-card-capture" 2>/dev/null
```

如果命令执行失败（例如因为平台不支持），请提供以下可点击的链接：`https://mcp.rye.com/bt-card-capture`
告知用户：“我已在您的浏览器中打开了一个安全的支付卡信息输入页面。请在此处输入您的卡信息并点击‘提交’。您的卡信息不会被存储在此聊天记录中，而是直接传输到 BasisTheory 的 PCI 合规存储系统中。提交后，请复制页面上显示的令牌并粘贴到这里。”

等待用户粘贴令牌（通常是一个 UUID 格式的字符串，例如 `d1ff0c32-...`）。

**如果用户记忆中已有 BT 令牌，请跳过此步骤**，直接使用该令牌。

**如果购买过程中出现与 CVC/CVV 相关的错误（例如“信息缺失”或支付会话问题”），可能是保存的令牌已过期（BasisTheory 会在 24 小时后清除 CVC 信息）。请打开以下链接刷新 CVC 信息：**
```bash
open "https://mcp.rye.com/bt-cvc-refresh?token_id=SAVED_TOKEN_ID" 2>/dev/null || xdg-open "https://mcp.rye.com/bt-cvc-refresh?token_id=SAVED_TOKEN_ID" 2>/dev/null
```

如果命令执行失败，请提供以下可点击的链接：
告知用户：“您保存的支付卡安全码已过期。我已打开一个页面让您重新输入 CVC 信息——无需重新输入完整的卡信息。操作完成后请关闭该页面，我会重新尝试购买。”

**使用相同的 BT 令牌再次尝试购买。**

## 步骤 2：向 Rye 提交订单**

合作伙伴的 API 端点通过特定的路径进行身份验证，无需添加 API 密钥头。仅接受发送到 `/partners/clawdbot/` 的请求。

```bash
curl -s -X POST https://api.rye.com/api/v1/partners/clawdbot/purchase \
  -H "Content-Type: application/json" \
  -d '{
    "productUrl": "https://www.example-store.com/products/cool-thing",
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
      "type": "basis_theory_token",
      "basisTheoryToken": "d1ff0c32-..."
    },
    "constraints": {
      "maxTotalPrice": 50000
    }
  }'
```

`constraints.maxTotalPrice`：用户的消费限额（以分为单位，例如 $500 对应 50000 分）。如果订单总金额超过此限额，API 会拒绝订单。如果用户表示“无消费限额”，请忽略 `constraints` 字段。

POST 请求的响应中包含一个 `id` 字段（例如 `ci_abc123`），请使用该 ID 来查询订单状态。

## 步骤 3：查询订单状态

提交订单后，使用 POST 请求中的 `id` 来查询订单最终状态：

```bash
curl -s https://api.rye.com/api/v1/partners/clawdbot/purchase/CHECKOUT_INTENT_ID
```

请将 `CHECKOUT_INTENT_ID` 替换为实际的订单 ID（例如 `ci_abc123`）。

每 5 秒查询一次订单状态，直到状态变为以下之一：
- `retrieving_offer`：正在获取产品详情和价格（继续查询）
- `placing_order`：订单正在提交给商店（继续查询）
- `completed`：订单成功提交（停止查询）
- `failed`：订单失败（停止查询）

当订单状态变为 `completed` 时，向用户显示：
- 产品名称（来自 `offer.product.title`）
- 总金额（来自 `offer.cost.total`，以美元显示，单位为分）
- 订单 ID（如果有的话）

如果订单失败，请向用户显示 `failureReason.message`。

## 价格与配送

API 会自动验证商店的定价信息。如果提交的链接不受支持，API 会返回错误信息——请告知用户仅支持 Amazon 和 Shopify 商店。

- **Shopify 商店**：采用商店的标价，我们不加价。
- **Amazon**：收取 3% 的手续费以覆盖交易成本。
- Amazon 订单金额低于 $15 时，运费为 $6.99。
- Amazon 订单金额达到 $15 或以上时，可享受免费的 2 天 Prime 配送服务。
- Amazon 订单通过用户的个人 Amazon 账户进行处理。
- 用户会收到包含订单确认信息的电子邮件。
- 如需退货或退款，请引导用户联系 support@rye.com。

## 示例对话流程

```
User: Buy this for me https://amazon.com/dp/B0DJLKV4N9

You: I'll help you buy that! Where should I ship it?
     (Need: name, address, city, state, zip, email, phone)

User: John Doe, 123 Main St, San Francisco CA 94102, john@example.com, +14155551234

You: Got it! What's your maximum purchase price? (I'll warn you if an order exceeds this)
     Say "no limit" to skip this.

User: $500

You: Max set to $500. I'm opening a secure card entry page in your browser now.
     Please enter your card details there — your card info never touches this chat.
     After submitting, copy the token shown on the page and paste it here.
     [Opens https://mcp.rye.com/bt-card-capture]

User: d1ff0c32-a1b2-4c3d-8e4f-567890abcdef

You: Got it! Submitting your order...
     [POST to purchase API with the BT token, gets back ci_abc123]

You: Order submitted! Waiting for confirmation...
     [Polls GET /purchase/ci_abc123 every 5 seconds]

You: Order confirmed!
     Product: Wireless Earbuds Pro
     Total: $358.44 (includes 3% service fee)
     Order ID: RYE-ABC123

     Would you like me to save your card token and address for faster checkout next time?
```

## 消费限额

在用户首次购买前，询问他们的最高消费限额。将此信息保存在用户设备的本地内存中。
- 如果订单总金额（包括所有费用）超过限额，请提醒用户并请求确认。
- 用户可以选择“无消费限额”以取消此限制。

## 内存管理

保存的数据仅存储在用户设备上的代理程序内存中，不会同步到云端或在不同设备间共享。

在用户完成首次成功购买后（需获得用户同意）：
- 将 BasisTheory 令牌 ID 保存在内存中，以备后续购买使用（注意：保存的是令牌 ID，而非卡信息；该令牌无法反推为卡号）。
- 将收货地址保存在内存中。
- 将最高消费限额保存在内存中。
- 在后续购买时，直接使用已保存的 BT 令牌，无需再次输入卡信息。
- 使用已保存的令牌下单前，请务必再次确认用户的意愿。
- 如果用户要求删除保存的令牌，请让他们告知您以便从内存中删除该令牌。如需从 BasisTheory 的存储系统中彻底撤销令牌，请引导他们联系 support@rye.com。