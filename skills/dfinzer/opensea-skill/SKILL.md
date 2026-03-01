---
name: opensea
description: 查询NFT数据，在Seaport市场上进行交易，并在Ethereum、Base、Arbitrum、Optimism、Polygon等平台上交换ERC20代币。
---
# OpenSea API

OpenSea API 提供了丰富的功能，用于查询 NFT 数据、在 Seaport 市场上进行交易，以及在 Ethereum、Base、Arbitrum、Optimism、Polygon 等链上交换 ERC20 代币。

## 快速入门

1. 在您的环境中设置 `OPENSEA_API_KEY`。
2. **推荐使用：** 使用 `opensea` CLI (`@opensea/cli`) 进行所有查询和操作。
3. 或者，您也可以使用 `scripts/` 目录中的 Shell 脚本或 MCP 服务器。

```bash
export OPENSEA_API_KEY="your-api-key"

# Install the CLI globally (or use npx)
npm install -g @opensea/cli

# Get collection info
opensea collections get boredapeyachtclub

# Get floor price and volume stats
opensea collections stats boredapeyachtclub

# Get NFT details
opensea nfts get ethereum 0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d 1234

# Get best listings for a collection
opensea listings best boredapeyachtclub --limit 5

# Search across OpenSea
opensea search "cool cats"

# Get trending tokens
opensea tokens trending --limit 5

# Get a swap quote
opensea swaps quote \
  --from-chain base --from-address 0x0000000000000000000000000000000000000000 \
  --to-chain base --to-address 0xTokenAddress \
  --quantity 0.02 --address 0xYourWallet
```

## 任务指南

> **推荐使用：** 使用 `opensea` CLI (`@opensea/cli`) 作为主要工具。它提供了统一的接口、结构化的输出和内置的分页功能。您可以通过 `npm install -g @opensea/cli` 或 `npx @opensea/cli` 来安装它。`scripts/` 目录中的 Shell 脚本也可以作为替代方案。

### 代币交换

OpenSea 的 API 包含了一个跨链 DEX 聚合器，可以支持在所有支持的链上以最优路径交换 ERC20 代币。

| 任务 | CLI 命令 | 替代命令 |
|------|------------|-------------|
| 获取交换报价 | `opensea swaps quote --from-chain <chain> --from-address <addr> --to-chain <chain> --to-address <addr> --quantity <qty> --address <wallet>` | `get_token_swap_quote` (MCP) 或 `opensea-swap.sh` |
| 获取热门代币 | `opensea tokens trending [--chains <chains>] [--limit <n>]` | `get_trending_tokens` (MCP) |
| 获取按交易量排序的顶级代币 | `opensea tokens top [--chains <chains>] [--limit <n>]` | `get_top_tokens` (MCP) |
| 获取代币详情 | `opensea tokens get <chain> <address>` | `get_tokens` (MCP) |
| 搜索代币 | `opensea search <query> --types token` | `search_tokens` (MCP) |
| 查看代币余额 | `get_token_balances` (MCP) | — |

### 阅读 NFT 数据

| 任务 | CLI 命令 | 替代命令 |
|------|------------|-------------|
| 获取收藏品详情 | `opensea collections get <slug>` | `opensea-collection.sh <slug>` |
| 获取收藏品统计信息 | `opensea collections stats <slug>` | `opensea-collection-stats.sh <slug>` |
| 列出收藏品中的 NFT | `opensea nfts list-by-collection <slug> [--limit <n>]` | `opensea-collection-nfts.sh <slug> [limit] [next]` |
| 获取单个 NFT | `opensea nfts get <chain> <contract> <token_id>` | `opensea-nft.sh <chain> <contract> <token_id>` |
| 按钱包列出 NFT | `opensea nfts list-by-account <chain> <address> [--limit <n>]` | `opensea-account-nfts.sh <chain> <address> [limit]` |
| 按合约列出 NFT | `opensea nfts list-by-contract <chain> <contract> [--limit <n>]` | — |
| 获取收藏品属性 | `opensea collections traits <slug>` | — |
| 获取合约详情 | `opensea nfts contract <chain> <address>` | — |
| 刷新 NFT 元数据 | `opensea nfts refresh <chain> <contract> <token_id>` | — |

### 市场查询

