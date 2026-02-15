---
name: setup-dca
description: >-
  Set up a non-custodial dollar-cost averaging strategy on Uniswap. Use when
  user wants to create recurring swaps, auto-buy ETH/BTC/SOL with USDC on a
  schedule, or build a DCA bot. Covers USDC approval, swap path selection,
  frequency configuration, Gelato keeper automation, and monitoring. Works on
  local testnet for development or mainnet for production.
model: opus
allowed-tools:
  - Task(subagent_type:trade-executor)
  - mcp__uniswap__execute_swap
  - mcp__uniswap__get_quote
  - mcp__uniswap__get_token_price
  - mcp__uniswap__get_agent_balance
  - mcp__uniswap__get_pools_by_token_pair
  - mcp__uniswap__check_safety_status
---

# 设置自动定投（DCA）策略

## 概述

该功能用于在 Uniswap 上设置完整的非托管式自动定投策略。无需手动执行交易、监控价格、寻找最优交易路径或管理审批流程，只需通过一条命令即可完成整个 DCA 策略的配置：验证策略、选择最佳交易路径、设置执行频率、处理 Permit2 审批、执行首次交易，并设置后续的自动化操作。

**为什么这比手动操作好十倍：**

1. **最优路径选择**：自动发现适用于您的代币对的所有 Uniswap 池版本和费用等级中的最佳交易路径。手动定投往往使用次优路径，每次交易会因不必要的滑点损失 0.1-0.5% 的费用。
2. **审批管理**：正确处理 Permit2 审批流程——这是导致 DCA 执行失败的一个常见原因。一次设置即可覆盖未来的所有交易。
3. **两种自动化模式**：自执行模式（由代理触发交易）适用于开发和测试；Gelato 保持器模式（链上自动化）适用于无需信任的环境。如果没有此功能，设置 Gelato 保持器需要了解任务创建、解析器合约和费用支付的相关知识。
4. **内置安全机制**：每次交易都会经过安全检查，包括滑点防护、余额验证和断路器保护。手动定投没有这些安全机制——配置错误的机器人可能会因一次错误交易而耗尽钱包资金。
5. **成本预测**：在执行前会显示包括 gas 费用、滑点和保持器费用在内的总成本预测，避免意外支出。

## 适用场景

当用户提出以下需求时，可以使用此功能：
- “在 Uniswap 上设置自动定投”
- “创建定期交易”
- “每周用 USDC 自动购买 ETH”
- “构建自动定投机器人”
- “每天用 100 美元自动购买 ETH”
- “每周购买 WBTC”
- “在未来 3 个月内积累 UNI”
- “安排定期从 USDC 到 ETH 的交易”

**不适用场景**：
- 用户仅需要执行一次性交易（请使用 `execute-swap`）；
- 用户需要管理现有的 DCA 策略（目前不支持，需取消并重新创建）；
- 用户希望将资金投入 LP 位置（请使用 `full-lp-workflow`）。

## 参数

| 参数                | 是否必填 | 默认值       | 获取方式                                                                                   |
|------------------|--------|------------|-----------------------------------------------------------------------------------------|
| targetAsset           | 是       | --          | 需要积累的代币：“ETH”、“WBTC”、“UNI”、“SOL” 或 0x 地址                                      |
| amountPerExecution    | 是       | --          | 每次交易的金额：“100 美元”、“100 USDC” 或 “相当于 0.1 ETH 的价值”                         |
| inputToken          | 否       | USDC         | 需要支付的代币：“USDC”、“USDT”、“DAI”、“WETH”                                      |
| frequency           | 否       | weekly       | 执行频率：“daily”、“weekly”、“biweekly”、“monthly”                                        |
| totalExecutions      | 否       | --          | 执行次数：“52 周”、“12 个月” 或 “无限期”                                        |
| chain              | 否       | ethereum     | 目标链：“ethereum”、“base”、“arbitrum”                                      |
| slippageTolerance     | 否       | 50 (0.5%)      | 每次交易的最大滑点百分比（以基点计）                                        |
| keeperMode           | 否       | self-execute    | “self-execute”（代理触发）或 “gelato”（链上自动化）                                    |
| startImmediately       | 否       | true         | 是否立即执行首次交易                                                          |

