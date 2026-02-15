---
name: food402
description: 在土耳其领先的食品配送服务 TGO Yemek（Trendyol GO）上订购食物。用户可以通过该平台在土耳其订购外卖、浏览餐厅、搜索菜品、管理配送地址、查看订单历史记录，以及使用 3D Secure 支付方式进行结账。
metadata: {"openclaw": {"emoji": "🍕", "requires": {"bins": ["curl", "jq", "openssl"], "env": ["TGO_EMAIL", "TGO_PASSWORD", "GOOGLE_PLACES_API_KEY"]}, "primaryEnv": "TGO_EMAIL"}}
---

# Food402 - TGO 餐饮外卖服务

从土耳其领先的外卖服务 Trendyol GO (TGO Yemek) 下单。此技能支持完整的餐饮订购流程：浏览餐厅、查看菜单、自定义菜品、管理购物车，并使用 3D Secure 支付方式完成结算。

## 设置

### OpenClaw

将以下内容添加到您的 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "skills": {
    "entries": {
      "food402": {
        "enabled": true,
        "env": {
          "TGO_EMAIL": "your-tgo-email@example.com",
          "TGO_PASSWORD": "your-tgo-password",
          "GOOGLE_PLACES_API_KEY": "your-google-api-key"
        }
      }
    }
  }
}
```

### Claude Code / Cursor / Codex / Gemini CLI

在您的 shell 配置文件（`~/.bashrc`、`~/.zshrc` 等）中设置环境变量：

```bash
export TGO_EMAIL="your-tgo-email@example.com"
export TGO_PASSWORD="your-tgo-password"
export GOOGLE_PLACES_API_KEY="your-google-api-key"  # Optional: for Google Reviews
```

然后重新加载 shell 或运行 `source ~/.zshrc`（或相应的命令）。

## 认证

该技能会自动处理认证过程。在进行 API 调用时：

1. 运行 `{baseDir}/scripts/auth.sh get-token` 以获取有效的 JWT 令牌。
2. 该脚本会将令牌缓存到 `/tmp/food402-token` 文件中，并自动刷新（令牌在 60 秒后过期）。
3. 如果任何 API 调用返回 401 错误，请使用 `{baseDir}/scripts/auth.sh clear-token` 清除令牌并重试。

**手动认证检查：**
```bash
{baseDir}/scripts/auth.sh check-token
```

## 必需的工作流程

**重要提示：** 您必须按照以下顺序操作：

1. **select_address** - 必须首先执行此步骤（设置购物车的配送地址）。
2. **get_restaurants** 或 **search_restaurants** - 浏览/搜索餐厅。
3. **get_restaurant_menu** - 查看餐厅菜单。
4. **get_product_details** - 检查菜品定制选项（如需要）。
5. **add_to_basket** - 将菜品添加到购物车。
6. **checkout_ready** - 确认购物车已准备好支付。
7. **place_order** - 使用 3D Secure 完成订单。

如果 `add_to_basket` 失败，请先尝试 `clear_basket`，然后再重试。

---

## 地址管理操作

### get_addresses

获取用户保存的配送地址。首先调用此函数以显示可用的地址。

```bash
TOKEN=$({baseDir}/scripts/auth.sh get-token)
curl -s "https://api.tgoapis.com/web-user-apimemberaddress-santral/addresses" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-correlationid: $(uuidgen)" \
  -H "pid: $(uuidgen)" \
  -H "sid: $(uuidgen)" | jq
```

**响应字段：** `id`, `addressName`, `addressLine`, `neighborhoodName`, `districtName`, `cityName`, `latitude`, `longitude`

### select_address

**在浏览餐厅或添加菜品到购物车之前必须执行此操作。** 设置购物车的配送地址。

**参数：**
- `addressId`（必需）：从 get_addresses 获取的地址 ID

```bash
TOKEN=$({baseDir}/scripts/auth.sh get-token)
curl -s -X POST "https://api.tgoapis.com/web-checkout-apicheckout-santral/shipping" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "x-correlationid: $(uuidgen)" \
  -H "pid: $(uuidgen)" \
  -H "sid: $(uuidgen)" \
  -d '{"shippingAddressId": {addressId}, "invoiceAddressId": {addressId}}'
