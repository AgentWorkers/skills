---
name: stock-info-explorer
description: >-
  A Yahoo Finance (yfinance) powered financial analysis tool.
  Get real-time quotes, generate high-resolution charts with moving averages + indicators (RSI/MACD/Bollinger/VWAP/ATR),
  summarize fundamentals, and run a one-shot report that outputs both a text summary and a Pro chart.
---

# 股票信息查询工具

该工具通过 `yfinance` 从 Yahoo Finance 获取股票的 OHLCV（开盘价、最高价、最低价、收盘价、成交量）数据，并在本地计算各种技术指标（无需 API 密钥）。

## 命令

### 1) 实时报价 (`price`)
```bash
uv run --script scripts/yf.py price TSLA
# shorthand
uv run --script scripts/yf.py TSLA
```

### 2) 基本面信息 (`fundamentals`)
```bash
uv run --script scripts/yf.py fundamentals NVDA
```

### 3) 股价趋势分析 (`history`)
```bash
uv run --script scripts/yf.py history AAPL 6mo
```

### 4) 专业图表 (`pro`)
生成高分辨率的 PNG 图表。默认图表会显示 **成交量** 以及 **移动平均线（MA5/20/60）**。

```bash
# candle (default)
uv run --script scripts/yf.py pro 000660.KS 6mo

# line
uv run --script scripts/yf.py pro 000660.KS 6mo line
```

#### 指标选项
通过添加参数来选择是否在图表中显示技术指标：

```bash
uv run --script scripts/yf.py pro TSLA 6mo --rsi --macd --bb
uv run --script scripts/yf.py pro TSLA 6mo --vwap --atr
```

- `--rsi` : RSI(14) （相对强弱指数）
- `--macd`: MACD(12,26,9) （移动平均线）
- `--bb`  : Bollinger Bands(20,2) （布林带）
- `--vwap`: VWAP（选定时间范围内的成交量加权平均）
- `--atr` : ATR(14) （平均真实范围）

### 5) 一次性报告 (`report`) ⭐
打印一份简洁的文本摘要（包含股价、基本面信息和技术指标信号），并自动生成包含布林带、RSI 和 MACD 的专业图表。

```bash
uv run --script scripts/yf.py report 000660.KS 6mo
# output includes: CHART_PATH:/tmp/<...>.png
```

## 可支持的股票代码示例
- 美国股票：`AAPL`, `NVDA`, `TSLA`
- 韩国股票：`005930.KS`, `000660.KS`
- 加密货币：`BTC-USD`, `ETH-KRW`
- 外汇：`USDKRW=X`

## 注意事项 / 限制
- 所有技术指标均基于本地计算得出的股价数据（Yahoo Finance 不会提供预先计算好的指标数据）。
- 不同股票/市场的数据质量可能有所不同（例如，某些股票的成交量数据可能缺失）。

---

**韩文说明：**  
这是一个综合性的股票分析工具，能够同时处理实时股价、基本面数据以及技术指标（包括图表和指标摘要）。