如果用户未提供 `amountPerExecution` 或 `targetAsset`，**请询问用户这些信息**——切勿自行猜测 DCA 策略的参数。

## 工作流程

```
                           DCA SETUP PIPELINE
  ┌──────────────────────────────────────────────────────────────────────┐
  │                                                                      │
  │  Step 1: VALIDATE & ANALYZE                                          │
  │  ├── Check wallet balance (enough for at least 3 executions)         │
  │  ├── Verify target asset exists on chain                             │
  │  ├── Get current price of target asset                               │
  │  └── Output: Balance check + current price baseline                  │
  │          │                                                           │
  │          ▼                                                           │
  │                                                                      │
  │  Step 2: FIND OPTIMAL SWAP PATH                                      │
  │  ├── Discover all pools for inputToken/targetAsset                   │
  │  ├── Get quotes across fee tiers at DCA amount                       │
  │  ├── Select path with lowest price impact at execution size          │
  │  └── Output: Best route + expected slippage per execution            │
  │          │                                                           │
  │          ▼                                                           │
  │                                                                      │
  │  Step 3: COST PROJECTION                                             │
  │  ├── Estimate gas cost per execution                                 │
  │  ├── Calculate total cost over full DCA period                       │
  │  ├── Project keeper fees (if Gelato mode)                            │
  │  ├── Compare DCA vs lump-sum at current price                        │
  │  └── Output: Full cost breakdown + projection                        │
  │          │                                                           │
  │          ▼                                                           │
  │                                                                      │
  │  Step 4: USER CONFIRMATION                                           │
  │  ├── Present: strategy summary + cost projection                     │
  │  ├── Ask: "Proceed with this DCA strategy?"                          │
  │  └── User must explicitly confirm                                    │
  │          │                                                           │
  │          ▼                                                           │
  │                                                                      │
  │  Step 5: CONFIGURE & EXECUTE                                         │
  │  ├── Check/set Permit2 approval for inputToken                       │
  │  ├── If startImmediately: execute first swap via trade-executor      │
  │  ├── If gelato: create Gelato task with resolver + fund keeper       │
  │  ├── If self-execute: write DCA config to .uniswap/dca-config.json  │
  │  └── Output: Configuration + first execution result                  │
  │          │                                                           │
  │          ▼                                                           │
  │                                                                      │
  │  Step 6: MONITORING SETUP                                            │
  │  ├── Record baseline: price, balance, execution count                │
  │  ├── Set up execution tracking                                       │
  │  └── Output: DCA dashboard with next execution time                  │
  │                                                                      │
  └──────────────────────────────────────────────────────────────────────┘
```

### 第 1 步：验证与分析

在确认执行策略之前，请检查以下前提条件：
1. 调用 `mcp__uniswap__get_agent_balance` 以验证钱包中有足够的 `inputToken` 余额（至少足够进行 3 次交易）。
2. 调用 `mcp__uniswap__get_token_price` 获取 `targetAsset` 的价格基准。
3. 调用 `mcp__uniswap__check_safety_status` 以确认支出限额是否满足 DCA 的需求。

**向用户展示结果：**

```text
Step 1/6: Validation

  Wallet Balance: 5,200 USDC on Ethereum
  DCA Budget:     $100/week x 52 weeks = $5,200 total
  Balance Check:  PASS (covers full DCA period)

  Target Asset:   ETH at $1,960.00
  Per Execution:  ~0.051 ETH per $100

  Proceeding to path selection...
```

**检查提示：** 如果钱包余额不足以支持 3 次交易，请警告用户并询问是否希望缩短 DCA 周期。

### 第 2 步：寻找最优交易路径

1. 调用 `mcp__uniswap__get_pools_by_token_pair` 获取目标链上 `inputToken`/`targetAsset` 对应的池信息。
2. 调用 `mcp__uniswap__get_quote` 获取 `amountPerExecution` 数量下前 2-3 个池的价格信息，以便比较交易成本。
3. 选择交易成本最低的路径。

**向用户展示结果：**

