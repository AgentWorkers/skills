---
name: trade-signal
version: 1.0.2
description: 实时交易信号，提供可执行的买入/卖出/持有建议，适用于股票交易决策、股票分析、技术分析、买卖建议、盈利策略、价格目标、分析师评级、入场/出场点、投资组合再平衡等需要具体操作建议的场合。支持美国及全球市场、亚洲新兴市场、个股、交易型开放式指数基金（ETFs）和期权策略。
homepage: https://terminal-x.ai
metadata: {"category":"finance","api_base":"https://app.terminal-x.ai/api"}
---

# 交易信号

为AI代理提供买入/卖出/持有交易建议。将复杂的市场情报转化为关于全球股票及其他公开证券的清晰、可执行的买入/卖出/持有建议。该服务会为特定证券提供具体的价格目标、实时数据以及机构级别的交易分析。虽然该服务具有前瞻性，但也能对当前或历史的价格走势进行技术分析和基本面分析，并对证券价格变动的原因给出定性和定量的解释。

## 快速入门

```bash
# Get trade signal for a stock
./scripts/search.sh "Should I buy NVDA?"

# Get signal with full analysis
./scripts/search.sh "Is AAPL a sell at current levels?"

# Check multiple tickers
./scripts/search.sh "AAPL NVDA TSLA MSFT"

# Earnings play analysis
./scripts/search.sh "What's the best trade ahead of NVDA's upcoming earnings? Give me specific options strategy with prices."
```

**基础URL:** `https://app.terminal-x.ai/api`

---

## 功能

### 📊 交易信号功能

| 查询类型 | 示例 |
|------------|----------|
| **交易决策** | 买入/卖出/持有建议、入场/出场时机、持仓规模 |
| **收益预测** | 盈利预发布前的布局、盈利发布后的反应、历史模式 |
| **价格驱动因素** | 影响股价的因素、宏观经济事件、技术指标 |
| **分析师观点** | 评级上调/下调、价格目标调整、投资观点 |
| **技术分析** | 支撑/阻力位、波动性、动量指标 |
| **风险评估** | 止损水平、下行风险、风险/回报分析 |

#### 每条回复包含：

- **信号**：明确的买入/卖出/持有/避免交易的建议，以及时间范围（T+1、T+5等） |
- **技术分析**：入场、出场、止损位以及支撑/阻力区 |
- **原因分析**：推动交易决策的宏观经济、技术及市场情绪因素 |
- **证券代码**：主要证券代码及相关ETF和关联金融产品 |
- **数据来源**：引用编号[1]、[2]、[3]，链接至华尔街研究、SEC文件和市场数据

### 📈 市场覆盖范围

**涵盖37,565只全球股票和6,104只ETF，覆盖所有主要交易所：**

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

- **华尔街研究** — 高盛、摩根士丹利、JP摩根、花旗、UBS、美国银行、Stifel等机构的分析师报告和投资观点 |
- **分析师观点**：评级上调/下调、新研报发布、价格目标调整 |
- **SEC文件**：10-K年报、10-Q季度报告、8-K临时报告、内幕交易信息、13F年度报告、13D季度报告、DEF14A文件等，均可在EDGAR平台上获取 |
- **会议记录**：财报电话会议、并购电话会议、管理层讨论会、投资者日会议的实时记录 |
- **实时新闻**：彭博社、路透社、CNBC、FT、WSJ等媒体 |
- **公司文件**：公司新闻稿、财报、公司演示文稿、投资者日活动资料、财务报告等

---

## 回复格式

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
  "agentAnswer": "**Hold current position: Sell at $185-190 on any post-earnings bounce within T+1 to T+3.**
  NVDA closed at $181.36 and trades at $180.88 after hours. Despite consistent earnings beats since August 2024, 
  the stock has exhibited a persistent sell-the-fact pattern, declining in 4 of the last 5 post-earnings sessions. [1]
  
  Options markets price a 6.68% implied move ($12.13 swing) for the November 19 after-hours release. [2]",
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
| `tradeSignal` | 买入/卖出/持有建议 |
| `priceTarget` | 入场价格、出场价格、止损价格、时间范围 |
| `agentAnswer` | 基于AI的分析结果及引用来源[1]、[2] |
| `sources` | 引用的标题、来源名称及日期 |
| `technicals` | 相关技术指标（RSI、MACD、支撑/阻力位、趋势分析） |
| `relatedAnalysis` | 相关研究主题 |

---

## 示例输出

### 示例1：基于驱动因素的分析及交易建议
**查询：** `./scripts/search.sh "是什么导致了白银价格的下跌？请为明天制定交易策略。"`

