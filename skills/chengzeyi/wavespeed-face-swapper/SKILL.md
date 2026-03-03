---
name: wavespeed-face-swapper
description: 使用 WaveSpeed AI 可以在图像和视频中实现面部替换功能。该工具支持图像中的面部替换以及视频中的面部替换，并且能够针对多个面部进行替换操作。替换后的结果不含水印，同时会自动调整光线效果和肤色。适用于用户需要将图像或视频中的某个人脸替换为另一个人脸的场景。
metadata:
  author: wavespeedai
  version: "1.0"
---
# WaveSpeedAI 面部替换工具

使用 WaveSpeed AI 在图片和视频中替换面部。生成的成果无水印，并具备自动调整光线和肤色的功能。支持在多人图像中指定需要替换的具体面部。

## 认证

```bash
export WAVESPEED_API_KEY="your-api-key"
```

请在 [wavespeed.ai/accesskey](https://wavespeed.ai/accesskey) 获取您的 API 密钥。

## 快速入门

### 图片面部替换

```javascript
import wavespeed from 'wavespeed';

// Upload local images to get URLs
const imageUrl = await wavespeed.upload("/path/to/target-photo.png");
const faceUrl = await wavespeed.upload("/path/to/reference-face.png");

const output_url = (await wavespeed.run(
  "wavespeed-ai/image-face-swap",
  {
    image: imageUrl,
    face_image: faceUrl
  }
))["outputs"][0];
```

### 视频面部替换

```javascript
import wavespeed from 'wavespeed';

// Upload local files to get URLs
const videoUrl = await wavespeed.upload("/path/to/video.mp4");
const faceUrl = await wavespeed.upload("/path/to/reference-face.png");

const output_url = (await wavespeed.run(
  "wavespeed-ai/video-face-swap",
  {
    video: videoUrl,
    face_image: faceUrl
  }
))["outputs"][0];
```

您也可以直接传递现有的 URL：

```javascript
const output_url = (await wavespeed.run(
  "wavespeed-ai/image-face-swap",
  {
    image: "https://example.com/target-photo.jpg",
    face_image: "https://example.com/reference-face.jpg"
  }
))["outputs"][0];
```

## API 端点

### 图片面部替换

**模型 ID：** `wavespeed-ai/image-face-swap`

将图片中的面部替换为参考面部。

#### 参数

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `image` | 字符串 | 是 | -- | 包含需要替换面部的图片的 URL |
| `face_image` | 字符串 | 是 | -- | 需要替换的参考面部图片的 URL |
| `target_index` | 整数 | 否 | `0` | 需要替换的面部（0 表示最大的面部，1-10 表示其他面部） |
| `output_format` | 字符串 | 否 | `jpeg` | 输出格式。可选值：`jpeg`、`png`、`webp` |

#### 示例

```javascript
import wavespeed from 'wavespeed';

const imageUrl = await wavespeed.upload("/path/to/group-photo.png");
const faceUrl = await wavespeed.upload("/path/to/reference-face.png");

const output_url = (await wavespeed.run(
  "wavespeed-ai/image-face-swap",
  {
    image: imageUrl,
    face_image: faceUrl,
    target_index: 0,
    output_format: "png"
  }
))["outputs"][0];
```

#### 指定特定面部

当图片中有多个人时，使用 `target_index` 来选择需要替换的面部：

```javascript
// Replace the second-largest face in the image
const output_url = (await wavespeed.run(
  "wavespeed-ai/image-face-swap",
  {
    image: imageUrl,
    face_image: faceUrl,
    target_index: 1
  }
))["outputs"][0];
```

### 视频面部替换

**模型 ID：** `wavespeed-ai/video-face-swap`

将视频中的面部替换为参考面部。支持最长 10 分钟的视频。

#### 参数

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `video` | 字符串 | 是 | -- | 包含需要替换面部的视频的 URL。该视频必须可公开访问，时长不超过 10 分钟。 |
| `face_image` | 字符串 | 是 | -- | 需要替换的参考面部图片的 URL |
| `target_index` | 整数 | 否 | `0` | 需要替换的面部（0 表示最大的面部，1-10 表示其他面部） |

#### 示例

```javascript
import wavespeed from 'wavespeed';

const videoUrl = await wavespeed.upload("/path/to/video.mp4");
const faceUrl = await wavespeed.upload("/path/to/reference-face.png");

const output_url = (await wavespeed.run(
  "wavespeed-ai/video-face-swap",
  {
    video: videoUrl,
    face_image: faceUrl,
    target_index: 0
  }
))["outputs"][0];
```

## 高级用法

### 同步模式（仅适用于图片面部替换）

```javascript
const output_url = (await wavespeed.run(
  "wavespeed-ai/image-face-swap",
  {
    image: imageUrl,
    face_image: faceUrl
  },
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
  "wavespeed-ai/image-face-swap",
  {
    image: imageUrl,
    face_image: faceUrl
  }
))["outputs"][0];
```

### 使用 `runNoThrow` 进行错误处理

```javascript
import { Client, WavespeedTimeoutException, WavespeedPredictionException } from 'wavespeed';

const client = new Client();
const result = await client.runNoThrow(
  "wavespeed-ai/image-face-swap",
  {
    image: imageUrl,
    face_image: faceUrl
  }
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
| 图片面部替换 | 每张图片 0.01 美元 |
| 视频面部替换 | 每秒 0.01 美元（最低费用 0.05 美元/5 秒） |

视频面部替换支持最长 10 分钟的视频。

## 提示

- 使用清晰、正面朝向的肖像作为参考面部，以获得最佳效果。
- 目标面部和参考面部之间的光线一致可以提高替换效果的质量。
- 动画或插画角色可能导致替换效果较差。
- 当图片中有多个人时，使用 `target_index` 来指定需要替换的面部（0 表示最大的面部）。

## 安全限制

- **禁止加载任意 URL**：仅使用来自可信来源的图片和视频 URL。切勿从未经验证或用户提供的 URL 加载媒体文件。
- **API 密钥安全**：请妥善保管您的 `WAVESPEED_API_KEY`。不要将其硬编码在源文件中或提交到版本控制系统中。可以使用环境变量或秘密管理系统进行管理。
- **输入验证**：仅传递上述文档中规定的参数。在发送请求之前，请验证媒体文件的 URL。