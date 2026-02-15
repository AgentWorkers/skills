---
name: amped-defi
description: 25款DeFi工具，支持通过SODAX SDK进行跨链交易、桥接以及货币市场操作。可以在链A上供应资产，在链B上借款。兼容的链包括Ethereum、Arbitrum、Base、Optimism、Avalanche、BSC、Polygon、Sonic、LightLink和HyperEVM。
version: 1.0.0
author: Amped Finance
tools:
  # Discovery Tools (7)
  - amped_supported_chains
  - amped_supported_tokens
  - amped_wallet_address
  - amped_money_market_reserves
  - amped_money_market_positions
  - amped_cross_chain_positions
  - amped_user_intents
  # Swap Tools (4)
  - amped_swap_quote
  - amped_swap_execute
  - amped_swap_status
  - amped_swap_cancel
  # Bridge Tools (3)
  - amped_bridge_discover
  - amped_bridge_quote
  - amped_bridge_execute
  # Money Market Tools (6)
  - amped_mm_supply
  - amped_mm_withdraw
  - amped_mm_borrow
  - amped_mm_repay
  - amped_mm_create_supply_intent
  - amped_mm_create_borrow_intent
  # Wallet Management Tools (5)
  - amped_list_wallets
  - amped_add_wallet
  - amped_rename_wallet
  - amped_remove_wallet
  - amped_set_default_wallet
---

# Amped DeFi 技能

## 概述

**Amped DeFi** 技能为代理提供链上 DeFi 操作能力，利用 SODAX SDK 实现跨多个链的无缝 **交易**、**桥接** 以及 **货币市场**（供应/借款/偿还/提取）操作。该技能抽象了跨链意图流、许可处理和策略执行的复杂性，使代理能够安全高效地执行 DeFi 操作。

**主要功能：**
- 通过求解器网络进行跨链和同链代币交易
- 在分支链与 Sonic 中心链之间进行代币桥接
- **跨链货币市场操作**：在一个链上供应，在另一个链上借款！
- 货币市场操作（供应、提取、借款、偿还），并支持头寸跟踪
- 策略执行（消费限额、滑点上限、允许列表）

## 工具分类

### 发现工具

在执行操作之前，使用这些工具来探索支持的链、代币和钱包状态。

| 工具 | 用途 |
|------|---------|
| `amped_supported_chains` | 列出所有支持的分支链（例如：ethernet、arbitrum、sonic） |
| `amped_supported_tokens` | 获取特定模块（交易/桥接/货币市场）在某个链上支持的代币 |
| `amped_wallet_address` | 通过 walletId 解析钱包地址（在执行模式下验证私钥与地址的匹配） |
| `amped_money_market_reserves` | 查看可用的货币市场储备（抵押品/借款市场） |
| `amped_money_market_positions` | 查看用户在单个链上的货币市场头寸 |
| `amped_cross_chain_positions` | **推荐**：查看所有链上的汇总头寸，包括总供应/借款量、健康因子、借款能力、净年化收益率（APY）和风险指标 |
| `amped_user_intents` | 从 SODAX 后端 API 查询用户的交易/桥接意图历史。显示未完成、已完成和已取消的意图及其完整事件详情。 |

**使用建议：** 在尝试任何操作之前，始终先使用发现工具来验证链和代币的支持情况。

### 用户意图历史（SODAX API）

查询 SODAX 后端 API 以获取钱包的完整意图历史：

```
→ amped_user_intents(
    walletId="main",
    status="all",     // "all", "open", or "closed"
    limit=10,         // Number of results (max 100)
    offset=0          // For pagination
  )
← Returns: {
    pagination: { total: 1545, offset: 0, limit: 10, hasMore: true },
    intents: [
      {
        intentHash: "0x5b18d04a545f089e6de59106fa79498cfc0b0274...",
        txHash: "0x1c4a8ded456b97ba9fa2b95ee954ed7e92a40365...",
        chainId: 146,
        blockNumber: 57622027,
        status: "closed",
        createdAt: "2025-12-10T19:44:00.380Z",
        input: { token: "0x654D...", amount: "10000000000000000000", chainId: 1768124270 },
        output: { token: "0x9Ee1...", minAmount: "78684607057391028830", chainId: 5 },
        deadline: "2026-12-10T19:48:32.000Z",
        events: [
          { type: "intent-filled", txHash: "0x7981...", blockNumber: 57622086, ... }
        ]
      }
    ],
    summary: { totalIntents: 1545, returned: 10, openIntents: 3, closedIntents: 1537 }
  }
```

**使用建议：**
- 跟踪待处理交易/桥接操作的状态
- 查看历史意图执行历史
- 调试失败或取消的意图
- 监控求解器的性能和成交率

### 交易工具

通过 SODAX 基于意图的求解器网络进行跨链和同链代币交易。

