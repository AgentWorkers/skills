---
name: competitor-analysis
description: '**使用场景：**  
当用户请求“分析竞争对手”、“竞争对手的SEO策略”、“哪些关键词在排名中表现优异”、“进行竞争分析”、“了解竞争对手的运营情况”、“他们有哪些不同的做法”、“为什么他们的排名更高”，或“监视竞争对手的SEO策略”时，可使用该工具。该工具会分析竞争对手的SEO和地理位置策略，包括他们的排名关键词、内容创作方式、外部链接情况以及人工智能驱动的引用模式，从而帮助用户发现超越竞争对手的机会。  
**相关功能说明：**  
- **内容差距分析（Content Gap Analysis）**：适用于专注于内容差异的分析场景。  
- **外部链接分析器（Backlink Analyzer）**：提供详细的外部链接信息。'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "medium"
  tags:
    - seo
    - geo
    - competitor analysis
    - competitive intelligence
    - benchmarking
    - market analysis
    - ranking analysis
  triggers:
    - "analyze competitors"
    - "competitor SEO"
    - "who ranks for"
    - "competitive analysis"
    - "what are my competitors doing"
    - "competitor keywords"
    - "competitor backlinks"
    - "what are they doing differently"
    - "why do they rank higher"
    - "spy on competitor SEO"
---

# 竞争对手分析

> **[SEO与GEO技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 包含20项SEO与GEO相关技能 · 可通过 `npx skills add aaron-he-zhu/seo-geo-claude-skills` 安装

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../keyword-research/) · **竞争对手分析** · [SERP分析](../serp-analysis/) · [内容差距分析](../content-gap-analysis/)

**构建** · [SEO内容编写器](../../build/seo-content-writer/) · [地理内容优化器](../../build/geo-content-optimizer/) · [元标签优化器](../../build/meta-tags-optimizer/) · [结构化标记生成器](../../build/schema-markup-generator/)

**优化** · [页面SEO审计器](../../optimize/on-page-seo-auditor/) · [技术SEO检查器](../../optimize/technical-seo-checker/) · [内部链接优化器](../../optimize/internal-linking-optimizer/) · [内容更新器](../../optimize/content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告器](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)

**跨领域** · [内容质量审计器](../../cross-cutting/content-quality-auditor/) · [域名权威度审计器](../../cross-cutting/domain-authority-auditor/) · [实体优化器](../../cross-cutting/entity-optimizer/) · [内存管理](../../cross-cutting/memory-management/)

</details>

该技能提供全面的竞争对手SEO和GEO策略分析，帮助你了解市场中的有效策略，并发现超越竞争对手的机会。

## 适用场景

- 进入新市场或细分领域
- 根据竞争对手的成功情况制定内容策略
- 了解竞争对手为何排名更高
- 寻找反向链接和合作机会
- 发现竞争对手遗漏的内容空白
- 分析竞争对手的人工智能引用策略
- 对比自身的SEO表现

## 功能概述

1. **关键词分析**：识别竞争对手排名靠前的关键词
2. **内容审计**：分析竞争对手的内容策略和格式
3. **反向链接分析**：审查竞争对手的链接构建方式
4. **技术评估**：评估竞争对手网站的健康状况
5. **地理分析**：了解竞争对手在人工智能搜索结果中的表现
6. **差距识别**：发现竞争对手忽略的机会
7. **策略提取**：从竞争对手的成功中提取可操作的洞察

## 使用方法

### 基础竞争对手分析

```
Analyze SEO strategy for [competitor URL]
```

```
Compare my site [URL] against [competitor 1], [competitor 2], [competitor 3]
```

### 专项分析

```
What content is driving the most traffic for [competitor]?
```

### 地理聚焦分析

```
How is [competitor] getting cited in AI responses? What can I learn?
```

## 数据来源

> 请参阅 [CONNECTORS.md](../../CONNECTORS.md) 以获取工具类别的相关信息。

**通过连接 **SEO工具**、**分析工具** 和 **AI监控工具**：
- 自动获取竞争对手的关键词排名、反向链接信息、高排名内容以及域名权威度数据。
- 将这些数据与你的网站指标（来自 **分析工具** 和 **搜索控制台**）进行对比。
- 使用 **AI监控工具** 分析你和竞争对手的人工智能引用模式。

