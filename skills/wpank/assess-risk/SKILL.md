---
name: assess-risk
description: 对任何拟议的 Uniswap 操作（如交易、流动性提供者（LP）策略、跨链桥接功能或代币交互）进行独立的风险评估。该评估会涵盖滑点风险、非永久性损失风险、流动性风险、智能合约风险以及跨链桥接风险，并给出明确的“批准”（APPROVE）或“否决”（VETO）决策。当用户询问某项操作是否安全或需要风险评估时，可以使用此功能。
model: opus
allowed-tools: [Task(subagent_type:risk-assessor)]
---

# 评估风险

## 概述

该功能为任何提议的Uniswap操作提供独立、多维度的风险评估。它将任务委托给`risk-assessor`代理，该代理会从5个以上维度对风险进行评估，并生成一个综合评分，同时给出“批准（APPROVE）”、“有条件批准（CONDITIONAL_APPROVE）”、“否决（VETO）”或“绝对否决（HARD_VETO）”的决策。

`risk-assessor`是一个**终端节点**——它不会受到其他代理的影响。其评估结果是基于链上数据的，因此是独立且客观的。

## 适用场景

当用户提出以下问题时，应激活此功能：
- “这笔交易安全吗？”
- “将100 ETH兑换成USDC的风险如何？”
- “我应该将资金投入这个流动性池（LP）吗？”
- “将X代币兑换成Y代币的风险有多大？”
- “将代币桥接到Base链安全吗？”
- “使用这个代币进行流动性池操作（LP）的风险如何？”
- “这个代币适合交易吗？”
- “在交易前需要进行风险检查。”

## 参数

| 参数              | 是否必填 | 默认值    | 获取方式                                              |
| ---------------------- | -------- | ---------- | ----------------------------------------------------------- |
| operation       | 是      | —          | 用户想要执行的操作的文字描述                         |
| riskTolerance     | 否       | “conservative”（保守）、“moderate”（中等）、“aggressive”（激进） |

`operation`参数的示例包括：
- 交易操作：例如“在Ethereum网络上将100 ETH兑换成USDC”
- 流动性池操作：例如“向WETH/USDC V3流动性池中注入5万美元（0.05%的份额）”
- 桥接操作：例如“将10 ETH从Ethereum桥接到Base链”
- 代币检查：例如“PEPE代币是否适合交易？”
- 流动性池检查：例如“UNI/WETH流动性池的风险如何？”

## 工作流程

1. **解析用户请求中的操作信息**：
   - 确定操作类型（交易、添加流动性、移除流动性、桥接或代币检查）
   - 涉及的代币
   - 交易金额
   - 链路（Ethereum或其他链）
   - 流动性池（如适用）

2. **委托给`risk-assessor`代理**：使用解析后的操作详情和风险容忍度调用`Task(subagent_type:risk-assessor)`。代理会从以下维度进行评估：
   - **滑点（Slippage）**：交易规模与流动性池中的流动性之间的价格影响
   - **非永久性损失（Impermanent Loss）**：基于代币对波动性的预期非永久性损失（仅针对流动性池操作）
   **流动性（Liquidity）**：当前头寸是否可以平仓？总市值（TVL）与头寸规模的比例
   **智能合约（Smart Contract）**：流动性池的运行时间、Uniswap版本以及智能合约的安全性（如V4版本）
   **桥接（Bridge）**：桥接机制的可靠性及跨链流动性

3. **以清晰的方式呈现评估结果**：包括每个维度的评分以及最终的决策。

## 输出格式

### 评估结果为“批准（APPROVE）”时：

```text
Risk Assessment

  Operation: Swap 100 ETH for USDC on Ethereum
  Risk Tolerance: Moderate
  Decision: APPROVE

  Risk Dimensions:
    Slippage:        LOW  (0.3% price impact — sufficient liquidity)
    Liquidity:       LOW  (TVL 250x trade size — deep pool)
    Smart Contract:  LOW  (V3 pool, 18 months old, battle-tested)
    Bridge:          N/A  (not a cross-chain operation)

  Composite Risk: LOW
  
  Conditions: None — safe to proceed

  HARD VETO Checks:
    ✓ Verified tokens
    ✓ Pool TVL > $1,000
    ✓ Price impact < 10%
```

### 评估结果为“有条件批准（CONDITIONAL_APPROVE）”时：

```text
Risk Assessment

  Operation: LP $50K into NEWTOKEN/WETH 0.3% V4 (Ethereum)
  Risk Tolerance: Conservative
  Decision: VETO

  Risk Dimensions:
    Slippage:        MEDIUM  (1.2% entry impact due to low liquidity)
    Impermanent Loss: HIGH   (>25% annual estimate — extremely volatile pair)
    Liquidity:       HIGH    (TVL only 8x position size — exit risk)
    Smart Contract:  HIGH    (V4 pool with unaudited hook contract)
    Bridge:          N/A

  Composite Risk: HIGH (exceeds conservative tolerance)

  Why VETO:
    - Impermanent loss estimate exceeds 20% annually
    - V4 hook contract is unaudited — elevated smart contract risk
    - Position would represent 12% of pool TVL — concentration risk

  Mitigations (if you still want to proceed):
    - Reduce position size to < 1% of pool TVL ($4,200)
    - Use a wider range to reduce IL exposure
    - Wait for hook contract audit
    - Switch to risk tolerance "aggressive" (not recommended)
```

### 评估结果为“否决（VETO）”时：

```text
Risk Assessment

  Operation: Swap 1000 ETH for SCAMTOKEN
  Decision: HARD VETO (non-overridable)

  HARD VETO Trigger: Unverified token contract
  
  SCAMTOKEN (0x1234...5678) failed verification:
    - Not on any verified token list
    - Contract deployed < 24 hours ago
    - No trading history

  This operation CANNOT proceed regardless of risk tolerance.
  Hard vetoes protect against potential rug pulls and scam tokens.

  Suggestion: Use "research-token SCAMTOKEN" to investigate further.
```

## 重要说明

- `risk-assessor`是一个独立的终端节点，其评估结果不可被其他代理更改。
- **绝对否决（HARD_VETO）**的决定是不可协商的，适用于以下情况：代币未经过验证、流动性池的总市值（TVL）低于1000美元、交易价格的影响超过10%，或桥接金额超过流动性池的承载能力。
- 该功能仅用于风险评估，不执行任何操作。它仅用于提供决策建议。
- 对于流动性池操作（LP），在评估风险时总会同时考虑非永久性损失（IL）这一维度。
- 当数据不足时，`risk-assessor`会默认认为相关维度的风险为“高风险”，而不会进行猜测。

## 错误处理

| 错误类型            | 显示给用户的消息                                      | 建议的操作                                      |
| ----------------------------- | ------------------------------------------------------ | -------------------------------------- |
| 无法解析操作信息       | “需要更多详细信息。您具体打算做什么？”                          | 要求用户详细描述操作内容                         |
| 未找到相关代币        | “无法找到代币X。”                                      | 提供代币的合约地址                             |
| 无法获取流动性池数据     | “无法获取流动性池数据以进行风险分析。”                         | 请稍后再试                         |
| 代理不可用          | “风险评估代理当前不可用。”                                   | 检查代理的配置                         |