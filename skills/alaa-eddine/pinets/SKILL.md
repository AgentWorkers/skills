---
name: pinets
description: 使用 `pinets-cli` 从命令行运行 Pine Script 指标。当需要执行、测试或分析 Pine Script 指标，计算技术分析指标（如 RSI、SMA、EMA、MACD 等），或获取加密货币交易对的市场数据时，可以使用该工具。该工具可以从 `.pine` 文件或标准输入（stdin）中运行 PineScript 指标，并输出生成的图表及变量数据。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - pinets
    primaryEnv: ""
    emoji: "\U0001F4C8"
    homepage: https://github.com/QuantForgeOrg/pinets-cli
---
# pinets-cli — 从终端运行Pine Script指标

`pinets` 是一个命令行工具（CLI），它通过 [PineTS](https://github.com/QuantForgeOrg/PineTS) 运行时环境来执行TradingView的Pine Script指标，并输出包含计算结果的结构化JSON数据。

## 安装

```bash
# Global install
npm install -g pinets-cli

# Or run directly with npx (no install needed)
npx pinets-cli run indicator.pine --symbol BTCUSDT -q
```

（如果全局安装了`pinets`，请执行相应的命令。）

## 使用方法

在使用`npx`时，以下示例中的`pinets`应替换为`npx pinets-cli`。

## 核心命令

```
pinets run [file] [options]
```

指标参数可以是**文件路径**，也可以通过标准输入（stdin）提供。

## 选项

### 数据源（必须指定一个）

| 选项                  | 描述                                                  |
| ----------------------- | -------------------------------------------------------------------------------------------- |
| `-s, --symbol <ticker>` | 来自Binance的合约代码（例如：`BTCUSDT`、`ETHUSDT`、`SOLUSDT.P`（用于期货合约） |
| `-t, --timeframe <tf>`  | 图表时间周期：`1`、`5`、`15`、`30`、`60`、`120`、`240`、`1D`、`1W`、`1M`（默认：`60`） |
| `-d, --data <path>`     | 包含蜡烛图数据的JSON文件（作为`--symbol`的替代选项）                                       |

### 输出选项

| 选项                  | 描述                                                    |
| --------------------- | -------------------------------------------------------------- |
| `-o, --output <path>` | 将输出结果写入文件而非标准输出（stdout）                                |
| `-f, --format <type>` | `default`（仅生成图表）或 `full`（生成图表 + 计算结果 + 市场数据） |
| `--pretty`            | 以美观的方式打印JSON数据                                              |
| `--clean`             | 从图表数据中过滤掉空值、`null`和`false`值        |
| `--plots <names>`     | 以逗号分隔的图表名称列表（默认：所有图表）                           |
| `-q, --quiet`         | 抑制信息输出（在解析标准输出时非常有用）         |

### 图表控制选项

| 选项                | 描述                                              |
| ------------------- | -------------------------------------------------------- |
| `-n, --candles <N>` | 输出的蜡烛图数量（默认：`500`）                |
| `-w, --warmup <N>`  | 从输出结果中排除额外的预热蜡烛图（默认：`0`） |

### 调试选项

| 选项      | 描述                                 |
| --------- | ------------------------------------------- |
| `--debug` | 在标准错误输出（stderr）中显示编译后的JavaScript代码         |

## 使用示例

### 使用实时Binance数据运行.pine文件

```bash
pinets run indicator.pine --symbol BTCUSDT --timeframe 60 --candles 100 -q
```

### 运行带有预热数据的指标（对长周期指标很重要）

```bash
# EMA 200 needs at least 200 bars to initialize
pinets run ema200.pine -s BTCUSDT -t 1D -n 100 -w 200 -q
```

### 通过标准输入传递Pine Script代码

```bash
echo '//@version=5
indicator("RSI")
plot(ta.rsi(close, 14), "RSI")' | pinets run -s BTCUSDT -t 60 -n 20 -q
```

### 使用自定义JSON数据运行指标

```bash
pinets run indicator.pine --data candles.json --candles 50 -q
```

### 将输出结果保存到文件

```bash
pinets run rsi.pine -s BTCUSDT -t 60 -o results.json -q
```

### 获取完整的执行上下文

```bash
pinets run indicator.pine -s BTCUSDT -f full -q --pretty
```

### 使用`--clean`过滤信号数据（适用于基于信号的指标）

```bash
# Without --clean: 500 entries, mostly false
pinets run ma_cross.pine -s BTCUSDT -t 1D -n 500 -q

# With --clean: Only actual signals
pinets run ma_cross.pine -s BTCUSDT -t 1D -n 500 --clean -q
```

### 使用`--plots`选择特定图表

```bash
# Get only RSI, ignore bands
pinets run rsi_bands.pine -s BTCUSDT --plots "RSI" -q

# Get only Buy and Sell signals
pinets run signals.pine -s BTCUSDT --plots "Buy,Sell" -q

# Combine both: only signals, only true values
pinets run signals.pine -s BTCUSDT --plots "Buy,Sell" --clean -q
```

## 输出格式

### `default`格式

```json
{
  "indicator": {
    "title": "RSI",
    "overlay": false
  },
  "plots": {
    "RSI": {
      "title": "RSI",
      "options": { "color": "#7E57C2" },
      "data": [
        { "time": 1704067200000, "value": 58.23 },
        { "time": 1704070800000, "value": 61.45 }
      ]
    }
  }
}
```

### `full`格式

在默认输出的基础上，还会添加`result`（每个交易时段的原始计算结果）和`marketData`（OHLCV数据）。

## JSON数据格式（用于`--data`选项）

```json
[
  {
    "openTime": 1704067200000,
    "open": 42000.5,
    "high": 42500.0,
    "low": 41800.0,
    "close": 42300.0,
    "volume": 1234.56,
    "closeTime": 1704070799999
  }
]
```

必填字段：`open`、`high`、`low`、`close`、`volume`。推荐字段：`openTime`、`closeTime`。

## Pine Script快速参考

`pinets-cli` 支持标准的TradingView Pine Script v5+语法：

```pinescript
//@version=5
indicator("My Indicator", overlay=false)

// Technical analysis functions
rsi = ta.rsi(close, 14)
[macdLine, signalLine, hist] = ta.macd(close, 12, 26, 9)
sma = ta.sma(close, 20)
ema = ta.ema(close, 9)
bb_upper = ta.sma(close, 20) + 2 * ta.stdev(close, 20)

// Output — each plot() creates a named entry in the JSON output
plot(rsi, "RSI", color=color.purple)
```

## 重要提示

- **在程序解析JSON输出时，请务必使用`-q`选项**。
- **预热数据很重要**：对于具有较长回顾周期的指标（如SMA 200、EMA 200），前N个时段的结果可能为`NaN`。使用`--warmup`选项可以预先提供数据。
- **时间值**以毫秒为单位的Unix时间戳形式提供。
- 错误信息会通过标准错误输出（stderr）显示，并返回退出代码1。
- 该工具内部集成了PineTS，运行时无需额外安装npm包。

## 预热数据建议

| 指标名称             | 最小预热时间（周期）                          |
| ------------------- | ---------------------------------- |
| SMA(N) / EMA(N)     | N                                      |
| RSI(14)             | 30                                      |
| MACD(12,26,9)       | 50                                      |
| Bollinger Bands(20) | 30                                      |
| SMA(200)            | 200                                      |

经验法则：预热时间应为最长回顾周期的1.5到2倍。