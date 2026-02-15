---
name: deAPI AI Media Suite
description: 市场上最便宜的AI媒体API。它支持以下功能：转录YouTube视频、使用Flux和Z-Image模型生成图片、将文本转换为8种语言中的54种语音、通过OCR提取文本、创建视频、去除图片背景、图像放大处理以及应用风格转换——所有这些功能都可通过同一个统一的API实现。注册即可免费获得5美元的信用额度，足以支持数百小时的转录工作或数千张图片的生成。其价格仅为其他同类服务的几分之一。
homepage: https://deapi.ai
source: https://github.com/zrewolwerowanykaloryfer/deapi-clawdbot-skill
author: zrewolwerowanykaloryfer
license: MIT
requiredEnv:
  - DEAPI_API_KEY
metadata: {"clawdbot":{"requires":{"env":["DEAPI_API_KEY"]}}}
tags:
  - media
  - transcription
  - image-generation
  - tts
  - ocr
  - video
  - audio
  - embeddings
---

# deAPI 媒体生成服务

deAPI 提供了基于人工智能的媒体处理工具，这些工具通过去中心化的 GPU 网络实现。您可以在 [deapi.ai](https://deapi.ai) 获取 API 密钥（注册即可免费获得 5 美元信用额度）。

## 设置

```bash
export DEAPI_API_KEY=your_api_key_here
```

## 可用功能

| 功能 | 适用场景 |
|----------|---------------------------|
| 转录 | 转录 YouTube、Twitch、Kick、X 的视频或音频文件 |
| 生成图片 | 根据文本描述生成图片（使用 Flux 模型） |
| 生成音频 | 将文本转换为语音（TTS，支持 54 种以上语言，8 种语言） |
| 生成视频 | 根据文本生成视频或对图片进行动画处理 |
| OCR | 从图片中提取文本 |
| 去除背景 | 从图片中去除背景 |
| 图像放大 | 放大图片分辨率（2x/4x） |
| 图像转换 | 对图片应用风格转换（支持多张图片） |
| 生成文本嵌入 | 生成用于语义搜索的文本嵌入 |
| 查看余额 | 查看账户余额 |

---

## 异步操作模式（重要！）

**所有 deAPI 请求都是异步的。** 请按照以下模式进行操作：

### 1. 提交请求
```bash
curl -s -X POST "https://api.deapi.ai/api/v1/client/{endpoint}" \
  -H "Authorization: Bearer $DEAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

响应中包含 `request_id`。

### 2. 每 10 秒轮询一次请求状态
```bash
curl -s "https://api.deapi.ai/api/v1/client/request-status/{request_id}" \
  -H "Authorization: Bearer $DEAPI_API_KEY"
```

### 3. 处理状态
- `processing` → 等待 10 秒后再次轮询
- `done` → 从 `result_url` 获取结果
- `failed` → 向用户报告错误

### 常见错误处理
| 错误代码 | 处理方式 |
|-------|--------|
| 401 Unauthorized | 检查 DEAPI_API_KEY 是否正确 |
| 429 Rate Limited | 等待 60 秒后重试 |
| 500 Server Error | 等待 30 秒后重试一次 |

---

## 转录（YouTube、音频、视频）

**适用场景：** 用户希望将 YouTube、Twitch、Kick、X 或音频文件的内容转录为文本。

**端点：**
- 视频（YouTube 格式，mp4 或 webm）：`vid2txt`
- 音频（mp3、wav、m4a、flac、ogg）：`aud2txt`

**请求示例（视频）：**
```bash
curl -s -X POST "https://api.deapi.ai/api/v1/client/vid2txt" \
  -H "Authorization: Bearer $DEAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video_url": "{VIDEO_URL}", "include_ts": true, "model": "WhisperLargeV3"}'
```

**请求示例（音频）：**
```bash
curl -s -X POST "https://api.deapi.ai/api/v1/client/aud2txt" \
  -H "Authorization: Bearer $DEAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"audio_url": "{AUDIO_URL}", "include_ts": true, "model": "WhisperLargeV3"}'
