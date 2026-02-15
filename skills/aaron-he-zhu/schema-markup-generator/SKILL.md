---
name: schema-markup-generator
description: '**使用场景：**  
当用户请求“添加数据结构标记（schema markup）”、“生成结构化数据”、“生成 JSON-LD 格式的数据”、“创建丰富的内容片段（rich snippets）”、“创建 FAQ 数据结构”、“在 Google 中显示星级评分”、“添加产品信息标记（product markup）”或“创建食谱数据结构（recipe schema）”时，该工具可生成 Schema.org JSON-LD 格式的结构化数据。这些数据可用于在搜索引擎中展示丰富的搜索结果，包括 FAQ 片段、操作指南卡片（How-To cards）、产品列表、用户评价等。  

**相关工具：**  
- 用于元标签优化（meta-tag optimization）的工具：`meta-tags-optimizer`  
- 用于更广泛的技术性搜索引擎优化（technical SEO）的工具：`technical-seo-checker`'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "medium"
  tags:
    - seo
    - schema markup
    - structured data
    - json-ld
    - rich results
    - rich snippets
    - faq schema
    - how-to schema
    - product schema
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

# 结构化数据生成器（Schema Markup Generator）

> **[SEO与地理信息技能库](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20项SEO与地理信息相关技能 · 全部技能安装方式：`npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>浏览全部20项技能</summary>

**研究** · [关键词研究](../../research/keyword-research/) · [竞争对手分析](../../research/competitor-analysis/) · [SERP分析](../../research/serp-analysis/) · [内容差距分析](../../research/content-gap-analysis/)

**构建** · [SEO内容编写器](../seo-content-writer/) · [地理内容优化器](../geo-content-optimizer/) · [元标签优化器](../meta-tags-optimizer/) · **结构化数据生成器**

**优化** · [页面SEO审核器](../../optimize/on-page-seo-auditor/) · [技术SEO检查器](../../optimize/technical-seo-checker/) · [内部链接优化器](../../optimize/internal-linking-optimizer/) · [内容更新器](../../optimize/content-refresher/)

**监控** · [排名追踪器](../../monitor/rank-tracker/) · [反向链接分析器](../../monitor/backlink-analyzer/) · [性能报告器](../../monitor/performance-reporter/) · [警报管理器](../../monitor/alert-manager/)

**跨领域技能** · [内容质量审核器](../../cross-cutting/content-quality-auditor/) · [域名权威性审核器](../../cross-cutting/domain-authority-auditor/) · [实体优化器](../../cross-cutting/entity-optimizer/) · [内存管理](../../cross-cutting/memory-management/)

</details>

此技能能够生成符合Schema.org标准的结构化数据（JSON-LD格式），帮助搜索引擎更好地理解您的内容，从而在搜索结果页面（SERP）中呈现更丰富的信息。

## 何时使用此技能

- 为常见问题页面添加FAQ结构化数据，以提升在SERP中的显示效果
- 为操作指南类型的内容生成How-To结构化数据
- 为电子商务页面添加产品结构化数据
- 为博客文章实现Article结构化数据
- 为本地商家页面添加Local Business结构化数据
- 生成评论/评分结构化数据
- 为品牌页面实现Organization结构化数据
- 任何需要提升内容可见性的页面

## 此技能的功能

1. **选择合适的结构化数据类型**
2. **生成有效的JSON-LD格式结构化数据**
3. **将内容映射到相应的结构化数据属性**
4. **提供验证指导**
5. **处理复杂的多类型结构化数据**
6. **确定哪些内容适合呈现为丰富结果（rich results）**

## 使用方法

### 为内容生成结构化数据

```
Generate schema markup for this [content type]: [content/URL]
```

```
Create FAQ schema for these questions and answers: [Q&A list]
```

### 具体的结构化数据类型

```
Create Product schema for [product name] with [details]
```

```
Generate LocalBusiness schema for [business name and details]
```

### 审核现有的结构化数据

```
Review and improve this schema markup: [existing schema]
```

## 数据来源

> 请参阅[CONNECTORS.md](../../CONNECTORS.md)，了解工具类别的相关信息。

**使用[网络爬虫时：**
自动爬取并提取页面内容（可见文本、标题、列表、表格）、现有的结构化数据标记、页面元数据以及与结构化数据属性匹配的内容元素。

**仅使用手动数据时：**
要求用户提供：
1. 页面URL或完整的HTML内容
2. 页面类型（文章、产品、常见问题、操作指南等）
3. 结构化数据所需的具体信息（价格、日期、作者信息、问答对等）
4. 当前使用的结构化数据标记（如果需要优化现有数据）

根据提供的数据执行完整的工作流程。在输出中明确标注哪些数据来自自动提取，哪些数据是用户提供的。

## 使用说明

当用户请求生成结构化数据标记时：

1. **确定内容类型及是否适合呈现为丰富结果**
   参考[CORE-EEAT基准](../../references/core-eeat-benchmark.md)中的**O05（结构化数据标记）**条目，了解内容类型与结构化数据类型的映射关系：

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

2. **生成FAQ结构化数据**

   ```markdown
   ### FAQ Schema (FAQPage)
   
   **Requirements**:
   - Minimum 2 Q&A pairs
   - Questions must be complete questions
   - Answers should be comprehensive
   - Must match visible page content
   
   **Generated Schema**:
   
   ```json
   {
     "@context": "https://schema.org",
     "@type": "FAQPage",
     "mainEntity": [
       {
         "@type": "Question",
         "name": "[页面上显示的问题1]",
         "acceptedAnswer": {
           "@type": "Answer",
           "text": "[完整答案]"
         }
       },
       {
         "@type": "Question",
         "name": "[问题2]",
         "acceptedAnswer": {
           "@type": "Answer",
           "text": "[完整答案]"
         }
       }
     ]
   }
   ```
   
   **Rich Result Preview**:
   ```
   [页面标题]
   [URL]
   [元描述]
   
   ▼ 问题1？
     [答案预览...]
   ▼ 问题2？
     [答案预览...]
   ```
   ```

3. **生成操作指南结构化数据**

   ```markdown
   ### How-To Schema (HowTo)
   
   **Requirements**:
   - Clear step-by-step instructions
   - Each step must have text
   - Optional: images, videos, time, supplies
   
   **Generated Schema**:
   
   ```json
   {
     "@context": "https://schema.org",
     "@type": "HowTo",
     "name": "[操作指南标题]",
     "description": "[该指南的简要描述]",
     "totalTime": "PT[X]M",
     "estimatedCost": {
       "@type": "MonetaryAmount",
       "currency": "USD",
       "value": "[费用]"
     },
     "supply": [
       {
         "@type": "HowToSupply",
         "name": "[供应项1]"
       }
     ],
     "tool": [
       {
         "@type": "HowToTool",
         "name": "[工具1]"
       }
     ],
     "step": [
       {
         "@type": "HowToStep",
         "name": "[步骤1标题]",
         "text": "[步骤1的详细说明]",
         "url": "[URL]#step1",
         "image": "[步骤1的图片链接]"
       },
       {
         "@type": "HowToStep",
         "name": "[步骤2标题]",
         "text": "[步骤2的详细说明]",
         "url": "[URL]#step2",
         "image": "[步骤2的图片链接]"
       }
     ]
   }
   ```
   ```

4. **生成文章结构化数据**

   ```markdown
   ### Article Schema
   
   **Schema Type Options**:
   - `Article` - General articles
   - `BlogPosting` - Blog posts
   - `NewsArticle` - News content
   - `TechArticle` - Technical documentation
   
   **Generated Schema**:
   
   ```json
   {
     "@context": "https://schema.org",
     "@type": "Article",
     "headline": "[文章标题 - 最多110个字符]",
     "description": "[文章摘要]",
     "image": [
       "[图片URL 1 - 宽度1200px]",
       "[图片URL 2 - 4:3比例]",
       "[图片URL 3 - 16:9比例]"
     ],
     "datePublished": "[ISO 8601日期: 2024-01-15T08:00:00+00:00]",
     "dateModified": "[ISO 8601日期]",
     "author": {
       "@type": "Person",
       "name": "[作者名称]",
       "url": "[作者个人资料链接]"
     },
     "publisher": {
       "@type": "Organization",
       "name": "[出版商名称]",
       "logo": {
         "@type": "ImageObject",
         "url": "[Logo URL - 最高60像素]"
       }
     },
     "mainEntityOfPage": {
       "@type": "WebPage",
       "@id": "[页面的 canonical URL]"
     }
   }
   ```
   ```

5. **生成产品结构化数据**

   ```markdown
   ### Product Schema
   
   **Requirements for Rich Results**:
   - Name (required)
   - Image (required)
   - Offers with price (for price rich results)
   - AggregateRating (for star ratings)
   - Review (for review snippets)
   
   **Generated Schema**:
   
   ```json
   {
     "@context": "https://schema.org",
     "@type": "Product",
     "name": "[产品名称]",
     "image": [
       "[产品图片URL 1]",
       "[产品图片URL 2]"
     ],
     "description": "[产品描述]",
     "sku": "[SKU]",
     "mpn": "[制造商部件编号]",
     "brand": {
       "@type": "Brand",
       "name": "[品牌名称]"
     },
     "offers": {
       "@type": "Offer",
       "url": "[产品链接]",
       "priceCurrency": "USD",
       "price": "[价格]",
       "priceValidUntil": "[有效期]",
       "availability": "https://schema.org/InStock",
       "seller": {
         "@type": "Organization",
         "name": "[卖家名称]"
       }
     },
     "aggregateRating": {
       "@type": "AggregateRating",
       "ratingValue": "[4.5]",
       "reviewCount": "[89]"
     },
     "review": {
       "@type": "Review",
       "reviewRating": {
         "@type": "Rating",
         "ratingValue": "[5]"
       },
       "author": {
         "@type": "Person",
         "name": "[评论者名称]"
       },
       "reviewBody": "[评论内容]"
     }
   }
   ```
   ```

6. **生成本地商家结构化数据**

   ```markdown
   ### LocalBusiness Schema
   
   **Generated Schema**:
   
   ```json
   {
     "@context": "https://schema.org",
     "@type": "[LocalBusiness/Restaurant/Store/etc.]",
     "name": "[商家名称]",
     "image": "[商家图片URL]",
     "@id": "[商家URL]",
     "url": "[网站URL]",
     "telephone": "[电话号码]",
     "priceRange": "[$$]",
     "address": {
       "@type": "PostalAddress",
       "streetAddress": "[街道地址]",
       "addressLocality": "[城市]",
       "addressRegion": "[州]",
       "postalCode": "[邮政编码]",
       "addressCountry": "US"
     },
     "geo": {
       "@type": "GeoCoordinates",
       "latitude": [纬度],
       "longitude": [经度]
     },
     "openingHoursSpecification": [
       {
         "@type": "OpeningHoursSpecification",
         "dayOfWeek": ["周一", "周二", "周三", "周四", "周五"],
         "opens": "09:00",
         "closes": "17:00"
       }
     ],
     "aggregateRating": {
       "@type": "AggregateRating",
       "ratingValue": "[4.5]",
       "reviewCount": "[123]"
     }
   }
   ```
   ```

7. **生成组织结构化数据**

   ```markdown
   ### Organization Schema
   
   **Generated Schema**:
   
   ```json
   {
     "@context": "https://schema.org",
     "@type": "Organization",
     "name": "[组织名称]",
     "url": "[网站URL]",
     "logo": "[Logo URL]",
     "sameAs": [
       "[Facebook URL]",
       "[Twitter URL]",
       "[LinkedIn URL]",
       "[Instagram URL]"
     ],
     "contactPoint": {
       "@type": "ContactPoint",
       "telephone": "[电话号码]",
       "contactType": "客户服务",
       "availableLanguage": ["英语"]
     }
   }
   ```
   ```

8. **生成面包屑导航结构化数据**

   ```markdown
   ### BreadcrumbList Schema
   
   **Generated Schema**:
   
   ```json
   {
     "@context": "https://schema.org",
     "@type": "BreadcrumbList",
     "itemListElement": [
       {
         "@type": "ListItem",
         "position": 1,
         "name": "首页",
         "item": "[首页URL]"
       },
       {
         "@type": "ListItem",
         "position": 2,
         "name": "[类别名称]",
         "item": "[类别URL]"
       },
       {
         "@type": "ListItem",
         "position": 3,
         "name": "[页面名称]",
         "item": "[页面URL]"
       }
     ]
   }
   ```
   ```

9. **组合多种结构化数据类型**

   ```markdown
   ### Combined Schema Implementation
   
   For pages needing multiple schema types:
   
   ```json
   <script type="application/ld+json">
   [
     {
       "@context": "https://schema.org",
       "@type": "Article",
       "headline": "[文章标题]",
       "author": { "@type": "Person", "name": "[作者名称]" }
     },
     {
       "@context": "https://schema.org",
       "@type": "FAQPage",
       "mainEntity": [{ "@type": "Question", "name": "[问题]", "acceptedAnswer": { "@type": "Answer", "text": "[答案]" } }]
     },
     {
       "@context": "https://schema.org",
       "@type": "BreadcrumbList",
       "itemListElement": [{ "@type": "ListItem", "position": 1, "name": "首页", "item": "[URL]" }]
     }
   ]
   </script>
   ```
   ```

10. **提供实现和验证**

    ```markdown
    ## Implementation Guide

    ### Adding Schema to Your Page

    **Option 1: In HTML <head>**
    ```html
    <head>
      <script type="application/ld+json">
        [您的JSON-LD结构化数据]
      </script>
    </head>
    ```

    **Option 2: Before closing </body>**
    ```html
      <script type="application/ld+json">
        [您的JSON-LD结构化数据]
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
- [ ] 提供了页面URL或内容
- [ ] 选择的内容类型与结构化数据类型匹配（例如，文章对应Article类型）
- [ ] 所有必需的数据都齐全（根据结构化数据类型，如作者信息、日期、价格等）
- [ ] 确认内容适合呈现为丰富结果

### 输出验证
- [ ] JSON语法正确（无多余的逗号，引号使用正确）
- [ ] 为所选的结构化数据类型提供了所有必需的属性
- [ ] URL是绝对路径，而非相对路径
- [ ] 日期格式符合ISO 8601标准（YYYY-MM-DDTHH:MM:SS+00:00）
- [ ] 结构化数据内容与页面实际显示的内容一致
- [ ] 通过结构化数据验证工具的检查（无错误）
- [ ] 明确标注每个数据点的来源（来自网络爬虫提取、用户提供或手动输入）

## 示例

**用户**：“为一篇关于SEO的页面生成FAQ结构化数据”

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
        "text": "SEO（搜索引擎优化）是指通过优化网站和内容来提高在搜索引擎结果页面（SERP）中的排名。它包括技术优化、内容创作和链接建设，以增加网站的有机流量和吸引目标访客。",
      }
    },
    {
      "@type": "Question",
      "name": "SEO需要多长时间才能见效？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO通常需要3-6个月才能看到显著效果，但这取决于竞争情况、域名权威性和投入的努力。新网站可能需要6-12个月，而具有现有权威性的网站在竞争较小的关键词上可能在1-3个月内看到改进。",
      }
    },
    {
      "@type": "Question",
      "name": "SEO比付费广告更好吗？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO和付费广告有不同的作用。SEO可以提供长期的、可持续的流量，且无需支付每次点击的费用，但需要时间来建立效果。付费广告可以立即产生效果，但一旦停止支付就会停止。大多数成功的企业会同时使用这两种方式：付费广告用于快速获取潜在客户，SEO用于长期发展。"
      }
    }
  ]
}
```

### Implementation

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "什么是SEO？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO（搜索引擎优化）是指通过优化网站和内容来提高在搜索引擎结果页面（SERP）中的排名。它包括技术优化、内容创作和链接建设，以增加网站的有机流量和吸引目标访客。",
      }
    },
    {
      "@type": "Question",
      "name": "SEO需要多长时间才能见效？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO通常需要3-6个月才能看到显著效果，但这取决于竞争情况、域名权威性和投入的努力。新网站可能需要6-12个月，而具有现有权威性的网站在竞争较小的关键词上可能在1-3个月内看到改进。",
      }
    },
    {
      "@type": "Question",
      "name": "SEO比付费广告更好吗？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO和付费广告有不同的作用。SEO可以提供长期的、可持续的流量，且无需支付每次点击的费用，但需要时间来建立效果。付费广告可以立即产生效果，但一旦停止支付就会停止。大多数成功的企业会同时使用这两种方式：付费广告用于快速获取潜在客户，SEO用于长期发展。」
      }
    }
  ]
}
```

### Validation

Test with ~~schema validator

### SERP Preview

```
SEO指南：初级教程
yoursite.com/seo-guide/
从零开始学习SEO，通过我们的全面指南...

