---
name: overlay-market
description: 在 BSC（Binance Smart Chain）上，您可以交易基于 Overlay Protocol 的杠杆化永续期货。您可以使用相关工具来扫描市场、利用技术指标分析价格、查看钱包余额、编写/执行交易代码，并监控交易头寸的盈亏情况。该工具适用于希望在 Overlay 上进行交易、分析市场行情或管理交易头寸的用户。
compatibility: Requires Node.js 18+. Run `npm install` in the skill directory. Requires network access to BSC RPC and Overlay APIs.
metadata:
  author: overlay-market
  version: "0.1.1"
  chain: bsc
  chain-id: "56"
env:
  OVERLAY_PRIVATE_KEY:
    required: false
    description: Private key for signing transactions (needed for send.js and --dry-run)
  BSC_RPC_URL:
    required: false
    description: BSC RPC endpoint (defaults to bsc-dataseed.binance.org)
---
# 覆盖市场（Overlay Market）

在 BSC 上，您可以交易 30 多个市场（包括加密货币、商品、指数和社交指标）的杠杆化永续期货。

覆盖市场属于合成市场——您交易的依据是协议管理的价格数据流，而非订单簿。开仓时需要使用 USDT 作为抵押品。

## 交易签名

该功能会生成未签名的交易对象（JSON 格式，包含 `to`、`data`、`value` 和 `chainId` 字段）。您的代理需要具备在 BSC（链 ID 为 56）上进行交易签名和广播的能力。我们提供了一个名为 `send.js` 的脚本，用于简化私钥签名操作，但任何签名工具都可以使用。

推荐的设置方式是使用具有受限权限的智能合约账户（例如使用 Safe 和 Zodiac Roles 功能），这样代理只能调用经过授权的函数。为了快速测试，我们还在 `.env` 文件中提供了原始私钥。

## 配置

位于技能根目录下的 `.env` 文件会被所有脚本自动加载：

```
OVERLAY_PRIVATE_KEY=0xabc...   # optional, needed for send.js and dry-run
BSC_RPC_URL=https://...        # optional, defaults to bsc-dataseed.binance.org
```

`OVERLAY_PRIVATE_KEY` 仅对 `send.js` 脚本和 `--dry-run` 模拟模式有效。如果您的代理已经具备交易签名和广播的能力，可以直接使用 `build.js`/`unwind.js` 生成的未签名交易 JSON 数据，而无需使用 `send.js`。在调用 `unwind.js` 时，请使用 `--owner <address>` 参数来指定账户地址。

## 外部服务

这些脚本会访问以下外部服务：

- **覆盖市场 API** (`apioverlay.market`）：
  - `/data/api/markets` — 市场目录
  - `/bsc-charts/v1/charts` — 开盘价、最高价、最低价、收盘价（OHLC）数据
  - `/bsc-charts/v1/charts/marketsPricesOverview` — 当前价格及价格变动信息
- **Goldsky Subgraph** (`api.goldsky.com`)：用于获取持仓数据的 GraphQL 端点
- **1inch Proxy** (`1inch-proxy-overlay-market-account.workers.dev`)：用于获取 OVL→USDT 交易报价的 Cloudflare Workers 代理（由 `unwind.js` 使用）
- **BSC RPC** (`bsc-dataseed.binance.org` 或通过 `BSC_RPC_URL` 自定义）：用于链上数据读取和交易广播

## 脚本

### balance.js — 检查钱包中的 USDT 和 BNB 余额

`node scripts/balance.js [address]`

### scan.js — 获取所有市场的相关信息（包括价格及 1小时、24小时、7天的价格变动）

`node scripts/scan.js [--details <market>]`

`--details <market>` 可以显示特定市场的详细信息（例如跟踪的资产、数据来源和计算方法）。

### chart.js — 显示 OHLC 图表以及 SMA(20)、RSI(14)、ATR(14) 指数

```bash
node scripts/chart.js <market> [timeframe] [candles]
```

- `market` — 市场名称（例如 `BTC/USD`、`SOL`、`GOLD/SILVER`）或合约地址。支持部分匹配。
- `timeframe` — 时间周期（`5m`、`15m`、`30m`、`1h`、`4h`、`12h`、`1d`（默认为 `1h`）
- `candles` — 图表显示的蜡烛图数量（默认为 48 根）

### build.js — 编码用于开仓的交易（buildStable）

```bash
node scripts/build.js <market> <long|short> <collateral_usdt> <leverage> [--slippage <pct>] [--dry-run]
```

该脚本会从状态合约中获取当前中间价，并设置价格限制及滑点容忍度（默认为 1%）。如果执行价格超出限制，交易将在链上被撤销。

`--dry-run` 选项会检查用户的 USDT 余额和交易权限，并模拟交易过程，但不会实际执行交易。输出内容包括交易金额、预计入场价格以及交易是否成功。注意：模拟是在当前区块中进行的，实际交易会在后续区块中执行，因此数值（价格、盈亏、收到的金额）可能会有所差异。

### unwind.js — 编码用于平仓的交易（unwindStable）

```bash
node scripts/unwind.js <market> <position_id> --direction <long|short> [--owner <addr>] [--slippage <pct>] [--dry-run]
```

必须指定 `--direction` 参数，以确定平仓的方向（`isLong: true` 表示多头平仓，`isLong: false` 表示空头平仓）。平仓时会平仓 100% 的持仓。滑点保护机制与开仓交易相同（默认为 1%）。

`--dry-run` 选项会显示当前持仓价值、盈亏、交易费用以及预期收到的 USDT 金额，并模拟平仓交易。

### send.js — 签名并广播未签名的交易

该脚本会从标准输入（stdin）或命令行参数（CLI）读取未签名的交易 JSON 数据，使用 `OVERLAY_PRIVATE_KEY` 进行签名，然后将其广播到 BSC 并等待确认。返回结果包含 `{"hash", "status", "blockNumber", "gasUsed"`。

### positions.js — 开仓并显示盈亏情况

`node scripts/positions.js [owner_address]`

该脚本会返回包含持仓信息的 JSON 数据（包括持仓 ID、市场名称、持仓方向、杠杆率、抵押品金额、当前价值、盈亏金额及百分比）。

## 工作流程

将构建和平仓操作的 JSON 数据输出到标准输出（stdout），并将相关信息输出到标准错误输出（stderr），以便后续通过管道（pipe）传递给 `send.js` 脚本进行处理：

```bash
# Research
node scripts/balance.js
node scripts/scan.js
node scripts/scan.js --details "BTC/USD"
node scripts/chart.js BTC/USD 4h

# Dry-run before opening
node scripts/build.js BTC/USD long 5 3 --dry-run

# Open: 5 USDT long BTC 3x
node scripts/build.js BTC/USD long 5 3 2>/dev/null | node scripts/send.js

# Monitor
node scripts/positions.js

# Dry-run before closing
node scripts/unwind.js BTC/USD 0xce --direction long --dry-run

# Close (positionId and direction from positions output)
node scripts/unwind.js BTC/USD 0xce --direction long 2>/dev/null | node scripts/send.js

# Without OVERLAY_PRIVATE_KEY (external signer)
node scripts/unwind.js BTC/USD 0xce --direction long --owner 0x1234...
```

## 相关合约（BSC 主网）

- **Shiva**（交易合约）：`0xeB497c228F130BD91E7F13f81c312243961d894A`
- **OverlayV1State**（数据读取合约）：`0x10575a9C8F36F9F42D7DB71Ef179eD9BEf8Df238`

## 资源

- 应用程序：https://appoverlay.market
- 文档：https://docsoverlay.market