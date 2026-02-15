---
name: full-lp-workflow
description: >-
  Full LP workflow from opportunity scanning to position entry. Autonomously
  finds the best LP opportunity, designs a strategy, assesses risk, executes
  any needed swaps, enters the position, and reports portfolio impact. Use when
  user has capital and wants end-to-end LP management. Most complex multi-agent
  orchestration in the system.
model: opus
allowed-tools:
  - Task(subagent_type:opportunity-scanner)
  - Task(subagent_type:lp-strategist)
  - Task(subagent_type:risk-assessor)
  - Task(subagent_type:trade-executor)
  - Task(subagent_type:liquidity-manager)
  - Task(subagent_type:portfolio-analyst)
  - mcp__uniswap__check_safety_status
  - mcp__uniswap__get_agent_balance
---

# 完整的LP工作流程（Full LP Workflow）

## 概述

这是系统中最为复杂的多智能体协作流程。它将一个简单的指令——“我有2万美元，帮我找到收益最高的LP机会”——通过一个包含6个智能体的工作流程，转化为一个经过充分研究、风险评估、结构最优化的LP投资组合。

**为什么这比单独调用每个智能体要好10倍：**

1. **端到端自动化**：手动操作时，你需要扫描投资机会、研究市场、设计策略、评估风险、可能进行代币交换、增加流动性，并进行验证——每个步骤都需要不同的工具和专业知识。而这个流程只需一个命令即可完成所有这些操作。
2. **具有复合上下文的智能流程**：每个智能体都会基于前一个智能体的研究成果进行工作。LP策略制定者不仅会得到代币对，还会收到机会扫描器对为何选择该投资机会的全面分析；风险评估者则会评估LP策略制定者设计的实际策略，而不仅仅是进行一般的评估。
3. **两个用户确认环节**：在花费任何资金（进行代币交换）和投入资本（进入LP投资组合）之前，系统会暂停并请求用户的明确批准，让你始终掌握控制权。
4. **条件性代币交换**：如果你持有的代币不符合LP投资组合的要求，系统会自动处理代币交换——但会先向你展示具体的操作计划。
5. **投资组合影响报告**：进入投资组合后，投资组合分析师会向你详细展示你的投资组合发生了哪些变化，并提供持续的监控建议。
6. **每个阶段的故障恢复**：如果流程中的某个智能体出现故障，系统会显示已经完成的工作，并提供恢复建议。

## 适用场景

当用户说出以下内容时，激活此流程：

- “我有2万美元，帮我找到收益最高的LP机会并进入投资”
- “自动LP：找到收益最高的选项并进入投资”
- “使用1万美元进行完整的LP投资”
- “帮我找到收益最高的选项并建立投资组合”
- “我想进行LP投资，但不知道该选择哪个机会”
- “将5000美元投入到Uniswap中，找到最佳的投资机会”
- “端到端的LP流程：扫描、制定策略并进入投资”
- “目前最好的LP投资机会是什么？帮我安排”

**不适用场景**：
- 当用户已经知道想要投资哪个投资池时（使用`manage-liquidity`）；
- 当用户只是想比较不同策略而不执行任何操作时（使用`lp-strategy`）；
- 当用户只是想扫描投资机会而不进行实际操作时（使用`scan-opportunities`）。

## 参数

| 参数               | 是否必填 | 默认值    | 提取方式                                                         |
| ------------------ | -------- | ---------- | ------------------------------------------------------------------ |
| 资本                 | 是      | --         | 需要部署的总资本：“2万美元”、“10 ETH”、“5000美元”                               |
| 链路                 | 否       | 所有链路     | 目标链路或“所有链路”（用于跨链扫描）                         |
| 风险容忍度           | 否       | 中等       | “保守”、“中等”、“激进”                                           |
| 代币对偏好           | 否       | --         | 可选的代币对：例如“ETH/USDC”、“稳定币对”                    |
| 排除的代币             | 否       | --         | 需要排除的代币：“PEPE、SHIB”（避免低质量代币）                         |
| 资本代币             | 否       | 自动检测     | 资本所在的代币：“USDC”、“ETH”，从钱包自动检测                         |

如果用户没有提供资本金额，请**询问用户**——切勿自行猜测应部署的金额。

## 工作流程

