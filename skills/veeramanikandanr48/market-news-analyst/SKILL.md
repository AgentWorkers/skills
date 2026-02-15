---
name: market-news-analyst
description: 此技能适用于分析近期影响市场走势的新闻事件及其对股票市场和大宗商品的影响。当用户请求分析过去10天内的重大财经新闻、了解市场对货币政策决策（如FOMC、ECB、BOJ）的反应、评估地缘政治事件对大宗商品的影响，或需要全面审查大盘股公司的收益公告时，可使用该技能。该技能会利用WebSearch/WebFetch工具自动收集新闻，并生成按影响程度排序的分析报告。所有的分析过程及输出结果均以英文形式呈现。
---

# 市场新闻分析师

## 概述

该技能能够全面分析过去10天内影响市场走势的新闻事件，重点关注这些事件对美国股市和商品市场的影响。该技能利用WebSearch和WebFetch工具自动从可信来源收集新闻，评估市场影响的程度，分析实际的市场反应，并生成按市场影响重要性排序的结构化英文报告。

## 何时使用此技能

在以下情况下使用此技能：
- 用户请求分析最近的重大市场新闻（过去10天内）
- 用户希望了解市场对特定事件（如联邦公开市场委员会（FOMC）决策、企业收益、地缘政治事件）的反应
- 用户需要包含影响评估的市场新闻摘要
- 用户询问新闻事件与商品价格走势之间的相关性
- 用户请求分析央行政策公告对市场的影响

**示例用户请求：**
- “分析过去10天的主要市场新闻”
- “最新的FOMC决策对市场产生了什么影响？”
- “本周最重要的市场事件有哪些？”
- “分析最近的地缘政治新闻及其对商品价格的影响”
- “回顾大型科技公司的收益及其对市场的影响”

## 分析工作流程

分析市场新闻时，请遵循以下六个步骤的结构化流程：

### 第一步：通过WebSearch/WebFetch收集新闻

**目标：**收集过去10天内影响市场走势的重大新闻。

**搜索策略：**

执行并行WebSearch查询，涵盖不同的新闻类别：

**货币政策：**
- 搜索：过去10天的FOMC会议、联邦储备系统利率、欧洲央行（ECB）政策决策、日本银行（BOJ）的决策
- 目标：央行决策、前瞻性指导变化、通胀评论

**通胀/经济数据：**
- 搜索：[当前月份]的CPI通胀报告、非农就业数据（NFP）、GDP数据、生产者价格指数（PPI）
- 目标：主要的经济数据发布和意外情况

**大型科技公司收益：**
- 搜索：[当前季度]的苹果公司（Apple）收益、微软（Microsoft）收益、英伟达（NVIDIA）收益、亚马逊（Amazon）收益、Meta收益、谷歌（Google）收益
- 目标：最大公司的收益结果、市场反应

**地缘政治事件：**
- 搜索：中东冲突对油价的影响、乌克兰战争、美中紧张关系、贸易战关税
- 目标：影响市场的冲突、制裁、贸易争端

**商品市场：**
- 搜索：上周的油价新闻、黄金价格、欧佩克（OPEC）会议、天然气价格、铜价
- 目标：供应中断、需求变化、价格走势

**企业新闻：**
- 搜索：重大并购公告、银行收益、科技行业新闻、破产、信用评级下调
- 目标：超出大型科技公司范围的重大企业事件

**推荐的新闻来源（优先顺序）：**
1. 官方来源：FederalReserve.gov、SEC.gov（EDGAR）、Treasury.gov、BLS.gov
2. 一级财经新闻：彭博社（Bloomberg）、路透社（Reuters）、《华尔街日报》（Wall Street Journal）、《金融时报》（Financial Times）
3. 专业来源：CNBC（实时）、MarketWatch（摘要）、S&P Global Platts（商品市场）

