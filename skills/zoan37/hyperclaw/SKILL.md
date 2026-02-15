---
name: hyperclaw
description: 在 Hyperliquid 平台上进行交易。支持超过 228 种金融衍生品，包括 HIP-3 标准的股票/商品衍生品（如 TSLA、GOLD）；具备市场扫描、情绪分析以及预测市场数据的功能。提供用于查询账户状态、市场数据、资金费率、订单簿、交易操作以及收集市场情报的命令。
user-invocable: true
metadata:
  openclaw:
    requires:
      env:
        - HL_ACCOUNT_ADDRESS
        - HL_SECRET_KEY
---

# HyperClaw – Hyperliquid交易技能

通过CLI在Hyperliquid上进行交易。支持原生加密货币（如BTC、ETH、SOL等），以及由HIP-3构建和部署的衍生品（如股票、商品、外汇），还包括市场扫描和智能分析工具。

## 设置

运行一次设置脚本，以创建虚拟环境并安装依赖项：

```bash
bash {baseDir}/scripts/setup.sh
```

然后在技能根目录中配置`.env`文件，填写您的Hyperliquid API凭据：

```
HL_ACCOUNT_ADDRESS=0x_your_wallet_address
HL_SECRET_KEY=0x_your_api_wallet_private_key
HL_TESTNET=true
```

API密钥可从以下地址获取：https://app.hyperliquid.xyz/API — 请使用专用的API钱包，而非您的主钱包私钥。

**智能分析命令（情感分析、解锁、开发者检查）为可选配置：**
```
XAI_API_KEY=xai-...
```

配置完`.env`文件后，启动缓存代理（可避免速率限制）：

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
| `status` | 账户余额、账户模式、持仓情况、盈亏（适用于统一/组合保证金账户） | `hyperliquid_tools.py status` |
| `positions` | 详细持仓信息（杠杆率、清算信息） | `hyperliquid_tools.py positions` |
| `orders` | 开立订单 | `hyperliquid_tools.py orders` |
| `check` | 持仓健康检查（账簿比率、资金状况、盈亏、杠杆率、清算警告） | `hyperliquid_tools.py check` 或 `check --address 0x...` |
| `user-funding` | 您收到的/支付的资金 | `hyperliquid_tools.py user-funding --lookback 7d` |
| `portfolio` | 投资组合表现（盈亏、按时间段划分的交易量） | `hyperliquid_tools.py portfolio` 或 `portfolio --address 0x...` |
| `swap` | 在USDC与HIP-3衍生品之间进行抵押品交换（例如USDH、USDe、USDT0） | `hyperliquid_tools.py swap 20` 或 `swap 20 --token USDe` 或 `swap 10 --to-usdc` |

### 市场数据

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `price [COINS...]` | 当前价格（支持HIP-3衍生品前缀） | `hyperliquid_tools.py price BTC ETH xyz:TSLA` |
| `funding [COINS...]` | 资金费率（每小时更新，包含年化利率APR）。`--predicted`显示下一个小时结算的预估费率（实际费率可能在小时结束前因市场价格变动而调整），并提供与Binance/Bybit的对比数据（APR已标准化）。 | `hyperliquid_tools.py funding BTC SOL DOGE` 或 `funding BTC --predicted` |
| `book COIN` | 第二层订单簿（包含价差） | `hyperliquid_tools.py book SOL` |
| `candles COIN` | 带有简单移动平均线（SMA）的OHLCV蜡烛图数据 | `hyperliquid_tools.py candles BTC --interval 1h --lookback 7d` |
| `funding-history COIN` | 历史资金费率统计 | `hyperliquid_tools.py funding-history BTC --lookback 24h` |
| `trades COIN` | 最近的交易记录（包含买卖倾向） | `hyperliquid_tools.py trades BTC --limit 20` |
| `raw COIN` | 原始JSON数据（用于进一步处理） | `hyperliquid_tools.py raw BTC` |

### 分析

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `analyze [COINS...]` | 全面市场分析（价格、资金状况、订单簿深度等） | `hyperliquid_tools.py analyze BTC ETH SOL` |
| `scan` | 扫描所有衍生品以寻找交易机会。`--sort {funding\|volume\|oi\|price-change}`可根据指定指标对结果进行排序（默认为多部分视图）。 | `hyperliquid_tools.py scan --top 20 --min-volume 100000` 或 `scan --sort volume --top 10` |
| `hip3 [COIN]` | HIP-3衍生品数据（价格、价差、资金费率） | `hyperliquid_tools.py hip3 TSLA` |
| `hip3` | 所有HIP-3衍生品资产 | `hyperliquid_tools.py hip3` |
| `dexes` | 列出所有HIP-3衍生品及其对应的资产 | `hyperliquid_tools.py dexes` |
| `history` | 通过API获取的交易历史记录 | `hyperliquid_tools.py history --limit 20` |

