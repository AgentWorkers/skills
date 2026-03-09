---
name: okx-cex-market
description: "此技能适用于用户查询以下信息时：‘BTC的价格’、‘ETH的行情报价’、‘显示订单簿’、‘市场深度’、‘BTC的K线图’、‘OHLCV图表数据’、‘资金费率’、‘未平仓合约数量’、‘标记价格’、‘指数价格’、‘最近的交易记录’、‘价格限制’、‘列出可交易的金融产品’、‘有哪些金融产品可用’，或任何其他关于OKX CEX公共市场数据的查询请求。所有这些命令均为只读操作，无需API凭证即可执行。请勿使用该技能来查询账户余额/持仓情况（请使用`okx-cex-portfolio`）、下达/取消订单（请使用`okx-cex-trade`），或运行网格交易/自动投资策略机器人（请使用`okx-cex-bot`）。"
license: MIT
metadata:
  author: okx
  version: "1.0.0"
  homepage: "https://www.okx.com"
  moltbot:
    requires:
      bins: ["okx"]
    install:
      - id: npm
        kind: node
        package: "@okx_ai/okx-trade-cli"
        bins: ["okx"]
        label: "Install okx CLI (npm)"
---
# OKX CEX 市场数据 CLI

OKX 交易所的公开市场数据：价格、订单簿、蜡烛图、资金费率、未平仓合约量以及合约信息。所有命令均为 **只读**，且 **无需 API 凭据**。

## 先决条件

1. 安装 `okx` CLI：
   ```bash
   npm install -g @okx_ai/okx-trade-cli
   ```
2. 获取市场数据无需任何凭据——所有命令都是公开的。
3. 验证安装：
   ```bash
   okx market ticker BTC-USDT
   ```

## 模拟模式与实时模式

市场数据命令是公开且只读的——**模拟模式没有任何效果**。无论是否添加 `--demo` 参数，返回的数据都是一样的。运行任何市场数据命令前无需确认。

## 技能分类

- 获取市场数据（价格、图表、深度、资金费率）：使用 `okx-cex-market`（此技能）
- 查看账户余额、盈亏、持仓、费用、转账：使用 `okx-cex-portfolio`
- 下单（常规现货/掉期/期货/算法交易）：使用 `okx-cex-trade`
- 设置网格交易或自动投资（DCA）机器人：使用 `okx-cex-bot`

## 快速入门

```bash
# Current BTC spot price
okx market ticker BTC-USDT

# All SWAP (perp) tickers
okx market tickers SWAP

# BTC perp order book (top 5 levels each side)
okx market orderbook BTC-USDT-SWAP

# BTC hourly candles (last 20)
okx market candles BTC-USDT --bar 1H --limit 20

# BTC perp current funding rate
okx market funding-rate BTC-USDT-SWAP

# BTC perp funding rate history
okx market funding-rate BTC-USDT-SWAP --history

# Open interest for all SWAP instruments
okx market open-interest --instType SWAP

# List all active SPOT instruments
okx market instruments --instType SPOT
```

## 命令索引

| 编号 | 命令 | 类型 | 描述 |
|---|---|---|---|
| 1 | `okx market ticker <instId>` | 只读 | 单个合约：最新价格、24小时最高/最低价/成交量 |
| 2 | `okx market tickers <instType>` | 只读 | 某类型合约的所有报价代码 |
| 3 | `okx market instruments --instType <type>` | 只读 | 可交易合约列表 |
| 4 | `okx market orderbook <instId> [--sz <n>]` | 只读 | 订单簿中的买盘/卖盘信息 |
| 5 | `okx market candles <instId> [--bar] [--limit]` | 只读 | OHLCV 蜡烛图数据 |
| 6 | `okx market index-candles <instId> [--bar] [--limit]` | 只读 | 索引类型的 OHLCV 蜡烛图 |
| 7 | `okx market funding-rate <instId> [--history]` | 只读 | 当前或历史资金费率 |
| 8 | `okx market trades <instId> [--limit <n>]` | 只读 | 最近的交易记录 |
| 9 | `okx market mark-price --instType <type> [--instId <id>]` | 只读 | 合约的标记价格 |
| 10 | `okx market index-ticker [--instId <id>] [--quoteCcy <ccy>]` | 只读 | 指数价格（例如 BTC-USD） |
| 11 | `okx market price-limit <instId>` | 只读 | 合约的涨跌价限制 |
| 12 | `okx market open-interest --instType <type> [--instId <id>]` | 只读 | 合约和加密货币的未平仓合约量 |

