---
name: ethereum
description: 与以太坊区块链交互：可以查看 ETH 和 ERC-20 类型的代币余额、交易记录、gas 费用信息以及 ENS（Ethereum Name Service）的相关信息。支持使用 MetaMask 进行操作。
metadata: {"openclaw":{"requires":{"bins":["cast"]},"install":[{"id":"foundry","kind":"shell","command":"curl -L https://foundry.paradigm.xyz | bash && foundryup","bins":["cast"],"label":"Install Foundry (cast)"}]}}
---

# Ethereum 钱包命令行界面（CLI）

## 设置

安装 Foundry（包含 `cast`）：
```bash
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

配置 RPC（可选）：
```bash
export ETH_RPC_URL="https://eth.llamarpc.com"
```

## 检查 ETH 余额

```bash
cast balance <ADDRESS> --rpc-url https://eth.llamarpc.com
```

以人类可读的形式显示余额：
```bash
cast balance <ADDRESS> --ether --rpc-url https://eth.llamarpc.com
```

## ENS 查找

将 ENS 解析为地址：
```bash
cast resolve-name vitalik.eth --rpc-url https://eth.llamarpc.com
```

反向查找（从地址到 ENS）：
```bash
cast lookup-address <ADDRESS> --rpc-url https://eth.llamarpc.com
```

## ERC-20 代币余额

```bash
# USDC balance (6 decimals)
cast call 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  "balanceOf(address)(uint256)" <ADDRESS> \
  --rpc-url https://eth.llamarpc.com

# Format with decimals
cast call 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  "balanceOf(address)(uint256)" <ADDRESS> \
  --rpc-url https://eth.llamarpc.com | xargs -I {} cast --to-unit {} 6
```

## 代币信息

```bash
# Token name
cast call <TOKEN_CONTRACT> "name()(string)" --rpc-url https://eth.llamarpc.com

# Token symbol
cast call <TOKEN_CONTRACT> "symbol()(string)" --rpc-url https://eth.llamarpc.com

# Decimals
cast call <TOKEN_CONTRACT> "decimals()(uint8)" --rpc-url https://eth.llamarpc.com

# Total supply
cast call <TOKEN_CONTRACT> "totalSupply()(uint256)" --rpc-url https://eth.llamarpc.com
```

## 交易信息

```bash
cast tx <TX_HASH> --rpc-url https://eth.llamarpc.com
```

交易收据：
```bash
cast receipt <TX_HASH> --rpc-url https://eth.llamarpc.com
```

## 气体价格

当前气体价格：
```bash
cast gas-price --rpc-url https://eth.llamarpc.com
```

单位：gwei
```bash
cast --to-unit $(cast gas-price --rpc-url https://eth.llamarpc.com) gwei
```

## 区块信息

最新区块：
```bash
cast block latest --rpc-url https://eth.llamarpc.com
```

特定区块：
```bash
cast block 17000000 --rpc-url https://eth.llamarpc.com
```

## NFT（ERC-721）所有者

```bash
cast call <NFT_CONTRACT> "ownerOf(uint256)(address)" <TOKEN_ID> --rpc-url https://eth.llamarpc.com
```

## 账户随机数（Nonce）

```bash
cast nonce <ADDRESS> --rpc-url https://eth.llamarpc.com
```

## 区块链信息

```bash
cast chain-id --rpc-url https://eth.llamarpc.com
```

## 常见代币合约

| 代币 | 合约地址 |
|-------|----------|
| USDC | 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 |
| USDT | 0xdAC17F958D2ee523a2206206994597C13D831ec7 |
| DAI | 0x6B175474E89094C44Da98b954EescdeCB5BE3830 |
| WETH | 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 |
| LINK | 0x514910771AF9Ca656af840dff83E8264EcF986CA |

## 公共 RPC 端点

| 提供者 | URL |
|----------|-----|
| LlamaRPC | https://eth.llamarpc.com |
| Ankr | https://rpc.ankr.com/eth |
| PublicNode | https://ethereum.publicnode.com |
| Cloudflare | https://cloudflare-eth.com |

## 注意事项

- 地址以 `0x` 开头，为 42 位的十六进制字符串
- 1 ETH = 10^18 wei
- 气体价格会波动，请在交易前查看最新价格
- 公共 RPC 服务存在速率限制
- 可使用 `--rpc-url` 参数或设置 `ETH_RPC_URL` 环境变量来指定 RPC 服务地址