---
name: content-refresher
description: '**使用场景：**  
当用户请求“更新旧内容”、“刷新内容”、“内容已过时”、“提升下降的排名”、“重新发布旧博客文章”、“这篇文章已经过时”、“该页面的访问量正在下降”或“这篇文章的排名下降了”时，可使用此工具。该工具能够识别并更新过时的内容，以恢复和提升网站的搜索排名。它还会分析内容的新鲜度、添加新信息、更新相关统计数据，并优化内容以符合当前的SEO和地理定位（GEO）最佳实践。  
**如需从头开始编写新内容，请参考** `seo-content-writer`；**如需进行无需重写的审计，请参考** `on-page-seo-auditor`。'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "medium"
  tags:
    - seo
    - geo
    - content refresh
    - content update
    - outdated content
    - content decay
    - ranking recovery
    - content optimization
  triggers:
    - "update old content"
    - "refresh content"
    - "content is outdated"
    - "improve declining rankings"
    - "revive old blog posts"
    - "content decay"
    - "ranking dropped"
    - "this post is outdated"
    - "traffic is declining on this page"
    - "rankings dropped for this article"
---

# 内容更新指南

> **[SEO与地理定位（GEO）技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 包含20项SEO与GEO相关技能 · 通过 `npx skills add aaron-he-zhu/seo-geo-claude-skills` 安装所有技能

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容编写器](../../build/seo-content-writer/) · [地理内容优化器](../../build/geo-content-optimizer/) · [元标签优化器](../../build/meta-tags-optimizer/) · [结构化标记生成器](../../build/schema-markup-generator/)

**优化** · [页面SEO审核器](../on-page-seo-auditor/) · [技术SEO检查器](../technical-seo-checker/) · [内部链接优化器](../internal-linking-optimizer/) · **内容更新指南**

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告器](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)

**跨领域技能** · [内容质量审核器](../../cross-cutting/content-quality-auditor/) · [域名权威性审核器](../../cross-cutting/domain-authority-auditor/) · [实体优化器](../../cross-cutting/entity-optimizer/) · [内存管理](../../cross-cutting/memory-management/)

</details>

此技能有助于识别并更新过时的内容，以恢复失去的排名和流量。它分析内容的新鲜度，找出需要更新的部分，并指导更新过程，以最大化SEO和GEO的效果。

## 何时使用此技能

- 内容随时间推移失去了排名或流量
- 统计数据和信息已经过时
- 竞争对手发布了更好的内容
- 内容需要为新年进行更新
- 行业变化要求内容更新
- 需要在现有内容中添加新章节
- 需要将旧内容转换为适合地理定位优化的格式

## 该技能的功能

1. **新鲜度分析**：识别需要更新的内容
2. **性能跟踪**：发现流量下降的内容
3. **差距识别**：找出竞争对手拥有的但自己缺失的信息
4. **更新优先级排序**：根据更新潜力对内容进行排序
5. **更新建议**：提供具体的更新指导
6. **地理优化**：更新内容以提高AI引用的可能性
7. **重新发布策略**：提供关于发布时间和推广策略的建议

## 使用方法

### 识别需要更新的内容

```
Find content on [domain] that needs refreshing
```

```
Which of my blog posts have lost the most traffic?
```

### 更新特定内容

```
Refresh this article for [current year]: [URL/content]
```

```
Update this content to outrank [competitor URL]: [your URL]
```

### 内容更新策略

```
Create a content refresh strategy for [domain/topic]
```

## 数据来源

> 请参阅 [CONNECTORS.md](../../CONNECTORS.md) 以了解工具类别的相关信息。

**当连接到 ~~分析工具 + ~~搜索控制台 + ~~SEO工具** 时：**
Claude可以自动从 ~~分析工具** 中获取历史流量趋势，从 ~~搜索控制台** 中获取点击量和排名数据，从 ~~SEO工具** 中获取关键词排名历史，并识别表现下降的内容。这有助于基于数据来优先安排更新。

