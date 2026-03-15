---
name: nano-banana-image-gen
description: 使用 Pixwith API 的 Nano Banana 2 模型生成和编辑图像。该模型支持文本到图像以及图像到图像的转换（最多可参考 4 张图片）。适用于用户需要生成图像、编辑照片、创作 AI 艺术作品，或进行文本到图像/图像到图像转换的场景。
  Generate and edit images using Pixwith API's Nano Banana 2 model.
  Supports text-to-image and image-to-image (up to 4 reference images).
  Use when the user asks to generate images, edit photos, create AI art,
  text-to-image, or image-to-image with Nano Banana 2.
version: 1.0.1
publisher: Pixwith AI
homepage: https://pixwith.ai
categories:
  - image-generation
  - image-editing

tags:
  - pixwith
  - nano-banana
  - image-generation
  - text-to-image
  - image-to-image

env:
  PIXWITH_API_KEY:
    required: true
    description: Pixwith API key used to authenticate API requests.

permissions:
  network:
    domains:
      - api.pixwith.ai
      - uploads.pixwith.ai
      - "*.amazonaws.com"

  filesystem:
    access: user-provided
    description: >
      May read image files explicitly provided by the user for upload
      when performing image generation or editing tasks.

  persistence:
    modify_agent_config: false
    write_files: false
    
capabilities:
  - check_credits
  - text_to_image
  - image_to_image
  - image_upload
  - task_creation
  - task_status_polling
---
# Pixwith Nano Banana 2 — AI 图像生成

通过 Pixwith API 使用 Nano Banana 2 模型生成和编辑图像。支持文本到图像以及图像到图像的转换，最多可使用 4 张参考图像，支持多种分辨率（1K / 2K / 4K）和灵活的宽高比。

## ⚠️ 重要提示：**请勿更改 API 响应值**

API 返回的所有值（`task_id`、`result_urls`、`image_url`、`upload_url`、`fields`）都是不可修改的令牌。请严格按照返回的内容使用这些值，不得添加、删除或更改任何字符。将每个值存储在 shell 变量中并直接使用。`task_id` 或 `result_urls` 中的任何一个字符错误都可能导致错误或链接失效。

## 设置

此功能需要一个名为 `PIXWITH_API_KEY` 的环境变量。

**如果该变量未设置，请指导用户按照以下步骤操作：**

1. 访问 https://pixwith.ai/api 并注册/登录。
2. 点击“添加”创建新的 API 密钥并复制它。
3. 将密钥添加到 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "skills": {
    "entries": {
      "nano-banana-image-gen": {
        "enabled": true,
        "env": { "PIXWITH_API_KEY": "key_your_key_here" }
      }
    }
  }
}
```

**验证**方法如下：

```bash
curl -s -X POST https://api.pixwith.ai/api/task/get_credits \
  -H "Content-Type: application/json" \
  -H "Api-Key: $PIXWITH_API_KEY"
```

成功的响应格式为 `{"code": 1, "data": {"credits": 500}}`。

## 价格

| 分辨率 | 每张图片的 Credits 数量 |
|------------|-------------------|
| 1K         | 10                |
| 2K         | 15                |
| 4K         | 20                |

在创建任务之前，请务必告知用户相关费用。

## 模型参数

- **model_id**：`0-41`（固定值）
- **prompt**（必填）：描述要生成的图像或要应用的编辑内容。
- **image_urls**（可选）：图像到图像模式时使用的 1–4 张公开可访问的图像 URL。
- **options.prompt_optimization**（布尔值，默认为 `true`）：自动将提示翻译成英文。
- **options.resolution**（必填）：`1K`、`2K` 或 `4K`。
- **options.aspect_ratio**（必填）：`0`（自动匹配输入图像的尺寸）、`1:1`、`16:9`、`9:16`、`3:4`、`4:3`、`3:2`、`2:3`、`5:4`、`4:5`、`21:9`。

## 工作流程 A — 文本到图像

当用户仅提供文本提示而没有图像时使用此流程。

### 第 1 步：检查 Credits 数量

```bash
curl -s -X POST https://api.pixwith.ai/api/task/get_credits \
  -H "Content-Type: application/json" \
  -H "Api-Key: $PIXWITH_API_KEY"
```

验证 `data.credits` 是否足够用于所选分辨率。

### 第 2 步：创建任务

```bash
curl -s -X POST https://api.pixwith.ai/api/task/create \
  -H "Content-Type: application/json" \
  -H "Api-Key: $PIXWITH_API_KEY" \
  -d '{
    "prompt": "<user_prompt>",
    "model_id": "0-41",
    "options": {
      "prompt_optimization": true,
      "resolution": "1K",
      "aspect_ratio": "1:1"
    }
  }'