| 工具 | 用途 |
|------|---------|
| `amped_swap_quote` | 获取包含滑点和费用估算的精确交易报价 |
| `amped_swap_execute` | 执行交易（自动处理许可、批准和执行） |
| `amped_swap_status` | 检查交易或意图的状态 |
| `amped_swap_cancel` | 取消活跃的交易意图（如果支持的话） |

**使用建议：**
- 在同一链上交换不同代币
- 进行跨链交易（例如：在 Ethereum 上交换 USDC 到 Arbitrum 上的 USDT）
- 当需要通过求解器竞争获得更有竞争力的价格时

**不建议使用交易工具的情况：**
- 在不同链之间转移相同代币（请使用桥接工具）
- 进行借款/贷款操作（请使用货币市场工具）

### 桥接工具

通过交易基础设施在链之间桥接代币。

> **注意：** 在 SODAX 中，桥接和跨链交易使用相同的基于意图的消息系统。`amped_bridge_execute` 工具内部会委托给交易基础设施，从而提供更好的路由和可靠性。
>
> **推荐做法：** 直接使用跨链交易（`amped_swap_quote` + `amped_swap_execute`）进行桥接。你可以在一个链上直接将 USDC 交换为另一个链上的原生代币（如 ETH、AVAX、POL 等）。

| 工具 | 用途 |
|------|---------|
| `amped_bridge_discover` | 发现两个链之间可桥接的代币 |
| `amped_bridge_quote` | 检查桥接可行性、限额和最大可桥接金额 |
| `amped_bridge_execute` | 执行桥接（委托给交易基础设施） |

**使用建议：**
- 将代币从一个链转移到另一个链（例如：从 Base 上的 USDC 到 Arbitrum 上的 ETH）
- 在新链上获取原生气体代币（例如：从 USDC 到 Polygon 上的 POL）
- 将资产转移到/从 Sonic 中心链转移

**推荐的气体分配方法：**
```
// Get gas tokens on multiple chains from a single source
→ amped_swap_quote(srcChainId="base", dstChainId="polygon", srcToken="USDC", dstToken="POL", amount="0.5", ...)
→ amped_swap_execute(quote)
// Result: 0.5 USDC on Base → ~4 POL on Polygon
```

### 货币市场工具

使用 **跨链功能**，在 SODAX 货币市场上供应、借款、偿还和提取资产。

| 工具 | 用途 |
|------|---------|
| `amped_mm_supply` | 向货币市场供应代币作为抵押品。支持跨链供应。 |
| `amped_mm_withdraw` | 从货币市场提取供应的代币。支持跨链提取。 |
| `amped_mm_borrow` | 用提供的抵押品借款。**关键功能：可以借款到不同的链！** |
| `amped_mm_repay` | 偿还借款的代币。使用 `-1` 作为金额参数或设置 repayAll=true 以完成偿还。 |
| `amped_mm_create_supply(intent` | [高级] 创建供应意图但不执行（用于自定义流程） |
| `amped_mm_create_borrow(intent` | [高级] 创建借款意图但不执行（支持跨链） |

**跨链货币市场功能：**

SODAX 货币市场支持强大的跨链操作：

1. **跨链借款**（最强大的功能）
   - 在链 A 上供应抵押品（例如：Ethereum）
   - 在链 B 上借款代币（例如：Arbitrum）
   - 抵押品留在链 A 上，但你会在链 B 上收到借款的代币
   - 使用 `dstChainId` 参数指定目标链

2. **跨链供应**
   - 在链 A 上供应代币
   - 抵押品记录在链 B 上（如果不同）
   - 使用 `dstChainId` 参数

**使用货币市场的情况：**
- 通过供应资产赚取收益
- 用现有抵押品借款
- **在不转移抵押品的情况下访问链 B 的流动性**
- 在不同链之间套利利率
- 管理杠杆头寸
- 偿还债务以提高健康因子

**不建议使用货币市场的情况：**
- 简单的代币交换（使用交易工具）
- 在不借款的情况下在不同链之间转移资产（使用桥接工具）

### 钱包管理工具

使用昵称管理多个钱包，便于识别。

| 工具 | 用途 |
|------|---------|
| `amped_list_wallets` | 列出所有配置的钱包及其昵称和地址 |
| `amped_add_wallet` | 使用昵称添加新钱包（支持私钥或 Bankr 钱包） |
| `amped_rename_wallet` | 重命名现有钱包的昵称 |
| `amped_remove_wallet` | 从配置中删除钱包 |
| `amped_set_default_wallet` | 设置默认使用的钱包 |

**使用钱包管理工具的情况：**
- 为不同目的设置多个钱包（交易、持有、测试）
- 用易于记忆的昵称组织钱包
- 在不同操作之间切换钱包
- 管理多个地址的投资组合

