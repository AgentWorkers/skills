---
name: manage-liquidity
description: 在 Uniswap V2/V3/V4 的交易池中，可以添加流动性、移除流动性，或者收取费用。该功能涵盖了整个流程，包括交易池的选择、参数优化、审批流程、安全检查以及交易执行。适用于用户希望参与流动性提供（LP）、移除已持有的头寸（position），或收取累计费用的情况。
model: opus
allowed-tools: [Task(subagent_type:liquidity-manager), Task(subagent_type:pool-researcher), mcp__uniswap__get_positions_by_owner, mcp__uniswap__get_position, mcp__uniswap__check_safety_status]
---

# 管理流动性

## 概述

这是Uniswap上所有流动性操作的核心功能。它主要处理三种操作：

1. **添加流动性**：寻找最佳的流动性池，推荐合适的范围，处理用户确认流程，并将代币存入池中。
2. **移除流动性**：从现有持仓中提取代币（部分或全部）。
3. **收取费用**：从持仓中提取累积的交易费用。

每种操作都会委托给`liquidity-manager`代理执行，用户可以选择是否使用`pool-researcher`代理来辅助选择更合适的流动性池。该功能会解析用户的意图，验证参数，并协调相应的代理流程。

## 使用场景

当用户提及与提供、移除或管理Uniswap流动性相关的操作时，应激活此功能：

**添加流动性：**
- “为ETH/USDC添加流动性”
- “在Base平台上为WETH/USDC提供流动性”
- “将代币加入ETH/USDC的最佳流动性池”
- “开设UNI/WETH的持仓”
- “我想向ETH/USDC的流动性池中投入5000美元”
- “将代币存入费用率为0.05%的流动性池”
- “向我的WETH/USDC持仓中投入1万美元”

**移除流动性：**
- “移除我的流动性”
- “关闭我的ETH/USDC持仓”
- “从持仓#12345中提取50%的代币”
- “退出我的流动性持仓”

**收取费用：**
- “收取我的交易费用”
- “从持仓#12345中提取累积的费用”
- “我赚了多少钱？”（先查询费用金额，再询问用户是否需要收取）

## 参数

### 添加流动性时的参数

| 参数          | 是否必填 | 默认值 | 提取方式                                      |
|---------------|--------|---------|-------------------------------------------|
| action         | 是      | —        | 对于此子流程，始终使用“add”                    |
| token0         | 是      | —        | 第一种代币（例如：ETH、WETH、USDC或0x地址）                   |
| token1         | 是      | —        | 第二种代币                                      |
| amount         | 是      | —        | 金额（美元：“$5000”），代币数量（“2.5 ETH”）或同时指定           |
| chain          | 否      | ethereum    | “ethereum”、“base”、“arbitrum”、“optimism”、“polygon”           |
| version        | 否      | v3        | “v2”（被动模式），“v3”（主动管理模式），“v4”（高级管理模式）         |
| range         | 否      | medium      | “narrow”（±5%）、“medium”（±15%）、“wide”（±50%）、“full”（±∞）        |
| feeTier        | 否      | 自动检测    | “0.01%”、“0.05%”、“0.3%”或bps：100、500、3000、10000           |

### 移除流动性/收取费用时的参数

| 参数          | 是否必填 | 默认值 | 提取方式                                      |
|---------------|--------|----------|-------------------------------------------------------|
| action         | 是      | —        | “remove”或“collect”                                  |
| positionId      | 是*     | —        | NFT代币ID（例如：“position #12345”）或通过搜索获取         |
| chain          | 否      | ethereum    | 持仓所在的链                         |
| percentage     | 否      | 100       | “50%”、“all”、“half”（仅用于移除操作）                   |
| collectFees     | 是      | true       | 是否在移除时同时收取费用                         |

*如果用户未提供持仓ID（例如：“移除我的ETH/USDC持仓”），则使用`get_positions_by_owner`函数进行搜索，并在继续操作前确认用户信息。*

## 工作流程

### 添加流动性流程
```
Step 1: PARSE INTENT
├── Extract: tokens, amount, chain, version, range, fee tier
├── Normalize: "ETH" → "WETH", "$5K" → "$5000"
└── If any required params missing → ASK the user (don't guess)

Step 2: POOL SELECTION (if user didn't specify exact pool)
├── If "best pool" or no fee tier specified:
│   └── Delegate to pool-researcher: "Find the best pool for {token0}/{token1} on {chain}"
│       Pool researcher returns ranked pools with APY, TVL, depth
│       Pick the recommended pool (or present top 3 if user wants to choose)
└── If specific pool given: use directly

Step 3: PRE-FLIGHT CHECKS
├── Check safety status via check_safety_status
├── Verify wallet has sufficient token balances
└── If checks fail → STOP and tell user what's wrong

Step 4: DELEGATE TO LIQUIDITY-MANAGER
├── Pass: token0, token1, amount, chain, version, range, feeTier, pool address
├── The liquidity-manager agent handles:
│   a. Check and execute token approvals (Permit2)
│   b. Calculate optimal tick range based on range strategy
│   c. Simulate the add-liquidity transaction
│   d. Route through safety-guardian for validation
│   e. Execute the transaction
│   f. Wait for confirmation
└── Returns: positionId, amounts deposited, tick range, tx hash

Step 5: PRESENT RESULT
├── Position ID (NFT token ID)
├── Tokens deposited with USD values
├── Price range (lower price, upper price, current price)
├── Estimated fee APY (from pool-researcher data)
├── Explorer link to the transaction
└── Tip: "Monitor with /track-performance"
```

