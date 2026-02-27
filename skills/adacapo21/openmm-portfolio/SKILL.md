---
name: openmm-portfolio
description: "使用 OpenMM 实现跨交易所的余额追踪、订单概览以及市场数据管理。"
allowed-tools: Read, Glob, Grep, Bash(openmm:*)
license: MIT
metadata:
  author: qbtlabs
  version: '0.1.1'
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

跟踪账户余额、查看未成交订单，并监控多个交易所的市场数据。

## 所需凭据

必须通过环境变量配置至少一个交易所的凭据。请为想要查询的每个交易所设置相应的凭据：

```bash
# MEXC
MEXC_API_KEY=your-mexc-api-key
MEXC_SECRET=your-mexc-secret
MEXC_UID=your-mexc-uid-for-whitelisted-access

# Gate.io
GATEIO_API_KEY=your-gateio-api-key
GATEIO_SECRET=your-gateio-secret

# Bitget (requires passphrase)
BITGET_API_KEY=your-bitget-api-key
BITGET_SECRET=your-bitget-secret
BITGET_PASSPHRASE=your-bitget-passphrase

# Kraken
KRAKEN_API_KEY=your-kraken-api-key
KRAKEN_SECRET=your-kraken-secret
```

有关详细的配置说明，请参阅**openmm-exchange-setup**技能。

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
```

## 检查市场价格

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
| `list_orders` | 列出某个交易所的未成交订单 |
| `get_ticker` | 获取交易对的当前价格 |
| `get_orderbook` | 订单簿深度（买盘/卖盘） |
| `get_trades` | 最近的交易记录及买卖汇总 |
| `get_cardano_price` | Cardano代币的聚合价格 |
| `discover_pools` | 查找Cardano去中心化交易所（DEX）的流动性池 |

## 给代理的建议

1. **交易前请检查余额** —— 始终核实可用资金。
2. **分别查询每个交易所** —— 没有跨交易所的汇总命令。
3. **使用`--json`格式输出** —— 便于程序化处理。
4. **使用`BASE/QUOTE`格式** —— 例如：`BTC/USDT`、`ADA/EUR`、`SNEK/USDT`。
5. **遵守最低订单金额要求** —— MEXC/Gate.io/Bitget：1 USDT；Kraken：5 EUR/USD。