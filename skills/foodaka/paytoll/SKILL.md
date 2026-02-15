---
name: paytoll
description: "27款工具，适用于去中心化金融（DeFi）、去中心化交易所（DEX）交易、跨链桥接、Twitter/X平台的数据获取、链上代币管理，以及通过Base平台上的x402微支付方式访问大型语言模型（LLM）。无需使用API密钥——支付过程本身即实现了身份验证。"
metadata: {"mcpServers":{"paytoll":{"command":"npx","args":["-y","paytoll-mcp"],"env":{"PRIVATE_KEY":"${PRIVATE_KEY}"}}}}
requires.env: ["PRIVATE_KEY"]
requires.bins: ["node"]
homepage: https://paytoll.io
repository: https://github.com/foodaka/paytoll-mcp
---

# PayToll

通过 PayToll MCP 服务器，您可以访问 27 种工具，这些工具涵盖了 DeFi 智能分析、DEX 交易、跨链桥接、社交媒体、链上代币数据、加密工具以及 LLM（大型语言模型）访问等功能。每个工具的调用都会在 Base 网络上消耗少量 USDC，费用会自动从用户配置的钱包中扣除。无需 API 密钥或订阅服务——支付即作为身份验证方式。

## 设置要求

用户必须具备以下条件：
- 在其环境中设置一个专用的钱包私钥，并将其设置为 `PRIVATE_KEY`（请勿使用您的主钱包，而是使用一个资金较少的钱包）。
- 该钱包中需要有足够的 USDC（几美元即可支持数千次调用）。
- 在 Base 网络上还需要有一定数量的 ETH（用于支付交易手续费）。

私钥永远不会离开用户的设备，它仅用于在本地签署 EIP-712 格式的支付授权请求，且永远不会被传输到任何服务器。

## 安全性