```

### add_address

添加新的配送地址。首先使用 get_cities → get_districts → get_neighborhoods 查找位置 ID。

**参数：**
- `name`（必需）：名字
- `surname`（必需）：姓氏
- `phone`（必需）：不带国家代码的电话号码（例如："5356437070")
- `addressName`（必需）：地址标签（例如：“家”、“工作”）
- `addressLine`（必需）：街道地址
- `cityId`（必需）：从 get_cities 获取
- `districtId`（必需）：从 get_districts 获取
- `neighborhoodId`（必需）：从 get_neighborhoods 获取
- `latitude`（必需）：坐标字符串
- `longitude`（必需）：坐标字符串
- `apartmentNumber`, `floor`, `doorNumber`, `addressDescription`（可选）
- `elevatorAvailable`（可选）：布尔值

```bash
TOKEN=$({baseDir}/scripts/auth.sh get-token)
curl -s -X POST "https://api.tgoapis.com/web-user-apimemberaddress-santral/addresses" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "x-correlationid: $(uuidgen)" \
  -H "pid: $(uuidgen)" \
  -H "sid: $(uuidgen)" \
  -d '{
    "name": "{name}",
    "surname": "{surname}",
    "phone": "{phone}",
    "addressName": "{addressName}",
    "addressLine": "{addressLine}",
    "cityId": {cityId},
    "districtId": {districtId},
    "neighborhoodId": {neighborhoodId},
    "latitude": "{latitude}",
    "longitude": "{longitude}",
    "countryCode": "TR",
    "elevatorAvailable": false
  }' | jq
```

**注意：** 如果响应代码为 429，表示需要 OTP 验证。请引导用户直接在 tgoyemek.com 上添加地址。

### get_cities

获取所有城市列表以供用户选择地址。

```bash
TOKEN=$({baseDir}/scripts/auth.sh get-token)
curl -s "https://api.tgoapis.com/web-user-apimemberaddress-santral/cities" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-correlationid: $(uuidgen)" \
  -H "pid: $(uuidgen)" \
  -H "sid: $(uuidgen)" | jq '.cities[] | {id, name}'
```

### get_districts

获取某个城市的所有区域。

**参数：**
- `cityId`（必需）：从 get_cities 获取的城市 ID

```bash
TOKEN=$({baseDir}/scripts/auth.sh get-token)
curl -s "https://api.tgoapis.com/web-user-apimemberaddress-santral/cities/{cityId}/districts" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-correlationid: $(uuidgen)" \
  -H "pid: $(uuidgen)" \
  -H "sid: $(uuidgen)" | jq '.districts[] | {id, name}'
```

### get_neighborhoods

获取某个区域的所有社区。

**参数：**
- `districtId`（必需）：从 get_districts 获取的区域 ID

---

## 餐厅查找操作

### get_restaurants

列出选定地址附近的餐厅。**必须先执行 select_address 操作。**

**参数：**
- `latitude`（必需）：来自选定地址的坐标
- `longitude`（必需）：来自选定地址的坐标
- `page`（可选）：页码，默认为 1
- `sortBy`（可选）：`RECOMMENDED`（默认）、`RESTAURANT_SCORE` 或 `RESTAURANT_DISTANCE`
- `minBasketPrice`（可选）：传递 400 以过滤订单金额大于或等于 400 土耳其里拉的餐厅

**排序关键字（土耳其语和英语）：**
- "önerilen" / "recommended" / "推荐" → `RECOMMENDED`
- "en yakın" / "closest" / "最近的" → `RESTAURANT_DISTANCE`
- "en iyi" / "best rated" / "评分最高的" → `RESTAURANT_SCORE`
- "en ucuz" / "最便宜的" → 请使用 `search_restaurants`（返回产品价格）

```bash
TOKEN=$({baseDir}/scripts/auth.sh get-token)
curl -s "https://api.tgoapis.com/web-discovery-apidiscovery-santral/restaurants/filters?openRestaurants=true&latitude={latitude}&longitude={longitude}&pageSize=50&page={page}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-correlationid: $(uuidgen)" \
  -H "pid: $(uuidgen)" \
  -H "sid: $(uuidgen)" | jq
