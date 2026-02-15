---
name: rank-tracker
description: 跟踪并分析传统搜索结果和人工智能生成响应中关键词的排名位置随时间的变化情况。监控排名变化，识别趋势，并在出现显著变化时发出警报。
geo-relevance: "medium"
---

# 排名跟踪器

此功能可帮助您跟踪、分析并报告关键词随时间的变化情况，包括传统搜索引擎结果页（SERP）的排名以及人工智能（AI）/地理位置（GEO）的可见性，从而提供全面的搜索性能洞察。

## 适用场景

- 为新营销活动设置排名跟踪
- 监控关键词排名的变化
- 分析排名趋势
- 与竞争对手进行排名对比
- 跟踪SERP中的特色内容
- 监控AI相关信息的展示情况
- 为利益相关者生成排名报告

## 功能概述

1. **排名跟踪**：记录并监控关键词的排名情况。
2. **趋势分析**：识别排名随时间的变化模式。
3. **变化检测**：标记出显著的排名变动。
4. **竞争对手对比**：与竞争对手进行基准对比。
5. **SERP特色内容跟踪**：监控特色片段（Featured Snippets）和PAA（Product Answer Boxes）的展示情况。
6. **地理位置可见性跟踪**：跟踪AI相关信息的展示情况。
7. **报告生成**：生成排名性能报告。

## 使用方法

### 设置跟踪

```
Set up rank tracking for [domain] targeting these keywords: [keyword list]
```

### 分析排名

```
Analyze ranking changes for [domain] over the past [time period]
```

### 与竞争对手对比

```
Compare my rankings to [competitor] for [keywords]
```

### 生成报告

```
Create a ranking report for [domain/campaign]
```

## 数据来源

> 请参阅 [CONNECTORS.md](../../CONNECTORS.md)，了解工具类别的相关信息。

**当连接了以下工具时：**
- **SEO工具**：自动获取关键词排名。
- **搜索控制台**：获取搜索量数据。
- **分析工具**：获取流量数据。
- **AI监控工具**：获取AI相关信息的展示情况。
系统会每天自动检查排名，并结合历史趋势数据进行分析。

**仅使用手动数据时：**
- 请用户提供以下信息：
  - 关键词的当前及历史排名情况。
  - 目标关键词列表及其搜索量。
  - 竞争对手的域名及其关键词排名。
  - SERP中的特色内容及PAA的展示情况。
  - AI相关信息的展示数据（如需跟踪地理位置指标）。
根据提供的数据进行分析。在报告中明确标注哪些数据来自自动收集，哪些数据来自用户提供。

## 使用说明

当用户请求排名跟踪或分析时，请按照以下步骤操作：

1. **设置关键词跟踪**：
   ```markdown
   ## Rank Tracking Setup
   
   ### Tracking Configuration
   
   **Domain**: [domain]
   **Tracking Location**: [country/city]
   **Device**: [Mobile/Desktop/Both]
   **Language**: [language]
   **Update Frequency**: [Daily/Weekly/Monthly]
   
   ### Keywords to Track
   
   | Keyword | Volume | Current Rank | Type | Priority |
   |---------|--------|--------------|------|----------|
   | [keyword 1] | [vol] | [rank] | Primary | High |
   | [keyword 2] | [vol] | [rank] | Primary | High |
   | [keyword 3] | [vol] | [rank] | Secondary | Medium |
   | [keyword 4] | [vol] | [rank] | Long-tail | Medium |
   | [keyword 5] | [vol] | [rank] | Brand | High |
   
   ### Competitor Tracking
   
   Track these competitors for benchmark:
   1. [Competitor 1] - [domain]
   2. [Competitor 2] - [domain]
   3. [Competitor 3] - [domain]
   
   ### Tracking Categories
   
   | Category | Keywords | Description |
   |----------|----------|-------------|
   | Brand | [X] | Brand name variations |
   | Product | [X] | Product-related terms |
   | Informational | [X] | Educational queries |
   | Commercial | [X] | Buying intent terms |
   ```