```

响应中包含 `data.task_id` 和 `data.estimated_time`（以秒为单位）。

### 第 3 步：等待结果

等待 `estimated_time` 秒后，再次检查：

```bash
curl -s -X POST https://api.pixwith.ai/api/task/get \
  -H "Content-Type: application/json" \
  -H "Api-Key: $PIXWITH_API_KEY" \
  -d '{"task_id": "<task_id>"}'
```

- 如果 `data.status` 为 `1`，表示仍在处理中，等待 5 秒后再次检查。
- 如果 `data.status` 为 `2`，表示任务已完成，`data.result_urls` 中包含图像 URL。
- 如果 `data.status` 为 `3`，表示任务失败，请通知用户。

将 `result_urls` 的确切值展示给用户。

## 工作流程 B — 图像到图像

当用户提供一张或多张参考图像以及文本提示时使用此流程。

### 第 1 步：上传本地图像（如需要）

如果用户提供了本地文件路径（而非公共 URL），请先上传文件。

**上传要求：**

- 允许的格式：仅限 `.jpg`、`.jpeg`、`.png`
- 文件大小上限：**10 MB**
- `content_type` 必须与文件格式匹配：`.jpg`/`.jpeg` 为 `image/jpeg`，`.png` 为 `image/png`
- 预签的上传 URL 在 **10 分钟** 后失效

**1a. 获取预签的上传 URL：**

```bash
curl -s -X POST https://api.pixwith.ai/api/task/pre_url \
  -H "Content-Type: application/json" \
  -H "Api-Key: $PIXWITH_API_KEY" \
  -d '{"image_name": "photo.jpg", "content_type": "image/jpeg"}'
```

根据文件扩展名设置 `content_type`：
- `.jpg` / `.jpeg` → `"image/jpeg"`
- `.png` → `"image/png"`

响应内容：
- `data.upload_url` — 预签的 POST 数据（`url` + `fields`）
- `data.image_url` — 最终的 CDN URL，用于 `image_urls`

**1b. 使用预签数据上传文件：**

```bash
curl -s -X POST "<upload_url.url>" \
  -F "key=<upload_url.fields.key>" \
  -F "Content-Type=<upload_url.fields.Content-Type>" \
  -F "x-amz-credential=<upload_url.fields.x-amz-credential>" \
  -F "x-amz-algorithm=<upload_url.fields.x-amz-algorithm>" \
  -F "x-amz-date=<upload_url.fields.x-amz-date>" \
  -F "x-amz-signature=<upload_url.fields.x-amz-signature>" \
  -F "policy=<upload_url.fields.policy>" \
  -F "file=@/path/to/local/image.jpg"
```

将 `upload_url.fields` 对象中的所有字段填写到表单中。
上传完成后，使用步骤 1a 中的 `data.image_url` 作为图像 URL。

如果用户已有公共图像 URL（以 `http` 开头），则跳过此步骤。

### 第 2 步：检查 Credits 数量

与工作流程 A 的第 1 步相同。

### 第 3 步：使用图像创建任务

```bash
curl -s -X POST https://api.pixwith.ai/api/task/create \
  -H "Content-Type: application/json" \
  -H "Api-Key: $PIXWITH_API_KEY" \
  -d '{
    "prompt": "<edit_instruction>",
    "image_urls": ["<image_url_1>", "<image_url_2>"],
    "model_id": "0-41",
    "options": {
      "prompt_optimization": true,
      "resolution": "1K",
      "aspect_ratio": "0"
    }
  }'
```

在编辑图像时，`aspect_ratio: "0"` 会自动匹配输入图像的尺寸。

### 第 4 步：等待结果

与工作流程 A 的第 3 步相同。

## 错误处理

所有 API 响应遵循 `{"code": 1, "message": "success", "data": {...}}` 的格式。
当 `code` 为 `0` 时，`message` 中会包含错误信息。常见错误包括：
- **无效的 API 密钥** — 密钥缺失、错误或已被禁用。
- **Credits 不足** — 用户需要访问 https://pixwith.ai/pricing 购买更多 Credits。
- **无效的图像格式** — 仅支持 jpg、png、jpeg 格式。
- **无效的图像 URL** — URL 不可公开访问。

## 默认值

当用户未指定偏好设置时，使用以下默认值：

- 分辨率：`1K`
- 宽高比：`1:1`（文本到图像）或 `0`（图像到图像）
- `prompt_optimization`：`true`