## 安全规则

⚠️ **必须遵守这些规则——这些规则由策略引擎执行：**

1. **执行前务必获取报价**
   - 在调用 `amped_swap_quote` 之前，切勿执行交易
   - 在调用 `amped_bridge_quote` 之前，切勿执行桥接
   - 查看报价输出中的滑点和输出金额是否可接受

2. **验证链和代币是否受支持**
   - 在执行操作之前，调用 `amped_supported_chains` 和 `amped_supported_tokens`
   - 不支持的链/代币会返回明确的错误信息

3. **检查滑点是否在可接受范围内**
   - 滑点以 **基点（bps）** 表示：100 bps = 1%
   - 默认最大滑点：100 bps（1%）
   - 滑点超过配置上限的报价将被拒绝
   - 违反策略会返回带有补救建议的结构化错误

4. **切勿尝试耗尽整个钱包余额**
   - 保留足够的余额用于支付气体费用
   - 消费限额按交易和每天进行限制
   - 策略限制：`maxSwapInputUsd`、`maxBridgeAmountToken`、`maxBorrowUsd`

5. **执行后务必验证交易状态**
   - 使用 `amped_swap_status` 跟踪交易完成情况
   - 查看 `amped_money_market_positions` 以验证头寸更新
   - 仅凭交易哈希值不能假设操作成功

6. **遵守允许列表**
   - 仅在对 `allowedChains` 和 `allowedTokensByChain` 中指定的链上进行操作
   - 被阻止的接收者将被拒绝
   - 策略违规会返回带有补救建议的结构化错误

7. **模拟功能默认启用**
   - 除非操作员进行覆盖，否则 `skipSimulation` 为 `false`
   - 模拟可以在广播前捕获可撤销的情况

8. **监控货币市场头寸的健康因子**
   - 健康因子 < 1.0 表示有清算风险
   | 保持健康因子 > 1.5 以确保安全边际
   - 使用 `amped_money_market_positions` 进行监控

## 参数约定

### 金额单位
- **金额以人类可读的单位表示**（例如：“100”表示 100 USDC，“0.5”表示 0.5 ETH）
- SDK 会根据 SODAX 配置中的代币小数位数内部转换为原始单位
- 例如：
  - “1000” USDC（USDC 有 6 位小数）→ 10000000000 原始单位
  - “1.5” ETH（ETH 有 18 位小数）→ 1500000000000000000 原始单位

### 滑点（基点）
- 滑点以 **基点（bps）** 表示，其中 100 bps = 1%
- 常见值：
  - `50` = 0.5%（稳定对）
  - `100` = 1%（标准）
  - `300` = 3%（波动较大的对或跨链）
- 超过配置的 `maxSlippageBps` 的报价将被拒绝

### 链标识符
- 链 ID 是 **字符串标识符**，而不是数字链 ID：
  - “ethereum”（Ethereum 主网）
  - “arbitrum”（Arbitrum One）
  - “sonic”（Sonic 中心链）
  - “base”（Base）
  - “optimism”（Optimism）
  - “avalanche”（Avalanche）
  - “bsc”（BNB 智能链）

### 代币地址
- 代币地址应该是 **校验和地址**（遵循 EIP-55 规范）
- 例如：
  - “0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48”（Ethereum 上的 USDC）
  - “0x4200000000000000000000000000000000000006”（Base 上的 WETH）

### 钱包识别
- 所有执行工具都需要一个 `walletId` 字符串
- 钱包解析通过 ID 进行；私钥永远不会在工具参数中暴露

### 可选参数
- `recipient`：可选的目标地址（默认为钱包地址）
- `timeoutMs`：可选的操作超时（以毫秒为单位）
- `policyId`：可选的策略配置文件选择器，用于自定义限制
- `dstChainId`：**对于跨链货币市场** - 操作的目标链

## 工作流程

### 交易工作流程

执行代币交易的完整工作流程：

```
Step 1: Discovery (if needed)
  → amped_supported_chains
  → amped_supported_tokens(module="swaps", chainId="ethereum")

Step 2: Get Quote
  → amped_swap_quote(
      walletId="main",
      srcChainId="ethereum",
      dstChainId="arbitrum",
      srcToken="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
      dstToken="0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
      amount="1000",
      type="exact_input",
      slippageBps=100
    )
  ← Returns: { quoteId, expectedOutput, slippageBps, fees, deadline }

Step 3: Review Quote
  ✓ Check slippageBps ≤ maxSlippageBps (configurable, default 100)
  ✓ Verify expectedOutput meets requirements
  ✓ Confirm fees are acceptable

Step 4: Execute Swap
  → amped_swap_execute(
      walletId="main",
      quote=<quote from step 2>,
      maxSlippageBps=100,
      skipSimulation=false
    )
  ← Returns: { spokeTxHash, hubTxHash, intentHash, status }

Step 5: Verify Status
  → amped_swap_status(txHash=spokeTxHash)
  ← Returns: { status, confirmations, filledAmount, remainingAmount }

Step 6: Handle Failures (if needed)
  → amped_swap_cancel(walletId="main", intent=<intent>, srcChainId="ethereum")
```

