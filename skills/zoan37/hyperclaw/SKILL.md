---
name: hyperclaw
description: 在 Hyperliquid 平台上进行交易。支持超过 228 种金融产品（包括股票、期权等），以及 HIP-3 标准的证券和商品（如特斯拉股票（TSLA）、黄金等）。平台提供市场扫描、情绪分析以及预测市场数据等功能。同时，用户可以执行各种命令来查询账户状态、市场数据、资金费率、订单簿、交易记录以及收集市场情报。
user-invocable: true
metadata:
  openclaw:
    requires:
      env:
        - HL_ACCOUNT_ADDRESS
        - HL_SECRET_KEY
---

# HyperClaw – Hyperliquid交易技能

通过CLI在Hyperliquid上进行交易。支持原生加密货币（如BTC、ETH、SOL等），以及通过HIP-3构建和部署的衍生品（如股票、商品、外汇），还包括市场扫描和智能分析工具。

## 设置

运行一次设置脚本，以创建虚拟环境并安装依赖项：

```bash
bash {baseDir}/scripts/setup.sh
```

然后在技能根目录下配置`.env`文件，填写您的Hyperliquid API凭据：

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

配置`.env`文件后，启动缓存代理（以避免API请求的速率限制）：

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
| `status` | 查看账户余额、持仓及盈亏（包括HIP-3衍生品） | `hyperliquid_tools.py status` |
| `positions` | 详细持仓信息（杠杆率、强制平仓条件） | `hyperliquid_tools.py positions` |
| `orders` | 查看未成交订单 | `hyperliquid_tools.py orders` |
| `user-funding` | 查看您的资金流入/流出情况 | `hyperliquid_tools.py user-funding --lookback 7d` |
| `portfolio` | 查看投资组合表现（盈亏、按时间段划分的交易量） | `hyperliquid_tools.py portfolio` |

### 市场数据

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `price [COINS...]` | 查看当前价格（支持HIP-3交易对前缀） | `hyperliquid_tools.py price BTC ETH xyz:TSLA` |
| `funding [COINS...]` | 查看资金费率（每小时更新，包括年化利率） | `hyperliquid_tools.py funding BTC SOL DOGE` |
| `book COIN` | 查看带有价差的L2订单簿 | `hyperliquid_tools.py book SOL` |
| `candles COIN` | 查看带有SMA指标的OHLCV蜡烛图数据 | `hyperliquid_tools.py candles BTC --interval 1h --lookback 7d` |
| `funding-history COIN` | 查看历史资金费率统计 | `hyperliquid_tools.py funding-history BTC --lookback 24h` |
| `trades COIN` | 查看最近的交易记录及买卖倾向 | `hyperliquid_tools.py trades BTC --limit 20` |
| `raw COIN` | 获取原始JSON数据用于进一步处理 | `hyperliquid_tools.py raw BTC` |

### 分析

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `analyze [COINS...]` | 进行全面的市场分析（价格、资金流动、未平仓合约数量、订单簿深度） | `hyperliquid_tools.py analyze BTC ETH SOL` |
| `scan` | 扫描所有资产以寻找资金机会 | `hyperliquid_tools.py scan --top 20 --min-volume 100000` |
| `hip3 [COIN]` | 查看HIP-3衍生品数据（价格、价差、资金费率） | `hyperliquid_tools.py hip3 TSLA` |
| `hip3` | 查看所有HIP-3交易对资产 | `hyperliquid_tools.py hip3` |
| `dexes` | 列出所有HIP-3交易对及其对应的资产 | `hyperliquid_tools.py dexes` |
| `history` | 从API获取交易历史记录 | `hyperliquid_tools.py history --limit 20` |

### 交易

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `leverage COIN LEV` | 为某个资产设置杠杆率（该杠杆率会在Hyperliquid账户中持久保存） | `hyperliquid_tools.py leverage SOL 5` |
| `leverage COIN LEV --isolated` | 使用隔离保证金设置杠杆率 | `hyperliquid_tools.py leverage xyz:TSLA 3 --isolated` |
| `buy COIN SIZE` | 市场买入（多头） | `hyperliquid_tools.py buy SOL 0.5` |
| `buy COIN SIZE --leverage LEV` | 先设置杠杆率再执行市场买入 | `hyperliquid_tools.py buy SOL 0.5 --leverage 5` |
| `sell COIN SIZE` | 市场卖出（空头） | `hyperliquid_tools.py sell SOL 0.5` |
| `sell COIN SIZE --leverage LEV` | 先设置杠杆率再执行市场卖出 | `hyperliquid_tools.py sell SOL 0.5 --leverage 5` |
| `limit-buy COIN SIZE PRICE` | 设置限价买入订单（GTC） | `hyperliquid_tools.py limit-buy SOL 1 120` |
| `limit-sell COIN SIZE PRICE` | 设置限价卖出订单（GTC） | `hyperliquid_tools.py limit-sell SOL 1 140` |
| `stop-loss COIN SIZE TRIGGER` | 设置止损触发条件 | `hyperliquid_tools.py stop-loss SOL 0.5 115` |
| `take-profit COIN SIZE TRIGGER` | 设置止盈触发条件 | `hyperliquid_tools.py take-profit SOL 0.5 150` |
| `close COIN` | 平仓全部持仓（支持HIP-3衍生品） | `hyperliquid_tools.py close SOL` |
| `cancel OID` | 取消特定订单 | `hyperliquid_tools.py cancel 12345` |
| `cancel-all` | 取消所有未成交订单 | `hyperliquid_tools.py cancel-all` |
| `modify-order OID PRICE` | 修改现有订单的价格/数量 | `hyperliquid_tools.py modify-order 12345 130.5 --size 2` |

