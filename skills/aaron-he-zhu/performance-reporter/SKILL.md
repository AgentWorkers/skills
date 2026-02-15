---
name: performance-reporter
description: 生成全面的SEO和GEO性能报告，涵盖排名、流量、反向链接以及AI可见性指标。为利益相关者提供执行摘要和详细分析报告。
geo-relevance: "medium"
---

# 性能报告工具

该工具能够生成全面的SEO和GEO性能报告，将多种指标整合为可操作的洞察结果。它提供执行摘要、详细分析以及可视化数据展示，以便与利益相关者进行沟通。

## 适用场景

- 月度/季度SEO报告
- 执行层利益相关者更新
- 机构为客户提供的报告
- 跟踪营销活动效果
- 综合多种SEO指标
- 制作GEO可见性报告
- 记录SEO工作的投资回报率（ROI）

## 工具功能

1. **数据聚合**：整合多个SEO数据源
2. **趋势分析**：识别各项指标之间的模式
3. **执行摘要**：生成高层次的概览
4. **可视化报告**：以清晰的形式呈现数据
5. **基准对比**：根据目标和竞争对手进行跟踪
6. **内容质量监控**：整合审核页面的CORE-EEAT评分
7. **ROI计算**：衡量SEO投资回报
8. **建议**：基于数据提出行动方案

## 使用方法

### 生成性能报告

```
Create an SEO performance report for [domain] for [time period]
```

### 执行摘要

```
Generate an executive summary of SEO performance for [month/quarter]
```

### 具体报告类型

```
Create a GEO visibility report for [domain]
```

```
Generate a content performance report
```

## 数据来源

> 请参阅[CONNECTORS.md](../../CONNECTORS.md)以获取工具类别的占位符信息。

**当连接到以下工具时：**
- **分析工具**：自动聚合来自分析工具的流量数据
- **搜索控制台**：来自搜索控制台的搜索性能数据
- **SEO工具**：来自SEO工具的排名和反向链接数据
- **AI监控工具**：来自AI监控工具的GEO可见性数据。这些工具将生成包含历史趋势的综合性多源报告。

**仅使用手动数据时：**
- 要求用户提供以下数据：
  - 分析工具的截图或流量数据导出（会话数、用户数、转化次数）
  - 搜索控制台数据（展示次数、点击次数、平均排名）
  - 报告期间的关键词排名数据
  - 反向链接指标（引用域名、新增/丢失的链接）
  - 关键绩效指标和用于比较的目标
  - 如果需要跟踪GEO指标，请提供AI引用数据

使用提供的数据进行完整分析。在输出中注明哪些指标是自动收集的，哪些是用户提供的。

## 操作步骤

当用户请求性能报告时：

1. **定义报告参数**

   ```markdown
   ## Report Configuration
   
   **Domain**: [domain]
   **Report Period**: [start date] to [end date]
   **Comparison Period**: [previous period for comparison]
   **Report Type**: [Monthly/Quarterly/Annual/Custom]
   **Audience**: [Executive/Technical/Client]
   **Focus Areas**: [Rankings/Traffic/Content/Backlinks/GEO]
   ```

2. **生成执行摘要**

   ```markdown
   # SEO Performance Report
   
   **Domain**: [domain]
   **Period**: [date range]
   **Prepared**: [date]
   
   ---
   
   ## Executive Summary
   
   ### Overall Performance: [Excellent/Good/Needs Attention/Critical]
   
   **Key Highlights**:
   
   🟢 **Wins**:
   - [Win 1 - e.g., "Organic traffic increased 25%"]
   - [Win 2 - e.g., "3 new #1 rankings achieved"]
   - [Win 3 - e.g., "Conversion rate improved 15%"]
   
   🟡 **Watch Areas**:
   - [Area 1 - e.g., "Mobile rankings declining slightly"]
   - [Area 2 - e.g., "Competitor gaining ground on key terms"]
   
   🔴 **Action Required**:
   - [Issue 1 - e.g., "Technical SEO audit needed"]
   
   ### Key Metrics at a Glance
   
   | Metric | This Period | Last Period | Change | Target | Status |
   |--------|-------------|-------------|--------|--------|--------|
   | Organic Traffic | [X] | [Y] | [+/-Z%] | [T] | ✅/⚠️/❌ |
   | Keyword Rankings (Top 10) | [X] | [Y] | [+/-Z] | [T] | ✅/⚠️/❌ |
   | Organic Conversions | [X] | [Y] | [+/-Z%] | [T] | ✅/⚠️/❌ |
   | Domain Authority | [X] | [Y] | [+/-Z] | [T] | ✅/⚠️/❌ |
   | AI Citations | [X] | [Y] | [+/-Z%] | [T] | ✅/⚠️/❌ |
   
   ### SEO ROI
   
   **Investment**: $[X] (content, tools, effort)
   **Organic Revenue**: $[Y]
   **ROI**: [Z]%
   ```

