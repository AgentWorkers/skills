---
name: waitingformacguffin
description: 来自 waitingformacguffin.com 的奥斯卡预测市场情报：提供实时赔率、大额投注者的活动情况、价格走势、前期获奖情况、订单簿深度以及所有19个奥斯卡奖项类别的领先者变化信息。当用户询问奥斯卡市场、投注赔率、提名名单或需要市场更新时，可参考此数据。
allowed-tools: Bash(curl *), Read
homepage: https://github.com/sonderspot/waitingformacguffin-public
metadata:
  version: "1.3.0"
  last_updated: "2026-03-13"
  clawdbot:
    requires:
      bins:
        - curl
---
# WaitingForMacGuffin -- Oscar Market Intelligence

## 欢迎信息

当用户首次安装此技能或与您交流时，请自我介绍：

“您好！您刚刚解锁了来自WaitingForMacGuffin.com的奥斯卡市场情报服务——提供实时赔率、大额交易数据以及涵盖所有19个奥斯卡奖项类别的数据驱动分析功能。

以下是我能为您提供的服务：

- **市场动态**：了解奥斯卡市场的最新动态（包括大额交易、价格变动和热门候选人的变化）
- **深度分析**：查询特定演员（如“Timothee Chalamet”）或获取最佳影片的赔率信息（包含候选人概况、趋势及市场前兆）
- **投注建议**：根据风险等级为您提供奥斯卡奖项的投注建议（附带投资回报率及投资组合选项）
- **前兆模拟**：在金球奖（DGA）结果公布后，为您制定投资策略（考虑滑点因素，包含预期收益及持仓规模）

您对哪些内容感兴趣呢？

---

这些数据来自[waitingformacguffin.com](https://waitingformacguffin.com)，通过两个API端点提供不同粒度级别的市场情报。

**基础URL**：`https://waitingformacguffin.com`

无需身份验证，所有数据均为公开且仅限读取。

---

## 工具1：奥斯卡简报

**使用场景**：当用户询问“奥斯卡市场当前情况如何？”、“有最新更新吗？”或希望快速了解市场概况时。

**返回内容**：仅显示筛选后的关键信息——价格变动、大额交易（金额超过1000美元）、热门候选人的变化以及市场情绪。如果市场较为平静，也会如实告知（绝不会伪造交易活动）。

### API调用

```bash
curl -s "https://waitingformacguffin.com/api/oscar/brief?hours=24&sensitivity=medium"
```

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `hours` | 数字 | 24 | 回顾时间范围（1-168小时） |
| `sensitivity` | 字符串 | "medium" | "low"（价格变动超过7个百分点或交易金额超过5000美元）,"medium"（价格变动超过3个百分点或交易金额超过1000美元）,"high"（价格变动超过1个百分点或交易金额超过500美元） |
| `categories` | 字符串 | "big 6" | 用逗号分隔的奖项类别（最佳影片、最佳导演、最佳男主角、最佳女主角、最佳男配角、最佳女配角） |

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
    "overall_sentiment": "quiet | active | volatile",
    "whale_leaderboard": [
      {
        "rank": 1,
        "nominee": "Jessie Buckley",
        "category": "best-actress",
        "categoryName": "Best Actress",
        "totalVolumeUsd": 4850.00,
        "tradeCount": 1,
        "yesVolumeUsd": 4850.00,
        "noVolumeUsd": 0,
        "sentiment": "bullish | bearish | mixed"
      }
    ]
  }
}
```

`whale_leaderboard`根据回顾时间范围内的总交易量对候选人进行排名。可用于回答诸如“谁的交易量最大？”或“资金流向哪里？”等问题。如需查看所有19个奖项类别，请使用`categories=`并传入所有类别名称（详见下方“可用类别”部分）。

### 结果展示方式

- 首先展示`overall_sentiment`和`whale_trade_count_24h`
- 列出热门候选人的价格信息
- 按严重程度对信号进行分类展示（严重程度从高到低）
- 如果`signals`为空，则显示“市场较为平静——没有显著交易”

### 示例

---

## 工具2：奥斯卡研究

**使用场景**：当用户询问“关于Timothee Chalamet的情况”，“我应该投注X吗？”，“最佳影片的赔率是多少？”或希望深入了解特定候选人或奖项类别时。

**返回内容**：提供详细的分析结果，包括赔率、7天内的趋势、该候选人的过往获奖情况、市场情绪以及订单簿信息。

### API调用

```bash
curl -s "https://waitingformacguffin.com/api/oscar/research?query=Chalamet"
```

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `query` | 字符串 | （必填） | 候选人姓名、电影名称或奖项类别名称。支持模糊匹配 |
| `include_orderbook` | 布尔值 | true | 是否包含订单簿深度和滑点分析 |
| `budget_for_slippage` | 数字 | 500 | 用于计算滑点的预算金额（100-100000美元） |
| `category` | 字符串 | （可选） | 用于进一步明确查询范围的奖项类别 |

### 查询解析方式

系统会自动进行模糊匹配：
1. **奖项类别名称**：如“best-picture”或“Best Picture”会返回该类别的概览
2. **精确名称**：如“Timothee Chalamet”（不区分大小写）
3. **子字符串匹配**：如“Chalamet”会匹配到“Timothee Chalamet”
4. **特殊字符处理**：如“Timothee”会匹配到“Timothee”
5. **电影名称**：与电影数据库进行匹配
6. **拼写校正**：使用Levenshtein算法进行拼写校正（编辑距离小于等于3）

### 三种响应模式

**1. 候选人深度分析**（`mode: "nominee"）：针对单个候选人的详细分析：

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

