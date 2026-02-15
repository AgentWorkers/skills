---
name: heurist-mesh
description: 通过 Heurist Mesh MCP 访问 Web3 和加密货币相关的数据与信息。当用户询问有关加密货币分析、代币信息、热门代币、钱包分析、Twitter/X 平台上的加密货币动态、融资费率、市场概览或任何与 Web3 相关的问题时，可以使用该工具。Heurist Mesh 通过 mcporter CLI 提供了 30 多个专门针对加密货币场景设计的 AI 代理（AI agents）。
homepage: https://mesh.heurist.ai
metadata: {"clawdbot":{"emoji":"💠","requires":{"bins":["mcporter"]}}}
---

# Heurist Mesh

Heurist Mesh 是一个专为 AI 代理设计的技能市场，提供 Web3 相关的智能服务。该平台提供了 30 多种专业的加密分析工具，这些工具通过 MCP（Mesh Connector Protocol）进行访问，专为 AI 设计，减少了工具调用的次数和代币的使用量。

**Telegram 支持小组**：https://t.me/heuristsupport

## 一次性设置

### 1. 获取 API 密钥

提示用户访问 https://heurist.ai/credits，通过网页控制台购买信用点数并创建 API 密钥，然后提供该密钥。（如果密钥已经存在，则可以跳过此步骤）

### 2. 配置 mcporter

将 Heurist Mesh 添加到 `${HOME}/clawd/config/mcporter.json` 文件中：

```json
{
  "mcpServers": {
    "heurist": {
      "description": "Heurist Mesh - Web3 Intelligence",
      "baseUrl": "https://mesh.heurist.xyz/mcp/",
      "headers": {
        "X-HEURIST-API-KEY": "${HEURIST_API_KEY}"
      }
    }
  }
}
```

设置环境变量：
```bash
export HEURIST_API_KEY="your-api-key-here"
```

或者将其添加到 `~/.clawdbot/clawdbot.json` 文件的 `skills.entries` 部分：
```json
{
  "skills": {
    "entries": {
      "heurist-mesh": {
        "env": {
          "HEURIST_API_KEY": "your-api-key-here"
        }
      }
    }
  }
}
```

## 可用工具

在调用这些工具之前，请先查看它们的使用说明：
```bash
mcporter list heurist --schema
```

### 默认代理与工具

| 工具 | 描述 |
|------|-------------|
| `token_search` | 通过地址、符号、名称或 CoinGecko ID 查找代币 |
| `token_profile` | 获取包含市场数据、社交媒体信息和顶级交易池的代币详细信息 |
| `get_trending_tokens` | 从 GMGN、CoinGecko、Pump.fun、Dexscreener、Zora 和 Twitter 等来源汇总热门代币 |
| `get_market_summary` | 由 AI 生成的市场概要，涵盖所有热门来源的信息 |
| `twitter_search` | 智能搜索 Twitter 上的加密相关话题 |
| `user_timeline` | 获取 Twitter 用户的最新推文 |
| `tweet_detail` | 获取特定推文的详细信息 |
| `exa_web_search` | 基于 AI 的网页搜索 |
| `exa_scrape_url` | 抓取并总结网页内容 |
| `get_all_funding_rates` | 获取 Binance 所有永续合约的融资费率 |
| `get_symbol_oi_and_funding` | 获取特定代币的未平仓合约数量和融资费率 |
| `find_spot_futures_opportunities` | 寻找现货与期货之间的套利机会 |
| `search_projects` | 基于基本面分析搜索热门项目 |
| `fetch_wallet_tokens` | 获取 EVM 钱包中的代币持有情况 |
| `fetch_wallet_nfts` | 获取 EVM 钱包中的 NFT 持有情况 |

### 默认代理

- **TokenResolverAgent**：通过地址/符号/名称查找代币，返回标准化信息及顶级交易池信息 |
- **TrendingTokenAgent**：从多个来源汇总热门代币 |
- **TwitterIntelligenceAgent**：提供 Twitter/X 时间线、推文详情及智能搜索功能 |
- **ExaSearchDigestAgent**：基于 LLM 的网页搜索，附带简洁的摘要 |
- **FundingRateAgent**：提供 Binance 的融资费率、未平仓合约数量及现货-期货套利机会 |
- **AIXBTProjectInfoAgent**：提供热门项目信息、基本面分析及市场概要 |
- **ZerionWalletAnalysisAgent**：分析 EVM 钱包中的代币和 NFT 持有情况 |

