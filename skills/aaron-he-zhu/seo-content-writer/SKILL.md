---
name: seo-content-writer
description: 生成高质量、经过SEO优化的内容，以在搜索引擎中获得良好的排名。通过应用页面内的SEO最佳实践、关键词优化以及内容结构来提升内容的可见性和用户参与度。
geo-relevance: "medium"
---

# SEO内容撰写专家

该技能专注于创作经过搜索引擎优化的内容，既能确保在搜索结果中获得良好的排名，又能为读者提供实质性的价值。它运用了经过验证的SEO写作技巧、恰当的关键词整合方法以及最佳的内容结构。

## 适用场景

- 撰写针对特定关键词的博客文章  
- 创建针对搜索优化的 landing 页面  
- 为专题系列撰写核心内容（pillar content）  
- 为电子商务平台编写产品描述  
- 为本地SEO策略创建服务页面  
- 制作操作指南和教程  
- 撰写对比分析和评论文章  

## 技能核心功能  

1. **关键词整合**：自然地融入目标关键词及相关关键词  
2. **结构优化**：创建易于阅读、条理清晰的内容  
3. **标题与元信息生成**：撰写引人注目、点击率高的标题  
4. **标题层级优化**：合理使用H1-H6标题层级  
5. **内部链接建议**：提供相关的内部链接建议  
6. **可读性提升**：确保内容易于理解且具有吸引力  
7. **特色片段优化**：优化内容以适应搜索引擎结果页（SERP）的展示  

## 使用方法  

### 基础内容创作  

```
Write an SEO-optimized article about [topic] targeting the keyword [keyword]
```  
```
Create a blog post for [topic] with these keywords: [keyword list]
```  

### 特殊需求下的应用  

```
Write a 2,000-word guide about [topic] targeting [keyword],
include FAQ section for featured snippets
```  

### 内容撰写流程  

```
Here's my content brief: [brief]. Write SEO-optimized content following this outline.
```  

## 数据来源  

> 请参阅 [CONNECTORS.md](../../CONNECTORS.md) 以获取工具类别的相关信息。  

**当连接到 ~~SEO工具 + ~~搜索控制台时：**  
自动获取关键词指标（搜索量、难度、点击成本CPC）、竞争对手内容分析（排名靠前的页面、内容长度、常见主题）、SERP展示特征（特色片段、PAA问题）以及关键词机会（相关关键词、基于问题的查询）。  

**仅使用手动数据时：**  
要求用户提供：  
1. 目标主要关键词及3-5个次要关键词  
2. 目标受众和搜索意图（信息型/商业型/交易型）  
3. 目标字数及期望的语气  
4. 可参考的竞争对手URL或内容示例  

根据提供的数据执行完整的工作流程。在输出结果中明确标注哪些数据来自自动化收集，哪些来自用户提供。  

## 指导步骤  

当用户请求SEO内容时：  

1. **收集需求**  
   确认或询问以下信息：  
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
   在写作前进行必要的研究：  
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

6. **使用SEO标题层级构建内容结构**  
   ```markdown
   ### Content Structure
   
   **H1**: [Primary keyword in H1 - only one per page]
   
   **Introduction** (100-150 words)
   - Hook reader in first sentence
   - State what they'll learn
   - Include primary keyword in first 100 words
   
   **H2**: [Secondary keyword or question]
   [Content section]
   
   **H2**: [Secondary keyword or question]
   
   **H3**: [Sub-topic]
   [Content]
   
   **H3**: [Sub-topic]
   [Content]
   
   **H2**: [Secondary keyword or question]
   [Content]
   
   **H2**: Frequently Asked Questions
   [FAQ section for PAA optimization]
   
   **Conclusion**
   - Summarize key points
   - Include primary keyword
   - Clear call-to-action
   ```  

7. **应用页面内SEO最佳实践**  
   ```markdown
   ### On-Page SEO Checklist
   
   **Keyword Placement**:
   - [ ] Primary keyword in title
   - [ ] Primary keyword in H1
   - [ ] Primary keyword in first 100 words
   - [ ] Primary keyword in at least one H2
   - [ ] Primary keyword in conclusion
   - [ ] Primary keyword in meta description
   - [ ] Secondary keywords in H2s/H3s
   - [ ] Related terms throughout body
   
   **Content Quality**:
   - [ ] Comprehensive coverage of topic
   - [ ] Original insights or data
   - [ ] Actionable takeaways
   - [ ] Examples and illustrations
   - [ ] Expert quotes or citations (for E-E-A-T)
   
   **Readability**:
   - [ ] Paragraphs of 3-5 sentences (per CORE-EEAT O06 Section Chunking standard)
   - [ ] Varied sentence length
   - [ ] Bullet points and lists
   - [ ] Bold key phrases
   - [ ] Table of contents for long content
   
   **Technical**:
   - [ ] Internal links to relevant pages (2-5)
   - [ ] External links to authoritative sources (2-3)
   - [ ] Image alt text with keywords
   - [ ] URL slug includes keyword
   ```  