**2. 奖项类别概览**（`mode: "category"）：针对特定奖项类别的概览：

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

**3. 模糊匹配结果处理**（`mode: "disambiguation"）：当存在多个匹配结果时：

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

遇到模糊匹配时，请询问用户具体指的是哪个奖项类别，然后重新调用API并添加`&category=best-picture`参数。

### 结果展示方式

**候选人深度分析**：按以下顺序展示：
1. 候选人姓名、所属奖项类别及代码标识
2. 赔率：当前赔率、预期概率及7天内的趋势
3. 历史获奖情况：列出该候选人曾获得的奖项
4. 市场情绪：交易数量、总交易量及市场趋势
5. 订单簿信息：用户预算范围内的最佳买入价、订单簿深度及滑点情况
6. 新闻资讯：相关新闻标题及来源
7. 综合评估：包括整体评估、优势分析、风险因素及影响因素

**奖项类别概览**：以表格形式展示各奖项的赔率和趋势

**模糊匹配结果处理**：列出所有匹配结果，然后让用户选择所需的奖项类别。

### 示例

---

## 工具3：奥斯卡前兆模拟

**使用场景**：当用户询问“金球奖结果公布后该如何投资？”、“根据SAG奖项结果为我制定投资组合”，“我有500美元，应该在 guild week 之后投注什么？”或希望根据历史数据制定投资组合时。

**返回内容**：基于历史数据模拟的投资组合方案，考虑滑点因素，包含预期收益计算、持仓规模建议及每个投资位置的标签。

### API调用

```bash
curl -s "https://waitingformacguffin.com/api/oscar/simulate?precursor=dga&budget=500"
```

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `precursor` | 字符串 | （必填） | 基于哪个前兆奖项进行模拟：`dga`（金球奖）、`sag`（演员工会奖）、`bafta`（英国电影学院奖）等 |
| `budget` | 数字 | （必填） | 投资组合的预算金额（50-100000美元） |
| `risk_tolerance` | 字符串 | **风险容忍度**：`conservative`（保守型，预留20%资金）、`moderate`（平衡型）、`aggressive`（激进型） |
| `categories` | 字符串 | 可选类别 | 用逗号分隔的奖项类别（用于限定模拟范围）

### 风险容忍度指南

| 风险等级 | 单个投资位置的最大金额 | 预留资金比例 | 最小预期收益 | 适合人群 |
|-------|-------------------|---------|----------|----------|
| 保守型 | 预算的50% | 20% | 预期收益至少10% | 适合希望安心投资的人 |
| 平衡型 | 预算的70% | 预期收益至少5% | 风险与收益较为平衡（推荐） |
| 激进型 | 预算的90% | 预期收益至少5% | 相信数据，愿意承担较高风险 |

