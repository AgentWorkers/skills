---
name: seo-optimizer
description: 此技能适用于分析HTML/CSS网站以进行SEO优化、解决SEO相关问题、生成SEO报告，或实施SEO最佳实践。当用户需要SEO审计、优化服务、元标签改进、schema标记的添加、站点地图生成，或任何与搜索引擎优化相关的任务时，均可使用该技能。
---

# SEO优化工具

## 概述

该工具为HTML/CSS网站提供全面的SEO优化功能。它可以分析网站中的SEO问题，应用最佳实践，并生成涵盖所有关键SEO方面的优化报告，包括元标签、标题结构、图片优化、Schema标记、移动优化和技术SEO等。

## 何时使用该工具

当用户请求以下服务时，请使用该工具：
- “分析我的网站是否存在SEO问题”
- “对这一页进行SEO优化”
- “生成SEO审计报告”
- “修复我网站上的SEO问题”
- “为我的页面添加合适的元标签”
- “应用Schema标记”
- “生成站点地图”
- “提高我网站的搜索引擎排名”
- 任何与HTML/CSS网站的搜索引擎优化相关的工作

## 工作流程

### 1. 初始SEO分析

使用SEO分析脚本进行全面分析：

```bash
python scripts/seo_analyzer.py <directory_or_file>
```

该脚本会分析HTML文件，并生成一份详细的报告，内容包括：
- 标题标签（长度、是否存在、唯一性）
- 元描述（长度、是否存在）
- 标题结构（H1-H6层次结构）
- 图片alt属性
- Open Graph标签
- Twitter Card标签
- Schema.org标记
- HTML lang属性
- 视口和字符集meta标签
- 规范URL
- 内容长度

**输出选项**：
- 默认：包含问题、警告和最佳实践的易读文本报告
- `--json`：用于程序处理的机器可读JSON格式

**示例用法**：
```bash
# Analyze single file
python scripts/seo_analyzer.py index.html

# Analyze entire directory
python scripts/seo_analyzer.py ./public

# Get JSON output
python scripts/seo_analyzer.py ./public --json
```

### 2. 查看分析结果

分析工具将发现的问题分为三个级别：

**严重问题（🔴）** - 需立即修复：
- 缺少标题标签
- 缺少元描述
- 缺少H1标题
- 图片没有alt属性
- 缺少HTML lang属性

**警告（⚠️）** - 为获得最佳SEO效果，请尽快修复：
- 标题/描述长度不佳
- 多个H1标签
- 缺少Open Graph或Twitter Card标签
- 缺少viewport meta标签
- 缺少Schema标记
- 标题层次结构问题

**最佳实践（✅）** - 已经优化：
- 元素格式正确
- 长度合适
- 必需的标签都已添加

### 3. 优先处理并修复问题

按优先级处理问题：

#### 优先级1：严重问题

**缺少或格式不佳的标题标签**：
```html
<!-- Add unique, descriptive title to <head> -->
<title>Primary Keyword - Secondary Keyword | Brand Name</title>
```
- 标题长度保持在50-60个字符
- 在标题开头包含目标关键词
- 每个页面的标题都要唯一

**缺少元描述**：
```html
<!-- Add compelling description to <head> -->
<meta name="description" content="Clear, concise description that includes target keywords and encourages clicks. 150-160 characters.">
```

**缺少H1标题或多个H1标题**：
- 每个页面确保只有一个H1标题
- H1标题应描述主要内容
- H1标题应与标题标签相匹配或相关

**图片没有alt文本**：
```html
<!-- Add descriptive alt text to all images -->
<img src="image.jpg" alt="Descriptive text explaining image content">
```

**缺少HTML lang属性**：
```html
<!-- Add to opening <html> tag -->
<html lang="en">
```

#### 优先级2：重要优化

**Viewport Meta标签**（对移动SEO至关重要）：
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

**字符集声明**：
```html
<meta charset="UTF-8">
```

**Open Graph标签**（用于社交媒体分享）：
```html
<meta property="og:title" content="Your Page Title">
<meta property="og:description" content="Your page description">
<meta property="og:image" content="https://example.com/image.jpg">
<meta property="og:url" content="https://example.com/page-url">
<meta property="og:type" content="website">
```

