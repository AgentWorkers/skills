---
name: find-arbitrage-opps
description: 通过比较 BTC/WBTC 和 USDT/USDC 等可互换代币对的价格，在不同交易所之间寻找套利机会。
metadata:
  author: hummingbot
---
# find-arbitrage-opps

该脚本用于通过比较交易对的价格来寻找所有与 Hummingbot 连接的交易所中的套利机会，同时考虑可互换的代币（例如：BTC = WBTC, USDT = USDC）。

## 先决条件

必须运行 Hummingbot API，并且已配置交易所连接器：

```bash
bash <(curl -s https://raw.githubusercontent.com/hummingbot/skills/main/skills/lp-agent/scripts/check_prerequisites.sh)
```

## 工作流程

### 第一步：定义代币映射

用户需要指定基础代币和报价代币，包括它们的可互换形式：

- **基础代币**：BTC、WBTC、cbBTC（均代表比特币）
- **报价代币**：USDT、USDC、USD（均代表美元）

### 第二步：寻找套利机会

```bash
# Basic usage - find BTC/USDT arb opportunities
python scripts/find_arb_opps.py --base BTC --quote USDT

# Include fungible tokens
python scripts/find_arb_opps.py --base BTC,WBTC --quote USDT,USDC

# More examples
python scripts/find_arb_opps.py --base ETH,WETH --quote USDT,USDC,USD
python scripts/find_arb_opps.py --base SOL --quote USDT,USDC --min-spread 0.1

# Filter by specific connectors
python scripts/find_arb_opps.py --base BTC --quote USDT --connectors binance,kraken,coinbase
```

### 第三步：分析结果

脚本会输出以下信息：
- 各交易所的价格
- 所有交易所中的最佳买价/卖价
- 套利差（低价买入，高价卖出）
- 建议的套利交易对

## 脚本选项

```bash
python scripts/find_arb_opps.py --help
```

| 选项 | 描述 |
|--------|-------------|
| `--base` | 基础代币，用逗号分隔（例如：BTC,WBTC） |
| `--quote` | 报价代币，用逗号分隔（例如：USDT,USDC） |
| `--connectors` | 过滤特定交易所连接器（可选） |
| `--min-spread` | 显示的最小价差百分比（默认值：0.0%） |
| `--json` | 以 JSON 格式输出结果 |

## 输出示例

```
Arbitrage Opportunities: BTC vs USDT
=====================================

Prices Found:
  binance          BTC-USDT     $67,234.50
  kraken           BTC-USD      $67,289.00
  coinbase         BTC-USD      $67,312.25
  okx              BTC-USDT     $67,198.00
  hyperliquid      BTC-USD      $67,245.00

Best Opportunities:
  Buy  okx BTC-USDT @ $67,198.00
  Sell coinbase BTC-USD @ $67,312.25
  Spread: 0.17% ($114.25)
```

## 环境变量

脚本会查找以下位置的 `.env` 文件：
- `./hummingbot-api/.env` → `~/.hummingbot/.env` → `.env`

## 要求

- Hummingbot API 必须正在运行
- 交易所连接器已配置相应的 API 密钥