▼ 什么是SEO？
  SEO（搜索引擎优化）是指通过优化网站和内容来提高在搜索结果页面（SERP）中的排名...
▼ SEO需要多长时间才能见效？
  SEO通常需要3-6个月才能看到显著效果...
▼ SEO比付费广告更好吗？
  SEO和付费广告有不同的作用...

```
```

## 结构化数据类型快速参考

| 内容类型 | 结构化数据类型 | 关键属性 |
|--------------|-------------|----------------|
| 博文 | BlogPosting/Article | headline, datePublished, author |
| 产品 | Product | name, price, availability |
| 常见问题 | FAQPage | Question, Answer |
| 操作指南 | HowTo | step, totalTime |
| 本地商家 | LocalBusiness | address, geo, openingHours |
| 食谱 | Recipe | ingredients, cookTime |
| 活动 | Event | startDate, location |
| 视频 | VideoObject | uploadDate, duration |
| 课程 | Course | provider, name |
| 评论 | Review | itemReviewed, ratingValue |

## 成功技巧

1. **与页面显示的内容一致** - 结构化数据必须反映用户实际看到的内容
2. **不要滥用** - 仅为相关内容添加结构化数据
3. **保持更新** - 当日期和价格发生变化时及时更新
4. **彻底测试** - 部署前进行验证
5. **监控Search Console** - 注意错误和警告

