---
name: chainaware-behavioral-prediction
license: MIT
description: "Use this skill whenever a user asks about wallet safety, fraud risk, rug pull detection,  wallet behavior analysis, DeFi personalization, on-chain reputation scoring, AML checks,  token ranking by holder quality, airdrop screening, lending risk, token launch auditing,  or AI agent trust scoring. Triggers on questions like: is this wallet safe?, will this pool rug pull?, what will this address do next?,  score this wallet, detect fraud for address, personalize my DeFi agent,  rank this token, top AI tokens, best holders of this token,  check this contract, is this token safe?, profile this wallet,  KYC this address, pre-screen this user, AML check this wallet,  is this address suspicious?, screen this wallet before onboarding,  what is the risk score of this address?, analyze on-chain behavior,  is this LP safe to deposit?, will this contract rug?,  what DeFi products suit this wallet?, segment this user,  what is this wallet's experience level?, find strong token holders,  which token has the best community?, rank tokens by holder quality,  should we list this token?, audit this launch, is this deployer trustworthy?,  vet this IDO, launch safety check, screen this airdrop list, filter bots from airdrop,  rank these wallets for token distribution, fair airdrop allocation,  assess this borrower, what collateral ratio for this wallet?, lending risk for 0x...,  what interest rate for this borrower?, should I lend to this wallet?,  screen this AI agent, is this agent wallet safe?, agent trust score for 0x...,  check the feeder wallet for this agent, can I trust this agent?,  route this wallet to onboarding, is this user a beginner?, skip onboarding for this wallet?,  or any request to analyze a blockchain wallet address, smart contract, token, or AI agent  for risk, behavior, intent, community strength, or trustworthiness.  Also use when integrating the ChainAware MCP server into Claude Code, Cursor,  ChatGPT, or any MCP-compatible AI agent framework.
metadata:
  openclaw:
    requires:
      env:
        - CHAINAWARE_API_KEY
    primaryEnv: CHAINAWARE_API_KEY
    env_usage:
      CHAINAWARE_API_KEY: "Passed as the `apiKey` parameter in every tool call (predictive_fraud, predictive_behaviour, predictive_rug_pull).Never logged or included in output. Sourced exclusively from the CHAINAWARE_API_KEY environment variable — never hardcoded."
    data_handling:
      external_endpoints:
        - url: https://prediction.mcp.chainaware.ai/sse
          transport: SSE
          purpose: Blockchain wallet and contract behavioural analysis
          data_sent:
            - Wallet addresses (pseudonymous on-chain identifiers)
            - Smart contract / LP addresses
            - Network identifier (e.g. ETH, BNB, BASE)
          data_NOT_sent:
            - Names, emails, or any off-chain PII
            - Raw transaction data
            - Private keys or seed phrases
          retention: Governed by ChainAware's privacy policy
          privacy_policy: https://chainaware.ai/privacy

    emoji: 🔮
    homepage: https://github.com/ChainAware/behavioral-prediction-mcp
    author: ChainAware
    tags:
      - web3
      - blockchain
      - fraud-detection
      - rug-pull
      - wallet-analytics
      - defi
      - mcp
      - ai-agents
      - personalization
      - aml
      - token-rank
      - on-chain-intelligence
---

# ChainAware行为预测MCP

## 该技能的功能

**ChainAware行为预测MCP**可将任何AI代理连接到持续更新的Web3行为智能层：该层涵盖了**8个区块链**上的**1400多万个钱包账户**，这些数据基于**13亿多个预测性数据点**构建而成。该技能通过一个统一的MCP端点提供以下五项功能：

1. **欺诈检测**——在欺诈行为发生之前进行预测（在ETH网络上准确率约为98%）；
2. **行为分析**——分析钱包的意图、风险承受能力、使用经验以及可能的下一步行动；
3. **抽逃资金检测**——预测智能合约或流动性池是否可能实施抽逃资金操作；
4. **代币排名列表**——根据持有者社区的强大程度对代币进行排名；
5. **单一代币排名**——深入分析单个代币的社区质量和顶级持有者情况。

