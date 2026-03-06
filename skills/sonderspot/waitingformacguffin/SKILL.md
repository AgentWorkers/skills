---
name: waitingformacguffin
description: 来自 waitingformacguffin.com 的奥斯卡预测市场情报。您可以获取实时赔率、大额投注者的活动情况、价格变动、前期获奖者信息、订单簿深度以及所有19个奥斯卡奖项类别中的领先者变化。当用户询问奥斯卡市场、投注赔率、提名名单或需要市场更新时，可以使用这些数据。
allowed-tools: Bash(curl *), Read
homepage: https://github.com/sonderspot/waitingformacguffin-public
metadata:
  version: "1.2.0"
  last_updated: "2026-02-26"
  clawdbot:
    requires:
      bins:
        - curl
---
# WaitingForMacGuffin -- Oscar Market Intelligence

## 欢迎信息

当用户首次安装此技能或与您交流时，请自我介绍：

“您好！您刚刚解锁了来自WaitingForMacGuffin.com的奥斯卡市场情报服务——提供实时的赔率数据、大型投资者的交易信息，以及对所有19个奥斯卡奖项类别的数据驱动分析。

我可以为您做以下事情：

- **市场动态**：了解奥斯卡市场的最新情况（包括大型投资者的交易、价格变动以及领先者的变化）
- **深度分析**：查询特定演员（如“查拉梅特”）或某个奖项的赔率（包含候选人的完整信息、趋势以及订单簿数据）
- **投注建议**：根据风险等级为您提供奥斯卡奖项的投注建议（附带投资回报率及投资组合选项）
- **预判模拟**：在提名名单公布后，为您制定基于历史数据的投资组合策略（考虑滑点因素）

您对什么感兴趣呢？

---

