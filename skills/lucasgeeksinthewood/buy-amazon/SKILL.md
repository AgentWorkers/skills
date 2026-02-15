---
name: Buy Amazon
description: "需要在亚马逊上购买商品吗？只需搜索产品，比较价格和评分，然后下订单，商品就会寄送到美国境内的任何地址。"
homepage: https://buystuff.ai
emoji: 📦
user-invocable: true
tags:
  - shopping
  - buy
  - amazon
  - purchase
  - gift
  - order
  - delivery
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
    purpose: "Used to send payment link and order updates. Not shared with third parties."
  - field: agentId
    destination: https://buystuff.ai
    purpose: "Optional agent identifier for order tracking. Not shared with third parties."
permissions:
  - network: https://buystuff.ai
    reason: "All API calls go to buystuff.ai which proxies Amazon product data and manages orders."
---

## 何时使用此技能

当用户有以下需求时，激活此技能：
- **购买商品**：例如“给我买副耳机”、“订购一份生日礼物”、“我需要一个新键盘”；
- **在亚马逊上购物**：例如“在亚马逊上帮我找些东西”、“哪个笔记本电脑支架好？”；
- **比较产品**：例如“50美元以下最好的无线耳机是哪些？”；
- **赠送礼物**：例如“为我妈妈订购一份礼物”、“在30美元以内买些不错的东西”；
- **重新订购或查询订单状态**：例如“我的订单在哪里？”、“查询订单AC-047的进度”。

只要用户提到购买、订购、购物、赠送或购买相关的内容，就可以使用此技能。

## 工作原理（简述）

1. 在亚马逊上搜索商品；
2. 将商品添加到购物车；
3. 输入收货地址和电子邮件地址进行结账；
4. 确认订单；
5. 用户会收到包含支付链接的电子邮件，用户付款后，我们会完成发货。

所有API请求都发送到 **https://buystuff.ai**，无需任何设置或API密钥。

## 会话管理

每个API响应都会包含一个 `X-Session-ID` 标头以及JSON正文中的 `sessionId` 字段。请保存这个会话ID，并在后续的所有请求中将其作为 `X-Session-ID` 标头发送。这样您可以：
- 将多个商品添加到同一个购物车中；
- 在不记住购物车ID的情况下查看当前购物车的内容；
- 保持整个购物流程的连贯性。

**注意**：如果不发送会话ID，每次请求都会自动生成一个新的会话ID。每个会话一次只能关联一个购物车；确认订单后，下次发送 `POST /cart` 会创建一个新的购物车。

## 支付方式

**此API不收集任何支付信息**，也不涉及信用卡、代币或钱包等支付方式。

订单确认后，buystuff.ai会向用户发送一个简单的支付链接。用户通过该链接在buystuff.ai网站上安全完成付款，后续的购买和发货流程由我们处理：
- **服务费用**：总金额的10%（包含运费）；
- **支付方式**：用户会收到包含支付链接的电子邮件；
- **配送**：付款完成后，我们会在24-48小时内从亚马逊购买商品并发货；
- **退款**：请联系 support@buystuff.ai。

在确认订单前，务必向用户展示完整的费用明细。

## 数据处理

所有数据仅传输到 **https://buystuff.ai**，不会泄露给任何第三方。

| 数据类型 | 收集时间 | 用途 |
|---------|---------|--------|
| 搜索查询 | 第1步 | 用于查找商品（不包含个人身份信息） |
| 收货地址 | 第4步 | 用于配送订单 |
| 电子邮件 | 第4步 | 用于发送支付链接和订单更新信息 |
| 代理ID（可选） | 第4步 | 用于追踪代理的订单状态 |

## 用户确认要求

在确认订单之前，**必须获得用户的明确同意**。请向用户展示费用明细，并等待他们的确认。禁止自动完成购买操作。即使用户已确认，也不会通过此API直接扣款——用户需通过电子邮件链接自行完成支付。

---

## 第1步：搜索商品

`/buy-amazon-search`

**请求参数：**
| 参数类型 | 是否必填 | 说明 |
|---------|--------|---------|
| `q`     | 字符串 | 搜索关键词 |
| `sort_by` | 字符串 | 可选 | `price_low_to_high`（价格从低到高）、`price_high_to_low`（价格从高到低）、`average_review`（平均评分）、`most_recent`（最新商品） |
| `number_of_results` | 整数 | 可选 | 限制显示结果数量（默认20条） |
| `exclude_sponsored` | 布尔值 | 可选 | 是否排除广告商品 |
| `page`    | 整数 | 可选 | 显示结果页码 |

响应内容包含 `results[]`，其中包含 `asin`（商品ID）、`title`（商品标题）、`price`（价格）、`rating`（评分）、`ratingsTotal`（总评分）、`isPrime`（是否为Prime会员商品）、`isBestseller`（是否为畅销商品）等字段。