8. **撰写内容**  
   按照以下结构进行写作：  
   ```markdown
   # [H1 with Primary Keyword]
   
   [Hook sentence that grabs attention]
   
   [Problem statement or context - why this matters]
   
   [Promise - what the reader will learn/gain] [Include primary keyword naturally]
   
   [Brief overview of what's covered - can be bullet points for scanability]
   
   ## [H2 - First Main Section with Secondary Keyword]
   
   [Introduction to section - 1-2 sentences]
   
   [Main content with valuable information]
   
   [Examples, data, or evidence to support points]
   
   [Transition to next section]
   
   ### [H3 - Sub-section if needed]
   
   [Detailed content]
   
   [Key points in bullet format]:
   - Point 1
   - Point 2
   - Point 3
   
   ## [H2 - Second Main Section]
   
   [Continue with valuable content...]
   
   > **Pro Tip**: [Highlighted tip or key insight]
   
   | Column 1 | Column 2 | Column 3 |
   |----------|----------|----------|
   | Data | Data | Data |
   
   ## [H2 - Additional Sections as Needed]
   
   [Content...]
   
   ## Frequently Asked Questions
   
   ### [Question from PAA or common query]?
   
   [Direct, concise answer in 40-60 words for featured snippet opportunity]
   
   ### [Question 2]?
   
   [Answer]
   
   ### [Question 3]?
   
   [Answer]
   
   ## Conclusion
   
   [Summary of key points - include primary keyword]
   
   [Final thought or insight]
   
   [Clear call-to-action: what should reader do next?]
   ```  

9. **优化特色片段展示**  
   ```markdown
   ### Featured Snippet Optimization
   
   **For Definition Snippets**:
   "[Term] is [clear, concise definition in 40-60 words]"
   
   **For List Snippets**:
   Create clear, numbered or bulleted lists under H2s
   
   **For Table Snippets**:
   Use comparison tables with clear headers
   
   **For How-To Snippets**:
   Number each step clearly: "Step 1:", "Step 2:", etc.
   ```  

10. **添加内部/外部链接**  
   ```markdown
   ### Link Recommendations
   
   **Internal Links** (include 2-5):
   1. "[anchor text]" → [/your-page-url] (relevant because: [reason])
   2. "[anchor text]" → [/your-page-url] (relevant because: [reason])
   
   **External Links** (include 2-3 authoritative sources):
   1. "[anchor text]" → [authoritative-source.com] (supports: [claim])
   2. "[anchor text]" → [authoritative-source.com] (supports: [claim])
   ```  

11. **最终SEO审核**  
    ```markdown
    ### Content SEO Score

    | Factor | Status | Notes |
    |--------|--------|-------|
    | Title optimized | ✅/⚠️/❌ | [notes] |
    | Meta description | ✅/⚠️/❌ | [notes] |
    | H1 with keyword | ✅/⚠️/❌ | [notes] |
    | Keyword in first 100 words | ✅/⚠️/❌ | [notes] |
    | H2s optimized | ✅/⚠️/❌ | [notes] |
    | Internal links | ✅/⚠️/❌ | [notes] |
    | External links | ✅/⚠️/❌ | [notes] |
    | FAQ section | ✅/⚠️/❌ | [notes] |
    | Readability | ✅/⚠️/❌ | [notes] |
    | Word count | ✅/⚠️/❌ | [X] words |

    **Overall SEO Score**: [X]/10

    **Improvements to Consider**:
    1. [Suggestion]
    2. [Suggestion]
    ```  

