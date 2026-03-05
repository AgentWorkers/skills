---
name: content-refresher
version: "3.0.0"
description: '当用户请求“更新旧内容”、“刷新内容”、“内容已经过时”、“提升下降的排名”、“重新激活旧的博客文章”、“这篇文章已经过时”或“该页面的流量正在下降”时，应使用此技能。该技能用于识别并更新过时的内容，以恢复和提升搜索引擎排名。它包括分析内容的新鲜度、添加新信息、更新统计数据，并优化内容以满足当前的SEO和地理位置（GEO）最佳实践。如需从头开始编写新内容，请参阅“seo-content-writer”；如需进行无需重写的审计，请参阅“on-page-seo-auditor”。'
license: Apache-2.0
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
metadata:
  author: aaron-he-zhu
  version: "3.0.0"
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
    - content-update
    - content-decay
    - evergreen-content
    - content-freshness
    - content-revival
    - refresh-content
    - update-statistics
    - republishing
    - content-lifecycle
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
# 内容更新技巧

> **[SEO与地理定位（GEO）技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 包含20项SEO与GEO相关技能 · 全部技能可通过 `npx skills add aaron-he-zhu/seo-geo-claude-skills` 安装

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [搜索引擎排名（SERP）分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容撰写工具](../../build/seo-content-writer/) · [地理定位内容优化工具](../../build/geo-content-optimizer/) · [元标签优化工具](../../build/meta-tags-optimizer/) · [结构化标记生成工具](../../build/schema-markup-generator/)

**优化** · [页面SEO审核工具](../on-page-seo-auditor/) · [技术SEO检查工具](../technical-seo-checker/) · [内部链接优化工具](../internal-linking-optimizer/) · **内容更新技巧**

**监控** · [排名追踪工具](../../monitor/rank-tracker/) · [反向链接分析工具](../../monitor/backlink-analyzer/) · [性能报告工具](../../monitor/performance-reporter/) · [警报管理工具](../../monitor/alert-manager/)

**跨领域工具** · [内容质量审核工具](../../cross-cutting/content-quality-auditor/) · [域名权威性审核工具](../../cross-cutting/domain-authority-auditor/) · [实体信息优化工具](../../cross-cutting/entity-optimizer/) · [内存管理工具](../../cross-cutting/memory-management/)

</details>

此技能用于识别并更新过时的内容，以恢复失去的排名和流量。它能够分析内容的新鲜度，找出需要更新的部分，并指导更新过程，从而最大化SEO和GEO的效果。

## 何时使用此技能

- 内容随着时间推移失去了排名或流量
- 统计数据和信息已经过时
- 竞争对手发布了更好的内容
- 内容需要根据新情况更新
- 行业变化要求更新内容
- 需要在现有内容中添加新章节
- 需要将旧内容转换为适合地理定位优化的格式

## 此技能的功能

1. **新鲜度分析**：识别需要更新的内容
2. **性能监控**：找出流量下降的内容
3. **差距识别**：发现竞争对手拥有的但自己缺失的信息
4. **更新优先级排序**：根据更新潜力对内容进行排序
5. **更新建议**：提供具体的更新指导
6. **地理定位优化**：更新内容以提高AI引用的可能性
7. **重新发布策略**：提供关于发布日期和推广策略的建议

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

> 有关工具类别的更多信息，请参阅 [CONNECTORS.md](../../CONNECTORS.md)。

**当连接到 ~~分析工具 + ~~搜索控制台 + ~~SEO工具** 时：**
Claude可以自动从 ~~分析工具** 获取历史流量趋势，从 ~~搜索控制台** 获取点击量和排名数据，从 ~~SEO工具** 获取关键词排名历史记录，并识别表现下降的内容。这有助于基于数据来优先安排更新任务。

**仅使用手动数据时：**
请用户提供以下信息：
1. 流量数据或显示性能趋势的截图
2. 关键页面的排名截图或历史记录
3. 内容的发布日期和最后一次更新日期
4. 用户认为需要更新的内容列表

使用提供的数据进行分析。在输出结果中注明哪些发现是基于自动化数据得出的，哪些是基于人工审核得出的。

## 使用说明

当用户请求内容更新帮助时：

1. **CORE-EEAT快速评估** — 在更新之前，进行一次快速的CORE-EEAT评估，以便将精力集中在最薄弱的环节上。参考：[CORE-EEAT基准](../../references/core-eeat-benchmark.md)

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

2. **确定需要更新的内容**  
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
   流量高且下降速度快 = 🔴 立即更新  
   流量高但下降速度慢 = 🟡 安排更新  
   流量低且下降速度快 = 🟡 评估后再决定  
   流量低且下降速度慢 = 🟢 优先级较低  
   ```
   ```

3. **分析单个内容以确定更新需求**  
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

5. **制定更新计划** — 包括结构调整、内容添加、统计数据的更新、链接的更新以及图片的替换  
   > **参考**：请参阅 [references/refresh-templates.md](./references/refresh-templates.md) 以获取完整的更新计划模板（第5步）。

6. **撰写更新后的内容** — 包括更新的引言、新章节、更新后的统计数据、新的常见问题解答部分  
   > **参考**：请参阅 [references/refresh-templates.md](./references/refresh-templates.md) 以获取更新内容撰写模板（第6步）。

7. **在更新过程中进行地理定位优化** — 使用清晰的定义、可引用的陈述、问答部分以及更新的引用信息  
   > **参考**：请参阅 [references/refresh-templates.md](./references/refresh-templates.md) 以获取地理定位优化模板（第7步）。

8. **制定重新发布策略** — 包括发布日期（是否更新“最后更新”标签/保持原样）、技术实现细节以及推广计划  
   > **参考**：请参阅 [references/refresh-templates.md](./references/refresh-templates.md) 以获取重新发布策略模板（第8步）。

9. **生成更新报告** — 包括变更摘要、已完成更新的内容、预期效果以及下一次审核日期  
   > **参考**：请参阅 [references/refresh-templates.md](./references/refresh-templates.md) 以获取更新报告模板（第9步）。

## 验证要点

### 输入验证
- [ ] 已明确指定目标内容的URL或标题  
- [ ] 有可用的历史性能数据（流量趋势、排名信息）  
- [ ] 已知内容的发布/更新日期  
- [ ] 如果与竞争对手进行比较，请提供竞争对手的URL

### 输出验证
- [ ] 每条建议都基于具体的数据点（而非泛泛而谈）  
- [ ] 过时的内容会附带具体的示例和替换数据  
- [ ] 所有建议的添加内容都会包含字数统计和在文档中的位置  
- [ ] 每个数据来源都会明确标注（来自 ~~分析工具、~~搜索控制台、~~SEO工具，或是用户提供的数据）

## 示例

> **参考**：请参阅 [references/refresh-example.md](./references/refresh-example.md) 以获取完整的示例（云托管服务的内容更新流程）和详细的内容更新检查清单。

## 成功技巧

1. **按投资回报率（ROI）优先级排序** — 先更新潜力较大的内容  
2. **不要仅仅添加日期** — 要进行实质性的改进  
3. **超越竞争对手** — 不仅添加他们已有的内容，还要添加更多有价值的内容  
4. **跟踪更新效果** — 监控更新后的排名变化  
5. **定期进行审核** — 每季度检查内容的质量  
6. **进行地理定位优化** — 每次更新都是一个优化地理定位的机会  

> **参考资料**：有关内容衰退的信号、生命周期阶段、更新与重写决策框架以及不同类型内容的更新策略，请参阅 [references/content-decay-signals.md](./references/content-decay-signals.md)。

## 参考资料

- [内容衰退信号](./references/content-decay-signals.md) — 不同类型内容的衰退指标、生命周期阶段以及更新触发条件  
- [更新模板](./references/refresh-templates.md) — 第5至9步的详细输出模板（更新计划、内容撰写、地理定位优化、重新发布、报告）  
- [更新示例及检查清单](./references/refresh-example.md) — 完整的更新示例及更新前的检查清单  

## 相关技能

- [内容差距分析](../../research/content-gap-analysis/) — 确定需要添加的内容  
- [SEO内容撰写工具](../../build/seo-content-writer/) — 撰写新章节  
- [地理定位内容优化工具](../../build/geo-content-optimizer/) — 优化内容以适应AI需求  
- [页面SEO审核工具](../on-page-seo-auditor/) — 审核更新后的内容  
- [内容质量审核工具](../../cross-cutting/content-quality-auditor/) — 进行全面的80项CORE-EEAT审核