**搜索执行：**
- 使用WebSearch进行广泛的主题搜索
- 使用WebFetch从官方来源或主要新闻媒体获取具体URL
- 收集发布日期，确保新闻在10天时间范围内
- 记录：事件日期、来源、标题、关键细节、市场背景（盘前、交易时间、盘后）

**筛选标准：**
- 重点关注一级市场事件（参见references/market_event_patterns.md）
- 优先考虑具有明显市场影响的新闻（价格波动、成交量激增）
- 排除：特定股票的小盘股新闻、次要产品更新、常规文件

在整个收集过程中，使用英文思考。为每条重要新闻记录以下信息：
- 日期和时间
- 事件类型（货币政策、收益、地缘政治等）
- 来源可靠性等级
- 初始市场反应（如果可观察）

### 第二步：加载知识库参考资料

**目标：**利用领域专业知识来评估新闻影响。

根据收集到的新闻类型，加载相关的参考文件：

**始终加载：**
- `references/market_event_patterns.md` - 所有主要事件类型的综合模式
- `references/trusted_news_sources.md` - 来源可信度评估

**根据收集到的新闻有条件加载：**

如果找到**货币政策新闻**：
- 重点关注：market_event_patterns.md中的“央行货币政策事件”部分
- 关键框架：加息/降息的反应、量化宽松（QE）/量化紧缩（QT）的影响、鹰派/鸽派立场

如果找到**地缘政治事件**：
- 加载：`references/geopolitical_commodity_correlations.md`
- 重点关注：能源商品、贵金属、与事件相匹配的区域框架

如果找到**大型科技公司收益**：
- 加载：`references/corporate_news_impact.md`
- 重点关注：特定公司部分、行业传染模式

如果找到**商品新闻**：
- 加载：`references/geopolitical_commodity_correlations.md`
- 重点关注：特定商品部分（石油、黄金、铜等）

**知识整合：**
将收集到的新闻与历史模式进行比较，以：
- 预测预期的市场反应
- 识别异常情况（市场反应与历史模式不同）
- 评估反应是典型的幅度还是超常的
- 确定是否如预期发生了传染效应

### 第三步：影响程度评估

**目标：**按市场影响的重要性对每个新闻事件进行排名。

**影响评估框架：**

对于每条新闻，从三个维度进行评估：

**1. 资产价格影响（主要因素）：**

衡量实际或预期的价格变动：

**股市：**
- 指数层面：标准普尔500指数（S&P 500）、纳斯达克100指数（Nasdaq 100）、道琼斯指数（Dow Jones）
  - 严重：当日±2%以上
  - 重大：±1-2%
  - 中等：±0.5-1%
  - 轻微：±0.2-0.5%
  - 可忽略：<0.2%

- 行业层面：特定行业ETF
  - 严重：±5%以上
  - 重大：±3-5%
  - 中等：±1-3%
  - 轻微：<1%

- 特定股票：大型科技公司
  - 严重：±10%以上（且指数权重导致指数变动）
  - 重大：±5-10%
  - 中等：±2-5%

**商品市场：**
- 石油（WTI/Brent）：
  - 严重：±5%以上
  - 重大：±3-5%
  - 中等：±1-3%

- 黄金：
  - 严重：±3%以上
  - 重大：±1.5-3%
  - 中等：±0.5-1.5%

- 基础金属（铜等）：
  - 严重：±4%以上
  - 重大：±2-4%
  - 中等：±1-2%

**债券市场：**
- 10年期国债收益率：
  - 严重：当日±20个基点（bps）以上
  - 重大：±10-20个基点
  - 中等：±5-10个基点

**货币市场：**
- 美元指数（DXY）：
  - 严重：±1.5%以上
  - 重大：±0.75-1.5%
  - 中等：±0.3-0.75%

**2. 影响范围（乘数）：**

评估影响的市场/行业数量：

- **系统性（3倍乘数）：**多个资产类别、全球市场
  - 例子：FOMC意外决策、银行危机、重大战争爆发

