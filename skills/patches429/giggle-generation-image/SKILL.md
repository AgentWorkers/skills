---
name: giggle-generation-image
description: Supports text-to-image and image-to-image. Use when the user needs to create or generate images. Use cases: (1) Generate from text description, (2) Use reference images, (3) Customize model, aspect ratio, resolution. Triggers: generate image, draw, create image, AI art.
version: "0.0.4"
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "📂",
        "requires": { "bins": ["python3"], "env": ["GIGGLE_API_KEY"] },
        "primaryEnv": "GIGGLE_API_KEY",
      },
  }
---

# Giggle 图像生成（多模型支持）

通过 giggle.pro 的 Generation API 生成 AI 图像，支持多种模型。

**API 密钥**：优先从以下位置加载：1) `~/.openclaw/.env`（推荐）；2) 系统环境变量 `GIGGLE_API_KEY`。如果未配置，脚本会提示用户输入。

> **注意**：所有命令必须通过 `exec` 工具执行，**严禁** 使用 `python3 << 'EOF'` 或内联代码的形式。

## 支持的模型

| 模型 | 描述 |
|-------|-------------|
| seedream45 | 具有现实感和创意性的图像生成模型 |
| midjourney | Midjourney 风格的图像生成模型 |
| nano-banana-2 | Nano Banana 2 模型 |
| nano-banana-2-fast | Nano Banana 2 的快速生成版本 |

---

## 执行流程（三阶段双路径）

图像生成通常需要 30–120 秒。该流程采用“快速提交 + 定时轮询 + 同步回退”的三阶段架构。

> **重要提示**：**严禁** 将 `GIGGLE_API_KEY` 作为参数传递给 `exec` 的 `env` 参数。API 密钥会从 `~/.openclaw/.env` 或系统环境变量中读取。

---

### 第一阶段：提交任务（执行时间约 10 秒）

**首先向用户发送提示信息**：“图像生成中，通常需要 30–120 秒。结果会自动发送给您。”

```bash
# Text-to-image (default seedream45)
python3 scripts/generation_api.py \
  --prompt "description" --aspect-ratio 16:9 \
  --model seedream45 --resolution 2K \
  --no-wait --json

# Text-to-image - Midjourney
python3 scripts/generation_api.py \
  --prompt "description" --model midjourney \
  --aspect-ratio 16:9 --resolution 2K \
  --no-wait --json

# Image-to-image - Reference URL
python3 scripts/generation_api.py \
  --prompt "Convert to oil painting style, keep composition" \
  --reference-images "https://example.com/photo.jpg" \
  --model nano-banana-2-fast \
  --no-wait --json

# Batch generate multiple images
python3 scripts/generation_api.py \
  --prompt "description" --generate-count 4 \
  --no-wait --json
```

**示例响应信息**：
```json
{"status": "started", "task_id": "xxx"}
```

**立即将任务 ID 存储在内存中**（使用 `addMemory` 函数）：
```
giggle-generation-image task_id: xxx (submitted: YYYY-MM-DD HH:mm)
```

---

### 第二阶段：注册定时任务（间隔 45 秒）

使用 `cron` 工具注册定时任务。**请严格遵循参数格式**：

```json
{
  "action": "add",
  "job": {
    "name": "giggle-generation-image-<first 8 chars of task_id>",
    "schedule": {
      "kind": "every",
      "everyMs": 45000
    },
    "payload": {
      "kind": "systemEvent",
      "text": "Image task poll: exec python3 scripts/generation_api.py --query --task-id <full task_id>, handle stdout per Cron logic. If stdout is non-JSON plain text, forward to user and remove Cron. If stdout is JSON, do not send message, keep waiting. If stdout is empty, remove Cron immediately."
    },
    "sessionTarget": "main"
  }
}
```

**定时任务触发逻辑**（根据 `exec` 的输出结果判断）：

| `exec` 的输出内容 | 处理方式 |
|----------------|--------|
| 非空纯文本（不以 `{` 开头） | **原样发送给用户**，**删除定时任务** |
| 输出为空 | 图像已生成，**立即删除定时任务**，**无需发送通知** |
| JSON 格式（以 `{` 开头且包含 `"status"` 字段） | **无需发送通知**，**保持定时任务运行** |

---

### 第三阶段：同步等待（定时任务未触发时的备用方案）

无论定时任务是否成功注册，都需要执行此阶段。

```bash
python3 scripts/generation_api.py --query --task-id <task_id> --poll --max-wait 180
```

