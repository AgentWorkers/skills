---
name: hyperclaw
description: 在Hyperliquid平台上进行交易。支持超过228种金融衍生品，包括HIP-3标准的股票/商品衍生品（如TSLA、GOLD）；具备市场扫描、情绪分析、Grok网络搜索以及预测市场数据等功能。提供用于查询账户状态、市场数据、资金费率、订单簿、交易操作以及收集市场情报的命令。
user-invocable: true
metadata:
  openclaw:
    requires:
      env:
        - HL_ACCOUNT_ADDRESS
        - HL_SECRET_KEY
---
# HyperClaw - Hyperliquid 交易技能

通过 CLI 在 Hyperliquid 上进行交易。支持原生加密货币（如 BTC、ETH、SOL 等）、HIP-3 构建和部署的衍生品（如股票、商品、外汇）、市场扫描以及智能分析工具。

## 设置

运行一次设置脚本以创建虚拟环境并安装依赖项：

```bash
bash {baseDir}/scripts/setup.sh
```

然后在技能根目录中配置 `.env` 文件，填写您的 Hyperliquid API 凭据：

```
HL_ACCOUNT_ADDRESS=0x_your_wallet_address
HL_SECRET_KEY=0x_your_api_wallet_private_key
HL_TESTNET=false
```

API 密钥获取地址：https://app.hyperliquid.xyz/API — 请使用专用的 API 钱包，而非您的主钱包私钥。

对于智能分析命令（如情绪分析、解锁资产、开发者检查、查询信息、搜索等）是可选的：
```
XAI_API_KEY=xai-...
```

配置完 `.env` 后，启动缓存代理（以避免 API 被限制）：

```bash
{baseDir}/scripts/.venv/bin/python {baseDir}/scripts/server.py &
```

## 如何运行命令

```bash
{baseDir}/scripts/.venv/bin/python {baseDir}/scripts/hyperliquid_tools.py <command> [args]
```

## 命令参考

### 账户

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `status` | 查看账户余额、账户模式、持仓情况以及盈亏（适用于统一账户/衍生品账户） | `hyperliquid_tools.py status` |
| `positions` | 查看详细持仓信息（杠杆率、强制平仓规则） | `hyperliquid_tools.py positions` |
| `orders` | 下单 | `hyperliquid_tools.py orders` |
| `check` | 检查持仓健康状况（账簿比例、资金状况、盈亏、杠杆率、强制平仓警告） | `hyperliquid_tools.py check` 或 `check --address 0x...` |
| `user-funding` | 查看您的资金收支记录 | `hyperliquid_tools.py user-funding --lookback 7d` |
| `portfolio` | 查看投资组合表现（盈亏、按时间段划分的交易量） | `hyperliquid_tools.py portfolio` 或 `portfolio --address 0x...` |
| `swap` | 在 USDC 和 HIP-3 衍生品之间进行资产兑换 | `hyperliquid_tools.py swap 20` 或 `swap 20 --token USDe` 或 `swap 10 --to-usdc` |

### 市场数据

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `price [COINS...]` | 查看当前价格（支持使用 HIP-3 衍生品前缀） | `hyperliquid_tools.py price BTC ETH xyz:TSLA` |
| `funding [COINS...]` | 查看资金费率（每小时更新 + 年化利率）。`--predicted` 可显示下一个小时结算的预计费率（实际费率可能在小时结束前发生变化），并提供与 Binance/Bybit 的对比数据（年化利率已标准化）。 | `hyperliquid_tools.py funding BTC SOL DOGE` 或 `funding BTC --predicted` |
| `book COIN` | 查看 L2 订单簿及价差 | `hyperliquid_tools.py book SOL` |
| `candles COIN` | 查看带有简单移动平均线的蜡烛图数据 | `hyperliquid_tools.py candles BTC --interval 1h --lookback 7d` |
| `funding-history COIN` | 查看历史资金费率 | `hyperliquid_tools.py funding-history BTC --lookback 24h` |
| `trades COIN` | 查看最近的交易记录及买卖倾向 | `hyperliquid_tools.py trades BTC --limit 20` |
| `raw COIN` | 获取原始 JSON 数据 | `hyperliquid_tools.py raw BTC` |

