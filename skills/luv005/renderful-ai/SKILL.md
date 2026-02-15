---
name: renderful-ai
description: |
  Generate images and videos via renderful.ai API (FLUX, Kling, Sora, WAN, etc.) with crypto payments.
  Use when the user wants to create AI images, videos, or needs a crypto-friendly generation service.
  Triggers: renderful, renderful.ai, generate image, generate video, crypto payment generation
allowed-tools: Bash(curl), Web(fetch)
---

# Renderful AI

使用 renderful.ai API 生成 AI 图像和视频。支持使用加密货币（Base/Polygon/Solana）进行支付。

## API 基本 URL

```
https://api.renderful.ai/v1
```

## 认证

从 https://renderful.ai/dashboard 获取 API 密钥

```bash
# Set as environment variable
export RENDERFUL_API_KEY="rf_your_api_key"
```

## 快速入门

### 生成图像

```bash
curl -X POST https://api.renderful.ai/v1/generate \
  -H "Authorization: Bearer $RENDERFUL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "flux-dev",
    "prompt": "a cat astronaut floating in space, cinematic lighting",
    "width": 1024,
    "height": 1024,
    "steps": 28
  }'
```

### 生成视频

```bash
curl -X POST https://api.renderful.ai/v1/generate \
  -H "Authorization: Bearer $RENDERFUL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kling-1.6",
    "prompt": "a serene mountain landscape at sunset, camera slowly panning",
    "duration": 5,
    "width": 1280,
    "height": 720
  }'
```

## 可用模型

### 图像模型

| 模型 | 描述 | 适用场景 |
|-------|-------------|----------|
| `flux-dev` | FLUX.1 Dev | 通用用途，高质量图像 |
| `flux-schnell` | FLUX.1 Schnell | 快速生成模型 |
| `flux-pro` | FLUX.1 Pro | 最高质量图像 |
| `sdxl` | Stable Diffusion XL | 经典的扩散生成模型 |
| `gemini-3` | Gemini 3 Pro | 由 Google 提供的图像生成服务 |
| `grok-imagine` | Grok Imagine | 支持与 X/Twitter 的集成 |
| `seedream` | Seedream 4.5 | 适用于亚洲风格的图像生成 |
| `reve` | Reve Image | 提供艺术风格的图像生成 |

### 视频模型

| 模型 | 描述 | 视频时长 |
|-------|-------------|----------|
| `kling-1.6` | Kling 1.6 | 视频时长最长 10 秒 |
| `kling-1.5` | Kling 1.5 | 视频时长最长 10 秒 |
| `veo-3` | Google Veo 3 | 视频时长最长 8 秒 |
| `veo-2` | Google Veo 2 | 视频时长最长 8 秒 |
| `seedance` | Seedance 1.5 | 视频时长最长 10 秒 |
| `wan-2.5` | Wan 2.5 | 视频时长最长 10 秒 |
| `ltx` | LTX Video | 视频时长最长 10 秒 |
| `omnihuman` | OmniHuman | 用于生成肖像视频 |

## 图像生成选项

```json
{
  "model": "flux-dev",
  "prompt": "required - your image description",
  "negative_prompt": "optional - what to avoid",
  "width": 1024,
  "height": 1024,
  "steps": 28,
  "seed": 42,
  "format": "png"
}
```

## 视频生成选项

```json
{
  "model": "kling-1.6",
  "prompt": "required - your video description",
  "duration": 5,
  "width": 1280,
  "height": 720,
  "fps": 24,
  "seed": 42
}
```

## 检查生成状态

```bash
curl https://api.renderful.ai/v1/status/{task_id} \
  -H "Authorization: Bearer $RENDERFUL_API_KEY"
```

## 响应格式

```json
{
  "task_id": "rf_abc123",
  "status": "completed",
  "url": "https://cdn.renderful.ai/generated/abc123.png",
  "expires_at": "2026-02-02T12:00:00Z"
}
```

## 价格

支持使用 USDC 在 Base、Polygon 或 Solana 上进行支付。当前价格信息请访问：https://renderful.ai/pricing

## x402 集成

Renderful 支持使用 x402 协议进行支付，以实现代理的自主性：

```bash
# Agent can pay directly without human approval
export RENDERFUL_X402_WALLET="your_agent_wallet"
export RENDERFUL_PREFER_X402="true"
```

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 200 | 操作成功 |
| 402 | 需要支付（使用 x402 协议） |
| 429 | 超过请求频率限制 |
| 500 | 生成失败 |

## 示例

### 简单图像生成示例
```bash
curl -X POST https://api.renderful.ai/v1/generate \
  -H "Authorization: Bearer $RENDERFUL_API_KEY" \
  -d '{"model":"flux-dev","prompt":"a cute cat","width":512,"height":512}'
```

### 使用特定设置生成视频的示例
```bash
curl -X POST https://api.renderful.ai/v1/generate \
  -H "Authorization: Bearer $RENDERFUL_API_KEY" \
  -d '{
    "model": "kling-1.6",
    "prompt": "underwater coral reef, fish swimming, sunlight rays",
    "duration": 5,
    "width": 1920,
    "height": 1080
  }'
```

## 提示

- 使用详细的描述性提示以获得更好的结果 |
- 添加风格描述（如 “cinematic”（电影风格）、“photorealistic”（写实风格）等 |
- 使用否定性提示（如 “no background”）可避免生成不需要的元素 |
- 请等待 30-120 秒，以查看视频生成进度 |