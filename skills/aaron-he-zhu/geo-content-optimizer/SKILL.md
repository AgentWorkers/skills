---
name: geo-content-optimizer
version: "3.0.0"
description: '此技能适用于以下场景：用户请求“针对AI进行优化”、“让内容被ChatGPT引用”、“在AI生成的答案中显示自己的内容”、“进行地理定位优化（GEO optimization）”、“优化生成式引擎（generative engine optimization）”、“优化Google AI Overview的相关内容”、“让内容被Perplexity AI提及”、“在Google Gemini生成的答案中显示自己的内容”、“确保AI生成的内容中不提及自己的品牌”、“使内容适合被AI引用”或“提高内容在AI系统中的被引用频率”。该技能旨在提升内容在多个AI系统（如ChatGPT、Claude、Perplexity AI、Google AI Overview和Google Gemini）中的被引用频率。具体优化措施包括：添加可被引用的陈述、构建结构化的问答部分、提供带有来源的精确统计数据、标注专家信息以及遵循FAQ（常见问题解答）的格式规范。优化目标主要围绕CORE-EEAT框架中的GEO-First相关项目（C02、C09、O03、R01–R05、E01）展开。优化完成后，会生成相应的GEO评分报告、重写后的内容段落以及一个引用优化检查清单。如需针对SEO（搜索引擎优化）的写作指导，请参考seo-content-writer；如需处理实体和品牌在AI中的展示问题，请参考entity-optimizer。'
license: Apache-2.0
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
metadata:
  author: aaron-he-zhu
  version: "3.0.0"
  geo-relevance: "high"
  tags:
    - geo
    - ai-citations
    - chatgpt
    - perplexity-ai
    - google-ai-overview
    - gemini
    - llm-citations
    - generative-engine-optimization
    - ai-overview-optimization
    - quotable-content
  triggers:
    - "optimize for AI"
    - "get cited by ChatGPT"
    - "AI optimization"
    - "appear in AI answers"
    - "GEO optimization"
    - "AI-friendly content"
    - "LLM citations"
    - "get cited by AI"
    - "show up in ChatGPT answers"
    - "AI doesn't mention my brand"
    - "make content AI-quotable"
---
# 地理内容优化器（GEO Content Optimizer）

> **[SEO与地理优化技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 包含20项SEO与地理优化相关技能 · 全部技能的安装命令：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容编写器](../seo-content-writer/) · **地理内容优化器** · [元标签优化器](../meta-tags-optimizer/) · [结构化标记生成器](../schema-markup-generator/)

**优化** · [页面SEO审核器](../../optimize/on-page-seo-auditor/) · [技术SEO检查器](../../optimize/technical-seo-checker/) · [内部链接优化器](../../optimize/internal-linking-optimizer/) · [内容更新工具](../../optimize/content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告工具](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)

**跨领域工具** · [内容质量审核器](../../cross-cutting/content-quality-auditor/) · [域名权威性审核器](../../cross-cutting/domain-authority-auditor/) · [实体优化器](../../cross-cutting/entity-optimizer/) · [内存管理工具](../../cross-cutting/memory-management/)

</details>

该工具用于优化内容，使其更易于被AI系统引用。随着AI系统越来越多地直接回答用户查询，让内容被这些系统引用变得至关重要。

## 适用场景

- 优化现有内容以增加被AI引用的机会
- 创建同时符合SEO和地理优化要求的新内容
- 提高内容在AI推荐结果中的显示概率
- 使内容更易于被AI系统引用
- 增加AI系统信任的权威性信号
- 优化内容结构以便AI系统更好地理解

## 功能介绍

1. **引用优化**：提高内容被AI引用的可能性
2. **结构优化**：优化内容结构，便于AI系统理解
3. **权威性提升**：增加AI系统信任的权威性信号
4. **事实准确性**：提升内容的准确性和可验证性
5. **引用生成**：创建易于被引用的陈述
6. **来源标注**：添加AI系统可验证的引用信息
7. **地理评分**：评估内容的AI友好度

## 使用方法

### 优化现有内容

```
Optimize this content for GEO/AI citations: [content or URL]
```

```
Make this article more likely to be cited by AI systems
```

### 创建符合地理优化要求的内容

```
Write content about [topic] optimized for both SEO and GEO
```

### 进行地理内容审计

```
Audit this content for GEO readiness and suggest improvements
```

## 数据来源

> 有关工具类别的详细信息，请参阅 [CONNECTORS.md](../../CONNECTORS.md)。

**当连接到AI监控工具和SEO工具时：**
- 自动获取AI引用模式（哪些内容被ChatGPT、Claude、Perplexity等系统引用）、当前的AI可见性评分、竞争对手的引用频率以及内容在AI推荐结果中的显示情况。

**仅使用手动数据时：**
- 请用户提供以下信息：
  - 需要AI引用的目标查询词
  - 当前内容的URL或完整文本
  - 竞争对手被AI引用的实例

- 使用提供的数据完成整个优化流程。在输出结果中明确标注哪些数据来自自动化收集，哪些来自用户提供。

