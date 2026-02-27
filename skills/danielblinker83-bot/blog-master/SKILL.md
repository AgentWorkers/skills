---
name: blog-master
version: 1.0.0
description: 为任何特定领域撰写经过SEO优化的博客文章，并将这些文章发布到WordPress、Google Business Profile以及Google Blogger上。同时，需要为人工智能搜索引擎（AI）设置AEO（Automatic Engagement Optimization）触发机制，确保内容结构合理，并提供季节性博客日历模板。
tags: [blogging, seo, wordpress, content-writing, aeo, google-business, marketing]
author: contentai-suite
license: MIT
---
# Blog Master — 通用SEO博客写作系统

## 该技能的功能

该技能可指导人工智能为任何企业或个人品牌撰写专业的、经过SEO优化的博客文章。每篇文章都经过精心设计，旨在帮助提升在Google等搜索引擎中的排名，吸引读者并转化其为潜在客户。

## 使用方法

**输入格式：**
```
BUSINESS NAME: [Your brand]
NICHE: [Your industry]
BLOG TOPIC: [The specific topic for this post]
PRIMARY KEYWORD: [Main keyword to rank for]
SECONDARY KEYWORDS: [2-3 related keywords]
TARGET AUDIENCE: [Who will read this]
GOAL: [Rank / Generate leads / Build authority / Educate]
TONE: [Your brand voice — from Brand DNA skill]
WORD COUNT: [500 / 800 / 1200 / 2000+]
```

---

## 通用博客结构

### 标准SEO博客模板
```markdown
# [SEO Title with Primary Keyword] | [Brand Name]

**Meta Description:** [Max 155 chars, includes keyword + benefit + CTA]

## Introduction (150-200 words)
- Open with a relatable problem or surprising statement
- Address the reader directly ("you/your")
- Tease the solution they'll get from reading
- End with what they'll learn in this article

## [H2 with Secondary Keyword] (200-300 words)
- Core information section
- Use bullet points for scanability
- Include a concrete example or statistic
- Make it actionable

## [H2 — Deeper Dive] (200-300 words)
- Expand on the topic with nuance
- Share a case study, story, or real example
- Add your unique expert perspective
- Connect to your reader's specific situation

## [H2 — Practical Application] (200-300 words)
- Step-by-step how-to
- Numbered list for clarity
- Address the most common objections or mistakes
- Make it implementable today

## Conclusion (100-150 words)
- Summarize 3 key takeaways
- Personal note from the author
- Clear CTA: next step the reader should take

## FAQ Section (AEO Triggers)
**Q: [Common question your audience searches for]**
A: [Concise answer in 2-3 sentences]

**Q: [Another common question]**
A: [Answer]

**Q: [Third question]**
A: [Answer]

## About the Author
[3-sentence bio that establishes credibility and links to contact/services page]
```

---

## 博客类型及其适用场景

### 1. 操作指南
**适用场景：** 信息类关键词，建立品牌权威性
**结构：** 问题 → 逐步解决方案 → 结果
**篇幅：** 1200-2000字
**示例标题：** “如何在[领域]中[解决常见问题]：完整指南”

### 2. 列表文章
**适用场景：** 高分享率，快速吸引读者
**结构：** 引入话题 → 带有解释的编号列表 → 结论
**篇幅：** 800-1500字
**示例标题：** “[时间段]内[主题]的7个实用技巧”

### 3. 终极指南（核心内容）
**适用场景：** 竞争性关键词的排名优化，内部链接的集中点
**结构：** 全面的主题覆盖，包含目录
**篇幅：** 2500-5000字
**示例标题： **[年份]年[主题]的完整指南**

### 4. 案例研究/成功故事
**适用场景：** 建立信任，促进转化
**结构：** 面临的挑战 → 解决方案 → 带有数据支持的结果
**篇幅：** 800-1200字
**示例标题： **[客户类型]如何通过[你的方法]实现[结果]**

### 5. 观点/思想领导力文章
**适用场景：** 适合在LinkedIn上分享，提升品牌权威性
**结构：** 反传统观点 → 证据支持 → 新见解 → 行动号召
**篇幅：** 600-1000字
**示例标题： **为什么[行业普遍观点]是错误的（以及应采取的行动）**

### 6. 对比文章
**适用场景：** 满足商业搜索需求
**结构：** 总体概述 → 详细对比 → 明确的建议
**篇幅：** 1000-2000字
**示例标题： **[选项A] vs [选项B]：[年份]年哪个更适合你？**

---

