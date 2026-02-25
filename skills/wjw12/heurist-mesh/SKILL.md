---
name: heurist-mesh-skill
description: 实时加密代币数据、去中心化金融（DeFi）分析、区块链数据、Twitter/X等社交媒体的情报分析，以及强大的网络搜索功能——所有这些功能都集成在一个技能（Skill）中。对于需要深入了解的领域，“Ask Heurist”智能助手能够提供市场趋势分析、交易策略建议、宏观新闻解读以及深入的研究支持。
---
# Heurist Mesh

Heurist Mesh 是一个开放式的、基于模块化的 AI 工具网络，专为加密货币和区块链数据提供分析服务。所有功能均可通过统一的 REST API 进行访问。

### 推荐使用的代理和工具

**TrendingTokenAgent** — 监测热门代币及市场概况
- `get_trending_tokens` — 获取在 CEX（中心化交易所）和 DEX（去中心化交易所）中最受关注和交易的代币
- `get_market_summary` — 获取最新的市场新闻，包括宏观信息和重大更新

**TokenResolverAgent** — 查找代币并获取详细信息
- `token_search` — 通过地址、交易代码或名称搜索代币（最多返回 5 个结果）
- `token_profile` — 获取代币的详细信息，包括交易对、融资费率及各类指标

**DefiLlamaAgent** — DeFi 协议及链上指标分析
- `get_protocol_metrics` — 获取协议的 TVL（总价值锁定）、费用、交易量、收入、支持的链以及增长趋势
- `get_chain_metrics` — 获取区块链的 TVL、费用、主要支持的协议及其增长趋势

**TwitterIntelligenceAgent** — Twitter/X 数据分析
- `user_timeline` — 获取用户的最新帖子和公告
- `tweet_detail` — 获取包含回复的推文详情
- `twitter_search` — 按主题搜索推文和有影响力的提及

**ExaSearchDigestAgent** — 基于 LLM 的网络搜索服务，支持摘要功能
- `exa_web_search` — 带有时间与领域过滤条件的网络搜索
- `exa_scrape_url` — 抓取 URL 并提取或总结相关信息

**ChainbaseAddressLabelAgent** — EVM（以太坊虚拟机）地址标签管理
- `get_address_labels` — 获取 ETH 或 Base 地址的标签（如身份信息、合约名称、钱包行为、ENS（以太坊名称服务））

**ZerionWalletAnalysisAgent** — EVM 钱包资产分析
- `fetch_wallet_tokens` — 获取钱包持有的代币及其对应的 USD 价值及 24 小时价格变化
- `fetch_wallet_nfts` — 获取钱包持有的 NFT（非同质化代币）集合

**ProjectKnowledgeAgent** — 加密项目数据库
- `get_project` — 通过项目名称、交易代码或 X 账号查询项目信息（包括团队、投资者、活动等）
- `semantic_search_projects` — 支持自然语言搜索，可筛选 10,000 多个项目（按投资者、标签、融资年份或交易所筛选）

**CaesarResearchAgent** — 学术研究支持
- `caesar_research` — 提交研究请求以获取深入分析结果
- `get_research_result` — 根据 ID 获取研究结果

**AskHeuristAgent** — 加密相关问题解答及深度分析服务（适用于需要深入研究的场景）
- `ask_heurist` — 提出加密相关问题（可选择普通模式或深度分析模式）
- `check_job_status` — 查看待处理分析任务的进度

## 设置（在调用任何 API 之前必须完成）

您需要至少配置一种支付方式。**在设置完成之前，请勿调用任何 Mesh 工具的 API。**

### 第一步：选择支付方式

**选项 A：Heurist API 密钥（推荐——最简单的方式）**

1. 通过以下方式获取 API 密钥：
   - 在 https://heurist.ai/credits 购买信用点数
   - 或者通过 Twitter 获取 100 个免费信用点数（详见 [references/heurist-api-key.md](references/heurist-api-key.md)）
