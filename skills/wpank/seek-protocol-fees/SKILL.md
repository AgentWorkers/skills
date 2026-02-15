---
name: seek-protocol-fees
description: >-
  Analyze TokenJar profitability and optionally execute a Firepit burn-and-claim.
  Autonomous pipeline: checks balances, prices assets, calculates profit vs.
  4,000 UNI burn cost, simulates, and executes if profitable. Default is
  preview-only. Use when user asks "Is the TokenJar profitable?", "Execute a
  burn", or "Claim protocol fees."
model: opus
allowed-tools:
  - Task(subagent_type:protocol-fee-seeker)
  - Task(subagent_type:safety-guardian)
  - mcp__uniswap__get_tokenjar_balances
  - mcp__uniswap__get_firepit_state
  - mcp__uniswap__get_agent_balance
---

# 获取协议费用

## 概述

这是一个用于处理Uniswap协议费用系统的自动化流程：TokenJar（地址：`0xf38521f130fcCF29dB1961597bc5d2B60F995f85`）会收集来自V2、V3、V4、UniswapX和Unichain的费用。Firepit（地址：`0x0D5Cd355e2aBEB8fb1552F56c965B867346d6721`）允许任何人通过燃烧4,000个UNI来释放这些累积的资产。当TokenJar的资产价值超过燃烧成本加上Gas费用时，就会出现盈利机会。

该工具可以通过一个命令完成整个流程：检查余额、计算资产价格、计算盈利能力、模拟燃烧过程，并且只有在用户明确同意的情况下才会执行实际的燃烧操作。

**为什么这个工具比单独使用各个工具要好10倍：**

1. **将9个步骤压缩为一个命令**：如果没有这个工具，用户需要手动检查TokenJar的余额、将每种代币的价格转换为美元、检查Firepit的阈值、根据当前价格计算UNI的燃烧成本、估算Gas费用、确定净利润、选择最佳资产、模拟燃烧过程，最后才能执行燃烧操作。而这个工具可以自动完成这些步骤，并在每个步骤之间保持数据的一致性。
2. **安全防护机制**：默认模式下仅提供预览功能（`auto-execute: false`）。即使启用了执行功能，系统也会先进行模拟，通过“安全守护者”（safety-guardian）进行验证，并检查nonce值的有效性，以防止竞态条件（race conditions）——这些在手动使用工具时很容易被忽略。
3. **盈利报告**：输出的是结构化的盈利报告，而不是来自6个不同工具的原始JSON数据。用户可以一目了然地看到总价值、燃烧成本、Gas费用、净利润、投资回报率（ROI）以及每种资产的详细情况。
4. **燃烧后的转换**：用户可以选择在同一流程中将获得的代币转换为稳定币（stablecoins），从而计算出转换后的实际净利润。

## 使用场景

当用户提出以下问题时，可以使用此工具：
- “燃烧TokenJar是否有盈利？”
- “检查协议费用的盈利能力”
- “执行Firepit的燃烧操作”
- “燃烧UNI并领取协议费用”
- “TokenJar里有多少资产？燃烧是否值得？”
- “从TokenJar中领取费用”
- “获取协议费用”
- “运行燃烧和领取费用的流程”

**注意不要使用的情况**：
- 如果用户只是想监控费用积累情况（请使用`monitor-tokenjar`），或者需要历史燃烧数据分析（请使用`analyze-burn-economics`）。

## 参数

| 参数          | 是否必填 | 默认值          | 获取方式                                                         |
| -------------- | -------- | ---------------- | --------------------------------------------------------------------- |
| chain          | 否       | ethereum         | TokenJar和Firepit始终使用Ethereum主网                         |
| auto-execute   | 否       | false            | 如果选择“执行燃烧”或“领取费用”，则设置为true；选择“检查”或“预览”则设置为false |
| post-burn-swap | 否       | false            | 如果选择“转换为稳定币”或“兑换为USDC”，则设置为true                     |
| recipient      | 否       | 连接的钱包         | 如果提供了具体地址，则使用该地址；否则使用代理的钱包                         |

如果用户的意图不明确（是预览还是执行），**系统将默认显示预览结果**，并在执行任何操作前要求用户明确确认。

## 工作流程

