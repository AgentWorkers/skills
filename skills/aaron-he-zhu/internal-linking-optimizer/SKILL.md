---
name: internal-linking-optimizer
version: "3.0.0"
description: '当用户请求“修复内部链接”、“优化网站架构”、“调整链接结构”、“分配页面权重”、“制定内部链接策略”、“处理孤立页面”或“网站架构混乱”等问题时，应使用此技能。该技能通过分析和优化内部链接结构来提升网站架构的质量，合理分配页面权重，并帮助搜索引擎更好地理解页面之间的内容关系。同时，还会制定相应的内部链接策略。如需进行更全面的页面审核，请参考“on-page-seo-auditor”；如需分析外部链接，请参考“backlink-analyzer”。'
license: Apache-2.0
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    primaryEnv: AHREFS_API_KEY
  author: aaron-he-zhu
  version: "3.0.0"
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
    - internal-links
    - site-architecture
    - link-equity
    - orphan-pages
    - topical-authority
    - hub-and-spoke
    - pillar-cluster
    - anchor-text
    - crawl-depth
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

**构建** · [SEO内容编写器](../../build/seo-content-writer/) · [地理内容优化器](../../build/geo-content-optimizer/) · [元标签优化器](../../build/meta-tags-optimizer/) · [结构化标记生成器](../../build/schema-markup-generator/)

**优化** · [页面SEO审核器](../on-page-seo-auditor/) · [技术SEO检查器](../technical-seo-checker/) · **内部链接优化器** · [内容更新工具](../content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告工具](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)

**跨领域工具** · [内容质量审核器](../../cross-cutting/content-quality-auditor/) · [域名权威度审核器](../../cross-cutting/domain-authority-auditor/) · [实体优化器](../../cross-cutting/entity-optimizer/) · [内存管理工具](../../cross-cutting/memory-management/)

</details>

该工具会分析您网站的内部链接结构，并提供通过策略性内部链接来提升SEO的建议。它有助于分配网站权重、增强内容的主题相关性以及提高网站的可爬取性。

## 适用场景

- 优化网站架构以提升SEO效果
- 为重要页面分配权重
- 修复没有内部链接的“孤儿页面”
- 制定主题集群的内部链接策略
- 优化锚文本以提高SEO效果
- 恢复排名下降的页面
- 为新内容规划内部链接

## 功能介绍

1. **链接结构分析**：绘制当前的内部链接模式
2. **权重流动分析**：展示PageRank在网站中的流动情况
3. **孤儿页面检测**：找出没有内部链接的页面
4. **锚文本优化**：提升锚文本的多样性
5. **主题集群链接**：创建主题集群的链接策略
6. **链接机会识别**：确定需要添加链接的位置
7. **导航优化**：优化整个网站的链接元素

## 使用方法

### 分析当前链接结构

```
Analyze internal linking structure for [domain/sitemap]
```

```
Find internal linking opportunities for [URL]
```

### 制定链接策略

```
Create internal linking plan for topic cluster about [topic]
```

```
Suggest internal links for this new article: [content/URL]
```

### 修复问题

```
Find orphan pages on [domain]
```

```
Optimize anchor text across the site
```

## 数据来源

> 有关工具类别的更多信息，请参阅 [CONNECTORS.md](../../CONNECTORS.md)。

**当与 ~~网络爬虫 + ~~分析工具连接时：**
Claude可以通过 ~~网络爬虫** 自动完成整个网站的爬取，绘制完整的链接图谱；从 ~~分析工具** 获取页面性能数据，识别高价值页面，并分析网站内的链接流动情况。这有助于制定数据驱动的内部链接策略。

**仅使用手动数据时：**
请用户提供以下信息：
1. 网站地图URL或重要页面列表
2. 需要更多内部链接的关键页面URL
3. 内容类别或主题集群
4. 现有的链接结构文档

根据提供的数据进行分析。在输出结果中注明哪些发现来自自动爬取，哪些来自人工审核。

## 使用说明

