---
name: unifai
description: 这是一个用于在 UnifAI 网络上搜索和调用服务的命令行界面（CLI）。它支持超过 40 种服务，涵盖去中心化金融（DeFi）、代币数据、社交媒体、网络搜索、新闻、旅行、体育和实用工具等领域。
homepage: https://github.com/unifai-network/unifai-sdk-js
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["unifai"],"env":["UNIFAI_AGENT_API_KEY"]},"optional-env":["SOLANA_PRIVATE_KEY","EVM_PRIVATE_KEY","SOLANA_RPC_URL","ETHEREUM_RPC_URL","BASE_RPC_URL","BSC_RPC_URL","POLYGON_RPC_URL"],"install":[{"id":"node","kind":"node","package":"unifai-sdk","bins":["unifai"],"label":"Install unifai-sdk (node)"}]}}
allowed-tools:
  - Bash(unifai:*)
version: "1.0.3"
---
# UnifAI CLI

UnifAI CLI 是一个用于在 UnifAI 网络中搜索和调用服务的命令行工具。它支持 40 多种服务，涵盖去中心化金融（DeFi）、代币数据、社交媒体、网络搜索、新闻、旅行、体育和实用工具等领域。

## 功能概述

UnifAI 提供以下功能：
- **搜索服务**：通过自然语言查询查找所需的服务和操作。
- **调用服务**：以可定制的参数和重试逻辑执行服务操作。
- **管理配置**：配置 API 密钥，并设置不同的优先级。

### 可用的服务类别

- **去中心化金融（DeFi）**：交换、借贷、提供流动性（Aave、Uniswap、Jupiter、Meteora、Pendle、Compound、1inch 等）。
- **代币与市场数据**：价格、OHLCV（开高低收盘价）、安全分析（Birdeye、CoinGecko、DexScreener、DefiLlama、GoPlusSecurity）。
- **钱包与链数据**：Solana、Ethereum、Base、BSC、Polygon 等链上的代币余额。
- **社交媒体**：Twitter/X 的搜索、用户时间线、推文线程。
- **网络搜索与新闻**：通用搜索、Google 新闻、金融数据（SerpAPI、Tavily）。
- **旅行**：航班和酒店搜索。
- **体育**：NBA 比分、足球结果（ESPN）。
- **实用工具**：数学计算、时间查询、域名可用性检查、Solana 租用管理。

## 安装

全局安装该工具，以便在本地使用二进制文件：

```bash
npm install -g unifai-sdk
```

或者通过 `npx` 命令直接使用（无需安装）：

```bash
-npx -p unifai-sdk unifai <command>
```

## 配置

设置您的 API 密钥：

```bash
export UNIFAI_AGENT_API_KEY="your-key-here"
```

或者创建一个配置文件：

```bash
unifai config init
# Edit ~/.config/unifai-cli/config.yaml
```

## 命令

### 搜索服务

搜索结果会以 JSON 格式返回，其中包含完整的数据结构（对自动化脚本非常有用）：

```bash
unifai search --query "solana swap"
unifai search --query "token price" --limit 5
```

### 调用服务

#### 带有参数的调用

#### 带有交易签名的调用

#### 从文件加载参数

### 签署交易

### 配置设置

### 版本信息

## 使用说明

**重要提示：** 在调用任何服务之前，请务必先进行搜索。每个服务都有其特定的字段名称（例如，Solana 的字段名为 `toWalletAddress`，Polygon 的字段名为 `recipientWalletAddress`）。切勿猜测字段名称，否则可能会导致操作失败或出现难以理解的服务器错误。

1. **搜索**：获取服务 ID 和完整的数据结构。
2. 读取 JSON 响应中的 `payload` 字段，其中包含所有字段的名称、类型以及是否为必填项。请严格按照这些字段名称进行操作。
3. 使用正确的数据结构调用服务。