- **跨资产（2倍乘数）：**股票 + 商品，或股票 + 债券
  - 例子：通胀意外、地缘政治供应冲击

- **行业广泛（1.5倍乘数）：**整个行业或相关行业
  - 例子：科技行业收益集中、能源政策公告

- **特定股票（1倍乘数）：**单一公司（除非是具有指数影响力的大型科技公司）
  - 例子：个别公司收益、并购

**3. 前瞻性意义（修正因子）：**

考虑未来的影响：

- **制度变革（+50%）：**根本性的市场结构变化
  - 例子：美联储从加息转向降息、重大地缘政治重新调整

- **趋势确认（+25%）：**强化现有趋势
  - 例子：连续强劲的通胀数据、持续的收益超出预期

- **孤立事件（0%）：**一次性事件，未来信号有限
  - 例子：数据点在范围内、公司特定问题

**影响得分计算：**

```
Impact Score = (Price Impact Score × Breadth Multiplier) + Forward-Looking Modifier

Price Impact Score:
- Severe: 10 points
- Major: 7 points
- Moderate: 4 points
- Minor: 2 points
- Negligible: 1 point
```

**示例计算：**

**FOMC加息75个基点（鹰派立场）：**
- 价格影响：标准普尔500指数下跌2.5%（严重 = 10分）
- 影响范围：系统性（股票、债券、美元、商品均受到影响）= 3倍
- 前瞻性：趋势确认（持续紧缩）= +25%
- **得分：（10 × 3）× 1.25 = 37.5**

**英伟达收益超出预期：**
- 价格影响：英伟达股价上涨15%，纳斯达克指数上涨1.5%（严重 = 10分）
- 影响范围：行业广泛（半导体、科技行业）= 1.5倍
- 前瞻性：趋势确认（人工智能需求）= +25%
- **得分：（10 × 1.5）× 1.25 = 18.75**

**地缘政治事件爆发（中东）：**
- 价格影响：油价上涨8%，标准普尔指数下跌1.2%（严重 = 10分）
- 影响范围：跨资产（石油、股票、黄金）= 2倍
- 前瞻性：孤立事件（无进一步升级）= 0%
- **得分：（10 × 2）× 1.0 = 20**

**单一股票收益（非大型科技公司）：**
- 价格影响：股票价格上涨12%，无指数影响（重大 = 7分）
- 影响范围：特定股票 = 1倍
- 前瞻性：孤立事件 = 0%
- **得分：（7 × 1）× 1.0 = 7**

**排名：**
对所有新闻事件进行评分后，按影响得分从高到低排序。这决定了报告的顺序。

### 第四步：市场反应分析

**目标：**分析市场对这些事件的真实反应。

对于每个影响得分大于5的新闻事件，进行详细的反应分析：

**即时反应（盘中）：**
- 方向：正面、负面、混合
- 幅度：与价格影响类别一致
- 时间：盘前、盘中、盘后
- 波动性：VIX指数变动、买卖价差

**多资产反应：**

**股票：**
- 指数表现（标准普尔500指数、纳斯达克100指数、道琼斯指数、罗素2000指数）
- 行业轮动（哪些行业表现优异/不佳）
- 个别股票走势（大型科技公司、相关公司）
- 成长股与价值股、大盘股与小盘股的差异

**固定收益：**
- 国债收益率（2年期、10年期、30年期）
- 收益曲线形态（陡峭化、平坦化、倒挂）
- 信用利差（投资级债券与高收益债券）
- TIPS收益率曲线（通胀预期）

**商品：**
- 能源：原油（WTI、布伦特）、天然气
- 贵金属：黄金、白银
- 基础金属：铜、铝（如相关）
- 农产品：小麦、玉米、大豆（如相关）

**货币：**
- 美元指数（DXY）
- 欧元/美元、美元/日元、英镑/美元
- 新兴市场货币
- 安全避险货币（日元、瑞士法郎）