3. **报告自然搜索流量表现**

   ```markdown
   ## Organic Traffic Analysis
   
   ### Traffic Overview
   
   | Metric | This Period | vs Last Period | vs Last Year |
   |--------|-------------|----------------|--------------|
   | Sessions | [X] | [+/-Y%] | [+/-Z%] |
   | Users | [X] | [+/-Y%] | [+/-Z%] |
   | Pageviews | [X] | [+/-Y%] | [+/-Z%] |
   | Avg. Session Duration | [X] | [+/-Y%] | [+/-Z%] |
   | Bounce Rate | [X]% | [+/-Y%] | [+/-Z%] |
   | Pages per Session | [X] | [+/-Y] | [+/-Z] |
   
   ### Traffic Trend
   
   ```
   [月份1]  ████████████████████ [X]
   [月份2]  █████████████████████ [Y]
   [月份3]  ███████████████████████ [Z]
   [当前]  ████████████████████████ [W]
   ```
   
   ### Traffic by Source
   
   | Channel | Sessions | % of Total | Change |
   |---------|----------|------------|--------|
   | Organic Search | [X] | [Y]% | [+/-Z%] |
   | Direct | [X] | [Y]% | [+/-Z%] |
   | Referral | [X] | [Y]% | [+/-Z%] |
   | Social | [X] | [Y]% | [+/-Z%] |
   
   ### Top Performing Pages
   
   | Page | Sessions | Change | Conversions |
   |------|----------|--------|-------------|
   | [Page 1] | [X] | [+/-Y%] | [Z] |
   | [Page 2] | [X] | [+/-Y%] | [Z] |
   | [Page 3] | [X] | [+/-Y%] | [Z] |
   
   ### Traffic by Device
   
   | Device | Sessions | Change | Conv. Rate |
   |--------|----------|--------|------------|
   | Desktop | [X] ([Y]%) | [+/-Z%] | [%] |
   | Mobile | [X] ([Y]%) | [+/-Z%] | [%] |
   | Tablet | [X] ([Y]%) | [+/-Z%] | [%] |
   ```

4. **报告关键词排名**

   ```markdown
   ## Keyword Ranking Performance
   
   ### Rankings Overview
   
   | Position Range | Keywords | Change | Traffic Impact |
   |----------------|----------|--------|----------------|
   | Position 1 | [X] | [+/-Y] | [Z] sessions |
   | Position 2-3 | [X] | [+/-Y] | [Z] sessions |
   | Position 4-10 | [X] | [+/-Y] | [Z] sessions |
   | Position 11-20 | [X] | [+/-Y] | [Z] sessions |
   | Position 21-50 | [X] | [+/-Y] | [Z] sessions |
   
   ### Ranking Distribution Change
   
   ```
   上一期： ▓▓▓▓░░░░░░░░░░░░
   本期： ▓▓▓▓▓▓░░░░░░░░░
                 ↑ 更多关键词进入顶级排名

5. **报告GEO/AI表现**

   ```markdown
   ## GEO (AI Visibility) Performance
   
   ### AI Citation Overview
   
   | Metric | This Period | Last Period | Change |
   |--------|-------------|-------------|--------|
   | Keywords with AI Overview | [X]/[Y] | [X]/[Y] | [+/-Z] |
   | Your AI Citations | [X] | [Y] | [+/-Z%] |
   | Citation Rate | [X]% | [Y]% | [+/-Z%] |
   | Avg Citation Position | [X] | [Y] | [+/-Z] |
   
   ### AI Citation by Topic
   
   | Topic Cluster | Opportunities | Citations | Rate |
   |---------------|---------------|-----------|------|
   | [Topic 1] | [X] | [Y] | [Z]% |
   | [Topic 2] | [X] | [Y] | [Z]% |
   | [Topic 3] | [X] | [Y] | [Z]% |
   
   ### GEO Wins This Period
   
   | Query | Citation Status | Source Page | Impact |
   |-------|-----------------|-------------|--------|
   | [query 1] | 🆕 New citation | [page] | High visibility |
   | [query 2] | ⬆️ Improved position | [page] | Better exposure |
   
   ### GEO Optimization Opportunities
   
   | Query | AI Overview | You Cited? | Gap | Action |
   |-------|-------------|------------|-----|--------|
   | [query] | Yes | No | [gap] | [action] |
   ```

