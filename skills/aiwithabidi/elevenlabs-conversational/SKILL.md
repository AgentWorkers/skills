---
name: elevenlabs-conversational
description: Full ElevenLabs platform integration — text-to-speech, voice cloning, and Conversational AI agent creation. Not just TTS — build interactive voice agents with emotion control, streaming audio, and phone system integration. Use for voice synthesis, cloning, or building conversational AI agents.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, ElevenLabs API key
metadata: {"openclaw": {"emoji": "\ud83d\udde3\ufe0f", "requires": {"env": ["ELEVENLABS_API_KEY"]}, "primaryEnv": "ELEVENLABS_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# 🗣️ ElevenLabs Conversational

**不仅仅是文本转语音（TTS）——全面的语音交互AI功能。** 提供语音合成、语音克隆以及OpenClaw代理的语音交互AI代理创建服务。

## 语音合成与语音交互AI的对比

| 功能        | 语音合成（TTS）          | 语音交互AI        |
|------------|------------------|-------------------|
| 功能用途      | 将文本转换为语音          | 全面的语音交互代理     |
| 数据流向      | 单向传输              | 双向交互          |
| 应用场景      | 旁白、警报提示          | 电话客服、智能助手      |
| 延迟        | 批量处理即可          | 需要实时响应       |

现有的ElevenLabs功能仅支持文本转语音（TTS）。而此功能则涵盖了包括语音交互AI代理在内的**完整平台**。

## 所需参数

| 参数        | 是否必需 | 说明              |
|------------|-----------|-------------------|
| `ELEVENLABS_API_KEY` | ✅ | ElevenLabs API密钥        |

## 快速入门

```bash
# List available voices
python3 {baseDir}/scripts/elevenlabs_api.py voices

# Text to speech
python3 {baseDir}/scripts/elevenlabs_api.py tts "Hello world" --voice Rachel --output hello.mp3

# TTS with emotion control
python3 {baseDir}/scripts/elevenlabs_api.py tts "I'm so excited!" --voice Rachel --stability 0.3 --style 0.8

# Streaming TTS (lower latency)
python3 {baseDir}/scripts/elevenlabs_api.py tts-stream "Hello world" --voice Rachel --output hello.mp3

# List conversational AI agents
python3 {baseDir}/scripts/elevenlabs_api.py list-agents

# Create a conversational AI agent
python3 {baseDir}/scripts/elevenlabs_api.py create-agent --name "Support Bot" --voice Rachel --prompt "You are a helpful support agent."

# Get agent details
python3 {baseDir}/scripts/elevenlabs_api.py get-agent <agent_id>

# Voice cloning (instant)
python3 {baseDir}/scripts/elevenlabs_api.py clone-voice "My Voice" --files sample1.mp3 sample2.mp3
```

## 命令

### `voices`
列出所有可用的语音资源，包括ID、名称、类别和语言。

### `tts <text>`
将文本转换为语音（非流式输出）。
- `--voice NAME`  — 语音名称或ID（默认：Rachel）
- `--output FILE`  — 输出文件路径（默认：output.mp3）
- `--model ID`  — 使用的模型（默认：eleven_multilingual_v2）
- `--stability FLOAT`  — 0.0-1.0，数值越小表达越丰富（默认：0.5）
- `--similarity FLOAT`  — 0.0-1.0，语音相似度调整（默认：0.75）
- `--style FLOAT`  — 0.0-1.0，语音风格调整（默认：0.0）

### `tts-stream <text>`
流式文本转语音——延迟更低，数据到达时立即输出。
- 与`tts`命令选项相同

### `list-agents`
列出所有已创建的语音交互AI代理。

### `create-agent`
创建一个新的语音交互AI代理。
- `--name NAME`  — 代理名称
- `--voice NAME`  — 使用的语音资源
- `--prompt TEXT`  — 代理的系统提示语
- `--first-message TEXT`  — 问候语
- `--language CODE`  — 语言代码（默认：en）

### `get-agent <agent_id>`
获取某个语音交互AI代理的详细信息。

### `clone-voice <name>`
创建一个语音克隆版本。
- `--files FILE [FILE ...]`  — 音频样本文件（至少1个，建议3个以上）
- `--description TEXT`  — 语音描述

## 集成方式

### 与Twilio（电话服务）集成
1. 创建一个语音交互AI代理
2. 配置Twilio的Webhook以连接到ElevenLabs
3. 将来电路由到该AI代理处理

### 与Vapi集成
1. 在ElevenLabs中创建相应的语音资源
2. 在Vapi助手配置中使用该语音资源的ID
3. Vapi负责整体流程协调，ElevenLabs负责语音处理

### 与LiveKit集成
1. 通过流式API生成TTS音频
2. 将音频文件发布到LiveKit房间
3. 订阅参与者的音频数据以进行文本转语音处理

## 开发者信息
由[M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) | [agxntsix.ai](https://www.agxntsix.ai)开发
[YouTube频道](https://youtube.com/@aiwithabidi) | [GitHub仓库](https://github.com/aiwithabidi)
该功能属于**AgxntSix Skill Suite**的一部分，专为OpenClaw代理设计。

📅 **需要帮助为您的业务设置OpenClaw吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)