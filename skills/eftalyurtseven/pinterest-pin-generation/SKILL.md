---
name: pinterest-pin-generation
description: 使用 each::sense AI 生成 Pinterest 图钉图片。可以创建标准图钉、创意图钉、产品图钉、食谱图钉以及信息图等类型，所有图片都经过优化，以符合 Pinterest 的格式和最佳实践。
metadata:
  author: eachlabs
  version: "1.0"
---
# Pinterest 图片生成

使用 `each-sense` 生成适用于 Pinterest 的高质量图片。该功能生成的图片符合 Pinterest 的格式要求、长宽比以及平台最佳实践，旨在最大化用户互动率并节省资源。

## 特点

- **标准图片**：垂直比例为 2:3 的图片，适合在 Pinterest 的信息流中展示
- **创意图片**：多页故事风格的图片内容
- **产品图片**：结合生活方式元素的商品图片
- **食谱图片**：包含详细步骤的美食摄影
- **DIY/教程图片**：包含清晰视觉步骤的教学内容
- **信息图图片**：数据可视化及教育性内容
- **引用图片**：具有启发性的文本图片
- **购物图片**：可直接用于商品目录的图片
- **视频缩略图**：吸引眼球的视频内容封面
- **图板封面图片**：用于图板的统一缩略图集

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 Pinterest pin for a home decor brand showing a cozy living room with warm lighting, minimalist Scandinavian style, space at top for text overlay",
    "mode": "max"
  }'
```

## Pinterest 图片格式与尺寸

| 图片类型 | 长宽比 | 推荐尺寸 | 使用场景 |
|----------|--------------|------------------|----------|
| 标准图片 | 2:3 | 1000x1500 | 通用内容，最高可见度 |
| 创意图片封面 | 9:16 | 1080x1920 | 多页故事风格内容 |
| 方形图片 | 1:1 | 1000x1000 | 产品展示，简单设计 |
- 长图片 | 1:2.1 | 1000x2100 | 信息图，逐步指南 |
- 视频缩略图 | 2:3 或 9:16 | 1000x1500 或 1080x1920 | 视频内容封面 |
- 图板封面图片 | 2:3 | 600x900 | 图板缩略图集 |

## 使用场景示例

### 1. 标准图片（2:3 比例）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 vertical Pinterest pin for a travel blog about Santorini, Greece. Show the iconic white buildings with blue domes overlooking the sea, golden hour lighting, dreamy atmosphere. Leave space at the top third for text overlay like a blog title.",
    "mode": "max"
  }'
```

### 2. 创意图片封面

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 9:16 Idea Pin cover for a morning routine series. Show an aesthetic flat lay of coffee, journal, plants, and skincare products on a marble surface. Soft natural morning light, clean minimalist aesthetic. This is the cover image for a multi-page story.",
    "mode": "max"
  }'
```

### 3. 产品图片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 Pinterest product pin for handmade ceramic mugs. Show a beautiful handcrafted mug with coffee, placed on a wooden table with soft natural light, cozy kitchen background slightly blurred. Lifestyle product photography style, warm and inviting mood.",
    "mode": "max"
  }'
```

### 4. 食谱图片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 Pinterest recipe pin for homemade chocolate chip cookies. Show freshly baked cookies on a cooling rack, some stacked, with melted chocolate visible, rustic wooden background. Food photography style with steam or warmth visible. Leave top portion clear for recipe title text.",
    "mode": "max"
  }'
```

### 5. DIY/教程图片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 Pinterest pin for a DIY macrame wall hanging tutorial. Show the finished macrame piece hanging on a white wall with a plant nearby, bohemian aesthetic. The image should look like the final result of a craft project, inspiring and achievable. Space for tutorial title at top.",
    "mode": "max"
  }'
```

### 6. 信息图图片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:2.1 long Pinterest infographic background for productivity tips. Design a clean, modern gradient background going from soft blue at top to teal at bottom, with subtle geometric patterns or icons related to productivity (clocks, checkmarks, calendars). Leave clear spaces for 5-6 text sections. Minimal and professional design.",
    "mode": "max"
  }'
```

### 7. 引用图片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 Pinterest quote pin background for motivational content. Show a serene nature scene - misty mountains at sunrise with soft pink and purple colors. The image should be slightly muted/faded to allow white text to be readable on top. Inspirational and calming mood.",
    "mode": "max"
  }'
```

### 8. 购物图片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 Pinterest shopping pin for a summer dress collection. Show a floral maxi dress on a model in a garden setting, natural daylight, lifestyle fashion photography. The dress should be clearly visible and the main focus, styled with simple accessories. E-commerce catalog quality.",
    "mode": "max"
  }'