```

**处理完成后：** 以可读格式显示带有时间戳的转录结果。

---

## 图像生成（Flux 模型）

**适用场景：** 用户希望根据文本描述生成图片。

**端点：** `txt2img`

**模型：**
| 模型 | API 名称 | 需要的步骤 | 最大图片数量 | 备注 |
|-------|----------|-------|----------|-------|
| Klein（默认） | `Flux_2_Klein_4B_BF16` | 4 张图片 | 最快，推荐使用 |
| Flux | `Flux1schnell` | 4-10 张图片 | 分辨率更高 |
| Turbo | `ZImageTurbo_INT8` | 4-10 张图片 | 推理速度最快 |

**请求示例：**
```bash
curl -s -X POST "https://api.deapi.ai/api/v1/client/txt2img" \
  -H "Authorization: Bearer $DEAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "{PROMPT}",
    "model": "Flux_2_Klein_4B_BF16",
    "width": 1024,
    "height": 1024,
    "steps": 4,
    "seed": {RANDOM_0_TO_999999}
  }'
```

**注意：** Klein 模型不支持 `guidance` 参数，请省略该参数。

---

## 文本转语音（54 种以上语言）

**适用场景：** 用户希望将文本转换为语音。

**端点：** `txt2audio`

**常用语音：**
| 语音 ID | 语言 | 特点 |
|----------|----------|-------------|
| `af_bella` | 美式英语 | 温暖、友好（音质最佳） |
| `af_heart` | 美式英语 | 表情丰富、富有情感 |
| `am_adam` | 美式英语 | 低沉、权威 |
| `bf_emma` | 英式英语 | 优雅（最佳英式发音） |
| `jf_alpha` | 日语 | 自然的女性日语发音 |
| `zf_xiaobei` | 中文 | 普通中文女性发音 |
| `ef_dora` | 西班牙语 | 西班牙语女性发音 |
| `ff_siwis` | 法语 | 法语女性发音（音质最佳） |

**请求示例：**
```bash
curl -s -X POST "https://api.deapi.ai/api/v1/client/txt2audio" \
  -H "Authorization: Bearer $DEAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "{TEXT}",
    "voice": "af_bella",
    "model": "Kokoro",
    "lang": "en-us",
    "speed": 1.0,
    "format": "mp3",
    "sample_rate": 24000
  }'
```

**参数：**
- `lang`：`en-us`、`en-gb`、`ja`、`zh`、`es`、`fr`、`hi`、`it`、`pt-br`
- `speed`：0.5-2.0
- `format`：mp3/wav/flac/ogg
- `sample_rate`：22050/24000/44100/48000

---

## 视频生成

**适用场景：** 用户希望根据文本生成视频或对图片进行动画处理。

**端点：**
- 根据文本生成视频：`txt2video`（multipart/form-data）
- 根据图片生成视频：`img2video`（multipart/form-data）

**⚠️ 重要提示：** 对于 `Ltxv_13B_0_9_8_Distilled_FP8` 模型：**
- `guidance` 参数必须设置为 0（最大值！
- `steps` 参数必须设置为 1（最大值！）
- `fps` 最小值为 30 帧/秒

**请求示例（根据文本生成视频）：**
```bash
curl -s -X POST "https://api.deapi.ai/api/v1/client/txt2video" \
  -H "Authorization: Bearer $DEAPI_API_KEY" \
  -F "prompt={PROMPT}" \
  -F "model=Ltxv_13B_0_9_8_Distilled_FP8" \
  -F "width=512" \
  -F "height=512" \
  -F "guidance=0" \
  -F "steps=1" \
  -F "frames=120" \
  -F "fps=30" \
  -F "seed={RANDOM_0_TO_999999}"
```

**参数：**
| 参数 | 是否必填 | 限制条件 | 说明 |
|-----------|----------|-------------|-------------|
| `prompt` | 是 | - | 视频描述 |
| `model` | 是 | - | 使用 `Ltxv_13B_0_9_8_Distilled_FP8` 模型 |
| `width` | 是 | 256-768 | 视频宽度（例如 512） |
| `height` | 是 | 256-768 | 视频高度（例如 512） |
| `guidance` | 是 | 必须设置为 0 |
| `steps` | 是 | 必须设置为 1 |
| `frames` | 是 | 30-300 | 帧数 |
| `fps` | 是 | 最小值为 30 帧/秒 |
| `seed` | 是 | 0-999999 | 随机种子值 |

**请求示例（根据图片生成视频）：**
```bash
# Download image first if URL provided
curl -s -o {LOCAL_IMAGE_PATH} "{IMAGE_URL}"

