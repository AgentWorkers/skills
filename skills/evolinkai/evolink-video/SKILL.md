---
name: evolink-video
description: AI视频生成工具：Sora、Kling、Veo 3、Seedance、Hailuo、WAN、Grok。支持文本转视频、图片转视频以及视频编辑功能。共37个模型，只需一个API密钥即可使用。
version: 2.0.1
user-invocable: true
metadata:
  openclaw:
    requires:
      env:
        - EVOLINK_API_KEY
    primaryEnv: EVOLINK_API_KEY
    os: ["macos", "linux", "windows"]
    emoji: "\U0001F3AC"
    homepage: https://evolink.ai
---
# Evolink Video — 人工智能视频生成服务

通过一个统一的API，可以使用包括Sora、Kling、Veo 3、Seedance、Hailuo、WAN和Grok在内的37个模型生成人工智能视频。支持文本转视频、图片转视频、仅使用视频的开头和结尾帧，以及音频生成等功能。

> 更多关于Evolink Video的详细信息，请访问[evolink-media](https://clawhub.ai/EvoLinkAI/evolink-media)。如需使用图片和音乐功能，请安装完整的Evolink Video插件。

## 安装完成后

首次加载该插件时，会向用户显示以下提示：
- **已安装MCP工具且拥有API密钥**：「嗨！我是您的AI视频制作工具，支持37个模型。您想制作什么类型的视频呢？」
- **已安装MCP工具但未获取API密钥**：「您需要一个Evolink API密钥，请在evolink.ai注册。准备好开始了吗？」
- **未安装MCP工具**：「MCP服务器尚未连接。需要我帮助设置吗？即便如此，我仍可以通过文件托管API来管理文件。」

提示信息应简洁明了，仅提出一个问题以引导用户继续操作。

## 外部接口

| 服务 | URL |
|---------|-----|
| 视频生成API | `https://api.evolink.ai/v1/videos/generations` (POST) |
| 任务状态查询 | `https://api.evolink.ai/v1/tasks/{task_id}` (GET) |
| 文件管理API | `https://files-api.evolink.ai/api/v1/files/*` (上传/列表/删除) |

## 安全与隐私

- **`EVOLINK_API_KEY`** 用于验证所有请求，由OpenClaw自动注入。请严格保密该密钥。
- 用户输入的提示内容和图片会被发送到`api.evolink.ai`。上传的文件将在72小时后失效，生成的视频链接将在24小时后失效。

## 设置

请在[evolink.ai](https://evolink.ai)的“仪表盘”页面获取您的API密钥。

**MCP服务器**：`@evolinkai/evolink-media`（[GitHub](https://github.com/EvoLinkAI/evolink-media-mcp) · [npm](https://www.npmjs.com/package/@evolinkai/evolink-media)  
**推荐使用mcporter工具**：`mcporter call --stdio "npx -y @evolinkai/evolink-media@latest" list_models`  
**Claude工具**：`claude mcp add evolink-media -e EVOLINK_API_KEY=your-key -- npx -y @evolinkai/evolink-media@latest`  
在Claude Desktop或Cursor环境中，可以通过`npx -y @evolinkai/evolink-media@latest`命令添加MCP服务器，并设置环境变量`EVOLINK_API_KEY=your-key`。详细配置信息请参考`references/video-api-params.md`。

## 核心原则

1. **提供选择**：仅展示选项，让用户自行选择模型、风格和时长。
2. **用户主导创作**：在提供参数建议前，先询问用户的创作需求。
3. **智能上下文感知**：记录用户的使用历史，提供迭代、扩展或重新制作视频的选项。
4. **理解用户意图**：在询问配置方式之前，先了解用户的具体需求。

## MCP工具

| 工具 | 使用场景 | 返回值 |
|------|-------------|---------|
| `generate_video` | 从文本或图片生成视频 | `task_id`（异步返回） |
| `upload_file` | 上传图片用于视频生成 | 图片URL（同步返回） |
| `delete_file` | 删除文件 | 确认操作是否成功 |
| `list_files` | 查看已上传的文件或剩余的文件使用量 | 文件列表 |
| `check_task` | 查询视频生成进度 | 进度状态及视频链接 |
| `list_models` | 显示可用模型列表 | 模型列表 |
| `estimate_cost` | 查看价格信息 | 模型详情 |

**注意**：`generate_video`操作会返回一个`task_id`。请持续调用`check_task`，直到状态变为“completed”或“failed”。

## 可用的视频模型（共37个）

### 推荐模型

| 模型 | 适用场景 | 特点 | 是否支持音频 |
|-------|----------|----------|-------|
| `seedance-1.5-pro` （默认） | 图片转视频、仅使用视频的开头和结尾帧 | 支持音频 |
| `sora-2-preview` | 适合制作电影风格的预览视频 | 支持图片转视频 |
| `kling-o3-text-to-video` | 文本转视频 | 支持图片转视频 |
| `veo-3.1-generate-preview` | 提供谷歌风格的视频预览 | 支持图片转视频 |
| `MiniMax-Hailuo-2.3` | 高质量视频生成 | 支持图片转视频 |
| `wan2.6-text-to-video` | 阿里巴巴最新的图片转视频功能 | 支持图片转视频 |
| `sora-2` [测试版] | 适合制作电影风格的视频 | 支持图片转视频 |
| `veo3.1-pro` [测试版] | 高质量视频生成，支持音频 | 支持图片转视频 |

**26个稳定可用模型**：Seedance（3个）、Sora Preview（1个）、Kling（10个）、Veo 3.1（2个）、Hailuo（3个）、WAN（7个）  
**11个测试版模型**：Sora 2/Pro/Max/Character（4个）、Veo 3/3.1（5个）、Grok Imagine（2个）

完整模型列表及详细信息请参考`references/video-api-params.md`。

## 视频生成流程

### 第1步：检查API密钥

如果收到401错误，请检查您的API密钥是否有效（网址：`evolink.ai/dashboard/keys`）。

### 第2步（如需）：上传文件

对于图片转视频或仅使用视频的开头和结尾帧的操作：
1. 使用`upload_file`命令上传图片（支持格式：JPEG/PNG/GIF/WebP），并提供`file_path`、`base64_data`或`file_url`；系统会返回`file_url`（同步处理）。
2. 将`file_url`作为参数传递给`generate_video`函数。

### 第3步：明确用户需求

- 如果用户需求明确（例如：“制作一只猫跳舞的视频”），直接进入第4步；  
- 如果需求模糊（例如：“我想制作一个视频”），则询问用户：“是文本转视频，还是需要使用参考图片？”  
仅询问必要的信息。

### 第4步：收集所需参数

根据用户需求收集以下参数：
- **prompt**：必填项，用于描述视频内容。
- **model**：根据用户需求选择合适的模型（例如：`seedance-1.5-pro`）。
- **duration**：用户指定的视频时长（通常为4–15秒）。
- **aspect_ratio**：视频的宽高比（默认为16:9，其他选项包括9:16、1:1、4:3、3:4、21:9）。
- **quality**：视频分辨率（480p、720p、1080p或4k）。
- **image_urls**：如果提供参考图片，这些图片将用于生成视频（`seedance-1.5-pro`模型需要2张图片）。

### 第5步：生成视频并监控进度

1. 调用`generate_video`函数，告知用户“正在生成视频，预计耗时约X秒”。
2. 每10–15秒检查一次任务进度。
3. 如果生成过程超过3次未完成，提示用户“视频生成中……”。
4. 生成完成后，分享视频链接，并提醒用户链接有效期为24小时，请及时保存。
5. 如果生成失败，显示错误信息并提供重试建议（如果可以重试的话）。
6. 如果请求超时（10分钟后仍未完成），提示用户“生成时间过长，请稍后再试”。

## 错误处理

### 常见错误及处理方式

| 错误代码 | 处理方式 |
|-------|--------|
| 401 | API密钥无效，请在evolink.ai dashboard/keys页面检查。 |
| 402 | 账户余额不足，请在evolink.ai dashboard/billing页面充值。 |
| 429 | 使用频率超出限制，请等待30秒后重试。 |
| 503 | 服务器繁忙，请稍后重试。 |

### 任务失败（状态为“failed”时的处理方式

| 错误代码 | 是否可以重试 | 处理方式 |
|------|--------|--------|
| `content_policy_violation` | 不允许使用不适宜的内容（如名人、成人内容或暴力场景），请修改提示。 |
| `invalid_parameters` | 参数不符合模型要求，请检查输入值。 |
| `image_dimension_mismatch` | 图片尺寸与模型要求不匹配，请调整图片尺寸。 |
| `image_processing_error` | 图片格式、大小或URL有问题，请检查并重新上传。 |
| `generation_timeout` | 生成失败，请简化提示内容或重试。 |
| `quota_exceeded` | 账户余额不足，请充值后重试。 |
| `resource_exhausted` | 资源耗尽，请等待30–60秒后重试。 |
| `service_error` | 服务器暂时无法处理，请稍后尝试。 |

## 无MCP服务器时的使用方法

请使用Evolink提供的文件托管API进行文件上传（文件上传后有效期为72小时）。上传命令请参考`references/file-api.md`。

## 参考资料

- `references/video-api-params.md`：包含所有模型的详细API参数、请求策略和错误代码。
- `references/file-api.md`：文件托管API的使用说明（包括curl命令）。