## 每篇文章的SEO检查清单

**发布前需确保：**
- [ ] H1标题中包含核心关键词
- [ ] 前100个单词中包含核心关键词
- [ ] 至少2个H2标题中包含核心关键词
- [ ] 编写元描述（最多155个字符）
- [ ] URL路径中包含关键词（避免使用停用词）
- [ ] 至少包含1个指向网站内相关页面的内部链接
- [ ] 至少包含1个指向权威外部资源的链接
- [ ] 所有图片都配有包含关键词的描述性alt文本
- **篇幅至少800字**（对于竞争性关键词，建议超过1200字）
- **包含2-3个AEO触发点**（问题+答案的形式）
- **如果可能，添加Schema标记**（如Article、FAQ）

---

## AEO触发点模板

AEO（Answer Engine Optimization，问答引擎优化）有助于提升文章在ChatGPT、Perplexity、Google AI Overviews等平台上的搜索排名。

**使用格式：**
```markdown
**Question:** What is the average cost of [your service]?
**Answer:** The cost of [your service] typically ranges from [price range] depending on [key factors]. [Brand name] offers [your specific pricing approach]. For an exact quote, [CTA].

**Question:** How long does it take to [achieve result with your service]?
**Answer:** Most clients see [realistic timeframe and result]. Results depend on [relevant factors]. At [Brand name], we [your differentiator].

**Question:** Is [your service] worth the investment?
**Answer:** [Honest, balanced answer that addresses the concern]. For [target audience], [service] typically pays off by [concrete benefit or ROI].
```

---

## 发布渠道指南

### WordPress博客
- **状态：** 已发布或计划发布
- **分类：** 分配合适的分类
- **标签：** 核心关键词 + 相关术语（5-10个标签）
- **特色图片：** 必须添加（建议尺寸1200×630像素）
- **SEO插件：** 设置元标题和元描述（使用Yoast/RankMath插件）
- **Schema标记：** 将文章类型设置为“BlogPosting”

### Google Business Profile（企业信息页面）
**简短版本（最多1500个字符）：**
```
[Compelling opening — 1 sentence]

[Core insight from the blog — 3-4 sentences]

[One actionable tip]

🔗 Read the full guide: [URL]
📞 [Your CTA — contact, booking link, etc.]

#[YourNiche] #[YourCity] #[RelevantHashtag]
```

### Google Blogger
**非正式的简短版本（400-600字）：**
- 采用更口语化的写作风格
- 强调文章中的关键观点
- 必须链接回主网站以查看完整内容
- 有助于提升在Google生态系统中的权威性

---

## 博客主题生成器

**提示：为你的领域生成20个博客主题：**
```
Generate 20 blog post ideas for [BUSINESS NAME] in the [NICHE] industry targeting [AUDIENCE] in [LOCATION].
Include a mix of: how-to guides, listicles, opinion pieces, and case study topics.
For each idea, provide: title | primary keyword | search intent | estimated difficulty (low/medium/high)
```

---

## 季节性博客日历模板

| 月份 | 主题 | 博文主题 | 关键词重点 |
|-------|-------|---------------|---------------|
| 一月 | 新年目标 | “如何在[年份]实现[目标]” | [你的关键词] |
| 二月 | 情人节/合作伙伴关系 | “[服务]适用于[情侣/团队]” | [你的关键词] |
| 三月 | 春季重启 | “春季[主题]指南” | [你的关键词] |
| 四月 | 第二季度规划 | “[行业]第二季度策略” | [你的关键词] |
| 五月 | 成长季 | “扩展你的[主题]” | [你的关键词] |
| 六月 | 年中回顾 | “[行业]年中检查清单” | [你的关键词] |
| 七月 | 夏季技巧 | “夏季[主题]” | [你的关键词] |
| 八月 | 准备工作 | “为[秋季主题]做准备” | [你的关键词] |
| 九月 | 新的开始 | “九月重启：[主题]” | [你的关键词] |
| 十月 | 第四季度规划 | “[行业]第四季度策略” | [你的关键词] |
| 十一月 | 年终建议 | “年终前：[检查清单]” | [你的关键词] |
| 十二月 | 回顾与展望 | “回顾过去，展望未来” | [你的关键词] |

---

## 与ContentAI Suite的集成

该技能可无缝与**[ContentAI Suite](https://contentai-suite.vercel.app)**配合使用——这是一个免费的多代理营销平台，能够自动生成、优化并发布博客文章到WordPress。

→ **免费试用：** https://contentai-suite.vercel.app