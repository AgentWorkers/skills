---
name: object-removal
description: 使用 each::sense AI 去除照片中不需要的物体、人物、文字以及瑕疵。该工具通过智能修复技术（inpainting）来填补被删除的区域，从而实现图像的完美修复。
metadata:
  author: eachlabs
  version: "1.0"
---
# 对象移除与修复

使用 `each::sense` 功能从照片中移除不需要的元素。该技能能够智能地移除对象、人物、文字、水印以及图像瑕疵，并通过上下文相关的内容无缝填充被移除的区域。

## 特点

- **对象移除**：从任何照片中移除不需要的元素
- **人物移除**：干净地从背景中移除人物
- **文字/水印移除**：清除图像中的多余文字和水印
- **瑕疵修复**：去除皮肤瑕疵和图像瑕疵
- **电线/线路移除**：清除电线、电缆等杂乱元素
- **标志移除**：从图像中移除品牌标识和标志
- **阴影移除**：消除不必要的阴影
- **背景清理**：移除干扰背景的元素

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the person standing on the left side of this photo",
    "image_urls": ["https://example.com/beach-photo.jpg"],
    "mode": "max"
  }'
```

## 使用案例示例

### 1. 从照片中移除人物

从合影或风景照片中移除不需要的个人。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the person in the red shirt from this beach photo. Fill the area naturally with the ocean and sand background.",
    "image_urls": ["https://example.com/beach-group.jpg"],
    "mode": "max"
  }'
```

### 2. 移除不需要的对象

通过移除干扰元素来清理照片。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the trash can and bench from the right side of this park landscape photo. Make it look like a clean natural scene.",
    "image_urls": ["https://example.com/park-landscape.jpg"],
    "mode": "max"
  }'
```

### 3. 移除文字/水印

清除图像中的多余文字和水印。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the watermark from the bottom right corner of this image. Restore the original background seamlessly.",
    "image_urls": ["https://example.com/watermarked-image.jpg"],
    "mode": "max"
  }'
```

### 4. 修复瑕疵/缺陷

修复皮肤瑕疵或图像瑕疵。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the skin blemishes and acne marks from this portrait photo. Keep the skin looking natural and maintain the original skin texture.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 5. 移除电线/线路

清除风景和建筑照片中的电线等杂乱元素。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove all the power lines and electrical wires from this sunset cityscape photo. Make the sky look clean and unobstructed.",
    "image_urls": ["https://example.com/cityscape-wires.jpg"],
    "mode": "max"
  }'
```

### 6. 从地标照片中移除游客

通过移除人群，获得完美的空白地标照片。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove all the tourists and people from this Eiffel Tower photo. I want it to look like an empty plaza with just the monument.",
    "image_urls": ["https://example.com/eiffel-tower-crowded.jpg"],
    "mode": "max"
  }'
```

### 7. 从照片中移除特定人物

从个人照片中移除特定人物，保留回忆。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the person on the right side of this vacation photo. Fill in with the background scenery naturally so it looks like a solo travel photo.",
    "image_urls": ["https://example.com/vacation-couple.jpg"],
    "mode": "max"
  }'
```

### 8. 移除标志/品牌

清除产品照片中的品牌标识。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the brand logo from the t-shirt in this photo. Replace it with plain fabric that matches the shirt color and texture.",
    "image_urls": ["https://example.com/branded-shirt.jpg"],
    "mode": "max"
  }'
```

### 9. 清理产品照片

清除电商产品照片中的干扰元素。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Clean up this product photo by removing the price tag, dust spots, and the reflection of the photographer in the surface. Make it look professional and ready for e-commerce.",
    "image_urls": ["https://example.com/product-raw.jpg"],
    "mode": "max"
  }'
```

### 10. 移除阴影

消除照片中的不需要的阴影。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the harsh shadow cast by the photographer on the ground in this outdoor portrait. Make the lighting look natural and even.",
    "image_urls": ["https://example.com/portrait-shadow.jpg"],
    "mode": "max"
  }'
```

## 多轮对象移除

使用 `session_id` 进行迭代移除和优化：

```bash
# First removal
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the car parked on the left side of this street photo",
    "image_urls": ["https://example.com/street-scene.jpg"],
    "session_id": "cleanup-project-001"
  }'

# Second removal (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now also remove the garbage bins near the building entrance",
    "session_id": "cleanup-project-001"
  }'

# Refinement (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The area where the car was removed looks a bit blurry. Can you improve the texture to match the surrounding pavement better?",
    "session_id": "cleanup-project-001"
  }'
```

## 对象移除的提示技巧

在请求对象移除时，请提供以下详细信息：

1. **需要移除的内容**：明确指出需要移除的对象
2. **位置**：描述对象在图像中的位置（左侧、右侧、中心或背景）
3. **填充建议**：说明应如何填充被移除的区域
4. **保留元素**：说明是否需要保留某些元素

### 提示示例结构

```
"Remove [object description] from [location in image].
Fill the area with [expected background/content].
Keep [elements to preserve] intact."
```

### 推荐的提示示例

- “移除左侧喷泉附近穿蓝色夹克的人”
- “从图像中移除所有文字和水印，恢复原始背景”
- “移除汽车，并用匹配的草地和小路替换该区域”

### 应避免的提示

- “清理这张照片”（过于模糊）
- “移除一些东西”（不够具体）
- “让照片更美观”（目标不明确）

## 模式选择

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终成果、复杂移除、专业处理 | 较慢 | 最高质量 |
| `eco` | 快速预览、简单移除、批量处理 | 较快 | 良好质量 |

**建议**：对于复杂的移除操作（如人物、大型对象），使用 `max` 模式；对于简单的修复（如小瑕疵、灰尘），使用 `eco` 模式。

## 最佳实践

### 为了获得最佳效果

- **高分辨率源图像**：使用最高质量的源图像
- **清晰描述**：明确指出需要移除的内容及其位置
- **简单背景**：在简单、重复的背景前移除对象更容易操作
- **多轮处理**：对于复杂场景，分多次处理以逐步移除对象

### 具有挑战性的场景

- **复杂背景**：在细节丰富、独特的背景前移除对象可能需要手动优化
- **大型对象**：移除占据图像较大比例（超过30%）的对象可能导致效果不自然
- **反射**：具有反射的对象可能需要分别处理对象及其反射
- **阴影**：如果对象投下可见的阴影，请记得请求阴影移除

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 数据不平衡 | 在 eachlabs.ai 补充数据 |
| 内容违规 | 禁止的内容 | 查看内容指南 |
| 超时 | 生成过程复杂 | 将客户端超时设置为至少10分钟 |
| 移除效果不佳 | 提示不明确 | 更详细地描述位置和填充内容 |

## 客户端超时配置

对象移除操作可能需要时间，尤其是对于复杂场景。请将您的 HTTP 客户端超时设置为至少 **10分钟**，以避免提前断开连接。

```bash
# Example with extended timeout
curl --max-time 600 -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove all people from this crowded plaza photo",
    "image_urls": ["https://example.com/crowded-plaza.jpg"],
    "mode": "max"
  }'
```

## 相关技能

- `each-sense` - 核心 API 文档
- `image-edit` - 通用图像编辑功能
- `background-removal` - 移除和替换背景