```
                          FULL LP WORKFLOW PIPELINE
  ┌─────────────────────────────────────────────────────────────────────┐
  │                                                                     │
  │  Step 1: SCAN (opportunity-scanner)                                 │
  │  ├── Scan LP opportunities across chains                            │
  │  ├── Filter by risk tolerance and capital size                      │
  │  ├── Rank top 3-5 by risk-adjusted yield                           │
  │  └── Output: Ranked Opportunity List                                │
  │          │                                                          │
  │          ▼ USER CHOICE POINT                                        │
  │  ┌───────────────────────────────────────────────────┐              │
  │  │  Present top opportunities to user.               │              │
  │  │  User picks one OR accepts recommendation (#1).   │              │
  │  └───────────────────────────────────────────────────┘              │
  │          │                                                          │
  │          ▼                                                          │
  │                                                                     │
  │  Step 2: STRATEGIZE (lp-strategist)                                 │
  │  ├── Design optimal strategy for chosen opportunity                 │
  │  ├── Version, fee tier, range width, rebalance plan                 │
  │  ├── Conservative/moderate/optimistic APY estimates                 │
  │  └── Output: LP Strategy Recommendation                             │
  │          │                                                          │
  │          ▼                                                          │
  │                                                                     │
  │  Step 3: RISK CHECK (risk-assessor)                                 │
  │  ├── Receives: opportunity data + strategy details                  │
  │  ├── Evaluates: IL, slippage, liquidity, smart contract             │
  │  ├── Decision: APPROVE / CONDITIONAL / VETO / HARD_VETO            │
  │  └── Output: Risk Assessment Report                                 │
  │          │                                                          │
  │          ▼ CONDITIONAL GATE                                         │
  │  ┌───────────────────────────────────────────────────┐              │
  │  │  APPROVE / COND. APPROVE → Continue               │              │
  │  │  VETO / HARD_VETO → STOP with full report         │              │
  │  └───────────────────────────────────────────────────┘              │
  │          │                                                          │
  │          ▼                                                          │
  │                                                                     │
  │  Step 4: SWAP IF NEEDED (trade-executor) -- CONDITIONAL             │
  │  ├── Check wallet balances vs required tokens                       │
  │  ├── If tokens needed: calculate swap amounts                       │
  │  ├── USER CONFIRMATION #1: "Swap X for Y to prepare for LP?"       │
  │  ├── Execute swap(s) if confirmed                                   │
  │  └── Output: Swap result OR "tokens already held"                   │
  │          │                                                          │
  │          ▼                                                          │
  │                                                                     │
  │  Step 5: ENTER POSITION (liquidity-manager)                         │
  │  ├── USER CONFIRMATION #2: "Add liquidity with these params?"      │
  │  ├── Handle approvals (Permit2)                                     │
  │  ├── Add liquidity at recommended range                             │
  │  ├── Wait for transaction confirmation                              │
  │  └── Output: Position ID, amounts deposited, tick range             │
  │          │                                                          │
  │          ▼                                                          │
  │                                                                     │
  │  Step 6: CONFIRM & REPORT (portfolio-analyst)                       │
  │  ├── Verify position was created successfully                       │
  │  ├── Show portfolio impact (before vs after)                        │
  │  ├── Monitoring instructions                                        │
  │  └── Output: Portfolio Report + Next Steps                          │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
```

### 第0步：准备工作（Pre-Flight）

在开始流程之前：

1. 通过`mcp__uniswap__check_safety_status`检查安全性状态——确认可用的支出限额是否足够覆盖资本金额。
2. 通过`mcp__uniswap__get_agent_balance`检查目标链路上的钱包余额——确认钱包中确实有指定的资本。
3. 如果任何一项检查失败，请立即停止流程并通知用户，避免浪费智能体的计算资源。

### 第1步：扫描投资机会（机会扫描器，Opportunity-Scanner）

将任务委托给`Task(subagent_type:opportunity-scanner)`：

```
Scan for LP opportunities with these parameters:
- Available capital: {capital}
- Chains: {chain or "all supported chains"}
- Risk tolerance: {riskTolerance}
- Type: "lp" (LP opportunities only)
- Minimum TVL: $50,000
- Top N: 5

Additional filters:
- Pair preference: {pairPreference or "none"}
- Exclude tokens: {excludeTokens or "none"}

Return the top 5 LP opportunities ranked by risk-adjusted yield.
Each opportunity must include fee APY, estimated IL, risk-adjusted yield,
TVL, volume, and risk rating.
```

**向用户展示可选的投资机会，并让用户进行选择：**

