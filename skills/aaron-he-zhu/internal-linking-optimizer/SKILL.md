---
name: internal-linking-optimizer
description: '**使用场景：**  
当用户提出以下需求时，可使用该工具：  
- “修复内部链接”  
- “优化网站架构”  
- “调整链接结构”  
- “分配页面权重（page authority）”  
- “制定内部链接策略”  
- 处理“孤立页面”（即没有其他页面链接到的页面）  
- “网站架构混乱”  
- “页面没有任何外部链接”  

**功能说明：**  
该工具用于分析和优化网站的内部链接结构，从而提升网站架构的质量、分配页面权重，并帮助搜索引擎更好地理解页面之间的内容关系。同时，它还能帮助制定有效的内部链接策略。  
- **针对更全面的页面审核，可参考** `on-page-seo-auditor` 工具。  
- **针对外部链接分析，可参考** `backlink-analyzer` 工具。'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "low"
  tags:
    - seo
    - internal linking
    - site architecture
    - link structure
    - page authority
    - link equity
    - content silos
    - navigation optimization
  triggers:
    - "fix internal links"
    - "improve site architecture"
    - "link structure"
    - "distribute page authority"
    - "internal linking strategy"
    - "site navigation"
    - "link equity"
    - "orphan pages"
    - "site architecture is messy"
    - "pages have no links pointing to them"
---

# 内部链接优化器

> **[SEO与地理定位技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与地理定位相关技能 · 全部技能的安装命令：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容编写器](../../build/seo-content-writer/) · [地理内容优化器](../../build/geo-content-optimizer/) · [元标签优化器](../../build/meta-tags-optimizer/) · [结构标记生成器](../../build/schema-markup-generator/)

**优化** · [页面SEO审计器](../on-page-seo-auditor/) · [技术SEO检查器](../technical-seo-checker/) · **内部链接优化器** · [内容更新工具](../content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告器](../../monitor/performance-reporter/) · [警报管理系统](../../monitor/alert-manager/)

**跨领域工具** · [内容质量审计器](../../cross-cutting/content-quality-auditor/) · [域名权威度审计器](../../cross-cutting/domain-authority-auditor/) · [实体优化器](../../cross-cutting/entity-optimizer/) · [内存管理工具](../../cross-cutting/memory-management/)

</details>

该工具会分析您网站的内部链接结构，并提供通过战略性内部链接来提升SEO的建议。它有助于分配网站权威性、增强主题相关性以及提高网站的爬取效率。

## 适用场景

- 优化网站架构以提升SEO效果
- 将权威性分配给重要页面
- 修复没有内部链接的“孤儿页面”
- 制定主题群组内部的链接策略
- 优化锚文本以提高SEO效果
- 恢复排名下降的页面
- 为新内容规划内部链接

## 功能介绍

1. **链接结构分析**：绘制当前的内部链接模式
2. **权威性流动分析**：展示PageRank在网站中的流动情况
3. **孤儿页面检测**：找出没有内部链接的页面
4. **锚文本优化**：提高锚文本的多样性
5. **主题群组链接策略**：创建主题群组之间的链接结构
6. **链接机会识别**：确定需要添加链接的位置
7. **导航优化**：优化整个网站的链接元素

## 使用方法

### 分析当前链接结构

```
Analyze internal linking structure for [domain/sitemap]
```

### 制定链接策略

```
Create internal linking plan for topic cluster about [topic]
```

### 修复问题

```
Find orphan pages on [domain]
```

### 数据来源

> 请参阅[CONNECTORS.md](../../CONNECTORS.md)以获取工具类别的相关信息。

**当与[网络爬虫 + 分析工具]结合使用时：**
Claude可以通过网络爬虫自动完成整个网站的爬取，绘制完整的链接图谱；从分析工具中获取页面性能数据，识别高价值页面，并分析网站内的链接流动情况。这有助于制定数据驱动的内部链接策略。