- **不执行任何交易。** 交易构建工具（如 `aave-supply`、`swap-build` 等）仅返回未签名的交易数据供用户审核，不会在链上广播或执行任何操作。
- **仅支持微支付。** 大多数工具的调用费用在 0.001–0.08 美元之间。钱包资金不会被耗尽——每次支付都是一次独立的、小额的授权请求。
- **开源代码。** MCP 服务器的源代码可以在 [https://github.com/foodaka/paytoll-mcp](https://github.com/foodaka/paytoll-mcp) 上查看。

## 可用工具

### Aave DeFi 智能分析工具

当用户需要查询 DeFi 的收益、借贷信息或 Aave 的持仓情况时，可以使用以下工具：

**`aave-best-yield`**（每次调用费用：0.01 美元）
- 查找指定资产在所有 Aave v3 平台和链上的最佳收益。
- 适用场景：例如：“USDC 的最佳收益是多少？”、“我应该将 ETH 投放到哪里以获得最高的收益？”
- 输入参数：`asset`（例如：“USDC”、“ETH”、“WBTC”）

**`aave-best-borrow`**（每次调用费用：0.01 美元）
- 查找指定资产在所有 Aave v3 市场上的最低借款利率。
- 适用场景：例如：“在哪里可以以最低利率借款 DAI？”、“ETH 的最低借款利率是多少？”
- 输入参数：`asset`（例如：“USDC”、“ETH”、“DAI”）

**`aave-markets`**（每次调用费用：0.005 美元）
- 获取所有 Aave v3 市场的综合数据，包括供应量/借款利率、总市值（TVL）和利用率。
- 适用场景：例如：“显示所有 Aave 市场”、“查看 DeFi 借贷利率概览”、“我可以在 Aave 上提供哪些资产？”

**`aave-health-factor`**（每次调用费用：0.005 美元）
- 计算用户在 Aave 上的“健康状况”——表示其持仓距离清算的距离有多近。
- 适用场景：例如：“我的健康状况如何？”、“我有被清算的风险吗？”、“查询 0x... 的健康状况”
- 输入参数：`chainId`

**`aave-user-positions`**（每次调用费用：0.01 美元）
- 获取用户在所有链上的完整借贷持仓信息。
- 适用场景：例如：“我的 Aave 持仓情况是什么？”、“展示我的 DeFi 投资组合”、“我正在提供/借款哪些资产？”

### Aave 交易工具

当用户需要生成 Aave 操作的交易数据时，可以使用以下工具。这些工具返回未签名的交易数据，不会在链上广播。

**`aave-supply`**（每次调用费用：0.01 美元）
- 用于在 Aave 上进行资产供应（存款）操作。
- 适用场景：例如：“向 Aave 存入 100 USDC”、“将 ETH 存入 Aave”
- 输入参数：`tokenAddress`、`amount`、`chainId`

**`aave-borrow`**（每次调用费用：0.01 美元）
- 用于在 Aave 上进行借款操作。
- 适用场景：例如：“从 Aave 借入 50 DAI”、“在 Aave 上贷款”
- 输入参数：`tokenAddress`、`amount`、`chainId`

**`aave-repay`**（每次调用费用：0.01 美元）
- 用于偿还 Aave 的贷款。
- 适用场景：“偿还我的 DAI 贷款”、“在 Aave 上归还 100 USDC”
- 输入参数：`tokenAddress`、`chainId`、`amount` 或 `max: true`

**`aave-withdraw`**（每次调用费用：0.01 美元）
- 用于从 Aave 中提取资产。
- 适用场景：“从 Aave 提取我的 USDC”、“取出我的 ETH”

### DEX 交易与跨链桥接工具

这些工具由 Li.Fi 集成器提供支持，支持同链交易和跨 12 个网络（Ethereum、Base、Arbitrum、Optimism、Polygon、Avalanche、BSC、zkSync、Linea、Scroll、Fantom、Gnosis）的跨链桥接。要进行桥接，请设置 `fromChain` 和 `toChain` 为相应的链 ID——Li.Fi 会自动选择最优的桥接协议（如 Stargate、Across、Hop 等）进行路由。这些工具也返回未签名的交易数据，不会在链上广播。

**`swap-quote`**（每次调用费用：0.005 美元）
- 获取 DEX 交易或跨链桥接的价格报价。
- 适用场景：“1 ETH 可以兑换多少 USDC？”、“将 ETH 从 Ethereum 桥接到 Arbitrum 的价格是多少？”、“交换率是多少？”
- 输入参数：`fromChain`、`fromToken`、`toToken`、`amount`（可选参数 `toChain` 用于跨链交易）、`slippage`（滑点）

**`swap-build`**（每次调用费用：0.01 美元）
- 生成可用于签署的交换或桥接交易数据。
- 适用场景：“在 Base 上将 1 ETH 交换成 USDC”、“将 100 USDC 从 Ethereum 桥接到 Arbitrum”
- 输入参数：`fromChain`、`fromToken`、`toToken`、`amount`（可选参数 `toChain`、`slippage`）

**`token-balance`**（每次调用费用：0.005 美元）
- 查看钱包中任何支持链上的代币余额。
- 适用场景：“我的 ETH 余额是多少？”、“我在 Base 上有多少 USDC？”
- 输入参数：`chainId`（对于原生代币，可选参数 `tokenAddress` 可省略）

### 链上代币数据工具

这些工具用于链上代币的分析、流动性池的查找以及热门代币的查询。

**`onchain-token-data`**（每次调用费用：0.015 美元）
- 获取全面的链上代币数据，包括价格、供应量、市值（FDV）和顶级流动性池信息。
- 适用场景：“了解这个代币的情况”、“PEPE 在 Base 上的市值是多少？”
- 输入参数：`network`、`contractAddress`

**`onchain-token-price`**（每次调用费用：0.015 美元）
- 根据合约地址获取链上代币的价格。
- 适用场景：“这个代币在链上的价格是多少？”
- 输入参数：`network`、`contractAddress`

**`search-pools`**（每次调用费用：0.015 美元）
- 根据代币名称、符号或合约地址在多个网络中搜索流动性池。
- 适用场景：“查找 PEPE 的流动性池”、“搜索 WETH 的流动性池”
- 输入参数：`query`

**`trending-pools`**（每次调用费用：0.015 美元）
- 获取按交易活跃度排序的热门流动性池信息。
- 适用场景：“Base 上有哪些热门交易？”、“展示 Ethereum 上的热门池”
- 输入参数：`network`（例如：“eth”、“base”、“solana”）

### 社交媒体工具（X/Twitter）

当用户需要查询推文、Twitter 用户信息或希望在 X 上发布内容时，可以使用以下工具：

**`twitter-search`**（每次调用费用：0.08 美元）
- 搜索过去 7 天内的推文，每次最多返回 20 条结果。
- 适用场景：“在 Twitter 上搜索比特币的相关内容”、“人们如何评价 ETH？”、“查找关于 Aave 的推文”
- 输入参数：`query`（X API 的搜索语法）、`maxResults`（10-20 条）、`sortOrder`（“recency” 或 “relevancy”）

**`twitter-user-tweets`**（每次调用费用：0.08 美元）
- 获取用户的最新推文，每次最多返回 20 条。可以排除回复和转发。
- 适用场景：“Vitalik 最近发了什么推文？”、“显示 Elon 的最新推文”
- 输入参数：`userId`、`maxResults`（5-20 条）、`excludeReplies`、`excludeRetweets`（是否排除回复和转发）

**`twitter-tweet-lookup`**（每次调用费用：0.02 美元）
- 根据推文 ID 查找推文及其相关指标和作者信息。每次最多返回 10 条推文。
- 适用场景：“显示这条推文的信息”、“查询推文 ID 123... 的详细信息”
- 输入参数：`ids`（推文 ID 的数组）

**`twitter-user-lookup`**（每次调用费用：0.02 美元）
- 根据用户名或用户 ID 查找 X/Twitter 用户。
- 适用场景：“@elonmusk 是谁？”、“查找用户 ID 44196397 的信息”
- 输入参数：`username` 或 `userId`（必须指定一个）

**`twitter-post`**（每次调用费用：0.015 美元）
- 使用用户的 OAuth 2.0 访问令牌发布推文。支持回复和引用推文。
- 适用场景：“帮我发布这条推文”、“回复这条推文”
- 输入参数：`text`、`accessToken`（用户的 OAuth 令牌）、`replyToId`（可选）、`quoteTweetId`（可选）
- 注意：需要用户的 X API OAuth 令牌，并且必须具有 `tweet.write` 权限。

### 加密工具

这些工具用于查询代币价格、ENS（Ethereum 名称服务）解析和地址验证。

**`crypto-price`**（每次调用费用：0.015 美元）
- 从 CoinGecko 获取实时加密货币价格，可选参数包括市场数据。
- 适用场景：“ETH 的价格是多少？”、“BTC 的价格是多少？”、“SOL 的价格是多少？”
- 输入参数：`symbol`（例如：“BTC”、“ETH”、“SOL”），可选参数 `currency`、`includeMarketData`

**`ens-lookup`（每次调用费用：0.001 美元）
- 将 ENS 名称解析为 Ethereum 地址，并进行反向查询。
- 适用场景：“vitalik.eth 的地址是什么？”、“反向查询 0x... 的地址”
- 输入参数：`name`（例如：“vitalik.eth”）或 `address`

**`wallet-validator`**（每次调用费用：0.0005 美元）
- 验证字符串是否为有效的钱包地址（包括校验和验证）。
- 适用场景：“这个地址有效吗？”、“检查 0x... 是否是有效的地址”
- 输入参数：`address`（可选参数 `network`：“ethereum”、“bitcoin”、“solana”）

### LLM 代理工具

当用户希望通过 PayToll 查询 AI 模型时，可以使用以下工具：

**`llm-openai`**（每次调用费用：0.01 美元）
- 查询 OpenAI 模型：GPT-4o、GPT-4o-mini、GPT-4 Turbo、GPT-3.5 Turbo、o3-mini。
- 输入参数：`messages`，可选参数 `model`、`temperature`、`max_tokens`

**`llm-anthropic`**（每次调用费用：0.01 美元）
- 查询 Anthropic 模型：Claude Sonnet 4、Haiku 4、Claude 3.5 Sonnet、Claude 3.5 Haiku、Claude 3 Haiku。
- 输入参数：`messages`，可选参数 `model`、`temperature`、`max_tokens`

**`llm-google`**（每次调用费用：0.01 美元）
- 查询 Google 模型：Gemini 2.0 Flash、Gemini 2.0 Flash Lite、Gemini 1.5 Pro、Gemini 1.5 Flash。
- 输入参数：`messages`，可选参数 `model`、`temperature`、`max_tokens`

## 使用指南

- 在每次调用工具之前，务必告知用户该操作会消耗 USDC，尤其是在会话中的首次调用时。
- 对于多步骤查询（例如：“查找所有稳定币的最佳收益”），请批量提交问题以减少调用次数。
- 如果某个工具返回支付错误，用户可能需要向钱包中充值 USDC。
- 交易构建工具返回的只是未签名的数据——请提醒用户需要自行完成签名和广播操作。
- MCP 服务器会动态地从 API 中加载新的工具，因此可能会添加更多功能。

## 价格汇总

| 工具 | 费用 |
|------|------|
| `aave-best-yield` | 0.01 美元 |
| `aave-best-borrow` | 0.01 美元 |
| `aave-markets` | 0.005 美元 |
| `aave-health-factor` | 0.005 美元 |
| `aave-user-positions` | 0.01 美元 |
| `aave-supply` | 0.01 美元 |
| `aave-borrow` | 0.01 美元 |
| `aave-repay` | 0.01 美元 |
| `aave-withdraw` | 0.01 美元 |
| `swap-quote` | 0.005 美元 |
| `swap-build` | 0.01 美元 |
| `token-balance` | 0.005 美元 |
| `onchain-token-data` | 0.015 美元 |
| `onchain-token-price` | 0.015 美元 |
| `search-pools` | 0.015 美元 |
| `trending-pools` | 0.015 美元 |
| `twitter-search` | 0.08 美元 |
| `twitter-user-tweets` | 0.08 美元 |
| `twitter-tweet-lookup` | 0.02 美元 |
| `twitter-user-lookup` | 0.02 美元 |
| `twitter-post` | 0.015 美元 |
| `crypto-price` | 0.015 美元 |
| `ens-lookup` | 0.001 美元 |
| `wallet-validator` | 0.0005 美元 |
| `llm-openai` | 0.01 美元 |
| `llm-anthropic` | 0.01 美元 |
| `llm-google` | 0.01 美元 |