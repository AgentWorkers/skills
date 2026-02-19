---
name: cross-chain-arbitrage-cn
description: "跨链套利 | Cross-Chain Arbitrage  
Uniswap 的跨链套利机会 | Uniswap 提供的跨链套利功能  
发现不同链上的价格差异 | Identify price differences across different blockchains  
关键词：跨链（Cross-Chain）、套利（Arbitrage）、Uniswap、套利策略（Arbitrage Strategy）"
metadata:
  openclaw:
    emoji: ⛓️
    fork-of: "https://clawhub.ai"
---## 评估风险，并在有利可图时执行交易  
该技能使用 ERC-7683 标准进行跨链结算。支持仅扫描模式，以便用户在不执行交易的情况下进行研究。  

**模型：opus**  

**允许使用的工具：**  
- `Task(subagent_type:opportunity-scanner)`（机会扫描器）  
- `Task(subagent_type:risk-assessor)`（风险评估器）  
- `Task(subagent_type:cross-chain-executor)`（跨链执行器）  
- `Task(subagent_type:portfolio-analyst)`（投资组合分析师）  
- `mcp__uniswap__check_safety_status`（检查安全状态）  
- `mcp__uniswap__get_agent_balance`（获取账户余额）  

### 跨链套利  

#### 概述  
该技能可自动发现并执行跨链套利机会——即在不同的区块链上查找相同代币的价格差异，并从中获利。它涵盖了整个流程：扫描 11 个区块链上的价格、计算总成本、进行风险评估、通过 ERC-7683 进行跨链交易以及生成利润报告。  

**为何这种方式比手动操作好 10 倍：**  
1. **同时扫描多个区块链的价格**：手动检查以太坊（Ethereum）、Base、Arbitrum、Optimism、Polygon 等 6 个区块链上的 ETH 价格需要耗费大量时间；而机会扫描器能在几秒钟内完成所有链上的扫描。  
2. **详细计算总成本**：套利中最常见的错误是忽略成本。该技能会列出所有成本项目（来源链的气费、桥接费用、目标链的气费以及交易中的滑点），仅展示在扣除所有成本后仍有利润的机会。  
3. **对时间敏感**：套利机会非常短暂，可能瞬间消失。该技能会持续提醒用户这一点，并在机会可能已经消失之前迅速采取行动。  
4. **风险控制**：在执行任何资金转移之前，风险评估器会评估桥接风险、执行风险和流动性风险；如果风险过高，整个流程将被终止。  
5. **仅扫描模式**：如果用户不想立即执行交易，可以选择仅扫描模式，查看现有机会而不投入资金。  

#### 适用场景  
当用户提出以下请求时，可激活该技能：  
- “查找跨链的 ETH 套利机会”  
- “是否存在 WETH 在不同链上的价格差异？”  
- “利用价格差异获利”  
- “在 Base 与 Ethereum 之间进行套利”  
- “是否有 USDC 的套利机会？”  
- “使用 5,000 美元进行跨链套利”  
- “仅扫描套利机会——不执行”（仅扫描模式）  

**不适用场景**  
- 如果用户需要在同一区块链内进行交易（使用 `execute-swap`），或仅需要桥接代币（使用 `bridge-tokens`），或想查看普通的投资组合收益机会（使用 `scan-opportunities` 或 `find-yield`）。  

#### 参数设置  
| 参数          | 是否必填 | 默认值            | 设置方法                                      |  
|---------------|---------|------------------|-----------------------------------------|  
| token         | 否       | 前 5 种常见代币        | 要检查的代币（例如：WETH、USDC，或默认扫描所有代币）         |  
| chains        | 否       | 所有区块链          | 要扫描的区块链列表（例如：all 或 “ethereum, base”）           |  
| minProfit     | 否       | 0.5%            | 所有成本后的最低净利润阈值                         |  
| maxAmount     | 否       | 每次交易的最大资金限额                    |  
| riskTolerance | 否       | “保守”、“中等”或“激进”        | 风险容忍度设置                              |  
| mode          | 否       | “execute”（执行）或 “scan”（仅扫描）            | 执行模式                                   |  

如果 `mode` 设置为 “scan”，或者用户请求 “仅扫描” 或 “不执行”，则跳过步骤 3-4，直接显示机会报告。  

#### 工作流程  
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

### 步骤 0：准备工作  
在开始之前：  
1. 通过 `mcp__uniswap__check_safety_status` 检查安全状态。  
2. 通过 `mcp__uniswap__get_agent_balance` 获取相关区块链上的账户余额。  
3. 如果账户余额不足，停止操作并通知用户。  

### 步骤 1：扫描机会（opportunity-scanner）  
委托 `Task(subagent_type:opportunity-scanner)` 执行机会扫描。  

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

**如果模式为“scan”**，则在此步骤结束。  

