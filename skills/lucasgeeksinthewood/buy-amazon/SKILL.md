---
name: Buy Amazon
description: "需要在亚马逊上购买商品吗？只需在 Amazon.com 上搜索和购物——比较价格和评分，将商品添加到购物车中，然后下订单，商品会寄送到美国境内的任何地址。这是一个专为人工智能（AI）代理设计的简单电子商务购物 API。"
homepage: https://buystuff.ai
emoji: 📦
user-invocable: true
tags:
  - shopping
  - buy
  - amazon
  - amazon.com
  - purchase
  - gift
  - order
  - delivery
  - ecommerce
  - online-shopping
  - product-search
env:
  - name: BUYSTUFF_AGENT_ID
    required: false
    description: "Optional identifier for your agent, used to track orders. If omitted, orders are anonymous."
data_sent:
  - field: shipping address
    destination: https://buystuff.ai
    purpose: "Required to fulfill the Amazon order. Stored only for order processing."
  - field: email address
    destination: https://buystuff.ai
    purpose: "Receives a payment link that the user must manually approve and pay. No automatic charges. Not shared beyond buystuff.ai and Amazon fulfillment."
  - field: agentId
    destination: https://buystuff.ai
    purpose: "Optional agent identifier for order tracking. Not shared beyond buystuff.ai."
permissions:
  - network: https://buystuff.ai
    reason: "All API calls go to buystuff.ai, which uses the Rainforest API (an authorized Amazon product data provider) for search and product details. buystuff.ai handles cart, checkout, and payment link delivery. No direct Amazon credentials are used or needed."
---
## 何时使用此技能

当用户有以下需求时，激活此技能：
- **购买商品**：例如“给我买副耳机”、“订购一份生日礼物”、“我需要一个新的键盘”；
- **在亚马逊上购物**：例如“在亚马逊上帮我找些东西”、“有什么好的笔记本电脑支架吗？”；
- **比较产品**：例如“50美元以下最好的无线耳机是哪些？”；
- **发送礼物**：例如“为我妈妈订购一份礼物”、“在30美元以下买些不错的东西”；
- **重新订购或追踪订单**：例如“我的订单在哪里？”、“查询订单AC-047”的情况。

如果用户提到购买、订购、购物、送礼或进行交易等相关操作，那么就可以使用此技能。

## 工作原理（简述）

1. 在亚马逊上搜索商品；
2. 将商品添加到购物车；
3. 输入收货地址和电子邮件地址完成结算；
4. 用户会收到一封包含支付链接的电子邮件；
5. 用户自行付款，我们负责发货。此API不会收取任何费用。

所有API请求都发送到 **https://buystuff.ai**，无需任何设置或API密钥。产品数据通过 [Rainforest API](https://www.rainforestapi.com/) 获取，该API是亚马逊授权的数据提供商。

## 会话管理

每个API响应中都包含 `X-Session-ID` 头部和 `sessionId` 字段。请在后续的所有请求中将该会话ID作为 `X-Session-ID` 头部字段发送。这样可以帮助：
- 将多个商品添加到同一个购物车；
- 在不记住购物车ID的情况下查看当前购物车内容；
- 确保整个购物流程的连贯性。

**注意**：如果没有发送会话ID，每次请求都会自动生成一个新的会话ID。每个会话一次只能关联一个购物车。在请求支付链接后，下一次发送 `POST /cart` 请求会创建一个新的购物车。

## 支付方式

**此API不会收集任何支付信息**，也不涉及信用卡、代币或钱包等支付方式。

当用户准备好付款时，系统会向用户发送一个安全的支付链接。用户需要在 buystuff.ai 网站上完成付款，我们负责从亚马逊购买商品并送货上门。**此技能本身不会处理任何支付流程**。

- **服务费用**：总金额的10%（包含运费）；
- **支付方式**：用户会收到一封包含支付链接的电子邮件；
- **配送**：付款完成后，我们会在24-48小时内从亚马逊购买商品并发货；
- **退款**：请联系 support@buystuff.ai。

在请求支付链接之前，务必向用户展示完整的费用明细。

## 数据处理

