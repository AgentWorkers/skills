---
name: content-gap-analysis
description: 通过识别竞争对手所覆盖但您尚未涉及的主题和关键词，发现内容创作的机会。揭示您内容策略中尚未被开发的潜力以及存在的战略缺口。
geo-relevance: "medium"
---

# 内容差距分析

该技能通过分析您的内容与竞争对手内容之间的差距，来识别内容创作的机遇。它能帮助您发现缺失的主题、可针对的关键词以及应创建的内容格式。

## 适用场景

- 规划内容策略和编辑日程
- 寻找快速见效的内容创作机会
- 了解竞争对手在哪些方面表现优于您
- 识别您所在领域中未被充分覆盖的主题
- 扩展到相关主题领域
- 确定内容创作的优先级
- 发现竞争对手忽略的地域性（GEO）机会

## 功能介绍

1. **关键词差距分析**：找出竞争对手排名靠前但您尚未覆盖的关键词。
2. **主题覆盖范围分析**：识别需要更多内容的主题领域。
3. **内容格式差距**：揭示缺失的内容类型（如视频、工具、指南等）。
4. **受众需求分析**：将差距与受众的阅读或使用流程相匹配。
5. **地域性机会检测**：发现您尚未涉及的、可以通过人工智能回答的主题。
6. **优先级排序**：根据影响力和所需工作量对差距进行排序。
7. **内容日程规划**：制定填补这些差距的内容计划。

## 使用方法

### 基础差距分析

```
Find content gaps between my site [URL] and [competitor URLs]
```

```
What content am I missing compared to my top 3 competitors?
```

### 针对特定主题的分析

```
Find content gaps in [topic area] compared to industry leaders
```

```
What [content type] do competitors have that I don't?
```

### 以受众为中心的分析

```
What content gaps exist for [audience segment] in my niche?
```

## 数据来源

> 请参阅 [CONNECTORS.md](../../CONNECTORS.md)，了解可使用的工具类别。

**当连接了 ~~SEO工具 + ~~搜索分析工具 + ~~数据分析工具 + ~~人工智能监控工具时：**
可以自动从 ~~搜索分析工具（页面索引、页面流量、关键词排名）获取您网站的内容清单，从 ~~SEO工具（关键词排名、热门页面、外部链接数量）获取竞争对手的内容数据，以及从 ~~人工智能监控工具获取相关的数据。关键词重叠分析和差距识别可以自动化完成。

**仅使用手动数据时：**
请用户提供以下信息：
1. 您的网站URL和内容清单（包含已发布的内容及其主题）。
2. 竞争对手的网站URL（3-5个网站）。
3. 您当前的网站流量和关键词表现（如有）。
4. 您现有的内容优势和劣势。
5. 行业背景和业务目标。

使用提供的数据进行分析。在输出结果中明确标注哪些数据来自自动化收集，哪些来自用户提供。

## 操作步骤

当用户请求进行内容差距分析时：

1. **明确分析范围**
   清晰界定分析参数：
   
   ```markdown
   ### Analysis Parameters
   
   **Your Site**: [URL]
   **Competitors to Analyze**: [URLs or "identify for me"]
   **Topic Focus**: [specific area or "all"]
   **Content Types**: [blogs, guides, tools, videos, or "all"]
   **Audience**: [target audience]
   **Business Goals**: [traffic, leads, authority, etc.]
   ```

2. **审核现有内容**
   ```markdown
   ## Your Content Inventory
   
   **Total Indexed Pages**: [X]
   **Content by Type**:
   - Blog posts: [X]
   - Landing pages: [X]
   - Resource pages: [X]
   - Tools/calculators: [X]
   - Case studies: [X]
   
   **Content by Topic Cluster**:
   
   | Topic | Articles | Keywords Ranking | Traffic |
   |-------|----------|------------------|---------|
   | [topic 1] | [X] | [X] | [X] |
   | [topic 2] | [X] | [X] | [X] |
   | [topic 3] | [X] | [X] | [X] |
   
   **Top Performing Content**:
   1. [Title] - [traffic] visits - [keywords] keywords
   2. [Title] - [traffic] visits - [keywords] keywords
   3. [Title] - [traffic] visits - [keywords] keywords
   
   **Content Strengths**:
   - [Strength 1]
   - [Strength 2]
   
   **Content Weaknesses**:
   - [Weakness 1]
   - [Weakness 2]
   ```