| 任务 | CLI 命令 | 替代命令 |
|------|------------|-------------|
| 获取收藏品的最佳 listing | `opensea listings best <slug> [--limit <n>]` | `opensea-best-listing.sh <slug> <token_id>` |
| 获取特定 NFT 的最佳 listing | `opensea listings best-for-nft <slug> <token_id>` | `opensea-best-listing.sh <slug> <token_id>` |
| 获取 NFT 的最佳报价 | `opensea offers best-for-nft <slug> <token_id>` | `opensea-best-offer.sh <slug> <token_id>` |
| 列出所有收藏品 listing | `opensea listings all <slug> [--limit <n>]` | `opensea-listings-collection.sh <slug> [limit]` |
| 列出所有收藏品报价 | `opensea offers all <slug> [--limit <n>]` | `opensea-offers-collection.sh <slug> [limit]` |
| 获取收藏品报价 | `opensea offers collection <slug> [--limit <n>]` | `opensea-offers-collection.sh <slug> [limit]` |
| 获取属性报价 | `opensea offers traits <slug> --type <type> --value <value>` | — |
| 按哈希获取订单 | — | `opensea-order.sh <chain> <order_hash>` |

### 市场操作（POST）

| 任务 | 脚本 |
|------|--------|
| 获取交易完成数据（购买 NFT） | `opensea-fulfill-listing.sh <chain> <order_hash> <buyer>` |
| 获取交易完成数据（接受报价） | `opensea-fulfill-offer.sh <chain> <order_hash> <seller> <contract> <token_id>` |
| 通用 POST 请求 | `opensea-post.sh <path> <json_body>` |

### 搜索

| 任务 | CLI 命令 |
|------|------------|
| 搜索收藏品 | `opensea search <query> --types collection` |
| 搜索 NFT | `opensea search <query> --types nft` |
| 搜索代币 | `opensea search <query> --types token` |
| 搜索账户 | `opensea search <query> --types account` |
| 搜索多种类型 | `opensea search <query> --types collection,nft,token` |
| 在特定链上搜索 | `opensea search <query> --chains base,ethereum` |

### 事件和监控

| 任务 | CLI 命令 | 替代命令 |
|------|------------|-------------|
| 列出最近的事件 | `opensea events list [--event-type <type>] [--limit <n>]` | — |
| 获取收藏品事件 | `opensea events by-collection <slug> [--event-type <type>]` | `opensea-events-collection.sh <slug> [event_type] [limit]` |
| 获取特定 NFT 的事件 | `opensea events by-nft <chain> <contract> <token_id>` | — |
| 获取账户事件 | `opensea events by-account <address>` | — |
| 实时流式事件 | — | `opensea-stream-collection.sh <slug>` （需要 websocat） |

事件类型：`sale`（销售）、`transfer`（转移）、`mint`（铸造）、`listing`（上架）、`offer`（报价）、`trait_offer`（属性报价）、`collection_offer`（收藏品报价）

### 账户

| 任务 | CLI 命令 |
|------|------------|
| 获取账户详情 | `opensea accounts get <address>` |

### 通用请求

| 任务 | 脚本 |
|------|--------|
| 任何 GET 端点 | `opensea-get.sh <path> [query]` |
| 任何 POST 端点 | `opensea-post.sh <path> <json_body>` |

## 买卖 NFT 的工作流程

### 购买 NFT

1. 找到 NFT 并查看其 listing：
   ```bash
   ./scripts/opensea-best-listing.sh cool-cats-nft 1234
   ```

2. 从响应中获取订单哈希，然后获取交易完成数据：
   ```bash
   ./scripts/opensea-fulfill-listing.sh ethereum 0x_order_hash 0x_your_wallet
   ```

3. 响应中包含可以在链上执行的交易数据。

### 卖出 NFT（接受报价）

1. 查看您的 NFT 的报价：
   ```bash
   ./scripts/opensea-best-offer.sh cool-cats-nft 1234
   ```

2. 获取报价的交易完成数据：
   ```bash
   ./scripts/opensea-fulfill-offer.sh ethereum 0x_offer_hash 0x_your_wallet 0x_nft_contract 1234
   ```

3. 执行返回的交易数据。

### 创建 listing/报价

创建新的 listing 和报价需要钱包签名。请使用 `opensea-post.sh` 并遵循 Seaport 的订单格式——详细信息请参见 `references/marketplace-api.md`。

## OpenSea CLI (`@opensea/cli`)

