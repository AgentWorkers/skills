---
name: schemaorg-site-enhancer
description: 该工具能够通过添加适当的 schema.org 结构化数据来提升由代理程序生成的网站的 SEO 效果、丰富网页内容，并提高其在搜索引擎中的可见性。适用于在创建或优化网站时为组织、产品、文章、事件等添加 JSON-LD 标记。同时提供相应的模板、生成工具以及验证指南。
---
# Schema.org 网站增强工具

## 概述

该工具帮助开发人员将 schema.org 结构化数据集成到网站中，从而实现更丰富的搜索结果、更好的搜索引擎优化（SEO），以及与搜索引擎的更有效沟通。它提供了现成的 JSON-LD 模板、生成脚本以及针对常见数据类型的实现模式。

## 适用场景

- 在新建需要优化 SEO 的网站时
- 为现有网站添加 schema.org 标记
- 为组织、产品、文章、博客文章、事件、常见问题解答（FAQ）或本地商家信息生成 JSON-LD
- 根据 schema.org 标准验证标记的正确性
- 为重复出现的网站类型创建可重用的模板

**触发条件**：
- “为该网站添加 schema.org 标记”
- “为 [产品/文章/事件] 生成 JSON-LD”
- “通过结构化数据提升 SEO”
- “为 [类型] 创建模板”
- “验证我的 schema.org 实现”

## 核心功能

1. **JSON-LD 模板生成** – 为 15 种以上常见数据类型生成可插入的 JSON-LD 脚本
2. **自定义数据结构构建** – 根据用户提供的详细信息构建定制的结构化数据
3. **验证指导** – 根据 schema.org 规范和 Google 的丰富结果指南检查标记
4. **模板复用** – 在多个页面/网站中保持一致的结构化数据
5. **自动集成模式** – 提供将 schema 数据注入 HTML 框架（如 React、Next.js、纯 HTML）的指导

## 快速入门

### 基本用法

当用户请求添加 schema.org 标记时：
1. 确定所需的数据类型（组织、产品、文章等）
2. 从用户或现有网站内容中收集所需属性
3. 使用相应的模板生成 JSON-LD
4. 提供将 `<script type="application/ld+json">` 添加到 HTML 中的指导
5. （可选）使用 Google 的丰富结果测试进行验证

### 示例请求

- “为我的自由职业作品集添加 schema.org 标记” → 组织 + 个人
- “我出售手工珠宝，需要添加产品数据结构” → 包含价格、可用性、品牌的产品信息
- “我的博客需要文章结构化数据以提升 SEO” → 包含作者、日期、图片的博客文章
- “我们举办技术研讨会，需要添加事件数据结构” → 包含地点、日期、组织者的事件信息
- “为这个页面创建 FAQ 数据结构” → 包含问题和答案的 FAQ 页面

## 支持的数据类型

### 必需类型（始终可用）
- **Organization** – 公司、机构、组织
- **Person** – 个人资料
- **WebSite** – 网站级元数据
- **WebPage** – 通用页面标记
- **Article** / **BlogPosting** – 新闻和博客内容

### 商业相关类型
- **Product** – 在售商品（价格、可用性、SKU）
- **Offer** – 价格和可用性详情
- **AggregateRating** – 评论摘要
- **Brand** – 制造商或品牌信息

### 本地与事件相关类型
- **LocalBusiness** – 实体商家位置
- **Place** – 通用位置数据
- **Event** – 研讨会、会议、网络研讨会
- **Venue** – 活动地点

### 内容与媒体相关类型
- **VideoObject** – 嵌入式视频
- **ImageObject** – 照片和图形
- **AudioObject** – 播客、音频片段

### 交互式类型
- **FAQPage** – 常见问题解答
- **HowTo** – 分步指南
- **Recipe** – 烹饪步骤（食材、步骤、营养信息）
- **Review** – 个人评价

## 实现模式

### 模式 1：静态 HTML 注入

对于纯 HTML 或静态网站，直接在 `<head>` 中添加 JSON-LD：

```html
<head>
  <!-- other head content -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Your Company",
    "url": "https://example.com",
    "logo": "https://example.com/logo.png"
  }
  </script>
</head>
```

### 模式 2：React / Next.js 组件

创建可重用的组件：

```jsx
// components/JsonLd.js
export function JsonLd({ data }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}

// Usage in page:
<JsonLd data={{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Your Post Title",
  "author": { "@type": "Person", "name": "Author Name" },
  "datePublished": "2025-02-20T10:00:00Z"
}} />
```

### 模式 3：模板变量

