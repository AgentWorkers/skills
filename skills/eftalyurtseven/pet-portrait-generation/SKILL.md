---
name: pet-portrait-generation
description: 使用 each::sense AI 生成自定义的宠物肖像。您可以根据照片创建逼真、艺术化或风格化的宠物肖像，支持多种风格，包括卡通、文艺复兴风格、水彩画、波普艺术、动漫风格以及自定义的产品原型图。
metadata:
  author: eachlabs
  version: "1.0"
---
# 宠物肖像生成

使用 `each-sense` 功能，您可以生成令人惊叹的定制宠物肖像。将您的宠物照片转换为各种风格的精美艺术品——从逼真的肖像到有趣的卡通插画，再到华丽的文艺复兴风格画作，以及个性化的产品。

## 特点

- **逼真肖像**：专业工作室品质的宠物摄影
- **卡通/插画风格**：可爱、色彩丰富的宠物卡通形象
- **文艺复兴/皇家风格**：带有历史服饰的华丽肖像
- **水彩画**：艺术风格的水彩宠物作品
- **波普艺术**：大胆、充满活力的波普艺术风格肖像
- **动漫风格**：日式动漫风格的宠物角色
- **服装肖像**：宠物穿着各种服装和主题服饰
- **多宠物肖像**：包含多只宠物的家庭合照
- **纪念肖像**：为心爱的宠物制作的纪念艺术品
- **产品样图**：宠物肖像应用于马克杯、画布和商品上

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a beautiful portrait of my golden retriever in a classic oil painting style",
    "image_urls": ["https://example.com/my-pet-photo.jpg"],
    "mode": "max"
  }'
```

## 使用案例示例

### 1. 逼真宠物肖像

创建一张专业工作室品质的肖像，捕捉宠物的个性。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a realistic professional portrait of my cat. Studio lighting, soft bokeh background in warm earth tones. Capture the eyes beautifully with catchlights. High-end pet photography style.",
    "image_urls": ["https://example.com/my-cat.jpg"],
    "mode": "max"
  }'
```

### 2. 卡通/插画宠物肖像

将您的宠物变成一个有趣、色彩丰富的卡通角色。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform my dog into a cute cartoon illustration. Disney/Pixar style with big expressive eyes, playful pose. Vibrant colors, clean lines. Include a fun background with bones and toys.",
    "image_urls": ["https://example.com/my-dog.jpg"],
    "mode": "max"
  }'
```

### 3. 文艺复兴/皇家宠物肖像

为您的宠物打造一幅带有历史服饰的华丽肖像。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a renaissance-style royal portrait of my cat. Dress them as a noble king with a golden crown, velvet robe with ermine fur trim, and royal jewelry. Classical oil painting style, dramatic lighting, ornate gilded frame effect. Regal and majestic.",
    "image_urls": ["https://example.com/my-cat.jpg"],
    "mode": "max"
  }'
```

### 4. 水彩宠物画

创作一幅精美的水彩宠物作品。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Paint my dog in a loose, expressive watercolor style. Soft edges, beautiful color bleeds and washes. Capture their personality with artistic brush strokes. Pastel background with splashes of color. Fine art watercolor painting look.",
    "image_urls": ["https://example.com/my-dog.jpg"],
    "mode": "max"
  }'
```

### 5. 波普艺术宠物肖像

创作一幅受安迪·沃霍尔启发的大胆、充满活力的波普艺术肖像。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a pop art portrait of my cat in Andy Warhol style. Bold, bright contrasting colors - hot pink, electric blue, yellow, orange. High contrast, graphic style with halftone dots. Create a 2x2 grid with different color variations.",
    "image_urls": ["https://example.com/my-cat.jpg"],
    "mode": "max"
  }'
```

### 6. 动漫风格宠物肖像

将您的宠物变成一个可爱的动漫角色。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an anime-style portrait of my dog. Japanese anime aesthetic with big sparkly eyes, soft shading, and cute kawaii expression. Include cherry blossoms in the background. Studio Ghibli inspired, warm and whimsical.",
    "image_urls": ["https://example.com/my-dog.jpg"],
    "mode": "max"
  }'
```

### 7. 穿着服装的宠物

给您的宠物穿上有趣的服装和主题服饰。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a portrait of my cat as a space astronaut. Wearing a detailed NASA spacesuit with helmet, floating in space with Earth visible in the background. Stars and nebula. Realistic lighting, cinematic quality.",
    "image_urls": ["https://example.com/my-cat.jpg"],
    "mode": "max"
  }'
```

### 8. 多宠物家庭肖像

