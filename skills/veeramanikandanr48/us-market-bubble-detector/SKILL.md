---
name: us-market-bubble-detector
description: 通过使用修订版的Minsky/Kindleberger框架v2.1，利用定量数据驱动的分析方法来评估市场泡沫风险。该框架优先考虑客观指标（如看涨/看跌期权比率、VIX指数、保证金债务水平、市场交易活跃度以及IPO数据），而非主观判断。同时，该框架具备严格的定性调整标准，以防止确认偏误（即投资者倾向于相信自己先前的观点）。该工具支持实际的投资决策制定，要求用户必须收集相关数据并经过机械化的评分流程。适用于用户咨询市场泡沫风险、估值问题或获利时机等情况。
---

# 美国市场泡沫检测技巧（修订版 v2.1）

## v2.1 的主要修订内容

**与 v2.0 相比的关键变化：**
1. ✅ **强制性的定量数据收集** - 使用实际测量值，而非印象或猜测
2. ✅ **明确的阈值设置** - 每个指标都有具体的数值标准
3. ✅ **两阶段评估流程** - 先进行定量评估，再根据结果进行定性调整（严格顺序）
4. ✅ **更严格的定性标准** - 最高得分为 +3 分（从 +5 分降低），需要可量化的证据
5. ✅ **防止确认偏误** - 设立明确的检查清单以避免过度评分
6. ✅ **细化的风险等级** - 新增了“高风险”等级（8-9 分），以更细致地管理风险

---

## 适用场景

在以下情况下使用此技巧：

**英文：**
- 用户询问“市场是否处于泡沫状态？”或“我们是否处于泡沫中？”
- 用户需要关于获利了结、新入场时机或卖空决策的建议
- 用户报告社会现象（如非投资者进入市场、媒体炒作、IPO 激增）
- 用户提到“这次不同”或“革命性技术”成为主流等观点
- 用户咨询现有持仓的风险管理方法

**日文：**
- ユーザーが「今の相場はバブルか？」と尋ねる
- 投資の利確・新規参入・空売りのタイミング判断を求める
- 社会現象（非投資家の参入、メディア過熱、IPO氾濫）を観察し懸念を表明
- 「今回は違う」「革命的技術」などの物語が主流化している状況を報告
- 保有ポジションのリスク管理方法を相談

---

## 评估流程（严格顺序）

### 第一阶段：强制性定量数据收集

**重要提示：** 在开始评估之前，必须收集以下数据：

#### 1.1 市场结构数据（最高优先级）
```
□ Put/Call Ratio (CBOE Equity P/C)
  - Source: CBOE DataShop or web_search "CBOE put call ratio"
  - Collect: 5-day moving average

□ VIX (Fear Index)
  - Source: Yahoo Finance ^VIX or web_search "VIX current"
  - Collect: Current value + percentile over past 3 months

□ Volatility Indicators
  - 21-day realized volatility
  - Historical position of VIX (determine if in bottom 10th percentile)
```

#### 1.2 杠杆率与持仓数据
```
□ FINRA Margin Debt Balance
  - Source: web_search "FINRA margin debt latest"
  - Collect: Latest month + Year-over-Year % change

□ Breadth (Market Participation)
  - % of S&P 500 stocks above 50-day MA
  - Source: web_search "S&P 500 breadth 50 day moving average"
```

#### 1.3 IPO 与新发行数据
```
□ IPO Count & First-Day Performance
  - Source: Renaissance Capital IPO or web_search "IPO market 2025"
  - Collect: Quarterly count + median first-day return
```

**⚠️ 未收集到第一阶段的数据前，不得进行评估**

---

### 第二阶段：定量评估（定量评分）

根据收集到的数据，按照以下标准进行机械性评分：

#### 指标 1：看跌/看涨比率（市场情绪）
```
Scoring Criteria:
- 2 points: P/C < 0.70 (excessive optimism, call-heavy)
- 1 point: P/C 0.70-0.85 (slightly optimistic)
- 0 points: P/C > 0.85 (healthy caution)

Rationale: P/C < 0.7 is historically characteristic of bubble periods
```

