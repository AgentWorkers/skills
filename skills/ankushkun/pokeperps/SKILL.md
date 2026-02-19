---
name: pokeperps
description: 在 Solana 上的 PokePerps DEX 上，您可以交易基于宝可梦 TCG 卡价格的永续期货。您可以搜索卡片、分析价格、模拟交易、开设/平仓杠杆多头/空头头寸以及管理投资组合。当用户询问有关宝可梦卡片交易、永续期货或 PokePerps 的信息时，可以使用该平台。
license: BUSL-1.1
compatibility: Requires network access to https://backend.pokeperps.fun. Optional Solana keypair for trade execution.
metadata:
  author: ankushKun
  version: "1.0"
  website: https://pokeperps.fun
  blockchain: solana
---
# PokePerps AI Agent Skill

## 平台：[PokePerps](https://pokeperps.fun)  
PokePerps 是一个去中心化的永续期货交易所，专注于宝可梦集换式卡牌（TCG）的价格交易。  

## 区块链：Solana（主网测试版）  
PokePerps 使用 Solana 区块链作为基础技术框架。  

## 后端 API：`https://backend.pokeperps.fun`  
所有与后端交互的请求都发送到这个地址。  

## WebSocket：`wss://backend.pokeperps.fun/ws/trading`  
用于实时接收和发送交易相关的消息。  

## 程序 ID：`8hH5CWo14R5QhaFUuXpxJytchS6NgrhRLHASyVeriEvN`  
这是用于识别该 AI 代理的唯一程序 ID。  

## 抵押品：USDC（`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`）  
在 PokePerps 中，交易需要使用 USDC 作为抵押品。  

### PokePerps 的主要功能  
PokePerps 允许用户交易基于宝可梦集换式卡牌实际价格的永续期货合约。这些价格数据实时从 TCGPlayer 市场获取，并通过 Ed25519 算法进行加密处理后发布到区块链上。  

## 推荐使用 MCP 服务器（Model Context Protocol）  
AI 代理与 PokePerps 交互的最佳方式是通过 **Model Context Protocol (MCP) 服务器**。  

#### 仅读取模式（无需钱包）  
```json
{
  "mcpServers": {
    "pokeperps": {
      "command": "npx",
      "args": ["@pokeperps/mcp"]
    }
  }
}
```  

#### 需要 Solana 密钥对的交易执行  
```json
{
  "mcpServers": {
    "pokeperps": {
      "command": "npx",
      "args": ["@pokeperps/mcp"],
      "env": {
        "POKEPERPS_KEYPAIR": "/path/to/your/keypair.json"
      }
    }
  }
}
```  

### MCP 环境变量  
以下是 MCP 服务器需要的一些配置参数：  
| 变量 | 描述 | 默认值 |  
| --- | --- | --- |  
| `POKEPERPS_KEYPAIR` | Solana 密钥对的 JSON 文件路径 | （仅读取模式时无需提供） |  
| `POKEPERPS_API_URL` | 后端 API 地址 | `https://backend.pokeperps.fun` |  
| `POKEPERPS_RPC_URL` | Solana RPC 地址 | `https://api.mainnet-beta.solana.com` |  

### MCP 工具  
PokePerps 提供了多种工具来帮助用户和代理进行交易和数据分析：  
| 工具 | 描述 |  
| --- | --- |  
| `get_market_movers` | 获取收益最高、损失最大或波动最大的卡牌信息 |  
| `get_portfolio` | 查看钱包中的全部持仓及计算后的盈亏（PnL） |  
| `get_trading_signals` | 提供预先计算的交易信号和建议 |  
| `prepare-trade` | 在交易前验证交易细节（如保证金、费用、风险等） |  
| `simulate_trade` | 模拟不同价格下的盈亏情况 |  
| `search_cards` | 按名称搜索宝可梦卡牌 |  
| `get_card_details` | 获取卡牌的完整信息（包括售价、销售记录等） |  
| `batch_get_cards` | 一次请求可获取最多 50 张卡牌信息 |  
| `get_tradable_products` | 列出所有有活跃交易市场的产品 ID |  
| `get_trading_config` | 设置交易参数（杠杆率、费用等） |  

#### 需要 `POKEPERPS_KEYPAIR` 的执行工具  
| 工具 | 描述 |  
| --- | --- |  
| `open_position` | 开立新的多头/空头头寸 |  
| `close_position` | 平仓以实现盈亏 |  
| `deposit` | 向交易账户存入 USDC |  
| `withdraw` | 从交易账户提取 USDC |  
| `get_wallet_status` | 查看钱包余额和交易状态 |  

