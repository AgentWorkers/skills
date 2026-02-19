---
name: ccxt
description: 使用 CCXT CLI，您可以与 100 多家加密货币交易所进行交互：获取市场信息、查看订单簿、行情数据、下达交易指令、查询账户余额等。
homepage: https://docs.ccxt.com
user-invocable: true
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["ccxt"]},"install":[{"id":"node","kind":"node","package":"ccxt-cli","bins":["ccxt"]}]}}
---
# CCXT — 加密货币交易所交易工具

您可以使用 `ccxt` 命令行工具（CLI）与 100 多个加密货币交易所（如 Binance、Bybit、OKX、Kraken、Coinbase 等）进行交互。该工具支持获取市场数据、下达订单、查看账户余额以及实时数据流。

## 核心语法

```bash
ccxt <exchange_id> <methodName> [args...] [options]
```

## 在调用任何方法之前

如果您不确定某个方法需要哪些参数，可以运行以下命令：

```bash
ccxt explain <methodName>
```

该命令会显示该方法所需和可选的参数及其说明。

## 可用选项

| 标志 | 功能 |
|------|---------|
| `--verbose` | 显示原始的请求/响应数据 |
| `--sandbox` | 使用测试网（sandbox）环境 |
| `--raw` | 以纯 JSON 格式输出数据（不进行格式化） |
| `--swap` | 指定用于交易衍生品（swap）的账户 |
| `--future` | 指定用于交易期货的账户 |
| `--spot` | 指定用于交易现货的账户 |
| `--option` | 指定用于交易期权的账户 |
| `--param key=value` | 传递额外的交易所特定参数（可重复使用） |
| `--no-keys` | 跳过 API 密钥的加载 |

## 常用操作

### 市场数据（公开数据 — 无需 API 密钥）

**获取市场信息（列出交易所上的所有交易对）：**
```bash
ccxt <exchange> fetchMarkets --raw
```

**获取单个交易代码（ticker）：**
```bash
ccxt <exchange> fetchTicker "BTC/USDT" --raw
```

**获取多个交易代码：**
```bash
ccxt <exchange> fetchTickers --raw
```

**获取订单簿信息：**
```bash
ccxt <exchange> fetchOrderBook "BTC/USDT" --raw
```

**获取 OHLCV 图表数据：**
```bash
ccxt <exchange> fetchOHLCV "BTC/USDT" 1h undefined 10 --raw
```

**获取最近的交易记录：**
```bash
ccxt <exchange> fetchTrades "BTC/USDT" --raw
```

**获取交易所状态：**
```bash
ccxt <exchange> fetchStatus --raw
```

**获取货币信息：**
```bash
ccxt <exchange> fetchCurrencies --raw
```

### 交易操作（需要 API 密钥）

**下达订单：**
```bash
ccxt <exchange> createOrder "BTC/USDT" limit buy 0.001 50000 --raw
ccxt <exchange> createOrder "BTC/USDT" market buy 0.001 --raw
```

**使用额外参数下达订单：**
```bash
ccxt <exchange> createOrder "BTC/USDT" limit buy 0.001 50000 --param stopPrice=49000 --raw
```

**取消订单：**
```bash
ccxt <exchange> cancelOrder "<order_id>" "BTC/USDT" --raw
```

**获取未成交订单：**
```bash
ccxt <exchange> fetchOpenOrders "BTC/USDT" --raw
```

**获取已成交订单：**
```bash
ccxt <exchange> fetchClosedOrders "BTC/USDT" --raw
```

**获取特定订单信息：**
```bash
ccxt <exchange> fetchOrder "<order_id>" "BTC/USDT" --raw
```

### 账户操作（需要 API 密钥）

**查看账户余额：**
```bash
ccxt <exchange> fetchBalance --raw
```

**查看衍生品账户余额：**
```bash
ccxt <exchange> fetchBalance --swap --raw
```

**获取我的交易记录：**
```bash
ccxt <exchange> fetchMyTrades "BTC/USDT" --raw
```

**获取衍生品持仓信息：**
```bash
ccxt <exchange> fetchPositions --swap --raw
```

**获取存款地址：**
```bash
ccxt <exchange> fetchDepositAddress "BTC" --raw
```

### 衍生品相关操作

**获取资金费率：**
```bash
ccxt <exchange> fetchFundingRate "BTC/USDT:USDT" --raw
```

**获取资金费率历史记录：**
```bash
ccxt <exchange> fetchFundingRateHistory "BTC/USDT:USDT" --raw
```

**获取标价/指数价格：**
```bash
ccxt <exchange> fetchMarkOHLCV "BTC/USDT:USDT" 1h --raw
ccxt <exchange> fetchIndexOHLCV "BTC/USDT:USDT" 1h --raw
```

## 重要规则

1. **在引用交易代码时，请确保包含 `/` 或 `:`，例如 `"BTC/USDT"` 或 `"BTC/USDT:USDT"`。**
2. 当提供某些参数时，可以使用 `undefined` 作为占位符来跳过可选参数。例如：`ccxt binance fetchOHLCV "BTC/USDT" 1h undefined 10` 会跳过 `since` 参数，但会提供 `limit` 参数。
3. 如果需要程序化解析输出结果或用户需要纯 JSON 格式的数据，请使用 `--raw` 选项。
4. 使用 `--sandbox` 选项可以在测试环境中进行测试。建议用户在尝试下达订单时使用测试模式。
5. ISO8601 格式的日期时间（例如 `"2025-01-01T00:00:00Z"`）会自动转换为毫秒格式。
6. API 密钥必须通过环境变量（如 `BINANCE_APIKEY`、`BINANCE_SECRET`）或配置文件进行配置。如果因密钥缺失导致私有方法失败，请指导用户设置正确的密钥。
7. 衍生品交易代码的格式应为 `"BASE/QUOTE:SETTLE"`，例如 `"BTC/USDT:USDT"` 表示 USDT 保证金衍生品。
8. 在执行 `createOrder` 命令之前，请务必与用户确认交易金额和价格。CLI 会立即执行命令，不会显示确认提示。
9. 当输出数据量较大（例如 `fetchMarkets` 返回数百条记录）时，建议使用 `| head` 命令进行筛选或提示用户缩小查询范围。
10. 要查看支持的交易所列表，可以运行 `ccxt exchanges`，或访问 [https://docs.ccxt.com](https://docs.ccxt.com)。

## 认证设置

请指导用户通过以下两种方式之一配置认证信息：

**方法 1 — 使用环境变量：**
```bash
export BINANCE_APIKEY=your_api_key
export BINANCE_SECRET=your_secret
```

**方法 2 — 使用配置文件**（配置文件路径可在 `ccxt --help` 中查看）：
```json
{
  "binance": {
    "apiKey": "your_api_key",
    "secret": "your_secret"
  }
}
```

## 错误处理

- 如果出现 `AuthenticationError`，则表示 API 密钥缺失或无效。
- 如果出现 `ExchangeNotAvailable` 或 `NetworkError`，则可能是交易所暂时不可用或处于限流状态。
- 如果出现 `BadSymbol`，则表示该交易对在该交易所不存在，请使用 `fetchMarkets` 命令检查可用的交易对。
- 如果出现 `InsufficientFunds`，则表示账户余额不足，无法执行该操作。