**代理提示：**
- 显示3-5个搜索结果，以便用户进行比较，不要直接选择第一个结果；
- 提及产品的评分和评论数量，因为用户通常会信任这些信息；
- 突出显示Prime会员商品（享受免费配送）和特价商品；
- 如果没有找到结果，建议用户调整搜索关键词或尝试其他搜索词；
- 如果用户有预算范围，可以使用 `sort_by=price_low_to_high` 并告知用户符合预算的商品。

## 第2步：查看商品详情

`/buy-amazon-details`

响应内容包含商品的详细信息：`title`（商品标题）、`brand`（品牌）、`price`（价格）、`buyboxWinner`（是否为Prime会员商品、是否可配送、库存情况）、`rating`（评分）、`ratingBreakdown`（评分分布）、`specifications`（产品规格）等。

**代理提示：**
- 检查 `buyboxWinner.availability`，如果显示“缺货”，请告知用户并提供替代建议；
- 如果 `buyboxWinner.shipping.raw` 为“FREE”，请特别强调这一点，因为用户通常看重免费配送；
- 展示 `ratingBreakdown` 的百分比，让用户了解评分的真实性（注意避免大量1星评价）；
- 如果商品有多种款式或颜色，请在添加到购物车前询问用户的具体需求；
- 提及用户关心的关键产品规格。

## 第3步：将商品添加到购物车

`/buy-amazon-cart`

**请求参数：**
| 参数类型 | 是否必填 | 说明 |
|---------|--------|---------|
| `asin`     | 字符串 | 是 | 商品ID |
| `quantity` | 整数 | 可选 | 默认值：1 |

请保存响应中的 `cartId`，因为结账时需要使用它。

**多件商品购物车**：可以使用相同的会话再次调用 `POST /cart` 将更多商品添加到同一个购物车中。如果输入相同的 `asin`，系统会自动合并数量。

**查看当前购物车内容**（无需提供 `cartId`）：

## 更新商品数量：

## 删除商品：

## 如果添加商品失败**：可能是商品ID无效或商品已售罄。请引导用户重新搜索并选择其他商品。

## 第4步：结账

`/buy-amazon-checkout`

**请求参数：**
| 参数类型 | 是否必填 | 说明 |
|---------|--------|---------|
| `shipping.name` | 字符串 | 是 | 收货人全名 |
| `shipping.line1` | 字符串 | 是 | 街道地址 |
| `shipping.line2` | 字符串 | 可选 | 公寓号、套房号或单元号 |
| `shipping.city` | 字符串 | 是 | 城市名称 |
| `shipping.state` | 字符串 | 是 | 两位数的州代码 |
| `shipping.zip` | 字符串 | 是 | 邮政编码 |
| `shipping.country` | 字符串 | 可选 | 默认值：“US” |
| `email` | 字符串 | 是 | 用于发送支付链接和订单更新信息 |
| `agentId` | 字符串 | 可选 | 代理ID |

响应内容包含 `summary`，其中包含 `subtotal`（小计）、`shipping`（运费）、`serviceFee`（服务费用）和 `total`（总金额）。

**代理提示：**
- 如果用户未提供收货地址，可以自然地询问：“应该将商品寄送到哪里？”；
- 如果用户未提供电子邮件地址，可以询问：“我们应该将支付链接发送到哪个邮箱？”；
- 在确认订单前，务必向用户展示完整的费用明细：
  - 小计、运费（Prime会员通常免费）、服务费用（10%）、**总金额**；
- 如果用户对价格感到惊讶，提醒他们服务费用为10%，并建议他们重新选择商品。

## 第5步：确认订单

**仅在用户表示同意后调用此接口。**

响应内容包含 `orderId`（订单ID）、`status`（订单状态）和 `total`（总金额）。

请告知用户：“请查看您的电子邮件，支付链接已发送。付款后，我们将在24-48小时内发货！”

## 第6步：查询订单状态

`/buy-amazon-status`

**订单状态**：`PENDING_FULFILLMENT` → `PROCESSING` → `SHIPPED` → `DELIVERED`

当订单状态变为 `SHIPPED` 时，系统会提供 `trackingNumber`（跟踪号码），请将此号码告知用户。

---

## 示例：
- **购买耳机**：
- **购买生日礼物**：
- **多件商品订单**：

## 常见问题处理：
- **用户未提供预算范围**：正常搜索并展示价格范围。如果搜索结果差异较大，可以询问用户：“您有特定的价格范围吗？”
- **商品缺货**：告知用户该商品当前无法购买，并从搜索结果中推荐类似商品；
- **用户想在购买后更改选择**：用户可以取消支付，未支付的订单会自动失效；
- **用户询问退款事宜**：引导用户联系 support@buystuff.ai；
- **搜索结果过多**：使用 `sort_by`、`exclude_sponsored` 或更具体的搜索条件来缩小搜索范围。

## 快速参考：