#### 指标 2：波动性抑制与新高点
```
Scoring Criteria:
- 2 points: VIX < 12 AND major index within 5% of 52-week high
- 1 point: VIX 12-15 AND near highs
- 0 points: VIX > 15 OR more than 10% from highs

Rationale: Extreme low volatility + highs indicates excessive complacency
```

#### 指标 3：杠杆率（保证金债务余额）
```
Scoring Criteria:
- 2 points: YoY +20% or more AND all-time high
- 1 point: YoY +10-20%
- 0 points: YoY +10% or less OR negative

Rationale: Rapid leverage increase is a bubble precursor
```

#### 指标 4：IPO 市场过热
```
Scoring Criteria:
- 2 points: Quarterly IPO count > 2x 5-year average AND median first-day return +20%+
- 1 point: Quarterly IPO count > 1.5x 5-year average
- 0 points: Normal levels

Rationale: Poor-quality IPO flood is characteristic of late-stage bubbles
```

#### 指标 5：市场广度异常（领先股数量减少）
```
Scoring Criteria:
- 2 points: New high AND < 45% of stocks above 50DMA (narrow leadership)
- 1 point: 45-60% above 50DMA (somewhat narrow)
- 0 points: > 60% above 50DMA (healthy breadth)

Rationale: Rally driven by few stocks is fragile
```

#### 指标 6：价格加速
```
Scoring Criteria:
- 2 points: Past 3-month return exceeds 95th percentile of past 10 years
- 1 point: Past 3-month return in 85-95th percentile of past 10 years
- 0 points: Below 85th percentile

Rationale: Rapid price acceleration is unsustainable
```

---

### 第三阶段：定性调整（修订版 v2.1）

**最高得分：+3 分（从 v2.0 的 +5 分降低）**

**⚠️ 防止确认偏误检查清单：**
```
Before adding ANY qualitative points:
□ Do I have concrete, measurable data? (not impressions)
□ Would an independent observer reach the same conclusion?
□ Am I avoiding double-counting with Phase 2 scores?
□ Have I documented specific evidence with sources?
```

#### 调整 A：社会渗透率（0-1 分，严格标准）
```
+1 point: ALL THREE criteria must be met:
  ✓ Direct user report of non-investor recommendations
  ✓ Specific examples with names/dates/conversations
  ✓ Multiple independent sources (minimum 3)

+0 points: Any criteria missing

⚠️ INVALID EXAMPLES:
- "AI narrative is prevalent" (unmeasurable)
- "I saw articles about retail investors" (not direct report)
- "Everyone is talking about stocks" (vague, unverified)

✅ VALID EXAMPLE:
"My barber asked about NVDA (Nov 1), dentist mentioned AI stocks (Nov 2),
Uber driver discussed crypto (Nov 3)"
```

#### 调整 B：媒体/搜索趋势（0-1 分，需要量化数据）
```
+1 point: BOTH criteria must be met:
  ✓ Google Trends showing 5x+ YoY increase (measured)
  ✓ Mainstream coverage confirmed (Time covers, TV specials with dates)

+0 points: Search trends <5x OR no mainstream coverage

⚠️ CRITICAL: "Elevated narrative" without data = +0 points

HOW TO VERIFY:
1. Search "[topic] Google Trends 2025" and document numbers
2. Search "[topic] Time magazine cover" for specific dates
3. Search "[topic] CNBC special" for episode confirmation

✅ VALID EXAMPLE:
"Google Trends: 'AI stocks' at 780 (baseline 150 = 5.2x).
Time cover 'AI Revolution' (Oct 15, 2025).
CNBC 'AI Investment Special' (3 episodes Oct 2025)."

⚠️ INVALID EXAMPLE:
"AI/technology narrative seems elevated" (unmeasurable)
```

#### 调整 C：估值脱节（0-1 分，避免重复计算）
```
+1 point: ALL criteria must be met:
  ✓ P/E >25 (if NOT already counted in Phase 2 quantitative)
  ✓ Fundamentals explicitly ignored in mainstream discourse
  ✓ "This time is different" documented in major media

+0 points: P/E <25 OR fundamentals support valuations

⚠️ SELF-CHECK QUESTIONS (if ANY is YES, score = 0):
- Is P/E already in Phase 2 quantitative scoring?
- Do companies have real earnings supporting valuations?
- Is the narrative backed by fundamental improvements?

✅ VALID EXAMPLE for +1:
"S&P P/E = 35x (vs historical 18x).
CNBC article: 'Earnings don't matter in AI era' (Oct 2025).
Bloomberg: 'Traditional metrics obsolete' (Nov 2025)."

⚠️ INVALID EXAMPLE:
"P/E 30.8 but companies have real earnings and AI has fundamental backing"
(fundamentals support = +0 points)
```