```
                        SEEK-PROTOCOL-FEES PIPELINE
  ┌─────────────────────────────────────────────────────────────────────┐
  │                                                                     │
  │  Step 1: PRE-FLIGHT (direct MCP calls)                              │
  │  ├── get_tokenjar_balances — what's in the jar?                     │
  │  ├── get_firepit_state — threshold, nonce, readiness                │
  │  ├── get_agent_balance — does agent have enough UNI?                │
  │  └── Gate: if jar empty or no UNI → STOP immediately               │
  │          │                                                          │
  │          ▼ (all pre-flight data feeds into Step 2)                  │
  │                                                                     │
  │  Step 2: PROFITABILITY ANALYSIS (protocol-fee-seeker)               │
  │  ├── Price all TokenJar assets in USD                               │
  │  ├── Calculate: burn cost + gas cost vs. jar value                  │
  │  ├── Select optimal assets to claim                                 │
  │  ├── Determine net profit and ROI                                   │
  │  └── Output: Profitability Report                                   │
  │          │                                                          │
  │          ▼ PROFITABILITY GATE                                       │
  │  ┌───────────────────────────────────────────────────┐              │
  │  │  PROFITABLE     → Present report, proceed         │              │
  │  │  NOT PROFITABLE → Present report, STOP            │              │
  │  │  MARGINAL       → Present report, warn user       │              │
  │  └───────────────────────────────────────────────────┘              │
  │          │ (only if profitable)                                     │
  │          ▼                                                          │
  │                                                                     │
  │  Step 3: USER CONFIRMATION                                          │
  │  ├── If auto-execute: false → present report, ask user              │
  │  ├── If auto-execute: true → present report, proceed                │
  │  └── User must explicitly confirm before UNI is burned              │
  │          │                                                          │
  │          ▼                                                          │
  │                                                                     │
  │  Step 4: SIMULATE + EXECUTE (protocol-fee-seeker)                   │
  │  ├── execute_burn(simulate=true) — dry run                          │
  │  ├── safety-guardian validates transaction                          │
  │  ├── Nonce freshness check (race condition protection)              │
  │  ├── execute_burn(simulate=false) — broadcast                       │
  │  └── Wait for confirmation                                          │
  │          │                                                          │
  │          ▼                                                          │
  │                                                                     │
  │  Step 5: POST-BURN REPORT                                           │
  │  ├── Show received tokens with USD values                           │
  │  ├── If post-burn-swap: convert to stablecoins                      │
  │  ├── Calculate final net profit after all costs                     │
  │  └── Recommend next burn timing                                     │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
```

### 第1步：预检查（直接调用MCP）

在调用代理之前，同时执行三个MCP调用以快速评估可行性：
1. 调用`mcp__uniswap__get_tokenjar_balances`获取TokenJar的当前余额。
2. 调用`mcp__uniswap__get_firepit_state`获取Firepit的阈值、nonce值以及钱包的准备状态。
3. 调用`mcp__uniswap__get_agent_balance`检查代理的UNI余额。

**异常处理**（如果任何步骤失败，立即停止流程）：
| 检查项                        | 条件                                      | 失败时的处理方式                                                    |
| ---------------------------- | ------------------------------------------- | ------------------------------------------------------------------- |
| TokenJar为空               | 所有余额均为零                             | “TokenJar为空，无法领取费用。”                                      |
| 代理的UNI不足                | UNI余额低于阈值（4,000 UNI）                         | “UNI不足：当前有{X}个，需要{threshold}个UNI，请先获取足够的UNI。”            |
| Firepit未准备好             | 合同状态显示未准备好                         | “Firepit合约未准备好：原因：{reason}。”                                   |

**预检查完成后向用户展示结果：**

```text
Step 1/5: Pre-Flight Complete

  TokenJar: 6 tokens detected (WETH, USDC, USDT, DAI, WBTC, UNI)
  Firepit: Threshold 4,000 UNI | Nonce: 42
  Agent UNI Balance: 5,200 UNI (sufficient)

  Analyzing profitability...
```

### 第2步：盈利能力分析（protocol-fee-seeker）

将所有预检查数据传递给`Task(subagent_type:protocol-fee-seeker)`进行计算：

```
Analyze the profitability of a Firepit burn-and-claim.

Pre-flight data:
- TokenJar balances: {from Step 1 — full balance data}
- Firepit state: threshold={threshold} UNI, nonce={nonce}
- Agent UNI balance: {balance}

Tasks:
1. Price every TokenJar asset in USD using get_token_price.
2. Calculate UNI burn cost: {threshold} UNI * current UNI price.
3. Estimate gas cost for the burn transaction using get_gas_price.
4. Calculate net profit: total_jar_value - (UNI_cost + gas_cost).
5. Select optimal assets to claim (highest value, exclude LP tokens, up to maxReleaseLength).
6. Provide a clear PROFITABLE / NOT_PROFITABLE / MARGINAL verdict.

Return a structured profitability report with per-asset breakdown.
```

