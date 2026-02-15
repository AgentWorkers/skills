---
name: eachlabs-face-swap
description: 使用 EachLabs AI 在图像之间交换人脸。当用户需要替换或交换照片中的人脸时，可以使用此功能。
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs 面部替换功能

使用 EachLabs 的预测 API 在图片和视频之间进行面部替换。

## 认证

```
Header: X-API-Key: <your-api-key>
```

请设置 `EACHLABS_API_KEY` 环境变量。您可以在 [eachlabs.ai](https://eachlabs.ai) 获取该密钥。

## 可用模型

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| AI Face Swap V1 | `aifaceswap-face-swap` | 图片面部替换 |
| Eachlabs Face Swap | `each-faceswap-v1` | 图片面部替换 |
| Face Swap (legacy) | `face-swap-new` | 图片面部替换 |
| Faceswap Video | `faceswap-video` | 视频面部替换 |

## 示例

### 使用 AI Face Swap V1 进行图片面部替换

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "aifaceswap-face-swap",
    "version": "0.0.1",
    "input": {
      "target_image": "https://example.com/target-photo.jpg",
      "swap_image": "https://example.com/source-face.jpg"
    }
  }'
```

### 使用 Eachlabs 进行图片面部替换

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "each-faceswap-v1",
    "version": "0.0.1",
    "input": {
      "target_image": "https://example.com/target-photo.jpg",
      "swap_image": "https://example.com/source-face.jpg"
    }
  }'
```

### 视频面部替换

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "faceswap-video",
    "version": "0.0.1",
    "input": {
      "target_video": "https://example.com/target-video.mp4",
      "swap_image": "https://example.com/source-face.jpg"
    }
  }'
```

### 替代方案：使用 GPT Image v1.5 进行编辑

对于基于提示的面部替换操作，可以使用以下方法：

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "gpt-image-v1-5-edit",
    "version": "0.0.1",
    "input": {
      "prompt": "Replace the face in image 1 with the face from image 2. Keep the same pose, lighting, and expression. Maintain natural skin tone and seamless blending.",
      "image_urls": [
        "https://example.com/target-photo.jpg",
        "https://example.com/source-face.jpg"
      ],
      "quality": "high"
    }
  }'
```

## 预测流程

1. **检查模型**：`GET https://api.eachlabs.ai/v1/model?slug=<slug>` — 验证模型是否存在，并返回包含正确输入参数的 `request_schema`。在创建预测请求之前，请务必执行此操作以确保输入正确。
2. **发送请求**：`POST https://api.eachlabs.ai/v1/prediction`，并提供模型 slug、版本 `"0.0.1"` 以及符合 schema 的输入数据。
3. **查询结果**：`GET https://api.eachlabs.ai/v1/prediction/{id}`，直到状态变为 `"success"` 或 `"failed"`。
4. **提取输出结果**：从响应中获取输出图片的 URL。

## 优化建议

- 使用高质量、面部清晰且光线充足的源图片。
- 源图片应为正面或接近正面的肖像照片。
- 确保源图片和目标图片的光线条件一致，以获得更自然的效果。
- 在提示中指定“无缝融合”和“自然肤色”等参数。
- 对于目标图片，确保面部清晰可见且未被严重遮挡。