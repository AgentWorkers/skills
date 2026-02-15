---
name: hyperliquid-prime
description: 在 Hyperliquid 的衍生品市场中（包括原生市场及 HIP-3 市场）进行交易，支持智能订单路由和跨市场拆分功能。适用于用户需要在 Hyperliquid 平台上交易加密货币、股票或商品的情况，可确保在分散的市场中获得最佳执行效果；支持将大订单拆分到多个交易场所；允许用户比较不同市场的资金费率；提供聚合的订单簿视图；并支持管理多种类型的抵押品。系统能够同时处理原生 Hyperliquid 衍生品（如 ETH、BTC）以及 HIP-3 市场的交易。在执行过程中，当需要最佳流动性时，系统会自动处理抵押品兑换（例如 USDC 到 USDH/USDT0）。
---

# Hyperliquid Prime

这是一个TypeScript SDK，它作为Hyperliquid原生市场（包括ETH、BTC）以及HIP-3部署市场的**中间层**（即“代理经纪层”）。该SDK能够自动发现某种资产的所有可交易市场，比较各市场的流动性、资金费用和执行成本，并将订单路由到最佳执行路径；或者在多个市场之间分散订单以获得最优的成交结果，同时支持自动的抵押品转换。

## 适用场景

- 在Hyperliquid平台上交易加密货币、股票（如AAPL、NVDA、TSLA）、指数或商品（如GOLD、SILVER）；
- 需要在多个市场（包括原生市场和HIP-3市场）中为同一资产选择最佳执行路径；
- 为提高成交效果和降低价格波动，将大额订单分散到多个市场；
- 比较不同抵押品类型的资金费用；
- 查看分散在不同市场中的汇总订单簿；
- 管理可能涉及多种抵押品类型的头寸；
- 当非USDC市场提供更优惠的价格时，自动进行抵押品转换（例如将USDC转换为USDH或USDT0）。

## 快速入门

### 安装

```bash
npm install hyperliquid-prime
```

### 仅读模式（无需钱包）

```typescript
import { HyperliquidPrime } from 'hyperliquid-prime'

const hp = new HyperliquidPrime({ testnet: true })
await hp.connect()

// Get all perp markets for an asset (native + HIP-3)
const markets = hp.getMarkets('ETH') // or 'TSLA', 'BTC', etc.

// Get routing quote for best execution
const quote = await hp.quote('TSLA', 'buy', 50)
const quoteWithLev = await hp.quote('TSLA', 'buy', 50, { leverage: 5, isCross: true })

// Aggregated orderbook
const book = await hp.getAggregatedBook('TSLA')

// Funding rate comparison
const funding = await hp.getFundingComparison('TSLA')

await hp.disconnect()
```

### 交易模式（需要钱包）

```typescript
const hp = new HyperliquidPrime({
  privateKey: '0x...',
  testnet: true,
})
await hp.connect()

// Quote then execute (recommended)
const quote = await hp.quote('TSLA', 'buy', 50, { leverage: 5, isCross: true })
const receipt = await hp.execute(quote.plan)

// One-step convenience
const receipt2 = await hp.long('TSLA', 50, { leverage: 5 })
const receipt3 = await hp.short('TSLA', 25, { leverage: 3, isCross: false })

// Split across multiple markets for better fills
const splitQuote = await hp.quoteSplit('TSLA', 'buy', 200, { leverage: 4 })
const splitReceipt = await hp.executeSplit(splitQuote.splitPlan)
// Or one-step: await hp.longSplit('TSLA', 200)

// Unified position view
const positions = await hp.getGroupedPositions()

await hp.disconnect()
```

### 命令行接口（CLI）

```bash
# Show all perp markets for an asset (native + HIP-3)
hp markets ETH
hp markets TSLA

# Aggregated orderbook
hp book TSLA

# Compare funding rates
hp funding TSLA

# Get routing quote
hp quote TSLA buy 50
hp quote TSLA buy 50 --leverage 5
hp quote TSLA buy 50 --leverage 3 --isolated

# Execute trades
HP_PRIVATE_KEY=0x... hp long TSLA 50
HP_PRIVATE_KEY=0x... hp short TSLA 25
HP_PRIVATE_KEY=0x... hp long TSLA 50 --leverage 5
HP_PRIVATE_KEY=0x... hp short TSLA 25 --leverage 3 --isolated

# View positions and balance
HP_PRIVATE_KEY=0x... hp positions
HP_PRIVATE_KEY=0x... hp balance

# Use testnet
hp markets TSLA --testnet
```

## 重要说明：费用与自动操作

**构建费**：所有通过SDK执行的订单默认会收取1个基点（0.01%）的构建费，该费用由Hyperliquid的原生构建费机制收取。首次使用钱包进行交易时，SDK会发送一条链上交易以确认这笔费用。如需完全禁用此费用，请在配置文件中设置`builder: null`。

