---
name: cross-chain-arbitrage
description: >-
  Find and execute cross-chain arbitrage opportunities. Scans prices across all
  chains, evaluates profitability after all costs (gas, bridge fees, slippage),
  assesses risk, and executes if profitable. Uses ERC-7683 for cross-chain
  settlement. Supports scan-only mode for research without execution.
model: opus
allowed-tools:
  - Task(subagent_type:opportunity-scanner)
  - Task(subagent_type:risk-assessor)
  - Task(subagent_type:cross-chain-executor)
  - Task(subagent_type:portfolio-analyst)
  - mcp__uniswap__check_safety_status
  - mcp__uniswap__get_agent_balance
---

# 跨链套利

## 概述

该功能可自动发现并执行跨链套利机会——即在不同的区块链上查找同一代币的价格差异，并从中获利。它涵盖了整个流程：扫描11个区块链上的价格、计算全部成本、进行风险评估、通过ERC-7683协议执行跨链交易以及生成利润报告。

**为何该功能比手动操作高效10倍：**

1. **多链同时扫描价格**：手动检查以太坊（Ethereum）、Base、Arbitrum、Optimism、Polygon等6个区块链上的ETH价格需要耗费大量时间。而该功能可在几秒钟内完成所有支持链的价格扫描。
2. **全面成本核算**：套利中最常见的错误就是忽略了成本。该功能会详细列出所有成本组成部分（来源网络费、桥接费、目标网络费以及双方的滑点），并仅展示在扣除所有成本后仍有利润的机会。
3. **对时间敏感**：套利机会非常短暂，可能瞬间消失。该功能会持续提醒用户这一风险，并迅速采取行动；但如果用户确认操作时机会可能已经消失，也会及时提示。
4. **风险控制**：在执行任何资金转移之前，风险评估机制会评估桥接风险、执行风险和流动性。如果风险过高，整个流程将被中止。
5. **仅扫描模式**：如果用户不想立即执行操作，可以选择“仅扫描”模式，查看现有套利机会而无需投入资金。

## 使用场景

当用户提出以下请求时，可激活该功能：
- “查找跨链ETH套利机会”
- “是否存在WETH在不同区块链上的价格差异？”
- “利用价格差异获利”
- “扫描Base链与以太坊之间的套利机会”
- “是否有USDC的套利机会？”
- “使用5000美元进行跨链套利”
- “仅扫描套利机会——不执行”（仅扫描模式）

**不适用场景**：
- 用户需要在同一区块链上进行交易（使用`execute-swap`）
- 用户仅需要桥接代币而不进行套利（使用`bridge-tokens`）
- 用户希望获取普通流动性挖矿（LP）收益（使用`scan-opportunities`或`find-yield`）

## 参数设置

| 参数                | 是否必填 | 默认值            | 设置方法                                                     |
|------------------|--------|------------------|---------------------------------------------------------|
| token             | 否       | 前5大热门代币        | 需要检查的代币（例如“WETH”、“USDC”，或默认扫描热门代币）                         |
| chains            | 否       | 所有区块链         | 需要扫描的区块链（例如“all”或具体列表，如“ethereum, base”）                     |
| minProfit          | 否       | 0.5%             | 所有成本后的最低净利润阈值                                      |
| maxAmount          | 否       | --              | 每次套利操作的最大资金限额                                      |
| riskTolerance       | 否       | 中等             | 风险容忍度设置（“conservative”、“moderate”、“aggressive”）                   |
| mode                | 否       | execute          | “execute”（执行完整流程）或“scan”（仅扫描，不执行）                         |

如果`mode`设置为“scan”，或者用户请求“仅扫描”/“不执行”/“显示套利机会”，则跳过步骤3-4，直接展示套利机会报告。

## 工作流程