**分析完成后向用户展示结果：**

```text
Step 2/5: Profitability Analysis Complete

  TokenJar Value:  $52,000
  ┌─────────────────────────────────────────────┐
  │  WETH     7.20    $18,000   (34.6%)         │
  │  USDC     15,000  $15,000   (28.8%)         │
  │  USDT     8,500   $8,500    (16.3%)         │
  │  WBTC     0.08    $6,400    (12.3%)         │
  │  DAI      4,100   $4,100    (7.9%)          │
  └─────────────────────────────────────────────┘

  Burn Cost:
    UNI burn:  4,000 UNI ($28,000)
    Gas:       ~$45
    Total:     $28,045

  Net Profit:  $23,955
  ROI:         85.4%
  Verdict:     PROFITABLE
```

**如果分析结果显示无盈利：**

```text
Step 2/5: Profitability Analysis Complete

  TokenJar Value:  $18,000
  Burn Cost:       $28,045 (4,000 UNI + gas)
  Net Profit:      -$10,045
  Verdict:         NOT PROFITABLE

  The TokenJar value ($18,000) does not cover the burn cost ($28,045).
  Estimated time to profitability: ~1.4 days (at $7,400/day accumulation rate).

  Pipeline stopped. No burn executed.
```

### 第3步：用户确认

如果燃烧操作是有盈利的，并且`auto-execute`设置为`false`（默认值），则向用户展示完整的盈利报告并请求明确确认：

```text
Burn Confirmation Required

  TokenJar Value:  $52,000 (5 assets)
  Burn Cost:       $28,045 (4,000 UNI + $45 gas)
  Net Profit:      $23,955 (85.4% ROI)

  Assets to Claim: WETH, USDC, USDT, WBTC, DAI
  Post-Burn Swap:  {Yes — convert to USDC | No — keep as received}

  This will permanently burn 4,000 UNI. Proceed? (yes/no)
```

**只有在使用者明确确认后，才继续执行第4步。** 如果`auto-execute`设置为`true`，仍然会展示报告，但会直接执行燃烧操作。

### 第4步：模拟 + 执行（protocol-fee-seeker）

将执行流程委托给`Task(subagent_type:protocol-fee-seeker)`：

```
Execute the Firepit burn-and-claim.

Profitability analysis (from Step 2):
{Full profitability report}

Selected assets: {asset list from Step 2}
Nonce at analysis time: {nonce from Step 1}

Execute the following sequence:
1. Simulate: execute_burn(simulate=true) with the selected assets.
2. If simulation succeeds, delegate to safety-guardian for transaction validation.
3. Nonce freshness check: re-read Firepit state. If nonce has changed, ABORT (race condition).
4. Execute: execute_burn(simulate=false) to broadcast.
5. Wait for transaction confirmation.

If any step fails, report the failure point and do not proceed.
```

**执行过程中向用户展示进度：**

```text
Step 4/5: Executing Burn

  Simulation:     SUCCESS
  Safety Check:   APPROVED by safety-guardian
  Nonce Check:    Fresh (42 — unchanged)
  Broadcasting... confirmed in block 19,500,000

  Tx: https://etherscan.io/tx/0xabcd...1234
```

**如果检测到竞态条件：**

```text
Step 4/5: Execution ABORTED — Race Condition

  Nonce changed: was 42, now 43.
  Another searcher burned before us. TokenJar balances have changed.

  Returning to profitability analysis with fresh data...
```

### 第5步：燃烧后的结果报告

**向用户展示最终结果：**

```text
Step 5/5: Burn Complete

  Burned:    4,000 UNI ($28,000)
  Gas:       $45
  Received:
    WETH     7.20    $18,000
    USDC     15,000  $15,000
    USDT     8,500   $8,500
    WBTC     0.08    $6,400
    DAI      4,100   $4,100

  Gross Value:  $52,000
  Total Cost:   $28,045
  Net Profit:   $23,955 (85.4% ROI)
  Tx:           https://etherscan.io/tx/0xabcd...1234

  ──────────────────────────────────────
  Next Burn Estimate
  ──────────────────────────────────────
  Accumulation Rate: ~$7,400/day
  Est. Next Profitable Burn: ~3.8 days
```

