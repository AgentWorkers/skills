---
name: Meta Tags - SEO Tag Generator
description: 生成用于 SEO、Open Graph、Twitter Cards 和 JSON-LD 的 HTML 元标签。可直接复制粘贴使用，非常适合网页开发者。这是一个免费的命令行工具（CLI）。
---

# 元标签

生成用于搜索引擎优化（SEO）、Open Graph、Twitter Cards 和 JSON-LD 的完整元标签。

## 安装

```bash
npm install -g @lxgicstudios/meta-tags
```

## 基本用法

```bash
npx @lxgicstudios/meta-tags -t "Page Title" -d "Description" -u "https://example.com"
```

## 命令

### 生成所有标签

```bash
meta-tags -t "My Website" -d "Welcome to my site" -u "https://example.com"
```

### 带有社交媒体图片的元标签

```bash
meta-tags -t "Blog Post" -d "Great article" -i "https://example.com/image.jpg"
```

### 文章类型

```bash
meta-tags -t "How to Code" --type article --author "John Doe" --published "2024-01-15"
```

### 从配置文件生成元标签

```bash
meta-tags --config seo.json -o head.html
```

## 选项

| 选项 | 描述 |
|--------|-------------|
| `-t, --title` | 页面标题（必填） |
| `-d, --description` | 元描述 |
| `-u, --url` | 标准URL |
| `-i, --image` | Open Graph/Twitter 图片 |
| `-k, --keywords` | 关键词（用逗号分隔） |
| `--site-name` | 网站名称 |
| `--twitter` | Twitter 账号 |
| `--type` | 元标签类型：网站、文章、产品 |
| `--format` | 输出格式：html、json、react、vue |

## 输出示例

```html
<!-- Primary Meta Tags -->
<title>My Website</title>
<meta name="description" content="Welcome...">
<link rel="canonical" href="https://example.com">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:title" content="My Website">
<meta property="og:image" content="https://...">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:title" content="My Website">

<!-- JSON-LD -->
<script type="application/ld+json">...</script>
```

## 输出格式

```bash
meta-tags -t "Title" --format html   # Default
meta-tags -t "Title" --format json   # JSON
meta-tags -t "Title" --format react  # React Helmet
meta-tags -t "Title" --format vue    # Vue useHead
```

## 常见使用场景

**博客文章元标签：**
```bash
meta-tags -t "My Article" -d "Description" -i "cover.jpg" --type article --author "Me"
```

**为 Next.js 生成元标签：**
```bash
meta-tags -t "Page" --format react -o metadata.tsx
```

---

**由 [LXGIC Studios](https://lxgicstudios.com) 开发**

🔗 [GitHub](https://github.com/lxgicstudios/meta-tags) · [Twitter](https://x.com/lxgicstudios)