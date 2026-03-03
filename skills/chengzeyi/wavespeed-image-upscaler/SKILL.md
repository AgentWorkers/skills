---
name: wavespeed-image-upscaler
description: 使用 WaveSpeed AI 的 Image Upscaler 工具，可以将图像分辨率提升至 2K、4K 或 8K。该工具接受图像 URL 作为输入，并生成更高分辨率的输出文件，支持 JPEG、PNG 和 WebP 三种输出格式。适用于用户需要提升图像分辨率或优化图像质量的情况。
metadata:
  author: wavespeedai
  version: "1.0"
---
# WaveSpeedAI 图像放大器

使用 WaveSpeed AI 的图像放大器将图像放大到 2K、4K 或 8K 分辨率。

## 认证

```bash
export WAVESPEED_API_KEY="your-api-key"
```

请在 [wavespeed.ai/accesskey](https://wavespeed.ai/accesskey) 获取您的 API 密钥。

## 快速入门

```javascript
import wavespeed from 'wavespeed';

// Upload a local image to get a URL
const imageUrl = await wavespeed.upload("/path/to/photo.png");

const output_url = (await wavespeed.run(
  "wavespeed-ai/image-upscaler",
  { image: imageUrl }
))["outputs"][0];
```

您也可以直接传递现有的图像 URL：

```javascript
const output_url = (await wavespeed.run(
  "wavespeed-ai/image-upscaler",
  { image: "https://example.com/photo.jpg" }
))["outputs"][0];
```

## API 端点

**模型 ID：** `wavespeed-ai/image-upscaler`

将图像放大到更高的分辨率。

### 参数

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|-----------|------|----------|---------|-------------|
| `image` | 字符串 | 是 | -- | 需要放大的图像的 URL |
| `target_resolution` | 字符串 | 否 | `4k` | 目标分辨率。可选值：`2k`、`4k`、`8k` |
| `output_format` | 字符串 | 否 | `jpeg` | 输出格式。可选值：`jpeg`、`png`、`webp` |

### 示例

```javascript
import wavespeed from 'wavespeed';

const imageUrl = await wavespeed.upload("/path/to/photo.png");

const output_url = (await wavespeed.run(
  "wavespeed-ai/image-upscaler",
  {
    image: imageUrl,
    target_resolution: "8k",
    output_format: "png"
  }
))["outputs"][0];
```

## 高级用法

### 同步模式

使用同步模式进行请求，该模式会等待结果而不会进行轮询：

```javascript
const output_url = (await wavespeed.run(
  "wavespeed-ai/image-upscaler",
  { image: imageUrl },
  { enableSyncMode: true }
))["outputs"][0];
```

### 带有重试配置的自定义客户端

```javascript
import { Client } from 'wavespeed';

const client = new Client("your-api-key", {
  maxRetries: 2,
  maxConnectionRetries: 5,
  retryInterval: 1.0,
});

const output_url = (await client.run(
  "wavespeed-ai/image-upscaler",
  { image: imageUrl, target_resolution: "4k" }
))["outputs"][0];
```

### 使用 `runNoThrow` 进行错误处理

```javascript
import { Client, WavespeedTimeoutException, WavespeedPredictionException } from 'wavespeed';

const client = new Client();
const result = await client.runNoThrow(
  "wavespeed-ai/image-upscaler",
  { image: imageUrl }
);

if (result.outputs) {
  console.log("Upscaled image URL:", result.outputs[0]);
  console.log("Task ID:", result.detail.taskId);
} else {
  console.log("Failed:", result.detail.error.message);
  if (result.detail.error instanceof WavespeedTimeoutException) {
    console.log("Request timed out - try increasing timeout");
  } else if (result.detail.error instanceof WavespeedPredictionException) {
    console.log("Prediction failed");
  }
}
```

## 价格

每张图像费用为 0.01 美元（所有分辨率均相同）。

## 安全限制

- **禁止加载任意 URL**：仅使用来自可信来源的图像 URL。切勿从未经验证的或用户提供的 URL 加载图像。
- **API 密钥安全**：请妥善保管您的 `WAVESPEED_API_KEY`。不要将其硬编码在源文件中，也不要提交到版本控制系统中。请使用环境变量或秘密管理系统来管理它。
- **输入验证**：仅传递上述文档中规定的参数。在发送请求之前，请验证图像 URL 的有效性。