**注意：** 不同服务使用不同的字段名称来表示相似的功能。例如：
| 服务类型 | “发送到”字段 | “金额”字段 |
|--------|----------------|----------------|
| Solana--7--transfer | toWalletAddress | amount |
| Polygon--160--transfer | recipientWalletAddress | amount |
| Jupiter--5--swap | outputToken | inAmount |

**务必先使用 `unifai search` 功能获取服务信息，并仔细阅读返回的数据结构。切勿猜测字段名称。**

## 错误处理

- **错误：需要 API 密钥** — 请设置环境变量 `UNIFAI_AGENT_API_KEY`。
- **错误：需要私钥** — 请设置 `SOLANA_PRIVATE_KEY` 或 `EVM_PRIVATE_KEY` 以进行交易签名。
- **错误：需要 RPC URL** — 系统提供了默认的 RPC URL，但您也可以通过环境变量进行自定义（例如 `POLYGON_RPC_URL`）。
- **服务器端错误**（例如：“Error: Failed to create transaction: ...”）：通常是由于字段名称错误或参数无效导致的。请重新检查搜索结果中的数据结构。
- **使用 `--sign` 选项但未获取 `txId`**：这种情况正常，表示该服务不需要签名，响应会直接返回。

## 交易签名

交易签名是可选的，需要通过环境变量提供私钥：
- `SOLANA_PRIVATE_KEY`：Solana 的私钥（格式为 base58、JSON 数组或来自 `solana-keygen` 的密钥存储文件路径）。
- `EVM_PRIVATE_KEY`：EVM 的私钥（十六进制格式，可带前缀 `0x` 或不带前缀）。适用于 Ethereum、Polygon、Base、BSC、Hyperliquid 和 Polymarket。

**RPC URL**（可选，系统提供默认值）：
- `SOLANA_RPC_URL`：`https://api.mainnet-beta.solana.com`
- `ETHEREUM_RPC_URL`：`https://eth.llamarpc.com`
- `BASE_RPC_URL`：`https://mainnet.base.org`
- `BSC_RPC_URL`：`https://bsc-dataseed.binance.org`
- `POLYGON_RPC_URL`：`https://rpc-mainnet.matic.quiknode.pro`

请注意，公共 RPC URL 可能存在访问限制。在生产环境中，请使用您自己的 RPC URL。

所有签名操作都在 CLI 进程中本地完成。私钥仅由 `@solana/web3.js` 和 `ethers` 库用于在提交交易前进行签名。CLI 的源代码位于：[https://github.com/unifai-network/unifai-sdk-js/tree/main/src/cli](https://github.com/unifai-network/unifai-sdk-js/tree/main/src/cli)。

## 常见使用示例

```bash
# Step 1: Always search first to get the exact schema
unifai search --query "solana transfer"

# Solana transfer (uses toWalletAddress, not "to")
unifai invoke --action "Solana--7--transfer" \
  --payload '{"toWalletAddress":"...","amount":0.01}' --sign

# Jupiter swap on Solana
unifai invoke --action "Jupiter--5--swap" \
  --payload '{"inputToken":"SOL","outputToken":"USDC","inAmount":0.1}' --sign

# Polygon transfer (uses recipientWalletAddress)
unifai invoke --action "Polygon--160--transfer" \
  --payload '{"recipientWalletAddress":"0x...","amount":0.01}' --sign

# Polymarket - get open orders (read-only, but still needs signing)
unifai invoke --action "polymarket--127--getOpenOrders" --payload '{}' --sign

# Read-only actions don't need --sign
unifai invoke --action "Birdeye--174--RetrieveTheLatestPrice" \
  --payload '{"address":"So11111111111111111111111111111111111111112","chain":"solana"}'

# Search for any capability
unifai search --query "weather forecast"
unifai search --query "sports scores"
```

## 安全注意事项

- **私钥**：`SOLANA_PRIVATE_KEY` 和 `EVM_PRIVATE_KEY` 仅用于交易签名。
- **本地签名**：所有交易签名操作都在本地进程内完成，不会将私钥发送到外部 API。