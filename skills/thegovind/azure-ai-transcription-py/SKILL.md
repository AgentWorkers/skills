---
name: azure-ai-transcription-py
description: |
  Azure AI Transcription SDK for Python. Use for real-time and batch speech-to-text transcription with timestamps and diarization.
  Triggers: "transcription", "speech to text", "Azure AI Transcription", "TranscriptionClient".
package: azure-ai-transcription
---

# Azure AI Transcription SDK for Python

这是一个用于 Azure AI Transcription（语音转文本）的客户端库，支持实时转录和批量转录功能。

## 安装

```bash
pip install azure-ai-transcription
```

## 环境变量

```bash
TRANSCRIPTION_ENDPOINT=https://<resource>.cognitiveservices.azure.com
TRANSCRIPTION_KEY=<your-key>
```

## 认证

使用订阅密钥进行认证（此客户端不支持 DefaultAzureCredential）：

```python
import os
from azure.ai.transcription import TranscriptionClient

client = TranscriptionClient(
    endpoint=os.environ["TRANSCRIPTION_ENDPOINT"],
    credential=os.environ["TRANSCRIPTION_KEY"]
)
```

## 批量转录

```python
job = client.begin_transcription(
    name="meeting-transcription",
    locale="en-US",
    content_urls=["https://<storage>/audio.wav"],
    diarization_enabled=True
)
result = job.result()
print(result.status)
```

## 实时转录

```python
stream = client.begin_stream_transcription(locale="en-US")
stream.send_audio_file("audio.wav")
for event in stream:
    print(event.text)
```

## 最佳实践

1. 当有多个说话者时，启用“对话记录”功能。
2. 对于存储在 blob 存储中的长文件，使用批量转录方式。
3. 采集时间戳以用于生成字幕。
4. 指定语言以提高识别准确性。
5. 在实时转录过程中处理流式数据传输的背压问题。
6. 转录任务完成后，关闭相应的转录会话。