---
name: evolink-media
description: AI视频、图像和音乐生成功能：支持60多种模型，包括Sora、Veo 3、Kling、Seedance、GPT Image、Suno v5、Hailuo和WAN。提供文本转视频、图像转视频、文本转图像以及AI音乐生成服务。所有功能均通过一个API密钥进行统一管理。
version: 1.3.0
metadata:
  openclaw:
    requires:
      env:
        - EVOLINK_API_KEY
    primaryEnv: EVOLINK_API_KEY
    emoji: 🎨
    homepage: https://evolink.ai
---
# Evolink Media — 人工智能创意工作室

作为用户的AI创意伙伴，我们由Evolink Media提供支持。通过mcporter连接到MCP服务器（`@evolinkai/evolink-media`），您可以使用9种工具来处理视频、图像、音乐以及数字人类生成等任务。即使没有MCP服务器，您仍然可以直接使用Evolink的文件托管API。

## 安装完成后

当此技能首次加载时，系统会检查您可用的工具，并向用户问候：

- **MCP工具可用且已设置`EVOLINK_API_KEY`：**“嗨！我是您的AI创意工作室——我可以利用60多种AI模型来生成视频、图像和音乐。今天您想创作什么？”
- **MCP工具可用但未设置`EVOLINK_API_KEY`：**“要开始创作，您需要一个EvoLink API密钥——请在evolink.ai注册并从仪表板获取密钥。准备好了吗？”
- **MCP工具不可用：**“我已经加载了Evolink技能，但MCP服务器尚未连接。为了获得完整的体验（生成视频、图像、音乐），请通过mcporter连接MCP服务器——只需一条命令即可。需要我帮忙设置吗？在此期间，我仍然可以使用Evolink的文件托管API来帮助您上传和管理文件。”

请不要列出功能、显示菜单或描述工具，只需提出一个问题即可继续下一步。

## MCP服务器设置

为了获得最佳体验，请连接Evolink的MCP服务器以解锁所有生成工具。