### 相关资源  
- `pokeperps://docs/trading-guide`：交易指南和风险参数  
- `pokeperps://docs/api-reference`：完整的 OpenAPI 规范  

## 交易参数  
以下是 PokePerps 的主要交易参数：  
| 参数 | 值 |  
| --- | --- |  
| 最大杠杆率 | 50 倍 |  
| 最小持仓金额 | 1 美元 |  
| 每用户最大持仓金额 | 100,000 美元 |  
| 交易费用 | 开仓和平仓时收取 0.05%（5 个基点） |  
| 维持保证金 | 1%（100 个基点） |  
| 清算费用 | 清算方收取 0.5%，保险公司收取 0.5% |  
| 资金追加间隔 | 8 小时 |  
| 资金追加率上限 | 每间隔 ±0.05% |  
| 价格更新频率 | 每 15 秒 |  
| 抵押品 | USDC（SPL Token） |  

### 操作说明  
- 可以选择 **做多**（预测价格上升）或 **做空**（预测价格下降）  
- 可使用 1 到 50 倍的杠杆率  
- 持仓没有到期时间限制（永久有效）  
- 可随时平仓以实现盈亏  
- 价格实时跟踪 TCGPlayer 市场价格  

## 架构说明  
后端不负责交易数据的签名或提交；这些操作由客户端完成。  

## API 端点  
基础 URL：`https://backend.pokeperps.fun`  

### 卡片查询  
以下是用于查询卡牌信息的 API 方法：  
| 方法 | 路径 | 描述 |  
| --- | --- | --- |  
| GET | `/api/cards/search?q={query}&limit={1-50}` | 按名称搜索卡牌 |  
| GET | `/api/dashboard?limit={1-200}` | 显示最活跃的交易卡牌 |  
| GET | `/api/cards/{product_id}` | 获取单张卡牌的详细信息 |  
| GET | `/api/cards/{product_id}/bundle` | 一次性获取所有卡牌数据 |  
| GET | `/api/cards/{product_id}/history?range=month` | 查看价格历史 |  
| GET | `/api/cards/{product_id}/signals` | 获取交易信号和建议 |  
| POST | `/api/cards/batch` | 一次请求获取最多 50 张卡牌信息 |  

### 交易相关 API  
以下是用于进行交易的 API 方法：  
| 方法 | 路径 | 描述 |  
| --- | --- | --- |  
| GET | `/api/trading/tradable` | 查看所有可交易的产品 ID |  
| GET | `/api/trading/config` | 设置交易参数 |  
| GET | `/api/trading/exchange` | 查看交易所状态 |  
| GET | `/api/trading/market/{product_id}` | 查看市场状态 |  
| GET | `/api/trading/market/{product_id}/stats` | 查看市场统计数据 |  
| GET | `/api/trading/account/{wallet}` | 查看用户账户信息 |  
| GET | `/api/trading/account/{wallet}/positions` | 查看用户持仓 |  
| GET | `/api/trading/portfolio/{wallet}` | 查看完整持仓及盈亏 |  
| GET | `/api/trading/prepare-trade/{id}?wallet=X&side=Y&size=Z&leverage=W` | 交易前验证 |  
| POST | `/api/trading/simulate` | 模拟交易结果 |  
| GET | `/api/trading/analytics/movers?limit={1-50}` | 获取收益最高/最低或波动最大的卡牌信息 |  

### 交易相关操作  
以下是用于执行交易的 API 方法：  
| 方法 | 路径 | 描述 |  
| --- | --- | --- |  
| POST | `/api/trading/tx/create-account` | 创建交易账户 |  
| POST | `/api/trading/tx/deposit` | 存入 USDC |  
| POST | `/api/trading/tx/withdraw` | 提取 USDC |  
| POST | `/api/trading/tx/open-position` | 开立多头/空头头寸 |  
| POST | `/api/trading/tx/close-position` | 平仓 |  
| POST | `/api/trading/tx/add-margin` | 为持仓追加保证金 |  

### Oracle 数据  
`/api/oracle/prices`：获取所有当前的 oracle 价格  
`/api/trading/oracle/prices`：获取最佳可用价格  
`/api/trading/oracle/{product_id}`：获取单张卡牌的 oracle 价格  
`/api/trading/oracle/prices`：批量获取多个产品的 oracle 价格  

