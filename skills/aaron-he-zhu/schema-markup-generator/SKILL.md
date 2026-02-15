---
name: schema-markup-generator
description: 生成结构化数据标记（Schema.org JSON-LD），以便在搜索引擎中呈现丰富的搜索结果，包括常见问题解答（FAQ）片段、操作指南卡片、产品列表、评论等。
geo-relevance: "medium"
---

# 架构标记生成器（Schema Markup Generator）

此技能能够生成符合 Schema.org 标准的结构化数据标记（JSON-LD 格式），帮助搜索引擎更好地理解您的内容，从而在搜索结果页面（SERPs）中呈现更丰富的信息。

## 适用场景

- 为常见问题解答（FAQ）页面添加结构化数据，以提升在搜索结果中的显示效果
- 为操作指南（How-To）内容生成结构化数据
- 为电子商务产品页面生成结构化数据
- 为博客文章生成结构化数据
- 为本地商家页面生成结构化数据
- 生成评论/评分信息
- 为组织页面生成结构化数据
- 适用于任何可以通过结构化数据提升页面可见性的场景

## 功能概述

1. **选择合适的结构化数据类型**
2. **生成有效的 JSON-LD 标记**
3. **将内容映射到相应的结构化数据属性**
4. **提供验证指导**
5. **处理复杂的多类型结构化数据**
6. **确定哪些内容适合生成丰富的搜索结果**

## 使用方法

### 为内容生成结构化数据

```
Generate schema markup for this [content type]: [content/URL]
```

### 具体的结构化数据类型

```
Create Product schema for [product name] with [details]
```

### 审查现有的结构化数据

```
Review and improve this schema markup: [existing schema]
```

## 数据来源

> 请参阅 [CONNECTORS.md](../../CONNECTORS.md) 以获取工具类别的相关信息。

**使用网络爬虫时：**
- 自动爬取页面内容（可见文本、标题、列表、表格）、现有的结构化数据标记、页面元数据以及与结构化数据属性匹配的内容元素。
**仅使用手动提供的数据时：**
- 要求用户提供：
  - 页面 URL 或完整的 HTML 内容
  - 页面类型（文章、产品、常见问题解答等）
  - 结构化数据所需的具体信息（价格、日期、作者信息、问答对等）
  - 当前使用的结构化数据标记（如需优化现有数据）

根据提供的数据完成整个工作流程。请在输出中明确标注哪些数据来自自动提取，哪些数据是用户提供的。

## 使用说明

当用户请求生成结构化数据标记时：

1. **确定内容类型及是否适合生成丰富的搜索结果**
   参考 [CORE-EEAT 基准](../../references/core-eeat-benchmark.md) 中的 **O05（结构化数据标记）** 部分，了解如何将内容类型映射到相应的结构化数据类型：

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

2. **生成常见问题解答（FAQ）结构化数据**

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
         "name": "[页面上显示的问题 1]",
         "acceptedAnswer": {
           "@type": "Answer",
           "text": "[完整答案]"
         }
       },
       {
         "@type": "Question",
         "name": "[页面上显示的问题 2]",
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
   
   ▼ 问题 1？
     [答案预览...]
   ▼ 问题 2？
     [答案预览...]
   ```
   ```

3. **生成操作指南（How-To）结构化数据**

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
     "description": "[内容简介]",
     "totalTime": "PT[X]M",
     "estimatedCost": {
       "@type": "MonetaryAmount",
       "currency": "USD",
       "value": "[费用]"
     },
     "supply": [
       {
         "@type": "HowToSupply",
         "name": "[供应项 1]"
       }
     ],
     "tool": [
       {
         "@type": "HowToTool",
         "name": "[工具 1]"
       }
     ],
     "step": [
       {
         "@type": "HowToStep",
         "name": "[步骤 1 标题]",
         "text": "[步骤 1 详细说明]",
         "url": "[URL]#step1",
         "image": "[步骤 1 图片 URL]"
       },
       {
         "@type": "HowToStep",
         "name": "[步骤 2 标题]",
         "text": "[步骤 2 详细说明]",
         "url": "[URL]#step2",
         "image": "[步骤 2 图片 URL]"
       }
     ]
   }
   ```
   ```