2. **记录当前排名**：
   ```markdown
   ## Current Ranking Snapshot
   
   **Date**: [date]
   **Domain**: [domain]
   
   ### Ranking Overview
   
   | Position Range | Keyword Count | % of Total |
   |----------------|---------------|------------|
   | #1 | [X] | [X]% |
   | #2-3 | [X] | [X]% |
   | #4-10 | [X] | [X]% |
   | #11-20 | [X] | [X]% |
   | #21-50 | [X] | [X]% |
   | #51-100 | [X] | [X]% |
   | Not ranking | [X] | [X]% |
   
   ### Position Distribution
   
   ```
   排名1：███████ [X]个关键词
   排名2-3：█████ [X]个关键词
   排名4-10：███████████████ [X]个关键词
   排名11-20：███████████ [X]个关键词
   排名21+：█████████ [X]个关键词
   ```
   
   ### Detailed Rankings
   
   | Keyword | Position | URL | SERP Features | Change |
   |---------|----------|-----|---------------|--------|
   | [kw 1] | 3 | [url] | Featured Snippet | +2 ↑ |
   | [kw 2] | 7 | [url] | PAA | -1 ↓ |
   | [kw 3] | 12 | [url] | None | New |
   | [kw 4] | 1 | [url] | Featured Snippet | — |
   ```

3. **分析排名变化**：
   ```markdown
   ## Ranking Change Analysis
   
   **Period**: [start date] to [end date]
   
   ### Overall Movement
   
   | Metric | Start | End | Change |
   |--------|-------|-----|--------|
   | Avg Position | [X] | [Y] | [+/-Z] |
   | Keywords in Top 10 | [X] | [Y] | [+/-Z] |
   | Keywords in Top 3 | [X] | [Y] | [+/-Z] |
   | Keywords #1 | [X] | [Y] | [+/-Z] |
   
   ### Biggest Improvements 📈
   
   | Keyword | Old Rank | New Rank | Change | Est. Traffic Impact |
   |---------|----------|----------|--------|---------------------|
   | [kw 1] | 15 | 4 | +11 | +[X] visits/mo |
   | [kw 2] | 25 | 9 | +16 | +[X] visits/mo |
   | [kw 3] | 8 | 2 | +6 | +[X] visits/mo |
   
   **Possible causes**:
   - [kw 1]: [hypothesis - e.g., content refresh may have improved relevance]
   - [kw 2]: [hypothesis]

   ### Biggest Declines 📉

   | Keyword | Old Rank | New Rank | Change | Est. Traffic Impact |
   |---------|----------|----------|--------|---------------------|
   | [kw 1] | 3 | 12 | -9 | -[X] visits/mo |
   | [kw 2] | 7 | 18 | -11 | -[X] visits/mo |

   **Likely factors**:
   - [kw 1]: [hypothesis - e.g., competitor may have published updated guide]
   - [kw 2]: [hypothesis]

   > These are hypotheses based on available signals, not confirmed causes. Investigate each with the relevant skill (on-page-seo-auditor, content-quality-auditor, backlink-analyzer) to confirm.
   
   **Recommended actions**:
   - [kw 1]: [action to recover]
   - [kw 2]: [action to recover]
   
   ### Stable Keywords
   
   [X] keywords remained within ±3 positions (stable)
   
   ### New Rankings
   
   | Keyword | Position | URL | Notes |
   |---------|----------|-----|-------|
   | [kw 1] | [pos] | [url] | [notes] |
   
   ### Lost Rankings
   
   | Keyword | Last Position | URL | Action |
   |---------|---------------|-----|--------|
   | [kw 1] | [pos] | [url] | [investigate/refresh] |
   ```

4. **跟踪SERP特色内容**：
   ```markdown
   ## SERP Feature Tracking
   
   ### Feature Ownership
   
   | Feature | Your Count | Competitor Avg | Opportunity |
   |---------|------------|----------------|-------------|
   | Featured Snippets | [X] | [Y] | [+/-Z] |
   | People Also Ask | [X] | [Y] | [+/-Z] |
   | Image Pack | [X] | [Y] | [+/-Z] |
   | Video Results | [X] | [Y] | [+/-Z] |
   | Local Pack | [X] | [Y] | [+/-Z] |
   
   ### Featured Snippet Status
   
   | Keyword | You Own? | Current Owner | Winnable? |
   |---------|----------|---------------|-----------|
   | [kw 1] | ✅ Yes | You | Maintain |
   | [kw 2] | ❌ No | [Competitor] | High |
   | [kw 3] | ❌ No | [Competitor] | Medium |
   
   ### PAA Appearances
   
   | Question | Your Answer? | Position | Action |
   |----------|--------------|----------|--------|
   | [Question 1] | ✅/❌ | [pos] | [action] |
   | [Question 2] | ✅/❌ | [pos] | [action] |
   ```