### 移除流动性流程
```
Step 1: IDENTIFY POSITION
├── If position ID given → use directly
├── If "my ETH/USDC position" → call get_positions_by_owner
│   ├── Filter by token pair and chain
│   ├── If multiple matches → LIST them and ask user to choose
│   └── If no matches → tell user "No positions found for {pair}"
└── Confirm: "I found position #{id} — {pair} {feeTier} with {value}. Remove?"

Step 2: DELEGATE TO LIQUIDITY-MANAGER
├── Pass: positionId, chain, percentage (default 100%), collectFees
├── Agent handles: fee collection → partial/full removal → safety validation → execution
└── Returns: tokens received, fees collected, tx hash

Step 3: PRESENT RESULT
├── Tokens received with USD values
├── Fees collected (if any)
├── Total value received
├── Explorer link
└── If partial removal: remaining position details
```

### 收取费用流程
```
Step 1: IDENTIFY POSITION (same as remove)

Step 2: CHECK UNCOLLECTED FEES
├── Call get_position to see tokensOwed0 and tokensOwed1
├── If fees are zero → "No fees to collect on this position"
└── Show fee amounts and ask to proceed

Step 3: DELEGATE TO LIQUIDITY-MANAGER
├── Pass: positionId, chain, action: "collect"
└── Returns: fees collected, tx hash

Step 4: PRESENT RESULT
├── Fees collected (token amounts + USD values)
├── Explorer link
└── Tip: "Your position is still active and earning more fees"
```

## 关键决策点

在以下情况下，系统必须**停止操作并询问用户**，而不是自动执行：

| 情况                          | 应采取的行动                                      |
|----------------------------------|-----------------------------------------------------------|
| 找到多个符合条件的流动性池     | 列出所有选项，让用户选择一个                             |
| 金额超过钱包余额       | 显示余额，询问用户是否希望减少投入金额                         |
| 流动性池的总价值（TVL）低于1万美元 | 警告流动性风险较低，请求用户确认                         |
| 未指定范围策略         | 默认使用“medium”策略，但需说明相关风险                         |
| 用户首次进行流动性操作       | 在执行前简要说明潜在风险                             |
| 移除的流动性超过池总价值的50%     | 警告移除操作可能对价格产生影响                         |

## 输出格式

### 添加流动性成功
```text
Liquidity Added Successfully

  Position: #456789
  Pool:     WETH/USDC 0.05% (V3, Ethereum)
  
  Deposited:
    0.5 WETH  ($980)
    980 USDC  ($980)
    Total:    $1,960

  Range:
    Lower: $1,700 (tick -204714)
    Upper: $2,300 (tick -199514)
    Current: $1,963 — IN RANGE ✓
    Width: ±15% (medium)

  Expected Fee APY: ~15-21% (based on 7d pool data)
  
  Tx: https://etherscan.io/tx/0x...

  Next steps:
  - Monitor with: "How are my positions doing?"
  - Rebalance if out of range: "Rebalance position #456789"
  - Collect fees anytime: "Collect fees from position #456789"
```

### 移除流动性成功
```text
Liquidity Removed

  Position: #456789 (CLOSED)
  
  Received:
    0.52 WETH  ($1,020)
    950 USDC   ($950)
    Total:     $1,970

  Fees Collected:
    0.01 WETH  ($19.60)
    15.20 USDC ($15.20)
    Total fees: $34.80

  Net Result: +$44.80 (+2.3%) including fees
  
  Tx: https://etherscan.io/tx/0x...
```

## 重要说明

- **临时性损失风险**：在为波动性较大的货币对添加流动性时，务必提醒用户存在临时性损失的风险。
- **Gas费用**：在Ethereum主网上，添加流动性操作的Gas费用为15-50美元。对于小额交易，需特别说明。
- **范围选择的影响**：选择较窄的范围会导致更高的费用，但需要更频繁的重新平衡；选择较宽的范围则费用较低，但维护成本也较低。务必向用户解释这些差异。
- **V2与V3模式**：V2模式为“设置一次即可长期使用”的模式，但收益较低；V3模式需要用户主动管理，但收益较高。帮助用户根据需求做出选择。
- **禁止自动执行**：对于移除流动性或重新平衡的操作，必须在使用前获得用户的确认。

## 错误处理

| 错误类型                | 显示给用户的消息                                      | 建议的操作                                      |
|-------------------|---------------------------------------------------------|---------------------------------------------------------|
| 未配置钱包             | “未配置用于交易的钱包。”                                    | 在`.env`文件中设置WALLET_TYPE和PRIVATE_KEY                         |
| 钱包余额不足             | “您的余额为X，但需要Y才能完成操作。”                             | 减少投入金额或更换所需的代币                         |
| 未找到合适的流动性池         | “在当前费用等级下未找到对应的流动性池。”                         | 尝试其他费用等级或检查代币名称                         |
| 未找到相关持仓           | “在当前链上未找到指定的持仓。”                             | 检查链和持仓ID                               |
| 安全检查失败             | “交易因安全原因被阻止：{原因}”                               | 调整参数或检查安全配置                             |
| 交易失败             | “交易失败：{原因}”                                    | 检查交易细节或重试                               |
| liquidity-manager不可用       | “流动性管理代理当前不可用。”                                 | 检查代理的配置情况                               |