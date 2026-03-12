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
      CHAINAWARE_API_KEY: " Passed as the `apiKey` parameter in every tool call (predictive_fraud, predictive_behaviour, predictive_rug_pull).Never logged or included in output. Sourced exclusively from the CHAINAWARE_API_KEY environment variable — never hardcoded."
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
      user_consent_note: "Users should be informed that wallet addresses submitted for analysis are transmitted to ChainAware's servers. Wallet addresses are pseudonymous blockchain identifiers and do not constitute personal data under most jurisdictions, but operators should assess their own regulatory context."
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

# ChainAware 行为预测 MCP

## 该技能的功能

**ChainAware 行为预测 MCP** 将任何 AI 代理连接到持续更新的网络3行为智能层：该层涵盖了 **8 个区块链** 上的 **1400 万个钱包账户**，这些数据基于 **13 亿多个预测数据点** 构建而成。通过一个统一的 MCP 端点，它提供以下五项功能：

1. **欺诈检测** — 在欺诈行为发生之前进行预测（在 ETH 上的准确率约为 98%）；
2. **行为分析** — 分析钱包的意图、风险承受能力、使用经验以及下一步可能采取的行动；
3. **拉盘检测** — 预测智能合约或流动性池是否可能进行拉盘操作；
4. **代币排名列表** — 根据持有者社区的强度对代币进行排名；
5. **单一代币排名** — 深入分析单个代币的社区质量和顶级持有者。

与仅描述过去事件的传统区块链分析工具不同，该 MCP 具有 **预测性** — 它能够告知您的代理 **即将发生什么**。

**MCP 服务器地址：** `https://prediction.mcp.chainaware.ai/sse`  
**GitHub：** https://github.com/ChainAware/behavioral-prediction-mcp  
**官方网站：** https://chainaware.ai  
**定价 / API 密钥：** https://chainaware.ai/pricing

---

## 何时使用该技能

- 当用户询问钱包安全性、欺诈风险或可疑活动时；
- 当用户希望在与其交互之前对钱包、合约或流动性池进行筛查时；
- 当用户需要对区块链地址进行反洗钱（AML）/合规性检查时；
- 当用户需要对钱包进行行为分析或个性化设置时；
- 当用户询问代币质量、社区强度或持有者信息时；
- 当用户正在构建 DeFi 平台、AI 代理或合规性工具时；
- 当用户希望将 ChainAware MCP 集成到他们的代码库中时。

## 何时不使用该技能

- 当用户询问一般的区块链数据（如余额、交易历史）时 — 请使用区块链浏览器；
- 当用户需要实时价格数据或市值信息时 — 请使用市场数据 API；
- 当用户需要分析智能合约代码中的错误时 — 请使用代码审计工具；
- 对于需要结合多种工具进行复杂分析的情况（欺诈 + 行为 + 拉盘操作） — 请升级到 `chainaware-wallet-auditor` 子代理；
- 对于批量筛查多个钱包时 — 请使用 `chainaware-fraud-detector` 子代理；
- 当用户需要个性化营销信息时 — 请使用 `chainaware-wallet-marketer` 子代理。

---

## 支持的区块链

| 工具 | 支持的网络 |
|---|---|
| 欺诈检测 | ETH, BNB, POLYGON, TON, BASE, TRON, HAQQ |
| 行为分析 | ETH, BNB, BASE, HAQQ, SOLANA |
| 拉盘检测 | ETH, BNB, BASE, HAQQ |
| 代币排名列表 | ETH, BNB, BASE, SOLANA |
| 单一代币排名 | ETH, BNB, BASE, SOLANA |

---

## 逐步工作流程

### 对钱包进行欺诈筛查

1. **确认输入** — 钱包地址和网络。如果缺少网络信息，请询问用户。
2. 使用钱包地址和网络调用 `predictive_fraud`。
3. 根据下面的阈值表解释 `probabilityFraud` 的结果。
4. 查看 `forensic_details` 以识别负面标志（如混合器使用、受制裁实体、暗网交易等）。
5. 用通俗的语言报告状态、评分以及任何相关的欺诈标志。

### 进行行为分析/个性化设置

1. **确认输入** — 钱包地址和网络。
2. 使用钱包地址和网络调用 `predictive_behaviour`。
3. 提取关键信息：`intention.Value`（交易/质押/桥接/购买 NFT 的概率）、`experience.Value`、`categories`、`recommendation`。
4. 根据主要类别和意图信号对钱包进行分类。
5. 根据分析结果生成个性化的建议或下一步最佳行动。

### 进行拉盘/合约安全检查

