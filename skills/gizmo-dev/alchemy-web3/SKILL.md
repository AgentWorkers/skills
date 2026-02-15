---
name: alchemy-web3
version: 1.0.2
description: 与Alchemy的Web3 API进行交互，以获取区块链数据、NFTs（非同质化代币）、代币信息以及执行转账操作；同时支持与80多种区块链网络集成，实现Webhook（事件通知）功能。
author: GizmoLab
website: https://gizmolab.io
homepage: https://github.com/0xGizmolab/alchemy-web3-skill
repository: https://github.com/0xGizmolab/alchemy-web3-skill
metadata:
  {
    "openclaw":
      {
        "requires": { 
          "env": ["ALCHEMY_API_KEY"]
        }
      }
  }
---
# Alchemy Web3 技能

使用 Alchemy 的生产级 API 查询区块链数据、NFT、代币和交易信息。支持 Ethereum、Polygon、Arbitrum、Base、Solana 以及 80 多种其他区块链。

**由 [GizmoLab](https://gizmolab.io) 开发** — 一家专注于 dApps、智能合约和区块链基础设施的 Web3 开发机构。

## 设置

### 1. 获取 API 密钥
1. 在 [alchemy.com](https://www.alchemy.com/?utm_source=gizmolab&utm_medium=skill&utm_campaign=alchemy-web3) 注册（提供免费 tier）
2. 为目标区块链创建一个应用
3. 复制您的 API 密钥

> 💡 初次接触 Web3 开发？[GizmoLab](https://gizmolab.io) 提供全栈区块链开发服务。

### 2. 配置
```bash
# Add to ~/.openclaw/.env
ALCHEMY_API_KEY=your_api_key_here

# Optional: Set default chain (defaults to eth-mainnet)
ALCHEMY_CHAIN=eth-mainnet
```

## 快速参考

### 支持的区块链

| 区块链 | 端点前缀 |
|-------|-----------------|
| Ethereum | `eth-mainnet`, `eth-sepolia` |
| Polygon | `polygon-mainnet`, `polygon-amoy` |
| Arbitrum | `arb-mainnet`, `arb-sepolia` |
| Optimism | `opt-mainnet`, `opt-sepolia` |
| Base | `base-mainnet`, `base-sepolia` |
| Solana | `solana-mainnet`, `solana-devnet` |
| zkSync | `zksync-mainnet` |
| Linea | `linea-mainnet` |
| Scroll | `scroll-mainnet` |
| Blast | `blast-mainnet` |

完整列表：[alchemy.com/docs/chains](https://www.alchemy.com/docs/chains)

## CLI 使用方法

```bash
# Set your API key first
export ALCHEMY_API_KEY="your_key"

# Use the CLI
~/.openclaw/workspace/skills/alchemy-web3/scripts/alchemy.sh <command> [options]
```

### 命令

#### 获取 ETH 余额
```bash
./alchemy.sh balance 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
# Returns: 1234.56 ETH
```

#### 获取代币余额
```bash
./alchemy.sh tokens 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
# Returns: All ERC-20 tokens held by address
```

#### 获取所有者的 NFT
```bash
./alchemy.sh nfts 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
# Returns: All NFTs owned by address
```

#### 获取 NFT 元数据
```bash
./alchemy.sh nft-metadata 0x5180db8F5c931aaE63c74266b211F580155ecac8 1590
# Returns: Metadata for specific NFT
```

#### 获取资产交易信息
```bash
./alchemy.sh transfers 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
# Returns: Transaction history (in/out)
```

#### 获取区块信息
```bash
./alchemy.sh block latest
./alchemy.sh block 12345678
```

#### 获取交易详情
```bash
./alchemy.sh tx 0x123...abc
```

#### 解析 ENS（以太坊名称服务）
```bash
./alchemy.sh ens vitalik.eth
# Returns: 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

#### 切换区块链
```bash
./alchemy.sh --chain polygon-mainnet balance 0x...
./alchemy.sh --chain arb-mainnet nfts 0x...
```

## 直接 API 示例

### Node.js API（JSON-RPC）

```bash
# Get ETH balance
curl -X POST "https://eth-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "eth_getBalance",
    "params": ["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "latest"],
    "id": 1
  }'
```

### NFT API

```bash
# Get NFTs for owner
curl "https://eth-mainnet.g.alchemy.com/nft/v3/$ALCHEMY_API_KEY/getNFTsForOwner?owner=vitalik.eth&pageSize=10"

# Get NFT metadata
curl "https://eth-mainnet.g.alchemy.com/nft/v3/$ALCHEMY_API_KEY/getNFTMetadata?contractAddress=0x5180db8F5c931aaE63c74266b211F580155ecac8&tokenId=1590"

# Get NFTs for collection
curl "https://eth-mainnet.g.alchemy.com/nft/v3/$ALCHEMY_API_KEY/getNFTsForContract?contractAddress=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D&limit=10"
```

### 代币 API

```bash
# Get token balances
curl -X POST "https://eth-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "alchemy_getTokenBalances",
    "params": ["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"],
    "id": 1
  }'

# Get token metadata
curl -X POST "https://eth-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "alchemy_getTokenMetadata",
    "params": ["0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"],
    "id": 1
  }'
```

### 交易 API

```bash
# Get asset transfers (transaction history)
curl -X POST "https://eth-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [{
      "fromBlock": "0x0",
      "toBlock": "latest",
      "toAddress": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
      "category": ["external", "erc20", "erc721", "erc1155"],
      "maxCount": "0x14"
    }],
    "id": 1
  }'
