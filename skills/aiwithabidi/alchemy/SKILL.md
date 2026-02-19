---
name: alchemy
description: "Alchemy — 一个用于处理区块链数据的工具，支持非同质化代币（NFTs）、代币余额、交易记录、gas价格以及Webhook功能的平台。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "⛓️", "requires": {"env": ["ALCHEMY_API_KEY"]}, "primaryEnv": "ALCHEMY_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# ⛓️ Alchemy

Alchemy 是一个用于处理区块链数据、非同质化代币（NFTs）、代币余额、交易、gas 价格以及 Webhook 的工具。

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `ALCHEMY_API_KEY` | ✅ | Alchemy API 密钥 |


## 快速入门

```bash
# Get ETH balance
python3 {{baseDir}}/scripts/alchemy.py get-balance --address <value>

# Get ERC-20 token balances
python3 {{baseDir}}/scripts/alchemy.py get-token-balances --address <value>

# Get transaction by hash
python3 {{baseDir}}/scripts/alchemy.py get-transaction --hash <value>

# Get block by number
python3 {{baseDir}}/scripts/alchemy.py get-block --block "latest"

# Get NFTs for address
python3 {{baseDir}}/scripts/alchemy.py get-nfts --address <value>

# Get NFT metadata
python3 {{baseDir}}/scripts/alchemy.py get-nft-metadata --contract <value> --token-id <value>

# Get token metadata
python3 {{baseDir}}/scripts/alchemy.py get-token-metadata --contract <value>

# Get current gas price
python3 {{baseDir}}/scripts/alchemy.py get-gas-price

# Get latest block number
python3 {{baseDir}}/scripts/alchemy.py get-block-number

# Get event logs
python3 {{baseDir}}/scripts/alchemy.py get-logs --address <value> --from-block "0x0" --to-block "latest" --topics <value>

# Get asset transfers for address
python3 {{baseDir}}/scripts/alchemy.py get-asset-transfers --address <value> --category "external,erc20"

# Get NFT floor price
python3 {{baseDir}}/scripts/alchemy.py get-floor-price --contract <value>
```


## 输出格式

所有命令默认以 JSON 格式输出结果。


## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/alchemy.py` | 主 CLI 工具——包含所有命令 |


## 致谢

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发  
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)  
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)