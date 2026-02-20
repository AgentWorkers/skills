---
name: album-cover-generation
description: 使用 each::sense AI 生成专业的音乐专辑封面。为嘻哈、摇滚、流行、电子、爵士、古典、独立音乐专辑、单曲以及 Spotify 画布视觉效果创建艺术作品。
metadata:
  author: eachlabs
  version: "1.0"
---
# 专辑封面制作

使用 `each-sense` 生成精美、专业的专辑封面艺术作品。该功能可为各类音乐作品创建高质量视觉素材，适用于流媒体平台、数字发行和实体媒体。

## 主要特点

- **完整专辑封面**：适用于所有平台的标准 3000x3000 像素图片
- **单曲封面**：吸引眼球的单曲视觉设计
- **EP 封面**：适合扩展播放的统一设计
- **Spotify Canvas**：适用于流媒体的垂直动画视频
- **特定音乐风格**：嘻哈、摇滚、流行、电子、爵士、古典、独立音乐
- **多轮迭代**：通过用户反馈优化设计
- **品牌一致性**：确保所有作品保持统一的视觉风格

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 album cover for a hip-hop album called \"Midnight Dreams\". Dark city skyline at night, neon lights reflecting on wet streets, cinematic and moody atmosphere.",
    "mode": "max"
  }'
```

## 专辑封面格式与尺寸

| 格式 | 宽高比 | 推荐尺寸 | 适用场景 |
|--------|--------------|------------------|----------|
| 专辑封面 | 1:1 | 3000x3000 像素 | 所有平台 |
| 单曲封面 | 1:1 | 3000x3000 像素 | 单曲发布 |
| EP 封面 | 1:1 | 3000x3000 像素 | 扩展播放作品 |
| Spotify Canvas | 9:16 | 1080x1920 像素 | 垂直动画视频 |
| 黑胶唱片封面 | 1:1 | 3000x3000 像素 | 实体黑胶包装 |
| CD 封面 | 1:1 | 3000x3000 像素 | 实体 CD 包装 |

## 适用场景示例

### 1. 嘻哈/说唱专辑封面

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 hip-hop album cover for \"Street Chronicles\". Urban environment with graffiti walls, gold chains aesthetic, dark moody lighting with purple and gold accents. Leave space at bottom for artist name and album title. Gritty, authentic street vibe.",
    "mode": "max"
  }'
```

### 2. 摇滚/金属专辑封面

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 heavy metal album cover for \"Eternal Flames\". Epic dark fantasy scene with a burning skull, lightning storms, gothic cathedral ruins in the background. High contrast, dramatic red and black color scheme. Classic metal album art style like Iron Maiden or Metallica.",
    "mode": "max"
  }'
```

### 3. 流行专辑封面

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 pop album cover for \"Sunshine State\". Bright, colorful aesthetic with pastel gradients (pink, blue, yellow). Abstract geometric shapes, playful and energetic mood. Modern, clean design that appeals to Gen-Z. Think Dua Lipa or Ariana Grande album vibes.",
    "mode": "max"
  }'
```

### 4. 电子/EDM专辑封面

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 electronic music album cover for \"Neon Pulse\". Futuristic cyberpunk cityscape, glowing neon lights in cyan and magenta, digital glitch effects, synthwave aesthetic. Dark background with vibrant light trails. High-tech, immersive club atmosphere.",
    "mode": "max"
  }'
```

### 5. 爵士专辑封面

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 jazz album cover for \"Blue Notes After Dark\". Classic Blue Note Records inspired design. Abstract illustration of a saxophone player silhouette, smoky jazz club atmosphere. Two-tone color palette (deep blue and cream). Minimalist, sophisticated, vintage 1960s jazz aesthetic.",
    "mode": "max"
  }'
```

### 6. 古典专辑封面

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 classical music album cover for \"Symphonic Visions\". Elegant and timeless design featuring a grand concert hall interior with golden chandeliers, velvet curtains. Soft, warm lighting. Refined and prestigious aesthetic suitable for an orchestra recording. Deutsche Grammophon style.",
    "mode": "max"
  }'
```

### 7. 独立/另类专辑封面

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 indie album cover for \"Suburban Daydreams\". Nostalgic, dreamy aesthetic with faded film photography look. Empty suburban street at golden hour, lo-fi grainy texture. Melancholic but beautiful mood. Think Bon Iver, Phoebe Bridgers, or The National album art style.",
    "mode": "max"
  }'
```

### 8. 单曲封面

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 single artwork for a song called \"Heartbeat\". Minimalist design with a stylized anatomical heart in neon red against a pure black background. Simple, bold, and immediately recognizable. Modern and striking for streaming thumbnail visibility.",
    "mode": "max"
  }'
