---
name: eachlabs-product-visuals
description: 使用 EachLabs 的 AI 模型生成专业的电子商务产品图片和视频。这些服务包括产品拍摄、背景替换、生活场景模拟以及 360 度全景视图。适用于用户需要产品图片用于电子商务或市场营销的场景。
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs 产品视觉效果

使用 EachLabs 的 AI 模型生成专业的产品照片、电商视觉素材和产品视频。

## 认证

```
Header: X-API-Key: <your-api-key>
```

请设置 `EACHLABS_API_KEY` 环境变量。您可以在 [eachlabs.ai](https://eachlabs.ai) 获取该密钥。

## 推荐模型

### 电商专用模型

| 任务 | 模型 | Slug |
|------|-------|------|
| 产品拍摄 | Product to Photoshoot | `product-to-photoshoot` |
| 产品与模型的搭配 | Product Photo to Modelshoot | `product-photo-to-modelshoot` |
| 颜色变体 | Product Colors | `product-colors` |
| 食物摄影 | Food Photos | `food-photos` |
| 背景去除 | Product Background Remover | `product-background-remover` |
| 图像放大 | Product Photo Upscaler | `product-photo-upscaler` |
| 产品展示场景 | Product Home View | `product-home-view` |
| 产品特写 | Bria Product Shot | `bria-product-shot` |
| 产品全景拍摄 | Eachlabs Product Arc Shot | `eachlabs-product-arc-shot-v1` |
| 产品放大效果 | Eachlabs Product Zoom In | `eachlabs-product-zoom-in-v1` |

### 通用模型

| 任务 | 模型 | Slug |
|------|-------|------|
| 产品摄影 | GPT Image v1.5 | `gpt-image-v1-5-text-to-image` |
| 背景替换 | GPT Image v1.5 Edit | `gpt-image-v1-5-edit` |
| 产品编辑 | Flux 2 Turbo Edit | `flux-2-turbo-edit` |
| 多角度视图 | Qwen Image Edit | `qwen-image-edit-2511-multiple-angles` |
| 背景去除 | Rembg Enhance | `rembg-enhance` |
| 背景去除 | Eachlabs BG Remover | `eachlabs-bg-remover-v1` |
| 图像放大 | Eachlabs Upscaler Pro | `eachlabs-image-upscaler-pro-v1` |
| 广告修复 | SDXL Ad Inpaint | `sdxl-ad-inpaint` |
| 自定义产品风格 | Z Image Trainer | `z-image-trainer` |
| 产品视频 | Pixverse v5.6 Image-to-Video | `pixverse-v5-6-image-to-video` |

## 预测流程

1. **检查模型**：`GET https://api.eachlabs.ai/v1/model?slug=<slug>` — 验证模型是否存在，并返回包含确切输入参数的 `request_schema`。在创建预测之前务必执行此操作，以确保输入正确。
2. **发送请求**：`POST https://api.eachlabs.ai/v1/prediction`，提供模型 Slug、版本 `"0.0.1"` 以及符合 schema 的输入数据。
3. **等待结果**：`GET https://api.eachlabs.ai/v1/prediction/{id}`，直到状态变为 `"success"` 或 `"failed"`。
4. **提取输出 URL**：从响应中获取输出 URL。

## 工作流程

### 产品背景为白色

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "gpt-image-v1-5-edit",
    "version": "0.0.1",
    "input": {
      "prompt": "Place this product on a clean white background with soft studio lighting and subtle shadows",
      "image_urls": ["https://example.com/product.jpg"],
      "background": "opaque",
      "quality": "high"
    }
  }'
```

### 生活场景生成

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "gpt-image-v1-5-edit",
    "version": "0.0.1",
    "input": {
      "prompt": "Place this coffee mug on a cozy wooden desk in a modern home office with warm morning light, lifestyle photography",
      "image_urls": ["https://example.com/mug.jpg"],
      "quality": "high"
    }
  }'
```

### 多角度产品视图

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "qwen-image-edit-2511-multiple-angles",
    "version": "0.0.1",
    "input": {
      "image_urls": ["https://example.com/product.jpg"],
      "horizontal_angle": 45,
      "vertical_angle": 15,
      "zoom": 5
    }
  }'
```

通过使用不同的 `horizontal_angle` 值（0, 45, 90, 135, 180, 225, 270, 315，共 360 度）分别进行预测，以生成多个角度的产品视图。

### 产品背景透明

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "gpt-image-v1-5-edit",
    "version": "0.0.1",
    "input": {
      "prompt": "Remove the background from this product image",
      "image_urls": ["https://example.com/product.jpg"],
      "background": "transparent",
      "output_format": "png"
    }
  }'
```

### 从图片生成产品视频

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "pixverse-v5-6-image-to-video",
    "version": "0.0.1",
    "input": {
      "image_url": "https://example.com/product-studio.jpg",
      "prompt": "Slow cinematic camera rotation around the product with dramatic studio lighting",
      "duration": "5",
      "resolution": "1080p"
    }
  }'
```

## 产品描述提示：

- 指定光线效果：例如 “柔和的摄影棚灯光”、“戏剧性的侧光”、“自然的光线”
- 提及表面材质：例如 “大理石表面”、“木质桌面”、“干净的白色背景”
- 添加阴影效果：例如 “柔和的阴影”、“表面的反射”
- 提供场景背景：例如 “生活场景”、“使用中的产品”、“平铺摆放”
- 对于批量目录拍摄，请使用相似的描述提示以保持一致性

## 批量处理

对于批量处理，可以为每个产品分别发送 POST 请求以并行生成多个预测结果。请独立检查每个预测的结果。

## 参数参考

有关完整的模型参数，请参阅 [eachlabs-image-generation](../eachlabs-image-generation/references/MODELS.md) 和 [eachlabs-video-generation](../eachlabs-video-generation/references/MODELS.md)。