3. **分析竞争对手的内容**
   ```markdown
   ## Competitor Content Analysis
   
   ### Competitor 1: [Name/URL]
   
   **Content Volume**: [X] pages
   **Monthly Traffic**: [X] visits
   
   **Content Distribution**:
   | Type | Count | Est. Traffic |
   |------|-------|--------------|
   | Blog posts | [X] | [X] |
   | Guides | [X] | [X] |
   | Tools | [X] | [X] |
   | Videos | [X] | [X] |
   
   **Topic Coverage**:
   | Topic | Articles | Your Coverage |
   |-------|----------|---------------|
   | [topic] | [X] | [X or "None"] |
   
   **Unique Content They Have**:
   1. [Content piece] - [traffic] - [why it works]
   2. [Content piece] - [traffic] - [why it works]
   
   [Repeat for each competitor]
   ```

4. **识别关键词差距**
   ```markdown
   ## Keyword Gap Analysis
   
   ### Keywords Competitors Rank For (You Don't)
   
   **High Priority Gaps** (High volume, achievable difficulty)
   
   | Keyword | Volume | Difficulty | Competitor | Their Position |
   |---------|--------|------------|------------|----------------|
   | [kw 1] | [vol] | [diff] | [comp] | [pos] |
   | [kw 2] | [vol] | [diff] | [comp] | [pos] |
   | [kw 3] | [vol] | [diff] | [comp] | [pos] |
   
   **Quick Win Gaps** (Lower volume, low difficulty)
   
   | Keyword | Volume | Difficulty | Competitor | Their Position |
   |---------|--------|------------|------------|----------------|
   | [kw 1] | [vol] | [diff] | [comp] | [pos] |
   
   **Long-term Gaps** (High volume, high difficulty)
   
   | Keyword | Volume | Difficulty | Competitor | Their Position |
   |---------|--------|------------|------------|----------------|
   | [kw 1] | [vol] | [diff] | [comp] | [pos] |
   
   ### Keyword Overlap Analysis
   
   ```
   文氏图表示方法：
   
        您          竞争对手1
         ○               ○
        / \             / \
       /   \           /   \
      /  A  \ B       / C   \
     /       \       /       \
    ○─────────○─────○─────────○
              竞争对手2
   
   A：仅您排名靠前的关键词：[X]
   B：与竞争对手1重叠的关键词：[X]
   C：所有竞争对手都涉及的关键词：[X]
   缺口：他们都有但您没有的关键词：[X]
   ```
   
   **Unique Keywords (Your Advantage)**:
   | Keyword | Your Position | Volume |
   |---------|---------------|--------|
   | [kw] | [pos] | [vol] |
   ```

5. **绘制主题差距图**
   ```markdown
   ## Topic Gap Analysis
   
   ### Topic Coverage Comparison
   
   | Topic Area | You | Comp 1 | Comp 2 | Comp 3 | Gap? |
   |------------|-----|--------|--------|--------|------|
   | [Topic 1] | ✅ [X] | ✅ [X] | ✅ [X] | ✅ [X] | No |
   | [Topic 2] | ❌ 0 | ✅ [X] | ✅ [X] | ✅ [X] | **Yes** |
   | [Topic 3] | ✅ [X] | ✅ [X] | ❌ 0 | ✅ [X] | Partial |
   | [Topic 4] | ❌ 0 | ✅ [X] | ✅ [X] | ❌ 0 | **Yes** |
   
   ### Missing Topic Clusters
   
   #### Gap 1: [Topic Area]
   
   **Why it matters**: [Business relevance]
   **Competitor coverage**: [Who covers it and how]
   **Opportunity size**: [Traffic/keyword potential]
   
   **Sub-topics to cover**:
   1. [Sub-topic] - [X] search volume
   2. [Sub-topic] - [X] search volume
   3. [Sub-topic] - [X] search volume
   
   **Recommended approach**:
   - Pillar content: [topic]
   - Cluster articles: [list]
   - Supporting content: [list]
   ```

