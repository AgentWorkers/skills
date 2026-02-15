---
name: on-page-seo-auditor
description: '**使用说明：**  
当用户请求进行“页面SEO审计”、“页面SEO检查”、“SEO评分”、“页面优化”、“此页面存在哪些SEO问题”、“此页面的SEO有哪些问题”、“为我页面评分”或“为什么这个页面没有排名”时，请使用该工具。该工具会执行全面的页面SEO审计，以识别优化机会，包括标题标签、元描述、页面头部、内容质量、内部链接以及图片优化等方面。对于服务器速度和爬虫相关的问题，请参考`technical-seo-checker`；如需进行全面的EEAT（Engineering, Environment, and Artifacts）内容质量评分，请参考`content-quality-auditor`。'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "medium"
  tags:
    - seo
    - on-page audit
    - page optimization
    - seo audit
    - content optimization
    - header tags
    - image optimization
    - seo score
  triggers:
    - "audit page SEO"
    - "on-page SEO check"
    - "SEO score"
    - "page optimization"
    - "what SEO issues"
    - "check my page"
    - "on-page audit"
    - "what's wrong with this page's SEO"
    - "score my page"
    - "why isn't this page ranking"
---

# 在页面上的SEO审计工具

> **[SEO与地理位置技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与地理位置相关技能 · 全部安装方法：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容编写器](../../build/seo-content-writer/) · [地理位置内容优化器](../../build/geo-content-optimizer/) · [元标签优化器](../../build/meta-tags-optimizer/) · [架构标记生成器](../../build/schema-markup-generator/)

**优化** · **在页面上的SEO审计** · [技术SEO检查器](../technical-seo-checker/) · [内部链接优化器](../internal-linking-optimizer/) · [内容更新器](../content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告器](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)

**跨领域** · [内容质量审计器](../../cross-cutting/content-quality-auditor/) · [域名权威性审计器](../../cross-cutting/domain-authority-auditor/) · [实体优化器](../../cross-cutting/entity-optimizer/) · [内存管理](../../cross-cutting/memory-management/)

</details>

该工具可执行详细的在页面上的SEO审计，以识别问题并发现优化机会。它分析所有影响搜索排名的页面元素，并提供可操作的改进建议。

## 何时使用此技能

- 在页面发布前后进行审计
- 查明页面排名不佳的原因
- 优化现有内容以提高性能
- 创建发布前的SEO检查清单
- 与竞争对手比较在页面上的SEO情况
- 进行系统性的全站SEO改进
- 培训团队成员掌握SEO最佳实践

## 该技能的功能

1. **标题标签分析**：评估标题的优化程度和点击率潜力
2. **元描述审核**：检查描述的质量和长度
3. **标题结构审计**：分析H1-H6标题的层次结构
4. **内容质量评估**：审查内容的深度和优化情况
5. **关键词使用分析**：检查关键词的放置和密度
6. **内部链接审核**：评估内部链接的结构
7. **图片优化检查**：审核图片的alt文本和文件优化情况
8. **技术性在页面上的审核**：检查URL、规范链接以及移动设备兼容性

## 使用方法

### 审计单个页面

```
Audit the on-page SEO of [URL]
```

```
Check SEO issues on this page targeting [keyword]: [URL/content]
```

### 与竞争对手进行比较

```
Compare on-page SEO of [your URL] vs [competitor URL] for [keyword]
```

### 在发布前审计内容

```
Pre-publish SEO audit for this content targeting [keyword]: [content]
```

## 数据来源

> 请参阅[CONNECTORS.md](../../CONNECTORS.md)以获取工具类别的相关信息。

**当与SEO工具和网络爬虫连接时：**
Claude可以通过网络爬虫自动获取页面HTML，从SEO工具中获取关键词搜索量和难度数据，从搜索控制台获取点击率数据，并下载竞争对手的页面进行比较。这可以实现基于实时数据的完全自动化审计。

**仅使用手动数据时：**
要求用户提供：
1. 页面URL或完整的HTML内容
2. 目标的主要和次要关键词
3. 用于比较的竞争对手页面URL（可选）

使用提供的数据进行完整审计。在输出中注明哪些发现是来自自动化爬取，哪些是来自手动审核。

## 指令

当用户请求进行在页面上的SEO审计时：