### 桥接工作流程

在链之间桥接代币的完整工作流程：

```
Step 1: Discover Routes
  → amped_bridge_discover(
      srcChainId="ethereum",
      dstChainId="sonic",
      srcToken="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    )
  ← Returns: { bridgeableTokens: [...] }

Step 2: Get Bridge Quote
  → amped_bridge_quote(
      srcChainId="ethereum",
      dstChainId="sonic",
      srcToken="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
      dstToken="0x29219dd400f2bf60e5a23d13be72b486d4038894"
    )
  ← Returns: { isBridgeable: true, maxBridgeableAmount: "1000000" }

Step 3: Review Limits
  ✓ Verify isBridgeable === true
  ✓ Check amount ≤ maxBridgeableAmount
  ✓ Confirm amount within policy limits

Step 4: Execute Bridge
  → amped_bridge_execute(
      walletId="main",
      srcChainId="ethereum",
      dstChainId="sonic",
      srcToken="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
      dstToken="0x29219dd400f2bf60e5a23d13be72b486d4038894",
      amount="5000",
      recipient="0x..." // optional, defaults to wallet
    )
  ← Returns: { spokeTxHash, hubTxHash }
```

### 货币市场供应工作流程

向货币市场供应资产并监控头寸的完整工作流程：

```
Step 1: View Available Markets
  → amped_money_market_reserves(chainId="sonic")
  ← Returns: { reserves: [
      { token: "USDC", supplyAPY: "4.5%", totalSupplied: "..." },
      { token: "WETH", supplyAPY: "2.1%", totalSupplied: "..." }
    ]}

Step 2: Check Current Positions (RECOMMENDED: use cross-chain view)
  → amped_cross_chain_positions(walletId="main")
  ← Returns: { 
      summary: {
        totalSupplyUsd: "15000.00",
        totalBorrowUsd: "5000.00",
        netWorthUsd: "10000.00",
        availableBorrowUsd: "7000.00",
        healthFactor: "2.55",
        healthFactorStatus: { status: "healthy", color: "green" },
        liquidationRisk: "none",
        weightedSupplyApy: "4.25%",
        weightedBorrowApy: "3.50%",
        netApy: "1.08%"
      },
      chainBreakdown: [...],
      collateralUtilization: {...},
      riskMetrics: {...},
      positions: [...],
      recommendations: ["💡 You have $7000.00 in available borrowing power."]
    }

Step 3: Supply Tokens
  → amped_mm_supply(
      walletId="main",
      chainId="sonic",
      token="0x29219dd400f2bf60e5a23d13be72b486d4038894",
      amount="1000",
      useAsCollateral=true  // Use as collateral for borrowing
    )
  ← Returns: { txHash, spokeTxHash, hubTxHash }

Step 4: Verify Position Update (cross-chain view)
  → amped_cross_chain_positions(walletId="main")
  ← Returns: Updated positions reflecting the new supply across all chains
```

### 跨链头寸视图（推荐）

`amped_cross_chain_positions` 工具提供了跨所有链的 **统一投资组合视图**。这是查看货币市场头寸的推荐方式。

**显示内容：**
- **总投资组合概览**：所有链上的供应、借款和净资产
- **健康指标**：健康因子及状态指示器、清算风险水平
- **借款能力**：基于抵押品的可用借款金额
- **收益指标**：加权供应/借款年化收益率（APY）、净年化收益率（APY）
- **链细分**：每个链上的头寸摘要
- **抵押品利用率**：你的抵押品使用了多少
- **风险指标**：当前杠杆率（LTV）、清算前的缓冲区、安全最大借款额
- **个性化建议**：基于你的头寸生成的智能建议