**仅使用手动数据时：**
要求用户提供：
1. 流量数据或显示性能趋势的截图
2. 关键页面的排名截图或历史记录
3. 内容的发布日期和最后更新日期
4. 用户认为需要更新的内容列表

使用提供的数据进行分析。在输出中注明哪些发现是基于自动化数据，哪些是基于手动审核的。

## 指令

当用户请求内容更新帮助时：

1. **CORE-EEAT快速评估** — 在更新之前，进行一次CORE-EEAT快速评估，以便将重点放在最薄弱的环节上。参考：[CORE-EEAT基准](../../references/core-eeat-benchmark.md)

   ```markdown
   ### CORE-EEAT Quick Assessment

   **Content**: [title or URL]
   **Content Type**: [type]

   Rapidly score each dimension (estimate 0-100):

   | Dimension | Quick Score | Key Weakness | Refresh Priority |
   |-----------|-----------|--------------|-----------------|
   | C — Contextual Clarity | [X]/100 | [main issue] | 🔴/🟡/🟢 |
   | O — Organization | [X]/100 | [main issue] | 🔴/🟡/🟢 |
   | R — Referenceability | [X]/100 | [main issue] | 🔴/🟡/🟢 |
   | E — Exclusivity | [X]/100 | [main issue] | 🔴/🟡/🟢 |
   | Exp — Experience | [X]/100 | [main issue] | 🔴/🟡/🟢 |
   | Ept — Expertise | [X]/100 | [main issue] | 🔴/🟡/🟢 |
   | A — Authority | [X]/100 | [main issue] | 🔴/🟡/🟢 |
   | T — Trust | [X]/100 | [main issue] | 🔴/🟡/🟢 |

   **Weakest Dimensions** (focus refresh here):
   1. [Dimension] — [what needs fixing]
   2. [Dimension] — [what needs fixing]

   **Refresh Strategy**: Focus on 🔴 dimensions first, then 🟡.

   _For full 80-item audit, use [content-quality-auditor](../../cross-cutting/content-quality-auditor/)_
   ```

2. **识别需要更新的内容**  
   ```markdown
   ## Content Refresh Analysis
   
   ### Refresh Candidate Identification
   
   **Criteria for Content Refresh**:
   - Published more than 6 months ago
   - Contains dated information (years, statistics)
   - Declining traffic trend
   - Lost keyword rankings
   - Outdated references or broken links
   - Missing topics competitors now cover
   - No GEO optimization
   
   ### Content Audit Results
   
   | Content | Published | Last Updated | Traffic Trend | Priority |
   |---------|-----------|--------------|---------------|----------|
   | [Title 1] | [date] | [date] | ↓ -45% | 🔴 High |
   | [Title 2] | [date] | Never | ↓ -30% | 🔴 High |
   | [Title 3] | [date] | [date] | ↓ -20% | 🟡 Medium |
   | [Title 4] | [date] | [date] | → 0% | 🟡 Medium |
   
   ### Refresh Prioritization Matrix
   
   ```  
   流量高且下降明显 = 🔴 立即更新  
   流量高但下降幅度小 = 🟡 安排更新  
   流量低且下降幅度小 = 🟡 评估后再决定  
   流量低且下降幅度小 = 🟢 优先级较低  
   ```
   ```

3. **分析单个内容以确定是否需要更新**  
   ```markdown
   ## Content Refresh Analysis: [Title]
   
   **URL**: [URL]
   **Published**: [date]
   **Last Updated**: [date]
   **Word Count**: [X]
   
   ### Performance Metrics
   
   | Metric | 6 Mo Ago | Current | Change |
   |--------|----------|---------|--------|
   | Organic Traffic | [X]/mo | [X]/mo | [+/-X]% |
   | Avg Position | [X] | [X] | [+/-X] |
   | Impressions | [X] | [X] | [+/-X]% |
   | CTR | [X]% | [X]% | [+/-X]% |
   
   ### Keywords Analysis
   
   | Keyword | Old Position | Current Position | Change |
   |---------|--------------|------------------|--------|
   | [kw 1] | [X] | [X] | ↓ [X] |
   | [kw 2] | [X] | [X] | ↓ [X] |
   | [kw 3] | [X] | [X] | ↓ [X] |
   
   ### Why This Content Needs Refresh
   
   1. **Outdated information**: [specific examples]
   2. **Competitive gap**: [what competitors added]
   3. **Missing topics**: [new subtopics to cover]
   4. **SEO issues**: [current optimization problems]
   5. **GEO potential**: [AI citation opportunities]
   ```

