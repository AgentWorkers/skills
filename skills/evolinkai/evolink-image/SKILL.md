---
name: evolink-image
description: AI图像生成与编辑工具：GPT Image、GPT-4o、Nano Banana 2、Seedream、Qwen、WAN、Gemini。支持文本到图像（Text-to-Image）和图像到图像（Image-to-Image）的功能，以及图像修复（Image Inpainting）功能。共20个模型，只需一个API密钥即可使用所有功能。
version: 1.4.0
user-invocable: true
metadata:
  openclaw:
    requires:
      env:
        - EVOLINK_API_KEY
    primaryEnv: EVOLINK_API_KEY
    os: ["macos", "linux", "windows"]
    emoji: 🖼️
    homepage: https://evolink.ai
---
# Evolink Image — 人工智能图像生成与编辑

通过一个统一的API，可以使用包括GPT Image 1.5、GPT-4o Image、Nano Banana 2、Seedream、Qwen、WAN和Gemini在内的20个模型来生成和编辑AI图像。

> 更多关于[evolink-media](https://clawhub.ai/EvoLinkAI/evolink-media)的详细信息，请访问该链接。您还可以安装该工具以使用视频和音乐功能。

## 安装完成后

当此工具首次加载时，会向用户显示以下提示：

- **已准备好MCP工具和API密钥**：“嗨！我是您的人工智能图像生成工具，提供了20个模型供您选择。您想创建什么？”
- **仅配备了MCP工具，但尚未获取API密钥**：“您需要一个Evolink API密钥——请在evolink.ai注册。准备好开始了吗？”
- **未安装MCP工具**：“MCP服务器尚未连接。需要我帮助设置吗？即使没有MCP工具，我也可以通过托管API来管理文件。”

请保持提示简洁，只提出一个问题以便用户继续操作。

## 外部端点

| 服务 | URL |
|---------|-----|
| 生成API | `https://api.evolink.ai/v1/images/generations` (POST) |
| 任务状态 | `https://api.evolink.ai/v1/tasks/{task_id}` (GET) |
| 文件API | `https://files-api.evolink.ai/api/v1/files/*` (上传/列表/删除) |

## 安全性与隐私

- **`EVOLINK_API_KEY`**用于验证所有请求。该密钥由OpenClaw自动注入，属于机密信息，请妥善保管。
- 用户输入的提示内容和生成的图像会被发送到`api.evolink.ai`。上传的文件将在**72小时后**失效，生成的图像链接将在**24小时后**失效。

## 设置

请在[evolink.ai](https://evolink.ai)的“仪表盘”页面获取您的API密钥。

**MCP服务器：** `@evolinkai/evolink-media`（[GitHub](https://github.com/EvoLinkAI/evolink-media-mcp) · [npm](https://www.npmjs.com/package/@evolinkai/evolink-media)`  

**推荐使用`mcporter`：** `mcporter call --stdio "npx -y @evolinkai/evolink-media@latest" list_models`

**Claude工具：** `claude mcp add evolink-media -e EVOLINK_API_KEY=your-key -- npx -y @evolinkai/evolink-media@latest`

**在Claude Desktop/Cursor中设置MCP服务器：** 使用命令`npx -y @evolinkai/evolink-media@latest`，并设置环境变量`EVOLINK_API_KEY=your-key`。详细配置信息请参阅`references/image-api-params.md`。

## 核心原则

1. **提供指导，而非直接决定**：展示各种选项，让用户自行选择模型、风格和格式。
2. **让用户主导创作过程**：在建议参数之前，先询问用户的创作需求。
3. **智能理解用户意图**：记住用户的操作历史，提供迭代、调整或修改结果的功能。
4. **先理解用户需求，再指导操作方式**：在询问配置方法之前，先了解用户的具体需求。

## MCP工具

| 工具 | 使用场景 | 返回值 |
|------|-------------|---------|
| `generate_image` | 生成或编辑图像 | `task_id`（异步返回） |
| `upload_file` | 上传本地图像以供编辑或参考 | 文件URL（同步上传） |
| `delete_file` | 删除文件 | 需用户确认 |
| `list_files` | 查看已上传的文件或剩余的文件使用量 | 文件列表 |
| `check_task` | 监控生成进度 | 任务状态及生成的图像链接 |
| `list_models` | 查看可用的模型 | 模型列表 |
| `estimate_cost` | 查看价格信息 | 模型详情 |

**注意：** `generate_image`操作会返回一个`task_id`。请持续调用`check_task`，直到任务状态变为“completed”或“failed”。

## 可用的图像模型（共20个）

### 推荐模型

| 模型 | 适用场景 | 生成速度 |
|-------|----------|-------|
| `gpt-image-1.5` （默认） | 最新的OpenAI模型 | 生成速度中等 |
| `gemini-3.1-flash-image-preview` | Nano Banana 2模型——Google快速生成引擎 | 生成速度较快 |
| `z-image-turbo` | 快速迭代模型 | 生成速度极快 |
| `doubao-seedream-4.5` | 具有高度真实感的模型 | 生成速度中等 |
| `qwen-image-edit` | 支持基于文本的编辑 | 生成速度中等 |
| `gpt-4o-image` [测试版] | 图像质量最高，支持复杂编辑 | 生成速度中等 |
| `gemini-3-pro-image-preview` | Google生成的预览模型 | 生成速度中等 |

### 稳定运行的模型（共16个）

`gpt-image-1.5`, `gpt-image-1`, `gemini-3.1-flash-image-preview`, `gemini-3-pro-image-preview`, `z-image-turbo`, `doubao-seedream-4.5`, `doubao-seedream-4.0`, `doubao-seedream-3.0-t2i`, `doubao-seededit-4.0-i2i`, `doubao-seededit-3.0-i2i`, `qwen-image-edit`, `qwen-image-edit-plus`, `wan2.5-t2i-preview`, `wan2.5-i2i-preview`, `wan2.5-text-to-image`, `wan2.5-image-to-image`

### 测试版模型（共4个）

`gpt-image-1.5-lite`, `gpt-4o-image`, `gemini-2.5-flash-image`, `nano-banana-2-lite`

## 图像生成流程

### 第1步：检查API密钥

如果收到401错误，请检查您的API密钥是否有效（网址：`evolink.ai/dashboard/keys`）。

### 第2步：上传文件（如需编辑图像）

- 对于图像编辑或参考用途：
  - 使用`upload_file`命令，提供`file_path`、`base64_data`或`file_url`，系统会返回`file_url`（同步上传）。
  - 使用`file_url`作为`generate_image`函数的参数。

支持的文件格式：JPEG/PNG/GIF/WebP。文件大小上限为100MB。文件在上传后72小时内有效，每个用户默认有100个上传权限（VIP用户可增加至500个）。

### 第3步：明确用户需求

- 如果用户请求“生成日落场景的图像”，则直接进入第4步；
- 如果请求不明确，可询问用户：“是想要创建新图像、编辑现有图像，还是将其作为参考图像使用？”

仅询问用户真正需要的信息。

### 第4步：收集所需参数

- **prompt**：始终询问用户希望生成的图像内容。
- **model**：根据需求选择合适的模型（如`gpt-image-1.5`（质量一般）或`gpt-4o-image`（质量较高）。
- **size**：指定图像的尺寸和比例（例如：`1024x1024`/`1024x1536`/`1536x1024`）。
- **n**：询问用户是否需要生成多张图像（1–4张）。
- **image_urls**：提供用于编辑或参考的图像URL（最多14个），这些URL会触发i2i（图像拼接）功能。
- **mask_url**：用于部分编辑的PNG掩码图像（仅适用于`gpt-4o-image`模型）。

### 第5步：生成图像并监控进度

- 调用`generate_image`函数，并告知用户：“正在生成中……预计耗时约X秒。”
- 每3–5秒检查一次任务进度。
- 如果生成过程持续超过3次提示“Still working...”，则说明生成失败。
- 生成完成后，分享图像链接，并提醒用户链接将在24小时后失效，请及时保存。
- 如果生成失败，显示错误信息并提供重试建议（如果可以重试的话）。
- 如果等待5分钟后仍未完成生成，提示“生成时间过长（任务ID：{id}），请稍后再试。”

## 错误处理

### 常见HTTP错误

| 错误代码 | 处理方式 |
|-------|--------|
| 401 | API密钥无效，请在evolink.ai的仪表板页面检查密钥信息。 |
| 402 | 账户余额不足，请在evolink.ai的仪表板页面充值。 |
| 429 | 使用频率超出限制，请等待30秒后重试。 |
| 503 | 服务器繁忙，请稍后重试。 |

### 任务失败（状态为“failed”时的处理方式

| 错误代码 | 是否可以重试 | 处理方式 |
|------|--------|--------|
| `content_policy_violation` | 无法重试 | 请修改请求内容（避免使用名人、不适宜公开的内容或暴力场景）。 |
| `invalid_parameters` | 无法重试 | 核对参数是否符合模型要求。 |
| `image_dimension_mismatch` | 无法重试 | 调整图像尺寸以匹配指定比例。 |
| `image_processing_error` | 无法重试 | 检查图像格式、尺寸或URL是否有效。 |
| `generation_timeout` | 可以重试 | 如果问题重复出现，尝试简化请求内容。 |
| `quota_exceeded` | 可以重试 | 购买更多使用权限。 |
| `resource_exhausted` | 可以重试 | 等待30–60秒后再试。 |
| `service_error` | 可以重试 | 1分钟后再次尝试。 |
| `generation_failed_no_content` | 可以重试 | 修改请求内容后再试。 |

更多错误处理详情请参阅`references/image-api-params.md`。

## 无需MCP服务器的情况

您也可以使用Evolink的文件托管API来上传图像（文件在上传后72小时内有效）。有关curl命令的详细信息，请参阅`references/file-api.md`。

## 参考资料

- `references/image-api-params.md`：包含所有API参数、19个模型的详细信息、请求策略及错误代码。
- `references/file-api.md`：介绍文件托管API（包括上传、列表和删除操作的curl命令）。