---
name: eachlabs-image-edit
description: 使用 EachLabs 的 AI 模型来编辑、转换、放大和优化图像。支持图像编辑、风格转换、背景去除、图像放大、图像修复、面部替换、虚拟试穿、3D 生成以及图像分析等功能。适用于用户需要对现有图像进行编辑或处理的场景。
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs 图像编辑

通过 EachLabs Predictions API，使用 130 多个 AI 模型来编辑、转换和增强现有图像。

## 认证

```
Header: X-API-Key: <your-api-key>
```

设置 `EACHLABS_API_KEY` 环境变量。您可以在 [eachlabs.ai](https://eachlabs.ai) 获取密钥。

## 模型选择指南

### 通用图像编辑

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Flux 2 Turbo Edit | `flux-2-turbo-edit` | 快速高质量编辑 |
| Flux 2 Flash Edit | `flux-2-flash-edit` | 最快编辑速度 |
| Flux 2 Max Edit | `flux-2-max-edit` | 最高质量编辑 |
| Flux 2 Pro Edit | `flux-2-pro-edit` | 专业级质量编辑 |
| Flux 2 Flex Edit | `flux-2-flex-edit` | 灵活编辑 |
| Flux 2 Edit | `flux-2-edit` | 标准 Flux 编辑 |
| Flux 2 LoRA Edit | `flux-2-lora-edit` | 基于 LoRA 的编辑 |
| XAI Grok Imagine Edit | `xai-grok-imagine-image-edit` | 创意编辑 |
| GPT Image v1.5 Edit | `gpt-image-v1-5-edit` | 高质量编辑（最多支持 10 张图片） |
| Bytedance Seedream v4.5 Edit | `bytedance-seedream-v4-5-edit` | Bytedance 最新模型 |
| Gemini 3 Pro Image Edit | `gemini-3-pro-image-preview-edit` | Google 提供的编辑服务 |
| Qwen Image Edit Plus | `qwen-image-edit-plus` | 高级 Qwen 编辑功能 |
| Reve Fast Edit | `reve-fast-edit` | 快速艺术编辑 |
| Reve Edit | `reve-edit` | 艺术风格编辑 |
| Chrono Edit | `chrono-edit` | 时间效果编辑 |
| Dream Omni 2 Edit | `dreamomni2-edit` | 梦幻风格编辑 |
| Kling O1 | `kling-o1` | 最新的 Kling 编辑工具 |
| Seedream V4 Edit | `seedream-v4-edit` | Seedream 提供的编辑服务 |
| SeedEdit 3.0 | `seededit-3-0` | SeedEdit 编辑工具 |
| Nano Banana Pro Edit | `nano-banana-pro-edit` | 轻量级编辑工具 |
| Nano Banana Edit | `nano-banana-edit` | 基础编辑工具 |

### 多图像编辑

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Flux Kontext Max | `flux-kontext-max` | 最佳的多图像编辑功能 |
| Flux Kontext Pro | `flux-kontext-pro` | 专业级多图像编辑 |
| Flux Kontext Dev | `flux-kontext-dev` | 开发者版多图像编辑 |
| Multi Image Kontext Max | `multi-image-kontext-max` | 高级多图像编辑 |
| Multi Image Kontext Pro | `multi-image-kontext-pro` | 专业级多图像编辑 |
| Multi Image Kontext | `multi-image-kontext` | 基础多图像编辑 |
| Flux Kontext Dev LoRA | `flux-kontext-dev-lora` | 基于 LoRA 的多图像编辑 |
| P Image Edit | `p-image-edit` | 多图像编辑工具 |
| Wan v2.6 I2I | `wan-v2-6-image-to-image` | 多图像参考编辑 |

### 多角度视图

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Qwen Multi-Angle | `qwen-image-edit-2511-multiple-angles` | 多角度视图编辑 |
| Qwen Image Edit | `qwen-ai-image-edit` | Qwen 提供的图像编辑服务 |

### 图像放大与增强

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Topaz Image Upscale | `topaz-upscale-image` | 最高质量放大 |
| Flux Vision Upscaler | `flux-vision-upscaler` | AI 放大技术 |
| Recraft Clarity Upscale | `recraft-clarity-upscale` | 图像清晰度增强 |
| CCSR Upscaler | `ccsr` | 细节修复技术 |
| Each Upscaler | `each-upscaler` | 通用图像放大 |
| Eachlabs Pro Upscaler | `eachlabs-image-upscaler-pro-v1` | 专业级图像放大 |
| Real ESRGAN | `real-esrgan` | 面部美化技术 |
| Real ESRGAN A100 | `real-esrgan-a100` | 快速面部美化 |
| GFPGAN | `gfpgan` | 面部修复技术 |
| Tencent Flux SRPO | `tencent-flux-srpo-image-to-image` | 超高分辨率技术 |

### 背景去除与修复

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Rembg | `rembg` | 背景去除 |
| Rembg Enhance | `rembg-enhance` | 改进版背景去除 |
| Eachlabs BG Remover | `eachlabs-bg-remover-v1` | 背景去除工具 |
| Flux Fill Pro | `flux-fill-pro` | 图像修复工具 |
| Stable Diffusion Inpainting | `stable-diffusion-inpainting` | 经典图像修复技术 |
| Realistic Background | `realistic-background` | 真实背景替换 |
| SDXL Ad Inpaint | `sdxl-ad-inpaint` | 广告背景修复 |
| Realistic Vision Inpainting | `realisitic-vision-v3-inpainting` | 真实感图像修复 |

### 风格转换与效果

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| ByteDance Style Changer | `bytedance` | 风格转换工具 |
| Nano Banana Pro Sketch | `nano-banana-pro-sketch` | 素描风格转换 |
| Nano Banana Pro Comic | `nano-banana-pro-comic-art` | 漫画风格转换 |
| Nano Banana Pro Realism | `nano-banana-pro-realism` | 照片真实感增强 |
| Cartoonify | `cartoonify` | 卡通风格转换 |
| Illusion Diffusion | `illusion-diffusion-hq` | 光学错觉效果 |
| Fog Effect | `salih-girgin-fog-effect-image-to-image` | 雾效效果 |

### 后处理效果

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Post Processing Combine | `post-processing` | 多效果组合 |
| Vignette | `post-processing-vignette` | 视野效果 |
| Sharpen | `post-processing-sharpen` | 图像锐化 |
| Grain | `post-processing-grain` | 电影颗粒效果 |
| Color Correction | `post-processing-color-correction` | 色彩校正 |
| Color Tint | `post-processing-color-tint` | 色彩调整 |
| Blur | `post-processing-blur` | 模糊效果 |
| Desaturate | `post-processing-desaturate` | 色调降低 |
| Solarize | `post-processing-solarize` | 日光效果 |
| Dodge Burn | `post-processing-dodge-burn` | 高光与阴影效果 |
| Chromatic Aberration | `post-processing-chromatic-aberration` | 色差校正 |
| Parabolize | `post-processing-parabolize` | 抛物线效果 |

### 人脸与肖像

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| AI Face Swap V1 | `aifaceswap-face-swap` | 人脸替换 |
| Eachlabs Face Swap | `each-faceswap-v1` | 人脸替换 |
| Face to Sticker | `face-to-sticker` | 图像转贴纸 |
| Instant ID | `instant-id` | 头像生成 |
| Instant ID Anime | `instant-id-ip-adapter` | 动漫风格头像 |
| Photomaker | `photomaker` | 照片合成 |
| Photomaker Style | `photomaker-style` | 风格合成 |
| Omni Zero | `omni-zero` | 零样本身份生成 |
| AI Face Aesthetics | `ai-face-aesthetics` | 人脸美学分析 |
| Baby Generator | `baby-generator` | 婴儿面部生成 |
| Hairstyle Changer | `change-haircut` | 发型变换 |
| Couple Image Gen v2 | `couple-image-generation-v2` | 情侣图像生成 |
| Become Image | `become-image` | 图像风格转换 |
| Higgsfield AI Soul | `higgsfield-ai-soul` | 灵魂风格设计 |

### 虚拟试穿与时尚

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Kolors Virtual Try-On | `kling-v1-5-kolors-virtual-try-on` | 最佳虚拟试穿体验 |
| IDM VTON | `idm-vton` | 虚拟试穿服务 |

### 图像裁剪

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Luma Photon Reframe | `luma-photon-reframe-image` | 图像裁剪工具 |
| Luma Photon Flash Reframe | `luma-photon-flash-reframe-image` | 快速裁剪工具 |
| Luma Reframe Image | `reframe-image` | Dream Machine 提供的裁剪服务 |

### 基于参考的图像生成

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Vidu Q2 Reference | `vidu-q2-reference-to-image` | 基于参考的图像生成 |
| Minimax Subject Reference | `minimax-subject-reference` | 主体参考生成 |
| Ideogram Character | `ideogram-character` | 字符一致性生成 |
| Flux Redux Dev | `flux-redux-dev` | 风格参考生成 |
| Flux Redux Schnell | `flux-redux-schnell` | 快速风格参考生成 |

### ControlNet 与深度处理

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Flux Dev ControlNet | `flux-dev-controlnet` | Flux ControlNet 技术 |
| Flux Canny Pro | `flux-canny-pro` | 基于边缘的深度处理 |
| Flux Depth Pro | `flux-depth-pro` | 专业深度处理 |
| Flux Depth Dev | `flux-depth-dev` | 开发者版深度处理 |
| SDXL ControlNet | `sdxl-controlnet` | SDXL ControlNet 技术 |
| Z Image Turbo ControlNet | `z-image-turbo-controlnet` | 快速 ControlNet 技术 |
| Z Image Turbo ControlNet LoRA | `z-image-turbo-controlnet-lora` | ControlNet + LoRA 结合技术 |
| Z Image Turbo I2I | `z-image-turbo-image-to-image` | Z Image 转换技术 |
| Z Image Turbo I2I LoRA | `z-image-turbo-image-to-image-lora` | Z Image + LoRA 结合技术 |

### 3D 生成

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Hunyuan 3D V2.1 | `hunyuan-3d-v2-1` | 最新的 3D 生成技术 |
| Hunyuan 3D V2 | `hunyuan-3d-v2` | 3D 模型生成技术 |

### 图像分析

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Gemini 2.0 Flash Lite | `gemini-2-0-flash-lite` | 图像理解技术 |
| NSFW Detection | `nsfw-image-detection` | 内容审核 |
| Face Analyzer | `1019-face-analyzer` | 人脸分析 |
| BLIP-2 | `blip-2` | 图像字幕生成 |

### 产品与电子商务

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Bria Product Shot | `bria-product-shot` | 产品照片拍摄 |
| Product Shoot | `product-shoot` | 产品拍摄服务 |
| Runway Gen4 Image | `runway-gen4-image` | 第四代图像编辑技术 |
| Eachlabs Image Generation | `eachlabs-image-generation` | 定制图像生成 |
| Custom Image Gen v2 | `custom-image-generation-v2` | 定制图像生成 |
| Action Figure Generator | `action-figure-generator` | 动作人物生成 |
| Reve Fast Remix | `reve-fast-remix` | 快速混音编辑 |
| Reve Remix | `reve-remix` | 混音编辑技术 |

## 预测流程

1. **检查模型**：`GET https://api.eachlabs.ai/v1/model?slug=<slug>` — 确认模型存在，并获取包含精确输入参数的 `request_schema`。在创建预测之前务必执行此步骤以确保输入正确。
2. **发送请求**：`POST https://api.eachlabs.ai/v1/prediction`，传入模型 Slug、版本 `"0.0.1"` 以及符合 schema 的输入数据。
3. **等待结果**：`GET https://api.eachlabs.ai/v1/prediction/{id}`，直到状态变为 `"success"` 或 `"failed"`。
4. **提取输出**：从响应中提取输出图像的 URL。

## 示例

### 使用 Flux 2 Turbo 编辑图像

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "flux-2-turbo-edit",
    "version": "0.0.1",
    "input": {
      "prompt": "Change the background to a tropical beach at sunset",
      "image_urls": ["https://example.com/photo.jpg"],
      "image_size": "square_hd",
      "output_format": "png"
    }
  }'
