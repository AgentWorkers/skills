---
name: voice-assistant
description: OpenClaw的实时语音助手：该功能可将麦克风采集的音频通过可配置的文本转语音（STT）服务（Deepgram或ElevenLabs）传输到OpenClaw代理，随后通过可配置的语音合成（TTS）服务（Deepgram Aura或ElevenLabs）生成并播放响应语音。从音频采集到首次播放的整个过程耗时不到2秒，并且支持全程实时流式传输。
metadata:
  openclaw:
    emoji: "🎙️"
    requires:
      bins: ["uv"]
      env: []
    primaryEnv: "VOICE_STT_PROVIDER"
    install:
      - id: "uv"
        kind: "brew"
        formula: "uv"
        bins: ["uv"]
        label: "Install uv (brew)"
---

# 语音助手

这是一个用于您的 OpenClaw 代理的实时语音接口。您可以通过它与代理进行对话，并听到代理的回应。该接口支持配置不同的语音转文本（STT）和文本转语音（TTS）服务提供商，确保在整个过程中实现全流式传输，并且从用户开始说话到听到声音的延迟低于 2 秒。

## 架构

```
Browser Mic → WebSocket → STT (Deepgram / ElevenLabs) → Text
  → OpenClaw Gateway (/v1/chat/completions, streaming) → Response Text
  → TTS (Deepgram Aura / ElevenLabs) → Audio chunks → Browser Speaker
```

该语音接口连接到正在运行的 OpenClaw 网关的 OpenAI 兼容端点。它使用的是同一个代理，具备所有的上下文、工具和内存功能——只不过增加了语音交互的能力。

## 快速入门

```bash
cd {baseDir}
cp .env.example .env
# Fill in your API keys and gateway URL
uv run scripts/server.py
# Open http://localhost:7860 and click the mic
```

## 支持的提供商

### 语音转文本（STT）
| 提供商   | 模型            | 延迟      | 备注                        |
|-----------|------------------|----------|------------------------------|
| Deepgram  | nova-2 (流式)       | ~200-300ms   | 基于 WebSocket 的流式传输，具有最高的准确率和速度 |
| ElevenLabs | Scribe v1        | ~300-500ms   | 基于 REST 的接口，支持多种语言         |

### 文本转语音（TTS）
| 提供商    | 模型        | 延迟      | 备注                          |
|------------|--------------|----------|--------------------------------|
| Deepgram   | aura-2       | ~200ms   | 基于 WebSocket 的流式传输，成本低廉         |
| ElevenLabs | Turbo v2.5   | ~300ms   | 提供最佳的语音质量，支持流式传输         |

## 配置

所有配置均通过 `.env` 文件中的环境变量来完成：

```bash
# === Required ===
OPENCLAW_GATEWAY_URL=http://localhost:4141/v1    # Your OpenClaw gateway
OPENCLAW_MODEL=claude-sonnet-4-5-20250929        # Model your gateway routes to

# === STT Provider (pick one) ===
VOICE_STT_PROVIDER=deepgram                      # "deepgram" or "elevenlabs"
DEEPGRAM_API_KEY=your-key-here                   # Required if STT=deepgram
ELEVENLABS_API_KEY=your-key-here                 # Required if STT=elevenlabs

# === TTS Provider (pick one) ===
VOICE_TTS_PROVIDER=elevenlabs                    # "deepgram" or "elevenlabs"
# Uses the same API keys as above

# === Optional Tuning ===
VOICE_TTS_VOICE=rachel                           # ElevenLabs voice name/ID
VOICE_TTS_VOICE_DG=aura-2-theia-en              # Deepgram Aura voice
VOICE_VAD_SILENCE_MS=400                         # Silence before end-of-turn (ms)
VOICE_SAMPLE_RATE=16000                          # Audio sample rate
VOICE_SERVER_PORT=7860                           # Server port
VOICE_SYSTEM_PROMPT=""                           # Optional system prompt override
```

## 提供商组合

| 配置方式                         | 最适合的场景                         |
|------------------------------------|---------------------------------|
| Deepgram STT + ElevenLabs TTS     | 最佳的语音输出质量                 |
| Deepgram STT + Deepgram TTS       | 最低的延迟，使用同一供应商的服务           |
| ElevenLabs STT + ElevenLabs TTS   | 最佳的多语言支持                     |

## 工作原理

1. 浏览器通过 Web Audio API 捕获麦克风音频，并通过 WebSocket 流式传输原始 PCM 数据。
2. 服务器接收音频数据后，将其发送到配置好的 STT 服务提供商的流式传输端点。
3. STT 服务会实时返回部分转录结果；用户说完话后，完整文本会被发送到 OpenClaw 网关。
4. OpenClaw 网关通过 SSE（Server-Sent Events）协议逐个字符地将 LLM 的响应发送给浏览器。
5. 这些字符会被组合成句子大小的片段，然后发送给 TTS 服务提供商。
6. TTS 服务将处理后的音频片段通过相同的 WebSocket 通道发送回浏览器。
7. 浏览器使用 Web Audio API 播放音频，并通过抖动缓冲机制实现流畅的播放效果。

## 中断处理（用户插话）

当用户在代理仍在说话时开始讲话时：
- 当前的 TTS 播放会立即停止。
- 代理会暂停当前的响应。
- 系统会启动新的 STT 会话来捕获用户的插话内容。

## 使用示例

```
User: "Hey, set up my voice assistant"
→ OpenClaw runs: cd {baseDir} && cp .env.example .env
→ Opens .env for the user to fill in API keys
→ Runs: uv run scripts/server.py

User: "Start a voice chat"
→ Opens http://localhost:7860 in the browser

User: "Switch TTS to Deepgram"
→ Updates VOICE_TTS_PROVIDER=deepgram in .env
→ Restarts the server
```

## 故障排除

- **没有音频输出？** 确保您的 TTS API 密钥有效，并且配置的提供商正确无误。
- **延迟过高？** 尝试同时使用 Deepgram 作为 STT 和 TTS 服务提供商；确保网关位于同一网络环境中。
- **语音传输中断？** 将 `VOICE_VAD_SILENCE_MS` 的值设置为 600-800 毫秒。
- **出现回声/反馈？** 使用耳机，或启用浏览器 UI 中的内置回声消除功能。

## 延迟预算

| 环节                        | 目标延迟    | 实际延迟（典型值）                |
|-------------------------|-----------|------------------|
| 音频捕获 + 语音检测（VAD）        | <200ms    | ~100-150ms                     |
| 语音转文本（STT）            | <400ms    | ~200-400ms                     |
| OpenClaw LLM 的第一个响应字符    | <1500ms   | ~500-1500ms                     |
| TTS 的第一个音频片段          | <400ms    | ~200-400ms                     |
| **从开始到听到声音的总延迟**       | **<2.5 秒** | **约 1.0-2.5 秒**                 |