5. **跟踪地理位置/AI可见性**：
   ```markdown
   ## AI/GEO Visibility Tracking
   
   ### AI Overview Presence
   
   | Keyword | AI Overview | You Cited? | Citation Position |
   |---------|-------------|------------|-------------------|
   | [kw 1] | Yes | ✅ | 1st source |
   | [kw 2] | Yes | ✅ | 3rd source |
   | [kw 3] | Yes | ❌ | Not cited |
   | [kw 4] | No | N/A | N/A |
   
   ### AI Citation Rate
   
   | Metric | Value |
   |--------|-------|
   | Keywords with AI Overview | [X]/[Total] ([Y]%) |
   | Your citations in AI Overview | [X]/[Y] ([Z]%) |
   | Avg citation position | [X] |
   
   ### GEO Performance Trend
   
   | Period | AI Overviews Tracked | Your Citations | Rate |
   |--------|---------------------|----------------|------|
   | Last week | [X] | [Y] | [Z]% |
   | 2 weeks ago | [X] | [Y] | [Z]% |
   | Month ago | [X] | [Y] | [Z]% |
   
   ### GEO Improvement Opportunities
   
   | Keyword | Has AI Overview | You Cited? | Content Gap |
   |---------|-----------------|------------|-------------|
   | [kw 1] | Yes | No | Need clearer definition |
   | [kw 2] | Yes | No | Missing quotable stats |
   ```

6. **与竞争对手对比**：
   ```markdown
   ## Competitor Ranking Comparison
   
   ### Share of Voice
   
   | Domain | Keywords Ranked | Avg Position | Visibility |
   |--------|-----------------|--------------|------------|
   | [Your site] | [X] | [Y] | [Z]% |
   | [Competitor 1] | [X] | [Y] | [Z]% |
   | [Competitor 2] | [X] | [Y] | [Z]% |
   | [Competitor 3] | [X] | [Y] | [Z]% |
   
   ### Head-to-Head Comparison
   
   **You vs [Competitor 1]**:
   
   | Keyword | Your Rank | Their Rank | Winner |
   |---------|-----------|------------|--------|
   | [kw 1] | 3 | 7 | You ✅ |
   | [kw 2] | 12 | 5 | Them ❌ |
   | [kw 3] | 1 | 4 | You ✅ |
   
   **Summary**: You win [X]/[Y] keywords vs [Competitor 1]
   
   ### Competitor Movement Alerts
   
   | Competitor | Keyword | Their Change | Threat Level |
   |------------|---------|--------------|--------------|
   | [Comp 1] | [kw] | +15 positions | 🔴 High |
   | [Comp 2] | [kw] | +8 positions | 🟡 Medium |
   ```

7. **生成排名报告**：
   ```markdown
   # Ranking Performance Report
   
   **Domain**: [domain]
   **Report Period**: [start] to [end]
   **Generated**: [date]
   
   ## Executive Summary
   
   **Overall Trend**: [Improving/Stable/Declining]
   
   | Metric | Value | vs Last Period | Status |
   |--------|-------|----------------|--------|
   | Total keywords tracked | [X] | [+/-Y] | [status] |
   | Keywords in top 10 | [X] | [+/-Y] | [status] |
   | Keywords in top 3 | [X] | [+/-Y] | [status] |
   | Average position | [X] | [+/-Y] | [status] |
   | Estimated traffic | [X] | [+/-Y]% | [status] |
   
   ## Position Distribution
   
   ```
   排名1：███████████ [X]%
   排名2-3：███████ [X]%
   排名4-10：███████████████ [X]%
   排名11-20：█████████ [X]%
   排名21+： ████ [X]%
   ```
   
   ## Key Highlights
   
   ### Wins 🎉
   - [Achievement 1]
   - [Achievement 2]
   - [Achievement 3]
   
   ### Concerns ⚠️
   - [Issue 1]
   - [Issue 2]
   
   ### Opportunities 💡
   - [Opportunity 1]
   - [Opportunity 2]
   
   ## Detailed Analysis
   
   ### Top Performing Keywords
   
   | Keyword | Position | Change | Traffic | Notes |
   |---------|----------|--------|---------|-------|
   | [kw 1] | 1 | — | [X] | Stable leader |
   | [kw 2] | 2 | +3 | [X] | Growing |
   | [kw 3] | 3 | +5 | [X] | Big improvement |
   
   ### Keywords Needing Attention
   
   | Keyword | Position | Change | Issue | Recommended Action |
   |---------|----------|--------|-------|-------------------|
   | [kw 1] | 15 | -8 | Dropped | Refresh content |
   | [kw 2] | 22 | -5 | Competitor surge | Analyze competitor |
   
   ## SERP Feature Report
   
   | Feature | Count | Change | Competitor Avg |
   |---------|-------|--------|----------------|
   | Featured Snippets | [X] | [+/-Y] | [Z] |
   | PAA | [X] | [+/-Y] | [Z] |
   
   ## GEO/AI Visibility Report
   
   | Metric | This Period | Last Period | Trend |
   |--------|-------------|-------------|-------|
   | AI Overview appearances | [X] | [Y] | [↑/↓] |
   | Your citations | [X] | [Y] | [↑/↓] |
   | Citation rate | [X]% | [Y]% | [↑/↓] |
   
   ## Competitive Position
   
   **Share of Voice Ranking**: #[X] of [Y] competitors
   
   | Rank | Domain | Visibility |
   |------|--------|------------|
   | 1 | [domain] | [X]% |
   | 2 | [domain] | [X]% |
   | 3 | [domain] | [X]% |
   
   ## Recommendations
   
   ### Immediate Actions
   1. [Action] for [keyword] - [expected impact]
   2. [Action] for [keyword] - [expected impact]
   
   ### This Month
   1. [Action]
   2. [Action]
   
   ### Next Quarter
   1. [Strategic action]
   2. [Strategic action]
   
   ## Next Report

   Scheduled: [date]
   Focus areas: [areas to monitor]
   ```

