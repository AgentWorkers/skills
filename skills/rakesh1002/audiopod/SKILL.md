---
name: audiopod
description: 使用 AudioPod AI 的 API 执行音频处理任务，包括 AI 音乐生成（文本转音乐、文本转说唱、器乐片段、人声）、音频元素分离（将歌曲分解为人声和乐器部分）、文本转语音、降噪、语音转文本、说话者分离以及媒体文件提取等。当用户需要根据文本生成音乐或说唱内容、将歌曲拆分为人声和乐器部分、从文本生成语音、清理带有噪音的音频文件、转录音频或视频内容，或从 YouTube 或其他 URL 中提取音频文件时，可以使用该 API。使用该 API 需要设置 `AUDIOPOD_API_KEY` 环境变量，或直接提供 API 密钥。
---

# AudioPod AI

提供全面的音频处理服务：音乐生成、音频元素分离（stem separation）、文本转语音（TTS）、降噪、音频转文字（transcription）、语音分离（speaker separation）以及钱包管理（wallet management）。

## 设置

```bash
pip install audiopod  # Python
npm install audiopod  # Node.js
```

**身份验证：**  
设置环境变量 `AUDIOPOD_API_KEY`，或将其传递给客户端构造函数。

### 获取 API 密钥  
1. 在 https://audiopod.ai/auth/signup 注册（免费，无需信用卡）  
2. 访问 https://www.audiopod.ai/dashboard/account/api-keys  
3. 点击 “Create API Key” 并复制密钥（密钥以 `ap_` 开头）  
4. 在 https://www.audiopod.ai/dashboard/account/wallet 为钱包充值（按需支付，无需订阅）

```python
from audiopod import AudioPod
client = AudioPod()  # uses AUDIOPOD_API_KEY env var
# or: client = AudioPod(api_key="ap_...")
```

---

## AI 音乐生成  
根据文本提示生成歌曲、说唱、器乐曲目、音效样本和人声。  
**支持的功能：**  
`text2music`（带人声的歌曲）、`text2rap`（说唱）、`prompt2instrumental`（纯器乐）、`lyric2vocals`（仅人声）、`text2samples`（循环音效）、`audio2audio`（风格转换）、`songbloom`  

### Python SDK  
[相关代码块]  

### cURL  
[相关代码块]  

### 参数  
| 参数 | 是否必填 | 说明 |  
|-------|----------|-------------|  
| prompt | 是 | 音乐风格/类型描述 |  
| lyrics | （用于歌曲/说唱/人声） | 带副歌结构的歌词 |  
| audio_duration | 否 | 音频时长（秒，默认：30秒） |  
| genre_preset | 否 | 预设的音乐类型（从预设端点获取） |  
| display_name | 否 | 曲目显示名称 |  

---

## 音频元素分离  
将音频分离成单独的乐器/人声轨道。  
**分离模式：**  
| 模式 | 分离的音频元素 | 输出结果 | 适用场景 |  
|------|-------|--------|----------|  
| single | 1 | 仅分离指定元素 | 仅提取人声或鼓声 |  
| two | 2 | 人声 + 乐器 | 卡拉OK曲目 |  
| four | 4 | 人声、鼓声、贝斯、其他音效 | 标准混音模式（默认） |  
| six | 6 | 人声、鼓声、吉他、钢琴 | 完整的乐器分离 |  
| producer | 8 | 人声、踢鼓、军鼓、钹 | 节奏制作 |  
| studio | 12 | 人声、钹、低音贝斯、合成器 | 专业混音 |  
| mastering | 16 | 最高精度分离 | 用于司法分析 |  
**可分离的音频元素：** 人声、鼓声、贝斯、吉他、钢琴、其他音效  

### Python SDK  
[相关代码块]  

### cURL  
[相关代码块]  

### 响应格式  
[相关代码块]  

---

## 文本转语音（Text to Speech）  
可将文本转换为多种语言的语音，支持50多种语言，支持语音克隆功能。  
**语音类型：**  
- **50多种可用于制作的音色** — 支持60多种语言，自动检测语言类型  
- **自定义语音克隆** — 可根据约5秒的音频样本克隆任意语音  

### Python SDK  
[相关代码块]  

### cURL（原始HTTP请求，最可靠）  
[相关代码块]  

### 生成参数  
| 参数 | 是否必填 | 说明 |  
|-------|----------|-------------|  
| input_text | 是 | 需转换的文本（最多5000个字符）；使用 `input_text` 时通过原始HTTP请求，使用 `text` 时通过SDK请求 |  
| audio_format | 否 | 音频格式（mp3、wav、ogg，默认：mp3） |  
| speed | 否 | 语速（0.25–4.0，默认：1.0） |  
| language | 否 | 语言代码（省略时自动检测） |  

