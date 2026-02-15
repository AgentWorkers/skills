---
name: openbroker
description: Hyperliquid 交易命令行界面（CLI）：用于执行市场订单、限价订单、管理持仓、查看资金费率以及运行交易策略。适用于所有与 Hyperliquid 相关的衍生品交易任务。
license: MIT
compatibility: Requires Node.js 22+, network access to api.hyperliquid.xyz
metadata:
  author: monemetrics
  version: "1.0.37"
allowed-tools: Bash(openbroker:*) Bash(npm:*) Read
---

# Open Broker - Hyperliquid Trading CLI

这是一个用于在Hyperliquid去中心化交易所（DEX）上执行交易操作的命令行工具，支持交易构建者费用（builder fees）的收取。

## 安装

```bash
npm install -g openbroker
```

## 快速入门

```bash
# 1. Setup (generates wallet, creates config, approves builder fee)
openbroker setup

# 2. Fund your wallet with USDC on Arbitrum, then deposit at https://app.hyperliquid.xyz/

# 3. Start trading
openbroker account
openbroker buy --coin ETH --size 0.1
```

## 命令参考

### 设置（Setup）
```bash
openbroker setup              # One-command setup (wallet + config + builder approval)
openbroker approve-builder --check  # Check builder fee status (for troubleshooting)
```

`setup`命令负责完成以下操作：
1. 生成新的钱包或使用现有的私钥；
2. 将配置信息保存到`~/.openbroker/.env`文件中；
3. 自动批准交易构建者费用（进行交易时必需）。

### 账户信息
```bash
openbroker account            # Balance, equity, margin
openbroker account --orders   # Include open orders
openbroker positions          # Open positions with PnL
openbroker positions --coin ETH  # Specific coin
```

### 资金费率
```bash
openbroker funding --top 20   # Top 20 by funding rate
openbroker funding --coin ETH # Specific coin
```

### 市场
```bash
openbroker markets --top 30   # Top 30 main perps
openbroker markets --coin BTC # Specific coin
```

### 所有市场（Perps、Spot、HIP-3）
```bash
openbroker all-markets                 # Show all markets
openbroker all-markets --type perp     # Main perps only
openbroker all-markets --type hip3     # HIP-3 perps only
openbroker all-markets --type spot     # Spot markets only
openbroker all-markets --top 20        # Top 20 by volume
```

### 搜索市场（跨提供商查找资产）
```bash
openbroker search --query GOLD    # Find all GOLD markets
openbroker search --query BTC     # Find BTC across all providers
openbroker search --query ETH --type perp  # ETH perps only
```

### 现货市场（Spot Markets）
```bash
openbroker spot                   # Show all spot markets
openbroker spot --coin PURR       # Show PURR market info
openbroker spot --balances        # Show your spot balances
openbroker spot --top 20          # Top 20 by volume
```

## 交易命令

### 市场订单（快速执行）
```bash
openbroker buy --coin ETH --size 0.1
openbroker sell --coin BTC --size 0.01
openbroker buy --coin SOL --size 5 --slippage 100  # Custom slippage (bps)
```

### 市场订单（详细设置）
```bash
openbroker market --coin ETH --side buy --size 0.1
openbroker market --coin BTC --side sell --size 0.01 --slippage 100
```

### 限价订单
```bash
openbroker limit --coin ETH --side buy --size 1 --price 3000
openbroker limit --coin SOL --side sell --size 10 --price 200 --tif ALO
```

### 为现有持仓设置止盈/止损（TP/SL）
```bash
# Set take profit at $40, stop loss at $30
openbroker tpsl --coin HYPE --tp 40 --sl 30

# Set TP at +10% from entry, SL at entry (breakeven)
openbroker tpsl --coin HYPE --tp +10% --sl entry

# Set only stop loss at -5% from entry
openbroker tpsl --coin ETH --sl -5%

# Partial position TP/SL
openbroker tpsl --coin ETH --tp 4000 --sl 3500 --size 0.5
```

### 触发订单（独立的止盈/止损）
```bash
# Take profit: sell when price rises to $40
openbroker trigger --coin HYPE --side sell --size 0.5 --trigger 40 --type tp

# Stop loss: sell when price drops to $30
openbroker trigger --coin HYPE --side sell --size 0.5 --trigger 30 --type sl
```

### 取消订单
```bash
openbroker cancel --all           # Cancel all orders
openbroker cancel --coin ETH      # Cancel ETH orders only
openbroker cancel --oid 123456    # Cancel specific order
```

## 高级交易策略

### 时间加权平均价格（TWAP）
```bash
# Execute 1 ETH buy over 1 hour (auto-calculates slices)
openbroker twap --coin ETH --side buy --size 1 --duration 3600

# Custom intervals with randomization
openbroker twap --coin BTC --side sell --size 0.5 --duration 1800 --intervals 6 --randomize 20
```

### 分批增减持仓（网格订单）
```bash
# Place 5 buy orders ranging 2% below current price
openbroker scale --coin ETH --side buy --size 1 --levels 5 --range 2

# Scale out with exponential distribution
openbroker scale --coin BTC --side sell --size 0.5 --levels 4 --range 3 --distribution exponential --reduce
```

