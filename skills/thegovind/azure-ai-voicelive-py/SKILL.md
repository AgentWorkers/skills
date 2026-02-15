---
name: azure-ai-voicelive-py
description: 使用 Azure AI Voice Live SDK (azure-ai-voicelive) 构建实时语音 AI 应用程序。在开发需要与 Azure AI 进行实时双向音频通信的 Python 应用程序时，可运用此技能，例如语音助手、支持语音功能的聊天机器人、实时语音转语音翻译系统、由语音控制的虚拟形象（avatar），或任何基于 WebSocket 的音频流服务（这些服务都依赖于 AI 模型）。该 SDK 支持服务器端语音活动检测（Server VAD）、轮流对话模式、函数调用、虚拟形象集成以及语音转文字（transcription）功能。
package: azure-ai-voicelive
---

# Azure AI Voice Live SDK

使用双向WebSocket通信构建实时语音AI应用程序。

## 安装

```bash
pip install azure-ai-voicelive aiohttp azure-identity
```

## 环境变量

```bash
AZURE_COGNITIVE_SERVICES_ENDPOINT=https://<region>.api.cognitive.microsoft.com
# For API key auth (not recommended for production)
AZURE_COGNITIVE_SERVICES_KEY=<api-key>
```

## 认证

**推荐使用：DefaultAzureCredential**：
```python
from azure.ai.voicelive.aio import connect
from azure.identity.aio import DefaultAzureCredential

async with connect(
    endpoint=os.environ["AZURE_COGNITIVE_SERVICES_ENDPOINT"],
    credential=DefaultAzureCredential(),
    model="gpt-4o-realtime-preview",
    credential_scopes=["https://cognitiveservices.azure.com/.default"]
) as conn:
    ...
```

**API密钥**：
```python
from azure.ai.voicelive.aio import connect
from azure.core.credentials import AzureKeyCredential

async with connect(
    endpoint=os.environ["AZURE_COGNITIVE_SERVICES_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_COGNITIVE_SERVICES_KEY"]),
    model="gpt-4o-realtime-preview"
) as conn:
    ...
```

## 快速入门

```python
import asyncio
import os
from azure.ai.voicelive.aio import connect
from azure.identity.aio import DefaultAzureCredential

async def main():
    async with connect(
        endpoint=os.environ["AZURE_COGNITIVE_SERVICES_ENDPOINT"],
        credential=DefaultAzureCredential(),
        model="gpt-4o-realtime-preview",
        credential_scopes=["https://cognitiveservices.azure.com/.default"]
    ) as conn:
        # Update session with instructions
        await conn.session.update(session={
            "instructions": "You are a helpful assistant.",
            "modalities": ["text", "audio"],
            "voice": "alloy"
        })
        
        # Listen for events
        async for event in conn:
            print(f"Event: {event.type}")
            if event.type == "response.audio_transcript.done":
                print(f"Transcript: {event.transcript}")
            elif event.type == "response.done":
                break

asyncio.run(main())
```

## 核心架构

### 连接资源

`VoiceLiveConnection` 提供了以下连接资源：

| 资源 | 用途 | 主要方法 |
|----------|---------|-------------|
| `conn.session` | 会话配置 | `update(session=...)` |
| `conn.response` | 模型响应 | `create()`, `cancel()` |
| `conn.input_audio_buffer` | 音频输入 | `append()`, `commit()`, `clear()` |
| `conn.output_audio_buffer` | 音频输出 | `clear()` |
| `conn.conversation` | 对话状态 | `item.create()`, `item.delete()`, `item.truncate()` |
| `conn.transcription_session` | 文本转语音配置 | `update(session=...)` |

## 会话配置

```python
from azure.ai.voicelive.models import RequestSession, FunctionTool

await conn.session.update(session=RequestSession(
    instructions="You are a helpful voice assistant.",
    modalities=["text", "audio"],
    voice="alloy",  # or "echo", "shimmer", "sage", etc.
    input_audio_format="pcm16",
    output_audio_format="pcm16",
    turn_detection={
        "type": "server_vad",
        "threshold": 0.5,
        "prefix_padding_ms": 300,
        "silence_duration_ms": 500
    },
    tools=[
        FunctionTool(
            type="function",
            name="get_weather",
            description="Get current weather",
            parameters={
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        )
    ]
))
```

## 音频流

### 发送音频（Base64 PCM16格式）

```python
import base64

# Read audio chunk (16-bit PCM, 24kHz mono)
audio_chunk = await read_audio_from_microphone()
b64_audio = base64.b64encode(audio_chunk).decode()

await conn.input_audio_buffer.append(audio=b64_audio)
```

### 接收音频

