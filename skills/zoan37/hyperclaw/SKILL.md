---
name: hyperclaw
description: 在 Hyperliquid 平台上进行交易。支持超过 228 种衍生品合约，包括 HIP-3 标准的股票/商品衍生品（如 TSLA、GOLD）；具备市场扫描、情绪分析以及预测市场数据的功能。提供用于查询账户状态、市场数据、资金费率、订单簿、交易操作以及收集市场情报的命令。
user-invocable: true
metadata:
  openclaw:
    requires:
      env:
        - HL_ACCOUNT_ADDRESS
        - HL_SECRET_KEY
---
# HyperClaw – 超级流动交易技能

通过 CLI 在 Hyperliquid 上进行交易。支持原生加密货币（如 BTC、ETH、SOL 等）、HIP-3 构建并部署的衍生品（如股票、商品、外汇）、市场扫描以及智能分析工具。

## 设置

运行一次设置脚本以创建虚拟环境并安装依赖项：

```bash
bash {baseDir}/scripts/setup.sh
```

然后在技能根目录下配置 `.env` 文件，填写您的 Hyperliquid API 凭据：

```
HL_ACCOUNT_ADDRESS=0x_your_wallet_address
HL_SECRET_KEY=0x_your_api_wallet_private_key
HL_TESTNET=false
```

API 密钥可从以下地址获取：https://app.hyperliquid.xyz/API — 请使用专用的 API 钱包，而非您的主钱包私钥。

**智能分析命令（情感分析、解锁、开发者检查）为可选配置：**
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
| `status` | 账户余额、账户模式、持仓情况、盈亏（适用于统一账户/衍生品账户） | `hyperliquid_tools.py status` |
| `positions` | 详细持仓信息（杠杆率、强制平仓条件） | `hyperliquid_tools.py positions` |
| `orders` | 开立订单 | `hyperliquid_tools.py orders` |
| `check` | 持仓健康检查（账簿比率、资金状况、盈亏、杠杆率、强制平仓警告） | `hyperliquid_tools.py check` 或 `check --address 0x...` |
| `user-funding` | 您收到的/支付的资金 | `hyperliquid_tools.py user-funding --lookback 7d` |
| `portfolio` | 投资组合表现（盈亏、按时间段划分的交易量） | `hyperliquid_tools.py portfolio` 或 `portfolio --address 0x...` |
| `swap` | 在 USDC 与 HIP-3 衍生品之间进行抵押品交换（例如 USDH、USDe、USDT0、USDXL） | `hyperliquid_tools.py swap 20` 或 `swap 20 --token USDe` 或 `swap 10 --to-usdc` |

### 市场数据

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `price [COINS...]` | 当前价格（支持使用 HIP-3 衍生品前缀） | `hyperliquid_tools.py price BTC ETH xyz:TSLA` |
| `funding [COINS...]` | 资金费率（每小时更新 + 年化利率）。`--predicted` 可显示下一个小时结算的预估费率（实际费率可能在小时结束前因市场价格变动而调整），并提供与 Binance/Bybit 的对比数据（年化利率已标准化）。 | `hyperliquid_tools.py funding BTC SOL DOGE` 或 `funding BTC --predicted` |
| `book COIN` | 带有价差的二级市场订单簿 | `hyperliquid_tools.py book SOL` |
| `candles COIN` | 带有简单移动平均线的蜡烛图数据 | `hyperliquid_tools.py candles BTC --interval 1h --lookback 7d` |
| `funding-history COIN` | 历史资金费率统计 | `hyperliquid_tools.py funding-history BTC --lookback 24h` |
| `trades COIN` | 最近的交易记录及买卖倾向 | `hyperliquid_tools.py trades BTC --limit 20` |
| `raw COIN` | 原始 JSON 数据导出 | `hyperliquid_tools.py raw BTC` |

### 分析

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `analyze [COINS...]` | 全面市场分析（价格、资金状况、未平仓合约数量、成交量、订单簿深度） | `hyperliquid_tools.py analyze BTC ETH SOL` |
| `scan` | 扫描所有资产以寻找资金机会。`--sort {funding\|volume\|oi\|price-change}` 可按指定指标对结果进行排序（默认为多部分显示）。 | `hyperliquid_tools.py scan --top 20 --min-volume 100000` 或 `scan --sort volume --top 10` |
| `hip3 [COIN]` | HIP-3 衍生品数据（价格、价差、资金费率） | `hyperliquid_tools.py hip3 TSLA` |
| `hip3` | 所有 HIP-3 衍生品资产 | `hyperliquid_tools.py hip3` |
| `dexes` | 列出所有 HIP-3 衍生品及其对应的资产 | `hyperliquid_tools.py dexes` |
| `history` | 通过 API 获取交易历史记录 | `hyperliquid_tools.py history --limit 20` |

