---
name: gate-info-marketoverview
version: "2026.3.12-1"
updated: "2026-03-12"
description: "市场概述：每当用户询问整体市场情况时，请使用此技能。相关触发语句包括：“市场现状如何？”、“市场概况是什么？”、“加密货币领域正在发生什么？”  
MCP工具：  
- `info_marketsnapshot_get_market_overview`：获取市场概览信息  
- `info_coin_get_coin_rankings`：获取加密货币排名信息  
- `info_platformmetrics_get_defi_overview`：获取去中心化金融（DeFi）平台指标  
- `news_events_get_latest_events`：获取最新市场动态  
- `info_macro_get_macro_summary`：获取宏观经济指标摘要"
---
# gate-info-marketoverview

> 这是一个用于提供加密货币市场概览的技能。用户通过一句话询问整体市场状况，系统会同时调用5个MCP工具来获取市场数据、行业排行榜、DeFi领域的情况、近期事件以及宏观经济概要，随后通过大型语言模型（LLM）将这些信息整合成一份结构化的市场简报。

**触发场景**：用户询问整体市场状况，而非特定加密货币的情况。

---

## 路由规则

| 用户意图 | 关键词 | 动作 |
|-------------|----------|--------|
| 市场概览 | “市场怎么样？” “市场概况” “加密货币市场最近发生了什么” “今天是上涨还是下跌” | 执行此技能的完整工作流程 |
| 单个加密货币分析 | “比特币的情况如何？” “分析以太坊” | 路由到 `gate-info-coinanalysis` |
| 仅获取新闻 | “最近发生了什么？” | 路由到 `gate-news-briefing` |
| DeFi领域深度分析 | “哪种DeFi协议最好？” “TVL排名” | 路由到 `gate-info-defianalysis` |
| 宏观经济分析 | “就业报告如何？” “今天有经济数据吗？” | 路由到 `gate-info-macroimpact` |

---

## 执行流程

### 第1步：意图识别

确认用户询问的是整体市场状况（而非特定加密货币）。可选地提取以下信息：
- **时间范围**：例如“今天”、“这周”、“最近”（这些信息会影响新闻或事件的时间范围）

### 第2步：同时调用5个MCP工具

| 步骤 | MCP工具 | 参数 | 获取的数据 | 是否并行调用 |
|------|----------|------------|----------------|----------|
| 1a | `info_marketsnapshot_get_market_overview` | （无） | 全市场数据：总市值、24小时成交量、比特币主导地位、恐惧与贪婪指数、涨跌比例 | 是 |
| 1b | `info_coin_get_coin_rankings` | `ranking_type="gainers", time_range="24h", limit=5` | 前5名涨幅最大的加密货币 | 是 |
| 1c | `info_platformmetrics_get_defi_overview` | `category="all"` | DeFi领域的总TVL（总价值锁定）、DEX（去中心化交易所）24小时成交量、稳定币的总市值 | 是 |
| 1d | `news_events_get_latest_events` | `time_range="24h", limit=5` | 过去24小时内的主要事件 | 是 |
| 1e | `info_macro_get_macro_summary` | （无） | 宏观经济概况（美元指数、汇率、CPI趋势） | 是 |

> 这5个工具会同时并行调用，互不依赖。如果某个工具无法使用，则跳过该工具的调用，并在报告中相应部分标注“无数据”。如果`info_marketsnapshot_get_market_overview`无法使用，可以使用`info_marketsnapshot_get_market_snapshot`来获取比特币/以太坊的相关数据。

### 第2b步：可选的补充查询

| 条件 | 补充工具 | 参数 | 目的 |
|-----------|--------------------|------------|---------|
| 用户询问“这周的情况”或需要趋势分析 | `info_coin_get_coin_rankings` | `ranking_type="losers", time_range="24h", limit=5` | 显示跌幅最大的加密货币 |
| 用户对行业轮动感兴趣 | `info_coin_get_coin_rankings` | `ranking_type="hot", limit=10` | 显示热门加密货币 |

### 第3步：通过LLM整合信息

---

## 报告模板

