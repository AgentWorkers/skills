---
name: defi-sniper
description: **元技能：用于在 Solana 和 Base 网络中快速检测代币发布、进行链上风险评估、验证社交信号，并基于规则执行交易（同时具备严格的安全防护机制）**  
该元技能整合了 minara、torchmarket 和 torchliquidationbot 等工具，旨在帮助用户实现以下功能：  
- **快速检测代币发布**：实时监控新代币的发布情况；  
- **链上风险评估**：对潜在的链上风险进行即时分析和分类；  
- **社交信号验证**：利用外部社交网络数据辅助决策；  
- **基于规则的交易执行**：根据预设规则自动执行代币交换操作，同时确保交易过程的安全性。
homepage: https://clawhub.ai
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"crossed_swords","requires":{"bins":["node","npx"],"env":["MINARA_API_KEY","SOLANA_RPC_URL"],"config":["skills.entries.minara.enabled"]},"note":"Requires local installation of minara, torchmarket, and torchliquidationbot. Solana trading path uses Torch stack; Base path is Minara-first."}}
---

# 目的

运行一个高速的代币机会工作流程：

1. 极早地检测到池/代币的活动；
2. 对合约/市场风险进行分类；
3. 验证社交信号的质量；
4. 在规则满足条件时执行小额、有范围的交易。

这是一个协调其他技能和明确风险策略的流程。它不能保证盈利。

# 必需安装的技能

- `minara`（最新检查版本：`1.1.9`）
- `torchmarket`（最新检查版本：`4.2.7`）
- `torchliquidationbot`（最新检查版本：`3.0.2`）

安装/更新：

```bash
npx -y clawhub@latest install minara
npx -y clawhub@latest install torchmarket
npx -y clawhub@latest install torchliquidationbot
npx -y clawhub@latest update --all
```

# 必需的配置和凭据

最低要求：
- `MINARA_API_KEY`
- `SOLANA_RPC_URL`

根据执行路径的不同：
- Minara 签名者路径：推荐使用 Circle Wallet，或者根据 Minara 文档使用链路的私钥作为备用方案。
- Torch Vault 路径：需要 `VAULT_CREATOR` 和关联的代理钱包来执行 Vault 路由的操作。

在任何实际执行之前，需要进行以下预先检查：
- 明确选择了链（`solana` 或 `base`）
- 确定了资金来源（Vault 或签名者账户）
- 加载了最大风险限制
- 可以进行模拟执行

# 链路感知架构

## Solana 路径（全栈）

使用：
- `minara` 进行检测/意图解析；
- `torchmarket` 获取代币的深度信息、报价以及资金库/借贷状态；
- 可选使用 `torchmarket` 的执行模式（通过 Vault 路由）；
- 使用外部网络搜索进行社交确认。

## Base 路径（受限路径）

使用：
- `minara` 进行检测/意图/交易组装；
- 使用外部网络搜索进行社交确认。

重要注意事项：
- `Torch Market` 和 `Torch Liquidation Bot` 是针对 Solana 设计的，不能假设它们能提供 Base 链原生的代币风险评估功能。

# 输入参数（LM 必须首先收集）

- `target_chain`：`solana` 或 `base`
- `token_symbol_or_mint`
- `max_entry_size`（示例：`1 SOL` 或 Base 链的等价值）
- `max_slippage_bps`（示例：`300`）
- `risk_mode`：`observe`、`paper`、`live`
- `sentiment_min_accounts`（最低可信的、非机器人提及的数量）
- `execution_policy`：`manual-confirm` 或 `auto-with-guardrails`

如果缺少这些参数，则不要执行实际交易。

# 工具职责

## Minara (`minara`）

主要负责检测/情报收集和交换意图的生成：
- 市场聊天/情报分析；
- 生成交换意图的交易；
- 支持在 Solana 和 EVM（包括 Base）上的执行路径；
- 在需要快速解析和交易组装时使用 Minara。

## Torch Market (`torchmarket`）

提供 Solana 原生的深度状态信息：
- 代币发现（`getTokens`）和代币详情（`getToken`）；
- 买卖报价模拟（`getBuyQuote`、`getSellQuote`）；
- 资金库/借贷/持仓上下文（`getLendingInfo`、`getLoanPosition`）；
- 用于构建 Vault 路由交易的工具。

在进入 Solana 主网之前，使用 `torchmarket` 进行链上的结构检查和报价合理性验证。