## 结构化数据类型决策树

### 根据内容选择合适的结构化数据类型

| 内容类型 | 主要使用的结构化数据类型 | 如适用可添加的其他结构化数据类型 | 是否适合呈现为丰富结果 |
|-------------|---------------|-------------------|----------------------|
| 博文/文章 | Article | FAQ, HowTo | 文章轮播、FAQ丰富结果 |
| 产品页面 | Product | Review, Offer, AggregateRating | 带有价格/评分的产品片段 |
| 服务页面 | Service | FAQ, LocalBusiness | 服务片段 |
| 操作指南 | HowTo | Article, FAQ | 带有步骤的操作指南丰富结果 |
| 常见问题页面 | FAQPage | Article | SERP中的FAQ折叠面板 |
| 食谱 | Recipe | Video, AggregateRating | 食谱轮播 |
| 活动 | Event | Offer, Organization | 带有日期/地点的活动片段 |
| 视频 | VideoObject | Article | 视频轮播、关键时刻 |
| 本地商家 | LocalBusiness | Review, OpeningHoursSpecification | 本地商家信息、知识面板 |
| 个人/作者 | Person | Organization | 个人资料、组织信息 | 知识面板 |
| 组织 | Organization | ContactPoint, Logo | 信息面板 |
| 课程 | Course | Organization | 课程丰富结果 |
| 招聘信息 | JobPosting | Organization | Google招聘信息 |
| 面包屑导航 | BreadcrumbList | （始终与其他结构化数据一起添加） | SERP中的面包屑导航 |
| 软件/应用 | SoftwareApplication | Review, Offer | 应用程序片段 |