**第三阶段总得分：最高 +3 分**

---

### 第四阶段：最终判断（修订版 v2.1）

```
Final Score = Phase 2 Total (0-12 points) + Phase 3 Adjustment (0 to +3 points)
Range: 0 to 15 points

Judgment Criteria (with Risk Budget):
- 0-4 points: Normal (Risk Budget: 100%)
- 5-7 points: Caution (Risk Budget: 70-80%)
- 8-9 points: Elevated Risk (Risk Budget: 50-70%) ⚠️ NEW in v2.1
- 10-12 points: Euphoria (Risk Budget: 40-50%)
- 13-15 points: Critical (Risk Budget: 20-30%)
```

**v2.1 的关键变化：**
- 新增了“高风险”等级（8-9 分），以便更细致地评估市场状况
- 9 分不再代表极端保守的策略（之前为 40% 的风险预算）
- 在 8-9 分的情况下，允许承担 50-70% 的风险预算
- 从谨慎阶段到兴奋阶段的过渡更加平滑

---

## 数据来源（必备）

### 美国市场
- **看跌/看涨比率**：https://www.cboe.com/tradable_products/vix/
- **VIX**：Yahoo Finance (^VIX) 或 https://www.cboe.com/
- **保证金债务**：https://www.finra.org/investors/learn-to-invest/advanced-investing/margin-statistics
- **市场广度**：https://www.barchart.com/stocks/indices/sp/sp500?viewName=advanced
- **IPO**：https://www.renaissancecapital.com/IPO-Center/Stats

### 日本市场
- **日经期货 P/C**：https://www.barchart.com/futures/quotes/NO*0/options
- **JNIVE**：https://www.investing.com/indices/nikkei-volatility-historical-data
- **保证金债务**：JSF（日本证券金融）月度报告
- **市场广度**：https://en.macromicro.me/series/31841/japan-topix-index-200ma-breadth
- **IPO**：https://www.pwc.co.uk/services/audit/insights/global-ipo-watch.html

---

## 实施检查清单

使用该技巧时，请核对以下内容：

```
□ Have you collected all Phase 1 data?
□ Did you apply each indicator's threshold mechanically?
□ Did you keep qualitative evaluation within +5 point limit?
□ Are you NOT assigning points based on news article impressions?
□ Does your final score align with other quantitative frameworks?
```

---

## 重要原则（修订版）

### 1. 数据优先于印象
在没有定量数据的情况下，不要仅依赖“大量新闻报道”或“专家的谨慎看法”。

### 2. 严格顺序：定量 → 定性
始终按照以下顺序进行评估：第一阶段（数据收集）→ 第二阶段（定量评估）→ 第三阶段（定性调整）。

### 3. 主观指标的上限
定性调整的总分上限为 +5 分，不能凌驾于定量评估之上。

### 4. “大众观点”需谨慎对待
在没有非投资者的直接建议之前，不要轻易接受大众观点。

---

## 常见错误及解决方法（修订版）

### 错误 1：仅依据新闻文章进行评估
❌ “关于 Takaichi Trade 的报道很多” → 给出 2 分（媒体饱和度）
✅ 核实 Google Trends 的数据 → 用实际测量值进行评估

### 错误 2：对专家评论反应过度
❌ “市场过热”的警告 → 判断为兴奋阶段
✅ 用看跌/看涨比率、VIX 和保证金债务等可量化数据来做出判断

### 错误 3：对价格上涨情绪化反应
❌ 一天内价格上涨 4.5% → 给出 2 分（价格加速）
✅ 核实过去 10 年的价格走势 → 进行客观评估

### 错误 4：仅依据估值进行判断
❌ 市盈率 17 → 给出 2 分（估值脱节）
✅ 结合市盈率和其他定量指标进行综合判断

