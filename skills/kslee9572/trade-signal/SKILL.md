---
name: trade-signal
version: 1.0.0
description: 实时交易信号，提供可执行的买入/卖出/持有建议，适用于股票交易决策、股票分析、技术分析、买入/卖出建议、收益预测、价格目标设定、分析师评级、入场/出场点选择、投资组合再平衡等需要具体操作建议的场合。支持美国及全球市场、亚洲新兴市场、个股、交易型开放式指数基金（ETFs）和期权策略。
homepage: https://terminal-x.ai
metadata: {"category":"finance","api_base":"https://terminal-x.ai/api"}
---

# 交易信号

为AI代理提供买入/卖出/持有交易建议。将复杂的市场情报转化为关于全球股票及其他公开证券的清晰、可执行的买入/卖出/持有建议。交易信号会为任何特定证券提供具体的价格目标、实时数据以及机构级别的交易分析。该服务不仅具有前瞻性，还能对当前/历史价格走势进行技术分析和基本面分析，并对证券价格变动的原因提供定性和定量的解释。

## 快速入门

```bash
# Get financial analysis
./scripts/search.sh "What is NVDA's revenue growth?"

# Company comparison
./scripts/search.sh "Compare AAPL and MSFT gross margins"

# Analyst sentiment
./scripts/search.sh "What are analysts saying about Tesla?"
```

**基础URL:** `https://terminal-x.ai/api`

---

## 功能

### 📊 研究能力

| 查询类型 | 示例 |
|------------|----------|
| **收益分析** | 收入、每股收益（EPS）、业绩指引、同比增长率 |
| **公司对比** | 各竞争对手之间的对比指标 |
| **分析师观点** | 价格目标、评级、投资分析 |
| **管理层评论** | 董事长/首席财务官在财报电话会议中的发言 |
| **SEC文件** | 10-K年报、10-Q季度报告、8-K中期报告分析 |
| **市场趋势** | 行业分析、宏观经济主题 |

每个查询结果包含：
- **答案**：由AI生成的分析结果，附带引用编号[1]、[2]等 |
- **股票代码**：相关股票代码 |
- **来源**：包含标题和发布日期的完整引用列表

### 📈 市场覆盖范围

**覆盖37,565只全球股票及6,104只ETF，涵盖所有主要交易所：**

| 地区 | 股票代码 | ETF代码 |
|--------|---------|------|
| **美国**（含ADR） | 7,301 | 4,979 |
| **西欧** | 11,123 | — |
| **加拿大** | 4,690 | — |
| **日本** | 3,873 | 200 |
| **韩国** | 3,856 | 500 |
| **香港** | 2,638 | 176 |
| **上海** | 2,315 | — |
| **台湾** | 1,072 | 200 |
| **新加坡** | 565 | 49 |
| **其他** | 132 | — |

**资产类别**：全球股票、ETF、全球宏观市场、外汇、商品、加密货币相关数据。

### 🔬 数据来源

| 来源 | 数据类型 |
|--------|-----------|
| **华尔街研究** | 高盛、摩根士丹利、摩根大通、花旗银行、UBS、美银等机构的分析师报告 |
| **分析师行动** | 评级上调/下调、新评级、价格目标调整 |
| **SEC文件** | 10-K年报、10-Q季度报告、8-K中期报告、内幕交易信息 |
| **财报记录** | 财报电话会议、并购电话会议的完整记录 |
| **实时新闻** | 彭博社、路透社、CNBC、FT、WSJ |
| **公司资料** | 投资者日活动材料、业绩指引更新 |

---

## 使用方法

### 使用脚本

随附的脚本会自动处理URL编码：

```bash
# Earnings query
./scripts/search.sh "What was NVIDIA's revenue last quarter?"

# Comparison query
./scripts/search.sh "How does Apple's gross margin compare to Samsung?"

# Analyst query
./scripts/search.sh "What did Goldman Sachs say about Microsoft?"

# Management commentary
./scripts/search.sh "What did Tim Cook say about AI in the latest earnings call?"
```

