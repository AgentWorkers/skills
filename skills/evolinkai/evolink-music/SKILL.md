---
name: evolink-music
description: 使用 Suno v4、v4.5、v5 进行 AI 音乐生成：支持文本转音乐功能，可自定义歌词，支持纯器乐或人声音乐。共包含 5 个模型，只需一个 API 密钥即可使用所有功能。
version: 2.0.0
user-invocable: true
metadata:
  openclaw:
    requires:
      env:
        - EVOLINK_API_KEY
    primaryEnv: EVOLINK_API_KEY
    os: ["macos", "linux", "windows"]
    emoji: "\U0001F3B5"
    homepage: https://evolink.ai
---
# Evolink Music — 人工智能音乐生成服务

通过 Suno v4、v4.5 和 v5 生成人工智能音乐和歌曲，支持简单模式（仅描述音乐风格）或自定义模式（包括歌词、风格、节奏和人声）。所有操作均通过一个统一的 API 完成。

> 该功能可在 [evolink-media](https://clawhub.ai/EvoLinkAI/evolink-media) 网站上使用。如需支持视频和图片处理，请安装完整的 Evolink 服务。

## 安装完成后

当该功能首次加载时，会向用户显示以下提示：
- **已安装 MCP 工具且拥有 API 密钥**："您好！我是您的 AI 音乐制作工具——Suno v4/v5 已准备就绪。您想创作什么类型的音乐吗？"
- **已安装 MCP 工具但未获取 API 密钥**："您需要一个 EvoLink API 密钥，请在 evolink.ai 注册。准备好开始了吗？"
- **未安装 MCP 工具**："MCP 服务器尚未连接。需要我协助设置吗？我仍可以通过文件托管 API 来管理文件。"

请保持提示简洁，仅使用一个问题引导用户继续操作。

## 外部接口

| 服务 | URL          |
|---------|-------------|
| 音乐生成 API | `https://api.evolink.ai/v1/audios/generations` (POST) |
| 任务状态 | `https://api.evolink.ai/v1/tasks/{task_id}` (GET) |
| 文件操作 API | `https://files-api.evolink.ai/api/v1/files/*` (上传/列表/删除) |

## 安全与隐私

- **`EVOLINK_API_KEY`** 用于验证所有请求。该密钥由 OpenClaw 自动注入，属于敏感信息，请妥善保管。
- 用户输入的提示信息和音频数据会被发送至 `api.evolink.ai`。上传的文件将在 72 小时后失效，生成的音频文件链接将在 24 小时后失效。

## 设置

请在 [evolink.ai](https://evolink.ai) 的“控制面板”中获取您的 API 密钥。

**MCP 服务器：** `@evolinkai/evolink-media` （[GitHub](https://github.com/EvoLinkAI/evolink-media-mcp) · [npm](https://www.npmjs.com/package/@evolinkai/evolink-media)）

**推荐使用 `mcporter`：** `mcporter call --stdio "npx -y @evolinkai/evolink-media@latest" list_models`

**使用 Claude 工具进行配置：** `claude mcp add evolink-media -e EVOLINK_API_KEY=your-key -- npx -y @evolinkai/evolink-media@latest`

**在 Claude 桌面应用/Cursor 中配置：** 使用命令 `npx -y @evolinkai/evolink-media@latest` 并设置环境变量 `EVOLINK_API_KEY=your-key`。详细配置信息请参考 `references/music-api-params.md`。

## 核心原则

1. **提供选择**：仅展示选项，让用户自行决定使用哪种模型或风格。
2. **用户主导创作**：在建议参数之前，先询问用户的创作需求。
3. **智能上下文感知**：记录用户的历史操作，提供迭代、风格调整或重新混音的功能。
4. **先理解意图**：在询问配置方式之前，先了解用户的具体需求。

## MCP 工具

| 工具 | 使用场景 | 返回值           |
|------|-------------|-------------------|
| `generate_music` | 生成人工智能音乐或歌曲 | `task_id` (异步返回)       |
| `upload_file` | 上传音频文件以继续创作/混音 | 文件 URL (同步返回)       |
| `delete_file` | 删除文件           | 确认删除操作是否成功       |
| `list_files` | 查看已上传的文件或剩余的文件配额 | 文件列表             |
| `check_task` | 监控生成进度       | 任务状态及结果链接         |
| `list_models` | 查看可用的音乐模型     | 可用模型列表           |
| `estimate_cost` | 查看价格信息       | 模型相关信息         |

**重要提示：** `generate_music` 会返回一个 `task_id`。请持续调用 `check_task`，直到任务状态变为 `"completed"` 或 `"failed"`。

## 音乐模型（共 5 种，均为测试版本）

| 模型 | 音乐质量 | 最长时长 | 适用场景           |
|-------|---------|-----------------|-------------------|
| `suno-v4` （默认） | 一般       | 120 秒        | 平衡性高，适合入门使用       |
| `suno-v4.5` | 更优质     | 240 秒        | 提供更多风格选择       |
| `suno-v4.5plus` | 更优质     | 240 秒        | 扩展功能           |
| `suno-v4.5all` | 最优质     | 240 秒        | 具备所有 v4.5 特性       |
| `suno-v5` | 最高级     | 240 秒        | 专业级音乐制作效果     |

## 生成流程

### 第一步：检查 API 密钥

如果收到 401 错误，提示："您的 API 密钥无效，请在 evolink.ai/dashboard/keys 处检查。"

### 第二步：上传文件（如需）

对于需要继续创作或混音的情况：
使用 `upload_file` 函数，提供 `file_path`、`base64_data` 或 `file_url`，系统会返回 `file_url`（同步返回）。
支持的文件格式：MP3、WAV、FLAC、AAC、OGG、M4A 等。文件大小上限为 100MB，上传后 72 小时内有效。默认文件配额为 100 个文件，VIP 用户可使用 500 个文件。

### 第三步：明确创作需求

- 如果用户请求“制作一段轻松的低保真音乐”，直接进入第四步。
- 如果请求信息不明确，询问用户："您希望音乐具有什么样的氛围或风格？需要包含人声还是纯乐器？"

仅询问必要的信息，并在需要时才进行询问。

### 第四步：收集参数

音乐生成需要填写两个必填字段：
- **人声或纯乐器？** （设置 `instrumental: true/false`）
- **选择简单模式还是自定义模式？**
  - **简单模式** (`custom_mode: false`)：AI 会根据您的描述自动生成歌词和风格。
  - **自定义模式** (`custom_mode: true`)：用户可以自定义歌词（`[Verse]`/`[Chorus]`/`[Bridge]`）、风格标签和歌曲名称。
- **在自定义模式下，还需提供：**
  - `style`：音乐风格和氛围（例如：“流行、欢快、女性人声、120bpm”）
  - `title`：歌曲名称（最多 80 个字符）
  - `vocal_gender`：男性（`m`）或女性（`f`）——可选
- **两种模式均可选择：**
  - `duration`：目标时长（30–240 秒，不提供则由模型决定）
  - `negative_tags`：需要排除的音乐风格
  - `model`：默认使用 `suno-v4`；如需专业级效果，建议使用 `suno-v5`

**重要提示：** `custom_mode` 和 `instrumental` 都是必填的 API 参数，必须填写才能生成音乐。

### 第五步：生成音乐并监控进度

1. 调用 `generate_music`，并向用户提示："正在为您生成音乐，预计耗时约 X 秒。"
2. 每 5–10 秒检查一次任务进度。
3. 如果连续三次显示“仍在处理中...”，请继续等待。
4. 生成完成后，分享音频文件的链接及元数据（歌曲名称、时长、标签等）："链接将在 24 小时后失效，请及时保存。"
5. 如果生成失败，显示错误信息并提供重试建议（如可重试）。
6. 如果超时（5 分钟），提示："生成时间过长。任务 ID：`{id}`，请稍后再试。"

## 错误处理

### HTTP 错误

| 错误代码 | 处理方式         |
|---------|-------------------|
| 401     | API 密钥无效，请在 evolink.ai/dashboard/keys 处检查。 |
| 402     | 信用点数不足，请在 evolink.ai/dashboard/billing 处充值。 |
| 429     | 服务暂时繁忙，请等待 30 秒后重试。 |
| 503     | 服务器繁忙，请稍后重试。 |

### 任务失败（状态为 "failed"）

| 错误代码 | 是否可重试 | 处理方式           |
|---------|-----------------|-------------------|
| `content_policy_violation` | 不可重试 | 请修改请求内容或歌词。     |
| `invalid_parameters` | 不可重试 | 核对参数是否符合模型要求。     |
| `generation_timeout` | 可重试 | 重新尝试；如问题重复出现，简化请求内容。 |
| `quota_exceeded` | 可重试 | 充值信用点数后再试。     |
| `resource_exhausted` | 可重试 | 等待 30–60 秒后再试。     |
| `service_error` | 可重试 | 1 分钟后再次尝试。     |

**错误详情请参考：`references/music-api-params.md`**

## 无 MCP 服务器时的使用方法

请使用 Evolink 的文件托管 API 进行音频文件上传（文件上传后 72 小时内有效）。上传命令请参考 `references/file-api.md`。

## 参考资料

- `references/music-api-params.md`：完整的 API 参数、所有音乐模型信息、请求策略及错误代码。
- `references/file-api.md`：文件托管 API 的使用说明（包括 curl 命令）。