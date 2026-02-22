---
name: depth-map-generation
description: 使用 each::sense AI 从图像中生成深度图。该技术可用于 3D 效果、视差动画、VR/AR 应用程序、焦点效果以及立体图像的生成。
metadata:
  author: eachlabs
  version: "1.0"
---
# 深度图生成

使用 `each::sense` 从任何图像中生成精确的深度图。该功能可以从 2D 图像中提取深度信息，应用于 3D 效果、视差动画、VR/AR 应用、计算摄影等领域。

## 特点

- **单目深度估计**：从单张图像中提取深度信息
- **人像深度图**：为人像摄影效果提供精确的深度信息
- **风景深度图**：适用于全景和风景图像的场景深度分析
- **产品深度图**：适用于电商的 3D 可视化深度图
- **建筑深度图**：用于建筑和室内空间的深度分析
- **3D 视差效果**：生成适用于 Ken Burns 风格动画的深度数据
- **VR/AR 深度估计**：实现实时深度估计，提供沉浸式体验
- **立体图像生成**：利用深度信息将 2D 图像转换为立体 3D 图像
- **焦点堆叠**：基于深度信息选择焦点平面
- **基于深度的背景模糊**：实现具有深度感知的散景和模糊效果

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a depth map from this photo",
    "image_urls": ["https://example.com/photo.jpg"],
    "mode": "max"
  }'
```

## 深度图输出格式

| 格式 | 描述 | 使用场景 |
|--------|-------------|----------|
| 灰度图 | 8 位深度值（白色表示近处，黑色表示远处） | 通用用途，可视化展示 |
| 反向灰度图 | 8 位深度值（黑色表示近处，白色表示远处） | 与某些 3D 软件兼容 |
| 标准化深度图 | 0-1 范围的深度值 | 适用于机器学习流程 |
| 度量深度图 | 表示真实世界距离的深度值 | 适用于 VR/AR 和机器人技术 |

## 使用场景示例

### 1. 从照片生成深度图

从任何图像中提取基本深度信息。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a depth map from this image. Output as grayscale where white represents closer objects and black represents distant objects.",
    "image_urls": ["https://example.com/scene.jpg"],
    "mode": "max"
  }'
```

### 2. 人像深度图

从人像照片中提取精确的深度信息，用于实现散景效果和 3D 人像效果。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a high-precision depth map from this portrait photo. Focus on accurate edge detection around the subject, especially hair and facial features. I need this for applying realistic depth-of-field effects.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 3. 风景深度图

从风景和户外场景中生成具有较宽深度范围的深度图。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a depth map from this landscape photo. The scene has foreground elements, mid-ground terrain, and distant mountains. Capture the full depth range from near to far with good separation between depth layers.",
    "image_urls": ["https://example.com/landscape.jpg"],
    "mode": "max"
  }'
```

### 4. 产品深度图（用于 3D 效果）

为产品图片生成深度图，以实现 3D 视觉效果。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extract a depth map from this product photo. I need accurate depth information to create a 3D interactive view for an e-commerce website. Focus on capturing the product shape and surface details.",
    "image_urls": ["https://example.com/product-sneaker.jpg"],
    "mode": "max"
  }'
```

### 5. 建筑深度图

从建筑和室内照片中生成深度图，用于可视化展示。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a depth map from this interior architecture photo. Capture the spatial relationships between walls, furniture, and architectural elements. I need this for a virtual tour with depth-based transitions.",
    "image_urls": ["https://example.com/interior.jpg"],
    "mode": "max"
  }'
```

### 6. 3D 视差效果生成

生成适用于创建视差动画和 Ken Burns 风格效果的深度图。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a depth map from this photo that I will use for a 3D parallax animation. I need clear depth separation between foreground, midground, and background elements. The depth should be smooth with distinct layers for a compelling parallax effect.",
    "image_urls": ["https://example.com/scene-for-parallax.jpg"],
    "mode": "max"
  }'
```

### 7. VR/AR 深度估计

生成适用于虚拟现实和增强现实应用的深度图。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a depth map from this room photo for AR/VR use. I need metric depth estimation that accurately represents real-world distances. This will be used for placing virtual objects in an augmented reality application.",
    "image_urls": ["https://example.com/room.jpg"],
    "mode": "max"
  }'
```

### 8. 立体图像生成

利用深度估计将 2D 图像转换为立体 3D 图像。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a depth map from this photo and use it to create a stereoscopic 3D image pair (left and right eye views). The stereo effect should be subtle enough for comfortable viewing but noticeable enough to create depth perception.",
    "image_urls": ["https://example.com/photo-for-stereo.jpg"],
    "mode": "max"
  }'
```

