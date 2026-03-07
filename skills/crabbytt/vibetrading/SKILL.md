---
name: vibetrading
description: "使用 vibetrading Python 框架来构建、回测和部署加密货币交易策略。适用场景包括：  
(1) 从自然语言生成交易策略；  
(2) 在历史数据上回测交易策略；  
(3) 将策略部署到实际交易平台（如 Hyperliquid、Paradex、Lighter、Aster）；  
(4) 比较不同策略的性能；  
(5) 处理加密货币交易指标、头寸调整及风险管理相关任务。  
**不适用场景**：  
- 一般金融问题；  
- 非加密货币交易相关的内容；  
- 不属于 vibetrading 框架范围内的交易策略。"
---
# vibetrading

这是一个以代理（Agent）为中心的加密货币交易框架。策略是由带有 `@vibe` 装饰器的 Python 函数组成的，这些函数会调用沙箱（sandbox）函数（如 `get_perp_price`、`long`、`short` 等）。相同的代码既可用于回测（backtest），也可用于实时交易（live trading）。

## 安装

```bash
pip install vibetrading                    # Core
pip install "vibetrading[hyperliquid]"     # + Hyperliquid live trading
pip install "vibetrading[dev]"             # + pytest, ruff
```

## 核心工作流程

### 1. 编写策略

```python
import math
from vibetrading import vibe, get_perp_price, get_perp_position, get_perp_summary
from vibetrading import set_leverage, long, reduce_position, get_futures_ohlcv
from vibetrading.indicators import rsi

@vibe(interval="1h")
def my_strategy():
    price = get_perp_price("BTC")
    if math.isnan(price):
        return

    position = get_perp_position("BTC")
    if position and position.get("size", 0) != 0:
        pnl = (price - position["entry_price"]) / position["entry_price"]
        if pnl >= 0.03 or pnl <= -0.02:
            reduce_position("BTC", abs(position["size"]))
        return

    ohlcv = get_futures_ohlcv("BTC", "1h", 20)
    if ohlcv is None or len(ohlcv) < 15:
        return

    if rsi(ohlcv["close"]).iloc[-1] < 30:
        summary = get_perp_summary()
        margin = summary.get("available_margin", 0)
        if margin > 100:
            set_leverage("BTC", 3)
            qty = (margin * 0.1 * 3) / price
            if qty * price >= 15:
                long("BTC", qty, price, order_type="market")
```

### 2. 回测

```python
import vibetrading.backtest

results = vibetrading.backtest.run(code, interval="1h", slippage_bps=5)
m = results["metrics"]
# Keys: total_return, sharpe_ratio, sortino_ratio, calmar_ratio, max_drawdown,
#        win_rate, profit_factor, expectancy, number_of_trades, cagr, etc.
```

### 3. 部署到实时交易环境

```python
import vibetrading.live

await vibetrading.live.start(
    code,
    exchange="hyperliquid",
    api_key="0xWalletAddress",
    api_secret="0xPrivateKey",
    interval="1m",
)
```

## 策略规则

每个策略都必须满足以下要求：
- 导入并使用 `@vibe` 或 `@vibe(interval="1h")` 装饰器
- 在数据加载前检查价格是否为 `NaN`
- 在进入市场前检查当前持仓情况（避免过度持仓）
- 需要设置止盈和止损机制
- 在进行交易前确保 `margin > 50` 且 `qty * price >= 15`

订单类型：`"market"`（立即成交，可能存在滑点）或 `"limit"`（按指定价格成交）。

## 沙箱函数

**数据相关函数**：
`get_perp_price(asset)`, `get_spot_price(asset)`, `get_futures_ohlcv(asset, interval, limit)`, `get_spot_ohlcv(asset, interval, limit)`, `get_funding_rate(asset)`, `get_open_interest(asset)`, `get_current_time()`, `get_supported_assets()`

**账户相关函数**：
`get_perp_summary()` → 返回 `{available_margin, total_margin, ...}` 等信息
`get_perp_position(asset)` → 返回 `{size, entry_price, pnl, leverage}` 或 `None`
`my_spot_balance(asset?)`, `my_futures_balance()`

**交易相关函数**：
`long(asset, qty, price, order_type="market")`, `short(asset, qty, price, order_type="market")`, `buy(asset, qty, price)`, `sell(asset, qty, price)`, `reduce_position(asset, qty)`, `set_leverage(asset, leverage)`

## 指标

`from vibetrading.indicators import sma, ema, rsi, bbands, atr, macd, stochastic, vwap`

所有这些函数都接受 pandas Series 类型的输入，并返回 pandas Series 类型的结果。它们完全基于 pandas 库实现，不依赖其他外部库。

| 函数 | 参数 | 返回值 |
|---|---|---|
| `rsi` | `rsi(close, period=14)` | 返回 0-100 的 Series |
| `bbands` | `bbands(close, period=20, std=2.0)` | 返回 `(upper, middle, lower)` |
| `macd` | `macd(close, fast=12, slow=26, signal=9)` | 返回 `(macd_line, signal, histogram)` |
| `atr` | `atr(high, low, close, period=14)` | 返回 Series |
| `stochastic` | `stochastic(high, low, close, k=14, d=3)` | 返回 `(%K, %D)` |

## 持仓规模计算

`from vibetrading.sizing import kelly_size, fixed_fraction_size, volatility_adjusted_size, risk_per_trade_size`

- `kelly_size/win_rate, avg_win, avg_loss, balance, fraction=0.5)` — 使用半 Kelly 公式计算持仓规模（默认值）
- `risk_per_trade_size(balance, risk_pct, stop_distance, price)` — 基于风险计算的持仓规模

## 模板

```python
from vibetrading.templates import momentum, mean_reversion, grid, dca, multi_momentum
code = momentum()  # Returns valid strategy code string
```

## 人工智能生成

```python
import vibetrading.strategy

code = vibetrading.strategy.generate("BTC RSI oversold entry, 3x leverage", model="claude-sonnet-4-20250514")
result = vibetrading.strategy.validate(code)  # Static analysis
report = vibetrading.strategy.analyze(results, strategy_code=code)  # LLM analysis
```

使用该框架需要将 `ANTHROPIC_API_KEY` 或 `OPENAI_API_KEY` 设置在环境变量中。

## 策略比较

```python
import vibetrading.compare

results = vibetrading.compare.run({"RSI": code1, "MACD": code2}, slippage_bps=5)
vibetrading.compare.print_table(results)
df = vibetrading.compare.to_dataframe(results)
```

## 数据下载

```python
import vibetrading.tools
from datetime import datetime, timezone

data = vibetrading.tools.download_data(
    ["BTC", "ETH", "SOL"], exchange="binance", interval="1h",
    start_time=datetime(2025, 1, 1, tzinfo=timezone.utc),
    end_time=datetime(2025, 6, 1, tzinfo=timezone.utc),
)
results = vibetrading.backtest.run(code, data=data, slippage_bps=5)
```

## 交易所凭证

交易所凭证存储在 `.env.local` 文件中（该文件在 Git 仓库中被忽略）：

| 交易所 | `api_key` | `api_secret` | 其他信息 |
|---|---|---|---|
| Hyperliquid | 钱包地址 `0x...` | 私钥 `0x...` | — |
| Paradex | StarkNet 公钥 | StarkNet 私钥 | `account_address=` |
| Lighter | API 密钥 | API 密钥 | — |
| Aster | API 密钥 | API 密钥 | `user_address=` |

## 常见模式

有关详细的 API 文档、策略模板以及交易所特定的设置信息，请参阅 [references/api-details.md](references/api-details.md)。