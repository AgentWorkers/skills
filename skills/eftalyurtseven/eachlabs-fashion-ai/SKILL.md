---
name: eachlabs-fashion-ai
description: 使用 EachLabs AI 生成时尚模特的图像、虚拟试穿效果、T台展示视频以及广告宣传素材。当用户需要时尚相关内容、模特照片或虚拟试穿功能时，可随时使用该工具。
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs Fashion AI

使用 EachLabs 的模型生成 AI 时尚模型图像、虚拟试穿体验、T 台内容和活动视觉素材。

## 认证

```
Header: X-API-Key: <your-api-key>
```

请设置 `EACHLABS_API_KEY` 环境变量。您可以在 [eachlabs.ai](https://eachlabs.ai) 获取该密钥。

## 推荐模型

### 图像生成与编辑

| 任务 | 模型 | Slug |
|------|-------|------|
| 时尚模型生成 | GPT Image v1.5 | `gpt-image-v1-5-text-to-image` |
| 虚拟试穿（最佳选择） | Kolors Virtual Try-On | `kling-v1-5-kolors-virtual-try-on` |
| 虚拟试穿（备用选项） | IDM VTON | `idm-vton` |
| 模特佩戴服装 | Wan v2.6 Image-to-Image | `wan-v2-6-image-to-image` |
| 模特拍摄 | Product Photo to Modelshoot | `product-photo-to-modelshoot` |
| 拍摄造型 | Nano Banana Pro Photoshoot | `nano-banana-pro-photoshoot` |
| 面部/造型一致性 | Omni Zero | `omni-zero` |
| 角色一致性 | Ideogram Character | `ideogram-character` |
| Photomaker | Photomaker | `photomaker` |
| Photomaker 风格 | Photomaker Style | `photomaker-style` |
| 虚拟形象生成 | Instant ID | `instant-id` |
| 造型风格调整 | Higgsfield AI Soul | `higgsfield-ai-soul` |
| 生成完整形象 | Become Image | `become-image` |

### 训练

| 任务 | 模型 | Slug |
|------|-------|------|
| 品牌风格训练 | Z Image Trainer | `z-image-trainer` |
| 肖像 LoRA | Flux LoRA Portrait Trainer | `flux-lora-portrait-trainer` |

### 视频

| 任务 | 模型 | Slug |
|------|-------|------|
| T 台视频 | Pixverse v5.6 Image-to-Video | `pixverse-v5-6-image-to-video` |
| T 台动画 | Bytedance Omnihuman v1.5 | `bytedance-omnihuman-v1-5` |
| 动作参考 | Kling v2.6 Pro Motion | `kling-v2-6-pro-motion-control` |

## 预测流程

1. **检查模型**：`GET https://api.eachlabs.ai/v1/model?slug=<slug>` — 验证模型是否存在，并返回包含精确输入参数的 `request_schema`。在创建预测之前务必执行此操作，以确保输入正确。
2. **发送请求**：`POST https://api.eachlabs.ai/v1/prediction`，提供模型 Slug、版本 `"0.0.1"` 以及符合 schema 的输入数据。
3. **查询结果**：`GET https://api.eachlabs.ai/v1/prediction/{id}`，直到状态变为 `"success"` 或 `"failed"`。
4. **提取输出**：从响应中获取输出 URL。

## 工作流程

### AI 时尚模型生成

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "gpt-image-v1-5-text-to-image",
    "version": "0.0.1",
    "input": {
      "prompt": "Professional fashion model wearing a tailored navy blazer, editorial photography, studio lighting, full body shot, neutral background",
      "image_size": "1024x1536",
      "quality": "high"
    }
  }'
```

### 虚拟试穿

将服装图像与模特图像结合：

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "wan-v2-6-image-to-image",
    "version": "0.0.1",
    "input": {
      "prompt": "The person in image 1 wearing the clothing from image 2, professional fashion photography, editorial style",
      "image_urls": ["https://example.com/model.jpg", "https://example.com/garment.jpg"],
      "image_size": "portrait_4_3"
    }
  }'
```

### T 台/走秀视频

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "pixverse-v5-6-image-to-video",
    "version": "0.0.1",
    "input": {
      "image_url": "https://example.com/fashion-model.jpg",
      "prompt": "Fashion model walking confidently on a runway, camera follows from front, professional fashion show lighting",
      "duration": "5",
      "resolution": "1080p"
    }
  }'
```

### 带有动作参考的 T 台表演

使用真实的 T 台走秀动作作为参考：

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "kling-v2-6-pro-motion-control",
    "version": "0.0.1",
    "input": {
      "image_url": "https://example.com/fashion-model.jpg",
      "video_url": "https://example.com/runway-walk-reference.mp4",
      "character_orientation": "video"
    }
  }'
```

### 品牌风格训练

使用 LoRA 对您的品牌视觉风格进行训练，以生成一致的活动图像：

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "z-image-trainer",
    "version": "0.0.1",
    "input": {
      "image_data_url": "https://example.com/brand-photos.zip",
      "default_caption": "brand editorial fashion photography style",
      "training_type": "style",
      "steps": 1500
    }
  }'
```

## 时尚相关的提示

- 指定拍摄姿势：全身照、半身照、服装细节特写
- 说明照明方式：编辑室灯光、自然光、戏剧性侧光
- 指定风格：时尚杂志风格、街头风格、高级定制时装、休闲lookbook
- 为了多样性，请在提示中指定体型、肤色和年龄
- 为保持一致性，请在整个活动系列中使用相同的风格关键词

## 参数参考

有关完整的模型参数，请参阅 [eachlabs-image-generation](../eachlabs-image-generation/references/MODELS.md) 和 [eachlabs-video-generation](../eachlabs-video-generation/references/MODELS.md)。