## 跨技能工作流程

### 下单前查看价格
> 用户：“当前 BTC 的价格是多少？我想下限买入。”

```
1. okx-cex-market    okx market ticker BTC-USDT              → check last price and 24h range
        ↓ user decides price
2. okx-cex-portfolio okx account balance USDT                → confirm available funds
        ↓ user approves
3. okx-cex-trade     okx spot place --instId BTC-USDT --side buy --ordType limit --px <px> --sz <sz>
```

### 持有反向合约前查看资金费率
> 用户：“目前 BTC 反向合约的资金费率高吗？”

```
1. okx-cex-market    okx market funding-rate BTC-USDT-SWAP   → current rate + next funding time
2. okx-cex-market    okx market funding-rate BTC-USDT-SWAP --history  → trend over recent periods
        ↓ decide whether to hold position
3. okx-cex-portfolio okx account positions                   → check existing exposure
```

### 创建网格交易机器人前研究市场
> 用户：“我想设置一个 BTC 网格交易机器人——最近的价格区间是多少？”

```
1. okx-cex-market    okx market candles BTC-USDT --bar 4H --limit 50  → recent OHLCV for range
2. okx-cex-market    okx market ticker BTC-USDT                        → current price
3. okx-cex-market    okx market orderbook BTC-USDT --sz 20             → liquidity check
        ↓ decide minPx / maxPx
4. okx-cex-bot       okx bot grid create --instId BTC-USDT ...
```

### 比较反向合约与现货合约的溢价
> 用户：“BTC 现货合约和反向合约之间有溢价吗？”

```
1. okx-cex-market    okx market ticker BTC-USDT              → spot last price
2. okx-cex-market    okx market ticker BTC-USDT-SWAP         → perp last price
3. okx-cex-market    okx market mark-price --instType SWAP --instId BTC-USDT-SWAP  → mark price
```

### 查找并获取期权价格
> 用户：“本周到期的 BTC 期权价格是多少？”

```
1. okx-cex-market    okx market open-interest --instType OPTION --instId BTC-USD  → list active option instIds
        ↓ pick target instId from the list (e.g., BTC-USD-250328-95000-C)
2. okx-cex-market    okx market ticker BTC-USD-250328-95000-C → option last price and stats
3. okx-cex-market    okx market orderbook BTC-USD-250328-95000-C → bid/ask spread
```

> **注意**：`okx market instruments --instType OPTION` 需要指定 **标的资产**（例如 `--uly BTC-USD`）。如果标的资产未知，先使用 `okx market open-interest` 查找活跃的期权合约 ID。

## 操作流程

### 第一步：确定所需数据

- 当前价格：`okx market ticker`
- 某类别的所有价格：`okx market tickers`
- 订单簿深度：`okx market orderbook`
- 价格历史/图表：`okx market candles`
- 资金成本：`okx market funding-rate`
- 合约估值：`okx market mark-price` 或 `okx market price-limit`
- 市场成交量/未平仓合约量：`okx market open-interest`
- 存在的合约：`okx market instruments`

### 第二步：立即执行命令

所有市场数据命令均为只读操作，无需确认。

- `--instType` 可选值：`SPOT`、`SWAP`、`FUTURES`、`OPTION`
- `--bar` 可选值：`1m`、`3m`、`5m`、`15m`、`1H`、`2H`、`4H`、`6H`、`12H`、`1D`、`1W`、`1M`
- `--limit`：返回结果的数量（默认值因接口而异，通常为 100）
- `--history`：用于获取历史数据而非当前费率

### 第三步：无写入操作——无需验证

此技能中的所有命令均为只读操作，执行后无需任何验证。

## CLI 命令参考

### 单个合约的报价代码

```bash
okx market ticker <instId> [--json]
```

返回值：`last`（最新价格）、`24h high/low`（24小时最高/最低价）、`24h volume`（24小时成交量）、`sodUtc8`（24小时价格变化百分比）。

---

### 某类型合约的所有报价代码

```bash
okx market tickers <instType> [--json]
```

| 参数 | 必需 | 值 | 描述 |
|---|---|---|---|
| `instType` | 是 | `SPOT`、`SWAP`、`FUTURES`、`OPTION` | 合约类型 |