### 交易

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `leverage COIN LEV` | 为某个资产设置杠杆率（该杠杆率会在 Hyperliquid 上持续生效） | `hyperliquid_tools.py leverage SOL 5` |
| `leverage COIN LEV --isolated` | 使用隔离保证金设置杠杆率 | `hyperliquid_tools.py leverage xyz:TSLA 3 --isolated` |
| `buy COIN SIZE` | 市场买入（多头） | `hyperliquid_tools.py buy SOL 0.5` |
| `buy COIN SIZE --leverage LEV` | 先设置杠杆率后再进行市场买入 | `hyperliquid_tools.py buy SOL 0.5 --leverage 5` |
| `sell COIN SIZE` | 市场卖出（空头） | `hyperliquid_tools.py sell SOL 0.5` |
| `sell COIN SIZE --leverage LEV` | 先设置杠杆率后再进行市场卖出 | `hyperliquid_tools.py sell SOL 0.5 --leverage 5` |
| `limit-buy COIN SIZE PRICE` | 定价限价买入订单（GTC） | `hyperliquid_tools.py limit-buy SOL 1 120` |
| `limit-sell COIN SIZE PRICE` | 定价限价卖出订单（GTC） | `hyperliquid_tools.py limit-sell SOL 1 140` |
| `stop-loss COIN SIZE TRIGGER` | 止损触发条件（仅限市场方向） | `hyperliquid_tools.py stop-loss SOL 0.5 115` |
| `take-profit COIN SIZE TRIGGER` | 盈利触发条件（仅限市场方向） | `hyperliquid_tools.py take-profit SOL 0.5 150` |
| `close COIN` | 平仓全部持仓（支持 HIP-3 衍生品） | `hyperliquid_tools.py close SOL` |
| `cancel OID` | 取消特定订单 | `hyperliquid_tools.py cancel 12345` |
| `cancel-all` | 取消所有未成交订单 | `hyperliquid_tools.py cancel-all` |
| `modify-order OID PRICE` | 修改现有订单的价格/数量 | `hyperliquid_tools.py modify-order 12345 130.5 --size 2` |

**杠杆率说明：** 每个资产的杠杆率在您的 Hyperliquid 账户中单独设置，并会持续有效，直到您手动更改。每种资产都有最大杠杆率限制（例如：BTC=40x、ETH=25x、SOL=20x）。`leverage` 命令和 `--leverage` 标志用于显示当前杠杆率；如果超过限制会给出提示。您可以使用 `positions` 命令查看当前持仓的杠杆率。HIP-3 衍生品需要使用隔离保证金（`--isolated` 参数）。

### 智能分析（需要 XAI_API_KEY）

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `sentiment COIN` | 结合 Grok 网络数据和 Twitter 情感分析的结果 | `hyperliquid_tools.py sentiment BTC` |
| `unlocks [COINS...]` | 解锁特定代币的安排（默认为当前持仓） | `hyperliquid_tools.py unlocks SOL HYPE` |
| `devcheck COIN` | 开发者情绪分析及市场退出信号 | `hyperliquid_tools.py devcheck SOL` |

### 预测市场

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `polymarket [CATEGORY]` | 当前的 Polymarket 预测市场 | `hyperliquid_tools.py polymarket crypto` |

类别：`crypto`（默认）、`btc`、`eth`、`trending`、`macro`

### HIP-3 交易

HIP-3 衍生品使用特定的前缀：`dex:SYMBOL`（例如 `dex:XYZ` 表示 XYZ 股票/商品）。

**已知的 HIP-3 衍生品示例：** xyz（股票、商品）、vntl（私人公司相关资产）、flx（加密货币/商品）、hyna（加密货币）、km（指数相关资产）、abcd、cash。可以使用 `dexes` 命令动态查看所有可用的衍生品。

**HIP-3 衍生品与原生加密货币的区别：**
- 仅支持隔离保证金（不允许跨资产交叉使用保证金）
- 每个持仓的强制平仓价格单独计算
- 手续费较高（通常是普通水平的 2 倍）
- 订单簿较薄（价差较大）
- 最大杠杆率因资产而异（大多数股票为 10x，商品/金属为 20x）
- 部分衍生品需要非 USDC 类型的抵押品——交易前需先进行抵押品交换

**HIP-3 衍生品的抵押品要求：**  
某些衍生品支持除 USDC 以外的稳定币作为抵押品（例如 USDH、USDe、USDT0）。在交易前，请先使用 `swap` 命令将 USDC 兑换为所需的抵押品。请注意，这些抵押品的要求可能会随时变更。

| 抵押品 | 对应的交换命令 |
|-----------|--------------|
| USDC | 无需交换 |
| USDH | `swap <金额>`（默认） |
| USDe | `swap <金额> --token USDe` |
| USDT0 | `swap <金额> --token USDT0` |
| USDXL | `swap <金额> --token USDXL` |

**关于 USDXL 的说明：**  
USDXL（Last USD）不在 Hyperliquid 的官方支持列表中，其流动性较低。进行交换时价差可能较大。目前没有 HIP-3 衍生品使用 USDXL 作为抵押品，但如有需要仍可进行交换。

**km:US500 的交易示例流程：**  
```bash
hyperliquid_tools.py swap 20                          # Swap 20 USDC → USDH
hyperliquid_tools.py leverage km:US500 10 --isolated  # Set leverage
hyperliquid_tools.py buy km:US500 0.02                # Trade
hyperliquid_tools.py close km:US500                   # Close when done
hyperliquid_tools.py swap 20 --to-usdc                # Swap USDH back to USDC
```