**仅使用手动数据时**：
- 请用户提供以下信息：
  - 2-5个需要分析的竞争对手网址
  - 你自己的网站网址及当前指标（流量、排名等）
  - 行业或细分领域的背景信息
  - 需要关注的具体方面（关键词、内容、反向链接等）
  - 竞争对手的优缺点

根据提供的数据开始全面分析。在输出结果中明确标注哪些数据来自自动化收集，哪些来自用户提供。

## 使用说明

当用户请求竞争对手分析时：

1. **确定竞争对手**：
   如果未指定，协助确定竞争对手：
   
   ```markdown
   ### Competitor Identification Framework
   
   **Direct Competitors** (same product/service)
   - Search "[your main keyword]" and note top 5 organic results
   - Check who's advertising for your keywords
   - Ask: Who do customers compare you to?
   
   **Indirect Competitors** (different solution, same problem)
   - Search problem-focused keywords
   - Look at alternative solutions
   
   **Content Competitors** (compete for same keywords)
   - May not sell same product
   - Rank for your target keywords
   - Include media sites, blogs, aggregators
   ```

2. **收集竞争对手数据**：
   为每个竞争对手收集以下数据：
   
   ```markdown
   ## Competitor Profile: [Name]
   
   **Basic Info**
   - URL: [website]
   - Domain Age: [years]
   - Estimated Traffic: [monthly visits]
   - Domain Authority/Rating: [score]
   
   **Business Model**
   - Type: [SaaS/E-commerce/Content/etc.]
   - Target Audience: [description]
   - Key Offerings: [products/services]
   ```

3. **分析关键词排名**：
   ```markdown
   ### Keyword Analysis: [Competitor]
   
   **Total Keywords Ranking**: [X]
   **Keywords in Top 10**: [X]
   **Keywords in Top 3**: [X]
   
   #### Top Performing Keywords
   
   | Keyword | Position | Volume | Traffic Est. | Page |
   |---------|----------|--------|--------------|------|
   | [kw 1] | [pos] | [vol] | [traffic] | [url] |
   | [kw 2] | [pos] | [vol] | [traffic] | [url] |
   
   #### Keyword Distribution by Intent
   
   - Informational: [X]% ([keywords])
   - Commercial: [X]% ([keywords])  
   - Transactional: [X]% ([keywords])
   - Navigational: [X]% ([keywords])
   
   #### Keyword Gaps (They rank, you don't)
   
   | Keyword | Their Position | Volume | Opportunity |
   |---------|----------------|--------|-------------|
   | [kw 1] | [pos] | [vol] | [analysis] |
   ```

4. **审计内容策略**：
   ```markdown
   ### Content Analysis: [Competitor]
   
   **Content Volume**
   - Total Pages: [X]
   - Blog Posts: [X]
   - Landing Pages: [X]
   - Resource Pages: [X]
   
   **Content Performance**
   
   #### Top Performing Content
   
   | Title | URL | Est. Traffic | Keywords | Backlinks |
   |-------|-----|--------------|----------|-----------|
   | [title 1] | [url] | [traffic] | [X] | [X] |
   
   **Content Patterns**
   
   - Average word count: [X] words
   - Publishing frequency: [X] posts/month
   - Content formats used:
     - Blog posts: [X]%
     - Guides/tutorials: [X]%
     - Case studies: [X]%
     - Tools/calculators: [X]%
     - Videos: [X]%
   
   **Content Themes**
   
   | Theme | # Articles | Combined Traffic |
   |-------|------------|------------------|
   | [theme 1] | [X] | [traffic] |
   | [theme 2] | [X] | [traffic] |
   
   **What Makes Their Content Successful**
   
   1. [Success factor 1 with example]
   2. [Success factor 2 with example]
   3. [Success factor 3 with example]
   ```