12. **自我检查（CORE-EEAT标准）**  
    写作完成后，根据加载的CORE-EEAT标准对内容进行验证：  
    ```markdown
    ### CORE-EEAT Post-Write Check

    | ID | Standard | Status | Notes |
    |----|----------|--------|-------|
    | C01 | Intent Alignment: title = content | ✅/⚠️/❌ | [notes] |
    | C02 | Direct Answer in first 150 words | ✅/⚠️/❌ | [notes] |
    | C06 | Audience explicitly stated | ✅/⚠️/❌ | [notes] |
    | C10 | Conclusion answers opening question | ✅/⚠️/❌ | [notes] |
    | O01 | Heading hierarchy correct | ✅/⚠️/❌ | [notes] |
    | O02 | Summary/Key Takeaways present | ✅/⚠️/❌ | [notes] |
    | O06 | Paragraphs 3–5 sentences | ✅/⚠️/❌ | [notes] |
    | O09 | No filler; consistent terms | ✅/⚠️/❌ | [notes] |
    | R01 | ≥5 precise data points with units | ✅/⚠️/❌ | [notes] |
    | R02 | ≥1 citation per 500 words | ✅/⚠️/❌ | [notes] |
    | R04 | Claims backed by evidence | ✅/⚠️/❌ | [notes] |
    | R07 | Full entity names used | ✅/⚠️/❌ | [notes] |
    | C03 | ≥3 query variants covered | ✅/⚠️/❌ | [notes] |
    | O08 | Table of contents with jump links | ✅/⚠️/❌ | [notes] |
    | O10 | Images/videos captioned and informative | ✅/⚠️/❌ | [notes] |
    | E07 | Downloadable template/checklist included | ✅/⚠️/❌ | [notes] |

    **Items Needing Attention**: [list any ⚠️/❌ items]

    _For full 80-item audit, use [content-quality-auditor](../../cross-cutting/content-quality-auditor/)_
    ```  

## 验证要点  

### 输入验证  
- [ ] 主要关键词已确认且符合搜索意图  
- [ ] 指定了目标字数（实质性内容至少800字）  
- [ ] 明确了内容类型和目标受众  
- [ ] 已查看竞争对手的URL或确定了目标SERP展示特征  

### 输出验证  
- [ ] 主要关键词的密度控制在1-2%范围内（注：关键词密度仅供参考，现代搜索引擎更重视语义相关性和自然语言表达，而非严格的百分比要求。重点在于全面覆盖主题，并使用语义相关的变体，而非单纯追求密度）  
- [ ] 大纲中的所有部分均得到覆盖  
- [ ] 包含了2-5个相关内部链接  
- [ ] 包含了至少3个常见问题解答（FAQ）  
- [ ] 可读性适合目标受众  
- [ ] 明确标注了每个数据来源（SEO工具数据、用户提供的数据或估算值）  

## 示例  

**用户需求**：“撰写一篇针对小型企业的‘电子邮件营销最佳实践’的SEO优化文章”  

