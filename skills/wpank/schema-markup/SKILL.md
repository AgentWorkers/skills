---
name: schema-markup
model: fast
version: 1.0.0
description: >
  Add, fix, or optimize schema markup and structured data. Use when the user mentions
  schema markup, structured data, JSON-LD, rich snippets, schema.org, FAQ schema,
  product schema, review schema, or breadcrumb schema.
tags: [seo, schema, structured-data, json-ld, rich-snippets, search]
---

# 架构标记（Schema Markup）

实现 schema.org 标记，帮助搜索引擎理解页面内容，并在搜索结果中呈现更丰富的信息。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install schema-markup
```

## 使用场景

- 为新页面或现有页面添加结构化数据
- 修复架构验证错误
- 优化特定类型的搜索结果（如常见问题解答、产品信息、文章等）
- 在 React/Next.js 应用程序中实现 JSON-LD
- 审查现有的架构标记

## 初始评估

在实施架构标记之前，请了解以下内容：

1. **页面类型**：页面属于哪种类型？主要内容包括什么？可以呈现哪些类型的搜索结果？
2. **当前状态**：页面上是否存在现有的架构标记？是否存在验证错误？已经出现了哪些类型的搜索结果？
3. **目标**：希望实现哪些类型的搜索结果？这些搜索结果对业务有什么价值？

## 核心原则

### 1. 准确性优先
- 架构标记必须准确反映页面内容
- 不要标记页面上不存在的内容
- 内容发生变化时及时更新标记信息

### 2. 使用 JSON-LD
- Google 推荐使用 JSON-LD 格式
- 比 microdata 或 RDFa 更易于实现和维护
- 将 JSON-LD 标记放置在 `<head>` 标签内或 `</body>` 标签之前

### 3. 遵循 Google 的指南
- 仅使用 Google 支持的架构标记格式
- 避免使用垃圾信息（spam）策略
- 查看每种类型的具体要求

### 4. 全部内容进行验证
- 部署前进行测试
- 定期查看 Search Console 的优化报告
- 及时修复错误

## 常见架构类型

| 类型 | 适用场景 | 必需属性 |
|------|---------|-------------------|
| Organization（组织页面） | 公司主页/关于页面 | name, url |
| WebSite（网站） | 主页（包含搜索框） | name, url |
| Article（文章） | 博文、新闻 | headline, image, datePublished, author |
| Product（产品） | 产品页面 | name, image, offers |
| SoftwareApplication（软件应用） | SaaS 或应用页面 | name, offers |
| FAQPage（常见问题解答页面） | 常见问题及答案 | mainEntity（问答对数组） |
| HowTo（操作指南） | 教程 | name, step |
| BreadcrumbList（导航路径列表） | 包含导航路径的页面 | itemListElement |
| LocalBusiness（本地商家） | 本地商家页面 | name, address |
| Event（活动） | 活动、网络研讨会 | name, startDate, location |

**有关包含所需/推荐字段的 JSON-LD 示例，请参阅 `references/schema-examples.md`**

## 快速参考

### Organization（组织页面）
- 必需属性：name, url
- 推荐属性：logo, sameAs（用于关联社交媒体账号）、contactPoint

### Article/BlogPosting（文章/博客帖子）
- 必需属性：headline, image, datePublished, author
- 推荐属性：dateModified, publisher, description

### Product（产品）
- 必需属性：name, image, offers（价格、库存状态）
- 推荐属性：sku, brand, aggregateRating, review

### FAQPage（常见问题解答页面）
- 必需属性：mainEntity（问答对数组）

### BreadcrumbList（导航路径列表）
- 必需属性：itemListElement（包含位置、名称和项目的数组）

## 在一个页面上结合多种架构类型

可以使用 `@graph` 标签来组合多种架构类型：

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", "..." : "..." },
    { "@type": "WebSite", "..." : "..." },
    { "@type": "BreadcrumbList", "..." : "..." }
  ]
}
```