```
                     CROSS-CHAIN ARBITRAGE PIPELINE
  ┌─────────────────────────────────────────────────────────────────────┐
  │                                                                     │
  │  Step 1: SCAN (opportunity-scanner)                                 │
  │  ├── Compare token prices across all chains                         │
  │  ├── Calculate gross profit for each discrepancy                    │
  │  ├── Itemize ALL costs (gas, bridge, slippage)                      │
  │  ├── Filter: only net profit > minProfit                            │
  │  └── Output: Ranked Arbitrage Opportunities                         │
  │          │                                                          │
  │          ▼                                                          │
  │  ┌───────────────────────────────────────────────────┐              │
  │  │  SCAN-ONLY MODE?                                  │              │
  │  │  Yes → Present report, STOP.                      │              │
  │  │  No  → Continue to Step 2.                        │              │
  │  └───────────────────────────────────────────────────┘              │
  │          │                                                          │
  │          ▼ USER SELECTION                                           │
  │  ┌───────────────────────────────────────────────────┐              │
  │  │  Present opportunities to user.                   │              │
  │  │  User picks which opportunity to execute.         │              │
  │  │  WARN: "Opportunity may expire before execution." │              │
  │  └───────────────────────────────────────────────────┘              │
  │          │                                                          │
  │          ▼                                                          │
  │                                                                     │
  │  Step 2: RISK CHECK (risk-assessor)                                 │
  │  ├── Evaluate bridge risk (mechanism, settlement time)              │
  │  ├── Evaluate execution risk (slippage, speed)                      │
  │  ├── Evaluate liquidity on both chains                              │
  │  ├── Decision: APPROVE / VETO / HARD_VETO                          │
  │  └── Output: Risk Assessment                                        │
  │          │                                                          │
  │          ▼ CONDITIONAL GATE                                         │
  │  ┌───────────────────────────────────────────────────┐              │
  │  │  APPROVE → Proceed with confirmation              │              │
  │  │  VETO / HARD_VETO → STOP with report              │              │
  │  └───────────────────────────────────────────────────┘              │
  │          │                                                          │
  │          ▼ USER CONFIRMATION                                        │
  │  ┌───────────────────────────────────────────────────┐              │
  │  │  "Execute this arb? Opportunity may have shifted  │              │
  │  │   since scan. Confirm to proceed."                │              │
  │  └───────────────────────────────────────────────────┘              │
  │          │                                                          │
  │          ▼                                                          │
  │                                                                     │
  │  Step 3: EXECUTE (cross-chain-executor)                             │
  │  ├── Buy on cheaper chain                                           │
  │  ├── Bridge to expensive chain via ERC-7683                         │
  │  ├── Monitor bridge settlement                                      │
  │  ├── (Sell on expensive chain if needed)                            │
  │  └── Output: Execution Report                                       │
  │          │                                                          │
  │          ▼                                                          │
  │                                                                     │
  │  Step 4: REPORT (portfolio-analyst)                                 │
  │  ├── Calculate actual profit/loss after all costs                   │
  │  ├── Compare to projected profit                                    │
  │  └── Output: P&L Report                                             │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
```

### 步骤0：准备工作

开始前：
1. 通过`mcp__uniswap__check_safety_status`检查安全状态。
2. 通过`mcp__uniswap__get_agent_balance`查询相关区块链上的钱包余额。
3. 如果钱包余额不足，停止操作并通知用户。

### 步骤1：扫描套利机会（opportunity-scanner）

将任务委托给`Task(subagent_type:opportunity-scanner)`：

```
Scan for cross-chain arbitrage opportunities:
- Token: {token or "top 5 tokens by volume: WETH, USDC, USDT, WBTC, DAI"}
- Chains: {chains or "all supported chains"}
- Type: "arb" (arbitrage only)
- Minimum net profit: {minProfit}%

For each price discrepancy found, calculate and itemize:
1. Gross price difference (%)
2. Source chain gas cost (USD)
3. Bridge fee (USD)
4. Destination chain gas cost (USD)
5. Slippage estimate on both sides (USD)
6. NET profit after ALL costs (USD and %)

Only include opportunities where net profit > {minProfit}% after all costs.
Rank by net profit. Include time sensitivity assessment for each opportunity.
```