### 交易

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `leverage COIN LEV` | 为某个资产设置杠杆率（该杠杆率会在Hyperliquid账户中持续生效） | `hyperliquid_tools.py leverage SOL 5` |
| `leverage COIN LEV --isolated` | 使用隔离保证金设置杠杆率 | `hyperliquid_tools.py leverage xyz:TSLA 3 --isolated` |
| `buy COIN SIZE` | 市场买入（多头） | `hyperliquid_tools.py buy SOL 0.5` |
| `buy COIN SIZE --leverage LEV` | 先设置杠杆率后再进行市场买入 | `hyperliquid_tools.py buy SOL 0.5 --leverage 5` |
| `sell COIN SIZE` | 市场卖出（空头） | `hyperliquid_tools.py sell SOL 0.5` |
| `sell COIN SIZE --leverage LEV` | 先设置杠杆率后再进行市场卖出 | `hyperliquid_tools.py sell SOL 0.5 --leverage 5` |
| `limit-buy COIN SIZE PRICE` | 定价买入订单（GTC） | `hyperliquid_tools.py limit-buy SOL 1 120` |
| `limit-sell COIN SIZE PRICE` | 定价卖出订单（GTC） | `hyperliquid_tools.py limit-sell SOL 1 140` |
| `stop-loss COIN SIZE TRIGGER` | 止损触发条件（仅限市场订单） | `hyperliquid_tools.py stop-loss SOL 0.5 115` |
| `take-profit COIN SIZE TRIGGER` | 盈利平仓触发条件（仅限市场订单） | `hyperliquid_tools.py take-profit SOL 0.5 150` |
| `close COIN` | 平仓全部持仓（支持HIP-3衍生品） | `hyperliquid_tools.py close SOL` |
| `cancel OID` | 取消特定订单 | `hyperliquid_tools.py cancel 12345` |
| `cancel-all` | 取消所有未成交订单 | `hyperliquid_tools.py cancel-all` |
| `modify-order OID PRICE` | 修改现有订单的价格/数量 | `hyperliquid_tools.py modify-order 12345 130.5 --size 2` |

**杠杆率说明：**杠杆率是根据您的Hyperliquid账户为每个资产单独设置的，并会一直保持不变，直到您手动更改。每种资产都有最大杠杆率限制（例如：BTC=40倍，ETH=25倍，SOL=20倍）。`leverage`命令和`--leverage`参数可用于查看当前持仓的杠杆率。HIP-3衍生品需要使用隔离保证金（`--isolated`选项）。

### 智能分析（需要XAI_API_KEY）

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `sentiment COIN` | 结合Grok网络数据和Twitter情感分析的结果 | `hyperliquid_tools.py sentiment BTC` |
| `unlocks [COINS...]` | 解锁特定代币的安排（默认为当前持仓） | `hyperliquid_tools.py unlocks SOL HYPE` |
| `devcheck COIN` | 开发者情绪分析及市场趋势信号 | `hyperliquid_tools.py devcheck SOL` |

### 预测市场

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `polymarket [CATEGORY]` | 当前的Polymarket预测市场 | `hyperliquid_tools.py polymarket crypto` |

**类别示例：`crypto`（默认）、`btc`、`eth`、`trending`、`macro` |

### HIP-3交易

HIP-3衍生品使用特定的前缀来标识：`dex:SYMBOL`（例如`dex:XYZ`表示股票或商品）。

**已知的HIP-3衍生品示例：** xyz（股票/商品）、vntl（私人公司相关资产）、flx（加密货币/商品）、hyna（加密货币）、km（指数相关资产）、abcd、cash。可以使用`dexes`命令动态查看所有可用的衍生品。

**HIP-3衍生品与原生衍生品的区别：**
- 仅支持隔离保证金（不允许跨资产使用保证金）
- 每个持仓的清算价格单独计算
- 手续费较高（通常是普通水平的2倍）
- 订单簿较薄（价差较大）
- 最大杠杆率因资产而异（股票通常为10倍，商品/金属为20倍）
- 部分衍生品需要非USDC作为抵押品——交易前需先进行抵押品交换

**HIP-3衍生品的抵押品要求：**某些衍生品支持除USDC以外的稳定币作为抵押品（如USDH、USDe、USDT0）。在使用这些衍生品前，您需要先将USDC兑换为所需的抵押品。可以使用`dexes`命令查看当前的抵押品要求（这些要求可能会随时变化）。

| 抵押品 | 对应的交换命令 |
|-----------|--------------|
| USDC | 无需交换 |
| USDH | `swap <金额>`（默认） |
| USDe | `swap <金额> --token USDe` |
| USDT0 | `swap <金额> --token USDT0` |

**以km:US500为例的交易流程：**  
```bash
hyperliquid_tools.py swap 20                          # Swap 20 USDC → USDH
hyperliquid_tools.py leverage km:US500 10 --isolated  # Set leverage
hyperliquid_tools.py buy km:US500 0.02                # Trade
hyperliquid_tools.py close km:US500                   # Close when done
hyperliquid_tools.py swap 20 --to-usdc                # Swap USDH back to USDC
```

## 缓存代理（建议先启动代理）