使用 `@id` 来创建可引用的实体——定义一次后，可以在其他地方通过 `{ "@id": "..." }` 来引用。

## 验证与测试

### 工具
- **Google Rich Results Test**：https://search.google.com/test/rich-results
- **Schema.org Validator**：https://validator.schema.org/
- **Search Console**：优化报告

### 常见错误

| 错误类型 | 原因 | 修复方法 |
|-------|-------|-----|
| 缺少必需字段 | 未包含必需的属性 | 添加缺失的属性 |
| URL 不合法 | 相对 URL 或格式错误 | 使用完整的 URL（例如 `https://...`） |
| 日期格式错误 | 不符合 ISO 8601 标准 | 使用 `YYYY-MM-DDTHH:MM:SS+00:00` 格式 |
| 枚举值错误 | 使用错误的枚举值 | 使用 schema.org 定义的枚举值（例如 `https://schema.org/InStock`） |
| 内容不匹配 | 架构标记与实际页面内容不符 | 确保架构标记与页面内容一致 |
| 价格格式错误 | 包含货币符号或逗号 | 价格应仅使用数字格式（例如 `149.99`） |

## 实施方法

### 静态网站
- 直接在 HTML 模板中添加 JSON-LD 标记
- 使用 includes/partials 等方法实现可复用的架构标记

### 动态网站（React、Next.js）
```tsx
export function JsonLd({ data }: { data: Record<string, unknown> }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
```

### 内容管理系统（CMS）/WordPress
- 插件：Yoast、Rank Math、Schema Pro
- 根据需要修改主题以支持自定义架构类型
- 将自定义字段映射到结构化数据中

## 测试检查清单

- [ ] 在 Google Rich Results Test 中测试且无错误
- [ ] 推荐的属性没有警告
- [ ] 架构标记内容与页面实际内容一致
- [ ] 每种类型都包含了所有必需的属性
- [ ] URL 是完整的
- [ ] 日期格式符合 ISO 8601 标准
- [ ] 价格为纯数字格式（不含货币符号）

## 任务相关问题

在实施之前，请回答以下问题：

1. 这是一个什么类型的页面？（产品页面、文章页面、常见问题解答页面、本地商家页面）
2. 希望实现哪些类型的搜索结果？（例如常见问题解答的下拉菜单、产品评分、导航路径）
3. 有哪些数据可以用于填充架构标记？（价格、评分、日期等）
4. 页面上是否已经存在架构标记？（先使用 Google Rich Results Test 进行检查）
5. 你的技术栈是什么？（静态 HTML、React/Next.js、CMS/WordPress）

## 实施流程

1. **确定页面类型**：将网站页面与相应的架构类型对应起来
2. **从首页开始**：先实现 Organization 和 WebSite 类型的架构标记
3. **为每个页面添加相应的架构标记**：博客页面添加 Article 类型标记，产品页面添加 Product 类型标记等
4. **添加导航路径列表**：所有包含导航路径的页面都需要添加 BreadcrumbList
5. **验证每个页面**：部署前后使用 Google Rich Results Test 进行测试
6. **定期监控 Search Console**：部署后每周查看优化报告

## 绝对不要做的事情

- **绝对不要为页面上不存在的内容添加架构标记**：这违反 Google 的指南，可能会导致处罚
- **当可以选择 JSON-LD 时，绝对不要使用 microdata 或 RDFa**：JSON-LD 更易于维护，也是 Google 推荐的格式
- **绝对不要将应该动态变化的内容硬编码到架构标记中**：产品价格、库存状态和评分等数据应实时更新
- **部署前绝对不要跳过验证**：无效的架构标记比没有架构标记更糟糕，会浪费搜索引擎的爬取资源
- **绝对不要对所有页面使用相同的架构标记**：不同类型的页面需要使用相应的架构类型
- **绝对不要忽略 Search Console 的错误**：架构错误可能导致搜索结果完全消失