```text
Step 1/6: Opportunity Scan Complete

  Found 5 LP opportunities (filtered from 200+ pools):

  #  Pool                Chain    Fee APY  Est. IL  Net APY  Risk    TVL
  1  WETH/USDC 0.05%     ETH      21%      -6%      15%     MEDIUM  $332M
  2  WETH/USDC 0.05%     Base     18%      -5%      13%     MEDIUM  $45M
  3  ARB/WETH 0.30%      Arb      35%      -12%     23%     HIGH    $12M
  4  USDC/USDT 0.01%     ETH      8%       -0.1%    7.9%    LOW     $200M
  5  cbETH/WETH 0.05%    Base     12%      -3%      9%      LOW     $28M

  Recommended: #1 (WETH/USDC 0.05% on Ethereum) — best balance of yield and risk

  Which opportunity would you like to pursue? (1-5, or "1" to accept recommendation)
```

**等待用户选择后继续下一步。**

### 第2步：制定策略（LP策略制定者，LP-Strategist）

根据用户的选择，将任务委托给`Task(subagent_type:lp-strategist)`：

```
Design an optimal LP strategy for this opportunity:

Opportunity details (from opportunity-scanner):
{Full opportunity data from Step 1 for chosen pool}

LP parameters:
- Capital: {capital}
- Risk tolerance: {riskTolerance}
- Chain: {chain of chosen opportunity}

Provide:
1. Recommended version and fee tier (with rationale)
2. Optimal tick range (lower/upper prices, width %)
3. Conservative/moderate/optimistic APY and IL estimates
4. Rebalance strategy (trigger, frequency, estimated cost)
5. Comparison to the next-best alternative
```

**向用户展示策略详情：**

```text
Step 2/6: Strategy Designed

  Pool:     WETH/USDC 0.05% (V3, Ethereum)
  Range:    $1,700 - $2,300 (±15%, medium width)
  Expected: 15% net APY (moderate estimate)

  Strategy Details:
    Fee APY (moderate): 21%
    Estimated IL: -6%
    Net APY: 15%
    Rebalance: every 2-3 weeks (trigger: price within 10% of boundary)
    Rebalance cost: ~$15/rebalance on Ethereum

  Proceeding to risk assessment...
```

### 第3步：风险评估（风险评估者，Risk-Assessor）

将任务委托给`Task(subagent_type:risk-assessor)`，并提供完整的背景信息：

```
Evaluate risk for this LP strategy:

Operation: add liquidity
Token pair: {token0}/{token1}
Pool: {pool address}
Chain: {chain}
Capital: {capital}
Risk tolerance: {riskTolerance}

Strategy context (from lp-strategist):
{Full strategy recommendation from Step 2}

Opportunity context (from opportunity-scanner):
{Key metrics from Step 1: TVL, volume trend, risk rating}

Evaluate: impermanent loss risk, slippage risk (entry/exit), liquidity risk,
smart contract risk. Provide APPROVE/CONDITIONAL_APPROVE/VETO/HARD_VETO.
```

**决策流程（与研究及交易流程相同）：**

| 决策                | 操作                                      |
| ---------------------- | ---------------------------------------- |
| **批准（APPROVE）**       | 显示风险总结，进入第4步                               |
| **有条件批准（CONDITIONAL_APPROVE）** | 显示条件，询问用户是否同意                             |
| **否决（VETO）**        | 停止流程。显示投资机会、策略及否决原因，并提供替代方案         |
| **绝对否决（HARD_VETO）**     | 停止流程。显示否决原因。不可协商                             |

**向用户展示（批准情况）：**

```text
Step 3/6: Risk Assessment Passed

  Decision: APPROVE
  Composite Risk: MEDIUM
  IL Risk: MEDIUM (8.2% annual estimate for volatile pair)
  Slippage: LOW (deep pool, entry < 0.1% impact)
  Liquidity: LOW (TVL 6,640x your position)
  Smart Contract: LOW (V3, established pool)

  Proceeding to prepare tokens...
```

### 第4步：如有需要，进行代币交换（交易执行者，Trade-Executor）——条件性操作

检查钱包余额，确认是否拥有LP投资组合所需的代币数量：

1. 策略会指定每种代币所需的数量（例如，为了达到平衡的投资组合，可能需要50/50的比例）。
2. 通过`mcp__uniswap__get_agent_balance`检查当前钱包中的代币持有情况。
3. 计算是否需要进行代币交换。

**如果不需要代币交换：**

```text
Step 4/6: Token Preparation — Skipped

  You already hold sufficient WETH and USDC for this position.
  No swaps required.
```

**如果需要代币交换，请向用户请求确认：**

```text
Step 4/6: Token Preparation Required

  Your position needs:
    0.5 WETH  (~$980)
    980 USDC  (~$980)

  You currently hold:
    2.0 WETH  ($3,920)
    0 USDC    ($0)

  Proposed swap:
    Sell 0.5 WETH → Buy ~980 USDC
    Estimated slippage: 0.05%
    Gas: ~$8

  Approve this swap to prepare tokens for LP? (yes/no)
```