5. **分析反向链接情况**：
   ```markdown
   ### Backlink Analysis: [Competitor]
   
   **Overview**
   - Total Backlinks: [X]
   - Referring Domains: [X]
   - Domain Rating: [X]
   
   **Link Quality Distribution**
   - High Authority (DR 70+): [X]%
   - Medium Authority (DR 30-69): [X]%
   - Low Authority (DR <30): [X]%
   
   **Top Linking Domains**
   
   | Domain | DR | Link Type | Target Page |
   |--------|-----|-----------|-------------|
   | [domain 1] | [DR] | [type] | [page] |
   
   **Link Acquisition Patterns**
   
   - Guest posts: [X]%
   - Editorial/organic: [X]%
   - Resource pages: [X]%
   - Directories: [X]%
   - Other: [X]%
   
   **Linkable Assets (Content attracting links)**
   
   | Asset | Type | Backlinks | Why It Works |
   |-------|------|-----------|--------------|
   | [asset 1] | [type] | [X] | [reason] |
   ```

6. **进行技术SEO评估**：
   ```markdown
   ### Technical Analysis: [Competitor]
   
   **Site Performance**
   - Core Web Vitals: [Pass/Fail]
   - LCP: [X]s
   - FID: [X]ms
   - CLS: [X]
   - Mobile-friendly: [Yes/No]
   
   **Site Structure**
   - Site architecture depth: [X] levels
   - Internal linking quality: [Rating]
   - URL structure: [Clean/Messy]
   - Sitemap present: [Yes/No]
   
   **Technical Strengths**
   1. [Strength 1]
   2. [Strength 2]
   
   **Technical Weaknesses**
   1. [Weakness 1]
   2. [Weakness 2]
   ```

7. **地理/AI引用分析**：
   ```markdown
   ### GEO Analysis: [Competitor]
   
   **AI Visibility Assessment**
   
   Test competitor content in AI systems for relevant queries:
   
   | Query | AI Mentions Competitor? | What's Cited | Why |
   |-------|------------------------|--------------|-----|
   | [query 1] | Yes/No | [content] | [reason] |
   | [query 2] | Yes/No | [content] | [reason] |
   
   **GEO Strategies Observed**
   
   1. **Clear Definitions**
      - Example: [quote from their content]
      - Effectiveness: [rating]
   
   2. **Quotable Statistics**
      - Example: [quote from their content]
      - Effectiveness: [rating]
   
   3. **Q&A Format Content**
      - Examples found: [X] pages
      - Topics covered: [list]
   
   4. **Authority Signals**
      - Expert authorship: [Yes/No]
      - Citations to sources: [Yes/No]
      - Original research: [Yes/No]
   
   **GEO Opportunities They're Missing**
   
   | Topic | Why Missing | Your Opportunity |
   |-------|-------------|------------------|
   | [topic 1] | [reason] | [action] |
   ```

8. **整合竞争情报**：
   ```markdown
   # Competitive Analysis Report
   
   **Analysis Date**: [Date]
   **Competitors Analyzed**: [List]
   **Your Site**: [URL]
   
   ## Executive Summary
   
   [2-3 paragraph overview of key findings and recommendations]
   
   ## Competitive Landscape
   
   | Metric | You | Competitor 1 | Competitor 2 | Competitor 3 |
   |--------|-----|--------------|--------------|--------------|
   | Domain Authority | [X] | [X] | [X] | [X] |
   | Organic Traffic | [X] | [X] | [X] | [X] |
   | Keywords Top 10 | [X] | [X] | [X] | [X] |
   | Backlinks | [X] | [X] | [X] | [X] |
   | Content Pages | [X] | [X] | [X] | [X] |

   **Domain Authority Comparison (Recommended)**

   When domain-level comparison is needed, run the [domain-authority-auditor](../../cross-cutting/domain-authority-auditor/) for each competitor to get CITE scores:

   | Domain | CITE Score | C (Citation) | I (Identity) | T (Trust) | E (Eminence) | Veto |
   |--------|-----------|-------------|-------------|----------|-------------|------|
   | Your domain | [score] | [score] | [score] | [score] | [score] | [pass/fail] |
   | Competitor 1 | [score] | [score] | [score] | [score] | [score] | [pass/fail] |
   | Competitor 2 | [score] | [score] | [score] | [score] | [score] | [pass/fail] |

   This reveals domain authority gaps that inform link building and brand strategy beyond keyword-level competition.

   ## Competitor Strengths to Learn From
   
   ### [Competitor 1]
   - **Strength**: [description]
   - **Why It Works**: [analysis]
   - **How to Apply**: [action item]
   
   [Repeat for each competitor]
   
   ## Competitor Weaknesses to Exploit
   
   ### Gap 1: [Description]
   - Who's weak: [competitors]
   - Opportunity size: [estimate]
   - Recommended action: [specific steps]
   
   [Repeat for each gap]
   
   ## Keyword Opportunities
   
   ### Keywords to Target (Competitor overlap)
   | Keyword | Volume | Avg Position | Best Strategy |
   |---------|--------|--------------|---------------|
   | [kw] | [vol] | [pos] | [strategy] |
   
   ### Untapped Keywords (No competitor coverage)
   | Keyword | Volume | Difficulty | Opportunity |
   |---------|--------|------------|-------------|
   | [kw] | [vol] | [diff] | [description] |
   
   ## Content Strategy Recommendations
   
   Based on competitor analysis:
   
   1. **Create**: [Content type] about [topic] because [reason]
   2. **Improve**: [Existing content] to match/exceed [competitor content]
   3. **Promote**: [Content] to sites like [competitor's link sources]
   
   ## Action Plan
   
   ### Immediate (This Week)
   1. [Action item]
   2. [Action item]
   
   ### Short-term (This Month)
   1. [Action item]
   2. [Action item]
   
   ### Long-term (This Quarter)
   1. [Action item]
   2. [Action item]
   ```