### 分析

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `analyze [COINS...]` | 进行全面的市场分析（价格、资金状况、订单簿深度等） | `hyperliquid_tools.py analyze BTC ETH SOL` |
| `scan` | 扫描所有资产以寻找交易机会。`--sort {funding\|volume\|oi\|price-change}` 可按指定指标对结果进行排序（默认为多指标视图）。`--reverse` 可反转排序方向。 | `hyperliquid_tools.py scan --top 20 --min-volume 100000` 或 `scan --sort volume --top 10 --reverse` |
| `hip3 [COIN]` | 查看 HIP-3 衍生品数据（价格、价差、资金费率） | `hyperliquid_tools.py hip3 TSLA` |
| `hip3` | 查看所有 HIP-3 衍生品资产 | `hyperliquid_tools.py hip3` |
| `dexes` | 列出所有 HIP-3 衍生品及其对应的资产 | `hyperliquid_tools.py dexes` |
| `history` | 从 API 获取交易历史记录 | `hyperliquid_tools.py history --limit 20` |

### 交易

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `leverage COIN LEV` | 为资产设置杠杆率（该杠杆率会在 Hyperliquid 上保持不变） | `hyperliquid_tools.py leverage SOL 5` |
| `leverage COIN LEV --isolated` | 使用隔离保证金设置杠杆率 | `hyperliquid_tools.py leverage xyz:TSLA 3 --isolated` |
| `buy COIN SIZE` | 市场买入（多头） | `hyperliquid_tools.py buy SOL 0.5` |
| `buy COIN SIZE --leverage LEV` | 先设置杠杆率再买入 | `hyperliquid_tools.py buy SOL 0.5 --leverage 5` |
| `sell COIN SIZE` | 市场卖出（空头） | `hyperliquid_tools.py sell SOL 0.5` |
| `sell COIN SIZE --leverage LEV` | 先设置杠杆率再卖出 | `hyperliquid_tools.py sell SOL 0.5 --leverage 5` |
| `limit-buy COIN SIZE PRICE` | 设置限价买入订单（GTC） | `hyperliquid_tools.py limit-buy SOL 1 120` |
| `limit-sell COIN SIZE PRICE` | 设置限价卖出订单（GTC） | `hyperliquid_tools.py limit-sell SOL 1 140` |
| `stop-loss COIN SIZE TRIGGER` | 设置止损触发条件 | `hyperliquid_tools.py stop-loss SOL 0.5 115` |
| `take-profit COIN SIZE TRIGGER` | 设置止盈触发条件 | `hyperliquid_tools.py take-profit SOL 0.5 150` |
| `close COIN` | 关闭全部持仓（支持 HIP-3 衍生品） | `hyperliquid_tools.py close SOL` |
| `cancel OID` | 取消特定订单 | `hyperliquid_tools.py cancel 12345` |
| `cancel-all` | 取消所有未成交订单 | `hyperliquid_tools.py cancel-all` |
| `modify-order OID PRICE` | 修改现有订单的价格/数量 | `hyperliquid_tools.py modify-order 12345 130.5 --size 2` |

**杠杆率：** 每个资产在您的 Hyperliquid 账户上的杠杆率是单独设置的，并会一直保持不变。每种资产都有最大杠杆率限制（例如：BTC=40x, ETH=25x, SOL=20x）。`leverage` 命令和 `--leverage` 标志用于显示当前杠杆率；如果超过限制会给出提示。使用 `positions` 命令可查看当前持仓的杠杆率。HIP-3 衍生品需要使用隔离保证金（`--isolated` 参数）。

### 智能分析（需要 XAI_API_KEY）

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `sentiment COIN` | 使用 Grok 和 X/Twitter 进行情绪分析 | `hyperliquid_tools.py sentiment BTC` |
| `unlocks [COINS...]` | 解锁资产（默认针对当前持仓） | `hyperliquid_tools.py unlocks SOL HYPE` |
| `devcheck COIN` | 获取开发者情绪分析和资产解锁信号 | `hyperliquid_tools.py devcheck SOL` |
| `ask QUERY` | 向 Grok 提出问题 — 通过 Web 或 X 服务获取综合答案。`--web` 仅使用 Web 数据，`--x` 仅使用 X 服务。 | `hyperliquid_tools.py ask "What's driving ETH price today?"` 或 `ask "BTC whale activity" --x` |
| `search QUERY` | 通过 Grok 在 Web 和 X/Twitter 上进行搜索 — 每个来源的查询结果分别显示在不同部分。`--web` 仅使用 Web 数据，`--x` 仅使用 X 服务。 | `hyperliquid_tools.py search "Hyperliquid token unlock schedule"` 或 `search "SOL news" --web` |