```

### 9. EP 封面

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 EP cover for a 5-track R&B EP called \"Velvet Nights\". Luxurious, sensual aesthetic with deep purple velvet textures, soft ambient lighting, rose petals. Intimate and romantic mood. High-end, premium feel for an R&B/soul artist.",
    "mode": "max"
  }'
```

### 10. Spotify Canvas（垂直动画）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 9:16 vertical video for Spotify Canvas, 8 seconds long. Looping animation of abstract colorful paint swirls flowing upward, psychedelic and hypnotic movement. Vibrant colors (orange, pink, purple) blending smoothly. Seamless loop for continuous playback on Spotify.",
    "mode": "max"
  }'
```

## 最佳实践

### 设计原则
- **缩略图清晰度**：设计应在小尺寸（300x300 像素的缩略图）下仍可清晰显示
- **文字布局**：为艺术家名称和专辑标题留出 10-15% 的空间
- **色彩对比度**：使用高对比度以便在流媒体平台中突出显示
- **风格一致性**：设计应符合音乐类型的视觉风格
- **品牌一致性**：确保单曲和专辑作品保持统一的视觉风格

### 技术要求
- **分辨率**：始终请求 3000x3000 像素以获得最佳质量
- **宽高比**：标准专辑封面应为 1:1 的正方形
- **安全区域**：将关键元素放置在远离边缘的位置（某些平台可能会裁剪）
- **文件格式**：输出文件应为高分辨率的 PNG/JPG 格式

### 平台要求
- **Spotify**：要求使用 1:1 的正方形图片，推荐尺寸为 3000x3000 像素
- **Apple Music**：要求使用 1:1 的正方形图片，支持最大 4000x4000 像素
- **YouTube Music**：要求使用 1:1 的正方形图片
- **Bandcamp**：支持多种宽高比，但建议使用 1:1
- **Spotify Canvas**：要求使用 9:16 的垂直视频，时长 3-8 秒，可无缝循环

## 制作专辑封面的提示建议

在创建专辑封面时，请包含以下信息：

1. **音乐风格**：指定音乐类型以选择合适的视觉风格
2. **专辑/歌曲名称**：提供专辑或歌曲名称以获取创作灵感
3. **情感氛围**：明确作品的情感基调（如忧郁、振奋、怀旧、活力等）
4. **色彩方案**：指定所需的颜色或色彩搭配
5. **视觉元素**：说明希望使用的关键图像、符号或场景
6. **风格参考**：提及类似艺术家或专辑的封面风格
7. **文字位置**：指定标题和艺术家名称的显示位置

### 示例提示结构

```
"Create a [size] [genre] album cover for [title].
[Visual description] with [mood/atmosphere].
[Color scheme]. [Style reference].
[Additional requirements like text space, effects, etc.]"
```

## 模式选择

在生成封面之前，请询问用户：

**“您需要快速且低成本的方案，还是高质量的作品？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终发布的专辑封面、商业用途 | 较慢 | 最高质量 |
| `eco` | 快速概念设计、初步探索、A/B 测试 | 较快 | 良好质量 |

## 多轮创意迭代

使用 `session_id` 进行多次封面设计迭代：

```bash
# Initial concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 album cover for an ambient electronic album. Minimal, atmospheric, space theme.",
    "session_id": "album-project-001"
  }'

# Refine based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make it darker with more contrast. Add subtle star field in the background and a gradient from deep blue to black.",
    "session_id": "album-project-001"
  }'

# Request variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 2 more variations with different color schemes - one in purple tones and one in warm orange/red sunset colors.",
    "session_id": "album-project-001"
  }'
```

## 一致性策略

为专辑、单曲和宣传材料生成统一的设计风格：

```bash
# Main album cover
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 album cover for \"Fragments\" by an indie band. Shattered mirror aesthetic with warm golden light fragments. Artistic and abstract.",
    "session_id": "fragments-album-campaign"
  }'

# Single artwork (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create single artwork for the lead single from the same album. Use the same visual language but focus on a single large fragment. Maintain the color palette.",
    "session_id": "fragments-album-campaign"
  }'

# Spotify Canvas
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 9:16 Spotify Canvas video using the same shattered mirror aesthetic. Slow motion fragments floating and rotating, 6 seconds, seamless loop.",
    "session_id": "fragments-album-campaign"
  }'
```

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 数据不足 | 请在 eachlabs.ai 上补充数据 |
| 内容违规 | 内容不符合规定 | 调整提示以符合内容准则 |
| 超时 | 生成过程复杂 | 将客户端超时设置至少为 10 分钟 |

## 相关技能

- `each-sense`：核心 API 文档
- `product-photo-generation`：用于商品拍摄的产品照片生成服务
- `social-media-content`：用于社交媒体宣传的图形设计