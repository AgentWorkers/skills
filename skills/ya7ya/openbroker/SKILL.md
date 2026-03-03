---
name: openbroker
description: Hyperliquid交易插件具备后台持仓监控功能：可执行市场订单和限价订单，管理持仓情况，查看资金利率，并运行交易策略。同时，该插件会自动提醒用户盈亏变化及清算风险。
license: MIT
compatibility: Requires Node.js 22+, network access to api.hyperliquid.xyz
homepage: https://www.npmjs.com/package/openbroker
metadata: {"author": "monemetrics", "version": "1.0.45", "openclaw": {"requires": {"bins": ["openbroker"], "env": ["HYPERLIQUID_PRIVATE_KEY"]}, "primaryEnv": "HYPERLIQUID_PRIVATE_KEY", "install": [{"id": "node", "kind": "node", "package": "openbroker", "bins": ["openbroker"], "label": "Install openbroker (npm)"}]}}
allowed-tools: ob_account ob_positions ob_funding ob_markets ob_search ob_spot ob_fills ob_orders ob_order_status ob_fees ob_candles ob_funding_history ob_trades ob_rate_limit ob_buy ob_sell ob_limit ob_trigger ob_tpsl ob_cancel ob_twap ob_bracket ob_chase ob_watcher_status Bash(openbroker:*)
---
# Open Broker - Hyperliquid Trading CLI

这是一个用于在Hyperliquid去中心化交易所（DEX）上执行交易操作的命令行工具，支持交易手续费（builder fee）的收取。

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

`setup`命令提供了三种模式：
1. **导入现有密钥** — 使用您已有的私钥（主钱包）
2. **生成新钱包** — 创建一个新的主钱包
3. **生成API钱包**（推荐给代理使用） — 该钱包可以交易，但不能取款

对于第1和第2种模式，`setup`会自动保存配置并批准交易手续费。
关于第3种模式（API钱包），请参阅下面的“API钱包设置”部分。

### API钱包设置（推荐给代理使用）

API钱包可以代表主账户进行交易，但**不能取款**。这是自动化代理最安全的选择。

**操作流程：**
1. 运行`openbroker setup`并选择第3种模式（“生成API钱包”）
2. CLI会生成一对密钥，并打印出一个审批URL（例如：`https://openbroker.dev/approve?agent=0xABC...`）
3. 代理所有者需要在浏览器中打开该URL，并连接他们的主钱包（如MetaMask等）
4. 主钱包需要签署两笔交易：`ApproveAgent`（授权API钱包）和`ApproveBuilderFee`（批准1 bps的交易手续费）
5. CLI会自动检测到审批结果并保存配置

**设置完成后，配置文件中将包含以下内容：**
```
HYPERLIQUID_PRIVATE_KEY=0x...        # API wallet private key
HYPERLIQUID_ACCOUNT_ADDRESS=0x...    # Master account address
HYPERLIQUID_NETWORK=mainnet
```

**重要提示（针对代理）：** 使用API钱包时，需要将审批URL传递给代理所有者（即控制主钱包的人）。代理在开始交易前必须获得所有者的批准。CLI会等待最多10分钟以获取批准。如果超时，请重新运行`openbroker setup`。

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

### 所有市场（Perps + Spot + HIP-3）
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

### 现货市场
```bash
openbroker spot                   # Show all spot markets
openbroker spot --coin PURR       # Show PURR market info
openbroker spot --balances        # Show your spot balances
openbroker spot --top 20          # Top 20 by volume
```

### 交易成交
```bash
openbroker fills                          # Recent fills
openbroker fills --coin ETH               # ETH fills only
openbroker fills --coin BTC --side buy --top 50
```

### 订单历史
```bash
openbroker orders                         # Recent orders (all statuses)
openbroker orders --coin ETH --status filled
openbroker orders --top 50
```

### 订单状态
```bash
openbroker order-status --oid 123456789   # Check specific order
openbroker order-status --oid 0x1234...   # By client order ID
```

### 手续费安排
```bash
openbroker fees                           # Fee tier, rates, and volume
```

### K线数据（OHLCV）
```bash
openbroker candles --coin ETH                           # 24 hourly candles
openbroker candles --coin BTC --interval 4h --bars 48   # 48 four-hour bars
openbroker candles --coin SOL --interval 1d --bars 30   # 30 daily bars
```

