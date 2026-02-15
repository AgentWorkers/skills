---
name: podcast-generation
description: 使用 Azure OpenAI 的 GPT Realtime Mini 模型，通过 WebSocket 生成基于 AI 的播客风格音频叙事。该技术适用于构建文本转语音功能、音频叙事生成、从文本内容创建播客，或与 Azure OpenAI Realtime API 集成以实现实时音频输出。涵盖了从 React 前端到 Python FastAPI 后端的完整栈实现，包括 WebSocket 流传输。
---

# 使用 GPT Realtime Mini 生成播客内容

利用 Azure OpenAI 的 Realtime API 从文本内容生成真实的音频叙述。

## 快速入门

1. 配置 Realtime API 的环境变量
2. 通过 WebSocket 连接到 Azure OpenAI 的实时端点
3. 发送文本提示，接收 PCM 音频数据及文字转录结果
4. 将 PCM 数据转换为 WAV 格式
5. 将编码后的音频数据以 Base64 格式返回给前端进行播放

## 环境配置

```env
AZURE_OPENAI_AUDIO_API_KEY=your_realtime_api_key
AZURE_OPENAI_AUDIO_ENDPOINT=https://your-resource.cognitiveservices.azure.com
AZURE_OPENAI_AUDIO_DEPLOYMENT=gpt-realtime-mini
```

**注意**：端点地址中不应包含 `/openai/v1/`，只需提供基础 URL 即可。

## 核心工作流程

### 后端音频生成

```python
from openai import AsyncOpenAI
import base64

# Convert HTTPS endpoint to WebSocket URL
ws_url = endpoint.replace("https://", "wss://") + "/openai/v1"

client = AsyncOpenAI(
    websocket_base_url=ws_url,
    api_key=api_key
)

audio_chunks = []
transcript_parts = []

async with client.realtime.connect(model="gpt-realtime-mini") as conn:
    # Configure for audio-only output
    await conn.session.update(session={
        "output_modalities": ["audio"],
        "instructions": "You are a narrator. Speak naturally."
    })
    
    # Send text to narrate
    await conn.conversation.item.create(item={
        "type": "message",
        "role": "user",
        "content": [{"type": "input_text", "text": prompt}]
    })
    
    await conn.response.create()
    
    # Collect streaming events
    async for event in conn:
        if event.type == "response.output_audio.delta":
            audio_chunks.append(base64.b64decode(event.delta))
        elif event.type == "response.output_audio_transcript.delta":
            transcript_parts.append(event.delta)
        elif event.type == "response.done":
            break

# Convert PCM to WAV (see scripts/pcm_to_wav.py)
pcm_audio = b''.join(audio_chunks)
wav_audio = pcm_to_wav(pcm_audio, sample_rate=24000)
```

### 前端音频播放

```javascript
// Convert base64 WAV to playable blob
const base64ToBlob = (base64, mimeType) => {
  const bytes = atob(base64);
  const arr = new Uint8Array(bytes.length);
  for (let i = 0; i < bytes.length; i++) arr[i] = bytes.charCodeAt(i);
  return new Blob([arr], { type: mimeType });
};

const audioBlob = base64ToBlob(response.audio_data, 'audio/wav');
const audioUrl = URL.createObjectURL(audioBlob);
new Audio(audioUrl).play();
```

## 语音选项

| 语音 | 特性       |
|-------|-----------|
| alloy | 中性音色       |
| echo | 温暖的音色     |
| fable | 表达力强的音色   |
| onyx | 深沉的音色     |
| nova | 友好的音色     |
| shimmer | 清晰的音色     |

## Realtime API 的事件响应

- `response.output_audio_delta`：Base64 编码的音频数据块
- `response.output_audio_transcript_delta`：文字转录结果
- `response.done`：生成完成
- `error`：处理错误信息（使用 `event.error.message`）

## 音频格式

- **输入**：文本提示
- **输出**：PCM 格式的音频（24kHz、16位、单声道）
- **存储方式**：Base64 编码的 WAV 文件

## 参考资料

- **完整架构**：请参阅 [references/architecture.md](references/architecture.md) 了解完整的系统架构设计
- **代码示例**：请参阅 [references/code-examples.md](references/code-examples.md) 了解实际开发中的代码模式
- **PCM 转换**：使用 [scripts/pcm_to_wav.py](scripts/pcm_to_wav.py) 脚本进行音频格式转换