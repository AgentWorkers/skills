---
name: yahoo-data-fetcher
description: 从 Yahoo Finance 获取实时股票报价。
user-invocable: true
metadata:
  moltbot:
    emoji: "📈"
    requires:
      bins: ["node"]
    homepage: https://query1.finance.yahoo.com/v7/finance/quote
---

# Yahoo 数据获取器 – 股票报价

从 Yahoo Finance 获取当前的股票价格数据。

该功能可以获取一个或多个股票代码的最新市场报价，并返回格式化后的 JSON 数据。

---

## 命令

### `/stock quote`

获取一个或多个股票代码的最新报价。

---

## 输入参数

- `symbols`（字符串或字符串数组）

示例：
- `"AAPL"`
- `"AAPL MSFT TSLA"`
- `"AAPL,MSFT,TSLA"`
- `["AAPL", "MSFT"]`
- `{ "symbols": ["AAPL", "MSFT"] }`

---

## 输出结果

对于每个股票代码：

- `symbol` – 股票代码
- `price` – 最新市场价格
- `change` – 绝对价格变化额
- `changePercent` – 百分比变化率
- `currency` – 交易货币
- `marketState` – 市场状态（例如：`REGULAR`、`CLOSED`）

示例输出：

```json
[
  {
    "symbol": "AAPL",
    "price": 189.12,
    "change": 1.23,
    "changePercent": 0.65,
    "currency": "USD",
    "marketState": "REGULAR"
  }
]
```