**处理逻辑**：
- 如果输出为纯文本（表示图像生成完成或失败），**原样发送给用户**，并删除定时任务；
- 如果输出为空，说明图像已生成，**立即删除定时任务**，**无需发送通知**；
- 如果 `exec` 超时，**继续执行定时任务**。

---

## 新请求与旧任务的处理

**当用户发起新的图像生成请求时**，**必须重新执行第一阶段以提交新任务**，切勿重复使用内存中的旧任务 ID。

**只有当用户明确询问旧任务的进度时**，才需要从内存中查询旧任务 ID。

---

## 参数说明

| 参数 | 默认值 | 说明 |
|-----------|---------|-------------|
| `--prompt` | 必填 | 图像生成的描述性提示 |
| `--model` | seedream45 | 可选模型：seedream45, midjourney, nano-banana-2, nano-banana-2-fast |
| `--aspect-ratio` | 16:9 | 图像宽高比 |
| `--resolution` | 2K | 图像分辨率（文本转图像：1K, 2K, 4K；图像转图像：部分支持） |
| `--generate-count` | 1 | 生成图像的数量 |
| `--reference-images` | - | 图像转图像时的参考图像；支持 URL、Base64 编码或 asset_id 格式 |
| `--watermark` | false | 是否添加水印（仅适用于图像转图像的情况） |

---

## 图像转图像的参考图像格式

`reference_images` 参数是一个对象数组，每个元素可以是以下三种格式之一（可以混合使用）：

### 方法 1：URL

```json
{
  "prompt": "A cute orange cat sitting on the windowsill in the sun, realistic style",
  "reference_images": [
    {
      "url": "https://assets.ggltest.com/private/test_ai_director/0ebc2ffa7512a58df5/9y91pxl0hju.thumb.jpg?Expires=1772409599000&Key-Pair-Id=K271ZF3SQS38SK&Signature=..."
    }
  ],
  "generate_count": 1,
  "model": "nano-banana-2-fast",
  "aspect_ratio": "16:9",
  "watermark": false
}
```

### 方法 2：Base64 编码

```json
{
  "prompt": "A cute orange cat sitting on the windowsill in the sun, realistic style",
  "reference_images": [
    {
      "base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    }
  ],
  "generate_count": 1,
  "model": "nano-banana-2-fast",
  "aspect_ratio": "16:9",
  "watermark": false
}
```

> 使用原始的 Base64 字符串，**不要添加 `data:image/xxx;base64,` 前缀**。

### 方法 3：asset_id

```json
{
  "prompt": "A cute orange cat sitting on the windowsill in the sun, realistic style",
  "reference_images": [
    {
      "asset_id": "vvsdsfsdf"
    }
  ],
  "generate_count": 1,
  "model": "nano-banana-2-fast",
  "aspect_ratio": "16:9",
  "watermark": false
}
```

> 如果有多个参考图像，只需将它们添加到 `reference_images` 数组中即可。

---

## 用户交互指南

**如果用户提供的信息不完整，请按照以下步骤引导用户**；如果信息齐全，可以直接执行命令。

### 第一步：选择模型

```
Question: "Which model would you like to use?"
Title: "Image Model"
Options:
- "seedream45 - Realistic & creative (recommended)"
- "midjourney - Artistic style"
- "nano-banana-2 - High quality"
- "nano-banana-2-fast - Fast generation"
multiSelect: false
```

### 第二步：设置宽高比

```
Question: "What aspect ratio do you need?"
Title: "Aspect Ratio"
Options:
- "16:9 - Landscape (wallpaper/cover) (recommended)"
- "9:16 - Portrait (mobile)"
- "1:1 - Square"
- "Other ratios"
multiSelect: false
```

### 第三步：选择生成模式

```
Question: "Do you need reference images?"
Title: "Generation Mode"
Options:
- "No - Text-to-image only"
- "Yes - Image-to-image (style transfer)"
multiSelect: false
```

### 第四步：执行并显示结果

按照以下流程操作：发送提示信息 → 提交任务 → 注册定时任务 → 等待结果。

结果返回时，将 `exec` 的输出内容原样发送给用户。

**链接格式要求**：返回的图像链接必须是 **完整的签名 URL**（包含 Policy、Key-Pair-Id 和 Signature 参数）。正确格式示例：`https://assets.giggle.pro/...?Policy=...&Key-Pair-Id=...&Signature=...`。错误格式：不要返回仅包含基础路径的未签名链接（缺少查询参数）。