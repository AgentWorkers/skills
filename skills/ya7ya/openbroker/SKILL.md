---
name: openbroker
description: Hyperliquid交易插件具备后台持仓监控功能：可执行市价单、限价单，管理持仓情况，查看资金费率，并运行交易策略。该插件还提供自动警报功能，用于通知用户盈亏变化及清算风险。
license: MIT
compatibility: Requires Node.js 22+, network access to api.hyperliquid.xyz
homepage: https://www.npmjs.com/package/openbroker
metadata: {"author": "monemetrics", "version": "1.0.59", "openclaw": {"requires": {"bins": ["openbroker"], "env": ["HYPERLIQUID_PRIVATE_KEY"]}, "primaryEnv": "HYPERLIQUID_PRIVATE_KEY", "install": [{"id": "node", "kind": "node", "package": "openbroker", "bins": ["openbroker"], "label": "Install openbroker (npm)"}]}}
allowed-tools: ob_account ob_positions ob_funding ob_markets ob_search ob_spot ob_fills ob_orders ob_order_status ob_fees ob_candles ob_funding_history ob_trades ob_rate_limit ob_funding_scan ob_buy ob_sell ob_limit ob_trigger ob_tpsl ob_cancel ob_twap ob_bracket ob_chase ob_watcher_status Bash(openbroker:*)
---
# Open Broker - Hyperliquid Trading CLI

这是一个用于在Hyperliquid去中心化交易所（DEX）上执行交易操作的命令行工具，支持交易构建费用（builder fee）的自动支付。

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

## 重要提示：交易前请先查找资产

**在交易不熟悉的资产之前，请务必先进行搜索。** Hyperliquid支持主要的加密货币（如ETH、BTC、SOL等），以及HIP-3代币（如xyz:CL、xyz:GOLD、km:USOIL等），同时还提供现货市场。您可以使用搜索功能来查找正确的资产代码：

```bash
openbroker search --query GOLD              # Find all GOLD markets across all providers
openbroker search --query oil               # Find oil-related assets (CL, BRENTOIL, USOIL...)
openbroker search --query BTC --type perp   # BTC perps only
openbroker search --query NATGAS --type hip3  # HIP-3 only
```

或者使用`ob_search`插件工具：`{"query": "gold"}` 或 `{"query": "oil", "type": "hip3"}`

**HIP-3代币的代码格式为`dex:COIN`**，例如`xyz:CL`而非`CL`。如果遇到“未找到市场数据”的错误，请重新搜索以获取正确的代码。常见的HIP-3交易所包括`xyz`、`flx`、`km`、`hyna`、`vntl`、`cash`。

## 故障排除：使用CLI作为备用方案

如果`ob_*`插件工具出现意外错误、返回空结果或崩溃，**可以切换到相应的CLI命令**进行操作。CLI和插件工具使用相同的底层代码，但CLI具有更完善的错误处理和输出功能。

| 插件工具 | 对应的CLI命令 |
|-------------|---------------|
| `ob_account` | `openbroker account --json` |
| `ob_positions` | `openbroker positions --json` |
| `ob_funding` | `openbroker funding --json --include-hip3` |
| `ob_markets` | `openbroker markets --json --include-hip3` |
| `ob_search` | `openbroker search --query <QUERY>` |
| `ob_buy` | `openbroker buy --coin <COIN> --size <SIZE>` |
| `ob_sell` | `openbroker sell --coin <COIN> --size <SIZE>` |
| `ob_limit` | `openbroker limit --coin <COIN> --side <SIDE> --size <SIZE> --price <PRICE>` |
| `ob_tpsl` | `openbroker tpsl --coin <COIN> --tp <PRICE> --sl <PRICE>` |
| `ob_cancel` | `openbroker cancel --all` 或 `--coin <COIN>` |
| `ob_fills` | `openbroker fills --json` |
| `ob_orders` | `openbroker orders --json` |
| `ob_funding_scan` | `openbroker funding-scan --json` |
| `ob_candles` | `openbroker candles --coin <COIN> --json` |