**输出结果**：  
```markdown
# Email Marketing Best Practices: A Complete Guide for Small Businesses

**Meta Description**: Discover proven email marketing best practices that help small businesses increase open rates, boost engagement, and drive sales. Start improving your campaigns today. (158 chars)

---

Want to know the secret behind small businesses that consistently turn subscribers into loyal customers? It's not luck—it's strategic email marketing.

Email marketing remains one of the most effective channels for small businesses, delivering an average ROI of $42 for every $1 spent. But with inboxes more crowded than ever, following email marketing best practices isn't optional—it's essential for survival.

In this guide, you'll learn:
- How to build a quality email list that converts
- Proven strategies to increase open and click rates
- Advanced personalization techniques that drive results
- Common mistakes that kill email performance

Let's dive into the strategies that will transform your email marketing.

## Why Email Marketing Matters for Small Businesses

Before we explore the best practices, let's understand why email deserves your attention.

Unlike social media where algorithms control who sees your content, email gives you direct access to your audience. You own your email list—no platform can take it away.

**Key email marketing statistics for small businesses**:
- 81% of SMBs rely on email as their primary customer acquisition channel
- Email subscribers are 3x more likely to share content on social media
- Personalized emails generate 6x higher transaction rates

## Building a High-Quality Email List

### Use Strategic Opt-in Incentives

The foundation of effective email marketing is a quality list. Here's how to grow yours:

**Lead magnets that convert**:
- Industry-specific templates
- Exclusive discounts or early access
- Free tools or calculators
- Educational email courses

> **Pro Tip**: The best lead magnets solve a specific, immediate problem for your target audience.

### Implement Double Opt-in

Double opt-in confirms subscriber intent and improves deliverability. Yes, you'll have fewer subscribers, but they'll be more engaged.

| Single Opt-in | Double Opt-in |
|---------------|---------------|
| More subscribers | Fewer subscribers |
| Higher bounce rates | Lower bounce rates |
| Lower engagement | Higher engagement |
| Spam risk | Better deliverability |

## Crafting Emails That Get Opened

### Write Compelling Subject Lines

Your subject line determines whether emails get opened or ignored.

**Subject line best practices**:
1. Keep it under 50 characters
2. Create urgency without being spammy
3. Use numbers and specifics
4. Personalize when possible
5. A/B test consistently

### Optimize Preview Text

The preview text (preheader) is your second chance to convince someone to open. Use it to expand on your subject line, not repeat it.

## Personalization Strategies That Work

Generic emails perform poorly. Here's how to personalize effectively:

### Segment Your Email List

Divide your list based on:
- Purchase history
- Engagement level
- Demographics
- Interests or preferences
- Customer lifecycle stage

### Use Dynamic Content

Send the same email but show different content blocks based on subscriber data.

## Frequently Asked Questions

### How often should small businesses send marketing emails?

For most small businesses, sending 1-2 emails per week strikes the right balance. This keeps you top-of-mind without overwhelming subscribers. Monitor your unsubscribe rates—if they spike after increasing frequency, scale back.

### What is a good email open rate for small businesses?

A good email open rate for small businesses is 20-25%. However, this varies by industry. E-commerce averages 15-20%, while B2B services often see 25-30%. Focus on improving your own benchmarks rather than industry averages.

### Should I buy email lists to grow faster?

Never buy email lists. Purchased lists violate GDPR and CAN-SPAM regulations, damage your sender reputation, and result in poor engagement. Organic list growth, while slower, produces much better results.

## Conclusion

Implementing these email marketing best practices will help your small business build stronger customer relationships and drive consistent revenue. Remember: quality always beats quantity in email marketing.

Start with one improvement today. Whether it's segmenting your list, testing subject lines, or cleaning inactive subscribers, small changes compound into significant results.

**Ready to level up your email marketing?** Download our free Email Marketing Checklist to ensure every campaign you send follows these best practices.

---

*Further reading: [Internal link: "How to Write Email Copy That Converts"]*

*Sources: [Litmus Email Marketing Statistics](https://litmus.com), [Campaign Monitor Email Benchmarks](https://campaignmonitor.com)*
```  

## 内容类型模板  

- **操作指南**  
```
Write a how-to guide for [task] targeting [keyword]
```  
- **对比文章**  
```
Write a comparison article: [Option A] vs [Option B] for [keyword]
```  
- **列表文章**  
```
Write a list post: "X Best [Items] for [Audience/Purpose]" targeting [keyword]
```  
- **终极指南**  
```
Write an ultimate guide about [topic] (3,000+ words) targeting [keyword]
```  

## 成功技巧  

1. **匹配搜索意图**：信息型查询需要的是指导性内容，而非销售页面  
2. **前置关键信息**：在文章开头提供关键信息，便于读者快速获取有用信息  
3. **使用数据和示例**：具体数据比通用表述更有效  
4. **以用户为中心写作**：SEO优化应自然流畅  
5. **添加视觉元素**：用图片、表格、列表等方式丰富文本  
6. **定期更新**：新鲜的内容能向搜索引擎传递积极信号  

## 参考资料  

- [标题公式](./references/title-formulas.md)：经过验证的标题编写公式、关键词使用技巧、点击率提升方法  
- [内容结构模板](./references/content-structure-templates.md)：适用于博客文章、对比分析、列表文章、操作指南、专题页面的模板  

## 相关技能  

- [关键词研究](../../research/keyword-research/)：寻找目标关键词  
- [地理内容优化器](../geo-content-optimizer/)：优化内容以提升AI引用效果  
- [元标签优化器](../meta-tags-optimizer/)：生成吸引人的元标签  
- [页面内SEO审核工具](../../optimize/on-page-seo-auditor/)：审核页面内的SEO元素  
- [内部链接生成工具](../../optimize/internal-linking-optimizer/)：在写作过程中添加内部链接  
- [内容更新工具](../../optimize/content-refresher/)：更新现有内容  
- [内容质量审核工具](../../cross-cutting/content-quality-auditor/)：进行全面的质量审核  
- [内容绩效追踪工具](../../cross-cutting/memory-management/)：长期跟踪内容表现  
- [内容需求分析工具](../../research/content-gap-analysis/)：识别可创作的新内容主题  
- [结构化数据生成工具](../schema-markup-generator/)：为已发布的内容添加结构化数据