### 预测市场

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `polymarket [CATEGORY]` | 查看活跃的 Polymarket 预测市场 | `hyperliquid_tools.py polymarket crypto` |

类别：`crypto`（默认）、`btc`、`eth`、`trending`、`macro`

### HIP-3 交易

HIP-3 衍生品使用特定的前缀：`dex:SYMBOL`（例如：`dex:XYZ` 表示 XYZ 股票/商品）

```bash
hyperliquid_tools.py buy xyz:TSLA 1          # Buy TSLA on xyz dex
hyperliquid_tools.py sell vntl:ANTHROPIC 1   # Sell ANTHROPIC on vntl dex
hyperliquid_tools.py close xyz:GOLD          # Close GOLD position
hyperliquid_tools.py funding xyz:TSLA vntl:SPACEX km:US500
```

**已知的 HIP-3 衍生品示例：** xyz（股票/商品）、vntl（私人公司发行的代币）、flx（加密货币/商品）、hyna（加密货币）、km（指数）、abcd、cash。可以使用 `dexes` 命令动态查找所有可用的衍生品。

**HIP-3 衍生品与原生加密货币的区别：**
- 仅支持隔离保证金（不允许跨资产使用保证金）
- 每个持仓的强制平仓价格单独计算
- 手续费较高（通常是普通交易的两倍）
- 订单簿较薄（价差较大）
- 每种资产的杠杆率不同（大多数股票为 10x，商品/金属为 20x）
- 一些衍生品需要非 USDC 类型的抵押品 — 需要先进行资产兑换

**HIP-3 抵押品：** 一些衍生品支持除 USDC 以外的稳定币作为抵押品（如 USDH、USDe、USDT0）。在交易前需要先将 USDC 兑换为所需的抵押品。可以使用 `dexes` 命令查看当前的抵押品要求（这些要求可能会变动）。

| 抵押品 | 对应的兑换命令 |
|-----------|--------------|
| USDC | 无需兑换 |
| USDH | `swap <金额>` （默认） |
| USDe | `swap <金额> --token USDe` |
| USDT0 | `swap <金额> --token USDT0` |
| USDXL | `swap <金额> --token USDXL` |

**关于 USDXL：** USDXL（Last USD）不在 Hyperliquid 的官方支持列表中，其流动性较低。进行兑换时价差可能较大。目前没有 HIP-3 衍生品使用 USDXL 作为抵押品，但如有需要仍可进行兑换。

**以 km:US500 为例的交易流程：**  
```bash
hyperliquid_tools.py swap 20                          # Swap 20 USDC → USDH
hyperliquid_tools.py leverage km:US500 10 --isolated  # Set leverage
hyperliquid_tools.py buy km:US500 0.02                # Trade
hyperliquid_tools.py close km:US500                   # Close when done
hyperliquid_tools.py swap 20 --to-usdc                # Swap USDH back to USDC
```

## 缓存代理（建议先启动代理）

每次通过 CLI 执行命令时，SDK 都会重新启动并消耗约 40 个 API 计算单位来进行初始化。由于每分钟 IP 请求次数有限制（1200 次），连续执行 30 条命令后代理可能会达到速率限制。**请务必在运行命令前先启动代理。**

**启动代理：**  
```bash
{baseDir}/scripts/.venv/bin/python {baseDir}/scripts/server.py &
```

`.env` 文件默认包含 `HL_PROXY_URL=http://localhost:18731`。所有读取请求都会自动通过该代理进行转发。如需禁用代理（不建议），请将 `HL_PROXY_URL` 从文件中注释掉或删除。

**在安装或更新技能后（例如执行 `git pull` 或依赖项更新）需要重新启动代理。代理运行在内存中，因此不会自动更新代码或配置。**  
```bash
# Find and kill existing proxy, then restart
kill $(lsof -ti:18731) 2>/dev/null; {baseDir}/scripts/.venv/bin/python {baseDir}/scripts/server.py &
```