### 步骤 2：风险评估（risk-assessor）  
将选定的机会委托给 `Task(subagent_type:risk-assessor)` 进行风险评估。  

**决策流程：**  
| 决策            | 执行操作                                      |                                                                                              |  
|-----------------|--------------------------------------------------|                                                                                             |  
| **批准**          | 显示风险总结，等待用户确认                         |                                                                                              |  
| **条件性批准**      | 显示相关条件（例如：“减少交易金额”），征求用户意见                |                                                                                              |  
| **拒绝**          | 交易风险过高或流动性不足，终止操作                         |                                                                                              |  
| **绝对拒绝**        | 桥接流动性不足或存在重大风险，无法继续                         |                                                                                              |  

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

### 步骤 3：执行交易（cross-chain-executor）  
将交易委托给 `Task(subagent_type:cross-chain-executor)` 执行。  

**执行过程中更新进度：**  
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

### 步骤 4：生成报告（portfolio-analyst）  
将最终结果委托给 `Task(subagent_type:portfolio-analyst)` 进行分析。  

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

#### 输出格式  
- **成功执行**：  
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

- **仅扫描报告**：  
```text
Cross-Chain Arbitrage Scan

  Scanned: {n_tokens} tokens across {n_chains} chains
  Found: {n_opportunities} opportunities (> {minProfit}% net profit)

  {opportunity table}

  To execute: "Cross-chain arb, execute opportunity #N"
```  

- **交易被拒绝**：  
```text
Cross-Chain Arbitrage -- Risk Vetoed

  Opportunity: {token} {source} -> {dest} ({gross_spread}% gross)
  Risk: VETOED — {reason}

  {risk dimension details}

  Pipeline: Scan -> Risk (VETOED) -- No execution.
```  

#### 重要说明：  
- **套利机会具有时效性**：用户查看扫描结果并确认时，价格差异可能已经消失。该技能会明确提醒用户这一点，并不保证一定能获利。  
- **准确计算总成本至关重要**：切勿将未扣除成本的价差直接显示为利润；务必列出并扣除所有相关费用。例如，看似有 0.8% 利润的交易，实际净利润可能只有 0.2%，甚至为负数。  
- **桥接结算时间存在风险**：在 1-10 分钟的结算期间，目标链上的价格可能发生变化，导致利润消失或减少。风险评估器会考虑这一因素。  
- **默认设置为仅扫描模式**：如果用户不确定是否要执行交易，系统会默认使用仅扫描模式；用户之后仍可选择 “执行”。  
- **并非每次扫描都能找到机会**：像 WETH 或 USDC 这样的热门代币，在扣除成本后，价差很少超过 0.5%。请根据实际情况调整预期。  
- **小额交易时气费影响显著**：总成本为 15 美元的交易，如果气费超过 100 美分，几乎无法获利。请对小额交易保持警惕。  
- **套利并非毫无风险**：尽管称为“套利”，但跨链交易仍存在风险（如桥接失败、结算期间价格变动、智能合约风险等）。务必向用户明确说明这些风险。  

#### 错误处理  
| 错误类型          | 显示给用户的消息                                      | 建议的操作                                      |  
|-----------------|--------------------------------------------------|--------------------------------------------------|  
| 未找到套利机会       | “在 {chains} 上未找到净利润超过 {minProfit}% 的套利机会。”           | 调高最低净利润阈值或尝试其他代币                         |  
| 机会已过期        | “扫描后价格差异已消失，机会不再有利可图。”                        | 重新扫描以寻找新的套利机会                         |  
| 风险评估被拒绝       | “风险评估失败：{原因}。”                                      | 尝试减少交易金额或选择其他路径                         |  
| 桥接失败         | “桥接操作失败。资金应留在 {source_chain}。”                        | 检查源链账户余额                         |  
| 桥接延迟         | “桥接结算延迟（实际时间 {elapsed}，预期时间 {expected}）。请稍候。”           | 等待或手动检查订单状态                         |  
| 交易失败         | “在 {source_chain} 未能购买 {token}：{原因}。”                        | 检查账户余额和气费                         |  
| 账户余额不足       | {source_chain} 上的 {token} 数量不足，需要 {Y}。”                   | 减少交易金额或补充资金                         |  
| 超过安全限额       | “交易金额超出安全限制。”                                      | 调整交易金额                         |  
| 未配置钱包         | “未配置用于交易的钱包。”                                      | 使用 `setup-agent-wallet` 设置钱包                         |  
| 用户拒绝确认       | “套利操作已取消。以上为扫描结果供参考。”                         | 无需额外操作                             |  
| 实际利润低于预期       | “由于价格变动，实际利润为 {X}，低于预期 {Y}。”                   | 套利机会具有时效性，实际利润可能低于预期                         |  
| 出现亏损         | “由于结算期间价格变动，本次交易导致亏损 {X}。”                         | 跨链套利存在风险                         |