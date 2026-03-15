---
name: openbroker
description: Hyperliquid交易插件具备后台持仓监控功能以及自定义自动化功能。该插件可执行市场订单和限价订单，管理持仓情况，查看资金费率，运行交易策略，并编写基于事件的自动化脚本；同时会自动提醒用户盈亏变化及清算风险。
license: MIT
compatibility: Requires Node.js 22+, network access to api.hyperliquid.xyz
homepage: https://www.npmjs.com/package/openbroker
metadata: {"author": "monemetrics", "version": "1.0.65", "openclaw": {"requires": {"bins": ["openbroker"], "env": ["HYPERLIQUID_PRIVATE_KEY"]}, "primaryEnv": "HYPERLIQUID_PRIVATE_KEY", "install": [{"id": "node", "kind": "node", "package": "openbroker", "bins": ["openbroker"], "label": "Install openbroker (npm)"}]}}
allowed-tools: ob_account ob_positions ob_funding ob_markets ob_search ob_spot ob_fills ob_orders ob_order_status ob_fees ob_candles ob_funding_history ob_trades ob_rate_limit ob_funding_scan ob_buy ob_sell ob_limit ob_trigger ob_tpsl ob_cancel ob_twap ob_bracket ob_chase ob_watcher_status ob_auto_run ob_auto_stop ob_auto_list Bash(openbroker:*)
---
# Open Broker - Hyperliquid Trading CLI

这是一个用于在Hyperliquid去中心化交易所（DEX）上执行交易操作的命令行界面（CLI）工具，支持交易构建费用（builder fee）的收取。

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

**在交易不熟悉的资产之前，请务必先进行搜索。** Hyperliquid支持主要的加密货币（如ETH、BTC、SOL等），HIP-3代币（如xyz:CL、xyz:GOLD、km:USOIL等），以及现货市场。使用搜索功能来查找正确的资产代码：

```bash
openbroker search --query GOLD              # Find all GOLD markets across all providers
openbroker search --query oil               # Find oil-related assets (CL, BRENTOIL, USOIL...)
openbroker search --query BTC --type perp   # BTC perps only
openbroker search --query NATGAS --type hip3  # HIP-3 only
```

或者使用`ob_search`插件工具：`{"query": "gold"}` 或 `{"query": "oil", "type": "hip3"}`

**HIP-3代币使用`dex:COIN`格式**——例如，应输入`xyz:CL`而不是`CL`。如果出现“未找到市场数据”的错误，请重新搜索以获取正确的代码。常见的HIP-3交易所包括`xyz`、`flx`、`km`、`hyna`、`vntl`、`cash`。

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
| `ob_auto_run` | `openbroker auto run <script> --dry` |
| `ob_auto_stop` | （通过SIGINT信号停止自动化） |

**何时使用CLI作为备用方案：**
- 插件工具返回`null`、空数据或错误
- 需要插件工具无法提供的数据（例如`--verbose`调试输出）
- 需要长时间运行的操作（如策略交易、TWAP交易）——CLI能更好地处理超时和进度更新

在任何交易CLI命令后添加`--dry`参数即可预览操作而无需实际执行。对于信息查询命令，添加`--json`参数可获取结构化输出。

## 命令参考

### 设置

```bash
openbroker setup              # One-command setup (wallet + config + builder approval)
openbroker approve-builder --check  # Check builder fee status (for troubleshooting)
```

`setup`命令提供三种模式：
1. **生成新钱包**（推荐给代理）——创建一个专用的交易钱包，并自动批准交易构建费用。无需浏览器操作，只需用USDC充值即可开始交易。
2. **导入现有密钥**——使用你已有的私钥。
3. **生成API钱包**——创建一个只能用于交易但不能提款的受限钱包。需要通过主钱包在浏览器中批准。

对于第1和第2种模式，设置完成后会自动保存配置并批准交易构建费用。
关于第3种模式（API钱包），请参阅下面的API钱包设置部分。