6. **识别内容格式差距**
   ```markdown
   ## Content Format Gap Analysis
   
   ### Format Distribution Comparison
   
   | Format | You | Comp 1 | Comp 2 | Industry Avg |
   |--------|-----|--------|--------|--------------|
   | Long-form guides | [X] | [X] | [X] | [X] |
   | Tutorials | [X] | [X] | [X] | [X] |
   | Comparison posts | [X] | [X] | [X] | [X] |
   | Case studies | [X] | [X] | [X] | [X] |
   | Tools/calculators | [X] | [X] | [X] | [X] |
   | Templates | [X] | [X] | [X] | [X] |
   | Video content | [X] | [X] | [X] | [X] |
   | Infographics | [X] | [X] | [X] | [X] |
   | Original research | [X] | [X] | [X] | [X] |
   
   ### Format Gaps to Fill
   
   #### Gap: [Format Type]
   
   **Current state**: You have [X], competitors average [Y]
   **Best examples**: [Competitor content examples]
   **Opportunity**: [Description]
   **Effort to create**: [Low/Medium/High]
   **Expected impact**: [Low/Medium/High]
   
   **Recommended first project**:
   [Specific content idea]
   ```

7. **分析地域性/人工智能相关差距**
   ```markdown
   ## GEO Content Gap Analysis
   
   ### AI-Answerable Topics Assessment
   
   **Topics where competitors get AI citations (you don't)**:
   
   | Topic | AI Cites | Why They're Cited | Your Gap |
   |-------|----------|-------------------|----------|
   | [topic 1] | [Comp] | [reason] | [what you need] |
   | [topic 2] | [Comp] | [reason] | [what you need] |
   
   ### GEO-Optimized Content Gaps
   
   **Missing Q&A Content**:
   | Question | Search Volume | Currently Answered By |
   |----------|---------------|----------------------|
   | [question] | [vol] | [competitor] |
   
   **Missing Definition/Explanation Content**:
   | Term | Search Volume | Best Current Source |
   |------|---------------|---------------------|
   | [term] | [vol] | [source] |
   
   **Missing Comparison Content**:
   | Comparison | Search Volume | Best Current Source |
   |------------|---------------|---------------------|
   | [A vs B] | [vol] | [source] |
   
   ### GEO Opportunity Score
   
   | Topic | Traditional SEO Value | GEO Value | Combined Priority |
   |-------|----------------------|-----------|-------------------|
   | [topic] | [score] | [score] | [priority] |
   ```

8. **将差距与受众流程对应起来**
   ```markdown
   ## Audience Journey Gap Analysis
   
   ### Funnel Stage Coverage
   
   | Stage | Your Content | Competitor Avg | Gap |
   |-------|--------------|----------------|-----|
   | Awareness | [X] articles | [X] articles | [+/-X] |
   | Consideration | [X] articles | [X] articles | [+/-X] |
   | Decision | [X] articles | [X] articles | [+/-X] |
   | Retention | [X] articles | [X] articles | [+/-X] |
   
   ### Journey Gap Details
   
   #### Awareness Stage Gaps
   - Missing: [topics/content]
   - Opportunity: [description]
   
   #### Consideration Stage Gaps
   - Missing: [topics/content]
   - Opportunity: [description]
   
   #### Decision Stage Gaps
   - Missing: [topics/content]
   - Opportunity: [description]
   ```