**代理端点：**

| 端点 | 描述 |
|----------|-------------|
| `GET /health` | 检查代理状态和运行时间 |
| `GET /cache/stats` | 查看各类请求的缓存命中/未命中情况 |
| `POST /cache/clear` | 清空缓存（可选参数：`{"type":"..."}` 或 `{"user":"0x..."}`）

代理会缓存 `/info` 的响应数据（元数据缓存 300 秒，价格数据缓存 5 秒，用户状态缓存 2 秒）。交易相关命令（如 `buy`、`sell`、`close` 等）会直接发送到真实的 Hyperliquid API，因为 SDK 需要使用原始 URL 进行交易签名。代理仅用于缓存读取请求。响应头中会包含 `X-Cache: HIT` 或 `X-Cache: MISS` 字符串。

**代理环境变量：**

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `HL_UPSTREAM_URL` | `https://api.hyperliquid.xyz` | 上游 API 地址 |
| `HL_PROXY_PORT` | `18731` | 代理端口 |
| `HL_CACHE_WARMUP` | `true` | 启动时预热缓存 |

## 环境变量

| 变量 | 是否必需 | 描述 |
|----------|----------|-------------|
| `HL_ACCOUNT_ADDRESS` | 用于交易/状态查询 | Hyperliquid 钱包地址 |
| `HL_SECRET_KEY` | 用于交易操作 | API 钱包私钥 |
| `HL_TESTNET` | 默认为 `false`（表示主网），`true` 表示测试网 |
| `HL_PROXY_URL` | 推荐使用 | 缓存代理地址（默认：`http://localhost:18731`） |
| `HL_ENV_FILE` | 可选 | 用于覆盖 `.env` 文件中的环境变量。适用于从其他项目调用 HyperClaw 的封装脚本 |
| `XAI_API_KEY` | 用于智能分析功能 | 用于情绪分析、解锁资产、开发者检查、查询等操作的 Grok API 密钥 |

**仅读取数据的命令**（如 `price`、`funding`、`book`、`scan`、`hip3`、`dexes`、`raw`、`polymarket`）无需输入凭据即可使用。而交易和账户相关的命令则需要 `HL_ACCOUNT_ADDRESS` 和 `HL_SECRET_KEY`。

## 账户模式

**建议使用“统一模式”进行 API 钱包交易。** 在标准模式下，资金会分散存储在现货和衍生品清算所中，API 钱包无法在这两者之间转移资金。统一模式会将所有资金汇集到一个账户中，因此使用衍生品账户时可以无需手动转账即可访问全部资金。对于需要非 USDC 抵押品的 HIP-3 衍生品，两种模式都适用 — 只需使用 `swap` 命令将 USDC 兑换为所需的抵押品即可。

Hyperliquid 账户有多种运行模式，这些模式会影响资金的存放位置。`status` 命令会自动检测当前模式，并在输出中显示相应的标识（如 `[unified]`、`[portfolio margin]` 或 `[standard]`）。

| 模式 | 标识 | 资金存放方式 |
|------|-------|-------------------|
| **统一模式**（默认） | `[unified]` | 所有资产的资金集中在一个账户中（跨所有衍生品交易所）。现货和衍生品账户共享抵押品，所有余额都显示在现货清算所中。 |
| **投资组合保证金模式** | `[portfolio margin]` | 所有符合条件的资产（如 HYPE、BTC、USDH、USDC）的资金统一计算。这种模式更具资金效率（仍处于测试阶段）。 |
| **标准模式** | `[standard]` | 每个衍生品账户和现货账户的资金分别管理，不允许跨资产使用抵押品。 |
| **衍生品隔离模式** | `[unified]` | （已弃用）USDC 默认用于衍生品账户，其他抵押品用于现货账户。由于两种模式的表现相似，因此仍显示为 `[unified]`。 |

**在计算持仓规模时，请始终使用 `status` 命令显示的“投资组合价值”。** 在标准模式下，该值等于衍生品账户的价值；在统一/投资组合保证金模式下，该值等于衍生品账户价值加上现货账户的价值。注意：“Perp Margin”子字段（仅出现在非标准模式下）仅表示衍生品账户的余额，请勿将其用于计算规模。