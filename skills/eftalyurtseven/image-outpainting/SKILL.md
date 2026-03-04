---
name: image-outpainting
description: 使用 each::sense AI，您可以轻松地扩展和调整图像的尺寸，使其超出原始边界。该工具支持生成全景视图、调整图像的宽高比、添加背景效果，并能智能地裁剪照片。
metadata:
  author: eachlabs
  version: "1.0"
---
# 图像扩展功能

使用 `each::sense` 功能将图像扩展到其原始边界之外。该技术利用人工智能智能生成新内容，使其能够与原始图像无缝融合，从而实现纵横比转换、背景扩展以及创意图像处理。

## 主要功能

- **水平扩展**：向左右两侧扩展图像，以获得更宽的构图。
- **垂直扩展**：在图像的顶部和底部添加内容，使其看起来更高。
- **纵横比转换**：将竖屏图像转换为横屏图像，或反之亦然。
- **背景扩展**：为照片添加更多背景和场景元素。
- **裁剪恢复**：恢复或补充原始图像边框外的内容。
- **全景制作**：将单张图片转换为宽幅全景视图。
- **产品照片优化**：扩展产品图片以适应横幅和广告需求。
- **艺术作品扩展**：扩展插图和数字艺术作品的尺寸。

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extend this image horizontally to create a wider 16:9 composition, maintaining the same style and lighting",
    "image_urls": ["https://example.com/original-photo.jpg"],
    "mode": "max"
  }'
```

## 常见的应用场景

| 应用场景 | 目标纵横比 | 描述 |
|----------|--------------|-------------|
| 竖屏转横屏 | 16:9 | 将竖屏照片转换为适合视频或桌面的格式。 |
| 方形转宽屏 | 21:9 | 制作电影风格的构图。 |
| 产品横幅 | 3:1 或 4:1 | 扩展产品图片以适应网站横幅。 |
| 社交媒体 | 4:5 或 1:1 | 优化图片以适应 Instagram 的展示格式。 |
| 全景图 | 2:1 或 3:1 | 制作宽幅风景图片。 |
| 定制裁剪边距 | 自定义 | 为打印添加适当的边距。 |

## 应用场景示例

### 1. 水平扩展图像

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extend this image horizontally on both sides. Add more of the natural environment while keeping the subject centered. Maintain consistent lighting, color grading, and style throughout the extension.",
    "image_urls": ["https://example.com/landscape-photo.jpg"],
    "mode": "max"
  }'
```

### 2. 垂直扩展图像

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extend this image vertically - add more sky above and more ground/foreground below. Keep the horizon line natural and maintain the same atmosphere and time of day.",
    "image_urls": ["https://example.com/landscape.jpg"],
    "mode": "max"
  }'
```

### 3. 纵屏转横屏

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this vertical portrait photo to a horizontal 16:9 landscape format. Extend the background on both sides to create a wider scene. Keep the person as the main subject and ensure the extended areas match the original environment perfectly.",
    "image_urls": ["https://example.com/portrait-photo.jpg"],
    "mode": "max"
  }'
```

### 4. 方形转宽屏

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this square 1:1 image into a cinematic 21:9 widescreen format. Extend the scene horizontally while preserving the central composition. Match the lighting, textures, and visual style seamlessly.",
    "image_urls": ["https://example.com/square-image.jpg"],
    "mode": "max"
  }'
```

### 5. 扩展产品图片以适应横幅

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extend this product photo into a wide banner format (approximately 4:1 ratio). Keep the product on the left third of the image and extend the clean background to the right to create space for text overlay. Maintain the same studio lighting and surface texture.",
    "image_urls": ["https://example.com/product-shot.jpg"],
    "mode": "max"
  }'
```

### 6. 添加更多背景/场景元素

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Expand this image in all directions to add more environmental context. The subject is too tightly cropped - extend the scene to show more of the surroundings, making it feel less cramped. Keep the original subject size and add approximately 50% more space around it.",
    "image_urls": ["https://example.com/tight-crop.jpg"],
    "mode": "max"
  }'
```

### 7. 恢复裁剪后的图像

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "This photo has been tightly cropped - uncrop it to reveal more of the scene. Extend downward to show the full body (currently cut off at the waist) and extend the sides to show more of the room interior. Generate realistic content that matches the existing style.",
    "image_urls": ["https://example.com/cropped-photo.jpg"],
    "mode": "max"
  }'
```

