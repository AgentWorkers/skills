---
name: research-and-trade
description: >-
  Research a token and execute a trade if it passes due diligence. Autonomous
  research-to-trade pipeline: researches the token, evaluates risk, and only
  trades if the risk assessment approves. Stops and reports if risk is too high.
  Use when user wants "research X and buy if it looks good" or "due diligence
  then trade."
model: opus
allowed-tools:
  - Task(subagent_type:token-analyst)
  - Task(subagent_type:pool-researcher)
  - Task(subagent_type:risk-assessor)
  - Task(subagent_type:trade-executor)
  - mcp__uniswap__check_safety_status
---

# 研究与交易

## 概述

这是一个自动化的研究到执行流程。该流程无需手动调用四个不同的代理并连接它们的输出结果，而是通过一个命令完成整个专家级的工作流程：研究代币、寻找最佳交易池、评估风险——只有在风险评估通过后，才会执行交易。

**为什么这比单独调用各个代理要好10倍：**

1. **复合上下文**：每个代理都会接收到之前所有代理的累积信息。风险评估者不会孤立地评估交易，而是会结合代币分析师的流动性警告、交易池研究者的深度分析以及具体的交易金额，从而做出更全面的风险评估。
2. **自动风险控制**：在任何阶段，如果出现风险问题，流程会立即停止。这样既不会浪费Gas（交易费用），也不会浪费时间，并且用户会收到详细的解释。
3. **一步完成四步专家级工作流程**：手动协调代币研究、交易池选择、风险评估和交易执行需要大量的时间和专业知识。而这个流程将这一切压缩成一个简单的自然语言指令。
4. **逐步展示结果**：用户可以实时看到每个阶段的分析结果，而不仅仅是最终结果。即使流程在风险评估阶段停止，用户也能获得完整的研究报告。

## 适用场景

当用户说出以下指令时，可以激活该流程：

- “研究UNI代币，如果情况良好就购买”
- “先对AAVE进行尽职调查，然后再进行交易”
- “调查并交易ARB代币”
- “我应该购买LINK代币吗？如果可以，就购买”
- “PEPE代币安全吗？如果安全，就购买500美元的量”
- “研究X代币，评估风险，如果通过就进行交易”
- “自动交易：先研究再执行”
- “查看TOKEN代币，如果风险可接受就购买一些”

**不适用场景**

- 当用户仅需要研究代币而不进行交易时（请使用`research-token`命令）
- 当用户仅需要执行交易而不进行任何研究时（请使用`execute-swap`命令）

## 参数

| 参数                | 是否必填 | 默认值       | 提取方式                                                                                              |
|------------------|--------|------------|-------------------------------------------------------------------------------------------------------------------------|
| token               | 是      | --          | 需要研究的代币："UNI", "AAVE" 或者 0x 地址                                            |
| amount              | 是      | --          | 交易金额："$500", "1 ETH的量", "0.5 ETH"                                                    |
| chain               | 否       | ethereum     | 目标链："ethereum", "base", "arbitrum"                                                    |
| riskTolerance        | 否       | moderate     | "conservative"（保守），"moderate"（中等），"aggressive"（激进）                               |
| action              | 否       | buy         | "buy"（买入代币）或 "sell"（卖出代币）                                                    |
| payWith             | 否       | WETH         | 用于支付的代币："WETH", "USDC"等等                                                    |

如果用户没有提供交易金额，请**询问用户**——切勿自行猜测交易金额。

## 工作流程