**仅使用手动数据时：**
用户需要提供：
1. 网站地图URL或重要页面列表
2. 需要更多内部链接的关键页面URL
3. 内容类别或主题群组
4. 现有的链接结构文档

根据提供的数据进行分析。在输出结果中明确标注哪些发现来自自动化爬取，哪些来自人工审核。

## 使用说明

当用户请求内部链接优化时：
1. **分析当前的内部链接结构**
   ```markdown
   ## Internal Link Structure Analysis
   
   ### Overview
   
   **Domain**: [domain]
   **Total Pages Analyzed**: [X]
   **Total Internal Links**: [X]
   **Average Links per Page**: [X]
   
   ### Link Distribution
   
   | Links per Page | Page Count | Percentage |
   |----------------|------------|------------|
   | 0 (Orphan) | [X] | [X]% |
   | 1-5 | [X] | [X]% |
   | 6-10 | [X] | [X]% |
   | 11-20 | [X] | [X]% |
   | 20+ | [X] | [X]% |
   
   ### Top Linked Pages
   
   | Page | Internal Links | Authority | Notes |
   |------|----------------|-----------|-------|
   | [URL 1] | [X] | High | [notes] |
   | [URL 2] | [X] | High | [notes] |
   | [URL 3] | [X] | Medium | [notes] |
   
   ### Under-Linked Important Pages
   
   | Page | Current Links | Traffic | Recommended Links |
   |------|---------------|---------|-------------------|
   | [URL 1] | [X] | [X]/mo | [X]+ |
   | [URL 2] | [X] | [X]/mo | [X]+ |
   
   **Structure Score**: [X]/10
   ```

2. **识别孤儿页面**
   ```markdown
   ## Orphan Page Analysis
   
   ### Definition
   Orphan pages have no internal links pointing to them, making them 
   hard for users and search engines to discover.
   
   ### Orphan Pages Found: [X]
   
   | Page | Traffic | Priority | Recommended Action |
   |------|---------|----------|-------------------|
   | [URL 1] | [X]/mo | High | Link from [pages] |
   | [URL 2] | [X]/mo | Medium | Add to navigation |
   | [URL 3] | 0 | Low | Consider deleting/redirecting |
   
   ### Fix Strategy
   
   **High Priority Orphans** (have traffic/rankings):
   1. [URL] - Add links from: [relevant pages]
   2. [URL] - Add links from: [relevant pages]
   
   **Medium Priority Orphans** (potentially valuable):
   1. [URL] - Add to category/tag page
   2. [URL] - Link from related content
   
   **Low Priority Orphans** (consider removing):
   1. [URL] - Redirect to [better page]
   2. [URL] - Delete or noindex
   ```

3. **分析锚文本分布**
   > **CORE-EEAT标准**：内部链接的质量与CORE-EEAT基准中的R08（内部链接图谱）相关——使用描述性强的锚文本，确保链接能够体现主题权威性。详情请参阅[内容质量审计器](../../cross-cutting/content-quality-auditor/)。

4. **制定主题群组链接策略**
   ```markdown
   ## Topic Cluster Internal Linking
   
   ### Cluster: [Main Topic]
   
   **Pillar Page**: [URL]
   **Cluster Articles**: [X]
   
   ### Current Link Map
   
   ```
   [核心页面]
      ├── [群组文章1] ←→ [已链接？]
      ├── [群组文章2] ←→ [已链接？]
      ├── [群组文章3] ←→ [已链接？]
      └── [群组文章4] ←→ [已链接？]
   ```
   
   ### Recommended Link Structure
   
   ```
   [核心页面]
      ├── 链接到所有群组文章 ✅
      │
      ├── [群组文章1]
      │   ├── 链接到核心页面 ✅
      │   └── 链接到相关群组文章
      │
      ├── [群组文章2]
      │   ├── 链接到核心页面 ✅
      │   └── 链接到相关群组文章
      │
      └── [等等]
   ```
   
   ### Links to Add
   
   | From Page | To Page | Anchor Text | Location |
   |-----------|---------|-------------|----------|
   | [URL 1] | [URL 2] | "[anchor]" | [paragraph/section] |
   | [URL 2] | [URL 3] | "[anchor]" | [paragraph/section] |
   | [Pillar] | [Cluster 1] | "[anchor]" | [section] |
   ```