**示例响应：**
```json
{
  "success": true,
  "walletId": "main",
  "address": "0x...",
  "timestamp": "2026-02-02T12:58:27.999Z",
  "summary": {
    "totalSupplyUsd": "25000.00",
    "totalBorrowUsd": "8000.00",
    "netWorthUsd": "17000.00",
    "availableBorrowUsd": "12000.00",
    "healthFactor": "2.65",
    "healthFactorStatus": { "status": "healthy", "color": "green" },
    "liquidationRisk": "none",
    "weightedSupplyApy": "4.52%",
    "weightedBorrowApy": "3.21%",
    "netApy": "2.89%"
  },
  "chainBreakdown": [
    { "chainId": "ethereum", "supplyUsd": "15000.00", "borrowUsd": "5000.00", "healthFactor": "2.80" },
    { "chainId": "arbitrum", "supplyUsd": "5000.00", "borrowUsd": "2000.00", "healthFactor": "2.50" },
    { "chainId": "sonic", "supplyUsd": "5000.00", "borrowUsd": "1000.00", "healthFactor": "5.00" }
  ],
  "collateralUtilization": {
    "totalCollateralUsd": "20000.00",
    "usedCollateralUsd": "8000.00",
    "availableCollateralUsd": "12000.00",
    "utilizationRate": "40.00%"
  },
  "riskMetrics": {
    "maxLtv": "80.00%",
    "currentLtv": "32.00%",
    "bufferUntilLiquidation": "53.00%",
    "safeMaxBorrowUsd": "13600.00"
  },
  "recommendations": [
    "💡 You have $12000.00 in available borrowing power.",
    "🌐 You have positions across 3 chains. Monitor each chain's health factor independently."
  ]
}
```

**使用建议：**
- 始终从这里开始，以获取货币市场头寸的完整视图
- 在进行任何借款/提取操作之前，检查健康因子
- 监控所有链上的投资组合表现
- 识别机会（可用借款能力、利用率低的情况）

### 跨链货币市场借款工作流程（高级）

**关键功能：** 在不同于抵押品供应的链上借款！

```
Scenario: Supply USDC on Ethereum, borrow USDT to Arbitrum

Step 1: Verify Collateral Position on Source Chain
  → amped_money_market_positions(walletId="main", chainId="ethereum")
  ← Returns: { positions: [...], totalCollateralUSD, availableBorrowUSD, healthFactor }

Step 2: Check Borrow Capacity
  ✓ Verify availableBorrowUSD > desired borrow amount
  ✓ Check healthFactor will remain safe after borrow

Step 3: Cross-Chain Borrow
  → amped_mm_borrow(
      walletId="main",
      chainId="ethereum",        // Source chain (where collateral is)
      dstChainId="arbitrum",     // Destination chain (where you receive borrowed tokens)
      token="0xaf88d065e77c8cC2239327C5EDb3A432268e5831",  // USDT on Arbitrum
      amount="500",
      interestRateMode=2         // Variable rate
    )
  ← Returns: { 
      txHash, 
      spokeTxHash,               // On Ethereum (source)
      hubTxHash, 
      dstSpokeTxHash,            // On Arbitrum (destination)
      isCrossChain: true 
    }

Step 4: Verify Position
  → amped_money_market_positions(walletId="main", chainId="ethereum")
  ← Returns: Updated positions with new borrow recorded

Step 5: Verify Received Tokens on Destination Chain
  → amped_wallet_address(walletId="main")
  ← Check USDT balance on Arbitrum via external means or position query
```

### 跨链货币市场供应工作流程

```
Scenario: Supply tokens on Arbitrum, collateral recorded on Sonic

Step 1: Supply with Cross-Chain Flag
  → amped_mm_supply(
      walletId="main",
      chainId="arbitrum",        // Source chain (where tokens are)
      dstChainId="sonic",        // Destination chain (where collateral is recorded)
      token="0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
      amount="1000",
      useAsCollateral=true
    )
  ← Returns: {
      txHash,
      isCrossChain: true,
      message: "Tokens supplied on arbitrum. Collateral available on sonic."
    }

Step 2: Verify on Destination Chain
  → amped_money_market_positions(walletId="main", chainId="sonic")
  ← Returns: Collateral should appear on Sonic
```

### 货币市场偿还工作流程

偿还借款代币的完整工作流程：

```
Step 1: Check Borrow Position
  → amped_money_market_positions(walletId="main", chainId="sonic")
  ← Returns: { positions: [...], totalBorrowUSD, healthFactor }

Step 2: Repay (Full or Partial)
  Option A - Partial Repay:
  → amped_mm_repay(
      walletId="main",
      chainId="sonic",
      token="0x...",
      amount="500"
    )
  
  Option B - Full Repay:
  → amped_mm_repay(
      walletId="main",
      chainId="sonic",
      token="0x...",
      amount="-1",        // Special value for max
      repayAll=true
    )

Step 3: Verify Repayment
  → amped_money_market_positions(walletId="main", chainId="sonic")
  ← Returns: Updated positions with reduced borrow, improved healthFactor
```

### 货币市场提取工作流程

提取供应代币的完整工作流程：

```
Step 1: Check Position and Available Liquidity
  → amped_money_market_positions(walletId="main", chainId="sonic")
  ← Verify: withdrawal won't cause healthFactor to drop below safe level
  ← Verify: sufficient available liquidity in reserve

Step 2: Withdraw
  → amped_mm_withdraw(
      walletId="main",
      chainId="sonic",
      token="0x...",
      amount="500",
      withdrawType="default"  // Options: default, collateral, all
    )
  ← Returns: { txHash, spokeTxHash, hubTxHash }

Step 3: Verify Withdrawal
  → amped_money_market_positions(walletId="main", chainId="sonic")
  ← Returns: Updated positions with reduced supply
```

