---
name: freepik
version: 1.0.5
description: 使用 Freepik 的 AI API 可以生成图片、视频、图标、音频等多种内容。该 API 支持多种设计风格（如 Mystic、Flux、Kling、Hailuo、Seedream、RunWay、Magnific），并提供多种图像处理功能（如图像放大/缩小）。同时，Freepik 还提供了大量的库存素材资源，用户可以轻松搜索并使用这些素材。无论您是需要生成或编辑图片、制作视频、创建图标，还是需要处理音频文件，或者只是想搜索库存素材，Freepik 都能满足您的需求。
allowed-tools: Bash(curl *api.freepik.com*), Bash(curl **.freepik.com*), Bash(jq *), Bash(mkdir -p ~/.freepik/*)
argument-hint: "<command> [model] [--param value]"
metadata: {"openclaw":{"emoji":"🎨","primaryEnv":"FREEPIK_API_KEY","requires":{"env":["FREEPIK_API_KEY"]},"homepage":"https://github.com/SqaaSSL/freepik-openclaw-skill"}}
---
# Freepik API 功能介绍

使用 Freepik API 可以生成图片、视频、图标、音频，编辑图片以及搜索素材资源。

该 API 由 [ShellBot](https://getshell.ai) 团队开发。

## 参数说明

- **命令:** `$0` （可选值）：`generate`（生成图片）、`video`（生成视频）、`edit`（编辑图片）、`icon`（生成图标）、`audio`（生成音频）、`stock`（搜索素材）、`status`（查询任务状态）、`utility`（使用辅助工具）
- **参数 1:** `$1` （必选）：模型名称或任务 ID
- **后续参数:** `$2`, `$3` 等（根据需要添加更多参数）
- **所有参数:** 使用 `$ARGUMENTS` 来统一参数传递方式

## 会话输出

生成的文件将保存在会话文件夹中：
```bash
mkdir -p ~/.freepik/sessions/${CLAUDE_SESSION_ID}
```

下载的图片/视频/音频文件将保存在：`~/.freepik/sessions/${CLAUDE_SESSION_ID}/`

---

## 认证要求

所有请求都需要设置 `FREEPIK_API_KEY` 环境变量。

**请求头:** `x-freepik-api-key: $FREEPIK_API_KEY`

**基础 URL:** `https://api.freepik.com`

如果请求失败（返回 401/403 错误代码），请告知用户相关信息：
```
Get an API key from https://www.freepik.com/developers/dashboard/api-key
Then: export FREEPIK_API_KEY="your-key-here"
```

---

## 异步任务处理流程

大多数 AI 服务都是异步处理的。请按照以下步骤操作：

1. **提交任务**  
2. **等待任务完成**  
3. **获取结果 URL**  
4. 将结果 URL 显示给用户。该 URL 是 Freepik 的临时链接。

**重要安全规则：**
- **禁止使用 `curl` 从非 Freepik 的域名下载文件**，只能使用 `curl *api.freepik.com`。
- **禁止使用 `base64` 对本地文件进行编码**，优先使用 API 支持的 URL 参数传递方式。
- **禁止读取、编码或传输用户未提供的文件**。
- **结果 URL 直接提供给用户**，用户可以直接打开或下载文件。

**例外情况（同步操作）：**
- `remove-background`（删除背景）：`/v1/ai/beta/remove-background`
- **AI 图像分类**：`/v1/ai/classifier/image`

---

## 命令 `$0` 的详细说明

### 当 `$0 = "generate"`（生成图片）时

使用文本到图片模型生成图片。`$1` 用于指定模型。

#### 可用的模型及其特点：

| 模型名称 | 对应 API 端点 | 适用场景 |
|----------|----------|----------|
| `mystic` | `/v1/ai/mystic` | 超真实效果，支持 1K/2K/4K 分辨率，支持 LoRA 技术（Freepik 独有模型，推荐使用） |
| `flux-kontext-pro` | `/v1/ai/text-to-image/flux-kontext-pro` | 具有上下文感知功能的图片生成模型 |
| `flux-2-pro` | `/v1/ai/text-to-image/flux-2-pro` | 专业级图片生成模型，支持最多 4 张参考图片 |
| `flux-2-turbo` | `/v1/ai/text-to-image/flux-2-turbo` | 快速且经济高效的图片生成模型 |
| `flux-2-klein` | `/v1/ai/text-to-image/flux-2-klein` | 几秒内完成图片生成 |
| `flux-pro-v1-1` | `/v1/ai/text-to-image/flux-pro-v1-1` | 高质量图片生成模型 |
| `flux-dev` | `/v1/ai/text-to-image/flux-dev` | 高细节度的图片生成模型 |
| `hyperflux` | `/v1/ai/text-to-image/hyperflux` | 极速图片生成模型 |
| `seedream-v4-5` | `/v1/ai/text-to-image/seedream-v4-5` | 支持文本引导的图片编辑 |
| `seedream-v4` | `/v1/ai/text-to-image/seedream-v4` | 新一代图片生成模型 |
| `seedream-v4-edit` | `/v1/ai/text-to-image/seedream-v4-edit` | 支持多参考图片的编辑功能 |
| `seedream` | `/v1/ai/text-to-image/seedream` | 基础版本的图片生成模型 |
| `z-image` | `/v1/ai/text-to-image/z-image` | 快速生成图片，支持 LoRA 和 ControlNet 技术 |
| `runway` | `/v1/ai/text-to-image/runway` | 用于生成跑秀风格的图片 |

**默认行为：** 如果用户未指定模型，系统将使用 `mystic` 模型。

#### `mystic` 模型示例

**使用示例：**
```bash
freepik api generate --model=mystic --prompt="A beautiful landscape" --resolution=2k --num_images=3
```

**`mystic` 模型的参数说明：**
- `prompt`（字符串，必选）：生成内容的描述
- `resolution`（可选）：分辨率（"1k" | "2k" | "4k"，默认为 "2k")
- `num_images`（整数，可选）：生成图片的数量（1-4 张）
- `styling.style`（字符串，可选）：图片风格（"photo" | "digital_art" | "none"）
- `structure_reference`（对象，可选）：参考图片及其在图片中的位置（格式：`{image_url, strength: 0-100}`）
- `style_reference`（对象，可选）：参考图片及其在图片中的风格（格式：`{image_url, strength: 0-100}`）
- `loras`（数组，可选）：使用的 LoRA 模型 ID（来自 `/v1/ai/loras`）
- `seed`（整数，可选）：用于保证生成结果的稳定性

**获取可用 LoRA 模型：**
```bash
curl -s "https://api.freepik.com/v1/ai/loras" \
  -H "x-freepik-api-key: $FREEPIK_API_KEY" | jq '.data[] | {id, name, type}'
```

**自定义 LoRA 模型的训练方法：**
```bash
curl -s -X POST "https://api.freepik.com/v1/ai/loras/characters" \
  -H "x-freepik-api-key: $FREEPIK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-character", "images": ["<base64_or_url>", ...]}'
```

#### `flux-2-klein` 模型示例（几秒内完成生成）

**`flux-2-klein` 的参数说明：**
- `prompt`（字符串，必选）：生成内容的描述
- `aspect_ratio`（字符串，可选）：图片的宽高比（"square_1_1" | "widescreen_16_9" 等）
- `seed`（整数，可选）：用于保证生成结果的稳定性
- `input_image`（字符串，可选）：参考图片的 URL
- `input_image_2`（字符串，可选）：第二张参考图片的 URL
- `input_image_3`（字符串，可选）：第三张参考图片的 URL
- `safety_tolerance`（整数，可选）：生成结果的稳定性范围（0-5）
- `output_format`（字符串，可选）：输出图片的格式（"png" | "jpeg"）

#### `flux-kontext-pro` 模型示例

**`flux-kontext-pro` 的参数说明：**
- `prompt`（字符串，必选）：生成内容的描述
- `input_image`（字符串，可选）：用于生成图片的参考图片的 URL
- `prompt_upsampling`（布尔值，可选）：是否使用参考图片进行上采样
- `seed`（整数，可选）：用于保证生成结果的稳定性
- `guidance`（整数，可选）：生成过程中的指导参数（1-10）
- `steps`（整数，可选）：生成过程中的步骤数（1-100）

#### `seedream` 模型示例（适用于文本到图片和海报制作）

#### `classic-fast` 模型示例（快速图片生成）

---

### 当 `$0 = "video"`（生成视频）时

使用文本或图片生成视频。`$1` 用于指定模型。

#### 可用的模型及其特点：

| 模型名称 | 对应 API 端点 | 适用场景 |
|----------|----------|------|----------|
| `kling-v3-omni-pro` | `/v1/ai/video/kling-v3-omni-pro` | 支持多种视频格式和多帧合成，支持音频和语音 |
| `kling-v3-omni-std` | `/v1/ai/video/kling-v3-omni-std` | 标准版本的视频生成模型 |
| `kling-v3-pro` | `/v1/ai/video/kling-v3-pro` | 支持多帧合成 |
| `kling-v2-6-pro` | `/v1/ai/image-to-video/kling-v2-6-pro` | 支持视频到视频的转换 |
| `kling-v2-6-motion-pro` | `/v1/ai/video/kling-v2-6-motion-control-pro` | 支持视频中的动作合成 |
| `kling-v2-5-pro` | `/v1/ai/image-to-video/kling-v2-5-pro` | 高质量的视频生成模型 |
| `kling-v2-1-pro` | `/v1/ai/image-to-video/kling-v2-1-pro` | 高保真的视频生成模型 |
| `kling-v2-1-std` | `/v1/ai/image-to-video/kling-v2-1-std` | 标准版本的视频生成模型 |
| `kling-o1-pro` | `/v1/ai/image-to-video/kling-o1-pro` | 支持帧插值功能的视频生成模型 |
| `kling-o1-std` | `/v1/ai/image-to-video/kling-o1-std` | 标准版本的视频生成模型 |
| `kling-elements-pro` | `/v1/ai/image-to-video/kling-elements-pro` | 基于元素的视频生成模型 |
| `kling-elements-std` | `/v1/ai/image-to-video/kling-elements-std` | 标准版本的视频生成模型 |
| `hailuo-02-1080p` | `/v1/ai/image-to-video/minimax-hailuo-02-1080p` | 高质量的 1080p 视频生成模型 |
| `hailuo-02-768p` | `/v1/ai/image-to-video/minimax-hailuo-02-768p` | 768p 视频生成模型 |
| `hailuo-2-3-1080p` | `/v1/ai/image-to-video/minimax-hailuo-2-3-1080p` | 最新的 1080p 视频生成模型 |
| `hailuo-2-3-768p-fast` | `/v1/ai/image-to-video/minimax-hailuo-2-3-768p` | 快速生成的 768p 视频模型 |
| `hailuo-live` | `/v1/ai/image-to-video/minimax-live` | 动态插画的生成模型 |
| `wan-2-6-1080p` | `/v1/ai/image-to-video/wan-v2-6-1080p` | 1080p 视频生成模型 |
| `wan-2-6-720p` | `/v1/ai/image-to-video/wan-v2-6-720p` | 720p 视频生成模型 |
| `wan-2-6-t2v-1080p` | `/v1/ai/text-to-video/wan-v2-6-1080p` | 1080p 视频到视频的转换模型 |
| `wan-2-6-t2v-720p` | `/v1/ai/text-to-video/wan-v2-6-720p` | 720p 视频到视频的转换模型 |
| `wan-2-5-i2v-1080p` | `/v1/ai/image-to-video/wan-2-5-i2v-1080p` | 1080p 视频生成模型 |
| `wan-2-5-i2v-720p` | `/v1/ai/image-to-video/wan-2-5-i2v-720p` | 720p 视频生成模型 |
| `wan-2-5-t2v-480p` | `/v1/ai/text-to-video/wan-2-5-t2v-480p` | 480p 视频生成模型 |
| `wan-2-5-t2v-1080p` | `/v1/ai/text-to-video/wan-2-5-t2v-1080p` | 1080p 视频生成模型 |
| `wan-2-5-t2v-720p` | `/v1/ai/text-to-video/wan-2-5-t2v-720p` | 720p 视频生成模型 |
| `wan-2-5-t2v-480p` | `/v1/ai/text-to-video/wan-2-5-t2v-480p` | 480p 视频生成模型 |
| `runway-4-5-t2v` | `/v1/ai/text-to-video/runway-4-5` | 5/8/10 秒的视频生成模型 |
| `runway-4-5-i2v` | `/v1/ai/image-to-video/runway-4-5` | 支持多帧合成的视频生成模型 |
| `runway-gen4-turbo` | `/v1/ai/image-to-video/runway-gen4-turbo` | 快速视频生成模型 |
| `runway-act-two` | `/v1/ai/video/runway-act-two` | 用于角色表演的视频生成模型 |
| `ltx-2-pro-t2v` | `/v1/ai/text-to-video/ltx-2-pro` | 支持最高 4K 分辨率和音频的视频生成模型 |
| `ltx-2-pro-i2v` | `/v1/ai/image-to-video/ltx-2-pro` | 支持最高 4K 分辨率和音频的视频生成模型 |
| `ltx-2-fast-t2v` | `/v1/ai/text-to-video/ltx-2-fast` | 快速视频生成模型 |
| `seedance-1-5-pro-1080p` | `/v1/ai/video/seedance-1-5-pro-1080p` | 支持同步音频的视频生成模型 |
| `seedance-1-5-pro-720p` | `/v1/ai/video/seedance-1-5-pro-720p` | 720p 视频生成模型 |
| `seedance-1-5-pro-480p` | `/v1/ai/video/seedance-1-5-pro-480p` | 480p 视频生成模型 |
| `seedance-pro-1080p` | `/v1/ai/image-to-video/seedance-pro-1080p` | 1080p 视频生成模型 |
| `seedance-pro-720p` | `/v1/ai/image-to-video/seedance-pro-720p` | 720p 视频生成模型 |
| `seedance-pro-480p` | `/v1/ai/image-to-video/seedance-pro-480p` | 480p 视频生成模型 |
| `seedance-lite-1080p` | `/v1/ai/image-to-video/seedance-lite-1080p` | 轻量级的 1080p 视频生成模型 |
| `seedance-lite-720p` | `/v1/ai/image-to-video/seedance-lite-720p` | 720p 视频生成模型 |
| `seedance-lite-480p` | `/v1/ai/image-to-video/seedance-lite-480p` | 轻量级的 480p 视频生成模型 |
| `pixverse-v5` | `/v1/ai/image-to-video/pixverse-v5` | 360p 到 1080p 分辨率的稳定风格生成模型 |
| `pixverse-v5-transition` | `/v1/ai/image-to-video/pixverse-v5-transition` | 用于图片之间的过渡效果 |
| `omnihuman-1-5` | `/v1/ai/video/omni-human-1-5` | 通过音频生成人物动画 |
| `vfx` | `/v1/ai/video/vfx` | 用于视频效果的添加 |
| `ref-kling-v3-omni-pro` | `/v1/ai/reference-to-video/kling-v3-omni-pro` | 使用参考视频进行视频转换 |
| `ref-kling-v3-omni-std` | `/v1/ai/reference-to-video/kling-v3-omni-std` | 标准版本的视频转换模型 |

**默认行为：** 如果用户未指定模型，系统将使用 `kling-v3-omni-pro` 模型。

---

## 其他命令说明

- **`$0 = "edit"`（编辑图片）**：用于编辑、增强和转换图片。
- **`$0 = "icon"`（生成图标）**：根据文本描述生成 PNG 或 SVG 格式的图标。
- **$0 = "audio"`（生成音频）**：用于生成音乐、音效或提取音频片段。
- **$0 = "stock"`（搜索素材）**：用于搜索和下载图片、矢量图、图标或视频素材。
- **$0 = "status"`（查询任务状态）**：用于查看异步任务的状态。

---

## 常见任务路径示例

- 查看任务状态：`mystic/<task-id>`
- 生成图片：`text-to-image/<model>/<task-id>`
- 生成视频：`video/kling-v3-omni/<task-id>`
- 图标生成：`text-to-icon/<task-id>`
- 音乐生成：`music-generation/<task-id>`
- 音效生成：`sound-effects/<task-id>`
- 图像编辑：`upscale-creative/<task-id>` 或其他相关端点