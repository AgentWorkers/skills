# Cetus Protocol SDK v2 - OpenClaw集成指南

本指南涵盖了所有用于在Sui平台上构建DeFi应用程序的Cetus SDK v2包。

---

## 目录

1. [通用SDK](#common-sdk)
2. [CLMM SDK](#clmm-sdk)
3. [DLMM SDK](#dlmm-sdk)
4. [Vaults SDK](#vaults-sdk)
5. [Farms SDK](#farms-sdk)
6. [xCETUS SDK](#xcetus-sdk)
7. [限价单SDK](#limit-order-sdk)
8. [燃烧SDK](#burn-sdk)
9. [DCA SDK](#dca-sdk)
10. [Zap SDK](#zap-sdk)
11. [聚合器SDK](#aggregator-sdk)

---

## 通用SDK

这是一个基础性的实用工具库，所有Cetus SDK都会使用它。

```bash
npm install @cetusprotocol/common-sdk
```

该库提供了协议交互所需的基本实用工具和共享功能。所有其他SDK都依赖于这个包。

---

## CLMM SDK

集中式流动性做市商（Concentrated Liquidity Market Maker）——Cetus的核心自动做市商（AMM）机制。

```bash
npm install @cetusprotocol/sui-clmm-sdk
```

### 初始化

```typescript
import { CetusClmmSDK } from '@cetusprotocol/sui-clmm-sdk'

// Default mainnet
const sdk = CetusClmmSDK.createSDK()

// Custom environment
const sdk = CetusClmmSDK.createSDK({ env: 'mainnet' }) // or 'testnet'

// Custom RPC
const sdk = CetusClmmSDK.createSDK({ env: 'mainnet', full_rpc_url: 'YOUR_URL' })

// Custom SuiClient
const sdk = CetusClmmSDK.createSDK({ env: 'mainnet', sui_client: yourClient })

// Set sender address (required before tx operations)
sdk.setSenderAddress('YOUR_SUI_ADDRESS')
```

---

## DLMM SDK

动态流动性做市商（Dynamic Liquidity Market Maker）——基于离散bin的自动做市商机制，支持动态费用。

```bash
npm install @cetusprotocol/dlmm-sdk
```

### 初始化

```typescript
import { CetusDlmmSDK } from '@cetusprotocol/dlmm-sdk'

const sdk = CetusDlmmSDK.createSDK()
// or with options: CetusDlmmSDK.createSDK({ env, full_rpc_url, sui_client })
sdk.setSenderAddress(walletAddress)
```

### 池操作

```typescript
// Get all pools
const pools = await sdk.Dlmm.getPoolList()

// Get specific pool
const pool = await sdk.Dlmm.getPool(pool_id)

// Get bin configuration
const binConfig = await sdk.Dlmm.getBinConfig(config_id)

// Get pool transaction history
const history = await sdk.Dlmm.getPoolTransactionHistory(pool_id)
```

### 持仓管理

三种流动性分配策略：
- **现货**（Spot）：在所有bin中均匀分配流动性
- **买卖价**（BidAsk）：集中在特定价格区间
- **曲线**（Curve）：平滑的钟形曲线分布

```typescript
// Calculate optimal liquidity distribution
const addInfo = await sdk.Dlmm.calculateAddLiquidityInfo(params)

// Add liquidity
const payload = await sdk.Dlmm.addLiquidityPayload(params)

// Remove liquidity
const payload = await sdk.Dlmm.removeLiquidityPayload(params)

// Close position
const payload = await sdk.Dlmm.closePositionPayload(params)
```

### 交换操作

```typescript
// Get swap quote
const quote = await sdk.Dlmm.preSwapQuote(params)

// Execute swap
const payload = await sdk.Dlmm.swapPayload(params)
```

### 费用与奖励操作

```typescript
// Get total fee rate (base + variable)
const feeRate = await sdk.Dlmm.getTotalFeeRate(pool_id)

// Collect fees
const payload = await sdk.Dlmm.collectFeePayload(params)

// Collect rewards
const payload = await sdk.Dlmm.collectRewardPayload(params)
```

### 池创建

```typescript
// Create pool only
const payload = await sdk.Dlmm.createPoolPayload(params)

// Create pool + add initial liquidity
const payload = await sdk.Dlmm.createPoolAndAddLiquidityPayload(params)
```

### 实用工具：BinUtils

```typescript
import { BinUtils } from '@cetusprotocol/dlmm-sdk'

// Price-bin conversions
BinUtils.getPriceFromBinId(binId, binStep)
BinUtils.getBinIdFromPrice(price, binStep)

// Liquidity calculations
BinUtils.calculateLiquidity(params)
```

---

## Vaults SDK

自动化流动性管理，支持费用再投资和重新平衡。

```bash
npm install @cetusprotocol/vaults-sdk
```

### 初始化

```typescript
import { CetusVaultsSDK } from '@cetusprotocol/vaults-sdk'

const sdk = CetusVaultsSDK.createSDK()
// or: CetusVaultsSDK.createSDK({ env, sui_client })
// or: CetusVaultsSDK.createSDK({ env, full_rpc_url })
sdk.setSenderAddress(wallet)
```

### 存款

```typescript
// Calculate deposit amounts
const amounts = await sdk.Vaults.calculateDepositAmount(params)

// Execute deposit
const tx = await sdk.Vaults.deposit(params, tx)
```

### 提取

```typescript
// Calculate withdrawal amounts
const amounts = await sdk.Vaults.calculateWithdrawAmount(params)

// Execute withdrawal
const tx = await sdk.Vaults.withdraw(params, tx)
```

### 持仓锁定

```typescript
// Get vest info for multiple vaults
const vestInfoList = await sdk.Vest.getVaultsVestInfoList([vaultId])

// Get vest info for a single vault
const vestInfo = await sdk.Vest.getVaultsVestInfo(vault_id)

// Get user's vest NFTs
const nfts = await sdk.Vest.getOwnerVaultVestNFT(senderAddress)

// Redeem vested tokens
const payload = await sdk.Vest.buildRedeemPayload(options)
```

---

## Farms SDK

通过质押CLMM持仓来获得额外奖励。

```bash
npm install @cetusprotocol/farms-sdk
```

### 初始化

```typescript
import { CetusFarmsSDK } from '@cetusprotocol/farms-sdk'

const sdk = CetusFarmsSDK.createSDK()
// or: CetusFarmsSDK.createSDK({ env, sui_client })
sdk.setSenderAddress(wallet)
```

### 池查询

```typescript
// Get all farming pools
const pools = await sdk.Farms.getFarmsPoolList()

// Get specific pool
const pool = await sdk.Farms.getFarmsPool(pool_id)

// Get user's position NFTs
const nfts = await sdk.Farms.getOwnedFarmsPositionNFTList(wallet)

// Get specific NFT details
const nft = await sdk.Farms.getFarmsPositionNFT(position_nft_id)
```

### 质押操作

```typescript
// Stake a CLMM position into farm
const payload = await sdk.Farms.depositPayload({ pool_id, clmm_position_id })

// Unstake position from farm
const payload = await sdk.Farms.withdrawPayload({ pool_id, position_nft_id })

// Harvest rewards
const payload = await sdk.Farms.harvestPayload({ pool_id, position_nft_id })

// Batch harvest + collect CLMM fees
const payload = await sdk.Farms.batchHarvestAndClmmFeePayload(farms_list, clmm_list)
```

### 流动性操作（在池内）

```typescript
// Add liquidity with fixed coin amount
const payload = await sdk.Farms.addLiquidityFixCoinPayload(params)

// Remove liquidity
const payload = await sdk.Farms.removeLiquidityPayload(params)

// Claim fees and CLMM rewards
const payload = await sdk.Farms.claimFeeAndClmmReward({ pool_id, position_nft_id })
```

### 错误代码

| 代码 | 描述 |
|------|-------------|
| 1 | CLMM池ID无效 |
| 2 | 持仓NFT无效 |
| ... | ... |
| 15 | 存款金额低于最低限制 |

---

## xCETUS SDK

用于管理平台权益代币（Platform equity token）——将CETUS转换为不可转让的xCETUS，用于治理和奖励分配。

```bash
npm install @cetusprotocol/xcetus-sdk
```

### 初始化

```typescript
import { CetusXcetusSDK } from '@cetusprotocol/xcetus-sdk'

const sdk = CetusXcetusSDK.createSDK({ env: 'mainnet', sui_client })
sdk.setSenderAddress(wallet)
```

### 数据检索

```typescript
// Get user's veNFT (holds xCETUS balance)
const veNFT = await sdk.Xcetus.getOwnerVeNFT()

// Get user's active locks
const locks = await sdk.Xcetus.getOwnerRedeemLockList()

// Get dividend manager info
const dividendMgr = await sdk.Xcetus.getDividendManager()

// Get veNFT dividend info
const dividendInfo = await sdk.Xcetus.getVeNFTDividendInfo()

// Get xCETUS manager (for ratio calculations)
const manager = await sdk.Xcetus.getXcetusManager()
```

### 代币操作

```typescript
// Convert CETUS -> xCETUS (1:1 ratio)
const payload = await sdk.Xcetus.convertPayload(params)

// Start lock-up redemption (xCETUS -> CETUS, time-locked)
const payload = await sdk.Xcetus.redeemLockPayload(params)

// Complete redemption after lock expires
const payload = await sdk.Xcetus.redeemPayload(params)

// Cancel active lock
const payload = await sdk.Xcetus.cancelRedeemPayload(params)

// Claim accumulated dividends
const payload = await sdk.Xcetus.redeemDividendV3Payload(params)
```

### 实用函数

```typescript
// Calculate redeemable CETUS for given lock duration
const amount = sdk.Xcetus.redeemNum(lockDays, xCetusAmount)

// Reverse calculation
const xAmount = sdk.Xcetus.reverseRedeemNum(lockDays, cetusAmount)

// Get historical dividend data
const phaseInfo = await sdk.Xcetus.getPhaseDividendInfo(phase)

// Check lock status
import { XCetusUtil } from '@cetusprotocol/xcetus-sdk'
const isLocked = XCetusUtil.isLocked(lockObj)
```

---

## 限价单SDK

用于放置具有指定价格和到期时间的限价单。

```bash
npm install @cetusprotocol/limit-sdk
```

### 初始化

```typescript
import { CetusLimitSDK } from '@cetusprotocol/limit-sdk'

const sdk = CetusLimitSDK.createSDK()
// or: CetusLimitSDK.createSDK({ env, sui_client })
sdk.setSenderAddress(wallet)
```

### 单据管理

```typescript
// Place a limit order
const payload = await sdk.Limit.placeLimitOrder(params)
// params: coin types, amount, price, expiration

// Cancel running orders
const payload = await sdk.Limit.cancelOrdersByOwner(params)

// Claim completed order proceeds
const payload = await sdk.Limit.claimTargetCoin(params)
```

### 单据查询

```typescript
// Get order details
const order = await sdk.Limit.getLimitOrder(orderId)

// Get all orders for a wallet
const orders = await sdk.Limit.getOwnerLimitOrderList(address)

// Get order operation logs
const logs = await sdk.Limit.getLimitOrderLogs(orderId)

// Get claim logs
const claimLogs = await sdk.Limit.getLimitOrderClaimLogs(orderId)
```

### 池信息

```typescript
// Get supported tokens
const tokens = await sdk.Limit.getLimitOrderTokenList()

// Get available pools
const pools = await sdk.Limit.getLimitOrderPoolList()

// Get specific pool
const pool = await sdk.Limit.getLimitOrderPool(coinA, coinB)

// Get pool indexer ID
const indexerId = await sdk.Limit.getPoolIndexerId(coinA, coinB)
```

### 执行

```typescript
// Execute transaction
await sdk.FullClient.executeTx(keyPair, payload, true)
```

订单状态：`运行中` | `部分完成` | `已完成` | `已取消`

---

## 燃烧SDK

永久锁定流动性持仓，同时继续赚取费用和奖励。

```bash
npm install @cetusprotocol/burn-sdk
```

### 初始化

```typescript
import { CetusBurnSDK } from '@cetusprotocol/burn-sdk'

const sdk = CetusBurnSDK.createSDK()
// or: CetusBurnSDK.createSDK({ env, sui_client })
sdk.setSenderAddress(wallet)
```

### 查询

```typescript
// Get burn pool list
const pools = await sdk.Burn.getBurnPoolList()

// Get burn positions for a pool
const positions = await sdk.Burn.getPoolBurnPositionList(pool_id)

// Get burn positions for an account
const posIds = await sdk.Burn.getBurnPositionList(account_address)

// Get position details
const pos = await sdk.Burn.getBurnPosition(pos_id)
```

### 燃烧操作

```typescript
// Lock liquidity permanently (irreversible!)
const payload = await sdk.Burn.createBurnPayload(params)

// Burn LP v2 (auto-validates, no pool object needed)
const payload = await sdk.Burn.createBurnLPV2Payload(pos_id)
```

### 费用与奖励收集（燃烧后仍可进行）

```typescript
// Collect fees for single position
const payload = await sdk.Burn.createCollectFeePayload(params)

// Collect rewards for single position
const payload = await sdk.Burn.createCollectRewardPayload(params)

// Batch collect fees for multiple positions
const payload = await sdk.Burn.createCollectFeesPayload(params)

// Batch collect rewards for multiple positions
const payload = await sdk.Burn.createCollectRewardsPayload(params)
```

### 持仓锁定

```typescript
// Redeem vested tokens
const payload = await sdk.Burn.redeemVestPayload(params)
// params: versioned_id, vester_id, pool_data, period
```

---

## DCA SDK

美元成本平均（Dollar-Cost Averaging）——自动化的定期代币购买机制。

```bash
npm install @cetusprotocol/dca-sdk
```

### 初始化

```typescript
import { CetusDcaSDK } from '@cetusprotocol/dca-sdk'

const sdk = CetusDcaSDK.createSDK()
// or: CetusDcaSDK.createSDK({ env, sui_client })
sdk.setSenderAddress(wallet)
```

### 单据管理

```typescript
// Create DCA order
const payload = await sdk.Dca.dcaOpenOrderPayload({
  // coin types, total amount, per-cycle amount,
  // cycle frequency, min/max price bounds
})

// Get order details
const order = await sdk.Dca.getDcaOrders(orderId)

// Get order transaction history
const deals = await sdk.Dca.getDcaOrdersMakeDeal(orderId)

// Withdraw from DCA order
const payload = await sdk.Dca.withdrawPayload(params)

// Close one or multiple DCA orders
const payload = await sdk.Dca.dcaCloseOrderPayload(params)
```

### 代币白名单

```typescript
// Get supported tokens
const whitelist = await sdk.Dca.getDcaCoinWhiteList()
```

白名单模式：
| 模式 | 描述 |
|------|-------------|
| 0 | 禁用 |
| 1 | 仅限输入代币 |
| 2 | 仅限输出代币 |
| 3 | 两种代币均可 |

### 执行

```typescript
await sdk.FullClient.sendTransaction(keyPair, payload)
```

---

## Zap SDK

一键式流动性操作——支持灵活的输入方式来添加或移除流动性。

```bash
npm install @cetusprotocol/zap-sdk
```

### 初始化

```typescript
import { CetusZapSDK } from '@cetusprotocol/zap-sdk'

const sdk = CetusZapSDK.createSDK()
// or: CetusZapSDK.createSDK({ env, sui_client, full_rpc_url })
sdk.setSenderAddress(wallet)
```

### 存款（添加流动性）

存款方式：`FixedOneSide` | `FlexibleBoth` | `OnlyCoinA` | `OnlyCoinB`

```typescript
// Pre-calculate deposit amounts
const calcResult = await sdk.Zap.preCalculateDepositAmount({
  pool_id,
  tick_lower,
  tick_upper,
  current_sqrt_price,
  slippage,
  coin_type_a,
  coin_type_b,
  decimals_a,
  decimals_b,
  mode,
  amount_a, // or amount_b depending on mode
})

// Build and execute deposit
const payload = await sdk.Zap.buildDepositPayload({
  ...calcResult,
  // optional: existing position_id to add to
})
```

### 提取（移除流动性）

```typescript
// Pre-calculate withdrawal amounts
const calcResult = await sdk.Zap.preCalculateWithdrawAmount(params)

// Build withdrawal transaction
const payload = await sdk.Zap.buildWithdrawPayload({
  ...calcResult,
  collect_fee: true,    // optionally collect fees
  collect_reward: true, // optionally collect rewards
})
```

---

## Aggregator SDK

多DEX交换聚合器，可优化在Cetus、DeepBook、Kriya、FlowX、Aftermath等平台上的交易。

```bash
npm install @cetusprotocol/aggregator-sdk
```

### 工作流程

```typescript
import { CetusAggregatorSDK } from '@cetusprotocol/aggregator-sdk'

// Step 1: Initialize client
const client = CetusAggregatorSDK.createSDK({
  env: 'mainnet',
  // RPC and package config
})

// Step 2: Find optimal route
const routes = await client.findRouters({
  coinTypeFrom,
  coinTypeTo,
  amount,
})

// Step 3a: Fast swap (simple)
const result = await client.fastRouterSwap({
  routes,
  slippage, // e.g. 0.01 for 1%
  keyPair,
})

// Step 3b: Build PTB transaction (advanced)
const tx = await client.routerSwap({
  routes,
  slippage,
  // manage coin transfers manually
})
```

### 支持的DEX平台

Cetus、DeepBook、Kriya、FlowX、Aftermath、Turbos、Bluefin等。

### 主网合约地址

- **CetusAggregatorV2**：主要聚合器
- **CetusAggregatorV2ExtendV1**：扩展功能
- **CetusAggregatorV2ExtendV2**：扩展功能v2

---

## 共通模式

### SDK初始化（所有包均遵循此模式）

```typescript
// Default mainnet
const sdk = Cetus<Module>SDK.createSDK()

// Custom env
const sdk = Cetus<Module>SDK.createSDK({ env: 'testnet' })

// Custom RPC
const sdk = Cetus<Module>SDK.createSDK({ env: 'mainnet', full_rpc_url: 'YOUR_URL' })

// Custom SuiClient
const sdk = Cetus<Module>SDK.createSDK({ env: 'mainnet', sui_client: yourClient })

// Always set sender before transactions
sdk.setSenderAddress('0x...')

// Update RPC at runtime
sdk.updateFullRpcUrl('NEW_URL')
```

### 交易执行

```typescript
// Using FullClient
await sdk.FullClient.executeTx(keyPair, payload, true)

// Or sendTransaction
await sdk.FullClient.sendTransaction(keyPair, payload)
```

---

## 包引用

| 包名 | npm链接 | 用途 |
|---------|-----|---------|
| common | `@cetusprotocol/common-sdk` | 共享实用工具 |
| clmm | `@cetusprotocol/sui-clmm-sdk` | 集中式流动性做市商 |
| dlmm | `@cetusprotocol/dlmm-sdk` | 动态流动性做市商 |
| vaults | `@cetusprotocol/vaults-sdk` | 自动化仓库管理 |
| farms | `@cetusprotocol/farms-sdk` | 收益 farming |
| xcetus | `@cetusprotocol/xcetus-sdk` | 治理代币（xCETUS） |
| limit | `@cetusprotocol/limit-sdk` | 限价单 |
| burn | `@cetusprotocol/burn-sdk` | 永久锁定流动性 |
| dca | `@cetusprotocol/dca-sdk` | 美元成本平均 |
| zap | `@cetusprotocol/zap-sdk` | 一键式流动性操作 |
| aggregator | `@cetusprotocol/aggregator-sdk` | 多DEX交换路由 |