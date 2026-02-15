# OpenSea API

您可以使用OpenSea API查询NFT数据，在Seaport市场上进行交易，以及在Ethereum、Base、Arbitrum、Optimism、Polygon等多个链上交换ERC20代币。

## 快速入门

1. 在您的环境中设置`OPENSEA_API_KEY`。
2. 使用`scripts/`目录中的辅助脚本执行常见操作。
3. 使用MCP服务器进行代币交换和高级查询。

```bash
export OPENSEA_API_KEY="your-api-key"

# Token swap: ETH to token
./scripts/opensea-swap.sh 0xTokenAddress 0.1 0xYourWallet 0xYourKey base

# Token swap: Token to token (specify from_token as last arg)
./scripts/opensea-swap.sh 0xToToken 100 0xYourWallet 0xYourKey base 0xFromToken

# Get collection info
./scripts/opensea-collection.sh boredapeyachtclub

# Get NFT details
./scripts/opensea-nft.sh ethereum 0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d 1234

# Get best listing price for an NFT
./scripts/opensea-best-listing.sh boredapeyachtclub 1234
```

## 任务指南

### 代币交换

OpenSea的API提供了一个跨链DEX聚合器，可以支持在所有支持的链上以最优路径交换ERC20代币。

| 任务 | 工具/脚本 |
|------|-------------|
| 获取代币交换报价 | `get_token_swap_quote`（MCP）或`opensea-swap.sh` |
| 查看代币余额 | `get_token_balances`（MCP） |
| 搜索代币 | `search_tokens`（MCP） |
| 获取热门代币 | `get_trending_tokens`（MCP） |
| 获取交易量最高的代币 | `get_top_tokens`（MCP） |

### 阅读NFT数据

| 任务 | 脚本 |
|------|--------|
| 获取收藏品详情 | `opensea-collection.sh <slug>` |
| 获取收藏品统计信息 | `opensea-collection-stats.sh <slug>` |
| 列出收藏品中的NFT | `opensea-collection-nfts.sh <slug> [limit] [next]` |
| 获取单个NFT | `opensea-nft.sh <chain> <contract> <token_id>` |
| 按钱包列出NFT | `opensea-account-nfts.sh <chain> <address> [limit]` |

### 市场查询

| 任务 | 脚本 |
|------|--------|
| 获取NFT的最佳挂牌信息 | `opensea-best-listing.sh <slug> <token_id>` |
| 获取NFT的最佳报价 | `opensea-best-offer.sh <slug> <token_id>` |
| 列出所有收藏品挂牌信息 | `opensea-listings-collection.sh <slug> [limit]` |
| 列出所有收藏品报价 | `opensea-offers-collection.sh <slug> [limit]` |
| 获取特定NFT的挂牌信息 | `opensea-listings-nft.sh <chain> <contract> <token_id>` |
| 获取特定NFT的报价 | `opensea-offers-nft.sh <chain> <contract> <token_id>` |
| 根据订单哈希获取订单信息 | `opensea-order.sh <chain> <order_hash>` |

### 市场操作（POST）

| 任务 | 脚本 |
|------|--------|
| 获取交易完成信息（购买NFT） | `opensea-fulfill-listing.sh <chain> <order_hash> <buyer>` |
| 获取交易完成信息（接受报价） | `opensea-fulfill-offer.sh <chain> <order_hash> <seller> <contract> <token_id>` |
| 通用POST请求 | `opensea-post.sh <path> <json_body>` |

### 事件与监控

| 任务 | 脚本 |
|------|--------|
| 获取收藏品事件 | `opensea-events-collection.sh <slug> [event_type] [limit]` |
| 实时流式事件 | `opensea-stream-collection.sh <slug>`（需要websocat） |

### 通用请求

| 任务 | 脚本 |
|------|--------|
| 任何GET接口 | `opensea-get.sh <path> [query]` |
| 任何POST接口 | `opensea-post.sh <path> <json_body>` |

## 买卖NFT的工作流程

### 购买NFT

1. 查找NFT并查看其挂牌信息：
   ```bash
   ./scripts/opensea-best-listing.sh cool-cats-nft 1234
   ```

2. 从响应中获取订单哈希，然后获取交易完成信息：
   ```bash
   ./scripts/opensea-fulfill-listing.sh ethereum 0x_order_hash 0x_your_wallet
   ```

3. 响应中包含可在链上执行的交易数据。

### 卖出NFT（接受报价）

1. 查看您的NFT的报价：
   ```bash
   ./scripts/opensea-best-offer.sh cool-cats-nft 1234
   ```

2. 获取报价的交易完成信息：
   ```bash
   ./scripts/opensea-fulfill-offer.sh ethereum 0x_offer_hash 0x_your_wallet 0x_nft_contract 1234
   ```

3. 执行返回的交易数据。

### 创建挂牌信息/报价

创建新的挂牌信息和报价需要钱包签名。请使用`opensea-post.sh`并遵循Seaport的订单格式——详情请参见`references/marketplace-api.md`。

## 脚本参考

### NFT与收藏品相关脚本
| 脚本 | 用途 |
|--------|---------|
| `opensea-get.sh` | 通用GET请求（路径+可选查询） |
| `opensea-post.sh` | 通用POST请求（路径+JSON数据） |
| `opensea-collection.sh` | 根据slug获取收藏品信息 |
| `opensea-collection-stats.sh` | 获取收藏品统计信息 |
| `opensea-collection-nfts.sh` | 列出收藏品中的NFT |
| `opensea-nft.sh` | 根据链/合约/代币获取单个NFT信息 |
| `opensea-account-nfts.sh` | 列出钱包拥有的NFT |