返回表格：`instId`、`last`、`high24h`、`low24h`、`vol24h`。

---

### 可交易合约列表

```bash
okx market instruments --instType <type> [--instId <id>] [--json]
```

| 参数 | 必需 | 默认值 | 描述 |
|---|---|---|---|
| `--instType` | 是 | - | `SPOT`、`SWAP`、`FUTURES`、`OPTION` | 过滤条件 |
| `--instId` | 否 | - | 过滤条件（用于指定单个合约） |

返回结果：`instId`、`ctVal`、`lotSz`、`minSz`、`tickSz`、`state`。最多显示 50 行。

---

### 订单簿

```bash
okx market orderbook <instId> [--sz <n>] [--json]
```

| 参数 | 必需 | 默认值 | 描述 |
|---|---|---|---|
| `instId` | 是 | - | 合约 ID（例如 `BTC-USDT-SWAP`） |
| `--sz` | 否 | 5 | 每侧的深度级别（1–400） |

显示按价格升序排列的买盘前 5 笔和按价格降序排列的卖盘前 5 笔。

---

### OHLCV 蜡烛图

```bash
okx market candles <instId> [--bar <bar>] [--limit <n>] [--json]
```

| 参数 | 必需 | 默认值 | 描述 |
|---|---|---|---|
| `instId` | 是 | - | 合约 ID |
| `--bar` | 否 | `1m` | 时间粒度（`1m`、`1H`、`4H`、`1D` 等） |
| `--limit` | 否 | 100 | 返回的蜡烛图数量 |

返回列：`time`（时间）、`open`（开盘价）、`high`（最高价）、`low`（最低价）、`close`（收盘价）、`vol`（成交量）。

---

### 索引类型的蜡烛图

```bash
okx market index-candles <instId> [--bar <bar>] [--limit <n>] [--history] [--json]
```

参数与 `candles` 相同。使用索引合约 ID，例如 `BTC-USD`（而非 `BTC-USDT`）。

---

### 资金费率

```bash
okx market funding-rate <instId> [--history] [--limit <n>] [--json]
```

| 参数 | 必需 | 默认值 | 描述 |
|---|---|---|---|
| `instId` | 是 | - | 交易类型（例如 `BTC-USDT-SWAP`） |
| `--history` | 否 | false | 返回历史资金费率 |
| `--limit` | 否 | - | 返回的历史记录数量 |

- **当前费率**（不使用 `--history`）：返回 `fundingRate`、`nextFundingRate`、`fundingTime`。
- **历史费率**（使用 `--history`）：返回 `fundingRate`、`realizedRate`、`fundingTime`。

---

### 最近的交易记录

```bash
okx market trades <instId> [--limit <n>] [--json]
```

返回：`tradeId`、`px`（交易价格）、`sz`（交易数量）、`side`（交易方向）、`ts`（时间戳）。

---

### 合约的标记价格

```bash
okx market mark-price --instType <type> [--instId <id>] [--json]
```

返回：`instId`、`instType`、`markPx`（标记价格）。用于计算清算价格和合约估值。

---

### 指数报价代码

```bash
okx market index-ticker [--instId <id>] [--quoteCcy <ccy>] [--json]
```

| 参数 | 必需 | 默认值 | 描述 |
|---|---|---|---|
| `--instId` | 是 | - | 指数 ID（例如 `BTC-USD`） |
| `--quoteCcy` | 是 | - | 按报价货币过滤（例如 `USD`、`USDT`） |

返回：`idxPx`、`high24h`、`low24h`。

---

### 价格限制

```bash
okx market price-limit <instId> [--json]
```

返回：`buyLmt`（买入价上限）、`sellLmt`（卖出价下限）。仅适用于 `SWAP` 和 `FUTURES` 合约。

---

### 未平仓合约量

```bash
okx market open-interest --instType <type> [--instId <id>] [--json]
```

返回：`oi`（未平仓合约量）、`oiCcy`（基础货币单位）、`ts`（时间戳）。

---

## MCP 工具参考

