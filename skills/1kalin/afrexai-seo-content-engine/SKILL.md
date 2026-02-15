---
name: afrexai-seo-content-engine
description: 这是一个专为AI代理设计的完整SEO内容创作系统。该系统能够通过自然对话的方式帮助用户研究关键词、分析竞争对手、撰写优化过的文章，并跟踪文章的排名情况。整个过程无需使用任何API。
metadata:
  openclaw:
    version: "1.0.0"
    author: "AfrexAI"
    license: "MIT"
    tags: ["seo", "content", "writing", "blog", "marketing", "articles", "keywords"]
    category: "marketing"
---

# SEO内容引擎

将您的人工智能代理转变为一个完整的SEO内容团队。从研究到规划、写作、优化再到发布——所有步骤都通过自然语言完成。

无需API，也无需订阅。只需利用网络搜索和结构化框架，就能实现智能的工作流程。

---

## 1. 关键词研究框架

### 关键词扩展
给定一个主题时，系统地对其进行扩展：

1. **核心关键词**：主要术语（例如：“项目管理软件”）
2. **长尾关键词变体**：添加修饰词——如“最佳”、“顶级”、“免费”、“适用于[目标受众]”、“对比”、“替代方案”、“如何使用”、“指南”等
3. **问题关键词**：如何/什么/为什么/何时/在哪里 + 核心关键词
4. **问题导向关键词**：该内容能解决什么问题？（例如：“团队错过截止日期”、“项目超期”
5. **对比关键词**：“[产品A] vs [产品B]”、“[产品]的替代品”

### 搜索意图分类
对每个关键词进行意图分类：

| 意图 | 信号词 | 内容类型 |
|--------|-------------|--------------|
| **信息型** | 如何使用、什么是、指南、教程、为什么 | 教程、解释性文章 |
| **商业型** | 最佳、顶级、评测、对比 | 列表文章、对比文章、评测 |
| **交易型** | 购买、价格、折扣、免费试用、下载 | 产品页面、登录页面 |
| **导航型** | [品牌名称]、登录、支持、文档 | 品牌页面（价值较低，可忽略） |

### 竞争分析（使用网络搜索）

对于每个目标关键词：

```
Step 1: Search the exact keyword
Step 2: Analyze top 5 results:
  - What type of content ranks? (listicle, guide, review)
  - What's the average word count? (check article length)
  - What subtopics do ALL top results cover? (table stakes)
  - What subtopics do NONE cover? (your opportunity)
  - Who wrote them? (big brand = harder, niche blog = beatable)
Step 3: Score opportunity:
  - Mostly forums/Reddit in top 5 = HIGH opportunity (no dedicated content)
  - All big brands (Forbes, HubSpot) = LOW opportunity (hard to outrank)
  - Mix of niche sites = MEDIUM opportunity (winnable with better content)
```

### 关键词优先级矩阵
为每个关键词打分（每个维度1-5分）：

| 维度 | 1（低） | 5（高） |
|-----------|---------|----------|
| **相关性** | 间接相关 | 核心主题 |
| **意图匹配** | 仅信息型 | 商业/交易型 |
| **竞争差距** | 所有大型品牌 | 论坛、内容匮乏 |
| **商业价值** | 无转化路径 | 与产品直接相关 |
| **内容可行性** | 需要专有数据 | 可以基于专业知识撰写 |

**优先级**：得分 ≥ 18 = 立即撰写。13-17 = 排队。< 13 = 忽略。

---

## 2. 内容规划

### 内容大纲模板
在撰写任何文章之前，先创建这个大纲：

```markdown
# Content Brief: [Title]

**Target keyword**: [primary keyword]
**Secondary keywords**: [3-5 related terms to weave in naturally]
**Search intent**: [informational/commercial/transactional]
**Target word count**: [based on competitor analysis]
**Content type**: [guide/listicle/comparison/review/case study]

## Audience
- Who is searching this? [persona]
- What do they already know? [beginner/intermediate/advanced]
- What do they want to DO after reading? [action]

## Must-Cover Subtopics (from competitor analysis)
1. [Topic all competitors cover — table stakes]
2. [Topic all competitors cover — table stakes]
3. ...

## Differentiation Angles (our edge)
1. [Topic NO competitor covers — our advantage]
2. [Fresh data/perspective they're missing]
3. [Practical template/tool they don't provide]

## Internal Links
- Link TO: [existing content on your site]
- Link FROM: [update these older articles to link to this one]

## CTA
- Primary: [what should the reader do?]
- Secondary: [email signup, related article, tool]
```

