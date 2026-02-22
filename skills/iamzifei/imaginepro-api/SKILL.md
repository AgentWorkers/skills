---
name: imaginepro-api
description: 通过 ImaginePro API 生成 AI 图像（支持 Midjourney、Flux、Nano Banana、Lumi Girl 等模型，以及视频格式）
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - IMAGINEPRO_API_KEY
      bins:
        - python3
        - curl
    primaryEnv: IMAGINEPRO_API_KEY
    homepage: https://platform.imaginepro.ai/ai-agent-skill
    emoji: "\U0001F3A8"
---
# ImaginePro AI 图像生成 API

使用 ImaginePro API 生成令人惊叹的 AI 图像、视频并进行编辑。该技能封装了整个 ImaginePro 后端功能，支持 5 种生成模型、图像放大、背景去除、提示优化以及视频生成。

## 快速入门

```bash
# Set your API key (get one at https://platform.imaginepro.ai/dashboard/setup)
export IMAGINEPRO_API_KEY="your-api-key-here"

# Generate an image with Flux (fastest)
python3 imaginepro_api.py wait --prompt "a cyberpunk cityscape at sunset" --model flux

# Generate with Midjourney
python3 imaginepro_api.py wait --prompt "portrait of a warrior queen, cinematic lighting --ar 2:3"

# List available models and costs
python3 imaginepro_api.py models
```

## 认证

所有请求都需要从 ImaginePro 平台控制面板获取的 Bearer 令牌：

1. 在 https://platform.imaginepro.ai 注册
2. 从 https://platform.imaginepro.ai/pricing 购买信用点数
3. 在 https://platform.imaginepro.ai/dashboard/setup 获取您的 API 密钥
4. 设置环境变量：`export IMAGINEPRO_API_KEY="your-key"`

**基础 URL：** `https://api.imaginepro.ai/api/v1`

**请求头：** `Authorization: Bearer <IMAGINEPRO_API_KEY>`

## 可用模型

| 模型 | 端点 | 信用点数 | 适用场景 |
|-------|----------|---------|----------|
| Midjourney (alpha v6) | `/midjourney/imagine` | 10（快速）/ 5（放松模式） | 艺术风格、逼真图像 |
| Flux | `/flux/imagine` | 6 | 快速通用生成 |
| Nano Banana | `/universal/imagine` | 6 | 使用参考图像和文本进行生成（试穿、模型制作、场景预览） |
| Lumi Girl | `/universal/zimage` | 6 | 人物肖像、动漫风格图像 |
| MJ Video | `/video/mj/generate` | 10 | 根据起始和结束帧生成视频 |

## API 参考

### 图像生成

#### POST `/midjourney/imagine` — Midjourney 生成

核心模型。支持在提示字符串中使用 Midjourney 的参数（例如，`--ar 16:9`、`--style raw`、`--relax`）。

**请求：**
```json
{
  "prompt": "a majestic eagle soaring over mountains --ar 16:9",
  "ref": "optional-tracking-id",
  "webhookOverride": "https://your-server.com/webhook"
}
```

- 在提示中添加 `--relax` 以使用放松模式（需要 5 个信用点数，速度较慢）。
- 支持所有标准的 Midjourney 参数：`--ar`、`--style`、`--chaos`、`--no`、`--seed`、`--q` 等。

**响应：**
```json
{
  "success": true,
  "messageId": "uuid-of-the-generation-task",
  "createdAt": "2026-01-15T12:00:00+00:00"
}
```

**信用点数：** 10（快速模式）/ 5（放松模式）

---

#### POST `/flux/imagine` — Flux 生成

快速、高质量的图像生成。支持批量生成。

**请求：**
```json
{
  "prompt": "a cozy cabin in the woods, watercolor style",
  "n": 1,
  "ref": "optional-tracking-id",
  "webhookOverride": "https://your-server.com/webhook"
}
```

- `n`（可选，默认为 1）：要生成的图像数量（信用点数乘以 n）。

**响应：**
```json
{
  "success": true,
  "messageId": "uuid-of-the-generation-task",
  "createdAt": "2026-01-15T12:00:00+00:00"
}
```

**信用点数：** 每张图像 6 个信用点数

---

#### POST `/universal/imagine` — Nano Banana（参考图像生成）

使用文本和参考图像进行多模态生成。适用于虚拟试穿、产品模型制作、室内场景预览和风格转换。

**请求：**
```json
{
  "contents": [
    { "type": "text", "text": "Image creation: woman wearing this dress in a garden" },
    { "type": "image", "url": "https://example.com/dress.jpg" }
  ],
  "model": "nano-banana-2",
  "ref": "optional-tracking-id",
  "webhookOverride": "https://your-server.com/webhook"
}
```

- `contents`：内容项数组。第一个项应为 `type: "text"`，并带有前缀 `"Image creation: "` 的提示。后续项可以是 `type: "image"`，并包含参考图像的 `url` 字段。
- `model`：必须为 `"nano-banana-2"`。
- 支持多个参考图像（例如，一个人物照片和一件服装的照片用于虚拟试穿）。