**衍生品：**
- VIX指数（波动率指数）
- 期权活动（看跌/看涨比率、异常成交量）
- 期货头寸

**模式比较：**

将观察到的反应与知识库中的预期模式进行比较：

- **一致：**反应与历史模式相符
  - 例子：美联储加息 → 科技股下跌，美元上涨（符合预期）

- **放大：**反应超出典型模式
  - 例子：通胀数据超出预期0.3% → 卖盘幅度是典型的两倍
  - 调查：头寸、市场情绪、累积因素

- **减弱：**反应低于历史模式
  - 例子：地缘政治事件 → 石油价格几乎没有变动
  - 调查：是否已经计入价格，其他抵消因素

- **相反：**反应与历史模式相反
  - 例子：好消息被市场忽视，坏消息导致价格上涨
  - 调查：“好消息是坏消息”的动态、市场对美联储转向的预期

**异常情况识别：**

标记与模式显著偏离的反应：
- 市场对通常影响市场走势的新闻无动于衷
- 对通常不重要的新闻过度反应
- 传染效应未能如预期扩散
- 安全避险货币未起作用（相关性失效）

**情绪指标：**

- 风险偏好（风险上升 vs 风险下降）：哪种情况占主导
- 头寸情况：拥挤交易的解除证据
- 动量：后续交易中的延续或反转

### 第五步：相关性和因果关系评估

**目标：**区分直接影响和巧合的时间安排。

**多事件分析：**

当10天内发生多个重大事件时，评估它们之间的相互作用：

**强化事件：**
- 同方向的影响
  - 例子：鹰派FOMC决策 + 强劲的CPI → 股市普遍下跌

**抵消事件：**
- 相反方向的影响
  - 例子：强劲的收益（正面）+ 地缘政治紧张（负面）→ 总体反应减弱

**连续事件：**
- 一个事件为下一个事件创造了反应
  - 例子：第一次加息反应温和，第二次加息反应严重（累积紧缩担忧）

**巧合的时间：**
- 事件无关但同时发生
  - 难以单独评估每个事件的影响
  - 注意归因的不确定性

**地缘政治-商品相关性：**

对于地缘政治事件，使用geopolitical_commodity_correlations.md具体分析商品市场反应：

**能源：**
- 将冲突/制裁与供应中断风险联系起来
- 评估实际影响与预期影响
- 持续时间：短暂飙升还是持续上升

**贵金属：**
- 安全避险资金流动与实际利率驱动因素
- 黄金对风险规避事件的反应
- 中央银行购买的影响

**工业金属：**
- 经济放缓担忧导致的供应破坏
- 供应链中断
- 中国因素对铜、铝的影响

**农产品：**
- 黑海粮食出口（俄罗斯-乌克兰）
- 天气因素
- 粮食安全政策反应

**传递机制：**

追踪新闻如何通过市场传递：

**直接渠道：**
- 新闻 → 立即的资产价格反应
  - 例子：欧佩克减产 → 石油价格立即上涨

**间接渠道：**
- 新闻 → 经济影响 → 资产价格
  - 例子：加息 → 抵押贷款利率上升 → 房地产市场放缓 → 房屋建筑商股票下跌

**情绪渠道：**
- 新闻 → 风险偏好变化 → 资产重新配置
  - 例子：银行危机 → 投资者转向优质资产 → 国债上涨，股票下跌

**反馈循环：**
- 初始反应产生次级效应
  - 例子：股票抛售 → 追加保证金要求 → 强制性抛售 → 更深的抛售

### 第六步：报告生成

**目标：**创建按市场影响排序的结构化英文Markdown报告。

**报告结构：**

