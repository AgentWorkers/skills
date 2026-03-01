---
name: etoro-api
version: 1.0.0
description: 该功能允许代理与 eToro API 进行交互，从而获取市场数据、投资组合信息以及社交功能的相关内容，并能够以编程方式执行交易操作。
homepage: https://api-portal.etoro.com/
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "category": "finance",
        "api_base": "https://public-api.etoro.com/api/v1",
      },
  }
---
# eToro 公共 API

基础 URL：`https://public-api.etoro.com/api/v1`

## 关于

此技能允许通过编程方式与用户的 eToro 账户进行交互，包括执行交易。

## 认证与必需的请求头

**密钥（用户在安装时提供）**

- **公共 API 密钥**：应用程序密钥
- **用户密钥**：用户账户密钥
- **环境**：真实投资组合或虚拟投资组合（真实/演示）

**密钥生成（面向用户）：**

1. 登录 eToro。
2. 设置 > 交易。
3. 创建新密钥。
4. 选择 **环境**（真实或虚拟/演示）和 **权限**（读取或写入）。
5. 验证身份并复制生成的用户密钥。

**请求头（每个请求）：**

- `x-request-id`：每个请求的唯一 UUID
- `x-api-key`：公共 API 密钥（<PUBLIC_KEY>）
- `x-user-key`：用户密钥（<USER_KEY>）

示例：

```bash
curl -X GET "https://public-api.etoro.com/api/v1/watchlists" \
  -H "x-request-id: <UUID>" \
  -H "x-api-key: <PUBLIC_KEY>" \
  -H "x-user-key: <USER_KEY>"
```

## 请求约定

- **以下所有路径都是相对于基础 URL 的**（基础 URL 已包含 `/api/v1`）。
  例如：`GET /watchlists` 表示 `GET https://public-api.etoro.com/api/v1/watchlists`。
- 查询参数放在 URL 中，路径参数放在 URL 路径中。
- 对于文档中标记为 `array` 的查询参数，以 **逗号分隔的值** 的形式发送（例如，`instrumentIds=1001,1002`）。
- 分页模式因端点而异：
  - 搜索：`pageNumber`, `pageSize`
  - 人员搜索和交易历史：`page`, `pageSize`
  - 数据源：`take`, `offset`
  - 收藏列表项列表：`pageNumber`, `itemsPerPage`
- **请求体的大小写很重要**：
  - 交易执行使用 **PascalCase** 格式的字段（例如，`InstrumentID`, `IsBuy`, `Leverage`）。
  - 市场关闭体使用 `InstrumentId`（首字母大写，其余小写）。
  - 收藏列表项使用 `ItemId`, `ItemType`, `ItemRank`。
  - 数据源帖子体使用小驼峰式命名（`owner`, `message`, `tags`, `mentions`, `attachments`）。
- 一些响应可能会对相似的概念使用不同的大小写（例如，`instrumentId` 与 `InstrumentID`）。在提取 ID 时，如果两者都存在，请同时处理。

## 演示交易与真实交易

- 使用 **演示执行端点**（包含 `/demo/`）进行测试和模拟交易。
- 使用 **非演示执行端点** 进行真实交易。
- 对于投资组合/损益：
  - 演示：`/trading/info/demo/*`
  - 真实：`/trading/info/portfolio` 和 `/trading/info/real/pnl`
- 确保您的密钥环境与端点匹配（虚拟或真实）。每个用户密钥都与特定的环境相关联。

## 使用默认值

- 重要提示：您不需要指定所有参数。例如，如果用户没有指定杠杆率，则不要在 API 请求中发送该参数。

## 快速开始（演示交易）

1. **使用搜索功能获取 `instrumentId`**。
   搜索请求中需要 `fields` 参数。

```bash
curl -X GET "https://public-api.etoro.com/api/v1/market-data/search?internalSymbolFull=BTC&fields=instrumentId,internalSymbolFull,displayname" \
  -H "x-api-key: <PUBLIC_KEY>" \
  -H "x-user-key: <USER_KEY>" \
  -H "x-request-id: <UUID>"
```

2. **按金额下达演示市场订单**（使用 PascalCase 格式的请求体）：

```bash
curl -X POST "https://public-api.etoro.com/api/v1/trading/execution/demo/market-open-orders/by-amount" \
  -H "x-api-key: <PUBLIC_KEY>" \
  -H "x-user-key: <USER_KEY>" \
  -H "x-request-id: <UUID>" \
  -H "Content-Type: application/json" \
  -d '{
    "InstrumentID": 100000,
    "IsBuy": true,
    "Leverage": 1,
    "Amount": 100
  }'
```

## 常见 ID