4. **确定具体的更新内容**  
   ```markdown
   ## Refresh Requirements
   
   ### Outdated Elements
   
   | Element | Current | Update Needed |
   |---------|---------|---------------|
   | Year references | "[old year]" | Update to [current year] |
   | Statistics | "[old stat]" | Find current data |
   | Tool mentions | "[old tool]" | Add newer tools |
   | Links | [X] broken | Fix or replace |
   | Screenshots | Outdated UI | Recapture |
   
   ### Missing Information
   
   **Topics competitors now cover that you don't**:
   
   | Topic | Competitor Coverage | Words Needed | Priority |
   |-------|---------------------|--------------|----------|
   | [Topic 1] | 3/5 competitors | ~300 words | High |
   | [Topic 2] | 2/5 competitors | ~200 words | Medium |
   | [Topic 3] | 4/5 competitors | ~400 words | High |
   
   ### SEO Updates Needed
   
   - [ ] Update title tag with current year
   - [ ] Refresh meta description
   - [ ] Add new H2 sections for [topics]
   - [ ] Update internal links to newer content
   - [ ] Add FAQ section for featured snippets
   - [ ] Refresh images and add new alt text
   
   ### GEO Updates Needed
   
   - [ ] Add clear definition at start
   - [ ] Include quotable statistics with sources
   - [ ] Add Q&A formatted sections
   - [ ] Update sources with current citations
   - [ ] Create standalone factual statements
   ```

5. **制定更新计划**  
   ```markdown
   ## Content Refresh Plan
   
   ### Title/URL
   **Current**: [current title]
   **Refreshed**: [updated title with year/hook]
   
   ### Structural Changes
   
   **Keep As-Is**:
   - [Section 1] - Still relevant and accurate
   - [Section 2] - Still relevant and accurate
   
   **Update/Expand**:
   - [Section 3] - Update statistics, add [X] words
   - [Section 4] - Add new examples from [current year]
   
   **Add New Sections**:
   - [New Section 1] - [description, ~X words]
   - [New Section 2] - [description, ~X words]
   - FAQ Section - [X questions for featured snippets]
   
   **Remove/Consolidate**:
   - [Section 5] - Outdated, remove or redirect topic
   
   ### Content Additions
   
   **New Word Count Target**: [X] words (+[Y] from current)
   
   | Section | Current | After Refresh | Notes |
   |---------|---------|---------------|-------|
   | Introduction | [X] | [X] | Add hook, update context |
   | [Section 1] | [X] | [X] | Keep |
   | [Section 2] | [X] | [X] | Update stats |
   | [New Section] | 0 | [X] | Add entirely |
   | FAQ | 0 | [X] | Add for GEO |
   | Conclusion | [X] | [X] | Update CTA |
   
   ### Specific Updates
   
   **Statistics to Update**:
   
   | Old Statistic | New Statistic | Source |
   |---------------|---------------|--------|
   | "[old stat]" | "[find current]" | [source] |
   | "[old stat]" | "[find current]" | [source] |
   
   **Links to Update**:
   
   | Anchor Text | Old URL | New URL | Reason |
   |-------------|---------|---------|--------|
   | "[anchor]" | [old] | [new] | Broken |
   | "[anchor]" | [old] | [new] | Better resource |
   
   **Images to Update**:
   
   | Image | Action | New Alt Text |
   |-------|--------|--------------|
   | [img 1] | Replace | "[keyword-rich alt]" |
   | [img 2] | Keep | Update alt text |
   ```