```markdown
# Market News Analysis Report - [Date Range]

## Executive Summary

[3-4 sentences covering:]
- Period analyzed (specific dates)
- Number of significant events identified
- Dominant market theme/regime (risk-on/risk-off, sector rotation)
- Top 1-2 highest-impact events

## Market Impact Rankings

[Table format, sorted by Impact Score descending]

| Rank | Event | Date | Impact Score | Asset Classes Affected | Market Reaction |
|------|-------|------|--------------|------------------------|-----------------|
| 1 | [Event] | [Date] | [Score] | [Equities, Commodities, etc.] | [Brief reaction] |
| 2 | ... | ... | ... | ... | ... |

---

## Detailed Event Analysis

[For each event in rank order, provide comprehensive analysis]

### [Rank]. [Event Name] (Impact Score: [X])

**Event Date:** [Date, Time]
**Event Type:** [Monetary Policy / Earnings / Geopolitical / Economic Data / Corporate]
**News Source:** [Source, with credibility tier]

#### Event Summary
[3-4 sentences describing what happened]
- Key details (e.g., rate decision, earnings beat/miss magnitude, conflict developments)
- Context (was this expected, surprise factor)
- Forward guidance or implications stated

#### Market Reaction

**Immediate (Day-of):**
- **Equities:** S&P 500 [+/-X%], Nasdaq [+/-X%], Sector rotation [details]
- **Bonds:** 10Y yield [change], credit spreads [movement]
- **Commodities:** Oil [+/-X%], Gold [+/-X%], Copper [+/-X%] (if relevant)
- **Currencies:** USD [+/-X%], [other relevant pairs]
- **Volatility:** VIX [level/change]

**Follow-Through (Subsequent Sessions):**
- [Direction: sustained, reversed, or consolidated]
- [Additional price action details if significant]

**Pattern Comparison:**
- **Expected Reaction:** [Based on historical patterns from knowledge base]
- **Actual vs Expected:** [Consistent / Amplified / Dampened / Inverse]
- **Explanation of Deviation:** [If applicable, why reaction differed]

#### Impact Assessment Detail

**Asset Price Impact:** [Severe/Major/Moderate/Minor] - [Justification]
**Breadth:** [Systemic/Cross-Asset/Sector/Stock-Specific] - [Affected markets]
**Forward Significance:** [Regime Change/Trend Confirmation/Isolated/Contrary] - [Rationale]

**Calculated Score:** ([Price Score] × [Breadth Multiplier]) × [Forward Modifier] = [Total]

#### Sector-Specific Impacts

[If relevant, detail which sectors/industries were most affected]
- [Sector 1]: [Impact and reason]
- [Sector 2]: [Impact and reason]
- [Example: Technology -3% (rate sensitivity), Energy +5% (oil price spillover)]

#### Geopolitical-Commodity Correlation Analysis

[Include this section only for geopolitical events]
- [Specific commodity affected]: [Price movement]
- [Supply/demand mechanism]: [Explanation]
- [Historical precedent]: [Comparison to similar past events]
- [Expected duration]: [Temporary shock vs sustained impact]

[Repeat detailed analysis for each ranked event]

---

## Thematic Synthesis

### Dominant Market Narrative
[Identify overarching theme across the 10-day period]
- [E.g., "Persistent inflation concerns dominated despite mixed economic data"]
- [E.g., "Tech sector strength drove markets higher despite geopolitical headwinds"]

### Interconnected Events
[Analyze how events related or compounded]
- [Event A] + [Event B] → [Combined impact analysis]
- [Sequential causation if applicable]

### Market Regime Assessment
**Risk Appetite:** [Risk-On / Risk-Off / Mixed]
**Evidence:**
- [Supporting indicators: sector performance, safe haven flows, credit spreads, VIX]

**Sector Rotation Trends:**
- [Growth vs Value]
- [Cyclicals vs Defensives]
- [Outperformers and underperformers]

### Anomalies and Surprises
[Highlight unexpected market reactions]
1. [Event]: Market reacted [unexpectedly] because [explanation]
2. [Continue for significant anomalies]

---

## Commodity Market Deep Dive

[Dedicated section for commodity movements]

### Energy
- **Crude Oil (WTI/Brent):** [Price level, % change over period, key drivers]
- **Natural Gas:** [If significant movement]
- **Key Events:** [Specific news impacting energy: OPEC, geopolitics, inventory data]

### Precious Metals
- **Gold:** [Price level, % change, safe-haven flows vs real rate dynamics]
- **Silver:** [If significant divergence from gold]
- **Drivers:** [Geopolitical risk premium, inflation hedging, USD strength]

### Base Metals
- **Copper:** [As economic barometer - demand signals]
- **Aluminum, Nickel:** [If relevant supply/demand news]
- **China Factor:** [Impact of Chinese economic data/policy]

### Agricultural (If Relevant)
- **Grains:** [Wheat, Corn, Soybeans - weather, Ukraine conflict impacts]

[For each commodity, reference geopolitical events from main analysis and draw correlations]

---

## Forward-Looking Implications

### Market Positioning Insights
[What the news suggests for current market positioning]
- [Trend continuation or reversal signals]
- [Overvaluation or undervaluation indications]
- [Sentiment extremes (complacency or panic)]

### Upcoming Catalysts
[Events on horizon that may be set up by recent news]
- [Next FOMC meeting expectations post-recent decision]
- [Upcoming earnings seasons based on guidance]
- [Geopolitical developments to monitor]

### Risk Scenarios
[Based on recent news, identify key risks]
1. **[Risk Name]:** [Description, probability, potential impact]
2. **[Risk Name]:** [Description, probability, potential impact]
3. [Continue for 3-5 key risks]

---

## Data Sources and Methodology

### News Sources Consulted
[List primary sources used, organized by tier]
- **Official Sources:** [e.g., FederalReserve.gov, SEC.gov]
- **Tier 1 Financial News:** [e.g., Bloomberg, Reuters, WSJ]
- **Specialized:** [e.g., S&P Global Platts for commodities]

### Analysis Period
- **Start Date:** [Specific date]
- **End Date:** [Specific date]
- **Total Days:** 10

### Market Data
- Equity indices: [Data sources]
- Commodity prices: [Data sources]
- Economic data: [Government sources]

### Knowledge Base References
- `market_event_patterns.md` - Historical reaction patterns
- `geopolitical_commodity_correlations.md` - Geopolitical-commodity frameworks
- `corporate_news_impact.md` - Mega-cap impact analysis
- `trusted_news_sources.md` - Source credibility assessment

---

*Analysis Date: [Date report generated]*
*Language: English*
*Analysis Thinking: English*

```

