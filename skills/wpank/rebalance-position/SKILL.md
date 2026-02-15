---
name: rebalance-position
description: 通过平仓原有的Uniswap V3/V4杠杆交易头寸并重新开立一个以当前价格为基准的新头寸来重新平衡该头寸。该流程涵盖了费用收取、范围计算以及重新进入市场的所有步骤。适用于头寸超出预设范围且需要调整的情况。
model: opus
allowed-tools: [Task(subagent_type:liquidity-manager), mcp__uniswap__get_positions_by_owner, mcp__uniswap__get_position, mcp__uniswap__get_pool_info]
---

# 重新平衡持仓

## 概述

当一个 V3/V4 类型的长期合约（LP）持仓超出预设的范围时，该持仓将停止产生收益。此功能负责完成整个重新平衡的流程：收集累积的收益、关闭旧持仓、根据当前价格计算新的最佳范围，并开启新的持仓——所有这些操作都在一次操作中完成。

这是一个非常实用的功能，因为超出范围的持仓实际上相当于“死资本”。及时重新平衡的持仓与未受监控的持仓相比，可能会损失 15-30% 的年化收益（APY）。

## 适用场景

在用户发出以下指令时激活此功能：
- “重新平衡我的持仓”
- “我的持仓超出了范围”
- “调整我的长期合约范围”
- “重新调整我的流动性”
- “持仓 #12345 超出了范围，请处理”
- “我的 ETH/USDC 持仓不再产生收益”
- “将我的持仓范围调整到当前价格”
- “我的长期合约不再盈利”

此外，在以下情况下也应主动建议用户进行重新平衡：
- `track-performance` 或 `portfolio-report` 报告显示有持仓超出范围
- 用户询问“为什么我无法获得收益？”

## 参数

| 参数            | 是否必填 | 默认值       | 获取方式                                              |
| ------------------------- | -------- | ------------- | -------------------------------------------------------------- |
| positionId     | 否       | —            | 持仓 ID；或 “my ETH/USDC position”（通过搜索确定）                |
| chain         | 否       | ethereum      | 持仓所在的区块链                          |
| newRange       | 否       | 自动计算的最佳范围    | “narrow”（±5%）、“medium”（±15%）、“wide”（±50%）                           |

*如果未提供持仓 ID：使用 `get_positions_by_owner` 进行搜索，筛选出超出范围的持仓，并与用户确认。*

## 工作流程

### 重新平衡前的分析

在执行任何操作之前，先收集数据并向用户展示当前的情况：

```
Step 1: IDENTIFY THE POSITION
├── If position ID given → fetch via get_position
├── If "my X/Y position" → search via get_positions_by_owner
│   ├── Filter by token pair and out-of-range status
│   ├── If multiple out-of-range → list all, ask which one
│   └── If none out-of-range → "All your positions are in range!"
└── Validate: confirm the position IS actually out of range

Step 2: ANALYZE CURRENT SITUATION
├── Current pool state via get_pool_info
│   ├── Current price
│   ├── Pool TVL, volume, fee APY
│   └── Tick distribution (where is liquidity concentrated?)
├── Position details
│   ├── Current tick range (lower, upper)
│   ├── How far out of range (above or below?)
│   ├── Uncollected fees
│   ├── Current token balances in position
│   └── Time since going out of range (if estimable)
└── Cost-benefit calculation
    ├── Estimated gas cost for full rebalance (remove + add = ~$30-60 on mainnet)
    ├── Estimated daily fee revenue if rebalanced (from pool APY + position size)
    ├── Break-even time: gas_cost / daily_revenue
    └── If break-even > 30 days → WARN that rebalancing may not be worth it
```

### 展示重新平衡计划

在执行前，向用户明确说明即将发生的具体操作：

```text
Rebalance Plan for Position #12345

  Current Situation:
    Pool:      WETH/USDC 0.05% (V3, Ethereum)
    Status:    OUT OF RANGE ⚠ (price moved above your range)
    Current:   $1,963
    Your range: $1,500 - $1,800 (position is 9% above upper bound)
    
  Uncollected Fees: 0.01 WETH ($19.60) + 15.20 USDC ($15.20)
  Position Value: ~$3,940

  Proposed New Range:
    Strategy: Medium (±15%)
    Lower:    $1,668 (current - 15%)
    Upper:    $2,258 (current + 15%)
    Expected time-in-range: ~80-85%

  Cost:
    Gas (remove + add): ~$35
    Break-even: ~2 days at current fee APY

  Steps:
    1. Collect uncollected fees ($34.80)
    2. Remove all liquidity from position #12345
    3. Add liquidity at new range ($1,668 - $2,258)
    4. New position created with new NFT ID

  Proceed? (yes/no)
```

### 执行（用户确认后）

```
Step 3: DELEGATE TO LIQUIDITY-MANAGER
├── The agent executes atomically:
│   a. Collect fees from old position
│   b. Remove 100% liquidity from old position
│   c. Calculate new tick range based on:
│      - Current pool price
│      - Selected range strategy (narrow/medium/wide)
│      - Pool tick spacing
│   d. Approve tokens for new position (if needed)
│   e. Add liquidity at new range
│   f. Each step validated by safety-guardian
└── Returns: old position closed, fees collected, new position ID, new range, tx hashes

Step 4: PRESENT RESULT
├── Confirmation of old position closure
├── Fees collected (amounts + USD)
├── New position details (ID, range, amounts deposited)
├── Total gas cost for the operation
├── Net cost/benefit of the rebalance
└── Next steps for monitoring
```

## 范围策略指南

当用户未指定范围时，可参考以下决策框架：