---

## 根据市场状况推荐的行动（修订版 v2.1）

### 正常状态（0-4 分）
**风险预算：100%**
- 继续采用常规投资策略
- 设置 ATR 2.0 倍的止损点
- 采用阶梯式获利了结规则（每获利 20% 退出 25%）

**不建议卖空**
- 不满足综合条件（0/7 项）

### 谨慎状态（5-7 分）
**风险预算：70-80%**
- 开始部分获利了结（减少 20-30% 的持仓）
- 将 ATR 缩小至 1.8 倍
- 新建头寸的规模减少 50%

**不建议卖空**
- 等待更明确的反转信号

### 高风险状态（8-9 分）⚠️ 新增内容
**风险预算：50-70%**
- 加快获利了结（减少 30-50% 的持仓）
- 将 ATR 缩小至 1.6 倍
- 新建头寸时需高度谨慎，只选择优质资产
- 开始为未来的机会储备现金

**卖空建议：**
- 在满足至少 2/7 项综合条件后考虑
- 建立小规模试探性头寸（正常规模的 10-15%）
- 设置严格的止损点（ATR 2.0 倍）

**新增阶段的理由：**
- 此阶段表示高度谨慎，但并非极端保守
- 市场出现预警信号，但尚未出现崩溃迹象
- 在保持对优质资产敞口的同时，增强灵活性

### 兴奋状态（10-12 分）
**风险预算：40-50%**
- 加快阶梯式获利了结（减少 50-60% 的持仓）
- 将 ATR 缩小至 1.5 倍
- 除非市场出现大幅回调，否则不新建多头头寸

**卖空建议：**
- 在满足至少 3/7 项综合条件后考虑
- 建立小规模头寸（正常规模的 20-25%）
- 仅承担有限的风险

### 危险状态（13-15 分）
**风险预算：20-30%**
- 进行大规模获利了结或完全对冲
- 将 ATR 缩小至 1.2 倍或设置固定止损点
- 进入现金保存模式，为可能的重大市场变动做好准备

**卖空建议：**
- 在满足至少 5/7 项综合条件后考虑
- 逐步增加头寸规模
- 设置严格的止损点（ATR 1.5 倍或更高）

### 卖空的综合条件（7 项）

只有在满足以下至少 3 项条件后，才考虑卖空：

```
1. Weekly chart shows lower highs
2. Volume peaks out
3. Leverage indicators drop sharply (margin debt decline)
4. Media/search trends peak out
5. Weak stocks start to break down first
6. VIX surges (spike above 20)
7. Fed/policy shift signals
```

---

## 评估报告格式（v2.1）

```markdown
# [Market Name] Bubble Evaluation Report (Revised v2.1)

## Overall Assessment
- Final Score: X/15 points (v2.1: max reduced from 16)
- Phase: [Normal/Caution/Elevated Risk/Euphoria/Critical]
- Risk Level: [Low/Medium/Medium-High/High/Extremely High]
- Evaluation Date: YYYY-MM-DD

## Quantitative Evaluation (Phase 2)

| Indicator | Measured Value | Score | Rationale |
|-----------|----------------|-------|-----------|
| Put/Call | [value] | [0-2] | [reason] |
| VIX + Highs | [value] | [0-2] | [reason] |
| Margin YoY | [value] | [0-2] | [reason] |
| IPO Heat | [value] | [0-2] | [reason] |
| Breadth | [value] | [0-2] | [reason] |
| Price Accel | [value] | [0-2] | [reason] |

**Phase 2 Total: X/12 points**

## Qualitative Adjustment (Phase 3) - STRICT CRITERIA

**⚠️ Confirmation Bias Check:**
- [ ] All qualitative points have measurable evidence
- [ ] No double-counting with Phase 2
- [ ] Independent observer would agree

### A. Social Penetration (0-1 points)
- Evidence: [REQUIRED: Direct user reports with dates/names]
- Score: [+0 or +1]
- Justification: [Must meet ALL three criteria]

### B. Media/Search Trends (0-1 points)
- Google Trends Data: [REQUIRED: Measured numbers, YoY multiplier]
- Mainstream Coverage: [REQUIRED: Specific Time covers, TV specials with dates]
- Score: [+0 or +1]
- Justification: [Must have 5x+ search AND mainstream confirmation]

### C. Valuation Disconnect (0-1 points)
- P/E Ratio: [Current value]
- Fundamental Backing: [Yes/No - if Yes, score = 0]
- Narrative Analysis: [REQUIRED: Specific media quotes ignoring fundamentals]
- Score: [+0 or +1]
- Justification: [Must show fundamentals actively ignored]

**Phase 3 Total: +X/3 points (max reduced from +5 in v2.0)**

## Recommended Actions

**Risk Budget: X%** (Phase: [Normal/Caution/Elevated Risk/Euphoria/Critical])
- [Specific action 1]
- [Specific action 2]
- [Specific action 3]

**Short-Selling: [Not Allowed/Consider Cautiously/Active/Recommended]**
- Composite conditions: X/7 met
- Minimum required: [0/2/3/5] for current phase

## Key Changes in v2.1
- Stricter qualitative criteria (max +3, down from +5)
- Added "Elevated Risk" phase for 8-9 points
- Confirmation bias prevention checklist
- All qualitative points require measurable evidence
```