```text
Step 2/6: Path Selection

  Best Route: USDC -> WETH via 0.05% pool (V3, Ethereum)
  Pool TVL:   $285M
  Impact:     ~0.01% per $100 execution
  Alternative: 0.3% pool (0.02% impact -- slightly worse)

  Proceeding to cost projection...
```

### 第 3 步：成本预测

计算 DCA 策略的总成本：

```text
Step 3/6: Cost Projection

  DCA Strategy: $100 USDC -> ETH weekly for 52 weeks

  Per Execution:
    Swap Amount:   $100.00
    Est. Slippage: ~$0.01 (0.01%)
    Gas Cost:      ~$2.50 (at current gas)
    Net Purchase:  ~$97.49 of ETH

  Full Period (52 weeks):
    Total Spent:   $5,200.00
    Est. Gas:      ~$130.00 (2.5%)
    Est. Slippage: ~$0.52 (0.01%)
    Net Invested:  ~$5,069.48

  At Current Price ($1,960/ETH):
    Lump Sum Now:  2.653 ETH for $5,200
    DCA Estimate:  ~2.587 ETH (varies with price)

  Ready for your confirmation...
```

### 第 4 步：用户确认

向用户展示完整的策略摘要，并请求明确确认：

```text
DCA Strategy Confirmation

  Buy:        ETH with USDC
  Amount:     $100 per execution
  Frequency:  Weekly (every 7 days)
  Duration:   52 executions
  Chain:      Ethereum
  Route:      USDC/WETH 0.05% (V3)
  Slippage:   0.5% max
  Mode:       Self-execute (agent-triggered)
  Start:      Immediately (first swap now)
  Total Cost: ~$5,200 + ~$130 gas

  Proceed with this DCA strategy? (yes/no)
```

**只有在用户明确确认后，才能进入第 5 步。**

### 第 5 步：配置与执行

将首次交易委托给 `Task(subagent_type:trade-executor)`：

```
Execute this swap as the first DCA execution:
- Sell: {amountPerExecution} {inputToken}
- Buy: {targetAsset}
- Chain: {chain}
- Slippage tolerance: {slippageTolerance} bps
- Context: This is execution 1 of {totalExecutions} in a DCA strategy.
  Route through the {fee}% pool for optimal execution at this size.
```

执行完成后，保存 DCA 配置文件：

**对于自执行模式**，将配置文件保存为 `.uniswap/dca-config.json`：

```json
{
  "strategy": "dca",
  "inputToken": "USDC",
  "targetAsset": "WETH",
  "amountPerExecution": "100000000",
  "frequency": "weekly",
  "nextExecution": "2026-02-17T00:00:00Z",
  "totalExecutions": 52,
  "completedExecutions": 1,
  "chain": "ethereum",
  "chainId": 1,
  "route": {
    "pool": "0x...",
    "fee": 500,
    "version": "v3"
  },
  "slippageTolerance": 50,
  "status": "active",
  "createdAt": "2026-02-10T00:00:00Z",
  "executionHistory": []
}
```

**对于 Gelato 模式**，创建一个 Gelato 自动化任务，包括：
- 解析器：检查 `block.timestamp` 是否大于下次执行时间；
- 执行器：通过 Universal Router 使用配置的路径执行交易；
- 用 ETH 为保持器支付费用。

### 第 6 步：监控与设置

```text
Step 6/6: DCA Active

  First Execution:
    Sold:     100 USDC
    Received: 0.0510 WETH ($99.96)
    Gas:      $2.30
    Tx:       https://etherscan.io/tx/0x...

  Schedule:
    Next:     2026-02-17 (7 days)
    Remaining: 51 executions
    Mode:     Self-execute

  Config: .uniswap/dca-config.json
```

## 输出格式

### 设置成功

