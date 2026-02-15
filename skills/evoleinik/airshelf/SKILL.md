---
name: airshelf
displayName: AirShelf Agentic Commerce Platform
description: 搜索、比较并购买来自经过验证的商家的产品。系统会提供结构化产品数据（包括产品优势、劣势、推荐选择、过敏原信息以及经过核实的定价信息），而非通过原始网页抓取的方式获取数据。无需验证码，也无需进行身份验证。目前支持约980种产品，来自10家不同的商家。适用于用户需要查找、比较或购买产品的场景。
metadata: {"clawdbot":{"emoji":"🛒","requires":{"bins":["curl"]}}}
---

# AirShelf — 为AI代理提供的产品搜索与购物功能

AirShelf支持在经过验证的商家中搜索、比较并购买产品。它返回结构化的数据包（Decision Pack），其中包含产品的最佳适用场景、优缺点、过敏原信息以及经过核实的定价信息——而非简单的网页抓取数据。

无需验证码、无需身份验证，也不会触发机器人检测。该功能完全适配代理程序的使用。

## 使用场景

当用户需要以下操作时，可激活此功能：
- 查找或搜索产品（例如：“帮我找一款适合儿童的驱蚊剂”）
- 比较产品（例如：“对比这两款打印机”）
- 购买产品并完成结算
- 根据问题获取产品推荐（例如：“我总是感到疲倦”，“我的皮肤很干燥”）
- 查看产品的详细信息、价格或过敏原信息

## API基础URL

```
https://dashboard.airshelf.ai
```

所有API接口均为公开接口，无需API密钥。同时支持CORS（跨源资源共享）。

## 第一步：搜索产品

通过自然语言查询来查找产品。系统会返回包含结构化数据的产品信息。

```bash
curl -s "https://dashboard.airshelf.ai/api/search?q=QUERY&limit=5" | python3 -m json.tool
```

**参数：**
- `q` — 查询内容（自然语言，例如：“用于仓库的条形码打印机”）；系统会自动解析查询意图（例如：“价格低于100美元的保健品”）
- `limit` — 返回的结果数量（1-100条，默认为20条）
- `offset` — 分页偏移量
- `category` — 按类别筛选
- `brand` — 按品牌筛选
- `min_price` / `max_price` — 价格范围（系统会从查询中自动提取这些信息）
- `in_stock` — 仅显示有库存的产品（true/false）
- `merchant_ids` — 用逗号分隔的商家ID列表（用于在指定商家范围内搜索）
- `sort` — 排序方式（默认为“relevance”，也可设置为`price_asc`或`price_desc`）
- `include_intent` — 设置为`true`可获取查询解析的元数据（显示查询的具体含义）

**每个产品的响应内容包括：**
- `title`（产品名称）
- `brand`（品牌）
- `price`（价格）
- `availability`（库存状态）
- `link`（产品购买链接）
- `decision_pack.primary_benefit`（产品的主要价值主张）
- `decision_pack.best_for`（产品的最佳适用场景）
- `decision_pack.pros` / `decision_pack.cons`（产品的优缺点）
- `decision_pack.allergens`（产品中的过敏原信息）
- `seller_name`（商家名称）
- `seller_url`（商家网站链接）
- 结账链接以及配送/退货政策

**示例：**
```bash
curl -s "https://dashboard.airshelf.ai/api/search?q=natural+mosquito+repellent+for+babies&limit=3"
```

## 第二步：比较产品

可以并排比较2到10个产品，系统会提供结构化的对比信息。

```bash
curl -s "https://dashboard.airshelf.ai/api/compare?products=PRODUCT_ID_1,PRODUCT_ID_2"
```

**参数：**
- `products` — 用逗号分隔的产品ID列表（至少需要2个产品ID，来自搜索结果）