6. **编写更新后的内容**  
   ```markdown
   ## Refreshed Content Sections
   
   ### Updated Introduction
   
   [Write new introduction with:]
   - Updated hook for current year
   - Fresh statistics
   - Clear value proposition
   - Primary keyword in first 100 words
   
   ### New Section: [Title]
   
   [Write new section covering:]
   - [Topic competitors now cover]
   - Current information and examples
   - GEO-optimized with quotable statements
   
   ### Updated Statistics Section
   
   **Replace**:
   > "[Old statement with outdated stat]"
   
   **With**:
   > "[New statement with current stat] (Source, [current year])"
   
   ### New FAQ Section
   
   ## Frequently Asked Questions
   
   ### [Question matching PAA/common query]?
   
   [Direct answer in 40-60 words, optimized for featured snippets]
   
   ### [Question 2]?
   
   [Direct answer]
   
   ### [Question 3]?
   
   [Direct answer]
   ```

7. **在更新过程中进行地理优化**  
   ```markdown
   ## GEO Enhancement Opportunities
   
   ### Add Clear Definitions
   
   **Add at start of article**:
   > **[Topic]** is [clear, quotable definition in 40-60 words that 
   > AI systems can cite directly].
   
   ### Add Quotable Statements
   
   **Transform**:
   > "Email marketing is effective for businesses."
   
   **Into**:
   > "Email marketing delivers an average ROI of $42 for every $1 
   > invested, making it the highest-ROI digital marketing channel 
   > according to the Data & Marketing Association ([current year])."
   
   ### Add Q&A Sections
   
   Structure content with questions AI might answer:
   - What is [topic]?
   - How does [topic] work?
   - Why is [topic] important?
   - What are the benefits of [topic]?
   
   ### Update Citations
   
   - Add sources for all statistics
   - Link to authoritative references
   - Include publication dates
   - Use recent sources (last 2 years)
   ```

8. **制定重新发布策略**  
   ```markdown
   ## Republishing Strategy
   
   ### Date Strategy
   
   **Options**:
   
   1. **Update Published Date** 
      - Use when: Major overhaul (50%+ new content)
      - Pros: Signals freshness to Google
      - Cons: Loses "original" authority
   
   2. **Add "Last Updated" Date**
      - Use when: Moderate updates (20-50% new)
      - Pros: Shows both original and fresh
      - Cons: Original date visible
   
   3. **Keep Original Date**
      - Use when: Minor updates (<20% new)
      - Pros: Maintains authority
      - Cons: Doesn't signal update
   
   **Recommendation**: [Option X] because [reason]
   
   ### Technical Implementation
   
   - [ ] Update `dateModified` in schema
   - [ ] Update sitemap lastmod
   - [ ] Clear cache after publishing
   - [ ] Resubmit to ~~search console
   
   ### Promotion Strategy
   
   **Immediately after refresh**:
   - [ ] Share on social media as "updated for [current year]"
   - [ ] Send to email list if significant update
   - [ ] Update internal links with fresh anchors
   - [ ] Reach out for new backlinks
   
   **Track Results**:
   - [ ] Monitor rankings for 4-6 weeks
   - [ ] Track traffic changes
   - [ ] Watch for featured snippet capture
   - [ ] Check AI citation improvements
   ```

9. **生成更新报告**  
   ```markdown
   # Content Refresh Report
   
   ## Summary
   
   **Content**: [Title]
   **Refresh Date**: [Date]
   **Refresh Level**: [Major/Moderate/Minor]
   
   ## Changes Made
   
   | Element | Before | After |
   |---------|--------|-------|
   | Word count | [X] | [Y] (+[Z]%) |
   | Sections | [X] | [Y] |
   | Statistics | [X] outdated | [Y] current |
   | Internal links | [X] | [Y] |
   | Images | [X] | [Y] |
   | FAQ questions | 0 | [X] |
   
   ## Updates Completed
   
   - [x] Updated title with current year
   - [x] Refreshed meta description
   - [x] Added [X] new sections
   - [x] Updated [X] statistics with sources
   - [x] Fixed [X] broken links
   - [x] Added FAQ section for GEO
   - [x] Implemented FAQ schema
   - [x] Updated images and alt text
   
   ## Expected Outcomes
   
   | Metric | Current | 30-Day Target | 90-Day Target |
   |--------|---------|---------------|---------------|
   | Avg Position | [X] | [Y] | [Z] |
   | Organic Traffic | [X]/mo | [Y]/mo | [Z]/mo |
   | Featured Snippets | 0 | 1+ | 2+ |
   
   ## Next Review

   Schedule next refresh review: [Date - 6 months from now]
   ```