1. **收集页面信息**

   ```markdown
   ### Audit Setup
   
   **Page URL**: [URL]
   **Target Keyword**: [primary keyword]
   **Secondary Keywords**: [additional keywords]
   **Page Type**: [blog/product/landing/service]
   **Business Goal**: [traffic/conversions/authority]
   ```

2. **审计标题标签**

   ```markdown
   ## Title Tag Analysis
   
   **Current Title**: [title]
   **Character Count**: [X] characters
   
   | Criterion | Status | Notes |
   |-----------|--------|-------|
   | Length (50-60 chars) | ✅/⚠️/❌ | [notes] |
   | Keyword included | ✅/⚠️/❌ | Position: [front/middle/end] |
   | Keyword at front | ✅/⚠️/❌ | [notes] |
   | Unique across site | ✅/⚠️/❌ | [notes] |
   | Compelling/clickable | ✅/⚠️/❌ | [notes] |
   | Matches intent | ✅/⚠️/❌ | [notes] |
   
   **Title Score**: [X]/10
   
   **Issues Found**:
   - [Issue 1]
   - [Issue 2]
   
   **Recommended Title**:
   "[Optimized title suggestion]"
   
   **Why**: [Explanation of improvements]
   ```

3. **审计元描述**

   ```markdown
   ## Meta Description Analysis
   
   **Current Description**: [description]
   **Character Count**: [X] characters
   
   | Criterion | Status | Notes |
   |-----------|--------|-------|
   | Length (150-160 chars) | ✅/⚠️/❌ | [notes] |
   | Keyword included | ✅/⚠️/❌ | [notes] |
   | Call-to-action present | ✅/⚠️/❌ | [notes] |
   | Unique across site | ✅/⚠️/❌ | [notes] |
   | Accurately describes page | ✅/⚠️/❌ | [notes] |
   | Compelling copy | ✅/⚠️/❌ | [notes] |
   
   **Description Score**: [X]/10
   
   **Issues Found**:
   - [Issue 1]
   
   **Recommended Description**:
   "[Optimized description suggestion]" ([X] chars)
   ```

4. **审计标题结构**

   ```markdown
   ## Header Structure Analysis
   
   ### Current Header Hierarchy
   
   ```
   H1: [H1文本]
     H2: [H2文本]
       H3: [H3文本]
       H3: [H3文本]
     H2: [H2文本]
       H3: [H3文本]
     H2: [H2文本]
       H3: [H3文本]
   ```
   
   | Criterion | Status | Notes |
   |-----------|--------|-------|
   | Single H1 | ✅/⚠️/❌ | Found: [X] H1s |
   | H1 includes keyword | ✅/⚠️/❌ | [notes] |
   | Logical hierarchy | ✅/⚠️/❌ | [notes] |
   | H2s include keywords | ✅/⚠️/❌ | [X]/[Y] contain keywords |
   | No skipped levels | ✅/⚠️/❌ | [notes] |
   | Descriptive headers | ✅/⚠️/❌ | [notes] |
   
   **Header Score**: [X]/10
   
   **Issues Found**:
   - [Issue 1]
   - [Issue 2]
   
   **Recommended Changes**:
   - H1: [suggestion]
   - H2s: [suggestions]
   ```

5. **审计内容质量**

   ```markdown
   ## Content Quality Analysis
   
   **Word Count**: [X] words
   **Reading Level**: [Grade level]
   **Estimated Read Time**: [X] minutes
   
   | Criterion | Status | Notes |
   |-----------|--------|-------|
   | Sufficient length | ✅/⚠️/❌ | [comparison to ranking content] |
   | Comprehensive coverage | ✅/⚠️/❌ | [notes] |
   | Unique value/insights | ✅/⚠️/❌ | [notes] |
   | Up-to-date information | ✅/⚠️/❌ | [notes] |
   | Proper formatting | ✅/⚠️/❌ | [notes] |
   | Readability | ✅/⚠️/❌ | [notes] |
   | E-E-A-T signals | ✅/⚠️/❌ | [notes] |
   
   **Content Elements Present**:
   - [ ] Introduction with keyword
   - [ ] Clear sections/structure
   - [ ] Bullet points/lists
   - [ ] Tables where appropriate
   - [ ] Images/visuals
   - [ ] Examples/case studies
   - [ ] Statistics with sources
   - [ ] Expert quotes
   - [ ] FAQ section
   - [ ] Conclusion with CTA
   
   **Content Score**: [X]/10
   
   **Gaps Identified**:
   - [Missing topic/section 1]
   - [Missing topic/section 2]
   
   **Recommendations**:
   1. [Specific improvement]
   2. [Specific improvement]
   ```