6. **报告域名权威度（CITE评分）**

   如果之前已经使用`domain-authority-auditor`工具进行了域名权威度审计，请包括域名权威度的变化趋势：

   ```markdown
   ## Domain Authority (CITE Score)

   ### CITE Score Summary

   | Metric | This Period | Last Period | Change |
   |--------|-------------|-------------|--------|
   | CITE Score | [X]/100 | [Y]/100 | [+/-Z] |
   | C — Citation | [X]/100 | [Y]/100 | [+/-Z] |
   | I — Identity | [X]/100 | [Y]/100 | [+/-Z] |
   | T — Trust | [X]/100 | [Y]/100 | [+/-Z] |
   | E — Eminence | [X]/100 | [Y]/100 | [+/-Z] |

   **Veto Status**: ✅ No triggers / ⚠️ [item] triggered

   ### Key Changes

   - [Notable improvement or concern 1]
   - [Notable improvement or concern 2]

   _For full 40-item evaluation, run `/seo:audit-domain`_
   ```

**注意**：如果之前没有进行过CITE审计，请将此部分标记为“尚未评估 — 需要运行`domain-authority-auditor`以获取基准数据”，并跳过此步骤。

7. **内容质量（CORE-EEAT评分）**

   如果已经使用`/seo:audit-page`工具对关键页面进行了内容质量审计，请包括内容质量指标：

   ```markdown
   ## Content Quality (CORE-EEAT Score)

   ### Content Quality Summary

   | Metric | Value |
   |--------|-------|
   | Pages Audited | [count] |
   | Average CORE-EEAT Score | [score]/100 ([rating]) |
   | Average GEO Score (CORE) | [score]/100 |
   | Average SEO Score (EEAT) | [score]/100 |
   | Veto Items Triggered | [count] ([item IDs]) |

   ### Dimension Averages Across Audited Pages

   | Dimension | Average Score | Trend |
   |-----------|--------------|-------|
   | C — Contextual Clarity | [score] | [↑/↓/→] |
   | O — Organization | [score] | [↑/↓/→] |
   | R — Referenceability | [score] | [↑/↓/→] |
   | E — Exclusivity | [score] | [↑/↓/→] |
   | Exp — Experience | [score] | [↑/↓/→] |
   | Ept — Expertise | [score] | [↑/↓/→] |
   | A — Authority | [score] | [↑/↓/→] |
   | T — Trust | [score] | [↑/↓/→] |

   ### Key Content Quality Changes

   - [Notable score changes since last report]
   - [Pages with significant quality improvements/declines]

   _For full 80-item evaluation, run `/seo:audit-page` on individual pages. See CORE-EEAT benchmark for methodology._
   ```

**注意**：如果之前没有进行过内容质量审计，请将此部分标记为“内容质量尚未评估 — 需要对关键着陆页运行`/seo:audit-page`以建立基准数据”，并跳过此步骤。

8. **报告反向链接表现**

   ```markdown
   ## Backlink Performance
   
   ### Link Profile Summary
   
   | Metric | This Period | Last Period | Change |
   |--------|-------------|-------------|--------|
   | Total Backlinks | [X] | [Y] | [+/-Z] |
   | Referring Domains | [X] | [Y] | [+/-Z] |
   | Domain Authority | [X] | [Y] | [+/-Z] |
   | Avg. Link DA | [X] | [Y] | [+/-Z] |
   
   ### Link Acquisition
   
   | Period | New Links | Lost Links | Net |
   |--------|-----------|------------|-----|
   | Week 1 | [X] | [Y] | [+/-Z] |
   | Week 2 | [X] | [Y] | [+/-Z] |
   | Week 3 | [X] | [Y] | [+/-Z] |
   | Week 4 | [X] | [Y] | [+/-Z] |
   | **Total** | **[X]** | **[Y]** | **[+/-Z]** |
   
   ### Notable New Links
   
   | Source | DA | Type | Value |
   |--------|-----|------|-------|
   | [domain 1] | [DA] | [type] | High |
   | [domain 2] | [DA] | [type] | High |
   
   ### Competitive Position
   
   Your referring domains rank #[X] of [Y] competitors.
   ```