## 行业特定的结构化数据推荐

| 行业 | 必需的结构化数据类型 | 高价值附加结构化数据类型 |
|----------|-----------------|---------------------|
| 电子商务 | Product, BreadcrumbList, Organization | AggregateRating, FAQ, Review |
| SaaS | SoftwareApplication, FAQPage, Organization | HowTo, VideoObject, Review |
| 本地服务 | LocalBusiness, Service | FAQ, Review, Event |
| 出版/媒体 | Article, Person, Organization | FAQ, Speakable, VideoObject |
| 教育 | Course, Organization | FAQ, HowTo, Event |
| 医疗保健 | MedicalWebPage, Organization | FAQ, Physician, MedicalClinic |
| 房地产 | RealEstateListing, Organization | LocalBusiness, FAQ |
| 餐厅 | Restaurant, Menu | Review, Event, FAQ |

## 结构化数据实现的优先级

| 优先级 | 结构化数据类型 | 原因 |
|----------|-------------|-----|
| P0 -- 必须添加 | Organization, BreadcrumbList, WebSite (SearchAction) | 所有网站的基础 |
| P1 -- 核心内容 | Article, FAQPage, HowTo | 直接适用于呈现为丰富结果 |
| P2 -- 商业相关 | Product, Review, AggregateRating, Offer | 有助于增加收入的丰富结果 |
| P3 -- 增强权威性 | Person, SameAs, Speakable | 有助于提升网站权威性的元素 |
| P4 -- 专业领域 | 行业特定的结构化数据类型 | 适用于特定领域的丰富结果 |

