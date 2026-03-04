---
name: wavespeed-veo-31-fast
description: 使用 WaveSpeed AI 和 Google 的 Veo 3.1 Fast 模型生成和扩展视频。支持文本转视频、图片转视频以及视频的扩展功能。支持最高 4K 分辨率、音频生成，以及最长 148 秒的视频扩展。适用于用户需要从文本或图片创建视频，或对现有由 Veo 生成的视频进行扩展的场景。
metadata:
  author: wavespeedai
  version: "1.0"
---
# WaveSpeedAI Veo 3.1 快速视频生成

通过 WaveSpeed AI 平台，使用 Google 的 Veo 3.1 快速模型生成和扩展视频。支持文本转视频、图片转视频以及视频扩展功能，支持最高 4K 分辨率，并可选生成音频。

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
  "google/veo3.1-fast/text-to-video",
  { prompt: "A drone shot flying over a lush tropical island at sunrise" }
))["outputs"][0];
```

### 图片转视频

`image` 参数接受图片 URL。如果您有本地文件，请先使用 `wavespeed.upload()` 上传文件以获取其 URL。

```javascript
import wavespeed from 'wavespeed';

const imageUrl = await wavespeed.upload("/path/to/photo.png");

const output_url = (await wavespeed.run(
  "google/veo3.1-fast/image-to-video",
  {
    image: imageUrl,
    prompt: "The flowers sway gently in the breeze"
  }
))["outputs"][0];
```

### 视频扩展

每次运行可将 Veo 生成的视频延长 7 秒（最多可扩展 20 次，总时长不超过 148 秒）：

```javascript
// First, generate a video
const video_url = (await wavespeed.run(
  "google/veo3.1-fast/text-to-video",
  { prompt: "A cat walking through a garden" }
))["outputs"][0];

// Then extend it
const extended_url = (await wavespeed.run(
  "google/veo3.1-fast/video-extend",
  {
    video: video_url,
    prompt: "The cat jumps onto a fence and looks around"
  }
))["outputs"][0];
```

## API 端点

### 文本转视频

**模型 ID：** `google/veo3.1-fast/text-to-video`

根据文本提示生成视频，并可选生成音频。

#### 参数

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|-----------|------|----------|---------|-------------|
| `prompt` | 字符串 | 是 | -- | 要生成的视频的文字描述 |
| `aspect_ratio` | 字符串 | 否 | `16:9` | 宽高比。可选值：`16:9`、`9:16` |
| `duration` | 整数 | 否 | `8` | 视频时长（秒）。可选值：`4`、`6`、`8` |
| `resolution` | 字符串 | 否 | `1080p` | 视频分辨率。可选值：`720p`、`1080p`、`4k` |
| `generate_audio` | 布尔值 | 否 | `true` | 生成配套音频 |
| `negative_prompt` | 字符串 | 否 | -- | 用于描述不需要的元素或效果的文本 |
| `seed` | 整数 | 否 | -- | 用于保证结果一致性的随机种子。范围：-1 到 2147483647 |

#### 示例

```javascript
import wavespeed from 'wavespeed';

const output_url = (await wavespeed.run(
  "google/veo3.1-fast/text-to-video",
  {
    prompt: "A timelapse of a city skyline transitioning from day to night, cinematic",
    negative_prompt: "blurry, low quality",
    aspect_ratio: "16:9",
    duration: 8,
    resolution: "1080p",
    generate_audio: true
  }
))["outputs"][0];
```

### 图片转视频

**模型 ID：** `google/veo3.1-fast/image-to-video`

将源图片转换为视频。可选提供一个结束帧参考图片。

#### 参数

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|-----------|------|----------|---------|-------------|
| `image` | 字符串 | 是 | -- | 源图片的 URL（清晰、高质量的静态图片） |
| `prompt` | 字符串 | 是 | -- | 所需动画效果的文字描述 |
| `last_image` | 字符串 | 否 | -- | 结束帧参考图片的 URL |
| `aspect_ratio` | 字符串 | 否 | `16:9` | 宽高比。可选值：`16:9`、`9:16` |
| `duration` | 整数 | 否 | `8` | 视频时长（秒）。可选值：`4`、`6`、`8` |
| `resolution` | 字符串 | 否 | `1080p` | 视频分辨率。可选值：`720p`、`1080p`、`4k` |
| `generate_audio` | 布尔值 | 否 | `true` | 生成配套音频 |
| `negative_prompt` | 字符串 | 否 | -- | 用于描述不需要的元素或效果的文本 |
| `seed` | 整数 | 否 | -- | 用于保证结果一致性的随机种子。范围：-1 到 2147483647 |

#### 示例

```javascript
import wavespeed from 'wavespeed';