**何时使用CLI作为备用方案：**
- 插件工具返回`null`、空数据或抛出错误时；
- 需要插件工具无法提供的数据时（例如`--verbose`调试输出）；
- 需要长时间运行的操作时（如策略交易、TWAP交易）——CLI能更好地处理超时和进度显示。

在所有交易CLI命令后添加`--dry`参数可进行预览操作（不执行实际交易）。在信息查询命令后添加`--json`参数可获取结构化输出。

## 命令参考

### 设置

```bash
openbroker setup              # One-command setup (wallet + config + builder approval)
openbroker approve-builder --check  # Check builder fee status (for troubleshooting)
```

`setup`命令提供三种模式：
1. **生成新的交易钱包**（推荐给代理）：创建一个专用的交易钱包，并自动批准交易构建费用。无需浏览器操作，只需用USDC充值即可开始交易。
2. **导入现有密钥**：使用您已有的私钥。
3. **生成API钱包**：创建一个只能用于交易的受限钱包，无法提取资金。需要通过主钱包在浏览器中进行授权。

对于第1和第2种模式，设置完成后会自动保存配置并批准交易构建费用。
关于第3种模式（API钱包），请参阅下面的API钱包设置部分。

### 新交易钱包设置（推荐给代理）

这是最适合代理的设置方式：生成新的交易钱包，自动批准交易构建费用，充值完成后即可立即开始交易。

**操作步骤：**
1. 运行`openbroker setup`并选择第1个选项（“生成新的交易钱包”）。
2. CLI会生成钱包，保存配置并自动批准交易构建费用。
3. 在Arbitrum平台上用USDC充值钱包，然后登录https://app.hyperliquid.xyz/进行交易。

### API钱包设置（另一种方式）

API钱包可以代表主账户进行交易，**但不能提取资金**。如果您希望将资金保留在现有钱包中，并仅授权交易权限，可以选择此方式。

**操作步骤：**
1. 运行`openbroker setup`并选择第3个选项（“生成API钱包”）。
2. CLI会生成一对密钥，并打印一个授权URL（例如`https://openbroker.dev/approve?agent=0xABC...`）。
3. 代理所有者需要在浏览器中打开该URL，并连接他们的主钱包（如MetaMask）。
4. 主钱包需要执行两个交易：`ApproveAgent`（授权API钱包）和`ApproveBuilderFee`（批准1bps的交易费用）。
5. CLI会自动检测到授权信息并保存配置。

**设置完成后，配置文件将包含以下内容：**
```
HYPERLIQUID_PRIVATE_KEY=0x...        # API wallet private key
HYPERLIQUID_ACCOUNT_ADDRESS=0x...    # Master account address
HYPERLIQUID_NETWORK=mainnet
```

**对代理的重要提示：** 使用API钱包时，需将授权URL告知代理所有者（控制主钱包的人）。代理在开始交易前必须获得授权。CLI会等待最多10分钟以获取授权。如果超时，请重新运行`openbroker setup`。

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

### 市场信息

```bash
openbroker markets --top 30   # Top 30 main perps
openbroker markets --coin BTC # Specific coin
```

### 所有市场（包括主流资产、现货市场和HIP-3代币）

```bash
openbroker all-markets                 # Show all markets
openbroker all-markets --type perp     # Main perps only
openbroker all-markets --type hip3     # HIP-3 perps only
openbroker all-markets --type spot     # Spot markets only
openbroker all-markets --top 20        # Top 20 by volume
```

### 市场搜索（跨交易所查找资产）

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

### 交易成交记录

```bash
openbroker fills                          # Recent fills
openbroker fills --coin ETH               # ETH fills only
openbroker fills --coin BTC --side buy --top 50
```

### 订单状态

```bash
openbroker orders                         # Recent orders (all statuses)
openbroker orders --coin ETH --status filled
openbroker orders --top 50
```

### 费用安排

```bash
openbroker fees                           # Fee tier, rates, and volume
```

### K线数据（OHLCV）

```bash
openbroker candles --coin ETH                           # 24 hourly candles
openbroker candles --coin BTC --interval 4h --bars 48   # 48 four-hour bars
openbroker candles --coin SOL --interval 1d --bars 30   # 30 daily bars
```

