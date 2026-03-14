---
name: gate-info-coinanalysis
version: "2026.3.12-2"
updated: "2026-03-11"
description: "**货币综合分析**  
每当用户请求分析某一种货币时，可使用此功能。相关的触发短语包括：**analyze**（分析）、**how is**（情况如何）、**worth buying**（是否值得购买）、**look at**（查看）。  
**MCP工具**：  
- `info_coin_get_coin_info`：获取货币信息  
- `info_marketsnapshot_get_market_snapshot`：获取市场快照  
- `info_markettrend_get_technical_analysis`：获取技术分析报告  
- `news_feed_search_news`：搜索新闻  
- `news_feed_get_social_sentiment`：获取市场情绪数据"
---
# gate-info-coinanalysis

> 这是最常用的技能。用户输入一种加密货币的名称，系统会同时调用5个MCP工具来获取该加密货币的基本信息、市场数据、技术分析结果、新闻以及市场情绪数据，随后大型语言模型（LLM）会将这些信息整合成一份结构化的分析报告。

**触发场景**：用户提到特定的加密货币名称，或使用诸如“分析”、“目前情况如何”、“价值如何”、“查看”、“基本信息”、“市场分析”等关键词。

---

## 路由规则

| 用户意图 | 关键词 | 操作 |
|-------------|----------|--------|
| 单种加密货币的全面分析 | “分析SOL” “BTC目前的情况如何” “ETH是否值得购买” | 执行此技能的全部工作流程 |
| 仅查询价格 | “BTC的价格是多少” “ETH的当前价格” | 不要使用此技能——直接调用`info_marketsnapshot_get_market_snapshot` |
| 多种加密货币的比较 | “比较BTC和ETH” | 转向`gate-info-coincompare` |
| 仅查询新闻 | “最近有关SOL的新闻有哪些” | 转向`gate-news-briefing` |
| 仅查询技术分析 | “BTC的技术分析” “RSI指标是多少” | 转向`gate-info-trendanalysis` |

---

## 执行流程

### 第1步：意图识别与参数提取

从用户输入中提取以下信息：
- `symbol`：加密货币的代码符号（例如BTC、SOL、ETH）
- 如果用户提到了项目名称（例如Solana、Uniswap），则将其映射到相应的代码符号

如果无法识别该加密货币，请**要求用户确认硬币名称**——切勿自行猜测。

### 第2步：同时调用5个MCP工具

| 步骤 | MCP工具 | 参数 | 获取的数据 | 是否并行执行 |
|------|----------|------------|----------------|----------|
| 1a | `info_coin_get_coin_info` | `query={symbol}, scope="full"` | 基本信息：项目详情、团队信息、融资情况、所属领域、代币经济模型、解锁计划 | 是 |
| 1b | `info_marketsnapshot_get_market_snapshot` | `symbol={symbol}, timeframe="1d", source="spot"` | 市场数据：价格、24小时/7天价格变化、市值、资金率、恐惧与贪婪指数 | 是 |
| 1c | `info_markettrend_get_technical_analysis` | `symbol={symbol}` | 技术分析：多时间框架信号（RSI区间、MACD交叉、移动平均线对齐情况） | 是 |
| 1d | `news_feed_search_news` | `coin={symbol}, limit=5, sort_by="importance"` | 新闻：最近5条最重要的新闻 | 是 |
| 1e | `news_feed_get_social_sentiment` | `coin={symbol}` | 市场情绪：Twitter上相关KOL的讨论量、情绪倾向 | 是 |

> 这5个工具会同时独立执行，互不依赖。如果未配置新闻相关的MCP工具，则仅调用前3个工具；并将情绪数据标记为“无数据”。

### 第3步：大型语言模型（LLM）整合数据

将所有5个工具的响应结果传递给LLM，以生成结构化的分析报告。

### 第4步：输出结构化报告

---

## 报告模板