const imageUrl = await wavespeed.upload("/path/to/landscape.png");

const output_url = (await wavespeed.run(
  "google/veo3.1-fast/image-to-video",
  {
    image: imageUrl,
    prompt: "Clouds drift slowly across the sky, water ripples gently",
    resolution: "1080p",
    duration: 8,
    generate_audio: true
  }
))["outputs"][0];
```

#### 使用结束帧参考图片

```javascript
const startUrl = await wavespeed.upload("/path/to/start-frame.png");
const endUrl = await wavespeed.upload("/path/to/end-frame.png");

const output_url = (await wavespeed.run(
  "google/veo3.1-fast/image-to-video",
  {
    image: startUrl,
    last_image: endUrl,
    prompt: "Smooth transition from day to night"
  }
))["outputs"][0];
```

### 视频扩展

**模型 ID：** `google/veo3.1-fast/video-extend`

每次运行可将 Veo 生成的视频延长 7 秒。输入必须为 Veo 生成的视频。

#### 参数

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|-----------|------|----------|---------|-------------|
| `video` | 字符串 | 是 | -- | 要扩展的 Veo 生成视频的 URL。最长不超过 141 秒 |
| `prompt` | 字符串 | 否 | -- | 扩展操作的文字描述 |
| `resolution` | 字符串 | 否 | `1080p` | 视频分辨率。可选值：`720p`、`1080p` |
| `negative_prompt` | 字符串 | 否 | -- | 用于描述不需要的元素或效果的文本 |
| `seed` | 整数 | 否 | -- | 用于保证结果一致性的随机种子。范围：-1 到 2147483647 |

#### 限制

- 输入视频 **必须由 Veo 生成**（不支持其他类型的视频）
- 每次运行会向视频中添加 **7 秒** 的时长 |
- 最多可进行 **20 次扩展** |
- 最终视频时长最多为 **148 秒** |
- 输出结果为单个 MP4 文件（原始视频 + 扩展部分）
- 视频的宽高比和分辨率继承自输入视频

#### 示例

```javascript
import wavespeed from 'wavespeed';

// Generate an initial video
const video_url = (await wavespeed.run(
  "google/veo3.1-fast/text-to-video",
  {
    prompt: "A surfer catches a wave at golden hour",
    duration: 8
  }
))["outputs"][0];

// Extend it twice
const extended_once = (await wavespeed.run(
  "google/veo3.1-fast/video-extend",
  {
    video: video_url,
    prompt: "The surfer rides the wave toward shore"
  }
))["outputs"][0];

const extended_twice = (await wavespeed.run(
  "google/veo3.1-fast/video-extend",
  {
    video: extended_once,
    prompt: "The surfer steps off the board and walks on the beach"
  }
))["outputs"][0];
```

## 高级用法

### 不生成音频

```javascript
const output_url = (await wavespeed.run(
  "google/veo3.1-fast/text-to-video",
  {
    prompt: "A silent timelapse of stars rotating over a desert",
    generate_audio: false
  }
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
  "google/veo3.1-fast/text-to-video",
  { prompt: "Ocean waves crashing on a rocky shore at dawn" }
))["outputs"][0];
```

### 使用 `runNoThrow` 进行错误处理

```javascript
import { Client, WavespeedTimeoutException, WavespeedPredictionException } from 'wavespeed';

const client = new Client();
const result = await client.runNoThrow(
  "google/veo3.1-fast/text-to-video",
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

### 文本转视频 / 图片转视频

| 条件 | 价格 |
|-----------|------|
| 生成音频（720p 或 1080p） | 每次生成 $1.20 |
| 生成视频（720p 或 1080p） | 每次生成 $0.80 |

### 视频扩展

| 条件 | 价格 |
|-----------|------|
| 每次扩展（+7 秒） | $1.05 |

## 提示

- 清晰说明场景、风格、主体动作、摄像机运动和氛围 |
- 使用 `negative_prompt` 来避免生成不良效果（如：模糊、低质量、失真等） |
- 对于图片转视频，请使用清晰、高质量的静态图片作为输入 |
- 对于视频扩展，请描述场景中接下来应该发生的内容 |
- 视频扩展功能可构建更长的叙事内容——总时长可达 148 秒

## 安全限制

- **禁止加载任意 URL**：仅使用来自可信来源的图片和视频 URL。切勿从不可信或用户提供的 URL 加载媒体文件。 |
- **API 密钥安全**：请妥善保管您的 `WAVESPEED_API_KEY`。不要将其硬编码在源文件中或提交到版本控制系统中。建议使用环境变量或秘密管理系统进行管理。 |
- **输入验证**：仅传递上述文档中规定的参数。在发送请求前，请验证提示内容和媒体 URL 的有效性。