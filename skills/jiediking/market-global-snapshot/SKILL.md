---
name: market-global-snapshot
description: 生成一份结构化的全局市场快照报告，涵盖主要股票指数和商品市场信息。该报告可用于用户查询市场数据、股票市场报告、每日市场总结，或获取指数（标普500、道琼斯、纳斯达克、上证综合指数、深证指数、创业板指数、日经225、恒生指数）和商品（黄金、白银、原油、铜）的当前价格及价格变动情况。
---
# 市场报告技能

生成一份结构化的全球市场快照报告，其中包含股票指数和商品数据。

## 备用方案

1. **Yahoo Finance**（主要数据源） - 数据获取速度快，信息全面
2. **Trading Economics**（大多数指数的备用数据源）
3. **Sina Finance**（STAR Market Composite指数的备用数据源）

如果Yahoo Finance无法获取数据（由于速率限制、错误或无数据），则使用Trading Economics作为备用方案。
对于STAR Market Composite指数，专门使用Sina Finance作为备用数据源。

## 主要数据源：Yahoo Finance

### 代码符号

使用以下代码符号：
- 标准普尔500指数：`^GSPC`
- 道琼斯指数：`^DJI`
- 纳斯达克指数：`^IXIC`
- 上证综合指数：`000001.SS`
- 深证成分指数：`399001.SZ`
- STAR Market指数：`000680.SS`（注意：不是`000688.SS`）
- 日经225指数：`^N225`
- 孟买证券交易所指数（Sensex）：`^BSESN`
- 黄金：`GC=F`
- 白银：`SI=F`
- 原油：`CL=F`
- 铜：`HG=F`

### 数据查询方法

使用curl查询Yahoo Finance的API：

```bash
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/{TICKER}?interval=1d&range=5d" -H "User-Agent: Mozilla/5.0"
```

## 备用方案：Trading Economics

如果Yahoo Finance无法获取数据，使用Trading Economics的网页数据获取方法：

### 指数数据URL

- 美国（标准普尔500指数）：`https://tradingeconomics.com/united-states/stock-market`
- 中国（上证指数）：`https://tradingeconomics.com/china/stock-market`
- 中国（深证指数）：`https://tradingeconomics.com/china/stock-market`（相同页面，但数据不同）
- 日本（日经指数）：`https://tradingeconomics.com/japan/stock-market`
- 印度（孟买证券交易所指数）：`https://tradingeconomics.com/india/stock-market`

### 从Trading Economics提取数据

从页面内容中提取以下数据：
- **当前价格**：`6762.88`
- **前一交易日收盘价**：`6830.71`

计算：
- **价格变化**：`当前价格 - 前一交易日收盘价`
- **百分比变化**：`(价格变化 / 前一交易日收盘价) * 100`

**美国指数示例：**  
```
Actual: 6762.88
Previous: 6830.71
Change: 6762.88 - 6830.71 = -67.83
Percent: -67.83 / 6830.71 * 100 = -0.99%
```

## 备用方案：Sina Finance（仅用于STAR Market Composite指数）

如果Yahoo Finance无法获取STAR Market Composite指数（000680.SS）的数据，使用Sina Finance：

### 数据查询方法

```bash
curl -s "https://hq.sinajs.cn/list=sh000680" -H "Referer: https://finance.sina.com.cn" | iconv -f GB2312 -t UTF-8
```

### 响应数据格式

```
var hq_str_sh000680="科创综指,open,prev_close,low,high,close,...
```

### 数据提取

解析响应数据，提取以下信息：
- **指数名称**：科创综指（STAR Market Composite）
- **当前价格**：数据字段6（收盘价）
- **前一交易日收盘价**：数据字段3（前一交易日收盘价）

**示例：**  
```
科创综指,1771.6386,1774.0261,1744.2182,1782.4838,1744.0835,...
                                         ↑            ↑
                                     previous      current
Change: 1744.0835 - 1774.0261 = -29.94
Percent: -29.94 / 1774.0261 * 100 = -1.69%
```

## 重要提示：计算每日价格变化

**切勿使用`chartPreviousClose`**——该字段对于亚洲市场的数据通常不准确。

对于中国指数（上证、深证、STAR Market），请始终执行以下操作：
1. 使用`range=5d`参数查询多天的数据
2. 从`indicators.quote[0].close`数组中获取最后一个元素（即今天的收盘价）
3. 获取倒数第二个元素（即前一交易日的收盘价）
4. 计算：`今天收盘价 - 前一交易日收盘价`得到价格变化

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
Latest snapshot from the `market-global-snapshot` skill, generated at `UTC timestamp` and `China time`.

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

## 错误处理

如果Yahoo Finance、Trading Economics和Sina Finance都无法获取数据：
1. 仅返回可用的指数数据
2. 将无法获取的数据标记为“N/A”
3. 在报告底部显示错误信息：**⚠️ 由于API错误，部分数据无法获取**

## 历史数据

若需要获取前一天的数据，请使用数组中的倒数第二个元素（而非今天的数据）。
这是查询“昨天”数据时的默认行为。

**示例：**  
```
close array: [4124.19, 4108.57, 4082.47, 4122.68, 4182.59]
                                        ↑            ↑
                                   yesterday      today
```

## 格式规范

- 所有数字保留两位小数
- 价格用反引号括起来
- 正数用`📈`表示，负数用`📉`表示
- 价格变化用`+`或`-`符号表示
- 百分比变化用`%`符号括起来显示