**文件命名规则：**
`market_news_analysis_[开始日期]_到_[结束日期].md`

**报告质量标准：**
- 客观、基于事实的分析（不进行超出概率加权情景的推测）
- 用具体百分比量化价格变动
- 对主要观点引用来源
- 区分相关性和因果关系
- 在将市场变动归因于特定新闻时承认不确定性
- 使用正确的金融术语
- 保持英语的一致性

## 关键分析原则

在进行市场新闻分析时：

1. **关注真正影响市场走势的新闻，过滤掉次要事件**
2. **多资产视角：**分析股票、债券、商品、货币，以全面了解影响
3. **模式识别：**与历史先例进行比较，同时注意独特方面
4. **因果关系严谨性：**严格将市场变动归因于特定新闻，而非巧合的时间安排
5. **前瞻性：**强调对未来市场行为的启示，而不仅仅是回顾性描述
6. **客观性：**区分市场反应（实际发生的情况）和个人的市场观点（应该发生的情况）
7. **量化：**使用具体数字（百分比、基点），而不是模糊的术语（如“显著”、“较大”）
8. **来源可信度：**优先考虑官方来源和一级新闻，而非谣言和未经验证的报告
9. **广泛分析：**只有当涉及大型科技公司或系统性信号时，才关注个别股票走势
10. **英语一致性：**所有思考、分析和输出均使用英语，以保持一致性