---

## 参考文档

### `references/implementation_guide.md`（英文） - **推荐首次使用**
- 逐步的评估流程及强制性数据收集要求
- 不良案例与成功案例对比
- 自我检查质量标准（4 个等级）
- 审查过程中的警示信号
- 客观评估的最佳实践

### `references/bubble_framework.md`（日文）
- 详细的理论框架
- Minsky/Kindleberger 模型的解释
- 行为心理学要素

### `references/historical_cases.md`（日文）
- 过去市场泡沫案例的分析
- 互联网泡沫、加密货币泡沫、疫情期间的泡沫
- 共同模式的提取

### `references/quick_reference.md`（日文）/ `references/quick_reference_en.md`（英文）
- 日常使用检查清单
- 紧急情况下的快速评估工具
- 快速评分指南
- 关键数据来源

### 使用参考文档的时机
- **首次使用或需要详细指导时**：阅读 `implementation_guide.md`
- **需要理论背景时**：阅读 `bubble_framework.md`
- **需要历史背景时**：阅读 `historical_cases.md`
- **日常操作时**：阅读 `quick_reference.md`（日文）或 `quick_reference_en.md`

---

## v2.1 修订版的要点总结

**v2.0 的问题（2025 年 11 月发现）：**
- 定性调整过于宽松（最高分 +5 分）
- “人工智能相关话题”被过度重视 → 给分 +1 分（无数据支持）
- “市盈率 30.8” → 给分 +1 分（与定量数据重复计算）
- **结果：总分为 11/16 分，结论过于悲观且缺乏依据**

**v2.1 的改进措施：**
- 定性调整更加严格（最高分 +3 分）
- “人工智能相关话题”无数据支持时不得得分
- “市盈率 30.8 但有基本面支撑”时得分为 0 分
- **结果：总分为 9/15 分，评估更加客观**

**主要改进点：**
1. **防止确认偏误**：在添加定性分数前设置明确检查清单
2. **需要可量化证据**：没有具体数据时不得得分（如 Google Trends 数据、媒体报道）
3. **避免重复计算**：估值不得与第二阶段的定量数据重复计算
4. **细化的风险等级**：新增“高风险”等级，以便更精确地评估市场状况
5. **平衡风险预算**：9 分对应 50-70% 的风险预算（而非之前的极端保守策略）

**核心原则：**
> “我们信任上帝；其他人必须提供数据。”——W. Edwards Deming

**2025 年的启示：**
即使是基于数据的框架，也可能受到主观定性评估的影响。
v2.1 版要求所有定性评估都有可量化的证据支持。
独立观察者必须能够验证每一项调整的合理性。

---

**版本历史：**
- **v2.0**（2025 年 10 月 27 日）：强制要求收集定量数据
- **v2.1**（2025 年 11 月 3 日）：加强定性标准，防止确认偏误，细化风险等级

**修订原因：**
- 防止因未经验证的“主观观点”和重复计算而导致过度评分
- 确保所有市场泡沫风险评估都经过独立验证，避免确认偏误。