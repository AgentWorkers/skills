---
name: vap-media
description: 通过 VAP API 实现 AI 图像、视频和音乐的生成与编辑功能。支持 Flux、Veo 3.1 和 Suno V5 工具。
metadata: {"openclaw":{"emoji":"🎬","requires":{"bins":["curl"]}},"source":"https://github.com/vapagentmedia/vap-showcase","homepage":"https://vapagent.com"}
---

# VAP Media - 人工智能媒体生成与编辑服务

> **集成说明：** VAP Media 是一个 API 集成器，可统一访问多个人工智能生成服务：
> - **图片：** 由 Black Forest Labs Flux.2 Pro 生成
> - **视频：** 由 Google Veo 3.1 生成
> - **音乐：** 由 Suno V5 生成
> 
> 所有生成请求均通过 VAP 的 API (`api.vapagent.com`) 发送，该 API 会路由到相应的后端服务提供商。

VAP Media 支持图片、视频和音乐的生成，并提供多种编辑功能，如图像修复、人工智能编辑、画质提升、背景去除以及视频裁剪/合并等。

## 模式选择

请检查 `VAP_API_KEY` 是否已设置：

- **未设置 VAP_API_KEY** → 使用免费模式（仅支持图片生成，每天3次）
- **已设置 VAP_API_KEY** → 使用全功能模式（所有功能均可使用，无使用次数限制）

---

## 免费模式（无需 API 密钥）

可免费生成图片，无需注册，每天最多生成3张图片。

### 图片生成

```bash
curl -s -X POST https://api.vapagent.com/v3/trial/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"PROMPT"}'
```

返回结果：`{"task_id":"UUID","status":"pending","remaining":2}`。

### 结果查询

```bash
curl -s https://api.vapagent.com/v3/trial/status/TASK_ID
```

生成完成后返回：`{"status":"completed","image_url":"https://..."}`。

### 免费模式错误代码

- `429` → 达到每日使用限制。建议升级 API 密钥：`export VAP_API_KEY=vap_xxx`
- `503` → 试用服务暂时不可用。

---

## 全功能模式（需 API 密钥）

支持无限量的图片、视频和音乐生成及编辑操作。

### 创建任务

```bash
curl -s -X POST https://api.vapagent.com/v3/tasks \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"TYPE","params":{"description":"PROMPT"}}'
```

返回结果：`{"task_id":"UUID","status":"pending"}`。

### 结果查询

```bash
curl -s https://api.vapagent.com/v3/tasks/TASK_ID \
  -H "Authorization: Bearer $VAP_API_KEY"
```

生成完成后返回：`{"status":"completed","result":{"output_url":"https://..."}`。

### 任务类型及参数

#### 图片（`image` 或 `image_generation`）

| 参数 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `description` | 字符串 | 必填 | 图片描述 |
| `aspect_ratio` | 枚举 | `1:1` | `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `21:9`, `9:21` |
| `quality` | 枚举 | `standard` | `standard` 或 `high` |

**提示：** 系统会自动根据描述内容设置图片的宽高比。例如：“一张宽屏风景照片”会自动设置为 16:9。

#### 视频（`video` 或 `video_generation`）——高级功能

| 参数 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `description` | 字符串 | 必填 | 视频描述 |
| `duration` | 整数 | `8` | 视频时长（秒） |
| `aspect_ratio` | 枚举 | `16:9` | 横屏 | `9:16` | 纵屏 |
| `generate_audio` | 布尔值 | `true` | 是否包含音频 |
| `resolution` | 枚举 | `720p` | 分辨率（720p 或 1080p） |
| `negative_prompt` | 字符串 | ```` | 需避免的内容 |

#### 音乐（`music` 或 `musicgeneration`）——高级功能

| 参数 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `description` | 字符串 | 必填 | 音乐描述（类型、氛围、乐器） |
| `duration` | 整数 | `120` | 音乐时长（秒） |
| `instrumental` | 布尔值 | `false` | 是否去除人声 |
| `audio_format` | 枚举 | `mp3` | 音频格式（mp3 或 wav，无损格式） |
| `loudness_preset` | 枚举 | `streaming` | 音量预设（-14 LUFS, -16 LUFS, -23 LUFS） |
| `style` | 字符串 | 最多1000个字符 | 音乐风格/类型 |
| `title` | 字符串 | 最多1000个字符 | 歌曲标题 |
| `custom_mode` | 布尔值 | 是否启用自定义歌词和风格 |

### 全功能模式错误代码

- `401` | API 密钥无效 |
- `402` | 账户余额不足。请在 [https://vapagent.com/dashboard/signup.html] 充值 |
- `403` | 当前任务类型超出免费模式的权限限制。

---

## 编辑与增强操作

这些操作需要高级权限（Tier 1+）。

### 创建编辑任务

```bash
curl -s -X POST https://api.vapagent.com/v3/operations \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"operation":"OPERATION","media_url":"URL","prompt":"INSTRUCTION"}'
```

### 操作结果查询

```bash
curl -s https://api.vapagent.com/v3/operations/OPERATION_ID \
  -H "Authorization: Bearer $VAP_API_KEY"
