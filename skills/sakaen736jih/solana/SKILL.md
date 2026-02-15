---
name: solana
description: 与 Solana 区块链交互：查询账户余额、查看交易记录、监控非同质化代币（NFT）的状态，并浏览账户信息。支持使用 Phantom 和 Solflare 地址进行操作。
metadata: {"openclaw":{"requires":{"bins":["solana"]},"install":[{"id":"solana","kind":"shell","command":"sh -c \"$(curl -sSfL https://release.solana.com/stable/install)\"","bins":["solana"],"label":"Install Solana CLI"}]}}
---

# Solana 钱包 CLI

## 设置

安装 Solana CLI：
```bash
sh -c "$(curl -sSfL https://release.solana.com/stable/install)"
```

设置主网 RPC（Mainnet RPC）：
```bash
solana config set --url https://api.mainnet-beta.solana.com
```

## 检查余额

SOL 的余额：
```bash
solana balance <ADDRESS>
```

以 lamports 为单位表示的余额：
```bash
solana balance <ADDRESS> --lamports
```

## 查看账户信息

```bash
solana account <ADDRESS>
```

详细的 JSON 输出：
```bash
solana account <ADDRESS> --output json
```

## 交易历史

最近的交易记录：
```bash
solana transaction-history <ADDRESS> --limit 10
```

交易详情：
```bash
solana confirm <SIGNATURE> -v
```

## 代币余额（SPL 代币）

列出所有代币：
```bash
spl-token accounts --owner <ADDRESS>
```

特定代币的余额：
```bash
spl-token balance <TOKEN_MINT> --owner <ADDRESS>
```

## NFT 与代币信息

使用 Metaboss（NFT 工具）：
```bash
# Install
cargo install metaboss

# Get NFT metadata
metaboss decode mint -a <NFT_MINT_ADDRESS>
```

## 持股账户

查看持股情况：
```bash
solana stakes <ADDRESS>
```

## 使用公共 RPC 端点

```bash
# Mainnet
solana config set --url https://api.mainnet-beta.solana.com

# Devnet (testing)
solana config set --url https://api.devnet.solana.com

# Custom RPC
solana config set --url https://your-rpc-provider.com
```

## 快速余额查询（使用 curl）

```bash
curl -X POST https://api.mainnet-beta.solana.com -H "Content-Type: application/json" -d '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getBalance",
  "params": ["<ADDRESS>"]
}' | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"{d['result']['value']/1e9:.4f} SOL\")"
```

## 获取代币账户信息（使用 curl）

```bash
curl -X POST https://api.mainnet-beta.solana.com -H "Content-Type: application/json" -d '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getTokenAccountsByOwner",
  "params": [
    "<ADDRESS>",
    {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
    {"encoding": "jsonParsed"}
  ]
}'
```

## 监控地址

实时监控地址的变化：
```bash
watch -n 5 "solana balance <ADDRESS>"
```

## 常见地址

| 名称 | 地址                |
|------|-------------------|
| SOL 钱包 | So11111111111111111111111111111111111111112 |
| USDC   | EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v |
| USDT   | Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB |

## 注意事项：

- 地址为经过 base58 编码的公钥
- 1 SOL = 1,000,000,000 lamports
- 公共 RPC 端点存在请求速率限制
- 在高频率使用的情况下，可以考虑使用付费的 RPC 服务提供商（如 Helius、QuickNode、Alchemy）