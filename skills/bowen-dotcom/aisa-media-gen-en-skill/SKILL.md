---
name: openclaw-media-gen
description: "使用 AIsa，通过一个 API 密钥即可生成图像和视频：Gemini 3 Pro 用于生成图像，Qwen Wan 2.6 用于生成视频。"
homepage: https://openclaw.ai
metadata: {"openclaw":{"emoji":"🎬","requires":{"bins":["python3","curl"],"env":["AISA_API_KEY"]},"primaryEnv":"AISA_API_KEY"}}
---

# OpenClaw Media Gen 🎬

使用一个 AIsa API 密钥即可生成 **图片** 和 **视频**：

- **图片**：`gemini-3-pro-image-preview`（Gemini GenerateContent）
- **视频**：`wan2.6-t2v`（Qwen Wan 2.6 / Tongyi Wanxiang，异步任务）

API 参考：[AIsa API 参考](https://aisa.mintlify.app/api-reference/introduction)（所有页面可在 `https://aisa.mintlify.app/llms.txt` 查看）

## 🎯 价格优势

### 视频生成（WAN）- 成本对比

| 分辨率 | AIsa（合约） | AIsa（官方） | Bailian（官方） | OpenRouter |
|------------|-----------------|-----------------|-------------------|------------|
| 720P | **0.06 美元/秒** | 约 0.08 美元 | 约 0.10 美元 | ❌ |
| 1080P | **0.09 美元/秒** | 约 0.12 美元 | 约 0.15 美元 | ❌ |
| Pro/Animate | **0.108–0.156 美元** | 约 0.18 美元 | 约 0.25 美元 | ❌ |

**主要优势**：
- 比 Bailian 官方价格便宜 25-40%
- OpenRouter 不支持视频生成——AIsa 是唯一支持视频生成的统一 API
- 提供合约定价，适用于生产级工作负载
- 使用同一个 API 密钥即可生成图片和视频

## 🔥 您能做什么

### 图片生成（Gemini）
```
"Generate a cyberpunk cityscape at night, neon lights, rainy, cinematic"
```

### 视频生成（Wan 2.6）
```
"Use a reference image to generate a 5-second shot: slow camera push-in, wind blowing hair, cinematic, shallow depth of field"
```

## 快速入门

```bash
export AISA_API_KEY="your-key"
```

---

## 🖼️ 图片生成（Gemini）

### 端点

- 基础 URL：`https://api.aisa.one/v1`
- `POST /models/{model}:generateContent`

文档说明：`google-gemini-chat`（GenerateContent）请参阅 `https://aisa.mintlify.app/api-reference/chat/chat-api/google-gemini-chat.md`

### curl 示例（返回图片的 inline_data）

```bash
curl -X POST "https://api.aisa.one/v1/models/gemini-3-pro-image-preview:generateContent" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents":[
      {"role":"user","parts":[{"text":"A cute red panda, ultra-detailed, cinematic lighting"}]}
    ]
  }'
```

> 注意：响应中可能包含 `candidates[].parts[].inline_data`（通常包含 Base64 编码的数据和 MIME 类型）；客户端脚本会自动解析并保存文件。

---

## 🎞️ 视频生成（Qwen Wan 2.6 / Tongyi Wanxiang）

### 创建任务

- 基础 URL：`https://api.aisa.one/apis/v1`
- `POST /services/aigc/video-generation/video-synthesis`
- 请求头：`X-DashScope-Async: enable`（异步请求必需）

文档说明：`video-generation` 请参阅 `https://aisa.mintlify.app/api-reference/aliyun/video/video-generation.md`

```bash
curl -X POST "https://api.aisa.one/apis/v1/services/aigc/video-generation/video-synthesis" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-Async: enable" \
  -d '{
    "model":"wan2.6-t2v",
    "input":{
      "prompt":"cinematic close-up, slow push-in, shallow depth of field",
      "img_url":"https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/320px-Cat03.jpg"
    },
    "parameters":{
      "resolution":"720P",
      "duration":5,
      "shot_type":"single",
      "watermark":false
    }
  }'
```

### 查询任务状态

- `GET /services/aigc/tasks?task_id=...`

文档说明：`task` 请参阅 `https://aisa.mintlify.app/api-reference/aliyun/video/task.md`

```bash
curl "https://api.aisa.one/apis/v1/services/aigc/tasks?task_id=YOUR_TASK_ID" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

---

## Python 客户端

```bash
# Generate image (save to local file)
python3 {baseDir}/scripts/media_gen_client.py image \
  --prompt "A cute red panda, cinematic lighting" \
  --out "out.png"

# Create video task (requires img_url)
python3 {baseDir}/scripts/media_gen_client.py video-create \
  --prompt "cinematic close-up, slow push-in" \
  --img-url "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/320px-Cat03.jpg" \
  --duration 5

# Poll task status
python3 {baseDir}/scripts/media_gen_client.py video-status --task-id YOUR_TASK_ID

# Wait until success (optional: print video_url on success)
python3 {baseDir}/scripts/media_gen_client.py video-wait --task-id YOUR_TASK_ID --poll 10 --timeout 600

# Wait until success and auto-download mp4
python3 {baseDir}/scripts/media_gen_client.py video-wait --task-id YOUR_TASK_ID --download --out out.mp4
```

## 💡 使用场景

- **AI 代理**：自动化生成用于社交媒体和营销材料的视觉内容
- **内容创作者**：程序化生成自定义图片和视频
- **开发者**：构建具备多模态生成功能的应用程序
- **企业**：相比 Bailian，更具成本效益且价格更优

## 🚀 为什么选择 AIsa 进行媒体生成？

1. **统一 API**：一个 API 密钥即可生成图片（Gemini）和视频（WAN）
2. **最佳价格**：比其他服务便宜 25-40%
3. **适合生产环境**：提供合约定价和企业级支持
4. **无竞争对手**：OpenRouter 不支持视频生成
5. **集成简单**：内置 Python 客户端和异步任务管理功能