```
                          RESEARCH-AND-TRADE PIPELINE
  ┌─────────────────────────────────────────────────────────────────────┐
  │                                                                     │
  │  Step 1: RESEARCH (token-analyst)                                   │
  │  ├── Token metadata, liquidity, volume, risk factors                │
  │  ├── Cross-chain presence                                           │
  │  └── Output: Token Research Report                                  │
  │          │                                                          │
  │          ▼ (feeds into Step 2)                                      │
  │                                                                     │
  │  Step 2: POOL ANALYSIS (pool-researcher)                            │
  │  ├── Find all pools for {token}/{payWith} on {chain}                │
  │  ├── Rank by fee APY, depth, utilization                            │
  │  ├── Analyze depth at trade size (can it handle $X?)                │
  │  └── Output: Pool Research Report + Best Pool Selection             │
  │          │                                                          │
  │          ▼ (feeds into Step 3 with COMPOUND CONTEXT)                │
  │                                                                     │
  │  Step 3: RISK ASSESSMENT (risk-assessor)                            │
  │  ├── Receives: token risks + pool risks + trade size + slippage     │
  │  ├── Evaluates: slippage, liquidity, smart contract, token risk     │
  │  ├── Decision: APPROVE / CONDITIONAL_APPROVE / VETO / HARD_VETO    │
  │  └── Output: Risk Assessment Report                                 │
  │          │                                                          │
  │          ▼ CONDITIONAL GATE                                         │
  │  ┌───────────────────────────────────────────────────┐              │
  │  │  APPROVE         → Proceed to Step 4              │              │
  │  │  COND. APPROVE   → Show conditions, ask user      │              │
  │  │  VETO            → STOP. Show research + reason.  │              │
  │  │  HARD VETO       → STOP. Non-negotiable.          │              │
  │  └───────────────────────────────────────────────────┘              │
  │          │ (only if APPROVE or user confirms CONDITIONAL)           │
  │          ▼                                                          │
  │                                                                     │
  │  Step 4: USER CONFIRMATION                                          │
  │  ├── Present: research summary + risk score + swap quote            │
  │  ├── Ask: "Proceed with this trade?"                                │
  │  └── User must explicitly confirm                                   │
  │          │                                                          │
  │          ▼                                                          │
  │                                                                     │
  │  Step 5: EXECUTE (trade-executor)                                   │
  │  ├── Execute swap through safety-guardian pipeline                  │
  │  ├── Monitor transaction confirmation                               │
  │  └── Output: Trade Execution Report                                 │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
```

### 第1步：研究（代币分析师）

委托给`Task(subagent_type:token-analyst)`，并提供以下信息：

- 代币符号或地址
- 目标链
- 请求：完整的尽职调查报告

**需要传递给代理的信息：**

```
Research this token for a potential trade:
- Token: {token}
- Chain: {chain}
- Trade size: {amount}

Provide a full due diligence report: liquidity across all pools, volume profile
(24h/7d/30d), risk factors, and a trading recommendation with maximum trade size
at < 1% price impact.
```

**完成后的用户展示内容：**

```text
Step 1/5: Token Research Complete

  Token: UNI (Uniswap) on Ethereum
  Total Liquidity: $85M across 24 pools
  24h Volume: $15M | 7d Volume: $95M
  Volume Trend: Stable
  Risk Factors: None significant
  Max Trade (< 1% impact): $2.5M

  Proceeding to pool analysis...
```

**风险检查**：如果代币分析师报告了关键风险因素（总流动性低于10万美元、未找到合适的交易池、代币未通过验证），请向用户展示这些信息，并询问他们是否继续。

### 第2步：交易池分析（交易池研究者）

委托给`Task(subagent_type:pool-researcher)`，并提供代币研究的结果：

```
Find the best pool for trading {token}/{payWith} on {chain}.

Context from token research:
- Total liquidity: {from Step 1}
- Dominant pool: {from Step 1}
- Risk factors: {from Step 1}

Trade details:
- Trade size: {amount}
- Direction: {action} (buying/selling {token})

Analyze all pools for this pair across fee tiers. For each pool, report:
fee APY, TVL, liquidity depth at the trade size, and price impact estimate.
Recommend the best pool for this specific trade.
```

**完成后的用户展示内容：**

```text
Step 2/5: Pool Analysis Complete

  Best Pool: WETH/UNI 0.3% (V3, Ethereum)
  Pool TVL: $42M
  Price Impact: ~0.3% for your trade size
  Fee Tier: 0.3% (3000 bps)

  Proceeding to risk assessment...
```

### 第3步：风险评估（风险评估者）

