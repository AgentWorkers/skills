---
name: poster-design-generation
description: 使用 each::sense AI 生成专业的海报设计。通过 AI 驱动的创意生成功能，您可以制作电影海报、活动海报、励志海报、产品发布视觉素材、复古风格的海报以及旅行海报等。
metadata:
  author: eachlabs
  version: "1.0"
---
# 海报设计生成

使用 `each-sense` 功能生成精美、专业的海报设计。该技能可为电影、活动、产品、旅行、体育赛事、社会公益活动以及各种创意应用创建高质量的海报作品。

## 主要功能

- **电影海报**：具有戏剧性构图和出色排版效果的电影主题海报
- **活动/音乐会海报**：适用于现场活动的引人注目的宣传材料
- **励志海报**：包含鼓舞人心图像的励志设计
- **产品发布海报**：用于产品发布的商业视觉素材
- **极简艺术海报**：简洁、现代的设计风格
- **复古/怀旧海报**：来自不同时代的经典风格
- **旅游目的地海报**：激发旅行热情的视觉素材
- **体育赛事海报**：动态的体育宣传资料
- **教育/信息图海报**：信息丰富的视觉设计
- **社会公益海报**：用于提高公众意识的宣传素材

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a dramatic movie poster for a sci-fi thriller, dark atmosphere with neon accents, leave space at top for title",
    "mode": "max"
  }'
```

## 常见海报尺寸与格式

| 类型 | 长宽比 | 推荐尺寸 | 适用场景 |
|------|--------------|------------------|----------|
| 电影海报 | 2:3 | 1080x1620 | 影院海报、电影主题图 |
| 活动海报 | 11:17 | 1100x1700 | 音乐会传单、活动宣传 |
| 正方形海报 | 1:1 | 1080x1080 | 社交媒体、专辑封面 |
| 横屏海报 | 16:9 | 1920x1080 | 数字显示屏、横幅 |
| 纵屏海报 | 9:16 | 1080x1920 | 手机、数字标牌 |
| A系列海报 | 约1:1.414 | 2480x3508（A4纸幅） | 打印海报 |

## 适用场景示例

### 1. 电影海报设计

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 movie poster for a psychological thriller. A silhouette of a man standing at the edge of a foggy cliff, moody blue and grey tones, cinematic lighting with dramatic shadows. Leave space at the top third for the movie title and bottom for credits. Hollywood blockbuster quality.",
    "mode": "max"
  }'
```

### 2. 活动/音乐会海报

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design an 11:17 concert poster for an electronic music festival. Vibrant neon colors, abstract geometric shapes, laser beams and light effects, futuristic cyberpunk aesthetic. Include visual space for artist names at the top and event details at the bottom. High energy, rave culture vibes.",
    "mode": "max"
  }'
```

### 3. 励志海报

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an inspirational motivational poster. A lone climber reaching the summit of a mountain at sunrise, golden light breaking through clouds, epic landscape vista. Vertical 2:3 format with space at the bottom for an inspirational quote. Awe-inspiring, triumphant mood.",
    "mode": "max"
  }'
```

### 4. 产品发布海报

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a sleek product launch poster for a new smartphone. The phone floating in center with dynamic light trails and particle effects around it, dark premium background with subtle gradient. Modern tech aesthetic, Apple-style minimalism. 2:3 vertical format with space for product name and tagline.",
    "mode": "max"
  }'
```

### 5. 极简艺术海报

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a minimalist art poster in the style of Scandinavian design. Simple geometric shapes, limited color palette of terracotta, sage green, and cream. Abstract composition suggesting a landscape. Clean lines, modern aesthetic suitable for home decor. 3:4 vertical format.",
    "mode": "max"
  }'
```

### 6. 复古/怀旧海报

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a vintage 1950s travel poster style artwork. Classic American diner scene with neon signs, chrome details, and a classic car. Retro color palette with faded pastels, mid-century illustration style with visible brush strokes. Include decorative border typical of the era. 2:3 format.",
    "mode": "max"
  }'
```

### 7. 旅游目的地海报

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a travel poster for Tokyo, Japan. Cherry blossoms in the foreground, Mount Fuji in the distance, traditional temples mixed with modern skyscrapers. Warm sunset colors, dreamy wanderlust aesthetic. Art deco travel poster style with bold shapes. 2:3 vertical with space for destination name at bottom.",
    "mode": "max"
  }'
```