与仅描述过去事件的区块链取证工具不同，该MCP具有**预测性**——它能告知您的代理**即将发生什么**。

**MCP服务器URL：** `https://prediction.mcp.chainaware.ai/sse`  
**GitHub仓库：** https://github.com/ChainAware/behavioral-prediction-mcp  
**官方网站：** https://chainaware.ai  
**定价/API密钥：** https://chainaware.ai/pricing

---

## 何时使用该技能

- 当用户询问钱包安全性、欺诈风险或可疑活动时；
- 在与钱包、合约或流动性池交互之前，用户希望对其进行筛查时；
- 用户需要对区块链地址进行反洗钱（AML）/合规性检查时；
- 用户需要针对钱包进行行为分析或DeFi个性化处理时；
- 用户想了解代币质量、社区实力或持有者情况时；
- 用户正在构建DeFi平台、AI代理、启动平台或合规性工具时；
- 用户希望将ChainAware MCP集成到自己的代码库中时。

## 何时不使用该技能

- 当用户询问一般的区块链数据（如余额、交易历史）时——使用区块链浏览器；
- 当用户需要实时价格数据或市值信息时——使用市场数据API；
- 当用户需要分析智能合约代码中的错误时——使用代码审计工具；
- 对于需要结合多种工具进行复杂分析（欺诈检测+行为分析+抽逃资金检测）的情况——请联系`chainaware-wallet-auditor`子代理；
- 对于批量筛查多个钱包时——使用`chainaware-fraud-detector`子代理；
- 对于营销个性化需求时——使用`chainaware-wallet-marketer`子代理。

---

## 支持的区块链

| 工具 | 支持的网络 |
|---|---|
| 欺诈检测 | ETH、BNB、POLYGON、TON、BASE、TRON、HAQQ |
| 行为分析 | ETH、BNB、BASE、HAQQ、SOLANA |
| 抽逃资金检测 | ETH、BNB、BASE、HAQQ |
| 代币排名列表 | ETH、BNB、BASE、SOLANA |
| 单一代币排名 | ETH、BNB、BASE、SOLANA |

---

## 分步工作流程

### 钱包欺诈筛查

1. **确认输入**——钱包地址和网络。如果缺少网络信息，请询问用户。
2. 使用钱包地址和网络信息调用`predictive_fraud`函数。
3. 根据下表中的阈值解读`probabilityFraud`结果。
4. 查看`forensic_details`以获取负面标志（如混币器使用、受制裁实体、暗网关联等）。
5. 用通俗语言报告状态、评分及任何取证标志。

### 行为分析/个性化

1. **确认输入**——钱包地址和网络信息。
2. 使用钱包地址和网络信息调用`predictive_behaviour`函数。
3. 提取关键信号：`intention.Value`（交易/质押/桥接/非同质化代币购买概率）、`experience.Value`、`categories`、`recommendation`。
4. 根据主要类别和行为信号对钱包进行分类。
5. 根据分析结果生成个性化建议或下一步最佳行动方案。

### 抽逃资金/合约安全检查

1. **确认输入**——智能合约或流动性池的地址和网络信息。
2. （可选）首先对合约的**部署者**地址调用`predictive_fraud`函数以获取额外信息。
3. 使用合约地址调用`predictive_rug_pull`函数。
4. 解读`probabilityFraud`结果，并查看`forensic_details`中的流动性及合约风险标志。
5. 如果部署者的欺诈评分≥0.5，将整体风险等级提升一级。
6. 附上支持性取证证据报告结果。

### 代币排名/发现

1. 确定请求类型——是列出所有代币还是查询单个代币？
2. 对于列表查询：使用`token_rank_list`函数，并指定`category`、`network`、`sort_by: communityRank`、`sort_order: DESC`。
3. 对于单个代币查询：使用`token_rank_single`函数，并提供`contract_address`和`network`。
4. 报告`communityRank`、`normalizedRank`、`totalHolders`以及顶级持有者信息。

### 完整的尽职调查（多工具组合）