## 验证要点

### 输入验证
- 确保竞争对手网址与你的业务领域相关
- 明确分析范围（全面分析或聚焦特定领域）
- 提供可供对比的你的网站指标
- 确定至少2-3个竞争对手以发现有意义的趋势

### 输出验证
- 每条建议都应基于具体数据
- 竞争对手的优势需有可量化的证据支持（如指标、排名等）
- 机会应基于可识别的差距，而非主观假设
- 行动计划应具体且可执行
- 明确每项数据的来源（来自 **SEO工具**、**分析工具**、**AI监控工具** 或用户提供的数据）

## 示例

**用户请求**：“分析HubSpot为何在营销相关关键词上排名如此高”

**输出结果**：
```markdown
# Competitive Analysis: HubSpot

## SEO Strategy Overview

HubSpot dominates marketing keywords through a combination of:
1. **Massive content moat** - 10,000+ blog posts
2. **Free tools as linkbait** - Website grader, email signature generator
3. **Educational brand** - Academy, certifications, courses
4. **Topic cluster model** - Pioneered the pillar/cluster approach

## What Makes Them Successful

### Content Strategy

**Publishing Volume**: 50-100 posts/month
**Average Word Count**: 2,500+ words
**Content Types**:
- In-depth guides (35%)
- How-to tutorials (25%)
- Templates & examples (20%)
- Data/research (10%)
- Tools & calculators (10%)

**Top Performing Content Pattern**:
1. Ultimate guides on broad topics
2. Free templates with email gate
3. Statistics roundup posts
4. Definition posts ("What is [term]")

### GEO Success Factors

HubSpot appears in AI responses frequently because:

1. **Clear definitions** at the start of every post
   > "Inbound marketing is a business methodology that attracts customers by creating valuable content and experiences tailored to them."

2. **Quotable statistics**
   > "Companies that blog get 55% more website visitors"

3. **Comprehensive coverage** - AI trusts their authority

### Linkable Assets

| Asset | Backlinks | Why It Works |
|-------|-----------|--------------|
| Website Grader | 45,000+ | Free, instant value |
| Marketing Statistics | 12,000+ | Quotable reference |
| Blog Ideas Generator | 8,500+ | Solves real problem |

## Weaknesses to Exploit

1. **Content becoming dated** - Many posts 3+ years old
2. **Generic advice** - Lacks industry-specific depth
3. **Enterprise focus** - Underserves solopreneurs
4. **Slow innovation** - Same formats for years

## Your Opportunities

1. Create more specific, niche content they can't cover
2. Target long-tail keywords they ignore
3. Build interactive tools in emerging areas
4. Add original research they don't have
5. Focus on GEO-optimized definitions in your niche
```

## 高级分析类型

### 内容差距分析

```
Show me content [competitor] has that I don't, sorted by traffic potential
```

### 链接交叉分析

```
Find sites linking to [competitor 1] AND [competitor 2] but not me
```

### SERP特征分析

```
What SERP features do competitors win? (Featured snippets, PAA, etc.)
```

### 历史趋势跟踪