6. **审计关键词使用情况**

   ```markdown
   ## Keyword Optimization Analysis
   
   **Primary Keyword**: "[keyword]"
   **Keyword Density**: [X]%
   
   ### Keyword Placement
   
   | Location | Present | Notes |
   |----------|---------|-------|
   | Title tag | ✅/❌ | Position: [X] |
   | Meta description | ✅/❌ | [notes] |
   | H1 | ✅/❌ | [notes] |
   | First 100 words | ✅/❌ | Word position: [X] |
   | H2 headings | ✅/❌ | In [X]/[Y] H2s |
   | Body content | ✅/❌ | [X] occurrences |
   | URL slug | ✅/❌ | [notes] |
   | Image alt text | ✅/❌ | In [X]/[Y] images |
   | Conclusion | ✅/❌ | [notes] |
   
   ### Secondary Keywords
   
   | Keyword | Occurrences | Status |
   |---------|-------------|--------|
   | [keyword 1] | [X] | ✅/⚠️/❌ |
   | [keyword 2] | [X] | ✅/⚠️/❌ |
   
   ### LSI/Related Terms
   
   **Present**: [list of related terms found]
   **Missing**: [important related terms not found]
   
   **Keyword Score**: [X]/10
   
   **Issues**:
   - [Issue 1]
   
   **Recommendations**:
   - [Suggestion 1]
   ```

7. **审计内部链接**

   ```markdown
   ## Internal Linking Analysis
   
   **Total Internal Links**: [X]
   **Unique Internal Links**: [X]
   
   | Criterion | Status | Notes |
   |-----------|--------|-------|
   | Number of internal links | ✅/⚠️/❌ | [X] (recommend 3-5+) |
   | Relevant anchor text | ✅/⚠️/❌ | [notes] |
   | Links to related content | ✅/⚠️/❌ | [notes] |
   | Links to important pages | ✅/⚠️/❌ | [notes] |
   | No broken links | ✅/⚠️/❌ | [X] broken found |
   | Natural placement | ✅/⚠️/❌ | [notes] |
   
   **Current Internal Links**:
   1. "[Anchor text]" → [URL]
   2. "[Anchor text]" → [URL]
   3. "[Anchor text]" → [URL]
   
   **Internal Linking Score**: [X]/10
   
   **Recommended Additional Links**:
   1. Add link to "[Related page]" with anchor "[suggested anchor]"
   2. Add link to "[Related page]" with anchor "[suggested anchor]"
   
   **Anchor Text Improvements**:
   - Change "[current anchor]" to "[improved anchor]"
   ```

8. **审计图片**

   ```markdown
   ## Image Optimization Analysis
   
   **Total Images**: [X]
   
   ### Image Audit Table
   
   | Image | Alt Text | File Name | Size | Status |
   |-------|----------|-----------|------|--------|
   | [img1] | [alt or "missing"] | [filename] | [KB] | ✅/⚠️/❌ |
   | [img2] | [alt or "missing"] | [filename] | [KB] | ✅/⚠️/❌ |
   
   | Criterion | Status | Notes |
   |-----------|--------|-------|
   | All images have alt text | ✅/⚠️/❌ | [X]/[Y] have alt |
   | Alt text includes keywords | ✅/⚠️/❌ | [notes] |
   | Descriptive file names | ✅/⚠️/❌ | [notes] |
   | Appropriate file sizes | ✅/⚠️/❌ | [notes] |
   | Modern formats (WebP) | ✅/⚠️/❌ | [notes] |
   | Lazy loading enabled | ✅/⚠️/❌ | [notes] |
   
   **Image Score**: [X]/10
   
   **Recommendations**:
   1. Add alt text to image [X]: "[suggested alt text]"
   2. Compress image [Y]: Currently [X]KB, should be under [Y]KB
   3. Rename [filename] to [better-filename]
   ```