2. 将密钥保存在项目根目录下的 `.env` 文件中：
   ```
   HEURIST_API_KEY=your-api-key-here
   ```
3. 所有 API 请求均需使用 `Authorization: Bearer $HEURIST_API_KEY` 进行身份验证

**选项 B：基于 Base 的 x402 在链支付（使用 USDC）**

1. 您需要一个在 Base 区块链上拥有 USDC 存款的钱包私钥。
2. 将私钥保存在项目根目录下的 `.env` 文件中：
   ```
   WALLET_PRIVATE_KEY=0x...your-private-key
   ```
3. 有关使用 `cast`（Foundry）进行支付的详细流程，请参阅 [references/x402-payment.md](references/x402-payment.md)

**选项 C：Inflow 支付平台（通过 Inflow 支付 USDC）**

1. 如果您已经拥有 Inflow 账户信息，请将其保存在 `.env` 文件中：
   ```
   INFLOW_USER_ID=your-buyer-user-id
   INFLOW_PRIVATE_KEY=your-buyer-private-key
   ```
2. 如果没有，请创建一个买家账户并绑定电子邮件地址——详细步骤请参阅 [references/inflow-payment.md](references/inflow-payment.md)。
3. Inflow 支付流程分为两次请求：创建请求 → 用户确认 → 执行请求。完整流程请参见 [references/inflow-payment.md](references/inflow-payment.md)。

### 第二步：验证设置

在继续使用之前，请确认以下设置已完成：

- **API 密钥**：检查 `.env` 文件，确保 `HEURIST_API_KEY` 已设置且非空。
- **x402 支付**：检查 `.env` 文件，确保 `WALLET_PRIVATE_KEY` 已设置（以 `0x` 开头且长度为 66 个字符）。
- **Inflow 支付**：检查 `.env` 文件，确保 `INFLOW_USER_ID` 和 `INFLOW_PRIVATE_KEY` 已设置且非空。

**如果任何一项设置未完成，请停止操作并让用户完成支付方式的配置。在没有有效凭证的情况下，请勿调用 API。**

### 第三步：调用 API

一旦您获得了 Heurist API 密钥、x402 钱包私钥或 Inflow 密钥，就可以开始调用 API 了。在调用 API 之前，请确保您了解所需工具的接口结构和参数。

要获取工具的详细信息，可以使用 `mesh_schema` API：

```
GET https://mesh.heurist.xyz/mesh_schema?agent_id=TokenResolverAgent&agent_id=CoinGeckoTokenInfoAgent
```

默认计费单位为信用点数，1 信用点数相当于 0.01 美元。如果使用 x402 或 Inflow 支付方式，可以在请求中添加 `&pricing=usd` 以获取美元价格。该 API 会返回每个工具的详细信息（名称、类型、描述、必填/可选参数以及单价）。

接下来，请在请求中使用相应的凭证：

```bash
# With API key
curl -X POST https://mesh.heurist.xyz/mesh_request \
  -H "Authorization: Bearer $HEURIST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "TokenResolverAgent", "input": {"tool": "token_search", "tool_arguments": {"query": "ETH"}, "raw_data_only": true}}'

# With x402 — sign with cast (Foundry), no account or SDK needed
# See references/x402-payment.md for the full cast-based flow and helper script
```

## 发现更多工具

**所有工具的列表**：访问 `https://mesh.heurist.ai/metadata.json` 可查看完整的工具注册表。我们提供了 30 多种专业的加密分析工具，涵盖多种功能，例如：
- 查阅地址的交易历史
- 从哈希值中提取交易详情
- 监测 Base 区块链上的 USDC 流动情况
- 获取 Coingecko 的详细数据
- 进行 Firecrawl 爬取
- 使用 GoPlus 进行安全筛查
- 通过 Moni 分析 Twitter 账户的影响力
- 使用 SQL 查询区块链数据等

**仅支持 x402 支付方式的工具**：访问 `https://mesh.heurist.xyz/x402/agents` 可查看支持基于 Base 区块链的 USDC 支付的工具列表。