## Torch Liquidation Bot (`torchliquidationbot`）

专为清算操作设计的执行引擎：
- 持续扫描循环；
- 高速执行 Vault 路由的交易；
- 严格的 Vault 安全限制。

重要注意事项：
- 它是专门为清算流程设计的（`buildLiquidateTransaction` 路径），默认情况下不是用于普通买卖的工具。
- 除非有专门的交换执行器可用，否则不要将其用于其他用途。

# 标准信号链

使用此链来进行启动决策。

## 第 1 阶段：早期机会检测

使用 Minara 的情报来检测潜在的机会并解析交换意图。

所需输出：
- 代币/铸造者的标识符
- 链路
- 如果有的话，初始流动性信号
- 首次检测的时间戳

## 第 2 阶段：链上风险分类

对于 Solana 的候选项目，使用 Torch Market 的状态：
- 代币的状态和储备情况；
- 买卖报价的模拟；
- 相关的资金库和借贷上下文；
- 持有者的集中情况（如果可以通过代币/持有者查询获得）。

风险解读规则：
- 任何单一字段都不能作为完整的判断依据；
- 需要多个独立的指标才能批准交易。

## 第 3 阶段：社交信号确认

使用外部网络搜索工具（这些技能中不包含）来验证是否有真实账户在讨论该代币。

最低检查要求：
- 账户的质量（非简单的关注者/历史信号）
- 消息的多样性（避免重复的机器人垃圾信息）
- 与链上发布时间的时间对齐

## 第 4 阶段：决策矩阵

计算两个判断标准：
- `SecurityGate`：通过/未通过
- `SentimentGate`：通过/未通过

执行规则：
- 只有当两个标准都通过时才执行交易；
- 否则，不进行交易

## 第 5 阶段：执行

如果允许执行：
- 实施持仓上限（例如：1 SOL）
- 实施滑点上限
- 记录交易哈希和理由
- 立即设置交易后的监控条件

# 场景映射（PEPE2.0 在 Solana 上）

对于此技能请求中的场景：

1. Minara 标记一个新的 Solana 代币/池事件及其初始流动性信息。
2. Torch Market 获取代币的详细状态和报价/资金库信息。
3. 通过外部网络搜索（如 X/Twitter）并行进行社交验证。
4. 如果 `SecurityGate=pass` 且 `SentimentGate=pass`，则执行有限额的交易（例如 1 SOL），并设置固定的滑点容忍度。
5. 记录完整的决策过程：信号、检查、最终行动。

# 输出合同

始终返回以下信息：

- `Detection`：
  - 链路、代币 ID、首次检测的时间戳

- `OnChainRisk`：
  - 检查的指标
  - 通过/未通过及其原因

- `SocialSignal`：
  - 来源摘要
  - 通过/未通过及其原因

- `ExecutionDecision`：
  - 是否进行交易
  - 交易金额、滑点、执行路径

- `AuditTrail`：
  - 执行的具体检查
  - 未解决的不确定性

# 风险控制措施

- 绝不要部署无限制的交易金额；始终设置首次交易的金额上限。
- 交易时必须设置滑点限制。
- 不能仅凭炒作就进行交易。
- 不能仅凭一个指标就认为交易是“安全的”。
- 在 `auto-with-guardrails` 模式下，需要预先配置好硬性限制，并在失败时自动终止交易。

# 操作模式

## `observe`

仅进行检测和评分，不进行交易。

## `paper`

进行模拟交易，记录假设的盈亏。

## `live`

只有在通过预先检查和风险控制后才能进行实际交易。

# 失败处理

- 如果缺少关键参数/配置/环境变量：停止操作，并列出缺失的项。
- 如果检测到的风险数据不足：降级为 `observe` 模式。
- 如果无法获取情感分析来源：需要手动确认或拒绝交易。
- 如果在选定的链路上无法执行交易：返回明确的兼容性不匹配信息。

# 来自上游技能的已知限制

- `minara` 的文档描述了意图解析和交易组装的功能，但在提供的 `SKILL.md` 中没有提供专门的“mempool scanner”端点。
- `torchmarket` 提供了丰富的 Solana 代币/资金库/借贷状态和报价信息，但没有内置的“honeypot/rug score”标志。
- `Torch Liquidation Bot` 是专为清算设计的；将其作为通用交换执行器使用是一种非原生的使用方式。
- 社交信号检查需要依赖外部网络搜索技能。

请将这些限制作为最终操作结果的必报内容。