### 市场相关脚本
| 脚本 | 用途 |
|--------|---------|
| `opensea-listings-collection.sh` | 获取收藏品的所有挂牌信息 |
| `opensea-listings-nft.sh` | 获取特定NFT的挂牌信息 |
| `opensea-offers-collection.sh` | 获取收藏品的所有报价 |
| `opensea-best-listing.sh` | 获取NFT的最低挂牌价格 |
| `opensea-best-offer.sh` | 获取NFT的最高报价 |
| `opensea-order.sh` | 根据订单哈希获取订单信息 |
| `opensea-fulfill-listing.sh` | 获取购买交易信息 |
| `opensea-fulfill-offer.sh` | 获取出售交易信息 |

### 代币交换脚本
| 脚本 | 用途 |
|--------|---------|
| `opensea-swap.sh` | 通过OpenSea MCP进行代币交换 |

### 监控脚本
| 脚本 | 用途 |
|--------|---------|
| `opensea-events-collection.sh` | 收藏品事件历史记录 |
| `opensea-stream-collection.sh` | 实时WebSocket事件流 |

## 支持的链

`ethereum`, `matic`, `arbitrum`, `optimism`, `base`, `avalanche`, `klaytn`, `zora`, `blast`, `sepolia`

## 参考资料

- `references/rest-api.md` - REST接口及其分页机制
- `references/marketplace-api.md` - 买卖NFT的工作流程及Seaport详细信息
- `references/stream-api.md` - WebSocket事件流服务
- `references/seaport.md` - Seaport协议及NFT购买流程
- `references/token-swaps.md` - 通过MCP进行代币交换的流程

## OpenSea MCP服务器

OpenSea的官方MCP服务器提供了直接的LLM集成，支持代币交换和NFT操作。启用后，Claude可以执行交换、查询代币数据，并直接与NFT市场进行交互。

**设置步骤：**

1. 访问[OpenSea开发者门户](https://opensea.io/settings/developer)并验证您的电子邮件。
2. 为REST API访问生成一个新的API密钥。
3. 为MCP服务器生成一个单独的MCP令牌。

将令牌添加到您的MCP配置中：
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
| MCP工具 | 用途 |
|----------|---------|
| `get_token_swap_quote` | 获取代币交易的交换报价 |
| `get_token_balances` | 查看钱包中的代币持有量 |
| `search_tokens` | 按名称/符号搜索代币 |
| `get_trending_tokens` | 根据热度搜索热门代币 |
| `get_top_tokens` | 获取24小时交易量最高的代币 |
| `get_tokens` | 获取代币的详细信息 |

### NFT工具
| MCP工具 | 用途 |
|----------|---------|
| `search_collections` | 搜索NFT收藏品 |
| `search_items` | 搜索单个NFT |
| `get_collections` | 获取收藏品的详细信息 |
| `get_items` | 获取NFT的详细信息 |
| `get_nft_balances` | 列出钱包拥有的NFT |
| `get_trending_collections` | 热门NFT收藏品 |
| `get_top_collections` | 交易量最高的收藏品 |
| `get_activity` | 收藏品/物品的交易活动 |
| `get_upcoming_drops` | 即将发布的NFT |

### 账户与实用工具
| MCP工具 | 用途 |
|----------|---------|
| `get_profile` | 查看钱包信息及持有物品 |
| `account_lookup` | 解析ENS地址/用户名 |
| `get_chains` | 列出支持的链 |
| `search` | 基于AI的自然语言搜索 |
| `fetch` | 根据实体ID获取完整信息 |

---

## 通过MCP进行代币交换

OpenSea MCP支持在所有支持的DEX上交换ERC20代币——不仅仅是NFT！

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
- `fromContractAddress`: 需要交换的代币的合约地址（使用`0x0000...0000`表示原生ETH）
- `toContractAddress`: 目标代币的合约地址
- `fromChain` / `toChain`: 链的标识符
- `fromQuantity`: 以人类可读单位表示的数量（例如，“0.02”表示0.02 ETH）
- `address`: 您的钱包地址

**响应包含：**
- `swapQuote`: 价格信息、费用、滑点影响
- `swap.actions[0].transactionSubmissionData`: 可直接使用的交易数据

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

执行交换或购买NFT之前，您需要一个Ethereum钱包（私钥+地址）。

### 使用Node.js
```javascript
import crypto from 'crypto';
import { privateKeyToAccount } from 'viem/accounts';

const privateKey = '0x' + crypto.randomBytes(32).toString('hex');
const account = privateKeyToAccount(privateKey);

console.log('Private Key:', privateKey);
console.log('Address:', account.address);
```

### 使用OpenSSL
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

### 使用cast（Foundry）
```bash
cast wallet new
```

**重要提示：**请安全存储私钥。切勿将其提交到git或公开共享。

## 必需条件

- `OPENSEA_API_KEY`环境变量（用于REST API脚本）
- `OPENSEA_MCP_TOKEN`环境变量（用于MCP服务器，与API密钥分开）
- `curl`用于REST请求
- `websocat`（可选）用于WebSocket事件流
- `jq`（推荐）用于解析JSON响应

您可以在[opensea.io/settings/developer](https://opensea.io/settings/developer)获取这两个凭据。