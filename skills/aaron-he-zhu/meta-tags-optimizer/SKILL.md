---
name: meta-tags-optimizer
description: '**使用场景：**  
当用户请求“优化标题标签”、“编写元描述”、“提高点击率（CTR）”、“设置Open Graph标签”、“生成社交媒体预览图”、“我的标题标签需要修改”、“点击率过低”或“元标签无法正常显示”时，可使用该工具。该工具负责创建并优化包括标题标签、元描述、Open Graph标签以及Twitter卡片在内的元数据，以提升点击率和社交媒体分享效果。如需进行更全面的页面内容审计，可参考`on-page-seo-auditor`；如需处理结构化数据标记，可参考`schema-markup-generator`。'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "low"
  tags:
    - seo
    - meta tags
    - title tag
    - meta description
    - open graph
    - twitter cards
    - ctr optimization
    - social sharing
  triggers:
    - "optimize title tag"
    - "write meta description"
    - "improve CTR"
    - "Open Graph tags"
    - "social media preview"
    - "title optimization"
    - "meta tags"
    - "my title tag needs work"
    - "low click-through rate"
    - "fix my meta tags"
    - "OG tags not showing"
---

# 元标签优化器

> **[SEO与地理定位技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与地理定位相关技能 · 全部技能安装方式：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容编写器](../seo-content-writer/) · [地理内容优化器](../geo-content-optimizer/) · **元标签优化器** · [Schema标记生成器](../schema-markup-generator/)

**优化** · [页面SEO审核器](../../optimize/on-page-seo-auditor/) · [技术SEO检查器](../../optimize/technical-seo-checker/) · [内部链接优化器](../../optimize/internal-linking-optimizer/) · [内容更新器](../../optimize/content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告器](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)

**跨领域** · [内容质量审核器](../../cross-cutting/content-quality-auditor/) · [域名权威性审核器](../../cross-cutting/domain-authority-auditor/) · [实体优化器](../../cross-cutting/entity-optimizer/) · [内存管理](../../cross-cutting/memory-management/)

</details>

该技能能够生成引人注目且经过优化的元标签，从而提高搜索结果中的点击率，并提升社交媒体的分享效果。它涵盖标题标签、元描述以及社交媒体元标签。

## 何时使用此技能

- 为新页面创建元标签
- 优化现有元标签以提高点击率（CTR）
- 为社交媒体分享准备页面
- 修复重复或缺失的元标签
- 对标题和描述进行A/B测试
- 针对特定的SERP特征进行优化
- 为不同类型的页面生成元标签

## 该技能的功能

1. **标题标签生成**：编写引人注目且包含关键词的标题
2. **元描述编写**：创建具有吸引力的描述
3. **Open Graph优化**：为社交媒体分享准备页面
4. **Twitter卡片设置**：优化Twitter特定的元标签
5. **CTR分析**：提供改进建议以提升点击率
6. **字符计数**：确保符合SERP显示要求
7. **A/B测试建议**：提供多种版本以供测试

## 使用方法

### 创建元标签

```
Create meta tags for a page about [topic] targeting [keyword]
```

```
Write title and meta description for this content: [content/URL]
```

### 优化现有标签

```
Improve these meta tags for better CTR: [current tags]
```

### 社交媒体标签

```
Create Open Graph and Twitter card tags for [page/URL]
```

## 数据来源

> 请参阅[CONNECTORS.md](../../CONNECTORS.md)以获取工具类别的相关信息。

**当连接到[搜索控制台] + [SEO工具]时：**
自动获取当前的元标签、按查询生成的CTR数据、竞争对手的标题/描述模式、SERP预览数据以及展示次数/点击量指标，以识别优化机会。

**仅使用手动数据时：**
要求用户提供：
1. 当前页面的标题和元描述（如需优化现有元标签）
2. 目标关键词及2-3个次要关键词
3. 页面URL和主要内容/价值主张
4. 竞争对手的URL或在SERP中表现良好的标题示例

使用提供的数据完成整个工作流程。请在输出中明确指出哪些指标来自自动化收集，哪些来自用户提供的数据。

## 使用说明

当用户请求元标签优化时：

