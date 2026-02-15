---
name: monet-ai
description: >
  Monet AI – 一款用于生成视频、图片和音乐内容的人工智能 API。  
  支持多种模型，包括 Sora、Wan、Hailuo、Kling、Veo、GPT-4o、Flux、Imagen、Suno 等。
metadata:
  openclaw:
    requires:
      env:
        - MONET_API_KEY  # Required: API key from monet.vision
      bins: []
    install:
      - id: node
        kind: npm
        package: monet-ai
        label: Install monet-ai SDK (npm)
---
# Monet AI Skill

这是一个用于AI代理的内容生成API。

## 使用场景

当您需要执行以下操作时，可以使用此技能：
- 生成视频内容（Sora、Wan、Hailuo、Kling、Veo）
- 生成图像（GPT-4o、Flux、Imagen、Ideogram）
- 生成音乐（Suno、Udio）
- 将AI生成功能集成到您的代理工作流程中

## 安装

```bash
npm install monet-ai
```

## 获取API密钥

1. 访问 https://monet.vision 注册一个账户。
2. 登录后，前往 https://monet.vision/skills/keys 创建API密钥。
3. 将API密钥配置到环境变量或代码中。

如果您没有API密钥，请联系您的管理员在monet.vision上为您申请。

## 快速入门

```typescript
import { MonetAI } from "monet-ai";

const monet = new MonetAI({ 
  apiKey: process.env.MONET_API_KEY! 
});

// Create a video generation task
const task = await monet.createTask({
  type: "video",
  input: {
    model: "sora-2",
    prompt: "A cat running in the park",
    duration: 5,
    aspect_ratio: "16:9"
  }
});

// Poll for result
while (task.status === "pending" || task.status === "processing") {
  await new Promise(r => setTimeout(r, 3000));
  task = await monet.getTask(task.id);
}

console.log("Result:", task.outputs);
```

## 支持的模型

### 视频生成

#### Sora (OpenAI)

**sora-2**
```typescript
{
  model: "sora-2",
  prompt: string,                // Required
  images?: string[],             // Optional
  duration?: 10 | 15,           // Optional, default: 10
  aspect_ratio?: "16:9" | "9:16"
}
```

**sora-2-pro**
```typescript
{
  model: "sora-2-pro",
  prompt: string,
  images?: string[],
  duration?: 15 | 25,           // Optional, default: 15
  aspect_ratio?: "16:9" | "9:16"
}
```

#### Veo (Google)

**veo-3-1-fast**, **veo-3-1**
```typescript
{
  model: "veo-3-1-fast" | "veo-3-1",
  prompt: string,
  images?: string[],
  aspect_ratio?: "16:9" | "9:16"
}
```

**veo-3-fast**, **veo-3**
```typescript
{
  model: "veo-3-fast" | "veo-3",
  prompt: string,
  images?: string[],
  negative_prompt?: string
}
```

#### Wan

**wan-2-6**
```typescript
{
  model: "wan-2-6",
  prompt: string,
  images?: string[],
  duration?: 5 | 10 | 15,
  resolution?: "720p" | "1080p",
  aspect_ratio?: "16:9" | "9:16" | "4:3" | "3:4" | "1:1",
  shot_type?: "single" | "multi"
}
```

**wan-2-5**
```typescript
{
  model: "wan-2-5",
  prompt: string,
  images?: string[],
  duration?: 5 | 10,
  resolution?: "480p" | "720p" | "1080p",
  aspect_ratio?: "16:9" | "9:16" | "4:3" | "3:4" | "1:1"
}
```

**wan-2-2-flash**
```typescript
{
  model: "wan-2-2-flash",
  prompt: string,
  images?: string[],
  duration?: 5 | 10,
  resolution?: "480p" | "720p" | "1080p",
  negative_prompt?: string
}
```

**wan-2-2**
```typescript
{
  model: "wan-2-2",
  prompt: string,
  images?: string[],
  duration?: 5 | 10,
  resolution?: "480p" | "1080p",
  aspect_ratio?: "16:9" | "9:16" | "4:3" | "3:4" | "1:1",
  negative_prompt?: string
}
```

#### Kling

**kling-2-6**
```typescript
{
  model: "kling-2-6",
  prompt: string,
  images?: string[],
  duration?: 5 | 10,
  aspect_ratio?: "1:1" | "16:9" | "9:16",
  generate_audio?: boolean
}
```

**kling-2-5**
```typescript
{
  model: "kling-2-5",
  prompt: string,
  images?: string[],
  duration?: 5 | 10,
  aspect_ratio?: "1:1" | "16:9" | "9:16",
  negative_prompt?: string
}
```