## 验证要点

### 输入验证：
- 关键词列表是否完整，并包含相应的搜索量数据。
- 是否指定了目标域名和跟踪地点。
- 是否确定了用于对比的竞争对手域名。
- 是否有历史基线数据或设置了初始跟踪周期。

### 输出验证：
- 每个指标都应明确标注数据来源和收集日期。
- 排名变化应附有背景说明（与上一周期相比）。
- 对于显著的排名变化，应提供原因或调查说明。
- 明确每个数据点的来源（来自SEO工具、搜索控制台、用户提供的数据或估算值）。

## 示例

**用户请求：**“分析我上个月的排名变化”

**输出结果：**
```markdown
# Ranking Analysis: [current month, year]

## Summary

Your average position improved from 15.3 to 12.8 (-2.5 positions = better)
Keywords in top 10 increased from 12 to 17 (+5)

## Biggest Wins

| Keyword | Old | New | Change | Possible Cause |
|---------|-----|-----|--------|----------------|
| email marketing tips | 18 | 5 | +13 | Likely driven by content refresh |
| best crm software | 24 | 11 | +13 | Correlates with new backlinks acquired |
| sales automation | 15 | 7 | +8 | Correlates with schema markup addition |

## Needs Attention

| Keyword | Old | New | Change | Action |
|---------|-----|-----|--------|--------|
| marketing automation | 4 | 12 | -8 | Likely displaced by new HubSpot guide |

**Recommended**: Update your marketing automation guide with [current year] statistics and examples.
```

## 使用技巧

1. **保持一致性**：使用相同的时间、设备和地点进行跟踪。
2. **选择足够的关键词**：至少选择50-200个关键词以获得有意义的数据。
3. **按意图分类**：分别跟踪品牌相关、商业相关和信息类关键词。
4. **关注竞争对手**：了解竞争对手的排名变化有助于更准确地分析自己的排名。
5. **关注SERP特色内容**：没有特色片段的排名1可能会被有特色片段的排名4超越。
6. **包含地理位置指标**：AI相关信息的可见性越来越重要。

## 排名变化分析框架

### 排名变化的原因

| 类别 | 原因 | 检测方法 |
|----------|--------|-----------------|
| **算法更新** | Google核心算法更新、内容更新、垃圾信息处理 | 查看Google搜索状态仪表板、SEO新闻 |
| **竞争对手行为** | 发布新内容、内容更新、获得新链接 | 监控竞争对手的页面变化和SERP排名 |
| **自身操作** | 内容编辑、技术调整、系统迁移 | 与部署/变更日志对照 |
| **SERP特色内容变化** | 新特色片段的添加或删除 | 使用SERP监控工具 |
| **季节性变化** | 需求的周期性变化 | 年度对比 |
| **技术问题** | 爬取错误、网站速度下降、索引问题 | 使用搜索控制台和爬取报告 |
| **链接变化** | 失去链接、获得新链接、链接被屏蔽 | 使用链接监控工具 |