1. 调用`predictive_fraud`函数以获取欺诈评分和取证标志；
2. 调用`predictive_behaviour`函数以获取行为分析结果；
3. （如果涉及合约）调用`predictive_rug_pull`函数以获取合约风险评估；
4. 将这三项结果综合成一个包含风险等级和建议的统一报告。

> 对于复杂的尽职调查流程，请联系`chainaware-wallet-auditor`子代理。

---

## 风险评分阈值

| 评分范围 | 标签 | 建议行动 |
|---|---|---|
| 0.00 – 0.20 | 🟢 低风险 | 可以继续 |
| 0.21 – 0.50 | 🟡 中等风险 | 谨慎操作，持续监控 |
| 0.51 – 0.80 | 🔴 高风险 | 拒绝操作或要求额外验证 |
| 0.81 – 1.00 | ⛔ 极高风险 | 立即拒绝 |

---

## 可用工具

### 1. `predictive_fraud` — 欺诈检测

预测钱包进行欺诈行为的概率。包含反洗钱（AML）检查功能。
**使用场景**：用户在与其交互之前需要筛查钱包。

**输入参数：**
- `apiKey`（字符串，必填）——ChainAware API密钥
- `network`（字符串，必填）——例如 `ETH`、`BNB`、`BASE`
- `walletAddress`（字符串，必填）——要评估的钱包地址

**关键输出字段：**
- `status` — `"Fraud"`、`"Not Fraud"` 或 `"New Address"`
- `probabilityFraud` — 小数范围 0.00–1.00
- `forensic_details` — 详细的链上信息

**示例使用场景：**
- “在以太坊上与0xABC...进行交互安全吗？”
- “这个BNB钱包的欺诈风险是多少？”
- “对这个地址进行反洗钱检查。”
- “在用户加入之前先筛查这个钱包。”
- “这个地址是否在制裁名单上？”
- “预先检查这个用户的钱包是否符合合规要求。”

---

### 2. `predictive_behaviour` — 行为分析及个性化

分析钱包的链上历史并预测其下一步行动。

**输入参数：**
- `apiKey`（字符串，必填）
- `network`（字符串，必填）
- `walletAddress`（字符串，必填）

**关键输出字段：**
- `intention` — 预测的下一步行动（交易/质押/桥接/非同质化代币购买概率）
- `recommendation` — 个性化建议
- `categories` — 行为类别（DeFi贷款者、NFT交易者等）
- `riskProfile` — 风险承受能力和余额使用时长
- `experience` — 经验评分（0–100分，新手到专家）
- `protocols` — 该钱包使用的协议（Aave、Uniswap、GMX等）

**示例使用场景：**
- “这个钱包接下来会做什么？”
- “这个用户是DeFi贷款者还是NFT交易者？”
- “为这个地址推荐最佳的收益策略。”
- “根据这个用户的经验水平个性化我的DeFi代理的响应。”
- “根据这个用户的特征为我的营销活动筛选钱包。”

---

### 3. `predictive_rug_pull` — 抽逃资金检测

预测智能合约或流动性池是否可能实施抽逃资金操作。

**输入参数：**
- `apiKey`（字符串，必填）
- `network`（字符串，必填）
- `walletAddress`（字符串，必填）——智能合约或流动性池的地址

**关键输出字段：**
- `status` — `"Fraud"` 或 `"Not Fraud"`
- `probabilityFraud` — 小数范围 0.00–1.00
- `forensic_details` — 评分背后的链上指标

**示例使用场景：**
- “如果我投入资产，这个新的DeFi池会抽逃资金吗？”
- “这个智能合约安全吗？”
- “检查这个启动平台项目是否合法。”
- “监控这个流动性池的抽逃风险。”
- “这个合约的部署者可信吗？”

---

### 4. `token_rank_list` — 按持有者实力排名代币

根据持有者社区的质量和实力对代币进行排名。