### 8. 体育赛事海报

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a dynamic basketball championship poster. Action shot of a player mid-dunk, explosive energy with motion blur and particle effects, dramatic stadium lighting. Bold colors - deep blue and orange. High contrast, intense competitive spirit. 11:17 format with space for event title and date.",
    "mode": "max"
  }'
```

### 9. 教育/信息图海报

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an educational poster about the solar system. Visually stunning representation of planets in orbit around the sun, accurate relative sizes and colors, space background with stars and nebulae. Scientific but visually appealing, suitable for a classroom or museum. 16:9 horizontal format with areas for planet labels.",
    "mode": "max"
  }'
```

### 10. 社会公益海报

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a powerful environmental awareness poster about ocean conservation. A beautiful sea turtle swimming through crystal clear water, but with subtle hints of pollution in the background. Emotional, thought-provoking imagery that inspires action. Blue and green tones. 2:3 vertical format with space for campaign message.",
    "mode": "max"
  }'
```

## 最佳实践

### 构图与布局
- **排版空间**：务必为标题、副标题和文本内容预留足够的空间
- **安全边距**：为打印过程中的出血现象及重要内容留出边距
- **焦点**：明确视觉层次和注意力中心
- **平衡**：指定需要对称还是非对称的构图

### 视觉风格
- **色彩搭配**：说明具体的颜色或基于情绪的色彩方案（温暖、冷色调、鲜艳、柔和）
- **光线效果**：描述光线的方向、质量和氛围
- **风格参考**：参考特定的艺术流派、时代或设计风格
- **纹理效果**：指定所需的纹理效果（颗粒感、噪点、纸张质感、数字清晰度）

### 格式规范
- **长宽比**：务必根据实际用途指定所需的比例
- **分辨率**：打印版需更高分辨率，数字版使用标准分辨率
- **方向**：大多数海报采用竖屏（16:9）格式

## 海报设计提示

在创建海报设计时，请在提示中包含以下信息：

1. **用途**：海报的用途是什么？（电影、活动、产品等）
2. **格式**：指定所需的长宽比（2:3、11:17、1:1等）
3. **风格**：设计风格或时代特征（极简主义、复古、现代等）
4. **主要元素**：主要的视觉元素和构图方式
5. **色彩搭配**：具体的颜色或基于情绪的色彩方案
6. **排版位置**：文本的放置位置
7. **情感基调**：设计的情感氛围

### 示例提示结构

```
"Create a [format/ratio] [type] poster for [purpose].
[Visual description of main subject and composition].
[Style and aesthetic references].
[Color palette and lighting].
Leave space at [position] for [text elements]."
```

## 模式选择

在生成海报之前，请询问用户：

**“您需要快速且低成本的设计，还是高质量的设计？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终海报设计、适合打印 | 较慢 | 最高质量 |
| `eco` | 快速草图、概念探索、风格测试 | 较快 | 良好 |

## 多轮创意迭代

使用 `session_id` 进行海报设计的多次迭代：

```bash
# Initial concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a movie poster for a horror film, dark forest setting with fog",
    "session_id": "horror-poster-001",
    "mode": "max"
  }'

# Refine the design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add a creepy abandoned house in the background, and make the color palette more red and black",
    "session_id": "horror-poster-001"
  }'

# Request variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 2 more variations with different compositions - one more minimal, one more intense",
    "session_id": "horror-poster-001"
  }'
```

## 海报系列生成

为宣传活动生成统一风格的海报系列：

```bash
# Series poster 1
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create poster 1 of 4 for a summer music festival series. Beach sunset theme, vibrant orange and pink. Feature a DJ silhouette.",
    "session_id": "festival-series-2024",
    "mode": "max"
  }'

# Series poster 2 (maintains consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create poster 2 of 4 for the same series. Same color palette and style, but feature a live band on stage.",
    "session_id": "festival-series-2024"
  }'
```

## 使用参考图片

通过参考图片来提升海报设计的质量：

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a movie poster using this actor photo as the main character. Dramatic noir style, high contrast black and white with one accent color (red). Add rain effects and city silhouette in background.",
    "mode": "max",
    "image_urls": ["https://example.com/actor-portrait.jpg"]
  }'
```

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 平衡性不足 | 在 eachlabs.ai 网站补充数据 |
| 内容违规 | 内容不符合规定 | 调整提示内容以符合政策要求 |
| 超时 | 生成过程复杂 | 将客户端超时时间设置为至少10分钟 |

## 相关技能

- `each-sense`：核心 API 文档
- `meta-ad-creative-generation`：社交媒体广告创意设计
- `product-photo-generation`：电子商务产品图片生成
- `image-generation`：通用图片生成工具