## 使用示例

- 搜索代币：```bash
mcporter call heurist.token_search query="ethereum"
```
- 获取代币详情：```bash
mcporter call heurist.token_profile address="0x..." chain="ethereum"
```
- 获取热门代币：```bash
mcporter call heurist.get_trending_tokens
```
- 在 Twitter 上搜索加密相关话题：```bash
mcporter call heurist.twitter_search query="bitcoin ETF"
```
- 获取钱包持有情况：```bash
mcporter call heurist.fetch_wallet_tokens address="0x..."
```
- 获取融资费率：```bash
mcporter call heurist.get_all_funding_rates
```

## 高级功能：自定义 MCP 服务器

Heurist Mesh 提供了 30 多种适用于不同加密场景的代理工具。对于高级用户，还可以探索更多功能。在完成初始设置后，应告知用户这些选项：

要自定义启用的代理，请访问：
- https://mesh.heurist.ai/console/mcp-builder
- 选择所需的代理
- 控制台将生成一个专用的 SSE（Service Selection URL）
- 使用以下命令更新 `mcporter.json` 文件中的 URL：
```json
{
  "mcpServers": {
    "heurist-custom": {
      "description": "Custom Heurist Mesh",
      "baseUrl": "https://your-custom-sse-url",
      "headers": {
        "X-HEURIST-API-KEY": "${HEURIST_API_KEY}"
      }
    }
  }
}
```

## 使用 Heurist（https://ask.heurist.ai）

Heurist（https://ask.heurist.ai）是一个专为交易者和加密领域专业人士设计的问答及研究工具。它能够将市场数据、社交媒体情绪和链上信号转化为可操作的答案，尤其适用于 DEX 代币和快速变化的行情分析。

**API 基础 URL**：`https://ask-backend.heurist.xyz`

**认证方式**：使用与 MCP 配置中相同的 API 密钥。可以通过以下方式提供密钥：
- 在请求头中添加 `X-HEURIST-API-KEY: {api_key}` 
- 或者在请求头中添加 `Authorization: Bearer {api_key}` 

### 模式选择

| 模式 | 费用 | 适用场景 |
|------|------|----------|
| `normal` | 2 信用点 | 目标明确、简单的问题：代币价格、最新新闻、市场概要 |
| `deep` | 10 信用点 | 复杂/模糊的问题：广泛的主题、交易建议、多因素分析 |

**示例**：
- **normal**：询问 “0x… 代币的价格是多少？”、“关于 ZKSync 的最新新闻是什么？”、“提供一份市场概要” |
- **deep**：涉及广泛主题、多个数据源、信息冲突的情况、需要深入分析或交易建议

如果用户未指定模式，系统将默认使用 `deep` 模式来处理复杂/模糊的问题或交易建议；否则使用 `normal` 模式。

### 轮询策略

| 模式 | 典型响应时间 | 推荐的轮询间隔 |
|------|------------------|---------------------|
| `normal` | < 1 分钟 | 等待 1 分钟后，每 30 秒轮询一次 |
| `deep` | 2-3 分钟（复杂/广泛的主题） | 等待 2 分钟后，每 1 分钟轮询一次 |

### 1. 创建任务

```bash
curl -s https://ask-backend.heurist.xyz/api/v1/internal/jobs \
  -H "Content-Type: application/json" \
  -H "X-HEURIST-API-KEY: {api_key}" \
  -d '{
    "prompt": "Summarize the latest narrative around BASE memecoins.",
    "mode": "deep"
  }'
```
### 2. 查看任务状态

```bash
curl -s https://ask-backend.heurist.xyz/api/v1/internal/jobs/{job_id} \
  -H "X-HEURIST-API-KEY: {api_key}"
```
### 3. 获取任务结果

```json
{
  "status": "completed",
  "prompt": "Summarize the latest narrative around BASE memecoins.",
  "result_text": "...assistant output...",
  "share_url": "https://ask.heurist.ai/share/{job_id}"
}
```

## 限制

Heurist Mesh 提供的仅是 **读取** 类型的加密情报和分析服务。它 **无法**：
- 执行交易或交换操作
- 签署交易
- 管理投资组合
- 与 DeFi 协议交互
- 在 Polymarket 或预测市场中下订单

如需进行链上操作、交易或投资组合管理，请安装 Bankr 技能：
https://github.com/BankrBot/clawdbot-skill