### 资金流水记录
```bash
openbroker funding-history --coin ETH              # Last 24h
openbroker funding-history --coin BTC --hours 168  # Last 7 days
```

### 最近的交易记录
```bash
openbroker trades --coin ETH              # Last 30 trades
openbroker trades --coin BTC --top 50     # Last 50 trades
```

### 速率限制
```bash
openbroker rate-limit                     # API usage and capacity
```

## 交易命令

### 市场订单（快速模式）
```bash
openbroker buy --coin ETH --size 0.1
openbroker sell --coin BTC --size 0.01
openbroker buy --coin SOL --size 5 --slippage 100  # Custom slippage (bps)
```

### 市场订单（完整模式）
```bash
openbroker market --coin ETH --side buy --size 0.1
openbroker market --coin BTC --side sell --size 0.01 --slippage 100
```

### 限价订单
```bash
openbroker limit --coin ETH --side buy --size 1 --price 3000
openbroker limit --coin SOL --side sell --size 10 --price 200 --tif ALO
```

### 为现有持仓设置止盈/止损
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

## 高级执行策略

### 时间加权平均价格（TWAP）
```bash
# Execute 1 ETH buy over 1 hour (auto-calculates slices)
openbroker twap --coin ETH --side buy --size 1 --duration 3600

# Custom intervals with randomization
openbroker twap --coin BTC --side sell --size 0.5 --duration 1800 --intervals 6 --randomize 20
```

### 分批增减订单（网格订单）
```bash
# Place 5 buy orders ranging 2% below current price
openbroker scale --coin ETH --side buy --size 1 --levels 5 --range 2

# Scale out with exponential distribution
openbroker scale --coin BTC --side sell --size 0.5 --levels 4 --range 3 --distribution exponential --reduce
```

### 包括止盈和止损的订单
```bash
# Long ETH with 3% take profit and 1.5% stop loss
openbroker bracket --coin ETH --side buy --size 0.5 --tp 3 --sl 1.5

# Short with limit entry
openbroker bracket --coin BTC --side sell --size 0.1 --entry limit --price 100000 --tp 5 --sl 2
```

### 跟踪价格订单
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

### 定额投资（DCA）
```bash
# Buy $100 of ETH every hour for 24 hours
openbroker dca --coin ETH --amount 100 --interval 1h --count 24

# Invest $5000 in BTC over 30 days with daily purchases
openbroker dca --coin BTC --total 5000 --interval 1d --count 30
```

### 市场做市策略
```bash
# Market make ETH with 0.1 size, 10bps spread
openbroker mm-spread --coin ETH --size 0.1 --spread 10

# Tighter spread with position limit
openbroker mm-spread --coin BTC --size 0.01 --spread 5 --max-position 0.1
```

### 仅限做市商的订单类型（ALO）
```bash
# Market make using ALO (post-only) orders - guarantees maker rebates
openbroker mm-maker --coin HYPE --size 1 --offset 1

# Wider offset for volatile assets
openbroker mm-maker --coin ETH --size 0.1 --offset 2 --max-position 0.5
```

## 订单类型

### 限价订单与触发订单

**限价订单**（`openbroker limit`）：
- 一旦价格达到设定价格，立即执行
- 保留在订单簿中，直到成交或被取消
- 低于当前价格的限价卖单会立即成交（作为接受方）
- 不适合用于设置止损

**触发订单**（`openbroker trigger`, `openbroker tpsl`）：
- 在达到触发价格之前保持待定状态
- 仅在价格达到触发水平时才执行
- 是设置止损和获利了结的合适方式
- 不会提前成交

### 各种情况下的命令选择：

| 情况 | 命令 |
|----------|---------|
| 以低于市场价格的特定价格买入 | `openbroker limit` |
| 以高于市场价格的特定价格卖出 | `openbroker limit` |
| 设置止损（价格下跌时退出） | `openbroker trigger --type sl` |
| 设定止盈（达到目标价格时退出） | `openbroker trigger --type tp` |
| 为现有持仓添加止盈/止损 | `openbroker tpsl` |

## 常用参数

所有命令都支持`--dry`参数，用于预览操作（不执行实际交易）。

