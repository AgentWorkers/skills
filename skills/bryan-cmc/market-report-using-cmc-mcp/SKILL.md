---
name: market-report
description: >
  使用 CoinMarketCap (MCP) 数据生成一份全面的加密货币市场报告。  
  适用于用户询问市场整体状况、市场情绪或需要市场概要的情况；也可用于解答关于市场恐慌/贪婪情绪、比特币主导地位、山寨币投资时机、市场趋势等方面的问题。  
  触发词：`market report`、`market overview`、`what's happening in crypto`、`market sentiment`、`fear and greed`、`is it altcoin season`、`/market-report`
license: MIT
compatibility: ">=1.0.0"
user-invocable: true
allowed-tools:
  - mcp__cmc-mcp__get_global_metrics_latest
  - mcp__cmc-mcp__get_global_crypto_derivatives_metrics
  - mcp__cmc-mcp__trending_crypto_narratives
  - mcp__cmc-mcp__get_upcoming_macro_events
  - mcp__cmc-mcp__get_crypto_marketcap_technical_analysis
  - mcp__cmc-mcp__get_crypto_quotes_latest
  - mcp__cmc-mcp__search_cryptos
---
# 市场报告功能

通过系统地从多个CMC MCP工具中提取数据，生成一份全面的加密货币市场报告。

## 先决条件

在生成报告之前，请确认所有CMC MCP工具均可正常使用。如果某些工具出现故障或连接错误，请让用户先完成MCP连接的设置：

```json
{
  "mcpServers": {
    "cmc-mcp": {
      "url": "https://mcp.coinmarketcap.com/mcp",
      "headers": {
        "X-CMC-MCP-API-KEY": "your-api-key"
      }
    }
  }
}
```

请从[https://pro.coinmarketcap.com/login](https://pro.coinmarketcap.com/login)获取您的API密钥。

## 核心原则

从所有相关工具中获取数据，以提供完整的市场概览。用户希望每天都能获得一份可信赖的汇总信息。

## 报告工作流程

### 第1步：全球市场状况

调用`get_global_metrics_latest`获取以下信息：
- 整个加密货币市场的市值及其24小时、7天和30天的变化情况
- 恐惧与贪婪指数（当前值及趋势）
- 辅币季节性指数
- BTC和ETH的市场主导地位
- 总交易量
- ETF的流入量（BTC和ETH）

### 第2步：市场技术分析

调用`get_crypto_marketcap_technical_analysis`获取以下信息：
- 整个市场的RSI指标
- MACD技术指标
- 关键的支撑/阻力水平（斐波那契线、枢轴点）

### 第3步：杠杆与衍生品

调用`get_global_crypto_derivatives_metrics`获取以下信息：
- 总未平仓合约量及其变化情况
- 垂直利率（正数表示多头支付给空头）
- BTC的清算情况（多头与空头的对比）
- 期货合约与永续合约的分布情况

### 第4步：市场趋势分析

调用`trending_crypto_narratives`获取以下信息：
- 最热门的市场趋势主题/领域
- 每个趋势主题/领域的市值及表现
- 每个趋势主题中的热门加密货币

### 第5步：即将发生的重大事件

调用`get_upcoming_macro_events`获取以下信息：
- 美联储会议及利率决策
- 监管机构的截止日期
- 主要协议的升级
- 其他可能影响市场的重大事件

### 第6步：BTC和ETH的价格快速查询

调用`get_crypto_quotes_latest`（参数id="1,1027"）获取BTC和ETH的当前价格及其变化情况，作为报告的参考数据。

## 报告结构

请按照以下顺序呈现数据：

```
## Market Snapshot
- Total market cap: $X.XX T (24h: +X.X%)
- Fear & Greed: XX (Extreme Fear/Fear/Neutral/Greed/Extreme Greed)
- BTC Dominance: XX% | ETH Dominance: XX%
- Altcoin Season Index: XX

## BTC & ETH
- BTC: $XX,XXX (24h: X.X%, 7d: X.X%)
- ETH: $X,XXX (24h: X.X%, 7d: X.X%)

## Market Technicals
- RSI: XX (oversold/neutral/overbought)
- MACD: bullish/bearish
- Key levels: support at $X.XX T, resistance at $X.XX T

## Leverage & Sentiment
- Open Interest: $XXX B (24h: X.X%)
- Funding Rate: X.XXX% (longs/shorts paying)
- 24h Liquidations: $XXX M (XX% longs, XX% shorts)

## Trending Narratives
1. Narrative Name - $XX B market cap, +XX% (7d)
2. ...

## Upcoming Catalysts
- Date: Event description
- ...
```

## 报告的定制

- **简要概述**：如果用户要求提供简要的总结，只需重点展示市场概况和BTC/ETH的相关信息。
- **完整报告**：包含所有章节。
- **特定主题**：如果用户特别关注衍生品或市场趋势分析，可详细展开相关章节。

## 处理工具故障

在生成报告的过程中，如果某个工具出现故障：
1. 如果`get_global_metrics_latest`失败：该数据对市场概况部分至关重要。尝试重新调用一次；如果仍失败，请标记“全球市场数据不可用”并跳过该部分。
2. 如果`get_crypto_marketcap_technical_analysis`失败：跳过市场技术分析部分，继续处理其他数据。
3. 如果`get_global_crypto_derivatives_metrics`失败：跳过杠杆与市场情绪分析部分，并在报告中注明“衍生品数据不可用”。
4. 如果`trending_crypto_narratives`失败：跳过市场趋势分析部分，继续提供核心市场数据。
5. 如果`get_upcoming_macro_events`失败：跳过即将发生的重大事件部分，继续提供市场数据。
6. 如果`get_crypto_quotes_latest`失败：在报告中注明“BTC/ETH价格信息不可用”，但仍需提供其他可用数据。

无论遇到何种情况，都应尽可能提供部分报告，而不是完全放弃报告。请明确指出哪些部分缺失以及原因。