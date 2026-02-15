---
name: stock-price-checker
description: 使用 yfinance 库检查股票价格。无需 API 密钥。
homepage: https://finance.yahoo.com
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["python3","yfinance"]}}}
---

# 股票价格查询工具

使用 `yfinance` 库从 Yahoo Finance 获取当前的股票价格。

## 快速命令

```bash
cd skills/stock-price-checker

# Check stock price
python3 stock-price.py NVDA

# Check another stock
python3 stock-price.py AAPL
```

## 使用示例

**查询 NVIDIA 的股票价格：**
```bash
python3 stock-price.py NVDA
```

**查询 VOO（标准普尔 500 指数 ETF）：**
```bash
python3 stock-price.py VOO
```

**查询 QQQ（纳斯达克 100 指数 ETF）：**
```bash
python3 stock-price.py QQQ
```

**查询任意股票代码：**
```bash
python3 stock-price.py TSLA
python3 stock-price.py MSFT
python3 stock-price.py AAPL
```

## 输出格式

```json
{
  "symbol": "NVDA",
  "price": 189.52,
  "change": 3.05,
  "change_percent": 1.64,
  "previous_close": 186.47,
  "market_cap": 4614243483648,
  "volume": 112439494,
  "fifty_two_week_high": 212.19,
  "fifty_two_week_low": 86.62
}
```

## 技术说明

- 使用 `yfinance` 库从 Yahoo Finance 获取数据
- 无需 API 密钥
- 能够优雅地处理错误
- 支持大多数主流股票和 ETF
- 返回的数据包括市值、成交量以及 52 周价格波动范围

## 故障排除

- 如果输入的股票代码无效，脚本会返回错误信息
- 部分数据（如市值）可能无法为所有股票代码提供