| 对象类型           | 推荐范围        | 范围宽度      | 原因                                                  |
| ------------------------- | ---------------------- | ------------ | ----------------------------------------------------------- |
| 稳定对稳定资产     | 较窄的范围      | ±0.5%        | 价格波动小，需最大化资本效率                          |
| 稳定对波动性资产     | 中等范围      | ±15%        | 在盈利与减少重新平衡之间取得平衡                         |
| 波动性对波动性资产     | 较宽的范围      | ±30%        | 减少重新平衡的频率，但可能降低年化收益                     |
| 用户选择“激进策略”    | 较窄的范围      | ±5%        | 收益较高，但需要更频繁的重新平衡                     |
| 用户选择“保守策略”    | 较宽的范围      | ±50%        | 维护成本较低，但收益也较低                         |
| 持仓金额较小（<1000 美元） | 较宽的范围      | ±50%        | 高额的交易手续费使得频繁重新平衡不经济                    |

## 何时不应进行重新平衡

在以下情况下应主动建议用户不要重新平衡：

| 情况                                      | 建议                                              |
| ----------------------------------------- | ----------------------------------------------------------- |
| 持仓成本高于交易手续费10倍             | “交易手续费为 ${gas}，而您的持仓价值仅为 ${value}。”                   |
| 价格接近范围边界（在2%范围内）           | “价格接近您的范围范围，请等待价格再次进入范围。”                        |
| 持仓超出范围时间不足1小时             | “给价格一些时间，它可能会重新回到范围内。”                         |
| 用户对价格走势没有明确判断             | “建议设置较宽的范围以减少未来的重新平衡次数。”                     |
| 持仓达到盈亏平衡时间超过14天             | “以当前的费用率计算，重新平衡在 {days} 天内无法盈利。”                   |

## 输出格式

### 重新平衡成功

```text
Position Rebalanced Successfully

  Old Position: #12345 (CLOSED)
    Received: 0.52 WETH + 950 USDC ($1,970)
    Fees collected: 0.01 WETH + 15.20 USDC ($34.80)

  New Position: #67890
    Pool: WETH/USDC 0.05% (V3, Ethereum)
    Deposited: 0.51 WETH + 965 USDC ($1,960)
    Range: $1,668 - $2,258 (medium, ±15%)
    Current: $1,963 — IN RANGE ✓
    
  Cost:
    Gas: $32.50 (2 transactions)
    
  Net: Position rebalanced with $2.30 lost to gas
       Now earning ~15-21% APY in fees

  Txs:
    Remove: https://etherscan.io/tx/0x...
    Add:    https://etherscan.io/tx/0x...

  Monitor: "How are my positions doing?" or "Track position #67890"
```

### 持仓已回到范围内

```text
Position #12345 is IN RANGE ✓

  Pool:    WETH/USDC 0.05% (V3, Ethereum)
  Current: $1,963
  Range:   $1,700 - $2,300
  Status:  Actively earning fees

  No rebalance needed. Your position is healthy.
  
  Uncollected fees: $34.80
  Want to collect them? (This doesn't affect your position.)
```

## 重要提示

- **执行前务必确认。** 重新平衡涉及关闭并重新开启持仓，这个过程是不可逆的。
- **手续费很重要。** 在以太坊主网上，一次完整的重新平衡操作需要支付 30-60 美元的手续费。在 Layer-2 平台（如 Base、Arbitrum）上，手续费低于 1 美元。在提供建议时请考虑这一点。
- **未实现利润（IL）会被锁定。** 关闭持仓时，任何未实现的利润都会变为实际损失。如果持仓有较大的未实现利润，请务必告知用户。
- **重新平衡后的持仓会获得新的 NFT 令牌 ID。** 旧持仓的 NFT 令牌会被销毁。请确保用户了解这一点。
- **V2 类型的持仓无法重新平衡**——它们的范围是固定的。如果用户请求重新平衡 V2 持仓，请解释 V2 持仓的覆盖范围是固定的，不会“超出范围”。
- **退出时可能产生滑点。** 对于相对于池总价值（TVL）较大的持仓，退出操作可能会产生滑点。如果持仓金额超过池总价值的 5%，请提前警告用户。

## 错误处理

| 错误类型                | 显示给用户的消息                                      | 建议的操作                                      |
| ---------------------- | ------------------------------------------------------ | ------------------------------------------------------ |
| 未找到持仓                | “未找到持仓 #{id}。”                                      | 请检查持仓 ID 和所在的区块链                          |
| 持仓已回到范围内             | “持仓已回到范围内，无需重新平衡。”                             | 直接显示持仓状态                               |
| 该持仓为 V2 类型                | “V2 类型的持仓覆盖整个价格范围，因此不会超出范围。”                        | 解释 V2 和 V3 持仓的区别                         |
| 未配置钱包                 | “未配置用于交易的钱包。”                                   | 请设置 WALLET_TYPE 和 PRIVATE_KEY                          |
| 以太坊数量不足             | “以太坊数量不足，无法完成操作。”                               | 请为钱包充值以太坊                             |
| 安全检查失败                | “安全系统阻止了重新平衡操作：{原因}。”                             | 请检查安全配置                         |
| 移除持仓失败                | “尝试移除旧持仓失败：{原因}。”                               | 请检查持仓状态并重新尝试                         |
| 添加新持仓失败                | “成功移除了旧持仓，但新持仓添加失败。”                             | 请确认以太坊已充值钱包，并手动尝试添加新持仓                   |
| 流动性管理器不可用             | “流动性管理器当前不可用。”                                  | 请检查流动性管理器的配置                         |