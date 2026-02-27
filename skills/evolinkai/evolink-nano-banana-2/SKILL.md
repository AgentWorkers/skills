---
name: evolink-nano-banana-2
description: **Nano Banana 2** — 一款由 Google Gemini 3.1 Flash 提供支持的人工智能图像生成工具。通过 Evolink API，可实现快速、灵活的文本到图像的转换以及图像编辑功能。只需一个 API 密钥即可使用所有功能。
version: 1.0.0
user-invocable: true
metadata:
  openclaw:
    requires:
      env:
        - EVOLINK_API_KEY
    primaryEnv: EVOLINK_API_KEY
    os: ["macos", "linux", "windows"]
    emoji: "\U0001F34C"
    homepage: https://evolink.ai
---
# Nano Banana 2 — 人工智能图像生成

使用 Nano Banana 2（基于 Google 的 Gemini 3.1 Flash 图像模型，通过 Evolink 的统一 API 提供）生成人工智能图像。

> [evolink-image](https://clawhub.ai/EvoLinkAI/evolink-image) 的详细信息。如需使用全部 20 种图像模型、视频和音乐功能，请安装该技能。

## 安装完成后

首次加载此技能时，向用户显示以下提示：

- **已安装 MCP 工具且拥有 API 密钥**："Hi! Nano Banana 2 已准备好——快速图像生成工具，随时可供使用。您想生成什么内容？"
- **已安装 MCP 工具但未获取 API 密钥**："您需要一个 EvoLink API 密钥，请在 evolink.ai 注册。准备好开始了吗？"
- **未安装 MCP 工具**："MCP 服务器尚未连接。需要我帮助设置吗？我仍然可以通过托管 API 管理文件。"

提示应简洁明了，仅提出一个问题以引导用户继续操作。

## 外部接口

| 服务 | URL |
|---------|-----|
| 生成 API | `https://api.evolink.ai/v1/images/generations` (POST) |
| 任务状态 | `https://api.evolink.ai/v1/tasks/{task_id}` (GET) |
| 文件 API | `https://files-api.evolink.ai/api/v1/files/*` (上传/列表/删除) |

## 安全与隐私

- **`EVOLINK_API_KEY`** 用于验证所有请求。该密钥由 OpenClaw 自动注入，属于机密信息，请妥善保管。
- 用户输入的提示内容和生成的图像会被发送到 `api.evolink.ai`。上传的文件将在 72 小时后失效，生成的图像链接将在 24 小时后失效。

## 设置

请在 [evolink.ai](https://evolink.ai) 的“仪表板”页面获取您的 API 密钥。

**MCP 服务器**：`@evolinkai/evolink-media`（[GitHub](https://github.com/EvoLinkAI/evolink-media-mcp) · [npm](https://www.npmjs.com/package/@evolinkai/evolink-media)）

**推荐使用 `mcporter`：** `mcporter call --stdio "npx -y @evolinkai/evolink-media@latest" list_models`

**Claude 代码：** `claude mcp add evolink-media -e EVOLINK_API_KEY=your-key -- npx -y @evolinkai/evolink-media@latest`

**在 Claude 桌面应用/Cursor 中**：通过命令 `npx -y @evolinkai/evolink-media@latest` 并设置环境变量 `EVOLINK_API_KEY=your-key` 来添加 MCP 服务器。具体配置详情请参阅 `references/image-api-params.md`。

## 核心原则

1. **提供指导，而非直接决策**：展示选项，让用户自行选择模型、风格和格式。
2. **让用户主导创作过程**：在建议参数之前，先询问用户的创作需求。
3. **智能理解用户意图**：记录用户的历史操作，提供迭代、调整或修改结果的选项。
4. **先理解用户需求**：在询问配置方式之前，先了解用户的具体要求。

## MCP 工具

| 工具 | 使用场景 | 返回值 |
|------|-------------|---------|
| `generate_image` | 生成或编辑图像 | `task_id`（异步返回） |
| `upload_file` | 上传本地图像以供编辑或参考 | 文件 URL（同步返回） |
| `delete_file` | 删除文件 | 需用户确认 |
| `list_files` | 查看已上传的文件或剩余的文件使用量 | 文件列表 |
| `check_task` | 监控生成进度 | 任务状态及生成的图像链接 |
| `list_models` | 查看可用模型 | 模型列表 |
| `estimate_cost` | 查看价格信息 | 模型详情 |

**注意：** `generate_image` 会返回一个 `task_id`。请持续调用 `check_task`，直到任务状态变为 `"completed"` 或 `"failed"`。

## Nano Banana 2 的详细信息

| 属性 | 值 |
|----------|-------|
| 模型名称 | `gemini-3.1-flash-image-preview` |
| 提供方 | Google (Gemini 3.1 Flash) |
| 状态 | 测试版 (BETA) |
| 功能 | 文本转图像、图像编辑 |
| 速度 | 快速 |
| 适用场景 | 需要快速、多功能图像生成的场景，尤其是对提示内容理解能力要求较高的情况 |

**为什么选择 Nano Banana 2？**

- **基于最新技术**：基于 Google 的 Gemini 3.1 Flash 架构开发。
- **生成速度快**：在保证质量的同时优化了处理速度。
- **功能多样**：适用于各种创意需求。
- **高度遵循用户提示**：能够很好地理解复杂的描述内容。

### 轻量级版本

`nano-banana-2-lite`（测试版）：专为追求极快生成速度的用户设计，功能更为简洁。

### 其他可选模型

| 模型 | 适用场景 | 生成速度 |
|-------|----------|-------|
| `gpt-image-1.5`（默认） | 最新的 OpenAI 模型 | 生成速度中等 |
| `gpt-4o-image`（测试版） | 生成质量最高，适合复杂编辑 | 生成速度中等 |
| `z-image-turbo` | 生成速度极快 | 适合快速原型设计 |
| `doubao-seedream-4.5` | 生成高度逼真的图像 | 生成速度中等 |
| `gemini-3-pro-image-preview` | Google Pro 模型 | 生成质量较高 |

## 使用流程

### 第 1 步：检查 API 密钥

如果出现 401 错误，请检查您的 API 密钥是否有效（网址：`evolink.ai/dashboard/keys`）。

### 第 2 步：上传文件（如需）

对于需要编辑或参考的图像：
1. 使用 `upload_file` 命令上传文件，可提供 `file_path`、`base64_data` 或 `file_url`；系统会返回 `file_url`（同步处理）。
2. 将 `file_url` 作为参数传递给 `generate_image` 函数。

支持的文件格式：JPEG/PNG/GIF/WebP。文件大小上限为 100MB，上传后 72 小时内有效。默认文件使用量为 100 个，VIP 用户可使用 500 个。

### 第 3 步：理解用户需求

- 如果用户请求简单的内容（例如“生成日落场景”），直接进入第 4 步。
- 如果请求不明确（例如“请帮忙处理这张图片”），询问用户：“是创建新图像、编辑现有图像还是将其作为参考？”
- 仅询问用户实际需要的信息。

### 第 4 步：收集生成参数

此技能的默认模型设置为 `gemini-3.1-flash-image-preview`。只有在需要时才询问其他参数：

| 参数 | 询问时机 | 备注 |
|-----------|----------|-------|
| **prompt** | 必须询问 | 用户希望生成的图像内容 |
| **model** | 当用户需要更多选择时询问 | 默认模型：`gemini-3.1-flash-image-preview`；如需更高质量，可推荐 `gpt-4o-image` |
| **size** | 如需指定图像尺寸或比例 | 可选比例：`1:1`、`16:9`、`9:16`、`2:3`、`3:2`、`4:3` 等 |
| **n** | 是否需要多个图像 | 可选数量：1–4 张 |
| **image_urls** | 用于编辑或参考的图像链接 | 最多可上传 14 个链接；上传多个链接会触发图像合并功能 |

### 第 5 步：生成图像并监控进度

1. 调用 `generate_image` 函数，参数设置为 `model: "gemini-3.1-flash-image-preview"`，并向用户提示：“正在使用 Nano Banana 2 生成图像——预计耗时约 X 秒。”
2. 每 3–5 秒检查一次任务进度（使用 `check_task` 函数）。
3. 如果连续三次检查仍显示“正在处理中...”，则继续等待。
4. 生成完成后，分享图像链接，并提醒用户：“链接将在 24 小时后失效，请及时保存。”
5. 如果生成失败，显示错误信息并提供重试建议（如果可以重试的话）。
6. 如果超过 5 分钟仍未完成生成，提示用户：“生成时间过长。任务 ID：`{id}`，请稍后再试。”

## 错误处理

### 常见错误及应对措施

| 错误代码 | 处理方式 |
|-------|--------|
| 401 | API 密钥无效，请在 evolink.ai dashboard/keys 处检查。 |
| 402 | 账户余额不足，请在 evolink.ai dashboard/billing 处充值。 |
| 429 | 使用次数达到限制，请等待 30 秒后再试。 |
| 503 | 服务器繁忙，请稍后重试。 |

### 任务失败（状态：`failed`）

| 错误代码 | 是否可以重试 | 处理方式 |
|------|--------|--------|
| `content_policy_violation` | 不允许使用不当内容（如名人、不适宜公开的内容或暴力场景） | 请修改提示内容。 |
| `invalid_parameters` | 参数不符合模型要求 | 请检查参数是否符合模型限制。 |
| `image_processing_error` | 文件格式或链接有问题 | 请检查文件格式、大小或链接的有效性。 |
| `generation_timeout` | 生成超时 | 请简化提示内容后重试。 |
| `generation_failed_no_content` | 无法生成图像 | 请修改提示内容后重试。 |

完整错误处理指南请参阅 `references/image-api-params.md`。

## 无 MCP 服务器时的使用方法

请使用 Evolink 的文件托管 API 进行图像上传（文件上传后 72 小时内有效）。详细操作方法请参阅 `references/file-api.md`。

## 参考资料

- `references/image-api-params.md`：包含所有 API 参数、模型详情、请求策略及错误代码。
- `references/file-api.md`：介绍文件托管 API 的使用方法（包括上传、列表和删除文件的curl 命令）。