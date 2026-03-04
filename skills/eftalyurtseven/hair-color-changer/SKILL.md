---
name: hair-color-changer
description: 使用 each::sense AI 更改照片中的头发颜色。可以将头发颜色转换为任何颜色，包括自然色调、梦幻色彩、渐变效果、高光等。
metadata:
  author: eachlabs
  version: "1.0"
---
# 发色变换工具

使用 `each-sense` 功能可以改变照片中的头发颜色。该工具支持从微妙的自然变化到大胆的梦幻色彩的变换，同时具备渐变（ombre）、高光（highlights）和多色调（multi-tone）等复杂效果。

## 主要功能

- **自然发色**：金色、棕色、黑色、红色、红棕色
- **梦幻发色**：紫色、蓝色、粉色、绿色等
- **渐变效果**：从发根到发梢的平滑色彩过渡
- **高光与低光**：立体的色彩层次
- **灰发与银发**：优雅的银色、铂金色和灰色调
- **色彩校正**：修复或增强现有的头发颜色
- **多次尝试**：可以反复调整结果，尝试不同的颜色

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the hair color to platinum blonde, keep it looking natural and shiny",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

## 使用案例示例

### 1. 将头发颜色改为金色

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the hair to a warm honey blonde color. Keep the hair texture and shine natural, maintain realistic highlights throughout.",
    "image_urls": ["https://example.com/original-photo.jpg"],
    "mode": "max"
  }'
```

### 2. 将头发颜色改为棕色

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform the hair to a rich chocolate brown color. Add subtle warm undertones and natural-looking dimension to the brunette shade.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 3. 将头发颜色改为红色/红棕色

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the hair color to a vibrant auburn red. Make it look like natural ginger hair with copper highlights that catch the light.",
    "image_urls": ["https://example.com/model-photo.jpg"],
    "mode": "max"
  }'
```

### 4. 梦幻发色（紫色、蓝色、粉色）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform the hair to a vivid galaxy purple color. Make it look like professionally dyed hair with deep violet tones and subtle blue undertones. Keep the hair healthy and shiny looking.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

```bash
# Electric blue hair
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the hair to electric blue color, like a bold fashion statement. Mix of deep blue and bright cyan tones throughout.",
    "image_urls": ["https://example.com/photo.jpg"],
    "mode": "max"
  }'
```

```bash
# Pastel pink hair
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform the hair to a soft pastel pink color. Think rose gold meets cotton candy - delicate, feminine, and Instagram-worthy.",
    "image_urls": ["https://example.com/headshot.jpg"],
    "mode": "max"
  }'
```

### 5. 渐变效果

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an ombre hair effect - dark brown roots transitioning smoothly to caramel blonde at the ends. Make the gradient look natural and well-blended like salon balayage.",
    "image_urls": ["https://example.com/full-portrait.jpg"],
    "mode": "max"
  }'
```

```bash
# Fantasy ombre
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a fantasy ombre effect with dark purple roots fading into bright pink, then to peachy coral at the tips. Smooth gradient transitions like a sunset.",
    "image_urls": ["https://example.com/model.jpg"],
    "mode": "max"
  }'
```

### 6. 高光与低光效果

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add dimensional highlights and lowlights to the hair. Keep the base color but add face-framing blonde highlights and subtle caramel lowlights throughout for depth and dimension.",
    "image_urls": ["https://example.com/brunette-photo.jpg"],
    "mode": "max"
  }'
```

```bash
# Babylights effect
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add subtle babylights throughout the hair - very fine, delicate highlights like sun-kissed natural lightening. Keep it soft and natural looking.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 7. 灰发/银发

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform the hair to an elegant silver gray color. Make it look like intentional fashion-forward silver hair, not aging gray - metallic, shiny, and well-maintained.",
    "image_urls": ["https://example.com/fashion-photo.jpg"],
    "mode": "max"
  }'
```

```bash
# Platinum silver
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change hair to platinum silver with icy undertones. Think high fashion editorial silver - cool-toned, luminous, and striking.",
    "image_urls": ["https://example.com/model-headshot.jpg"],
    "mode": "max"
  }'
```