**kling-v2-1-master**, **kling-v2-1**, **kling-v2**
```typescript
{
  model: "kling-v2-1-master" | "kling-v2-1" | "kling-v2",
  prompt: string,
  images?: string[],
  duration?: 5 | 10,
  aspect_ratio?: "1:1" | "16:9" | "9:16",
  strength?: number,            // 0-1
  negative_prompt?: string
}
```

#### Hailuo

**hailuo-2-3**, **hailuo-2-3-fast**
```typescript
{
  model: "hailuo-2-3" | "hailuo-2-3-fast",
  prompt: string,
  images?: string[],
  duration?: 6 | 10,
  resolution?: "768p" | "1080p"
}
```

**hailuo-02**
```typescript
{
  model: "hailuo-02",
  prompt: string,
  images?: string[],
  duration?: 6 | 10,
  resolution?: "768p" | "1080p"
}
```

**hailuo-01-live2d**, **hailuo-01**
```typescript
{
  model: "hailuo-01-live2d" | "hailuo-01",
  prompt: string,
  images?: string[]
}
```

#### Doubao Seedance

**doubao-seedance-1-5-pro**
```typescript
{
  model: "doubao-seedance-1-5-pro",
  prompt: string,
  images?: string[],
  duration?: number,
  resolution?: "480p" | "720p",
  aspect_ratio?: "1:1" | "4:3" | "16:9" | "3:4" | "9:16" | "21:9",
  generate_audio?: boolean
}
```

**doubao-seedance-1-0-pro-fast**
```typescript
{
  model: "doubao-seedance-1-0-pro-fast",
  prompt: string,
  images?: string[],
  duration?: number,
  resolution?: "720p" | "1080p",
  aspect_ratio?: "1:1" | "4:3" | "16:9" | "3:4" | "9:16" | "21:9"
}
```

**doubao-seedance-1-0-pro**
```typescript
{
  model: "doubao-seedance-1-0-pro",
  prompt: string,
  images?: string[],
  duration?: 5 | 10,
  resolution?: "480p" | "1080p",
  aspect_ratio?: "1:1" | "4:3" | "16:9" | "3:4" | "9:16"
}
```

**doubao-seedance-1-0-lite**
```typescript
{
  model: "doubao-seedance-1-0-lite",
  prompt: string,
  images?: string[],
  duration?: 5 | 10,
  resolution?: "480p" | "720p" | "1080p"
}
```

#### 特殊功能

**kling-motion-control**
```typescript
{
  model: "kling-motion-control",
  prompt: string,                // Required
  images: string[],              // Required: min 1
  videos: string[],              // Required: min 1
  resolution?: "720p" | "1080p"
}
```

**runway-act-two**
```typescript
{
  model: "runway-act-two",
  images: string[],              // Required: min 1
  videos: string[],              // Required: min 1
  aspect_ratio?: "1:1" | "4:3" | "16:9" | "3:4" | "9:16" | "21:9"
}
```

**wan-animate-mix**, **wan-animate-mix-pro**
```typescript
{
  model: "wan-animate-mix" | "wan-animate-mix-pro",
  videos: string[],              // Required
  images: string[]               // Required
}
```

**wan-animate-move**, **wan-animate-move-pro**
```typescript
{
  model: "wan-animate-move" | "wan-animate-move-pro",
  videos: string[],              // Required
  images: string[]               // Required
}
```

---

### 图像生成

#### GPT (OpenAI)

**gpt-4o**
```typescript
{
  model: "gpt-4o",
  prompt: string,
  images?: string[],
  aspect_ratio?: "1:1" | "4:3" | "3:2" | "16:9" | "3:4" | "2:3" | "9:16",
  style?: string
}
```

**gpt-image-1-5**
```typescript
{
  model: "gpt-image-1-5",
  prompt: string,
  images?: string[],             // max 10
  aspect_ratio?: "1:1" | "3:2" | "2:3",
  quality?: "auto" | "low" | "medium" | "high"
}
```

#### Nano Banana

**nano-banana-1**
```typescript
{
  model: "nano-banana-1",
  prompt: string,
  images?: string[],             // max 5
  aspect_ratio?: "1:1" | "2:3" | "3:2" | "4:3" | "3:4" | "16:9" | "9:16"
}
```

**nano-banana-2**
```typescript
{
  model: "nano-banana-2",
  prompt: string,
  images?: string[],             // max 14
  aspect_ratio?: "1:1" | "2:3" | "3:2" | "4:3" | "3:4" | "4:5" | "5:4" | "16:9" | "9:16" | "21:9",
  resolution?: "1K" | "2K" | "4K"
}
```