## 使用说明

当用户请求进行地理优化时：

1. **加载CORE-EEAT地理优先优化目标**
   在优化之前，从 [CORE-EEAT基准](../../references/core-eeat-benchmark.md) 中加载与地理优化相关的关键内容：

   ```markdown
   ### CORE-EEAT GEO-First Targets

   These items have the highest impact on AI engine citation. Use as optimization checklist:

   **Top 6 Priority Items**:
   | Rank | ID | Standard | Why It Matters |
   |------|----|----------|---------------|
   | 1 | C02 | Direct Answer in first 150 words | All engines extract from first paragraph |
   | 2 | C09 | Structured FAQ with Schema | Directly matches AI follow-up queries |
   | 3 | O03 | Data in tables, not prose | Most extractable structured format |
   | 4 | O05 | JSON-LD Schema Markup | Helps AI understand content type |
   | 5 | E01 | Original first-party data | AI prefers exclusive, verifiable sources |
   | 6 | O02 | Key Takeaways / Summary Box | First choice for AI summary citations |

   **All GEO-First Items** (optimize for all when possible):
   C02, C04, C05, C07, C08, C09 | O02, O03, O04, O05, O06, O09
   R01, R02, R03, R04, R05, R07, R09 | E01, E02, E03, E04, E06, E08, E09, E10
   Exp10 | Ept05, Ept08 | A08

   **AI Engine Preferences**:
   | Engine | Priority Items |
   |--------|----------------|
   | Google AI Overview | C02, O03, O05, C09 |
   | ChatGPT Browse | C02, R01, R02, E01 |
   | Perplexity AI | E01, R03, R05, Ept05 |
   | Claude | R04, Ept08, Exp10, R03 |

   _Full benchmark: [references/core-eeat-benchmark.md](../../references/core-eeat-benchmark.md)_
   ```

2. **分析现有内容**

   ```markdown
   ## GEO Analysis: [Content Title]
   
   ### Current State Assessment
   
   | GEO Factor | Current Score (1-10) | Notes |
   |------------|---------------------|-------|
   | Clear definitions | [X] | [notes] |
   | Quotable statements | [X] | [notes] |
   | Factual density | [X] | [notes] |
   | Source citations | [X] | [notes] |
   | Q&A format | [X] | [notes] |
   | Authority signals | [X] | [notes] |
   | Content freshness | [X] | [notes] |
   | Structure clarity | [X] | [notes] |
   | **GEO Readiness** | **[avg]/10** | **Average across factors** |
   
   **Primary Weaknesses**:
   1. [Weakness 1]
   2. [Weakness 2]
   3. [Weakness 3]
   
   **Quick Wins**:
   1. [Quick improvement 1]
   2. [Quick improvement 2]
   ```

3. **应用地理优化技术**
   - **地理优化基础**：AI系统更倾向于引用权威性高（有专家资质、引用准确）、信息准确（可验证、最新）、表述清晰（结构合理、无歧义）且易于引用的内容。详情请参阅 [references/geo-optimization-techniques.md](./references/geo-optimization-techniques.md)。
   - 应用六项核心优化技术：定义优化、引用生成、权威性提升、结构优化、事实密度提升以及FAQ结构化标记的添加。
   - **参考资料**：[references/geo-optimization-techniques.md](./references/geo-optimization-techniques.md) 中提供了每项技术的详细示例、模板和检查清单。
   - 关键原则：
     - **定义**：25-50个单词，独立成句，以关键词开头
     - **易于引用的陈述**：包含具体数据来源的明确统计信息
     - **权威性信号**：带有专家资质和正确引用来源的引用
     - **结构**：问答格式、对比表、编号列表
     - **事实密度**：用具体数据替换模糊的表述
     - **FAQ结构化标记**：使用JSON-LD格式标注FAQ内容

4. **生成优化后的内容**

   ```markdown
   ## GEO Optimization Report

   ### Changes Made

   **Definitions Added/Improved**:
   1. [Definition 1] - [location in content]
   2. [Definition 2] - [location in content]

   **Quotable Statements Created**:
   1. "[Statement 1]"
   2. "[Statement 2]"

   **Authority Signals Added**:
   1. [Expert quote/citation]
   2. [Source attribution]

   **Structural Improvements**:
   1. [Change 1]
   2. [Change 2]

   ### Before/After GEO Score

   | GEO Factor | Before (1-10) | After (1-10) | Change |
   |------------|---------------|--------------|--------|
   | Clear definitions | [X] | [X] | +[X] |
   | Quotable statements | [X] | [X] | +[X] |
   | Factual density | [X] | [X] | +[X] |
   | Source citations | [X] | [X] | +[X] |
   | Q&A format | [X] | [X] | +[X] |
   | Authority signals | [X] | [X] | +[X] |
   | **Overall GEO Score** | **[avg]/10** | **[avg]/10** | **+[X]** |

   ### AI Query Coverage

   This content is now optimized to answer:
   - "What is [topic]?" ✅
   - "How does [topic] work?" ✅
   - "Why is [topic] important?" ✅
   - "[Topic] vs [alternative]" ✅
   - "Best [topic] for [use case]" ✅
   ```