### 8. 自然发色变化

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Adjust the hair color to be 2 shades darker, turning it from medium brown to a deep espresso brown. Keep all the natural texture and shine.",
    "image_urls": ["https://example.com/natural-photo.jpg"],
    "mode": "max"
  }'
```

```bash
# Warm up cool tones
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add warm golden undertones to the existing hair color. Keep the same overall shade but remove any ashy tones and make it warmer and more vibrant.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "eco"
  }'
```

### 9. 从同一张照片中尝试多种颜色

使用 `session_id` 可以在同一张照片上尝试不同的颜色：

```bash
# First option - Blonde
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change my hair to platinum blonde. I want to see how I would look with this color.",
    "image_urls": ["https://example.com/my-photo.jpg"],
    "session_id": "hair-color-tryout-001",
    "mode": "eco"
  }'

# Second option - Red (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now show me the same photo but with fiery red hair instead.",
    "session_id": "hair-color-tryout-001",
    "mode": "eco"
  }'

# Third option - Black (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "And one more variation with jet black hair please.",
    "session_id": "hair-color-tryout-001",
    "mode": "eco"
  }'
```

### 10. 变化前后的对比

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the hair to rose gold color, then create a side-by-side before and after comparison showing the original on the left and the new color on the right.",
    "image_urls": ["https://example.com/original-portrait.jpg"],
    "mode": "max"
  }'
```

```bash
# Iterative refinement for comparison
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform the hair to strawberry blonde.",
    "image_urls": ["https://example.com/client-photo.jpg"],
    "session_id": "client-consultation-001",
    "mode": "max"
  }'

# Follow-up to adjust
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the strawberry blonde a bit more pink and less orange. Also make it slightly lighter overall.",
    "session_id": "client-consultation-001",
    "mode": "max"
  }'
```

## 最佳实践

### 获得真实效果的建议

- **良好的光线**：选择头发部分光线清晰、均匀的照片
- **头发清晰可见**：确保头发没有被遮挡
- **正面拍摄**：正面或 3/4 角度的照片效果最佳
- **高分辨率**：高质量的源图片能获得更好的效果

### 提示建议

1. **明确要求**：详细描述你想要的发色（例如“暖色调的金色”而不是简单的“金色”
2. **提及底色调**：说明发色的底色调（暖色调、冷色调、中性色调、灰调、金色）
3. **保持纹理**：要求保留头发的自然纹理和光泽
4. **合理预期**：梦幻发色在较浅的底色上可能显得更加鲜艳

### 示例提示结构

```
"Change the hair to [specific color with undertones].
[Additional details about dimension, highlights, or effects].
Keep the hair looking [natural/healthy/shiny/textured]."
```

## 模式选择

**“您想要快速的结果还是最高质量？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终效果、客户展示、作品集制作 | 较慢 | 最高质量 |
| `eco` | 快速预览、尝试多种颜色、概念探索 | 较快 | 良好质量 |

## 多次尝试调整颜色

使用 `session_id` 可以反复调整和探索颜色：

```bash
# Start with a base change
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change my hair to copper red",
    "image_urls": ["https://example.com/selfie.jpg"],
    "session_id": "hair-exploration"
  }'

# Request adjustment
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make it more auburn and less orange, add some brown lowlights",
    "session_id": "hair-exploration"
  }'

# Try a completely different direction
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Actually, let me see the original photo with silver gray hair instead",
    "session_id": "hair-exploration"
  }'
```

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 预测生成失败 | 请在 eachlabs.ai 网站充值 |
| 未检测到头发 | 照片中看不到头发 | 使用头发清晰可见的照片 |
| 结果不自然 | 图像质量较低 | 使用分辨率更高、光线良好的照片 |
| 超时 | 生成过程复杂 | 将客户端的超时时间设置为至少 10 分钟 |

## 相关技能

- `each-sense`：核心 API 文档
- `face-swap`：面部替换功能
- `image-edit`：通用图像编辑工具
- `product-photo-generation`：电商产品图片生成工具