9. **报告内容表现**

   ```markdown
   ## Content Performance
   
   ### Content Publishing Summary
   
   | Metric | This Period | Last Period | Target |
   |--------|-------------|-------------|--------|
   | New articles published | [X] | [Y] | [Z] |
   | Content updates | [X] | [Y] | [Z] |
   | Total word count | [X] | [Y] | - |
   
   ### Top Performing Content
   
   | Content | Traffic | Rankings | Conversions | Status |
   |---------|---------|----------|-------------|--------|
   | [Title 1] | [X] | [Y] keywords | [Z] | ⭐ Top performer |
   | [Title 2] | [X] | [Y] keywords | [Z] | 📈 Growing |
   | [Title 3] | [X] | [Y] keywords | [Z] | ✅ Stable |
   
   ### Content Needing Attention
   
   | Content | Issue | Traffic Change | Action |
   |---------|-------|----------------|--------|
   | [Title] | [issue] | -[X]% | [action] |
   
   ### Content ROI
   
   | Content Piece | Investment | Traffic Value | ROI |
   |---------------|------------|---------------|-----|
   | [Title 1] | $[X] | $[Y] | [Z]% |
   | [Title 2] | $[X] | $[Y] | [Z]% |
   ```

10. **生成建议**

   ```markdown
   ## Recommendations & Next Steps
   
   ### Immediate Actions (This Week)
   
   | Priority | Action | Expected Impact | Owner |
   |----------|--------|-----------------|-------|
   | 🔴 High | [Action 1] | [Impact] | [Owner] |
   | 🔴 High | [Action 2] | [Impact] | [Owner] |
   
   ### Short-term (This Month)
   
   | Priority | Action | Expected Impact | Owner |
   |----------|--------|-----------------|-------|
   | 🟡 Medium | [Action 1] | [Impact] | [Owner] |
   | 🟡 Medium | [Action 2] | [Impact] | [Owner] |
   
   ### Long-term (This Quarter)
   
   | Priority | Action | Expected Impact | Owner |
   |----------|--------|-----------------|-------|
   | 🟢 Planned | [Action 1] | [Impact] | [Owner] |
   
   ### Goals for Next Period
   
   | Metric | Current | Target | Action to Achieve |
   |--------|---------|--------|-------------------|
   | Organic Traffic | [X] | [Y] | [action] |
   | Keywords Top 10 | [X] | [Y] | [action] |
   | AI Citations | [X] | [Y] | [action] |
   | Referring Domains | [X] | [Y] | [action] |
   ```

11. **编制完整报告**

   ```markdown
   # [Company] SEO & GEO Performance Report
   
   ## [Month/Quarter] [Year]
   
   ---
   
   ### Table of Contents
   
   1. Executive Summary
   2. Organic Traffic Performance
   3. Keyword Rankings
   4. GEO/AI Visibility
   5. Domain Authority (CITE Score)
   6. Content Quality (CORE-EEAT Score)
   7. Backlink Analysis
   8. Content Performance
   9. Technical Health
   10. Competitive Landscape
   11. Recommendations
   12. Appendix
   
   ---
   
   [Include all sections from above]
   
   ---
   
   ## Appendix
   
   ### Data Sources
   - ~~analytics (traffic and conversion data)
   - ~~search console (search performance)
   - ~~SEO tool (rankings and backlinks)
   - ~~AI monitor (GEO metrics)

   ### Methodology
   [Explain how metrics were calculated]

   ### Glossary
   - **GEO**: Generative Engine Optimization
   - **DA**: Domain Authority
   - [Additional terms]
   ```

## 验证要点

### 输入验证
- [ ] 报告周期明确，并与对比周期一致
- [ ] 所有所需的数据来源均已获取或已注明替代方案
- [ ] 确定了目标受众（执行层/技术团队/客户）
- [ ] 已确定用于基准测试的性能目标和KPI

### 输出验证
- [ ] 每个指标都标明了数据来源和收集日期
- [ ] 趋势包括同比对比
- [ ] 建议具体、有优先级且可执行
- [ ] 每个数据点的来源都明确标注（分析工具数据、搜索控制台数据、SEO工具数据、用户提供的数据或估算值）