**响应：**
```json
{
  "success": true,
  "messageId": "uuid-of-the-generation-task",
  "createdAt": "2026-01-15T12:00:00+00:00"
}
```

**信用点数：** 6 个信用点数

---

#### POST `/universal/zimage` — Lumi Girl

专门用于人物肖像和风格化图像的模型。支持通过 `--ar` 在提示中设置宽高比。

**请求：**
```json
{
  "prompt": "anime girl with silver hair in a moonlit forest --ar 3:4",
  "steps": 4,
  "width": 768,
  "height": 1024,
  "ref": "optional-tracking-id",
  "webhookOverride": "https://your-server.com/webhook"
}
```

- `steps`：始终为 4（固定值）。
- `width` / `height`：每个维度最大为 1024，必须能被 8 整除。如果提示中指定了 `--ar W:H`，则尺寸会自动计算（最大尺寸为 1024）。
- 如果未指定宽高比，默认为 1024x1024。

**响应：**
```json
{
  "success": true,
  "messageId": "uuid-of-the-generation-task",
  "createdAt": "2026-01-15T12:00:00+00:00"
}
```

**信用点数：** 6 个信用点数

---

#### POST `/video/mj/generate` — MJ Video

根据起始和结束帧生成视频。

**请求：**
```json
{
  "prompt": "smooth camera pan with cinematic motion",
  "startFrameUrl": "https://example.com/start.jpg",
  "endFrameUrl": "https://example.com/end.jpg",
  "timeout": 900,
  "ref": "optional-tracking-id",
  "webhookOverride": "https://your-server.com/webhook"
}
```

- `startFrameUrl`（必需）：起始帧图像的 URL。
- `endFrameUrl`（必需）：结束帧图像的 URL。
- `prompt`（可选，默认为 "smooth motion transition"）：运动描述。
- `timeout`（可选，默认为 900）：最大处理时间（以秒为单位）。

**响应：**
```json
{
  "success": true,
  "messageId": "uuid-of-the-generation-task",
  "createdAt": "2026-01-15T12:00:00+00:00"
}
```

**信用点数：** 10 个信用点数

---

### 后处理

#### POST `/midjourney/button` — Midjourney 放大/变体生成

放大 Midjourney 生成的图像或创建其变体。

**请求：**
```json
{
  "messageId": "original-task-message-id",
  "button": "U1",
  "ref": "optional-tracking-id",
  "webhookOverride": "https://your-server.com/webhook"
}
```

- `messageId`：原始 Midjourney 生成的任务 ID。
- `button`：要执行的操作。`U1`-`U4` 用于放大图像的四个象限，`V1`-`V4` 用于生成变体。

**响应：**
```json
{
  "success": true,
  "messageId": "uuid-of-the-upscale-task",
  "createdAt": "2026-01-15T12:00:00+00:00"
}
```

**信用点数：** 5 个信用点数

---

#### POST `/flux/upscale` — Flux 放大

放大任何图像（不限于 Flux 生成的图像）。

**请求：**
```json
{
  "image": "https://example.com/image.jpg",
  "scale": 2,
  "ref": "optional-tracking-id",
  "webhookOverride": "https://your-server.com/webhook"
}
```

- `image`（必需）：要放大的图像的 URL。
- `scale`（必需）：放大倍数，必须在 2 到 4 之间（包含 2 和 4）。

**响应：**
```json
{
  "success": true,
  "messageId": "uuid-of-the-upscale-task",
  "createdAt": "2026-01-15T12:00:00+00:00"
}
```

**信用点数：** 2 个信用点数

---

#### POST `/tools/remove-bg` — 去除图像背景

去除图像的背景。

**请求：**
```json
{
  "image": "https://example.com/photo.jpg",
  "ref": "optional-tracking-id",
  "webhookOverride": "https://your-server.com/webhook"
}
```

**响应：**
```json
{
  "success": true,
  "messageId": "uuid-of-the-removebg-task",
  "createdAt": "2026-01-15T12:00:00+00:00"
}
```

**信用点数：** 5 个信用点数

---

#### POST `/tools/prompt-extend` — 提示优化（免费）

将简短的提示扩展为详细、高质量的提示。

**请求：**
```json
{
  "prompt": "a sunset"
}
```

**响应：**
```json
{
  "prompt": "a breathtaking sunset over the Pacific Ocean, golden hour light casting warm amber and coral tones across scattered cumulus clouds, silhouetted palm trees in the foreground..."
}
```

**信用点数：** 免费

---

### 状态与历史记录

#### GET `/midjourney/message/{messageId}` — 查查生成状态

通过此端点可以查看任何生成任务的进度（适用于所有模型，不仅仅是 Midjourney）。

**响应（进行中）：**
```json
{
  "prompt": "a simple red circle on white background",
  "status": "PROCESSING",
  "progress": 0,
  "messageId": "2346e0bc-c3c3-48ea-adec-3a21609fd288",
  "createdAt": "2026-02-22T07:43:37+00:00",
  "updatedAt": "2026-02-22T07:43:37+00:00"
}
```

