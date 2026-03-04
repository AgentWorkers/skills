---
name: instagram-content-generation
description: 使用 each::sense AI 生成适合 Instagram 的内容。包括动态帖子、故事、Reels 封面、轮播图、引用图片以及品牌视觉素材，所有内容均需遵循 Instagram 的格式规范和提升用户参与度的最佳实践。
metadata:
  author: eachlabs
  version: "1.0"
---
# Instagram内容生成

使用`each-sense`生成吸引人的Instagram内容。该技能能够创建适合Instagram各种布局、格式和视觉最佳实践的图片和视频。

## 功能

- **动态帖子**：1:1的正方形图片，以实现最大兼容性
- **故事（Stories）与短视频（Reels）**：9:16的竖屏内容，提供沉浸式的全屏体验
- **轮播帖子（Carousel Posts）**：多张连贯的图片，用于讲述故事
- **引用图（Quote Graphics）**：以文字为主的视觉内容，提升互动性
- **产品展示（Product Showcases）**：专注于电商和产品的视觉素材
- **幕后花絮（Behind-the-Scenes）**：真实、坦率的风格内容
- **公告图（Announcement Graphics）**：用于活动发布和促销活动的宣传内容
- **生活方式平铺图（Lifestyle Flat Lays）**：精心策划的产品展示
- **品牌美学网格（Brand Aesthetic Grid）**：在所有帖子中保持一致的视觉风格

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Instagram feed post for a coffee brand showing a latte with beautiful latte art, morning light, cozy cafe vibes",
    "mode": "max"
  }'
```

## Instagram格式与尺寸

| 布局 | 长宽比 | 推荐尺寸 | 使用场景 |
|-----------|--------------|------------------|----------|
| 动态帖子 | 1:1 | 1080x1080 | 标准动态帖子，最高兼容性 |
| 动态帖子 | 4:5 | 1080x1350 | 竖屏动态帖子，占用更多屏幕空间 |
| 故事 | 9:16 | 1080x1920 | 全屏临时内容 |
| 短视频 | 9:16 | 1080x1920 | 全屏视频内容 |
| 短视频封面 | 9:16 | 1080x1920 | 短视频的缩略图 |
| 轮播 | 1:1 | 1080x1080 | 多张图片的可滑动帖子 |

## 使用场景示例

### 1. 动态帖子（1:1正方形）

经典的1:1正方形格式，适用于Instagram的所有布局。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 square Instagram feed post for a sustainable fashion brand. Show a model in casual earth-toned clothing against a natural outdoor background. Warm, authentic aesthetic with soft natural lighting. Clean composition suitable for a curated Instagram grid.",
    "mode": "max"
  }'
```

### 2. 故事（9:16竖屏）

专为Instagram故事设计的竖屏内容。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 9:16 Instagram Story for a yoga studio. Show a serene meditation scene with a person in lotus position, soft morning light streaming through windows, calming pastel colors. Leave safe zones at top and bottom for Instagram UI elements and swipe-up area.",
    "mode": "max"
  }'
```

### 3. 短视频封面图片

吸引眼球的缩略图，能够代表短视频的内容并鼓励用户点击。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 9:16 Reel cover image for a cooking tutorial. Show an appetizing finished dish (pasta with fresh basil) from above, vibrant colors, food photography style. The image should be eye-catching and make viewers want to watch the full Reel. Leave space at bottom for the Reel title overlay.",
    "mode": "max"
  }'
```

### 4. 轮播帖子（多张图片）

创建多张连贯的图片，用于讲述故事或展示多个产品。

```bash
# First carousel image - Cover slide
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 carousel image 1 of 5 for a skincare brand. This is the cover slide showing all 5 products arranged beautifully with soft pink and white aesthetic, clean minimal background, soft shadows. Premium feel.",
    "session_id": "skincare-carousel-001",
    "mode": "max"
  }'

# Second carousel image - Product detail
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create carousel image 2 of 5. Show the cleanser product close-up with water droplets and fresh ingredients like cucumber slices. Same aesthetic and lighting as the first image.",
    "session_id": "skincare-carousel-001",
    "mode": "max"
  }'

# Third carousel image - Another product
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create carousel image 3 of 5. Show the moisturizer with a soft texture swatch, dewy fresh feel. Maintain visual consistency with previous images.",
    "session_id": "skincare-carousel-001",
    "mode": "max"
  }'
```

### 5. 引用图

以文字为主的视觉内容，提升互动性和分享率。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Instagram quote graphic with the text: \"Success is not final, failure is not fatal: it is the courage to continue that counts.\" Use a minimalist design with elegant serif typography on a soft gradient background (light beige to warm cream). Add subtle decorative elements like thin lines or small botanical illustrations. Suitable for a motivational or business coaching account.",
    "mode": "max"
  }'
```

### 6. 产品展示帖子

专注于电商的内容，突出产品与生活方式的结合。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 4:5 Instagram product showcase for wireless headphones. Show the headphones being worn by a stylish person in an urban setting, walking through a modern city. Lifestyle photography style with natural lighting, premium aspirational feel. The product should be clearly visible but feel natural in the scene.",
    "mode": "max"
  }'
```

### 7. 幕后花絮内容

真实、坦率的风格内容，有助于建立与观众的连接。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 behind-the-scenes Instagram post for a bakery. Show a baker in the kitchen early morning, hands covered in flour, kneading dough. Warm golden lighting, authentic and candid feel - not overly polished. Capture the passion and craft of artisan baking. Documentary photography style.",
    "mode": "max"
  }'