创作一张包含多只宠物的美丽全家福。

```bash
# First request - provide all pet photos
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a family portrait with all three of my pets together. Classical portrait style with a warm, cozy living room background. Position them naturally as if they are posing together - the dog in the center, cats on either side. Soft, warm lighting, harmonious composition.",
    "image_urls": [
      "https://example.com/my-dog.jpg",
      "https://example.com/my-cat1.jpg",
      "https://example.com/my-cat2.jpg"
    ],
    "session_id": "pet-family-portrait",
    "mode": "max"
  }'

# Follow-up to adjust the portrait
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Can you make the background a garden setting with flowers instead? Keep the same arrangement of the pets.",
    "session_id": "pet-family-portrait"
  }'
```

### 9. 纪念宠物肖像

为心爱的宠物制作一幅感人的纪念肖像。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a memorial portrait for my beloved dog who passed away. Peaceful, serene setting with soft golden light. Include angel wings, subtle rainbow bridge elements in the background. Ethereal and comforting, celebrating their spirit. Beautiful tribute artwork.",
    "image_urls": ["https://example.com/my-dog.jpg"],
    "mode": "max"
  }'
```

### 10. 产品上的宠物肖像（马克杯、画布）

生成宠物肖像在商品上的样图。

```bash
# Pet portrait on a mug
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a product mockup of my cat portrait on a white ceramic coffee mug. The portrait should be a cute illustrated style. Show the mug on a wooden table with coffee, cozy morning setting. Professional product photography.",
    "image_urls": ["https://example.com/my-cat.jpg"],
    "session_id": "pet-products",
    "mode": "max"
  }'

# Same pet portrait on canvas
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a mockup of this same pet portrait as a canvas print hanging on a living room wall. Modern interior setting, natural lighting. Show it as wall art in context.",
    "session_id": "pet-products"
  }'
```

## 最佳实践

### 照片质量提示
- **清晰的照片**：使用光线充足、对焦清晰的宠物照片
- **面部可见**：确保宠物的面部清晰可见，没有遮挡
- **多角度照片**：为了获得最佳效果，请提供从不同角度拍摄的照片
- **自然表情**：自然拍摄的照片通常能拍出最好的肖像

### 提示技巧
- **明确风格**：指定具体的艺术风格、艺术家或参考作品
- **描述氛围**：包含情感基调（ playful, regal, peaceful 等）
- **指定颜色**：请求特定的色彩搭配或方案
- **背景细节**：描述您想要的场景或背景

### 示例提示结构

```
"Create a [style] portrait of my [pet type].
[Specific style details and references].
[Background/setting description].
[Mood and lighting].
[Any special elements or accessories]."
```

## 模式选择

在生成之前询问用户：

**“您想要快速且经济实惠的结果，还是最高质量的结果？”**

| 模式 | 适合场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终肖像、礼物、打印品 | 较慢 | 最高 |
| `eco` | 快速预览、风格探索 | 较快 | 良好 |

## 多轮创意迭代

使用 `session_id` 对肖像进行优化和迭代：

```bash
# Initial portrait
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a renaissance portrait of my dog as a nobleman",
    "image_urls": ["https://example.com/my-dog.jpg"],
    "session_id": "dog-portrait-project"
  }'

# Refine the result
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the costume more elaborate with gold embroidery and add a sword",
    "session_id": "dog-portrait-project"
  }'

# Try different variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 2 more variations with different poses and backgrounds",
    "session_id": "dog-portrait-project"
  }'
```

## 风格探索

生成不同的风格，找到完美的效果：

```bash
# Explore different styles with eco mode for speed
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create my cat portrait in oil painting style",
    "image_urls": ["https://example.com/my-cat.jpg"],
    "mode": "eco"
  }'

curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create my cat portrait in minimalist line art style",
    "image_urls": ["https://example.com/my-cat.jpg"],
    "mode": "eco"
  }'

curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create my cat portrait in stained glass window style",
    "image_urls": ["https://example.com/my-cat.jpg"],
    "mode": "eco"
  }'
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 平衡不足 | 在 eachlabs.ai 充值 |
| Image not processing | 图像 URL 无效或无法访问 | 确保图像 URL 可公开访问 |
| Timeout | 生成过程复杂 | 将客户端超时时间设置为至少 10 分钟 |
| 肖像相似度低 | 图像质量差 | 使用面部清晰、光线充足的照片 |

## 相关技能

- `each-sense` - 核心 API 文档
- `product-photo-generation` - 电商产品拍摄
- `image-generation` - 通用图像生成