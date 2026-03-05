---
name: schema-markup-generator
version: "3.0.0"
description: '当用户请求“添加架构标记”（add schema markup）、“生成结构化数据”（generate structured data）、“JSON-LD”（JSON-LD）、“丰富片段”（rich snippets）、“FAQ架构”（FAQ schema）、“操作指南架构”（HowTo schema）、“产品架构”（Product schema）、“文章架构”（Article schema）、“本地企业架构”（LocalBusiness schema）、“组织架构”（Organization schema）、“面包屑导航列表”（BreadcrumbList）、“希望在Google上显示星级评分”（I want star ratings in Google）、“丰富搜索结果”（rich search results）、“语音搜索优化”（voice search optimization）、“事件标记”（event markup）或“结构化数据验证错误”（structured data validation errors）时，应使用此技能。该技能会为FAQPage、HowTo、Article/BlogPosting、Product、AggregateRating、LocalBusiness、Organization、BreadcrumbList、Event和Recipe类型生成Schema.org JSON-LD格式的数据。生成的标记符合Google Rich Results、Bing结构化数据以及AI系统的要求（FAQ架构有助于提高AI的引用几率）。如需更广泛的技术SEO支持，请参阅technical-seo-checker；关于元标签优化，请参阅meta-tags-optimizer。'
license: Apache-2.0
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
allowed-tools: WebFetch
metadata:
  author: aaron-he-zhu
  version: "3.0.0"
  geo-relevance: "medium"
  tags:
    - seo
    - structured-data
    - json-ld
    - rich-results
    - rich-snippets
    - faq-schema
    - howto-schema
    - product-schema
    - article-schema
    - localbusiness-schema
    - schema-org
  triggers:
    - "add schema markup"
    - "generate structured data"
    - "JSON-LD"
    - "rich snippets"
    - "FAQ schema"
    - "schema.org"
    - "structured data markup"
    - "add FAQ rich results"
    - "I want star ratings in Google"
    - "product markup"
    - "recipe schema"
---
# Schema Markup Generator

> **[SEO & GEO Skills Library](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与GEO相关技能 · 全部技能安装方法：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容编写器](../seo-content-writer/) · [地理内容优化器](../geo-content-optimizer/) · [元标签优化器](../meta-tags-optimizer/) · **Schema标记生成器**

**优化** · [页面SEO审核器](../../optimize/on-page-seo-auditor/) · [技术SEO检查器](../../optimize/technical-seo-checker/) · [内部链接优化器](../../optimize/internal-linking-optimizer/) · [内容更新器](../../optimize/content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告器](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)

**跨领域技能** · [内容质量审核器](../../cross-cutting/content-quality-auditor/) · [域名权威度审核器](../../cross-cutting/domain-authority-auditor/) · [实体优化器](../../cross-cutting/entity-optimizer/) · [内存管理](../../cross-cutting/memory-management/)

</details>

此技能可生成JSON-LD格式的Schema.org结构化数据标记，帮助搜索引擎更好地理解您的内容，从而在搜索结果页面（SERPs）中呈现更丰富的信息。

## 何时使用此技能

- 为FAQ页面添加Schema标记，以提升在搜索结果中的显示效果
- 为教程类内容创建How-To Schema
- 为电商页面添加Product Schema
- 为博客文章添加Article Schema
- 为本地商家页面添加Local Business Schema
- 创建Review/Rating Schema
- 为品牌页面添加Organization Schema
- 任何需要提升搜索结果可见性的页面

## 该技能的功能

1. **选择合适的Schema类型**
2. **生成有效的JSON-LD标记**
3. **将内容映射到Schema属性**
4. **验证标记是否符合要求**
5. **处理复杂的多类型Schema**
6. **确定可实现的丰富搜索结果类型**

## 使用方法

### 为内容生成Schema标记

```
Generate schema markup for this [content type]: [content/URL]
```

```
Create FAQ schema for these questions and answers: [Q&A list]
```

### 具体的Schema类型

```
Create Product schema for [product name] with [details]
```

```
Generate LocalBusiness schema for [business name and details]
```

### 审核现有的Schema标记

```
Review and improve this schema markup: [existing schema]
```

## 数据来源

> 请参阅[CONNECTORS.md](../../CONNECTORS.md)，了解工具类别的相关信息。

**使用网络爬虫时：**
自动抓取并提取页面内容（可见文本、标题、列表、表格）、现有的Schema标记、页面元数据以及与Schema属性匹配的结构化内容元素。

