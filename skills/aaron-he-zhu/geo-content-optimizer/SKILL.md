---
name: geo-content-optimizer
description: '**使用说明：**  
当用户请求“针对AI进行优化”、“让内容被ChatGPT引用”、“实现AI优化”、“让内容出现在AI生成的答案中”、“进行GEO优化”或“让内容被AI系统引用”时，请使用此工具。该工具可优化内容以适应生成式引擎（Generative Engine Optimization, GEO）的要求，从而提高内容被ChatGPT、Claude、Perplexity和Google AI Overviews等AI系统引用的几率。同时，该工具还能确保内容在保持SEO价值的同时具备更好的AI友好性。如需针对SEO的写作服务，请参阅`seo-content-writer`；如需提升实体和品牌的曝光度，请参阅`entity-optimizer`。'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "high"
  tags:
    - geo
    - ai optimization
    - ai citations
    - chatgpt
    - perplexity
    - google ai overviews
    - generative engine optimization
    - llm optimization
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

> **[SEO与地理优化技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与地理优化技能 · 全部技能的安装方式：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容编写器](../seo-content-writer/) · **地理内容优化器** · [元标签优化器](../meta-tags-optimizer/) · [结构化标记生成器](../schema-markup-generator/)

**优化** · [页面SEO审核器](../../optimize/on-page-seo-auditor/) · [技术SEO检查器](../../optimize/technical-seo-checker/) · [内部链接优化器](../../optimize/internal-linking-optimizer/) · [内容更新工具](../../optimize/content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告工具](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)

**跨领域工具** · [内容质量审核器](../../cross-cutting/content-quality-auditor/) · [域名权威性审核器](../../cross-cutting/domain-authority-auditor/) · [实体优化器](../../cross-cutting/entity-optimizer/) · [内存管理工具](../../cross-cutting/memory-management/)

</details>

该工具用于优化内容，使其更易于被AI系统引用。随着AI系统越来越多地直接回答用户查询，获得这些系统的引用对于提升内容可见性至关重要。

## 适用场景

- 优化现有内容以增加被AI引用的机会
- 创建同时符合SEO和地理优化要求的新内容
- 提高内容在AI推荐结果中的展示几率
- 使内容更易于被AI系统引用
- 添加AI系统信任的权威性信号
- 优化内容结构，便于AI理解
- 在以AI为主导的搜索环境中提升内容可见性

## 功能介绍

1. **引用优化**：提高内容被AI引用的可能性
2. **结构优化**：使内容更易于AI理解
3. **权威性建设**：添加AI系统信任的信号
4. **事实准确性提升**：提高内容的准确性和可验证性
5. **引用生成**：创建易于记忆、可被引用的表述
6. **来源标注**：添加AI可验证的引用信息
7. **地理评分**：评估内容的AI友好度

## 使用方法

### 优化现有内容