| 参数 | 说明 |
|----------|-------------|
| `--coin` | 资产符号（ETH、BTC、SOL等） |
| `--side` | 订单方向：`buy` 或 `sell` |
| `--size` | 订单数量（以基础资产计） |
| `--price` | 限价 |
| `--dry` | 预览操作（不执行） |
| `--help` | 显示命令帮助信息 |

### 订单参数

| 参数 | 说明 |
|----------|-------------|
| `--trigger` | 触发价格（针对触发订单） |
| `--type` | 触发类型：`tp` 或 `sl` |
| `--slippage` | 价格滑点（以bps为单位） |
| `--tif` | 执行时间：GTC、IOC、ALO |
| `--reduce` | 仅用于减少订单数量的命令 |

### 止盈/止损价格格式

| 格式 | 例子 | 说明 |
|--------|---------|-------------|
| 绝对值 | `--tp 40` | 价格设置为40美元 |
| 相对值上升 | `--tp +10%` | 价格设定为入场价的10%以上 |
| 相对值下降 | `--sl -5%` | 价格设定为入场价的5%以下 |
| 入场价格 | `--sl entry` | 设定为平仓止损 |

## 配置设置

配置文件的加载顺序如下（优先级从高到低）：
1. 环境变量
2. 当前目录下的`.env`文件
3. `~/.openbroker/.env`文件（全局配置）

运行`openbroker setup`可以交互式地创建全局配置。

| 参数 | 是否必填 | 说明 |
|----------|----------|-------------|
| `HYPERLIQUID_PRIVATE_KEY` | 是 | 钱包私钥（格式为0x...） |
| `HYPERLIQUID_NETWORK` | 否 | `mainnet`（默认）或`testnet` |
| `HYPERLIQUID_ACCOUNT_ADDRESS` | 否 | 主账户地址（API钱包所需） |

交易手续费（1 bps / 0.01%）是硬编码的，无法修改。

## OpenClaw插件（可选）

该工具可以通过Bash独立使用——上述所有命令都可以通过`openbroker` CLI执行。为了获得更多功能，`openbroker` npm包还提供了一个**OpenClaw插件**，您可以将其与该工具一起使用。

### 插件功能：
- **结构化的代理工具**（`ob_account`、`ob_buy`、`ob_limit`等）——这些工具使用结构化的数据格式进行调用，而非简单的Bash字符串；代理会收到结构化的JSON响应。
- **后台持仓监控**——每30秒检查一次您的Hyperliquid账户，并在持仓开仓/平仓、盈亏显著变化或保证金使用达到危险水平时发送Webhook警报。
- **CLI命令**——`openclaw ob status`和`openclaw ob watch`用于查看监控结果。

### 启用插件

插件包含在`openbroker` npm包中。要在OpenClaw配置中启用它，请执行以下操作：

```yaml
plugins:
  entries:
    openbroker:
      enabled: true
      config:
        hooksToken: "your-hooks-secret"   # Required for watcher alerts
        watcher:
          enabled: true
          pollIntervalMs: 30000
          pnlChangeThresholdPct: 5
          marginUsageWarningPct: 80
```

插件会从`~/.openbroker/.env`文件中读取钱包凭证（由`openbroker setup`设置），因此除非您需要覆盖配置，否则无需在插件配置中重复输入`privateKey`。

### 设置Webhook以接收警报

为了使代理能够收到持仓警报，请在您的网关配置中启用相应的Webhook：

```yaml
hooks:
  enabled: true
  token: "your-hooks-secret"   # Must match hooksToken above
```

即使未启用Webhook，监控功能仍然会运行并跟踪账户状态（可通过`ob_watcher_status`查看），但无法自动通知代理。

### 是否使用插件：

- **仅使用工具（不使用插件）**：直接使用Bash命令（例如：`openbroker buy --coin ETH --size 0.1`）。此时没有后台监控功能。
- **使用插件**：当`ob_*`工具可用时，代理会优先使用这些工具（因为它们提供结构化数据）；对于工具未覆盖的功能（如交易策略或批量操作），则使用Bash命令。后台监控功能会自动发送警报。

## 风险提示：

- 使用前请务必先使用`--dry`参数预览订单。
- 在测试网络（`HYPERLIQUID_NETWORK=testnet`）上从小额交易开始。
- 定期监控持仓情况和清算价格。
- 仅在使用`--reduce`参数时才执行平仓操作。