### 内容日历结构
将文章组织成不同的主题群组：

```
PILLAR PAGE: "Complete Guide to [Topic]" (3,000-5,000 words)
├── CLUSTER: "How to [Subtopic A]" (1,500-2,500 words)
├── CLUSTER: "Best [Subtopic B] for [Audience]" (2,000-3,000 words)
├── CLUSTER: "[Subtopic C] vs [Subtopic D]" (1,500-2,000 words)
├── CLUSTER: "[Subtopic E] Template + Examples" (1,000-1,500 words)
└── CLUSTER: "Common [Topic] Mistakes" (1,500-2,000 words)
```

每个主题群组中的文章都会链接到相应的主题支柱，而每个主题支柱又会链接到所有群组。这样可以建立主题权威性。

---

## 3. 写作框架

### 文章结构（HBCFC公式）
每篇文章都遵循以下结构：

#### H — 引入（前100字）
- 以一个具体的数据、问题或引人注目的陈述开头
- 避免使用通用的开头语（如“在当今快节奏的世界里...”）
- 说明读者将获得什么以及为什么这很重要
- 在第一段中自然地包含主要关键词

#### B — 问题阐述
- 承认读者的困扰或目标
- 表明你理解他们的处境
- 创造紧张感：“大多数关于X的建议都忽略了Y”
- 过渡到你的解决方案

#### C — 核心内容（占文章字数的80%）
- 使用H2标题来划分主要部分，H3标题来划分小节
- 每个H2标题都应该能够独立回答一个问题
- 至少包括：
  - **每个部分的一个数据点或统计信息**（查找最新数据）
  - **每个主要部分的一个实际示例或模板**
  - 每500字中有一个“实用技巧”提示
  - 使用项目符号列表来提高可读性（便于读者快速浏览）
- 关键词的自然分布：主要关键词出现在2-3个H2标题中，次要关键词出现在H3标题和正文中

#### F — 常见问题（FAQ）部分（5-7个问题）
- 从搜索结果中的“人们也问”部分提取问题
- 简洁回答（每个问题40-60字）
- 自然地包含主要/次要关键词
- 这个部分有助于在Google中生成丰富的FAQ片段

#### C — 结论 + 行动号召（最后150-200字）
- 总结3个关键要点
- 再次自然地提及主要关键词
- 明确的行动号召（仅一个行动号召，避免分散注意力）

### 写作规则
1. **句子多样性**：混合使用短句（5-8个词）、中等长度的句子（12-18个词）和长句（20-25个词）。避免连续使用三个长句。
2. **段落长度**：每段最多2-4句。强调时可以使用单句段落。
3. **主动语态**：使用“该工具分析数据”，而不是“数据被工具分析”。
4. **具体化 > 模糊化**：使用“转化率提高了34%”而不是“效果显著提升”。
5. **避免填充语**：删除“需要注意的是”、“为了”、“总之”等短语。
6. **朗读测试**：如果读出来听起来像机器人说话，就重写。

### 关键词整合（自然分布）

```
✅ DO:
- Primary keyword in title (H1)
- Primary keyword in first 100 words
- Primary keyword in 1-2 H2 headings
- Primary keyword in conclusion
- Secondary keywords scattered in body (1-2 each)
- Semantic variants throughout (synonyms, related phrases)

❌ DON'T:
- Use exact keyword more than 1x per 200 words
- Force keywords into headings where they sound unnatural
- Use the same keyword phrase 3x in one paragraph
- Stuff keywords in image alt text unnaturally
```

---

## 4. 页面SEO检查清单
在发布前对每篇文章执行以下检查：

### 标题标签（H1）
- 包含主要关键词（最好放在开头）
- 不超过60个字符（以免在搜索结果中被截断）
- 有吸引力——你会在搜索结果中点击它吗？
- 包含一个强有力的词汇（如“终极的”、“完整的”、“经过验证的”、“必不可少的”）
- 如果相关，包含年份（例如：“2026年最佳X工具”）

### 元描述
- 150-160个字符
- 包含主要关键词
- 包含好处或结果
- 包含行动号召（如“学习如何...”、“发现...”、“了解...”）
- 独特（不要与其他页面重复）

### URL路径
- 简短（3-5个词）
- 包含主要关键词
- 不使用停用词（如“the”、“and”等）
- 词与词之间使用连字符
- 例如：`/best-project-management-tools`

### 标题
- 只有一个H1标题
- 每个主要部分使用H2标题（每篇文章5-8个）
- H2标题下的小节使用H3标题
- 至少有两个H2标题包含主要或次要关键词
- 标题具有描述性（不要使用“第1部分”、“A节”等）