```

### 9. 视频缩略图

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 Pinterest video thumbnail for a makeup tutorial. Show a close-up of a woman with beautiful eye makeup, soft ring light reflection in eyes, beauty photography style. The image should be eye-catching and make people want to watch the video. Professional makeup artistry showcase.",
    "mode": "max"
  }'
```

### 10. 图板封面图片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 Pinterest board cover for a Wedding Inspiration board. Show an elegant flat lay with wedding elements - white flowers, gold rings, lace fabric, calligraphy card, on a soft marble background. Romantic, luxurious, cohesive aesthetic that represents wedding planning content.",
    "mode": "max"
  }'
```

## 最佳实践

### 图片构图
- **垂直格式**：始终使用 2:3 或更高的比例，以在信息流中获得最佳显示效果
- **文字空间**：预留顶部 20-30% 的区域用于标题或文字
- **焦点**：将主要对象放置在中心或使用三分法则
- **高对比度**：确保图片在拥挤的信息流中脱颖而出
- **以移动设备优先**：考虑移动设备的显示效果（大多数 Pinterest 流量来自移动设备）

### 内容策略
- **生活方式元素**：展示产品的实际使用场景，而不仅仅是孤立的产品图片
- **具有吸引力**：创建用户想要保存和复制的图片
- **季节相关性**：考虑热门话题和季节性元素
- **可搜索性**：思考用户可能会搜索的内容
- **系列一致性**：在相关图片中保持视觉风格的一致性

### 技术规格
- **分辨率**：最小宽度为 1000px，以确保清晰显示
- **文件格式**：PNG 或 JPG，适用于网页展示
- **安全区域**：将关键内容置于边缘之外（Pinterest 可能会裁剪图片）
- **颜色**：使用鲜艳、饱和度高的颜色，以在信息流中脱颖而出

## 创建 Pinterest 图片的提示建议

在创建 Pinterest 图片时，请在提示中包含以下信息：

1. **长宽比**：指定 2:3、9:16 或 1:2.1 以获得最佳格式
2. **图片类型**：说明是产品图片、食谱图片还是教程图片等
- **视觉风格**：选择所需的视觉风格（极简、波西米亚风、现代风、乡村风）
- **文字空间**：请求用于标题或文字的区域
- **氛围**：选择适合图片的氛围（温馨、活力四射、奢华、宁静等）
- **目标受众**：谁会保存这张图片？
- **摄影风格**：选择合适的拍摄方式（平铺式、生活方式风格、人像拍摄）

### 示例提示结构

```
"Create a [aspect ratio] Pinterest [pin type] for [topic/product].
Show [visual description] with [style/aesthetic].
[Mood/lighting description].
[Text space requirements].
[Any additional Pinterest-specific requirements]."
```

## 模式选择

在生成图片之前，请询问用户：

**“您需要快速且低成本的图片，还是高质量图片？”**

| 模式 | 适用场景 | 速度 | 图片质量 |
|------|----------|-------|---------|
| `max` | 完成的图片，可直接发布 | 较慢 | 最高质量 |
| `eco` | 快速草图，测试概念，批量生成 | 较快 | 良好质量 |

## 多轮创意迭代

使用 `session_id` 进行图片设计的迭代：

```bash
# Initial pin design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 Pinterest pin for a fitness brand, showing healthy meal prep",
    "session_id": "fitness-pin-project"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add more colorful vegetables and make the lighting brighter and more energetic",
    "session_id": "fitness-pin-project"
  }'

# Request variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 2 more variations with different angles and compositions",
    "session_id": "fitness-pin-project"
  }'
```

## 季节性图片批量生成

为季节性内容生成主题化的图片集：

```bash
# Spring collection pin 1
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 spring Pinterest pin for a gardening blog - show colorful tulips in a garden, morning dew, fresh spring aesthetic",
    "session_id": "spring-collection",
    "mode": "eco"
  }'

# Spring collection pin 2
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create another spring pin for the same gardening blog - show someone planting seeds in a terracotta pot, hands in soil, same fresh spring aesthetic",
    "session_id": "spring-collection",
    "mode": "eco"
  }'
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 数据不平衡 | 在 eachlabs.ai 中补充数据 |
- 内容违规 | 违反 Pinterest 的内容规定 | 调整提示以符合 Pinterest 的内容指南 |
- 超时 | 生成过程复杂 | 将客户端超时时间设置为至少 10 分钟 |

## 相关技能

- `each-sense`：核心 API 文档
- `meta-ad-creative-generation`：用于 Facebook 和 Instagram 的广告创意生成
- `product-photo-generation`：用于电商产品的图片生成
- `social-media-content-generation`：用于一般社交媒体的图片生成