### 资金流动历史

```bash
openbroker funding-history --coin ETH              # Last 24h
openbroker funding-history --coin BTC --hours 168  # Last 7 days
```

### 最近的交易记录

```bash
openbroker trades --coin ETH              # Last 30 trades
openbroker trades --coin BTC --top 50     # Last 50 trades
```

### 价格限制

```bash
openbroker rate-limit                     # API usage and capacity
```

### 跨交易所资金费率扫描器

```bash
openbroker funding-scan                          # Scan all dexes, >25% threshold
openbroker funding-scan --threshold 50 --pairs   # Show opposing funding pairs
openbroker funding-scan --hip3-only --top 20     # HIP-3 only
openbroker funding-scan --watch --interval 120   # Re-scan every 2 minutes
```

## 交易命令

### HIP-3代币交易

所有交易命令都支持使用`dex:COIN`格式的HIP-3代币：

```bash
openbroker buy --coin xyz:CL --size 1              # Buy crude oil on xyz dex
openbroker sell --coin xyz:BRENTOIL --size 1        # Sell brent oil
openbroker limit --coin xyz:GOLD --side buy --size 0.1 --price 2500
openbroker funding-arb --coin xyz:CL --size 5000    # Funding arb on HIP-3
```

### 市场订单（快速操作）

```bash
openbroker buy --coin ETH --size 0.1
openbroker sell --coin BTC --size 0.01
openbroker buy --coin SOL --size 5 --slippage 100  # Custom slippage (bps)
```

### 市场订单（详细信息）

```bash
openbroker market --coin ETH --side buy --size 0.1
openbroker market --coin BTC --side sell --size 0.01 --slippage 100
```

### 限价订单

```bash
openbroker limit --coin ETH --side buy --size 1 --price 3000
openbroker limit --coin SOL --side sell --size 10 --price 200 --tif ALO
```

### 为现有订单设置止盈/止损

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

### 触发式订单（独立的止盈/止损）

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

### TWAP（时间加权平均价格）

```bash
# Execute 1 ETH buy over 1 hour (auto-calculates slices)
openbroker twap --coin ETH --side buy --size 1 --duration 3600

# Custom intervals with randomization
openbroker twap --coin BTC --side sell --size 0.5 --duration 1800 --intervals 6 --randomize 20
```

### 分阶段增减订单（网格订单）

```bash
# Place 5 buy orders ranging 2% below current price
openbroker scale --coin ETH --side buy --size 1 --levels 5 --range 2

# Scale out with exponential distribution
openbroker scale --coin BTC --side sell --size 0.5 --levels 4 --range 3 --distribution exponential --reduce
```

### 包括止盈/止损的订单

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

### 定投（DCA）

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

### 仅限做市商的订单类型

```bash
# Market make using ALO (post-only) orders - guarantees maker rebates
openbroker mm-maker --coin HYPE --size 1 --offset 1

# Wider offset for volatile assets
openbroker mm-maker --coin ETH --size 0.1 --offset 2 --max-position 0.5
```

## 订单类型

### 限价订单与触发式订单

**限价订单（`openbroker limit`）：**
- 一旦价格达到设定价格，立即执行。
- 保留在订单簿中，直到成交或被取消。
- 低于当前价格的限价卖单会立即成交（作为接单方）。
- 不适合用于设置止损。

**触发式订单（`openbroker trigger`、`openbroker tpsl`）：**
- 在达到触发价格前保持待定状态。
- 仅在价格达到触发价格时才执行。
- 是设置止损和获利的好方法。
- 不会提前成交。

### 各种情况的命令选择

| 操作场景 | 使用的命令 |
|----------|---------|
| 以低于市场价格的特定价格买入 | `openbroker limit` |
| 以高于市场价格的特定价格卖出 | `openbroker limit` |
| 设置止损（价格下跌时退出） | `openbroker trigger --type sl` |
| 设定获利目标（价格达到目标时退出） | `openbroker trigger --type tp` |
| 为现有订单添加止盈/止损 | `openbroker tpsl` |

## 常用参数

所有命令都支持`--dry`参数，用于预览操作（不执行实际交易）。

