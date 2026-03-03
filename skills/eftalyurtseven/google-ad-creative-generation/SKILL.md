---
name: google-ad-creative-generation
description: 使用 each::sense AI 生成 Google 广告创意。这些创意包括展示广告、YouTube 缩略图、Discovery 广告、Performance Max 广告资源以及响应式展示广告，均经过优化以符合 Google 的广告格式和最佳实践。
metadata:
  author: eachlabs
  version: "1.0"
---
# 谷歌广告创意生成

使用 `each-sense` 生成高转化率的谷歌广告创意。该技能能够生成针对谷歌广告平台（包括展示网络、YouTube、Discovery 和 Performance Max 广告系列）进行优化的图片和视频。

## 特点

- **展示广告**：适用于谷歌展示网络的静态图片，支持所有标准尺寸。
- **YouTube 缩略图**：为视频广告和有机内容定制缩略图。
- **Discovery 广告**：适用于 Gmail、Discovery 功能和 YouTube 主页的原生风格图片。
- **Performance Max**：为自动化谷歌广告系列提供多种格式的广告素材。
- **响应式展示广告**：为谷歌的机器学习优化广告投放提供多种广告素材。
- **购物广告**：为电子商务广告系列生成以产品为中心的创意内容。
- **应用广告**：为应用安装广告系列生成优化过的视觉素材。
- **视频广告**：适用于 YouTube 广告平台的短视频内容。

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Google Display ad banner for a SaaS product, 300x250 medium rectangle, showing a clean dashboard interface with professional blue color scheme",
    "mode": "max"
  }'
```

## 谷歌广告格式与尺寸

### 展示网络

| 格式 | 尺寸（像素） | 长宽比 | 适用场景 |
|--------|-----------|--------------|----------|
| 中等矩形 | 300x250 | 1.2:1 | 最常见，库存充足 |
| 大矩形 | 336x280 | 1.2:1 | 高级广告位 |
|  leaderboard（横幅） | 728x90 | 8:1 | 页眉/页脚广告位 |
| 移动 leaderboard（横幅） | 320x50 | 6.4:1 | 移动设备页眉广告 |
| 半页广告 | 300x600 | 1:2 | 高可见性侧边栏广告 |
| 大型移动横幅 | 320x100 | 3.2:1 | 移动设备插页广告 |
| Billboard（大型广告） | 970x250 | 3.9:1 | 高级桌面广告位 |
| 宽型广告（Skyscraper） | 160x600 | 1:3.75 | 侧边栏广告位 |

### YouTube 与视频

| 格式 | 尺寸/比例 | 适用场景 |
|--------|------------|----------|
| 定制缩略图 | 1280x720（16:9） | 视频缩略图、配套横幅 |
| In-Feed 缩略图 | 1200x628 | YouTube Discovery 广告 |
| Bumper 广告 | 6 秒，16:9 | 短视频广告（不可跳过） |
| Skippable In-Stream 广告 | 15-30 秒，16:9 | 播放前/中间的广告 |

### Discovery 与 Performance Max

| 格式 | 尺寸（像素） | 长宽比 | 适用场景 |
|--------|-----------|--------------|----------|
| 正方形 | 1200x1200 | 1:1 | Discovery 功能和 Performance Max 广告 |
| 横屏 | 1200x628 | 1.91:1 | Gmail、Discovery、YouTube 广告 |
| 纵屏 | 960x1200 | 4:5 | 以移动设备为主的广告位 |

### 响应式展示广告

| 广告类型 | 推荐尺寸 | 备注 |
|------------|-------------------|-------|
| 横屏图片 | 1200x628 | 必需，长宽比为 1.91:1 |
| 正方形图片 | 1200x1200 | 必需，长宽比为 1:1 |
| 徽标（横屏） | 512x128 | 可选，长宽比为 4:1 |
| 徽标（正方形） | 128x128 | 推荐，长宽比为 1:1 |

## 适用场景示例

### 1. 展示广告（中等矩形）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 300x250 Google Display ad for an online course platform. Show a person learning on laptop, modern gradient background in purple and blue, leave space for headline text at top and CTA button at bottom.",
    "mode": "max"
  }'
```