- `instrumentId`：来自搜索或仪器元数据
- `positionId`：来自投资组合端点
- `orderId`：来自执行响应或投资组合端点
- `marketId`：由仪器数据源端点使用（通常在仪器元数据/搜索字段中提供）
- `userId`：eToro 用户的数字 ID（在响应中通常称为 **CID**；通过人员端点/搜索功能获取）
- `watchlistId`：来自收藏列表列表/创建端点

## 市场数据（请求）

**搜索仪器**

- `GET /market-data/search`
- 必需的查询参数：`fields`（要返回的仪器字段的逗号分隔列表）
- 可选参数：`searchText`, `pageSize`, `pageNumber`, `sort`
- 搜索端点支持根据结果中返回的字段进行过滤；要查找确切的符号，请使用 `internalSymbolFull` 作为查询参数并确保完全匹配。
- 当需要 ID 时，建议至少包含以下字段：仪器标识符（可能显示为 `instrumentId` 或 `InstrumentID`），以及 `internalSymbolFull` 和 `displayname`（如果计划使用数据源，则还需要 `marketId`）。

**元数据**

- `GET /market-data/instruments`  
  过滤条件：`instrumentIds`, `exchangeIds`, `stocksIndustryIds`, `instrumentTypeIds`。

**价格与历史数据**

- `GET /market-data/instruments/rates`  
  必需参数：`instrumentIds`（逗号分隔）。
- `GET /market-data/instruments/history/closing-price`  
  返回所有仪器的历史收盘价（批量）。
- `GET /market-data/instruments/{instrumentId}/history/candles/{direction}/{interval}/{candlesCount}`  
  `direction`：`asc` 或 `desc`。`candlesCount` 最大为 1000。
- 仅使用支持的 `interval` 值（如有疑问，请参阅文档确认）。

**参考数据**

- `GET /market-data/exchanges`（可选参数 `exchangeIds`）
- `GET /market-data/instrument-types`
- `GET /market-data/stocks-industries`（可选参数 `stocksIndustryIds`）

## 交易执行（请求）

> 需要具有适当权限的密钥（通常是 **写入权限**）和正确的环境（演示或真实）。

### 按金额下达的市场开放订单

端点：

- `POST /trading/execution/demo/market-open-orders/by-amount`
- `POST /trading/execution/market-open-orders/by-amount`

请求体（PascalCase 格式，JSON）：

- **必需参数：** `InstrumentID`, `IsBuy`, `Leverage`, `Amount`
- **可选参数：** `StopLossRate`, `TakeProfitRate`, `IsTslEnabled`, `IsNoStopLoss`, `IsNoTakeProfit`

### 按单位下达的市场开放订单

端点：

- `POST /trading/execution/demo/market-open-orders/by-units`
- `POST /trading/execution/market-open-orders/by-units`

请求体（PascalCase 格式，JSON）：

- **必需参数：** `InstrumentID`, `IsBuy`, `Leverage`, `AmountInUnits`
- **可选参数：** `StopLossRate`, `TakeProfitRate`, `IsTslEnabled`, `IsNoStopLoss`, `IsNoTakeProfit`

### 取消市场开放订单

端点：

- `DELETE /trading/execution/demo/market-open-orders/{orderId}`
- `DELETE /trading/execution/market-open-orders/{orderId}`

### 市场关闭订单

端点：

- `POST /trading/execution/demo/market-close-orders/positions/{positionId}`
- `POST /trading/execution/market-close-orders/positions/{positionId}`
- `DELETE /trading/execution/market-close-orders/{orderId}`
- `DELETE /trading/execution/market-close-orders/{orderId}`

请求体（JSON）：

- **必需参数：** `InstrumentId`
- **可选参数：** `UnitsToDeduct`（数字或 `null`）

部分关闭：设置 `UnitsToDeduct`。
完全关闭：将 `UnitsToDeduct` 设置为 `null`。
必须根据 `positionId` 关闭订单，而不是根据符号。

### 市场触及型（限价）订单

端点：

- `POST /trading/execution/demo/limit-orders`
- `DELETE /trading/execution/demo/limit-orders/{orderId}`
- `POST /trading/execution/limit-orders`
- `DELETE /trading/execution/limit-orders/{orderId}`

请求体（PascalCase 格式，JSON）：

- **必需参数：** `InstrumentID`, `IsBuy`, `Leverage`, **`Rate`**，以及 **`Amount` 或 `AmountInUnits` 中的一个**
- **可选参数：** `StopLossRate`, `TakeProfitRate`, `IsTslEnabled`, `IsNoStopLoss`, `IsNoTakeProfit`
- **不要发送：** `IsDiscounted`, `CID`

## 交易信息与投资组合（请求）

- `GET /trading/info/demo/pnl`
- `GET /trading/info/real/pnl`
- `GET /trading/info/demo/portfolio`
- `GET /trading/info/portfolio`  
  使用这些信息来获取用于关闭/取消操作的 `positionId` 和 `orderId`。