## 跨链货币市场示例

### 示例 1：在 Ethereum 上供应，在 Base 上借款

```
User: "I have USDC on Ethereum. I want to borrow USDC on Base without moving my collateral."

Agent actions:
1. Check positions on Ethereum
   → amped_money_market_positions(walletId="main", chainId="ethereum")

2. Supply USDC on Ethereum
   → amped_mm_supply(
       walletId="main",
       chainId="ethereum",
       token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
       amount="10000",
       useAsCollateral=true
     )

3. Cross-chain borrow to Base
   → amped_mm_borrow(
       walletId="main",
       chainId="ethereum",        // Collateral is here
       dstChainId="base",         // Receive borrowed tokens here
       token="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  // USDC on Base
       amount="5000",
       interestRateMode=2
     )

4. Verify positions
   → amped_money_market_positions(walletId="main", chainId="ethereum")
   → amped_money_market_positions(walletId="main", chainId="base")
```

### 示例 2：跨链提取

```
User: "I have collateral on Sonic but I want to withdraw to Arbitrum."

Agent actions:
→ amped_mm_withdraw(
    walletId="main",
    chainId="sonic",             // Collateral source
    dstChainId="arbitrum",       // Token destination
    token="0x...",
    amount="1000"
  )
```

## 配置

### 环境变量

| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| `AMPED_OC_MODE` | 操作模式：`execute`（代理签名）或 `prepare`（返回未签名的交易） | `execute` |
| `AMPED_OC_WALLETS_JSON` | 按 walletId 键值对排列的钱包配置 JSON | `{}` |
| `AMPED_oc_RPC_URLS_JSON` | 按 chainId 键值对排列的 RPC URL JSON | `{}` |
| `AMPED_oc_LIMITS_JSON` | 策略限制配置 | `{}` |
| `AMPED_OC_SODAX_DYNAMIC_CONFIG` | 通过 `sodax.initialize()` 启用动态配置 | `false` |

### 钱包配置（`AMPED_oc_WALLETS_JSON`）

```json
{
  "main": {
    "address": "0x...",
    "privateKey": "0x..."  // Required for execute mode
  },
  "trading": {
    "address": "0x...",
    "privateKey": "0x..."
  }
}
```

**安全说明：** 私钥永远不会被记录。在准备模式下，只需要提供地址。**

### 策略限制（`AMPED_oc_LIMITS_JSON`）

```json
{
  "maxSwapInputUsd": 10000,
  "maxBridgeAmountToken": {
    "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48": 50000
  },
  "maxBorrowUsd": 5000,
  "maxSlippageBps": 100,
  "allowedChains": ["ethereum", "arbitrum", "sonic", "base"],
  "allowedTokensByChain": {
    "ethereum": ["0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "0x..."]
  },
  "blockedRecipients": ["0x..."]
}
```

### RPC 配置（`AMPED_oc_RPC_URLS_JSON`）

```json
{
  "ethereum": "https://eth-mainnet.g.alchemy.com/v2/...",
  "arbitrum": "https://arb-mainnet.g.alchemy.com/v2/...",
  "base": "https://base-mainnet.g.alchemy.com/v2/...",
  "sonic": "https://rpc.soniclabs.com"
}
```

## 错误处理

### 策略违规

策略违规会返回结构化错误，包含：
- `code`：错误代码（例如：`POLICY_SLIPPAGE_EXCEEDED`）
- `message`：人类可读的描述
- `remediation`：建议的解决方法
- `current`：违反策略的当前值
- `limit`：配置的限制

### 常见错误代码