**向用户展示结果：**

```text
Step 1: Arbitrage Scan Complete

  Token: WETH
  Chains scanned: 8 (Ethereum, Base, Arbitrum, Optimism, Polygon, BNB, Avalanche, Blast)

  Opportunities found: 2 (after filtering by {minProfit}% min net profit)

  #  Route                     Gross    Costs         Net Profit  Time Sensitivity
  1  WETH: Arbitrum → Optimism  0.8%    $12 total     $33 (0.66%) EPHEMERAL
     ├── Source gas:   $0.50
     ├── Bridge fee:   $2.00
     ├── Dest gas:     $0.50
     └── Slippage:     $9.00 (both sides)

  2  WETH: Base → Polygon       0.6%    $8 total      $22 (0.44%) EPHEMERAL
     ├── Source gas:   $0.10
     ├── Bridge fee:   $3.00
     ├── Dest gas:     $1.50
     └── Slippage:     $3.40 (both sides)

  WARNING: Arbitrage opportunities are ephemeral. These prices were captured at
  {timestamp} and may change by the time you confirm execution. The actual profit
  may differ from the estimates above.

  No opportunities found for: USDC, USDT, WBTC, DAI (spreads < {minProfit}% after costs)
```

**如果模式为“scan”**，则在此步骤结束：

```text
Arbitrage Scan Report (scan-only mode)

  {same opportunity table as above}

  To execute an opportunity, run: "Cross-chain arb, execute opportunity #1"
  Note: Opportunities are time-sensitive and may no longer be available.
```

**如果模式为“execute”**，询问用户希望执行哪个套利机会。

### 步骤2：风险评估（risk-assessor）

将选定的套利机会委托给`Task(subagent_type:risk-assessor)`：

```
Evaluate risk for this cross-chain arbitrage:

Operation: cross-chain arbitrage
Token: {token}
Source chain: {source_chain}
Destination chain: {dest_chain}
Amount: {amount or maxAmount}
Risk tolerance: {riskTolerance}

Opportunity details (from opportunity-scanner):
- Gross spread: {gross_pct}%
- Estimated net profit: {net_profit_usd} ({net_pct}%)
- Cost breakdown: {full cost itemization}
- Time sensitivity: ephemeral

Evaluate:
1. Bridge risk (settlement mechanism, historical reliability, available liquidity)
2. Execution risk (can the arb close before we complete? slippage may increase)
3. Liquidity risk (sufficient depth on both chains for the trade size)
4. Smart contract risk (pool ages and versions on both chains)

Key concern: arbitrage opportunities are time-sensitive. Factor in the risk that
the price discrepancy may close during bridge settlement (typically 1-10 minutes).
```

**决策流程**：
| 决策              | 执行动作                                      |
|------------------|---------------------------------------------------------|
| **批准**            | 显示风险总结，等待用户确认                                      |
| **条件性批准**        | 显示相关条件（例如“减少交易规模”），询问用户意见                        |
| **拒绝**            | **停止操作**：当前交易规模或风险超出容忍范围。显示详细原因                   |
| **强制拒绝**          | **停止操作**：桥接流动性不足或存在重大风险。不可协商                         |

**用户确认（包含时间提醒）：**

```text
Step 2: Risk Assessment Passed

  Decision: APPROVE
  Composite Risk: MEDIUM
  Bridge Risk: LOW (ERC-7683, established mechanism)
  Execution Risk: MEDIUM (arb may close during 2-5 min settlement)
  Liquidity: LOW (deep pools on both chains)

  Execute Arbitrage?
    Route:    Buy WETH on Arbitrum → Bridge → (Sell on Optimism)
    Amount:   $5,000
    Est. Profit: $33 (0.66%) after all costs
    Settlement: ~2-5 minutes

    IMPORTANT: This opportunity was scanned at {timestamp} ({N} seconds ago).
    The price discrepancy may have changed. Actual profit may differ from estimate.

  Proceed? (yes/no)
```