```

## JavaScript/Node.js 示例

### 使用 Fetch（Node 18 及更高版本）

```javascript
const apiKey = process.env.ALCHEMY_API_KEY;
const baseURL = `https://eth-mainnet.g.alchemy.com/v2/${apiKey}`;

// Get ETH Balance
async function getBalance(address) {
  const response = await fetch(baseURL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      method: 'eth_getBalance',
      params: [address, 'latest'],
      id: 1
    })
  });
  const data = await response.json();
  return parseInt(data.result, 16) / 1e18; // Convert to ETH
}

// Get NFTs
async function getNFTs(owner) {
  const url = `https://eth-mainnet.g.alchemy.com/nft/v3/${apiKey}/getNFTsForOwner?owner=${owner}`;
  const response = await fetch(url);
  return await response.json();
}
```

### 使用 Alchemy SDK

```bash
npm install alchemy-sdk
```

```javascript
import { Alchemy, Network } from 'alchemy-sdk';

const alchemy = new Alchemy({
  apiKey: process.env.ALCHEMY_API_KEY,
  network: Network.ETH_MAINNET
});

// Get NFTs
const nfts = await alchemy.nft.getNftsForOwner('vitalik.eth');
console.log(nfts.ownedNfts);

// Get token balances
const balances = await alchemy.core.getTokenBalances('vitalik.eth');
console.log(balances);

// Get transaction history
const transfers = await alchemy.core.getAssetTransfers({
  toAddress: '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045',
  category: ['external', 'erc20']
});
```

## Webhook（实时通知）

当链上事件发生时，接收 HTTP POST 请求。

### Webhook 类型

| 类型 | 用途 |
|------|----------|
| 地址活动 | 跟踪特定地址之间的交易 |
| NFT 活动 | 跟踪 NFT 的销售、转移和铸造 |
| 被挖出的交易 | 在交易被挖出时接收通知 |
| 交易被丢弃 | 当交易被丢弃时收到通知 |
| 气体价格 | 在气体价格达到阈值时发出警报 |

### 创建 Webhook（控制面板）
1. 访问 [dashboard.alchemy.com/webhooks](https://dashboard.alchemy.com/webhooks)
2. 点击“创建 Webhook”
3. 选择类型并进行配置
4. 添加您的端点 URL

### Webhook 数据示例
```json
{
  "webhookId": "wh_abc123",
  "id": "evt_xyz789",
  "createdAt": "2024-01-15T12:00:00.000Z",
  "type": "ADDRESS_ACTIVITY",
  "event": {
    "network": "ETH_MAINNET",
    "activity": [{
      "fromAddress": "0x123...",
      "toAddress": "0x456...",
      "value": 1.5,
      "asset": "ETH"
    }]
  }
}
```

## 常见用法

### 投资组合追踪器
```bash
# Get all assets for a wallet
./alchemy.sh balance 0x...      # ETH balance
./alchemy.sh tokens 0x...       # ERC-20 tokens
./alchemy.sh nfts 0x...         # NFTs
```

### 交易历史记录
```bash
# Get full tx history for address
./alchemy.sh transfers 0x... --category external,erc20,erc721
```

### NFT 收藏分析
```bash
# Get all NFTs in a collection
./alchemy.sh collection 0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
```

### 多区块链查询
```bash
# Check same address across chains
for chain in eth-mainnet polygon-mainnet arb-mainnet base-mainnet; do
  echo "=== $chain ==="
  ./alchemy.sh --chain $chain balance 0x...