**Twitter Card标签**：
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Your Page Title">
<meta name="twitter:description" content="Your page description">
<meta name="twitter:image" content="https://example.com/image.jpg">
```

**规范URL**：
```html
<link rel="canonical" href="https://example.com/preferred-url">
```

#### 优先级3：高级优化

**Schema标记** - 详细实现方法请参考`references/schemamarkup_guide.md`。常见类型包括：
- Organization（首页）
- Article/BlogPosting（博客文章）
- LocalBusiness（本地企业）
- Breadcrumb（导航栏）
- FAQ（常见问题解答）
- Product（产品）

示例实现：
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "author": {
    "@type": "Person",
    "name": "Author Name"
  },
  "datePublished": "2024-01-15",
  "image": "https://example.com/image.jpg"
}
</script>
```

### 4. 生成或更新站点地图

修复问题后，生成XML站点地图：

```bash
python scripts/generate_sitemap.py <directory> <base_url> [output_file]
```

**示例**：
```bash
# Generate sitemap for website
python scripts/generate_sitemap.py ./public https://example.com

# Specify output location
python scripts/generate_sitemap.py ./public https://example.com ./public/sitemap.xml
```

该脚本会：
- 自动查找所有HTML文件
- 生成正确的URL
- 包含lastmod日期
- 估算优先级和更新频率
- 生成格式正确的XML站点地图

**生成后**：
1. 将sitemap.xml文件上传到网站根目录
2. 在robots.txt文件中引用站点地图
3. 提交给Google Search Console和Bing Webmaster Tools

### 5. 更新robots.txt

使用`assets/robots.txt`中的模板进行自定义：

```
User-agent: *
Allow: /

# Block sensitive directories
Disallow: /admin/
Disallow: /private/

# Reference your sitemap
Sitemap: https://yourdomain.com/sitemap.xml
```

将robots.txt文件放置在网站根目录中。

### 6. 验证和测试

实施修复后：

**本地测试**：
1. 重新运行SEO分析工具以验证修复效果
2. 确保所有严重问题都已解决
3. 确认没有引入新的问题

**在线测试**：
1. 将更改部署到生产环境
2. 使用Google Rich Results Test进行测试：https://search.google.com/test/rich-results
3. 验证Schema标记：https://validator.schema.org/
4. 检查移动友好性：https://search.google.com/test/mobile-friendly
5. 监控Google Search Console中的数据

### 7. 持续优化

**定期维护**：
- 添加新页面时更新站点地图
- 保持元描述的新鲜和吸引力
- 确保新图片有alt文本
- 为新内容类型添加Schema标记
- 监控Search Console中的问题
- 定期更新内容

## 常见优化模式

### 模式1：新网站设置

对于全新的HTML/CSS网站：
1. 运行初始分析：`python scripts/seo_analyzer.py ./public`
2. 为所有页面添加必要的元标签（标题、描述、viewport）
3. 确保正确的标题结构（每个页面一个H1）
4. 为所有图片添加alt文本
5. 在首页应用Organization Schema
6. 生成站点地图：`python scripts/generate_sitemap.py ./public https://yourdomain.com`
7. 根据模板创建robots.txt文件
8. 部署并将站点地图提交给搜索引擎

### 模式2：现有网站审计

对于需要优化的现有网站：
1. 运行全面分析：`python scripts/seo_analyzer.py ./public`
2. 识别并优先处理问题（先处理严重问题）
3. 修复所有页面的严重问题
4. 添加缺失的Open Graph和Twitter Card标签
5. 为适当的页面应用Schema标记
6. 重新生成包含更新的站点地图
7. 用分析工具验证修复效果
8. 部署并监控

### 模式3：单页优化

针对特定页面进行优化：
1. 分析特定文件：`python scripts/seo_analyzer.py page.html`
2. 修复发现的问题
3. 优化标题和元描述以匹配目标关键词
4. 确保正确的标题层次结构
5. 为页面类型添加适当的Schema标记
6. 用分析工具验证效果
7. 如果有新页面，则更新站点地图

### 模式4：博客文章优化