## 排名变化应对策略

| 变化类型 | 时间范围 | 应对措施 |
|--------|-----------|--------|
| 排名下降1-3位 | 等待1-2周 | 可能是正常波动 |
| 排名下降3-5位 | 在1周内进行调查 | 检查技术问题或竞争对手的变化 |
| 排名下降5-10位 | 立即调查 | 全面诊断：技术、内容、链接方面 |
| 从第1位跌落 | 紧急响应 | 进行全面审计并制定恢复计划 |
| 排名上升 | 记录并分析原因 | 了解哪些因素起了作用，能否复制这些策略？ |

## 排名分布基准

### 不同位置的点击率

| 排名 | 桌面设备CTR | 移动设备CTR | 备注 |
|----------|------------|------------|-------|
| 第1位 | 31.7% | 24.0% | 比第10位高出约10倍 |
| 第2位 | 14.7% | 13.1% | 比第1位下降约50% |
| 第3位 | 10.7% | 9.5% | 具有较高价值 |
| 第4位 | 6.7% | 6.1% | 通常仍可见 |
| 第5位 | 5.1% | 4.6% | 通常仍可见 |
| 第6位 | 4.1% | 3.5% | 在大多数设备上不太可见 |
| 第7位 | 3.4% | 2.8% | 下降趋势明显 |
| 第8位 | 2.9% | 2.3% | |
| 第9位 | 2.5% | 1.9% | |
| 第10位 | 2.2% | 1.6% | 位于页面底部 |
| 第11-20位 | <1.5% | <1.0% | 几乎不可见 |

_注：点击率会因查询类型、SERP特色内容和行业而异。这些数据为平均值。_

### SERP特色内容对点击率的影响

| SERP特色内容 | 对自然搜索点击率的影响 |
|---------------------|---------------------|
| 自己的特色片段 | 提高结果点击率20-30% |
| 竞争对手的特色片段 | 降低第1位结果的点击率15-25% |
| AI相关信息 | 降低所有自然搜索结果的点击率10-30% |
| PAA框 | 降低第3-6位结果的点击率5-10% |
| 购物结果 | 降低商业查询的点击率10-20% |
| 知识面板 | 降低导航类查询的点击率5-15% |

## SERP波动性分析

### 算法更新的影响评估

| 更新类型 | 典型影响 | 恢复时间 | 应对策略 |
|------------|---------------|---------------|-------------------|
| 核心算法更新 | 流量波动±20-50% | 需要3-6个月（直到下一次核心算法更新） | 全面提升内容质量 |
| 有用的内容 | 重点提升内容质量 | 1-3个月 | 删除/改进无用的内容 |
| 垃圾信息处理 | 严厉打击作弊行为 | 清理链接库，移除垃圾链接 |
| 产品评论 | 根据评论内容调整 | 1-2个月 | 提升评论的深度和专业性 |
| 链接作弊 | 处理虚假链接 | 2-4个月 | 清除有害链接，建立高质量链接 |

## 跟踪配置最佳实践

| 设置项 | 建议 | 原因 |
|---------|---------------|-----|
| 检查频率 | 前20个关键词每天检查；其他关键词每周检查 | 在准确性和API成本之间取得平衡 |
| 地点设置 | 与目标市场匹配；分别跟踪本地排名 | 不同地区的排名可能有所不同 |
| 设备跟踪 | 分别跟踪移动设备和桌面设备 | 移动设备的排名差异显著 |
| 竞争对手跟踪 | 关键关键词跟踪3-5个竞争对手 | 有助于了解自身排名变化的原因 |
| SERP特色内容 | 跟踪哪些特色内容出现 | 解释点击率的变化原因 |
| 关键词分组 | 按主题、意图和用户转化阶段分组 | 识别规律，而不仅仅是关键词本身 |

## 参考资料

- [跟踪设置指南](./references/tracking-setup-guide.md) — 配置最佳实践、设备/地点设置及SERP特色内容跟踪方法

## 相关功能

- [关键词研究](../../research/keyword-research/) — 选择需要跟踪的关键词
- [SERP分析](../../research/serp-analysis/) — 了解SERP的构成 |
- [警报管理](../alert-manager/) — 设置排名警报 |
- [性能报告](../performance-reporter/) — 生成综合报告 |
- [内存管理](../../cross-cutting/memory-management/) — 将排名历史数据存储在项目中