- `GET /trading/info/trade/history`  
  必需参数：`minDate`（YYYY-MM-DD）。可选参数：`page`, `pageSize`。

## 收藏列表（请求）

**用户收藏列表**

- `GET /watchlists`  
  可选参数：`itemsPerPageForSingle`, `ensureBuiltinWatchlists`, `addRelatedAssets`。
- `GET /watchlists/{watchlistId}`  
  可选参数：`pageNumber`, `itemsPerPage`。
- `POST /watchlists`  
  查询参数：`name`（必需），`type`, `dynamicQuery`（可选）。（使用查询参数，而不是 JSON 请求体。）
- `PUT /watchlists/{watchlistId}`  
  查询参数：`newName`（必需）。（使用查询参数，而不是 JSON 请求体。）
- `DELETE /watchlists/{watchlistId}`

**收藏列表项（请求体结构）**

`WatchlistItemDto` 字段：

- `ItemId`（必需，整数）
- `ItemType`（必需，字符串：`Instrument` 或 `Person`）
- `ItemRank`（可选，整数）

端点：

- `POST /watchlists/{watchlistId}/items`
- `PUT /watchlists/{watchlistId}/items`
- `DELETE /watchlists/{watchlistId}/items`

示例请求体：

```json
[
  { "ItemId": 12345, "ItemType": "Instrument", "ItemRank": 1 },
  { "ItemId": 67890, "ItemType": "Instrument", "ItemRank": 2 }
]
```

**默认收藏列表**

- `POST /watchlists/default-watchlist/selected-items`
- `GET /watchlists/default-watchlists/items`  
  可选参数：`itemsLimit`, `itemsPerPage`。
- `POST /watchlists/newasdefault-watchlist`  
  查询参数：`name`（必需），`type`, `dynamicQuery`（可选）。
- `PUT /watchlists/setUserSelectedUserDefault/{watchlistId}`  
  查询参数：`newRank`（必需）。

**公共收藏列表**

- `GET /watchlists/public/{userId}`  
- `GET /watchlists/public/{userId}/{watchlistId}`

## 数据源（请求）

**读取数据源**

- `GET /feeds/instrument/{marketId}`  
  可选参数：`requesterUserId`, `take`, `offset`, `badgesExperimentIsEnabled`, `reactionsPageSize`。
- `GET /feeds/user/{userId}`  
  可选参数：`requesterUserId`, `take`, `offset`, `badgesExperimentIsEnabled`, `reactionsPageSize`。

注意事项：

- `marketId` 与仪器相关联（通常可以通过在 `fields` 中包含它来通过仪器元数据/搜索功能获取）。
- `userId` 是用户的数字 ID（CID）。如果您只有用户名，可以通过人员端点（参见用户信息与分析）来获取数字 ID。

**创建帖子**

- `POST /feeds/post`
- 请求体字段（小驼峰式命名，JSON）：
  - `owner`（整数）
  - `message`（字符串）
  - `tags`：`{ "tags": [{ "name": "...", "id": "..." }] }`
  - `mentions`：`{ "mentions": [{ "userName": "...", "id": "...", "isDirect": true }] }`
  - `attachments`：包含 `url`, `title`, `host`, `description`, `mediaType` 的对象数组，以及可选的 `media`。

示例请求体：

```json
{ "message": "Hello eToro feed!" }
```

## 精选列表与推荐（请求）

- `GET /curated-lists`
- `GET /market-recommendations/{itemsCount}`

## 热门投资者（跟随者）

- `GET /pi-data/copiers`

## 用户信息与分析（请求）

- `GET /user-info/people`  
  可选参数：`usernames`, `cidList`。
  当您需要数字 `userId` 用于数据源/公共收藏列表时，可以使用此信息将 **用户名 ↔ CID` 关联起来。
- `GET /user-info/people/search`  
  必需参数：`period`。可选参数：`page`, `pageSize`, `sort`, `popularInvestor`, `gainMax`, `maxDailyRiskScoreMin`, `maxDailyRiskScoreMax`, `maxMonthlyRiskScoreMin`, `maxMonthlyRiskScoreMax`, `weeksSinceRegistrationMin`, `countryId`, `instrumentId`, `instrumentPctMin`, `instrumentPctMax`, `isTestAccount` 等过滤条件。
- `GET /user-info/people/{username}/gain`
- `GET /user-info/people/{username}/daily-gain`  
  必需参数：`minDate`, `maxDate`, `type`（`Daily` 或 `Period`）。
- `GET /user-info/people/{username}/portfolio/live`
- `GET /user-info/people/{username}/tradeinfo`  
  必需参数：`period`（例如，`LastTwoYears`）。

## 响应与数据结构**

有关响应结构和完整示例，请参考：

- https://api-portal.etoro.com/
- MCP 服务器：`https://api-portal.etoro.com/mcp`