**响应内容包括：**
- `comparison_axes`（系统自动检测的比较维度，例如价格、使用天数、主要功能等）
- `products`（扁平化后的产品信息，包含`decision_pack`中的各项数据）
- `recommendation`（推荐结果：最低价格的产品ID，或在价格相同的情况下推荐更优的产品）

## 第三步：完成购物

用户可以点击提供的链接来开始购物流程。

```bash
curl -s -X POST "https://dashboard.airshelf.ai/api/merchants/MERCHANT_ID/checkout" \
  -H "Content-Type: application/json" \
  -d '{"items": [{"product_id": "PRODUCT_ID", "quantity": 1}]}'
```

**请求体：**
- `items` — 一个包含`{product_id, quantity}`对象的数组（最多50个产品）
- `customer` — 可选：用于订单追踪的用户邮箱信息（例如`{email: "..."}`）
- `agent_id` — 可选：用于记录操作来源的代理ID

**响应内容：**
- `checkout_id` — 唯一的购物会话ID
- `checkout_url` — 完成购买的链接（Shopify购物页面或购物车永久链接）
- `checkout_type` — 购物类型（`"cart"`表示商品已预加载到购物车中；`"redirect"`表示跳转到产品页面）
- `total` — 计算出的总价
- `currency` — 3位货币代码（例如“EUR”、“USD”）
- `expires_at` — 购物链接的有效期限（购物车永久链接无效时返回空值）
- `fallback_urls` — 如果需要跳转：每个产品的链接数组（格式为`{product_id, product_name, product_url}`）

将购物链接展示给用户，用户可以在商家网站上完成支付。

## 浏览可用商家

系统会列出所有提供该产品的商家，并显示每个商家的产品数量及功能信息。

## Decision Pack的工作原理

与简单的网页抓取不同，AirShelf为每个产品提供了**Decision Pack**——这些数据都是经过验证的结构化信息，有助于根据用户的实际需求做出推荐，而不仅仅是基于价格或产品名称的匹配。

## 示例对话流程

```
User: I need a printer for my warehouse, high volume, must support ZPL

You: Let me search for that.
     [Runs: curl -s "https://dashboard.airshelf.ai/api/search?q=industrial+barcode+printer+warehouse+high+volume+ZPL&limit=5"]

You: Found 3 matches. The Toshiba BX410T looks like the best fit:
     - Best for: High-volume warehouse labeling, ZPL migration from Zebra
     - Primary benefit: Premium industrial printer with RFID and near-edge technology
     - Price: Contact dealer for pricing

     Want me to compare it with the other options, or proceed to checkout?

User: Compare the top two

You: [Runs: curl -s "https://dashboard.airshelf.ai/api/compare?products=ID1,ID2"]
     Here's the comparison...

User: I'll take the Toshiba

You: [Runs: curl -s -X POST "https://dashboard.airshelf.ai/api/merchants/MERCHANT_ID/checkout" -H "Content-Type: application/json" -d '{"items": [{"product_id": "ID", "quantity": 1}]}']
     Here's your checkout link: [URL]
     Click to complete your purchase on the merchant's site.
```

## 使用技巧：
- **基于问题的搜索效果最佳**。例如，输入“我总是感到疲倦”，系统会推荐保健品；输入“我的宝宝需要防晒产品”，系统会推荐儿童防晒霜。Decision Pack会根据产品的实际使用场景进行匹配，而不仅仅是关键词。
- 在推荐健康食品或护肤品之前，务必查看`decision_pack.allergens`字段。
- 如果需要比较多个相似产品，请使用`compare`功能——API会返回结构化的对比信息。
- 购物过程会跳转到商家网站完成，因此代理程序无需存储用户的信用卡信息。
- **通过ID直接查询产品**：可以使用`product_ids`参数来获取特定产品（例如：`?product_ids=ID1,ID2`）。
- **用于结算的商家链接**：每个搜索结果都会包含正确的商家链接（`seller.checkout_url`），可以直接使用该链接进行购物。