**只有在使用者明确同意后，才执行代币交换。** 如果用户拒绝，停止流程并展示已经完成的工作（包括机会扫描、策略制定和风险评估结果）。

### 第5步：进入投资组合（流动性管理者，Liquidity-Manager）

向用户展示完整的LP投资组合详情，并请求用户进行第二次确认：

```text
Step 5/6: Ready to Add Liquidity

  Pool:     WETH/USDC 0.05% (V3, Ethereum)
  Deposit:
    0.5 WETH  (~$980)
    980 USDC  (~$980)
    Total:    ~$1,960

  Range:
    Lower: $1,700 (tick -204714)
    Upper: $2,300 (tick -199514)
    Current: $1,963 — IN RANGE
    Width: ±15% (medium)

  Expected Fee APY: ~15-21% (based on 7d pool data)

  Add liquidity with these parameters? (yes/no)
```

**只有在用户确认后，才继续下一步。** 然后将任务委托给`Task(subagent_type:liquidity-manager)`：

```
Add liquidity to this pool:

Pool: {pool address}
Chain: {chain}
Version: {version}
Token0: {token0 address} — Amount: {amount0}
Token1: {token1 address} — Amount: {amount1}
Tick lower: {tick_lower}
Tick upper: {tick_upper}

Strategy context:
- Range strategy: {medium/narrow/wide}
- From lp-strategist recommendation

Execute: handle approvals, simulate, route through safety-guardian, add liquidity,
wait for confirmation. Return position ID and actual amounts deposited.
```

### 第6步：确认并报告（投资组合分析师，Portfolio-Analyst）

将任务委托给`Task(subagent_type:portfolio-analyst)`，并提供新的投资组合详情：

```
Report on the portfolio impact of this new LP position:

New position:
- Position ID: {position_id from Step 5}
- Pool: {pool_address}
- Chain: {chain}
- Tokens deposited: {amounts}
- Tick range: {lower} to {upper}
- Transaction: {tx_hash}

Wallet address: {wallet_address}

Provide:
1. New position details and current status (in-range confirmation)
2. Portfolio impact (if other positions exist, show before/after composition)
3. Total portfolio value across all chains
4. Monitoring recommendations
```

**向用户展示最终结果：**

```text
Step 6/6: Position Confirmed & Portfolio Updated

  New Position: #456789
  Pool:     WETH/USDC 0.05% (V3, Ethereum)
  Status:   IN RANGE
  Value:    $1,960

  Deposited:
    0.5 WETH  ($980)
    980 USDC  ($980)

  Range:
    $1,700 — $2,300 (current: $1,963)

  Expected Returns:
    Fee APY: 15-21% (moderate-optimistic)
    Est. IL: -5 to -8% annualized
    Net: 9-15% annualized

  Portfolio Impact:
    Total LP Value:  $1,960 (new) + $45,000 (existing) = $46,960
    LP Allocation:   42% WETH, 35% USDC, 23% other
    Chain Split:     85% Ethereum, 15% Base

  ──────────────────────────────────────
  Pipeline Summary
  ──────────────────────────────────────
  Scan:      5 opportunities found, #1 selected
  Strategy:  V3 0.05%, ±15% range, bi-weekly rebalance
  Risk:      APPROVED (MEDIUM composite)
  Swap:      0.5 WETH → 980 USDC (preparation)
  Position:  #456789 — IN RANGE
  Cost:      $15.20 total gas (swap + LP entry)

  Next Steps:
  - Monitor: "How are my positions doing?"
  - Rebalance when needed: "Rebalance position #456789"
  - Collect fees: "Collect fees from position #456789"
```

## 关键决策点

在这些关键时刻，系统必须**停止并请求用户的确认**，而不能自行决策：

| 情况                          | 应采取的行动                                      |
| ----------------------------- | ------------------------------------------------------ |
| 未指定资本金额                | 询问：“您希望部署多少资本？”                                      |
| 找到多个合适的投资机会            | 展示前3-5个最佳选项，让用户选择                         |
| 风险评估者否决                    | 停止流程。展示研究结果、策略及否决原因                         |
| 需要进行代币交换以准备投资组合        | 向用户请求第一次确认：展示交换细节，询问是否继续                   |
| 准备增加流动性                | 向用户请求第二次确认：展示投资组合详情，询问是否继续                   |
| 资本超过安全支出限额              | 停止流程。显示限额，并建议减少资本或调整限额                         |
| 钱包余额不足                    | 停止流程。显示实际余额，并建议调整资本金额                         |
| 最佳投资机会位于用户资金所在的链路之外     | 解释跨链情况，并建议使用桥接工具或调整链路选择                   |