**输入参数：**
- `limit`（字符串，必填）——每页显示的代币数量
- `offset`（字符串，必填）——页码
- `network`（字符串，必填）——`ETH`、`BNB`、`BASE`、`SOLANA`
- `sort_by`（字符串，必填）——例如 `communityRank`
- `sort_order`（字符串，必填）——`ASC` 或 `DESC`
- `category`（字符串，必填）——`AI Token`、`RWA Token`、`DeFi Token`、`DeFAI Token`、`DePIN Token`
- `contract_name`（字符串，必填）——代币名称（空字符串表示无过滤）

**示例使用场景：**
- “以太坊上排名最高的AI代币有哪些？”
- “按社区实力对BNB上的DeFi代币进行排名。”
- “哪些RWA代币在BASE上的持有者基础最强大？”
- “显示以太坊上排名前十的代币。”

---

### 5. `token_rank_single` — 单一代币排名及顶级持有者

根据合约地址返回特定代币的排名和顶级持有者信息。

**输入参数：**
- `contract_address`（字符串，必填）——代币合约或铸造地址
- `network`（字符串，必填）——`ETH`、`BNB`、`BASE`、`SOLANA`

**关键输出字段：**
- `data CONTRACT` — 代币详细信息，包括`communityRank`、`normalizedRank`、`totalHolders`
- `data.topHolders` — 持有者钱包地址及其信息（余额、持有时长、交易次数、总积分、全球排名）

**示例使用场景：**
- “以太坊上USDT的排名是多少？”
- “0xdAC17F...在以太坊上的顶级持有者是谁？”
- “这个合约在BNB上的持有者基础有多强？”
- “显示这个Solana代币的顶级持有者。”

---

## 验证要点

### 输入验证
- ✅ 提供了钱包地址且地址非空
- ✅ 指定的网络被该工具支持（请参考上述表格）
- ✅ 设置了`CHAINAWARE_API_KEY`环境变量
- 对于`token_rank_list`：提供了`limit`、`offset`、`sort_by`、`sort_order`和`category`
- 对于`token_rank_single`：提供了`contract_address`和`network`
- ⚠️ 如果缺少网络信息，请在继续之前询问用户
- ⚠️ 如果请求的工具不支持该网络，请告知用户并建议使用其他工具

### 输出验证
- ✅ `probabilityFraud`字段存在且值在0.00–1.00范围内
- ✅ 风险等级标签正确应用（参见上述表格）
- ✅ 取证标志以通俗语言呈现，而非原始JSON格式
- ✅ 每条建议都指明了具体的判断依据
- ✅ 当工具不支持特定区块链时，会明确说明网络限制
- ✅ 对于行为分析结果，响应中至少包含`intention`、`experience`和`categories`字段

---

## 示例输出

### 欺诈检测 — 以太坊上的0xABC...

### 行为分析 — BASE上的0xDEF...

---

## 集成设置

### Claude代码（CLI）

### Claude Web / Claude桌面应用

1. 转到**设置 → 集成 → 添加集成**
2. 名称：`ChainAware行为预测MCP服务器`
3. URL：`https://prediction.mcp.chainaware.ai/sse?apiKey=your-key-here`

### Claude文档：https://code.claude.com/docs/en/mcp

### Cursor（`mcp.json`）

### ChatGPT连接器

1. 打开**ChatGPT设置 → 应用程序/连接器 → 添加连接器**
2. 名称：`ChainAware行为预测MCP服务器`
3. URL：`https://prediction.mcp.chainaware.ai/sse?apiKey=your-key-here`

### Node.js

### Python

---

## 实际应用场景

### DeFi平台
- **风险调整贷款**——利用欺诈评分和行为分析结果设定抵押要求和利率；
- **流动性管理**——根据意图信号预先配置储备金，防止资金流失；
- **收益路由**——识别寻求高收益的钱包，并将其引导至合适的资金池。

### AI代理个性化
- 为AI代理提供与每个钱包交互时的实时行为分析结果；
- 自动将用户分类为DeFi贷款者、NFT交易者等。

### 欺诈与合规性
- 在用户与Dapp交互之前筛查钱包；
- 对所有活跃钱包进行反洗钱监控；
- 在项目上线阶段检测可能实施抽逃资金的合约。