### 框架订单（包含入场价、止盈价和止损价）
```bash
# Long ETH with 3% take profit and 1.5% stop loss
openbroker bracket --coin ETH --side buy --size 0.5 --tp 3 --sl 1.5

# Short with limit entry
openbroker bracket --coin BTC --side sell --size 0.1 --entry limit --price 100000 --tp 5 --sl 2
```

### 追踪价格订单（Chase Order）
```bash
# Chase buy with ALO orders until filled
openbroker chase --coin ETH --side buy --size 0.5 --timeout 300

# Aggressive chase with tight offset
openbroker chase --coin SOL --side buy --size 10 --offset 2 --timeout 60
```

## 交易策略

### 资金套利
```bash
# Collect funding on ETH if rate > 25% annualized
openbroker funding-arb --coin ETH --size 5000 --min-funding 25

# Run for 24 hours, check every 30 minutes
openbroker funding-arb --coin BTC --size 10000 --duration 24 --check 30 --dry
```

### 网格交易
```bash
# ETH grid from $3000-$4000 with 10 levels, 0.1 ETH per level
openbroker grid --coin ETH --lower 3000 --upper 4000 --grids 10 --size 0.1

# Accumulation grid (buys only)
openbroker grid --coin BTC --lower 90000 --upper 100000 --grids 5 --size 0.01 --mode long
```

### 定投（DCA）
```bash
# Buy $100 of ETH every hour for 24 hours
openbroker dca --coin ETH --amount 100 --interval 1h --count 24

# Invest $5000 in BTC over 30 days with daily purchases
openbroker dca --coin BTC --total 5000 --interval 1d --count 30
```

### 市场做市（Market Making）
```bash
# Market make ETH with 0.1 size, 10bps spread
openbroker mm-spread --coin ETH --size 0.1 --spread 10

# Tighter spread with position limit
openbroker mm-spread --coin BTC --size 0.01 --spread 5 --max-position 0.1
```

### 仅限做市商的订单（Maker-Only Orders）
```bash
# Market make using ALO (post-only) orders - guarantees maker rebates
openbroker mm-maker --coin HYPE --size 1 --offset 1

# Wider offset for volatile assets
openbroker mm-maker --coin ETH --size 0.1 --offset 2 --max-position 0.5
```

## 订单类型

### 限价订单与触发订单

**限价订单（`openbroker limit`）**：
- 一旦价格达到设定价格，立即执行；
- 保留在订单簿中，直到成交或被取消；
- 低于当前价格的限价卖单会立即成交（成为市场的买家）；
- 不适合用于设置止损。

**触发订单（`openbroker trigger`、`openbroker tpsl`）**：
- 在触发价格达到之前保持闲置状态；
- 仅当价格触及触发水平时才会执行；
- 是设置止损和获利的好方法；
- 不会提前成交。

### 适用场景

| 场景 | 使用的命令 |
|----------|---------|
| 以低于市场的价格买入 | `openbroker limit` |
| 以高于市场的价格卖出 | `openbroker limit` |
| 设置止损（价格下跌时退出） | `openbroker trigger --type sl` |
| 设定获利（达到目标价格时退出） | `openbroker trigger --type tp` |
| 为现有持仓添加止盈/止损 | `openbroker tpsl` |

## 常用参数

所有命令都支持`--dry`参数，用于执行前的预览（不实际执行操作）。

| 参数 | 说明 |
|----------|-------------|
| `--coin` | 资产代号（如ETH、BTC、SOL等） |
| `--side` | 订单方向：`buy`（买入）或`sell`（卖出） |
| `--size` | 订单数量（以基础资产计） |
| `--price` | 限价 |
| `--dry` | 预览操作（不执行） |
| `--help` | 显示命令帮助信息 |

### 订单参数

| 参数 | 说明 |
|----------|-------------|
| `--trigger` | 触发价格（针对触发订单） |
| `--type` | 触发类型：`tp`（止盈）或`sl`（止损） |
| `--slippage` | 价格滑点（以基点为单位） |
| `--tif` | 订单有效期：GTC（立即执行）、IOC（成交即结算）或ALO（自动取消） |
| `--reduce` | 仅用于减少持仓数量的订单 |

### 止盈/止损价格格式

| 格式 | 例子 | 说明 |
|--------|---------|-------------|
| 绝对值 | `--tp 40` | 定价为40美元 |
| 比例上升 | `--tp +10%` | 比入场价高10% |
| 比例下降 | `--sl -5%` | 比入场价低5% |
| 入场价格 | `--sl entry` | 设定为入场价 |

## 配置

配置信息按以下优先级加载：
1. 环境变量；
2. 当前目录下的`.env`文件；
3. `~/.openbroker/.env`文件（全局配置）。

运行`openbroker setup`命令可以交互式地创建全局配置。

| 参数 | 是否必填 | 说明 |
|----------|----------|-------------|
| `HYPERLIQUID_PRIVATE_KEY` | 是 | 钱包私钥（格式为0x...） |
| `HYPERLIQUID_NETWORK` | 否 | 默认为`mainnet`，也可设置为`testnet` |
| `HYPERLIQUID_ACCOUNT_ADDRESS` | 否 | 用于API钱包 |

## 风险提示

- 使用命令前请务必先使用`--dry`参数进行预览；
- 在测试网（`HYPERLIQUID_NETWORK=testnet`）上从小额交易开始；
- 定期监控持仓情况和清算价格；
- 仅使用`--reduce`参数来减少持仓数量。