# 市场数据技能

此技能提供了对金融市场数据的访问权限。

## 工具

### `get_stock_price`

获取特定股票代码的OHLCV（开盘价、最高价、最低价、收盘价、成交量）数据。

**参数：**

- `ticker` (字符串)：股票代码（例如："AAPL", "BTC-USD"）。
- `timeframe` (字符串)：数据时间间隔。支持："1d"（1天）、"1wk"（1周）、"1mo"（1个月）。默认值："1d"。
- `period1` (字符串，可选)：开始日期，格式为YYYY-MM-DD。默认值为30天前。
- `period2` (字符串，可选)：结束日期，格式为YYYY-MM-DD。默认值为今天。

**用法：**

当用户需要查询股票价格、历史数据、图表数据或特定资产的近期表现时，可以使用此工具。

**示例：**

- "获取苹果公司的每日数据。" -> `get_stock_price({ ticker: 'AAPL', timeframe: '1d' })`
- "显示过去一年的比特币周线图。" -> `get_stock_price({ ticker: 'BTC-USD', timeframe: '1wk', period1: '2023-01-01' })`

### `get_crypto_price`

获取某种加密货币的当前价格和24小时波动率数据。

**参数：**

- `token` (字符串)：加密货币的名称或ID（例如："bitcoin", "solana", "ethereum"）。
- `currency` (字符串，可选)：目标货币。默认值："usd"。

**用法：**

用于查看加密货币的价格、波动率及24小时内的变化情况。

**示例：**

- "Solana的价格是多少？" -> `get_crypto_price({ token: 'solana' })`
- "比特币的情况如何？" -> `get_crypto_price({ token: 'bitcoin' })`

### `fetch_economic_calendar`

获取即将发生的重大经济事件（例如CPI、FOMC、GDP）。

**参数：**

- `importance` (字符串，可选)：事件的影响级别。可选值："High"（高）、"Medium"（中）、"Low"（低）、"All"（全部）。默认值："High"。
- `currencies` (字符串，可选)：用逗号分隔的货币代码（例如："USD,EUR"）。默认值："All"。

**用法：**

用于查看可能影响市场的新闻或安排风险管理。

**示例：**

- "本周有重大新闻吗？" -> `fetch_economic_calendar({ importance: 'High' })`
- "查看美元和欧元的相关新闻。" -> `fetch_economic_calendar({ currencies: 'USD,EUR' })`

### `get_news_headlines`

获取与特定资产或主题相关的最新50条新闻标题。

**参数：**

- `query` (字符串)：搜索主题（例如："苹果股票"、"比特币监管"、"英伟达财报"）。

**用法：**

用于进行情感分析并了解市场动态。

**示例：**

- "有关特斯拉的任何新闻吗？" -> `get_news_headlines({ query: 'Tesla Stock' })`
- "最新的加密货币监管动态是什么？" -> `get_news_headlines({ query: 'Crypto Regulation' })`