当用户请求内部链接优化时，请按照以下步骤操作：

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

   > **CORE-EEAT对齐**：内部链接的质量与CORE-EEAT基准测试中的R08（内部链接图谱）相一致——使用描述性强的锚文本，确保链接能够体现主题权重。详细审计请参考 [内容质量审核器](../../cross-cutting/content-quality-auditor/)。

   ```markdown
   ## Anchor Text Analysis
   
   ### Current Anchor Text Patterns
   
   **Most Used Anchors**:
   
   | Anchor Text | Count | Target Pages | Assessment |
   |-------------|-------|--------------|------------|
   | "click here" | [X] | [X] pages | ❌ Not descriptive |
   | "read more" | [X] | [X] pages | ❌ Not descriptive |
   | "[exact keyword]" | [X] | [page] | ⚠️ May be over-optimized |
   | "[descriptive phrase]" | [X] | [page] | ✅ Good |
   
   ### Anchor Text Distribution by Page
   
   **Page: [Important URL]**
   
   | Anchor Text | Source Page | Status |
   |-------------|-------------|--------|
   | "[anchor 1]" | [source URL] | ✅/⚠️/❌ |
   | "[anchor 2]" | [source URL] | ✅/⚠️/❌ |
   
   **Issues Found**:
   - Over-optimized anchors: [X] instances
   - Generic anchors: [X] instances
   - Same anchor to multiple pages: [X] instances
   
   ### Anchor Text Recommendations
   
   **For Page: [URL]**
   
   Current: "[current anchor]" used [X] times
   
   Recommended variety:
   - "[variation 1]" - Use from [page type]
   - "[variation 2]" - Use from [page type]
   - "[variation 3]" - Use from [page type]
   
   **Anchor Score**: [X]/10
   ```

4. **制定主题集群链接策略** — 绘制当前的链接结构，推荐具体的链接内容

   > **参考**：请参阅 [references/linking-templates.md](./references/linking-templates.md) 中的主题集群链接策略模板（第4步）。

5. **寻找合适的链接机会** — 分析每个页面，寻找与主题相关的链接机会，并优先处理影响较大的链接添加

   > **参考**：请参阅 [references/linking-templates.md](./references/linking-templates.md) 中的链接机会模板（第5步）。

6. **优化导航和页脚链接** — 分析主导航、页脚、侧边栏和面包屑导航，推荐需要添加或删除的页面

   > **参考**：请参阅 [references/linking-templates.md](./references/linking-templates.md) 中的导航优化模板（第6步）。

7. **生成链接实施计划** — 包括执行摘要、当前状态指标、分阶段的优先行动（第1-4周）、实施指南和跟踪计划

   > **参考**：请参阅 [references/linking-templates.md](./references/linking-templates.md) 中的完整实施计划模板（第7步）。

## 验证要点

### 输入验证
- 提供网站结构或站点地图（URL或文件）
- 明确目标页面或主题集群
- 如果针对特定页面进行优化，请提供该页面的URL或内容

### 输出验证
- 每条建议都应引用具体的数据来源
- 所有的链接建议都应包含源页面、目标页面和推荐的锚文本
- 孤儿页面列表应包含URL及推荐的优化措施
- 明确每个数据点的来源（来自 ~~网络爬虫数据、~~分析工具数据、用户提供的数据或人工分析）

## 示例

> **参考**：请参阅 [references/linking-example.md](./references/linking-example.md) 中的完整示例（关于电子邮件营销最佳实践中的内部链接优化案例）。

## 成功技巧

1. **质量优先于数量** — 添加相关链接，而非随机链接
2. **以用户需求为导向** — 链接应帮助用户更好地导航网站
3. **多样化锚文本** — 避免过度优化
4. **链接到重要页面** — 战略性地分配权重
5. **定期审核** — 随着内容更新，定期维护内部链接

## 参考资料

- [链接架构模式](./references/link-architecture-patterns.md) — 链接架构模型（中心辐射型、孤岛型、扁平型、金字塔型、网状型），锚文本多样性框架，链接权重流动模型，以及内部链接审核清单
- [链接模板](./references/linking-templates.md) — 第6-7步的详细输出模板（导航优化、实施计划）
- [链接优化示例](./references/linking-example.md) — 完整的内部链接优化案例

## 相关技能

- [内容差距分析](../../research/content-gap-analysis/) — 寻找需要链接的内容
- [SEO内容编写器](../../build/seo-content-writer/) — 创建适合链接的内容
- [页面SEO审核器](../on-page-seo-auditor/) — 审核整体的页面SEO效果
- [技术SEO检查器](../technical-seo-checker/) — 检查网站的可爬取性
- [内容质量审核器](../../cross-cutting/content-quality-auditor/) — 全面的80项CORE-EEAT审核
- [结构化标记生成器](../../build/schema-markup-generator/) — 用于生成面包屑导航和导航结构的标记