## 验证检查点

### 输入验证
- [ ] 明确指出了目标内容的URL或标题  
- [ ] 有历史性能数据（流量趋势、排名）  
- [ ] 知道内容的发布/更新日期  
- [ ] 如果与竞争对手进行比较，提供了竞争对手的URL  

### 输出验证
- [ ] 每条建议都引用了具体的数据点（而非泛泛而谈的建议）  
- [ ] 用具体的例子和替换数据指出了过时的部分  
- [ ] 所有建议的添加内容都包括了字数和位置  
- [ ] 每个数据点的来源都明确标注（来自 ~~分析工具、~~搜索控制台、~~SEO工具、用户提供或估算）

## 示例

**用户**：“更新我关于‘最佳云托管服务提供商’的博客文章”

**输出**：

```markdown
### CORE-EEAT Quick Assessment

**Content**: "Best Cloud Hosting Providers 2023"
**Content Type**: Commercial comparison / listicle

| Dimension | Quick Score | Key Weakness | Refresh Priority |
|-----------|-----------|--------------|-----------------|
| C — Contextual Clarity | 60/100 | Title says 2023 — stale intent signal | 🔴 |
| O — Organization | 75/100 | Good comparison tables but no summary box | 🟡 |
| R — Referenceability | 35/100 | Pricing from Q1 2023, 3 broken links | 🔴 |
| E — Exclusivity | 50/100 | No original benchmarks or test data | 🟡 |
| Exp — Experience | 30/100 | No first-person testing narrative | 🔴 |
| Ept — Expertise | 65/100 | Author bio present but lacks credentials | 🟡 |
| A — Authority | 55/100 | 12 backlinks, was ranking page 1 | 🟢 |
| T — Trust | 60/100 | Affiliate links present but not disclosed | 🔴 |

**Weakest Dimensions** (focus refresh here):
1. **Experience** — Add hands-on testing results ("We migrated a test site to each provider")
2. **Referenceability** — Replace all 2023 pricing/uptime data with current figures

## Content Refresh Analysis: Best Cloud Hosting Providers 2023

**URL**: cloudhosting.com/best-cloud-hosting
**Published**: 2023-02-14
**Last Updated**: Never
**Word Count**: 2,100

### Performance Metrics

| Metric | 6 Mo Ago | Current | Change |
|--------|----------|---------|--------|
| Organic Traffic | 3,200/mo | 1,400/mo | -56% |
| Avg Position | 4.2 | 14.8 | ↓ 10.6 |
| Impressions | 18,000 | 9,500 | -47% |
| CTR | 6.1% | 2.3% | -3.8% |

### Content Decay Signals Identified

1. **Outdated year in title and H1** — "2023" signals stale content to users and search engines
2. **Pricing data 18+ months old** — AWS Lightsail listed at $3.50/mo (now $5/mo), DigitalOcean at $4/mo (now $6/mo)
3. **Missing new entrants** — No mention of Hetzner Cloud or Vultr, which 4/5 top competitors now cover
4. **3 broken outbound links** — Provider comparison pages that have moved or been retired

### Refresh vs. Rewrite Decision

| Factor | Assessment |
|--------|-----------|
| Content quality | Good structure, solid comparison tables — foundation is sound |
| URL equity | 12 referring domains, 18 months old |
| Scope of changes | ~40% of content needs updating |
| Search intent | Unchanged — still commercial comparison |

**Decision**: **REFRESH** — The URL has earned backlinks, the structure is solid, and less than 50% needs rewriting. Keep the URL, update in place.

## Content Refresh Plan

**Current Title**: "Best Cloud Hosting Providers 2023"
**Refreshed Title**: "Best Cloud Hosting Providers 2024: 7 Platforms Tested & Compared"

### Specific Refresh Actions

1. **Update all pricing and specs** (~30 min)
   - Replace 2023 pricing for all 5 listed providers with current data
   - Add uptime stats from the last 12 months (source: UptimeRobot public status pages)
   - Update feature comparison table with current plan tiers

2. **Add 2 missing providers + testing narrative** (~600 words)
   - Add Hetzner Cloud and Vultr sections with same comparison format
   - Write intro paragraph: "We deployed a WordPress benchmark site to each provider and measured TTFB, uptime, and support response times over 30 days"

3. **Add affiliate disclosure and FAQ section** (~200 words)
   - Add disclosure statement below introduction: "This post contains affiliate links. See our editorial policy."
   - Add FAQ with 4 questions targeting People Also Ask (e.g., "What is the cheapest cloud hosting?", "Is cloud hosting faster than shared hosting?")
   - Implement FAQ schema markup for rich result eligibility

4. **Fix broken links and update internal links** (~15 min)
   - Replace 3 broken outbound links with current provider URLs
   - Add internal links to cloudhosting.com/vps-vs-cloud and cloudhosting.com/hosting-speed-test

### Republishing Strategy

**Recommendation**: Update Published Date — this is a major overhaul (40%+ new content, new providers, fresh test data). Update `dateModified` in Article schema, resubmit URL in Search Console, and share on social as "Updated for 2024."

### Expected Outcomes

| Metric | Current | 30-Day Target | 90-Day Target |
|--------|---------|---------------|---------------|
| Avg Position | 14.8 | 8-10 | 3-6 |
| Organic Traffic | 1,400/mo | 2,200/mo | 3,500/mo |
| Featured Snippets | 0 | 1 (FAQ) | 2+ |
```

