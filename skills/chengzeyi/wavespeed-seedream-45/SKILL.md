---
name: wavespeed-seedream-45
description: 使用 ByteDance 的 Seedream V4.5 模型以及 WaveSpeed AI 生成和编辑图像。支持文本到图像的转换，以及多图像编辑，自定义分辨率最高可达 4096x4096。该工具具备改进后的排版功能，适用于海报和标志的制作。适用于需要创建或编辑具有高质量文本渲染效果的图像的用户。
metadata:
  author: wavespeedai
  version: "1.0"
---
# WaveSpeedAI Seedream V4.5 图像生成/编辑

通过 WaveSpeed AI 平台，使用字节跳动的 Seedream V4.5 模型生成和编辑图像。支持高达 4096x4096 的自定义分辨率，并提供增强型的文字渲染功能，适用于海报和标志等场景。

## 认证

```bash
export WAVESPEED_API_KEY="your-api-key"
```

请在 [wavespeed.ai/accesskey](https://wavespeed.ai/accesskey) 获取您的 API 密钥。

## 快速入门

### 文本转图像

```javascript
import wavespeed from 'wavespeed';

const output_url = (await wavespeed.run(
  "bytedance/seedream-v4.5",
  { prompt: "A minimalist coffee shop logo with clean typography" }
))["outputs"][0];
```

### 图像编辑

`images` 参数接受一个图像 URL 数组（1-10 张图像）。如果您有本地文件，可以先使用 `wavespeed.upload()` 将它们上传以获取对应的 URL。

```javascript
import wavespeed from 'wavespeed';

// Upload a local image to get a URL
const imageUrl = await wavespeed.upload("/path/to/photo.png");

const output_url = (await wavespeed.run(
  "bytedance/seedream-v4.5/edit",
  {
    images: [imageUrl],
    prompt: "Add warm sunset lighting and lens flare"
  }
))["outputs"][0];
```

您也可以直接传递现有的图像 URL：

```javascript
const output_url = (await wavespeed.run(
  "bytedance/seedream-v4.5/edit",
  {
    images: ["https://example.com/photo.jpg"],
    prompt: "Add warm sunset lighting and lens flare"
  }
))["outputs"][0];
```

## API 端点

### 文本转图像

**模型 ID：** `bytedance/seedream-v4.5`

根据文本提示生成图像，支持高达 4096x4096 的自定义分辨率。

#### 参数

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|-----------|------|----------|---------|-------------|
| `prompt` | 字符串 | 是 | -- | 要生成的图像的文字描述 |
| `size` | 字符串 | 否 | `2048*2048` | 输出图像的尺寸（像素，格式为 `WIDTH*HEIGHT`），每个维度范围为 1024-4096。 |

#### 示例

```javascript
import wavespeed from 'wavespeed';

const output_url = (await wavespeed.run(
  "bytedance/seedream-v4.5",
  {
    prompt: "A movie poster for a sci-fi thriller with bold title text 'HORIZON' at the top",
    size: "2048*3072"
  }
))["outputs"][0];
```

### 图像编辑

**模型 ID：** `bytedance/seedream-v4.5/edit`

使用文本提示编辑现有图像。支持最多 10 张输入图像。编辑过程中会保留输入图像中的面部特征、光照效果和色彩色调。

#### 参数

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|-----------|------|----------|---------|-------------|
| `images` | 字符串数组 | 是 | `[]` | 要编辑的输入图像的 URL（1-10 张图像）。这些图像必须可公开访问。 |
| `prompt` | 字符串 | 是 | -- | 所需编辑的文字描述 |
| `size` | 字符串 | 否 | -- | 输出图像的尺寸（像素，格式为 `WIDTH*HEIGHT`），每个维度范围为 1024-4096。 |

#### 示例

```javascript
import wavespeed from 'wavespeed';

const imageUrl = await wavespeed.upload("/path/to/portrait.png");

const output_url = (await wavespeed.run(
  "bytedance/seedream-v4.5/edit",
  {
    images: [imageUrl],
    prompt: "Transform into a vibrant pop art style with bold colors",
    size: "2048*2048"
  }
))["outputs"][0];
```

#### 多图像编辑

```javascript
const img1 = await wavespeed.upload("/path/to/face.png");
const img2 = await wavespeed.upload("/path/to/scene.png");

const output_url = (await wavespeed.run(
  "bytedance/seedream-v4.5/edit",
  {
    images: [img1, img2],
    prompt: "Place the person from the first image into the scene from the second image"
  }
))["outputs"][0];
```

## 高级用法

### 同步模式

```javascript
const output_url = (await wavespeed.run(
  "bytedance/seedream-v4.5",
  { prompt: "A watercolor painting of a mountain lake at dawn" },
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
  "bytedance/seedream-v4.5",
  { prompt: "A neon sign that reads 'OPEN 24/7' in a rainy alley" }
))["outputs"][0];
```

### 使用 `runNoThrow` 进行错误处理

```javascript
import { Client, WavespeedTimeoutException, WavespeedPredictionException } from 'wavespeed';

const client = new Client();
const result = await client.runNoThrow(
  "bytedance/seedream-v4.5",
  { prompt: "A vintage travel poster for Tokyo" }
);

if (result.outputs) {
  console.log("Image URL:", result.outputs[0]);
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

每张图像的费用为 0.04 美元（包括生成和编辑服务）。

## 提示

- Seedream V4.5 在图像中的文本渲染方面表现优异，非常适合用于海报、标志和品牌视觉素材的创建。
- 支持高达 4096x4096 的自定义分辨率，可通过 `WIDTH*HEIGHT` 指定尺寸（例如，`2048*3072` 适用于竖版海报）。
- 在图像编辑过程中，模型会保留输入图像中的面部特征、光照效果和色彩色调。

## 安全限制

- **禁止加载任意 URL**：仅使用来自可信来源的图像 URL。切勿从未经验证或用户提供的 URL 加载图像。
- **API 密钥安全**：请妥善保管您的 `WAVESPEED_API_KEY`，不要将其硬编码在源文件中或提交到版本控制系统中。建议使用环境变量或秘密管理系统进行管理。
- **输入验证**：仅传递上述文档中规定的参数。在发送请求之前，请验证提示内容和图像 URL 的有效性。