对于博客文章：
1. 确保标题唯一（50-60个字符），包含目标关键词
2. 编写吸引人的元描述（150-160个字符）
3. 使用单个H1标题
4. 为各个部分使用正确的H2/H3标题层次结构
5. 为所有图片添加alt文本
6. 应用Article或BlogPosting Schema（参见`references/schema_markup_guide.md`）
7. 为社交媒体分享添加Open Graph和Twitter Card标签
8. 添加作者信息
9. 为导航栏添加Breadcrumb Schema

## 参考资料

### 详细指南

**`references/seo_checklist.md`**：
涵盖所有SEO方面的综合检查清单：
- 标题标签和元描述指南
- 标题结构最佳实践
- 图片优化技巧
- URL结构建议
- 内部链接策略
- 页面速度优化
- 移动优化要求
- 语义化HTML的使用
- 完整的技术SEO检查清单

如需了解任何SEO元素的详细规范，请参考此文件。

**`references/schema_markup_guide.md`：
关于如何实现Schema.org结构化数据的完整指南：
- 推荐的JSON-LD实现格式
- 10多种常见Schema类型及示例
- Organization、LocalBusiness、Article、BlogPosting、FAQ、Product等类型
- 每种类型所需的属性
- 最佳实践和常见错误
- 验证工具和资源

在为任何内容类型应用Schema标记时，请参考此文件。

### 脚本

**`scripts/seo_analyzer.py**：
用于自动化SEO分析的Python脚本。分析HTML文件中的常见问题并生成详细报告。支持文本或JSON格式输出，重复分析时结果稳定可靠。

**`scripts/generate_sitemap.py**：
用于生成XML站点地图的Python脚本。自动爬取目录，估算优先级和更新频率，并生成格式正确的站点地图以供搜索引擎使用。

### 资源文件

**`assets/robots.txt`：
包含常见配置和注释的robots.txt模板。根据具体需求进行自定义，并放置在网站根目录中。

## 关键原则

1. **以用户为中心**：首先优化用户体验，其次才是搜索引擎。良好的用户体验有助于提升SEO效果。

2. **内容唯一性**：每个页面都应有唯一的标题、描述和H1标题。重复内容会损害SEO排名。

3. **移动优先**：Google采用移动优先的索引策略。务必添加viewport meta标签并确保网站具有移动友好性。

4. **可访问性 = SEO**：可访问的网站（alt文本、语义化HTML、正确的标题）排名更高。

5. **质量优于数量**：高质量、有价值的内容比内容量大的网站排名更高。力求内容丰富。

6. **技术基础**：在进行高级优化之前，先修复关键的技术问题（如缺失的标签、损坏的结构）。

7. **结构化数据**：Schema标记有助于搜索引擎理解内容，从而提供更好的搜索结果。

8. **定期更新**：SEO是一个持续的过程。保持内容更新，监控分析结果，并根据算法变化进行调整。

9. **自然语言**：使用自然语言编写内容。避免过度使用关键词。

10. **验证**：在部署到生产环境之前，始终使用测试工具验证更改。

## 提高效果的小贴士

- **从解决关键问题开始**：首先修复缺失的标题标签和元描述——这些问题的影响最大。
- **保持一致性**：在所有页面上应用优化措施，而不仅仅是首页。
- **使用语义化HTML**：使用正确的HTML5语义标签（`<header>`、`<nav>`、`<main>`、`<article>`、`<aside>`、`<footer>`）。
- **优化图片**：压缩图片，使用描述性文件名，务必添加alt文本。
- **内部链接**：使用描述性的锚文本链接到相关页面。
- **页面速度很重要**：加载速度快的页面排名更高。
- **进行移动端测试**：大多数搜索来自移动设备——确保网站在移动端有良好的用户体验。
- **监控Search Console**：使用Google Search Console跟踪网站性能并发现问题。
- **定期更新**：更新内容，展示网站的活跃性和价值。

## 快速参考命令

```bash
# Analyze single file
python scripts/seo_analyzer.py index.html

# Analyze entire website
python scripts/seo_analyzer.py ./public

# Generate sitemap
python scripts/generate_sitemap.py ./public https://example.com

# Get JSON analysis output
python scripts/seo_analyzer.py ./public --json
```