---
name: onchain
description: 这是一个用于跟踪加密货币投资组合、市场数据以及交易所（CEX）交易历史的命令行界面（CLI）。当用户询问加密货币价格、钱包余额、投资组合价值、Coinbase/Binance的持有情况，或是Polymarket的预测结果时，可以使用该CLI。
---

# Onchain CLI

这是一个用于追踪加密货币投资组合、获取市场数据以及查询加密货币交易所（CEX）历史记录的命令行工具（CLI）。

## 使用方法

```
onchain <command>
```

## 命令

### 市场数据查询

```bash
onchain price <token>         # Token price (btc, eth, sol, etc.)
onchain markets               # Market overview with trending
```

### 钱包信息查询

```bash
onchain balance [address]           # Token balances (auto-detects EVM/Solana)
onchain balance --chain polygon     # Filter by chain
onchain history [address]           # Transaction history
onchain portfolio [address]         # Full portfolio with DeFi positions
```

### 加密货币交易所（CEX）信息查询

```bash
onchain coinbase balance      # Coinbase balances
onchain coinbase history      # Coinbase trade history
onchain binance balance       # Binance balances
onchain binance history       # Binance trade history
```

### 预测市场信息查询

```bash
onchain polymarket trending          # Trending markets
onchain polymarket search <query>    # Search markets
onchain polymarket view <slug>       # View market details
```

### 配置设置

```bash
onchain setup                 # Interactive setup wizard
onchain config                # View current config
onchain config wallet add <name> <address>
onchain config wallet set-default <name>
```

## 全局选项

- `--json` - 以 JSON 格式输出结果（适用于脚本程序）
- `--plain` - 禁用颜色和表情符号
- `--timeout <ms>` - 请求超时时间（以毫秒为单位）

## 配置文件

配置文件路径：`~/.config/onchain/config.json5`

### 必需的 API 密钥

| 功能          | API 密钥                | 获取方式                |
|---------------|------------------|----------------------|
| EVM 钱包        | `DEBANK_API_KEY`           | [DeBank](https://cloud.debank.com/)         |
| Solana 钱包        | `HELIUS_API_KEY`           | [Helius](https://helius.xyz/)         |
| Coinbase CEX      | `COINBASE_API_KEY` + `COINBASE_API_SECRET` | [Coinbase](https://www.coinbase.com/settings/api) |
| Binance CEX      | `BINANCE_API_KEY` + `BINANCE_API_SECRET` | [Binance](https://www.binance.com/en/my/settings/api-management) |

### 可选的 API 密钥

| 功能          | API 密钥                | 备注                        |
|---------------|------------------|--------------------------|
| 市场数据查询       | `COINGECKO_API_KEY`         | 免费 tier 可使用；Pro tier 提供更高数据量 |
| 市场数据备用来源 | `COINMARKETCAP_API_KEY`       | 替代市场数据源                |

## 示例用法

### 获取比特币价格

```bash
onchain price btc
```

### 查看钱包余额

```bash
onchain balance 0x1234...5678
```

### 查看包含 DeFi 项目的投资组合

```bash
onchain portfolio main  # Uses saved wallet named "main"
```

### 获取热门的预测市场信息

```bash
onchain polymarket trending -n 5
```

### 为脚本提供 JSON 格式输出

```bash
onchain --json price eth | jq '.priceUsd'
```

## 支持的区块链平台

### EVM（通过 DeBank）

Ethereum、BNB Chain、Polygon、Arbitrum、Optimism、Avalanche、Base、zkSync Era、Linea、Scroll、Blast、Mantle、Gnosis、Fantom、Celo 等。

### Solana（通过 Helius）

支持 Solana 主网的所有功能，包括 SPL 代币和 NFT。

## 代理程序集成

该 CLI 专为代理程序设计。使用建议：

1. **始终使用 `--json` 选项** 以进行程序化访问。
2. **检查退出代码**：0 表示成功，1 表示错误。
3. **使用已保存的钱包信息**：通过 `onchain setup` 配置钱包信息，之后可通过名称直接引用。
4. **实施速率限制**：部分 API 有请求速率限制，请在频繁调用时添加延迟。

### 代理程序使用示例

```bash
# Get portfolio value
VALUE=$(onchain --json portfolio main | jq -r '.totalValueUsd')

# Get price with change
onchain --json price btc | jq '{price: .priceUsd, change24h: .priceChange24h}'

# Check if market is bullish
CHANGE=$(onchain --json markets | jq '.marketCapChange24h')
```