### NFT与GameFi
- 根据玩家的链上行为历史个性化游戏内经济系统；
- 使用欺诈评分过滤参与NFT活动的机器人钱包和洗钱者。

---

## 成功使用技巧

1. **始终指定网络**——不同区块链上的工具可能有不同的行为表现；
2. **先进行欺诈检测**——在进行任何行为分析之前，先检查欺诈风险；
- **结合多种工具进行全面尽职调查**——欺诈检测、行为分析和抽逃资金检测相结合可获得完整信息；
- **使用部署者风险放大器**——即使合约来自可信的部署者，仍可能存在高风险；
- **批量筛查时**——使用`chainaware-fraud-detector`子代理，而非直接使用本技能；
- **以通俗语言呈现取证结果**——切勿向最终用户返回原始JSON数据。

---

## 相关子代理（Claude代码）

这些子代理位于`.claude/agents/`目录下，提供专门的自动化执行功能：

| 子代理 | 使用场景 |
|---|---|
| `chainaware-wallet-auditor` | 结合所有预测工具进行全面尽职调查 |
| `chainaware-fraud-detector` | 快速欺诈筛查，批量钱包检查 |
| `chainaware-rug-pull-detector` | 检测智能合约/流动性池的安全性及部署者风险 |
| `chainaware-wallet-marketer` | 为不同类型的钱包用户提供个性化营销信息 |
| `chainaware-reputation-scorer` | 给出0–4000的声誉评分 |
| `chainaware-aml-scorer` | 提供0–100的反洗钱合规性评分 |
| `chainaware-trust-scorer` | 提供0.00–1.00的信任评分 |
| `chainaware-wallet-ranker` | 评估钱包的使用体验并生成排行榜 |
| `chainaware-whale-detector` | 对VIP用户进行分级处理 |
| `chainaware-onboarding-router` | 根据用户水平引导钱包的注册流程 |
| `chainaware-token-ranker` | 按持有者社区实力对代币进行排名 |
| `chainaware-token-analyzer` | 详细分析单个代币的社区情况和顶级持有者 |
| `chainaware-defi-advisor` | 根据用户经验和风险等级提供个性化DeFi产品建议 |
| `chainaware-airdrop-screener` | 批量筛查钱包的空气滴落资格，过滤机器人和欺诈行为 |
| `chainaware-lending-risk-assessor` | 评估借款人的风险等级（A–F）、抵押比例和利率 |
| `chainaware-token-launch-auditor` | 对项目上线前的安全性进行审核（批准/有条件/拒绝） |
| `chainaware-agent-screener` | 为AI代理提供0–10的信任评分，包括对代理和关联钱包的欺诈检查 |

---

## 相关阅读资料

| 文章 | 链接 |
|---|---|
| 完整产品指南 | https://chainaware.ai/blog/chainaware-ai-products-complete-guide/ |
| 欺诈检测指南 | https://chainaware.ai/blog/chainaware-fraud-detector-guide/ |
| 抽逃资金检测指南 | https://chainaware.ai/blog/chainaware-rugpull-detector-guide/ |
| 代币排名指南 | https://chainaware.ai/blog/chainaware-token-rank-guide/ |
| 钱包排名指南 | https://chainaware.ai/blog/chainaware-wallet-rank-guide/ |
| 钱包审核指南 | https://chainaware.ai/blog/chainaware-wallet-auditor-how-to-use/ |
| 交易监控指南 | https://chainaware.ai/blog/chainaware-transaction-monitoring-guide/ |
| Web3行为分析指南 | https://chainaware.ai/blog/chainaware-web3-behavioral-user-analytics-guide/ |
| 信用评分指南 | https://chainaware.ai/blog/chainaware-credit-score-the-complete-guide-to-web3-credit-scoring-in-2026/ |
| Prediction MCP开发指南 | https://chainaware.ai/blog/prediction-mcp-for-ai-agents-personalize-decisions-from-wallet-behavior/ |
| Prediction MCP如何提升DeFi平台的效率 | https://chainaware.ai/blog/top-5-ways-prediction-mcp-will-turbocharge-your-defi-platform/ |
| 个性化对AI代理的重要性 | https://chainaware.ai/blog/why-personalization-is-the-next-big-thing-for-ai-agents/ |
| 用于DApp增长的Web3用户细分 | https://chainaware.ai/blog/web3-user-segmentation-behavioral-analytics-for-dapp-growth-2026/ |
| 基于AI的区块链分析 | https://chainaware.ai/blog/ai-powered-blockchain-analysis-machine-learning-for-crypto-security-2026/ |
| 取证分析与基于AI的加密分析对比 | https://chainaware.ai/blog/forensic-crypto-analytics-versus-ai-based-crypto-analytics/ |
| Web3的商业潜力 | https://chainaware.ai/blog/web3-business-potential/ |