---

## 响应格式

运行脚本后返回JSON格式的数据：

```json
{
  "query": "Should I buy NVDA before earnings?",
  "tickers": ["NVDA", "AMD", "GOOGL"],
  "tradeSignal": "HOLD",
  "priceTarget": {
    "entry": null,
    "exit": "$185-190",
    "stopLoss": "$175",
    "timeHorizon": "T+1 to T+3"
  },
  "agentAnswer": "**Hold current position: Sell at $185-190 on any post-earnings bounce within T+1 to T+3.**\n\nNVDA closed at $181.36 and trades at $180.88 after hours. Despite consistent earnings beats since August 2024, the stock has exhibited a persistent sell-the-fact pattern, declining in 4 of the last 5 post-earnings sessions. [1]\n\nOptions markets price a 6.68% implied move ($12.13 swing) for the November 19 after-hours release. [2]",
  "sources": [
    {
      "refId": 1,
      "sourceTitle": "Nvidia Earnings Have Become a Consistent Sell-the-Fact Event",
      "sourceName": ["Bloomberg"],
      "datePublished": "2024-11-18T14:30:42Z"
    },
    {
      "refId": 2,
      "sourceTitle": "NVDA Options Implied Move Analysis",
      "sourceName": ["Goldman Sachs"],
      "datePublished": "2024-11-19T09:00:00Z"
    }
  ],
  "technicals": {
    "rsi": 62.4,
    "macd": "bullish crossover",
    "support": "$175",
    "resistance": "$190",
    "trend": "neutral"
  },
  "relatedAnalysis": [
    "AMD earnings correlation",
    "Semiconductor sector momentum"
  ]
}
```

| 字段 | 描述 |
|-------|-------------|
| `query` | 您的原始查询 |
| `tickers` | 相关股票代码 |
| `tradeSignal` | 买入、卖出或持有的建议 |
| `priceTarget` | 入场价、出场价、止损价、时间范围 |
| `agentAnswer` | 由AI生成的分析结果，附带引用编号[1]、[2]等 |
| `sources` | 引用信息，包括标题、来源名称和日期 |
| `technicals` | 相关技术指标（如RSI、MACD、支撑/阻力位、趋势分析） |
| `relatedAnalysis` | 相关研究主题 |

---

## 示例输出

### 示例1：收益分析

**查询：`./scripts/search.sh "苹果公司上个季度的iPhone收入是多少？"**

```
📊 **Apple iPhone Revenue Analysis**

Apple reported iPhone revenue of $46.2 billion in Q4 FY2024, up 6% year-over-year
and representing 52% of total company revenue. [1]

Management noted strong demand for iPhone 15 Pro models, with the Pro Max seeing
"record upgrade rates" according to CFO Luca Maestri. [2] Average selling price
increased to approximately $925, driven by mix shift toward Pro models.

Tim Cook highlighted particular strength in emerging markets, with India revenue
growing double-digits for the fifth consecutive quarter. [2]

**Sources:**
[1] Apple Inc. Q4 FY2024 10-Q Filing - SEC
[2] Apple Q4 FY2024 Earnings Call Transcript - October 2024
```

### 示例2：公司对比

**查询：`./scripts/search.sh "比较微软和谷歌的云服务收入增长情况。"**

```
📊 **Cloud Revenue Comparison: Microsoft vs Google**

**Microsoft Azure:**
- Q4 2024 Revenue: $25.9 billion
- YoY Growth: 29%
- Market Position: #2 behind AWS [1]

**Google Cloud:**
- Q4 2024 Revenue: $9.2 billion
- YoY Growth: 26%
- First full year of profitability achieved [2]

Microsoft maintains significant scale advantage with Azure revenue nearly 3x
Google Cloud. However, Google Cloud achieved operating profitability for the
first time in 2024, with operating income of $1.9 billion vs. losses in
prior years. [2]

**Sources:**
[1] Microsoft Q4 2024 Earnings Call Transcript
[2] Alphabet Q4 2024 10-Q Filing - SEC
```