4. **生成文章（Article）结构化数据**

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
     "headline": "[文章标题 - 最多 110 个字符]",
     "description": "[文章摘要]",
     "image": [
       "[图片 URL 1 - 宽度 1200px]",
       "[图片 URL 2 - 4:3 比例]",
       "[图片 URL 3 - 16:9 比例]"
     ],
     "datePublished": "[ISO 8601 格式日期: 2024-01-15T08:00:00+00:00]",
     "dateModified": "[ISO 8601 格式日期]",
     "author": {
       "@type": "Person",
       "name": "[作者名称]",
       "url": "[作者个人资料 URL]"
     },
     "publisher": {
       "@type": "Organization",
       "name": "[出版商名称]",
       "logo": {
         "@type": "ImageObject",
         "url": "[标志 URL - 高度最大 60px]"
     },
     "mainEntityOfPage": {
       "@type": "WebPage",
       "@id": "[页面的 canonical URL]"
     }
   }
   ```
   ```

5. **生成产品（Product）结构化数据**

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
       "[产品图片 URL 1]",
       "[产品图片 URL 2]"
     ],
     "description": "[产品描述]",
     "sku": "[产品库存单位（SKU）]",
     "mpn": "[制造商部件编号]",
     "brand": {
       "@type": "Brand",
       "name": "[品牌名称]"
     },
     "offers": {
       "@type": "Offer",
       "url": "[产品购买链接]",
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

6. **生成本地商家（Local Business）结构化数据**

   ```markdown
   ### LocalBusiness Schema
   
   **Generated Schema**:
   
   ```json
   {
     "@context": "https://schema.org",
     "@type": "[LocalBusiness/Restaurant/Store/etc.]",
     "name": "[商家名称]",
     "image": "[商家图片 URL]",
     "@id": "[商家 URL]",
     "url": "[网站 URL]",
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

7. **生成组织（Organization）结构化数据**

   ```markdown
   ### Organization Schema
   
   **Generated Schema**:
   
   ```json
   {
     "@context": "https://schema.org",
     "@type": "Organization",
     "name": "[组织名称]",
     "url": "[网站 URL]",
     "logo": "[标志 URL]",
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

8. **生成导航栏（Breadcrumb）结构化数据**

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
         "item": "[首页 URL]"
       },
       {
         "@type": "ListItem",
         "position": 2,
         "name": "[分类名称]",
         "item": "[分类页面 URL]"
       },
       {
         "@type": "ListItem",
         "position": 3,
         "name": "[页面名称]",
         "item": "[当前页面 URL]"
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
       "itemListElement": [{ "@type": "ListItem", "position": 1, "name": "首页", "item": "[首页 URL]" }]
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
        [您的 JSON-LD 结构化数据代码]
      </script>
    </head>
    ```

    **Option 2: Before closing </body>**
    ```html
      <script type="application/ld+json">
        [您的 JSON-LD 结构化数据代码]
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
- 是否提供了页面 URL 或内容
- 选择的结构化数据类型是否适合内容类型（例如：文章适用于博客，产品适用于电子商务等）
- 是否提供了所有必需的数据（根据结构化数据类型，如作者信息、日期、价格等）
- 确认内容是否符合生成丰富搜索结果的条件

### 输出验证
- JSON 语法是否正确（无多余的逗号，引号使用正确）
- 是否为所选的结构化数据类型提供了所有必需的属性
- URL 是否为绝对路径（而非相对路径）
- 日期是否采用 ISO 8601 格式（YYYY-MM-DDTHH:MM:SS+00:00）
- 结构化数据内容是否与页面实际显示的内容完全一致
- 通过结构化数据验证工具的检查（无错误）
- 明确标注每个数据点的来源（来自网络爬虫提取、用户提供或手动输入）

## 示例

**用户请求：** 为一篇关于 SEO 的页面生成常见问题解答（FAQ）结构化数据

**输出：**

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
      "name": "什么是 SEO？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO（搜索引擎优化）是指通过优化网站和内容来提高在搜索结果页面（SERPs）中的排名。它包括技术优化、内容创作和链接建设，以增加网站的自然曝光率并吸引目标流量。"
      }
    },
    {
      "@type": "Question",
      "name": "SEO 需要多长时间才能见效？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO 通常需要 3-6 个月才能看到显著效果，但这取决于竞争情况、网站权威度和投入的努力。新网站可能需要 6-12 个月，而具有现有权威度的网站在竞争较少的关键词上可能在 1-3 个月内看到改进。"
      }
    },
    {
      "@type": "Question",
      "name": "SEO 比付费广告更好吗？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO 和付费广告有不同的作用。SEO 可以提供可持续的长期流量，且无需每次点击付费，但需要时间来建立效果。付费广告可以立即带来流量，但在停止支付后效果也会消失。大多数成功的企业会同时使用这两种方式：付费广告用于快速获取潜在客户，SEO 用于长期发展。"
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
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "什么是 SEO？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO（搜索引擎优化）是指通过优化网站和内容来提高在搜索结果页面（SERPs）中的排名。它包括技术优化、内容创作和链接建设，以增加网站的自然曝光率并吸引目标流量。"
      }
    },
    {
      "@type": "Question",
      "name": "SEO 需要多长时间才能见效？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO 通常需要 3-6 个月才能看到显著效果，但这取决于竞争情况、网站权威度和投入的努力。新网站可能需要 6-12 个月，而具有现有权威度的网站在竞争较少的关键词上可能在 1-3 个月内看到改进。」
      }
    },
    {
      "@type": "Question",
      "name": "SEO 比付费广告更好吗？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO 和付费广告有不同的作用。SEO 可以提供可持续的长期流量，且无需每次点击付费，但需要时间来建立效果。付费广告可以立即带来流量，但在停止支付后效果也会消失。大多数成功的企业会同时使用这两种方式：付费广告用于快速获取潜在客户，SEO 用于长期发展。」
      }
    }
  ]
}
```

### Validation

Test with ~~schema validator

### SERP Preview

```
SEO 指南：全面初学者教程
yoursite.com/seo-guide/
从零开始学习 SEO，通过我们的综合指南...