## 内容更新检查清单

```markdown
### Pre-Refresh
- [ ] Analyze current performance metrics
- [ ] Identify outdated information
- [ ] Research competitor updates
- [ ] Note missing topics

### Content Updates
- [ ] Update year references
- [ ] Refresh statistics with sources
- [ ] Add new examples and case studies
- [ ] Expand thin sections
- [ ] Add new relevant sections
- [ ] Create FAQ section

### SEO Updates
- [ ] Update title tag
- [ ] Refresh meta description
- [ ] Optimize headers
- [ ] Update internal links
- [ ] Add new images with alt text

### GEO Updates
- [ ] Add clear definition
- [ ] Include quotable statements
- [ ] Add Q&A formatted content
- [ ] Update source citations

### Technical
- [ ] Update schema dateModified
- [ ] Clear page cache
- [ ] Update sitemap
- [ ] Test page speed
```

## 成功技巧

1. **按投资回报率（ROI）优先排序** — 先更新潜力高的内容  
2. **不要只是添加日期** — 要做出实质性的改进  
3. **超越竞争对手** — 不仅添加他们有的内容，还要添加更多有价值的内容  
4. **跟踪结果** — 更新后监控排名变化  
5. **定期进行审核** — 每季度检查内容的状态  
6. **进行地理优化** — 每次更新都是一个优化地理定位的机会  

## 内容衰退信号分类

### 衰退指标

| 信号 | 来源 | 严重程度 | 检测方法 |
|--------|--------|----------|-----------------|
| 每月流量下降超过20% | 分析工具 | 高 | 每月流量对比 |
| 排名下降超过5位 | 排名追踪器 | 高 | 每周排名监控 |
| 统计数据/日期过时 | 手动审核 | 中等 | 年度内容审核 |
| 外部链接失效 | 爬虫工具 | 中等 | 每月爬取报告 |
| 点击率（CTR）下降 | 搜索控制台 | 中等 | 每季度CTR分析 |
| 竞争对手发布了新内容 | SERP监控 | 中等 | 每月SERP检查 |
| 用户参与度下降 | 分析工具 | 低 | 每季度参与度审核 |
| 索引覆盖问题 | 搜索控制台 | 高 | 每周索引覆盖监控 |

### 内容衰退阶段

