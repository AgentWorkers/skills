---
name: schema-markup
description: 当用户需要在其网站上添加、修改或优化结构化数据（structured data）及相应的标记（schema markup）时，可以使用此功能。此外，当用户提到“schema markup”、“structured data”、“JSON-LD”、“rich snippets”、“schema.org”、“FAQ schema”、“product schema”、“review schema”或“breadcrumb schema”等术语时，也适用此功能。对于更广泛的SEO相关问题，请参阅“seo-audit”。
---

# 架构标记（Schema Markup）

您是结构化数据和架构标记方面的专家。您的目标是实现 schema.org 的标记规范，以帮助搜索引擎理解页面内容，并在搜索结果中呈现更丰富、更有用的信息。

## 初始评估

在实施架构标记之前，请了解以下内容：

1. **页面类型**
   - 这是一个什么样的页面？
   - 主要内容是什么？
   - 可以实现哪些丰富的搜索结果？

2. **当前状态**
   - 现在是否有已存在的架构标记？
   - 当前的实现是否存在错误？
   - 哪些丰富的搜索结果已经出现了？

3. **目标**
   - 您希望实现哪些丰富的搜索结果？
   - 这些目标对业务有什么价值？

---

## 核心原则

### 1. 准确性第一
- 架构标记必须准确反映页面内容
- 不要标记不存在的内容
- 内容发生变化时要及时更新标记

### 2. 使用 JSON-LD 格式
- Google 推荐使用 JSON-LD 格式
- 更易于实现和维护
- 应放置在 `<head>` 标签中或 `<body>` 的末尾

### 3. 遵循 Google 的指南
- 仅使用 Google 支持的标记格式
- 避免使用垃圾信息策略
- 查看相关资格要求

### 4. 验证所有内容
- 部署前进行测试
- 监控 Search Console 的反馈
- 及时修复错误

---

## 常见的架构标记类型

### **组织（Organization）**
**适用场景**：公司/品牌的主页或关于页面

**必填属性**：
- name（名称）
- url（网址）

**推荐属性**：
- logo（徽标）
- sameAs（用于关联社交媒体账号）
- contactPoint（联系方式）

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Company",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/example",
    "https://linkedin.com/company/example",
    "https://facebook.com/example"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-555-5555",
    "contactType": "customer service"
  }
}
```

### **网站（包含 SearchAction）**
**适用场景**：主页，用于启用站点链接搜索框

**必填属性**：
- name（名称）
- url（网址）

**针对搜索框的属性**：
- potentialAction（用于指定搜索操作，例如“查看详情”）

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Example",
  "url": "https://example.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://example.com/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

### **文章/博客帖子（Article/BlogPosting）**
**适用场景**：博客文章、新闻文章

**必填属性**：
- headline（标题）
- image（图片）
- datePublished（发布日期）
- author（作者）

**推荐属性**：
- dateModified（修改日期）
- publisher（发布者）
- description（描述）
- mainEntityOfPage（页面的主要实体）

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to Implement Schema Markup",
  "image": "https://example.com/image.jpg",
  "datePublished": "2024-01-15T08:00:00+00:00",
  "dateModified": "2024-01-20T10:00:00+00:00",
  "author": {
    "@type": "Person",
    "name": "Jane Doe",
    "url": "https://example.com/authors/jane"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Example Company",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "description": "A complete guide to implementing schema markup...",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/schema-guide"
  }
}
```

### **产品（Product）**
**适用场景**：产品页面（电子商务或 SaaS 服务）

**必填属性**：
- name（产品名称）
- image（产品图片）
- offers（产品信息，包括价格和库存情况）

**推荐属性**：
- description（产品描述）
- sku（商品编号）
- brand（品牌）
- aggregateRating（综合评分）
- review（用户评价）

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Premium Widget",
  "image": "https://example.com/widget.jpg",
  "description": "Our best-selling widget for professionals",
  "sku": "WIDGET-001",
  "brand": {
    "@type": "Brand",
    "name": "Example Co"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/products/widget",
    "priceCurrency": "USD",
    "price": "99.99",
    "availability": "https://schema.org/InStock",
    "priceValidUntil": "2024-12-31"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "127"
  }
}
```

### **软件应用（SoftwareApplication）**
**适用场景**：SaaS 产品页面、应用程序的登录页面

**必填属性**：
- name（应用程序名称）
- offers（产品信息，包括是否免费）

**推荐属性**：
- applicationCategory（应用程序类别）
- operatingSystem（操作系统）
- aggregateRating（综合评分）

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Example App",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web, iOS, Android",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.6",
    "ratingCount": "1250"
  }
}
```

### **常见问题解答页面（FAQPage）**
**适用场景**：包含常见问题的页面

**必填属性**：
- mainEntity（问题/答案的数组）

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is schema markup?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Schema markup is a structured data vocabulary that helps search engines understand your content..."
      }
    },
    {
      "@type": "Question",
      "name": "How do I implement schema?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The recommended approach is to use JSON-LD format, placing the script in your page's head..."
      }
    }
  ]
}
```

### **操作指南（HowTo）**
**适用场景**：教学内容、教程

**必填属性**：
- name（指南名称）
- step（操作步骤的数组）

**推荐属性**：
- image（指南图片）
- totalTime（完成时间）
- estimatedCost（预计成本）
- supply/tool（所需工具）

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Add Schema Markup to Your Website",
  "description": "A step-by-step guide to implementing JSON-LD schema",
  "totalTime": "PT15M",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Choose your schema type",
      "text": "Identify the appropriate schema type for your page content...",
      "url": "https://example.com/guide#step1"
    },
    {
      "@type": "HowToStep",
      "name": "Write the JSON-LD",
      "text": "Create the JSON-LD markup following schema.org specifications...",
      "url": "https://example.com/guide#step2"
    },
    {
      "@type": "HowToStep",
      "name": "Add to your page",
      "text": "Insert the script tag in your page's head section...",
      "url": "https://example.com/guide#step3"
    }
  ]
}
```

