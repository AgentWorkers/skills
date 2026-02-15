---
name: bitskins-api
description: >
  Interacts with the BitSkins REST API V2 and WebSocket API for CS2/Dota 2 skin trading.
  Supports account management, market search, buying, selling, listing, delisting, relisting,
  price updates, Steam inventory/deposits/trades, wallet operations, and real-time WebSocket
  subscriptions. Use when the user wants to search for skins, check prices, buy or sell items,
  manage their BitSkins account, check balances, or interact with the BitSkins marketplace.
metadata:
  author: custom
  version: "1.0"
  env_vars: "BITSKINS_API_KEY"
---

# BitSkins API 使用指南

## 认证

所有对 BitSkins API 的请求都需要通过 `x-apikey` 头部进行认证。

API 密钥必须设置在环境变量 `BITSKINS_API_KEY` 中。用户可以在启用 API 访问权限后，从 BitSkins 账户设置中获取自己的 API 密钥。

**重要提示：** 某些接口（如钱包提款、双因素认证操作）还需要 `twofa_code` 参数。在调用这些接口时，务必向用户索取他们的双因素认证代码，而不要将其存储在系统中。

## 基本 URL

```
https://api.bitskins.com
```

## 发送请求

使用辅助脚本来发送 API 请求：

```bash
bash bitskins-api/scripts/bitskins-api.sh <METHOD> <PATH> [JSON_BODY]
```

**示例：**

```bash
# GET request (no body)
bash bitskins-api/scripts/bitskins-api.sh GET /account/profile/me

# POST request with JSON body
bash bitskins-api/scripts/bitskins-api.sh POST /account/profile/balance

# POST with parameters
bash bitskins-api/scripts/bitskins-api.sh POST /market/search/730 '{"limit":10,"offset":0,"where":{}}'
```

## 请求限制

- **全局限制：** 每 10 秒内最多 50 次请求
- **市场搜索 (`/market/search/*`)：** 每秒 1 次请求
- 在服务器负载较重的情况下，这些限制可能会降低。

## 请求格式

- API 接受 JSON 格式的数据
- **GET 请求：** 不需要请求体
- **POST 请求：** 需要包含所需参数的 JSON 请求体

## 响应格式

所有响应均为 JSON 格式。成功响应会直接返回数据；错误响应会包含错误代码，具体信息请参阅 [references/api-endpoints.md](references/api-endpoints.md)。

## API 分类

API 分为以下几类，请参阅 [references/api-endpoints.md](references/api-endpoints.md) 以获取完整的接口列表：

### 账户
- **个人资料：** 获取会话信息、余额、更新账户设置、更新交易链接、冻结账户
- **联盟计划：** 获取联盟计划相关信息、领取奖励、查看奖励历史、设置联盟代码
- **双因素认证：** 创建/验证/禁用双因素认证
- **API 访问权限：** 创建或禁用 API 密钥

### 配置
- **汇率：** 获取当前汇率
- **费用计划：** 获取可用的费用计划
- **平台状态：** 检查平台是否正常运行

### 市场（CS2 app_id=730，Dota 2 app_id=570）
- **价格信息：** 获取销售历史、价格汇总
- **搜索：** 浏览 CS2/Dota 2 市场、搜索物品、获取物品详情、按皮肤名称搜索、设置搜索条件
- **购买：** 单个购买、批量购买物品
- **提款：** 将购买的物品提款到 Steam
- **下架：** 从市场上移除物品
- **重新上架：** 将下架的物品重新上架
- **修改价格：** 修改单个或多个物品的价格
- **交易历史：** 查看物品交易记录
- **购买收据：** 获取购买收据
- **提升物品可见度：** 提升物品的可见性、管理提升设置、购买提升套餐
- **皮肤目录：** 获取游戏中所有可用的皮肤名称
- **在售物品：** 查看游戏中当前在售的所有物品

### Steam
- **库存：** 列出 Steam 库存中的物品
- **存入：** 将 Steam 中的物品存入 BitSkins
- **交易：** 查看 Steam 交易报价及其状态

### 钱包
- **统计信息：** 获取钱包统计信息、了解 KYC（了解客户）相关限制
- **交易记录：** 列出已完成和待处理的交易
- **报告：** 生成并下载钱包报告

### 钱包存入
- **Binance Pay：** 创建 Binance Pay 存款
- **加密货币：** 获取 BTC、LTC、ETH 的存款地址
- **礼品码：** 兑换礼品码、查看已使用的礼品码
- **Zen：** 创建 Zen 存款
- **银行卡（无限制）：** 添加银行卡、查看银行卡信息、通过银行卡存款

### 钱包提款
- **加密货币：** 提款到 BTC、LTC、ETH 地址
- **Binance Pay：** 通过 Binance Pay 提款
- **银行卡（无限制）：** 提款到 Visa 卡

### WebSocket

实时更新通过 `wss://ws_bitskins.com` 提供。详情请参阅 [references/websocket.md](references/websocket.md)。

## 常见操作模式

### 市场搜索

市场搜索接口支持使用 `where` 对象进行过滤，并支持 `limit`/`offset` 分页：

```json
{
  "limit": 20,
  "offset": 0,
  "order": [{"field": "price", "order": "ASC"}],
  "where": {
    "skin_name": ["AK-47 | Redline"],
    "price_from": 1000,
    "price_to": 5000
  }
}
```

**注意：** 价格单位为 **分**（例如，1000 分 = $10.00）。

### 购买物品

要购买物品，您需要知道物品的 `id` 和 `app_id`。首先使用市场搜索功能找到物品，然后执行相应的购买操作：

```json
{"app_id": 730, "id": "ITEM_ID", "max_price": 1500}
```

`max_price` 参数用于防止在搜索和购买过程中价格发生变化。

### 上架/存入物品

1. 获取 Steam 库存中的物品：`POST /steam/inventory/list`
2. 存入物品：`POST /steam/deposit/many`，并提供物品 ID 和价格信息
3. 监控交易状态：`POST /steam/trade/active`

### 提取购买的物品

购买物品后，可以将物品提款到 Steam：

```json
{"app_id": 730, "id": "ITEM_ID"}
```

## 重要提示

- 在执行任何购买、销售、提款或财务操作之前，请务必先与用户确认。
- 价格单位为分（整数形式）。
- 游戏 ID：CS2 = 730，Dota 2 = 570。
- 在 “mine” 相关接口中，`where_mine` 过滤器支持以下状态：`listed`（已上架）、`pending_withdrawal`（待提款）、`in_queue`（排队中）、`given`（已赠送）、`need_to_withdraw`（需要提款）。
- 双因素认证代码具有时效性；请始终向用户索取最新的认证代码。