5. **寻找合适的链接机会**
   ```markdown
   ## Contextual Link Opportunities
   
   ### Link Opportunity Analysis
   
   For each page, find relevant pages to link to based on:
   - Topic relevance
   - Keyword overlap
   - User journey logic
   - Authority distribution needs
   
   ### Opportunities Found
   
   **Page: [URL 1]**
   **Topic**: [topic]
   **Current internal links**: [X]
   
   | Opportunity | Target Page | Anchor Text | Why Link |
   |-------------|-------------|-------------|----------|
   | Paragraph 2 mentions "[topic]" | [URL] | "[topic phrase]" | Topic match |
   | Section on "[subject]" | [URL] | "[anchor]" | Related guide |
   | CTA at end | [URL] | "[anchor]" | User journey |
   
   **Page: [URL 2]**
   [Continue for each page...]
   
   ### Priority Link Additions
   
   **High Impact Links** (add these first):
   
   1. **From**: [Source URL]
      **To**: [Target URL]
      **Anchor**: "[anchor text]"
      **Why**: [reason - e.g., "Target page needs authority boost"]
      **Where to add**: [specific location in content]
   
   2. **From**: [Source URL]
      **To**: [Target URL]
      [etc.]
   ```

6. **优化导航和页脚链接**
   ```markdown
   ## Site-Wide Link Optimization
   
   ### Current Navigation Analysis
   
   **Main Navigation**:
   - Links present: [list]
   - Missing important pages: [list]
   - Too many links: [Yes/No]
   
   **Footer Navigation**:
   - Links present: [list]
   - SEO value: [assessment]
   
   ### Navigation Recommendations
   
   | Element | Current | Recommended | Reason |
   |---------|---------|-------------|--------|
   | Main nav | [X] links | [Y] links | [reason] |
   | Footer | [X] links | [Y] links | [reason] |
   | Sidebar | [status] | [recommendation] | [reason] |
   | Breadcrumbs | [status] | [recommendation] | [reason] |
   
   ### Pages to Add to Navigation
   
   1. [Page] - Add to [location] because [reason]
   2. [Page] - Add to [location] because [reason]
   
   ### Pages to Remove from Navigation
   
   1. [Page] - Move to [footer/remove] because [reason]
   ```

7. **生成链接实施计划**
   ```markdown
   # Internal Linking Optimization Plan
   
   **Site**: [domain]
   **Analysis Date**: [date]
   
   ## Executive Summary
   
   - Total link opportunities found: [X]
   - Orphan pages to fix: [X]
   - Estimated traffic impact: [+X%]
   - Priority actions: [X]
   
   ## Current State
   
   | Metric | Current | Target | Gap |
   |--------|---------|--------|-----|
   | Avg links per page | [X] | [X] | [X] |
   | Orphan pages | [X] | 0 | [X] |
   | Over-optimized anchors | [X]% | <10% | [X]% |
   | Topic cluster coverage | [X]% | 100% | [X]% |
   
   ## Priority Actions
   
   ### Phase 1: Critical Fixes (Week 1)
   
   **Fix Orphan Pages**:
   - [ ] [URL] - Add links from [X] pages
   - [ ] [URL] - Add links from [X] pages
   
   **High-Value Link Additions**:
   - [ ] Link [Page A] to [Page B] with "[anchor]"
   - [ ] Link [Page A] to [Page C] with "[anchor]"
   
   ### Phase 2: Topic Clusters (Week 2-3)
   
   **Cluster 1: [Topic]**
   - [ ] Ensure pillar links to all [X] cluster articles
   - [ ] Add [X] cross-links between cluster articles
   
   **Cluster 2: [Topic]**
   - [ ] [Tasks]
   
   ### Phase 3: Optimization (Week 4+)
   
   **Anchor Text Diversity**:
   - [ ] Vary anchors for [Page] - currently [X]% exact match
   - [ ] [Additional tasks]
   
   **Navigation Updates**:
   - [ ] Add [Page] to main navigation
   - [ ] Update footer links
   
   ## Implementation Guide
   
   ### Adding Internal Links
   
   Best practices:
   1. Add links contextually within content
   2. Use descriptive anchor text (not "click here")
   3. Link to relevant, helpful pages
   4. Aim for 3-10 internal links per 1,000 words
   5. Vary anchor text for the same target
   
   ### Anchor Text Guidelines
   
   | Type | Example | Usage |
   |------|---------|-------|
   | Exact match | "keyword research" | 10-20% |
   | Partial match | "tips for keyword research" | 30-40% |
   | Branded | "Brand's guide to..." | 10-20% |
   | Natural | "this article", "learn more" | 20-30% |
   
   ## Tracking Success

   Monitor these metrics weekly:
   - [ ] Rankings for target keywords
   - [ ] Traffic to previously orphan pages
   - [ ] Crawl stats in ~~search console
   - [ ] Internal link distribution changes
   ```