| 工具 | 描述 |
|---|---|
| `market_get_ticker` | 单个合约的报价代码 |
| `market_get_tickers` | 某类型合约的所有报价代码 |
| `market_get_instruments` | 合约列表 |
| `market_get_orderbook` | 订单簿深度 |
| `market_get_candles` | OHLCV 蜡烛图 |
| `market_get_index_candles` | 索引类型的 OHLCV 蜡烛图 |
| `market_get_funding_rate` | 资金费率（当前或历史数据） |
| `market_get_trades` | 最近的交易记录 |
| `market_get_mark_price` | 合约的标记价格 |
| `market_get_index_ticker` | 指数价格的报价代码 |
| `market_get_price_limit` | 合约的涨跌价限制 |
| `market_get_open_interest` | 未平仓合约量 |

---

## 输入/输出示例

**“BTC 的价格是多少？”**
```bash
okx market ticker BTC-USDT
# → instId: BTC-USDT | last: 95000.5 | 24h change %: +1.2% | 24h high: 96000 | 24h low: 93000
```

**“显示所有 SWAP 合约的报价代码”**
```bash
okx market tickers SWAP
# → table of all perpetual contracts with last price, 24h high/low/vol
```

**“显示 BTC/USDT 的订单簿情况”**
```bash
okx market orderbook BTC-USDT
# Asks (price / size):
#          95100.0  2.5
#          95050.0  1.2
# Bids (price / size):
#          95000.0  3.1
#          94950.0  0.8
```

**“显示过去 30 个时间段的 BTC 4H 蜡烛图”**
```bash
okx market candles BTC-USDT --bar 4H --limit 30
# → table: time, open, high, low, close, vol
```

**“当前 BTC 反向合约的资金费率是多少？”**
```bash
okx market funding-rate BTC-USDT-SWAP
# → fundingRate: 0.0001 | nextFundingRate: 0.00012 | fundingTime: ... | nextFundingTime: ...
```

**“显示 ETH 反向合约的历史资金费率”**
```bash
okx market funding-rate ETH-USDT-SWAP --history --limit 20
# → table: fundingRate, realizedRate, fundingTime
```

**“显示 BTC 反向合约的未平仓合约量”**
```bash
okx market open-interest --instType SWAP --instId BTC-USDT-SWAP
# → oi: 125000 | oiCcy: 125000 | ts: ...
```

**“列出所有可交易的现货合约”**
```bash
okx market instruments --instType SPOT
# → table: instId, ctVal, lotSz, minSz, tickSz, state (up to 50 rows)
```

## 特殊情况

- **合约 ID 格式**：
  - `SPOT` 使用 `BTC-USDT`；
  - `SWAP` 使用 `BTC-USDT-SWAP`；
  - `FUTURES` 使用 `BTC-USDT-250328`；
  - `OPTION` 使用 `BTC-USD-250328-95000-C`；
  - `INDEX` 使用 `BTC-USD`。
- **无法直接列出期权合约**：`okx market instruments --instType OPTION` 需要指定 `--uly BTC-USD`（标的资产）。如果标的资产未知，先使用 `okx market open-interest --instType OPTION` 查找活跃的期权合约 ID，然后再使用 `okx market ticker <instId>` 获取报价代码。
- **无数据返回**：可能是合约已退市或输入的合约 ID 错误——请使用 `okx market instruments` 验证。
- **资金费率**：仅适用于 `SWAP` 合约；对于 `SPOT`/`FUTURES` 合约会返回错误。
- **价格限制**：仅适用于 `SWAP` 和 `FUTURES` 合约。
- **标记价格**：适用于 `SWAP`、`FUTURES`、`OPTION` 合约；不适用于 `SPOT` 合约。
- **蜡烛图的时间粒度**：使用大写 `H`、`D`、`W`、`M` 表示小时/天/周/月（例如 `1H` 表示 1 小时）。
- **指数报价代码**：使用 `BTC-USD` 格式（而非 `BTC-USDT`）作为指数 ID。
- **订单簿的深度**：最大深度为 400；无论 `--sz` 设置如何，默认都会显示每侧的前三笔交易。

## 全局说明

- 所有市场数据命令均为公开数据——无需 API 密钥。
- `--json` 选项可返回原始的 OKX API v5 响应，适用于程序化调用。
- `--profile <name>` 对市场命令无效（无需身份验证）。
- 数据请求限制：每个 IP 每 2 秒内最多 20 次请求。
- 蜡烛图数据默认按最新时间排序。
- `tickers` 中的 `vol24h` 以基础货币表示（例如，`BTC-USDT` 的 `vol24h` 表示 BTC 的 24 小时成交量）。