使用占位符表示动态值：

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{{product_name}}",
  "description": "{{product_description}}",
  "offers": {
    "@type": "Offer",
    "price": "{{price}}",
    "priceCurrency": "USD"
  }
}
```

将 `{{variables}}` 替换为实际数据。

## 最佳实践

- **使用 JSON-LD** – 更易于维护的格式
- **保持更新** – schema.org 会不断更新；使用稳定版本（`@context: "https://schema.org"`）
- **仅包含相关属性** – 优先考虑质量而非数量；避免空字段
- **进行验证** – 使用 Google 的丰富结果测试或 schema.org 验证工具
- **测试丰富结果** – 并非所有数据类型都能生成丰富显示；遵循 Google 的指南
- **避免重复** – 每个页面应具有唯一的结构化数据；不要在多个页面上复制相同的 JSON-LD
- **性能** – JSON-LD 体积小；每页数据量控制在几 KB 以内

## 资源

### 脚本
- 用于生成和验证 schema.org 标记的 Python 工具：
  - `generate_jsonld.py` – 用于所有支持数据类型的生成函数
  - `validate_schema.py` – 本地验证工具
  - `templates/` – 包含占位符的 JSON-LD 模板

### 参考资料
- **详细文档**：
  - `schema_types.md` – 所有支持数据类型及其必需/可选属性的快速参考
  - `google_guidelines.md` – Google 的丰富结果要求和资格标准
  - `examples.md` – 各数据类型的实际使用示例

### 资源文件
- **模板文件**：
  - `html-head-injection.html` – 显示如何在 HTML 中放置 JSON-LD 的示例
  - `react-component-template.jsx` – Next.js/React 组件模板
  - `vue-component-template.vue` – 适用于 Nuxt/Vite 项目的 Vue 3 组件模板

## 高级功能：自定义数据结构构建

当标准数据类型不适用时，可以组合多个类型或使用 `Thing` 子类。例如，软件产品可以结合 `Product` 和 `SoftwareApplication`。

请参阅 `references/schema_extensions.md` 以了解组合模式。

## 常见问题解答

**问：为什么搜索结果中没有丰富显示？**
- 使用 Google 的工具进行验证
- 检查是否符合要求（某些类型需要手动审核）
- 确保页面已被索引且未被 robots.txt 文件阻止
- 请耐心等待——丰富结果显示可能需要几周时间

**问：schema 验证错误？**
- 使用正确的 `@context: "https://schema.org"`
- 缺少必需属性？为该类型添加必填字段
- 属性名称区分大小写；使用驼峰式命名（例如 `datePublished`，而非 `date_published`）

**问：一个页面上有多个数据结构？**
- 使用数组：`[ { "@type": "Article" }, { "@type": "Organization" } ]`
- 或者使用多个 `<script>` 标签（两种方法均可）

## 下一步操作

添加 schema.org 标记后：
1. 使用 [Google 丰富结果测试](https://search.google.com/test/rich-results) 进行测试
2. 监控 Search Console 以查看是否出现了丰富结果
3. 当内容发生变化时（如价格、日期、可用性）更新结构化数据

---

## 资源说明

该工具集提供了生成器、验证工具和模板，以简化 schema.org 的实现过程。

### 脚本
- `generate_jsonld.py` – 用于生成 15 种以上数据类型的 JSON-LD 的 Python 库
- `generate_jsonld_cli.py` – 用于本地使用的命令行接口
- `validate_schema.py` – 验证 JSON-LD 的结构、必填字段和日期格式

**Python 使用方法：**

```python
from generate_jsonld import generate_schema, format_jsonld

data = generate_schema("Organization", name="Acme", url="https://acme.com")
print(format_jsonld(data))
```

**命令行使用方法：**

```bash
python generate_jsonld_cli.py Product --name "Widget" --brand "Acme" --price 29.99 --url "https://shop.example.com/widget" --output schema.json
python validate_schema.py schema.json
```

### 参考资料
- `schema_types.md` – 所有支持数据类型及其必需/可选参数的快速参考
- `google_guidelines.md` – Google 的丰富结果要求和最佳实践
- `examples.md` – 各数据类型的实际使用示例（作品集、博客文章、产品、事件、本地商家、FAQ、食谱等）

在需要以下情况时请查阅这些资料：
- 查看特定类型所需的属性
- 根据 Google 的政策进行验证
- 复制并调整示例代码

### 资源文件
- `html-head-injection.html` – 显示如何在 `<head>` 中放置 JSON-LD 的简单 HTML 模板
- `react-component-template.jsx` – 适用于 Next.js 和其他 React 应用的可重用 React 组件（`<JsonLd>`, `<OrganizationJsonLd>`, `<ProductJsonLd>` 等）

将这些文件作为项目起点，复制到您的代码库中进行定制。