---

## 数据与隐私

### 数据传输

每次工具调用会将以下信息发送到`https://prediction.mcp.chainaware.ai/sse`：

| 字段 | 示例 | 备注 |
|---|---|---|
| `walletAddress` | `0xABC...` | 链上匿名标识符，不属于个人身份信息（PII） |
| `network` | `ETH` | 仅表示区块链类型 |
| `apiKey` | `_（你的密钥）` | 来自`CHAINAWARE_API_KEY`环境变量；不会被记录 |

**不传输的信息：**姓名、电子邮件地址、IP地址、原始交易历史或任何链下个人数据。

### API密钥管理

`CHAINAWARE_API_KEY`从环境变量中获取，并作为`apiKey`参数传递给每个工具。该密钥不会被记录在输出中，也不会写入磁盘。请将其视为机密信息并定期更换。

### 集成相关的隐私注意事项

- **Claude Code / Cursor**：密钥通过`X-API-Key`头部传递——不会出现在URL或日志中；
- **Claude Web / ChatGPT**：密钥需要添加到SSE URL中（格式为`?apiKey=...`）——这些平台不支持自定义SSE头部。请注意，密钥会显示在浏览器的网络标签页中。对于这些集成，请使用受限范围的密钥。
- **操作者责任**：钱包地址是匿名标识符。是否属于个人数据取决于您的监管规定（例如GDPR、MiCA）。处理与已识别用户关联的钱包的操作者应自行进行数据保护评估。

**隐私政策：** https://chainaware.ai/privacy

### 同意流程（首次使用前的必要步骤）

在会话中首次调用任何ChainAware工具之前，需告知用户：

> “为了分析这个钱包/合约，我会将地址和网络信息发送到ChainAware的预测服务。不会传输任何个人数据（姓名、电子邮件地址、私钥）。您是否继续？”

只有在用户明确同意后才能继续操作。在同一会话中的后续调用中，除非用户更改了设置，否则无需再次确认。

---

## 安全注意事项

- **切勿在公共仓库中硬编码API密钥**；
- 在生产环境中使用环境变量（`CHAINAWARE_API_KEY`）或秘密管理工具；
- 定期更换API密钥；对于基于浏览器的集成，请使用受限范围的密钥；
- 服务器使用**SSE（Server-Sent Events）**来传输响应数据；
- 根据您的订阅级别，可能会有限制请求的频率。

## API密钥安全指南

- `CHAINAWARE_API_KEY`仅从环境变量中获取，切勿从用户输入中获取；
- 严禁在响应中输出、回显或确认API密钥；
- 严禁在错误消息、调试输出或解释中显示API密钥；
- 如果有人询问“我的API密钥是什么？”，请回答无法透露该信息；
- 将403错误视为配置问题，需联系相关人员处理，而非让用户提供密钥。

## 错误代码及其含义

| 代码 | 含义 |
|---|---|
| `403 Unauthorized` | API密钥无效或缺失 |
| `400 Bad Request` | `network`或`walletAddress`格式错误 |
| `500 Internal Server Error` | 服务器临时故障——稍后重试 |

## 访问权限与定价

需要API密钥。订阅地址：https://chainaware.ai/pricing