**仅使用手动数据时：**
要求用户提供：
1. 页面URL或完整的HTML内容
2. 页面类型（文章、产品、FAQ、教程、本地商家等）
3. Schema所需的具体数据（价格、日期、作者信息、问答对等）
4. 当前使用的Schema标记（如需优化现有内容）

根据提供的数据执行完整的工作流程。请在输出中明确标注哪些数据来自自动提取，哪些数据是用户提供的。

## 使用说明

当用户请求生成Schema标记时：

1. **确定内容类型及是否适合生成丰富搜索结果**
   参考[CORE-EEAT基准](../../references/core-eeat-benchmark.md)中的**O05（Schema标记）**部分，了解如何将内容类型映射到相应的Schema类型：

   ```markdown
   ### CORE-EEAT Schema Mapping (O05)

   | Content Type | Required Schema | Conditional Schema |
   |-------------|----------------|--------------------|
   | Blog (guides) | Article, Breadcrumb | FAQ, HowTo |
   | Blog (tools) | Article, Breadcrumb | FAQ, Review |
   | Blog (insights) | Article, Breadcrumb | FAQ |
   | Alternative | Comparison*, Breadcrumb, FAQ | AggregateRating |
   | Best-of | ItemList, Breadcrumb, FAQ | AggregateRating per tool |
   | Use-case | WebPage, Breadcrumb, FAQ | — |
   | FAQ | FAQPage, Breadcrumb | — |
   | Landing | SoftwareApplication, Breadcrumb, FAQ | WebPage |
   | Testimonial | Review, Breadcrumb | FAQ, Person |

   *Use the mapping above to ensure schema type matches content type (CORE-EEAT O05: Pass criteria).*
   ```

   ```markdown
   ### Schema Analysis

   **Content Type**: [blog/product/FAQ/how-to/local business/etc.]
   **Page URL**: [URL]

   **Eligible Rich Results**:
   
   | Rich Result Type | Eligibility | Impact |
   |------------------|-------------|--------|
   | FAQ | ✅/❌ | High - Expands SERP presence |
   | How-To | ✅/❌ | Medium - Shows steps in SERP |
   | Product | ✅/❌ | High - Shows price, availability |
   | Review | ✅/❌ | High - Shows star ratings |
   | Article | ✅/❌ | Medium - Shows publish date, author |
   | Breadcrumb | ✅/❌ | Medium - Shows navigation path |
   | Video | ✅/❌ | High - Shows video thumbnail |
   
   **Recommended Schema Types**:
   1. [Primary schema type] - [reason]
   2. [Secondary schema type] - [reason]
   ```

2. **生成Schema标记**
   根据确定的内容类型，生成相应的JSON-LD Schema。支持的类型包括：FAQPage、HowTo、Article/BlogPosting/NewsArticle、Product、LocalBusiness、Organization、BreadcrumbList、Event、Recipe以及组合的多类型Schema。

   > **参考**：请参阅[references/schema-templates.md](./references/schema-templates.md)，获取所有Schema类型的完整JSON-LD模板，其中包含必填和可选属性。

   对于每个生成的Schema，应包括：
   - 所选类型的所有必填属性
   - 预示的丰富搜索结果外观
   - 明确哪些属性是必填的，哪些是可选的

   如果一个页面包含多种Schema类型，请将它们放在一个`<script type="application/ld+json">`标签内的JSON数组中。

3. **提供实现和验证步骤**

    ```markdown
    ## Implementation Guide

    ### Adding Schema to Your Page

    **Option 1: In HTML <head>**
    ```html
    <head>
      <script type="application/ld+json">
        [您的JSON-LD标记内容]
      </script>
    </head>
    ```

    **Option 2: Before closing </body>**
    ```html
      <script type="application/ld+json">
        [您的JSON-LD标记内容]
      </script>
    </body>
    ```

    ### Validation Steps

    1. **~~schema validator**
       - Test your live URL or paste code
       - Check for errors and warnings

    2. **Schema.org Validator**
       - URL: https://validator.schema.org/
       - Validates against Schema.org spec

    3. **~~search console**
       - Monitor rich results in ~~search console
       - Check Enhancements reports for issues

    ### Validation Checklist

    - [ ] JSON syntax is valid (no trailing commas)
    - [ ] All required properties present
    - [ ] URLs are absolute, not relative
    - [ ] Dates are in ISO 8601 format
    - [ ] Content matches visible page content
    - [ ] No policy violations
    ```

## 验证要点

