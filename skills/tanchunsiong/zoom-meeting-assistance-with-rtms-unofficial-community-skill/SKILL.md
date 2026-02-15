---
name: zoom-meeting-assistance-rtms-unofficial-community
description: Zoom RTMS 会议助手——可根据需求启动，通过 Zoom 的实时媒体流（Real-Time Media Streams）捕获会议音频、视频、文字记录、屏幕共享内容以及聊天记录。该工具能够处理 `meeting.rtms_started` 和 `meeting.rtms_stopped` 这两种 Webhook 事件，并提供基于人工智能的对话建议、情感分析以及实时会议摘要，同时会通过 WhatsApp 发送通知。适用于 Zoom RTMS Webhook 被触发时，或用户请求录制/分析会议数据的情况。
---

# Zoom RTMS 会议助手

这是一个用于捕获 Zoom 会议内容的无头（headless）服务，它利用实时媒体流（RTMS）技术来实现数据捕获。该服务能够接收 Webhook 事件，连接到 RTMS 的 WebSocket，记录所有媒体数据，并通过 OpenClaw 进行人工智能分析。

## 支持的 Webhook 事件

该服务可以处理两种 Zoom Webhook 事件：

- **`meeting.rtms_started`**：当 Zoom 为会议启用 RTMS 时，会发送此事件。该事件包含连接到 RTMS WebSocket 所需的 `server_urls`、`rtms_stream_id` 和 `meeting_uuid` 参数。
- **`meeting.rtms_stopped`**：当 RTMS 停用或会议结束时，Zoom 会发送此事件。此时服务会执行清理操作：关闭 WebSocket 连接，生成屏幕共享内容的 PDF 文件，并发送通知。

## Webhook 依赖

该服务需要一个公开的 Webhook 端点来接收来自 Zoom 的事件。**推荐使用** `ngrok-unofficial-webhook-skill`（位于 `skills/ngrok-unofficial-webhook-skill` 目录下）。该工具会自动检测到该服务，并通过 `skill.json` 文件中的 `webhookEvents` 配置来通知用户，同时提供将事件路由到该服务的功能。

其他 Webhook 解决方案（如自定义服务器或云函数）也可以使用，但可能需要额外的集成步骤才能将数据转发给该服务。

## 先决条件

**注意：** 该服务运行需要 `ffmpeg` 工具，用于会议后的媒体文件转换。

## 环境变量

请在服务的 `.env` 文件中配置以下环境变量：

- **必填：**
  - `ZOOM_SECRET_TOKEN`：Zoom Webhook 的秘密令牌
  - `ZOOM_CLIENT_ID`：Zoom 应用的客户端 ID
  - `ZOOM_CLIENT_SECRET`：Zoom 应用的客户端密钥

- **可选：**
  - `PORT`：服务器端口（默认值：`3000`
  - `AI_PROCESSING_INTERVAL_MS`：AI 分析的频率（单位：毫秒，默认值：`30000`）
  - `AI_FUNCTION_STAGGER_MS`：AI 调用之间的延迟时间（单位：毫秒，默认值：`5000`）
  - `AUDIO_DATA_OPT`：
    - `1`：混合音频流
    - `2`：多音频流（默认值：`2`
  - `OPENCLAW_NOTIFY_CHANNEL`：通知通道（默认值：`whatsapp`）
  - `OPENCLAW_NOTIFY_TARGET`：接收通知的电话号码或目标对象

## 启动服务

该服务会启动一个 Express 服务器，监听指定端口上的 Zoom Webhook 事件。

**⚠️ 重要提示：** 在将 Webhook 数据转发给该服务之前，请务必确认服务已正常运行。

如果服务未响应，请先启动服务后再进行数据转发。