[OpenSea CLI](https://github.com/ProjectOpenSea/opensea-cli) 是 AI 代理与 OpenSea 交互的推荐方式。它提供了统一的命令行接口和程序化的 TypeScript/JavaScript SDK。

### 安装

```bash
# Install globally
npm install -g @opensea/cli

# Or use without installing
npx @opensea/cli collections get mfers
```

### 认证

```bash
# Set via environment variable (recommended)
export OPENSEA_API_KEY="your-api-key"
opensea collections get mfers

# Or pass inline
opensea --api-key your-api-key collections get mfers
```

### CLI 命令

| 命令 | 描述 |
|---|---|
| `collections` | 获取、列出、统计 NFT 收藏品的属性 |
| `nfts` | 获取、列出、刷新 NFT 的元数据和合约详情 |
| `listings` | 获取所有 listing、最佳 listing 或特定 NFT 的最佳 listing |
| `offers` | 获取所有报价、收藏品的报价、特定 NFT 的最佳报价 |
| `events` | 列出市场事件（销售、转移、铸造等） |
| `search` | 搜索收藏品、NFT、代币和账户 |
| `tokens` | 获取热门代币、顶级代币和代币详情 |
| `swaps` | 获取代币交易的交换报价 |
| `accounts` | 获取账户详情 |

全局选项：`--api-key`、`--chain`（默认：ethereum）、`--format`（json/table/toon）、`--base-url`、`--timeout`、`--verbose`

### 输出格式

- **JSON**（默认）：适合代理和脚本的结构化输出。
- **Table**：适合人类阅读的表格格式（`--format table`）。
- **TOON**：一种以代币为导向的序列化格式，比 JSON 使用的字符数量少约 40%——非常适合 LLM/AI 代理的上下文窗口（`--format toon`）。

```bash
# JSON output (default)
opensea collections stats mfers

# Human-readable table
opensea --format table collections stats mfers

# Compact TOON format (best for AI agents)
opensea --format toon tokens trending --limit 5
```

### 分页

所有列表命令都支持使用 `--limit` 和 `--next` 进行基于游标的分页：

```bash
# First page
opensea collections list --limit 5

# Pass the "next" cursor from the response to get the next page
opensea collections list --limit 5 --next "LXBrPTEwMDA..."
```

### 程序化 SDK

CLI 还提供了一个 TypeScript/JavaScript SDK，可用于脚本和应用程序：

```typescript
import { OpenSeaCLI, OpenSeaAPIError } from "@opensea/cli"

const client = new OpenSeaCLI({ apiKey: process.env.OPENSEA_API_KEY })

const collection = await client.collections.get("mfers")
const { nfts } = await client.nfts.listByCollection("mfers", { limit: 5 })
const { listings } = await client.listings.best("mfers", { limit: 10 })
const { asset_events } = await client.events.byCollection("mfers", { eventType: "sale" })
const { tokens } = await client.tokens.trending({ chains: ["base"], limit: 5 })
const results = await client.search.query("mfers", { limit: 5 })

// Swap quote
const { quote, transactions } = await client.swaps.quote({
  fromChain: "base",
  fromAddress: "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
  toChain: "base",
  toAddress: "0x3ec2156d4c0a9cbdab4a016633b7bcf6a8d68ea2",
  quantity: "1000000",
  address: "0xYourWalletAddress",
})

// Error handling
try {
  await client.collections.get("nonexistent")
} catch (error) {
  if (error instanceof OpenSeaAPIError) {
    console.error(error.statusCode)   // e.g. 404
    console.error(error.responseBody) // raw API response
    console.error(error.path)         // request path
  }
}
```

### TOON 格式（适用于 AI 代理）

TOON（Token-Oriented Object Notation）是一种紧凑的序列化格式，使用的字符数量比 JSON 少约 40%，非常适合将 CLI 输出传递到 LLM 上下文中：

```bash
opensea --format toon tokens trending --limit 3
```

示例输出：
```
tokens[3]{name,symbol,chain,market_cap,price_usd}:
  Ethereum,ETH,ethereum,250000000000,2100.50
  Bitcoin,BTC,bitcoin,900000000000,48000.00
  Solana,SOL,solana,30000000000,95.25
next: abc123
```

TOON 也可以通过编程方式使用：

```typescript
import { formatToon } from "@opensea/cli"

const data = await client.tokens.trending({ limit: 5 })
console.log(formatToon(data))
```

### CLI 退出代码

- `0` - 成功
- `1` - API 错误
- `2` - 认证错误

---

## Shell 脚本参考

`scripts/` 目录包含直接使用 `curl` 调用 OpenSea REST API 的 Shell 脚本。这些脚本是上述 CLI 的替代方案。

### NFT 和收藏品脚本
| 脚本 | 用途 |
|--------|---------|
| `opensea-get.sh` | 通用 GET 请求（路径 + 可选查询） |
| `opensea-post.sh` | 通用 POST 请求（路径 + JSON 数据） |
| `opensea-collection.sh` | 根据 slug 获取收藏品信息 |
| `opensea-collection-stats.sh` | 获取收藏品统计信息 |
| `opensea-collection-nfts.sh` | 列出收藏品中的 NFT |
| `opensea-nft.sh` | 根据链/合约/代币获取单个 NFT |
| `opensea-account-nfts.sh` | 列出钱包拥有的 NFT |

### 市场脚本
| 脚本 | 用途 |
|--------|---------|
| `opensea-listings-collection.sh` | 获取收藏品的所有 listing |
| `opensea-listings-nft.sh` | 获取特定 NFT 的 listing |
| `opensea-offers-collection.sh` | 获取收藏品的所有报价 |
| `opensea-best-listing.sh` | 获取 NFT 的最低报价 |
| `opensea-best-offer.sh` | 获取 NFT 的最高报价 |
| `opensea-order.sh` | 根据哈希获取订单 |
| `opensea-fulfill-listing.sh` | 获取购买交易数据 |
| `opensea-fulfill-offer.sh` | 获取销售交易数据 |

### 代币交换脚本
| 脚本 | 用途 |
|--------|---------|
| `opensea-swap.sh` | 通过 OpenSea MCP 进行代币交换 |

### 监控脚本
| 脚本 | 用途 |
|--------|---------|
| `opensea-events-collection.sh` | 收藏品事件历史记录 |
| `opensea-stream-collection.sh` | 实时 WebSocket 事件流 |

## 支持的链

`ethereum`、`matic`、`arbitrum`、`optimism`、`base`、`avalanche`、`klaytn`、`zora`、`blast`、`sepolia`

## 参考资料

- [OpenSea CLI GitHub](https://github.com/ProjectOpenSea/opensea-cli) - 完整的 CLI 和 SDK 文档
- [CLI 参考](https://github.com/ProjectOpenSea/opensea-cli/blob/main/docs/cli-reference.md) - 完整的命令参考
- [SDK 参考](https://github.com/ProjectOpenSea/opensea-cli/blob/main/docs/sdk.md) - 程序化 SDK API
- [CLI 示例](https://github.com/ProjectOpenSea/opensea-cli/blob/main/docs/examples.md) - 实际使用示例
- `references/rest-api.md` - REST 端点家族和分页
- `references/marketplace-api.md` - 买卖流程和 Seaport 详情
- `references/stream-api.md` - WebSocket 事件流
- `references/seaport.md` - Seaport 协议和 NFT 购买流程
- `references/token-swaps.md` - 通过 MCP 进行代币交换

## OpenSea MCP 服务器

OpenSea 的 MCP 服务器提供了官方的 LLM 集成，支持代币交换和 NFT 操作。启用后，Claude 可以执行交换、查询代币数据，并直接与 NFT 市场进行交互。

**设置：**

1. 访问 [OpenSea 开发者门户](https://opensea.io/settings/developer) 并验证您的电子邮件。
2. 为 REST API 访问生成一个新的 API 密钥。
3. 为 MCP 服务器生成一个单独的 MCP 令牌。

将令牌添加到您的 MCP 配置中：
```json
{
  "mcpServers": {
    "opensea": {
      "url": "https://mcp.opensea.io/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_MCP_TOKEN"
      }
    }
  }
}
```

或者使用内联令牌格式：`https://mcp.opensea.io/YOUR_MCP_TOKEN/mcp`

### 代币交换工具
| MCP 工具 | 用途 |
|----------|---------|
| `get_token_swap_quote` | **获取代币交易的交换报价** |
| `get_token_balances` | 查看钱包中的代币持有量 |
| `search_tokens` | 按名称/符号查找代币 |
| `get_trending_tokens` | 根据热度查找热门代币 |
| `get_top_tokens` | 根据 24 小时的交易量获取顶级代币 |
| `get_tokens` | 获取详细的代币信息 |

### NFT 工具
| MCP 工具 | 用途 |
|----------|---------|
| `search_collections` | 搜索 NFT 收藏品 |
| `search_items` | 搜索单个 NFT |
| `getcollections` | 获取详细的收藏品信息 |
| `get_items` | 获取详细的 NFT 信息 |
| `get_nft_balances` | 列出钱包拥有的 NFT |
| `get_trending_collections` | 热门 NFT 收藏品 |
| `get_top_collections` | 按交易量排序的顶级收藏品 |
| `get_activity` | 收藏品/物品的交易活动 |
| `get_upcoming_drops` | 即将发布的 NFT 铸造

### 账户和实用工具
| MCP 工具 | 用途 |
|----------|---------|
| `get_profile` | 显示钱包信息和活动记录 |
| `account_lookup` | 解析 ENS/地址/用户名 |
| `get_chains` | 列出支持的链 |
| `search` | 基于 AI 的自然语言搜索 |
| `fetch` | 根据实体 ID 获取完整信息 |

---

## 通过 MCP 进行代币交换

OpenSea MCP 支持在支持的 DEX 之间交换 ERC20 代币——不仅仅是 NFT！

### 获取交换报价
```bash
mcporter call opensea.get_token_swap_quote --args '{
  "fromContractAddress": "0x0000000000000000000000000000000000000000",
  "fromChain": "base",
  "toContractAddress": "0xb695559b26bb2c9703ef1935c37aeae9526bab07",
  "toChain": "base",
  "fromQuantity": "0.02",
  "address": "0xYourWalletAddress"
}'
```

**参数：**
- `fromContractAddress`：要交换的代币的合约地址（使用 `0x0000...0000` 表示原生 ETH）
- `toContractAddress`：要交换到的代币的合约地址
- `fromChain` / `toChain`：链标识符
- `fromQuantity`：以人类可读单位表示的数量（例如，“0.02”表示 0.02 ETH）
- `address`：您的钱包地址

**响应包含：**
- `swapQuote`：价格信息、费用、滑点影响
- `swap.actions[0].transactionSubmissionData`：可直接使用的交易数据

### 执行交换
```javascript
import { createWalletClient, http } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { base } from 'viem/chains';

// Extract from swap quote response
const txData = response.swap.actions[0].transactionSubmissionData;

const wallet = createWalletClient({ 
  account: privateKeyToAccount(PRIVATE_KEY), 
  chain: base, 
  transport: http() 
});

const hash = await wallet.sendTransaction({
  to: txData.to,
  data: txData.data,
  value: BigInt(txData.value)
});
```

### 查看代币余额
```bash
mcporter call opensea.get_token_balances --args '{
  "address": "0xYourWallet",
  "chains": ["base", "ethereum"]
}'
```

## 创建钱包

要执行交换或购买 NFT，您需要一个 Ethereum 钱包（私钥 + 地址）。

### 使用 Node.js
```javascript
import crypto from 'crypto';
import { privateKeyToAccount } from 'viem/accounts';

const privateKey = '0x' + crypto.randomBytes(32).toString('hex');
const account = privateKeyToAccount(privateKey);

console.log('Private Key:', privateKey);
console.log('Address:', account.address);
```

### 使用 OpenSSL
```bash
# Generate private key
PRIVATE_KEY="0x$(openssl rand -hex 32)"
echo "Private Key: $PRIVATE_KEY"

# Derive address (requires node + viem)
node --input-type=module -e "
import { privateKeyToAccount } from 'viem/accounts';
console.log('Address:', privateKeyToAccount('$PRIVATE_KEY').address);
"
```

### 使用 cast (Foundry)
```bash
cast wallet new
```

**重要提示：** 请安全存储私钥。切勿将它们提交到 git 或公开分享。

## 必需条件

- `OPENSEA_API_KEY` 环境变量（用于 CLI、SDK 和 REST API 脚本）
- `OPENSEA_MCP_TOKEN` 环境变量（用于 MCP 服务器，与 API 密钥分开）
- Node.js >= 18.0.0（用于 `@opensea-cli`）
- `curl`（用于 REST Shell 脚本）
- `websocat`（可选）（用于 WebSocket API）
- `jq`（推荐）（用于解析 Shell 脚本中的 JSON 响应）

您可以在 [opensea.io/settings/developer](https://opensea.io/settings/developer) 获取这些凭据。