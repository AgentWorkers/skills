---
name: photo-restoration
description: 使用 each::sense AI 恢复和优化老旧、损坏或质量下降的照片。修复划痕、撕裂、褪色等问题，修复黑白照片的颜色，并恢复历史图片中的人脸。
metadata:
  author: eachlabs
  version: "1.0"
---
# 照片修复

使用 `each-sense` 工具来修复和优化老旧、损坏或质量下降的照片。该功能依托人工智能修复模型，能够修复划痕、为黑白照片上色、修复褪色问题、去除胶片颗粒感，让受损的照片焕发生机。

## 主要功能

- **损伤修复**：修复划痕、撕裂、褶皱等物理性损伤
- **上色**：为黑白照片添加自然色彩
- **褪色恢复**：恢复褪色或变淡照片的鲜艳度
- **水渍修复**：修复受水或潮湿损坏的照片
- **人脸修复**：优化和修复老旧或质量较差照片中的人脸
- **去除胶片颗粒感**：清除老照片中的颗粒和噪点
- **历史照片优化**：提升档案级或复古照片的质量
- **破损照片重建**：数字化修复破损的照片

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore this old damaged family photo - fix the scratches and improve the overall quality",
    "mode": "max",
    "image_urls": ["https://example.com/old-family-photo.jpg"]
  }'
```

## 使用案例示例

### 1. 老旧损坏照片修复

修复一张存在多种损伤（如划痕、污渍和质量下降）的照片。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore this old damaged photo from the 1950s. It has scratches, some staining, and general degradation. Please repair the damage while preserving the authentic vintage feel.",
    "mode": "max",
    "image_urls": ["https://example.com/damaged-1950s-photo.jpg"]
  }'
```

### 2. 黑白照片上色

为黑白照片添加逼真的色彩。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this black and white photo from the 1940s. It shows a family portrait - add natural, realistic colors to skin tones, clothing, and the background.",
    "mode": "max",
    "image_urls": ["https://example.com/bw-family-portrait.jpg"]
  }'
```

### 3. 修复划痕

去除照片上的划痕和表面损伤。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the scratches from this photo. There are multiple deep scratches across the surface and some light surface marks. Keep the image sharp and clear after repair.",
    "mode": "max",
    "image_urls": ["https://example.com/scratched-photo.jpg"]
  }'
```

### 4. 修复褪色照片

恢复褪色照片的色彩和对比度。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Enhance this faded photo - the colors have washed out over time and the image looks dull. Restore the vibrancy and contrast while keeping it looking natural, not over-processed.",
    "mode": "max",
    "image_urls": ["https://example.com/faded-vintage-photo.jpg"]
  }'
```

### 5. 水渍损坏照片修复

修复受水或潮湿损坏的照片。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore this water damaged photo. It has staining, warping effects, and some areas where the image has deteriorated due to moisture. Recover as much detail as possible.",
    "mode": "max",
    "image_urls": ["https://example.com/water-damaged-photo.jpg"]
  }'
```

### 6. 修复老旧照片中的人脸

优化和修复老旧照片中模糊或质量较差的人脸。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore the faces in this old family photo. The faces are blurry and lack detail. Enhance facial features to make them clear and recognizable while maintaining the authentic look of the era.",
    "mode": "max",
    "image_urls": ["https://example.com/old-blurry-faces.jpg"]
  }'
```

### 7. 历史照片修复

使用专业级修复技术恢复档案级照片的质量。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore this historical photograph from the early 1900s. It is a street scene that has significant age-related degradation. Improve clarity, fix damage, and optionally colorize it while preserving historical accuracy.",
    "mode": "max",
    "image_urls": ["https://example.com/historical-1900s-street.jpg"]
  }'
```

### 8. 家庭照片修复

通过全面修复技术恢复珍贵的家庭回忆。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore this precious family photo from my grandparents wedding in 1960. It has yellowing, some creases, and the edges are damaged. Make it look fresh while preserving the nostalgic quality.",
    "mode": "max",
    "image_urls": ["https://example.com/grandparents-wedding.jpg"]
  }'
```

### 9. 破损照片重建

数字化修复物理上破损的照片。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Repair this torn photo - there is a visible tear line running through the middle of the image. Reconstruct the damaged areas seamlessly and restore the photo to its original state.",
    "mode": "max",
    "image_urls": ["https://example.com/torn-photo.jpg"]
  }'
```

### 10. 去除胶片颗粒感

清除老照片中的颗粒和噪点。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the heavy film grain from this old photograph. The grain is very visible and distracting. Clean it up while preserving the sharpness and detail of the image. Keep some subtle texture so it does not look overly processed.",
    "mode": "max",
    "image_urls": ["https://example.com/grainy-film-photo.jpg"]
  }'
```

## 多轮修复流程

使用 `session_id` 进行迭代修复和优化：

```bash
# Initial restoration
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore this old damaged black and white photo - fix the scratches and damage first",
    "session_id": "family-photo-restoration",
    "image_urls": ["https://example.com/old-bw-damaged.jpg"]
  }'

# Follow up with colorization
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now colorize the restored photo with natural colors appropriate for the 1930s era",
    "session_id": "family-photo-restoration"
  }'

# Further refinement
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Enhance the faces to make them clearer and more detailed",
    "session_id": "family-photo-restoration"
  }'
```

## 批量修复

使用一致设置处理多张照片：

```bash
# Photo 1
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore and colorize this old family photo",
    "mode": "eco",
    "image_urls": ["https://example.com/family-photo-1.jpg"]
  }'

# Photo 2
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore and colorize this old family photo",
    "mode": "eco",
    "image_urls": ["https://example.com/family-photo-2.jpg"]
  }'

# Photo 3
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore and colorize this old family photo",
    "mode": "eco",
    "image_urls": ["https://example.com/family-photo-3.jpg"]
  }'
```

## 模式选择

在处理前询问用户：

**“您希望快速且经济实惠的修复效果，还是最高质量的修复效果？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终修复、珍贵家庭照片、专业档案级修复 | 较慢 | 最高质量 |
| `eco` | 快速预览、批量处理、初步评估 | 较快 | 良好质量 |

## 最佳实践

### 为了获得最佳效果

- **提供背景信息**：说明照片的年代、损伤类型以及需要保留的重点
- **先修复损伤**：在上色之前先修复划痕和撕裂
- **采用多轮修复流程**：对于复杂的项目，分阶段进行修复
- **明确要求人脸修复**：如果人脸重要，请明确说明需要修复人脸
- **保留原貌**：如需保留复古风格，请提出相应要求

### 提示建议

1. **描述损伤情况**：划痕、撕裂、褪色、水渍、泛黄等问题
2. **说明照片年代**：这有助于选择合适的修复方式
3. **说明优先级**：明确哪些方面最重要（人脸、整体清晰度、色彩准确性）
4. **设定预期**：选择自然效果还是极致优化

### 示例提示结构

```
"Restore this [era] photo. The damage includes [list damage types].
Focus on [priority areas]. [Additional preferences like colorization,
authenticity preservation, etc.]"
```

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 数据不足 | 在 eachlabs.ai 网站充值数据 |
| 内容违规 | 照片不符合政策要求 | 确保照片符合内容政策 |
| 超时 | 修复过程复杂 | 将客户端超时时间设置为至少 10 分钟 |
| 修复效果不佳 | 输入分辨率过低 | 使用最高分辨率的扫描或照片文件 |

## 相关技能

- `each-sense` - 核心 API 文档
- `image-enhancement` - 通用图像质量提升工具
- `face-restoration` - 专门用于人脸优化的工具
- `image-upscaling` - 图像分辨率提升工具