1. **确认输入** — 智能合约或流动性池的地址和网络。
2. （可选）首先对合约的 **部署者** 地址调用 `predictive_fraud` 以获取额外信息。
3. 使用合约地址调用 `predictive_rug_pull`。
4. 解释 `probabilityFraud` 的结果，并查看 `forensic_details` 以识别流动性风险和合约风险。
5. 如果部署者的欺诈评分 ≥ 0.5，则将整体风险提升一个等级。
6. 附带相关证据报告结果。

### 进行代币排名/发现

1. **确定需求** — 是要列出所有代币还是仅分析单个代币？
2. **对于列表请求**：使用适当的 `category`、`network`、`sort_by: communityRank`、`sort_order: DESC` 调用 `token_rank_list`。
3. **对于单个代币**：使用 `contract_address` 和 `network` 调用 `token_rank_single`。
4. 报告 `communityRank`、`normalizedRank`、`totalHolders` 以及顶级持有者的信息。

### 完整的尽职调查（多工具组合）

1. 调用 `predictive_fraud` 以获取欺诈评分和欺诈标志；
2. 调用 `predictive_behaviour` 以获取行为分析和意图；
3. （如果涉及合约地址）调用 `predictive_rug_pull` 以获取合约风险；
4. 将这三项结果综合起来，给出包含风险等级和建议的统一结论。

> 对于复杂的尽职调查流程，请升级到 `chainaware-wallet-auditor` 子代理。

---

## 风险评分阈值

| 评分范围 | 标签 | 建议行动 |
|---|---|---|
| 0.00 – 0.20 | 🟢 低风险 | 可以安全操作 |
| 0.21 – 0.50 | 🟡 中等风险 | 谨慎操作并持续监控 |
| 0.51 – 0.80 | 🔴 高风险 | 立即阻止或要求额外验证 |
| 0.81 – 1.00 | ⛔ 极高风险 | 立即拒绝 |

---

## 可用的工具

### 1. `predictive_fraud` — 欺诈检测

预测钱包进行欺诈行为的概率。包括反洗钱（AML）检查。
**使用场景**：用户在与其交互之前需要对钱包进行筛查。

**输入参数：**
- `apiKey`（字符串，必填）— ChainAware API 密钥
- `network`（字符串，必填）— 例如 `ETH`、`BNB`、`BASE`
- `walletAddress`（字符串，必填）— 需要评估的钱包地址