**抵押品转换（仅适用于拆分订单）**：当`executeSplit()`方法将订单路由到非USDC抵押品市场时，SDK会自动执行以下操作：
1. 启用用户账户的DEX（去中心化交易所）功能；
2. 从衍生品账户向现货账户转移USDC；
3. 下单将USDC转换为所需的抵押品代币（如USDH或USDT0）；
4. 在转换金额中加上1%的缓冲费以应对价格滑点。

这些操作仅在拆分订单执行时发生，并且仅在需要使用非USDC抵押品时才会执行。

**仅读操作**：查询报价、查看订单簿、比较资金费用以及发现市场功能无需钱包，也不会产生任何链上操作。

**认证信息**：交易操作需要使用`HP_PRIVATE_KEY`环境变量或`privateKey`配置选项提供的私钥。该私钥用于签署发送到Hyperliquid API的交易。源代码可在<https://github.com/mehranhydary/hl-prime>处查看，可供审计使用。

**用户确认流程**：SDK采用“先报价后执行”的确认机制：
- `quote()` / `quoteSplit()`方法仅用于获取执行计划（包括预估价格、市场和费用），不会触发任何链上操作；
- 调用者需（通过编程方式或CLI输出）审查该计划；
- `execute()` / `executeSplit()`方法必须被显式调用才能执行链上操作（如下单、确认费用或转换抵押品）；
- 便捷的一键操作方法（`long()`、`short()`、`longSplit()`、`shortSplit()`）结合了这两个步骤，以实现更直观的控制。

**实现说明**：此技能包仅包含使用说明（SKILL.md文件），SDK的实现需要通过`npm install hyperliquid-prime`单独安装。源代码为开源项目，可在安装前在GitHub仓库中查看。

## 路由原理

当你调用`hp.quote("TSLA", "buy", 50)`时，SDK会执行以下操作：
1. 获取TSLA在所有市场中的订单簿信息；
2. 遍历所有订单簿，估算平均成交价格和价格波动；
3. 根据以下因素对各个市场进行评分：
   - **价格波动**：完成交易所需的成本（以基点计）；
   **资金费用**：偏好更有利的资金方向；
   **抵押品转换成本**：转换为所需抵押品所需的预估费用；
4. 选择评分最低的市场并生成执行计划。

对于拆分订单（`quoteSplit`），SDK会合并所有订单簿的信息，优先使用最便宜的流动性在多个市场完成交易，并生成相应的拆分执行路径。抵押品要求和转换操作会在`executeSplit()`方法执行时根据实时余额进行估算和执行。如果报价选项中包含了杠杆比例，执行时会根据每个市场的情况应用相应的杠杆比例。

## 配置设置

```typescript
interface HyperliquidPrimeConfig {
  privateKey?: `0x${string}` // Required for trading
  walletAddress?: string       // Derived from privateKey if not provided
  testnet?: boolean            // Default: false
  defaultSlippage?: number     // Default: 0.01 (1%)
  logLevel?: 'debug' | 'info' | 'warn' | 'error' | 'silent'
  prettyLogs?: boolean         // Default: false
  builder?: BuilderConfig | null // Builder fee (default: 1 bps, null to disable)
}
```

### 构建费

所有通过SDK执行的订单默认会收取1个基点（0.01%）的构建费。你可以通过设置`builder: null`来禁用此费用，或者提供自定义的`{ address, feeBps }`配置来覆盖默认值。

## 主要方法

### 仅读模式
- `getMarkets(asset)`：获取某种资产的所有可交易市场（包括原生市场和HIP-3市场）；
- `getAggregatedMarkets()`：获取包含多个市场的资产组合；
- `getAggregatedBook(asset)`：获取所有市场的合并订单簿；
- `getFundingComparison(asset)`：比较不同市场的资金费用；
- `quote(asset, side, size, options?)`：为单个市场生成报价；
- `quoteSplit(asset, side, size, options?)`：为多个市场生成拆分报价。

### 交易模式（需要钱包）
- `execute(plan)`：执行单个市场的报价；
- `executeSplit(plan)`：执行拆分报价（包括抵押品转换）；
- `long(asset, size, options?)`：在最佳市场生成买单并执行；
- `short(asset, size, options?)`：在最佳市场生成卖单并执行；
- `longSplit(asset, size, options?)`：在多个市场生成拆分买单并执行；
- `shortSplit(asset, size, options?)`：在多个市场生成拆分卖单并执行；
- `close(asset)`：关闭某种资产的所有头寸。

### 交易选项
- `leverage?: number`：正数，例如5表示5倍杠杆；
- `isCross?: boolean`：默认值为`true`（跨市场交易）；设置为`false`表示仅在一个市场内交易；
- 如果设置了`isCross`，则必须同时设置`leverage`；如果省略`isCross`，SDK不会尝试设置杠杆比例。

### 头寸与余额
- `getPositions()`：获取所有头寸及其市场相关信息；
- `getGroupedPositions()`：按基础资产分组头寸；
- `getBalance()`：获取账户的保证金概览。

## 项目仓库

<https://github.com/mehranhydary/hl-prime>

## 许可证

MIT许可证