**响应（已完成）：**
```json
{
  "prompt": "a simple red circle on white background",
  "status": "DONE",
  "images": ["https://cdn-new.imaginepro.ai/storage/v1/object/public/cdn/2346e0bc-c3c3-48ea-adec-3a21609fd288.png"],
  "uri": "https://cdn-new.imaginepro.ai/storage/v1/object/public/cdn/2346e0bc-c3c3-48ea-adec-3a21609fd288.png",
  "progress": 100,
  "messageId": "2346e0bc-c3c3-48ea-adec-3a21609fd288",
  "createdAt": "2026-02-22T07:43:37+00:00",
  "updatedAt": "2026-02-22T07:43:49+00:00"
}
```

**响应（失败）：**
```json
{
  "status": "FAIL",
  "error": "Description of what went wrong"
}
```

**状态：`SUBMITTED` → `PROCESSING` → `DONE` | `FAIL`

**信用点数：** 查看状态是免费的

---

## 异步工作流程

所有生成端点都是 **异步** 的。工作流程如下：

1. **提交** 生成请求 → 收到 `messageId`
2. 每 3-5 秒轮询一次 `GET /midjourney/message/{messageId}`
3. 等待状态变为 `DONE`（图像准备好）或 `FAIL`（出现错误）
4. 从 `uri` 或 `images` 数组中下载结果

辅助脚本 `wait` 命令会自动执行整个流程。

## 信用点数费用总结

| 操作 | 信用点数 |
|-----------|---------|
| Midjourney Imagine（快速） | 10 |
| Midjourney Imagine（放松模式） | 5 |
| Midjourney 放大/变体生成 | 5 |
| Flux Imagine | 每张图像 6 个信用点数 |
| Flux 放大 | 2 个信用点数 |
| Nano Banana Imagine | 6 个信用点数 |
| Lumi Girl Imagine | 6 个信用点数 |
| MJ Video | 10 个信用点数 |
| 背景去除 | 5 个信用点数 |
| 提示优化 | 免费 |
| 状态查询 | 免费 |

## Python 辅助脚本

随附的 `imaginepro_api.py` 是一个不依赖任何外部库的 Python 脚本（仅使用标准库）。

### 命令

```bash
# Generate an image (async — returns messageId immediately)
python3 imaginepro_api.py imagine --prompt "a sunset over mountains" --model flux

# Generate and wait for result (blocking — polls until done)
python3 imaginepro_api.py wait --prompt "a sunset over mountains" --model flux

# Check status of a generation
python3 imaginepro_api.py status --id <messageId>

# Upscale (Midjourney)
python3 imaginepro_api.py upscale --id <messageId> --button U1

# Upscale (Flux)
python3 imaginepro_api.py upscale --image "https://example.com/img.jpg" --scale 2

# Remove background
python3 imaginepro_api.py removebg --image "https://example.com/photo.jpg"

# Enhance a prompt
python3 imaginepro_api.py enhance --prompt "a cat"

# List available models
python3 imaginepro_api.py models
```

### 标志参数

- `--json` — 输出原始 JSON 格式（默认为人类可读格式）
- `--timeout <seconds>` — `wait` 命令的最大等待时间（默认：300 秒）
- `--interval <seconds>` — `wait` 命令的轮询间隔（默认：5 秒）

## curl 示例

```bash
# Generate with Flux
curl -X POST https://api.imaginepro.ai/api/v1/flux/imagine \
  -H "Authorization: Bearer $IMAGINEPRO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a cyberpunk cityscape at sunset"}'

# Check status
curl https://api.imaginepro.ai/api/v1/midjourney/message/<messageId> \
  -H "Authorization: Bearer $IMAGINEPRO_API_KEY"

# Enhance a prompt (free)
curl -X POST https://api.imaginepro.ai/api/v1/tools/prompt-extend \
  -H "Authorization: Bearer $IMAGINEPRO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a cat"}'
```

## 错误处理

API 错误会返回包含 `message`、`error` 和 `statusCode` 的 JSON 数据：

```json
{
  "message": "Prompt is required.",
  "error": "Bad Request",
  "statusCode": 400
}
```

常见错误代码：
- `400` — 缺少必需参数或参数值无效
- `401` — API 密钥无效或缺失/信用点数不足
- `404` — 未找到消息
- `500` — 服务器内部错误（稍后重试）

## 对 AI 代理的建议

1. **对于简单的生成任务，始终使用 `wait` 命令** — 它会自动处理提交和轮询流程。
2. 在进行大量批量处理之前，请在 https://platform.imaginepro.ai/dashboard 检查信用点数，以避免中途失败。没有用于检查信用点数的 API 端点。
3. 在生成之前使用 `enhance` 功能优化提示内容 — 这是免费的，并且可以显著提高图像质量。
4. Midjourney 支持在提示字符串中直接使用参数，如 `--ar 16:9 --style raw --chaos 20`。
5. 对于 Nano Banana（虚拟试穿、模型制作），请在 `contents` 数组中提供参考图像的 URL。
6. **轮询间隔**：建议使用 5 秒。不要频繁轮询（超过 3 秒）。
7. **设置超时时间**：Midjourney 的处理时间可能为 30-120 秒，视频生成可能需要长达 15 分钟。请相应地设置超时时间。