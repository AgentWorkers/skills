---
name: evolink-image
description: AI图像生成与编辑工具：GPT Image、GPT-4o、Seedream、Qwen、WAN、Gemini。支持文本到图像（Text-to-Image）和图像到图像（Image-to-Image）的功能，以及图像修复（Image Inpainting）功能。共包含19个模型，只需使用一个API密钥即可访问所有功能。
version: 1.3.4
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

通过一个API，可以使用包括GPT Image 1.5、GPT-4o Image、Seedream、Qwen、WAN和Gemini在内的19个模型来生成和编辑AI图像。

> 更多关于[evolink-media](https://clawhub.ai/EvoLinkAI/evolink-media)的信息，请访问其官方网站。您还可以安装该技能以使用视频和音乐相关功能。

## 安装完成后

当此技能首次加载时，会向用户显示以下提示：
- **已准备好MCP工具和API密钥**：“嗨！我是您的AI图像工作室，提供了19个模型供您选择。您想创建什么？”
- **仅配备了MCP工具但未获取API密钥**：“您需要一个Evolink API密钥——请在evolink.ai注册。准备好开始了吗？”
- **未安装MCP工具**：“MCP服务器尚未连接。需要我帮助设置吗？我仍然可以通过托管API来管理文件。”

提示应简洁明了，仅提出一个问题以引导用户继续操作。

## 外部端点

| 服务 | URL |
|---------|-----|
| 生成API | `https://api.evolink.ai/v1/images/generations` (POST) |
| 任务状态 | `https://api.evolink.ai/v1/tasks/{task_id}` (GET) |
| 文件API | `https://files-api.evolink.ai/api/v1/files/*` (上传/列表/删除) |

## 安全与隐私

- **`EVOLINK_API_KEY`**用于验证所有请求。该密钥由OpenClaw自动注入，属于机密信息，请妥善保管。
- 用户输入的提示内容和生成的图像会被发送到`api.evolink.ai`。上传的文件将在**72小时内**失效，生成的图像链接将在**24小时内**失效。

## 设置

请在[evolink.ai](https://evolink.ai)的“仪表板”页面获取您的API密钥。

**MCP服务器**：`@evolinkai/evolink-media`（[GitHub](https://github.com/EvoLinkAI/evolink-media-mcp) · [npm](https://www.npmjs.com/package/@evolinkai/evolink-media)）

有关设置说明（包括mcporter、Claude Code、Claude Desktop和Cursor的使用方法），请参阅[GitHub的README文件](https://github.com/EvoLinkAI/evolink-media-mcp#setup)。

## 核心原则

1. **提供指导，而非直接决策**：向用户展示选项，让他们自行选择模型、风格和格式。
2. **让用户主导创作过程**：在建议参数之前，先询问用户的创作需求。
3. **智能理解上下文**：记录用户的操作历史，提供迭代、调整或修改结果的功能。
4. **先理解用户意图**：在询问配置方式之前，先了解用户的具体需求。

## MCP工具

| 工具 | 使用场景 | 返回值 |
|------|-------------|---------|
| `generate_image` | 创建或编辑图像 | `task_id`（异步返回） |
| `upload_file` | 上传本地图像以供编辑或参考 | 文件URL（同步返回） |
| `delete_file` | 删除文件 | 确认操作是否成功 |
| `list_files` | 查看已上传的文件或剩余的文件使用量 | 文件列表 |
| `check_task` | 监控生成进度 | 任务状态及生成的图像链接 |
| `list_models` | 查看可用的模型 | 模型列表 |
| `estimate_cost` | 查看价格信息 | 模型详情 |

**注意**：`generate_image`操作会返回一个`task_id`。请持续调用`check_task`，直到任务状态变为“completed”或“failed”。

## 图像模型（共19个）

### 推荐模型

| 模型 | 适用场景 | 生成速度 |
|-------|----------|-------|
| `gpt-image-1.5` （默认） | 最新的OpenAI模型 | 生成速度中等 |
| `z-image-turbo` | 快速生成 | 生成速度极快 |
| `doubao-seedream-4.5` | 具有高度真实感的图像 | 生成速度中等 |
| `qwen-image-edit` | 支持基于指令的编辑 | 生成速度中等 |
| `gpt-4o-image` [测试版] | 图像质量最高，支持复杂编辑 | 生成速度中等 |
| `gemini-3-pro-image-preview` | 谷歌开发的预览模型 | 生成速度中等 |

### 稳定运行的模型（共15个）

`gpt-image-1.5`、`gpt-image-1`、`gemini-3-pro-image-preview`、`z-image-turbo`、`doubao-seedream-4.5`、`doubao-seedream-4.0`、`doubao-seedream-3.0-t2i`、`doubao-seededit-4.0-i2i`、`doubao-seededit-3.0-i2i`、`qwen-image-edit`、`qwen-image-edit-plus`、`wan2.5-t2i-preview`、`wan2.5-i2i-preview`、`wan2.5-text-to-image`、`wan2.5-image-to-image`

### 测试版模型（共4个）

`gpt-image-1.5-lite`、`gpt-4o-image`、`gemini-2.5-flash-image`、`nano-banana-2-lite`

## 生成流程

### 第1步：检查API密钥

如果收到401错误，请检查您的API密钥是否有效（网址：`evolink.ai/dashboard/keys`）。

### 第2步：上传文件（如需）

对于图像编辑或参考用途：
1. 使用`upload_file`函数，传入`file_path`、`base64_data`或`file_url`，以获取`file_url`（操作为同步）。
2. 将`file_url`作为`generate_image`函数的参数使用。

支持的文件格式：JPEG/PNG/GIF/WebP。文件大小上限为100MB。文件在上传后72小时内失效，普通用户的使用量为100个文件，VIP用户为500个文件。

### 第3步：明确用户需求

- 如果用户请求“生成日落场景的图像”，则直接进入第4步；
- 如果请求“帮忙处理这张图片”，则询问用户：“是创建新图像、编辑现有图像还是将其作为参考？”
仅询问用户实际需要的信息。

### 第4步：收集所需参数

仅询问必要的参数：

| 参数 | 询问时机 | 说明 |
|-----------|----------|-------|
| **prompt** | 必须询问 | 用户希望看到的图像内容 |
| **model** | 根据需求选择模型 | 默认使用`gpt-image-1.5`；如需高质量图像，可使用`gpt-4o-image`；如需快速生成，可使用`z-image-turbo` |
| **size** | 需要指定图像尺寸 | GPT模型支持的尺寸为`1024x1024`/`1024x1536`/`1536x1024`；其他模型支持`1:1`/`16:9`/`9:16`等比例 |
| **n` | 是否需要多个图像 | 可选择生成1–4张图像 |
| **image_urls** | 提供用于编辑或参考的图像URL | 最多可提供14个URL；这些URL会触发i2i（图像合成）模式 |
| **mask_url** | 是否需要部分编辑 | 提供PNG格式的掩码图像；仅适用于`gpt-4o-image` |

### 第5步：生成图像并监控进度

1. 调用`generate_image`函数，告知用户：“正在生成中——预计耗时约X秒。”
2. 每3–5秒检查一次任务状态（使用`check_task`函数）。
3. 如果连续三次检查仍显示“正在处理中”，则提示用户“生成过程中……”
4. 生成完成后，分享图像链接，并提醒用户“链接在24小时后失效，请及时保存”。
5. 如果生成失败，显示错误信息并提供重试建议（如果可以重试的话）。
6. 如果超过5分钟仍未完成生成，提示用户“生成时间过长。任务ID：{id}——请稍后再试”。

## 错误处理

### 常见HTTP错误

| 错误代码 | 处理方式 |
|-------|--------|
| 401 | API密钥无效，请在evolink.ai/dashboard/keys页面检查 |
| 402 | 账户余额不足，请在evolink.ai/dashboard/billing页面充值 |
| 429 | 使用频率超出限制，请等待30秒后再试 |
| 503 | 服务器繁忙，请稍后重试 |

### 任务失败（状态为“failed”）

| 错误代码 | 是否可以重试 | 处理方式 |
|------|--------|--------|
| `content_policy_violation` | 不允许使用不适宜的内容（如名人、成人内容或暴力场景） | 请修改提示内容 |
| `invalid_parameters` | 参数值超出模型限制 | 请检查参数是否符合模型要求 |
| `image_dimension_mismatch` | 图像尺寸不匹配 | 请调整图像的宽高比 |
| `image_processing_error` | 图像处理失败 | 请检查图像的格式、大小或URL是否有效 |
| `generation_timeout` | 生成超时 | 请尝试重新生成；如果问题依旧，请简化提示内容 |
| `quota_exceeded` | 使用量超出限制 | 请充值账户 |
| `resource_exhausted` | 资源耗尽 | 请等待30–60秒后再试 |
| `service_error` | 服务暂时不可用 | 请稍后重试 |

## 无MCP服务器时的使用方法

可以使用Evolink的文件托管API来上传图像（文件在上传后72小时内失效）。详细信息请参阅[文件API文档](https://github.com/EvoLinkAI/evolink-media-mcp#file-api)。

## 参考资料

- `references/image-api-params.md`：包含所有API参数、19个模型的详细信息、请求策略及错误代码说明。
- [文件API文档](https://github.com/EvoLinkAI/evolink-media-mcp#file-api)：详细介绍文件托管API的使用方法。