每次通过CLI调用时，SDK都会重新启动并消耗约40个API权重单位来进行初始化。由于IP地址的调用频率限制为每分钟1200次，连续执行30次命令后代理可能会达到速率限制。**请务必在运行任何命令前先启动代理。**

**启动代理的方法：**  
```bash
{baseDir}/scripts/.venv/bin/python {baseDir}/scripts/server.py &
```

`.env`文件默认包含`HL_PROXY_URL=http://localhost:18731`。所有读取请求都会自动通过该代理进行转发。如需禁用代理（不建议），请将`HL_PROXY_URL`注释掉或从`.env`文件中删除。

**在安装或更新技能后（例如通过`git pull`或依赖项更新）需要重新启动代理。代理运行在内存中，因此不会自动检测代码或配置的变化：**  
```bash
# Find and kill existing proxy, then restart
kill $(lsof -ti:18731) 2>/dev/null; {baseDir}/scripts/.venv/bin/python {baseDir}/scripts/server.py &
```

**代理的API端点：**  
| 端点 | 描述 |
|----------|-------------|
| `GET /health` | 检查代理状态和运行时间 |
| `GET /cache/stats` | 查看各类请求的缓存命中/未命中率 |
| `POST /cache/clear` | 清空缓存（可选参数：`{"type":"..."}` 或 `{"user":"0x..."}`）

代理会缓存 `/info` 的响应数据（元数据300秒更新一次，价格数据5秒更新一次，用户状态2秒更新一次）。交易相关命令（如`buy`、`sell`、`close`等）会直接发送到Hyperliquid的API，因为SDK需要使用真实的API地址来进行交易签名。代理仅用于缓存数据的读取操作。响应中会包含`X-Cache: HIT`或`X-Cache: MISS`头部信息。

**代理的环境变量：**  
| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `HL_UPSTREAM_URL` | `https://api.hyperliquid.xyz` | 上游API地址 |
| `HL_PROXY_PORT` | `18731` | 代理端口 |
| `HL_CACHE_WARMUP` | `true` | 启动时预热缓存 |

## 环境变量

| 变量 | 是否必需 | 描述 |
|----------|----------|-------------|
| `HLACCOUNT_ADDRESS` | 用于交易/状态查询 | Hyperliquid钱包地址 |
| `HL_SECRET_KEY` | 用于交易操作 | API钱包私钥 |
| `HL_TESTNET` | 可选 | `true`表示测试网环境；`false`表示主网环境 |
| `HL_PROXY_URL` | 推荐设置 | 缓存代理的URL（默认：`http://localhost:18731`） |
| `HL_ENV_FILE` | 可选 | 用于覆盖`.env`文件中的环境变量设置。适用于需要从其他项目调用HyperClaw的脚本 |
| `XAI_API_KEY` | 用于智能分析功能 | 用于情感分析、解锁操作和开发者检查的Grok API密钥 |

**仅支持读取操作的命令**（如`price`、`funding`、`book`、`scan`、`hip3`、`dexes`、`raw`、`polymarket`）无需输入凭据即可使用。而涉及交易和账户管理的命令则需要`HL_ACCOUNT_ADDRESS`和`HL_SECRET_KEY`。

## 账户模式

**建议使用“统一模式”进行API钱包交易。**在标准模式下，资金会分散存储在现货和衍生品清算所之间，API钱包无法直接在这两个账户之间转账。而“统一模式”会将所有资金汇集到一个账户中，这样使用衍生品时无需手动转账即可访问全部资金。对于需要非USDC作为抵押品的HIP-3衍生品，两种模式都适用——只需使用`swap`命令将USDC兑换为所需的抵押品即可。

Hyperliquid账户有多种模式可供选择，这些模式会影响资金的存放位置。`status`命令会自动检测当前账户模式，并在输出中显示相应的标识（如`[unified]`、`[portfolio margin]`或`[standard]`）。

| 模式 | 标识 | 资金管理方式 |
|------|-------|-------------------|
| **统一模式**（默认） | `[unified]` | 所有资产的资金都集中在一个账户中，所有交易都在同一个清算所进行。现货和衍生品账户共享抵押品。所有余额都显示在同一个清算所中。 |
| **组合保证金模式** | `[portfolio margin]` | 所有符合条件的资产（包括HYPE、BTC、USDH、USDC）的资金都统一计算在一个保证金账户中。这种模式在资金利用效率上最高，但目前仍处于测试阶段。 |
| **标准模式** | `[standard]` | 每个衍生品账户都有独立的资金账户，现货和衍生品账户的资金不共享。 |
| **衍生品隔离模式** | `[unified]` | 已弃用。在这种模式下，USDC默认视为衍生品账户的资金，其他类型的抵押品则归入现货账户。虽然显示为`[unified]`，但实际上资金是分开管理的。 |

**注意：**在计算持仓规模时，请始终使用`status`命令中的“Portfolio Value”字段。在标准模式下，该值等于衍生品账户的资金；而在统一/组合保证金模式下，该值等于衍生品账户资金加上现货账户的资金。对于非标准模式，`Perp Margin`字段仅表示衍生品账户的资金部分，切勿将其用于计算持仓规模。