### 内容
- 至少1500个单词（对于竞争性关键词，建议2000字以上）
- 主要关键词自然出现4-8次
- 每个次要关键词出现1-3次
- 每500字至少有一个内部链接
- 至少2-3个外部链接指向权威来源
- 每300-500字添加一张图片（使用库存图片、图表或截图）
- 所有图片都有描述性alt文本

### 技术要求
- 定义Schema标记（至少包含文章类型）
- 超过2000字的文章需要提供目录
- 适应移动设备（避免使用过宽的表格，图片大小适中）
- 无损坏的链接

### Schema标记模板（文章）

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Title]",
  "description": "[Meta description]",
  "author": {
    "@type": "Person",
    "name": "[Author]"
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]",
  "publisher": {
    "@type": "Organization",
    "name": "[Site Name]"
  }
}
```

### FAQ Schema模板

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Question 1]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer 1]"
      }
    }
  ]
}
```

---

## 5. 内容类型 — 模板

### 模板A：“[X]的最佳选择”列表文章

```markdown
# Best [X] for [Y] in [Year]

[Hook: Stat about the problem or market size]
[Bridge: Why choosing the right X matters for Y]

## Quick Comparison Table
| Product | Best For | Price | Rating |
|---------|----------|-------|--------|

## 1. [Product Name] — Best Overall
### Why It Stands Out
### Key Features
### Pricing
### Who It's For
### Downsides

[Repeat for 7-10 products]

## How We Evaluated
[Methodology — builds trust]

## FAQ
## Final Verdict
```

### 模板B：“如何[X]”指南

```markdown
# How to [X]: Step-by-Step Guide ([Year])

[Hook: What you'll achieve by the end]
[Bridge: Common mistakes people make with X]

## What You'll Need
[Prerequisites, tools, time estimate]

## Step 1: [Action Verb + Outcome]
[Detailed instructions]
[Screenshot or example]
[Pro tip callout]

[Repeat for each step]

## Common Mistakes to Avoid
## Advanced Tips
## FAQ
## Next Steps
```

### 模板C：“[X] vs [Y]”对比文章

```markdown
# [X] vs [Y]: Which Is Better in [Year]?

[Hook: The core difference in one sentence]
[Bridge: When to choose X vs Y]

## Quick Verdict
[TL;DR comparison — who should choose what]

## Overview Comparison
| Feature | X | Y |
|---------|---|---|

## [Feature Category 1]: [X] vs [Y]
### How [X] Handles It
### How [Y] Handles It
### Winner: [X/Y] because [reason]

[Repeat for 5-7 feature categories]

## Pricing Breakdown
## Who Should Choose [X]
## Who Should Choose [Y]
## FAQ
## Our Recommendation
```

### 模板D：终极指南（主题支柱页面）

```markdown
# The Ultimate Guide to [Topic] ([Year])

[Hook: Why this topic matters now]
[Bridge: What this guide covers that others don't]

## Table of Contents

## Chapter 1: [Foundational Concept]
[Explain the basics — link to cluster article for deep dive]

## Chapter 2: [Core Strategy]
[Main approach — link to how-to cluster]

## Chapter 3: [Tools & Resources]
[Curated list — link to comparison cluster]

## Chapter 4: [Advanced Techniques]
[Expert-level tactics]

## Chapter 5: [Common Mistakes]
[What to avoid — link to mistakes cluster]

## Chapter 6: [Case Studies / Examples]
[Real-world applications]

## FAQ (10-15 questions for this one)
## Conclusion + What to Do Next
```

---

## 6. 内容优化工作流程

### 发布前的优化

```
1. READABILITY CHECK
   - Flesch Reading Ease: aim for 60-70 (8th-9th grade level)
   - No paragraphs over 4 sentences
   - No sentences over 25 words without a break
   - Subheading every 250-300 words

2. KEYWORD DENSITY CHECK
   - Primary keyword: 0.5-1.5% density (not higher)
   - If over 1.5%: replace some instances with synonyms
   - If under 0.5%: add naturally in body paragraphs

3. LINK AUDIT
   - Internal links: 3-5 per 1,500 words minimum
   - External links: 2-3 to authoritative sources (.gov, .edu, industry leaders)
   - No orphan pages (every article linked from at least one other)

4. MEDIA CHECK
   - Featured image with alt text
   - In-content images/diagrams every 300-500 words
   - Tables where data comparison exists
   - Callout boxes for key takeaways

5. CTA CHECK
   - One primary CTA (not competing CTAs)
   - CTA appears at end and optionally mid-article
   - CTA is specific ("Download the template" not "Learn more")
```

