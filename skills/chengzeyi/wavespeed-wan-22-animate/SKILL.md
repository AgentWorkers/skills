---
name: wavespeed-wan-22-animate
description: 使用 WaveSpeed AI 的 Wan 2.2 Animate 模型，可以通过驱动视频来为图像中的角色添加动画效果。该模型支持两种模式：**动画模式**（使图像中的角色按照视频中的动作进行移动）和**替换模式**（用图像中的角色替换视频中的主体）。输出的视频时长最长为 120 秒，分辨率支持 480p 或 720p。适用于用户希望利用参考视频为图像中的角色创建动画效果的场景。
metadata:
  author: wavespeedai
  version: "1.0"
---
# WaveSpeedAI Wan 2.2 动画功能

使用 WaveSpeed AI 的 Wan 2.2 动画模型，可以将图像中的角色通过驾驶视频进行动画处理。该模型提供两种模式：**动画模式**（使图像中的角色按照视频中的主体动作进行移动）和 **替换模式**（将视频中的主体替换为图像中的角色，同时保留动作和场景）。

## 认证

```bash
export WAVESPEED_API_KEY="your-api-key"
```

请在 [wavespeed.ai/accesskey](https://wavespeed.ai/accesskey) 获取您的 API 密钥。

## 快速入门

### 动画模式

使图像中的角色按照驾驶视频中的主体动作进行移动：

```javascript
import wavespeed from 'wavespeed';

// Upload local image and video
const imageUrl = await wavespeed.upload("/path/to/character.png");
const videoUrl = await wavespeed.upload("/path/to/driving-video.mp4");

const output_url = (await wavespeed.run(
  "wavespeed-ai/wan-2.2/animate",
  {
    image: imageUrl,
    video: videoUrl
  }
))["outputs"][0];
```

### 替换模式

将视频中的主体替换为图像中的角色：

```javascript
const output_url = (await wavespeed.run(
  "wavespeed-ai/wan-2.2/animate",
  {
    image: imageUrl,
    video: videoUrl,
    mode: "replace"
  }
))["outputs"][0];
```

您也可以直接传递现有的视频 URL：

```javascript
const output_url = (await wavespeed.run(
  "wavespeed-ai/wan-2.2/animate",
  {
    image: "https://example.com/character.png",
    video: "https://example.com/driving-video.mp4"
  }
))["outputs"][0];
```

## API 端点

**模型 ID：** `wavespeed-ai/wan-2.2animate`

使用驾驶视频为图像中的角色添加动画效果。

### 参数

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `image` | 字符串 | 是 | -- | 需要动画处理的角色图像的 URL |
| `video` | 字符串 | 是 | -- | 提供动作参考的驾驶视频的 URL |
| `prompt` | 字符串 | 否 | -- | 用于辅助操作的文本提示 |
| `mode` | 字符串 | 否 | `animate`：图像中的角色按照视频中的主体动作移动；`replace`：将视频中的主体替换为图像中的角色 |
| `resolution` | 字符串 | 否 | `480p` | 输出分辨率（可选值：`480p`、`720p`） |
| `seed` | 整数 | 否 | `-1` | 随机种子值（-1 表示随机生成）；范围：-1 至 2147483647 |

### 示例

```javascript
import wavespeed from 'wavespeed';

const imageUrl = await wavespeed.upload("/path/to/dancer.png");
const videoUrl = await wavespeed.upload("/path/to/dance-reference.mp4");

const output_url = (await wavespeed.run(
  "wavespeed-ai/wan-2.2/animate",
  {
    image: imageUrl,
    video: videoUrl,
    prompt: "a person dancing gracefully",
    mode: "animate",
    resolution: "720p",
    seed: 42
  }
))["outputs"][0];
```

### 替换模式示例

```javascript
const characterUrl = await wavespeed.upload("/path/to/anime-character.png");
const sceneUrl = await wavespeed.upload("/path/to/scene-video.mp4");

const output_url = (await wavespeed.run(
  "wavespeed-ai/wan-2.2/animate",
  {
    image: characterUrl,
    video: sceneUrl,
    mode: "replace",
    resolution: "720p"
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

const output_url = (await client.run(
  "wavespeed-ai/wan-2.2/animate",
  {
    image: imageUrl,
    video: videoUrl,
    mode: "animate"
  }
))["outputs"][0];
```

### 使用 `runNoThrow` 进行错误处理

```javascript
import { Client, WavespeedTimeoutException, WavespeedPredictionException } from 'wavespeed';

const client = new Client();
const result = await client.runNoThrow(
  "wavespeed-ai/wan-2.2/animate",
  {
    image: imageUrl,
    video: videoUrl
  }
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

| 分辨率 | 每 5 秒的费用 |
|------------|--------------------|
| 480p | $0.20 |
| 720p | $0.40 |

输出时长为 5 至 120 秒。最低收费为 5 秒。每秒费用：480p 分辨率为 $0.04，720p 分辨率为 $0.08。

## 提示

- 为了获得最佳效果，请确保输入图像与驾驶视频的构图和姿势一致。
- 图像和视频的宽高比应相同或相似。
- 避免输入媒体中存在手部、麦克风或道具等遮挡物。
- 初期原型制作可使用 480p 分辨率，如需制作高质量内容可升级至 720p 分辨率。
- **动画模式**：适用于希望图像角色模仿视频动作的场景。
- **替换模式**：适用于希望保留视频的场景和动作，但替换为其他角色的情况。

## 安全限制

- **禁止加载任意 URL**：仅使用来自可信来源的图像和视频 URL。切勿从未经验证或用户提供的 URL 加载媒体文件。
- **API 密钥安全**：请妥善保管您的 `WAVESPEED_API_KEY`，不要将其硬编码在源代码文件中或提交到版本控制系统中。建议使用环境变量或秘密管理系统进行管理。
- **输入验证**：仅传递上述文档中规定的参数，并在发送请求前验证媒体 URL 的有效性。