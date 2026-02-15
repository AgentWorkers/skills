---
name: parakeet-stt
description: >-
  Local speech-to-text with NVIDIA Parakeet TDT 0.6B v3 (ONNX on CPU).
  30x faster than Whisper, 25 languages, auto-detection, OpenAI-compatible API.
  Use when transcribing audio files, converting speech to text, or processing
  voice recordings locally without cloud APIs.
homepage: https://github.com/groxaxo/parakeet-tdt-0.6b-v3-fastapi-openai
metadata: {"clawdbot":{"emoji":"🦜","env":["PARAKEET_URL"]}}
---

# Parakeet TDT（语音转文本）

使用 NVIDIA Parakeet TDT 0.6B v3 和 ONNX Runtime 进行本地转录。  
可在 CPU 上运行——无需 GPU；转录速度比实时转录快约 30 倍。  

## 安装  

```bash
# Clone the repo
git clone https://github.com/groxaxo/parakeet-tdt-0.6b-v3-fastapi-openai.git
cd parakeet-tdt-0.6b-v3-fastapi-openai

# Run with Docker (recommended)
docker compose up -d parakeet-cpu

# Or run directly with Python
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 5000
```  

默认端口为 `5000`。可以通过设置 `PARAKEET_URL` 来更改端口（例如：`http://localhost:5092`）。  

## API 端点  

提供与 OpenAI 兼容的 API，地址为 `$PARAKEET_URL`（默认：`http://localhost:5000`）。  

## 快速入门  

```bash
# Transcribe audio file (plain text)
curl -X POST $PARAKEET_URL/v1/audio/transcriptions \
  -F "file=@/path/to/audio.mp3" \
  -F "response_format=text"

# Get timestamps and segments
curl -X POST $PARAKEET_URL/v1/audio/transcriptions \
  -F "file=@/path/to/audio.mp3" \
  -F "response_format=verbose_json"

# Generate subtitles (SRT)
curl -X POST $PARAKEET_URL/v1/audio/transcriptions \
  -F "file=@/path/to/audio.mp3" \
  -F "response_format=srt"
```  

## Python / OpenAI SDK  

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url=os.getenv("PARAKEET_URL", "http://localhost:5000") + "/v1",
    api_key="not-needed"
)

with open("audio.mp3", "rb") as f:
    transcript = client.audio.transcriptions.create(
        model="parakeet-tdt-0.6b-v3",
        file=f,
        response_format="text"
    )
print(transcript)
```  

## 响应格式  

| 格式 | 输出内容 |
|--------|--------|
| `text` | 纯文本 |
| `json` | `{"text": "..."}` |
| `verbose_json` | 带时间戳和单词的文本片段 |
| `srt` | SRT 字幕 |
| `vtt` | WebVTT 字幕 |

## 支持的语言（共 25 种）  

英语、西班牙语、法语、德语、意大利语、葡萄牙语、波兰语、俄语、  
乌克兰语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、捷克语、  
罗马尼亚语、匈牙利语、保加利亚语、斯洛伐克语、克罗地亚语、立陶宛语、拉脱维亚语、  
爱沙尼亚语、斯洛文尼亚语  

语言会自动检测，无需额外配置。  

## Web 界面  

在浏览器中打开 `$PARAKEET_URL`，即可使用拖放功能进行转录操作。  

## Docker 管理  

```bash
# Check status
docker ps --filter "name=parakeet"

# View logs
docker logs -f <container-name>

# Restart
docker compose restart

# Stop
docker compose down
```  

## 为什么选择 Parakeet 而不是 Whisper？  

- **速度**：在 CPU 上的转录速度比实时转录快约 30 倍。  
- **准确性**：与 Whisper v3 的准确性相当。  
- **隐私保护**：所有处理完全在本地完成，无需使用云服务。  
- **兼容性**：可以替代 OpenAI 的转录 API。