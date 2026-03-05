---
name: seo-content-writer
version: "3.0.0"
description: '此技能适用于用户需要执行以下任务时：撰写SEO相关内容（如博客文章、产品描述、 landing page等）。它采用了一套12步的工作流程来生成符合SEO优化要求的优质内容，包括：  
1. **CORE-EEAT预写作检查清单**：确保内容符合写作规范；  
2. **关键词整合**：在文章中合理分布目标关键词；  
3. **标题优化**：提供5种标题生成方案；  
4. **元描述编写**；  
5. **H1/H2/H3层级结构设计**；  
6. **特色内容片段设计**；  
7. **内部/外部链接建设**；  
8. **可读性提升**。  
生成的文档会包含以下要素：  
- 嵌入的SEO优化元素；  
- 多种标题版本；  
- 元描述；  
- 带有Schema结构的FAQ（常见问题解答）部分；  
- 以及自评式的CORE-EEAT检查清单。  
如需针对特定关键词进行内容优化（例如：为[关键词]撰写2000字的文章），请使用该技能。  
- 关于AI辅助内容生成（如引用优化），请参考`geo-content-optimizer`；  
- 如需更新现有内容，请使用`content-refresher`工具。'
license: Apache-2.0
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
metadata:
  author: aaron-he-zhu
  version: "3.0.0"
  geo-relevance: "medium"
  tags:
    - seo
    - content-writing
    - blog-writing
    - seo-copywriting
    - content-creation
    - featured-snippet-optimization
    - how-to-guide
  triggers:
    - "write SEO content"
    - "create blog post"
    - "write an article"
    - "content writing"
    - "draft optimized content"
    - "write for SEO"
    - "blog writing"
    - "write me an article"
    - "create a blog post about"
    - "help me write SEO content"
    - "draft content for"
---
# SEO内容撰写专家

