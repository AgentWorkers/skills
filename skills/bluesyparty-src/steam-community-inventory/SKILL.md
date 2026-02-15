---
name: steamcommunity
description: 从 steamcommunity.com 获取用户的 Steam 购物清单数据
homepage: https://steamcommunity.com/dev
metadata: {"clawdbot":{"emoji":"\u2694","requires":{"bins":["jq","curl"],"env":["STEAM_ID","STEAM_COOKIES"]}}}
---


# Steam社区库存技能

从 `steamcommunity.com` 获取并浏览Steam用户的库存信息。

## 准备工作

1. **获取您的Steam ID (SteamID64)**：
   - 访问您的Steam个人资料页面。
   - 如果您的URL是 `https://steamcommunity.com/profiles/76561198012345678`，那么您的Steam ID就是 `76561198012345678`。
   - 如果您的URL使用了一个自定义名称（如 `https://steamcommunity.com/id/myname`），请访问 [steamid.io](https://steamid.io) 并粘贴您的个人资料URL以获取Steam ID。

2. **获取Steam会话cookie**（在获取自己的库存信息时需要绕过速率限制）：
   - 在浏览器中登录 [steamcommunity.com](https://steamcommunity.com)。
   - 打开开发者工具（F12）> “应用程序”选项卡 > “Cookies” > `https://steamcommunity.com`。
   - 复制 `steamLoginSecure` cookie的值。

3. 设置环境变量：
   ```bash
   export STEAM_ID="your-steamid64"
   export STEAM_COOKIES="steamLoginSecure=your-cookie-value"
   ```

## 使用方法

所有命令都使用 `curl` 来调用Steam社区的库存接口。对于所有标准游戏的库存，上下文ID（Context ID）为 `2`。

### 常见游戏的应用ID

| 游戏 | 应用ID（App ID） |
|------|--------|
| CS2 / CS:GO | 730 |
| Team Fortress 2 | 440 |
| Dota 2 | 570 |
| Rust | 252490 |
| PUBG | 578080 |
| Steam社区（交易卡片等） | 753 |

### 获取游戏的库存信息

将 `$APP_ID` 替换为相应的游戏应用ID（参见上表）。对于所有标准游戏的库存，上下文ID为 `2`。

```bash
curl -s "https://steamcommunity.com/inventory/$STEAM_ID/$APP_ID/2?l=english&count=2000" \
  -H "Cookie: $STEAM_COOKIES" | jq '.'
```

### 获取CS2游戏的库存信息

```bash
curl -s "https://steamcommunity.com/inventory/$STEAM_ID/730/2?l=english&count=2000" \
  -H "Cookie: $STEAM_COOKIES" | jq '.'
```

### 获取物品详情（包括名称和数量）

```bash
curl -s "https://steamcommunity.com/inventory/$STEAM_ID/730/2?l=english&count=2000" \
  -H "Cookie: $STEAM_COOKIES" | jq '[.descriptions[] | {market_hash_name, type}]'
```

### 获取物品详细信息（将资产ID映射到对应的描述）

```bash
curl -s "https://steamcommunity.com/inventory/$STEAM_ID/730/2?l=english&count=2000" \
  -H "Cookie: $STEAM_COOKIES" | jq '{assets: [.assets[] | {assetid, classid, instanceid, amount}], total: .total_inventory_count}'
```

### 分页获取（当库存物品超过2000件时）

当库存物品数量超过2000件时，API会返回一个 `last_assetid` 字段。您可以使用这个值作为 `start_assetid` 来获取下一页的数据：

```bash
curl -s "https://steamcommunity.com/inventory/$STEAM_ID/730/2?l=english&count=2000&start_assetid=$LAST_ASSET_ID" \
  -H "Cookie: $STEAM_COOKIES" | jq '.'
```

通过检查响应中的 `more_items` 字段来判断是否还有更多页面（如果值为 `1`，则表示还有更多页面）。

## 响应格式

库存接口返回的JSON数据包含以下字段：

| 字段 | 说明 |
|-------|-------------|
| `assets` | 物品数组，包含 `appid`、`contextid`、`assetid`、`classid`、`instanceid`、`amount` 等信息 |
| `descriptions` | 物品元数据数组，包括 `market_hash_name`、`name`、`type`、`icon_url`、`tradable`、`marketable`、`tags` 等信息 |
| `total_inventory_count` | 库存中的物品总数 |
| `more_items` | 如果还有更多页面，则值为 `1`（否则为 `null`） |
| `last_assetid` | 返回的最后一个物品的ID；用作获取下一页的 `start_assetid` |
| `success` | 如果请求成功，则值为 `1` |

物品通过 `classid` 和 `instanceid` 与对应的描述信息关联。

## 注意事项

- **速率限制**：Steam社区的接口受到严格的IP地址速率限制。使用自己的cookie可以绕过这一限制。如果没有cookie，多次请求后可能会导致IP被封禁（冷却时间约为6小时）。
- **请求间隔**：如果同时获取多个用户的库存或页面数据，请在每次请求之间至少等待4秒。
- **`count` 参数**：最大值为5000，但建议设置为2000以避免问题。
- **上下文ID**：对于所有标准游戏的库存，使用 `2`；Steam社区中的物品（应用ID为753）在某些物品类型下会使用上下文ID `6`。
- **私人资料**：库存信息必须设置为公开状态，或者您需要以物品所有者的身份进行身份验证。