**关键输出字段：**
- `status` — `"Fraud"`、"`Not Fraud"` 或 `"New Address"`
- `probabilityFraud` — 小数范围 0.00–1.00
- `forensic_details` — 详细的链上信息

**示例请求：**
- *"在以太坊上与 0xABC... 交互安全吗？"
- *"这个 BNB 钱包的欺诈风险是多少？"
- *"对这个地址进行反洗钱检查。"
- *"在用户加入之前先对这个钱包进行筛查。"
- *"这个地址是否在制裁名单上？"
- *"对用户的钱包进行合规性检查。"

---

### 2. `predictive_behaviour` — 行为分析 & 个性化设置

分析钱包的链上历史并预测其下一步行动。

**输入参数：**
- `apiKey`（字符串，必填）
- `network`（字符串，必填）
- `walletAddress`（字符串，必填）

**关键输出字段：**
- `intention` — 预测的下一步行动（交易/质押/桥接/购买 NFT 的概率）
- `recommendation` — 个性化建议
- `categories` — 行为类别（DeFi 借贷者、NFT 交易者、桥接用户等）
- `riskProfile` — 风险承受能力和余额使用时间
- `experience` — 经验评分（0–100 分，新手到专家）
- `protocols` — 该钱包使用的协议（Aave、Uniswap、GMX 等）

**示例请求：**
- *"这个钱包接下来会做什么？"
- *"这个用户是 DeFi 借贷者还是 NFT 交易者？"
- *"为这个地址推荐最佳收益策略。"
- *"根据这个用户的经验水平个性化我的 DeFi 代理的响应。"
- *"为我的营销活动对钱包进行分类。"

---

### 3. `predictive_rug_pull` — 拉盘检测

预测智能合约或流动性池是否可能进行拉盘操作。

**输入参数：**
- `apiKey`（字符串，必填）
- `network`（字符串，必填）
- `walletAddress`（字符串，必填）— 智能合约或流动性池的地址

**关键输出字段：**
- `status` — `"Fraud"` 或 `"Not Fraud"`
- `probabilityFraud` — 小数范围 0.00–1.00
- `forensic_details` — 评分背后的链上指标

**示例请求：**
- *"如果我投入资产，这个新的 DeFi 流动性池会进行拉盘操作吗？"
- *"这个智能合约安全吗？"
- *"检查这个启动平台项目是否合法。"
- *"监控这个流动性池的位置是否存在拉盘风险。"
- *"这个合约的部署者可信吗？"

---

### 4. `token_rank_list` — 按持有者强度对代币进行排名

根据持有者社区的质量和强度对代币进行排名。

**输入参数：**
- `limit`（字符串，必填）— 每页显示的条目数量
- `offset`（字符串，必填）— 页码
- `network`（字符串，必填）— `ETH`、`BNB`、`BASE`、`SOLANA`
- `sort_by`（字符串，必填）— 例如 `communityRank`
- `sort_order`（字符串，必填）— `ASC` 或 `DESC`
- `category`（字符串，必填）— `AI Token`、`RWA Token`、`DeFi Token`、`DeFAI Token`、`DePIN Token`
- `contract_name`（字符串，必填）— 代币名称（空字符串表示无过滤）

**示例请求：**
- *"以太坊上排名最高的 AI 代币有哪些？"
- *"按社区强度对 BNB 上的 DeFi 代币进行排名。"
- *"哪些 RWA 代币在 BASE 上的持有者基础最强大？"
- *"显示以太坊上排名前 10 的代币。"
- *"比较 Solana 和以太坊上的 DePIN 代币。"

---

### 5. `token_rank_single` — 单一代币排名及顶级持有者

根据合约地址返回特定代币的排名和顶级持有者信息。

**输入参数：**
- `contract_address`（字符串，必填）— 代币合约地址
- `network`（字符串，必填）— `ETH`、`BNB`、`BASE`、`SOLANA`

**关键输出字段：**
- `data CONTRACT` — 代币详情，包括 `communityRank`、`normalizedRank`、`totalHolders`
- `data.topHolders` — 持有者钱包地址，包括 `balance`、`walletAgeInDays`、`transactionsNumber`、`totalPoints`、`globalRank`

**示例请求：**
- *"以太坊上 USDT 的排名是多少？"
- *"0xdAC17F... 在以太坊上的顶级持有者是谁？"
- *"这个合约在 BNB 上的持有者基础有多强？"
- *"显示这个 Solana 代币的顶级持有者。"

---

## 验证检查点

### 输入验证
- ✅ 提供了钱包地址且地址非空
- ✅ 指定了工具支持的网络（请参考上述表格）
- ✅ 设置了 `CHAINAWARE_API_KEY` 环境变量
- ✅ 对于 `token_rank_list`：提供了 `limit`、`offset`、`sort_by`、`sort_order` 和 `category`
- ✅ 对于 `token_rank_single`：提供了 `contract_address` 和 `network`
- ⚠️ 如果缺少网络信息，请在继续之前询问用户
- ⚠️ 如果请求的工具不支持该网络，请告知用户并建议替代方案

### 输出验证
- ✅ `probabilityFraud` 的值在 0.00–1.00 的范围内
- ✅ 风险阈值标签正确应用（参见上述表格）
- ✅ 法律证据以通俗语言呈现，而非原始 JSON 格式
- ✅ 每条建议都指出了具体的判断依据
- ✅ 当工具不支持所需的网络时，会明确说明网络限制
- ✅ 对于行为分析结果，响应中至少包含 `intention`、`experience` 和 `categories`

---

## 示例输出

### 欺诈检测 — 以太坊上的 0xABC...

### 行为分析 — BASE 上的 0xDEF...

---

## 集成设置

### Claude 代码（CLI）

```bash
claude mcp add --transport sse chainaware-behavioural-prediction-mcp-server \
  https://prediction.mcp.chainaware.ai/sse \
  --header "X-API-Key: your-key-here"
```

📚 文档：https://code.claude.com/docs/en/mcp

### Claude Web / Claude Desktop

1. 转到 **设置 → 集成 → 添加集成**
2. 名称：`ChainAware 行为预测 MCP 服务器`
3. URL：`https://prediction.mcp.chainaware.ai/sse?apiKey=your-key-here`

📚 文档：https://platform.claude.com/docs/en/agents-and-tools/remote-mcp-servers

### Cursor（`mcp.json`）

```json
{
  "mcpServers": {
    "chainaware-behavioural-prediction-mcp-server": {
      "url": "https://prediction.mcp.chainaware.ai/sse",
      "transport": "sse",
      "headers": {
        "X-API-Key": "your-key-here"
      }
    }
  }
}
```

📚 文档：https://cursor.com/docs/context/mcp

### ChatGPT 连接器

