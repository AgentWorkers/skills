---
name: cmc-mcp
description: >
  使用 CoinMarketCap MCP 获取加密货币市场数据、价格、技术分析、新闻和趋势信息。  
  适用于任何与加密货币、代币或区块链市场相关的问题，即使用户没有明确请求数据。这包括价格查询、投资组合分析、市场对比、持有者统计信息、技术指标以及新闻等内容。  
  触发词：`"bitcoin"`、`"ETH"`、`"crypto"`、`"token price"`、`"market cap"`、`"how is [coin] doing"`、`"/cmc-mcp"`
license: MIT
compatibility: ">=1.0.0"
homepage: https://github.com/coinmarketcap/skills-for-ai-agents-by-CoinMarketCap
source: https://github.com/coinmarketcap/skills-for-ai-agents-by-CoinMarketCap
user-invocable: true
requires-credentials:
  - name: X-CMC-MCP-API-KEY
    description: CoinMarketCap API key for MCP access
    obtain-from: https://pro.coinmarketcap.com/login
    storage: MCP server configuration (mcpServers in settings)
allowed-tools:
  - mcp__cmc-mcp__search_cryptos
  - mcp__cmc-mcp__get_crypto_quotes_latest
  - mcp__cmc-mcp__get_crypto_info
  - mcp__cmc-mcp__get_crypto_metrics
  - mcp__cmc-mcp__get_crypto_technical_analysis
  - mcp__cmc-mcp__get_crypto_latest_news
  - mcp__cmc-mcp__search_crypto_info
  - mcp__cmc-mcp__get_global_metrics_latest
  - mcp__cmc-mcp__get_global_crypto_derivatives_metrics
  - mcp__cmc-mcp__get_crypto_marketcap_technical_analysis
  - mcp__cmc-mcp__trending_crypto_narratives
  - mcp__cmc-mcp__get_upcoming_macro_events
---
# CoinMarketCap MCP 技能

您可以通过 MCP 工具访问 CoinMarketCap 的数据。利用这些工具，您可以提供关于加密货币的全面、数据丰富的答案。

## 先决条件

在使用 CMC 工具之前，请确认 MCP 连接是否正常。如果工具出现故障或返回连接错误，请让用户设置 MCP 连接：

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

请从 https://pro.coinmarketcap.com/login 获取您的 API 密钥。

## 核心原则

宁可获取更多数据也不要遗漏任何数据。多个工具提供的完整答案总比部分数据更好；如果有疑问，应使用更多工具来收集全面的信息。

## 工作流程

### 1. 先进行搜索

当用户提到某种加密货币的名称或符号时，先进行搜索以获取其 ID：

```
User: "How is Solana doing?"
→ Call search_cryptos with query "solana"
→ Get ID (e.g., 5426)
→ Then call other tools using that ID
```

大多数工具需要使用 CMC 的数字 ID，而不是名称或符号。搜索工具会返回以下信息：id、name、symbol、slug 和 rank。

### 2. 在必要时批量请求

处理多种加密货币时，应批量发送请求：

```
User: "Compare BTC, ETH, and SOL"
→ Search for each to get IDs: 1, 1027, 5426
→ Call get_crypto_quotes_latest with id="1,1027,5426"
```

这样比单独发送请求更高效，并且可以在响应中进行直接比较。

### 3. 根据查询类型选择合适的工具

**获取价格和市场数据：**
- `get_crypto_quotes_latest` 可以获取价格、市值、成交量、百分比变化（1小时、24小时、7天、30天、90天、1年）、流通供应量和市场占比。

**获取加密货币的背景信息及链接：**
- `get_crypto_info` 可以获取描述、官方网站、社交链接、浏览器地址、标签和发布日期。

**进行技术分析：**
- `get_crypto_technical_analysis` 可以获取移动平均线（SMA、EMA）、MACD、RSI、斐波那契水平和枢轴点。

**获取最新新闻：**
- `get_crypto_latest_news` 可以获取新闻标题、描述、内容、链接和发布日期。

**获取持有者和分布数据：**
- `get_crypto_metrics` 可以获取按持有价值划分的地址数量、大户与其他投资者的分布情况，以及持有者的类型（交易者、长期持有者等）。

**提供概念解释：**
- `search_crypto_info` 可以对加密货币概念、白皮书和常见问题进行语义搜索。

**了解整体市场状况：**
- `get_global_metrics_latest` 可以获取总市值、恐惧/贪婪指数、山寨币季节指数、BTC/ETH 的市场占比、成交量和 ETF 流量。

**获取衍生品和杠杆数据：**
- `get_global_crypto_derivatives_metrics` 可以获取未平仓合约量、融资利率、清算情况，以及期货与永续合约的对比数据。

**进行总市值的技术分析：**
- `get_crypto_marketcap_technical_analysis` 可以为整个加密货币市场提供技术分析指标。

**获取热门趋势：**
- `trending_crypto_narratives` 可以获取热门趋势信息，包括相关加密货币的市值、成交量和表现，以及每个趋势中的主要加密货币。

**获取即将发生的事件：**
- `get_upcoming_macro_events` 可以获取预定事件，如美联储会议、监管截止日期和重要公告。

## 错误处理

**如果搜索没有结果：**
1. 说明该加密货币未找到。
2. 让用户澄清或检查拼写。
3. 如果查询可能具有歧义，建议用户更换查询内容。

**如果工具出现故障或超时：**
1. 对于暂时性的错误，尝试重新请求一次。
2. 如果仍然失败，记录哪些数据无法获取，并使用其他工具继续查询。
3. 对于价格查询，`get_crypto_quotes_latest` 是关键工具；如果重试后仍失败，应告知用户数据暂时无法获取。
4. 对于背景信息查询，如果 `get_crypto_info` 失败，应注明“项目信息无法获取”，并使用其他工具提供可用的信息。

**如果遇到 API 调用限制（429 错误）：**
1. 告知用户 API 正在受到调用限制。
2. 建议用户稍后再试。
3. 考虑是否可以通过减少工具调用次数来解决问题。

## 根据用户需求调整回答方式

根据用户的提问方式调整回答内容：
- 对于非专业性的问题（例如“比特币表现如何？”），只需提供简洁的总结和关键数据。
- 对于技术性问题（例如“BTC 的 RSI 是多少？”），可以提供更详细的数据。
- 对于广泛性的问题（例如“加密货币市场最近发生了什么？”，可以使用全球指标和热门趋势等工具来提供帮助）。