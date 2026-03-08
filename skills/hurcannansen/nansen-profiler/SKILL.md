---
name: nansen-profiler
description: 钱包分析工具——可查看余额、盈亏情况（PnL）、标签信息、交易记录、交易对手方、关联钱包、批量处理功能以及交易追踪功能。适用于分析特定钱包地址或比较不同钱包的状态。
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
# 钱包分析器

所有命令的通用格式为：`nansen research profiler <sub> [选项]`

大多数命令都需要使用 `--address` 和 `--chain` 参数。

## 账户余额与身份信息

```bash
nansen research profiler balance --address <addr> --chain ethereum
nansen research profiler labels --address <addr> --chain ethereum
nansen research profiler search --query "Vitalik"
```

## 盈亏（PnL）

```bash
nansen research profiler pnl --address <addr> --chain ethereum --days 30
nansen research profiler pnl-summary --address <addr> --chain ethereum
```

## 交易记录与历史数据

```bash
nansen research profiler transactions --address <addr> --chain ethereum --limit 20
nansen research profiler historical-balances --address <addr> --chain solana --days 30
```

## 账户之间的关系

```bash
nansen research profiler related-wallets --address <addr> --chain ethereum
nansen research profiler counterparties --address <addr> --chain ethereum --days 30
```

## 涉嫌违规者（无需指定 `--chain` 参数）

```bash
nansen research profiler perp-positions --address <addr>
nansen research profiler perp-trades --address <addr> --days 7
```

## 批量处理、交易追踪与比较

```bash
# Batch — profile multiple wallets at once
nansen research profiler batch \
  --addresses "0xabc,0xdef" --chain ethereum \
  --include labels,balance,pnl

# Trace — BFS multi-hop counterparty trace (makes N*width API calls)
nansen research profiler trace --address <addr> --chain ethereum --depth 2 --width 5

# Compare — shared counterparties and tokens between two wallets
nansen research profiler compare --addresses "0xabc,0xdef" --chain ethereum
```

## 各种选项

| 选项 | 作用 |
|------|---------|
| `--address` | 钱包地址（必填） |
| `--chain` | 除“涉嫌违规者”和“搜索”功能外，其他功能均需指定链路 |
| `--days` | 回顾期（默认为30天） |
| `--limit` | 返回的结果数量 |
| `--include` | 包含的字段：`labels`、`balance`、`pnl` |
| `--depth` | 交易追踪的深度（1-5层，默认为2层） |
| `--width` | 交易追踪的显示宽度；保持较窄以节省资源 |
| `--fields` | 选择要显示的特定字段 |
| `--table` | 以表格形式输出结果 |
| `--format csv` | 将结果导出为CSV格式 |

## 注意事项：

- `pnl-summary` 功能不支持分页（返回的是汇总数据，而非详细列表）。
- `perp-positions` 功能不支持分页。
- `labels` 功能不支持分页；API会忽略 `per_page` 参数，始终返回该地址的所有标签信息。此子命令不支持 `--limit` 参数。
- `transactions` 功能的分页限制为每页100条记录（API限制）。
- `trace` 功能会进行大量API调用，建议适当减小 `--width` 的值以节省资源。
- `batch` 功能支持使用 `--file <路径>` 参数，每行记录一个钱包地址，作为 `--addresses` 参数的替代方式。