▼ 什么是 SEO？
  SEO（搜索引擎优化）是指通过优化网站和内容来提高在搜索结果页面（SERPs）中的排名...
▼ SEO 需要多长时间才能见效？
  SEO 通常需要 3-6 个月才能看到显著效果...
▼ SEO 比付费广告更好吗？
  SEO 和付费广告有不同的作用...

```
```

## 结构化数据类型快速参考

| 内容类型 | 结构化数据类型 | 关键属性 |
|--------------|-------------|----------------|
| 博文文章 | BlogPosting/Article | headline, datePublished, author |
| 产品 | Product | name, price, availability |
| 常见问题解答 | FAQPage | Question, Answer |
| 操作指南 | HowTo | step, totalTime |
| 本地商家 | LocalBusiness | address, geo, openingHours |
| 食谱 | Recipe | ingredients, cookTime |
| 活动 | Event | startDate, location |
| 视频 | VideoObject | uploadDate, duration |
| 课程 | Course | provider, name |
| 评论 | Review | itemReviewed, ratingValue |

## 成功技巧

1. **确保结构化数据与页面实际显示的内容一致**
2. **避免滥用** - 仅对相关内容添加结构化数据
3. **保持数据更新** - 当数据发生变化时及时更新日期和价格
4. **彻底测试** - 部署前进行验证
5. **监控搜索控制台** - 注意错误和警告

## 结构化数据类型决策树

### 根据内容选择合适的结构化数据类型

