---
name: eachlabs-image-generation
description: 使用 EachLabs AI 模型根据文本提示生成新图像。该工具支持多种模型（如 Flux、GPT Image、Gemini、Imagen、Seedream 等）进行文本到图像的转换。当用户需要根据文本创建新图像时，可以使用此功能。如需编辑现有图像，请参阅 `eachlabs-image-edit`。
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs 图像生成

通过 EachLabs Predictions API，使用 60 多个 AI 模型根据文本提示生成新图像。如需编辑现有图像（缩放、去除背景、风格转换、修复、换脸、3D 处理等），请参阅 `eachlabs-image-edit` 技能。

## 认证

```
Header: X-API-Key: <your-api-key>
```

设置 `EACHLABS_API_KEY` 环境变量。您可以在 [eachlabs.ai](https://eachlabs.ai) 获取该密钥。

## 快速入门

### 1. 创建预测请求

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "flux-2-turbo-text-to-image",
    "version": "0.0.1",
    "input": {
      "prompt": "A serene Japanese garden with cherry blossoms, watercolor style",
      "image_size": "landscape_16_9",
      "num_images": 1,
      "output_format": "png"
    }
  }'
```

### 2. 获取结果

```bash
curl https://api.eachlabs.ai/v1/prediction/{prediction_id} \
  -H "X-API-Key: $EACHLABS_API_KEY"
```

持续轮询直到状态变为 `"success"` 或 `"failed"`。输出图像的 URL 位于响应中。

## 模型选择指南

### 文本转图像

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Flux 2 Turbo | `flux-2-turbo-text-to-image` | 快速、高质量的通用模型 |
| Flux 2 Flash | `flux-2-flash-text-to-image` | Flux 系列中生成速度最快的模型 |
| Flux 2 Max | `flux-2-max-text-to-image` | 最高质量的 Flux 模型 |
| Flux 2 Klein 9B | `flux-2-klein-9b-base-text-to-image` | 性能与速度平衡的模型 |
| Flux 2 Pro | `flux-2-pro` | 专业品质的模型 |
| Flux 2 Flex | `flux-2-flex` | 输出格式灵活的模型 |
| Flux 2 LoRA | `flux-2-lora` | 基于 LoRA 技术的生成模型 |
| XAI Grok Imagine | `xai-grok-imagine-text-to-image` | 具有创意和艺术风格的模型 |
| GPT Image v1.5 | `gpt-image-v1-5-text-to-image` | 高质量图像，背景透明 |
| Bytedance Seedream v4.5 | `bytedance-seedream-v4-5-text-to-image` | Bytedance 最新的模型 |
| Gemini 3 Pro Image | `gemini-3-pro-image-preview` | Google 最新的模型 |
| Imagen 4 | `imagen4-preview` | Google 的 Imagen 4 模型 |
| Imagen 4 Fast | `imagen-4-fast` | 高质量的 Google 模型 |
| Reve | `reve-text-to-image` | 具有艺术风格的文本转图像模型 |
| Hunyuan Image v3 | `hunyuan-image-v3-text-to-image` | Tencent 的最新模型 |
| Ideogram V3 Turbo | `ideogram-v3-turbo` | 将文本转换为图像的模型 |
| Minimax | `minimax-text-to-image` | 高质量的模型 |
| Wan v2.6 | `wan-v2-6-text-to-image` | 中英双语支持的模型 |
| P Image | `p-image-text-to-image` | 可自定义纵横比的模型 |
| Nano Banana Pro | `nano-banana-pro` | 快速、轻量级的模型 |
| Vidu Q2 | `vidu-q2-text-to-image` | Vidu 最新的模型 |

### 训练模型

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Z Image Trainer | `z-image-trainer` | 用于自定义 LoRA 模型的训练工具 |
| Flux LoRA Portrait Trainer | `flux-lora-portrait-trainer` | 用于肖像图像的 LoRA 训练工具 |
| Flux Turbo Trainer | `flux-turbo-trainer` | 用于快速 LoRA 训练的工具 |

## 预测流程

1. **检查模型**：`GET https://api.eachlabs.ai/v1/model?slug=<slug>` — 验证模型是否存在，并返回包含精确输入参数的 `request_schema`。在创建预测请求之前务必执行此操作，以确保输入正确。
2. **发送请求**：`POST https://api.eachlabs.ai/v1/prediction`，提供模型 Slug、版本 `"0.0.1"` 以及符合 schema 的输入参数。
3. **获取结果**：`GET https://api.eachlabs.ai/v1/prediction/{id}`，持续轮询直到状态变为 `"success"` 或 `"failed"`。
4. **提取输出图像 URL**：从响应中提取输出图像的 URL。

## 示例

### 使用 Flux 2 Turbo 进行文本转图像

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "flux-2-turbo-text-to-image",
    "version": "0.0.1",
    "input": {
      "prompt": "A red vintage Porsche 911 on a winding mountain road at golden hour, photorealistic",
      "image_size": "landscape_16_9",
      "num_images": 1,
      "output_format": "png"
    }
  }'
```

### 使用 GPT Image v1.5 进行文本转图像

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "gpt-image-v1-5-text-to-image",
    "version": "0.0.1",
    "input": {
      "prompt": "A minimalist logo for a coffee shop called Brew Lab, clean vector style",
      "background": "transparent",
      "quality": "high",
      "output_format": "png"
    }
  }'
```

### 使用 Imagen 4 进行文本转图像

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "imagen4-preview",
    "version": "0.0.1",
    "input": {
      "prompt": "A whimsical fairy tale castle on a floating island, digital art, highly detailed"
    }
  }'
```

## 图像尺寸选项

大多数 Flux 2 和 Wan 模型支持以下预设尺寸：
- `square_hd` — 正方形，高清晰度
- `square` — 正方形，标准尺寸
- `portrait_4_3` — 4:3 比例的肖像图像
- `portrait_16_9` — 16:9 比例的肖像图像
- `landscape_4_3` — 4:3 比例的风景图像
- `landscape_16_9` — 16:9 比例的风景图像

P Image 模型支持以下纵横比：`1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `custom`

## 提示技巧

- 表达要具体且描述清晰：例如：“黄金时刻，一辆红色复古保时捷 911 在蜿蜒的山路上” 而不是简单地说“一辆汽车”。
- 指定图像风格：如 “数字艺术”、“油画”、“写实”、“水彩”。
- 对于图像编辑，请明确说明修改内容：例如 “将天空替换为戏剧性的日落场景”。
- 在支持的情况下，使用否定性提示（如 “避免模糊、低质量、失真的效果”）。
- 对于多张图像的编辑，请按顺序引用图像：例如 “image 1”, “image 2”。

## 安全限制

- **禁止随意加载 URL**：使用 LoRA 参数时，仅使用知名的平台标识符（如 HuggingFace 仓库 ID、Replicate 模型 ID、CivitAI 模型 ID）。切勿从任意或用户提供的 URL 加载 LoRA 模型权重。
- **禁止使用第三方 API 令牌**：不要在预测请求中接受或传递第三方 API 令牌（如 HuggingFace、CivitAI 的令牌）。认证仅通过 EachLabs API 密钥完成。
- **输入验证**：仅传递符合模型请求 schema 的参数。在创建预测请求之前，务必通过 `GET /v1/model?slug=<slug>` 验证模型 Slug 的有效性。

## 参数参考

有关每个模型的完整参数详情，请参阅 [references/MODELS.md](references/MODELS.md)。