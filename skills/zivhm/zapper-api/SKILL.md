---
name: zapper-api
description: 通过 Zapper API 查询 DeFi 投资组合、代币持有情况、NFT、交易记录及价格。支持 50 多个区块链平台。适用于用户查询钱包余额、DeFi 交易情况、NFT 收藏、代币价格或交易历史等场景。
homepage: https://zapper.xyz
metadata: {"openclaw":{"emoji":"🟪","requires":{"bins":["python3"]},"primaryEnv":"ZAPPER_API_KEY"}}
---

# Zapper API

使用 Zapper 的 GraphQL API 可以查询 50 多个区块链上的 DeFi 投资组合、NFT 以及交易记录。

## 设置

1. 从 [Zapper 控制台](https://zapper.xyz/developers) 获取 API 密钥（提供免费 tier）。
2. 在 `~/.config/zapper/addresses.json` 文件中配置地址信息：
   ```json
   {
     "apiKey": "your-api-key",
     "wallets": [
       {"label": "Main", "address": "0x..."},
       {"label": "DeFi", "address": "0x..."}
     ]
   }
   ```

或者设置环境变量：`export ZAPPER_API_KEY="your-api-key"`

## 命令

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `portfolio <地址>` | 显示代币及 DeFi 投资总额 | `zapper.py portfolio 0x123...` |
| `tokens <地址>` | 查看详细的代币持有情况 | `zapper.py tokens 0x123...` |
| `apps <地址>` | 查看 DeFi 交易情况（如锁定资产、借贷、质押等） | `zapper.py apps 0x123...` |
| `nfts <地址>` | 按价值排序的 NFT 持有情况 | `zapper.py nfts 0x123...` |
| `tx <地址>` | 查看最近 30 天的交易记录 | `zapper.py tx 0x123...` |
| `price <符号>` | 查询代币价格 | `zapper.py price ETH` |
| `claimables <地址>` | 查看未领取的奖励 | `zapper.py claimables 0x123...` |
| `config` | 显示配置信息 | `zapper.py config` |

## 选项

| 标志 | 命令 | 描述 |
|------|----------|-------------|
| `--24h` | `portfolio`, `tokens` | 显示 24 小时的价格变化 |
| `--short` | `portfolio` | 仅输出总价值 |
| `--per-wallet` | `portfolio` | 分别显示每个配置的钱包的信息 |
| `--json` | `all` | 以原始 JSON 格式输出结果 |
| `--limit N` | `most` | 最多显示 N 个项目 |

## 使用方法

```bash
# Portfolio summary
python3 scripts/zapper.py portfolio 0xADDRESS

# With 24h price changes
python3 scripts/zapper.py portfolio 0xADDRESS --24h

# Just total value
python3 scripts/zapper.py portfolio 0xADDRESS --short

# Per-wallet breakdown
python3 scripts/zapper.py portfolio --per-wallet

# Token holdings with prices
python3 scripts/zapper.py tokens 0xADDRESS --24h

# DeFi positions
python3 scripts/zapper.py apps 0xADDRESS

# NFT holdings
python3 scripts/zapper.py nfts 0xADDRESS

# Recent transactions
python3 scripts/zapper.py tx 0xADDRESS

# Token price
python3 scripts/zapper.py price ETH

# Unclaimed rewards
python3 scripts/zapper.py claimables 0xADDRESS

# JSON output
python3 scripts/zapper.py portfolio 0xADDRESS --json
```

## 钱包标签

建议使用配置好的钱包标签代替具体的钱包地址：

```bash
python3 scripts/zapper.py portfolio "Main"
python3 scripts/zapper.py tokens "DeFi"
```

## 支持的代币（`price` 命令）

ETH, WETH, USDC, USDT, DAI, WBTC, LINK, UNI, AAVE, MKR

## 支持的区块链

Ethereum, Base, Arbitrum, Optimism, Polygon, Solana, BNB Chain, Avalanche, zkSync, Linea, Scroll, Blast 以及更多区块链。

## 注意事项

- 免费 tier 的 API 密钥可在 [zapper.xyz/developers](https://zapper.xyz/developers) 获取。
- 请避免频繁发送请求，以免超出 API 的速率限制。
- NFT 的估值基于最低价格。
- 交易历史记录仅保留最近 30 天的数据。

## 参考资料

- [API.md](references/API.md) - GraphQL 查询示例
- [Zapper 文档](https://build.zapper.xyz/docs/api/) - 官方 API 文档