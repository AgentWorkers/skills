---
name: cryptoprice
description: 使用 Binance API 查询实时加密货币价格。可以获取比特币（Bitcoin）、以太坊（Ethereum）以及其他主要加密货币的最新价格。支持查询单个币种的信息，也可以显示热门币种的列表。
---
# CryptoPrice - 加密货币价格查询

使用官方的 Binance API 查询实时加密货币价格。

## 快速入门

### 查询热门货币的价格

```bash
uv run ~/.openclaw/skills/cryptoprice/scripts/cryptoprice.py
```

### 查询特定货币的价格

```bash
# Query Bitcoin
uv run ~/.openclaw/skills/cryptoprice/scripts/cryptoprice.py BTCUSDT

# Query Ethereum
uv run ~/.openclaw/skills/cryptoprice/scripts/cryptoprice.py ETHUSDT

# Shorthand (auto-completes USDT)
uv run ~/.openclaw/skills/cryptoprice/scripts/cryptoprice.py BTC
```

### 输出格式（JSON）

```bash
uv run ~/.openclaw/skills/cryptoprice/scripts/cryptoprice.py --json
uv run ~/.openclaw/skills/cryptoprice/scripts/cryptoprice.py BTC --json
```

### 列出所有交易对

```bash
uv run ~/.openclaw/skills/cryptoprice/scripts/cryptoprice.py --list
```

## 支持的货币

默认显示的热门货币包括：
- **BTC** - 比特币（Bitcoin）
- **ETH** - 以太坊（Ethereum）
- **BNB** - Binance Coin
- **SOL** - Solana
- **XRP** - Ripple
- **DOGE** - Dogecoin
- **ADA** - Cardano
- **AVAX** - Avalanche
- **DOT** - Polkadot
- **LINK** - Chainlink

## API 数据来源

- **Binance Spot API**：`https://api.binance.com/api/v3/ticker/price`
- 无需 API 密钥
- 提供低延迟的实时数据