### 响应格式  
[相关代码块]  

### 注意事项：**  
- 原始HTTP请求使用 `input_text` 作为参数，而非 `text`  
- SDK请求使用 `text` 作为参数  
- 输出文件可能为伪装成 `.mp3` 格式的 `.wav` 文件，可使用 `ffmpeg` 转换为 `.mp4a`  
- 每次生成服务需支付约55个信用点数，费用从钱包中扣除  

---

## 语音分离（Speaker Separation）  
自动识别并分离音频中不同说话者的声音。  
**Python SDK**  
[相关代码块]  

### cURL**  
[相关代码块]  

---

## 文本转语音（Speech to Text）  
将带有说话者信息的音频/视频转换为文本，支持单词级别的时间戳和多种输出格式。  
**Python SDK**  
[相关代码块]  

### 参数  
| 参数 | 是否必填 | 说明 |  
|-------|----------|-------------|  
| url / urls | 是 | 需转换的音频/视频链接（如YouTube、SoundCloud链接） |  
| language | 否 | 语言代码（ISO 639-1，省略时自动检测） |  
| enable_speaker_diarization | 否 | 是否启用说话者识别（默认：关闭） |  
| min_speakers / max_speakers | 否 | 提供说话者数量建议以优化识别效果 |  
| word_timestamps | 否 | 是否启用单词级时间戳（默认：开启） |  

### 输出格式：**  
- **json**：结构化输出，包含音频片段、时间戳和说话者信息  
- **srt**：SubRip字幕格式  
- **vtt**：WebVTT字幕格式  
- **txt**：纯文本转录结果  

---

## 降噪（Noise Reduction）  
去除音频/视频文件中的背景噪音。  
**Python SDK**  
[相关代码块]  

### cURL**  
[相关代码块]  

---

## 钱包与计费  
查看账户余额、估算费用及使用记录。  
**Python SDK**  
[相关代码块]  

### API 端点概览  
| 服务 | 端点 | 方法 |  
|---------|----------|--------|  
| **音乐** | `/api/v1/music/{task}` | POST |  
| 音乐任务 | `/api/v1/music/jobs/{id}` | GET/DELETE |  
| 音乐预设 | `/api/v1/music/presets` | GET |  
| **音频元素分离** | `/api/v1/stem-extraction/api/extract` | POST（multipart） |  
| 分离结果状态 | `/api/v1/stem-extraction/status/{id}` | GET |  
| 分离模式 | `/api/v1/stem-extraction/modes` | GET |  
| 分离任务 | `/api/v1/stem-extraction/jobs` | GET |  
| **文本转语音** | `/api/v1/voice/voices/{uuid}/generate` | POST（表单数据） |  
| SDK接口 | `/api/v1/voice/tts/generate` | POST（JSON） |  
| TTS状态 | `/api/v1/voice/tts-jobs/{id}/status` | GET |  
| TTS状态（SDK） | `/api/v1/voice/tts/status/{id}` | GET |  
| 语音列表 | `/api/v1/voice/voice-profiles` | GET |  
| 语音列表（SDK） | `/api/v1/voice/voices` | GET |  
| **语音识别** | `/api/v1/speaker/diarize` | POST（multipart） |  
| 语音识别任务 | `/api/v1/speaker/jobs/{id}` | GET/DELETE |  
| **文本转语音** | `/api/v1/transcribe/transcribe` | POST（JSON） |  
| 上传转录文件 | `/api/v1/transcribe/transcribe-upload` | POST（multipart） |  
| 转录结果 | `/api/v1/transcribe/jobs/{id}/transcript?format=` | GET |  
| 转录任务 | `/api/v1/transcribe/jobs` | GET |  
| **降噪** | `/api/v1/denoiser/denoise` | POST（multipart） |  
| 降噪任务 | `/api/v1/denoiser/jobs/{id}` | GET/DELETE |  
| **钱包** | `/api/v1/api-wallet/balance` | GET |  
| 钱包定价 | `/api/v1/api-wallet/pricing` | GET |  
| 钱包使用情况 | `/api/v1/api-wallet/usage` | GET |  

## 身份验证头信息**  
有两种身份验证方式：  
- `X-API-Key: ap_...` — 适用于大多数端点  
- `Authorization: Bearer ap_...` — 适用于文本转语音相关操作  

## 注意事项：**  
- SDK的方法签名可能与原始API有所不同；如有疑问，请参考cURL示例  
- TTS输出文件存储在Cloudflare R2上，可通过 `output_url` 下载  
- TTS输出文件可能为伪装成 `.mp3` 格式的 `.wav` 文件，发送前需使用 `ffmpeg` 转换为 `.mp4a`