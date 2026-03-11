---
name: indigo-analytics
description: "查询 Indigo 协议的 TVL（Total Value Locked）、协议统计数据、APR（年化回报率）以及 DEX（去中心化交易所）的收益数据。"
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
---
# Protocol Analytics

查询 Cardano 上 Indigo 协议的 TVL（锁定总价值）、协议统计数据、APR（年化回报率）以及 DEX（去中心化交易所）收益数据。

## MCP 工具

| 工具 | 描述 |
|------|-------------|
| `get_tvl` | 获取 Indigo 协议中锁定的总价值 |
| `get_protocol_stats` | 获取整个协议的统计数据和指标 |
| `get_apr_rewards` | 获取 Indigo 池中的 APR 回报率 |
| `get_apr_by_key` | 获取特定池的 APR 回报率 |
| `get_dex_yields` | 获取 Indigo iAsset 对的当前 DEX 收益数据 |

## 子技能

- [TVL 与统计数据](sub-skills/tvl-stats.md) — 锁定总价值与协议统计数据
- [APR 回报率](sub-skills/apr-rewards.md) — 池的 APR 回报率
- [DEX 收益数据](sub-skills/dex-yields.md) — iAsset 对的 DEX 收益数据

## 参考资料

- [MCP 工具参考](references/mcp-tools.md) — 工具的详细参数和返回类型
- [分析概念](references/concepts.md) — TVL、APR/APY、池类型及数据来源