## 示例

**用户请求**：“为cloudhosting.com生成2025年1月的月度SEO报告”

**输出示例**：

```markdown
# CloudHosting SEO & GEO Performance Report

**Domain**: cloudhosting.com
**Period**: January 1-31, 2025
**Comparison**: vs December 2024
**Prepared**: February 3, 2025

---

## Executive Summary

### Overall Performance: Good

**Key Highlights**:

🟢 **Wins**:
- Organic traffic increased 15.3% (45,200 → 52,100 sessions)
- 4 new Top 10 keyword rankings in "cloud hosting" cluster
- Organic conversions up 11.8% (612 → 684 trial signups)

🟡 **Watch Areas**:
- Mobile page speed declining (LCP 3.1s → 3.4s)
- Competitor SiteGround gaining on "managed cloud hosting" terms

🔴 **Action Required**:
- Fix crawl errors on /pricing/ pages (37 404s detected)

### Key Metrics at a Glance

| Metric | Jan 2025 | Dec 2024 | Change | Target | Status |
|--------|----------|----------|--------|--------|--------|
| Organic Traffic | 52,100 | 45,200 | +15.3% | 50,000 | ✅ |
| Keywords Top 10 | 87 | 79 | +8 | 90 | ⚠️ |
| Organic Conversions | 684 | 612 | +11.8% | 700 | ⚠️ |
| Domain Rating | 54 | 53 | +1 | 55 | ⚠️ |
| AI Citations | 18 | 12 | +50.0% | 20 | ⚠️ |

### SEO ROI

**Investment**: $8,200 (content production, tools, link building)
**Organic Revenue**: $41,040 (684 trials × 12% close rate × $500 MRR)
**ROI**: 400%

---

## Organic Traffic Analysis

### Traffic Overview

| Metric | Jan 2025 | vs Dec 2024 | vs Jan 2024 |
|--------|----------|-------------|-------------|
| Sessions | 52,100 | +15.3% | +38.2% |
| Users | 41,680 | +14.1% | +35.7% |
| Pageviews | 98,990 | +12.6% | +29.4% |
| Avg. Session Duration | 2m 48s | +6.2% | +18.3% |
| Bounce Rate | 42.3% | -3.1% | -8.7% |

### Top Performing Pages

| Page | Sessions | Change | Conversions |
|------|----------|--------|-------------|
| /guide/cloud-hosting | 8,420 | +22.1% | 142 |
| /compare/aws-vs-gcp | 5,310 | +31.4% | 87 |
| /pricing | 4,890 | +9.8% | 201 |

---

## GEO (AI Visibility) Performance

### AI Citation Overview

| Metric | Jan 2025 | Dec 2024 | Change |
|--------|----------|----------|--------|
| Keywords with AI Overview | 34/120 | 28/120 | +6 |
| Your AI Citations | 18 | 12 | +50.0% |
| Citation Rate | 15.0% | 10.0% | +5.0% |
| Avg Citation Position | 2.4 | 3.1 | +0.7 |

### GEO Wins This Period

| Query | Citation Status | Source Page | Impact |
|-------|-----------------|-------------|--------|
| "best cloud hosting for startups" | 🆕 New citation | /guide/cloud-hosting | High visibility |
| "cloud hosting vs shared hosting" | ⬆️ Position 4→2 | /compare/cloud-vs-shared | Better exposure |
| "managed cloud hosting benefits" | 🆕 New citation | /features/managed | High visibility |

---

## Domain Authority (CITE Score)

### CITE Score Summary

| Metric | Jan 2025 | Dec 2024 | Change |
|--------|----------|----------|--------|
| CITE Score | 71/100 | 67/100 | +4 |
| C — Citation | 68/100 | 65/100 | +3 |
| I — Identity | 55/100 | 52/100 | +3 |
| T — Trust | 82/100 | 80/100 | +2 |
| E — Eminence | 61/100 | 58/100 | +3 |

**Veto Status**: ✅ No triggers

_For full 40-item evaluation, run `/seo:audit-domain`_

---

## Recommendations & Next Steps

### Immediate Actions (This Week)

| Priority | Action | Expected Impact | Owner |
|----------|--------|-----------------|-------|
| P0 | Fix 37 crawl errors on /pricing/ pages | Recover ~800 lost sessions/month | Dev team |

### Short-term (This Month)

| Priority | Action | Expected Impact | Owner |
|----------|--------|-----------------|-------|
| P1 | Optimize mobile LCP on top 10 landing pages | Improve mobile rankings for 15+ keywords | Dev team |
| P1 | Publish 3 comparison pages targeting AI Overview queries | +5-8 new AI citations | Content team |

### Long-term (This Quarter)

| Priority | Action | Expected Impact | Owner |
|----------|--------|-----------------|-------|
| P2 | Build Wikidata entry and Schema.org for CloudHost Inc. | Strengthen CITE Identity score by +10 pts | SEO lead |
```