```
Optimize this content for GEO/AI citations: [content or URL]
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
自动获取AI引用模式（哪些内容被ChatGPT、Claude、Perplexity等AI系统引用）、当前的AI可见性评分、竞争对手的引用频率以及内容在AI推荐结果中的展示情况。

**仅使用手动数据时：**
请用户提供以下信息：
1. 需要AI引用的目标查询词
2. 当前内容的URL或完整文本内容
3. 竞争对手被AI引用的具体实例

根据提供的数据执行完整的工作流程。在输出中明确标注哪些数据来自自动化收集，哪些来自用户提供。

## 使用说明

当用户请求进行地理优化时，请按照以下步骤操作：

1. **加载CORE-EEAT地理优先优化目标**
   在优化之前，从 [CORE-EEAT基准](../../references/core-eeat-benchmark.md) 中加载与地理优化相关的关键信息：
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

2. **了解地理优化的基本原理**

   ```markdown
   ### How AI Systems Select Content to Cite
   
   AI systems prioritize content that is:
   
   **Authoritative**
   - From recognized experts or trusted sources
   - Contains proper citations and references
   - Shows expertise signals (author credentials, original research)
   
   **Accurate**
   - Factually correct and verifiable
   - Up-to-date information
   - Consistent with consensus knowledge
   
   **Clear**
   - Well-structured and organized
   - Contains clear definitions and explanations
   - Uses unambiguous language
   
   **Quotable**
   - Has standalone statements that answer questions
   - Contains specific facts, statistics, and data
   - Includes memorable, concise explanations
   ```

3. **分析现有内容**

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

4. **优化内容结构**
   AI系统偏好清晰、易于引用的定义：
   ```markdown
   ### Definition Optimization
   
   **Before** (Weak for GEO):
   > SEO is really important for businesses and involves various 
   > techniques to improve visibility online through search engines.
   
   **After** (Strong for GEO):
   > **Search Engine Optimization (SEO)** is the practice of optimizing 
   > websites and content to rank higher in search engine results pages 
   > (SERPs), increasing organic traffic and visibility.
   
   **Definition Template**:
   "[Term] is [clear category/classification] that [primary function/purpose], 
   [key characteristic or benefit]."
   
   **Checklist for GEO-Optimized Definitions**:
   - [ ] Starts with the term being defined
   - [ ] Provides clear category (what type of thing it is)
   - [ ] Explains primary function or purpose
   - [ ] Uses precise, unambiguous language
   - [ ] Can stand alone as a complete answer
   - [ ] Is 25-50 words for optimal citation length
   ```

5. **创建易于引用的表述**

   ```markdown
   ### Quotable Statement Optimization
   
   AI systems cite specific, standalone statements. Transform vague 
   content into quotable facts.
   
   **Weak (Not quotable)**:
   > Email marketing is pretty effective and lots of companies use it.
   
   **Strong (Quotable)**:
   > Email marketing delivers an average ROI of $42 for every $1 spent, 
   > making it one of the highest-performing digital marketing channels.
   
   **Types of Quotable Statements**:
   
   1. **Statistics**
      - Include specific numbers
      - Cite the source
      - Add context (timeframe, comparison)
      
      Example: "According to [Source], [specific statistic] as of [date]."
   
   2. **Facts**
      - Verifiable information
      - Unambiguous language
      - Authoritative source
      
      Example: "[Subject] was [fact], according to [authoritative source]."
   
   3. **Definitions** (covered above)
   
   4. **Comparisons**
      - Clear comparison structure
      - Specific differentiators
      
      Example: "Unlike [A], [B] [specific difference], which means [implication]."
   
   5. **How-to Steps**
      - Numbered, clear steps
      - Action-oriented language
      
      Example: "To [achieve goal], [step 1], then [step 2], and finally [step 3]."
   ```

6. **添加权威性信号**

   ```markdown
   ### Authority Signal Enhancement
   
   **Expert Attribution**
   
   Add expert quotes and credentials:
   
   > "AI will transform how we search for information," says Dr. Jane Smith, 
   > AI Research Director at Stanford University.
   
   **Source Citations**
   
   Properly cite sources that AI can verify:
   
   Before:
   > Studies show that most people prefer video content.
   
   After:
   > According to Wyzowl's 2024 Video Marketing Statistics report, 
   > 91% of consumers want to see more online video content from brands.
   
   **Authority Elements to Add**:
   - [ ] Author byline with credentials
   - [ ] Expert quotes with attribution
   - [ ] Citations to peer-reviewed research
   - [ ] References to recognized authorities
   - [ ] Original data or research
   - [ ] Case studies with named companies
   - [ ] Industry statistics with sources
   ```

7. **优化内容结构**
   ```html
   <h2>[主题]是什么？</h2>
   <p>[40-60字的直接回答]</p>
   
   <h2>[主题]是如何运作的？</h2>
   <p>[如有必要，提供详细的步骤说明]</p>
   
   <h2>[主题]为什么重要？</h2>
   <p>[提供具体理由及证据]</p>
   ```
   
   **Comparison Tables**
   
   For comparison queries, use clear tables:
   
   | Feature | Option A | Option B |
   |---------|----------|----------|
   | [Feature 1] | [Specific value] | [Specific value] |
   | [Feature 2] | [Specific value] | [Specific value] |
   | **Best for** | [Use case] | [Use case] |
   
   **Numbered Lists**
   
   For process or list queries:
   
   1. **Step 1: [Action]** - [Brief explanation]
   2. **Step 2: [Action]** - [Brief explanation]
   3. **Step 3: [Action]** - [Brief explanation]
   
   **Definition Boxes**
   
   Highlight key definitions:
   
   > **Key Definition**: [Term] refers to [clear definition].
   ```