| 参数 | 说明 |
|----------|-------------|
| `--coin` | 资产代码（如ETH、BTC、SOL等） |
| `--side` | 订单方向：买入或卖出 |
| `--size` | 订单数量（以基础资产计） |
| `--price` | 限价 |
| `--dry` | 预览操作（不执行） |
| `--help` | 显示命令帮助信息 |

### 订单相关参数

| 参数 | 说明 |
|----------|-------------|
| `--trigger` | 触发价格（针对触发式订单） |
| `--type` | 触发类型：止盈（tp）或止损（sl） |
| `--slippage` | 止损幅度（以基点计） |
| `--tif` | 订单生效时间：GTC（立即执行）、IOC（成交时执行）、ALO（自动取消） |
| `--reduce` | 仅用于减少订单数量 |

### 止盈/止损价格格式

| 格式 | 例子 | 说明 |
|--------|---------|-------------|
| 绝对值 | `--tp 40` | 价格设置为40美元 |
| 相对值（上涨） | `--tp +10%` | 价格设定为入场价的10%以上 |
| 相对值（下跌） | `--sl -5%` | 价格设定为入场价的5%以下 |
| 入场价格 | `--sl entry` | 设定为入场价作为止损 |

## 配置设置

配置文件的加载顺序如下（优先级从高到低）：
1. 环境变量
2. 当前目录下的`.env`文件
3. `~/.openbroker/.env`文件（全局配置）

运行`openbroker setup`可以交互式地配置全局设置。

| 参数 | 是否必需 | 说明 |
|----------|----------|-------------|
| `HYPERLIQUID_PRIVATE_KEY` | 是 | 钱包私钥（格式为0x...） |
| `HYPERLIQUID_NETWORK` | 否 | 默认为`mainnet`，或可选`testnet` |
| `HYPERLIQUID_ACCOUNT_ADDRESS` | 否 | 主账户地址（API钱包所需） |

交易构建费用（1bps/0.01%）是硬编码的，不可更改。

## OpenClaw插件（可选）

该工具也可以通过Bash独立使用——上述所有命令都可以通过`openbroker` CLI执行。为了获得更多功能，`openbroker` npm包还提供了一个**OpenClaw插件**，您可以将其与本工具一起使用。

### 插件附加的功能：

- **结构化的代理工具**（`ob_account`、`ob_buy`、`ob_limit`等）：使用结构化的输入格式进行命令调用，而非简单的Bash字符串。代理会收到结构化的JSON响应。
- **后台订单监控**：每30秒检查一次您的Hyperliquid账户，并在订单开立/关闭、盈亏显著变化或保证金使用率达到危险水平时发送Webhook警报。
- **CLI命令**：`openclaw ob status`和`openclaw ob watch`用于查看监控结果。

### 启用插件

插件包含在`openbroker` npm包中。要在OpenClaw配置中启用插件，请执行以下操作：

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

插件会从`~/.openbroker/.env`文件中读取钱包凭据（由`openbroker setup`设置），因此除非您需要覆盖设置，否则无需在插件配置中重复输入`privateKey`。

### 设置Webhook以接收警报

为了使代理能够收到订单状态警报，请在您的网关配置中启用相应的Webhook：

```yaml
hooks:
  enabled: true
  token: "your-hooks-secret"   # Must match hooksToken above
```

即使未启用Webhook，插件也会继续运行并监控账户状态（可通过`ob_watcher_status`查看），但无法主动通知代理。

### 是否使用插件

- **仅使用命令行工具**：直接使用Bash命令（例如`openbroker buy --coin ETH --size 0.1`），不启用后台监控。
- **结合插件使用**：当`ob_*`工具可用时，建议使用它们（因为它们提供结构化数据）；对于不支持的功能（如策略交易、分阶段增减订单），可以使用Bash命令。后台监控功能会自动发送警报。

## 风险提示

- 在实际交易前，请务必先使用`--dry`参数进行预览。
- 在测试网（`HYPERLIQUID_NETWORK=testnet`）上使用小金额进行测试。
- 定期检查订单状态和清算价格。
- 仅在使用`--reduce`参数时才执行平仓操作。