### 建议标签

| 标签 | 判断标准 | 图标 |
|-------|----------|------|
| `strong_buy` | 预期收益至少20%且滑点不超过3% | !!! |
| `buy` | 预期收益至少10% | !! |
| `speculative` | 预期收益超过0% | ! |
| `skip` | 无预期收益或低于风险阈值 | -- |

### 结果展示方式

1. 首先展示策略概述：包括前兆奖项名称、预算金额及风险容忍度
2. 以结构化的方式展示每个投资位置：
   ```
   {recommendation_icon} **{nominee}** -- {categoryName}
   ├─ Price: {currentPrice}c (market says {impliedProb}% / precursor says {precursorProb}%)
   ├─ Edge: {edge}% | Allocated: ${allocatedBudget}
   ├─ Fill: {contracts} contracts @ {avgFillPrice}c avg ({slippagePct}% slippage)
   ├─ Kalshi fee: ${kalshiFee} | Net expected profit: ${netExpectedProfit}
   └─ {reasoning}
   ```
3. 对于2个以上投资位置，提供汇总表格
4. 如有风险提示（如流动性问题或数据缺失），请予以说明
5. 必须始终显示免责声明

### 示例

---

## 前兆数据（辅助工具）

提供包含实时赔率和相关性评分的原始前兆数据。适用于需要前兆信息但无需完整投资组合模拟的情况。

### API调用

```bash
curl -s "https://waitingformacguffin.com/api/precursors"
```

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `category` | 字符串 | 所有6个主要奖项类别 | 用于筛选的单一类别名称 |
| `precursor` | 字符串 | 所有前兆奖项 | 用于筛选获奖候选人的前兆奖项ID |

### 返回内容

针对每个奖项类别，展示获奖候选人、相关奖项的获奖情况、相关性评分（0-100分）以及当前赔率。同时提供奖项的日程安排（已完成/即将举行的奖项）。

### 示例

---

## 可用奖项类别

`best-picture`（最佳影片）、`best-director`（最佳导演）、`best-actor`（最佳男主角）、`best-actress`（最佳女主角）、`supporting-actor`（最佳男配角）、`supporting-actress`（最佳女配角）、`best-cinematography`（最佳摄影）、`best-original-screenplay`（最佳原创剧本）、`best-adapted-screenplay`（最佳改编剧本）、`best-international-feature`（最佳国际影片）、`best-film-editing`（最佳电影剪辑）、`best-costume-design`（最佳服装设计）、`best-original-song`（最佳原创歌曲）、`best-original-score`（最佳原创配乐）、`best-production-design`（最佳制作设计）、`best-sound`（最佳音效）、`best-documentary-feature`（最佳纪录片）、`best-makeup-hairstyling`（最佳化妆与发型设计）、`best-visual-effects`（最佳视觉效果）

## 滑点评估标准

| 滑点百分比 | 含义 |
|-------|----------|---------|
| 健康 | ≤ 1% | 交易执行顺畅，适合增加持仓 |
| 中等 | 1-3% | 大多数投注情况下可接受 |
| 较高 | 3-7% | 建议分批下单 |
| 危险 | > 7% | 订单簿流动性较差，存在交易执行风险 |

## 优势指标含义

| 指标 | 含义 |
|-----------|---------|
| strong_value | 多个看涨信号，价格可能被低估 |
| fair_value | 信号相对均衡，价格反映市场实际情况 |
| overpriced | 风险信号占主导，价格可能被高估 |
| uncertain | 信号混乱或不足 |

## 重要说明

- 赔率以百分之一百为单位（1-99），表示预期概率%
- 大额交易指单笔交易金额超过1000美元
- 前兆奖项（如金球奖、演员工会奖、英国电影学院奖等）与奥斯卡奖项结果有历史相关性
- 订单簿数据来源于Kalshi预测市场
- 本服务提供的评估基于数据驱动的分析，不构成财务建议