### 步骤3：执行交易（cross-chain-executor）

将任务委托给`Task(subagent_type:cross-chain-executor)`：

```
Execute this cross-chain arbitrage:

Leg 1 (source chain):
- Chain: {source_chain}
- Action: Buy {token} (swap {capital_token} → {token})
- Amount: {amount}
- Pool: {best pool on source chain}

Leg 2 (bridge):
- Bridge {token} from {source_chain} to {dest_chain}
- Mechanism: ERC-7683

Leg 3 (destination chain — if needed):
- Chain: {dest_chain}
- Action: Sell {token} (swap {token} → {capital_token}) — only if the user
  wants to realize profit immediately. Otherwise, hold the {token} on dest chain.

Risk assessment: APPROVED, composite {risk_level}
Time sensitivity: HIGH — execute as quickly as possible.

Monitor bridge settlement and report progress. If bridge takes longer than
expected, warn about potential profit erosion.
```

**执行过程中更新进度：**

```text
Step 3: Executing Arbitrage...

  [1/3] Buying WETH on Arbitrum...
        Bought 2.55 WETH for $5,000 USDC — Tx: 0x...
  [2/3] Bridging WETH to Optimism via ERC-7683...
        Order ID: 0x... — Monitoring settlement...
        Status: PENDING (elapsed: 45s, expected: 2-5 min)
        Status: PENDING (elapsed: 2m 15s)
        Status: SETTLED (elapsed: 3m 02s) — 2.55 WETH received on Optimism
  [3/3] Holding WETH on Optimism (no sell leg — same token, profit realized)
        ✓ Arbitrage complete
```

### 步骤4：生成报告（portfolio-analyst）

将任务委托给`Task(subagent_type:portfolio-analyst)`：

```
Report on the result of this cross-chain arbitrage:

Execution details:
- Token: {token}
- Source: {source_chain} — bought at ${source_price}
- Destination: {dest_chain} — current price ${dest_price}
- Amount: {amount}
- Bridge order: {order_id}
- Transactions: {tx_hashes}

Calculate:
1. Actual gross profit (price difference realized)
2. All actual costs (gas, bridge fees, slippage — from execution receipts)
3. Net profit/loss
4. Comparison to projected profit from scan
5. Portfolio impact
```

**展示最终结果：**

```text
Step 4: Arbitrage Report

  Route:        WETH: Arbitrum → Optimism
  Amount:       2.55 WETH ($5,000)

  Profit & Loss:
    Gross spread:     $40.00 (0.80%)
    Source gas:        -$0.45
    Bridge fee:        -$1.80
    Dest gas:          -$0.00 (held, no sell)
    Slippage:          -$7.50
    ─────────────────────────
    Net profit:        $30.25 (0.61%)

  vs. Projected:     $33.00 (0.66%) — actual was 8% less due to slippage

  Timing:
    Scan to execution: 45 seconds
    Bridge settlement:  3 min 02 sec
    Total elapsed:      3 min 47 sec

  Portfolio Impact:
    WETH on Optimism:  2.55 WETH ($5,030.25)
    Net gain:          $30.25

  ──────────────────────────────────────
  Pipeline Summary
  ──────────────────────────────────────
  Scan:       2 opportunities found, #1 selected
  Risk:       APPROVED (MEDIUM)
  Execution:  Buy → Bridge → Hold (3 min 47 sec total)
  Result:     +$30.25 net profit (0.61%)
```

## 输出格式

### 成功执行

```text
Cross-Chain Arbitrage Complete

  Route:    {token}: {source_chain} -> {dest_chain}
  Amount:   ${amount}
  Net P&L:  +${net_profit} ({net_pct}%)
  Time:     {total_elapsed}

  Cost Breakdown:
    Gas: ${gas}  Bridge: ${bridge_fee}  Slippage: ${slippage}

  Pipeline: Scan -> Risk -> Execute -> Report (all passed)
```