委托给`Task(subagent_type:risk-assessor)`，并提供来自第1步和第2步的**复合上下文**信息：

```
Evaluate risk for this proposed swap:

Operation: swap {amount} {payWith} for {token}
Pool: {best pool from Step 2}
Chain: {chain}
Risk tolerance: {riskTolerance}

Token research context (from token-analyst):
{Full token research summary from Step 1}

Pool analysis context (from pool-researcher):
{Full pool analysis from Step 2}

Evaluate all applicable risk dimensions: slippage, liquidity, smart contract risk.
Provide a clear APPROVE / CONDITIONAL_APPROVE / VETO / HARD_VETO decision.
```

**风险评估者返回后的处理逻辑：**

| 决策                | 执行动作                                                                                   |
|------------------|----------------------------------------------------------------------------------------|
| **批准**              | 展示风险总结，进入第4步（用户确认）                                                         |
| **有条件批准**          | 显示具体条件（例如：“分成两笔交易”）。询问用户：“接受这些条件吗？”                                      |
| **否决**              | **停止**。展示完整的研究报告、风险评估结果及否决原因。提供替代方案。                                      |
| **绝对否决**            | **停止**。展示原因。这种情况下无法继续进行交易。                                                    |

**向用户展示内容（批准情况）：**

```text
Step 3/5: Risk Assessment Complete

  Decision: APPROVE
  Composite Risk: LOW
  Slippage Risk: LOW (0.3% estimated)
  Liquidity Risk: LOW (pool TVL 840x trade size)
  Smart Contract Risk: LOW (V3, 18-month-old pool)

  Ready for your confirmation...
```

**向用户展示内容（否决情况）：**

```text
Step 3/5: Risk Assessment -- VETOED

  Decision: VETO
  Reason: Price impact of 4.2% exceeds moderate risk tolerance (max 2%)

  Research Summary:
    Token: SMALLCAP ($180K total liquidity)
    Best Pool: WETH/SMALLCAP 1% (V3, $95K TVL)
    Your trade size ($5,000) represents 5.3% of pool TVL

  Suggestions:
    - Reduce trade size to < $1,000 for acceptable slippage
    - Use a limit order instead: "Submit limit order for SMALLCAP"
    - Try a different chain if more liquidity exists elsewhere

  Pipeline stopped. No trade executed.
```

### 第4步：用户确认

在执行任何交易之前，向用户展示清晰的总结，并请求明确确认：

```text
Trade Confirmation Required

  Research: UNI — $85M liquidity, stable volume, no risk factors
  Risk: APPROVED (LOW composite risk)

  Swap Details:
    Sell:  0.5 WETH (~$980)
    Buy:   ~28.5 UNI
    Pool:  WETH/UNI 0.3% (V3, Ethereum)
    Impact: ~0.3%
    Gas:   ~$8 estimated

  Proceed with this trade? (yes/no)
```

**只有在使用者明确确认后，才进入第5步。**

### 第5步：执行交易（交易执行者）

委托给`Task(subagent_type:trade-executor)`，并提供完整的流程上下文：

```
Execute this swap:
- Sell: {amount} {payWith}
- Buy: {token}
- Pool: {best pool address from Step 2}
- Chain: {chain}
- Slippage tolerance: {derived from risk assessment}
- Risk assessment: APPROVED, composite risk {level}

The token has been researched (liquidity: {X}, volume: {Y}) and risk-assessed
(slippage: {Z}, liquidity: {W}). Proceed with execution through the safety pipeline.
```

**展示最终结果：**

```text
Step 5/5: Trade Executed

  Sold:     0.5 WETH ($980.00)
  Received: 28.72 UNI ($985.50)
  Pool:     WETH/UNI 0.3% (V3, Ethereum)
  Slippage: 0.28% (within tolerance)
  Gas:      $7.20
  Tx:       https://etherscan.io/tx/0x...

  ──────────────────────────────────────
  Pipeline Summary
  ──────────────────────────────────────
  Research:  UNI — $85M liquidity, stable, no risk flags
  Pool:      WETH/UNI 0.3% — best depth for trade size
  Risk:      APPROVED (LOW)
  Execution: Success — 28.72 UNI received
  Total cost: $987.20 (trade + gas)
```