5. **进行自我检查**

   优化完成后，对优化后的内容进行再次审核：

   ```markdown
    ### CORE-EEAT GEO Post-Optimization Check

    | ID | Standard | Status | Notes |
    |----|----------|--------|-------|
    | C02 | Direct Answer in first 150 words | ✅/⚠️/❌ | [notes] |
    | C04 | Key terms defined on first use | ✅/⚠️/❌ | [notes] |
    | C09 | Structured FAQ with Schema | ✅/⚠️/❌ | [notes] |
    | O02 | Summary Box / Key Takeaways | ✅/⚠️/❌ | [notes] |
    | O03 | Comparisons in tables | ✅/⚠️/❌ | [notes] |
    | O05 | JSON-LD Schema Markup | ✅/⚠️/❌ | [notes] |
    | O06 | Section chunking (3–5 sentences) | ✅/⚠️/❌ | [notes] |
    | R01 | ≥5 precise data points with units | ✅/⚠️/❌ | [notes] |
    | R02 | ≥1 citation per 500 words | ✅/⚠️/❌ | [notes] |
    | R04 | Claims backed by evidence | ✅/⚠️/❌ | [notes] |
    | R07 | Full entity names | ✅/⚠️/❌ | [notes] |
    | E01 | Original first-party data | ✅/⚠️/❌ | [notes] |
    | Exp10 | Limitations acknowledged | ✅/⚠️/❌ | [notes] |
    | Ept08 | Reasoning transparency | ✅/⚠️/❌ | [notes] |

    **Items Needing Attention**: [list any ⚠️/❌ items]

    _For full 80-item audit, use [content-quality-auditor](../../cross-cutting/content-quality-auditor/)_
    ```

## 验证要点

### 输入验证
- 已确定内容来源（URL、完整文本或内容草稿）
- 明确了目标AI查询词或主题
- （如优化现有内容）已评估当前的地理优化基础情况

### 输出验证
- 至少添加了3个清晰、易于引用的定义
- 事实密度有所提升，包含至少5个可验证的数据点
- 所有陈述都引用了权威来源
- 问答部分涵盖了用户最常查询的内容
- 地理优化后的评分比基准提高了至少50%
- 每个数据点的来源均明确标注（来自AI监控数据、用户提供的数据或估算值）

## 示例

**用户请求**：“优化这段关于电子邮件营销的内容：‘电子邮件营销是一种有效的客户沟通方式。它已经存在很长时间了，许多企业都在使用。’”

**优化结果：**

```markdown
## GEO-Optimized Version

**Email marketing** is a digital marketing strategy that uses email to promote 
products, build customer relationships, and drive conversions. According to 
the Data & Marketing Association, email marketing delivers an average ROI 
of $42 for every $1 invested, making it the highest-performing digital 
marketing channel.

### Key email marketing formats include:

1. **Newsletters**: Regular updates sharing company news, industry insights, 
   and valuable content to maintain subscriber engagement
2. **Promotional emails**: Time-sensitive offers, discounts, and product 
   announcements designed to drive immediate sales
3. **Transactional emails**: Order confirmations, shipping updates, and 
   account notifications with 8x higher open rates than marketing emails
4. **Automated sequences**: Pre-scheduled email series triggered by user 
   actions, such as welcome series or abandoned cart reminders

> **Key statistic**: 81% of small businesses rely on email as their primary 
> customer acquisition channel (Emarsys, 2024).

---

### Changes Made:

Changes: added clear definition, 2 stats with sources, structured list, DMA/Emarsys citations, 3 quotable facts. **GEO Score**: 1/10 → 8/10.
```

## 地理优化检查清单

> 详细检查清单请参阅 [references/geo-optimization-techniques.md](./references/geo-optimization-techniques.md)，其中包含了定义、易于引用的内容、权威性、结构以及技术要素等方面的检查项目。

## 成功技巧

1. **先回答问题**：将答案放在第一句
2. **具体明确**：模糊的内容不易被引用
3. **引用来源**：AI系统信任可验证的信息
4. **保持内容更新**：定期更新数据和事实
5. **匹配查询格式**：问题需要直接的答案
6. **增强权威性**：专家资质有助于提高被引用的可能性

## 参考资料

- [AI引用模式](./references/ai-citation-patterns.md)：了解Google AI、ChatGPT、Perplexity和Claude等系统如何选择和引用来源
- [易于引用的内容示例](./references/quotable-content-examples.md)：优化前后的内容对比示例

## 相关技能

- [seo-content-writer](../seo-content-writer/)：用于创建符合SEO要求的内容
- [schema-markup-generator](../schema-markup-generator/)：用于添加结构化数据
- [content-refresher](../../optimize/content-refresher/)：用于更新内容以确保其新鲜度
- [content-quality-auditor](../../cross-cutting/content-quality-auditor/)：进行全面的内容质量审核
- [serp-analysis](../../research/serp-analysis/)：用于分析AI推荐内容的模式