| Code | 描述 | 解决方法 |
|------|-------------|-------------|
| `POLICY_SLIPPAGE_EXCEEDED` | 报价滑点超过 maxSlippageBps | 增加 maxSlippageBps 或等待更好的条件 |
| `POLICY_SPEND_LIMIT_EXCEEDED` | 金额超过单次交易或每日限制 | 减少金额或请求增加限制 |
| `POLICY_chain_NOT_ALLOWED` | 链不在 allowedChains 中 | 将链添加到 allowedChains 或使用不同的链 |
| `POLICY_TOKEN_NOT_ALLOWED` | 代币不在 allowedTokensByChain 中 | 将代币添加到允许列表或使用不同的代币 |
| `INSUFFICIENT_BALANCE` | 钱包余额不足 | 减少金额或补充钱包余额 |
| `INSUFFICIENT_ALLOWANCE` | 代币许可不足 | 工具将自动批准，或手动批准 |
| `QUOTE_EXPIRED` | 报价截止时间已过 | 获取新的报价 |
| BRIDGE_NOT_AVAILABLE` | 代币对无法桥接 | 使用不同的代币或不同的路径进行交易 |
| MM_HEALTH_FACTOR_LOW` | 操作会导致清算风险 | 先偿还债务或增加抵押品 |
| MM_CROSSCHAIN_NOT_SUPPORTED` | 该对不支持跨链操作 | 使用相同链的操作或不同的代币/链 |

## 幂等性和重试

### 客户端操作 ID

执行工具接受一个可选的 `clientOperationId` 参数以实现幂等性：
- 在缓存窗口内，具有相同 ID 的重复操作将返回缓存的结果
- 防止重复广播
- 推荐用于自动化工作流程

### 重试指南

- **读取操作**（报价、状态、头寸）：可以使用指数退避策略安全地重试
- **写入操作**（执行、供应、借款）：使用 `clientOperationId` 以防止重复
- **超时处理**：桥接和货币市场操作需要指定超时；遵循 SDK 的默认设置

## 安全模型

### 关键隔离

- 每个代理的工作空间都有独立的钱包配置
- 分支提供者按 `walletId` 进行缓存，不会在代理之间共享
- 私钥仅通过 `walletId` 进行解析；永远不会作为参数传递

### 执行模式与准备模式

| 模式 | 签名 | 使用场景 |
|------|---------|----------|
| `execute` | 代理使用私钥签名 | 自动化代理、服务器端操作 |
| `prepare` | 返回未签名的交易以供外部签名 | 硬件钱包、隔离签名、多签名 |

### 日志记录

结构化日志包括：
- `requestId`：唯一请求标识符
- `agentId`：代理标识符（如果可用）
- `walletId`：钱包标识符
- `opType`：操作类型（交易、桥接、供应等）
- `chainIds`、`tokenAddresses`：操作上下文
- `txHashes`：交易哈希（用于追踪）

**永远不会记录：** 私钥、完整的钱包 JSON、敏感配置

## 链特定说明

### Sonic 中心链

- Sonic 是 SODAX 操作的 **中心链**
- 使用 `SonicSpokeProvider` 而不是 `EvmSpokeProvider`
- 对中心链的操作需要特殊处理
- 货币市场操作以中心链为中心，但支持跨链交互

### EVM 分支链

- 对于标准的 EVM 链（Ethereum、Arbitrum、Base 等），使用 `EvmSpokeProvider`
- 应用标准的许可/批准流程
- 桥接操作流程：分支链 → 中心链 → 目标分支链
- 跨链货币市场操作利用中心链进行状态管理

## 跨链货币市场架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    SODAX Money Market Flow                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Cross-Chain Borrow Example:                                     │
│  Supply USDC on Ethereum → Borrow USDT on Arbitrum              │
│                                                                  │
│  ┌─────────────┐         ┌─────────┐         ┌─────────────┐   │
│  │  Ethereum   │ ──────► │  Sonic  │ ──────► │  Arbitrum   │   │
│  │  (Supply)   │         │  (Hub)  │         │  (Borrow)   │   │
│  └─────────────┘         └─────────┘         └─────────────┘   │
│        │                      │                     │           │
│        │  1. Supply USDC      │                     │           │
│        │  2. Record collateral│                     │           │
│        │─────────────────────►│                     │           │
│        │                      │  3. Verify collateral│           │
│        │                      │  4. Process borrow   │           │
│        │                      │────────────────────►│           │
│        │                      │                     │ 5. Deliver│
│        │                      │                     │    USDT   │
│        │                      │                     │           │
│                                                                  │
│  Key Insight: Your collateral stays on the source chain,         │
│  but you receive borrowed tokens on the destination chain!       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 示例

### 示例 1：简单的同链交易

```
User: "Swap 100 USDC for ETH on Ethereum"

Agent actions:
1. amped_swap_quote(
     walletId="main",
     srcChainId="ethereum",
     dstChainId="ethereum",
     srcToken="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
     dstToken="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
     amount="100",
     type="exact_input",
     slippageBps=100
   )
2. Review quote (slippage 0.8%, expected output 0.042 ETH)
3. amped_swap_execute(walletId="main", quote=<quote>, maxSlippageBps=100)
4. amped_swap_status(txHash=<spokeTxHash>)
```

### 示例 2：跨链桥接

```
User: "Bridge 1000 USDC from Ethereum to Sonic"