---

## 投注建议模式

### 检测用户意图

当用户的查询符合以下模式时，切换到**投注建议模式**：
- “给我一些投注建议”
- “哪些投注比较稳妥？”
- “我应该投什么？”
- “如何用100美元进行奥斯卡投注？”
- “为我制定一个投资组合”
- “保守型投注建议”
- “激进型投注建议”

对于以下情况，保持**信息提供模式**：
- “告诉我关于Timothee Chalamet的情况”（仅提供深度分析，不提供投注建议）
- “最佳影片的赔率是多少？”（仅提供奖项类别概览）
- “奥斯卡市场动态”或“市场概况”
- 简单的查询、奖项类别概览或模糊匹配结果

### 制定投注建议的步骤

1. 使用**奥斯卡简报**确定各奖项的热门候选人
2. 对每个候选人的投注方案，调用**奥斯卡研究**功能获取完整的风险评估信息
3. 按以下格式展示每个投注建议

### 每个投注建议的展示方式

对于每个推荐的投注方案，以结构化的方式展示：

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

在展示2个以上投注建议时，务必包含以下说明：

| 风险等级 | 表示符号 | 胜率范围 | 含义 |
|------|-------|-------------|---------|
| Near lock | 🟢 | 胜率超过85% | 最高置信度，最低投资回报率 |
| Strong favorite | 🟡 | 胜率70-84% | 稳定的投注选择，中等投资回报率 |
| Lean | 🟠 | 胜率45-69% | 有一定优势但存在风险 |
| Toss-up | 🔴 | 胜率低于45% | 高风险，高回报 |

### 语言使用规范

- 对于赔率低于85%的投注建议，切勿使用“肯定能赢”这样的表述
- 仅当赔率超过85%时，使用“锁定”或“接近锁定”
- 必须明确说明胜率百分比（例如“有67%的胜率”）
- 必须说明损失概率（例如“投注100美元有33%的概率会损失”
- 投资回报率需以美元为单位表示（例如“投注100美元预计能收回149美元”）
- 对于高波动性奖项，需特别提示风险：“支持性奖项的历史表现不稳定，即使热门候选人也可能落败”

### 对比表展示规则

在展示3个以上投注建议时，必须提供对比表：

```
| Pick | Tier | Price | Win% | ROI | Gap | Precursors |
|------|------|-------|------|-----|-----|------------|
| Name | 🟢   | 89c   | 89%  | +12%| 72  | 5 wins     |
| Name | 🟡   | 74c   | 74%  | +35%| 45  | 3 wins     |
| Name | 🟠   | 55c   | 55%  | +82%| 20  | 2 wins     |
```

### 投资组合建议

当用户请求投资组合建议或询问“如何用X美元进行投注”时，提供以下几种投资组合方案：

**保守型（最低风险）**：
- 仅包含胜率超过85%的投注建议
- 总投资回报率较低，但置信度较高
- 适合希望安心投资的用户

**平衡型（推荐）**：
- 包含胜率超过85%和低于85%的投注建议
- 投资回报率与置信度较为平衡
- 是风险与回报较为理想的组合

**激进型（最高投资回报率）**：
- 包含胜率超过85%和低于85%的投注建议
- 投资潜力较高，但风险也相应增加
- 适合愿意承担较高风险的用户

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

### 何时不适用投注建议模式

即使用户询问有关投注的问题，但在以下情况下仍应保持信息提供模式：
- 用户询问特定候选人的情况（例如“我应该投注Timothee Chalamet吗？”）——此时应提供包含风险数据的深度分析，无需切换到完整的投资组合模式
- 用户仅请求奖项类别的概览——此时应展示排名表，让用户了解哪些候选人受青睐
- 用户的查询仅是为了获取信息（例如“最佳影片的赔率是多少？”）

---

## 平台适配格式

系统会自动检测用户使用的平台，并相应调整输出格式。相同的数据在不同平台上可能呈现方式不同。

### 平台检测方法