9. **审计技术性在页面上的元素**

   ```markdown
   ## Technical On-Page Analysis
   
   | Element | Current Value | Status | Recommendation |
   |---------|---------------|--------|----------------|
   | URL | [URL] | ✅/⚠️/❌ | [notes] |
   | URL length | [X] chars | ✅/⚠️/❌ | [notes] |
   | URL keywords | [present/absent] | ✅/⚠️/❌ | [notes] |
   | Canonical tag | [URL or "missing"] | ✅/⚠️/❌ | [notes] |
   | Mobile-friendly | [yes/no] | ✅/⚠️/❌ | [notes] |
   | Page speed | [X]s | ✅/⚠️/❌ | [notes] |
   | HTTPS | [yes/no] | ✅/⚠️/❌ | [notes] |
   | Schema markup | [types or "none"] | ✅/⚠️/❌ | [notes] |
   
   **Technical Score**: [X]/10
   ```

10. **CORE-EEAT内容质量快速扫描**
    对与页面内容相关的CORE-EEAT项目进行快速扫描。参考：[CORE-EEAT基准](../../references/core-eeat-benchmark.md)

    ```markdown
    ## CORE-EEAT Quick Scan

    Content-relevant items from the 80-item benchmark:

    | ID | Check Item | Status | Notes |
    |----|-----------|--------|-------|
    | C01 | Intent Alignment | ✅/⚠️/❌ | Title promise = content delivery |
    | C02 | Direct Answer | ✅/⚠️/❌ | Core answer in first 150 words |
    | C09 | FAQ Coverage | ✅/⚠️/❌ | Structured FAQ present |
    | C10 | Semantic Closure | ✅/⚠️/❌ | Conclusion answers opening |
    | O01 | Heading Hierarchy | ✅/⚠️/❌ | H1→H2→H3, no skipping |
    | O02 | Summary Box | ✅/⚠️/❌ | TL;DR or Key Takeaways |
    | O03 | Data Tables | ✅/⚠️/❌ | Comparisons in tables |
    | O05 | Schema Markup | ✅/⚠️/❌ | Appropriate JSON-LD |
    | O06 | Section Chunking | ✅/⚠️/❌ | Single topic per section |
    | R01 | Data Precision | ✅/⚠️/❌ | ≥5 precise numbers |
    | R02 | Citation Density | ✅/⚠️/❌ | ≥1 per 500 words |
    | R06 | Timestamp | ✅/⚠️/❌ | Updated <1 year |
    | R08 | Internal Link Graph | ✅/⚠️/❌ | Descriptive anchors |
    | R10 | Content Consistency | ✅/⚠️/❌ | No contradictions |
    | Exp01 | First-Person Narrative | ✅/⚠️/❌ | "I tested" or "We found" |
    | Ept01 | Author Identity | ✅/⚠️/❌ | Byline + bio present |
    | T04 | Disclosure Statements | ✅/⚠️/❌ | Affiliate links disclosed |

    **CORE-EEAT Quick Score**: [X]/17 items passing

    > For a complete 80-item audit with weighted scoring, use [content-quality-auditor](../../cross-cutting/content-quality-auditor/).
    ```

11. **生成审计报告**

    ```markdown
    # On-Page SEO Audit Report
    
    **Page**: [URL]
    **Target Keyword**: [keyword]
    **Audit Date**: [date]
    
    ## Overall Score: [X]/100
    
    ```
    评分详情：
    ████████░░ 标题标签：8/10
    ██████░░░░ 元描述：6/10
    █████████░ 标题结构：9/10
    ███████░░░ 内容：7/10
    ██████░░░ 关键词：6/10
    █████░░░░ 内部链接：5/10
    ████░░░░░ 图片：4/10
    ████████░░ 技术性：8/10
    ```
    
    ## Priority Issues
    
    ### 🔴 Critical (Fix Immediately)
    1. [Critical issue 1]
    2. [Critical issue 2]
    
    ### 🟡 Important (Fix Soon)
    1. [Important issue 1]
    2. [Important issue 2]
    
    ### 🟢 Minor (Nice to Have)
    1. [Minor issue 1]
    2. [Minor issue 2]
    
    ## Quick Wins
    
    These changes will have immediate impact:
    
    1. **[Change 1]**: [Why and how]
    2. **[Change 2]**: [Why and how]
    3. **[Change 3]**: [Why and how]
    
    ## Detailed Recommendations
    
    ### Title Tag
    - **Current**: [current title]
    - **Recommended**: [new title]
    - **Impact**: [expected improvement]
    
    ### Meta Description
    - **Current**: [current description]
    - **Recommended**: [new description]
    - **Impact**: [expected improvement]
    
    ### Content Improvements
    1. [Specific content change with location]
    2. [Specific content change with location]
    
    ### Internal Linking
    1. Add link: "[anchor]" → [destination]
    2. Add link: "[anchor]" → [destination]
    
    ### Image Optimization
    1. [Image 1]: [change needed]
    2. [Image 2]: [change needed]
    
    ## Competitor Comparison
    
    | Element | Your Page | Top Competitor | Gap |
    |---------|-----------|----------------|-----|
    | Word count | [X] | [Y] | [+/-Z] |
    | Internal links | [X] | [Y] | [+/-Z] |
    | Images | [X] | [Y] | [+/-Z] |
    | H2 headings | [X] | [Y] | [+/-Z] |
    
    ## Action Checklist
    
    - [ ] Update title tag
    - [ ] Rewrite meta description
    - [ ] Add keyword to H1
    - [ ] Add [X] more internal links
    - [ ] Add alt text to [X] images
    - [ ] Add [X] more content sections
    - [ ] Implement FAQ schema
    - [ ] [Additional action items]
    
    ## Expected Results

    After implementing these changes:
    - Estimated ranking improvement: [X] positions
    - Estimated CTR improvement: [X]%
    - Estimated traffic increase: [X]%
    ```