### 2. YouTube 定制缩略图

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 16:9 YouTube thumbnail for a tech review video. Show a smartphone floating with dramatic lighting, bold contrasting colors, leave right side clear for text overlay. Eye-catching and clickable style.",
    "mode": "max"
  }'
```

### 3. Discovery 广告（Gmail/Discovery）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1.91:1 landscape Discovery ad for a travel agency. Show a stunning beach destination with turquoise water, aspirational vacation vibes. Native content feel, not overly promotional. 1200x628 pixels.",
    "mode": "max"
  }'
```

### 4. 购物广告产品图片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a product image for Google Shopping. Show wireless headphones on pure white background, multiple angles visible, clean e-commerce style. High detail, professional product photography look.",
    "mode": "max"
  }'
```

### 5. 应用广告

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 square ad for a fitness app install campaign. Show app interface mockup on phone screen with workout tracking visible, energetic person exercising in background. Vibrant orange and black brand colors.",
    "mode": "max"
  }'
```

### 6. 响应式展示广告组合

```bash
# Landscape asset (required)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1200x628 landscape image for responsive display ads. Insurance company - show a happy family in front of their home, warm and trustworthy feeling, soft natural lighting. Leave clear space for headline overlay.",
    "session_id": "responsive-insurance-001"
  }'

# Square asset (required)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1200x1200 square version of the same insurance ad. Same family, same style, recomposed for square format.",
    "session_id": "responsive-insurance-001"
  }'
```

### 7. Performance Max 多样化素材

```bash
# Asset 1 - Square
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 square image for Performance Max campaign. E-commerce fashion brand - show model wearing casual summer dress, lifestyle outdoor setting, Instagram-worthy aesthetic.",
    "session_id": "pmax-fashion-001",
    "mode": "max"
  }'

# Asset 2 - Landscape
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1.91:1 landscape version for the same fashion campaign, same model and dress, wider scene showing more environment.",
    "session_id": "pmax-fashion-001",
    "mode": "max"
  }'

# Asset 3 - Portrait
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 4:5 portrait version for mobile placements, same fashion campaign, vertical composition focusing on the dress.",
    "session_id": "pmax-fashion-001",
    "mode": "max"
  }'
```

### 8. YouTube Bumper 广告

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 6 second 16:9 bumper ad video for a car dealership. Quick cuts showing sleek new car exterior, interior dashboard, driving on highway. End with logo frame. Fast-paced, cinematic quality.",
    "mode": "max"
  }'
```

### 9. Leaderboard 横幅

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 728x90 leaderboard banner for a web hosting company. Horizontal layout with server imagery on left, gradient blue tech background. Leave center-right area for headline and CTA. Modern and professional.",
    "mode": "max"
  }'
```

### 10. 再营销广告（含产品图片）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 300x250 remarketing display ad featuring this watch product. Place the watch prominently with a lifestyle background showing success and sophistication. Add visual urgency elements suggesting limited availability.",
    "mode": "max",
    "image_urls": ["https://example.com/product-watch.jpg"]
  }'