1. **收集页面信息**

   ```markdown
   ### Page Analysis
   
   **Page URL**: [URL]
   **Page Type**: [blog/product/landing/service/homepage]
   **Primary Keyword**: [keyword]
   **Secondary Keywords**: [keywords]
   **Target Audience**: [audience]
   **Primary CTA**: [action you want users to take]
   **Unique Value Prop**: [what makes this page special]
   ```

2. **创建优化后的标题标签**

   ```markdown
   ### Title Tag Optimization
   
   **Requirements**:
   - Length: 50-60 characters (displays fully in SERP)
   - Include primary keyword (preferably near front)
   - Make it compelling and click-worthy
   - Match search intent
   - Include brand name if appropriate
   
   **Title Tag Formula Options**:
   
   1. **Keyword | Benefit | Brand**
      "[Primary Keyword]: [Benefit] | [Brand Name]"
      
   2. **Number + Keyword + Promise**
      "[Number] [Keyword] That [Promise/Result]"
      
   3. **How-to Format**
      "How to [Keyword]: [Benefit/Result]"
      
   4. **Question Format**
      "What is [Keyword]? [Brief Answer/Hook]"
      
   5. **Year + Keyword**
      "[Keyword] in [Year]: [Hook/Update]"
   
   **Generated Title Options**:
   
   | Option | Title | Length | Power Words | Keyword Position |
   |--------|-------|--------|-------------|------------------|
   | 1 | [Title] | [X] chars | [words] | [Front/Middle] |
   | 2 | [Title] | [X] chars | [words] | [Front/Middle] |
   | 3 | [Title] | [X] chars | [words] | [Front/Middle] |
   
   **Recommended**: Option [X]
   **Reasoning**: [Why this option is best]
   
   **Title Tag Code**:
   ```html
   <title>[选定的标题]</title>
   ```
   ```

3. **编写元描述**

   ```markdown
   ### Meta Description Optimization
   
   **Requirements**:
   - Length: 150-160 characters (displays fully in SERP)
   - Include primary keyword naturally
   - Include clear call-to-action
   - Match page content accurately
   - Create urgency or curiosity
   - Avoid duplicate descriptions
   
   **Meta Description Formula**:
   
   [What the page offers] + [Benefit to user] + [Call-to-action]
   
   **Power Elements to Include**:
   - Numbers and statistics
   - Current year
   - Emotional triggers
   - Action verbs
   - Unique value proposition
   
   **Generated Description Options**:
   
   | Option | Description | Length | CTA | Emotional Trigger |
   |--------|-------------|--------|-----|-------------------|
   | 1 | [Description] | [X] chars | [CTA] | [Trigger] |
   | 2 | [Description] | [X] chars | [CTA] | [Trigger] |
   | 3 | [Description] | [X] chars | [CTA] | [Trigger] |
   
   **Recommended**: Option [X]
   **Reasoning**: [Why this option is best]
   
   **Meta Description Code**:
   ```html
   <meta name="description" content="[选定的描述]">
   ```
   ```

4. **创建Open Graph标签**

   ```markdown
   ### Open Graph Tags (Facebook, LinkedIn, etc.)
   
   **Required OG Tags**:
   
   ```html
   <!-- 主要Open Graph标签 -->
   <meta property="og:type" content="[文章/网站/产品]">
   <meta property="og:url" content="[完整规范URL]">
   <meta property="og:title" content="[优化后的标题 - 最长60个字符]">
   <meta property="og:description" content="[优化后的描述 - 最长200个字符]">
   <meta property="og:image" content="[图片URL - 建议使用1200x630像素]">
   
   <!-- 可选但推荐 -->
   <meta property="og:site_name" content="[网站名称]">
   <meta property="og:locale" content="en_US">
   ```
   
   **OG Type Selection Guide**:
   
   | Page Type | og:type |
   |-----------|---------|
   | Blog post | article |
   | Homepage | website |
   | Product | product |
   | Video | video.other |
   | Profile | profile |
   
   **OG Title Considerations**:
   - Can be different from title tag
   - Optimize for social sharing context
   - More conversational tone acceptable
   - Up to 60 characters ideal
   
   **OG Description Considerations**:
   - Can be longer than meta description (up to 200 chars)
   - Focus on shareability
   - What would make someone click when shared?
   
   **OG Image Requirements**:
   - Recommended size: 1200x630 pixels
   - Minimum size: 600x315 pixels
   - Format: JPG or PNG
   - Keep text to less than 20% of image
   - Include branding subtly
   ```