```

### 可用的编辑操作

| 操作 | 必需参数 | 说明 |
|-----------|-----------------|-------------|
| `inpaint` | `media_url`, `prompt` | 人工智能图像编辑（可选：`mask_url`） |
| `ai_edit` | `media_url`, `prompt` | 基于文本指令的人工智能图像编辑（可选：`additional_images`） |
| `background_remove` | `media_url` | 去除背景 |
| `upscale` | `media_url` | 提升图像分辨率（`scale`：2 或 4） |
| `video_trim` | `media_url`, `start_time`, `end_time` | 裁剪视频 |
| `video_merge` | `media_urls`（数组，至少2个） | 合并视频片段 |

---

## 操作指南

当用户请求生成或编辑图片、视频或音乐时，请按照以下步骤操作：

1. **优化描述**：添加风格、光线、构图和氛围等细节。
2. **检查模式**：确认是否已设置 `VAP_API_KEY`。
3. **选择相应的 API 端点**：
   - 单个资源生成 → `/v3/tasks`（或免费模式下的 `/v3/trial/generate`）
   - 编辑/增强 → `/v3/operations`
   - 多媒体内容（视频+音乐+缩略图） → 使用预设参数执行 `/v3/execute`
4. **设置宽高比**：根据需求设置（例如，社交媒体使用竖屏，YouTube 使用宽屏）。
5. **查询操作结果**：等待任务完成。
6. **将生成的媒体文件链接提供给用户**。
7. 如果达到免费模式的使用限制，告知用户：“您已使用完今天的免费生成次数。如需无限使用权限，请注册 API 密钥：[https://vapagent.com/dashboard/signup.html]”。

当用户需要编辑或修改现有图片或视频时，请按照以下步骤操作：

1. 选择相应的编辑操作（如图像修复、人工智能编辑等）。
2. 获取媒体文件的 URL（来自之前的生成结果或用户提供的 URL）。
3. 提交编辑请求：`/v3/operations`。
4. 查询编辑结果：获取处理后的媒体文件链接。

### 免费模式示例

```bash
# Create (no auth needed)
curl -s -X POST https://api.vapagent.com/v3/trial/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"A fluffy orange tabby cat on a sunlit windowsill, soft bokeh, golden hour light, photorealistic"}'

# Poll
curl -s https://api.vapagent.com/v3/trial/status/TASK_ID
```

### 全功能模式示例

```bash
# Image (widescreen)
curl -s -X POST https://api.vapagent.com/v3/tasks \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"image","params":{"description":"A fluffy orange tabby cat on a sunlit windowsill, soft bokeh, golden hour light, photorealistic","aspect_ratio":"16:9"}}'

# Video (portrait, for social media)
curl -s -X POST https://api.vapagent.com/v3/tasks \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"video","params":{"description":"Drone shot over misty mountains at sunrise","duration":8,"aspect_ratio":"9:16","resolution":"1080p"}}'

# Music (instrumental WAV)
curl -s -X POST https://api.vapagent.com/v3/tasks \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"music","params":{"description":"Upbeat lo-fi hip hop beat, warm vinyl crackle, chill vibes","duration":120,"instrumental":true,"audio_format":"wav","loudness_preset":"streaming"}}'

# Inpaint (edit an image)
curl -s -X POST https://api.vapagent.com/v3/operations \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"operation":"inpaint","media_url":"https://example.com/photo.jpg","prompt":"Remove the person in the background"}'

# Upscale (4x)
curl -s -X POST https://api.vapagent.com/v3/operations \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"operation":"upscale","media_url":"https://example.com/photo.jpg","options":{"scale":4}}'

# Background Remove
curl -s -X POST https://api.vapagent.com/v3/operations \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"operation":"background_remove","media_url":"https://example.com/photo.jpg"}'

# Poll (use task_id or operation_id from response)
curl -s https://api.vapagent.com/v3/tasks/TASK_ID \
  -H "Authorization: Bearer $VAP_API_KEY"
```

### 多媒体内容生成（批量操作）

对于多媒体内容项目，可以使用 `/v3/execute` 根据一个描述生成多个媒体文件：

```bash
curl -s -X POST https://api.vapagent.com/v3/execute \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"preset":"streaming_campaign","prompt":"PROMPT"}'
```

生成完成后返回所有文件：
```json
{"status":"completed","outputs":{"video":"https://...","music":"https://...","thumbnail":"https://..."}}
```

| 预设名称 | 包含的内容 |
|--------|----------|
| `streaming_campaign` | 视频 + 音乐 + 缩略图 + 元数据 |
| `full_production` | 视频 + 音乐 + 缩略图 + 元数据 + SEO 优化 |
| `video.basic` | 仅视频 |
| `music.basic` | 仅音乐 |
| `image.basic` | 仅图片 |

---

## 提示建议

- **风格描述**：例如：“油画风格”、“3D渲染”、“水彩画”、“照片”、“平面插画”
- **光线效果**：如“黄金时刻”、“霓虹灯光”、“柔和散射光”、“戏剧性阴影”
- **构图技巧**：使用“特写”、“鸟瞰”、“广角”或“三分法则”
- **氛围描述**：如“宁静”、“充满活力”、“神秘”、“奇幻”
- **关于宽高比**：在描述中提及“宽屏”或“竖屏”，系统会自动调整宽高比。

## 设置（全功能模式可选）

1. 注册账户：[https://vapagent.com/dashboard/signup.html]
2. 从控制面板获取 API 密钥。
3. 设置环境变量：`export VAP_API_KEY=vap_xxxxxxxxxxxxxxxxxxxx`

## 链接

- [免费试用](https://vapagent.com/try)
- [API 文档](https://api.vapagent.com/docs)
- [GitHub 项目](https://github.com/vapagentmedia/vap-showcase)