curl -s -X POST "https://api.deapi.ai/api/v1/client/img2video" \
  -H "Authorization: Bearer $DEAPI_API_KEY" \
  -F "first_frame_image=@{LOCAL_IMAGE_PATH}" \
  -F "prompt=gentle movement, cinematic" \
  -F "model=Ltxv_13B_0_9_8_Distilled_FP8" \
  -F "width=512" \
  -F "height=512" \
  -F "guidance=0" \
  -F "steps=1" \
  -F "frames=120" \
  -F "fps=30" \
  -F "seed={RANDOM_0_TO_999999}"
```

**注意：** 视频生成可能需要 1-3 分钟。

---

## OCR（图片转文本）

**适用场景：** 用户希望从图片中提取文本。

**端点：** `img2txt`（multipart/form-data）

**请求示例：**
```bash
# Download image first if URL provided
curl -s -o {LOCAL_IMAGE_PATH} "{IMAGE_URL}"

# Send OCR request
curl -s -X POST "https://api.deapi.ai/api/v1/client/img2txt" \
  -H "Authorization: Bearer $DEAPI_API_KEY" \
  -F "image=@{LOCAL_IMAGE_PATH}" \
  -F "model=Nanonets_Ocr_S_F16"
```

## 去除背景**

**适用场景：** 用户希望从图片中去除背景。

**端点：** `img-rmbg`（multipart/form-data）

**请求示例：**
```bash
# Download image first if URL provided
curl -s -o {LOCAL_IMAGE_PATH} "{IMAGE_URL}"

# Send remove-bg request
curl -s -X POST "https://api.deapi.ai/api/v1/client/img-rmbg" \
  -H "Authorization: Bearer $DEAPI_API_KEY" \
  -F "image=@{LOCAL_IMAGE_PATH}" \
  -F "model=Ben2"
```

**结果：** 生成带有透明背景的 PNG 图片。

---

## 图像放大（2x/4x）

**适用场景：** 用户希望放大或优化图片分辨率。

**端点：** `img-upscale`（multipart/form-data）

**模型：**
| 放大倍率 | 模型 |
|-------|-------|
| 2x | `RealESRGAN_x2` |
| 4x | `RealESRGAN_x4` |

**请求示例：**
```bash
# Download image first if URL provided
curl -s -o {LOCAL_IMAGE_PATH} "{IMAGE_URL}"

# Send upscale request
curl -s -X POST "https://api.deapi.ai/api/v1/client/img-upscale" \
  -H "Authorization: Bearer $DEAPI_API_KEY" \
  -F "image=@{LOCAL_IMAGE_PATH}" \
  -F "model=RealESRGAN_x4"
```

## 图像转换（风格转换）

**适用场景：** 用户希望改变图片风格、合并图片或应用 AI 效果。

**端点：** `img2img`（multipart/form-data）

**模型：**
| 模型 | API 名称 | 最大支持图片数量 | 是否需要指导信息 | 需要的步骤 | 备注 |
|-------|----------|------------|----------|-------|-------|
| Klein（默认） | `Flux_2_Klein_4B_BF16` | 3 张图片 | 不需要指导信息 | 4 张图片（固定步骤） | 速度更快，支持多张图片 |
| Qwen | `QwenImageEdit_Plus_NF4` | 1 张图片 | 7.5 步骤 | 10-50 步骤（默认 20 步） | 提供更多调整选项 |

**请求示例（Klein 模型，支持最多 3 张图片）：**
```bash
# Download images first
curl -s -o {LOCAL_IMAGE_1} "{IMAGE_URL_1}"
curl -s -o {LOCAL_IMAGE_2} "{IMAGE_URL_2}"  # optional