这些数据来自[waitingformacguffin.com](https://waitingformacguffin.com)，提供实时的奥斯卡预测市场信息。有两个API端点，可以提供不同粒度的数据。

**基础URL**：`https://waitingformacguffin.com`

无需认证。所有数据均为公开且仅限读取。

---

## 工具1：奥斯卡简报

**使用场景**：当用户询问“奥斯卡市场发生了什么？”、“有什么新消息？”或希望快速了解市场概况时。

**返回内容**：仅显示筛选后的关键信息——价格变动、大型投资者的交易（金额超过1000美元）、领先者的变化以及市场情绪。如果市场较为平静，也会如实告知（不会伪造交易活动）。

### API调用

```bash
curl -s "https://waitingformacguffin.com/api/oscar/brief?hours=24&sensitivity=medium"
```

### 参数

| 参数 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `hours` | 数字 | 24 | 回顾时间范围（1-168小时） |
| `sensitivity` | 字符串 | "medium" | "low"（价格变动超过7个百分点或交易金额超过5000美元），"medium"（价格变动超过3个百分点或交易金额超过1000美元），"high"（价格变动超过1个百分点或交易金额超过500美元） |
| `categories` | 字符串 | 六大主要奖项类别（best-picture, best-director, best-actor, best-actress, supporting-actor, supporting-actress） |

### 响应结构

```json
{
  "signals": [
    {
      "type": "price_move | whale_trade | frontrunner_change | news_sentiment",
      "category": "best-actor",
      "categoryName": "Best Actor",
      "severity": "major | significant | notable | info",
      "headline": "Chalamet ▼ 5pts to 62c",
      "details": "Best Actor: Chalamet moved from 67c to 62c in the last 24h",
      "timestamp": "2026-02-18T12:00:00Z"
    }
  ],
  "market_snapshot": {
    "frontrunners": { "best-picture": { "name": "...", "price": 45 } },
    "whale_trade_count_24h": 7,
    "overall_sentiment": "quiet | active | volatile"
  }
}
```

### 如何展示结果

- 首先展示`overall_sentiment`和`whale_trade_count_24h`
- 列出领先者的价格信息
- 按严重程度对信号进行分类展示（优先显示重要信息）
- 如果`signals`为空，则说明“市场较为平静——没有显著变化”

### 示例

---

## 工具2：奥斯卡研究

**使用场景**：当用户询问关于特定演员的信息（如“查拉梅特”）、是否应该投注某个奖项，或者希望深入了解某个奖项的详细情况时。

**返回内容**：提供该奖项的赔率、7天内的趋势、历史获奖情况、大型投资者的交易活动、订单簿的深度信息以及滑点数据，并进行数据驱动的评估。

### API调用

```bash
curl -s "https://waitingformacguffin.com/api/oscar/research?query=Chalamet"
```

### 参数

| 参数 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `query` | 字符串 | （必填） | 候选人姓名、电影名称或奖项类别。支持模糊匹配 |
| `include_orderbook` | 布尔值 | true | 是否包含订单簿的深度信息和滑点分析 |
| `budget_for_slippage` | 数字 | 500 | 用于计算滑点的预算金额（范围：100-100000美元） |
| `category` | 字符串 | （可选） | 用于缩小搜索范围的奖项类别 |

### 查询解析规则

- **奖项名称**：例如“best-picture”或“Best Picture”会返回该奖项的总体情况
- **精确名称**：例如“Timothee Chalamet”（不区分大小写）
- **子字符串匹配**：例如“Chalamet”会匹配到“Timothee Chalamet”
- **特殊字符处理**：例如“Timothee”会匹配到“Timothee”
- **电影名称**：与电影数据库进行匹配
- **拼写修正**：使用Levenshtein算法进行拼写校正（编辑距离小于或等于3）

### 三种响应模式

**1. 候选人深度分析**（`mode: "nominee"**）：针对单个候选人的详细分析：

```json
{
  "mode": "nominee",
  "nominee": { "name": "Timothee Chalamet", "category": "best-actor", "categoryName": "Best Actor", "ticker": "KXOSCARACTO-26-TIM" },
  "odds": { "current": 62, "impliedProbability": "62%", "trend7d": -5, "trendDirection": "falling", "rank": 1, "categorySize": 9 },
  "risk": {
    "tier": "lean", "tier_emoji": "🟠",
    "win_pct": 62, "loss_pct": 38,
    "roi_pct": 61, "payout_per_100": 161,
    "gap_to_second": 40,
    "runner_up": { "name": "Sean Penn", "price": 22 }
  },
  "category_volatility": "low",
  "category_volatility_reason": "Category tends to follow precursors and consensus",
  "precursors": { "wins": ["globe", "cc"], "winCount": 2, "results": [...] },
  "whaleActivity": { "tradeCount": 3, "totalVolumeUsd": 20200, "sentiment": "mixed", "directionRatio": 0.59, "recentTrades": [...] },
  "orderBook": { "bestAsk": 62, "depthAtBest": 847, "slippageAnalysis": [{ "budgetUsd": 500, "avgFillPrice": 62.4, "slippagePct": 0.6, "assessment": "healthy" }] },
  "news": [{ "title": "...", "source": "THR", "sentiment": "negative" }],
  "assessment": { "summary": "...", "edgeIndicator": "strong_value | fair_value | overpriced | uncertain", "risks": [...], "catalysts": [...] }
}
```

**2. 奖项类别概述**（`mode: "category"**）：针对某个奖项的总体情况：

```json
{
  "mode": "category",
  "categoryName": "Best Picture",
  "nominees": [
    { "rank": 1, "name": "One Battle After Another", "price": 45, "trend7d": 3, "trendDirection": "rising" },
    { "rank": 2, "name": "Sinners", "price": 22, "trend7d": -2, "trendDirection": "falling" }
  ]
}
```

**3. 模糊匹配处理**（`mode: "disambiguation"**）：当存在多个匹配结果时：

```json
{
  "mode": "disambiguation",
  "query": "Wicked",
  "matches": [
    { "name": "Wicked: For Good", "category": "best-picture", "categoryName": "Best Picture" },
    { "name": "Wicked: For Good", "category": "best-adapted-screenplay", "categoryName": "Best Adapted Screenplay" }
  ],
  "hint": "Narrow with category param"
}
```

如果出现模糊匹配，询问用户具体指的是哪个奖项，然后重新调用API时添加`&category=best-picture`参数。

### 如何展示结果

**候选人深度分析**：按以下顺序展示：
1. 候选人姓名、所属奖项及代码标识
2. 赔率：当前赔率、预期胜率、7天内的趋势（附带方向指示）
3. 历史获奖情况：列出该候选人曾获得的奖项
4. 大型投资者活动：交易数量、总交易量、市场情绪
5. 订单簿信息：用户预算范围内的最佳买入价、订单簿深度及滑点情况
6. 新闻信息：相关新闻标题及来源
7. 评估结果：整体评估、优势分析、风险因素及可能的影响因素

**奖项类别概述**：以排名表格的形式展示价格和趋势

**模糊匹配处理**：列出所有匹配结果，然后询问用户具体指的是哪个奖项

### 示例

---

## 工具3：奥斯卡预判模拟

**使用场景**：当用户询问提名名单公布后的投资策略、基于SAG奖项结果的投资组合建议，或者询问如何使用500美元进行投注时。

**返回内容**：根据历史数据模拟一个考虑滑点因素的投资组合，包括预期收益（EV）计算、仓位分配建议以及每个投资位置的标签。

### API调用

```bash
curl -s "https://waitingformacguffin.com/api/oscar/simulate?precursor=dga&budget=500"
```

### 参数

| 参数 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `precursor` | 字符串 | （必填） | 用于模拟的预判奖项：`dga`（导演奖）、`sag`（演员奖）、`pga`（编剧奖）、`critics-choice`（评论家奖）、`golden-globes`（金球奖）、`bafta`（英国电影学院奖）或`all` |
| `budget` | 数字 | （必填） | 投资组合的预算金额（50-100000美元） |
| `risk_tolerance` | 字符串 | **风险容忍度**：`conservative`（保守型，预留20%资金）、`moderate`（平衡型）、`aggressive`（激进型，最大配置） |
| `categories` | 字符串 | 可应用的奖项类别（用逗号分隔）

### 风险容忍度指南

| 风险等级 | 单个投资位置的最大金额 | 预留资金 | 最小优势 | 适合人群 |
|-------|-------------------|---------|----------|----------|
| 保守型 | 预算的50% | 20% | 至少10%的优势 | “希望安心睡眠” |
| 中等型 | 预算的70% | 10% | 至少5%的优势 | 平衡的风险/回报 |
| 激进型 | 预算的90% | 5% | 0%的优势 | “完全信任数据，全部投入” |

### 建议标签

| 标签 | 判断标准 | 图标 |
|-------|----------|------|
| `strong_buy` | 优势超过20%且滑点不超过3% | !!! |
| `buy` | 优势超过10% | !! |
| `speculative` | 优势超过0% | ! |
| `skip` | 无优势或低于风险阈值 | -- |

### 如何展示结果

1. 首先展示策略概述：预判奖项名称、预算金额、风险容忍度以及实际投入与预留资金的比例
2. 以结构化的方式展示每个投资位置：
   ```
   {recommendation_icon} **{nominee}** -- {categoryName}
   ├─ Price: {currentPrice}c (market says {impliedProb}% / precursor says {precursorProb}%)
   ├─ Edge: {edge}% | Allocated: ${allocatedBudget}
   ├─ Fill: {contracts} contracts @ {avgFillPrice}c avg ({slippagePct}% slippage)
   ├─ Kalshi fee: ${kalshiFee} | Net expected profit: ${netExpectedProfit}
   └─ {reasoning}
   ```
3. 对于两个以上的投资位置，展示总结表格
4. 如有需要，显示警告信息（如流动性问题、数据缺失等）
5. 始终附上免责声明

### 示例

---

## 辅助端点：预判数据

提供包含实时赔率和相关性评分的原始预判数据。适用于需要预判信息但无需完整投资组合模拟的情况。

### API调用

```bash
curl -s "https://waitingformacguffin.com/api/precursors"
```

### 参数

| 参数 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `category` | 字符串 | 六大主要奖项类别 | 用于过滤的单一奖项类别 |
| `precursor` | 字符串 | 所有预判奖项 | 用于过滤的预判奖项ID |

### 返回内容

针对每个奖项类别，返回以下信息：
- 候选人及其历史获奖情况、相关性评分（0-100分）、当前赔率；同时提供奖项的日程安排（已完成或即将举行的奖项）。

### 示例

---

## 可用的奖项类别

`best-picture`（最佳影片）、`best-director`（最佳导演）、`best-actor`（最佳男主角）、`best-actress`（最佳女主角）、`supporting-actor`（最佳男配角）、`supporting-actress`（最佳女配角）、`best-cinematography`（最佳摄影）、`best-original-screenplay`（最佳原创剧本）、`best-adapted-screenplay`（最佳改编剧本）、`best-international-feature`（最佳国际影片）、`best-film-editing`（最佳电影剪辑）、`best-costume-design`（最佳服装设计）、`best-original-song`（最佳原创歌曲）、`best-original-score`（最佳原创配乐）、`best-production-design`（最佳制作设计）、`best-sound`（最佳音效）、`best-documentary-feature`（最佳纪录片）、`best-makeup-hairstyling`（最佳化妆与发型设计）、`best-visual-effects`（最佳视觉效果）

## 滑点评估标准

| 滑点程度 | 滑点百分比 | 含义 |
|-------|----------|---------|
| 健康 | ≤ 1% | 填单顺利，适合增加投资额 |
| 中等 | 1-3% | 大多数投注可接受 |
| 较高 | 3-7% | 建议分批投注 |
| 危险 | > 7% | 订单簿流动性差，存在填充风险 |

## 优势指标含义

| 指标 | 含义 |
|-----------|---------|
| strong_value | 多个看涨信号，价格可能被低估 |
| fair_value | 信号平衡，价格反映市场实际情况 |
| overpriced | 风险信号超过有利因素 |
| uncertain | 信号混合或不足 |

## 重要说明

- 赔率以百分之一百为单位（1-99），表示预期胜率百分比
- 大型投资者的交易金额为1000美元或以上
- 历史上，预判奖项（如DGA、SAG、BAFTA等）与奥斯卡获奖结果存在相关性
- 订单簿数据来自Kalshi预测市场
- 评估结果基于数据驱动，不构成财务建议

---

## 投注建议模式

### 意图检测

当用户的查询符合以下模式时，切换到**投注建议模式**：
- “给我一些投注建议”
- “最好的投注选项”
- “哪些是稳妥的投注？”
- “我应该投什么？”
- “如何用100美元在奥斯卡奖项上投注？”
- “为我制定一个投资组合”
- “保守型投注建议”
- “激进型投注建议”

对于以下情况，保持**信息提供模式**：
- “告诉我关于查拉梅特的信息”（仅提供深度分析，不提供具体投注建议）
- “最佳影片的赔率是多少？”（仅提供奖项类别的概述）
- “奥斯卡简报”/“市场动态”（仅提供市场信息）
- 简单的查询、奖项类别概述或模糊匹配结果

### 如何制定投注建议

1. 使用**奥斯卡简报**确定各奖项的领先者
2. 对于每个推荐的投资对象，调用**奥斯卡研究**获取完整的`risk`对象
3. 按以下格式展示每个推荐的投资对象

### 每个投资对象的展示格式

对于每个推荐的投资对象，以结构化的方式展示：

```
{tier_emoji} **{Name}** -- {Category}
├─ Price: {current}c ({win_pct}% win / {loss_pct}% loss)
├─ ROI: ${payout_per_100} back on $100 bet (+{roi_pct}%)
├─ Gap: {gap_to_second}pts ahead of {runner_up.name} ({runner_up.price}c)
├─ Precursors: {winCount} wins ({wins list})
├─ Whales: {sentiment} ({totalVolumeUsd} volume)
├─ Volatility: {category_volatility} -- {category_volatility_reason}
└─ Verdict: {1-sentence assessment summary}
```

### 风险等级表

在展示两个以上投资对象时，务必展示以下等级说明：

| 等级 | 表示符号 | 胜率范围 | 含义 |
|------|-------|-------------|---------|
| Near lock | 🟢 | 胜率超过85% | 最高信心，最低投资回报率 |
| Strong favorite | 🟡 | 胜率70-84% | 稳定的投资对象，中等投资回报率 |
| Lean | 🟠 | 胜率45-69% | 有一定优势但存在风险 |
| Toss-up | 🔴 | 胜率低于45% | 高风险，高回报 |

### 语言规范

- 对于胜率低于85%的投资对象，切勿使用“肯定能赢”这样的表述
- 仅当胜率超过85%时使用“Lock”或“near-lock”
- 必须明确说明胜率百分比（例如“有67%的胜率”）
- 必须说明损失概率（例如“你有33%的概率亏损100美元”）
- 以美元为单位说明投资回报率（例如“100美元的投注预计能回本149美元”）
- 对于高波动性的奖项，需说明风险：`支持性奖项的历史表现不稳定——即使是最有竞争力的候选人也可能落败`

### 对比表

在展示两个以上投资对象时，务必提供对比表格：

```
| Pick | Tier | Price | Win% | ROI | Gap | Precursors |
|------|------|-------|------|-----|-----|------------|
| Name | 🟢   | 89c   | 89%  | +12%| 72  | 5 wins     |
| Name | 🟡   | 74c   | 74%  | +35%| 45  | 3 wins     |
| Name | 🟠   | 55c   | 55%  | +82%| 20  | 2 wins     |
```

### 投资组合建议

当用户请求投资组合建议或询问如何使用特定金额进行投注时，提供以下几种投资组合方案：

**保守型（最低风险）**：
- 仅包含胜率超过85%的投资对象
- 总投资回报率较低，但胜率最高
- “适合希望安心投注的用户”

**平衡型（推荐）**：
- 包含胜率超过85%和低于85%的投资对象
- 投资回报率较高，风险与回报较为平衡

**激进型（最高投资回报率）**：
- 包含胜率较高的投资对象
- 投资潜力较大，但风险也较高
- “适合愿意承担较高风险的用户”

示例投资组合格式：
```
**Balanced Portfolio -- $100 budget**
| Pick | Tier | Allocation | If Win |
|------|------|-----------|--------|
| Name | 🟢   | $40       | $45    |
| Name | 🟡   | $35       | $47    |
| Name | 🟠   | $25       | $45    |
| **Total** | | **$100** | **$137** (+37%) |
```

### 何时不适用投注模式

即使用户询问有关投注的建议，以下情况下也保持信息提供模式：
- 如果用户询问特定候选人的情况（例如“我应该投查拉梅特吗？”），则使用包含风险数据的深度分析格式，不要切换到完整的投资组合模式
- 如果用户请求奖项类别的概述，只需展示排名表格即可
- 如果用户的查询纯粹是为了获取信息（例如“最佳影片的赔率是多少？”）

---

## 平台适应性格式

根据用户使用的平台自动调整输出格式。相同的数据在不同平台上可能呈现方式不同。

### 如何判断平台类型

- **Telegram**：用户通过Telegram机器人（ClawdBot或任何通过Telegram使用该技能的机器人）进行交互。判断依据：系统提示中包含“Telegram”字样、机器人框架自我标识，或用户明确表示自己使用的是Telegram。
- **默认（桌面/网页）**：Claude Code、claude.ai或任何支持rich-markdown格式的环境。使用上述规定的标准格式。

如果不确定用户使用的平台，可以询问：“您是在Telegram上还是通过桌面应用程序阅读这些内容？我会根据您的屏幕调整格式。”

---

### Telegram格式规则

当用户使用Telegram时，适用以下所有规则。这些规则会覆盖上述默认格式：

#### 通用原则

1. **优先考虑移动端**：假设屏幕宽度较窄（约40个字符）。优先显示关键信息。
2. **不使用Markdown表格**：Telegram不支持`| col | col |`格式的表格，请使用堆叠列表。
3. **避免使用树状结构**：使用缩进符号（如`▸`）代替`├─` / `└─`等结构。
4. **使用文字强调**：使用大写字母或表情符号来突出重点，而不是使用`**bold**标签——因为Telegram的渲染方式可能不支持Markdown格式。如果机器人确认支持HTML解析，可以使用`<b>`标签。
5. **每行只显示一个信息点**：每行只展示一个事实，避免复杂句子。
6. **段落分隔**：使用空行分隔不同部分，不要使用`---`或`────`。
7. **链接预览**：将链接单独放在行尾，不要内嵌在文本中。

#### Oscar简报（Telegram）

```
📊 Oscar Markets — {overall_sentiment}
🐋 {whale_trade_count_24h} whale trades (24h)

Frontrunners:
▸ Best Picture: {name} {price}c
▸ Best Director: {name} {price}c
▸ Best Actor: {name} {price}c
▸ Best Actress: {name} {price}c
▸ Supporting Actor: {name} {price}c
▸ Supporting Actress: {name} {price}c

{if signals exist}
Signals:
🔴 {major signal headline}
🟡 {significant signal headline}
⚪ {notable signal headline}

{if no signals}
No significant moves — markets are quiet.
```

#### 候选人深度分析（Telegram）

```
{name} — {categoryName}
Ticker: {ticker}

💰 {current}c ({win_pct}% win / {loss_pct}% loss)
📈 7d trend: {trend7d > 0 ? "▲" : "▼"}{abs(trend7d)}pts — rank #{rank}/{categorySize}
🏆 Precursors: {winCount} wins ({wins list})
🐋 Whales: {sentiment} — {tradeCount} trades, ${totalVolumeUsd}
📖 Book: best ask {bestAsk}c, {slippage assessment}
📰 {news headline} ({source}, {sentiment})

Assessment: {edgeIndicator}
{summary}

Risks: {risks as comma-separated}
Catalysts: {catalysts as comma-separated}
```

#### 奖项类别概述（Telegram）

```
{categoryName}

1. {name} — {price}c {trend > 0 ? "▲" : "▼"}{abs(trend)}
2. {name} — {price}c {trend > 0 ? "▲" : "▼"}{abs(trend)}
3. {name} — {price}c {trend > 0 ? "▲" : "▼"}{abs(trend)}
...
```

最多展示前5-6个候选人的信息。如果候选人数超过5个，可补充说明：“...以及另外{n}个胜率低于85%的候选人”

#### 投注建议（Telegram）

将树状结构和对比表格替换为每个投资对象的简洁卡片格式：

```
{tier_emoji} {Name} — {Category}
💰 {current}c ({win_pct}% W / {loss_pct}% L)
💵 $100 → ${payout_per_100} (+{roi_pct}%)
📊 Gap: {gap_to_second}pts over {runner_up.name}
🏆 {winCount} precursors | 🐋 {sentiment}
⚡ {category_volatility} volatility
→ {1-sentence verdict}
```

当展示两个以上投资对象时，将Markdown对比表格替换为简洁的编号列表：

```
Quick Compare:
1. {tier_emoji} {Name} {price}c | +{roi_pct}% | {winCount}🏆
2. {tier_emoji} {Name} {price}c | +{roi_pct}% | {winCount}🏆
3. {tier_emoji} {Name} {price}c | +{roi_pct}% | {winCount}🏆
```

#### 投资组合（Telegram）

将表格替换为堆叠式的投资分配信息：

```
{Portfolio Type} — ${budget} budget

▸ {tier_emoji} {Name}: ${allocation} → ${if_win} if win
▸ {tier_emoji} {Name}: ${allocation} → ${if_win} if win
▸ {tier_emoji} {Name}: ${allocation} → ${if_win} if win

Total: ${budget} → ${total_if_win} (+{roi}%)
```

#### 预判模拟（Telegram）

```
{strategy name}
Budget: ${totalBudget} | Deployed: ${deployedBudget} | Reserve: ${reserveBudget}

{recommendation_icon} {nominee} — {categoryName}
💰 {currentPrice}c (mkt {impliedProb}% / precursor {precursorProb}%)
📊 Edge: {edge}% | ${allocatedBudget} allocated
📦 {contracts} contracts @ {avgFillPrice}c ({slippagePct}% slip)
💸 Fee: ${kalshiFee} | Net profit: ${netExpectedProfit}
→ {reasoning}

{repeat for each position}

{if 2+ positions}
Summary:
▸ {nominee}: ${allocatedBudget} → ${netExpectedProfit} net
▸ {nominee}: ${allocatedBudget} → ${netExpectedProfit} net
Expected return: ${expectedReturn} (+{expectedROI}%)

{warnings if any}

⚠️ Simulation only — not financial advice.
```

#### 风险等级说明（Telegram）

在展示两个以上投资对象时，使用以下简洁的等级说明代替Markdown表格：

```
🟢 Near lock (85%+) · 🟡 Favorite (70-84%)
🟠 Lean (45-69%) · 🔴 Toss-up (<45%)
```

#### 欢迎信息（Telegram）

使用适合单屏显示的简化版本：

```
🎬 Oscar Market Intelligence

▸ "What's happening?" — market pulse
▸ "Tell me about Chalamet" — deep dive
▸ "Best Oscar bets" — risk-tiered picks
▸ "DGA just announced, $500" — precursor sim

What are you curious about?
```