## 验证检查点

### 输入验证
- [ ] 用户明确指定了目标关键词
- [ ] 页面内容可通过URL或提供的HTML访问
- [ ] 如果请求与竞争对手比较，则提供了竞争对手的URL

### 输出验证
- [ ] 每条建议都引用了具体的数据点（而非泛泛而谈）
- [ ] 评分基于可衡量的标准，而非主观意见
- [ ] 所有建议的修改都指明了具体的位置（如标题标签、H2标签、第5段等）
- [ ] 每个数据点的来源都明确标注（来自SEO工具、用户提供的数据或手动审核）

## 示例

**用户**：“审计https://example.com/best-noise-cancelling-headphones页面的SEO，目标关键词为‘best noise cancelling headphones’”

**输出**：

```markdown
# On-Page SEO Audit Report

**Page**: https://example.com/best-noise-cancelling-headphones
**Target Keyword**: best noise cancelling headphones
**Secondary Keywords**: wireless noise cancelling headphones, ANC headphones, noise cancelling headphones review
**Page Type**: commercial (reviews/roundup)
**Audit Date**: 2025-01-15

## Summary

| Audit Area | Score | Key Finding |
|------------|-------|-------------|
| Title Tag | 8/10 | Good keyword placement; slightly long at 63 chars |
| Meta Description | 6/10 | Missing CTA; keyword present but generic copy |
| Header Structure | 9/10 | Clean hierarchy; H2s cover all major products |
| Content Quality | 7/10 | 2,400 words is solid; lacks original test data |
| Keyword Optimization | 8/10 | Strong placement; density at 1.2% is healthy |
| Internal Links | 5/10 | Only 2 internal links; missing links to brand pages |
| Images | 6/10 | 3/8 images missing alt text; no WebP format |
| Technical Elements | 7/10 | Missing Product schema; good URL and mobile |

## Overall Score: 71/100

Calculation: (8x0.15 + 6x0.05 + 9x0.10 + 7x0.25 + 8x0.15 + 5x0.10 + 6x0.10 + 7x0.10) x 10 = 71

Score Breakdown:
████████░░ Title Tag:        8/10  (15%)
██████░░░░ Meta Description: 6/10  ( 5%)
█████████░ Headers:          9/10  (10%)
███████░░░ Content:          7/10  (25%)
████████░░ Keywords:         8/10  (15%)
█████░░░░░ Internal Links:   5/10  (10%)
██████░░░░ Images:           6/10  (10%)
███████░░░ Technical:        7/10  (10%)

## Priority Issues

### Critical
1. **Internal linking severely underdeveloped** — Only 2 internal links found. Add links to individual headphone review pages (/sony-wh1000xm5-review, /bose-qc-ultra-review) and the headphones category page. Target 5-8 contextual internal links.
2. **3 product images missing alt text** — Images for Sony WH-1000XM5, Bose QC Ultra, and Apple AirPods Max have empty alt attributes. Each missing alt tag is a lost ranking signal in Google Images.

### Important
1. **Meta description lacks call-to-action** — Current description states facts but does not compel clicks. Add "Compare prices and features" or "See our top picks" to drive CTR.

## Quick Wins

1. **Add alt text to 3 images** (5 min) — Use descriptive text like "Sony WH-1000XM5 noise cancelling headphones on desk" instead of empty attributes.
2. **Rewrite meta description with CTA** (5 min) — Change to: "Compare the 10 best noise cancelling headphones for 2025. Expert-tested picks from Sony, Bose, and Apple with pros, cons, and pricing. See our top picks."
3. **Add 4+ internal links** (10 min) — Link product names to their individual review pages and add a "See all headphones" link to the category hub.
```