# Send transform request (Klein - no guidance)
curl -s -X POST "https://api.deapi.ai/api/v1/client/img2img" \
  -H "Authorization: Bearer $DEAPI_API_KEY" \
  -F "image=@{LOCAL_IMAGE_1}" \
  -F "image=@{LOCAL_IMAGE_2}" \
  -F "prompt={STYLE_PROMPT}" \
  -F "model=Flux_2_Klein_4B_BF16" \
  -F "steps=4" \
  -F "seed={RANDOM_0_TO_999999}"
```

**请求示例（Qwen 模型，生成高质量单张图片）：**
```bash
# Download image first
curl -s -o {LOCAL_IMAGE_1} "{IMAGE_URL}"

# Send transform request (Qwen - with guidance)
curl -s -X POST "https://api.deapi.ai/api/v1/client/img2img" \
  -H "Authorization: Bearer $DEAPI_API_KEY" \
  -F "image=@{LOCAL_IMAGE_1}" \
  -F "prompt={STYLE_PROMPT}" \
  -F "model=QwenImageEdit_Plus_NF4" \
  -F "guidance=7.5" \
  -F "steps=20" \
  -F "seed={RANDOM_0_TO_999999}"
```

**示例指令：** “转换为水彩画风格”、“动漫风格”、“赛博朋克风格”

---

## 生成文本嵌入

**适用场景：** 用户需要文本嵌入以用于语义搜索、聚类或 RAG（Retrieval-Agnostic Generation）任务。

**端点：** `txt2embedding`

**请求示例：**
```bash
curl -s -X POST "https://api.deapi.ai/api/v1/client/txt2embedding" \
  -H "Authorization: Bearer $DEAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": "{TEXT}", "model": "Bge_M3_FP16"}'
```

**结果：** 生成一个 1024 维的向量（BGE-M3，支持多语言）

---

## 查看余额

**适用场景：** 用户希望查看剩余的信用额度。

**请求示例：**
```bash
curl -s "https://api.deapi.ai/api/v1/client/balance" \
  -H "Authorization: Bearer $DEAPI_API_KEY"
```

**响应示例：** `{ "data": { "balance": 4.25 } }`

---

## 价格（仅供参考）

| 功能 | 费用 |
|-----------|------|
| 转录 | 约 0.02 美元/小时 |
| 图像生成 | 约 0.002 美元/张图片 |
| TTS | 约 0.001 美元/1000 个字符 |
| 视频生成 | 约 0.05 美元/视频 |
| OCR | 约 0.001 美元/张图片 |
| 去除背景 | 约 0.001 美元/张图片 |
| 图像放大 | 约 0.002 美元/张图片 |
| 生成文本嵌入 | 约 0.0001 美元/1000 个文本嵌入 |

在 [deapi.ai](https://deapi.ai) 注册即可免费获得 5 美元信用额度。

---

*本文档源自 [deapi-ai/claude-code-skills](https://github.com/deapi-ai/claude-code-skills)，适用于 Clawdbot/OpenClaw。*

---

## 安全与隐私声明

本文档介绍了 **deAPI.ai** 的 REST API，这是一个合法的去中心化 AI 媒体服务。

**安全说明：**
- 所有的 `curl` 命令仅用于演示如何调用 API |
- 请求会被发送到 `api.deapi.ai`（deAPI 的官方端点） |
- 文档中的本地文件路径（如 `{LOCAL_IMAGE_PATH}` 仅为占位符，请使用实际的临时文件夹路径 |
- 该技能本身不执行任何代码或下载二进制文件 |
- 使用 API 时需要提供 API 密钥，该密钥需通过 `DEAPI_API_KEY` 环境变量设置 |

**隐私注意事项：**
- 用户提交的媒体链接（如 YouTube 视频链接、图片）会被发送到 deapi.ai 进行处理 |
- 生成的结果会通过 `result_url` 返回，该链接可能暂时可访问 |
- 结果会存储在 deAPI 的服务器上，请查阅其隐私政策以了解数据保留详情 |
- 请勿处理敏感或机密的媒体文件 |

**服务来源：** [deapi.ai](https://deapi.ai)  
**原始文档来源：** [github.com/deapi-ai/claude-code-skills](https://github.com/deapi-ai/claude-code-skills)  
**API 文档：** [docs.deapi.ai](https://docs.deapi.ai)