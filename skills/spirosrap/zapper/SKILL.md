---
name: zapper
description: 通过 Zapper 的 GraphQL API 查询 50 多个区块链上的 DeFi 投资组合数据。适用于用户查看钱包余额、DeFi 持有情况、NFT 持有量、代币价格或交易历史等场景。支持 Base、Ethereum、Polygon、Arbitrum、Optimism 等区块链。需要使用 ZAPPER_API_KEY 进行身份验证。
metadata: {"clawdbot":{"emoji":"⚡","homepage":"https://zapper.xyz","requires":{"bins":["curl","jq","python3"]}}}
---

# Zapper 技能

通过 Zapper 的 GraphQL API，可以查询 50 多个链上的 DeFi 投资组合数据。

## 快速入门

### 设置

从 [Zapper 仪表板](https://dashboard.zapper.xyz/settings/api) 获取您的 API 密钥（免费 tier 可用）：

```bash
mkdir -p ~/.clawdbot/skills/zapper
cat > ~/.clawdbot/skills/zapper/config.json << 'EOF'
{
  "apiKey": "YOUR_ZAPPER_API_KEY"
}
EOF
```

### 基本用法

```bash
# Portfolio summary
scripts/zapper.sh portfolio 0x...

# Token holdings
scripts/zapper.sh tokens 0x...

# DeFi positions
scripts/zapper.sh apps 0x...

# NFT holdings
scripts/zapper.sh nfts 0x...

# Token price
scripts/zapper.sh price ETH

# Recent transactions
scripts/zapper.sh tx 0x...

# Unclaimed rewards
scripts/zapper.sh claimables 0x...
```

## 命令

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `portfolio <地址>` | 查看所有链上的代币余额及总数 | `zapper.sh portfolio 0x123...` |
| `tokens <地址>` | 查看详细的代币持有情况 | `zapper.sh tokens 0x123...` |
| `apps <地址>` | 查看 DeFi 交易（如锁定池、借贷、质押等） | `zapper.sh apps 0x123...` |
| `nfts <地址>` | 查看 NFT 持有情况 | `zapper.sh nfts 0x123...` |
| `price <符号>` | 查找代币价格 | `zapper.sh price ETH` |
| `tx <地址>` | 查看最近的交易记录（人类可读格式） | `zapper.sh tx 0x123...` |
| `claimables <地址>` | 查看未领取的奖励 | `zapper.sh claimables 0x123...` |

## 支持的网络

Zapper 支持 50 多个链，包括：

- Ethereum
- Base
- Polygon
- Arbitrum
- Optimism
- Avalanche
- BNB Chain
- zkSync
- Linea
- Scroll
- 以及更多...

## 使用场景

- **投资组合跟踪**：汇总所有链上的 DeFi 交易
- **收益管理**：查看可领取的奖励及未领取的奖励
- **NFT 投资组合**：追踪不同市场中的 NFT 持有情况
- **交易历史**：查看链上的交易记录（人类可读格式）
- **代币价格**：快速查询代币价格

## API 参考

所有 API 端点均使用 `POST https://public.zapper.xyzgraphql` 进行 GraphQL 查询。

完整的 API 文档请参阅 [references/api.md](references/api.md)。

## 所需工具

- `curl`：用于发送 HTTP 请求
- `jq`：用于解析 JSON 数据
- `python3`：用于格式化输出结果
- Zapper API 密钥（免费 tier 可用）

## 注意事项

- 所有 API 端点都需要 API 密钥
- 根据您的 Zapper 订阅计划，部分 API 会受到速率限制
- GraphQL 查询支持灵活的数据筛选功能