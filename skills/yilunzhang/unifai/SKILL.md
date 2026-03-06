---
name: unifai
description: 这是一个用于在 UnifAI 网络上搜索和调用服务的命令行界面（CLI）。它支持 40 多种服务，涵盖去中心化金融（DeFi）、代币数据、社交媒体、网络搜索、新闻、旅行、体育和实用工具等领域。
allowed-tools:
  - Bash(unifai:*)
  - Bash(npx -p unifai-sdk unifai:*)
version: "1.0.0"
openclaw:
  requires:
    env:
      - UNIFAI_AGENT_API_KEY
    bins:
      - npx
  optional-env:
    - SOLANA_PRIVATE_KEY
    - EVM_PRIVATE_KEY
    - SOLANA_RPC_URL
    - ETHEREUM_RPC_URL
    - BASE_RPC_URL
    - BSC_RPC_URL
    - POLYGON_RPC_URL
---
# UnifAI CLI

这是一个用于在UnifAI网络上搜索和调用服务的命令行界面（CLI）。支持40多种服务，涵盖去中心化金融（DeFi）、代币数据、社交媒体、网络搜索、新闻、旅行、体育和实用工具等领域。

## 功能介绍

UnifAI允许您：

- **搜索服务**：使用自然语言查询来查找所需的服务和操作。
- **调用服务**：以可定制的参数和重试逻辑来执行操作。
- **管理配置**：配置API密钥，并设置不同的优先级。

### 可用的服务类别

- **去中心化金融（DeFi）**：交易、借贷、提供流动性（Aave、Uniswap、Jupiter、Meteora、Pendle、Compound、1inch等）
- **代币与市场数据**：价格、交易量、价格历史数据、安全分析（Birdeye、CoinGecko、DexScreener、DefiLlama、GoPlusSecurity）
- **钱包与链上数据**：Solana、Ethereum、Base、BSC、Polygon等链上的代币余额
- **社交媒体**：Twitter/X的搜索、用户时间线、推文线程
- **网络搜索与新闻**：通用搜索、Google新闻、金融数据（SerpAPI、Tavily）
- **旅行**：航班和酒店预订
- **体育**：NBA比分、足球比赛结果（ESPN）
- **实用工具**：数学计算、时间查询、域名可用性检查、Solana租赁管理

## 安装

```bash
# Global install
npm install -g unifai-sdk

# Or use via npx (no install needed)
npx -p unifai-sdk unifai <command>
```

## 配置

设置您的API密钥：

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

搜索结果将以JSON格式返回，包含完整的数据结构（对自动化脚本非常有用）：

```bash
unifai search --query "solana swap"
unifai search --query "token price" --limit 5
```

### 调用服务

#### 带有参数的调用

```bash
unifai search --query "solana" --no-schema
```

#### 带有交易签名的调用

```bash
unifai invoke --action "Solana--7--getBalance" --payload '{"address":"..."}'
```

#### 从文件加载参数

```bash
unifai invoke --action "MyAction" --payload @payload.json
```

### 签署交易

```bash
unifai tx sign <txId>
unifai tx sign <txId> --json
```

### 配置设置

```bash
unifai config init          # Create config file
unifai config show          # Show current config and sources
unifai config show --json   # JSON output
```

### 版本信息

```bash
unifai version
unifai --version
```

## 使用说明

**重要提示：** 在调用任何服务之前，请务必先进行搜索。每个服务都有其特定的字段名称（例如，Solana的字段名为`toWalletAddress`，Polygon的字段名为`recipientWalletAddress`）。切勿猜测字段名称，否则可能会导致操作失败或返回难以理解的服务器错误。

1. **搜索**：获取服务ID和完整的数据结构。
2. 从JSON响应中读取`payload`字段，其中包含所有字段的名称、类型及是否为必填项。请严格按照这些字段名称进行操作。
3. 使用正确的数据结构调用服务。
4. 如果使用了`--sign`选项且响应中包含`txId`，系统会自动签署交易并将其提交到区块链。

## 注意事项：字段名称不可猜测

不同的服务对于相似的功能会使用不同的字段名称。例如：

| 服务 | “发送到”字段 | “金额”字段 |
|--------|----------------|----------------|
| `Solana--7--transfer` | `toWalletAddress` | `amount` |
| `Polygon--160--transfer` | `recipientWalletAddress` | `amount` |
| `Jupiter--5--swap` | `outputToken` | `inAmount` |

**请务必先使用`unifai search`进行搜索，并查看返回的数据结构。切勿猜测字段名称。**

## 错误处理

- **错误：需要API密钥** — 请设置环境变量`UNIFAI_AGENT_API_KEY`。
- **错误：需要私钥** — 请设置`SOLANA_PRIVATE_KEY`或`EVM_PRIVATE_KEY`以进行交易签名。
- **错误：需要RPC地址** — 系统提供了默认的RPC地址，但您也可以通过环境变量进行自定义（例如`POLYGON_RPC_URL`）。
- **服务器端错误**（例如：“Error: Failed to create transaction: ...”）——通常是由于字段名称错误或输入值无效造成的。请重新检查`unifai search`返回的数据结构。
- **使用`--sign`选项但未提供txId** — 这是正常情况，表示该操作不需要签名，系统会直接返回响应结果。

## 交易签名

交易签名是可选的，需要通过环境变量提供私钥：

- `SOLANA_PRIVATE_KEY` — Solana私钥（base58编码、JSON数组或来自`solana-keygen`的密钥文件路径）。
- `EVM_PRIVATE_KEY` — EVM私钥（十六进制格式，可带或不带`0x`前缀），适用于Ethereum、Polygon、Base、BSC、Hyperliquid和Polymarket。

### RPC地址（可选，提供默认值）

- `SOLANA_RPC_URL` — 默认值：`https://api.mainnet-beta.solana.com`
- `ETHEREUM_RPC_URL` — 默认值：`https://eth.llamarpc.com`
- `BASE_RPC_URL` — 默认值：`https://mainnet.base.org`
- `BSC_RPC_URL` — 默认值：`https://bsc-dataseed.binance.org`
- `POLYGON_RPC_URL` — 默认值：`https://rpc-mainnet.matic.quiknode.pro`

请注意，公共RPC地址可能存在访问限制。在生产环境中，请使用您自己的RPC地址。

所有签名操作都在CLI进程中本地完成。私钥仅由`@solana/web3.js`和`ethers`库用于在提交交易前进行签名。CLI的源代码托管在[https://github.com/unifai-network/unifai-sdk-js/tree/main/src/cli]。

## 常见示例

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