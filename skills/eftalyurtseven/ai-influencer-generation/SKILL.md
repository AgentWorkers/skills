---
name: AI Influencer Generation
description: 使用 `each::sense` API 生成一致的人工智能影响者人物形象及社交媒体内容
metadata:
  category: image-generation
  api: sense
  endpoint: https://sense.eachlabs.run/chat
  features:
    - consistent-persona
    - social-media-content
    - brand-collaborations
    - virtual-models
---
# 人工智能影响者生成

使用 each::sense API 为社交媒体内容、品牌合作以及虚拟模特创建一致的人工智能影响者形象。

## 概述

“人工智能影响者生成”技能使您能够创建并维护以下方面的虚拟形象的一致性：

- **一致的人工智能形象**：生成在所有内容中外观一致的人工智能影响者
- **社交媒体内容**：创建 Instagram 帖子、Stories、Reels 缩略图、TikTok 内容等
- **品牌代言人**：用于产品推广和合作的虚拟代言人
- **虚拟模特**：用于时尚、生活方式和商业内容的 AI 生成模型

## 快速入门

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a portrait of a young female AI influencer with long dark wavy hair, warm brown eyes, natural makeup, wearing a casual white linen shirt. Soft golden hour lighting, neutral background. Professional photography style, Instagram aesthetic.",
    "mode": "max"
  }'
```

## 内容类型

| 内容类型 | 描述 | 推荐模式 |
|--------------|-------------|------------------|
| Instagram 帖子 | 主页照片、生活方式照片、肖像 | max |
| Instagram Stories | 休闲的幕后瞬间 | eco |
| Reels 缩略图 | 视频内容的吸引人封面图片 | max |
| TikTok 内容 | 紧跟潮流的视觉效果和缩略图 | eco |
| YouTube 缩略图 | 高质量的预览图片 | max |
| 品牌合作 | 产品植入、赞助内容 | max |
| 时尚/每日穿搭 | 当日穿搭、风格展示 | max |
| 旅行内容 | 基于地点的生活方式摄影 | max |

## 使用案例示例

### 1. 创建人工智能影响者形象（初始角色）

为人工智能影响者设定基本外观，以确保在所有后续内容中的统一性。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a detailed portrait of an AI influencer persona: A 25-year-old woman with shoulder-length auburn hair with subtle waves, bright green eyes, light freckles across her nose and cheeks, warm peachy skin tone. She has a friendly, approachable smile. Wearing minimal natural makeup. Clean white background, soft studio lighting. Ultra-realistic photography, 4K quality.",
    "session_id": "influencer-maya-2024",
    "mode": "max"
  }'
```

### 2. Instagram 生活方式帖子

为 Instagram 主页生成休闲的生活方式内容。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate an Instagram lifestyle photo: A young woman with shoulder-length auburn wavy hair, green eyes, and light freckles. She is sitting at a cozy coffee shop, holding a ceramic latte cup, wearing an oversized cream knit sweater. Warm ambient lighting, bokeh background with fairy lights. Candid pose, genuine smile. Instagram aesthetic, lifestyle photography.",
    "session_id": "influencer-maya-2024",
    "mode": "max",
    "image_urls": ["https://example.com/maya-reference.jpg"]
  }'
```

### 3. Instagram Stories 内容

创建轻松有趣的 Stories 内容。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an Instagram Stories photo: Close-up selfie of a young woman with auburn wavy hair and green eyes, light freckles. She is making a playful expression, holding up a peace sign. Morning light from a window, casual bedroom setting. Wearing a simple white t-shirt. Authentic, unfiltered look. Vertical 9:16 aspect ratio.",
    "session_id": "influencer-maya-2024",
    "mode": "eco",
    "image_urls": ["https://example.com/maya-reference.jpg"]
  }'
```

### 4. 品牌合作帖子

为品牌合作生成赞助内容。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a brand collaboration photo: A young woman with auburn wavy hair, green eyes, and freckles. She is elegantly holding a luxury skincare product bottle close to her face. Clean, minimalist white studio background. Wearing a silk robe in blush pink. Soft beauty lighting, dewy skin appearance. Professional product photography style, aspirational aesthetic.",
    "session_id": "influencer-maya-2024",
    "mode": "max",
    "image_urls": ["https://example.com/maya-reference.jpg"]
  }'
```

### 5. 旅行内容

创建激发旅行热情的摄影作品。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate travel influencer content: A young woman with auburn wavy hair, green eyes, and light freckles. She is standing on a scenic cliff overlooking the Santorini coastline, white and blue buildings in the background. Wearing a flowing white maxi dress, wind gently blowing her hair. Golden sunset lighting. Travel photography, wanderlust aesthetic, editorial quality.",
    "session_id": "influencer-maya-2024",
    "mode": "max",
    "image_urls": ["https://example.com/maya-reference.jpg"]
  }'
```

### 6. 时尚/每日穿搭

展示当天的穿搭内容。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an OOTD fashion post: Full-body shot of a young woman with auburn wavy hair, green eyes, and freckles. She is posing confidently on an urban street. Wearing a tailored beige blazer, white crop top, high-waisted dark denim jeans, and white sneakers. Carrying a designer handbag. Natural daylight, city backdrop with blurred pedestrians. Street style photography, fashion editorial aesthetic.",
    "session_id": "influencer-maya-2024",
    "mode": "max",
    "image_urls": ["https://example.com/maya-reference.jpg"]
  }'