**杠杆率说明：**  
杠杆率是根据您的Hyperliquid账户为每个资产单独设置的，并会一直保持不变，直到您手动更改。每种资产都有最大杠杆限制（例如：BTC=40倍，ETH=25倍，SOL=20倍）。`leverage`命令及`--leverage`标志可用于查看当前持仓的杠杆率。HIP-3衍生品需要使用隔离保证金（`--isolated`选项）。

### 智能分析（需要XAI_API_KEY）

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `sentiment COIN` | 进行Grok网络数据及Twitter情感分析 | `hyperliquid_tools.py sentiment BTC` |
| `unlocks [COINS...]` | 解锁代币的发行计划（默认基于当前持仓） | `hyperliquid_tools.py unlocks SOL HYPE` |
| `devcheck COIN` | 获取开发者情绪分析及市场退出信号 | `hyperliquid_tools.py devcheck SOL` |

### 预测市场

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `polymarket [CATEGORY]` | 查看Polymarket平台的预测数据 | `hyperliquid_tools.py polymarket crypto` |

**类别示例：** `crypto`（加密货币）、`btc`（比特币）、`eth`（以太坊）、`trending`（热门趋势）、`macro`（宏观经济指标）。

### HIP-3交易

HIP-3衍生品使用特定的交易对前缀：`dex:SYMBOL`（例如：`dex:XYZ`表示XYZ股票）。

**已知的HIP-3交易对：** xyz（股票、商品）、vntl（私人公司发行的代币）、flx（加密货币/商品）、hyna（加密货币）、km（指数）、abcd、cash。可以使用`dexes`命令动态查询所有可用的交易对。

**HIP-3交易对的特性：**
- 仅支持隔离保证金（不允许跨资产使用保证金）
- 每个持仓的强制平仓价格单独计算
- 手续费较高（通常是普通交易对的两倍）
- 订单簿较为稀疏（价差较大）
- 最大杠杆率因资产而异（大多数股票为10倍，商品/金属为20倍）

## 缓存代理（建议先行启动）

每次通过CLI执行命令时，都会重新启动SDK并消耗约40个API请求单位。由于每分钟IP请求量上限为1200次，连续执行30次命令后可能会触发速率限制。**请务必在运行命令前先启动缓存代理。**

**启动缓存代理：**

```bash
{baseDir}/scripts/.venv/bin/python {baseDir}/scripts/server.py &
```

`.env`文件默认配置了`HL_PROXY_URL=http://localhost:18731`，所有读取请求都会自动通过该代理。如需禁用代理（不建议），请将`HL_PROXY_URL`注释掉或从文件中删除。

**代理端点：**

| 端点 | 描述 |
|----------|-------------|
| `GET /health` | 检查代理状态和运行时间 |
| `GET /cache/stats` | 查看各类请求的缓存命中/未命中率 |
| `POST /cache/clear` | 清空缓存（可选参数：`{"type":"..."}` 或 `{"user":"0x..."}`）

代理会缓存 `/info` 的响应数据（元数据缓存300秒，价格数据5秒，用户状态信息2秒）。交易相关命令（如`buy`、`sell`、`close`等）会直接发送到Hyperliquid的API服务器，因为这些操作需要使用真实的API地址进行签名。代理仅用于缓存读取请求。响应头会包含`X-Cache: HIT`或`X-Cache: MISS`。

**代理环境变量：**

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `HL_UPSTREAM_URL` | `https://api.hyperliquid.xyz` | 上游API地址 |
| `HL_PROXY_PORT` | `18731` | 代理端口 |
| `HL_CACHE_WARMUP` | `true` | 启动时预热缓存 |

## 环境变量

| 变量 | 是否必需 | 描述 |
|----------|----------|-------------|
| `HL_ACCOUNT_ADDRESS` | 用于交易/状态查询 | Hyperliquid钱包地址 |
| `HL_SECRET_KEY` | 用于交易操作 | API钱包私钥 |
| `HL_TESTNET` | 默认值为`true`（测试网），`false`表示主网 |
| `HL_PROXY_URL` | 推荐设置 | 缓存代理地址（默认：`http://localhost:18731`） |
| `XAI_API_KEY` | 用于智能分析功能 | 用于情感分析、解锁操作和开发者检查的Grok API密钥 |

**仅读取数据的命令**（如`price`、`funding`、`book`、`scan`、`hip3`、`dexes`、`raw`、`polymarket`）无需输入凭据即可使用。而交易和账户相关命令则需要`HL_ACCOUNT_ADDRESS`和`HL_SECRET_KEY`。