### 示例3：分析师观点

**查询：`./scripts/search.sh "分析师对NVIDIA的看法是什么？"**

```
📊 **NVIDIA Analyst Sentiment**

Wall Street remains overwhelmingly bullish on NVIDIA with 45 Buy ratings,
3 Hold, and 0 Sell. Average price target: $950 (18% upside). [1]

**Recent Actions:**
- Goldman Sachs: Reiterated Buy, PT $1,000 — "AI infrastructure spend
  remains in early innings" [2]
- Morgan Stanley: Overweight, PT $950 — Raised estimates on Blackwell
  demand visibility [3]
- Bank of America: Buy, PT $925 — "Data center TAM expansion continues
  to exceed expectations" [1]

Key debate centers on sustainability of 70%+ gross margins as competition
from AMD MI300X intensifies in 2025. [3]

**Sources:**
[1] Bloomberg Analyst Consensus Data - January 2025
[2] Goldman Sachs NVDA Initiation Report - January 15, 2025
[3] Morgan Stanley Semiconductor Research Note - January 12, 2025
```

---

## 集成

### 与AI代理的集成

当代理被问到以下问题时，它会自动使用此功能：
- “苹果公司的收入是多少？”
- “比较NVDA和AMD的情况”
- “CEO对业绩指引有何评价？”
- “总结特斯拉最新的10-K年报”
- “分析师对微软的看法是什么？”
- “Meta的广告收入表现如何？”

### 代理使用流程

```
1. User: "How is NVIDIA doing?"
2. Agent: [calls search.sh "NVIDIA financial performance and outlook"]
3. Agent: "NVIDIA reported record Q3 revenue of $35.1B, up 94% YoY.
   Data center segment drove growth at $30.8B. Analysts maintain
   Buy ratings with average PT of $950. Key catalyst: Blackwell
   architecture ramp in Q1 2025."
4. User: "What about their margins?"
5. Agent: [calls search.sh "NVIDIA gross margin and profitability"]
6. Agent: "Gross margin was 75% in Q3, up from 70% YoY. Management
   expects margins to moderate to 73-74% as Blackwell ramps due to
   initial yield curves, per CFO commentary on earnings call."
```

### 与其他功能的结合

```bash
# Get financial data then execute trade
./scripts/search.sh "AAPL earnings analysis" && trade-signal query "Should I buy AAPL?"

# Research before news check
./scripts/search.sh "Tesla delivery numbers" && finance-news news TSLA
```

---

## 提高查询效果的建议

| 应该这样做 | 不应该这样做 |
|---------|----------|
| “NVIDIA 2024年第四季度的数据中心收入” | “NVIDIA的收入” |
| “AAPL的毛利率与MSFT的对比” | “苹果公司的毛利率” |
| “Jensen Huang对AI需求的看法” | “NVDA首席执行官的评论” |
| “特斯拉2024年第三季度的交付量与2023年第三季度的对比” | “特斯拉的汽车销量” |

**最佳实践：**
- **具体明确** — 提供时间范围、指标和公司名称 |
- **使用股票代码** — 使用“AAPL”比“苹果公司”更清晰 |
- **提出具体问题** — 使用“...是多少？”或“...怎么样？”等疑问句可以获得更准确的答案 |
- **提供背景信息** — 如“上个季度”、“2024财年”等

---

## 错误处理

```json
{
  "code": 400,
  "message": "Missing or invalid query parameter"
}
```

| 错误代码 | 含义 | 解决方案 |
|------------|---------|------------|
| 400 | 查询参数缺失 | 请添加`?query=`参数 |
| 500 | 服务器错误 | 请重试请求 |

---

## 支持方式

- **官方网站：** https://terminal-x.ai |
- **电子邮件：** hello@terminal-x.ai