| 内容类型 | 主要使用的结构化数据类型 | 如适用可添加的其他结构化数据类型 | 是否适合生成丰富的搜索结果 |
|-------------|---------------|-------------------|----------------------|
| 博文文章 | Article | FAQ, HowTo | 文章轮播、FAQ 结果 |
| 产品页面 | Product | Review, Offer, AggregateRating | 带有价格/评分的产品摘要 |
| 服务页面 | Service | FAQ, LocalBusiness | 服务摘要 |
| 操作指南 | HowTo | Article, FAQ | 带有步骤的操作指南结果 |
| 常见问题解答页面 | FAQPage | Article | SERP 中的 FAQ 折叠面板 |
| 食谱 | Recipe | Video, AggregateRating | 食谱轮播 |
| 活动 | Event | Offer, Organization | 带有日期/地点的活动摘要 |
| 视频 | VideoObject | Article | 视频轮播、关键时刻 |
| 本地商家 | LocalBusiness | Review, OpeningHoursSpecification | 本地商家信息、知识面板 |
| 个人/作者 | Person | Organization | 个人资料、组织信息 | 知识面板 |
| 组织 | Organization | ContactPoint, Logo | 信息面板 |
| 课程 | Course | Organization | 课程信息 | 课程结果 |
| 招聘信息 | JobPosting | Organization | Google for Jobs 招聘信息 |
| 导航栏 | BreadcrumbList | （始终与其他结构化数据一起添加） | SERP 中的导航栏 |
| 软件/应用 | SoftwareApplication | Review, Offer | 应用程序摘要 |

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

## 结构化数据实施优先级

| 优先级 | 结构化数据类型 | 原因 |
|----------|-------------|-----|
| P0 -- 必须添加 | Organization, BreadcrumbList, WebSite (SearchAction) | 所有网站的基础 |
| P1 -- 核心内容 | Article, FAQPage, HowTo | 直接生成丰富的搜索结果 |
| P2 -- 商业内容 | Product, Review, AggregateRating, Offer | 有助于增加收入的丰富结果 |
| P3 -- 增强权威性 | Person, SameAs, Speakable | 有助于提升搜索引擎排名 |
| P4 -- 专业领域 | 行业特定的结构化数据类型 | 生成特定领域的丰富结果 |

## 结构化数据验证快速参考

| 问题 | 影响 | 解决方法 |
|-------|--------|-----|
| 缺少必需的属性 | Google 会忽略该结构化数据 | 添加所有必需的字段（参考 schema.org） |
| 日期格式错误 | 可能导致结构化数据无法被正确解析 | 使用 ISO 8601 格式（例如：2026-02-11） |
| 使用错误的类型 | 结构化数据可能被误解 | 确保类型与 schema.org 中的定义完全匹配 |
| self-referencing sameAs （自我引用） | 可能导致错误 | sameAs 应该链接到外部个人资料 |
| 文章缺少图片 | 会导致文章无法显示为丰富搜索结果 | 添加带有有效 URL 的图片属性 |
| 评论缺少 itemReviewed | 评论无法显示 | 将评论嵌套在 Product/Service 等结构化数据中 |

## 参考资料

- [结构化数据模板](./references/schema-templates.md) - 所有结构化数据类型的现成 JSON-LD 模板
- [验证指南](./references/validation-guide.md) - 常见错误、必需的属性、测试流程

## 相关技能

- [seo-content-writer](../seo-content-writer/) — 创建适合标记的结构化内容
- [geo-content-optimizer](../geo-content-optimizer/) — 优化常见问题解答内容
- [on-page-seo-auditor](../../optimize/on-page-seo-auditor/) — 审查现有的结构化数据
- [technical-seo-checker](../../optimize/technical-seo-checker/) — 进行技术验证
- [entity-optimizer](../../cross-cutting/entity-optimizer/) — 审查 Person、Organization、Product 等实体信息 |
- [meta-tags-optimizer](../meta-tags-optimizer/) — 优化元标签和结构化数据