```
How has [competitor]'s SEO strategy evolved over the past year?
```

## 成功技巧

- **分析3-5个竞争对手** 以获得全面视角
- **包括间接竞争对手**——他们通常具有创新的方法
- **关注内容质量与用户体验** 而不仅仅是排名
- **研究他们的失败案例** 以避免重复他们的错误
- **定期监控**——竞争对手的策略会不断演变
- **关注可操作的洞察**——哪些措施你可以实际实施

## 消息传递对比框架

### 消息传递矩阵

从关键维度对比竞争对手的信息传递方式：

| 维度 | 你的网站 | 竞争对手A | 竞争对手B | 竞争对手C |
|-----------|-----------|-------------|-------------|-------------|
| 核心价值主张 | | | | |
| 主要呼吁行动 | | | | |
- 标题 | | | | |
- 语气/风格 | | | | |
- 关键差异化点 | | | | |
- 社交证明方式 | | | | |
- 类别定位 | | | | |
- 目标受众信号 | | | | |

### 叙事分析框架

分析每个竞争对手的故事框架：

| 元素 | 描述 | 如何识别 |
|---------|------------|----------------|
| **对立面** | 他们所针对的问题或“敌人” | 首页的“为什么选择我们”页面——他们抨击的现状是什么？ |
| **主角** | 故事中的“主角”是谁 | 客户故事、案例研究——主角是客户还是产品？ |
| **转变** | 他们承诺带来的改变 | 结果页面、用户评价——可衡量的变化是什么？ |
| **风险** | 不采取行动会带来什么后果 | 风险提示、紧迫感——是否使用了“错失机会”（FOMO）的表述？ |

### 价值主张对比

提取每个竞争对手的价值主张：

```
**[Competitor Name]**
- Promise: what they promise the customer will achieve
- Evidence: how they prove it (data, testimonials, demos)
- Mechanism: how their product delivers (the "how it works")
- Uniqueness: what they claim only they can do
```

## 定位策略框架

### 定位图（2x2矩阵）

在关键维度上对比竞争对手：

| 维度对 | 最适合的策略 |
|-----------|---------|
| 价格 vs. 功能 | 理解市场层级 |
- 易用性 vs. 功能强度 | 评估用户体验的权衡 |
- 专注中小企业 vs. 企业级 | 识别市场细分 |
- 单点解决方案 vs. 平台 | 寻找定位空间 |
- 市场成熟度 vs. 创新性 | 判断进入市场的时机 |

### 定位策略反向工程

重构每个竞争对手的隐含定位：

> 对于 **[目标受众]**，**[产品]** 在 **[类别]** 中具有 **[关键优势]**，因为 **[相信的理由]**。

## 竞争对手分析卡片模板

### 快速参考卡片结构

| 部分 | 内容 |
|---------|---------|
| **概述** | 一句话描述 + 目标客户 + 定价模式 |
| **他们的宣传内容** | 标语 + 3个主要差异化点 |
| **优势** | 他们真正擅长的方面（如实说明） |
| **劣势** | 评论中的常见问题、技术限制 |
| **你的差异化优势** | 3-5个具体的差异化点及证据 |
| **应对质疑** | “如果他们提到X，你如何回应” |
| **需要注意的问题** | 可能凸显你优势的问题 |
| **胜负关键点** | 与他们竞争时常见的胜负原因 |

## 参考资料

- [竞争对手分析卡片模板](./references/battlecard-template.md) — 适用于销售和营销团队的快速参考卡片
- [定位框架](./references/positioning-frameworks.md) — 定位图、策略矩阵和差异化分析工具

## 相关技能

- [域名权威度审计器](../../cross-cutting/domain-authority-auditor/) — 比较竞争对手的域名权威度分数
- [关键词研究](../keyword-research/) — 研究竞争对手的关键词排名
- [内容差距分析](../content-gap-analysis/) — 发现内容创作的机会
- [反向链接分析器](../../monitor/backlink-analyzer/) — 深入分析反向链接
- [SERP分析](../serp-analysis/) — 了解搜索结果的构成
- [内存管理](../../cross-cutting/memory-management/) — 将竞争对手数据存储在项目内存中
- [实体优化器](../../cross-cutting/entity-optimizer/) — 比较竞争对手的实体存在情况