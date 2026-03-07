---
name: market-global-snapshot
description: 生成一份结构化的全球市场快照报告，其中包含主要股票指数和商品的价格信息。该报告可用于用户查询市场数据、股票市场报告、每日市场总结，或获取指数（标准普尔500指数、道琼斯指数、纳斯达克指数、上证综合指数、深证指数、创业板指数、日经225指数、恒生指数）以及商品（黄金、白银、原油、铜）的当前价格及价格变动情况。
---
# 市场报告技能

生成一份结构化的全球市场快照报告，其中包含股票指数和商品数据。

## 备用方案

1. **Yahoo Finance**（首选） - 快速、数据全面
2. **Trading Economics**（备用） - 适用于指数数据，可靠性较高

如果 Yahoo Finance 出现故障（如速率限制、错误或数据缺失），则使用 Trading Economics 作为备用方案。

## 首选：Yahoo Finance

### 股票代码

使用以下股票代码：
- 标普 500：`^GSPC`
- 道琼斯：`^DJI`
- 纳斯达克：`^IXIC`
- 上证综合指数：`000001.SS`
- 深圳成分指数：`399001.SZ`
- 星期五市场（STAR Market）：`000680.SS`（注意：不是 `000688.SZ`）
- 日经 225：`^N225`
- 孟买证券交易所指数（Sensex）：`^BSESN`
- 黄金：`GC=F`
- 白银：`SI=F`
- 原油：`CL=F`
- 铜：`HG=F`

### 查询方法

使用 curl 查询 Yahoo Finance 的 API：

```bash
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/{TICKER}?interval=1d&range=5d" -H "User-Agent: Mozilla/5.0"
```

## 备用方案：Trading Economics

如果 Yahoo Finance 失效，则使用 Trading Economics 的网页数据获取方式：

### 指数查询链接

- 美国（标普 500）：`https://tradingeconomics.com/united-states/stock-market`
- 中国（上证）：`https://tradingeconomics.com/china/stock-market`
- 中国（深圳）：`https://tradingeconomics.com/china/stock-market`（相同页面，但数据不同）
- 日本（日经）：`https://tradingeconomics.com/japan/stock-market`
- 印度（孟买证券交易所指数）：`https://tradingeconomics.com/india/stock-market`

### 从 Trading Economics 提取数据

从页面内容中提取以下数据：
- **当前价格**：实时价格（例如：`6762.88`
- **前一交易日收盘价**：前一交易日的收盘价（例如：`6830.71`

计算：
- **涨跌幅度** = 当前价格 - 前一交易日收盘价
- **百分比涨幅** = （涨跌幅度 / 前一交易日收盘价）× 100

**美国指数示例：**  
```
Actual: 6762.88
Previous: 6830.71
Change: 6762.88 - 6830.71 = -67.83
Percent: -67.83 / 6830.71 * 100 = -0.99%
```

## 重要提示：计算每日涨跌幅度（Yahoo Finance）

**切勿使用 `chartPreviousClose`**——该数据对于亚洲市场通常是不准确的。**

对于中国指数（上证、深圳、星期五市场）：
1. 使用 `range=5d` 进行查询以获取多天的数据
2. 在 `indicators.quote[0].close` 数组中找到最后一个收盘价——这就是今天的收盘价
3. 找到倒数第二个收盘价——这就是前一交易日的收盘价
4. 计算：今天的收盘价 - 前一交易日的收盘价 = 涨跌幅度

**上证指数示例：**  
```
close array: [4182.59, 4122.68, 4082.47, 4108.57, 4124.19]
                                                      ↑ today (last)
                                                  ↑ previous (second to last)
Change: 4124.19 - 4108.57 = +15.62
```

## 输出格式

按照以下格式生成报告，并包含时间戳：

```
Latest snapshot from the `market-report` skill, generated at `UTC timestamp` and `China time`.

📊 Stock indices:

- 🇺🇸 S&P 500: `price` 📈/📉 `change` (`percent`)
- 🇺🇸 Dow Jones Industrial Average: `price` 📈/📉 `change` (`percent`)
- 🇺🇸 NASDAQ Composite: `price` 📈/📉 `change` (`percent`)

- 🇨🇳 SSE Composite: `price` 📈/📉 `change` (`percent`)
- 🇨🇳 Shenzhen Component Index: `price` 📈/📉 `change` (`percent`)
- 🇨🇳 STAR Market Composite: `price` 📈/📉 `change` (`percent`)

- 🇯🇵 Nikkei 225: `price` 📈/📉 `change` (`percent`)

- 🇮🇳 Sensex: `price` 📈/📉 `change` (`percent`)

🛢️ Commodities:

- 🟡 Gold: `price USD / troy oz` 📈/📉 `change` (`percent`)
- ⚪ Silver: `price USD / troy oz` 📈/📉 `change` (`percent`)
- 🛢️ Crude Oil: `price USD / barrel` 📈/📉 `change` (`percent`)
- 🟠 Copper: `price USD / lb` 📈/📉 `change` (`percent`)
```

## 格式要求：

- 所有数字保留两位小数
- 价格用反引号括起来
- 正数用 📈 表示，负数用 📉 表示
- 涨跌幅前加 + 或 - 符号
- 百分比涨幅用括号和 % 符号表示