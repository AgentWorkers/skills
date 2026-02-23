---
name: elevenlabs-speech
description: 使用 ElevenLabs AI 的文本转语音（Text-to-Speech）和语音转文本（Speech-to-Text）功能。当用户需要将文本转换为语音、转录语音消息或处理多种语言的语音数据时，可以使用该功能。该服务支持高质量的人工智能语音，并提供准确的转录结果。
---

# ElevenLabs Speech

提供全面的语音解决方案——通过一个API同时支持文本转语音（TTS）和语音转文本（STT）功能：
- **TTS**：将文本转换为自然流畅的语音
- **STT**：使用ElevenLabs的Scribe工具将语音转换为文本（具有高准确率的转录服务）

## 快速入门

### 环境设置

设置您的API密钥：
```bash
export ELEVENLABS_API_KEY="sk_..."
```

或者在工作区根目录下创建一个`.env`文件。

### 文本转语音（TTS）

将文本转换为自然流畅的语音：
```bash
python scripts/elevenlabs_speech.py tts -t "Hello world" -o greeting.mp3
```

使用自定义语音：
```bash
python scripts/elevenlabs_speech.py tts -t "Hello" -v "voice_id_here" -o output.mp3
```

### 可用语音列表

```bash
python scripts/elevenlabs_speech.py voices
```

## 在代码中使用

```python
from scripts.elevenlabs_speech import ElevenLabsClient

client = ElevenLabsClient(api_key="sk_...")

# Basic TTS
result = client.text_to_speech(
    text="Hello from zerox",
    output_path="greeting.mp3"
)

# With custom settings
result = client.text_to_speech(
    text="Your text here",
    voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel
    stability=0.5,
    similarity_boost=0.75,
    output_path="output.mp3"
)

# Get available voices
voices = client.get_voices()
for voice in voices['voices']:
    print(f"{voice['name']}: {voice['voice_id']}")
```

## 热门语音

| 语音ID | 名称 | 描述 |
|----------|------|-------------|
| `21m00Tcm4TlvDq8ikWAM` | Rachel | 自然、音色多变（默认） |
| `AZnzlk1XvdvUeBnXmlld` | Domi | 音量大、充满活力 |
| `EXAVITQu4vr4xnSDxMaL` | Bella | 语调柔和、令人放松 |
| `ErXwobaYiN019PkySvjV` | Antoni | 音色均衡 |
| `MF3mGyEYCl7XYWbV9V6O` | Elli | 温暖、亲切 |
| `TxGEqnHWrfWFTfGW9XjX` | Josh | 低沉、沉稳 |
| `VR6AewLTigWG4xSOukaG` | Arnold | 音色权威 |

## 语音设置

- **稳定性**（0-1）：数值越低，情感表达越强烈；数值越高，语音越稳定
- **相似度增强**（0-1）：数值越高，转录结果越接近原始语音

默认设置：稳定性=0.5，相似度增强=0.75

## 可用模型

- `eleven_turbo_v2_5` - 转换速度快、音质高（默认）
- `eleven_multilingual_v2` - 非英语语言的最佳选择
- `eleven_monolingual_v1` - 仅支持英语

## 与Telegram集成

当用户发送文本消息并希望接收语音回复时：
```python
# Generate speech
result = client.text_to_speech(text=user_text, output_path="reply.mp3")

# Send via Telegram message tool with media path
message(action="send", media="path/to/reply.mp3", as_voice=True)
```

## 价格信息

请访问 https://elevenlabs.io/pricing 查看当前收费标准。提供免费试用计划！

## 使用ElevenLabs Scribe进行语音转文本（STT）

使用ElevenLabs的Scribe工具将语音消息转录为文本：

### 转录音频

```bash
python scripts/elevenlabs_scribe.py voice_message.ogg
```

支持指定语言：
```bash
python scripts/elevenlabs_scribe.py voice_message.ogg --language ara
```

支持识别多个说话者的语音：
```bash
python scripts/elevenlabs_scribe.py voice_message.ogg --speakers 2
```

## 在代码中使用

```python
from scripts.elevenlabs_scribe import ElevenLabsScribe

client = ElevenLabsScribe(api_key="sk-...")

# Basic transcription
result = client.transcribe("voice_message.ogg")
print(result['text'])

# With language hint (improves accuracy)
result = client.transcribe("voice_message.ogg", language_code="ara")

# With speaker detection
result = client.transcribe("voice_message.ogg", num_speakers=2)
```

### 支持的文件格式

- mp3, mp4, mpeg, mpga, m4a, wav, webm
- 文件大小上限：100 MB
- 非常适合处理Telegram中的语音消息（格式为`.ogg`）

### 语言支持

Scribe支持99种语言，包括：
- 阿拉伯语（`ara`）
- 英语（`eng`）
- 西班牙语（`spa`）
- 法语（`fra`）
- 以及更多语言……

如果没有指定语言，系统会自动检测语言。

## 完整工作流程示例

**用户发送语音消息 → 您用语音回复：**

```python
from scripts.elevenlabs_scribe import ElevenLabsScribe
from scripts.elevenlabs_speech import ElevenLabsClient

# 1. Transcribe user's voice message
stt = ElevenLabsScribe()
transcription = stt.transcribe("user_voice.ogg")
user_text = transcription['text']

# 2. Process/understand the text
# ... your logic here ...

# 3. Generate response text
response_text = "Your response here"

# 4. Convert to speech
tts = ElevenLabsClient()
tts.text_to_speech(response_text, output_path="reply.mp3")

# 5. Send voice reply
message(action="send", media="reply.mp3", as_voice=True)
```

## 价格信息

请访问 https://elevenlabs.io/pricing 查看当前收费标准：

**TTS（文本转语音）：**
- 免费试用：每月10,000个字符
- 提供付费套餐

**STT（语音转文本） - Scribe：**
- 提供免费试用
- 详情请访问官方网站查询当前价格