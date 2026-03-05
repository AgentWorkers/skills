---
name: on-page-seo-auditor
version: "3.0.0"
description: '此技能适用于用户请求进行“页面SEO审计”、“页面SEO检查”、“SEO评分”、“页面优化”、“该页面存在哪些SEO问题”、“该页面的SEO状况如何”、“对我的页面进行评分”或“为什么这个页面没有排名”的情况。它能够执行全面的页面SEO审计，以识别优化机会，包括标题标签、元描述、页面头部、内容质量、内部链接以及图片优化等方面。对于服务器速度和爬虫相关的问题，请参阅“technical-seo-checker”；如需进行完整的EEAT内容质量评分，请参阅“content-quality-auditor”。'
license: Apache-2.0
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
allowed-tools: WebFetch
metadata:
  author: aaron-he-zhu
  version: "3.0.0"
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
    - page-audit
    - seo-score
    - on-page-optimization
    - optimization-checklist
    - seo-checklist
    - page-score
    - h1-optimization
    - meta-audit
    - content-audit
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

> **[SEO与地理定位技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与地理定位相关技能 · 全部技能的安装命令：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容编写器](../../build/seo-content-writer/) · [地理内容优化器](../../build/geo-content-optimizer/) · [元标签优化器](../../build/meta-tags-optimizer/) · [架构标记生成器](../../build/schema-markup-generator/)

**优化** · **在页面上的SEO审计** · [技术SEO检查器](../technical-seo-checker/) · [内部链接优化器](../internal-linking-optimizer/) · [内容更新工具](../content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告工具](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)

**跨领域技能** · [内容质量审计器](../../cross-cutting/content-quality-auditor/) · [域名权威性审计器](../../cross-cutting/domain-authority-auditor/) · [实体优化器](../../cross-cutting/entity-optimizer/) · [内存管理](../../cross-cutting/memory-management/)

</details>

该工具可执行详细的在页面上的SEO审计，以识别问题并发现优化机会。它分析所有影响搜索排名的页面元素，并提供可操作的优化建议。

## 何时使用此技能

- 在页面发布前后进行审计
- 查明页面排名不佳的原因
- 优化现有内容以提高表现
- 创建发布前的SEO检查清单
- 将您的在页面SEO与竞争对手进行比较
- 进行系统性的全站SEO改进
- 培训团队成员掌握SEO最佳实践

## 该技能的功能

1. **标题标签分析**：评估标题的优化程度和点击率潜力
2. **元描述审核**：检查描述的质量和长度
3. **标题结构审计**：分析H1-H6标题的层级结构
4. **内容质量评估**：审查内容的深度和优化情况
5. **关键词使用分析**：检查关键词的布局和密度
6. **内部链接审核**：评估内部链接的结构
7. **图片优化检查**：审核图片的替代文本和文件优化情况
8. **技术性在页面元素审核**：检查URL、规范链接（canonical link）以及移动设备适应性

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

> 有关工具类别的详细信息，请参阅[CONNECTORS.md](../../CONNECTORS.md)。

**当与SEO工具和网络爬虫结合使用时：**
Claude可以通过网络爬虫自动获取页面HTML内容，从SEO工具中获取关键词的搜索量和难度数据，从搜索控制台获取点击率数据，并下载竞争对手的页面进行比较。这可以实现基于实时数据的完全自动化审计。

**仅使用手动数据时：**
要求用户提供：
1. 页面URL或完整的HTML内容
2. 目标的主要和次要关键词
3. 用于比较的竞争对手页面URL（可选）

使用提供的数据进行全面审计。在输出结果中注明哪些发现来自自动化爬取，哪些来自手动审核。

## 使用说明

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

5. **审计内容质量** — 字数、阅读难度、完整性、格式、E-E-A-T（易读性、易懂性、吸引力、相关性）指标、内容元素检查清单、差距识别

   > **参考**：有关内容质量检查清单的模板，请参阅[references/audit-templates.md](./references/audit-templates.md)（步骤5）。