## 输出格式

### 流程成功（所有5步都完成）

```text
Research and Trade Complete

  Token: {symbol} ({name}) on {chain}
  Research: {1-line summary from token-analyst}
  Pool: {pool pair} {fee}% ({version}, {chain})
  Risk: {decision} ({composite_risk})

  Trade:
    Sold:     {amount} {payWith} (${usd_value})
    Received: {amount} {token} (${usd_value})
    Impact:   {slippage}%
    Gas:      ${gas_cost}
    Tx:       {explorer_link}

  Pipeline: Research -> Pool -> Risk -> Confirm -> Execute (all passed)
```

### 流程被否决（在风险评估阶段停止）

```text
Research and Trade -- Risk Vetoed

  Token: {symbol} ({name}) on {chain}
  Research: {1-line summary}
  Pool: {best pool found}
  Risk: VETOED — {reason}

  Details:
    {risk dimension scores}

  Suggestions:
    - {mitigation 1}
    - {mitigation 2}

  Pipeline: Research -> Pool -> Risk (VETOED) -- No trade executed.
```

## 重要说明

- **该流程始终会先进行研究**。如果用户只是想快速交易而不进行研究，请引导他们使用`execute-swap`命令。
- **对于绝对否决（HARD_VETO），风险控制是不可协商的**。如果风险评估者发出绝对否决（例如代币未通过验证、交易池的总流动性低于1000美元、价格波动率超过10%），流程将立即停止。用户无法更改这一决定。
- **否决只是提供信息**。对于普通否决，会向用户展示完整的研究报告并解释原因。用户可以选择直接使用`execute-swap`命令自行进行交易，但该流程不会自动执行交易。
- **复合上下文是关键**：风险评估者在拥有代币分析师的风险分析和交易池研究者的深度分析后，其评估效果会大大提升。
- **逐步展示结果**：不要等到流程结束才显示结果。每个代理完成步骤后，都会向用户展示简要总结，让他们了解当前进度。
- **必须提供交易金额**。切勿自行猜测交易金额。如果用户只要求“研究UNI代币”，请询问：“您想购买多少？”

## 错误处理

| 错误类型                | 向用户显示的消息                                                         | 建议的操作                                                                                          |
|------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| 未找到代币            | “在{chain}链上找不到代币{X}。”                                                         | 检查拼写或提供合约地址                                                         |
| 未找到合适的交易池          | “在{chain}链上未找到适用于{token}/{payWith}的交易池。”                                      | 尝试使用其他代币或链         |
| 代币研究失败            | “代币研究失败：{原因}。无法在没有尽职调查的情况下继续。”                                        | 重新尝试或直接使用`research-token`命令         |
| 交易池分析失败            | “交易池分析失败。研究已完成，但未找到最佳交易池。”                                      | 尝试手动选择交易池并执行`execute-swap`命令         |
| 风险评估否决            | “风险评估否决了此次交易：{原因}。”                                                     | 减少交易金额或尝试其他代币/交易池         |
| 绝对否决（HARD_VETO）        | “交易被阻止：{原因}。无论交易金额多少，此次交易都不安全。”                                      | 交易无法进行                                                            |
| 交易执行失败            | “交易执行失败：{原因}。研究数据和风险信息已保存。”                                         | 检查钱包余额和Gas费用；重新尝试                                         |
| 安全检查失败            | “超过了安全限制。请使用`check-safety`命令检查支付限制。”                                      | 等待限制重置或调整限制                                                         |
| 用户拒绝确认            | “交易已取消。研究结果和风险信息已展示供参考。”                                                     | 无需进一步操作                                                         |
| 未配置钱包              | “未配置钱包。无法执行交易。”                                                         | 使用`setup-agent-wallet`命令配置钱包                                         |
| 账户余额不足            | “{payWith}余额不足：当前余额为{X}，需要{Y}。”                                         | 增加余额或购买更多代币                                                         |