```

### 7. 健身内容

生成注重健康和福祉的图片。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create fitness influencer content: A young athletic woman with auburn hair in a high ponytail, green eyes, light freckles. She is doing a yoga pose on a mat in a bright, modern home gym. Wearing a matching sage green sports bra and leggings set. Morning sunlight streaming through large windows. Healthy glow, natural sweat. Fitness photography, wellness aesthetic.",
    "session_id": "influencer-maya-2024",
    "mode": "max",
    "image_urls": ["https://example.com/maya-reference.jpg"]
  }'
```

### 8. 产品推广

创建引人注目的产品展示内容。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate product promotion content: Close-up of a young woman with auburn wavy hair, green eyes, and freckles. She is applying lip gloss while looking at camera with a slight smile. The product is clearly visible in frame. Soft ring light reflection in eyes, beauty studio setting. Pink and rose gold color palette. Beauty influencer aesthetic, product-focused composition.",
    "session_id": "influencer-maya-2024",
    "mode": "max",
    "image_urls": ["https://example.com/maya-reference.jpg"]
  }'
```

### 9. 幕后内容

生成真实的幕后场景。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create behind-the-scenes content: A young woman with auburn wavy hair, green eyes, and freckles. She is sitting in a makeup chair, hair in rollers, laughing candidly while a makeup artist works. Studio environment visible with lighting equipment in background. Wearing a black cape over her clothes. Documentary style, authentic moment, slightly desaturated tones.",
    "session_id": "influencer-maya-2024",
    "mode": "eco",
    "image_urls": ["https://example.com/maya-reference.jpg"]
  }'
```

### 10. 季节性/节日内容

为特殊场合创建主题内容。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate holiday content: A young woman with auburn wavy hair, green eyes, and light freckles. She is decorating a Christmas tree, wearing a cozy red knit sweater. Warm interior with fireplace glow in background, string lights creating bokeh. Holding a gold ornament, looking at camera with a warm smile. Festive, cozy atmosphere, holiday photography aesthetic.",
    "session_id": "influencer-maya-2024",
    "mode": "max",
    "image_urls": ["https://example.com/maya-reference.jpg"]
  }'
```

## 维护角色一致性

### 使用参考图片

提供 `image_urls` 以确保人工智能影响者在所有内容中的外观一致：

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate new content maintaining the exact appearance of the reference image. Place her in a beach setting at sunset, wearing a casual summer dress.",
    "image_urls": ["https://your-storage.com/influencer-base-portrait.jpg"],
    "session_id": "influencer-maya-2024",
    "mode": "max"
  }'
```

### 多轮生成

使用 `session_id` 在多轮生成中保持角色背景的一致性：

```bash
# First request - establish persona
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "My AI influencer is named Sophia. She has long blonde hair, blue eyes, and a bright smile. She is 26 years old with a California beach vibe aesthetic.",
    "session_id": "sophia-influencer-session"
  }'

# Second request - generate content using established persona
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate an Instagram post of Sophia at a rooftop party in LA at night.",
    "session_id": "sophia-influencer-session",
    "mode": "max"
  }'
```

## 最佳实践

### 角色一致性

1. **创建详细的角色档案**：记录头发颜色、眼睛颜色、肤色、标志性特征以及偏好的审美风格
2. **使用一致的描述语**：在每个提示中始终包含关键识别特征
3. **保持风格连贯性**：保持光线、色彩分级和摄影风格的统一
4. **保存参考图片**：将生成的图片作为未来内容的参考

### 提示技巧

- **具体描述特征**：例如“深红波浪发、绿色眼睛、浅色雀斑”，而不是“迷人的女性”
- **描述审美风格**：包括摄影风格、光线和氛围
- **详细说明服装**：颜色、面料和风格，以体现个人品牌特色
- **提供环境背景**：与影响者的定位相匹配的场景
- **指定拍摄角度**：特写、全身照、自然照等

### 内容日程策略

| 日期 | 内容类型 | 模式 | 重点 |
|-----|--------------|------|-------|
| 星期一 | 励志语叠加 | eco | 灵感 |
| 星期二 | 时尚/每日穿搭 | max | 风格 |
| 星期三 | 幕后花絮 | eco | 真实感 |
| 星期四 | 产品/品牌内容 | max | 营收 |
| 星期五 | 生活方式/周末预览 | max | 互动性 |
| 周末 | 旅行/冒险 | max | 激发向往 |

## 模式选择

| 模式 | 适用场景 | 质量 | 速度 |
|------|----------|---------|-------|
| `max` | 主题图片、品牌合作、作品集 | 最高质量 | 标准 |
| `eco` | Stories、休闲内容、大量发布 | 良好 | 更快 |

## 错误处理

```bash
# Check response for errors
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate AI influencer content...",
    "mode": "max"
  }' 2>&1 | while read line; do
    if echo "$line" | grep -q "error"; then
      echo "Error occurred: $line"
      exit 1
    fi
    echo "$line"
  done
```

## 相关技能

- [图像生成](/skills/eachlabs-image-generation/SKILL.md) - 通用图像生成功能
- [产品视觉效果](/skills/eachlabs-product-visuals/SKILL.md) - 用于品牌合作的产品摄影
- [时尚 AI](/skills/eachlabs-fashion-ai/SKILL.md) - 时尚和风格内容生成