8. **提升内容的真实性**

   ```markdown
   ### Factual Density Improvement
   
   AI systems prefer fact-rich content over opinion-heavy content.
   
   **Content Transformation**:
   
   **Low factual density**:
   > Social media marketing is very popular nowadays. Many businesses 
   > use it and find it helpful for reaching customers.
   
   **High factual density**:
   > Social media marketing reaches 4.9 billion users globally (Statista, 2024). 
   > Businesses using social media marketing report 66% higher lead generation 
   > rates compared to non-users (HubSpot State of Marketing Report, 2024). 
   > The most effective platforms for B2B marketing are LinkedIn (96% usage), 
   > Twitter (82%), and Facebook (80%).
   
   **Factual Enhancement Checklist**:
   - [ ] Add specific statistics with sources
   - [ ] Include exact dates, numbers, percentages
   - [ ] Replace vague claims with verified facts
   - [ ] Add recent data (within last 2 years)
   - [ ] Include multiple data points per section
   - [ ] Cross-reference with authoritative sources
   ```

9. **实现FAQ结构化标记**
   ```json
   {
     "@context": "https://schema.org",
     "@type": "FAQPage",
     "mainEntity": [
       {
         "@type": "Question",
         "name": "[问题文本]",
         "acceptedAnswer": {
           "@type": "Answer",
           "text": "[答案文本]"
         }
       }
     ]
   }
   ```
   ```

10. **生成优化后的内容**

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

11. **进行自我检查**
   优化完成后，对优化结果进行再次审核：
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
- 提高了内容的真实性，包含至少5个可验证的数据点
- 所有陈述都引用了权威来源
- FAQ格式部分涵盖了用户最常查询的5个问题
- 地理优化后的评分比基准提高了至少50%
- 明确标注了每个数据点的来源（AI监控数据、用户提供的数据或估算值）

## 示例

**用户请求：**“优化这段关于‘电子邮件营销’的内容，使其更符合地理优化要求。”

**优化后的内容：**
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

| Element | Before | After |
|---------|--------|-------|
| Definition | None | Clear definition with category |
| Statistics | None | 2 specific stats with sources |
| Structure | Single paragraph | Structured list with headers |
| Authority | None | DMA and Emarsys citations |
| Quotable statements | 0 | 3 standalone facts |

**GEO Score**: Improved from 1/10 to 8/10
```

## 地理优化检查清单

使用此清单对任何内容进行优化：
```markdown
### GEO Readiness Checklist

**Definitions & Clarity**
- [ ] Key terms are clearly defined
- [ ] Definitions can stand alone as answers
- [ ] Language is precise and unambiguous

**Quotable Content**
- [ ] Specific statistics included
- [ ] Facts have source citations
- [ ] Memorable statements created

**Authority**
- [ ] Expert quotes or credentials present
- [ ] Authoritative sources cited
- [ ] Original data or research included

**Structure**
- [ ] Q&A format sections included
- [ ] Clear headings match common queries
- [ ] Comparison tables where relevant
- [ ] Numbered lists for processes

**Technical**
- [ ] FAQ schema markup added
- [ ] Content freshness indicated
- [ ] Sources are verifiable
```

## 成功技巧

1. **先回答问题**——将答案放在第一句
2. **具体说明**——模糊的内容难以被引用
3. **标注来源**——AI系统信任可验证的信息
4. **保持内容更新**——定期更新数据和事实
5. **匹配查询格式**——问题应得到直接的回答
6. **建立权威性**——专家资质能增加被引用的机会

## 参考资料

- [AI引用模式](./references/ai-citation-patterns.md) —— Google AI推荐系统、ChatGPT、Perplexity和Claude如何选择和引用来源
- [易于引用的内容示例](./references/quotable-content-examples.md) —— 优化前后内容对比示例

## 相关技能

- [SEO内容编写器](../seo-content-writer/) —— 创建符合SEO要求的内容
- [结构化标记生成器](../schema-markup-generator/) —— 添加结构化数据
- [关键词研究](../../research/keyword-research/) —— 确定地理优化所需的关键词
- [内容更新工具](../../optimize/content-refresher/) —— 更新内容以提高新鲜度
- [SERP分析](../../research/serp-analysis/) —— 分析AI推荐模式
- [内容质量审核器](../../cross-cutting/content-quality-auditor/) —— 全面80项的CORE-EEAT审核
- [域名权威性审核器](../../cross-cutting/domain-authority-auditor/) —— 域名层面的AI引用信号（补充页面层面的地理优化）