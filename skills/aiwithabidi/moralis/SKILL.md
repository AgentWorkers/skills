---
name: moralis
description: "Moralis — 提供Web3数据、代币价格、钱包历史记录、NFT信息、DeFi持仓情况以及区块链事件的相关服务。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🌐", "requires": {"env": ["MORALIS_API_KEY"]}, "primaryEnv": "MORALIS_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🌐 Moralis

Moralis 是一个工具，用于查询 Web3 数据、代币价格、钱包历史记录、NFT 信息、DeFi 持仓情况以及区块链事件。

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `MORALIS_API_KEY` | ✅ | Moralis 的 API 密钥 |

## 快速入门

```bash
# Get native balance
python3 {{baseDir}}/scripts/moralis.py get-native-balance --address <value> --chain "eth"

# Get ERC-20 token balances
python3 {{baseDir}}/scripts/moralis.py get-token-balances --address <value> --chain "eth"

# Get wallet transactions
python3 {{baseDir}}/scripts/moralis.py get-transactions --address <value> --chain "eth"

# Get token price
python3 {{baseDir}}/scripts/moralis.py get-token-price --address <value> --chain "eth"

# Get NFTs for wallet
python3 {{baseDir}}/scripts/moralis.py get-nfts --address <value> --chain "eth"

# Get NFT metadata
python3 {{baseDir}}/scripts/moralis.py get-nft-metadata --address <value> --token-id <value> --chain "eth"

# Get NFT transfers
python3 {{baseDir}}/scripts/moralis.py get-nft-transfers --address <value> --chain "eth"

# Get token transfers
python3 {{baseDir}}/scripts/moralis.py get-token-transfers --address <value> --chain "eth"

# Get DeFi positions
python3 {{baseDir}}/scripts/moralis.py get-defi-positions --address <value> --chain "eth"

# Resolve ENS/Unstoppable domain
python3 {{baseDir}}/scripts/moralis.py resolve-domain --domain <value>

# Search token by symbol
python3 {{baseDir}}/scripts/moralis.py search-token --symbol <value>

# Get block details
python3 {{baseDir}}/scripts/moralis.py get-block --block <value> --chain "eth"
```

## 输出格式

所有命令默认以 JSON 格式输出结果。

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/moralis.py` | 主要的命令行工具（包含所有 Moralis 命令） |

## 致谢

Moralis 由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
相关视频教程可在 [YouTube](https://youtube.com/@aiwithabidi) 查看，源代码托管在 [GitHub](https://github.com/aiwithabidi) 上。  
Moralis 是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理程序设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)