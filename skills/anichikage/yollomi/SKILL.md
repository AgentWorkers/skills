---
name: yollomi-ai-api
description: AI图像生成技能（用于生成图像）。Yollomi提供了多模型图像生成功能，可通过统一的API端点来生成AI图像。使用此功能需要YOLLOMI_API_KEY。
metadata: {"openclaw":{"requires":{"env":["YOLLOMI_API_KEY"]}}}
---

# Yollomi AI API 技能

通过 Yollomi API 生成图片和视频。所有模型都使用一个 **统一的接口**，只是通过不同的 `modelId` 参数来区分不同的模型。

## 设置

1. **API 密钥**：设置 `YOLLOMI_API_KEY`（环境变量）。

**注意**：
- 在当前技能实现中，视频生成功能暂时被禁用。

## 统一接口

```
POST /api/v1/generate
```

**请求头**：
- `Authorization: Bearer ${YOLLOMI_API_KEY}` 或 `X-API-Key: ${YOLLOMI_API_KEY}`
- `Content-Type`: `application/json`

**请求体**：
- `type`（必填）：`"image"` 或 `"video"`
- `modelId`（必填）：模型标识符
- 其他参数取决于具体模型（如 `prompt`、` imageUrl` 等）

**响应（图片）**：`{ images: string[], remainingCredits: number }`
**响应（视频）**：`{ video: string, remainingCredits: number }`

## 查看所有模型

```
GET /api/v1/models
```

返回所有可用的图片和视频模型 ID。

## 常见示例

- **生成图片**：
```bash
curl -X POST "${YOLLOMI_BASE_URL:-https://yollomi.com}/api/v1/generate" \
  -H "Authorization: Bearer $YOLLOMI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"image","modelId":"flux","prompt":"A cat in a hat","aspectRatio":"1:1"}'
```

- **去除背景**：
```bash
curl -X POST "${YOLLOMI_BASE_URL:-https://yollomi.com}/api/v1/generate" \
  -H "Authorization: Bearer $YOLLOMI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"image","modelId":"remove-bg","imageUrl":"https://example.com/photo.jpg"}'
```

- **生成视频**：
```bash
curl -X POST "${YOLLOMI_BASE_URL:-https://yollomi.com}/api/v1/generate" \
  -H "Authorization: Bearer $YOLLOMI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"video","modelId":"kling-2-1","prompt":"A cat walking in the rain"}'
```

## 宽高比（aspectRatio）

文本到图片模型支持的宽高比：

| 宽高比 | 描述 |
|------|-------------|
| 1:1 | 正方形（默认） |
| 16:9 | 横屏 |
| 9:16 | 纵屏 |

## 图片模型 ID

| modelId | 需要的 Credits | 是否必填 | 宽高比 |
|---------|---------|----------|-------------|
| flux | 4 | prompt | 1:1, 16:9, 9:16 |
| flux-schnell | 2 | prompt | 同上 |
| flux-2-pro | 15 | prompt | 同上 |
| remove-bg | 0 | imageUrl | - |
| nano-banana | 4 | prompt | 1:1, 16:9, 9:16 |
| nano-banana-pro | 15 | prompt | 同上 |
| flux-kontext-pro | 4 | prompt | 同上 |
| z-image-turbo | 1 | prompt | 宽度, 高度 |
| imagen-4-ultra | 6 | prompt | 同上 |
| image-4-fast | 3 | prompt | 同上 |
| ideogram-v3-turbo | 3 | prompt | 同上 |
| stable-diffusion-3-5-large | 7 | prompt | 同上 |
| seedream-4-5 | 4 | prompt | 同上 |
| object-remover | 3 | image, mask | - |
| face-swap | 3 | swapImage, inputImage | - |
| image-upscaler | 1 | imageUrl, scale | - |
| photo-restoration | 4 | imageUrl | - |
| qwen-image-edit | 3 | image, prompt | - |
| qwen-image-edit-plus | 3 | image, prompt | - |
| virtual-try-on | 3 | clothImage, personImage | - |
| ai-background-generator | 5 | imageUrl | prompt |

## 视频模型 ID

| modelId | 需要的 Credits |
|---------|---------|
| openai-sora-2 | ~50+ |
| google-veo-3 | 10 |
| google-veo-3-fast | 9 |
| google-veo-3-1 | 10 |
| google-veo-3-2 | 10 |
| google-veo-3-1-fast | 9 |
| kling-2-1 | 9 |
| kling-v2-6-motion-control | 7/sec |
| minimax-hailuo-2-3 | 9 |
| minimax-hailuo-2-3-fast | 9 |
| bytedance-seedance-1-pro-fast | 8 |
| runway-gen4-turbo | 变化不定 |
| pixverse-5 | 9 |
| wan-2-5-i2v | 9 |
| wan-2-5-t2v | 9 |
| wan-2-6-i2v | 29 |
| wan-2-6-t2v | 29 |

## 工作流程

1. **生成图片**：发送 POST 请求到 `/api/v1/generate`，参数为 `type: "image"`、`modelId` 和其他模型相关参数。
2. **生成视频**：发送 POST 请求到 `/api/v1/generate`，参数为 `type: "video"`、`modelId` 和可选的 `prompt` 或 `inputs`。
3. **查看所有模型**：发送 GET 请求到 `/api/v1/models`。
4. **401/402**：检查 API 密钥和剩余的 Credits 数量。

## 参考资料

完整的模型列表和参数说明：[models-reference.md](models-reference.md) 或通过 GET 请求 `/api/v1/models` 获取。