```

### 8. 公告图

用于活动发布、促销和宣传的公告内容。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Instagram announcement graphic for a summer sale. Bold, eye-catching design with tropical vibes - palm leaves, bright colors (coral, turquoise, sunny yellow). Leave clear space for text overlay that will say \"SUMMER SALE - UP TO 50% OFF\". Modern, fresh, energetic aesthetic suitable for a fashion brand.",
    "mode": "max"
  }'
```

### 9. 生活方式平铺图

精心策划的产品展示，适合生活方式和产品品牌。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Instagram flat lay for a travel brand. Overhead shot of travel essentials arranged aesthetically: passport, sunglasses, straw hat, camera, map, coffee cup, and small succulent. Marble or light wood surface background. Clean, organized, Pinterest-worthy composition with soft natural lighting. Wanderlust aesthetic.",
    "mode": "max"
  }'
```

### 10. 品牌美学网格

创建一致的视觉风格，提升Instagram的整体视觉效果。

```bash
# First grid image
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Instagram post for a minimalist home decor brand. Show a clean, modern living room corner with a simple plant, neutral tones (white, beige, light gray), lots of negative space. This is part of a cohesive grid aesthetic - keep colors muted and style consistent. Scandinavian interior design influence.",
    "session_id": "home-decor-grid",
    "mode": "max"
  }'

# Second grid image - maintaining consistency
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create another 1:1 post for the same minimalist home decor brand. Show a bedroom detail - perhaps a textured throw on a bed with a small nightstand. Same color palette and aesthetic as the previous image to maintain grid cohesion.",
    "session_id": "home-decor-grid",
    "mode": "max"
  }'

# Third grid image
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a third 1:1 post continuing the grid aesthetic. Show a close-up of a ceramic vase with dried pampas grass. Same minimalist, neutral, Scandinavian-inspired style.",
    "session_id": "home-decor-grid",
    "mode": "max"
  }'
```

## 最佳实践

### 动态帖子
- **网格布局**：考虑单个帖子在个人资料网格中的整体效果
- **统一编辑风格**：保持帖子之间的颜色和风格一致性
- **1:1 vs 4:5**：使用1:1格式以实现最大兼容性，使用4:5格式以获得更好的视觉效果
- **焦点元素**：将关键元素放在中心，以便在缩略图中显示

### 故事
- **安全区域**：避免将重要内容放在屏幕顶部15%和底部20%的区域（这些区域可能被UI元素遮挡）
- **竖屏设计**：专门为竖屏设计，而非横屏裁剪
- **互动元素**：预留空间用于投票、问题和贴纸
- **清晰易读**：内容应易于快速阅读

### 轮播
- **吸引注意力**：让第一张图片足够吸引人，以鼓励用户滑动浏览
- **视觉流程**：创建连贯的叙事或逻辑顺序
- **统一风格**：在整个轮播中保持相同的滤镜、字体和美学风格
- **结尾的呼吁行动（CTA）**：在最后一张图片中使用呼吁行动或总结

### 短视频封面
- **缩略图吸引力**：为短视频标签页中的小预览图进行设计
- **清晰的主题**：避免使用过于复杂的背景，以免在缩略图中难以看清
- **文字可读性**：如果使用文字，请确保在缩略图大小下仍可清晰显示

## Instagram内容创作提示

在创建Instagram内容时，请在提示中包含以下信息：

1. **格式**：指定长宽比（1:1、4:5、9:16）
2. **内容类型**：动态帖子、故事、短视频封面、轮播图片的数量
3. **品牌/领域**：该内容适用于哪种类型的账号？
4. **美学风格**：极简主义、大胆、复古、现代等
5. **色彩调色板**：具体的颜色或整体色调（温暖、冷色调、中性色）
6. **构图**：平铺展示、竖屏展示、生活方式风格、特写等
7. **文字空间**：如果需要添加字幕或叠加文字，请预留相应空间

### 示例提示结构

```
"Create a [aspect ratio] Instagram [content type] for a [brand/niche].
Show [visual description] with [aesthetic/mood].
[Color and style preferences].
[Additional requirements like text space, grid consistency, etc.]"
```

## 模式选择

在生成内容之前，请询问用户：

**“您需要快速且低成本的内容，还是高质量的内容？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终内容、作品集帖子、重要活动 | 较慢 | 最高质量 |
| `eco` | 快速草图、内容规划、A/B测试概念 | 较快 | 良好质量 |

## 多轮迭代内容生成

使用`session_id`来迭代内容并保持视觉一致性：

```bash
# Initial concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Instagram post for a jewelry brand, elegant and minimal",
    "session_id": "jewelry-content"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make it more luxurious, add soft bokeh background with golden tones",
    "session_id": "jewelry-content"
  }'

# Request Story version
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a 9:16 Story version of this same visual style",
    "session_id": "jewelry-content"
  }'
```

## 内容批量生成

生成多篇内容以供规划使用：

```bash
# Monday motivation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 motivational Monday post for a fitness brand - energetic gym scene, morning workout vibes",
    "mode": "eco"
  }'

# Wednesday product feature
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 product showcase for the same fitness brand - protein shake in a gym bag flat lay",
    "mode": "eco"
  }'

# Friday lifestyle
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 lifestyle post for the same fitness brand - friends laughing after a workout, feel-good Friday vibes",
    "mode": "eco"
  }'
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 资源不足 | 在eachlabs.ai平台上补充资源 |
| 内容违规 | 内容违反政策 | 调整提示以符合内容政策 |
| 超时 | 生成过程复杂 | 将客户端超时设置至少为10分钟 |

## 相关技能

- `each-sense` - 核心API文档
- `meta-ad-creative-generation` - Meta（Facebook & Instagram）广告创意生成
- `product-photo-generation` - 电商产品图片生成
- `tiktok-ad-creative-generation` - TikTok内容创作