## 按页面类型划分的审计检查清单

### 博文检查清单

```markdown
- [ ] Title includes keyword and is compelling
- [ ] Meta description has keyword and CTA
- [ ] Single H1 with keyword
- [ ] H2s cover main topics
- [ ] Keyword in first 100 words
- [ ] 1,500+ words for competitive topics
- [ ] 3+ internal links with varied anchors
- [ ] Images with descriptive alt text
- [ ] FAQ section with schema
- [ ] Author bio with credentials
```

### 产品页面检查清单

```markdown
- [ ] Product name in title
- [ ] Price and availability in description
- [ ] H1 is product name
- [ ] Product features in H2s
- [ ] Multiple product images with alt text
- [ ] Customer reviews visible
- [ ] Product schema implemented
- [ ] Related products linked
- [ ] Clear CTA button
```

### 登录页面检查清单

```markdown
- [ ] Keyword-optimized title
- [ ] Benefit-focused meta description
- [ ] Clear H1 value proposition
- [ ] Supporting H2 sections
- [ ] Trust signals (testimonials, logos)
- [ ] Single clear CTA
- [ ] Fast page load speed
- [ ] Mobile-optimized layout
```

## 成功技巧

1. **按影响程度优先处理问题**——先解决关键问题
2. **与竞争对手比较**——了解哪些方法对排名有效
3. **平衡优化和可读性**——不要过度优化
4. **定期审计**——内容会随时间退化
5. **测试更改**——更新后跟踪排名变化

## 评分标准

### 各部分的权重分布

| 审计部分 | 权重 | 最高分 | 说明 |
|--------------|--------|-----------|-----------|
| 标题标签 | 15% | 15 | 最强的排名信号 |
| 元描述 | 5% | 5 | 影响点击率，但非直接排名因素 |
| 标题结构 | 10% | 10 | 内容组织结构，语义信号 |
| 内容质量 | 25% | 25 | 最强的整体排名因素 |
| 关键词优化 | 15% | 15 | 相关性信号 |
| 内部/外部链接 | 10% | 权威性流动，上下文信号 |
| 图片优化 | 10% | 可访问性和图片搜索机会 |
| 页面级技术性 | 10% | 核心网页指标，移动设备兼容性 |

### 每个因素的评分标准

| 评分 | 含义 | 需要采取的行动 |
|-------|---------|-----------------|
| 10/10 | 优秀 — 完全遵循最佳实践 | 无需额外操作 |
| 7-9/10 | 良好 — 可以进行小改进 | 可选优化 |
| 4-6/10 | 需要改进 — 存在明显问题 | 本周内解决 |
| 1-3/10 | 较差 — 有严重问题 | 立即解决（紧急） |
| 0/10 | 缺失或损坏 | 立即修复（可能导致排名问题） |

### 评分转换公式

每个部分的得分乘以相应的权重，得出总分：

```
Overall Score = Sum of (section_score x section_weight) x 10
```

部分权重如下：标题标签0.15，元描述0.05，标题结构0.10，内容0.25，关键词0.15，内部/外部链接0.10，图片0.10，技术性0.10。

**示例**：

| 部分 | 评分/10 | 权重 | 加权得分 |
|---------|-----------|--------|----------|
| 标题标签 | 8 | 0.15 | 1.20 |
| 元描述 | 6 | 0.05 | 0.30 |
| 标题结构 | 9 | 0.10 | 0.90 |
| 内容质量 | 7 | 0.25 | 1.75 |
| 关键词优化 | 8 | 0.15 | 1.20 |
| 内部/外部链接 | 5 | 0.10 | 0.50 |
| 图片优化 | 6 | 0.10 | 0.60 |
| 页面级技术性 | 7 | 0.10 | 0.70 |
| **总分** | | **7.15** | **71/100**

