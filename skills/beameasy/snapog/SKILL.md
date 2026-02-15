---
name: snapog
description: 通过 SnapOG API，可以使用专业模板生成社交图片和原创卡片（OG Cards）。每次 API 调用都会生成一张像素完美的 PNG 图像。
homepage: https://snapog.dev
metadata: {"openclaw":{"emoji":"⚡","primaryEnv":"SNAPOG_API_KEY","requires":{"env":["SNAPOG_API_KEY"]}}}
---

# SnapOG — 社交媒体图片生成工具

SnapOG 可以根据专业设计的模板生成原图（OG images）、社交媒体卡片（social cards）以及营销视觉素材。生成结果为像素完美的 PNG 图片，耗时不到 100 毫秒。

**API 基址：** `https://api.snapog.dev`

## 认证

所有生成请求都需要使用 Bearer Token。API 密钥从 `SNAPOG_API_KEY` 环境变量中获取。

```
Authorization: Bearer $SNAPOG_API_KEY
```

预览和模板列表接口无需认证即可使用。

## 可用模板

| 模板 | ID | 适用场景 |
|----------|----|----------|
| 博文文章 | `blog-post` | 博文、教程、文档 |
| 公告 | `announcement` | 产品发布、更新信息 |
| 统计数据 | `stats` | 统计仪表盘、季度报告 |
| 引用 | `quote` | 客户评价、引用语、社交媒体分享 |
| 产品介绍 | `product` | SaaS 产品、价格信息、功能介绍 |
| GitHub 仓库 | `github-repo` | 开源项目、仓库信息 |
| 活动 | `event` | 会议、研讨会、网络研讨会 |
| 更新日志 | `changelog` | 版本更新信息 |
| 品牌介绍 | `brand-card` | 公司页面、文档、营销材料 |
| 图片标题 | `photo-hero` | 博文标题、新闻图片、作品集 |

## 核心工作流程

### 1. 列出模板并查看参数

```bash
curl https://api.snapog.dev/v1/templates
```

该接口会返回所有模板及其参数信息（参数名称、类型、必填字段、默认值）。如果用户未指定模板，请先调用此接口。

### 2. 生成图片（POST 请求）

用于下载图片或使用高级选项：

```bash
curl -X POST https://api.snapog.dev/v1/generate \
  -H "Authorization: Bearer $SNAPOG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "template": "blog-post",
    "params": {
      "title": "Building with MCP",
      "author": "Taylor",
      "tags": ["AI", "Tools"],
      "accentColor": "#6366f1"
    }
  }' \
  --output og-image.png
```

**POST 请求体字段：**
- `template`（字符串，必填）— 模板 ID
- `params`（对象，必填）— 模板参数
- `width`（数字）— 图片宽度（单位：像素，默认值：1200）
- `height`（数字）— 图片高度（单位：像素，默认值：630）
- `format`（字符串）— 输出格式（`png` | `svg` | `pdf`，默认值：`png`）
- `fontFamily`（字符串）— 任意 Google 字体名称
- `webhook_url`（字符串）— 生成完成后发送的 POST 请求 URL

将响应体直接保存为 `.png` 文件。响应的 Content-Type 为 `image/png`。

### 3. 通过 URL 生成图片（GET 请求）

当用户需要将图片嵌入 HTML 的 `<meta>` 标签或 Markdown 文本中时，可以使用此接口：

```
https://api.snapog.dev/v1/og/blog-post?title=Building+with+MCP&author=Taylor&tags=AI,Tools
```

该 URL 本身即可直接显示图片。参数通过查询字符串传递。需要设置 `Authorization` 请求头或使用签名 URL。

### 4. 预览模板（无需认证）

```bash
curl https://api.snapog.dev/v1/preview/blog-post --output preview.png
```

使用默认参数渲染模板，方便用户在自定义前查看模板效果。

### 5. 生成签名 URL（用于 `<meta>` 标签）

签名 URL 可以让你在 `<meta>` 标签中嵌入图片，而无需暴露 API 密钥：

```bash
curl -X POST https://api.snapog.dev/v1/sign \
  -H "Authorization: Bearer $SNAPOG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "template": "blog-post",
    "params": { "title": "My Post" },
    "expiresIn": 86400
  }'
```

返回格式如下：`{"url": "https://api.snapog.dev/v1/og/blog-post?title=...&token=..."}`。此 URL 无需认证，可直接用于 HTML 中：

```html
<meta property="og:image" content="SIGNED_URL_HERE" />
```

### 6. 批量生成图片（多种尺寸）

可以一次性生成多种尺寸的图片：

```bash
curl -X POST https://api.snapog.dev/v1/batch \
  -H "Authorization: Bearer $SNAPOG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "template": "blog-post",
    "params": { "title": "My Post" },
    "sizes": ["og", "twitter", "farcaster", "instagram-square"]
  }'
```

**支持的尺寸：** `og`（1200x630）、`twitter`（1200x628）、`farcaster`（1200x800）、`instagram-square`（1080x1080）、`instagram-story`（1080x1920）、`linkedin`（1200x627）、`facebook`（1200x630）、`pinterest`（1000x1500）。

## 常用参数

大多数模板支持以下通用参数：

- `title`（字符串，必填）— 主标题
- `accentColor`（颜色）— 主题颜色（例如：`#6366f1`）
- `logo`（字符串）— 徽标图片 URL
- `fontFamily`（字符串）— 任意 Google 字体名称

每个模板还有特定的参数。调用 `/v1/templates` 可查看该模板的完整参数信息。

## 使用建议

- **选择模板**：根据内容类型选择合适的模板，例如：`blog-post` 适用于博客文章，`announcement` 适用于产品发布，`github-repo` 适用于开源项目等。
- **颜色**：使用十六进制颜色格式（如 `#6366f1`）进行设置。大多数模板支持 `accentColor` 参数。
- **数组**：对于 `tags` 和 `changes` 等参数，请以 JSON 数组形式传递（例如：`["tag1", "tag2"]`）。
- **统计数据**：`stats` 模板接收 JSON 数组格式的数据，例如：`[{"label": "Users", "value": "10K"]`。
- **图片**：`logo`、`image`、`authorImage` 等参数请使用公开可访问的图片 URL。
- **输出格式**：默认输出为 1200x630 像素的 PNG 图片。可通过 `width`/`height` 参数进行自定义。
- **格式**：`svg` 用于矢量图像；`pdf` 用于打印文档。

## 完整 API 文档

如需完整的 API 参考文档（以 Markdown 格式），请查看：

```bash
curl https://api.snapog.dev/v1/docs
```