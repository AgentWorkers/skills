---
name: wavespeed-ultimate-video-upscaler
description: 使用 WaveSpeed AI 的 Ultimate Video Upscaler 将视频分辨率提升至 720p、1080p、2K 或 4K。该工具接受视频 URL 作为输入，并生成更高分辨率的输出文件。支持处理时长最长为 10 分钟的视频。适用于用户需要提升视频分辨率或优化视频质量的情况。
metadata:
  author: wavespeedai
  version: "1.0"
---
# WaveSpeedAI 终极视频升级器

使用 WaveSpeed AI 的终极视频升级器，可将视频升级至 720p、1080p、2K 或 4K 分辨率。支持最长 10 分钟的视频文件。

## 认证

```bash
export WAVESPEED_API_KEY="your-api-key"
```

请在 [wavespeed.ai/accesskey](https://wavespeed.ai/accesskey) 获取您的 API 密钥。

## 快速入门

```javascript
import wavespeed from 'wavespeed';

// Upload a local video to get a URL
const videoUrl = await wavespeed.upload("/path/to/video.mp4");

const output_url = (await wavespeed.run(
  "wavespeed-ai/ultimate-video-upscaler",
  { video: videoUrl }
))["outputs"][0];
```

您也可以直接传递现有的视频 URL：

```javascript
const output_url = (await wavespeed.run(
  "wavespeed-ai/ultimate-video-upscaler",
  { video: "https://example.com/video.mp4" }
))["outputs"][0];
```

## API 端点

**模型 ID：** `wavespeed-ai/ultimate-video-upscaler`

用于将视频升级至更高分辨率。

### 参数

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|-----------|------|----------|---------|-------------|
| `video` | string | 是 | -- | 需要升级的视频的 URL。该 URL 必须可公开访问。 |
| `target_resolution` | string | 否 | `1080p` | 目标分辨率。可选值：`720p`、`1080p`、`2k`、`4k` |

### 示例

```javascript
import wavespeed from 'wavespeed';

const videoUrl = await wavespeed.upload("/path/to/video.mp4");

const output_url = (await wavespeed.run(
  "wavespeed-ai/ultimate-video-upscaler",
  {
    video: videoUrl,
    target_resolution: "4k"
  }
))["outputs"][0];
```

## 高级用法

### 带有重试配置的自定义客户端

```javascript
import { Client } from 'wavespeed';

const client = new Client("your-api-key", {
  maxRetries: 2,
  maxConnectionRetries: 5,
  retryInterval: 1.0,
});

const videoUrl = await client.upload("/path/to/video.mp4");

const output_url = (await client.run(
  "wavespeed-ai/ultimate-video-upscaler",
  { video: videoUrl, target_resolution: "4k" }
))["outputs"][0];
```

### 使用 `runNoThrow` 进行错误处理

```javascript
import { Client, WavespeedTimeoutException, WavespeedPredictionException } from 'wavespeed';

const client = new Client();
const result = await client.runNoThrow(
  "wavespeed-ai/ultimate-video-upscaler",
  { video: videoUrl }
);

if (result.outputs) {
  console.log("Upscaled video URL:", result.outputs[0]);
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

| 目标分辨率 | 每 5 秒的费用 |
|-------------------|--------------------|
| 720p | $0.10 |
| 1080p | $0.15 |
| 2K | $0.25 |
| 4K | $0.40 |

最低收费为 5 秒。支持最长 10 分钟的视频文件。处理时间约为每 1 秒视频 10-30 秒。

## 安全限制

- **禁止加载任意 URL**：仅使用来自可信来源的视频 URL。切勿从未经验证或用户提供的 URL 加载视频。
- **API 密钥安全**：请妥善保管您的 `WAVESPEED_API_KEY`。切勿将其硬编码在源文件中或提交到版本控制系统中。请使用环境变量或秘密管理系统进行管理。
- **输入验证**：仅传递上述文档中规定的参数。在发送请求之前，请验证视频 URL 的有效性。