Agent actions:
1. amped_bridge_discover(srcChainId="ethereum", dstChainId="sonic", srcToken="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
2. amped_bridge_quote(srcChainId="ethereum", dstChainId="sonic", srcToken="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", dstToken="0x29219dd400f2bf60e5a23d13be72b486d4038894")
3. amped_bridge_execute(walletId="main", srcChainId="ethereum", dstChainId="sonic", srcToken="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", dstToken="0x29219dd400f2bf60e5a23d13be72b486d4038894", amount="1000")
```

### 示例 3：同一链上的供应和借款循环

```
User: "Supply 5000 USDC and borrow 2000 USDT on Sonic"

Agent actions:
1. amped_money_market_reserves(chainId="sonic")
2. amped_mm_supply(walletId="main", chainId="sonic", token="0x29219dd400f2bf60e5a23d13be72b486d4038894", amount="5000")
3. amped_money_market_positions(walletId="main", chainId="sonic")
4. amped_mm_borrow(walletId="main", chainId="sonic", token="0x...usdt...", amount="2000")
5. amped_money_market_positions(walletId="main", chainId="sonic") // Verify new health factor
```

### 示例 4：跨链货币市场（高级）

```
User: "I want to use my USDC on Ethereum as collateral to borrow USDC on Arbitrum for a trading opportunity"

Agent actions:
1. Verify supported chains and tokens
   → amped_supported_tokens(module="moneyMarket", chainId="ethereum")
   → amped_supported_tokens(module="moneyMarket", chainId="arbitrum")

2. Check current positions
   → amped_money_market_positions(walletId="main", chainId="ethereum")
   → amped_money_market_positions(walletId="main", chainId="arbitrum")

3. Supply USDC on Ethereum
   → amped_mm_supply(
       walletId="main",
       chainId="ethereum",
       token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
       amount="50000",
       useAsCollateral=true
     )

4. Cross-chain borrow to Arbitrum
   → amped_mm_borrow(
       walletId="main",
       chainId="ethereum",        // Source: collateral is here
       dstChainId="arbitrum",     // Destination: receive tokens here
       token="0xaf88d065e77c8cC2239327C5EDb3A432268e5831",  // USDC on Arbitrum
       amount="20000",
       interestRateMode=2
     )

5. Verify the cross-chain borrow worked
   → Check positions on Ethereum (collateral + debt recorded)
   → Check USDC balance on Arbitrum (borrowed tokens received)

Result: User has 20k USDC on Arbitrum to trade with, while their 50k USDC collateral remains on Ethereum!
```

## 交易执行架构

### SODAX-First 路由（强制要求）

**重要提示：** 所有 DeFi 操作必须首先通过 SODAX SDK 路由。外部钱包后端（如 Bankr）仅用于交易执行——从不用于路由决策。

```
┌─────────────────────────────────────────────────────────────────┐
│                  SODAX SDK (Routing Layer)                      │
│  ✓ Calculates optimal swap routes                               │
│  ✓ Determines bridge paths                                      │
│  ✓ Manages money market intents                                 │
│  ✓ Handles slippage, fees, deadlines                            │
│  ✓ Prepares transaction data (to, data, value)                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼ raw transaction data
┌─────────────────────────────────────────────────────────────────┐
│           Wallet Backend (Execution Layer ONLY)                 │
│  ✓ Signs the pre-computed transaction                           │
│  ✓ Submits to blockchain                                        │
│  ✓ Returns transaction hash                                     │
│  ✗ NO routing decisions                                         │
│  ✗ NO token swapping logic                                      │
│  ✗ NO DeFi protocol selection                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 支持的后端

| 后端 | 描述 | 使用场景 |
|---------|-------------|----------|
| `localKey` | 通过 `~/.evm-wallet.json` 或配置文件直接使用私钥签名 | 默认，自我托管 |
| `bankr` | 使用 Bankr API 提交交易 | 通过 Bankr 管理钱包 |

### 后端选择

钱包后端的選擇方式如下：
1. `config.json` → `walletBackend: "bankr" | "localKey"`
2. 环境设置：`AMPED_OC_WALLET_BACKEND`
3. 默认值：`localKey`

### Bankr 集成

当配置 `walletBackend: "bankr"` 时：

1. **SODAX SDK 准备交易** - 所有路由、计算和意图创建都在 SODAX 中完成
2. **交易数据传递给 Bankr** - 仅发送原始的 `{to, data, value, chainId}` 数据
3. **Bankr 签署并提交** - Bankr 按照 SODAX 的准备内容执行交易
4. **Bankr 不进行路由** - Bankr 不会解释或重新路由交易

这确保了：
- 所有后端的行为一致
- 始终应用 SODAX 的优化
- 审计跟踪显示 SODAX 为路由权威
- 后端仅负责执行

### 配置示例（Bankr）

```json
// ~/.openclaw/extensions/amped-defi/config.json
{
  "walletBackend": "bankr",
  "bankrApiKey": "bk_...",
  "bankrApiUrl": "https://api.bankr.bot",
  "bankrWalletAddress": "0x..."
}
```

**安全说明：** Bankr API 密钥存储在本地，永远不会在工具参数或日志中暴露。