9. **确定优先级并制定行动计划**
   ```markdown
   # Content Gap Analysis Report
   
   ## Executive Summary
   
   **Analysis Date**: [Date]
   **Sites Analyzed**: [Your site] vs [Competitors]
   
   **Key Findings**:
   1. [Most significant gap]
   2. [Second significant gap]
   3. [Third significant gap]
   
   **Total Opportunity**:
   - Keywords gaps identified: [X]
   - Estimated traffic opportunity: [X]/month
   - Quick wins available: [X] pieces
   
   ---
   
   ## Prioritized Gap List
   
   ### Tier 1: Quick Wins (Do Now)
   
   | Content to Create | Target Keyword | Volume | Difficulty | Impact |
   |-------------------|----------------|--------|------------|--------|
   | [Title idea] | [keyword] | [vol] | [diff] | High |
   | [Title idea] | [keyword] | [vol] | [diff] | High |
   
   **Why prioritize**: Low effort, immediate ranking potential
   
   ### Tier 2: Strategic Builds (This Quarter)
   
   | Content to Create | Target Keyword | Volume | Difficulty | Impact |
   |-------------------|----------------|--------|------------|--------|
   | [Title idea] | [keyword] | [vol] | [diff] | High |
   
   **Why prioritize**: High value, requires more resources
   
   ### Tier 3: Long-term Investments (This Year)
   
   | Content to Create | Target Keyword | Volume | Difficulty | Impact |
   |-------------------|----------------|--------|------------|--------|
   | [Title idea] | [keyword] | [vol] | [diff] | High |
   
   **Why prioritize**: Builds authority, competitive differentiator
   
   ---
   
   ## Content Calendar Recommendation
   
   ### Month 1
   | Week | Content | Type | Target Keyword | Status |
   |------|---------|------|----------------|--------|
   | 1 | [Title] | [Type] | [Keyword] | Planned |
   | 2 | [Title] | [Type] | [Keyword] | Planned |
   | 3 | [Title] | [Type] | [Keyword] | Planned |
   | 4 | [Title] | [Type] | [Keyword] | Planned |
   
   ### Month 2
   [Continue...]
   
   ### Month 3
   [Continue...]
   
   ---
   
   ## Success Metrics
   
   Track these to measure gap-filling success:
   
   | Metric | Current | 3-Month Target | 6-Month Target |
   |--------|---------|----------------|----------------|
   | Keyword coverage | [X] | [X] | [X] |
   | Topic clusters complete | [X] | [X] | [X] |
   | Traffic from new content | [X] | [X] | [X] |
   | AI citations | [X] | [X] | [X] |
   ```

## 验证要点

### 输入验证
- [ ] 您提供的内容清单完整或具有代表性。
- [ ] 已识别出至少2-3个竞争对手的网站URL。
- [ ] 分析范围明确（是针对特定主题还是全面分析）。
- [ ] 业务目标和优先级已明确。

### 输出验证
- [ ] 每条建议都基于具体的数据点（而非泛泛而谈）。
- [ ] 差距分析是对同类内容进行对比的（主题群组与主题群组之间的对比）。
- [ ] 优先级排序基于可衡量的标准（如内容量、难度、与业务目标的契合度）。
- [ ] 内容日程规划将差距与实际的时间框架相对应。
- [ ] 每个数据来源都明确标注（来自 ~~SEO工具、~~数据分析工具、~~人工智能监控工具，或是用户提供的数据）。

## 示例

**用户**：“我想对比我的SaaS营销博客与HubSpot和Drift的内容差距。”

**输出结果：**
```markdown
# Content Gap Analysis: SaaS Marketing Blog

## Executive Summary

Compared to HubSpot and Drift, your blog has significant gaps in:
1. **Interactive tools** - They have 15+, you have 0
2. **Comparison content** - Missing "[Your Tool] vs [Competitor]" pages
3. **GEO-optimized definitions** - No glossary or term definitions

Total opportunity: ~25,000 monthly visits from 45 keyword gaps

## Top Keyword Gaps

### Quick Wins (Difficulty <40)

| Keyword | Volume | Difficulty | Who Ranks |
|---------|--------|------------|-----------|
| saas marketing metrics | 1,200 | 32 | HubSpot #3 |
| b2b email sequences | 890 | 28 | Drift #5 |
| saas onboarding emails | 720 | 25 | Neither! |
| marketing qualified lead definition | 1,800 | 35 | HubSpot #1 |

### Content Format Gaps

**You're missing**:
- [ ] Interactive ROI calculator (HubSpot gets 15k visits/mo from theirs)
- [ ] Email template library (Drift's gets 8k visits/mo)
- [ ] Marketing glossary (HubSpot's definition pages rank for 500+ keywords)

## Recommended Content Calendar

**Week 1**: "SaaS Marketing Metrics: Complete Guide" (Quick win)
**Week 2**: "What is a Marketing Qualified Lead?" (GEO opportunity)
**Week 3**: "B2B Email Sequence Templates" (Format gap)
**Week 4**: "[Your Tool] vs HubSpot" (Comparison gap)
```

## 高级分析方法

### 竞争对手群组对比
```
Compare our topic cluster coverage for [topic] vs top 5 competitors
```

### 时间序列差距分析
```
What content have competitors published in the last 6 months that we haven't covered?
```

### 基于用户意图的差距分析
```
Find gaps in our [commercial/informational] intent content
```

