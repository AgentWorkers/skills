---
name: crypto-research
description: >
  使用 CoinMarketCap 的 MCP 数据对某种加密货币进行全面尽职调查。  
  当用户询问关于某种加密货币的详细信息（而不仅仅是价格）时，可以使用此功能。这些信息可能包括：“[coin] 是什么？”、“[coin] 是否合法？”、“分析 [coin] 的情况？”、代币经济学相关的问题、持有者分布情况，或任何关于该加密货币的深入信息请求。  
  触发语句：`research [coin]`、`tell me about [coin]`、`should I invest in [coin]`、`DYOR [coin]`、`is [coin] safe`、`/crypto-research`
license: MIT
compatibility: ">=1.0.0"
user-invocable: true
allowed-tools:
  - mcp__cmc-mcp__search_cryptos
  - mcp__cmc-mcp__get_crypto_quotes_latest
  - mcp__cmc-mcp__get_crypto_info
  - mcp__cmc-mcp__get_crypto_metrics
  - mcp__cmc-mcp__get_crypto_technical_analysis
  - mcp__cmc-mcp__get_crypto_latest_news
  - mcp__cmc-mcp__search_crypto_info
---
# 加密货币研究技能

通过对多种加密货币市场数据（CMC MCP工具）进行系统的收集与分析，对任何一种加密货币进行全面的研究。

## 先决条件

在开始研究之前，请确认相关CMC MCP工具是否可用。如果工具出现故障或连接错误，请让用户重新设置MCP连接：

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

从https://pro.coinmarketcap.com/login获取您的API密钥。

## 核心原则

进行彻底的研究需要从多个角度来审视一种加密货币。在得出结论之前，必须收集所有相关数据，并同时关注潜在的“积极信号”（green flags）和“负面信号”（red flags）。

## 研究工作流程

### 第1步：确定目标代币

使用代币名称/符号调用`search_cryptos`函数以获取CMC ID。如果返回多个结果，请用户明确指出他们所指的具体代币。

### 第2步：基本信息

调用`get_crypto_info`函数获取以下信息：
- 项目描述和类别
- 上市日期
- 官网、社交媒体链接、文档资料
- 标签（DeFi、Layer 1、Meme coin等）

### 第3步：市场数据

调用`get_crypto_quotes_latest`函数获取以下数据：
- 当前价格和市值
- 过去24小时、7天、30天、90天及1年的价格变化
- 成交量和成交量变化
- 流通供应量与总供应量
- 市值排名

### 第4步：持有者分析

调用`get_crypto_metrics`函数获取以下信息：
- 持有者分布情况（按持有价值划分：$0-1k、$1k-100k、$100k+）
- 大额持有者的集中度（顶级持有者所占比例）
- 持有者行为（交易者、长期持有者等）

### 第5步：技术分析

调用`get_crypto_technical_analysis`函数获取以下技术指标：
- 移动平均线（7天、30天、200天的SMA/EMA）
- 相对强弱指数（RSI，低于30表示超卖，高于70表示超买）
- MACD信号
- 菲波那契支撑/阻力位和枢轴点

### 第6步：最新新闻

调用`get_crypto_latest_news`函数（设置限制为5-10条）以获取最新新闻和市场情绪。

### 第7步：深入研究（如有需要）

如果需要对代币的技术、应用场景或运作机制有更深入的了解，可以再次调用`search_crypto_info`函数。

## 分析框架

收集数据后，从以下维度进行评估：

### 基本面分析
- 该加密货币解决了什么问题？
- 是否已有可用的产品？
- 与竞争对手相比如何？
- 其应用场景是否具有可持续性？

### 代币经济学分析
- 目前流通的代币占总供应量的比例是多少？
- 是否存在通货膨胀或通货紧缩的情况？
- 是否有大量代币即将解锁？
- 持有者分布情况如何？

### 市场地位分析
- 市值排名及走势
- 成交量与市值的比例（交易活跃度如何？）
- 价格走势（是持续积累还是分散？）

### 风险因素

**负面信号及其影响：**
- 大额持有者高度集中（<10%的代币由少数地址持有）：这些大持有者可能瞬间抛售，导致价格暴跌
- 持有者数量相对于市值较少：持有者基础薄弱，价格容易被操纵
- 持有者数量持续减少：机构投资者可能正在撤离，而散户可能继续持有代币
- 负面新闻持续：持续的负面报道往往预示着价格进一步下跌
- 价格较历史高点下跌超过80%且未反弹：可能表明存在根本性问题，而不仅仅是市场周期性的波动
- 交易量极低：难以在不大幅亏损的情况下卖出代币

**积极信号及其影响：**
- 持有者数量持续增长：表明有真实的用户需求，而非人为炒作
- 长期持有者比例较高：这些持有者经过充分研究，因此卖出压力较小
- 持有者分布较为均衡：不易受到单一主体的价格操纵
- 开发和新闻更新频繁：团队正在积极推进项目，项目具有发展潜力
- 社区活跃度较高：社区效应有助于提升代币价值并维持需求

## 报告格式

将研究结果按照以下格式呈现：

```
## [Token Name] Research Report

### Overview
- Category: [DeFi/Layer 1/Meme/etc.]
- Launched: [Date]
- Rank: #XX by market cap

### Market Data
- Price: $X.XX
- Market Cap: $X.XX B
- 24h Volume: $X.XX M
- Performance: 24h X.X% | 7d X.X% | 30d X.X% | 1y X.X%

### Supply
- Circulating: X.XX M (XX% of max)
- Max Supply: X.XX M

### Holder Analysis
- Total Addresses: X.XX M
- Whale Concentration: X.X%
- Long-term Holders: XX%
- Holder Trend: Growing/Stable/Declining

### Technical Outlook
- RSI: XX (oversold/neutral/overbought)
- Trend: Above/Below 200d MA
- Key Support: $X.XX
- Key Resistance: $X.XX

### Recent News
- [Headline 1]
- [Headline 2]
- ...

### Green Flags
- [List positive indicators]

### Red Flags
- [List concerns]

### Summary
[2-3 sentence synthesis of the research findings]
```

## 重要说明

- 本报告仅用于研究目的，不构成财务建议
- 必须同时呈现正面和负面的研究结果
- 如果数据缺失或无法获取，请明确说明
- 对于非常新的代币，某些指标可能不完整

## 处理工具故障

如果在研究过程中遇到工具故障，请按照以下步骤处理：
1. 如果`search_cryptos`失败：无法继续研究，请用户核实代币名称的拼写或尝试使用合约地址。
2. 如果`get_crypto_info`失败：跳过“项目概述”部分，并在报告中注明“项目详细信息不可用”。
3. 如果`get_crypto_quotes_latest`失败：报告将不包含价格数据，请重试一次，然后在报告中注明“市场数据不可用”。
4. 如果`get_crypto_metrics`失败：跳过“持有者分析”部分，并在报告中注明“持有者分布数据不可用”。
5. 如果`get_crypto_technical_analysis`失败：跳过“技术分析”部分，并在报告中注明“技术分析结果不可用”。
6. 如果`get_crypto_latest_news`失败：跳过“最新新闻”部分，继续使用其他可用数据完成报告。

请始终根据现有数据完成报告，切勿放弃整个研究过程。