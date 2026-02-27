---
name: voice-memo
description: "通过 BlueBubbles 使用 ElevenLabs 的 TTS（文本到语音）功能发送原生 iMessage 语音消息。适用场景包括：用户请求发送语音消息、需要内容被朗读出来、希望获取故事或摘要的版本，或者语音传递比文本更具有吸引力时。使用此功能需要 ElevenLabs 的 API 密钥和 BlueBubbles 服务。"
homepage: https://github.com/amzzzzzzz/imessage-voice-memo-skill
metadata: { "openclaw": { "emoji": "🎙️", "platform": "macOS", "requires": { "bins": ["curl", "afconvert"] }, "credentials": ["BLUEBUBBLES_PASSWORD", "ELEVENLABS_API_KEY"] } }
---
# 语音备忘录

使用 ElevenLabs 的 TTS 服务和 BlueBubbles 功能，发送原生的 iMessage 语音消息（而非文件附件）。

## 快速入门

运行以下脚本，并提供需要发送的文本和接收者信息：

```bash
scripts/send-voice-memo.sh "Your message here" +14169060839
```

该脚本将执行以下操作：
1. 通过 ElevenLabs 生成 TTS 音频（默认使用 Rachel 的语音）
2. 将音频转换为 Opus 格式（CAF 格式，24kHz 频率，这是 iMessage 的原生格式）
3. 通过 BlueBubbles 以原生语音消息的形式发送出去

## 所需条件

- BlueBubbles 必须在本地运行，并且已启用私有 API 功能
- 拥有 ElevenLabs 的 API 密钥（用于 TTS 服务）
- 使用 macOS 系统（以便使用 `afconvert` 进行音频转换）
- 在 `~/.openclaw/.env` 文件中设置以下环境变量：
  ```bash
  ELEVENLABS_API_KEY=your-key-here
  BLUEBUBBLES_PASSWORD=your-password-here
  # Optional overrides:
  ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM  # Rachel (default)
  ELEVENLABS_MODEL_ID=eleven_turbo_v2_5      # Turbo v2.5 (default)
  ```

## 工作原理

**2026-02-19 发现的关键参数：**

| 参数 | 值 | 说明 |
|-----------|-------|-----|
| chatGuid | `any;-;+PHONE` | 必须使用此格式，否则会导致超时 |
| method | `private-api` | 用于发送原生语音消息 |
| isAudioMessage | `true` | 必须设置为 `true` |
| Audio format | Opus 格式，24kHz 频率（CAF 格式） | 这是 iMessage 的原生音频格式 |
| Pre-convert | `true` | 必须启用预转换功能，防止 BlueBubbles 使用错误的编码格式进行转换 |

## 语音设置

**默认语音：** Rachel（ElevenLabs 提供）
- 语音 ID：`21m00Tcm4TlvDq8ikWAM`
- 语音模型：`eleven_turbo_v2_5`（发音清晰、自然）
- 成本：每 30 秒的语音消息约 0.04 美元

**表情标签：**
- `[laughs]` — 表示自然地笑出声
- `[sighs]` — 表示叹息
- `[excited]` — 表示兴奋的语气

示例：`"[excited] 哦，太棒了！成功了！"`

有关所有可用语音及其 ID 的详细信息，请参阅 [VOICES.md](references/VOICES.md)。

## 双向语音备忘录

**发送（Amz → Amy）：**
使用此功能发送语音备忘录后，接收方会看到原生的语音消息（带有波形图界面）。

**接收（Amy → Amz）：**
BlueBubbles 会自动将接收到的语音备忘录转换为 MP3 格式。OpenClaw 会通过 Whisper 功能将其转录成文本，并自动插入对话内容中。

**注意事项：**
- 接收到的语音备忘录转录内容会像普通文本消息一样显示在对话中，但不会自动保存到内存或文件中。用户需要自行选择是否保存这些内容。
- 如果希望防止转录内容被保存，可以指示代理不要将语音备忘录内容存储在内存中。

## 常见问题解决方法

- **语音消息以文件附件的形式发送：**
  - 确保 `method` 参数设置为 `private-api`。
  - 检查 `chatGuid` 是否使用了 `any;-;+PHONE` 格式。
  - 确认响应中包含 `isAudioMessage: true`。

- **API 超时：**
  - 使用 `any;-;+PHONE` 格式设置 `chatGuid`。
  - 确保 BlueBubbles 的私有 API 功能已启用。
  - 如果 BlueBubbles 运行缓慢，可以尝试重启该服务。

- **音频文件无法播放：**
  - 确保音频已转换为 Opus 格式（24kHz 频率）。
  - 避免让 BlueBubbles 使用错误的编码格式进行转换。
  - 使用 `afinfo output.caf` 命令检查音频文件格式（应显示为 Opus 格式，24000 Hz）。