### 发布后的操作

```
1. INDEX REQUEST
   - Submit URL to Google Search Console
   - Share on social media (generates initial signals)

2. INTERNAL LINKING UPDATE
   - Find 3-5 existing articles related to this topic
   - Add contextual links from those articles to this new one
   - This distributes link equity and helps discovery

3. MONITOR (Week 1-4)
   - Track ranking position for target keyword
   - Monitor organic impressions in Search Console
   - Check bounce rate and time on page

4. UPDATE CYCLE
   - Refresh content every 6-12 months
   - Update stats, add new sections, improve based on search performance
   - Articles that rank page 2 (positions 11-20) = highest ROI to update
```

---

## 7. 内容评分标准
在发布前对每篇文章进行评分（目标分数为85分以上）：

| 标准 | 分数 | 评分方法 |
|----------|--------|-------------|
| **关键词优化** | 15分 | 标题 + H2标题 + 关键词的自然分布 |
| **内容深度** | 20分 | 覆盖所有竞争对手涵盖的子主题，并提供独特视角 |
| **可读性** | 15分 | 段落简短、句子多样、易于阅读 |
| **实用性** | 15分 | 使用模板、示例和可操作的步骤（而不仅仅是理论） |
| **结构** | 10分 | H2/H3标题层次清晰、逻辑流畅、长篇文章有目录 |
| **内部链接** | 5分 | 3个以上与内容相关的内部链接 |
| **外部链接** | 5分 | 2个以上权威外部参考链接 |
| **媒体元素** | 5分 | 包含图片、表格或图表 |
| **元标签** | 5分 | 标题不超过60个字符，描述不超过150个字符，两者都包含关键词 |
| **行动号召的清晰度** | 5分 | 单一明确的行动号召 |
| **总分** | 100分 |

**评分指南**：
- 90-100分：立即发布——具有很强的排名潜力
- 80-89分：发布后进行少量修改
- 70-79分：需要修改——可能缺乏深度或优化
- 低于70分：需要重写——存在重大问题

---

## 8. SEO代理命令
使用自然语言触发这些工作流程：

| 命令 | 功能 |
|---------|-------------|
| “研究[主题]的关键词” | 完整的关键词扩展和优先级矩阵 |
| “分析[关键词]的竞争对手” | 分析排名前5的SERP结果及内容差距 |
| “为[关键词]创建内容大纲” | 使用上述模板创建完整的大纲 |
| “撰写关于[主题]的文章” | 使用HBCFC框架和页面SEO检查清单撰写完整文章 |
| “优化这篇文章” | 对现有内容执行优化流程 |
| “评估这篇文章” | 应用100分评分标准 |
| “为[主题]规划内容群组” | 创建主题支柱及5-6篇内部链接的文章 |
| “为这篇文章生成Schema标记” | 为文章添加Schema标记和FAQ JSON-LD |
| “创建[列表文章/指南/对比文章]” | 使用相应的模板 |
| “审核我的SEO” | 根据提供的内容执行全面的页面SEO检查 |

---

## 9. 高级技巧

### 语义SEO（主题权威性）
不要只针对一个关键词——要掌握整个主题：
1. 通过关键词研究映射你所在领域的所有子主题
2. 为每个子主题创建内容（采用内容群组模型）
3. 使用上下文相关的锚文本相互链接
4. Google更倾向于全面覆盖某个主题的网站

### 优化特色片段
要获得特色片段（排名第一）：
- **段落片段**：在直接对应问题的H2标题下用40-60个字回答问题
- **列表片段**：使用有序/无序列表，并加上明确的H2标题
- **表格片段**：使用带有清晰标题的HTML表格
- 针对当前片段较弱或缺失的关键词进行优化

### 内容更新信号
Google更喜欢针对时效性强的查询提供新鲜内容：
- 在标题中包含当前年份（如果相关）
- 每年更新数据和统计信息
- 在文章中添加“最后更新：[日期]”
- 在重大更新后重新发布文章并更新日期

### E-E-A-T信号（经验、专业性、权威性、可信度）
- **经验**：提供第一手示例（如“当我测试这个时...”）
- **专业性**：引用具体数据，说明方法论
- **权威性**：链接到权威来源，并被其他来源引用
- **可信度**：提供作者简介、关于页面、联系方式、HTTPS协议和隐私政策

---

*由[AfrexAI](https://afrexai-cto.github.io/context-packs/)构建——为企业提供AI代理基础设施。*