5. **创建Twitter卡片标签**

   ```markdown
   ### Twitter Card Tags
   
   **Card Type Selection**:
   
   | Card Type | Best For | Image Size |
   |-----------|----------|------------|
   | summary | Articles, blogs | 144x144 min |
   | summary_large_image | Visual content | 300x157 min |
   | player | Video/audio | 640x360 min |
   | app | Mobile apps | 800x418 |
   
   **Twitter Card Code**:
   
   ```html
   <!-- Twitter卡片标签 -->
   <meta name="twitter:card" content="[摘要图片/摘要]">
   <meta name="twitter:site" content="@[你的Twitter账号]">
   <meta name="twitter:creator" content="@[作者Twitter账号]">
   <meta name="twitter:title" content="[标题 - 最长70个字符]">
   <meta name="twitter:description" content="[描述 - 最长200个字符]">
   <meta name="twitter:image" content="[图片URL]">
   <meta name="twitter:image:alt" content="图片描述（用于辅助访问）"]">
   ```
   
   **Twitter-Specific Considerations**:
   - Shorter titles work better (under 70 chars)
   - Include @mentions if relevant
   - Hashtag-relevant terms can help discovery
   - Test with Twitter Card Validator
   ```

6. **其他元标签**

   ```markdown
   ### Additional Recommended Meta Tags
   
   **Canonical URL** (Prevent duplicates):
   ```html
   <link rel="canonical" href="[首选URL]">
   ```
   
   **Robots Tag** (Indexing control):
   ```html
   <meta name="robots" content="index, follow">
   ```
   
   **Viewport** (Mobile optimization):
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1">
   ```
   
   **Author** (For articles):
   ```html
   <meta name="author" content="[作者名称]">
   ```
   
   **Language**:
   ```html
   <html lang="en">
   ```
   
   **Article-Specific** (For blog posts):
   ```html
   <meta property="article:published_time" content="[ISO 8601格式的日期]">
   <meta property="article:modified_time" content="[ISO 8601格式的日期]">
   <meta property="article:author" content="[作者URL]">
   <meta property="article:section" content="[类别]">
   <meta property="article:tag" content="[标签1]">
   ```
   ```

7. **生成完整的元标签块**

   ```markdown
   ## Complete Meta Tags
   
   Copy and paste this complete meta tag block:
   
   ```html
   <!-- 主要元标签 -->
   <title>[优化后的标题]</title>
   <meta name="title" content="[优化后的标题]">
   <meta name="description" content="[优化后的描述]">
   <link rel="canonical" href="[规范URL]">
   
   <!-- Open Graph / Facebook -->
   <meta property="og:type" content="[类型]">
   <meta property="og:url" content="[URL]">
   <meta property="og:title" content="[OG标题]">
   <meta property="og:description" content="[OG描述]">
   <meta property="og:image" content="[图片URL]">
   <meta property="og:site_name" content="[网站名称]">
   
   <!-- Twitter -->
   <meta name="twitter:card" content="摘要图片">
   <meta name="twitter:url" content="[URL]">
   <meta name="twitter:title" content="[Twitter标题]">
   <meta name="twitter:description" content="[Twitter描述]">
   <meta name="twitter:image" content="[图片URL]">
   <meta name="twitter:image:alt" content="图片描述（用于辅助访问）"]">
   ```
   ```

8. **CORE-EEAT一致性检查**

   验证元标签是否符合内容质量标准。参考：[CORE-EEAT基准](../../references/core-eeat-benchmark.md)

   ```markdown
   ### CORE-EEAT Meta Tag Alignment

   | Check | Status | Notes |
   |-------|--------|-------|
   | **C01 Intent Alignment**: Title promise matches actual content delivery | ✅/⚠️/❌ | [Does the title accurately represent what the page delivers?] |
   | **C02 Direct Answer**: Meta description reflects the core answer available in first 150 words | ✅/⚠️/❌ | [Does the description preview the direct answer?] |

   **If C01 fails**: Title is misleading — rewrite to match actual content.
   **If C02 fails**: Content may need restructuring to front-load the answer, or description should better reflect available content.
   ```

9. **提供CTR优化建议**

   ```markdown
   ## CTR Optimization Analysis

   ### Power Words Used
   - [Word 1] - Creates [emotion/action]
   - [Word 2] - Creates [emotion/action]

   ### CTR Boosting Elements

   | Element | Present | Impact |
   |---------|---------|--------|
   | Numbers | Yes/No | +20-30% CTR |
   | Current Year | Yes/No | +15-20% CTR |
   | Power Words | Yes/No | +10-15% CTR |
   | Question | Yes/No | +10-15% CTR |
   | Brackets | Yes/No | +10% CTR |

   ### A/B Test Suggestions

   Test these variations:

   **Version A** (Current):
   - Title: [Title]
   - Description: [Description]

   **Version B** (Test):
   - Title: [Alternative title]
   - Description: [Alternative description]
   - Hypothesis: [Why this might perform better]
   ```

## 验证要点

### 输入验证
- [ ] 确认目标关键词并与页面内容匹配
- [ ] 确定页面类型（博客/产品/着陆页/首页）
- [ ] 明确目标受众和搜索意图
- [ ] 清晰阐述独特价值主张

### 输出验证
- [ ] 标题长度为50-60个字符（在SERP中能完整显示）
- [ ] 元描述长度为150-160个字符
- [ ] 关键词同时出现在标题和描述中
- [ ] 指定了Open Graph图片（建议使用1200x630像素）
- [ ] 所有HTML语法均正确（无未闭合的引号或标签）
- [ ] 明确每个数据点的来源（来自搜索控制台的CTR数据、SEO工具的竞争数据、用户提供的数据或估算值）

## 示例

**用户**：“为一篇关于‘如何在[当前年份]开始播客’的博客文章创建元标签”

**输出**：

```markdown
## Meta Tags: How to Start a Podcast ([current year])

