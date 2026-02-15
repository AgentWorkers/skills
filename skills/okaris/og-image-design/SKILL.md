---
name: og-image-design
description: |
  Open Graph and social sharing image design with platform specs, text placement, and branding.
  Covers OG meta tags, Twitter cards, LinkedIn previews, and dynamic generation.
  Use for: social sharing images, blog thumbnails, link previews, social cards.
  Triggers: og image, open graph, social sharing image, twitter card, social card,
  link preview image, og meta, sharing preview, social thumbnail, meta image,
  og:image, twitter:image, linkedin preview
allowed-tools: Bash(infsh *)
---

# 原生图片设计（OG Image Design）

通过 [inference.sh](https://inference.sh) 命令行工具来生成用于社交分享的图片（Open Graph 图片）。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate an OG image with HTML-to-image
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1200px;height:630px;background:linear-gradient(135deg,#1a1a2e,#16213e);display:flex;align-items:center;padding:60px;font-family:system-ui;color:white\"><div><h1 style=\"font-size:56px;margin:0;line-height:1.2\">How We Reduced Build Times by 80%</h1><p style=\"font-size:24px;opacity:0.8;margin-top:20px\">engineering.yourcompany.com</p></div></div>"
}'
```

## 平台规格

| 平台 | 尺寸 | 长宽比 | 文件大小 | 格式 |
|----------|-----------|--------------|-----------|--------|
| **Facebook** | 1200 x 630 px | 1.91:1 | < 8 MB | JPG, PNG |
| **Twitter/X (summary_large_image)** | 1200 x 628 px | 1.91:1 | < 5 MB | JPG, PNG, WEBP, GIF |
| **Twitter/X (summary)** | 800 x 418 px | 1.91:1 | < 5 MB | JPG, PNG |
| **LinkedIn** | 1200 x 627 px | 1.91:1 | < 5 MB | JPG, PNG |
| **Discord** | 1200 x 630 px | 1.91:1 | < 8 MB | JPG, PNG |
| **Slack** | 1200 x 630 px | 1.91:1 | — | JPG, PNG |
| **iMessage** | 1200 x 630 px | 1.91:1 | — | JPG, PNG |

**通用标准：1200 x 630 px 的图片，格式为 PNG 或 JPG，文件大小不超过 5 MB。**

## 优质图片布局

```
┌──────────────────────────────────────────────────┐
│                                                  │
│  ┌─────────────────────────────────┐  ┌───────┐  │
│  │                                 │  │       │  │
│  │  Title Text (max 60 chars)      │  │ Logo/ │  │
│  │  ───────────────────            │  │ Visual│  │
│  │  Subtitle (max 100 chars)       │  │       │  │
│  │                                 │  │       │  │
│  │  author / site name             │  └───────┘  │
│  └─────────────────────────────────┘             │
│                                                  │
└──────────────────────────────────────────────────┘
  1200 x 630 px
```

## 设计规则

### 文本

| 规则 | 值 |
|------|-------|
| 标题字体大小 | 48-64px |
| 副标题字体大小 | 20-28px |
| 标题最大长度 | 60 个字符（部分平台会自动截断） |
| 副标题最大长度 | 100 个字符 |
| 行高 | 标题：1.2-1.3 像素 | 副标题：1.2-1.3 像素 |
| 字体粗细 | 标题：加粗/黑色 | 副标题：常规字体 |
| 文本对比度 | 符合 WCAG AA 标准（至少 4.5:1 的对比度） |

### 安全区域（Safe Zones）

```
┌──────────────────────────────────────────────────┐
│  ┌──────────────────────────────────────────────┐│
│  │ 40px padding from all edges                  ││
│  │                                              ││
│  │  Content lives here                          ││
│  │                                              ││
│  │                                              ││
│  └──────────────────────────────────────────────┘│
└──────────────────────────────────────────────────┘
```

- 所有边缘至少保留 40px 的内边距
- 部分平台会裁剪图片边缘或添加圆角
- 绝不要将重要文本放置在图片的外侧 5% 区域内

### 颜色

| 背景类型 | 使用场景 |
|----------------|-------------|
| 固定品牌颜色 | 保持一致性，适合企业形象 |
| 渐变背景 | 现代感强，吸引眼球 |
| 带图层的照片 | 适用于博客文章或新闻报道 |
| 深色背景 | 对比度更高，在信息流中更显眼 |

**在社交信息流中，深色背景通常比浅色背景更受欢迎**——因为大多数信息流的背景都是白色或浅色的，所以深色图片更显眼。

## 根据内容类型生成的模板

### 博客文章

```bash
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1200px;height:630px;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;padding:60px;font-family:system-ui,sans-serif;color:white\"><div style=\"flex:1\"><p style=\"font-size:18px;text-transform:uppercase;letter-spacing:2px;opacity:0.8;margin:0\">Engineering Blog</p><h1 style=\"font-size:52px;margin:16px 0 0;line-height:1.2;font-weight:800\">How We Reduced Build Times by 80%</h1><p style=\"font-size:22px;opacity:0.9;margin-top:16px\">A deep dive into our CI/CD optimization</p></div></div>"
}'
```

### 产品/发布公告

```bash
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1200px;height:630px;background:#0f0f0f;display:flex;align-items:center;justify-content:center;font-family:system-ui;color:white;text-align:center\"><div><p style=\"font-size:20px;color:#22c55e;text-transform:uppercase;letter-spacing:3px\">Now Available</p><h1 style=\"font-size:64px;margin:12px 0;font-weight:900\">DataFlow 2.0</h1><p style=\"font-size:24px;opacity:0.7\">Automated reports. Zero configuration.</p></div></div>"
}'
```

### 教程/操作指南

```bash
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1200px;height:630px;background:linear-gradient(to right,#1a1a2e,#16213e);display:flex;align-items:center;padding:60px;font-family:system-ui;color:white\"><div><div style=\"display:inline-block;background:#e74c3c;color:white;padding:8px 16px;border-radius:4px;font-size:16px;font-weight:bold;margin-bottom:16px\">TUTORIAL</div><h1 style=\"font-size:48px;margin:0;line-height:1.2\">Build a REST API in 10 Minutes with Node.js</h1><p style=\"font-size:20px;opacity:0.7;margin-top:16px\">Step-by-step guide with code examples</p></div></div>"
}'
```

### 由 AI 生成的图片

```bash
# When you want a striking visual instead of text-based
infsh app run falai/flux-dev-lora --input '{
  "prompt": "clean professional social sharing card, dark gradient background, abstract geometric shapes, modern tech aesthetic, minimal, no text, 1200x630 equivalent aspect ratio",
  "width": 1200,
  "height": 630
}'
```

## 原生图片元标签参考

```html
<!-- Essential (Facebook, LinkedIn, Discord, Slack) -->
<meta property="og:title" content="Title here (60 chars max)" />
<meta property="og:description" content="Description (155 chars max)" />
<meta property="og:image" content="https://yoursite.com/og-image.png" />
<meta property="og:url" content="https://yoursite.com/page" />
<meta property="og:type" content="article" />