## 常见问题解决方案

### 标题标签问题

| 问题 | 影响 | 快速修复方法 |
|-------|--------|-------------------|
| 标题缺失 | 严重 | 添加：“[主要关键词]：[好处] | [品牌]” |
| 过长（>60个字符） | 中等 | 缩短标题长度；将品牌信息放在结尾 |
| 过短（<30个字符） | 中等 | 扩展标题内容，添加修饰词或好处描述 |
| 关键词缺失 | 严重 | 重新编写标题，确保包含主要关键词 |
| 标题重复 | 严重 | 为每个页面创建独特的标题，并添加具体描述 |

### 元描述问题

| 问题 | 影响 | 快速修复方法 |
|-------|--------|-------------------|
| 描述缺失 | 中等 | 编写：“[此页面介绍的内容]。[主要好处]。[行动号召]。”（150-160个字符） |
| 过长（>160个字符） | 低分 | 去除冗余部分，确保核心信息在150个字符内 |
| 关键词缺失 | 低分 | 自然地融入主要关键词 |
| 无行动号召 | 低分 | 添加“了解更多”、“发现”、“开始使用”等提示 |
| 多个页面使用相同描述 | 中等 | 为每个页面编写独特的描述 |

### 标题结构问题

| 问题 | 影响 | 快速修复方法 |
|-------|--------|-----------|
| 缺少H1标题 | 严重 | 为每个页面添加一个包含主要关键词的H1标题 |
| 多个H1标题 | 严重 | 保留一个H1标题，其余的改为H2标题 |
| 标题层次混乱 | 中等 | 保持H1→H2→H3的顺序 |
| 标题描述不够清晰 | 中等 | 重新编写标题，确保包含关键词变体 |
| 无H2标题（仅一个长段落） | 中等 | 将内容分成多个段落，并使用H2标题 |

### 内容问题

| 问题 | 影响 | 快速修复方法 |
|-------|--------|-----------|
| 内容太少（<300个字符） | 严重 | 添加子主题、常见问题解答或示例 |
| 关键词过度使用（>3%） | 严重 | 减少关键词使用频率，使用同义词和相关术语 |
| 缺乏结构化数据 | 中等 | 添加相关的数据结构（如FAQ、操作指南等） |
| 缺少内部链接 | 中等 | 添加3-5个相关的内部链接 |
| 无图片 | 低分 | 添加2-3张带有alt文本的图片 |

## 行业基准数据

### 不同查询类型的页面内容长度标准

| 查询类型 | 前10名页面的平均字数 | 推荐最低字数 |
|-----------|--------------------------|-------------------|
| 信息类（指南） | 2,200字 | 1,500字 |
| 商业类（评论） | 1,800字 | 1,200字 |
| 交易类（产品） | 800字 | 500字 |
| 地方服务类 | 600字 | 400字 |
| 定义类查询 | 1,200字 | 800字 |

### 页面速度基准

| 指标 | 良好 | 需要改进 | 较差 |
|--------|------|-------------------|------|
| LCP | ≤2.5秒 | 2.5-4.0秒 | >4.0秒 |
| FID/INP | ≤100毫秒/200毫秒 | 100-300毫秒 | >300毫秒 |
| CLS | ≤0.1 | 0.1-0.25 | >0.25 |
| TTFB | ≤800毫秒 | 800-1800毫秒 | >1800毫秒 |

## 参考资料

- [评分标准](./references/scoring-rubric.md) — 详细的评分标准、权重分布和评分范围

## 相关技能

- [SEO内容编写器](../../build/seo-content-writer/) — 创建优化后的内容
- [技术SEO检查器](../technical-seo-checker/) — 进行技术性SEO审计 |
- [元标签优化器](../../build/meta-tags-optimizer/) — 优化元标签 |
- [SERP分析](../../research/serp-analysis/) — 提供SERP分析结果 |
- [内容更新器](../content-refresher/) — 更新现有内容 |
- [内容质量审计器](../../cross-cutting/content-quality-auditor/) — 进行全面的CORE-EEAT审计 |
- [内部链接优化器](../internal-linking-optimizer/) — 优化内部链接结构 |
- [架构标记生成器](../../build/schema-markup-generator/) — 验证和生成架构标记