## 验证要点

### 输入验证
- 提供网站结构或站点地图（URL或文件）
- 明确目标页面或主题群组
- 如果针对特定页面进行优化，请提供该页面的URL或内容

### 输出验证
- 每条建议都应引用具体的数据来源
- 所有的链接建议都应包含源页面、目标页面和推荐的锚文本
- 孤儿页面列表应包含URL及建议的操作步骤
- 明确每个数据点的来源（网络爬虫数据、分析工具数据或用户提供的数据）

## 示例

**用户**：“为我的关于‘电子邮件营销最佳实践’的博客文章寻找内部链接机会”

**输出结果：**
```markdown
## Internal Linking Opportunities

**Page**: /blog/email-marketing-best-practices/
**Current Internal Links**: 2

### Recommended Links to Add

| Section | Text to Link | Target Page | Anchor |
|---------|--------------|-------------|--------|
| Para 2 | "building your email list" | /blog/grow-email-list/ | "building your email list" |
| Para 5 | "subject lines" | /blog/email-subject-lines/ | "write compelling subject lines" |
| Section on segmentation | "audience segments" | /blog/email-segmentation-guide/ | "segment your audience" |
| CTA section | "marketing automation" | /services/email-automation/ | "email automation services" |
| Conclusion | "email marketing tools" | /blog/best-email-tools/ | "top email marketing tools" |

### Pages That Should Link TO This Article

| Source Page | Location | Anchor Text |
|-------------|----------|-------------|
| /blog/digital-marketing-guide/ | Email section | "email marketing best practices" |
| /services/marketing-services/ | Related content | "email marketing strategies" |
| /blog/lead-generation-tips/ | Email mention | "email marketing techniques" |

### Priority Actions

1. Add 5 outbound internal links (listed above)
2. Request 3 inbound links from related pages
3. Add to "Marketing" category page
```

## 成功技巧

1. **质量优先于数量**——添加相关链接，而非随机链接
2. **以用户为中心**——链接应有助于用户导航
3. **多样化锚文本**——避免过度优化
4. **链接到重要页面**——策略性地分配权威性
5. **定期审计**——随着内容更新，需要持续维护内部链接

## 链接架构模式

### 常见架构模型

| 模型 | 描述 | 适用场景 | 限制 |
|-------|------------|---------|------------|
| **中心辐射型** | 中心页面链接到各个主题群组 | 适用于需要强化主题权威性的网站 | 可能导致某些主题群组被孤立 |
| **孤立结构** | 严格的分类层次结构，垂直链接方式 | 适用于大型电子商务网站或具有严格分类体系的网站 | 限制跨主题内容的发现 |
| **扁平结构** | 所有页面从首页点击2-3次即可到达 | 适用于小型网站（少于100页） | 不适合大型网站 |
| **金字塔结构** | 主页 → 分类 → 子分类 → 页面 | 适用于新闻网站或大型博客 | 深层页面可能获得较少的权威性 |
| **网状/矩阵结构** | 相关内容之间自由链接 | 适用于知识库或维基网站 | 无规则时可能导致链接结构混乱 |

