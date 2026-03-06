---
name: nansen-smart-money
description: 智能资金追踪功能：包括网络流量数据（Netflow）、交易记录、持仓情况、直接现金分配（DCAs）以及相关交易信息。该功能可用于识别哪些智能资金钱包正在进行买入/卖出操作，或追踪大型投资者（“鲸鱼投资者”）的交易活动。
metadata:
  openclaw:
    requires:
      env:
        - NANSEN_API_KEY
      bins:
        - nansen
    primaryEnv: NANSEN_API_KEY
    install:
      - kind: node
        package: nansen-cli
        bins: [nansen]
allowed-tools: Bash
---
# 智能资金（Smart Money）

所有命令：`nansen research smart-money <sub> [选项]`

## 子命令

```bash
# Netflow — what tokens are smart money accumulating?
nansen research smart-money netflow --chain solana --limit 10

# DEX trades — real-time spot trades by smart money
nansen research smart-money dex-trades --chain solana --labels "Smart Trader" --limit 20

# Holdings — aggregated SM portfolio
nansen research smart-money holdings --chain solana --limit 10

# DCAs — Jupiter DCA strategies (Solana only, no --chain needed)
nansen research smart-money dcas --limit 10

# Perp trades — Hyperliquid only (no --chain needed)
nansen research smart-money perp-trades --limit 10

# Historical holdings — time series of SM positions
nansen research smart-money historical-holdings --chain solana --days 30
```

## 标签（Labels）

使用 `--labels` 根据智能资金类别进行筛选：

| 标签 | 用途 |
|-------|----------|
| `Fund` | 加密基金 |
| `Smart Trader` | 历史表现最佳的投资者 |
| `30D Smart Trader` | 近30天内表现最佳的投资者 |
| `90D Smart Trader` | 过去90天内表现最佳的投资者 |
| `180D Smart Trader` | 过去180天内表现最佳的投资者 |
| `Smart HL Perps Trader` | 表现最活跃的投资者 |

```bash
nansen research smart-money netflow --chain solana --labels "Fund" --limit 10
```

## 标志（Flags）

| 标志 | 用途 |
|------|---------|
| `--chain` | 必需用于查询净流量（netflow）、去中心化交易所交易（dex-trades）、持仓（holdings）或历史持仓（historical-holdings） |
| `--labels` | 根据智能资金标签进行筛选（支持多词标签） |
| `--limit` | 显示结果的数量 |
| `--days` | 查看历史持仓的时间范围（默认为30天） |
| `--sort` | 对结果进行排序（例如：`value_usd:desc` 表示按美元价值降序排序） |
| `--fields` | 选择要显示的字段 |
| `--table` | 以表格形式输出结果 |
| `--format csv` | 以CSV格式导出结果 |

## 注意事项：

- `dcas` 仅适用于 Solana（Jupiter）网络，因此不需要使用 `--chain` 标志。
- `perp-trades` 仅适用于 Hyperliquid 网络，因此不需要使用 `--chain` 标志。
- 使用 `historical-holdings` 时需要指定 `--chain` 标志，可选地还需要指定 `--token-address`。