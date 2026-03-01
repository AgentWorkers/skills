---
name: website-seo
version: 1.0.0
description: 适用于任何网站的完整页面SEO系统——包括页面优化、结构化数据标记（schema markup）、技术SEO检查清单、内部链接策略、Core Web Vitals指标指导，以及基于AI的内容差距分析功能。该系统兼容所有内容管理系统（CMS），如WordPress、Webflow、Squarespace或自定义系统。
tags: [seo, on-page-seo, technical-seo, schema-markup, core-web-vitals, wordpress, content-optimization]
author: contentai-suite
license: MIT
---
# 网站SEO——通用页面优化系统

## 该技能的功能

本技能将指导您完成整个网站SEO审计和优化流程，涵盖页面元素、技术基础、结构化数据标记（Schema Markup）以及长期实施的优化策略。

## 如何使用该技能

**输入格式：**
```
WEBSITE URL: [Your website]
CMS: [WordPress / Webflow / Squarespace / Shopify / Custom]
NICHE: [Your industry]
TARGET LOCATION: [Local / National / Global]
PRIORITY PAGES: [Homepage / Service pages / Blog / Product pages]
CURRENT ISSUES: [Known issues or "unknown — need full audit"]
GOAL: [Rank for specific keywords / Improve existing rankings / Fix technical issues]
```

---

## 第1阶段：页面级优化

### 标题标签优化

**格式：** `主要关键词 — 次要关键词 | 品牌名称`

```
Rules:
- 50-60 characters maximum
- Primary keyword as close to the beginning as possible
- Each page must have a UNIQUE title
- Make it compelling for humans, not just crawlers

Bad: "Home | Company Name"
Good: "Personal Training Rotterdam — 1-on-1 Coaching | Brand Name"
```

### 元描述优化

**格式：** `[优势] + [主要关键词] + [呼叫行动（CTA）`

```
Rules:
- 150-160 characters
- Include primary keyword naturally
- Include a call-to-action
- Each page must have a UNIQUE meta description
- Think of it as a micro-ad for your page in search results

Prompt to generate:
"Write a meta description for a [PAGE TYPE] page about [TOPIC] for [BRAND NAME].
Primary keyword: [KEYWORD]. Audience: [AUDIENCE].
Max 155 characters. Include a benefit + soft CTA."
```

### 标题层级结构（H1-H6）

```
Rules:
- ONE H1 per page — contains primary keyword
- H2s: section headers — contain secondary/LSI keywords
- H3s: subsections
- Never skip levels (don't go H1 → H3)
- Headers should describe the content below them accurately

Audit prompt:
"Review the heading structure of this page: [paste page content]
Identify: missing H1, keyword opportunities in headers, hierarchy issues."
```

### 内容优化

```
On-Page Content Checklist:
- [ ] Primary keyword in first 100 words
- [ ] Primary keyword appears naturally throughout (1-2% density)
- [ ] LSI keywords (related terms) used throughout
- [ ] Minimum 300 words for service pages, 800+ for blog posts
- [ ] Content answers the search intent (informational/commercial/navigational)
- [ ] Internal links to 2-3 relevant pages on your site
- [ ] External link to 1 authoritative source
- [ ] All images have descriptive alt text

Content optimization prompt:
"Optimize this content for the keyword [KEYWORD]:
[Paste your existing content]
Suggest: where to add the keyword naturally, missing LSI terms,
structural improvements, and any thin content sections to expand."
```

---

## 第2阶段：技术SEO基础

### 核心技术检查清单

```
INDEXABILITY:
- [ ] robots.txt exists and doesn't block important pages
- [ ] XML sitemap submitted to Google Search Console
- [ ] No important pages with noindex tag
- [ ] Canonical tags set correctly

PERFORMANCE:
- [ ] Page loads under 3 seconds (test: PageSpeed Insights)
- [ ] Images compressed and in WebP format where possible
- [ ] Minified CSS and JavaScript
- [ ] Browser caching enabled

MOBILE:
- [ ] Mobile-responsive design
- [ ] No intrusive interstitials on mobile
- [ ] Tap targets large enough (48×48px minimum)
- [ ] Text readable without zooming

CRAWLABILITY:
- [ ] Clean URL structure (yoursite.com/service-name not yoursite.com/p=123)
- [ ] No broken internal links
- [ ] No redirect chains (A→B→C, should be A→C directly)
- [ ] HTTPS enabled on all pages

CORE WEB VITALS:
- [ ] LCP (Largest Contentful Paint) < 2.5 seconds
- [ ] CLS (Cumulative Layout Shift) < 0.1
- [ ] FID/INP (Interaction to Next Paint) < 200ms
```

