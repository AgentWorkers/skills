---
name: photo-colorization
description: 使用 each::sense AI 为黑白照片上色。通过智能且具备上下文感知能力的颜色化技术，让老式的家庭肖像、历史图片、复古照片以及档案资料焕发出新的生机。
metadata:
  author: eachlabs
  version: "1.0"
---
# 照片着色

使用 `each::sense` 将黑白照片转换为生动、逼真的彩色图像。该技能利用人工智能智能分析图像内容，并应用符合历史背景的、恰当的色彩。

## 特点

- **自动着色**：人工智能检测图像中的主体并自动应用自然色彩
- **历史准确性**：根据时代背景进行着色，确保色彩的真实性
- **肖像优化**：为人物和肖像提供逼真的肤色
- **风景修复**：为户外和自然场景赋予自然色彩
- **复古照片修复**：让老照片焕发生机
- **批量处理**：依次为多张照片着色
- **风格保留**：保持原始照片的质量和细节

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this black and white photo with natural, realistic colors",
    "image_urls": ["https://example.com/bw-photo.jpg"],
    "mode": "max"
  }'
```

## 常见用途

| 用途 | 描述 | 适用场景 |
|------|-------------|---------|
| 家族档案 | 为老家庭肖像和照片着色 | 个人照片修复 |
| 历史文献 | 为档案资料提供符合时代背景的着色 | 博物馆、历史学家 |
| 肖像优化 | 为人物提供逼真的肤色和面部特征 | 专业修复工作 |
| 风景修复 | 为户外和自然场景赋予自然色彩 | 自然风光摄影 |
| 复古时尚 | 精确还原服装和织物的颜色 | 时尚档案 |
| 军事/战争照片 | 修复具有历史意义的军事照片 | 纪念项目 |
| 建筑物修复 | 为建筑物和室内场景着色 | 房地产、文化遗产保护 |

## 用途示例

### 1. 自动着色

使用人工智能检测的颜色进行基础着色。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this black and white photograph. Apply natural, realistic colors based on the image content. Maintain the original quality and details.",
    "image_urls": ["https://example.com/old-photo.jpg"],
    "mode": "max"
  }'
```

### 2. 历史照片着色

根据时代背景进行精确着色。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this historical photograph from the 1940s. Use period-accurate colors typical of that era - muted tones, authentic clothing colors, and historically appropriate details. This appears to be a street scene.",
    "image_urls": ["https://example.com/1940s-street.jpg"],
    "mode": "max"
  }'
```

### 3. 家庭肖像着色

用温暖、自然的色调让老照片焕发生机。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this old family portrait photo. Apply natural skin tones, realistic hair colors, and period-appropriate clothing colors. The photo appears to be from the 1950s-1960s era. Make it look warm and inviting.",
    "image_urls": ["https://example.com/family-portrait-bw.jpg"],
    "mode": "max"
  }'
```

### 4. 风景着色

为户外和自然场景赋予自然色彩。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this black and white landscape photograph. Apply natural colors - blue sky, green foliage, brown earth tones. Make it look like a vibrant summer day while preserving the original composition and atmosphere.",
    "image_urls": ["https://example.com/landscape-bw.jpg"],
    "mode": "max"
  }'
```

### 5. 具体肤色的肖像

控制肤色的着色效果，以获得准确的结果。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this portrait photograph. The subject has a medium olive skin tone and dark brown hair. Apply natural, warm skin colors with subtle pink undertones. Eyes appear to be brown. Clothing looks like a dark formal suit.",
    "image_urls": ["https://example.com/portrait-bw.jpg"],
    "mode": "max"
  }'
```

### 6. 复古照片着色

还原具有时代特色的老照片。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this vintage photograph from the 1920s. Apply colors that match the Art Deco era - rich jewel tones for clothing, sepia-influenced skin tones, and period-appropriate interior colors. Maintain the vintage aesthetic while adding realistic color.",
    "image_urls": ["https://example.com/1920s-vintage.jpg"],
    "mode": "max"
  }'