### 输入验证
- 是否提供了页面URL或内容
- 选择的Schema类型是否适用于该内容（例如，博客使用Article Schema，电商使用Product Schema等）
- 是否提供了所有必要的数据（根据Schema类型，如作者信息、日期、价格等）
- 内容是否符合生成丰富搜索结果的条件

### 输出验证
- JSON语法是否正确（无多余的逗号，引号使用正确）
- 是否为所选Schema类型提供了所有必填属性
- URL是否为绝对路径（非相对路径）
- 日期格式是否符合ISO 8601标准（YYYY-MM-DDTHH:MM:SS+00:00）
- Schema内容是否与页面实际显示的内容完全一致
- 通过Schema验证器检查，无错误
- 明确每个数据点的来源（来自网络爬虫提取、用户提供或手动输入）

## 示例

**用户请求**：为一篇关于SEO的页面生成FAQ Schema

**输出**：

```markdown
## FAQ Schema for SEO Page

### Schema Markup

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "什么是SEO？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO（搜索引擎优化）是指通过优化网站和内容来提高在搜索结果页面（SERPs）中的排名。它包括技术优化、内容创作和链接建设，以增加网站的自然流量和吸引目标访客。”
      }
    },
    {
      "@type": "Question",
      "name": "SEO需要多长时间才能见效？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO通常需要3-6个月才能看到显著效果，但这取决于竞争情况、域名权威度和投入的努力。新网站可能需要6-12个月，而具有较高权威度的现有网站在竞争较小的关键词上可能1-3个月内就能看到效果。”
      }
    },
    {
      "@type": "Question",
      "name": "SEO比付费广告更好吗？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO和付费广告有不同的作用。SEO提供可持续的长期流量，无需每次点击付费，但需要时间来建立效果；而付费广告可以立即带来流量，但停止付费后效果也会消失。大多数成功的企业会同时使用这两种方法：付费广告用于快速获取潜在客户，SEO用于长期发展。”
      }
    }
  ]
}
```

_Implementation: Wrap the above JSON-LD in `<script type="application/ld+json">...</script>` and place in `<head>` or before `</body>`. Test with ~~schema validator._

### SERP Preview

```
SEO指南：完整的初学者教程
yoursite.com/seo-guide/
通过我们的全面指南从零开始学习SEO...

▼ 什么是SEO？
  SEO（搜索引擎优化）是通过优化网站和内容来提高在搜索结果页面（SERPs）中排名的方法...
▼ SEO需要多长时间才能见效？
  SEO通常需要3-6个月才能看到显著效果...
▼ SEO比付费广告更好吗？
  SEO和付费广告有不同的作用...

```
```

## Schema类型快速参考

| 内容类型 | Schema类型 | 关键属性 |
|--------------|-------------|----------------|
| 博文 | BlogPosting/Article | 标题、发布日期、作者 |
| 产品 | Product | 名称、价格、库存情况 |
| FAQ | FAQPage | 问题、答案 |
| 教程 | HowTo | 步骤、总时长 |
| 本地商家 | LocalBusiness | 地址、地理位置、营业时间 |
| 食谱 | Recipe | 食材、烹饪时间 |
| 活动 | Event | 开始日期、地点 |
| 视频 | VideoObject | 上传日期、时长 |
| 课程 | Course | 提供者、名称 |
| 评论 | Review | 评价对象、评分 |

## 成功技巧

1. **确保Schema与可见内容一致** - Schema标记应反映用户实际看到的内容
2. **避免过度使用** - 仅对相关内容添加Schema标记
3. **保持更新** - 当数据（如日期、价格）发生变化时及时更新
4. **彻底测试** - 部署前进行验证
5. **监控Search Console** - 注意任何错误或警告

## Schema类型决策树

> **参考**：请参阅[references/schema-decision-tree.md](./references/schema-decision-tree.md)，了解完整的决策树（内容到Schema的映射关系）、行业特定建议、实施优先级（P0-P4）以及验证快速参考。

## 参考资料

- [Schema模板](./references/schema-templates.md) - 所有Schema类型的完整JSON-LD模板
- [验证指南](./references/validation-guide.md) - 常见错误、必填属性、测试流程

## 相关技能

- [seo-content-writer](../seo-content-writer/) — 创建适合标记的内容
- [on-page-seo-auditor](../../optimize/on-page-seo-auditor/) — 审核现有的Schema标记
- [technical-seo-checker](../../optimize/technical-seo-checker/) — 进行技术验证
- [entity-optimizer](../../cross-cutting/entity-optimizer/) — 用于优化Organization、Person、Product等实体类型的Schema标记