### Title Tag
```html
<title>如何在[当前年份]开始播客：完整的初学者指南</title>
```
**Length**: ~55 characters ✅
**Keyword**: "how to start a podcast" at front ✅
**Power Words**: "Complete", "Beginner's" ✅

### Meta Description
```html
<meta name="description" content="通过我们的分步指南学习如何在[当前年份]开始播客。涵盖设备、托管、录制以及发布第一集的内容。今天就开始播客吧！">
```
**Length**: ~163 characters ✅
**Keyword**: Included naturally ✅
**CTA**: "Start podcasting today!" ✅

### Complete Meta Tag Block

```html
<!-- 主要元标签 -->
<title>如何在[当前年份]开始播客：完整的初学者指南</title>
<meta name="description" content="通过我们的分步指南学习如何在[当前年份]开始播客。涵盖设备、托管、录制以及发布第一集的内容。今天就开始播客吧！">
<link rel="canonical" href="https://yoursite.com/how-to-start-a-podcast/">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="article">
<meta property="og:url" content="https://yoursite.com/how-to-start-a-podcast/">
<meta property="og:title" content="如何在[当前年份]开始播客（完整指南）">
<meta property="og:description" content="启动播客所需的一切：设备推荐、托管平台、录制技巧和分步发布清单。无需经验。」>
<meta property="og:image" content="https://yoursite.com/images/podcast-guide.jpg">
<meta property="og:site_name" content="你的网站名称">

<!-- Twitter -->
<meta name="twitter:card" content="摘要图片">
<meta name="twitter:title" content="如何在[当前年份]开始播客">
<meta name="twitter:description" content="完整的初学者指南：包括设备、托管、录制等内容。」>
<meta name="twitter:image" content="https://yoursite.com/images/podcast-guide.jpg">
<meta name="twitter:site" content="@你的Twitter账号">
<!-- 文章标签 -->
<meta property="article:published_time" content "[YYYY-MM-DD]T08:00:00+00:00">
<meta property="article:author" content="https://yoursite.com/author/name">
<meta property="article:section" content="播客">
<meta property="article:tag" content="播客">
<meta property="article:tag" content="内容创作">
```

### A/B Test Variations