<!-- Twitter/X specific -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Title here" />
<meta name="twitter:description" content="Description" />
<meta name="twitter:image" content="https://yoursite.com/og-image.png" />

<!-- Image dimensions (optional but recommended) -->
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
```

### Twitter 卡片类型

| 卡片类型 | 图片尺寸 | 使用场景 |
|-----------|-----------|----------|
| `summary` | 800 x 418 px（小缩略图） | 简短更新、链接 |
| `summary_large_image` | 1200 x 628 px（全宽图片） | 博客文章、新闻报道 |

**除非有特殊原因，否则始终使用 `summary_large_image`——大尺寸图片的点击率更高。**

## 一致性系统

对于拥有大量页面的博客或网站，建议建立模板系统：

| 元素 | 保持一致 | 可变部分 |
|---------|----------------|------|
| 背景样式 | 使用相同的渐变效果或品牌颜色 | — |
| 字体系列 | 使用相同的字体 | — |
| 布局 | 保持相同的元素位置 | — |
| 标志/品牌标识 | 保持相同的放置位置（角落） | — |
| 类别标签 | 保持相同的样式 | 每个类别使用不同的颜色 |
| 标题文字 | 保持相同的大小和粗细 | 标题和内容可以调整 |

## 测试原生图片

| 工具 | URL |
|------|-----|
| Facebook 调试工具 | developers.facebook.com/tools/debug/ |
| Twitter 卡片验证工具 | cards-dev.twitter.com/validator |
| LinkedIn 帖子检查工具 | linkedin.com/post-inspector/ |
| OpenGraph.xyz | opengraph.xyz |

```bash
# Research OG debugging tools
infsh app run tavily/search-assistant --input '{
  "query": "open graph image debugger preview tool test og:image"
}'
```

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 未设置原生图片 | 平台会显示随机页面元素或无图片显示 | 必须设置 `og:image` 标签 |
| 文本太小 | 在移动设备上难以阅读 | 标题字体大小至少为 48px，图片宽度至少为 1200px |
| 背景颜色太浅 | 在白色或浅色背景下难以看清 | 使用深色或饱和度较高的背景 |
| 文字太多 | 信息过于杂乱 | 最多显示标题、副标题和品牌标识 |
| 图片过大（>5MB） | 部分平台无法加载 | 将图片大小优化到 1MB 以下 |
| 未设置安全区域 | 图片在某些平台上会被裁剪 | 所有边缘至少保留 40px 的内边距 |
| 不同平台使用不同的图片 | 共享体验不一致 | 所有平台都使用 1200x630 的图片 |
| 图片链接使用 HTTP 协议 | 许多平台要求使用 HTTPS | 必须通过 HTTPS 提供原生图片 |
| 使用相对路径 | 共享时图片无法正确显示 | 使用绝对路径 |

## 相关技能

```bash
npx skills add inferencesh/skills@ai-image-generation
npx skills add inferencesh/skills@landing-page-design
npx skills add inferencesh/skills@prompt-engineering
```

查看所有可用应用：`infsh app list`