### 中心辐射型架构的实现方法

```
Homepage
  └── Topic Hub A (pillar page)
  │     ├── Cluster Article A1 ←→ A2
  │     ├── Cluster Article A2 ←→ A3
  │     └── Cluster Article A3 ←→ A1
  └── Topic Hub B (pillar page)
        ├── Cluster Article B1 ←→ B2
        └── Cluster Article B2 ←→ B1

Cross-links: A2 → B1 (related subtopics)
```

## 锚文本多样性框架

### 锚文本类型

| 类型 | 例子 | 目标分布 | 风险等级 |
|------|---------|-------------------|------------|
| 完全匹配 | “关键词研究工具” | 10-15% | 如果比例过高，可能导致过度优化 |
| 部分匹配 | “最佳关键词研究工具” | 20-30% | 安全且自然 |
| 品牌名称 | “Ahrefs关键词探索器” | 15-25% | 始终安全 |
| 通用文本 | “点击这里”、“了解更多”、“阅读此内容” | 5-10% | SEO价值较低 |
| 描述性文本 | “这份全面的指南涵盖了...” | 20-30% | 最自然，推荐使用 |
| 裸露的URL | “example.com/page” | 5-10% | 适用于引用链接 |

### 锚文本的最佳实践
- 对同一目标页面使用多样化的锚文本
- 使用能够向用户和搜索引擎传达信息的描述性文本
- 不要对不同目标页面使用相同的锚文本
- 注意避免过度优化商业关键词

## 链接权值流动模型

### 链接权值分配

| 页面位置 | 获得的权值 | 提高权值的措施 |
|--------------|----------------|-------------------|
| 主页 | 最高（所有外部链接都指向这里） | 通过显眼的链接将权值分配给关键页面 |
| 分类页面 | 权值较高（来自首页和子页面的链接） | 除了导航链接外，还应从博客文章中添加链接 |
| 优质内容 | 权值中等偏高（如果内部链接丰富） | 增加来自其他高质量页面的链接 |
| 深层页面 | 权值较低（内部链接较少） | 从相关页面添加上下文相关的链接 |
| 孤儿页面 | 权值为零（没有内部链接！） | 关键：至少添加3个内部链接 |

### 内部链接审计检查清单

| 检查项 | 工具/方法 | 合格标准 |
|-------|------------|--------------|
| 孤儿页面 | 爬取报告 | 不存在孤儿页面 |
| 点击深度 | 爬取报告 | 所有关键页面都在首页的3次点击范围内 |
| 错误的内部链接 | 爬取报告 | 不存在404错误的内部链接 |
| 重定向链 | 爬取报告 | 重定向链不超过2层 |
| 锚文本多样性 | 手动审计 | 链接文本中完全匹配的内容不超过30% |
| 双向链接 | 手动审计 | 相关页面之间相互链接 |
| 导航一致性 | 手动审计 | 关键页面在主导航中可见 |
| 每1000字内的上下文链接数量 | 手动审计 | 每1000字应有3-5个上下文相关的链接 |

## 参考资料

- [链接架构模式](./references/link-architecture-patterns.md) — 架构模型、实施指南和链接权值优化策略

## 相关技能

- [内容差距分析](../../research/content-gap-analysis/) — 寻找需要链接的内容
- [SEO内容编写器](../../build/seo-content-writer/) — 创建适合链接的内容
- [页面SEO审计器](../on-page-seo-auditor/) — 审查整体的页面SEO情况
- [技术SEO检查器](../technical-seo-checker/) — 检查网站的爬取可行性
- [内容质量审计器](../../cross-cutting/content-quality-auditor/) — 全面的CORE-EEAT审计 |
- [结构标记生成器](../../build/schema-markup-generator/) — 生成面包屑导航和结构标记