## 根据受众定制的报告模板

### 执行报告（1页）

重点内容：业务影响、ROI、主要指标、关键建议

### 营销团队报告（3-5页）

重点内容：详细指标、内容表现、营销活动结果

### 技术SEO报告（5-10页）

重点内容：爬虫数据、技术问题、详细排名、反向链接分析

### 客户报告（2-3页）

重点内容：达成目标的进度、成功案例、具体建议

## 成功技巧

1. **先提供洞察**：从重要的信息开始，而不是直接展示原始数据
2. **数据可视化**：图表和图形有助于更好地理解数据
3. **对比不同时间段**：上下文使数据更有意义
4. **包含行动建议**：每份报告都应能推动决策
5. **根据受众定制**：执行层和技术团队需要的信息不同
6. **跟踪GEO指标**：AI可见性越来越重要

## SEO/GEO指标定义及基准

### 自然搜索指标

| 指标 | 定义 | 合适范围 | 警示值 | 来源 |
|--------|-----------|-----------|---------|--------|
| 自然搜索会话数 | 来自自然搜索的访问量 | 每月增长 | 下降超过10% | 分析工具 |
| 关键词可见性 | 目标关键词在前100名中的占比 | 超过60% | 低于40% | SEO工具 |
| 平均排名 | 被跟踪关键词的平均排名 | 低于20 | 高于30 | 搜索控制台 |
| 自然搜索点击率 | 搜索中的点击次数与展示次数的比率 | 超过3% | 低于1.5% | 搜索控制台 |
| 被索引的页面数 | 被谷歌索引的页面数 | 持续增长 | 持续减少 | 搜索控制台 |
| 自然转化率 | 自然搜索转化次数与自然搜索会话数的比率 | 超过2% | 低于0.5% | 分析工具 |
| 非品牌自然流量 | 自然流量中去除品牌搜索后的流量 | 占自然流量的比例超过50% | 低于30% | 分析工具 |

### GEO/AI可见性指标

| 指标 | 定义 | 合适范围 | 警示值 | 来源 |
|--------|-----------|-----------|---------|--------|
| AI引用率 | 被监控查询中引用您内容的比例 | 超过20% | 低于5% | AI监控工具 |
| AI引用排名 | 在AI回答中被引用的平均排名 | 前3个来源 | 未被引用 | AI监控工具 |
| AI答案覆盖率 | 您的主题在AI答案中出现的比例 | 持续增长 | 持续下降 | AI监控工具 |
| 品牌在AI中的提及次数 | 您的品牌在AI回答中被提及的次数 | 持续增长 | 为零 | AI监控工具 |

### 域名权威度指标

| 指标 | 定义 | 合适范围 | 警示值 | 来源 |
|--------|-----------|-----------|---------|--------|
| 域名评分/权威度 | 域名的整体强度 | 持续增长 | 持续下降 | SEO工具 |
| 引用域名 | 链接到您的唯一域名数量 | 每月增长 | 每月减少超过10% | 链接数据库 |
| 反向链接增长率 | 每月的新增反向链接数量 | 正值 | 负值趋势 | 链接数据库 |
| 有害链接比例 | 有害链接与总链接的比例 | 低于5% | 高于10% | 链接数据库 |

## 根据受众定制的报告模板

### 执行报告（高管层/领导层）

**重点内容：**业务成果、ROI、竞争地位
**长度：**1页 + 附录
**频率：**每月或每季度

| 部分 | 内容 |
|---------|---------|
| 流量与收入 | 自然搜索流量趋势及带来的收入 |
| 竞争地位 | 与前三名竞争对手的可见性对比 |
| AI可见性 | AI引用趋势及覆盖范围 |
| 关键成果 | 产生业务影响的关键成果 |
| 风险 | 需要解决的三大问题 |
| 投资需求 | 下一阶段所需的资源 |

