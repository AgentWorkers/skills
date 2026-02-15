---
name: seo-content-factory
description: 生成完全符合SEO优化标准的博客文章和稿件，这些文章需要经过关键词研究、竞争对手分析，并确保内容符合搜索引擎的排名规则（SERP）。您可以在创建SEO相关内容、博客文章或为客户提供的内容时使用这些方法。
argument-hint: "[keyword-or-topic] [word-count]"
allowed-tools: Read, Write, Grep, Glob, Bash, WebFetch, WebSearch
---

# SEO内容工厂

这是一个端到端的SEO内容生成流程：从确定目标关键词到生成可发布的文章，旨在帮助内容在搜索引擎中获得更好的排名。

## 使用方法

```
/seo-content-factory "best project management tools for freelancers" 2000
/seo-content-factory "how to start a dropshipping business"
/seo-content-factory batch keywords.txt
```

- `$ARGUMENTS[0]`：目标关键词或主题（如需批量处理，可输入“batch”）
- `$ARGUMENTS[1]`：文章的字数（默认为1,500字）

（批量模式下，需要提供一个文件，每行包含一个关键词）

## 内容生成流程

### 第1阶段：关键词分析

针对目标关键词 `$ARGUMENTS[0]`：

1. **搜索该关键词**，了解当前的搜索引擎结果页面（SERP）情况。
2. **识别以下信息**：
   - 用户的搜索意图（信息型、交易型、导航型、商业型）
   - 有助于提高排名的内容类型（列表文章、操作指南、对比文章、攻略、评论）
   - 前5名搜索结果的平均字数
   - 常见的子主题和相关问题
   - 相关关键词和长尾关键词

3. **生成关键词簇**：
   - 主关键词
   - 3-5个次要关键词
   - 5-10个长尾关键词变体
   - 3-5个相关问题（采用“人们也问”（People Also Ask）的格式）

### 第2阶段：竞争对手内容分析

分析目标关键词的前5名搜索结果：

1. **内容缺口**：这些结果中缺少哪些内容？这就是我们的机会。
2. **内容结构**：它们的结构是怎样的？（使用H2/H3标题）
3. **独特视角**：有哪些未被覆盖的视角？
4. **内容更新性**：这些结果是否过时？我们能否提供2026年的数据？
5. **可链接性**：这些内容有哪些可被其他网站链接的点？

### 第3阶段：内容架构设计

在开始写作之前，先设计好文章的结构：

```
Title: [Primary keyword + compelling modifier]
Meta Description: [150-160 chars, includes primary keyword, has CTA]
URL Slug: [primary-keyword-short-form]

H1: [Title]
  Introduction (100-150 words)
    - Hook with statistic or question
    - Promise what the reader will learn
    - Include primary keyword naturally

  H2: [Section based on search intent]
    H3: [Subsection]
    H3: [Subsection]

  H2: [Section covering competitor gap]
    H3: [Subsection]

  H2: [Unique angle section]

  H2: [FAQ section - from People Also Ask]
    H3: [Question 1]
    H3: [Question 2]
    H3: [Question 3]

  Conclusion (100-150 words)
    - Summarize key takeaways
    - Clear CTA
```

### 第4阶段：内容创作

遵循以下SEO内容规则进行写作：

**关键词使用**（必须遵守）：
- 主关键词出现在：标题、H1标题、前100个单词、1-2个H2标题、最后100个单词以及元描述中
- 关键词密度：1-2%（自然融入，切勿刻意堆砌）
- 次要关键词：每个使用1-2次，分散在文章各处
- 长尾关键词变体：自然地出现在正文中和H3标题中

**可读性**：
- 弗莱施-金凯德 readability等级：6-8（适合所有读者）
- 句子长度：平均不超过20个单词
- 段落长度：不超过3-4句话
- 大量使用项目符号和编号列表
- 如果主题合适，可以加入表格或对比内容
- 每200-300个单词使用一个H2标题来分隔段落

**提高互动性**：
- 以引人注目的开头（统计数据、问题或强调性陈述）开始
- 全文使用“你”和“你的”等代词，保持对话式语气
- 包含具体的数字和数据
- 提供可操作的结论或建议（而不仅仅是信息）
- 每个段落之间使用过渡语句，引导读者阅读下一部分

**体现E-E-A-T原则**（体验、专业性、权威性、可信度）：
- 使用第一人称表达（如“根据我的经验...”）
- 明确引用具体的工具、流程或方法
- 提供带有来源的统计数据
- 提出有深度的观点，而不仅仅是泛泛而谈的建议

### 第5阶段：页面内SEO元素

在撰写文章的同时生成以下内容：

```yaml
title_tag: "[Primary Keyword] - [Modifier] | [Brand]" (50-60 chars)
meta_description: "[Benefit statement with primary keyword and CTA]" (150-160 chars)
url_slug: "[primary-keyword]"
primary_keyword: "[keyword]"
secondary_keywords: ["kw1", "kw2", "kw3"]
word_count: [actual count]
reading_time: "[X] min read"
content_type: "[listicle|how-to|guide|comparison|review]"
search_intent: "[informational|transactional|commercial|navigational]"
```

**内部链接建议**：为文章生成3-5个推荐的内部链接锚文本及其目标主题
**外部链接建议**：引用2-3个权威来源
**图片建议**：为每张图片添加3-5个描述性文字，并包含关键词
**结构化数据标记**：使用JSON-LD格式添加适当的结构化数据（如Article、FAQ、HowTo）

### 第6阶段：输出格式

最终文章提供两种格式：

1. **纯Markdown格式**：适用于CMS系统（如Ghost、Hugo、Jekyll）
2. **适用于WordPress的HTML格式**：包含正确的标题标签、结构化数据标记，以及作为HTML注释的元描述

```html
<!-- SEO Meta
Title: [title tag]
Description: [meta description]
Slug: [url-slug]
Keywords: [primary], [secondary1], [secondary2]
-->

<article>
  <h1>...</h1>
  ...
</article>

<script type="application/ld+json">
{schema markup}
</script>
```

## 批量处理模式

当 `$ARGUMENTS[0]$ 为“batch”时，从 `$ARGUMENTS[1]$ 中读取关键词文件，并为每个关键词生成相应的文章：
1. 运行上述所有生成流程
2. 将每篇文章保存为 `output/[url-slug].md` 和 `output/[url-slug].html`
3. 生成一个索引文件 `output/batch-summary.md`，内容包括：
   - 所生成的所有文章
   - 每篇文章的主关键词和次要关键词
   - 每篇文章的字数
   - 建议的发布顺序（根据关键词的难度排序，从简单到复杂）
   - 文章之间的内部链接关系

## 质量检查

在交付前，请验证以下内容：
- 主关键词是否出现在标题、H1标题、前100个单词以及元描述中
- 关键词密度是否在1-2%之间（避免过度使用）
- 所有的H2/H3标题是否具有描述性（避免使用“Introduction”或“Conclusion”等通用标题）
- FAQ部分是否使用了用户实际搜索的常见问题
- 文章长度是否超过竞争对手的平均水平
- 每500个单词至少包含一个表格、列表或视觉元素
- 结构化数据标记是否为有效的JSON-LD格式
- 元描述长度是否在150-160个字符之间
- 标题标签长度是否在50-60个字符之间
- 每个段落都有实际意义，避免冗长的无意义内容