所有API请求都发送到 `https://buystuff.ai`，产品数据通过 [Rainforest API](https://www.rainforestapi.com/) 获取，该API是亚马逊授权的数据提供商。仅会将配送信息分享给亚马逊用于订单处理，不会向第三方出售或共享任何数据。

| 数据类型 | 获取时机 | 用途 |
|---------|---------|--------|
| 搜索查询 | 第1步 | 用于查找产品（不包含个人身份信息） |
| 收货地址 | 第4步 | 用于配送订单 |
| 电子邮件 | 第4步 | 用于发送支付链接和更新信息 |
| 代理ID（可选） | 第4步 | 用于追踪代理的订单状态 |

## 安全性：此API不会收取费用

**此技能仅用于生成支付链接，不会直接收取费用或完成购买。**用户必须自行打开邮件、查看订单信息并在 buystuff.ai 上完成付款。**在请求支付链接之前，必须获得用户的明确同意。**务必向用户展示费用明细，并等待用户的确认。即使代理未经请求直接调用相关接口，最坏的情况也只是用户收到一封可以忽略的支付链接邮件——不会产生任何费用，也不会完成任何购买。

---

## 第1步：搜索产品

`/buy-amazon-search`

**参数说明：**
| 参数 | 类型 | 是否必填 | 说明 |
|------|------|---------|-------------|
| `q` | 字符串 | 是 | 搜索关键词 |
| `sort_by` | 字符串 | 否 | 排序方式（`price_low_to_high`、`price_high_to_low`、`average_review`、`most_recent`） |
| `number_of_results` | 整数 | 否 | 限制结果数量（默认20条） |
| `exclude_sponsored` | 布尔值 | 否 | 是否排除广告商品 |
| `page` | 整数 | 否 | 结果页码 |

响应中包含 `results[]` 数组，其中包含产品的 `asin`、`title`、`price`、`rating`、`ratingsTotal`、`isPrime`、`isBestseller`、`isDeal` 等信息。

**代理使用建议：**
- 显示3-5个搜索结果供用户比较，不要直接选择第一个；
- 提及产品的评分和评价数量，用户通常会信任这些信息；
- 突出显示免运费的商品（Prime会员专享）和特价商品；
- 如果没有找到结果，建议用户扩大搜索范围或更换关键词；
- 如果用户有预算，可以使用 `sort_by=price_low_to_high` 并告知用户符合预算的商品。

## 第2步：查看产品详情

`/buy-amazon-details`

**响应内容：** 包含产品的完整信息，如 `title`、`brand`、`price`、`buyboxWinner`（运费、库存情况）、`rating`、`ratingBreakdown`、`specifications`、`variants` 等。

**代理使用建议：**
- 检查 `buyboxWinner.availability`，如果显示“缺货”，请告知用户并提供替代选项；
- 如果 `buyboxWinner.shipping.raw` 为“FREE”，请特别强调这一点，用户通常很看重免运费；
- 显示 `ratingBreakdown` 的百分比，让用户判断评分的真实性（注意避免大量1星评价）；
- 如果产品有不同版本（颜色、尺寸等），请询问用户具体需求后再添加到购物车；
- 提及用户关心的产品规格。

## 第3步：添加到购物车

`/buy-amazon-cart`

**参数说明：**
| 参数 | 类型 | 是否必填 | 说明 |
|------|------|---------|-------------|
| `asin` | 字符串 | 是 | 亚马逊产品ID |
| `quantity` | 整数 | 否 | 默认值：1 |

请保存响应中的 `cartId`，用于后续的结算操作。

**多件商品购物车**：使用相同的会话再次调用 `POST /cart` 将更多商品添加到同一个购物车。如果重复输入相同的 `asin`，系统会合并数量。

**查看当前购物车内容**（无需 `cartId`）：

**修改商品数量：** [具体代码]

**删除商品：** [具体代码]

**如果添加商品失败**：可能是产品ID无效或商品已售罄。请返回搜索页面，帮助用户选择其他商品。

## 第4步：结算**

`/buy-amazon-checkout`

**参数说明：**
| 参数 | 类型 | 是否必填 | 说明 |
|------|------|---------|-------------|
| `shipping.name` | 字符串 | 是 | 收货人全名 |
| `shipping.line1` | 字符串 | 是 | 街道地址 |
| `shipping.line2` | 字符串 | 否 | 公寓号、套间号 |
| `shipping.city` | 字符串 | 是 | 城市名称 |
| `shipping.state` | 字符串 | 是 | 2位州代码 |
| `shipping.zip` | 字符串 | 是 | 邮政编码 |
| `shipping.country` | 字符串 | 否 | 默认值：“US” |
| `email` | 字符串 | 是 | 用于发送支付链接和订单更新 |
| `agentId` | 字符串 | 否 | 代理ID |

响应中包含 `summary`，其中包含 `subtotal`（小计）、`shipping`（运费）、`serviceFee`（服务费用）和 `total`（总价）。

**代理使用建议：**
- 如果用户尚未提供收货地址，可以自然地询问：“应该寄送到哪里？”；
- 如果没有提供电子邮件地址，可以询问：“我们应该将支付链接发送到哪个邮箱？”；
- 在请求支付链接之前，务必向用户展示完整的费用明细：
  - 小计、运费（Prime会员通常免运费）、服务费用（10%）、**总价**；
- 如果用户对价格感到惊讶，提醒他们服务费用为10%，并建议他们选择其他商品。

## 第5步：请求支付链接

**仅在用户同意后调用此接口。**此接口不会收取费用或完成购买，只会发送支付链接邮件。

**响应内容：** 包含 `orderId`（订单ID）、`status`（状态）、`total`（总价）和确认信息。用户会收到一封包含支付链接的电子邮件。

**告知用户：**“请查看您的电子邮件中的支付链接——付款完成后，我们将在24-48小时内发货！”

## 第6步：追踪订单

`/buy-amazon-status`

**订单状态**：`PENDING_FULFILLMENT` → `PROCESSING` → `SHIPPED` → `DELIVERED`

当订单状态变为 `SHIPPED` 时，系统会提供 `trackingNumber`（追踪号码），请将其告知用户。

---

## 示例：购买耳机

[示例代码]

## 示例：购买生日礼物

[示例代码]

## 示例：多件商品订单

[示例代码]

## 常见问题处理：
- **用户没有预算**：正常搜索并展示价格范围。如果搜索结果差异较大，可以询问用户：“您有特定的价格范围吗？”
- **商品缺货**：告知用户“该商品目前缺货”，并推荐相似的商品；
- **用户想比较两个产品**：获取两个产品的详细信息并快速对比价格、评分和关键规格；
- **用户结账后改变主意**：用户可以选择不支付链接。未付款的订单将会过期；
- **用户询问退款事宜**：引导用户联系 support@buystuff.ai；
- **搜索结果过多**：使用 `sort_by`、`exclude_sponsored` 或更具体的搜索条件来缩小范围。

## 快速参考

[快速参考代码]