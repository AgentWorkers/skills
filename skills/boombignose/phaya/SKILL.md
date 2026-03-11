---
name: phaya
description: 使用 Phaya SaaS 后端通过简单的 REST API 调用来生成图片、视频、音频和音乐，并运行大型语言模型（LLM）的聊天功能。当用户需要生成媒体内容、调用 AI 模型，或使用 Phaya API 进行图片/视频/音频/文本生成时，可以使用该服务。
metadata: {"clawdbot":{"emoji":"🎬","requires":{"anyBins":["curl","python3"]},"os":["linux","darwin","win32"]}}
---
# Phaya Media API

Phaya 是一个基于 FastAPI 构建的后端服务，它能够将 AI 生成的媒体内容整合到多个平台中，包括 KIE.ai（Sora 2、Veo 3.1、Seedance、Kling、Seedream、Suno）、Google Gemini TTS 以及 OpenRouter 的大型语言模型（LLMs）。

## 认证

所有 API 端点都需要使用 Bearer 令牌或 API 密钥进行身份验证：

```
Authorization: Bearer <your_api_key>
```

**获取用户信息及信用余额：**
- `GET /api/v1/user/profile` — 获取完整用户信息
- `GET /api/v1/user/credits` → 返回信用余额（例如：`{"credits_balance": 84.90, ...}`）

**请求限制：** 每个 API 密钥每分钟最多允许 60 次请求。

## 信用系统

每次生成媒体内容都会消耗相应的信用点数；如果生成失败，系统会自动退还已消耗的信用点数。

| 信用点数 | 服务类型 |
|---------|---------|
| 0.5     | 图像转视频（使用 FFmpeg）/ Sora 2 角色创建 |
| 1.0     | 文本转图像（使用 Z-Image） |
| 1.5     | Seedream 5.0 |
| 2–4     | Nano Banana 2（1K/2K/4K 分辨率） |
| 3.0     | 文本转音乐（使用 Suno） |
| 2–35     | Seedance 1.5 Pro（根据分辨率、时长和音频质量计费） |
| 8.0     | Sora 2 视频生成 |
| 1.21–1.82/秒 | Kling 2.6 动作控制（720p/1080p） |
| 15.0     | Veo 3.1 快速模式（`veo3_fast`） |
| 50.0     | Veo 3.1 高质量模式（`veo3`） |

## 任务处理与状态查询

所有媒体生成操作都是异步进行的。创建任务时，API 会立即返回一个 `job_id`；您需要通过特定的状态查询端点来获取任务的实际执行进度。

```
POST /api/v1/<service>/create   →  { "job_id": "uuid" }
GET  /api/v1/<service>/status/{job_id}  →  { "status": "...", "<media>_url": "..." }
```

**状态码说明：**
- 图像/音乐相关端点：`PENDING`、`QUEUED`、`PROCESSING`、`COMPLETED`、`FAILED`
- 语音/字幕相关端点：`PENDING`、`PROCESSING`、`COMPLETED`、`FAILED`
- 视频下载相关端点：`processing`、`completed`、`failed`、`cancelled`

**不同媒体类型的响应字段：**

| 媒体类型 | 响应字段           |
|------------|-------------------|
| 图像     | `image_url`           |
| 视频     | `video_url`           |
| 音频/音乐 | `audio_url`         | （音乐生成时还会返回 `audio_urls[]`） |
| Sora 2 角色 | `character_id`       | （字符串形式的角色 ID，而非 URL） |

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

### 3. 与 Phaya-GPT 进行对话
```python
r = httpx.post(f"{BASE}/phaya-gpt/chat/completions", headers=HEADERS, json={
    "messages": [{"role": "user", "content": "Hello, what can you do?"}],
    "stream": False
})
print(r.json()["message"]["content"])   # flat dict — NOT choices[0].message.content
```

## 额外资源

- 完整的 API 端点列表：[endpoints.md](endpoints.md)
- 各服务类型的 Curl 和 Python 使用示例：[examples.md](examples.md)