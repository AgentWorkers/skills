---
name: meta-tags-optimizer
version: "3.0.0"
description: '此技能适用于以下场景：用户请求“优化标题标签”、“编写元描述”、“提高点击率（CTR）”、“设置Open Graph标签”、“生成社交媒体预览图”、“我的标题标签需要修改”、“点击率过低”或“元标签无法正常显示”等情况。该技能用于创建和优化元标签（包括标题标签、元描述、Open Graph标签和Twitter卡片），以提升点击率和社交分享的参与度。如需进行更全面的页面SEO审计，请使用`on-page-seo-auditor`工具；如需处理结构化数据标记，请使用`schema-markup-generator`工具。'
license: Apache-2.0
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
metadata:
  author: aaron-he-zhu
  version: "3.0.0"
  geo-relevance: "low"
  tags:
    - seo
    - meta-tags
    - title-tag
    - meta-description
    - open-graph
    - twitter-card
    - ctr
    - social-sharing
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
# 元标签优化器 (Meta Tags Optimizer)

> **[SEO与地理定位技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 包含20项SEO与地理定位相关技能 · 全部技能可通过 `npx skills add aaron-he-zhu/seo-geo-claude-skills` 安装

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容编写器](../seo-content-writer/) · [地理内容优化器](../geo-content-optimizer/) · **元标签优化器** · [结构化数据生成器](../schema-markup-generator/)

**优化** · [页面SEO审核器](../../optimize/on-page-seo-auditor/) · [技术SEO检查器](../../optimize/technical-seo-checker/) · [内部链接优化器](../../optimize/internal-linking-optimizer/) · [内容更新工具](../../optimize/content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告工具](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)

**跨领域工具** · [内容质量审核器](../../cross-cutting/content-quality-auditor/) · [域名权威度审核器](../../cross-cutting/domain-authority-auditor/) · [实体信息优化器](../../cross-cutting/entity-optimizer/) · [内存管理工具](../../cross-cutting/memory-management/)

</details>

该技能可生成吸引人的、经过优化的元标签，从而提高搜索结果中的点击率，并提升社交媒体的分享率。它涵盖了标题标签、元描述以及社交媒体相关的元标签。

## 适用场景

- 为新页面创建元标签
- 优化现有元标签以提高点击率
- 为页面准备社交媒体分享内容
- 修复重复或缺失的元标签
- 对标题和描述进行A/B测试
- 根据特定SERP特征进行优化
- 为不同类型的页面生成元标签

## 功能介绍

1. **生成标题标签**：编写包含关键词的、吸引人的标题。
2. **编写元描述**：创建易于点击的描述内容。
3. **优化Open Graph元标签**：为社交媒体分享做好准备。
4. **设置Twitter卡片元标签**：优化Twitter特定的元标签。
5. **分析点击率**：提供改进建议以提升点击率。
6. **检查字符长度**：确保元标签符合SERP的显示要求。
7. **提供A/B测试选项**：提供多种版本以供测试。

## 使用方法

### 创建元标签

```
Create meta tags for a page about [topic] targeting [keyword]
```

### 优化现有元标签

```
Improve these meta tags for better CTR: [current tags]
```

### 设置社交媒体元标签

```
Create Open Graph and Twitter card tags for [page/URL]
```

## 数据来源

> 请参阅 [CONNECTORS.md](../../CONNECTORS.md) 以了解工具类别的相关信息。

**当连接了[搜索控制台](~~search console)和[SEO工具](~~SEO tool)时：**
- 自动获取当前的元标签、按查询生成的点击率数据、竞争对手的标题/描述模式、SERP预览数据以及展示次数/点击次数指标，从而发现优化机会。
**仅使用手动数据时：**
- 要求用户提供：
  - 当前页面的标题和元描述（如需优化现有元标签）。
  - 目标关键词及2-3个次要关键词。
  - 页面URL和主要内容/价值主张。
  - 竞争对手的URL或在SERP中表现良好的标题示例。