```

添加 `&sortType=RESTAURANT_SCORE` 或 `&sortType=RESTAURANT_DISTANCE` 以进行排序（推荐排序时省略此参数）。

**响应字段：** `id`, `name`, `kitchen`, `rating`, `ratingText`, `minBasketPrice`, `averageDeliveryInterval`, `distance`, `neighborhoodName`, `isClosed`, `campaignText`

### search_restaurants

通过关键字搜索餐厅和产品。搜索结果包含产品价格（对“最便宜”的查询很有用）。

**重要提示：** 始终检查 `isClosed` 字段。切勿推荐已关闭的餐厅。

**参数：**
- `searchQuery`（必需）：搜索关键字（例如：“pizza”, “burger”, “dürüm”）
- `latitude`（必需）：来自选定地址的坐标
- `longitude`（必需）：来自选定地址的坐标
- `page`（可选）：页码，默认为 1

**响应包含：** 餐厅信息以及包含 `id`, `name`, `description`, `price` 的 `products[]` 数组

---

## 菜单与产品操作

### get_restaurant_menu

获取餐厅的完整菜单及其分类和菜品。

**参数：**
- `restaurantId`（必需）：餐厅 ID
- `latitude`（必需）：坐标
- `longitude`（必需）：坐标

**响应结构：**
- `info`：餐厅详情（id, name, rating, workingHours, deliveryTime, minOrderPrice）
- `categories[]`：菜单分类以及其中的 `items[]`（id, name, description, price, likePercentage）

### get_product_details

获取产品的定制选项（需要排除的食材、额外选项/尺寸的修改组）。

**参数：**
- `restaurantId`（必需）：餐厅 ID
- `productId`（必需）：菜单中的产品 ID
- `latitude`（必需）：坐标
- `longitude`（必需）：坐标

**响应包含 `components[]`：**
- `type`：`INGREDIENTS`（需要排除的食材）或 `MODIFIER_GROUP`（可选的额外选项/尺寸）
- `modifierGroupId`：在将修改项添加到购物车时使用此 ID
- `options[]`：可选选项，包含 `id`, `name`, `price`, `isPopular`
- `isSingleChoice`, `minSelections`, `maxSelections`：选择规则

### get_product_recommendations

获取与所选菜品“搭配得很好的”其他产品的推荐。

**参数：**
- `restaurantId`（必需）：餐厅 ID
- `productIds`（必需）：产品 ID 数组

---

## 购物车管理操作

### add_to_basket

将菜品添加到购物车。**必须先执行 select_address 操作。**

**参数：**
- `storeId`（必需）：餐厅 ID（数字类型）
- `latitude`（必需）：坐标（数字类型，不是字符串）
- `longitude`（必需）：坐标（数字类型，不是字符串）
- `items[]`（必需）：要添加的菜品数组

**菜品结构：**
```json
{
  "productId": 12345,
  "quantity": 1,
  "modifierProducts": [
    {
      "productId": 111,
      "modifierGroupId": 222,
      "modifierProducts": [],
      "ingredientOptions": {"excludes": [], "includes": []}
    }
  ],
  "ingredientOptions": {
    "excludes": [{"id": 333}],
    "includes": []
  }
}
```

**如果此操作失败，请先尝试 `clear_basket`，然后再重试。**

### get_basket

获取当前购物车的内容。

**响应包含：** `storeGroups[]`（包含餐厅信息和产品）、`summary[]`、`totalPrice`、`deliveryPrice`、`isEmpty`

### remove_from_basket

从购物车中删除一个菜品。

**参数：**
- `itemId`（必需）：来自 get_basket 响应的菜品 UUID（使用 `itemId` 字段，而非 `productId`）

```bash
TOKEN=$({baseDir}/scripts/auth.sh get-token)
curl -s -X DELETE "https://api.tgoapis.com/web-checkout-apicheckout-santral/carts/items/{itemId}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-correlationid: $(uuidgen)" \
  -H "pid: $(uuidgen)" \
  -H "sid: $(uuidgen)" | jq
```

### clear_basket

清空整个购物车。

```bash
TOKEN=$({baseDir}/scripts/auth.sh get-token)
curl -s -X DELETE "https://api.tgoapis.com/web-checkout-apicheckout-santral/carts" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-correlationid: $(uuidgen)" \
  -H "pid: $(uuidgen)" \
  -H "sid: $(uuidgen)"
```

## 结算与支付操作

### get_saved_cards

获取用户保存的支付卡信息（已屏蔽敏感信息）。如果没有支付卡，用户需要在 tgoyemek.com 上添加一张。

**使用带有不同头的 Payment API：**

```bash
TOKEN=$({baseDir}/scripts/auth.sh get-token)
curl -s "https://payment.tgoapps.com/v2/cards/" \
  -H "Authorization: bearer $TOKEN" \
  -H "app-name: TrendyolGo" \
  -H "x-applicationid: 1" \
  -H "x-channelid: 4" \
  -H "x-storefrontid: 1" | jq
```

**响应：** `cards[]`，包含 `cardId`, `maskedCardNumber`, `bankName`, `cardNetwork`, `isDebitCard`

### checkout_ready

确认购物车已准备好结算。在 place_order 之前调用此函数。

**检查响应：**
- 如果 `totalProductCount` 为 0，表示购物车为空。
- 检查 `warnings[]` 以查看是否有问题（例如，订单金额低于最低要求）。
- 返回购物车的完整详情和 `totalPrice`。

### set_order_note

设置订单备注和服务偏好。在 place_order 之前调用此函数。

**参数：**
- `note`（可选）：给快递员/餐厅的备注
- `noServiceWare`（可选）：不提供塑料餐具（默认值：false）
- `contactlessDelivery`（可选）：不按门铃（默认值：false）
- `dontRingBell`（可选）：不按门铃（默认值：false）

### place_order

使用 3D Secure 支付方式完成订单。这是一个三步过程。

**参数：**
- `cardId`（必需）：从 get_saved_cards 获取的卡片 ID

**步骤 1：获取包含支付信息的购物车数据**
```bash
TOKEN=$({baseDir}/scripts/auth.sh get-token)
curl -s "https://api.tgoapis.com/web-checkout-apicheckout-santral/carts?cartContext=payment&limitPromoMbs=false" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-correlationid: $(uuidgen)" \
  -H "pid: $(uuidgen)" \
  -H "sid: $(uuidgen)"