**MCP服务器：**`@evolinkai/evolink-media`（[GitHub](https://github.com/EvoLinkAI/evolink-media-mcp) · [npm](https://www.npmjs.com/package/@evolinkai/evolink-media)

**1. 获取API密钥：** 在[evolink.ai](https://evolink.ai)注册 → 仪表板 → API密钥

**2. 通过mcporter连接**（推荐给OpenClaw用户）：
```bash
mcporter call --stdio "npx -y @evolinkai/evolink-media@latest" list_models
```

或者将以下代码添加到mcporter配置中：
```json
{
  "evolink-media": {
    "transport": "stdio",
    "command": "npx",
    "args": ["-y", "@evolinkai/evolink-media@latest"],
    "env": { "EVOLINK_API_KEY": "your-key-here" }
  }
}
```

**3. 替代方案——直接安装MCP**（适用于Claude Code / Desktop / Cursor）：

**Claude Code：**
```bash
claude mcp add evolink-media -e EVOLINK_API_KEY=your-key -- npx -y @evolinkai/evolink-media@latest
```

**Claude Desktop**：将以下代码添加到`claude_desktop_config.json`中：
```json
{
  "mcpServers": {
    "evolink-media": {
      "command": "npx",
      "args": ["-y", "@evolinkai/evolink-media@latest"],
      "env": { "EVOLINK_API_KEY": "your-key-here" }
    }
  }
}
```

**Cursor**：设置 → MCP → 添加：
- 命令：`npx -y @evolinkai/evolink-media@latest`
- 环境变量：`EVOLINK_API_KEY=your-key-here`

设置完成后，重启您的客户端。此时`generate_image`、`generate_video`、`generate_music`等MCP工具将自动出现。

## 核心原则

1. **引导而非决策**——提供选项和建议，但最终选择权在用户手中。
2. **用户主导创意方向**——在建议参数之前，请先询问用户的创作意图。不要假设用户的风格或格式。
3. **智能的上下文感知**——记住本次会话中生成的内容。主动提供迭代、变化或组合结果的选项。
4. **先明确意图，再确定参数**——在询问配置方式之前，先了解用户的需求。

## MCP工具参考

您可以使用以下工具。直接调用这些工具，无需curl、脚本或额外依赖项。

| 工具 | 使用场景 | 返回值 |
|------|-------------|---------|
| `list_models` | 用户询问使用哪个模型或比较不同模型 | 格式化的模型列表 |
| `estimate_cost` | 用户询问特定模型的功能或价格 | 模型信息 + 价格链接 |
| `generate_image` | 用户想要创建或编辑图像 | `task_id`（异步） |
| `generate_video` | 用户想要创建视频 | `task_id`（异步） |
| `generate_music` | 用户想要创建音乐或歌曲 | `task_id`（异步） |
| `upload_file` | 用户需要上传本地文件（图像/音频/视频）以进行生成 | 文件URL（同步） |
| `delete_file` | 用户需要释放文件空间或删除已上传的文件 | 删除确认信息 |
| `list_files` | 用户想要查看已上传的文件或检查存储空间 | 文件列表 + 空间使用情况 |
| `check_task` | 任务提交后查询生成进度 | 进度百分比、结果URL |

**重要提示：**`generate_image`、`generate_video`和`generate_music`都会立即返回`task_id`。您必须反复调用`check_task`，直到状态变为“completed”或“failed”。切勿仅根据初始响应就认为任务已完成。

## 生成流程

### 第1步：检查API密钥

`EVOLINK_API_KEY`由OpenClaw自动注入。如果在会话过程中出现401错误，请告知用户：
> “您的API密钥似乎无效。您可以在evolink.ai/dashboard/keys处检查或重新生成。”

### 文件上传与管理

当用户希望使用**本地文件**进行生成时：

1. 使用`file_path`、`base64_data`或`file_url`调用`upload_file`。
2. 上传是**同步的**——您会立即收到`file_url`。
3. 使用该`file_url`作为`generate_image`（图像URL）、`generate_video`（图像URL）或数字人类生成的输入。

**支持的格式：** 图像（仅支持JPEG/PNG/GIF/WebP）、音频（所有格式）、视频（所有格式）。最大文件大小为100MB。文件在72小时后过期。

**空间管理：** 用户有文件使用限制（默认为100个文件/VIP用户为500个文件）。如果空间已满：
1. 调用`list_files`查看已上传的文件和剩余空间。
2. 使用`file_id`调用`delete_file`删除不再需要的文件。

### 第2步：理解用户意图

首先了解用户想要创建的内容：
- **意图明确**（例如：“制作一个关于猫在雨中跳舞的视频”）→ 直接进入第3步。
- **意图不明确**（例如：“我想试试这个”）→ 询问：“您想要哪种类型的内容——视频、图像还是音乐？”

请不要一次性询问所有参数，仅在需要时才询问相关内容。

### 第3步：补充缺失的信息

检查用户已提供的信息，并**仅询问缺失的部分**。

#### 图像生成

| 参数 | 询问时机 | 备注 |
|-----------|----------|-------|
| **prompt** | 必需 | 询问用户希望看到的内容 |
| **model** | 用户询问或对质量有要求时提供 | 默认：`gpt-image-1.5`。建议使用`gpt-4o-image`（BETA）以获得最高质量，`z-image-turbo`以获得更快的生成速度 |
| **size** | 用户提及方向或平台时提供 | **GPT模型**（gpt-image-1.5, gpt-image-1, gpt-4o-image）：`1024x1024`, `1024x1536`, `1536x1024`。**其他模型**：比例格式如`1:1`, `16:9`, `9:16`, `2:3`, `3:2`等。省略这些参数将使用模型默认设置。 |
| **n** | 用户需要多个版本时提供 | 1–4张图像 |
| **image_urls** | 用户想要编辑或引用现有图像时提供 | 最多14个URL；这将触发图像到图像的生成模式 |
| **mask_url** | 用户想要编辑图像的一部分时提供 | PNG格式的掩码图；仅适用于`gpt-4o-image` |

#### 视频生成

| 参数 | 询问时机 | 备注 |
|-----------|----------|-------|
| **prompt** | 必需 | 询问用户想要的场景 |
| **model** | 用户询问或需要特定功能时提供 | 默认：`seedance-1.5-pro`。请参阅模型快速参考。 |
| **duration** | 用户提及视频长度时提供 | 不同模型的支持长度不同 |
| **aspect_ratio** | 用户提及画面比例时提供 | 默认：`16:9` |
| **quality** | 用户提及分辨率偏好时提供 | `480p` / `720p` / `1080p` |
| **image_urls** | 用户提供参考图像时提供 | 1张图像 = 生成单帧视频；2张图像 = 生成第一帧和最后一帧（仅适用于`seedance-1.5-pro`） |
| **generate_audio** | 使用`seedance-1.5-pro`或`veo3.1-pro`（BETA）时询问 | 询问：“是否希望在视频中添加自动生成的音频（人声、音效、音乐）？”

#### 音乐生成

音乐生成需要两个必填参数——在调用`generate_music`之前必须收集这两个参数。

**决策流程（按此顺序提问）：**

1. **人声还是器乐？**
   → 设置`instrumental: true/false`

2. **简单模式还是自定义模式？**
   - **简单模式**（`custom_mode: false`）：AI根据您的描述编写歌词并选择风格。最简单的方式。
   - **自定义模式**（`custom_mode: true`）：您可以控制风格标签、歌曲标题，并使用`[Verse]`, `[Chorus]`, `[Bridge]`等标记来编写歌词。
   → 设置`custom_mode: true/false`

3. **如果是自定义模式**，还需收集以下信息：
   - `style`：音乐风格 + 情绪 + 速度标签（例如：“pop, upbeat, female vocals, 120bpm”）
   - `title`：歌曲名称（最多80个字符）
   - `vocal_gender`：`m`（男性）或`f`（女性）——可选

4. **时长偏好？**
   - `duration`：目标时长（以秒为单位）。如果未指定，模型将自动决定时长。

5. **两种模式均可选择的选项：**
   - `negative_tags`：需要排除的风格（例如：“heavy metal, screaming”）
   - `model`：默认使用`suno-v4`。建议使用`suno-v5`以获得更高质量的结果。

> **规则：** 在调用`generate_music`之前，必须同时设置`custom_mode`和`instrumental`。这两个参数是必填项，没有默认值。

### 第4步：生成并监控进度

1. 使用收集到的参数调用相应的`generate_*`工具。
2. 告诉用户：“正在生成您的[类型]——预计耗时约X秒。我会随时更新进度。”
   - 如果响应中包含`task_info.estimated_time`，请使用该值。
3. 使用`check_task`定期查询进度：
   - **图像**：每3–5秒查询一次。
   - **视频**：每10–15秒查询一次。
   - **音乐**：每5–10秒查询一次。
4. 在查询过程中向用户报告进度百分比。
5. 连续收到3次“processing”状态后，告知用户：“仍在处理中，请稍候……”
6. **生成完成后**：分享结果URL，并提醒用户：“下载链接将在24小时后失效，请尽快下载。”
   - 从`result_data[]`中获取元数据（标题、时长、音乐标签）。
7. **生成失败时**：显示`check_task`的输出中的错误详情和建议。如果可以重试，请提供重试选项。

## 错误处理

### HTTP错误（立即显示）

| 错误代码 | 告诉用户的提示 |
|-------|----------------------|
| 401 Unauthorized | “您的API密钥无效。请在evolink.ai/dashboard/keys处检查或重新生成。” |
| 402 Payment Required | “您的账户余额不足。请在evolink.ai/dashboard/billing处充值。” |
| 429 Rate Limited | “请求过多——请等待30秒后再试。” |
| 503 Service Unavailable | “Evolink服务器暂时繁忙。请稍后再次尝试。”

### 任务错误（当`check_task`的状态为“failed”时）

| 错误代码 | 是否可重试 | 应采取的行动 |
|------------|-----------|--------|
| `content_policy_violation` | 不可重试 | 修改提示内容——避免使用真实照片、名人、不适宜的内容或暴力场景 |
| `invalid_parameters` | 不可重试 | 核对参数值是否符合模型要求 |
| `image_dimension_mismatch` | 不可重试 | 调整图像大小以匹配所需的画面比例 |
| `image_processing_error` | 不可重试 | 检查图像格式（JPG/PNG/WebP）、大小（小于10MB）和URL是否可访问 |
| `generation_timeout` | 可重试 | 简化提示或降低分辨率 |
| `quota_exceeded` | 可重试 | 等待30秒后再试。建议充值 |
| `resource_exhausted` | 可重试 | 等待30-60秒后再试 |
| `service_error` | 可重试 | 1分钟后再次尝试 |

## 模型快速参考

### 视频模型（共37个——展示部分推荐模型）

| 模型 | 适用场景 | 主要特点 | 支持音频 |
|-------|----------|----------|-------|
| `seedance-1.5-pro` （默认） | 图像到视频，生成第一帧和最后一帧 | 支持i2v格式，时长4–12秒，分辨率1080p | 支持自动音频 |
| `seedance-2.0` | 新一代运动模型（API待更新） | — | — |
| `sora-2-preview` | 电影级预览 | 支持t2v格式，时长1080p | — |
| `kling-o3-text-to-video` | 文本到视频，时长1080p | 支持t2v格式 | — |
| `veo-3.1-generate-preview` | Google视频预览 | 支持t2v格式，时长1080p | — |
| `MiniMax-Hailuo-2.3` | 高质量视频 | 支持t2v格式，时长1080p | — |
| `wan2.6-text-to-video` | 阿里巴巴最新t2v模型 | 支持t2v格式 | — |
| `sora-2` （BETA） | 电影级效果，严格遵循提示 | 支持t2v格式，时长1080p | — |
| `veo3.1-pro` （BETA） | 最高质量+音频支持 | 支持t2v格式，时长1080p | 自动添加音频 |

### 图像模型（共20个——展示部分推荐模型）

| 模型 | 适用场景 | 生成速度 | |
|-------|----------|-------|
| `gpt-image-1.5` （默认） | 最新的OpenAI模型 | 生成速度中等 |
| `gemini-3.1-flash-image-preview` | Nano Banana 2模型，生成速度快 | 生成速度较快 |
| `z-image-turbo` | 快速迭代模型 | 生成速度极快 |
| `doubao-seedream-4.5` | 真实感强的图像模型 | 生成速度中等 |
| `qwen-image-edit` | 基于指令的编辑模型 | 生成速度中等 |
| `gpt-4o-image` （BETA） | 最高质量，支持复杂编辑 | 生成速度中等 |
| `gemini-3-pro-image-preview` | Google模型预览 | 生成速度中等 |

### 音乐模型（全部为BETA版本）

| 模型 | 音乐质量 | 最大时长 | 备注 |
|-------|---------|--------------|-------|
| `suno-v4` （默认） | 生成质量良好 | 时长120秒 | 平衡性较好 |
| `suno-v4.5` | 生成质量更佳 | 时长240秒 | 提供更多功能 |
| `suno-v4.5plus` | 生成质量更佳 | 时长240秒 | 提供更多高级功能 |
| `suno-v4.5all` | 最高质量 | 时长240秒 | 提供所有高级功能 |
| `suno-v5` | 最高质量 | 时长240秒 | 生成效果最佳 |

## 异步处理时间参考

| 任务类型 | 通常处理时间 | 定期查询频率 | 最大等待时间 |
|------|-------------|------------|------------------------|
| 图像 | 3–30秒 | 每3–5秒查询一次 | 最大等待时间5分钟 |
| 视频 | 30–180秒 | 每10–15秒查询一次 | 最大等待时间10分钟 |
| 音乐 | 30–120秒 | 每5–10秒查询一次 | 最大等待时间5分钟 |

如果任务处理时间超过最大等待时间，请告知用户：“处理时间比预期长。任务可能仍在后台运行——您可以使用任务ID `[id]` 再次查看。”

## 跨媒体创作建议

在成功生成内容后，主动提供相关的创作建议：

- **图像生成后**：“想将这张图片制作成视频吗？我可以将其作为`seedance-1.5-pro`的参考图像。”
- **视频生成后**：“需要为这段视频配乐吗？我可以生成符合风格的音乐。”
- **音乐生成后**：“需要为这段音乐搭配视觉素材吗？我可以生成相应的图像或视频循环。”
- **任何时候**：“想要尝试不同的风格或模型吗？”

## 无MCP服务器时——直接使用文件托管API

当MCP工具不可用时，您仍然可以通过`curl`使用Evolink的文件托管服务。这适用于上传图像、音频或视频文件以获取公开访问的URL。

**基础URL：** `https://files-api.evolink.ai`
**认证方式：** `Authorization: Bearer $EVOLINK_API_KEY`

### 上传本地文件

```bash
curl -X POST https://files-api.evolink.ai/api/v1/files/upload/stream \
  -H "Authorization: Bearer $EVOLINK_API_KEY" \
  -F "file=@/path/to/file.jpg"
```

### 从URL上传文件

```bash
curl -X POST https://files-api.evolink.ai/api/v1/files/upload/url \
  -H "Authorization: Bearer $EVOLINK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"file_url": "https://example.com/image.jpg"}'
```

### 获取响应

```json
{
  "data": {
    "file_id": "file_abc123",
    "file_url": "https://...",
    "download_url": "https://...",
    "file_size": 245120,
    "mime_type": "image/jpeg",
    "expires_at": "2025-03-01T10:30:00Z"
  }
}
```

使用响应中的`file_url`作为公开访问链接。文件在72小时后过期。

### 查看文件列表和检查空间使用情况

```bash
curl https://files-api.evolink.ai/api/v1/files/list?page=1&pageSize=20 \
  -H "Authorization: Bearer $EVOLINK_API_KEY"

curl https://files-api.evolink.ai/api/v1/files/quota \
  -H "Authorization: Bearer $EVOLINK_API_KEY"
```

### 删除文件

```bash
curl -X DELETE https://files-api.evolink.ai/api/v1/files/{file_id} \
  -H "Authorization: Bearer $EVOLINK_API_KEY"
```

**支持的文件类型：** 图像（JPEG/PNG/GIF/WebP）、音频（所有格式）、视频（所有格式）。最大文件大小为100MB。用户空间限制：默认100个文件/VIP用户500个文件。

> **提示：** 要获得完整的创作功能（生成视频、图像、音乐），请通过mcporter连接MCP服务器`@evolinkai/evolink-media`——请参考上述MCP服务器设置。

## 参考资料

- `references/api-params.md`：所有工具的完整API参数参考。