- 使用提供的数据完成整个工作流程。在输出中明确标注哪些数据来自自动化收集，哪些来自用户提供。

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

2. **生成优化后的标题标签**

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

4. **生成Open Graph、Twitter卡片及其他元标签**
   生成Open Graph元标签（og:type、og:url、og:title、og:description、og:image）、Twitter卡片元标签、规范URL、robots标签、viewport标签、作者信息以及特定于文章的元标签。然后将它们组合成一个完整的元标签块。

   > **参考资料**：请参阅 [references/meta-tag-code-templates.md](./references/meta-tag-code-templates.md)，其中包含Open Graph类型选择指南、Twitter卡片类型选择、所有HTML代码模板以及完整的元标签块模板。

5. **核心质量标准检查（CORE-EEAT）**
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

6. **提供点击率优化建议**

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
- [ ] 确认目标关键词与页面内容一致。
- [ ] 确定页面类型（博客/产品/登录页/服务页/首页）。
- [ ] 明确目标受众和搜索意图。
- [ ] 清晰阐述产品的独特价值主张。

### 输出验证
- [ ] 标题长度在50-60个字符之间（在SERP中能完整显示）。
- [ ] 元描述长度在150-160个字符之间。
- [ ] 目标关键词同时出现在标题和描述中。
- [ ] 指定了Open Graph图片（建议使用1200x630像素的图片）。
- [ ] 所有HTML语法均正确（无未闭合的引号或标签）。
- [ ] 明确标注每个数据来源（搜索控制台的点击率数据、SEO工具提供的数据或用户提供的数据）。

## 示例

**用户请求：** 为一篇关于“如何在[当前年份]开始播客”的博客文章生成元标签。

**输出结果：**

```markdown
## Meta Tags: How to Start a Podcast ([current year])

### Title Tag
```html
<title>如何在[当前年份]开始播客：新手指南</title>
```
**Length**: ~55 characters ✅
**Keyword**: "how to start a podcast" at front ✅
**Power Words**: "Complete", "Beginner's" ✅

### Meta Description
```html
<meta name="description" content="通过我们的分步指南学习如何在[当前年份]开始播客。涵盖设备选择、托管、录制以及首期节目的发布。立即开始你的播客之旅！">
```
**Length**: ~163 characters ✅
**Keyword**: Included naturally ✅
**CTA**: "Start podcasting today!" ✅

_Complete meta tag block (with OG, Twitter, Article tags) generated using template from [references/meta-tag-code-templates.md](./references/meta-tag-code-templates.md)._

### A/B Test Variations

**Title Variation B**:
"Start a Podcast in [current year]: Step-by-Step Guide (+ Free Checklist)"

**Title Variation C**:
"How to Start a Podcast: [current year] Guide [Equipment + Software + Tips]"

**Description Variation B**:
"Want to start a podcast in [current year]? This guide covers everything: equipment ($100 budget option), best hosting platforms, recording tips, and how to get your first 1,000 listeners."
```

## 成功技巧
1. **将关键词放在开头**：将重要词汇放在标题的开头。
2. **与页面内容匹配**：描述应准确反映页面内容。
3. **具体明确**：模糊的描述容易被忽略。
4. **进行A/B测试**：细微的改动可能显著影响点击率。
5. **定期更新**：添加当前年份的信息并更新描述内容。
6. **参考竞争对手**：了解在SERP中哪些元素有效。

## 参考资料
- [元标签公式](./references/meta-tag-formulas.md) — 经验证的标题和描述生成公式。
- [点击率与社交媒体参考](./references/ctr-and-social-reference.md) — 页面类型模板、点击率数据、Open Graph最佳实践。

## 相关技能
- [SEO内容编写器](../seo-content-writer/) — 用于生成元标签的内容。
- [结构化数据生成器](../schema-markup-generator/) — 用于添加结构化数据。
- [页面SEO审核器](../../optimize/on-page-seo-auditor/) — 用于审核所有元标签。
- [SERP分析器](../../research/serp-analysis/) — 用于分析竞争对手的元标签。