```text
DCA Strategy Active

  Strategy:
    Buy:        ETH with USDC
    Amount:     $100 per execution
    Frequency:  Weekly
    Duration:   52 executions (~1 year)
    Chain:      Ethereum
    Route:      USDC/WETH 0.05% (V3)
    Mode:       Self-execute

  First Execution:
    Sold:       100 USDC
    Received:   0.0510 WETH ($99.96)
    Slippage:   0.04%
    Gas:        $2.30
    Tx:         https://etherscan.io/tx/0x...

  Projections:
    Total Budget:    $5,200 + ~$130 gas
    Est. ETH:        ~2.59 ETH (at current prices)
    Next Execution:  2026-02-17

  Config: .uniswap/dca-config.json
  Status: ACTIVE -- 1/52 executions complete
```

### 未立即执行的设置

```text
DCA Strategy Configured (Not Started)

  Strategy:
    Buy:        ETH with USDC
    Amount:     $100 per execution
    Frequency:  Weekly
    Chain:      Ethereum
    Route:      USDC/WETH 0.05% (V3)
    Mode:       Self-execute

  First Execution: 2026-02-17 (scheduled)
  Config: .uniswap/dca-config.json
  Status: CONFIGURED -- awaiting first execution
```

## 重要说明

- **DCA 是一种长期策略。** 该功能仅设置配置，首次交易可选项由用户选择是否执行。后续交易取决于保持器模式：自执行模式需要代理运行；Gelato 模式则完全在链上自动执行。
- **自执行模式需要代理在线。** 如果代理在交易执行时离线，交易将推迟到下次执行。Gelato 模式完全自动化，无需代理。
- **对于小额 DCA，gas 费用很重要。** 在以太坊主网上，每次交易的 gas 费用约为 2-5 美元，因此每周 100 美元的 DCA 策略可能因 gas 而损失 20-50% 的费用。如果 gas 费用超过交易金额的 5%，系统会发出警告，并建议使用 Base 或 Arbitrum 进行交易。
- **DCA 的滑点通常可以忽略不计。** DCA 的交易金额相对于池的总价值（TVL）来说通常较小，因此价格影响很小。尽管如此，系统仍会强制执行滑点容忍度作为安全措施。
- **DCA 配置文件是核心依据。** `.uniswap/dca-config.json` 文件记录了交易历史、下次执行时间和策略参数。删除该文件将取消 DCA 策略。
- **要取消 DCA，需删除配置文件或将 `status` 设置为 “cancelled”。对于 Gelato 模式，还需在链上取消相应的自动化任务。
- **对于小额 DCA，建议使用 L2 链。** Base 和 Arbitrum 的 gas 费用比以太坊主网低 10-100 倍，适合小额定投策略。

## 错误处理

| 错误类型                | 向用户显示的提示              | 建议的操作                                      |
|------------------|----------------------------------|-----------------------------------------------------|
| 账户余额不足             | “钱包中有 {X} {inputToken}，但 DCA 需要至少 {Y} 来完成 3 次交易。”        | 为钱包充值或减少每次交易的金额                          |
| 未找到目标资产             | “在 {chain} 上未找到 {targetAsset}。”                          | 检查拼写或提供合约地址                            |
| 未找到交易池             | “在 {chain} 上未找到 {inputToken}/{targetAsset} 的交易池。”         | 尝试其他链或代币对                              |
| Gas 费用过高             | “Gas 费用（约 ${X}）超过了交易金额的 5%（{Y}）。建议使用 Base 链。”        | 更换到成本更低的 L2 链                          |
| 安全检查失败             | “该 DCA 策略会超出安全限制。”                          | 调整支出限额或减少交易金额                          |
| 审批失败             | “无法批准 {inputToken} 的 Permit2 请求：{原因}。”                   | 检查钱包权限并重试                              |
| 首次交易失败             | “首次 DCA 执行失败：{原因}。策略已配置但未启动。”                     | 解决问题并手动触发首次交易                          |
| Gelato 设置失败             | “无法创建 Gelato 自动化任务：{原因}。”                         | 使用自执行模式                              |
| 配置文件写入失败             | “无法写入 DCA 配置文件：{原因}。”                         | 检查文件权限                              |
| 未配置钱包             | “未配置钱包。无法执行 DCA。”                          | 使用 `setup-agent-wallet` 功能配置钱包                    |
| 超出支出限额             | “DCA 总金额（{X}）超过了每日支出限额（{Y}。”                     | 调整支出限额或减少交易频率/金额                          |