**如果`post-burn-swap`设置为`true`，则添加转换细节：**

```text
  Post-Burn Conversions:
    WETH  → 17,950 USDC  (0.28% slippage)
    WBTC  → 6,380 USDC   (0.31% slippage)
    USDT  → 8,495 USDC   (0.06% slippage)
    DAI   → 4,098 USDC   (0.05% slippage)

  Final USDC Balance: 51,923 USDC
  Conversion Costs:   $77
  True Net Profit:    $23,878 (after all costs)
```

## 输出格式

### 预览模式（默认）

```text
Protocol Fee Analysis

  TokenJar Value:  ${total_value} ({num_assets} assets)
  ┌──────────────────────────────────────┐
  │  {token}  {balance}  ${value}  ({%}) │
  │  ...                                 │
  └──────────────────────────────────────┘

  Burn Cost:   ${uni_cost} ({threshold} UNI) + ${gas} gas = ${total_cost}
  Net Profit:  ${net_profit}
  ROI:         {roi}%
  Verdict:     {PROFITABLE | NOT_PROFITABLE | MARGINAL}

  {if profitable: "Ready to execute. Say 'burn it' to proceed."}
  {if not profitable: "Est. time to profitability: {days} days."}
```

### 执行模式

```text
Protocol Fee Burn Complete

  Burned:     {threshold} UNI (${uni_cost})
  Gas:        ${gas_cost}
  Received:   {num_assets} assets worth ${gross_value}
  Net Profit: ${net_profit} ({roi}% ROI)
  Tx:         {explorer_link}

  Pipeline: Pre-flight -> Analysis -> Confirm -> Simulate -> Execute (all passed)
```

## 重要说明：

- **默认情况下仅提供预览功能。** 除非用户明确启用执行，否则该工具不会燃烧UNI。这是一个具有破坏性的、不可逆的操作——4,000个UNI将被发送到一个无法使用的地址。
- **仅支持Ethereum主网。** TokenJar和Firepit合约部署在Ethereum主网上。`chain`参数的存在是为了未来的兼容性，但目前仅支持`ethereum`主网。
- **竞态条件是真实存在的。** 其他工具也会监控同一个TokenJar。在执行前检查nonce值的有效性非常重要；如果在分析和执行之间有其他燃烧操作发生，系统会安全地中止流程。
- **UNI一旦燃烧将无法恢复。** 与可以重新交易的Swap操作不同，UNI的燃烧是不可逆的。工具会在确认步骤中明确告知用户这一点。
- **主网上的Gas费用至关重要。** Ethereum的Gas费用会显著影响盈利能力。系统会在分析中考虑当前的Gas价格，并在利润空间较小时建议用户等待更低的Gas费用。
- **默认情况下排除LP代币。** TokenJar中的一些资产可能是需要额外赎回的LP代币。除非另有指示，否则系统会自动排除这些代币。

## 错误处理

| 错误类型                        | 向用户显示的消息                                      | 建议的操作                                      |
| ---------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------- |
| TokenJar为空               | “TokenJar为空，无法领取费用。”                                      | 等待费用积累足够后再尝试                              |
| UNI不足                         | “UNI不足：当前有{X}个，需要{threshold}个UNI。”                        | 获取足够的UNI或等待价格下降                              |
| 无盈利                         | “燃烧操作无盈利：TokenJar的价值{X}低于燃烧成本{Y}。”                        | 等待更多费用积累后再尝试                              |
| 模拟失败                         | “燃烧模拟失败：原因：{reason}。”                                  | 重新检查Firepit的状态并重试                              |
| 安全检查失败                         | “安全验证拒绝执行燃烧操作：原因：{reason}。”                           | 重新检查安全配置                                  |
| 检测到竞态条件                     | “其他工具先进行了燃烧操作，nonce值从{X}变为{Y}。”                         | 用新的数据重新运行模拟                              |
| 交易被撤销                         | “燃烧交易被撤销：原因：{reason}。”                                  | 检查Gas费用、nonce值和Firepit的状态                         |
| 未配置钱包                         | “未配置钱包，无法执行燃烧操作。”                                  | 使用`setup-agent-wallet`工具配置钱包                         |
| 燃烧后的转换失败                     | “燃烧操作成功，但{token}的转换失败：原因：{reason}。”                        | 手动通过`execute-swap`进行转换                         |
| Gas费用突然上涨                     | “Gas费用升高（{gas}），当前燃烧操作勉强有利可图。”                         | 等待Gas费用降低或接受较低的利润                         |