```

### 7. 军事/战争照片着色

精确修复具有历史意义的军事照片。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this World War II military photograph. Apply historically accurate colors - olive drab for US Army uniforms, appropriate skin tones for the soldiers, realistic equipment colors. Maintain the somber, documentary feel of the original while adding authentic military colors.",
    "image_urls": ["https://example.com/wwii-soldiers.jpg"],
    "mode": "max"
  }'
```

### 8. 建筑物着色

为建筑物和室内场景着色。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this black and white photograph of a Victorian-era building. Apply appropriate architectural colors - red or brown brick, white trim, dark roof tiles, green copper patina if visible. Include natural sky colors and surrounding landscape elements.",
    "image_urls": ["https://example.com/victorian-building.jpg"],
    "mode": "max"
  }'
```

### 9. 时尚/服装着色

精确还原服装和织物的颜色。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this 1960s fashion photograph. Apply era-appropriate colors - bold mod colors like orange, turquoise, and pink were popular. The model appears to be wearing a structured dress. Apply realistic fabric textures and vibrant 60s palette.",
    "image_urls": ["https://example.com/1960s-fashion.jpg"],
    "mode": "max"
  }'
```

### 10. 批量着色

使用会话连续性为多张照片统一着色风格。

```bash
# First photo in batch
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this black and white family photo from the 1950s. Apply warm, natural colors with period-appropriate tones. This is photo 1 of a series from the same family album.",
    "image_urls": ["https://example.com/family-album-001.jpg"],
    "session_id": "family-album-colorization",
    "mode": "max"
  }'

# Second photo (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this second photo from the same family album. Maintain consistent skin tones and color style as the previous colorization.",
    "image_urls": ["https://example.com/family-album-002.jpg"],
    "session_id": "family-album-colorization",
    "mode": "max"
  }'

# Third photo (continuing series)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize the third photo. Same family, same era. Keep the color palette consistent with previous images.",
    "image_urls": ["https://example.com/family-album-003.jpg"],
    "session_id": "family-album-colorization",
    "mode": "max"
  }'
```

## 最佳实践

### 图像质量
- **分辨率**：分辨率较高的照片可以获得更好的着色效果
- **对比度**：原始照片的对比度越高，人工智能识别细节的能力越强
- **清晰度**：清晰的照片着色效果更好
- **照片质量**：在着色前进行数字修复可以提升效果

### 提示
- **提供背景信息**：说明照片的时代、地点或主题
- **指定肤色**：如果知道肤色，请描述人物的肤色
- **标注服装颜色**：如果知道原始颜色，请提供相关信息
- **描述场景**：室外/室内、季节、时间

### 历史准确性
- 研究相应时期的色彩搭配
- 考虑地区在时尚和建筑风格上的差异
- 军事制服和装备有明确的颜色记录
- 复古汽车和车辆的颜色通常有详细的资料记录

## 模式选择

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终修复、档案工作、礼品用途 | 较慢 | 最高质量 |
| `eco` | 快速预览、批量测试、草图 | 较快 | 良好质量 |

**建议**：先使用 `eco` 模式进行初步测试，再使用 `max` 模式获得最终效果。

## 多轮优化

使用 `session_id` 进行多次迭代和优化着色过程：

```bash
# Initial colorization
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this old portrait photograph with natural colors",
    "image_urls": ["https://example.com/portrait.jpg"],
    "session_id": "portrait-restoration"
  }'

# Refine the result
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The skin tones look a bit too warm. Can you redo the colorization with cooler, more natural skin tones?",
    "session_id": "portrait-restoration"
  }'

# Further adjustment
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The dress should be blue, not green. Please adjust the clothing color.",
    "session_id": "portrait-restoration"
  }'
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 数据不足 | 在 eachlabs.ai 网站补充数据 |
| `Invalid image URL` | 图像链接无法访问 | 确保图像链接可公开访问 |
| Timeout | 图像过大或场景复杂 | 将客户端超时时间设置为至少 10 分钟 |
| 着色效果不佳 | 图像质量较低 | 使用更高分辨率、更清晰的图片 |

## 相关技能

- `each-sense` - 核心 API 文档
- `image-restoration` - 通用图像修复
- `image-enhancement` - 图像增强和放大
- `face-restoration` - 专门用于面部修复的技能