### 优化交易流程  
与传统流程相比，PokePerps 仅使用了 **6 个 API 调用**，而非传统的 15 个以上。  

### 盈亏（PnL）计算  
PokePerps 采用特定的算法来计算用户的盈亏（PnL）。  

### 决策支持  
`/api/cards/{id}/signals` 提供预先计算的交易分析数据：  
- **做多**：24 小时内的价格变化为正，且活动评分高；近期销售量高于市场价格；挂牌数量减少（供应减少）。  
- **做空**：24 小时内的价格变化为负，且 30 天内的价格变化也为负；近期销售量低于市场价格；挂牌数量增加（供应增加）；多头持仓的未平仓合约数量（OI）相对于空头较多（可能存在做空挤压）。  

### WebSocket 连接  
通过 `wss://backend.pokeperps.fun/ws/trading` 进行实时通信：  
事件类型包括 `price_update`（价格更新）、`position_opened`（头寸开启）、`position_closed`（头寸平仓）、`market_stats`（市场统计）和 `account_update`（账户信息更新）。  

## 速率限制  
- 全局 API 请求限制：每个 IP 每分钟 300 次请求。  
- Oracle 价格更新频率：每个 IP 每 10 秒更新一次（每个产品最多 2 次）。  
- WebSocket 连接限制：每个 IP 最多 25 个连接，总计 1000 个。  
- 每次请求最多可请求 200 个产品 ID。  

## 错误代码  
以下是部分常见的错误代码及其含义：  
| 代码 | 名称 | 含义 |  
| --- | --- | --- |  
| 6012 | InvalidAmount | 输入的金额无效或为负数 |  
| 6013 | InsufficientBalance | 账户余额不足 |  
| 6014 | ExchangePaused | 交易所暂停服务 |  
| 6015 | InvalidLeverage | 杠杆率超出范围（1-50 倍） |  
| 6016 | PositionTooSmall | 持仓金额低于最低要求 |  
| 6018 | MarketInactive | 市场暂停服务 |  
| 6019 | MaxOpenInterestExceeded | 未平仓合约数量达到上限 |  
| 6030 | OraclePriceStale | 价格数据过期（超过 15 秒） |  
| 6031 | PositionTooLarge | 持仓金额超过上限（100,000 美元） |  
| 6035 | InvalidEd25519Instruction | Ed25519 算法签名错误 |  

更多详细信息，请参阅 [references/API.md](references/API.md)。  

### AI 代理的最佳实践  
- **减少 API 调用次数**：  
  - 例如，`GET /account` + `GET /positions` + 多次 oracle 调用，可以合并为 `GET /api/trading/portfolio/{wallet}`（一次调用）。  
  - 多次 `GET /api/cards/{id}` 调用，可以合并为 `POST /api/cards/batch`（一次调用获取最多 50 张卡牌信息）。  
- 交易前的验证步骤可以合并为 `GET /api/trading/prepare-trade/{id}`（一次调用）。  
- 避免扫描所有卡牌来获取价格变动信息，直接使用 `GET /api/trading/analytics/movers`（一次调用）。  

### 持仓管理建议：  
1. 在开新头寸前检查 `riskStatus`（风险状态）；如果显示“警告”或“危险”，则避免开仓。  
2. 使用 `distanceToLiquidation` 作为止损标准（保守策略：<10% 时平仓；中等策略：<5%）。  
3. 监控 `fundingDirection`，避免持有需要支付额外费用的持仓。  
4. 在进行大额交易前，检查 `wouldExceedOI` 以确保不会超出保证金限制。  

### 安全措施：  
- 在签名交易前，始终在客户端验证交易数据（PDA）。  
- 不要在 API 调用中暴露私钥。  
- 在交易前确认 `oracleAge` 是否小于 15 秒。  
- 在执行交易前，通过 `prepare-trade` 方法检查是否可以进行交易。  

## 其他参考资料：  
- [references/API.md](references/API.md)：完整的 API 请求/响应格式。  
- [references/TRANSACTIONS.md](references/TRANSACTIONS.md)：链上交易构建、PDA 计算方法及 Ed25519 算法签名。  
- [references/EXAMPLES.md](references/EXAMPLES.md)：完整的代码示例（TypeScript、Python、cURL）。