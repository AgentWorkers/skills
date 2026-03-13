---
name: xhs-md2img
description: 将 Markdown 文本转换为美观的 Xiaohongshu (XHS) 样式卡片图片，支持 5 种主题、确定的浏览器截图规则、自动分页、智能标题提取以及 AI 生成的装饰性背景。
metadata:
  clawdbot:
    emoji: "🎴"
    requires:
      env: [DASHSCOPE_API_KEY]
      anyBins: [python3, python]
    primaryEnv: DASHSCOPE_API_KEY
    permissions:
      network: true
      filesystem: true
---
# xhs-md2img

该工具可将 Markdown 文本转换为 Xiaohongshu (XHS) 样式的多页卡片图片，确保在浏览器中的渲染效果和截图行为具有确定性。

## 概述

该工具能够将 Markdown 内容渲染为可直接发布的 XHS 卡片图片，并专为在浏览器截图服务中稳定运行而设计。

**使用场景：**
- 将长篇内容转换为适合 XHS 的多张图片帖子
- 从 Markdown 文章生成带有样式的卡片图片
- 生成尺寸一致、具有分页功能的多页截图

## 快速入门

只需提供 Markdown 文本即可开始使用：

```json
{
  "markdown": "## 5个提升效率的方法\n\n**1. 番茄工作法** — 25分钟专注 + 5分钟休息\n\n**2. 任务批处理** — 把相似的事情集中做\n\n> 效率不是做更多的事，而是用更少的时间做对的事。"
}
```

默认输出格式为 1125x1500 像素的 PNG 图片（在 `export_scale=3` 时，CSS 尺寸为 375x500）。

## 输入参数

完整的输入参数规范请参见 `templates/input-schema.json`。

**核心内容/样式参数：**
- `markdown`（必填）：Markdown 内容。使用 `---` 进行手动分页。
- `title`、`author`、`description`：封面元数据。
- `theme`：可选主题，包括 `default`、`monokai`、`nord`、`sakura`、`mint`。
- `font_family`：字体系列，如 `sans-serif`、`serif`、`wenkai`。
- `padding`：内边距大小，可选 `small`、`medium`、`large`。
- `show_cover`：是否显示封面块。
- `bg_style`：背景图片样式，可选 `ai_art` 或 `none`。

**浏览器截图控制参数：**
- `card_width` / `card_height`：单张卡片的 CSS 尺寸（默认为 375x500）。
- `export_scale`：像素比例放大倍数（默认为 3）。
- `viewport_width` / `viewport_height`：浏览器视口尺寸，用于保证渲染稳定性。
- `page_gap`：DOM 中卡片之间的垂直间距（默认为 20）。
- `pagination_mode`：分页方式，可选 `mixed`、`auto`、`manual_only`。
- `max_pages`：分页的最大限制，防止无限分页。
- `show_page_number`：是否显示页码指示器。
- `avoid_orphan_heading`：确保每个标题后面至少有一个内容块。
- `last_page_compact`：当内容较短时，压缩最后一张卡片。

## 确定的浏览器截图规则

为了获得一致的 XHS 样式输出，请遵循以下规则：

1. **固定的卡片几何形状**
   - 卡片的比例必须保持为 3:4（基础尺寸为 375x500）。
   - 输出图片的像素尺寸应为 `card_width * export_scale` × `card_height * export_scale`。
  - 建议使用 `export_scale=3` 以获得最佳 XHS 质量（输出尺寸为 1125x1500）。

2. **稳定的浏览器环境**
   - 使用无头浏览器（headless browser），并设置 `deviceScaleFactor=export_scale`。
  - 保持缩放比例在 100%；不要使用浏览器的打印模式。
  - 使用指定的视口尺寸（推荐使用 440x760）。

3. **渲染准备条件（在分页/截图前必须满足）**
  - 等待 `document.fonts_ready`。
  - 确保 `document.body[data-fonts-loaded="true"]` 已设置。
  - 连续两帧动画的 `.xhs-card` 元素的边界框保持不变。

4. **仅截图元素**
   - 仅截取每个 `.xhs-card` 元素的截图，避免截取整个页面后进行裁剪。
  - 在截图过程中禁用动画/过渡效果。
  - 仅输出 PNG 格式的图片。

有关实现指南和故障检查，请参阅 `references/browser-screenshot-spec.md`。

## 渲染流程

### 1. 智能格式化（LLM）