### 新钱包设置（推荐给代理）

这是最适合代理的设置方式。系统会生成一个新钱包，自动批准交易构建费用，充值完成后代理即可立即开始交易。

**操作步骤：**
1. 运行`openbroker setup`并选择选项1（“生成新钱包”）。
2. CLI会生成钱包，保存配置并自动批准交易构建费用。
3. 用USDC在Arbitrum平台上充值钱包，然后登录https://app.hyperliquid.xyz/进行交易。

### API钱包设置（备用方案）

API钱包可以代表主账户进行交易，**但不能提款**。如果你希望将资金保留在现有钱包中，并仅委托交易权限，可以选择此方式。

**操作步骤：**
1. 运行`openbroker setup`并选择选项3（“生成API钱包”）。
2. CLI会生成一对密钥，并提供一个批准链接（例如`https://openbroker.dev/approve?agent=0xABC...`）。
3. 代理所有者需要在浏览器中打开该链接，并连接他们的主钱包（如MetaMask）。
4. 主钱包需要执行两个交易：`ApproveAgent`（授权API钱包）和`ApproveBuilderFee`（批准1 bps的费用）。
5. CLI会自动检测到批准结果并保存配置。

**设置完成后，配置文件将包含以下内容：**
```
HYPERLIQUID_PRIVATE_KEY=0x...        # API wallet private key
HYPERLIQUID_ACCOUNT_ADDRESS=0x...    # Master account address
HYPERLIQUID_NETWORK=mainnet
```

**重要提示（针对代理）：**使用API钱包时，需将批准链接告知代理所有者（控制主钱包的人）。代理在开始交易前必须获得批准。CLI最多会等待10分钟。如果超时，请重新运行`openbroker setup`。

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

### 所有市场（包括主流资产、现货市场和HIP-3资产）

```bash
openbroker all-markets                 # Show all markets
openbroker all-markets --type perp     # Main perps only
openbroker all-markets --type hip3     # HIP-3 perps only
openbroker all-markets --type spot     # Spot markets only
openbroker all-markets --top 20        # Top 20 by volume
```

### 搜索市场（跨交易所查找资产）

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

### 订单状态

```bash
openbroker order-status --oid 123456789   # Check specific order
openbroker order-status --oid 0x1234...   # By client order ID
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

### 资金使用历史

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

### 资金费率扫描（跨交易所）

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

### 市场订单（详细操作）

```bash
openbroker market --coin ETH --side buy --size 0.1
openbroker market --coin BTC --side sell --size 0.01 --slippage 100
```

### 限价单

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

### 分批增减订单（网格交易）

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

### 仅限做市商的订单类型

```bash
# Market make using ALO (post-only) orders - guarantees maker rebates
openbroker mm-maker --coin HYPE --size 1 --offset 1