## 常见误区

**过度归因：**
- 并非每个市场变动都是由新闻驱动的（还存在技术因素、资金流动、月末再平衡）
- 当归因不确定时，要予以承认

**近期偏见：**
- 最新的新闻并不总是最重要的
- 按实际影响排名，而非时间顺序

**事后偏见：**
- 区分“事后看来显而易见”的情况和“当时令人惊讶”的情况
- 注意共识预期与实际结果的区别

**单一因素分析：**
- 市场对多种因素同时作出反应
- 认识到相互作用的影响

**忽视幅度：**
- 预期之外的“热门”CPI（高出共识0.1%）与高出0.5%是不同的
- 量化意外因素

## 资源

### 参考资料/

**market_event_patterns.md** - 包括以下内容的综合知识库：
- 中央银行货币政策事件（FOMC、ECB、BOJ、PBOC）
- 通胀数据发布（CPI、PPI、PCE）
- 就业数据（NFP、失业率、工资）
- GDP报告
- 地缘政治事件（冲突、贸易战争、制裁）
- 企业收益（大型科技公司、银行、能源行业）
- 信用事件和评级变化
- 特定商品事件（欧佩克、天气、供应中断）
- 经济衰退指标
- 历史案例研究（2008年危机、COVID-19、2022年通胀）
- 模式识别框架和情绪分析

**geopolitical_commodity_correlations.md** - 详细的相关性分析，涵盖：
- 能源商品（原油、天然气、煤炭）和地缘政治冲突
- 贵金属（黄金、白银、铂金、钯金）的安全避险动态
- 基础金属（铜、铝、镍、锌）和经济/政治风险
- 农产品（小麦、玉米、大豆）和天气/政策
- 稀土元素和关键矿产（中国主导、供应安全）
- 地区地缘政治框架（中东、俄罗斯-欧洲、亚太地区、拉丁美洲）
- 相关性总结表
- 时间范围考虑

**corporate_news_impact.md** - 大型科技公司分析框架：
- “七大巨头”科技公司（英伟达、苹果、微软、亚马逊、Meta、谷歌、特斯拉）
- 金融行业的大型科技公司（摩根大通、美国银行等）
- 医疗保健行业的大型科技公司（联合健康、辉瑞、强生、默克）
- 能源行业的大型科技公司（埃克森美孚、雪佛龙）
- 消费品行业的大型科技公司（宝洁、可口可乐、百事可乐）
- 工业行业的大型科技公司（波音、卡特彼勒）
- 收益影响框架、产品发布、并购、监管问题
- 行业传染模式
- 影响幅度框架

**trusted_news_sources.md** - 来源可信度指南：
- 一级主要来源（央行、政府机构、SEC）
- 二级主要财经新闻（彭博社、路透社、华尔街日报、金融时报、CNBC）
- 三级专业来源（能源、科技、新兴市场、中国特定领域、加密货币）
- 四级分析和研究（独立研究、央行出版物、智库）
- 搜索和聚合工具
- 来源质量评估标准
- 速度与准确性之间的权衡
- 10天分析的推荐搜索策略
- 来源可信度框架
- 应避免的警示来源

## 重要说明

- 所有分析思考必须使用英语进行
- 所有输出文件必须使用Markdown格式
- 使用WebSearch和WebFetch工具自动收集新闻
- 重点关注参考资料中定义的可信新闻来源
- 按影响得分（价格影响 × 影响范围 × 前瞻性）对事件进行排名
- 分析周期：从当前日期起过去10天
- 重点分析美国股市和商品市场
- FOMC和其他央行政策决策获得最高优先级分析
- 严格区分相关性和因果关系
- 用具体百分比量化所有市场反应
- 根据收集到的新闻类型加载适当的参考文件
- 生成按市场影响排序的全面报告（影响最大的排在最前面）