> **[SEO与地理定位技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与地理定位相关技能 · 全部技能可通过 `npx skills add aaron-he-zhu/seo-geo-claude-skills` 安装

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · **SEO内容撰写工具** · [地理内容优化器](../geo-content-optimizer/) · [元标签优化器](../meta-tags-optimizer/) · [结构化标记生成器](../schema-markup-generator/)

**优化** · [页面SEO审核工具](../../optimize/on-page-seo-auditor/) · [技术SEO检查工具](../../optimize/technical-seo-checker/) · [内部链接优化器](../../optimize/internal-linking-optimizer/) · [内容更新工具](../../optimize/content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告工具](../../monitor/performance-reporter/) · [警报管理工具](../../monitor/alert-manager/)

**跨领域技能** · [内容质量审核工具](../../cross-cutting/content-quality-auditor/) · [域名权威性审核工具](../../cross-cutting/domain-authority-auditor/) · [实体优化工具](../../cross-cutting/entity-optimizer/) · [内存管理工具](../../cross-cutting/memory-management/)

</details>

该技能可生成经过搜索引擎优化的内容，既能在排名上取得良好表现，又能为读者提供真正有价值的信息。它运用了经过验证的SEO写作技巧、恰当的关键词整合方法以及最佳的内容结构。

## 适用场景

- 撰写针对特定关键词的博客文章
- 创建适合搜索的 landing 页面
- 为专题系列开发核心内容
- 为电子商务平台编写产品描述
- 为本地SEO创建服务页面
- 制作操作指南和教程
- 撰写对比和评测文章

## 该技能的功能

1. **关键词整合**：自然地融入目标关键词及相关关键词
2. **结构优化**：创建易于阅读、组织有序的内容
3. **标题与元标签生成**：撰写引人注目、点击率高的标题
4. **标题层级优化**：使用合理的H1-H6标题层级
5. **内部链接建议**：提供相关的内部链接建议
6. **可读性提升**：确保内容易于理解且引人入胜
7. **特色片段优化**：优化内容以适应搜索引擎的特色展示

## 使用方法

### 基本内容创作

```
Write an SEO-optimized article about [topic] targeting the keyword [keyword]
```

```
Create a blog post for [topic] with these keywords: [keyword list]
```

### 特定需求下的使用

```
Write a 2,000-word guide about [topic] targeting [keyword],
include FAQ section for featured snippets
```

### 内容需求说明

```
Here's my content brief: [brief]. Write SEO-optimized content following this outline.
```

## 数据来源

> 请参阅 [CONNECTORS.md](../../CONNECTORS.md) 以获取工具类别的相关信息。

**当连接到 ~~SEO工具 + ~~搜索控制台时：**
自动获取关键词指标（搜索量、难度、CPC）、竞争对手内容分析（排名靠前的页面、内容长度、常见主题）、SERP特色展示（特色片段、PAA问题）以及关键词机会（相关关键词、基于问题的查询）。

**仅使用手动数据时：**
要求用户提供：
1. 目标主要关键词及3-5个次要关键词
2. 目标受众和搜索意图（信息型/商业型/交易型）
3. 目标字数和期望的语气
4. 可参考的竞争对手网址或内容示例

根据提供的数据开始完整的工作流程。在输出中注明哪些指标来自自动化收集，哪些来自用户提供的数据。

## 指导步骤

当用户请求SEO内容时：

1. **收集需求**
   确认或询问以下内容：
   ```markdown
   ### Content Requirements
   
   **Primary Keyword**: [main keyword]
   **Secondary Keywords**: [2-5 related keywords]
   **Target Word Count**: [length]
   **Content Type**: [blog/guide/landing page/etc.]
   **Target Audience**: [who is this for]
   **Search Intent**: [informational/commercial/transactional]
   **Tone**: [professional/casual/technical/friendly]
   **CTA Goal**: [what action should readers take]
   **Competitor URLs**: [top ranking content to beat]
   ```

2. **加载CORE-EEAT质量标准**
   在开始写作前，从 [CORE-EEAT基准](../../references/core-eeat-benchmark.md) 中加载内容质量标准：
   ```markdown
   ### CORE-EEAT Pre-Write Checklist

   **Content Type**: [identified from requirements above]
   **Loaded Constraints** (high-weight items for this content type):

   Apply these standards while writing:

   | ID | Standard | How to Apply |
   |----|----------|-------------|
   | C01 | Intent Alignment | Title promise must match content delivery |
   | C02 | Direct Answer | Core answer in first 150 words |
   | C06 | Audience Targeting | State "this article is for..." |
   | C10 | Semantic Closure | Conclusion answers opening question + next steps |
   | O01 | Heading Hierarchy | H1→H2→H3, no level skipping |
   | O02 | Summary Box | Include TL;DR or Key Takeaways |
   | O06 | Section Chunking | Each section single topic; paragraphs 3–5 sentences |
   | O09 | Information Density | No filler; consistent terminology |
   | R01 | Data Precision | ≥5 precise numbers with units |
   | R02 | Citation Density | ≥1 external citation per 500 words |
   | R04 | Evidence-Claim Mapping | Every claim backed by evidence |
   | R07 | Entity Precision | Full names for people/orgs/products |
   | C03 | Query Coverage | Cover ≥3 query variants (synonyms, long-tail) |
   | O08 | Anchor Navigation | Table of contents with jump links |
   | O10 | Multimedia Structure | Images/videos have captions and carry information |
   | E07 | Practical Tools | Include downloadable templates, checklists, or calculators |

   _These 16 items apply across all content types. For content-type-specific dimension weights, see the Content-Type Weight Table in [core-eeat-benchmark.md](../../references/core-eeat-benchmark.md)._
   _Full 80-item benchmark: [references/core-eeat-benchmark.md](../../references/core-eeat-benchmark.md)_
   _For complete content quality audit: use [content-quality-auditor](../../cross-cutting/content-quality-auditor/)_
   ```

3. **研究与规划**
   在开始写作前：
   ```markdown
   ### Content Research
   
   **SERP Analysis**:
   - Top results format: [what's ranking]
   - Average word count: [X] words
   - Common sections: [list]
   - SERP features: [snippets, PAA, etc.]
   
   **Keyword Map**:
   - Primary: [keyword] - use in title, H1, intro, conclusion
   - Secondary: [keywords] - use in H2s, body paragraphs
   - LSI/Related: [terms] - sprinkle naturally throughout
   - Questions: [PAA questions] - use as H2/H3s or FAQ
   
   **Content Angle**:
   [What unique perspective or value will this content provide?]
   ```

4. **创建优化后的标题**
   ```markdown
   ### Title Optimization
   
   **Requirements**:
   - Include primary keyword (preferably at start)
   - Under 60 characters for full SERP display
   - Compelling and click-worthy
   - Match search intent
   
   **Title Options**:
   
   1. [Title option 1] ([X] chars)
      - Keyword position: [front/middle]
      - Power words: [list]
   
   2. [Title option 2] ([X] chars)
      - Keyword position: [front/middle]
      - Power words: [list]
   
   **Recommended**: [Best option with reasoning]
   ```

5. **编写元描述**
   ```markdown
   ### Meta Description
   
   **Requirements**:
   - 150-160 characters
   - Include primary keyword naturally
   - Include call-to-action
   - Compelling and specific
   
   **Meta Description**:
   "[Description text]" ([X] characters)
   
   **Elements included**:
   - ✅ Primary keyword
   - ✅ Value proposition
   - ✅ CTA or curiosity hook
   ```

6. **构建内容结构并开始写作**
   结构如下：H1（每个页面使用一个主要关键词）> 引言（100-150字，包含吸引人的开头、承诺以及关键词）> H2小节（次要关键词/问题）> H3子标题> 常见问题解答（FAQ）> 结论（总结 + 关键词 + 行动号召）

7. **应用页面SEO最佳实践**
   遵循页面SEO检查清单（关键词布局、内容质量、可读性、技术要素），并使用内容写作模板（标题中包含关键词、吸引人的开头、使用H2/H3小节、FAQ和行动号召）。
   > **参考**：请参阅 [references/seo-writing-checklist.md](./references/seo-writing-checklist.md) 以获取完整的页面SEO检查清单、内容写作模板和特色片段优化指南。
   写作时的关键要求：
   - 标题、H1、前100字、至少一个H2小节以及结论中必须包含主要关键词
   - 每段3-5句话；句子长度多样化；使用项目符号和加粗的关键短语
   - 包含2-5个内部链接和2-3个外部权威链接
   - 常见问题解答部分需包含40-60字的答案，以便被搜索引擎收录为特色片段
   - 根据需要优化内容格式，使其适合定义、列表或操作指南的形式

8. **添加内部/外部链接**
   ```markdown
   ### Link Recommendations
   
   **Internal Links** (include 2-5):
   1. "[anchor text]" → [/your-page-url] (relevant because: [reason])
   2. "[anchor text]" → [/your-page-url] (relevant because: [reason])
   
   **External Links** (include 2-3 authoritative sources):
   1. "[anchor text]" → [authoritative-source.com] (supports: [claim])
   2. "[anchor text]" → [authoritative-source.com] (supports: [claim])
   ```

9. **最终SEO审核和CORE-EEAT自我检查**
    从10个SEO方面（标题、元描述、H1、关键词布局、内部链接、外部链接、FAQ、可读性、字数）对内容进行评分，给出总分（10分）。
    然后验证16项CORE-EEAT预写作要求（C01、C02、C06、C10、O01、O02、O06、O09、R01、R02、R04、R07、C03、O08、O10、E07），并标记通过/警告/失败的状态。列出需要改进的项。
    _如需进行全面的80项审核，请使用 [content-quality-auditor](../../cross-cutting/content-quality-auditor/)_

## 验证要点

### 输入验证
- [ ] 主要关键词已确认且符合搜索意图
- [ ] 指定了目标字数（实质性内容至少800字）
- [ ] 明确了内容类型和目标受众
- [ ] 已查看竞争对手的网址或确定了目标SERP特色展示

### 输出验证
- [ ] 主要关键词的密度在1-2%范围内（注意：关键词密度仅供参考，并非硬性要求。现代搜索引擎更重视语义相关性和自然语言表达，而非精确的密度比例。重点在于全面覆盖主题，而非达到特定的百分比。）
- [ ] 大纲中的所有部分都已涵盖
- [ ] 包含了2-5个相关内部链接
- [ ] 常见问题解答部分包含至少3个问题
- [ ] 可读性适合目标受众
- [ ] 每个数据来源都明确标注（来自SEO工具、用户提供或估算）

## 示例

**用户**：“撰写一篇针对小型企业的‘电子邮件营销最佳实践’的SEO优化文章”

> **参考**：请参阅 [references/seo-writing-checklist.md](./references/seo-writing-checklist.md)，了解包含元描述、H1/H2/H3层级、带有引用数据的统计信息、对比表格、常见问题解答部分以及带有行动号召的完整SEO文章示例。

示例输出展示了：标题和前100字中包含关键词、带有来源（DMA、Emarsys）的统计数据、对比表格、项目符号列表、专业提示、包含40-60字答案的常见问题解答部分，以及结论中的明确行动号召。

## 内容类型模板

### 操作指南

```
Write a how-to guide for [task] targeting [keyword]
```

### 对比文章

```
Write a comparison article: [Option A] vs [Option B] for [keyword]
```

### 列表文章

```
Write a list post: "X Best [Items] for [Audience/Purpose]" targeting [keyword]
```

### 终极指南

```
Write an ultimate guide about [topic] (3,000+ words) targeting [keyword]
```

## 成功技巧

1. **匹配搜索意图** - 信息型查询需要的是指南，而非销售页面
2. **提前提供价值** - 将关键信息放在文章开头，以便读者快速获取有用信息
3. **使用数据和示例** - 具体内容总是比通用内容更有效
4. **以用户为中心进行写作** - SEO优化应显得自然
5. **添加视觉元素** - 用图片、表格、列表等方式打破文本的单一性
6. **定期更新** - 新鲜的内容能向搜索引擎传递更新信号

## 参考资料

- [标题公式](./references/title-formulas.md) - 经验证的标题公式、常用关键词、点击率提升技巧
- [内容结构模板](./references/content-structure-templates.md) - 博客文章、对比文章、列表文章、操作指南、专题页面的模板

## 相关技能

- [关键词研究](../../research/keyword-research/) — 寻找目标关键词
- [地理内容优化器](../geo-content-optimizer/) — 优化内容以获得AI推荐
- [元标签优化器](../meta-tags-optimizer/) — 创建吸引人的元标签
- [页面SEO审核工具](../../optimize/on-page-seo-auditor/) — 审核SEO元素
- [内容质量审核工具](../../cross-cutting/content-quality-auditor/) — 全面的80项CORE-EEAT审核