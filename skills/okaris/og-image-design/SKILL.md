---
name: og-image-design
description: "**Open Graph与社交分享图像设计：包括平台规范、文本布局及品牌元素**  
本文档详细介绍了如何根据不同平台的规范来设计用于社交分享的图像，涵盖了OG元标签（Open Graph Meta Tags）、Twitter卡片（Twitter Cards）、LinkedIn预览图（LinkedIn Previews）的创建方法，以及图像的动态生成技术。这些设计适用于多种场景，如社交分享、博客缩略图、链接预览图等。  
**相关术语说明：**  
- **OG Meta Tags**：Open Graph元标签，用于描述图片内容，帮助搜索引擎和社交媒体平台正确显示图片信息。  
- **Twitter Cards**：Twitter提供的卡片格式，用于在Twitter上分享图片时显示额外信息。  
- **LinkedIn Previews**：LinkedIn用于预览链接内容的图片格式。  
- **Dynamic Generation**：动态图像生成技术，可根据用户行为或平台需求动态生成图片内容。  
**应用场景：**  
- 社交分享图像  
- 博客缩略图  
- 链接预览图  
- 社交媒体卡片  
**触发条件（Trigger Terms）：**  
- `og-image`：Open Graph图像标签  
- `open-graph`：Open Graph相关功能  
- `social-sharing-image`：社交分享图像  
- `twitter-card`：Twitter卡片  
- `social-card`：社交媒体卡片  
- `link-preview-image`：链接预览图像  
- `meta-image`：元图像（用于社交媒体平台显示）  
- `sharing-preview`：分享预览图  
- `social-thumbnail`：社交媒体缩略图  
**文档结构：**  
- 开篇介绍Open Graph与社交分享的基本概念  
- 分别讲解不同平台的图像设计规范  
- 介绍OG元标签的编写方法  
- 展示Twitter卡片和LinkedIn预览图的创建步骤  
- 说明动态图像生成的实现方式  
- 提供相关代码示例和配置指南  
**注意事项：**  
- 请确保遵循各平台的图像尺寸、格式和内容要求。  
- 适当添加品牌元素（如Logo、颜色方案等）以提升品牌形象。  
- 测试图像在不同设备上的显示效果，确保兼容性。"
allowed-tools: Bash(infsh *)
---
# 原生图片设计（OG Image Design）

您可以通过 [inference.sh](https://inference.sh) 命令行工具来生成用于社交分享的图片（Open Graph 标签）。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate an OG image with HTML-to-image
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1200px;height:630px;background:linear-gradient(135deg,#1a1a2e,#16213e);display:flex;align-items:center;padding:60px;font-family:system-ui;color:white\"><div><h1 style=\"font-size:56px;margin:0;line-height:1.2\">How We Reduced Build Times by 80%</h1><p style=\"font-size:24px;opacity:0.8;margin-top:20px\">engineering.yourcompany.com</p></div></div>"
}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以选择 [手动安装及验证](https://dist.inference.sh/cli/checksums.txt)。

## 平台规格

| 平台 | 尺寸 | 长宽比 | 文件大小 | 格式 |
|----------|-----------|--------------|-----------|--------|
| **Facebook** | 1200 x 630 像素 | 1.91:1 | < 8 MB | JPG, PNG |
| **Twitter/X (summary_large_image)** | 1200 x 628 像素 | 1.91:1 | < 5 MB | JPG, PNG, WEBP, GIF |
| **Twitter/X (summary)** | 800 x 418 像素 | 1.91:1 | < 5 MB | JPG, PNG |
| **LinkedIn** | 1200 x 627 像素 | 1.91:1 | < 5 MB | JPG, PNG |
| **Discord** | 1200 x 630 像素 | 1.91:1 | < 8 MB | JPG, PNG |
| **Slack** | 1200 x 630 像素 | 1.91:1 | — | JPG, PNG |
| **iMessage** | 1200 x 630 像素 | 1.91:1 | — | JPG, PNG |

**通用推荐尺寸：1200 x 630 像素，格式为 PNG 或 JPG，文件大小不超过 5 MB。**

## 优质布局指南

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
| 标题字体大小 | 48-64 像素 |
| 副标题字体大小 | 20-28 像素 |
| 标题最大长度 | 60 个字符（部分平台会自动截断） |
| 副标题最大长度 | 100 个字符 |
| 行高 | 标题为 1.2-1.3 像素 |
| 字体粗细 | 标题使用粗体/黑色字体，副标题使用常规字体 |
| 文本对比度 | 符合 WCAG AA 标准（至少 4.5:1 的对比度）

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

- 所有边缘至少保留 40 像素的间距
- 部分平台会裁剪图片边缘或添加圆角
- 绝不要将重要文本放置在图片的外侧 5% 区域内

### 颜色

| 背景类型 | 使用场景 |
|----------------|-------------|
| 固定品牌颜色 | 保持一致性，适合企业风格 |
| 渐变背景 | 现代感强，吸引眼球 |
| 带图层的照片 | 适合博客文章或新闻报道 |
| 深色背景 | 对比度更高，在信息流中更显眼 |

**深色背景在社交信息流中效果更好**——大多数信息流的背景为白色或浅色，因此深色图片更易脱颖而出。

## 根据内容类型选择模板

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

### 人工智能生成的图片

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
| `summary` | 800 x 418 像素（小缩略图） | 简短更新、链接 |
| `summary_large_image` | 1200 x 628 像素（全宽） | 博客文章、新闻报道 |

**除非有特殊原因，否则请始终使用 `summary_large_image`——大尺寸图片的点击率更高。**

## 一致性系统

对于拥有大量页面的博客或网站，建议建立模板系统：

| 元素 | 保持一致 | 可变元素 |
|---------|----------------|------|
| 背景样式 | 使用相同的渐变效果或品牌颜色 | — |
| 字体系列 | 使用相同的字体 | — |
| 布局 | 保持相同的元素位置 | — |
| 标志/品牌标识 | 保持相同的放置位置（角落） | — |
| 类别标签 | 保持相同的样式，颜色根据类别区分 | |
| 标题文字 | 保持相同的大小和粗细 | 标题和内容可调整 |

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
| 文本太小 | 在移动设备上难以阅读 | 标题字体大小至少为 48 像素，图片宽度至少为 1200 像素 |
| 背景太浅 | 在白色或浅色背景的信息流中难以显示 | 使用深色或饱和度较高的背景 |
| 文字太多 | 信息过于杂乱 | 最多包含标题、副标题和品牌标识 |
| 图片过大（>5MB） | 部分平台无法加载 | 尽量将图片大小优化到 1MB 以下 |
| 未设置安全区域间距 | 图片在某些平台上会被裁剪 | 所有边缘至少保留 40 像素的间距 |
| 不同平台使用不同的图片 | 共享体验不一致 | 所有平台都使用 1200x630 像素的图片 |
| 使用 HTTP 图片链接 | 许多平台要求使用 HTTPS | 必须通过 HTTPS 提供原生图片 |
| 相对路径的图片链接 | 共享时可能无法正确显示 | 使用绝对路径 |

## 相关技能

```bash
npx skills add inference-sh/skills@ai-image-generation
npx skills add inference-sh/skills@landing-page-design
npx skills add inference-sh/skills@prompt-engineering
```

查看所有可用应用：`infsh app list`