## 缓存代理（建议先启动代理）

每次通过 CLI 执行命令时，都会重新启动 SDK 并消耗约 40 个 API 计算单位来进行初始化。由于每分钟 API 请求的权重上限为 1200，连续执行 30 条命令后代理可能会达到请求限制。**在运行任何命令之前，请务必先启动代理。**

**启动代理：**  
```bash
{baseDir}/scripts/.venv/bin/python {baseDir}/scripts/server.py &
```

`.env` 文件默认包含 `HL_PROXY_URL=http://localhost:18731`。所有读取请求都会自动通过该代理进行转发。如需禁用代理（不建议），请在 `.env` 文件中注释掉或删除 `HL_PROXY_URL`。

**安装或更新技能后（例如通过 `git pull` 或依赖项更新）请重新启动代理。** 代理在内存中运行，因此不会自动检测代码或配置的变化。

**代理的常用端点：**  
| 端点 | 描述 |
|----------|-------------|
| `GET /health` | 检查代理状态和运行时间 |
| `GET /cache/stats` | 查看各类请求的缓存命中/未命中率 |
| `POST /cache/clear` | 清空缓存（可选参数：`{"type":"..."}` 或 `{"user":"0x..."}`）

代理会缓存 `/info` 的响应数据（元数据缓存 300 秒，价格数据 5 秒，用户状态数据 2 秒）。交易相关命令（如 `buy`、`sell`、`close` 等）会直接发送到 Hyperliquid 的真实 API，因为这些操作需要使用真实的 API 地址进行签名。代理仅用于缓存读取请求。

**代理的环境变量：**  
| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `HL_UPSTREAM_URL` | `https://api.hyperliquid.xyz` | 上游 API 地址 |
| `HL_PROXY_PORT` | `18731` | 代理端口 |
| `HL_CACHE_WARMUP` | `true` | 启动时预热缓存 |

## 环境变量

| 变量 | 是否必需 | 描述 |
|----------|----------|-------------|
| `HL_ACCOUNT_ADDRESS` | 用于交易/状态查询 | Hyperliquid 钱包地址 |
| `HL_SECRET_KEY` | 用于交易操作 | API 钱包的私钥 |
| `HL_TESTNET` | 默认值：`false`（表示主网），`true` 表示测试网 |
| `HL_PROXY_URL` | 推荐设置 | 缓存代理的 URL（默认：`http://localhost:18731`） |
| `HL_ENV_FILE` | 可选 | 如果设置此变量，则优先从该文件读取环境变量，而非默认的 `.env` 文件。适用于需要从其他项目调用 HyperClaw 的脚本 |
| `XAI_API_KEY` | 用于智能分析功能 | 用于情感分析、解锁操作和开发者检查的 API 密钥 |

**仅读取数据的命令**（`price`、`funding`、`book`、`scan`、`hip3`、`dexes`、`raw`、`polymarket`）无需输入凭据即可使用。而交易和账户相关的命令则需要 `HL_ACCOUNT_ADDRESS` 和 `HL_SECRET_KEY`。

## 账户模式

**建议使用“统一模式”进行 API 钱包交易。**在标准模式下，资金会被分配到现货市场和衍生品清算所之间，API 钱包无法在这两个市场之间转账。统一模式会将所有资金合并到一个账户中，因此使用衍生品账户的交易者可以无需手动转账即可访问全部资金。对于需要非 USDC 抵押品的 HIP-3 衍生品，两种模式都适用——只需使用 `swap` 命令将 USDC 兑换为所需的抵押品即可。

Hyperliquid 账户有多种模式，这些模式会影响资金的存放位置。`status` 命令会自动检测当前模式，并在输出中显示相应的模式标识（如 `[unified]`、`[portfolio margin]` 或 `[standard]`）。

| 模式 | 标识 | 资金存放方式 |
|------|-------|-------------------|
| **统一模式**（默认） | `[unified]` | 所有资产的资金集中在一个账户中（包括现货和衍生品）。所有资金都显示在现货清算所的账户中。 |
| **投资组合保证金模式** | `[portfolio margin]` | 所有符合条件的资产（包括 HYPE、BTC、USDH、USDC）的资金合并计算。这种模式在资金利用效率上最高，但目前仍处于测试阶段。 |
| **标准模式** | `[standard]` | 每个资产在现货市场和衍生品市场都有独立的账户。不允许跨市场使用保证金。 |
| **衍生品隔离模式** | `[unified]` | 已弃用。在这种模式下，USDC 默认用于衍生品账户，其他资产则使用现货市场的资金。虽然显示为 `[unified]`，但实际上两者资金是分开管理的。 |

**注意：** 在计算持仓规模时，请始终参考 `status` 命令返回的“投资组合价值”（Portfolio Value）。在标准模式下，该数值等于衍生品账户的资产价值；而在统一/投资组合保证金模式下，该数值等于衍生品账户价值加上现货市场的资金余额。**“衍生品保证金”（Perp Margin）这一字段仅用于非统一模式，使用时请注意其含义。**