1. 打开 **ChatGPT 设置 → 应用程序 / 连接器 → 添加连接器**
2. 名称：`ChainAware 行为预测 MCP 服务器`
3. URL：`https://prediction.mcp.chainaware.ai/sse?apiKey=your-key-here`

### Node.js

```javascript
import { MCPClient } from "mcp-client";
const client = new MCPClient("https://prediction.mcp.chainaware.ai/");

const fraud = await client.call("predictive_fraud", {
  apiKey: process.env.CHAINAWARE_API_KEY,
  network: "ETH",
  walletAddress: "0xYourWalletAddress"
});

const topTokens = await client.call("token_rank_list", {
  limit: "10", offset: "0", network: "ETH",
  sort_by: "communityRank", sort_order: "DESC",
  category: "AI Token", contract_name: ""
});
```

### Python

```python
from mcp_client import MCPClient
import os

client = MCPClient("https://prediction.mcp.chainaware.ai/")
result = client.call("predictive_fraud", {
    "apiKey": os.environ["CHAINAWARE_API_KEY"],
    "network": "ETH",
    "walletAddress": "0xYourWalletAddress"
})
```

---

## 实际应用场景

### DeFi 平台
- **风险调整借贷** — 使用欺诈评分和行为分析结果来设定抵押品要求和利率；
- **流动性管理** — 根据意图信号预先调整储备金以防止资金流失；
- **收益路由** — 识别寻求高收益的钱包并将它们引导至最优的托管平台。

### AI 代理个性化
- 为代理提供每个钱包的实时行为分析结果；
- 自动将用户分类为 DeFi 借贷者、NFT 交易者、桥接用户等。

### 欺诈与合规性
- 在用户与 Dapp 交互之前对钱包进行筛查；
- 对所有活跃钱包进行反洗钱监控；
- 在项目启动阶段检测可能的拉盘行为。

### NFT 与 GameFi
- 根据玩家的链上行为历史个性化游戏内经济系统；
- 使用欺诈评分过滤参与 NFT 分发的机器人钱包和洗钱者。

---

## 成功使用技巧

1. **始终指定网络** — 不同区块链上的工具表现可能不同；
2. **先进行欺诈检测** — 在进行任何行为分析之前，先检查欺诈风险；
- **结合多种工具进行全面尽职调查** — 欺诈检测 + 行为分析 + 拉盘检测可以提供完整的评估；
- **使用部署者风险放大器** — 即使部署者来自可信来源，合约本身仍可能存在风险；
- **进行批量筛查时** — 使用 `chainaware-fraud-detector` 子代理，而不是直接使用本技能；
- **以通俗语言呈现法律证据** — 绝不要向最终用户返回原始 JSON 数据。

---

## 相关子代理（Claude 代码）

这些子代理位于 `.claude/agents/` 目录下，提供专门的自动化执行功能：

| 子代理 | 使用场景 |
|---|---|
| `chainaware-wallet-auditor` | 结合所有预测工具进行全面尽职调查 |
| `chainaware-fraud-detector` | 快速欺诈筛查，批量钱包检查 |
| `chainaware-rug-pull-detector` | 检测智能合约/流动性池的安全性 |
| `chainaware-wallet-marketer` | 为不同类型的钱包提供个性化营销信息 |
| `chainaware-reputation-scorer` | 给出 0–4000 的声誉评分 |
| `chainaware-aml-scorer` | 给出 0–100 的反洗钱合规性评分 |
| `chainaware-trust-scorer` | 提供 0.00–1.00 的信任评分 |
| `chainaware-wallet-ranker` | 为钱包提供使用体验排名和排行榜 |
| `chainaware-whale-detector` | 对高级用户进行分类 |
| `chainaware-onboarding-router` | 根据用户水平引导钱包的注册流程 |
| `chainaware-token-ranker` | 根据持有者社区强度对代币进行排名 |
| `chainaware-token-analyzer` | 对单个代币进行深入分析（包括社区排名和顶级持有者） |
| `chainaware-defi-advisor` | 根据使用经验和风险等级提供个性化的 DeFi 产品推荐 |
| `chainaware-airdrop-screener` | 批量筛查钱包的空气投放资格，过滤机器人和欺诈行为 |
| `chainaware-lending-risk-assessor` | 评估借款人的风险等级（A–F）、抵押品比例和利率等级 |
| `chainaware-token-launch-auditor` | 在项目发布前进行安全审核（批准/有条件/拒绝） |
| `chainaware-agent-screener` | 为 AI 代理提供 0–10 的信任评分（基于代理和关联钱包的欺诈检测） |

---

## 相关阅读材料