# Wider offset for volatile assets
openbroker mm-maker --coin ETH --size 0.1 --offset 2 --max-position 0.5
```

## 订单类型

### 限价单与触发式订单

**限价单**（`openbroker limit`）：
- 一旦价格达到设定值立即执行。
- 保留在订单簿中，直到成交或被取消。
- 限价卖单在当前价格以下时立即成交（作为接受方）。
- 不适合用于设置止损。

**触发式订单**（`openbroker trigger`、`openbroker tpsl`）：
- 保持静止状态，直到达到触发价格。
- 仅在价格达到触发水平时激活。
- 是设置止损和获利的好方法。
- 不会提前成交。

**何时使用每种订单类型：**

| 使用场景 | 命令 |
|----------|---------|
| 以低于市场的价格买入 | `openbroker limit` |
| 以高于市场的价格卖出 | `openbroker limit` |
| 设置止损（价格下跌时退出） | `openbroker trigger --type sl` |
| 设定获利（价格达到目标时退出） | `openbroker trigger --type tp` |
| 为现有订单添加止盈/止损 | `openbroker tpsl` |

## 常用参数

所有命令都支持`--dry`参数，用于预览操作而无需执行。

| 参数 | 说明 |
|----------|-------------|
| `--coin` | 资产代码（如ETH、BTC、SOL等） |
| `--side` | 订单方向：`buy`或`sell` |
| `--size` | 订单数量（以基础资产计） |
| `--price` | 限价 |
| `--dry` | 预览操作 |
| `--help` | 显示命令帮助信息 |

### 订单参数

| 参数 | 说明 |
|----------|-------------|
| `--trigger` | 触发价格 |
| `--type` | 触发类型：`tp`或`sl` |
| `--slippage` | 止损/止盈幅度（以基点计） |
| `--tif` | 执行时间：GTC、IOC、ALO |
| `--reduce` | 仅减少订单数量 |

### 止盈/止损价格格式

| 格式 | 例子 | 说明 |
|--------|---------|-------------|
| 绝对值 | `--tp 40` | 价格设置为40美元 |
| 相对值（上涨） | `--tp +10%` | 价格设置为当前价格的10%以上 |
| 相对值（下跌） | `--sl -5%` | 价格设置为当前价格的95%以下 |
| 进价 | `--sl entry` | 设置止损为进价 |

## 配置设置

配置文件从以下来源加载（按优先级顺序）：
1. 环境变量
2. 当前目录下的`.env`文件
3. `~/.openbroker/.env`文件（全局配置）

运行`openbroker setup`可以交互式地创建全局配置。

| 参数 | 是否必需 | 说明 |
|----------|----------|-------------|
| `HYPERLIQUID_PRIVATE_KEY` | 是 | 钱包私钥（格式为0x...） |
| `HYPERLIQUID_NETWORK` | 否 | 默认为`mainnet`或`testnet` |
| `HYPERLIQUID_ACCOUNT_ADDRESS` | 否 | 主账户地址（API钱包所需） |

交易构建费用（1 bps / 0.01%）是硬编码的，无法更改。

## OpenClaw插件（可选）

该工具可以通过Bash独立使用——上述所有命令都可以通过`openbroker` CLI执行。为了获得更多功能，`openbroker` npm包还提供了一个**OpenClaw插件**，你可以将其与本技能一起使用。

### 插件新增功能：

- **结构化的代理工具**（`ob_account`、`ob_buy`、`ob_limit`等）——使用结构化的输入格式进行调用，而非Bash字符串。代理会收到结构化的JSON响应。
- **后台订单监控**——每30秒检查一次你的Hyperliquid账户，并在订单开立/关闭、盈亏显著变化或保证金使用达到危险水平时发送Webhook警报。
- **自动化工具**（`ob_auto_run`、`ob_auto_stop`、`ob_auto_list`）——允许在代理端启动、停止和管理自定义交易自动化脚本。
- **CLI命令**（`openclaw ob status`和`openclaw ob watch`）——用于查看订单监控状态。

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

插件会从`~/.openbroker/.env`文件中读取钱包凭据（由`openbroker setup`设置），因此除非需要覆盖，否则无需在插件配置中重复输入`privateKey`。

### 设置Webhook以接收警报

为了使代理能够收到订单监控警报，需要在你的网关配置中启用相应的钩子：

```yaml
hooks:
  enabled: true
  token: "your-hooks-secret"   # Must match hooksToken above