## 成功技巧

1. **聚焦可操作的差距**：并非所有差距都值得填补。
2. **考虑资源限制**：根据实际执行能力来安排优先级。
3. **质量优先于数量**：填补5个高质量的内容缺口比填补20个低质量的内容更有价值。
4. **跟踪效果**：衡量填补差距后的实际效果。
5. **定期更新**：随着竞争对手发布新内容，差距也会发生变化。
6. **关注地域性机会**：不要只优化传统搜索流量。

## 内容审核框架

### 内容覆盖矩阵

按主题和格式绘制各竞争对手的内容覆盖情况：

| 主题/主题 | 您的内容 | 竞争对手A | 竞争对手B | 存在差距吗？ | 优先级 |
|------------|-------------|-------------|-------------|------|----------|
| [主题1] | 博文 | 博文系列、网络研讨会 | 无 | 对竞争对手B来说是优势 | 高优先级 |
| [主题2] | 无 | 白皮书 | 博文、视频 | 您需要补充内容 | 高优先级 |
| [主题3] | 案例研究 | 无 | 案例研究 | 已覆盖 | 低优先级 |

### 内容类型覆盖矩阵

| 内容格式 | 您 | 竞争对手A | 竞争对手B | 竞争对手C | 市场需求 |
|---------------|-----|--------|--------|--------|-------------------|
| 博文 | ✅ | ✅ | ✅ | ✅ | 需要补充 |
| 操作指南 | ✅ | ✅ | ❌ | ✅ | 预期会有需求 |
| 视频内容 | ❌ | ✅ | ✅ | ✅ | 需求正在增长 |
| 互动工具 | ❌ | ❌ | ❌ | ✅ | 可作为差异化优势 |
| 研究/数据 | ❌ | ✅ | ❌ | ❌ | 高价值的内容 |
| 模板/下载 | ✅ | ❌ | ✅ | ❌ | 有助于吸引潜在客户 |
| 播客 | ❌ | ❌ | ✅ | ❌ | 新兴内容形式 |

## 漏斗阶段差距分析

### 内容漏斗映射

| 漏斗阶段 | 内容目的 | 需要的内容格式 | 存在的差距 |
|-------------|----------------|-----------------|------------|
| 了解阶段 | 吸引新访客 | 博文、社交媒体、视频、公关 | 有机流量低，品牌搜索量少 |
| 考虑阶段 | 教育和互动 | 指南、对比文章、网络研讨会 | 离站率高，页面浏览量低 |
| 决策阶段 | 转化访客 | 案例研究、价格信息、演示文稿、试用 | 转化率低 |
| 保留阶段 | 保持客户关系 | 帮助文档、邮件系列、社区活动 | 客户流失率高，互动少 |
| 推广阶段 | 促使客户成为推广者 | 评价计划、推荐内容 | 推荐流量低 |

## 差距优先级评分

### 影响力 x 工作量矩阵

从影响力和工作量两个维度对每个差距进行1-5分的评分：

| 影响力因素 | 权重 | 评估方法 |
|--------------|--------|--------------|
| 搜索需求 | 30% | 相关关键词的搜索量 |
| 竞争对手覆盖情况 | 25% | 有多少竞争对手提供了该类型内容？ |
| 与业务相关性 | 25% | 该内容与您的核心业务有多相关？ |
| 漏斗阶段需求 | 20% | 哪个阶段的需求最迫切？ |

**优先级**：首先选择影响大且工作量小的差距。

## 参考资料

- [差距分析框架](./references/gap-analysis-frameworks.md) — 提供内容审核模板、漏斗映射和差距优先级评估方法。

## 相关技能

- [关键词研究](../keyword-research/) — 深入研究关键词差距。
- [竞争对手分析](../competitor-analysis/) — 了解竞争对手的策略。
- [SEO内容撰写](../../build/seo-content-writer/) — 创作填补差距的内容。
- [内容更新](../../optimize/content-refresher/) — 更新现有内容以填补发现的差距。
- [内部链接优化](../../optimize/internal-linking-optimizer/) — 识别并优化内部链接的不足。
- [外部链接分析](../../monitor/backlink-analyzer/) — 分析外部链接的潜在机会。
- [内容管理](../../cross-cutting/memory-management/) — 随时间跟踪内容差距的变化。