如果输入为纯文本，将其重新格式化为 Markdown，同时保持原文内容：
- 提取简短的封面标题（10-20 个字符）。
- 添加结构元素（如 `##`、`**`、列表、引号）。
- 保留所有原始的符号/表情符号/标签。

### 2. 将 Markdown 转换为 HTML

使用 `python-markdown` 工具，并启用以下扩展功能：
- `tables`、`fenced_code`、`codehilite`、`nl2br`、`sane_lists`、`smarty`、`attr_list`、`md_in_html`、`toc`。
- 将 XHS 标签（`#tag#`）转换为具有样式的卡片元素。

### 3. 使用 HTML/CSS 构建卡片

使用 `templates/card-template.html` 文件，根据指定的主题和尺寸生成卡片结构。

卡片层次结构：
- `.xhs-card`：固定大小的卡片容器。
- `.bg-art`：可选的半透明背景图片。
- `.card-inner`：显示内容的区域。

### 4. 分页规则（关键步骤）

在 DOM 中实现分页功能，而不是使用 PDF 或打印格式的分页方式。

优先级顺序：
- 首先根据手动分页符（`---`）进行分割。
- 在每个段落内，根据顶级元素进行分割。
- 如果 `avoid_orphan_heading` 为 `true`，则避免将标题作为页面上的最后一个可见元素。
- 尽可能保持列表/表格/代码块的结构完整。
- 如果单个元素的内容超过一页，则进行安全分割：
  - 列表：按 `li` 分割。
  - 表格：按行组分割。
  - 代码/预格式化文本：按行组分割。
  - 段落：按句子分割。

**溢出处理规则：**
- 页面内容区域的高度必须满足 `scrollHeight <= clientHeight`。
- 保留底部的安全间距（约 16 CSS 像素），以防止内容被裁剪。

### 5. 多页截图输出

对于每一页：
- 创建一个 `.xhs-card` 元素。
- 添加可选的页码指示器（`page` / `total_pages`）。
- 将该元素的截图保存为 PNG 图片。
- 按索引顺序返回所有页面的截图。

**输出格式：**

```json
{
  "__type": "xhs_card_images",
  "title": "Extracted or provided title",
  "theme": "default",
  "total_pages": 3,
  "pages": [
    {
      "index": 0,
      "page": 1,
      "total_pages": 3,
      "width": 1125,
      "height": 1500,
      "size_bytes": 123456,
      "url": "https://...",
      "oss_uploaded": true
    }
  ]
}
```

如果未配置开源软件（OSS），则返回每个页面的 `data_uri`。

## XHS 视觉质量检查

在返回图片之前，请验证以下内容：
- 每页的实际尺寸是否符合输出公式。
- 图片底部没有裁剪的内容。
- 不同页面之间的标题和正文间距一致。
- 页码的显示效果（半透明效果）要清晰可见。
- 当 `last_page_compact` 为 `true` 时，最后一页没有大面积的空白区域。

## 主题系统

`references/themes.md` 文件中定义了 5 个内置主题：

| 主题 | 背景颜色 | 风格 |
|-------|-----------|------|
| `default` | 白色 `#ffffff` | 简洁、专业 |
| `monokai` | 深蓝色 `#272822` | 技术风格，适合开发者 |
| `nord` | 深蓝色 `#2e3440` | 北欧极简风格 |
| `sakura` | 浅粉色 `#fff5f5` | 温暖、女性化 |
| `mint` | 浅绿色 `#f0faf4` | 清新、自然 |

## AI 背景生成

当 `bg_style` 设置为 `ai_art` 时：
- 使用大型语言模型（LLM）根据内容或主题生成抽象的背景图片。
- 背景图片提供者自动选择：
  - 当 `LLM_BASE_URL` 指向 Google 时，优先使用 Gemini。
  - 如果可用，其次使用 DashScope wanx。
- 背景图片会以较低的透明度（8-18%）融入卡片中。

**限制：**
- 生成的背景图片仅用于装饰目的（如水彩、模糊效果、几何图案或植物轮廓）。
- 图片中不允许出现文字、人脸或具体的物体。

有关提供者的 API 详细信息，请参阅 `references/api-reference.md`。

## 隐私与外部接口

网络请求可能涉及以下服务：
- 大型语言模型（LLM）API：用于格式化文本、生成标题和背景图片提示。
- DashScope/Gemini：用于生成背景图片（仅提供图片提示）。
- 阿里云 OSS：用于上传生成的图片（可选）。

在生成图片的过程中，不会向模型发送用户的原始文档内容；仅使用抽象的提示文本。