```

即使没有启用钩子，插件也会继续运行并监控账户状态（可通过`ob_watcher_status`访问），但无法主动触发代理操作。

### 是否使用插件

- **仅使用CLI**：可以直接使用Bash命令（例如`openbroker buy --coin ETH --size 0.1`）。此时没有后台监控功能。
- **结合使用CLI和插件**：当插件可用时，建议使用`ob_*`工具（因为它们提供结构化数据）；对于不支持的命令（如策略交易、分批增减订单），可以使用Bash。插件会自动发送警报。

## 交易自动化

自动化脚本允许你使用TypeScript编写自定义的交易逻辑。你可以编写所需的逻辑，OpenBroker会负责轮询、事件检测和SDK访问。

### 自动化的实现方式

自动化脚本是一个`.ts`文件，其中包含一个默认函数。该函数会接收`AutomationAPI`对象，该对象提供了完整的Hyperliquid客户端接口、事件订阅功能、持久化状态和日志记录功能。运行时系统会每10秒检查一次Hyperliquid服务器，并在检测到变化时触发相应的事件。

### 编写自动化脚本

在`~/.openbroker/automations/`目录下创建一个`.ts`文件：

```typescript
// ~/.openbroker/automations/funding-scalp.ts
export default function(api) {
  const COIN = 'ETH';

  api.on('funding_update', async ({ coin, annualized }) => {
    if (coin !== COIN) return;

    if (annualized > 0.5 && !api.state.get('isShort')) {
      api.log.info('High positive funding — going short');
      await api.client.marketOrder(COIN, false, 0.1);
      api.state.set('isShort', true);
    } else if (annualized < -0.1 && api.state.get('isShort')) {
      api.log.info('Funding normalized — closing short');
      await api.client.marketOrder(COIN, true, 0.1);
      api.state.set('isShort', false);
    }
  });

  api.onStop(async () => {
    if (api.state.get('isShort')) {
      api.log.warn('Closing short on shutdown');
      await api.client.marketOrder('ETH', true, 0.1);
      api.state.set('isShort', false);
    }
  });
}
```

### AutomationAPI接口

| 属性/方法 | 说明 |
|-------------------|-------------|
| `api.client` | 完整的Hyperliquid客户端接口，提供`marketOrder()`、`limitOrder()`、`triggerOrder()`、`cancelAll()`、`getUserStateAll()`、`getAllMids()`、`updateLeverage()`等方法 |
| `api.on(event, handler)` | 订阅市场/账户事件 |
| `api.every(ms, handler)` | 按指定间隔（与轮询周期对齐）执行处理函数 |
| `api.onStart(handler)` | 在所有处理函数注册完成后调用，但在首次轮询之前 |
| `api.onStop(handler)` | 在系统关闭时调用（通过SIGINT信号），用于清理操作（如关闭订单） |
| `api.onError(handler)` | 当处理函数抛出错误时调用，用于错误处理 |
| `api.state.get(key)` | 获取持久化状态值 |
| `api.state.set(key, value)` | 设置持久化状态值 |
| `api.state.delete(key)` | 删除持久化状态值 |
| `api.state.clear()` | 清除所有状态值 |
| `api.publish(message, options?)` | 通过Webhook向OpenClaw代理发送消息。代理收到消息后可以采取相应操作（如通知用户）。返回`true`表示消息已成功发送。参数包括`{ name?, wakeMode?, deliver?, channel? }` |
| `api.log.info/warn/error/debug(msg)` | 提供结构化的日志记录功能 |
| `api.utils` | 提供辅助函数，如`roundPrice`、`roundSize`、`sleep`、`normalizeCoin`、`formatUsd`、`annualizeFundingRate` |
| `api.id` | 自动化脚本的ID（文件名或`--id`参数） |
| `api.dryRun` | 如果使用`--dry`参数运行，则此参数为`true`（此时脚本执行会被拦截） |

### 事件类型

| 事件 | 事件内容 | 触发条件 |
|-------|---------|------|
| `tick` | `{ timestamp, pollCount }` | 每次轮询周期触发（默认间隔为10秒） |
| `price_change` | `{ coin, oldPrice, newPrice, changePct }` | 当价格变化超过0.01%时触发 |
| `funding_update` | `{ coin, fundingRate, annualized, premium }` | 每次轮询时更新所有资产的资金费率数据 |
| `position_opened` | `{ coin, side, size, entryPrice }` | 新订单创建时触发 |
| `position_closed` | `{ coin, previousSize, entryPrice }` | 旧订单关闭时触发 |
| `position_changed` | `{ coin, oldSize, newSize, entryPrice }` | 订单大小发生变化时触发 |
| `pnl_threshold` | `{ coin, unrealizedPnl, changePct, positionValue }` | 盈亏变化超过订单价值的5%时触发 |

### 事件说明

#### `tick` — 每次轮询都会触发

无论市场状况如何，`tick`事件都会被触发。适用于需要定期检查的情况（例如检查价格是否超过某个绝对阈值）。这是最可靠的事件类型。

**事件内容：`{ timestamp: number, pollCount: number }`

**使用场景：**
- 检查价格是否超过/低于某个绝对阈值（例如“当ETH价格低于3000美元时触发警报”）
- 需要根据自定义条件进行判断的情况（例如“如果我没有持仓且资金充足，则触发操作”）
- 需要定期执行的任务（尽管`api.every()`更适合更长的间隔）

**示例：**价格绝对阈值警报

#### `price_change` — 相对价格变化

当某种货币的中间价格相对于上一次轮询发生了≥0.01%的变化时触发。这个事件可以过滤掉价格波动带来的干扰，仅捕捉实际的价格变化。

**使用场景：**
- 对价格变动做出反应（例如检测价格突破或趋势变化）
- 监控特定货币的波动性
- 编写基于价格变化的入场/出场逻辑

**注意：**`price_change`事件不会包含价格数据——你需要通过`api.client.getAllMids()`自行获取价格信息。这是因为`tick`事件会在其他事件处理之前触发。

#### `funding_update` — 资金费率更新

每次轮询时，如果某个资产的资金费率发生变化，就会触发此事件。由于涉及大量资产，因此事件触发频率较高（例如如果有150种代币，每次轮询会触发150次）。

**事件内容：`{ coin: string, fundingRate: number, annualized: number, premium: number }`
- `fundingRate`：原始的每小时资金费率
- `annualized`：年化资金费率
- `premium`：附加费用

**使用场景：**
- 资金费率套利策略
- 监控极端资金费率情况（用于判断入场/出场时机）
- 扫描所有资产的最高/最低资金费率

#### `position_opened` — 新订单创建

当系统中出现新的订单时触发此事件。适用于自动设置新订单的止盈/止损或记录新订单的创建。

**使用场景：**
- 自动为新订单设置止盈/止损
- 在新订单创建时记录日志或发出警报
- 开始针对新订单的监控

#### `position_closed` — 旧订单关闭

当之前存在但在当前轮询中已关闭的订单被删除时触发此事件。这适用于记录订单关闭的情况。

**使用场景：**
- 在订单关闭时记录日志或发出警报
- 在订单关闭后清理相关操作
- 在订单关闭后更新相关状态

#### `position_changed` — 订单大小或方向变化

当现有订单的大小或方向发生变化时触发此事件。例如，用于调整新订单的止盈/止损或记录订单的变动情况。

**使用场景：**
- 在订单部分关闭或方向改变时更新止盈/止损
- 调整新订单的止盈/止损
- 在订单部分关闭或完全关闭时使用`position_opened`和`position_closed`事件

#### `pnl_threshold` — 盈亏显著变化

当未实现的盈亏（unrealized PnL）变化超过订单价值的5%时触发此事件。此事件用于触发风险警报。

**使用场景：**
- 在盈亏发生显著变化时触发警报
- 自动减少风险（例如在盈亏超过5%时关闭部分订单）
- 通过`api.publish()`向用户发送警报

#### 选择合适的事件类型

| 使用场景 | 最适合的事件 | 说明 |
|----------|-----------|-----|
| 当价格达到固定阈值时触发警报 | `tick` | 每次轮询都会触发 |
| 对价格波动做出反应 | `price_change` | 提供两次轮询之间的相对价格变化 |
| 资金费率策略 | `funding_update` | 直接提供年化费率 |
| 为新订单自动设置止盈/止损 | `position_opened` | 在新订单创建时触发 |
| 记录订单关闭情况 | `position_closed` | 在订单关闭时触发 |
| 跟踪订单规模变化 | `position_changed` | 仅在订单规模发生变化时触发 |
| 风险管理 | `pnl_threshold` | 在盈亏变化超过5%时触发警报 |

### 可用的客户端方法

`api.client`对象提供了完整的Hyperliquid SDK接口：

**交易相关方法：**`marketOrder(coin, isBuy, size)`、`limitOrder(coin, isBuy, size, price)`、`triggerOrder(coin, isBuy, size, triggerPx, isMarket)`、`takeProfit(coin, isBuy, size, triggerPx)`、`stopLoss(coin, isBuy, size, triggerPx)`、`cancel(coin, oid)`、`cancelAll(coin?)`

**市场数据相关方法：**`getAllMids()`、`getMetaAndAssetCtxs()`、`getRecentTrades(coin)`、`getCandleSnapshot(coin, interval)`、`getFundingHistory(coin)`、`getPredictedFundings()`

**账户相关方法：`getUserStateAll()`、`getOpenOrders()`、`getUserFills()`、`getUserFunding()`、`getHistoricalOrders()`、`getUserFees()`、`getUserRateLimit()`、`getSpotBalances()`、`getLeverage(coin, leverage, isIsolated?)`

### 示例：价格突破

```typescript
// ~/.openbroker/automations/breakout.ts
export default function(api) {
  const COIN = 'ETH';
  const BREAKOUT_PCT = 2;  // 2% move triggers entry
  const SIZE = 0.5;
  let basePrice = null;

  api.onStart(async () => {
    const mids = await api.client.getAllMids();
    basePrice = parseFloat(mids[COIN]);
    api.log.info(`Watching ${COIN} from $${basePrice} for ${BREAKOUT_PCT}% breakout`);
  });

  api.on('price_change', async ({ coin, newPrice }) => {
    if (coin !== COIN || !basePrice) return;
    const totalChange = ((newPrice - basePrice) / basePrice) * 100;

    if (Math.abs(totalChange) >= BREAKOUT_PCT && !api.state.get('inPosition')) {
      const side = totalChange > 0;  // true = long, false = short
      api.log.info(`Breakout! ${totalChange.toFixed(2)}% — entering ${side ? 'long' : 'short'}`);
      await api.client.marketOrder(COIN, side, SIZE);
      api.state.set('inPosition', true);
    }
  });
}
```

### 示例：定期定额投资（DCA）

```typescript
// ~/.openbroker/automations/hourly-dca.ts
export default function(api) {
  const COIN = 'ETH';
  const USD_PER_BUY = 100;

  // Buy $100 of ETH every hour
  api.every(60 * 60 * 1000, async () => {
    const mids = await api.client.getAllMids();
    const price = parseFloat(mids[COIN]);
    const size = parseFloat(api.utils.roundSize(USD_PER_BUY / price, 4));
    await api.client.marketOrder(COIN, true, size);
    const count = (api.state.get('buyCount') || 0) + 1;
    api.state.set('buyCount', count);
    api.log.info(`DCA #${count}: bought ${size} ${COIN} at $${price}`);
  });
}
```

### 示例：保证金监控

```typescript
// ~/.openbroker/automations/margin-guard.ts
export default function(api) {
  api.on('margin_warning', async ({ marginUsedPct, equity }) => {
    api.log.warn(`Margin at ${marginUsedPct.toFixed(1)}% — reducing positions`);

    // Close the smallest position to free margin
    const state = await api.client.getUserStateAll();
    const positions = state.assetPositions
      .filter(p => parseFloat(p.position.szi) !== 0)
      .sort((a, b) => Math.abs(parseFloat(a.position.positionValue)) - Math.abs(parseFloat(b.position.positionValue)));

    if (positions.length > 0) {
      const pos = positions[0].position;
      const size = Math.abs(parseFloat(pos.szi));
      const isBuy = parseFloat(pos.szi) < 0; // Close short = buy, close long = sell
      api.log.info(`Closing smallest position: ${pos.coin} (${pos.szi})`);
      await api.client.marketOrder(pos.coin, isBuy, size);
    }
  });
}
```

### 向代理发送消息（使用Webhook）

使用`api.publish()`向OpenClaw代理发送消息。代理收到消息后可以采取相应操作（如通知用户、执行交易等）。

**注意：**`api.publish()`在消息成功发送时返回`true`，否则表示Webhook未配置（未设置钩子）。使用此方法需要设置`OPENCLAW_HOOKS_TOKEN`（在作为OpenClaw插件运行时会自动配置）。

**示例：**使用`api.publish()`发送价格警报

```typescript
// ~/.openbroker/automations/price-alert.ts
export default function(api) {
  const COIN = 'ETH';
  const THRESHOLD = 4000;

  api.on('price_change', async ({ coin, newPrice, changePct }) => {
    if (coin !== COIN) return;

    const crossed = api.state.get<boolean>('crossed', false);
    if (!crossed && newPrice >= THRESHOLD) {
      api.state.set('crossed', true);
      await api.publish(
        `${COIN} crossed above $${THRESHOLD}! Price: $${newPrice.toFixed(2)} (+${changePct.toFixed(2)}%)`,
      );
    } else if (crossed && newPrice < THRESHOLD) {
      api.state.set('crossed', false);
    }
  });
}
```

### 运行自动化脚本

**通过CLI：**
```bash
openbroker auto run my-strategy --dry       # Test without trading
openbroker auto run ./funding-scalp.ts      # Run from path
openbroker auto run my-strategy --poll 5000 # Poll every 5s
openbroker auto list                        # Show available scripts
openbroker auto status                      # Show running automations
```

**通过OpenClaw插件运行自动化脚本：**
- `ob_auto_run`：`{"script": "funding-scalp", "dry": true}` — 启动自动化脚本
- `ob_auto_stop`：`{"id": "funding-scalp"}` — 停止正在运行的自动化脚本
- `ob_auto_list`：`{"}` — 列出所有可用和正在运行的自动化脚本

**参数说明：**
| 参数 | 说明 | 默认值 |
|------|-------------|---------|
| `--dry` | 是否拦截执行操作 | `false` |
| `--verbose` | 是否显示调试信息 | `false` |
| `--id <name>` | 自定义自动化脚本的ID | 脚本文件名 |
| `--poll <ms>` | 轮询间隔（以毫秒为单位） | `10000` |

**给代理编写自动化脚本时的注意事项：**
- 在实际交易前务必先用`--dry`参数进行预览测试。
- 使用`api.state`来跟踪订单状态（在系统重启后也能保持数据）。
- 使用`api.onStop()`来清理操作（如关闭订单）。
- 使用`api.publish()`向OpenClaw代理发送警报或事件信息——不要手动构建Webhook请求。
- 运行时系统会捕获每个处理函数的错误——即使某个函数失败，其他函数仍会继续执行。
- 脚本文件位于`~/.openbroker/automations/`目录下。
- 所有交易命令都支持HIP-3代币（例如`api.client.marketOrder('xyz:CL', true, 1)`）。
- 自动化脚本在网关重启后仍会继续运行。

## 风险提示

- 在实际交易前务必先使用`--dry`参数进行预览。
- 在测试环境中（`HYPERLIQUID_NETWORK=testnet`）使用较小的交易金额进行测试。
- 监控订单状态和保证金使用情况。
- 使用`--reduce`参数仅用于关闭订单。