---
name: quodd
description: 通过 Quodd API 获取实时股票报价。可以获取美国股票的当前价格、每日最高/最低价以及盘后数据。当用户查询股票价格、报价、市场数据或股票代码信息时，可以使用此功能。
metadata: {"openclaw":{"emoji":"📈","requires":{"bins":["python3"],"env":["QUODD_USERNAME","QUODD_PASSWORD"]}}}
---

# Quodd 股票报价

通过 Quodd API 获取美国股票的实时报价。

更多信息，请访问：https://www.quodd.com/stock-and-etf-data

## 快速入门

```bash
# Get a quote for Apple
python scripts/quote.py AAPL

# Get quotes for multiple tickers
python scripts/quote.py AAPL MSFT META
```

## 先决条件

设置以下环境变量：

```bash
export QUODD_USERNAME="your_username"
export QUODD_PASSWORD="your_password"
```

## 使用方法

### 单个股票代码

```bash
python scripts/quote.py AAPL
```

### 多个股票代码

```bash
python scripts/quote.py AAPL MSFT META GOOGL
```

### JSON 格式输出

```bash
python scripts/quote.py AAPL --format json
```

### 强制刷新令牌

```bash
python scripts/quote.py AAPL --no-cache
```

## 输出格式

### 文本格式（默认）

```
Quodd Stock Quotes
Symbol   Date        Time      High      Low     Close    AH Time     AH Price
-------------------------------------------------------------------------------
AAPL     01/29/26    14:30    185.50   180.25   182.63   17:45:30     182.80
```

### JSON 格式

```json
{
  "quotes": [
    {
      "symbol": "AAPL",
      "date": "01/29/26",
      "time": "14:30",
      "high": 185.50,
      "low": 180.25,
      "close": 182.63,
      "after_hours_time": "17:45:30",
      "after_hours_price": 182.80
    }
  ]
}
```

## 输出字段

- **Symbol** - 股票代码
- **Date** - 报价日期
- **Time** - 报价时间
- **High** - 当日最高价
- **Low** - 当日最低价
- **Close** - 最后交易价格
- **AH Time** - 收盘后交易时间
- **AH Price** - 收盘后价格

## 注意事项

- 认证令牌会缓存在 `~/.openclaw/credentials/quodd-token.json` 文件中，缓存有效期为 20 小时。
- 如果在更改凭证后遇到认证错误，请使用 `--no-cache` 选项。