```python
async for event in conn:
    if event.type == "response.audio.delta":
        audio_bytes = base64.b64decode(event.delta)
        await play_audio(audio_bytes)
    elif event.type == "response.audio.done":
        print("Audio complete")
```

## 事件处理

```python
async for event in conn:
    match event.type:
        # Session events
        case "session.created":
            print(f"Session: {event.session}")
        case "session.updated":
            print("Session updated")
        
        # Audio input events
        case "input_audio_buffer.speech_started":
            print(f"Speech started at {event.audio_start_ms}ms")
        case "input_audio_buffer.speech_stopped":
            print(f"Speech stopped at {event.audio_end_ms}ms")
        
        # Transcription events
        case "conversation.item.input_audio_transcription.completed":
            print(f"User said: {event.transcript}")
        case "conversation.item.input_audio_transcription.delta":
            print(f"Partial: {event.delta}")
        
        # Response events
        case "response.created":
            print(f"Response started: {event.response.id}")
        case "response.audio_transcript.delta":
            print(event.delta, end="", flush=True)
        case "response.audio.delta":
            audio = base64.b64decode(event.delta)
        case "response.done":
            print(f"Response complete: {event.response.status}")
        
        # Function calls
        case "response.function_call_arguments.done":
            result = handle_function(event.name, event.arguments)
            await conn.conversation.item.create(item={
                "type": "function_call_output",
                "call_id": event.call_id,
                "output": json.dumps(result)
            })
            await conn.response.create()
        
        # Errors
        case "error":
            print(f"Error: {event.error.message}")
```

## 常见模式

### 手动切换模式（无语音活动检测，No VAD）

```python
await conn.session.update(session={"turn_detection": None})

# Manually control turns
await conn.input_audio_buffer.append(audio=b64_audio)
await conn.input_audio_buffer.commit()  # End of user turn
await conn.response.create()  # Trigger response
```

### 中断处理

```python
async for event in conn:
    if event.type == "input_audio_buffer.speech_started":
        # User interrupted - cancel current response
        await conn.response.cancel()
        await conn.output_audio_buffer.clear()
```

### 对话历史记录

```python
# Add system message
await conn.conversation.item.create(item={
    "type": "message",
    "role": "system",
    "content": [{"type": "input_text", "text": "Be concise."}]
})

# Add user message
await conn.conversation.item.create(item={
    "type": "message",
    "role": "user", 
    "content": [{"type": "input_text", "text": "Hello!"}]
})

await conn.response.create()
```

## 语音选项

| 语音效果 | 描述 |
|-------|-------------|
| `alloy` | 中性、平衡的语音效果 |
| `echo` | 温暖、适合对话的语音效果 |
| `shimmer` | 清晰、专业的语音效果 |
| `sage` | 平静、权威的语音效果 |
| `coral` | 友善、欢快的语音效果 |
| `ash` | 深沉、稳重的语音效果 |
| `ballad` | 表现力丰富的语音效果 |
| `verse` | 适合故事叙述的语音效果 |

Azure 提供的语音模型：`AzureStandardVoice`, `AzureCustomVoice`, `AzurePersonalVoice`。

## 音频格式

| 格式 | 采样率 | 适用场景 |
|--------|-------------|----------|
| `pcm16` | 24kHz | 默认格式，高质量 |
| `pcm16-8000hz` | 8kHz | 适用于电话通话 |
| `pcm16-16000hz` | 16kHz | 适用于语音助手 |
| `g711_ulaw` | 8kHz | 适用于美国地区的电话通话 |
| `g711_alaw` | 8kHz | 适用于欧洲地区的电话通话 |

## 语音活动检测（Voice Activity Detection, VAD）选项

```python
# Server VAD (default)
{"type": "server_vad", "threshold": 0.5, "silence_duration_ms": 500}

# Azure Semantic VAD (smarter detection)
{"type": "azure_semantic_vad"}
{"type": "azure_semantic_vad_en"}  # English optimized
{"type": "azure_semantic_vad_multilingual"}
```

## 错误处理

```python
from azure.ai.voicelive.aio import ConnectionError, ConnectionClosed

try:
    async with connect(...) as conn:
        async for event in conn:
            if event.type == "error":
                print(f"API Error: {event.error.code} - {event.error.message}")
except ConnectionClosed as e:
    print(f"Connection closed: {e.code} - {e.reason}")
except ConnectionError as e:
    print(f"Connection error: {e}")
```

## 参考资料

- **详细API参考**：请参阅 [references/api-reference.md](references/api-reference.md)
- **完整示例**：请参阅 [references/examples.md](references/examples.md)
- **所有模型与类型**：请参阅 [references/models.md](references/models.md)