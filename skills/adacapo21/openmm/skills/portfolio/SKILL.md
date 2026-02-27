---
name: openmm-portfolio
version: 0.1.0
description: "使用 OpenMM 实现跨交易所的余额跟踪、订单概览以及市场数据查询功能。"
tags: [openmm, portfolio, balance, orders, market-data]
metadata:
  openclaw:
    emoji: "💼"
    requires:
      bins: [openmm]
      env: [MEXC_API_KEY, GATEIO_API_KEY, BITGET_API_KEY, KRAKEN_API_KEY]
    install:
      - kind: node
        package: "@3rd-eye-labs/openmm"
        bins: [openmm]
---
# OpenMM投资组合管理

跟踪账户余额、查看未成交订单，并监控各大交易所的市场数据。

## 查看余额

```bash
# All assets on an exchange
openmm balance --exchange mexc
openmm balance --exchange kraken

# Specific asset
openmm balance --exchange mexc --asset BTC
openmm balance --exchange kraken --asset ADA
openmm balance --exchange bitget --asset USDT

# JSON output
openmm balance --exchange mexc --json
```

要查看所有交易所的余额，请分别查询每个交易所：

```bash
openmm balance --exchange mexc
openmm balance --exchange gateio
openmm balance --exchange bitget
openmm balance --exchange kraken
```

## 查看未成交订单

```bash
# All open orders on an exchange
openmm orders list --exchange mexc

# Filter by trading pair
openmm orders list --exchange bitget --symbol SNEK/USDT

# Limit results
openmm orders list --exchange kraken --limit 5

# Get specific order details
openmm orders get --exchange mexc --id 123456 --symbol BTC/USDT
```

## 查看市场价格

```bash
# Current price
openmm ticker --exchange mexc --symbol BTC/USDT
openmm ticker --exchange kraken --symbol ADA/EUR

# Order book depth
openmm orderbook --exchange bitget --symbol SNEK/USDT --limit 10

# Recent trades
openmm trades --exchange mexc --symbol ETH/USDT --limit 50
```

## 比较不同交易所的价格

```bash
# Compare DEX and CEX prices for Cardano tokens
openmm price-comparison --symbol SNEK
openmm price-comparison --symbol INDY
```

## Cardano代币价格

```bash
# Aggregated price from DEX pools
openmm pool-discovery prices NIGHT
openmm pool-discovery prices SNEK

# Discover liquidity pools
openmm pool-discovery discover INDY
openmm pool-discovery discover SNEK --min-liquidity 50000
```

## MCP工具：投资组合概览

在使用MCP服务器时，以下工具对投资组合管理非常有用：

| 工具 | 描述 |
|------|-------------|
| `get_balance` | 获取某个交易所的余额（全部资产或特定资产） |
| `list_orders` | 列出该交易所的未成交订单 |
| `get_ticker` | 获取交易对的最新价格 |
| `get_strategy_status` | 查看带有未成交订单的网格策略及其价差 |
| `get_cardano_price` | 获取Cardano代币的汇总价格 |

MCP服务器还提供了一个`portfolio_overview`命令，可以自动汇总某个交易所的余额和未成交订单信息。

## 给代理的建议：

1. **交易前请先查看余额** —— 确认可用资金。
2. **分别查询每个交易所的数据** —— 没有跨交易所的数据汇总功能。
3. **使用`--json`参数进行数据解析** —— 以结构化格式输出数据，便于程序化使用。
4. **监控网格策略** —— 使用`get_strategy_status`工具查看当前激活的网格策略。