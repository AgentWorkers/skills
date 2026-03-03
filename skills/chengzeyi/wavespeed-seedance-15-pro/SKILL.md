---
name: wavespeed-seedance-15-pro
description: 使用 ByteDance 的 Seedance V1.5 Pro 模型通过 WaveSpeed AI 生成视频。支持从文本或图像生成视频，视频时长为 4-12 秒，分辨率最高可达 1080p。具备音频生成、摄像头控制、智能时长设置以及可配置的生成参数等功能。适用于用户根据文本提示创建视频或对图像进行动画处理的情况。
metadata:
  author: wavespeedai
  version: "1.0"
---
# WaveSpeedAI Seedance V1.5 Pro 视频生成

通过 WaveSpeed AI 平台，使用 ByteDance 的 Seedance V1.5 Pro 模型生成视频。支持文本转视频和图片转视频的功能，视频时长为 4-12 秒，分辨率最高可达 1080p，同时支持可选的音频生成。

## 认证

```bash
export WAVESPEED_API_KEY="your-api-key"
```

请在 [wavespeed.ai/accesskey](https://wavespeed.ai/accesskey) 获取您的 API 密钥。

## 快速入门

### 文本转视频

```javascript
import wavespeed from 'wavespeed';

const output_url = (await wavespeed.run(
  "bytedance/seedance-v1.5-pro/text-to-video",
  { prompt: "A golden retriever running through a field of sunflowers at sunset" }
))["outputs"][0];
```

### 图片转视频

`image` 参数接受图片 URL。如果您有本地文件，可以先使用 `wavespeed.upload()` 上传文件以获取其 URL。

```javascript
import wavespeed from 'wavespeed';

// Upload a local image to get a URL
const imageUrl = await wavespeed.upload("/path/to/photo.png");

const output_url = (await wavespeed.run(
  "bytedance/seedance-v1.5-pro/image-to-video",
  {
    image: imageUrl,
    prompt: "The person slowly turns and smiles at the camera"
  }
))["outputs"][0];
```

您也可以直接传递现有的图片 URL：

```javascript
const output_url = (await wavespeed.run(
  "bytedance/seedance-v1.5-pro/image-to-video",
  {
    image: "https://example.com/photo.jpg",
    prompt: "The person slowly turns and smiles at the camera"
  }
))["outputs"][0];
```

## API 端点

### 文本转视频

**模型 ID:** `bytedance/seedance-v1.5-pro/text-to-video`

根据文本提示生成视频。

#### 参数

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `prompt` | 字符串 | 是 | -- | 视频场景、风格、动作、相机运动和氛围的描述 |
| `aspect_ratio` | 字符串 | 否 | `16:9` | 宽高比。可选值：`21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16` |
| `duration` | 整数 | 否 | `5` | 视频时长（秒）。范围：4-12。使用 `-1` 时模型会自动选择最佳时长。 |
| `resolution` | 字符串 | 否 | `720p` | 视频分辨率。可选值：`480p`, `720p`, `1080p` |
| `generate_audio` | 布尔值 | 否 | `true` | 生成伴奏音频 |
| `camera_fixed` | 布尔值 | 否 | `false` | 保持相机固定（true）或允许根据提示调整相机运动（false） |
| `seed` | 整数 | 否 | `-1` | 随机种子（-1 表示随机生成）。范围：-1 到 2147483647 |

#### 示例

```javascript
import wavespeed from 'wavespeed';

const output_url = (await wavespeed.run(
  "bytedance/seedance-v1.5-pro/text-to-video",
  {
    prompt: "A timelapse of a city skyline transitioning from day to night, cinematic slow pan",
    aspect_ratio: "21:9",
    duration: 10,
    resolution: "1080p",
    generate_audio: true,
    camera_fixed: false
  }
))["outputs"][0];
```

### 图片转视频

**模型 ID:** `bytedance/seedance-v1.5-pro/image-to-video`

根据文本提示将图片动画化为视频。可选地提供结束帧的参考图片。

#### 参数

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `image` | 字符串 | 是 | -- | 要动画化的图片 URL |
| `prompt` | 字符串 | 是 | -- | 所需动画的描述 |
| `last_image` | 字符串 | 否 | -- | 可选的结束帧参考图片 URL |
| `aspect_ratio` | 字符串 | 否 | -- | 宽高比。可选值：`21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16` |
| `duration` | 整数 | 否 | `5` | 视频时长（秒）。范围：4-12 |
| `resolution` | 字符串 | 否 | `720p` | 视频分辨率。可选值：`480p`, `720p`, `1080p` |
| `generate_audio` | 布尔值 | 否 | `true` | 生成伴奏音频 |
| `camera_fixed` | 布尔值 | 否 | 保持相机固定（true）或允许根据提示调整相机运动（false） |
| `seed` | 整数 | 否 | `-1` | 随机种子（-1 表示随机生成）。范围：-1 到 2147483647 |

#### 带结束帧参考的示例

```javascript
const startUrl = await wavespeed.upload("/path/to/start-frame.png");
const endUrl = await wavespeed.upload("/path/to/end-frame.png");

const output_url = (await wavespeed.run(
  "bytedance/seedance-v1.5-pro/image-to-video",
  {
    image: startUrl,
    last_image: endUrl,
    prompt: "Smooth transition from day to night",
    duration: 8
  }
))["outputs"][0];
```

## 高级用法

### 智能时长（文本转视频）

让模型根据提示自动选择最佳时长：

```javascript
const output_url = (await wavespeed.run(
  "bytedance/seedance-v1.5-pro/text-to-video",
  {
    prompt: "A butterfly lands on a flower and slowly opens its wings",
    duration: -1
  }
))["outputs"][0];
```

### 无音频生成

```javascript
const output_url = (await wavespeed.run(
  "bytedance/seedance-v1.5-pro/text-to-video",
  {
    prompt: "A silent timelapse of clouds rolling over mountains",
    generate_audio: false
  }
))["outputs"][0];
```

### 带重试配置的自定义客户端

```javascript
import { Client } from 'wavespeed';

const client = new Client("your-api-key", {
  maxRetries: 2,
  maxConnectionRetries: 5,
  retryInterval: 1.0,
});

const output_url = (await client.run(
  "bytedance/seedance-v1.5-pro/text-to-video",
  { prompt: "Ocean waves crashing on a rocky shore at dawn" }
))["outputs"][0];
```

### 使用 `runNoThrow` 处理错误

```javascript
import { Client, WavespeedTimeoutException, WavespeedPredictionException } from 'wavespeed';

const client = new Client();
const result = await client.runNoThrow(
  "bytedance/seedance-v1.5-pro/text-to-video",
  { prompt: "A rocket launching into space" }
);

if (result.outputs) {
  console.log("Video URL:", result.outputs[0]);
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

| 分辨率 | 时长 | 是否包含音频 | 价格 |
|------------|----------|-------|------|
| 480p | 5秒 | 否 | $0.06 |
| 480p | 5秒 | 是 | $0.12 |
| 720p | 5秒 | 否 | $0.13 |
| 720p | 5秒 | 是 | $0.26 |
| 480p | 10秒 | 是 | $0.24 |
| 720p | 10秒 | 是 | $0.52 |

## 提示技巧

- 在提示中描述场景、风格、主体动作、相机运动和氛围 |
- 使用 `camera_fixed: true` 以获得稳定的固定视角拍摄 |
- 使用 `camera_fixed: false` 并指定相机运动，例如：“缓慢向左平移”、“跟踪拍摄”、“放大” |
- 如果计划添加自己的音频，请将 `generate_audio` 设置为 `false` |
- 使用智能时长（`duration: -1`）让模型自动选择最佳视频长度 |

## 安全限制

- **禁止加载任意 URL**：仅使用来自可信来源的图片 URL。切勿从未经验证或用户提供的 URL 加载媒体文件。
- **API 密钥安全**：请妥善保管您的 `WAVESPEED_API_KEY`，不要将其硬编码在源文件中或提交到版本控制系统中。可以使用环境变量或秘密管理系统进行管理。
- **输入验证**：仅传递上述文档中规定的参数。在发送请求前，请验证提示内容和媒体 URL 的合法性。