- **Telegram**：用户通过Telegram机器人（如ClawdBot或任何通过Telegram使用该技能的机器人）进行交互。判断依据：系统提示中包含“Telegram”字样、机器人框架自我标识，或用户明确表示自己使用的是Telegram。
- **默认平台（桌面/网页）**：Claude Code、claude.ai或任何支持富文本格式的环境。此时请使用上述规定的标准格式。

**注意事项**：
- 如果不确定用户使用的平台，可询问：“您是在Telegram上还是通过桌面应用查看此内容？我会根据您的屏幕格式进行调整。”

### Telegram专属格式规则

当用户使用Telegram时，需遵循以下规则：
1. **优先考虑移动端显示**：假设屏幕宽度有限（约40个字符）。优先显示关键信息。
2. **避免使用Markdown表格**：Telegram不支持`| col | col |`格式的表格，请使用堆叠列表代替。
3. **避免使用树状结构**：使用缩进符号（如`▸`）代替`├─`/`└─`等结构。
4. **使用文字强调**：使用大写字母或表情符号来表示强调内容，而非`**bold**标签——因为Telegram的解析方式可能不支持Markdown格式。如果机器人支持HTML解析，可使用`<b>`标签。
5. **每行仅显示一个信息点**：每行只展示一个事实，避免复杂句子。
6. **段落分隔**：使用空行分隔不同部分，避免使用`---`或`────`。
7. **链接展示**：将链接单独放在行尾，不要内嵌在文本中。

#### Oscar简报（Telegram专属格式）

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

#### 候选人深度分析（Telegram专属格式）

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

#### 奖项类别概览（Telegram专属格式）

```
{categoryName}

1. {name} — {price}c {trend > 0 ? "▲" : "▼"}{abs(trend)}
2. {name} — {price}c {trend > 0 ? "▲" : "▼"}{abs(trend)}
3. {name} — {price}c {trend > 0 ? "▲" : "▼"}{abs(trend)}
...
```

最多展示前5-6个热门候选人。如果超过这个数量，可添加：“...以及另外{n}个候选人”

#### 投注建议（Telegram专属格式）

将树状结构和对比表替换为每个投注建议的简洁卡片格式：

```
{tier_emoji} {Name} — {Category}
💰 {current}c ({win_pct}% W / {loss_pct}% L)
💵 $100 → ${payout_per_100} (+{roi_pct}%)
📊 Gap: {gap_to_second}pts over {runner_up.name}
🏆 {winCount} precursors | 🐋 {sentiment}
⚡ {category_volatility} volatility
→ {1-sentence verdict}
```

当展示3个以上投注建议时，将Markdown对比表替换为简洁的编号列表：

```
Quick Compare:
1. {tier_emoji} {Name} {price}c | +{roi_pct}% | {winCount}🏆
2. {tier_emoji} {Name} {price}c | +{roi_pct}% | {winCount}🏆
3. {tier_emoji} {Name} {price}c | +{roi_pct}% | {winCount}🏆
```

#### 投资组合（Telegram专属格式）

将表格替换为简洁的分配结构：

```
{Portfolio Type} — ${budget} budget

▸ {tier_emoji} {Name}: ${allocation} → ${if_win} if win
▸ {tier_emoji} {Name}: ${allocation} → ${if_win} if win
▸ {tier_emoji} {Name}: ${allocation} → ${if_win} if win

Total: ${budget} → ${total_if_win} (+{roi}%)
```

#### 前兆模拟（Telegram专属格式）

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

#### 风险等级标识（Telegram专属格式）

在展示2个以上投注建议时，使用以下简洁的标识代替Markdown表格：

```
🟢 Near lock (85%+) · 🟡 Favorite (70-84%)
🟠 Lean (45-69%) · 🔴 Toss-up (<45%)
```

#### 欢迎信息（Telegram专属格式）

使用适合单屏显示的简化版本：

```
🎬 Oscar Market Intelligence

▸ "What's happening?" — market pulse
▸ "Tell me about Chalamet" — deep dive
▸ "Best Oscar bets" — risk-tiered picks
▸ "DGA just announced, $500" — precursor sim

What are you curious about?
```