```

**步骤 2：选择支付方式（使用 Payment API）**
```bash
# Get bin code from card's maskedCardNumber (first 6 digits + **)
BINCODE="${maskedCardNumber:0:6}**"

curl -s -X POST "https://payment.tgoapps.com/v3/payment/options" \
  -H "Authorization: bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "app-name: TrendyolGo" \
  -H "x-applicationid: 1" \
  -H "x-channelid: 4" \
  -H "x-storefrontid: 1" \
  -d '{
    "paymentType": "payWithCard",
    "data": {
      "savedCardId": {cardId},
      "binCode": "{binCode}",
      "installmentId": 0,
      "reward": null,
      "installmentPostponingSelected": false
    }
  }'
```

**步骤 3：提交支付（使用 Payment API）**
```bash
curl -s -X POST "https://payment.tgoapps.com/v2/payment/pay" \
  -H "Authorization: bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "app-name: TrendyolGo" \
  -H "x-applicationid: 1" \
  -H "x-channelid: 4" \
  -H "x-storefrontid: 1" \
  -d '{
    "customerSelectedThreeD": false,
    "paymentOptions": [{"name": "payWithCard", "cardNo": "", "customerSelectedThreeD": false}],
    "callbackUrl": "https://tgoyemek.com/odeme"
  }'
```

**3D Secure 处理：** 如果响应包含 `json.content`（HTML）或 `redirectUrl`：
1. 将 HTML 保存到临时文件中。
2. 在浏览器中打开：`{baseDir}/scripts/3dsecure.sh "$HTML_content"`。
3. 告知用户在浏览器中完成验证。

---

## 订单历史操作

### get_orders

获取用户的订单历史记录及其状态。

**参数：**
- `page`（可选）：页码，默认为 1

**响应：** `orders[]`，包含 `id`, `orderDate`, `store`, `status`, `price`, `products`

### get_order_detail

获取特定订单的详细信息，包括配送状态。

**参数：**
- `orderId`（必需）：来自 get_orders 的订单 ID

**响应包含：** 订单详情、配送状态、预计到达时间、产品信息及价格

---

## Google 评论（可选）

### get_google_reviews

获取餐厅的 Google 地图评分和评论。**需要设置 GOOGLE_PLACES_API_KEY 环境变量。**

**参数：**
- `restaurantId`, `restaurantName`, `neighborhoodName`, `tgoDistance`, `tgoRating`, `latitude`, `longitude`

此操作使用 Google Places API 来查找餐厅并比较评分。仅在配置了 GOOGLE_PLACES_API_KEY 时使用。

---

## 错误处理

| 状态 | 操作 |
|--------|--------|
| **401 Unauthorized** | 令牌过期。运行 `{baseDir}/scripts/auth.sh clear-token`，然后重试操作。 |
| **400 Bad Request** | 检查参数。解析并显示响应正文中的错误信息。 |
| **429 Rate Limited** | 需要 OTP 验证。请引导用户直接在 tgoyemek.com 上完成操作。 |
| **5xx 服务器错误** | TGO 服务暂时不可用。稍后重试。 |
| **3D Secure** | 保存 HTML 内容，使用 `{baseDir}/scripts/3dsecure.sh` 在浏览器中打开，并告知用户完成验证。 |

**始终解析错误响应，并向用户清晰地显示错误信息。**

---

## 指南

- **在进行 API 调用之前** 必须进行认证。使用 auth.sh 辅助工具。
- **切勿** 向用户暴露原始凭据、JWT 或令牌。
- **在执行破坏性操作**（如 clear_basket、place_order）之前，请先获得用户的确认。
- **在推荐餐厅之前**，务必检查 `isClosed` 字段。
- **以清晰、易读的格式** 展示结果，而不是原始的 JSON 数据。
- **遵循所需的工作流程**：select_address → browse → menu → add_to_basket → checkout。
- **正确处理坐标**：get_restaurants 使用字符串坐标，add_to_basket 使用数字坐标。
- **如果 add_to_basket 失败**，请先尝试 clear_basket，然后再重试。
- **进行支付时**，始终使用 Payment API 的正确头部信息（小写形式，如 "bearer", app-name, x-applicationid 等）。