```markdown
## Crypto Market Overview

> Data as of: {timestamp}

### 1. Market Summary

| Metric | Current Value | 24h Change |
|--------|--------------|------------|
| Total Market Cap | ${total_market_cap} | {change}% |
| 24h Volume | ${total_volume_24h} | {change}% |
| BTC Dominance | {btc_dominance}% | {change}pp |
| Fear & Greed Index | {fear_greed_index} | {Extreme Fear/Fear/Neutral/Greed/Extreme Greed} |
| Gainer/Loser Ratio | {gainers}/{losers} | {Bulls/Bears/Balanced} |

**Market Status**: {One-sentence description of the current market state based on the above metrics}

### 2. Sectors & Leaderboard

**24h Top Gainers**

| Rank | Coin | Price | 24h Change |
|------|------|-------|------------|
| 1 | {symbol} | ${price} | +{change}% |
| 2 | ... | ... | ... |

**24h Top Losers** (if data available)

| Rank | Coin | Price | 24h Change |
|------|------|-------|------------|
| 1 | {symbol} | ${price} | {change}% |
| 2 | ... | ... | ... |

{If the leaderboards show sector patterns (e.g., L2s rallying, Memes dumping), flag sector rotation}

### 3. DeFi Overview

| Metric | Value | Change |
|--------|-------|--------|
| DeFi Total TVL | ${defi_tvl} | {change}% |
| DEX 24h Volume | ${dex_volume} | {change}% |
| Stablecoin Total Market Cap | ${stablecoin_cap} | {change}% |

### 4. Recent Major Events

1. 🔴/🟡/🟢 [{event_title}] — {event_summary} ({time})
2. ...

> 🔴 = High impact, 🟡 = Medium impact, 🟢 = Low impact

### 5. Macro Environment

| Metric | Value | Trend |
|--------|-------|-------|
| US Dollar Index (DXY) | {dxy} | {Rising/Falling/Sideways} |
| 10Y Treasury Yield | {yield_10y}% | {Rising/Falling} |
| Fed Funds Rate | {fed_rate}% | {Hiking/Cutting/Paused} |

{If there are upcoming macro events (NFP, CPI, FOMC), briefly mention potential market impact}

### 6. Overall Assessment

{LLM generates a 3-5 sentence assessment:}
- Current market phase (bull / bear / sideways / recovery)
- Primary drivers
- Key risks or opportunities to watch

> The above analysis is data-driven and does not constitute investment advice.
```

---

## 决策逻辑

| 条件 | 标签/评估 |
|-----------|-----------------|
| 恐惧与贪婪指数 > 75 | “极度贪婪——在高点需谨慎” |
| 恐惧与贪婪指数 < 25 | “极度恐惧——恐慌中可能存在机会” |
| 比特币主导地位超过55%且其他加密货币普遍下跌 | “资金正在回流至比特币——其他加密货币面临压力” |
| 比特币主导地位下降且其他加密货币普遍上涨 | “可能迎来加密货币板块的上涨趋势” |
| 上涨/下跌比例 > 3:1 | “市场普遍上涨——多头占优势” |
| 上涨/下跌比例 < 1:3 | “市场普遍下跌——空头占优势” |
| DeFi领域的TVL在7天内变化超过10% | “大量资金流入DeFi领域” |
| 稳定币市值上升 | “场外资金流入——市场看涨信号” |
| 任何工具返回空数据或错误 | 跳过该部分；标注“数据不可用” |

---

## 错误处理

| 错误类型 | 处理方式 |
|------------|----------|
| `get_market_overview`或核心数据获取失败 | 返回仅包含可用部分的简化版本；或使用`info_marketsnapshot_get_market_snapshot`来获取比特币/以太坊的数据 |
| 宏观经济数据不可用 | 跳过“宏观经济环境”部分；标注“宏观经济数据暂时不可用” |
| 事件数据不可用 | 跳过“近期重大事件”部分 |
| 所有工具均失败 | 返回错误信息；建议用户稍后再试 |

---

## 跨技能路由

| 用户后续请求 | 路由到 |
|-----------------------|----------|
| “比特币的情况如何？” / 点击特定加密货币 | `gate-info-coinanalysis` |
| “为什么XX币价格突然上涨？” | `gate-news-eventexplain` |
| “有最新的新闻吗？” | `gate-news-briefing` |
| “DeFi领域的详细信息” | `gate-info-defianalysis` |
| “宏观经济数据的影响” | `gate-info-macroimpact` |
| “提供比特币的技术分析” | `gate-info-trendanalysis` |

---

## 安全规则

1. **禁止提供投资建议**：市场分析基于数据，必须包含“本内容不构成投资建议”的免责声明。
2. **禁止做出趋势预测**：不得发布“明天价格会上涨/下跌”之类的预测。
3. **数据透明性**：明确标注数据来源和更新时间。
4. **标注缺失数据**：如果某个部分的数据缺失，必须如实说明，切勿伪造数据。
5. **使用客观中立的语言**：描述市场状况时避免使用情绪化的语言。