6. **审计关键词使用情况** — 检查所有页面元素中主要/次要关键词的布局、LSI（相关术语）以及关键词的密度

   > **参考**：有关关键词优化模板，请参阅[references/audit-templates.md](./references/audit-templates.md)（步骤6）。

7. **审计内部链接** — 链接数量、链接文本的相关性、失效链接以及需要添加的链接

   > **参考**：有关内部链接检查清单的模板，请参阅[references/audit-templates.md](./references/audit-templates.md)（步骤7）。

8. **审计图片** — 图片的替代文本、文件名、大小、格式以及懒加载功能

   > **参考**：有关图片优化模板，请参阅[references/audit-templates.md](./references/audit-templates.md)（步骤8）。

9. **审计技术性在页面元素** — URL、规范链接、移动设备适应性、页面加载速度、HTTPS协议以及页面的架构标记（schema）

   > **参考**：有关技术性在页面元素检查的模板，请参阅[references/audit-templates.md](./references/audit-templates.md)（步骤9）。

10. **CORE-EEAT内容质量快速扫描** — 从80项评估指标中筛选出的17项与页面内容相关的指标

    > **参考**：有关CORE-EEAT快速扫描模板，请参阅[references/audit-templates.md](./references/audit-templates.md)（步骤10）。完整评估标准请参见[CORE-EEAT评估标准](../../references/core-eeat-benchmark.md)。

11. **生成审计报告** — 提供包含整体得分、问题优先级（紧急/重要/次要）、快速改进措施、详细建议、竞争对手对比结果以及行动清单的审计报告

    > **参考**：有关完整审计报告模板的详细信息，请参阅[references/audit-templates.md](./references/audit-templates.md)（步骤11）。

## 验证要点

### 输入验证
- 用户明确指定了目标关键词
- 页面内容可以通过URL或提供的HTML内容访问
- 如果需要与竞争对手进行比较，则提供了竞争对手的页面URL

### 输出验证
- 每条建议都基于具体的数据点（而非泛泛而谈）
- 评分基于可衡量的标准，而非主观判断
- 所有建议的修改都指明了具体的位置（如标题标签、H2标题、第5段等）
- 每个数据点的来源都明确标注（来自SEO工具、用户提供的数据或手动审核）

## 示例

> 有关完整的审计示例（以降噪耳机为例）以及不同页面类型（博客文章、产品页面、着陆页）的检查清单，请参阅[references/audit-example.md](./references/audit-example.md)。

## 成功技巧

1. **按问题影响程度优先处理** — 先解决关键问题
2. **与竞争对手进行比较** — 了解哪些优化措施有助于提高排名
3. **平衡优化与可读性** — 避免过度优化
4. **定期进行审计** — 内容会随时间退化
5. **测试更改效果** — 更新后跟踪排名变化

> **评分详情**：有关评分标准、评分细则、问题解决流程以及行业基准信息，请参阅[references/scoring-rubric.md](./references/scoring-rubric.md)。

## 参考资料

- [评分标准](./references/scoring-rubric.md) — 详细的评分标准、权重分配以及在页面上SEO审计的评分等级
- [审计模板](./references/audit-templates.md) — 第5至11步的详细输出模板（内容质量、关键词、链接、图片、技术性元素、CORE-EEAT评估、审计报告）
- [审计示例与检查清单](./references/audit-example.md) — 完整的审计示例以及不同页面类型的检查清单（博客、产品页面、着陆页）

## 相关技能

- [seo-content-writer](../../build/seo-content-writer/) — 创建优化后的内容
- [technical-seo-checker](../technical-seo-checker/) — 进行技术性SEO审计
- [meta-tags-optimizer](../../build/meta-tags-optimizer/) — 优化元标签
- [serp-analysis](../../research/serp-analysis/) — 为审计结果提供SERP（搜索结果页面）背景信息
- [content-refresher](../content-refresher/) — 更新现有内容
- [content-quality-auditor](../../cross-cutting/content-quality-auditor/) — 进行全面的80项CORE-EEAT评估
- [internal-linking-optimizer](../internal-linking-optimizer/) — 优化内部链接结构
- [schema-markup-generator](../../build/schema-markup-generator/) — 验证并生成页面的架构标记