## 流程失败时的恢复措施

如果流程在中间阶段失败，系统会报告已经完成的工作以及剩余的任务：

```text
LP Workflow — Partial Completion

  Completed:
    [done] Step 1: Scan — 5 opportunities found, #1 selected
    [done] Step 2: Strategy — V3 0.05%, ±15% range designed
    [done] Step 3: Risk — APPROVED (MEDIUM)
    [FAIL] Step 4: Swap — Transaction reverted (insufficient gas)

  Remaining:
    [ ] Step 5: Add liquidity
    [ ] Step 6: Portfolio report

  Recovery Options:
    - Ensure sufficient ETH for gas and retry: "Continue LP workflow"
    - Add liquidity manually with the strategy above: "Add liquidity to WETH/USDC 0.05%"
    - Start over: "Full LP workflow with $X"
```

## 输出格式

### 流程成功完成（所有6个步骤均完成）

```text
Full LP Workflow Complete

  Opportunity: {pool_pair} {fee}% on {chain}
  Strategy:    {version}, {range_width} range, {rebalance_frequency} rebalance
  Risk:        {decision} ({composite_risk})
  Position:    #{position_id} — {status}
  Value:       ${total_value}

  Returns (moderate estimate):
    Fee APY: {fee_apy}%
    Est. IL: {il}%
    Net APY: {net_apy}%

  Cost: ${total_gas} gas across {n} transactions

  Pipeline: Scan -> Strategy -> Risk -> Swap -> Enter -> Confirm (all passed)
```

## 重要说明

- **这是最复杂的智能体协作流程**：它协调了6个智能体的工作，包含2个用户确认环节和条件性代币交换步骤。每个智能体都会收到前一个智能体的所有相关信息。
- **两次明确确认**：在任何代币交换之前以及增加流动性之前，都需要用户的确认。
- **条件性代币交换**：只有当用户持有的代币不符合要求时，才会执行第4步的代币交换；如果用户已经持有所需的代币，则跳过此步骤。
- **链路考虑**：如果扫描所有链路，最佳投资机会可能位于用户资金所在的链路之外。系统应提醒用户并建议使用桥接工具或调整链路筛选条件。
- **gas费用**：在Ethereum网络上，整个流程（包括代币交换和LP投资）的gas费用约为15-50美元。对于小额投资（<1000美元），需提醒用户gas费用会显著影响投资回报。
- **绝不自动执行**：尽管这是一个“自动”流程，但任何涉及用户资金的操作都需要用户的明确确认。

## 错误处理

| 错误类型                | 向用户显示的消息                                      | 建议的操作                                      |
| ---------------------- | ------------------------------------------------------ | ---------------------------------------- |
| 未找到合适的投资机会           | “在{链路}上没有符合您条件的LP投资机会。”                         | 扩大链路筛选范围或降低最低TVL要求                         |
| 机会扫描失败                | “机会扫描失败。无法找到合适的LP投资目标。”                         | 尝试直接使用`scan-opportunities`功能                     |
| LP策略制定失败                | “{投资池}的策略制定失败。保留扫描结果。”                         | 尝试使用`lp-strategy`或`optimize-lp`功能                     |
| 风险评估者否决                | “风险评估被否决：{原因}。当前策略：{总结}。”                         | 选择其他投资机会或调整投资规模                         |
| 代币不足                | “没有足够的{代币}来准备LP投资。您有{X}，但需要{Y}。”                         | 减少资本或获取所需的代币                         |
| 代币交换失败                | “代币交换失败：{原因}。保留策略和风险评估结果。”                         | 重试或手动进行代币交换                         |
| 流动性添加失败                | “添加流动性失败：{原因}。代币仍在您的钱包中。”                         | 重试或直接使用`manage-liquidity`功能                     |
| 投资组合未得到确认              | “投资组合已创建，但尚未在链路上确认。稍后再次检查。”                     | 等待并使用`track-performance`功能进行检查                   |
| 超过安全支出限额              | “{X}的资本超过了{Y}的支出限额。”                         | 减少资本金额或调整安全配置                         |
| 未配置钱包                | “未配置钱包。无法执行交易。”                                 | 使用`setup-agent-wallet`功能配置钱包                     |
| 用户拒绝确认                | “代币交换被取消。保留策略——您可以手动继续操作。”                         | 使用`manage-liquidity`功能进行手动操作                     |
| 用户拒绝确认                | “LP投资被取消。之前的所有研究结果均已展示。”                         | 调整参数后重新尝试                         |