### 8. 从单张图片创建全景图

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this landscape photo into a wide panoramic image with a 3:1 aspect ratio. Extend the scenic view on both left and right sides, continuing the mountain range, sky, and terrain naturally. Create a sweeping vista that feels like a real panoramic photograph.",
    "image_urls": ["https://example.com/mountain-view.jpg"],
    "mode": "max"
  }'
```

### 9. 扩展艺术作品/插图

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extend this digital illustration horizontally to double its width. Continue the artistic style, color palette, and visual elements seamlessly. This is a fantasy landscape illustration - extend the magical forest and atmospheric elements on both sides while maintaining the same painting technique and mood.",
    "image_urls": ["https://example.com/fantasy-illustration.jpg"],
    "mode": "max"
  }'
```

### 10. 为竖屏图片添加背景元素

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "This is a headshot with a blurred background. Extend the image to show more of the environment - convert to a 3/4 or full body shot by extending downward, and widen the scene to show the cafe/office setting implied by the background. Keep the portrait style and depth of field consistent.",
    "image_urls": ["https://example.com/headshot.jpg"],
    "mode": "max"
  }'
```

## 多次扩展操作

使用 `session_id` 可以多次执行图像扩展操作：

```bash
# Initial extension request
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extend this beach photo horizontally to create a wider 16:9 composition",
    "image_urls": ["https://example.com/beach.jpg"],
    "session_id": "outpaint-beach-001",
    "mode": "max"
  }'

# Request adjustments
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The right side extension looks good, but can you add some palm trees on the left side to balance the composition?",
    "session_id": "outpaint-beach-001"
  }'

# Further refinement
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now extend it vertically as well - add more dramatic sky with sunset clouds above",
    "session_id": "outpaint-beach-001"
  }'
```

## 使用提示时的注意事项

在请求图像扩展时，请提供以下详细信息：

1. **扩展方向**：指定是水平扩展、垂直扩展还是全方位扩展。
2. **目标纵横比**：指定所需的纵横比（如 16:9、21:9 等）。
3. **内容要求**：描述扩展区域应显示的内容。
4. **风格一致性**：要求生成内容在光线、颜色和氛围上保持一致。
5. **主体位置**：指定原始主体应放置的位置。
6. **应用场景**：说明图片用途（如横幅、社交媒体、打印等）。

### 示例提示结构

```
"Extend this [image type] [direction] to [target ratio/size].
[Describe what to add in extended areas].
Maintain [lighting/style/atmosphere] consistency.
Position the original [subject] in the [location]."
```

## 模式选择

在生成结果之前，请询问用户：

**“您需要快速且低成本的解决方案，还是高质量的结果？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终输出、专业用途、复杂场景 | 较慢 | 最高质量 |
| `eco` | 快速预览、构图测试、多次迭代 | 较快 | 良好质量 |

## 最佳实践

- **使用高分辨率的原始图像**：从高分辨率的原始图片开始处理。
- **清晰的边缘**：边缘清晰的图像扩展效果更好。
- **统一的光线效果**：在提示中详细描述光线情况，以获得更好的融合效果。
- **合理的扩展比例**：通常建议将图像大小扩展 2-3 倍。
- **多次迭代**：通过多次操作逐步优化结果。

## 需避免的常见错误

- 不要一次性进行过度扩展，应分步骤进行。
- 避免在图像边缘扩展包含复杂前景元素的区域。
- 对于风格化强烈或抽象的图像，不要期望完美的扩展效果。
- 明确指定扩展区域应显示的具体内容。

## 常见纵横比参考

| 名称 | 纵横比 | 常见用途 |
|------|-------|------------|
| 方形 | 1:1 | Instagram、缩略图 |
| 标准照片 | 4:3 | 传统摄影 |
| Instagram 竖屏照片 | 4:5 | Instagram 展示图 |
| 高清视频 | 16:9 | YouTube、演示文稿 |
| 电影风格 | 21:9 | 电影、超宽显示器 |
| 全景图 | 2:1、3:1 | 风景图片、横幅 |
| 横幅广告 | 4:1、5:1 | 网站标题、广告 |

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 数据平衡不足 | 请在 eachlabs.ai 网站补充数据。 |
| 内容违规 | 图片内容不符合规定 | 调整提示内容以符合规定。 |
| 超时 | 生成过程复杂 | 将客户端超时时间设置为至少 10 分钟。 |
| 边缘融合效果差 | 图像质量较低 | 使用更高分辨率的原始图片。 |

## 相关技能

- `each-sense`：核心 API 文档。
- `image-inpainting`：编辑图像中的特定区域。
- `image-upscaling`：提升图像分辨率。
- `background-removal`：去除并替换图像背景。