### 仅扫描结果

```text
Cross-Chain Arbitrage Scan

  Scanned: {n_tokens} tokens across {n_chains} chains
  Found: {n_opportunities} opportunities (> {minProfit}% net profit)

  {opportunity table}

  To execute: "Cross-chain arb, execute opportunity #N"
```

### 交易被拒绝

```text
Cross-Chain Arbitrage -- Risk Vetoed

  Opportunity: {token} {source} -> {dest} ({gross_spread}% gross)
  Risk: VETOED — {reason}

  {risk dimension details}

  Pipeline: Scan -> Risk (VETOED) -- No execution.
```

## 重要说明：

- **套利机会具有时效性**：用户查看扫描结果并确认操作时，价格差异可能已经消失。该功能会明确提醒用户这一点，并不保证一定能获利。
- **全面成本核算至关重要**：切勿将总价格差直接视为利润。必须详细列出并扣除所有费用（来源网络费、桥接费、目标网络费及滑点）。例如，看似有0.8%利润的机会，实际净利润可能只有0.2%，甚至为负数。
- **桥接结算时间存在风险**：在1-10分钟的桥接结算期间，目标区块链上的价格可能会变动，导致利润消失或减少。风险评估机制会考虑这一因素。
- **默认设置为仅扫描模式**：如果用户不确定是否要执行操作，系统会默认使用仅扫描模式。用户之后仍可以选择“执行”。
- **并非每次扫描都能找到套利机会**：像WETH、USDC这样的热门代币，在扣除成本后，价格差异通常不超过0.5%。请用户对此有所预期。
- **小额交易时网络费影响显著**：总成本为150美元的套利交易，如果网络费高达15美元，几乎无法盈利。请用户注意这一点。
- **该操作并非无风险**：尽管称为“套利”，但跨链套利仍存在风险（如桥接失败、结算期间价格变动、智能合约风险等）。务必向用户明确说明其风险性。

## 错误处理

| 错误类型                | 显示给用户的消息                                      | 建议的操作                                      |
|------------------|--------------------------------------------------|---------------------------------------------------------|
| 未找到套利机会           | “在{chains}链上，没有净利润超过{minProfit}%的套利机会。”                 | 调高最低利润阈值或尝试其他代币                         |
| 套利机会已过期             | “扫描后价格差异已消失，该套利机会不再具有盈利性。”                   | 重新扫描以寻找新的机会                         |
| 风险评估拒绝             | “风险评估结果：{原因}。”                                      | 尝试减少交易金额或选择其他路径                         |
| 风险评估强制拒绝           | “因{原因}，操作被拒绝。桥接流动性不足。”                         | 无法继续执行该交易                         |
| 桥接失败                | “桥接操作失败。资金应保留在{source_chain}链上。”                       | 检查源钱包余额                         |
| 桥接操作延迟             | “桥接结算延迟（实际时间{elapsed}，预期时间为{expected}）。请稍候……”         | 等待或手动检查订单状态                         |
| 源链交易失败             | “在{source_chain}链上购买{token}失败：{原因}。”                         | 检查余额和网络费                         |
| 账户余额不足             | “{source_chain}链上的{token}数量不足，需要{Y}。”                         | 减少交易金额或先补充资金                         |
| 超过安全限额             | “交易金额超过安全使用限制。”                                   | 调整交易金额或修改安全限制                         |
| 未配置钱包             | “未配置用于交易的钱包。”                                   | 使用`setup-agent-wallet`设置钱包                         |
| 用户拒绝确认             | “套利操作已取消。以上为扫描结果供参考。”                         | 无需额外操作                         |
| 实际利润低于预期           | “由于价格变动，实际利润为{X}，低于预期{Y}。”                         | 针对短暂性套利机会的常见情况                         |
| 净利润为负（亏损）           | “由于结算期间价格变动，本次交易导致亏损{X}。”                         | 跨链套利的固有风险                         |