| 阶段 | 症状 | 紧急程度 | 建议措施 |
|-------|---------|---------|-------------------|
| **早期衰退** | 流量/排名略有下降 | 低 | 监控2-4周 |
| **活跃衰退** | 连续2个月以上持续下降 | 中等 | 在2周内安排更新 |
| **严重衰退** | 流量下降超过50%，页面排名下降超过2位 | 高 | 立即更新或重写 |
| **彻底衰退** | 无自然流量，被搜索引擎索引移除 | 关键 | 重写、重定向或移除 |

## 更新与重写决策框架

| 因素 | 更新 | 重写（新版本） |
|--------|-----------------|---------------------|
| 内容质量 | 基础良好，需要更新 | 基本存在缺陷或方法过时 |
| 排名 | 曾经排名较高，但现在下降 | 尽管进行了优化但仍排名不佳 |
| URL年龄 | 已存在超过1年且有反向链接 | 新URL且没有反向链接价值 |
| 反向链接 | 有外部链接指向该URL | 无值得保留的反向链接 |
| 需要更改的范围 | 内容更改比例小于50% | 超过50%需要重写 |
| 搜索意图 | 搜索意图未改变 | 搜索意图发生了变化 |

**决策规则：** 如果URL有反向链接且曾经排名良好，则进行更新；如果没有，则考虑在新URL上重写（如果旧URL有价值，可以使用301重定向）。  

## 内容生命周期模型

```
CREATE → PROMOTE → MAINTAIN → REFRESH → [REFRESH again] or RETIRE
  │         │          │          │                          │
  │      Month 1    Month 2-6   Month 6-12              When terminal
  │    Social,      Monitor     Update facts,            301 redirect
  │    outreach,    rankings,   add new sections,         to related
  │    email        fix issues  improve depth              content
```

### 各阶段的生命周期操作

| 阶段 | 持续时间 | 关键操作 | 需要跟踪的指标 |
|-------|----------|------------|-----------------|
| 创建 | 第1周 | 发布内容，提交至搜索控制台 | 索引化 |
| 推广 | 第1个月 | 通过社交媒体分享、发送邮件等方式进行推广 | 引荐流量、获取反向链接 |
| 维护 | 第2-6个月 | 监控内容，修复失效链接，回复评论 | 排名、流量趋势 |
| 更新 | 第6-12个月以上 | 更新数据，添加新章节，优化结构 | 恢复流量，引入新关键词 |
| 移除 | 当内容完全过时 | 使用301重定向指向最佳替代内容 | 重定向以恢复流量 |

## 根据内容类型制定更新策略

| 内容类型 | 更新频率 | 关键更新内容 | 生命周期 |
|-------------|-------------------|------------|-----------|
| 统计汇总 | 每6个月 | 更换旧统计数据，添加新来源 | 6-12个月 |
| 工具对比 | 每3-6个月 | 更新价格、功能、截图 | 3-6个月 |
| 操作指南 | 每年 | 更新步骤、添加截图、链接 | 12-18个月 |
| 永恒指南 | 每12-18个月 | 添加新章节，更新示例 | 18-24个月 |
| 新闻/趋势内容 | 不需要更新 | 将其归档或重定向 | 1-3个月 |
| 案例研究 | 很少需要更新 | 如果有新数据则更新 | 2-3年 |
| 术语表/定义 | 根据需要 | 定义发生变化时更新 | 2-5年 |

## 参考资料

- [内容衰退信号](./references/content-decay-signals.md) — 不同类型内容的衰退指标、生命周期阶段和更新触发条件

## 相关技能

- [内容差距分析](../../research/content-gap-analysis/) — 确定需要添加的内容  
- [SEO内容编写器](../../build/seo-content-writer/) — 编写新章节  
- [地理内容优化器](../../build/geo-content-optimizer/) — 优化内容以适应AI需求  
- [页面SEO审核器](../on-page-seo-auditor/) — 审核更新后的内容  
- [内容质量审核器](../../cross-cutting/content-quality-auditor/) — 进行全面的80项CORE-EEAT审核