### 9. 焦点堆叠深度图

生成用于计算焦点堆叠和全焦点合成效果的深度图。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a depth map from this macro/close-up photo. I need precise depth information to identify focus planes for computational focus stacking. Each depth layer should be clearly defined so I can select which areas should be in focus.",
    "image_urls": ["https://example.com/macro-photo.jpg"],
    "mode": "max"
  }'
```

### 10. 基于深度的背景模糊

生成深度图，以实现真实的散景和背景模糊效果。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a depth map from this photo for applying depth-aware background blur. The subject in the foreground should be clearly separated from the background. I need accurate edge detection so the blur transition looks natural, similar to a portrait mode effect.",
    "image_urls": ["https://example.com/photo-for-blur.jpg"],
    "mode": "max"
  }'
```

## 多轮深度处理

使用 `session_id` 对深度图进行优化，或处理多张相关图像：

```bash
# Initial depth estimation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a depth map from this photo",
    "image_urls": ["https://example.com/scene.jpg"],
    "session_id": "depth-project-001"
  }'

# Refine the depth map
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The depth map looks good but can you enhance the edge detection around the main subject? The boundaries are a bit fuzzy.",
    "session_id": "depth-project-001"
  }'

# Apply the depth map for an effect
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now use this depth map to create a 3D parallax video animation with subtle camera movement",
    "session_id": "depth-project-001"
  }'
```

## 批量深度处理

同时处理多张图像，以获得一致的深度估计结果：

```bash
# Process first image
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a depth map from this product photo. I will be sending more product images that need consistent depth estimation.",
    "image_urls": ["https://example.com/product1.jpg"],
    "session_id": "product-depth-batch",
    "mode": "eco"
  }'

# Process second image with same settings
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate depth map for this product using the same approach as before",
    "image_urls": ["https://example.com/product2.jpg"],
    "session_id": "product-depth-batch",
    "mode": "eco"
  }'
```

## 模式选择

| 模式 | 最适合的场景 | 处理速度 | 图像质量 |
|------|----------|-------|---------|
| `max` | 最终产品深度图、VR/AR 应用、专业合成 | 处理速度较慢 | 精度最高 |
| `eco` | 快速预览、批量处理、原型制作 | 处理速度较快 | 图像质量良好 |

**建议**：当深度精度至关重要时（如 VR/AR、3D 转换、专业合成），使用 `max` 模式；对于快速迭代和批量处理，使用 `eco` 模式。

## 最佳实践

### 输入图像质量
- **分辨率**：较高的分辨率输入可以生成更详细的深度图
- **光照**：均匀的光照有助于提高深度估计的准确性
- **对比度**：物体之间的对比度越高，深度分离效果越好
- **焦点**：清晰的照片有助于在深度图中获得更准确的边缘信息

### 深度图的应用场景
- **视差效果**：使用 3-5 个不同的深度层以获得最佳效果
- **散景/模糊效果**：确保主体边缘清晰，以实现自然的模糊效果
- **3D 转换**：提供关于场景规模的上下文信息，以获得准确的深度值
- **VR/AR**：请求度量深度值，以实现真实世界的距离感

### 使用提示
1. **指定输出格式**：选择灰度图、标准化深度图或度量深度图
2. **描述场景**：帮助模型理解场景的空间关系
3. **说明使用场景**：不同的应用需要不同的深度特性
4. **指定边缘质量**：指定是否需要清晰的深度过渡效果

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 数据不平衡 | 请在 eachlabs.ai 上补充数据 |
| Image loading failed | 图像 URL 无效或无法访问 | 确保图像 URL 可公开访问 |
| Timeout | 图像复杂或分辨率过高 | 将客户端超时时间设置为至少 10 分钟 |
| 低质量的深度输出 | 输入图像质量较差 | 使用更高分辨率、光照更好的图像 |

## 技术说明

- **客户端超时**：将 HTTP 客户端超时时间设置为至少 10 分钟，以处理复杂的深度估计任务
- **支持的图像格式**：支持 JPEG、PNG 和 WebP 格式的输入图像
- **输出格式**：深度图通常以灰度 PNG 格式输出
- **深度范围**：默认为相对深度（0-1）；可根据需求提供度量深度值

## 相关技能

- `each-sense`：核心 API 文档
- `image-to-3d`：从图像生成完整的 3D 模型
- `image-editing`：对图像应用基于深度的效果
- `video-generation`：利用深度图创建视差视频