```
📊 **Silver Price Decline: Catalyst Analysis**

**Signal: AVOID** | Time Horizon: T+1
Related: SLV (-28.54%), SI (-0.77%), XAGUSD (+2.58%)

Silver has entered bear market territory after falling nearly 22% from its
recent record high, driven by a confluence of macro and technical factors. [1][2]

**Macro Catalysts:**
- President Trump's announcement of Kevin Warsh as Fed pick eased concerns
  about Fed independence, triggering a sharp dollar rally [7][10]
- Repricing underway with assumption that smaller Fed balance sheet would
  tighten financial conditions [8]
- Declining capital leakage from China — more capital returning to China,
  affecting precious metals where sentiment is currently driving prices [7][9]

**Technical Catalysts:**
- Parabolic run with 14% intraday surge showed clear blowoff top pattern [1][9]
- One-month volatility surged above 96%, steepest level in nearly 25 years [7][10][12]
- Inverted volatility curve signals traders anticipate further unwinding [7][10][12]
- CME raised margin requirements to 11% from 9% — familiar late-cycle signal
  that speculative excess is being wrung out [5][8][13]

**Valuation:**
Current price ($86.62) trades significantly above 200-day MA of $48/oz,
indicating deeply overbought conditions. Analysts estimate fair value
around $60/oz. JPMorgan's Marko Kolanovic suggests silver should trade
at half its current price later in 2026. [14][16][18][20][21][22][23]

**Trade Decision:**
Avoid purchasing silver for tomorrow. Market likely to continue unwinding
speculative positions. Wait for stabilization at $75-$80 support zone
before considering new long positions. [3][11]

**Sources:**
[1] Bloomberg News: Silver Bear Market Entry 
[2] Goldman Sachs Precious Metals Weekly Report
[7] Bloomberg Terminal — Silver Volatility Analysis
[10] Reuters — Fed Policy Impact on Dollar
[16] JPMorgan Research Note — Precious Metals Outlook
[21] CME Group — Margin Requirement Update
```

### 示例2：买入/卖出建议及价格目标
**查询：** `./scripts/search.sh "请给出一个明确的买入/卖出/持有建议，并提供T+5的时间范围内的目标价格。"`

```
📊 **Silver Trade Signal: 5-Day Outlook**

**Signal: HOLD** | Target Range: $80-$90 | Time Horizon: T+5

Silver has experienced extreme volatility with current price at $86.31,
following intraday high of $88.00 and low of $77.00 today. [1]

**Technical Summary:**
- 1-Month Volatility: >96% (extreme)
- Volatility Curve: Steeply inverted — traders anticipate further unwinding [5]
- Gold/Silver Ratio: Below 50 (stretched outperformance vs gold) [7][17]
- Support: $83-$85 (larger retracement) | Resistance: $93.50-$96.00 [9]

**Historical Pattern:**
In six prior instances since 1970 where silver doubled in 40 days and rose
over 10% in a single day, prices were lower 20 days later. This suggests
caution, but immediate sustained crashes are not guaranteed. [16]

**Bullish Factors (Long-term):**
- Structural supply deficit from solar, EVs, and data centers [7][3]
- Physical demand from China and India remains strong [1][5][8]
- Shanghai silver futures trading at premium to global spot [1][5][8]

**Bearish Factors (Short-term):**
- CME margin hike to 11% forcing speculative liquidation [10]
- Risk-reward completely skewed at current levels [14][11]
- "Meme trader" phenomenon contributing to volatility [9]

**Trade Decision:**
HOLD for next 5 trading days. Consolidation phase likely after correction
from peak near $120.60. Target $80-$90 reflects stabilization period with
potential for minor upward corrections within volatile environment.

**Sources:**
[1] Silver Spot Market Data — February 1, 2026
[5] CME Group — Volatility Curve Analysis
[7] Bloomberg — Gold/Silver Ratio Report
[9] Reuters — Silver Market Dynamics
[14] Bank of America — Precious Metals Valuation
[16] Historical Precious Metals Database — Pattern Analysis

```

### 示例3：分析师观点
**查询：** `./scripts/search.sh "分析师对NVIDIA的看法是什么？"`

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

当代理被问及以下问题时，会自动使用此功能：
- “我应该买入NVDA吗？”
- “你对AAPL有什么看法？”
- “应该卖出还是持有TSLA？”
- “请为META股票提供一个交易建议。”
- “现在买入AMD合适吗？”
- “在财报发布前分析GOOGL的情况。”
- “分析师对MSFT有什么评价？”
- “目前最适合购买的科技股有哪些？”

### 代理使用流程示例

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

| 推荐做法 | 不推荐的做法 |
|---------|----------|
| 使用具体信息** | 只使用通用词汇 |
| 使用证券代码** | 例如使用“AAPL”而非“Apple” |
| 提出明确问题** | 例如“AAPL的毛利率与MSFT相比如何？” |
| 提供背景信息** | 例如“上个季度”、“2024财年”、“同比” |

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

## 帮助支持

- **官网：** https://terminal-x.ai |
- **邮箱：** hello@terminal-x.ai