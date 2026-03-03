---
name: wavespeed-watermark-remover
description: 使用 WaveSpeed AI 去除图片和视频中的水印、标志、字幕以及文本叠加层。该工具能够智能地检测并去除水印，同时保留图像的纹理和背景。支持处理时长最长为 10 分钟的图片和视频。适用于用户需要从媒体文件中移除水印或文本叠加层的情况。
metadata:
  author: wavespeedai
  version: "1.0"
---
# WaveSpeedAI 去水印工具

使用 WaveSpeed AI 从图片和视频中去除水印、LOGO、字幕以及文本叠加层。该工具能够智能地检测并去除水印，同时保留图像的纹理和背景。

## 认证

```bash
export WAVESPEED_API_KEY="your-api-key"
```

您可以在 [wavespeed.ai/accesskey](https://wavespeed.ai/accesskey) 获取您的 API 密钥。

## 快速入门

### 图片去水印

```javascript
import wavespeed from 'wavespeed';

// Upload a local image to get a URL
const imageUrl = await wavespeed.upload("/path/to/watermarked-image.png");

const output_url = (await wavespeed.run(
  "wavespeed-ai/image-watermark-remover",
  { image: imageUrl }
))["outputs"][0];
```

### 视频去水印

```javascript
import wavespeed from 'wavespeed';

// Upload a local video to get a URL
const videoUrl = await wavespeed.upload("/path/to/watermarked-video.mp4");

const output_url = (await wavespeed.run(
  "wavespeed-ai/video-watermark-remover",
  { video: videoUrl }
))["outputs"][0];
```

您也可以直接传递视频的 URL：

```javascript
const output_url = (await wavespeed.run(
  "wavespeed-ai/image-watermark-remover",
  { image: "https://example.com/watermarked-image.jpg" }
))["outputs"][0];
```

## API 端点

### 图片去水印

**模型 ID：** `wavespeed-ai/image-watermark-remover`

从图片中去除水印、LOGO 和文本叠加层，同时保留图像的纹理和背景。

#### 参数

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `image` | 字符串 | 是 | -- | 需要处理的图片 URL |
| `output_format` | 字符串 | 否 | `jpeg` | 输出格式。可选值：`jpeg`、`png`、`webp` |

#### 示例

```javascript
import wavespeed from 'wavespeed';

const imageUrl = await wavespeed.upload("/path/to/watermarked-photo.png");

const output_url = (await wavespeed.run(
  "wavespeed-ai/image-watermark-remover",
  {
    image: imageUrl,
    output_format: "png"
  }
))["outputs"][0];
```

### 视频去水印

**模型 ID：** `wavespeed-ai/video-watermark-remover`

从视频中去除水印、LOGO、字幕以及文本叠加层。该工具采用基于时间信息的修复算法，可防止帧间出现闪烁现象。支持处理时长最长为 10 分钟的视频。

#### 参数

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `video` | 字符串 | 是 | -- | 需要处理的视频 URL。该 URL 必须是公开可访问的，且视频时长不得超过 10 分钟。 |

#### 示例

```javascript
import wavespeed from 'wavespeed';

const videoUrl = await wavespeed.upload("/path/to/watermarked-video.mp4");

const output_url = (await wavespeed.run(
  "wavespeed-ai/video-watermark-remover",
  { video: videoUrl }
))["outputs"][0];
```

## 高级用法

### 同步模式（仅适用于图片去水印）

```javascript
const output_url = (await wavespeed.run(
  "wavespeed-ai/image-watermark-remover",
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
  "wavespeed-ai/image-watermark-remover",
  { image: imageUrl }
))["outputs"][0];
```

### 使用 `runNoThrow` 进行错误处理

```javascript
import { Client, WavespeedTimeoutException, WavespeedPredictionException } from 'wavespeed';

const client = new Client();
const result = await client.runNoThrow(
  "wavespeed-ai/image-watermark-remover",
  { image: imageUrl }
);

if (result.outputs) {
  console.log("Output URL:", result.outputs[0]);
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

| 操作 | 费用 |
|-----------|------|
| 图片去水印 | 每张图片 0.012 美元 |
| 视频去水印 | 每秒 0.01 美元（最低费用为 0.05 美元/5 秒） |

视频去水印支持处理时长最长为 10 分钟的视频。处理时间约为每秒视频长度的 5-20 秒。

## 安全限制

- **禁止加载任意 URL**：仅使用来自可信来源的图片和视频 URL。切勿从未经验证的用户提供的 URL 加载媒体文件。
- **API 密钥安全**：请妥善保管您的 `WAVESPEED_API_KEY`，切勿将其硬编码在源代码文件中或提交到版本控制系统中。建议使用环境变量或秘密管理工具进行存储。
- **输入验证**：仅传递上述文档中规定的参数。在发送请求之前，请验证媒体文件的 URL 是否合法。