#### Wan

**wan-i-2-6**
```typescript
{
  model: "wan-i-2-6",
  prompt: string,
  images?: string[],             // max 4
  aspect_ratio?: "1:1" | "4:3" | "3:2" | "16:9" | "3:4" | "2:3" | "9:16" | "21:9"
}
```

**wan-2-5**
```typescript
{
  model: "wan-2-5",
  prompt: string,
  images?: string[],             // max 2
  aspect_ratio?: "1:1" | "4:3" | "3:2" | "16:9" | "3:4" | "2:3" | "9:16" | "21:9"
}
```

#### Flux

**flux-2-dev**
```typescript
{
  model: "flux-2-dev",
  prompt: string,
  aspect_ratio?: "1:1" | "4:3" | "3:2" | "16:9" | "3:4" | "2:3" | "9:16"
}
```

**flux-kontext-pro**, **flux-kontext-max**
```typescript
{
  model: "flux-kontext-pro" | "flux-kontext-max",
  prompt: string,
  images?: string[],
  aspect_ratio?: "1:1" | "4:3" | "3:2" | "16:9" | "3:4" | "2:3" | "9:16",
  style?: string
}
```

**flux-1-schnell**
```typescript
{
  model: "flux-1-schnell",
  prompt: string
}
```

#### Imagen (Google)

**imagen-3-0**, **imagen-4-0**
```typescript
{
  model: "imagen-3-0" | "imagen-4-0",
  prompt: string,
  aspect_ratio?: "1:1" | "3:4" | "4:3" | "9:16" | "16:9",
  style?: string
}
```

#### Ideogram

**ideogram-v2**, **ideogram-v3**
```typescript
{
  model: "ideogram-v2" | "ideogram-v3",
  prompt: string,
  aspect_ratio?: "1:1" | "4:3" | "3:2" | "16:9" | "3:4" | "2:3" | "9:16",
  style?: string
}
```

#### 其他

**seedream-4-0**
```typescript
{
  model: "seedream-4-0",
  prompt: string,
  images?: string[],             // max 10
  aspect_ratio?: "1:1" | "4:3" | "3:2" | "16:9" | "3:4" | "2:3" | "9:16"
}
```

**stability-1-0**
```typescript
{
  model: "stability-1-0",
  prompt: string,
  aspect_ratio?: "1:1" | "4:3" | "3:2" | "16:9" | "3:4" | "2:3" | "9:16",
  style?: string,
  negative_prompt?: string
}
```

---

### 音乐生成

**suno-3.5**, **udio-v1-6**
```typescript
{
  model: "suno-3.5" | "udio-v1-6",
  prompt: string                 // Required: music description
}
```

---

## API方法

### createTask(options)
创建一个异步任务。立即返回任务ID。

```typescript
const task = await monet.createTask({
  type: "video",
  input: { model: "sora-2", prompt: "A cat" },
  idempotency_key: "unique-key"  // Required - must be a unique value (e.g., UUID)
});
```

> ⚠️ **重要提示**：`idempotency_key` 是必需的。请使用一个唯一的值（例如UUID）以防止请求重试时创建重复的任务。

### createTaskStream(options)
创建一个支持SSE流式传输的任务。返回一个 `ReadableStream` 对象。

```typescript
const stream = await monet.createTaskStream({
  type: "video", 
  input: { model: "sora-2", prompt: "A cat" }
});
```

### getTask(taskId)
获取任务的状态和结果。

```typescript
const task = await monet.getTask("task_id");
```

### listTasks(options)
分页列出所有任务。

```typescript
const list = await monet.listTasks({ page: 1, pageSize: 20 });
```

## 配置

```typescript
const monet = new MonetAI({
  apiKey: "monet_xxx",    // Required: API key from monet.vision
  timeout: 60000          // Optional: timeout in ms
});
```

## 环境变量

```bash
MONET_API_KEY=monet_xxx
```

## curl 示例

### 创建任务

```bash
curl -X POST https://monet.vision/api/v1/tasks/async \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer monet_xxx" \
  -d '{
    "type": "video",
    "input": {
      "model": "sora-2",
      "prompt": "A cat running"
    }
  }'
```

### 获取任务信息

```bash
curl https://monet.vision/api/v1/tasks/task_id \
  -H "Authorization: Bearer monet_xxx"
```

### 列出任务

```bash
curl "https://monet.vision/api/v1/tasks/list?page=1" \
  -H "Authorization: Bearer monet_xxx"
```