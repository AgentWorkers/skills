---
name: voice-assistant
description: >
  Windows voice companion for OpenClaw. Custom wake word via Porcupine,
  local STT via faster-whisper, streamed responses over the gateway WebSocket,
  and ElevenLabs TTS with natural chime/thinking sounds. Supports multi-turn
  conversation with automatic follow-up listening, mic suppression to prevent
  feedback, and a system tray with pause/resume. Recommended voices:
  Matilda (XrExE9yKIg1WjnnlVkGX, free tier) or Ivy (MClEFoImJXBTgLwdLI5n,
  paid tier). Fully customizable wake word, voice, hotkey, and silence thresholds.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎙️",
        "os": ["win32"],
        "requires":
          {
            "bins": ["python"],
            "env":
              [
                "GATEWAY_TOKEN",
                "GATEWAY_URL",
                "ELEVENLABS_API_KEY",
                "PORCUPINE_ACCESS_KEY",
              ],
          },
        "primaryEnv": "ELEVENLABS_API_KEY",
      },
  }
---

# OpenClaw语音助手

这是一个基于Python的辅助应用程序，它为OpenClaw添加了语音功能。您只需说出唤醒词（或按下热键），然后自然地说话，就能听到AI的回应——接着您可以继续进行多轮对话。

```
Mic → Porcupine wake word → faster-whisper STT → OpenClaw Gateway → ElevenLabs TTS → Speaker
```

## 快速入门

```bash
# 1. Navigate to the skill scripts
cd {baseDir}/scripts

# 2. Create a virtual environment and install dependencies
python -m venv venv
venv\Scripts\pip install -r requirements.txt

# 3. Copy .env.example to .env and fill in your keys
copy .env.example .env

# 4. Run the assistant
venv\Scripts\python src\assistant.py
```

## 所需条件

| 服务 | 所需内容 | 费用 |
|---------|--------------|------|
| **OpenClaw网关** | 需要在本地运行于 `ws://127.0.0.1:18789` 并使用网关令牌 | — |
| **ElevenLabs** | API密钥 + 语音ID（免费 tier 支持默认语音） | 免费 |
| **Picovoice** | 从 [picovoice.ai](https://picovoice.ai) 获取访问密钥（免费 tier 可使用） | 免费 |
| **Python** | 3.10及以上版本（测试版本为3.14） | — |
| **麦克风** | 任意输入设备 | — |

## 配置文件（.env）

```ini
# OpenClaw Gateway
GATEWAY_URL=ws://127.0.0.1:18789
GATEWAY_TOKEN=your-gateway-token

# ElevenLabs TTS
ELEVENLABS_API_KEY=your-api-key
ELEVENLABS_VOICE_ID=XrExE9yKIg1WjnnlVkGX  # Matilda (free tier) — or MClEFoImJXBTgLwdLI5n for Ivy (paid)
ELEVENLABS_MODEL_ID=eleven_v3

# Porcupine Wake Word
PORCUPINE_ACCESS_KEY=your-access-key
PORCUPINE_MODEL_PATH=              # path to custom .ppn file (optional)

# Whisper STT
WHISPER_MODEL=base                  # tiny, base, small, medium, large

# Tuning
WAKE_SENSITIVITY=0.7               # 0.0–1.0 (higher = more sensitive)
SILENCE_TIMEOUT=1.5                # seconds of silence to stop recording
HOTKEY=ctrl+shift+k                # global keyboard shortcut
```

## 自定义唤醒词

1. 访问 [Picovoice控制台](https://console.picovoice.ai/)  
2. 创建一个自定义唤醒词（例如：“Hey Claudia”或“Hey OpenClaw”）  
3. 下载适用于您操作系统的`.ppn`文件  
4. 在`.env`文件中设置`PORCUPINE_MODEL_PATH`为该文件的路径  
5. 如果未使用自定义模型，系统将使用内置的“hey google”作为唤醒词  

## 个性化语音效果

当助手被激活时（例如说“Yep!”、“Hi!”），或者思考时（例如说“Hmm...”、“Let me think...”），会播放相应的音频片段。这些音频片段可以使用您选择的ElevenLabs语音库生成。

```bash
cd {baseDir}/scripts
venv\Scripts\python generate_chime_sounds.py
venv\Scripts\python generate_thinking_sounds.py
```

在修改`ELEVENLABS_VOICE_ID`后，请重新运行相关配置。

## 在后台运行

使用`start.bat`命令以无控制台窗口的方式启动应用程序（通过`pythonw.exe`执行）。助手会以系统托盘图标的形式显示，并提供暂停/恢复/退出的功能。

若要在Windows系统中实现自动启动，请将`start.bat`创建为“shell:startup”快捷方式。

## 工作原理

1. **唤醒**：Porcupine语音识别模块检测到唤醒词或用户按下热键。  
2. **提示音**：播放随机生成的激活提示音（例如“Yep!”、“Hi!”）。  
3. **录音**：开始录制语音，直到检测到1.5秒的静默（初始静默时间为2秒）。  
4. **思考音**：在处理语音时播放提示音（例如“Hmm...”、“Let me think...”）。  
5. **转录**：使用`fast-whisper`技术将音频实时转换为文本（使用CPU和int8格式）。  
6. **网关传输**：通过WebSocket将文本发送到OpenClaw网关，并接收AI的响应。  
7. **语音播放**：ElevenLabs将AI的回复转换为语音并通过扬声器播放。  
8. **后续交互**：在用户说完话后，系统会自动等待5秒以保持对话的连贯性。  
9. **待机状态**：如果5秒内没有新的语音输入，系统会重新进入唤醒词监听状态。  

为了防止反馈循环，系统会在扬声器播放声音期间自动关闭麦克风。

## 详细架构

有关源文件结构、WebSocket协议细节以及音频处理流程的详细信息，请参阅 [references/architecture.md](references/architecture.md)。

## 故障排除

如遇到麦克风检测问题、网关连接故障、TTS转换错误或唤醒词设置问题，请参考 [references/troubleshooting.md](references/troubleshooting.md) 中的解决方案。