### URL结构最佳实践

```
Good URL structure:
yoursite.com/service/keyword-based-page-name
yoursite.com/blog/topic-keyword-post-title

Bad URL structure:
yoursite.com/page?id=123
yoursite.com/2024/01/01/blog/post
yoursite.com/my-awesome-service-page-click-here

Rules:
- Use hyphens (-) not underscores (_)
- Lowercase only
- Include primary keyword
- Remove stop words (the, a, and, or) where possible
- Keep it short — under 60 characters ideal
```

---

## 第3阶段：结构化数据标记（Schema Markup）

结构化数据标记能向搜索引擎准确说明您的内容含义，从而生成更丰富的搜索结果展示。

### 最有价值的结构化数据类型

**本地企业（针对地理位置相关的业务）：**
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "[Business Name]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[Street]",
    "addressLocality": "[City]",
    "postalCode": "[Code]",
    "addressCountry": "[Country Code]"
  },
  "telephone": "[Phone]",
  "url": "[Website URL]",
  "openingHours": ["Mo-Fr 09:00-17:00"],
  "priceRange": "$$"
}
```

**文章/博客帖子：**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Post Title]",
  "author": {"@type": "Person", "name": "[Author Name]"},
  "datePublished": "[ISO Date]",
  "description": "[Meta Description]"
}
```

**常见问题解答（FAQ）：**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "[Question text]",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "[Answer text]"
    }
  }]
}
```

**结构化数据生成提示：**
```
Generate [SCHEMA TYPE] schema markup for [BUSINESS NAME].
Details: [provide business details, page content, or FAQ content]
Output: valid JSON-LD format ready to add to the page <head>
```

---

## 第4阶段：内部链接策略

内部链接有助于分配页面权重，并帮助用户浏览您的网站。

**中心辐射式链接结构（Hub and Spoke Model）：**
```
PILLAR PAGE (broad topic) → linked to by all related pages
CLUSTER PAGES (specific subtopics) → each links back to pillar page

Example:
Pillar: "Ultimate Guide to [Your Service]"
Clusters:
- "[Specific aspect 1] Explained"
- "How to [specific task] — Step by Step"
- "[Topic] for Beginners"
- "[Advanced topic] Guide"
```

**内部链接规则：**
- 从高流量页面链接到您希望提升排名的页面
- 使用描述性的锚文本（避免使用“点击这里”或“阅读更多”）
- 每个新页面或文章添加2-3个内部链接
- 每季度检查一次失效的内部链接

---

## 第5阶段：持续SEO监控

### 每月SEO审计检查清单

```
RANKING:
- [ ] Check Google Search Console for position changes
- [ ] Identify keywords dropped — investigate why
- [ ] Find new keyword opportunities from "Queries" report

TECHNICAL:
- [ ] Check for new crawl errors in GSC
- [ ] Review Core Web Vitals report
- [ ] Check any new 404 errors

CONTENT:
- [ ] Update any outdated statistics or information
- [ ] Add internal links from new content to older pages
- [ ] Identify thin pages (under 300 words) for expansion
```

### SEO审计提示
```
I'm auditing [WEBSITE URL] for [NICHE] targeting [KEYWORDS].
Based on SEO best practices, identify the top 10 issues to fix.
Priority order: technical issues → on-page → content gaps → link opportunities.
Format: Issue | Impact (High/Medium/Low) | Recommended fix
```

---

## 与ContentAI Suite配合使用

本技能可与**[ContentAI Suite](https://contentai-suite.vercel.app)**无缝集成——这是一个免费的多代理营销平台，能够为任何企业快速生成专业内容。

→ **免费试用：** https://contentai-suite.vercel.app