**Title Variation B**:
"Start a Podcast in [current year]: Step-by-Step Guide (+ Free Checklist)"

**Title Variation C**:
"How to Start a Podcast: [current year] Guide [Equipment + Software + Tips]"

**Description Variation B**:
"Want to start a podcast in [current year]? This guide covers everything: equipment ($100 budget option), best hosting platforms, recording tips, and how to get your first 1,000 listeners."
```

## 页面类型模板

### 首页

```html
<title>[Brand Name] - [Primary Value Proposition]</title>
<meta name="description" content="[Brand] helps [audience] [achieve goal]. [Key feature/benefit]. [CTA]">
```

### 产品页面

```html
<title>[Product Name] - [Key Benefit] | [Brand]</title>
<meta name="description" content="[Product] [key features]. [Price/offer if applicable]. [Social proof]. [CTA]">
```

### 博客文章

```html
<title>[How to/What is/Number] [Keyword] [Benefit/Year]</title>
<meta name="description" content="[What they'll learn]. [Key points covered]. [CTA]">
```

### 服务页面

```html
<title>[Service] in [Location] - [Brand] | [Differentiator]</title>
<meta name="description" content="[Service description]. [Experience/credentials]. [Key benefit]. [CTA]">
```

## 成功技巧

1. **前置关键词** - 将重要词汇放在开头
2. **匹配搜索意图** - 描述应准确反映页面内容
3. **具体明确** - 模糊的描述会被忽略
4. **测试不同版本** - 微小的改动可能会显著影响点击率
5. **定期更新** - 添加当前年份信息，更新内容
6. **查看竞争对手** - 了解在SERP中哪些方法有效

## 标题标签公式模板

### 经验证的标题公式

| 公式 | 模板 | 示例 | 适用场景 |
|---------|----------|---------|---------|
| “如何”系列 | 如何[实现目标]（[年份]） | 如何提高SEO排名（2026年） | 信息类指南 |
| 数字列表 | [数字] [形容词] [目标受众] | 15个经过验证的电子商务SEO策略 | 列表文章 |
| 问题式 | [问题]？[这里是答案预览] | 什么是技术SEO？完整指南 | 定义类内容 |
| 对比式 | [选项A] vs [选项B]：[区别点] | Ahrefs vs SEMrush：哪个SEO工具更胜一筹？ | 对比页面 |
| 基于年份 | [年份]的最佳[主题]（[经过测试/排名]） | 2026年最佳SEO工具（专家测试） | 持久且新鲜的内容 |
| 优势驱动 | [优势]：[如何实现] | 在Google上排名第一的10步SEO清单 | 高点击率页面 |
| 括号式 | [主题]（[修饰词]） | 链接构建指南（含模板） | 传递价值信号 |
| 负面式 | [数字] [主题] 错误 [后果] | 7个会毁掉你排名的SEO错误 | 问题意识类内容 |

## 标题标签中的关键词

| 关键词类型 | 常用关键词 | 使用建议 |
|----------|-----------|---------------|
| 紧急性 | 现在、今天、快速、立即、2026 | 避免过度使用；需结合实质内容 |
| 价值性 | 免费、经过验证、完整、必备、终极 | 避免夸大其词 |
| 具体性 | [具体数字]、分步说明、清单、模板 | 越具体，点击率越高 |
| 好奇心 | 秘密、鲜为人知、令人惊讶 | 必须兑现承诺 |
| 权威性 | 专家、有研究支持、数据驱动 | 仅用于真正专业的内容 |
| 情感性 | 最佳、最差、错误、警告、有力 | 平衡情感与可信度 |

## 标题标签长度优化

| 长度范围 | 在SERP中的显示效果 | 建议 |
|-------------|--------------|----------------|
| <30个字符 | 可能显示不完整 | 通过添加修饰词或品牌名称来扩展 |
| 30-50个字符 | 在所有设备上都能完整显示 | 非常适合移动设备 |
| 50-60个字符 | 在桌面设备上能完整显示，可能在移动设备上被截断 | 最佳长度 |
| 60-65个字符 | 在某些设备上可能被截断 | 前置关键词 |
| >65个字符 | 在所有设备上都会被截断 | 应避免使用 |

## 元描述写作框架

### AIDA框架

| 元素 | 功能 | 示例 |
|---------|-------------|---------|
| **注意力** | 用醒目的声明或问题吸引注意力 | “想让你的自然流量翻倍吗？” |
| **兴趣** | 建立相关性 | “本指南涵盖了15个经过验证的策略...” |
| **欲望** | 展示好处 | “...被顶级网站用来提高200%流量的方法。” |
| **行动** | 提供行动号召 | “现在就阅读完整指南。” |

**完整示例**：“想让你的自然流量翻倍吗？本指南涵盖了顶级网站使用的15个经过验证的SEO策略，可提高200%的流量。现在就阅读完整指南。”（158个字符）

### PAS框架

| 元素 | 功能 | 示例 |
|---------|-------------|---------|
| **问题** | 识别痛点 | “在Google上难以排名吗？” |
| **放大** | 强化问题 | “大多数SEO指南已经过时，忽略了关键的排名因素。” |
| **解决方案** | 提供解决方案 | “我们的2026年指南涵盖了真正有效的方法。立即阅读。” |

## CTR优化数据

### 提高自然点击率（CTR）的因素

| 因素 | 对CTR的影响 | 实施方法 |
|--------|-----------|----------------|
| 标题中的数字 | +20-30% | 如“7种方法”、“15个技巧”、“2026年” |
| 标题中的问题 | +14% | 以“How”、“What”、“Why”开头 |
| 情感词汇 | +7% | 如“经过验证”、“必备”、“错误” |
| 括号/括号 | +38% | 如“[指南]”、“（附示例）” |
| 当前年份 | +10-15% | 如“2026年最佳SEO工具” |
| 关键词 | +12% | 参见上面的关键词列表 |
| 与搜索意图匹配 | +15-25% | 使标题与SERP预期一致 |
| 丰富的内容（Schema标记） | +30% | 常见问题解答、操作指南、评分 |

## 各平台的Open Graph最佳实践

### 平台特定的OG优化

| 平台 | 图片尺寸 | 标题长度 | 描述长度 | 特殊标签 |
|----------|-----------|-------------|-------------------|-------------|
| Facebook | 1200x630像素 | 40-60个字符 | 125-155个字符 | og:type, og:locale |
| Twitter/X | 1200x600像素 | 最多70个字符 | 200个字符 | twitter:card, twitter:site |
| LinkedIn | 1200x627像素 | 70个字符 | 150个字符 | 标准OG标签 |
| Pinterest | 1000x1500像素（2:3） | 100个字符 | 500个字符 | 建议使用og:type=article |
| Slack | 最小500x500像素 | 完整标题 | 前300个字符 | 标准OG标签 |

### OG标签检查清单

| 标签 | 是否必需 | 备注 |
|-----|----------|-------|
| og:title | 是 | 可能与HTML标题不同；需优化以适应社交媒体分享 |
| og:description | 是 | 需针对社交媒体进行优化；可能与元描述不同 |
| og:image | 是 | 必须是绝对URL；建议使用1200x200像素的图片 |
| og:url | 是 | 规范URL |
| og:type | 是 | 首页使用“website”，博客文章使用“article” |
| og:site_name | 建议使用 | 例如“en_US” |
| twitter:card | 建议使用 | 文章使用“summary_large_image” |
| twitter:site | 建议使用 | @你的品牌名称 |

## 参考资料

- [元标签公式](./references/meta-tag-formulas.md) — 提供经过验证的标题和描述公式，包含模板、关键词和CTR数据

## 相关技能

- [seo-content-writer](../seo-content-writer/) — 用于编写元标签的内容 |
- [schema-markup-generator](../schema-markup-generator/) — 用于添加结构化数据 |
- [on-page-seo-auditor](../../optimize/on-page-seo-auditor/) — 用于审核所有元标签 |
- [serp-analysis](../../research/serp-analysis/) — 用于分析竞争对手的元标签 |
- [geo-content-optimizer](../geo-content-optimizer/) — 地理定位优化可辅助元标签的优化 |
- [content-quality-auditor](../../cross-cutting/content-quality-auditor/) — 全面的CORE-EEAT审核，包括元标签涉及的C01/C02项目 |