### 营销团队报告

**重点内容：**渠道表现、内容效果、技术状况
**长度：**2-3页
**频率：**每月

| 部分 | 内容 |
|---------|---------|
| 关键词表现 | 排名变化、新发现的关键词 |
| 内容表现 | 流量最高、参与度最高、转化率最高的页面 |
| 技术状况 | 爬虫错误、页面速度、索引情况 |
| 反向链接情况 | 新增链接、丢失的链接、质量评估 |
| GEO表现 | AI引用变化、新引用 |
| 行动事项 | 优先级排序的任务列表 |

### 技术SEO报告

**重点内容：**可爬取性、索引情况、页面速度、错误情况
**长度：**详细
**频率：**每周或每两周

| 部分 | 内容 |
|---------|---------|
| 爬虫统计 | 爬取的页面数、错误情况、爬虫预算使用情况 |
| 索引情况 | 被索引的页面、被排除的页面、出错的页面 |
| 核心网页健康指标 | LCP、CLS、INP的趋势 |
| 错误日志 | 新出现的4xx/5xx错误及解决状态 |
| 结构验证 | 新出现的警告、富结果资格 |
| 技术问题 | 按优先级排列的未解决问题 |

## 趋势分析框架

### 同比分析

| 分析方法 | 适用场景 | 限制 |
|-----------|---------|-----------|
| 周与周（WoW） | 发现突然变化 | 受工作日模式影响，数据波动较大 |
| 月与月（MoM） | 识别趋势 | 季节性偏差 |
| 年与年（YoY） | 考虑季节性因素 | 无法反映最新变化 |
| 连续30天平均值 | 平滑数据波动 | 可能滞后于实际变化 |

### 趋势解读指南

| 趋势 | 可能原因 | 建议措施 |
|---------|-------------|-------------------|
| 持续增长 | 策略有效 | 继续执行，优化表现优异的部分 |
| 突然上升后下降 | 内容传播迅速或算法波动 | 调查原因，如可重复则继续优化 |
| 逐渐下降 | 内容质量下降、竞争加剧、技术问题 | 需要进行全面审计 |
| 横盘 | 现有策略达到极限 | 需要开发新的内容领域或链接策略 |
| 季节性波动 | 行业/需求周期 | 根据周期规划内容发布计划 |

## SEO归因指南

### SEO中的归因挑战

| 挑战 | 影响 | 应对措施 |
|----------|--------|-----------|
| 长转化路径 | SEO很少获得最终转化的功劳 | 使用辅助转化报告 |
| 品牌与非品牌内容 | 品牌搜索会影响自然搜索数据 | 始终区分品牌内容和非品牌内容 |
| 跨设备转化路径 | 移动搜索到桌面设备的转化 | 启用跨设备跟踪 |
| SEO与付费推广的交叉影响 | 是否存在互相影响 | 测试关闭针对品牌关键词的付费推广 |
| 内容对销售的辅助作用 | 难以准确归因 | 在CRM系统中追踪内容的触达情况 |

## 参考资料

- [KPI定义](../../references/kpi-definitions.md) — 完整的SEO/GEO指标定义，包括基准值、合适范围和警告阈值
- [报告模板](./references/report-templates.md) — 根据受众定制的报告模板（执行层、营销团队、技术团队、客户）

## 相关工具

- [内容质量审计工具](../../cross-cutting/content-quality-auditor/) — 将CORE-EEAT评分作为页面级别的内容质量KPI
- [域名权威度审计工具](../../cross-cutting/domain-authority-auditor/) — 在定期报告中包含CITE评分作为域名级别的KPI
- [排名追踪工具](../rank-tracker/) — 详细的排名数据
- [反向链接分析工具](../backlink-analyzer/) — 反向链接分析工具
- [警报管理工具](../alert-manager/) — 设置报告触发条件
- [SERP分析工具](../../research/serp-analysis/) — SERP组成数据
- [内存管理工具](../../cross-cutting/memory-management/) — 将报告存档在项目内存中
- [实体优化工具](../../cross-cutting/entity-optimizer/) — 跟踪品牌搜索和知识面板指标
- [技术SEO检查工具](../../optimize/technical-seo-checker/) — 将技术健康数据纳入报告