**典型工作流程：**
1. 以后台进程的形式启动服务器。
2. Zoom 发送 `meeting.rtms_started` Webhook 事件 → 服务连接到 RTMS 的 WebSocket。
3. 实时捕获音频、视频、文字记录、屏幕共享内容和聊天记录等媒体数据。
4. 定期执行 AI 分析（生成对话建议、情感分析结果等）。
5. 收到 `meeting.rtms_stopped` 事件后，服务会关闭连接并生成屏幕共享内容的 PDF 文件。

## 录制数据的存储结构

所有录制文件按日期进行分类存储：

每个媒体流对应的文件夹包含以下文件：

| 文件名 | 文件内容 | 是否可搜索 |
|------|---------|-----------|
| `metadata.json` | 会议元数据（UUID、流 ID、操作员、开始时间） | ✅ |
| `transcript.txt` | 带时间戳的纯文本记录（每条发言占一行，便于搜索） | ✅ |
| `transcript.vtt` | 带时间戳的 VTT 格式记录 | ✅ |
| `transcript.srt` | SRT 格式的记录文件 | ✅ |
| `events.log` | 参与者加入/离开、当前发言者变更记录（JSON 格式） | ✅ |
| `chat.txt` | 带时间戳的聊天记录 | ✅ |
| `ai_summary.md` | 由 AI 生成的会议总结（Markdown 格式） | ✅ | 首先阅读此文件以获取会议概览 |
| `ai_dialog.json` | AI 生成的对话建议 | ✅ |
| `ai_sentiment.json` | 每位参与者的情绪分析结果 | ✅ |
| `mixedaudio.raw` | 混合音频流（原始 PCM 格式） | ❌ | 二进制文件 |
| `activespeakervideo.h264` | 当前发言者的视频流（原始 H.264 格式） | ❌ | 二进制文件 |
| `processed/screenshare.pdf` | 去重后的屏幕共享图片（PDF 格式） | ❌ | 二进制文件 |

所有生成的会议总结文件也会被复制到一个中央文件夹中，以便统一管理和查询。

## 查找和查询过去的会议记录

`.txt`、`.md`、`.json` 和 `.log` 文件均为文本格式，支持搜索。可以先查看 `ai_summary.md` 以获取会议概览，然后根据需要深入查看 `transcript.txt` 文件中的具体内容。

## API 端点

（相关 API 端点信息请参见文档中的说明。）

## 会议后的处理流程

当 `meeting.rtms_stopped` 事件触发时，服务会自动执行以下操作：
1. 从屏幕共享图片生成 PDF 文件。
2. 将 `mixedaudio.raw` 文件转换为 `mixedaudio.wav` 格式。
3. 将 `activespeakervideo.h264` 文件转换为 `activespeakervideo.mp4` 格式。
4. 将混合音频流与当前发言者的视频流合并为 `final_output.mp4` 文件。

虽然提供了手动转换脚本，但由于自动转换会在会议结束时执行，因此通常不需要手动重新转换。

## 查阅会议数据

会议结束后或进行中，可以通过以下路径读取相关文件：

（文件路径格式：`recordings/YYYY/MM/DD/{streamId}/`）

## 自定义提示信息

如果您希望调整会议总结的样式或分析内容，可以自定义相关的提示信息：

| 文件名 | 用途 | 自定义示例 |
|------|---------|----------------------|
| `summary_prompt.md` | 会议总结生成 | 概述格式（项目符号列表 vs 散文格式）、重点内容、长度设置 |
| `query.prompt.md` | 查询结果格式 | 响应内容的显示方式、详细程度设置 |
| `query.prompt_current_meeting.md` | 实时会议分析 | 会议中需要重点展示的内容 |
| `query.prompt_dialog_suggestions.md` | 对话建议的显示风格 | 正式 vs 非正式的语气、建议条数设置 |
| `query.prompt_sentiment_analysis.md` | 情感分析逻辑 | 自定义情感分析类别、阈值设置 |

**提示：** 修改相关文件前请先备份原始文件，以便在需要时恢复原始设置。