```

## 最佳实践

### 展示广告
- **品牌一致性**：在所有尺寸中保持一致的色彩、字体和视觉风格。
- **清晰的层次结构**：明确图像、标题和呼叫行动（CTA）的视觉层次。
- **最少文字**：让图片发挥主要作用；谷歌更喜欢以图片为主的广告。
- **高对比度**：确保在不同网站背景下的可读性。
- **呼叫行动按钮的可见性**：使呼叫行动按钮清晰突出。

### YouTube 缩略图
- **正面朝向**：带有眼神交流的人脸可以提高点击率。
- **鲜艳的色彩**：使用与 YouTube 白色界面形成对比的鲜艳色彩。
- **易读的文字**：如果添加文字，请确保在小尺寸下仍可清晰显示。
- **情感表达**：展示强烈的情感以引发好奇心。
- **避免杂乱**：保持构图简洁明了。

### Discovery 广告
- **原生感**：设计时要与有机内容融合，不要看起来像广告。
- **鼓舞人心的图片**：使用能激发行动的生活方式图片。
- **高质量**：Discovery 广告位更倾向于高质量的内容。
- **以移动设备为主**：针对移动设备屏幕进行设计，因为大部分 Discovery 流量来自移动设备。

### Performance Max
- **多样化的素材**：提供多种不同比例的图片以优化机器学习效果。
- **一致的品牌形象**：在所有素材变体中保持视觉一致性。
- **测试不同风格**：混合使用生活方式图片和产品图片。
- **避免图片中的文字**：谷歌的机器学习算法对无文字的图片效果更好。

### 响应式展示广告
- **测试所有组合**：设计适用于任何标题/描述的图片。
- **安全区域**：将重要元素远离边缘（保留 15% 的边距）。
- **可伸缩性**：确保图片在 300px 到 1200px 宽度范围内都能显示良好。

## 创建谷歌广告创意时的提示

在创建谷歌广告创意时，请在提示中包含以下细节：

1. **精确尺寸**：指定像素尺寸或长宽比（例如 300x250、1.91:1 等）。
2. **广告格式**：说明是用于展示广告、YouTube、Discovery 还是 Performance Max。
3. **产品/服务**：清楚地描述你正在推广的内容。
4. **视觉焦点**：主要视觉元素应该是什么？
5. **色彩方案**：使用品牌色彩或所需的调色板。
6. **文字空间**：请求为标题、描述或呼叫行动按钮预留空间。
7. **风格参考**：专业、轻松、简洁、醒目等。

### 示例提示结构

```
"Create a [dimensions] [ad format] for [product/service].
Show [visual description] with [color scheme/style].
Leave space for [text elements].
[Additional requirements like brand guidelines, urgency, etc.]"
```

## 模式选择

在生成广告创意之前，询问用户：

**“您需要快速且低成本的方案，还是高质量的作品？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终广告创意、Performance Max 广告素材、A/B 测试结果 | 较慢 | 最高质量 |
| `eco` | 快速草图、概念探索、批量横幅设计 | 较快 | 一般质量 |

## 多轮创意迭代

使用 `session_id` 进行广告创意的迭代：

```bash
# Initial creative
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 300x250 display ad for a fintech app, modern and trustworthy",
    "session_id": "fintech-display-001"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the background darker, add subtle grid pattern, more techy feel",
    "session_id": "fintech-display-001"
  }'

# Generate size variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a 728x90 leaderboard version with the same style",
    "session_id": "fintech-display-001"
  }'
```

## 批量生成横幅尺寸

为某个广告系列生成多种横幅尺寸：

```bash
# Medium Rectangle
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 300x250 display ad for online shoe store, lifestyle shot of running shoes in action",
    "session_id": "shoe-campaign-001",
    "mode": "eco"
  }'

# Leaderboard
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 728x90 leaderboard version, same shoe campaign style, horizontal layout",
    "session_id": "shoe-campaign-001",
    "mode": "eco"
  }'

# Half Page
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 300x600 half page version, vertical layout showcasing the shoes",
    "session_id": "shoe-campaign-001",
    "mode": "eco"
  }'
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 资源不足 | 在 eachlabs.ai 网站补充资源 |
| 内容政策违规 | 内容被禁止 | 调整提示以符合谷歌广告政策 |
| 超时 | 生成过程复杂 | 将客户端超时设置为至少 10 分钟 |
| 尺寸不匹配 | 请求的尺寸无效 | 使用上表中的标准谷歌广告尺寸 |

## 相关技能

- `each-sense` - 核心 API 文档
- `meta-ad-creative-generation` - 用于 Facebook/Instagram 广告创意的生成工具
- `tiktok-ad-creative-generation` - 用于 TikTok 广告创意的生成工具
- `product-photo-generation` - 用于生成电子商务产品图片的工具