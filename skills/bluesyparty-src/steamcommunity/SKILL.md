---
name: steam-community-inventory
description: 检索 Steam 的库存数据，并管理 steamcommunity.com 上的交易报价。
homepage: https://steamcommunity.com/dev
metadata: {"clawdbot":{"emoji":"\u2694","requires":{"bins":["jq","curl"],"env":["STEAM_ID","STEAM_COOKIES","STEAM_API_KEY","STEAM_SESSION_ID"]}}}
---


# Steam社区库存技能

该技能允许您检索和浏览Steam用户的库存信息，并在steamcommunity.com网站上发送/管理交易请求。

## 设置

1. **获取您的Steam ID (SteamID64)**：
   - 访问您的Steam个人资料页面。
   - 如果您的URL是`https://steamcommunity.com/profiles/76561198012345678`，那么您的Steam ID就是`76561198012345678`。
   - 如果您的URL使用了一个昵称（如`https://steamcommunity.com/id/myname`），请访问[steamid.io](https://steamid.io)并将您的个人资料URL粘贴到这里以获取Steam ID。

2. **获取您的Steam Web API密钥**：
   - 访问[https://steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey)。
   - 注册一个域名（任何值都可以，例如`localhost`）。
   - 复制页面上显示的API密钥。

3. **获取Steam会话cookie**（用于交易请求和绕过库存请求速率限制）：
   - 在浏览器中登录[steamcommunity.com](https://steamcommunity.com)。
   - 打开开发者工具（F12）> 应用程序选项卡 > Cookies > `https://steamcommunity.com`。
   - 复制`steamLoginSecure` cookie的值。
   - 复制`sessionid` cookie的值。

4. **设置环境变量**：
   ```bash
   export STEAM_ID="your-steamid64"
   export STEAM_API_KEY="your-api-key"
   export STEAM_COOKIES="steamLoginSecure=your-cookie-value"
   export STEAM_SESSION_ID="your-sessionid-cookie-value"
   ```

## 使用方法

所有命令都使用`curl`来调用Steam社区的库存接口。对于所有标准游戏库存，上下文ID（Context ID）为`2`。

### 常见应用ID

| 游戏 | 应用ID |
|------|--------|
| CS2 / CS:GO | 730 |
| Team Fortress 2 | 440 |
| Dota 2 | 570 |
| Rust | 252490 |
| PUBG | 578080 |
| Steam社区（交易卡片等） | 753 |

### 获取游戏的库存信息

将`$APP_ID`替换为相应的游戏应用ID（参见上表）。对于所有标准游戏库存，上下文ID为`2`。

```bash
curl -s "https://steamcommunity.com/inventory/$STEAM_ID/$APP_ID/2?l=english&count=2000" \
  -H "Cookie: $STEAM_COOKIES" | jq '.'
```

### 获取CS2游戏的库存信息

```bash
curl -s "https://steamcommunity.com/inventory/$STEAM_ID/730/2?l=english&count=2000" \
  -H "Cookie: $STEAM_COOKIES" | jq '.'
```

### 获取物品列表（包括名称和数量）

```bash
curl -s "https://steamcommunity.com/inventory/$STEAM_ID/730/2?l=english&count=2000" \
  -H "Cookie: $STEAM_COOKIES" | jq '[.descriptions[] | {market_hash_name, type}]'
```

### 获取物品详情（将资产ID与描述关联）

```bash
curl -s "https://steamcommunity.com/inventory/$STEAM_ID/730/2?l=english&count=2000" \
  -H "Cookie: $STEAM_COOKIES" | jq '{assets: [.assets[] | {assetid, classid, instanceid, amount}], total: .total_inventory_count}'
```

### 分页获取（当库存物品超过2000件时）

当物品数量超过2000件时，API会返回一个`last_assetid`字段。您可以使用这个值作为`start_assetid`来获取下一页的数据：

```bash
curl -s "https://steamcommunity.com/inventory/$STEAM_ID/730/2?l=english&count=2000&start_assetid=$LAST_ASSET_ID" \
  -H "Cookie: $STEAM_COOKIES" | jq '.'
```

通过检查响应中的`more_items`字段来判断是否还有更多页面（如果值为`1`，则表示还有更多页面）。

## 响应格式

库存接口返回的JSON数据包含以下字段：

| 字段 | 描述 |
|-------|-------------|
| `assets` | 物品数组，包含`appid`、`contextid`、`assetid`、`classid`、`instanceid`、`amount`等信息 |
| `descriptions` | 物品元数据数组：`market_hash_name`、`name`、`type`、`icon_url`、`tradable`、`marketable`、`tags`等 |
| `total_inventory_count` | 库存中的物品总数 |
| `more_items` | 如果还有更多页面，则值为`1`；否则为`0` |
| `last_assetid` | 返回的最后一个物品的ID；用作下一页的`start_assetid` |
| `success` | 如果请求成功，则值为`1` |

物品与描述之间的关联通过`classid`和`instanceid`来确定。

## 注意事项

- **速率限制**：Steam社区接口对每个IP的请求有严格的速率限制。使用自己的cookie可以绕过这一限制。如果没有cookie，多次请求后可能会被IP封禁（冷却时间约为6小时）。
- **请求间隔**：如果同时获取多个库存或页面的数据，请在每次请求之间至少等待4秒。
- **`count`参数**：最大值为5000，但建议设置为2000以避免问题。
- **上下文ID**：对于所有标准游戏库存，使用`2`。Steam社区中的特殊物品（appid为753）某些类型的物品可能需要使用`context ID` `6`。
- **私人资料**：要查看库存信息，必须将资料设置为公开状态，或者您需要以所有者身份登录。

---

## 交易请求

进行交易请求需要已认证的会话（cookie）和Steam Web API密钥。`sessionid` cookie需要以cookie的形式以及POST请求体参数的形式发送。

### 交易伙伴的识别

可以通过两种方式识别交易伙伴：

1. **通过SteamID64** — 例如`76561198012345678`。将其转换为32位的账户ID，用于`partner`字段：从SteamID64中减去`76561197960265728`。
2. **通过交易URL** — 例如`https://steamcommunity.com/tradeoffer/new/?partner=52079950&token=YDAlR4bC`。`partner`字段中的值是32位的账户ID。如果交易伙伴不在您的好友列表中，则需要`token`参数。

### 发送交易请求

此操作会将您库存中的物品发送给其他用户（或请求他们库存中的物品）。每个物品都需要提供`appid`、`contextid`和`assetid`（这些信息可以从上述库存接口获取）。

`json_tradeoffer`参数是一个JSON字符串，用于描述双方交易的物品。`me`对象包含您要发送的物品；`them`对象包含您希望接收的物品。

```bash
# Set trade parameters
PARTNER_ACCOUNT_ID="52079950"  # 32-bit account ID (from trade URL or SteamID64 - 76561197960265728)
PARTNER_STEAM_ID="76561198012345678"  # Full SteamID64 (= 76561197960265728 + PARTNER_ACCOUNT_ID)
TRADE_TOKEN="YDAlR4bC"         # From partner's trade URL (omit if partner is on your friends list)
TRADE_MESSAGE="Here's the trade we discussed"

# Build the json_tradeoffer payload
# me.assets = items YOU are giving, them.assets = items you WANT from them
JSON_TRADEOFFER='{
  "newversion": true,
  "version": 4,
  "me": {
    "assets": [
      {"appid": 730, "contextid": "2", "amount": 1, "assetid": "YOUR_ASSET_ID"}
    ],
    "currency": [],
    "ready": false
  },
  "them": {
    "assets": [
      {"appid": 730, "contextid": "2", "amount": 1, "assetid": "THEIR_ASSET_ID"}
    ],
    "currency": [],
    "ready": false
  }
}'

# Send with trade token (non-friend)
curl -s "https://steamcommunity.com/tradeoffer/new/send" \
  -X POST \
  -H "Cookie: sessionid=$STEAM_SESSION_ID; $STEAM_COOKIES" \
  -H "Referer: https://steamcommunity.com/tradeoffer/new/?partner=$PARTNER_ACCOUNT_ID&token=$TRADE_TOKEN" \
  -H "Origin: https://steamcommunity.com" \
  -d "sessionid=$STEAM_SESSION_ID" \
  -d "serverid=1" \
  -d "partner=$PARTNER_STEAM_ID" \
  --data-urlencode "tradeoffermessage=$TRADE_MESSAGE" \
  --data-urlencode "json_tradeoffer=$JSON_TRADEOFFER" \
  -d "captcha=" \
  --data-urlencode "trade_offer_create_params={\"trade_offer_access_token\":\"$TRADE_TOKEN\"}" \
  | jq '.'
```

**向好友发送交易请求**（无需`token`）：在`Referer`参数中省略`token`，并将`trade_offer_create_params`设置为`{}`：

```bash
curl -s "https://steamcommunity.com/tradeoffer/new/send" \
  -X POST \
  -H "Cookie: sessionid=$STEAM_SESSION_ID; $STEAM_COOKIES" \
  -H "Referer: https://steamcommunity.com/tradeoffer/new/?partner=$PARTNER_ACCOUNT_ID" \
  -H "Origin: https://steamcommunity.com" \
  -d "sessionid=$STEAM_SESSION_ID" \
  -d "serverid=1" \
  -d "partner=$PARTNER_STEAM_ID" \
  --data-urlencode "tradeoffermessage=$TRADE_MESSAGE" \
  --data-urlencode "json_tradeoffer=$JSON_TRADEOFFER" \
  -d "captcha=" \
  -d "trade_offer_create_params={}" \
  | jq '.'
```

请求成功后，系统会返回一个`tradeofferid`：

```json
{"tradeofferid": "1234567890", "needs_mobile_confirmation": true, "needs_email_confirmation": false}
```

#### 发送礼物（不请求接收物品）

将`them.assets`设置为空数组`[]`：

```bash
JSON_TRADEOFFER='{
  "newversion": true,
  "version": 4,
  "me": {
    "assets": [
      {"appid": 730, "contextid": "2", "amount": 1, "assetid": "YOUR_ASSET_ID"}
    ],
    "currency": [],
    "ready": false
  },
  "them": {
    "assets": [],
    "currency": [],
    "ready": false
  }
}'
```

### 获取已发送和接收的交易请求

使用官方的Steam Web API和您的API密钥来获取这些信息。

```bash
# Get all active trade offers (sent and received)
curl -s "https://api.steampowered.com/IEconService/GetTradeOffers/v1/?key=$STEAM_API_KEY&get_sent_offers=1&get_received_offers=1&active_only=1&get_descriptions=1&language=english" \
  | jq '.'
```

```bash
# Get only received active offers
curl -s "https://api.steampowered.com/IEconService/GetTradeOffers/v1/?key=$STEAM_API_KEY&get_sent_offers=0&get_received_offers=1&active_only=1&get_descriptions=1&language=english" \
  | jq '.response.trade_offers_received'
```

```bash
# Get only sent active offers
curl -s "https://api.steampowered.com/IEconService/GetTradeOffers/v1/?key=$STEAM_API_KEY&get_sent_offers=1&get_received_offers=0&active_only=1&get_descriptions=1&language=english" \
  | jq '.response.trade_offers_sent'
```

### 获取特定的交易请求

```bash
curl -s "https://api.steampowered.com/IEconService/GetTradeOffer/v1/?key=$STEAM_API_KEY&tradeofferid=$TRADE_OFFER_ID&language=english&get_descriptions=1" \
  | jq '.response.offer'
```

### 获取交易请求的汇总信息

```bash
curl -s "https://api.steampowered.com/IEconService/GetTradeOffersSummary/v1/?key=$STEAM_API_KEY&time_last_visit=0" \
  | jq '.response'
```

### 接受交易请求

接受交易请求需要使用Steam社区的Web接口（而非Web API）。您需要`tradeofferid`和交易伙伴的SteamID64。

```bash
TRADE_OFFER_ID="1234567890"
PARTNER_STEAM_ID="76561198012345678"

curl -s "https://steamcommunity.com/tradeoffer/$TRADE_OFFER_ID/accept" \
  -X POST \
  -H "Cookie: sessionid=$STEAM_SESSION_ID; $STEAM_COOKIES" \
  -H "Referer: https://steamcommunity.com/tradeoffer/$TRADE_OFFER_ID/" \
  -d "sessionid=$STEAM_SESSION_ID" \
  -d "tradeofferid=$TRADE_OFFER_ID" \
  -d "serverid=1" \
  -d "partner=$PARTNER_STEAM_ID" \
  -d "captcha=" \
  | jq '.'
```

### 取消已发送的交易请求

```bash
curl -s "https://api.steampowered.com/IEconService/CancelTradeOffer/v1/" \
  -X POST \
  -d "key=$STEAM_API_KEY" \
  -d "tradeofferid=$TRADE_OFFER_ID"
```

### 拒绝接收的交易请求

```bash
curl -s "https://api.steampowered.com/IEconService/DeclineTradeOffer/v1/" \
  -X POST \
  -d "key=$STEAM_API_KEY" \
  -d "tradeofferid=$TRADE_OFFER_ID"
```

### 获取交易历史记录

```bash
curl -s "https://api.steampowered.com/IEconService/GetTradeHistory/v1/?key=$STEAM_API_KEY&max_trades=10&get_descriptions=1&language=english&include_failed=0" \
  | jq '.response.trades'
```

### 交易请求的状态参考

| 值 | 状态 | 描述 |
|-------|-------|-------------|
| 1 | 无效 | 无效或未知的状态 |
| 2 | 活动中 | 请求已发送，但双方尚未操作 |
| 3 | 已接受 | 物品已交换 |
| 4 | 被拒绝 | 接收方提出了反交易请求 |
| 5 | 过期 | 未在截止日期前被接受 |
| 6 | 被取消 | 发送方取消了请求 |
| 7 | 被拒绝 | 接收方拒绝了请求 |
| 8 | 物品不可用 | 交易请求中的物品不再可用 |
| 9 | 创建中（需要确认） | 需要通过手机/电子邮件确认后再发送 |
| 10 | 通过二次验证取消 | 通过手机/电子邮件确认取消 |
| 11 | 待处理中 | 交易暂时搁置；物品将从双方的库存中移除，随后自动交付 |

### 交易请求的相关说明

- **手机确认**：大多数交易请求需要Steam Mobile Authenticator的确认。如果需要确认，响应中会显示`needs_mobileconfirmation: true`。
- **交易暂缓**：如果账户未启用Steam Guard Mobile Authenticator超过7天，所有交易将被暂缓15天。
- **交易伙伴的库存**：要查看交易伙伴可交易的物品，请使用他们的SteamID64（而不是`$STEAM_ID`）来获取他们的库存信息。他们的库存必须设置为公开状态，或者您需要与他们成为好友。
- **`partner`字段**：发送请求时，`partner`参数中需要提供完整的SteamID64。交易URL中的`partner`查询参数是32位的账户ID。
- **Cookie过期**：`sessionid`和`steamLoginSecure` cookie会在您的Steam会话结束时失效。如果它们失效，请从浏览器中重新获取这些cookie。