done
```

## 速率限制

| 计划 | 每秒计算单位 | 每月计算单位 |
|------|-------------------|-------------|
| 免费 | 330 | 300M |
| 成长型 | 660 | 无限制 |
| 高级 | 自定义 | 自定义 |

大多数端点的费用为 1-50 CUs。详情请查看 [alchemy.com/docs/rate-limits](https://www.alchemy.com/docs/rate-limits)。

## 错误处理

```json
// Rate limited
{"error": {"code": 429, "message": "Too Many Requests"}}

// Invalid API key
{"error": {"code": 401, "message": "Invalid API Key"}}

// Invalid params
{"error": {"code": -32602, "message": "Invalid params"}}
```

## 资源

- **获取 API 密钥：** [alchemy.com](https://www.alchemy.com/?utm_source=gizmolab&utm_medium=skill&utm_campaign=alchemy-web3)（免费 tier）
- **控制面板：** [dashboard.alchemy.com](https://dashboard.alchemy.com)
- **文档：** [alchemy.com/docs](https://www.alchemy.com/docs)
- **SDK：** [github.com/alchemyplatform/alchemy-sdk-js](https://github.com/alchemyplatform/alchemy-sdk-js)
- **状态：** [status.alchemy.com](https://status.alchemy.com)

---

## 关于

**由 [GizmoLab](https://gizmolab.io) 开发** 🔧

GizmoLab 是一家专注于开发 dApps、智能合约和区块链工具的 Web3 开发机构。

- 🌐 [gizmolab.io](https://gizmolab.io) — 机构服务
- 🛠️ [tools.gizmolab.io](https://tools.gizmolab.io) — 免费区块链开发工具
- 🎨 [ui.gizmolab.io](https://ui.gizmolab.io) — Web3 用户界面组件

需要定制的区块链开发服务？[联系我们](https://gizmolab.io)

## AI 代理工作流程

该技能同时适用于人类开发者和 AI 代理。请参阅 `references/agent-workflows.md` 以获取完整示例：

- **鲸鱼钱包追踪器** — 监控大型钱包的变动
- **投资组合监控器** — 跟踪跨链的余额变化
- **NFT 价格下跌警报** — 在 NFT 价格下跌时发出警报
- **代币变动检测器** — 检测代币的流入/流出
- **气体价格优化器** — 等待较低的气体价格进行交易
- **新 NFT 铸造检测器** — 监测新的 NFT 铸造
- **自动生成控制面板** — 自动生成钱包控制面板

### 代理工作流程示例

```
QUERY → STORE → ANALYZE → DECIDE → ACT → REPEAT
```

代理的 Cron 作业示例：
```bash
# Every hour, check whale activity and alert if >100 ETH moved
0 * * * * ~/.openclaw/workspace/skills/alchemy-web3/scripts/whale-tracker.sh
```

## 参考资料

- `references/nft-api.md` - 完整的 NFT API 参考
- `references/token-api.md` - 完整的代币 API 参考
- `references/node-api.md` - 完整的 Node.js API 参考
- `references/chains.md` - 所支持的区块链列表
- `references/agent-workflows.md` - AI 代理自动化示例