```markdown
## {symbol} Comprehensive Analysis

### 1. Fundamentals Overview

| Metric | Value |
|--------|-------|
| Project Name | {project_name} |
| Sector | {category} |
| Market Cap Rank | #{market_cap_rank} |
| Circulating Market Cap | ${market_cap} |
| Fully Diluted Valuation | ${fdv} |
| Total Funding Raised | ${total_funding} |
| Key Investors | {investors} |

{Brief analysis of tokenomics and unlock schedule; flag any upcoming large unlocks}

### 2. Market Data & Technical Analysis

**Current Market Data**

| Metric | Value | Status |
|--------|-------|--------|
| Price | ${price} | — |
| 24h Change | {change_24h}% | {Up/Down/Sideways} |
| 7d Change | {change_7d}% | {Up/Down/Sideways} |
| 24h Volume | ${volume_24h} | {High/Low/Normal} |
| RSI(14) | {rsi} | {Overbought/Oversold/Neutral} |
| Fear & Greed Index | {fear_greed} | {Extreme Fear/Fear/Neutral/Greed/Extreme Greed} |

**Technical Signals**

{Based on info_markettrend_get_technical_analysis multi-timeframe signals, give a Bullish/Bearish/Neutral overall assessment}

- Short-term (1h/4h): {signal}
- Medium-term (1d): {signal}
- Support: ${support}
- Resistance: ${resistance}

### 3. News & Market Sentiment

**Recent Key News**

1. [{title}]({source}) — {summary} ({time})
2. ...

**Social Sentiment**

- Twitter Discussion Volume: {level}
- KOL Sentiment Bias: {Bullish/Bearish/Neutral}
- Sentiment Score: {sentiment_score}

### 4. Overall Assessment

{LLM generates a 3-5 sentence assessment covering:}
- Current market phase for this asset
- Primary drivers (fundamentals / technicals / sentiment)
- Key risks to monitor

### ⚠️ Risk Warnings

{Data-driven risk alerts, e.g.:}
- RSI overbought — elevated short-term pullback risk
- Upcoming large token unlock
- High funding rate — leveraged long crowding
- Low liquidity (if applicable)

> The above analysis is data-driven and does not constitute investment advice. Please make decisions based on your own risk tolerance.
```

---

## 决策逻辑

| 条件 | 评估结果 |
|-----------|------------|
| RSI > 70 | 标记为“超买状态——短期回调风险增加” |
| RSI < 30 | 标记为“超卖状态——可能出现反弹” |
| 24小时成交量 > 7天平均成交量的2倍 | 标记为“成交量显著上升” |
| 24小时成交量 < 7天平均成交量的0.5倍 | 标记为“成交量显著下降” |
| 资金率 > 0.05% | 标记为“资金率较高——多头情绪浓厚” |
| 资金率 < -0.05% | 标记为“资金率较低——空头情绪浓厚” |
| 恐惧与贪婪指数（Fear & Greed Index） > 75 | 标记为“极度贪婪——需谨慎操作” |
| 恐惧与贪婪指数 < 25 | 标记为“极度恐惧——可能存在投资机会” |
| 下30天内将有超过5%的流通代币被解锁 | 标记为“即将有大量代币解锁——可能带来卖出压力” |
| 任何工具返回空数据或错误 | 跳过该部分；在报告中注明“数据不可用” |

---

## 错误处理

| 错误类型 | 处理方式 |
|------------|----------|
| 未找到相应的加密货币 | 提示用户确认硬币名称；建议使用`info_coin_search_coins` |
| 单个工具执行超时 | 跳过该部分；注明“该数据暂时无法获取” |
| 所有工具均失败 | 返回错误信息；建议用户稍后再试 |
| 用户输入了多个加密货币名称 | 转向`gate-info-coincompare` |
| 用户输入了地址而非硬币名称 | 转向`gate-info-addresstracker` |

---

## 跨技能路由

| 用户后续操作意图 | 转向的技能 | -----------------------|
| “提供技术分析” | `gate-info-trendanalysis` |
| “最近有什么新闻吗？” | `gate-news-briefing` |
| “关于链上数据的情况如何？” | `gate-info-tokenonchain` |
| “这种加密货币安全吗？” | `gate-info-riskcheck` |
| “比较XX和YY” | `gate-info-coincompare` |
| “为什么价格在波动？” | `gate-news-eventexplain` |

---

## 安全规则

1. **禁止提供投资建议**：整体评估结果基于数据驱动，必须包含“本报告不构成投资建议”的免责声明。
2. **禁止预测价格**：不得输出具体的目标价格或涨跌预测。
3. **数据透明度**：明确标注每个数据来源及其更新时间。
4. **处理缺失数据**：当某个数据维度缺失时，必须如实告知用户——严禁伪造数据。