| 文章 | 链接 |
|---|---|
| 完整产品指南 | https://chainaware.ai/blog/chainaware-ai-products-complete-guide/ |
| 欺诈检测指南 | https://chainaware.ai/blog/chainaware-fraud-detector-guide/ |
| 拉盘检测指南 | https://chainaware.ai/blog/chainaware-rugpull-detector-guide/ |
| 代币排名指南 | https://chainaware.ai/blog/chainaware-token-rank-guide/ |
| 钱包排名指南 | https://chainaware.ai/blog/chainaware-wallet-rank-guide/ |
| 钱包审核指南 | https://chainaware.ai/blog/chainaware-wallet-auditor-how-to-use/ |
| 交易监控指南 | https://chainaware.ai/blog/chainaware-transaction-monitoring-guide/ |
| Web3 行为分析指南 | https://chainaware.ai/blog/chainaware-web3-behavioral-user-analytics-guide/ |
| 信用评分指南 | https://chainaware.ai/blog/chainaware-credit-score-the-complete-guide-to-web3-credit-scoring-in-2026/ |
| Prediction MCP 开发者指南 | https://chainaware.ai/blog/prediction-mcp-for-ai-agents-personalize-decisions-from-wallet-behavior/ |
| Prediction MCP 如何提升 DeFi 平台的效率 | https://chainaware.ai/blog/top-5-ways-prediction-mcp-will-turbocharge-your-defi-platform/ |
| 个性化对 AI 代理的重要性 | https://chainaware.ai/blog/why-personalization-is-the-next-big-thing-for-ai-agents/ |
| 用于 DApp 成长的 Web3 用户细分 | https://chainaware.ai/blog/web3-user-segmentation-behavioral-analytics-for-dapp-growth-2026/ |
| 基于 AI 的区块链分析 | https://chainaware.ai/blog/ai-powered-blockchain-analysis-machine-learning-for-crypto-security-2026/ |
| 法律分析与基于 AI 的加密货币分析 | https://chainaware.ai/blog/forensic-crypto-analytics-versus-ai-based-crypto-analytics/ |
| Web3 的商业潜力 | https://chainaware.ai/blog/web3-business-potential/ |

---

## 数据与隐私

### 数据传输

每次工具调用都会将以下信息传输到 `https://prediction.mcp.chainaware.ai/sse`：

| 字段 | 示例 | 备注 |
|---|---|---|
| `walletAddress` | `0xABC...` | 链上匿名标识符，不属于个人身份信息（PII） |
| `network` | `ETH` | 仅表示区块链类型 |
| `apiKey` | `_（你的密钥）` | 来自 `CHAINAWARE_API_KEY` 环境变量；不会被记录 |

**不会发送的数据：** 名称、电子邮件地址、IP 地址、私钥、原始交易历史或任何链下个人数据。

### API 密钥处理

`CHAINAWARE_API_KEY` 从环境变量中读取，并作为 `apiKey` 参数传递给每个工具调用。它不会被包含在输出中，也不会被写入磁盘或记录。请将其视为机密信息并定期更换。

### 集成相关的隐私注意事项

- **Claude Code / Cursor**：密钥通过 `X-API-Key` 标头传递 — 不会显示在 URL 或日志中；
- **Claude Web / ChatGPT**：密钥必须附加到 SSE URL（`?apiKey=...`）—— 这些平台不支持自定义 SSE 标头。请注意，密钥会显示在浏览器的网络标签页中。对于这些集成，请使用受限范围的密钥。
- **操作者责任**：钱包地址是匿名标识符。是否构成个人数据取决于您的监管规定（例如 GDPR、MiCA）。处理与已识别用户关联的钱包的操作者应自行进行数据保护评估。

**隐私政策：** https://chainaware.ai/privacy

---

## 安全注意事项

- **切勿在公共仓库中硬编码 API 密钥**；
- 在生产环境中使用环境变量（`CHAINAWARE_API_KEY`）或秘密管理工具；
- 定期更换 API 密钥；对于基于浏览器的集成，请使用受限范围的密钥；
- 服务器使用 **SSE（Server-Sent Events）** 来传输响应；
- 根据您的订阅等级，应用相应的速率限制。

---

## 错误代码及含义

| 代码 | 含义 |
|---|---|
| `403 Unauthorized` | `apiKey` 无效或缺失 |
| `400 Bad Request` | `network` 或 `walletAddress` 格式错误 |
| `500 Internal Server Error` | 临时后端故障 — 稍后重试 |

---

## 访问与定价

需要 API 密钥。订阅地址：https://chainaware.ai/pricing