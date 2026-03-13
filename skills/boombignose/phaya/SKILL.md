---
name: phaya
description: 使用 Phaya SaaS 后端通过简单的 REST API 调用来生成图片、视频、音频和音乐，并运行大型语言模型（LLM）的聊天功能。当用户需要生成媒体内容、调用 AI 模型，或使用 Phaya API 进行图片/视频/音频/文本生成时，可以使用该服务。
metadata: {"clawdbot":{"emoji":"🎬","requires":{"anyBins":["curl","python3"],"optionalBins":["ffmpeg","yt-dlp"],"envVars":["PHAYA_API_KEY","PHAYA_BASE"]},"credentials":[{"name":"PHAYA_API_KEY","description":"Bearer token for the Phaya API. Obtain from your account dashboard after signing up at the Phaya host. Treat as sensitive — all generation endpoints deduct real credits.","required":true}],"os":["linux","darwin","win32"]}}
---
# Phaya Media API

Phaya 是一个基于 FastAPI 的后端服务，它能够将 AI 生成的媒体内容分发到多个平台，包括 KIE.ai（Sora 2、Veo 3.1、Seedance、Kling、Seedream、Suno）、Google Gemini TTS 以及 OpenRouter 的大语言模型（LLMs）。

## 认证

所有 API 端点都需要使用 Bearer 令牌或 API 密钥进行身份验证：

```
Authorization: Bearer <your_api_key>
```

在使用此服务之前，请设置以下环境变量：

```bash
export PHAYA_API_KEY="your_api_key_here"   # required — all endpoints
export PHAYA_BASE="https://your-api-host/api/v1"  # required — your Phaya instance URL
```

获取您的个人资料和信用余额：
- `GET /api/v1/user/profile` — 获取完整个人资料
- `GET /api/v1/user/credits` — 返回信用余额信息（例如：`{"credits_balance": 84.90, ...}`）

**请求速率限制：** 每个 API 密钥每分钟最多允许发送 60 次请求。

## 费用说明

此服务采用付费信用系统：每次生成媒体内容都会从您的账户中扣除相应的信用额度。视频生成的费用可能在 8 到 50 个信用额度之间。建议先使用费用较低的接口（如文本转图像接口，仅需 1 个信用额度）来测试服务是否正常工作。如果任务失败，系统会自动退还已扣除的信用额度；但成功完成任务后（即使您未使用该服务），信用额度也不会被退还。

**建议：** 为初始测试创建一个信用额度较低的 API 密钥。

## 信用系统

生成媒体内容时需要扣除相应的信用额度；任务失败时信用额度会自动退还。

| 信用额度 | 服务类型 |
|---------|---------|
| 0.5     | 图像转视频（使用本地 FFmpeg） |
| 1.0     | 文本转图像（使用 Z-Image） |
| 1.5     | Seedream 5.0     |
| 2–4     | Nano Banana 2（1K/2K/4K 分辨率） |
| 3.0     | 文本转音乐（使用 Suno） |
| 2–35     | Seedance 1.5 Pro（根据分辨率、时长和音频质量计费） |
| 8.0     | Sora 2 视频生成 |
| 1.21–1.82/秒 | Kling 2.6 动作控制（720p/1080p） |
| 15.0     | Veo 3.1 快速模式（`veo3_fast`） |
| 50.0     | Veo 3.1 高质量模式（`veo3`） |

## 任务处理与状态查询

所有媒体生成操作都是异步进行的。创建任务后，相关接口会立即返回一个 `job_id`；您需要通过查询状态接口来获取任务的实际进度。

```
POST /api/v1/<service>/create   →  { "job_id": "uuid" }
GET  /api/v1/<service>/status/{job_id}  →  { "status": "...", "<media>_url": "..." }
```

**状态代码说明：**
- 图像/音乐任务：`PENDING`、`QUEUED`、`PROCESSING`、`COMPLETED`、`FAILED`
- 语音/字幕任务：`PENDING`、`PROCESSING`、`COMPLETED`、`FAILED`
- 视频下载任务：`processing`、`completed`、`failed`、`cancelled`

**不同媒体类型的响应字段：**

| 媒体类型 | 响应字段         |
|------------|-------------------|
| 图像     | `image_url`        |
| 视频     | `video_url`        |
| 音频/音乐 | `audio_url`       | （音乐任务还会返回 `audio_urls[]`） |
| Sora 2 角色 | `character_id`     | （字符串格式的 ID，非 URL） |

请每隔 3–5 秒查询一次任务状态，直到任务完成。

## 快速入门

### 1. 生成图片（文本转图像）
```python
import httpx, time

BASE = "https://your-api-host/api/v1"
HEADERS = {"Authorization": "Bearer YOUR_API_KEY"}

r = httpx.post(f"{BASE}/text-to-image/generate", headers=HEADERS, json={
    "prompt": "A futuristic city at sunset, ultra-detailed",
    "aspect_ratio": "16:9"
})
job_id = r.json()["job_id"]

while True:
    s = httpx.get(f"{BASE}/text-to-image/status/{job_id}", headers=HEADERS).json()
    if s["status"] == "COMPLETED":
        print("Image URL:", s["image_url"])
        break
    if s["status"] == "FAILED":
        raise RuntimeError("Job failed")
    time.sleep(4)
```

### 2. 生成视频（Sora 2 文本转视频）
```python
r = httpx.post(f"{BASE}/sora2-text-to-video/create", headers=HEADERS, json={
    "prompt": "A dragon flying over mountains at dawn",
    "aspect_ratio": "landscape",
    "n_frames": "10"          # "10" or "15" as a string
})
job_id = r.json()["job_id"]
# Poll /sora2-text-to-video/status/{job_id} → s["video_url"]
```

### 3. 与 Phaya-GPT 进行交互
```python
r = httpx.post(f"{BASE}/phaya-gpt/chat/completions", headers=HEADERS, json={
    "messages": [{"role": "user", "content": "Hello, what can you do?"}],
    "stream": False
})
print(r.json()["message"]["content"])   # flat dict — NOT choices[0].message.content
```

## 额外资源

- 完整的 API 接口列表：[endpoints.md](endpoints.md)
- 各类服务的 Curl 和 Python 示例代码：[examples.md](examples.md)

## 本地运行要求

大多数功能仅需要 `python3`（或 `curl`）以及您的 API 密钥，因为所有 AI 处理都在远程服务器上完成。

**两个可选的本地运行功能：**
- `POST /image-to-video/create`（使用本地 FFmpeg）—— 需要安装 FFmpeg
- `POST /video-download/create`（使用 yt-dlp）—— 下载操作在 Phaya 服务器端通过 yt-dlp 完成，不依赖本地系统

此服务不依赖于任何本地 AI 模型、GPU 或高耗磁盘的操作。