### **面包屑导航（BreadcrumbList）**
**适用场景**：任何具有面包屑导航的页面

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Blog",
      "item": "https://example.com/blog"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "SEO Guide",
      "item": "https://example.com/blog/seo-guide"
    }
  ]
}
```

### **本地企业（LocalBusiness）**
**适用场景**：本地企业的位置信息页面

**必填属性**：
- name（企业名称）
- address（企业地址）
- （根据企业类型添加其他相关属性）

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Example Coffee Shop",
  "image": "https://example.com/shop.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main Street",
    "addressLocality": "San Francisco",
    "addressRegion": "CA",
    "postalCode": "94102",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "37.7749",
    "longitude": "-122.4194"
  },
  "telephone": "+1-555-555-5555",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "08:00",
      "closes": "18:00"
    }
  ],
  "priceRange": "$$"
}
```

### **评论/综合评分（Review/AggregateRating）**
**适用场景**：包含用户评论的产品页面

**注意**：自我评价的评论（例如评价自己的产品）是不符合指南的。评论必须来自真实客户。

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Example Product",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "bestRating": "5",
    "worstRating": "1",
    "ratingCount": "523"
  },
  "review": [
    {
      "@type": "Review",
      "author": {
        "@type": "Person",
        "name": "John Smith"
      },
      "datePublished": "2024-01-10",
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "5"
      },
      "reviewBody": "Excellent product, exceeded my expectations..."
    }
  ]
}
```

### **活动（Event）**
**适用场景**：活动页面、网络研讨会、会议

**必填属性**：
- name（活动名称）
- startDate（开始日期）
- location（活动地点；在线活动时使用 eventAttendanceMode）

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Annual Marketing Conference",
  "startDate": "2024-06-15T09:00:00-07:00",
  "endDate": "2024-06-15T17:00:00-07:00",
  "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
  "eventStatus": "https://schema.org/EventScheduled",
  "location": {
    "@type": "VirtualLocation",
    "url": "https://example.com/conference"
  },
  "image": "https://example.com/conference.jpg",
  "description": "Join us for our annual marketing conference...",
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/conference/tickets",
    "price": "199",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "validFrom": "2024-01-01"
  },
  "performer": {
    "@type": "Organization",
    "name": "Example Company"
  },
  "organizer": {
    "@type": "Organization",
    "name": "Example Company",
    "url": "https://example.com"
  }
}
```

---

## 单个页面上使用多种架构标记类型

您可以在一个页面上使用多种架构标记类型（通常也是推荐的做法）：

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "Example Company",
      "url": "https://example.com"
    },
    {
      "@type": "WebSite",
      "@id": "https://example.com/#website",
      "url": "https://example.com",
      "name": "Example",
      "publisher": {
        "@id": "https://example.com/#organization"
      }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [...]
    }
  ]
}
```

---

## 验证与测试

### 工具
- **Google 富富结果测试**：https://search.google.com/test/rich-results
- **Schema.org 验证工具**：https://validator.schema.org/
- **Search Console**：提供相关优化报告

### 常见错误

- **缺少必填属性**：检查 Google 的文档以确认所需字段
- **值无效**：日期必须符合 ISO 8601 格式；URL 必须完整；枚举值必须准确无误
- **与页面内容不符**：架构标记与实际显示的内容不一致
- **产品无评论时显示评分**：无评论的产品不应显示评分
- **价格不一致**：显示的价格与实际价格不符

---

## 实现方式

### **静态网站**
- 直接在 HTML 模板中添加 JSON-LD 标记
- 使用包含（includes）或部分（partials）代码片段来实现可复用的架构标记

### **动态网站（React、Next.js 等）**
- 使用组件来渲染架构标记
- 通过服务器端渲染来优化搜索引擎排名（SEO）
- 将数据序列化为 JSON-LD 格式

```jsx
// Next.js example
export default function ProductPage({ product }) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "Product",
    name: product.name,
    // ... other properties
  };

  return (
    <>
      <Head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
        />
      </Head>
      {/* Page content */}
    </>
  );
}
```

### **内容管理系统（CMS）/ WordPress**
- 使用插件（如 Yoast、Rank Math、Schema Pro）来辅助实现
- 通过主题定制来添加结构化数据

---

## 输出格式

### 架构标记的实现方式

```json
// Full JSON-LD code block
{
  "@context": "https://schema.org",
  "@type": "...",
  // Complete markup
}
```

### 代码放置位置及方法

- 说明代码应放置的位置以及如何添加

### 测试检查清单
- [ ] 在 Google 富富结果测试中通过验证
- [ ] 无错误或警告
- [ ] 与页面内容一致
- [ ] 所有必填属性都已包含

---

## 需要咨询的问题

如果您需要更多信息，请提出以下问题：
1. 这是一个什么样的页面？
2. 您希望实现哪些丰富的搜索结果？
3. 有哪些数据可以用来填充架构标记？
4. 页面上是否已有现有的架构标记？
5. 您使用的实现技术栈是什么？

---

## 相关技能

- **SEO 审计（seo-audit）**：用于整体 SEO 优化，包括架构标记的检查
- **程序化 SEO（programmatic-seo）**：用于大规模的模板化架构标记管理
- **分析跟踪（analytics-tracking）**：用于衡量架构标记对搜索结果的影响