## 结构化数据验证快速参考

| 问题 | 影响 | 解决方法 |
|-------|--------|-----|
| 缺少必需的属性 | Google会忽略该结构化数据 | 添加所有必需的字段（参考schema.org） |
| 日期格式错误 | 可能导致结构化数据无法被识别 | 使用ISO 8601格式（例如：2026-02-11） |
| @type错误 | 结构化数据被错误解读 | 确保@type与schema.org的标准完全匹配 |
| 同一组织的多个sameAs链接 | 可能导致错误 | sameAs应链接到外部个人资料 |
| 文章缺少图片 | 会导致文章无法作为丰富结果显示 | 添加带有有效URL的图片属性 |
| 评论缺少itemReviewed | 评论无法被正确显示 | 将评论嵌套在Product/Service等结构化数据中 |

## 参考资料

- [结构化数据模板](./references/schema-templates.md) - 所有结构化数据类型的JSON-LD模板
- [验证指南](./references/validation-guide.md) - 常见错误、必需的属性、测试流程

## 相关技能

- [seo-content-writer](../seo-content-writer/) — 创建适合标记的结构化数据
- [geo-content-optimizer](../geo-content-optimizer/) — 优化常见问题页面的内容
- [on-page-seo-auditor](../../optimize/on-page-seo-auditor/) — 审核现有的结构化数据
- [technical-seo-checker](../../optimize/technical-seo-checker/) — 进行技术验证
- [entity-optimizer](../../cross-cutting/entity-optimizer/) — 用于审核Organization、Person、Product等实体相关的结构化数据 |
- [meta-tags-optimizer](../meta-tags-optimizer/) — 在结构化数据的同时优化元标签