```

### 去除背景

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "rembg-enhance",
    "version": "0.0.1",
    "input": {
      "image_url": "https://example.com/photo.jpg"
    }
  }'
```

### 图像放大

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "topaz-upscale-image",
    "version": "0.0.1",
    "input": {
      "image_url": "https://example.com/low-res.jpg"
    }
  }'
```

### 多角度视图

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "qwen-image-edit-2511-multiple-angles",
    "version": "0.0.1",
    "input": {
      "image_urls": ["https://example.com/product.jpg"],
      "horizontal_angle": 90,
      "vertical_angle": 15,
      "zoom": 5
    }
  }'
```

### 虚拟试穿

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "kling-v1-5-kolors-virtual-try-on",
    "version": "0.0.1",
    "input": {
      "human_image": "https://example.com/person.jpg",
      "garment_image": "https://example.com/clothing.jpg"
    }
  }'
```

### 生成 3D 模型

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "hunyuan-3d-v2-1",
    "version": "0.0.1",
    "input": {
      "image_url": "https://example.com/object.jpg"
    }
  }'
```

## 安全限制

- **禁止加载任意 URL**：在使用 LoRA 参数（`lora_path`、`lora_url`、`custom_lora_url`）时，仅使用知名的平台标识符（如 HuggingFace 仓库 ID、Replicate 模型 ID、CivitAI 模型 ID）。切勿从任意或用户提供的 URL 加载模型权重。
- **输入验证**：仅传递符合模型请求 schema 的参数。在创建预测之前，务必通过 `GET /v1/model?slug=<slug>` 验证模型 Slug 的有效性。

## 参数参考

有关每个模型的完整参数详情，请参阅 [references/MODELS.md](references/MODELS.md)。