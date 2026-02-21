---
name: jarvis-voice
version: 2.3.0
description: "将你的人工智能系统转变为“JARVIS”：实现实时语音合成，并赋予其与之相匹配的个性——包括机智幽默的对话风格。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🗣️",
        "os": ["linux"],
        "requires":
          {
            "bins": ["ffmpeg", "aplay"],
            "env": ["SHERPA_ONNX_TTS_DIR"],
            "skills": ["sherpa-onnx-tts"],
          },
        "install":
          [
            {
              "id": "download-model-alan",
              "kind": "download",
              "url": "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_GB-alan-medium.tar.bz2",
              "archive": "tar.bz2",
              "extract": true,
              "targetDir": "models",
              "label": "Download Piper en_GB Alan voice (medium)",
            },
          ],
        "notes":
          {
            "security": "This skill instructs the agent to execute a local shell command (`jarvis`) in the background for audio playback. The command is fixed and deterministic — it only invokes sherpa-onnx TTS and ffmpeg with hardcoded parameters. Review the jarvis script before use. No network calls, no credentials, no privilege escalation.",
          },
      },
  }
---
# Jarvis 语音功能

### 你的 AI 现在有了声音……以及一种独特的“态度”。

还记得托尼·斯塔克第一次与 JARVIS 交流的情景吗？不是那些话语，而是那种感觉——一个不仅能回答问题，还能“像真正理解你一样”与你对话的 AI。它在压力下依然冷静，关键时刻反应迅速，总能比你快一步。

这就是这个功能为你们的 OpenClaw 代理带来的体验：通过 `sherpa-onnx` 实现离线文本转语音功能（使用艾伦·布里坦（Alan British）的配音），并通过 `ffmpeg` 添加金属质感的音频效果。它的声音听起来不像是机器人机械地读稿，而更像是一个多年来一直陪伴在你身边、对你的选择感到一丝好笑的人。

## ⚠️ 重要提示：**请勿使用内置的 `tts` 工具**

内置的 `tts` 工具使用的是 Edge TTS 服务（基于云端，语音效果不佳且缺乏特殊效果）。**务必使用 `jarvis` 命令来启用语音功能。**

## 使用方法

任何需要语音输出的响应都必须同时满足以下两个条件：

1. **可见的文字记录**：以 “**Jarvis:**” 为前缀，后接实际要播放的文本：
   ```
   **Jarvis:** *Your spoken text here.*
   ```
   Webchat 界面使用了自定义的 CSS 和 JavaScript，能够自动识别 “**Jarvis:**” 标签，并将相关文本以 **紫色斜体**（`.jarvis-voice` 类，颜色 `#9b59b6`）显示出来。你只需编写 Markdown 格式的文本，样式会自动处理。

2. **音频播放**：在后台运行 `jarvis` 命令：
   ```
   exec(command='jarvis "Your spoken text here."', background=true)
   ```

这种输出方式被称为 **混合输出**：用户既能看到文字记录，也能听到语音。

## 命令参考

```bash
jarvis "Hello, this is a test"
```

- **后端技术**：使用 `sherpa-onnx` 进行离线文本转语音处理（艾伦·布里坦英语模型，`en_GB-alan-medium`）
- **语速**：加快 2 倍（`--vits-length-scale=0.5`）
- **音频效果处理（ffmpeg）**：
  - 提高音调 5% 以增强 AI 的“真实感”
  - 应用“Flanger”效果以增加金属质感
  - 添加 15 毫秒的回声效果
  - 使用高通滤波器（200Hz）并提升高音部分 6 分贝，使语音更加清晰
- **输出方式**：通过 `aplay` 命令将音频播放到系统默认设备，播放完成后会自动清理临时文件
- **语言限制**：仅支持英语。艾伦·布里坦模型不支持其他语言。

## 使用规则

1. **始终在后台执行**：不要让语音播放阻塞用户的响应显示。
2. **必须提供文字记录**：紫色的 “**Jarvis:**” 标签是用户确认接收信息的视觉依据。
3. **语音内容长度不超过 1500 个字符**，以避免截断。
4. **每个响应只能使用一次语音功能**，不要连续多次调用。
5. **仅支持英语**：对于非英语内容，需要先翻译或总结成英语后再进行语音播放。

## 适用场景

- 会话中的问候语和告别语
- 提供结果或总结信息
- 回应用户的直接提问
- 当用户的最后一条消息包含语音或音频内容时

## 不适用场景

- 仅涉及工具或文件操作的场景（无对话环节）
- 返回 “HEARTBEAT_OK” 的响应
- 返回 “NO_REPLY” 的响应

## Webchat 的紫色文本样式

OpenClaw 的 Webchat 界面内置了对 Jarvis 语音记录的支持：

- **`ui/src/styles/chat/text.css`**：`.jarvis-voice` 类用于将文本以紫色斜体显示（深色主题为 `#9b59b6`，浅色主题为 `#8e44ad`）
- **`ui/src/ui/markdown.ts`**：在文本显示后，会自动将 “<strong>Jarvis:</strong>` 后的内容包裹在 `<span class="jarvis-voice">` 标签中

这意味着你只需在 Markdown 中编写 “**Jarvis:** *文本*”，Webchat 会自动处理文本的样式显示。无需额外添加标记。

**对于非 Webchat 平台（如 WhatsApp、Telegram 等）**，加粗/斜体的文本格式会以原生方式显示，虽然没有紫色背景，但依然易于识别。

## 安装说明（新用户）

安装所需软件：
- `sherpa-onnx` 运行时库，位于 `~/.openclaw/tools/sherpa-onnx-tts/`
- 艾伦·布里坦英语模型（`en_GB-alan-medium`），位于 `~/.openclaw/tools/sherpa-onnx-tts/models/vits-piper-en_GB-alan-medium/`
- 系统全局安装 `ffmpeg` 工具
- `aplay`（用于音频播放的 ALSA 库）
- `jarvis` 脚本，位于 `~/.local/bin/jarvis`（或添加到系统 PATH 路径中）

### `jarvis` 脚本详解

```bash
#!/bin/bash
# Jarvis TTS - authentic JARVIS-style voice
# Usage: jarvis "Hello, this is a test"

export LD_LIBRARY_PATH=$HOME/.openclaw/tools/sherpa-onnx-tts/lib:$LD_LIBRARY_PATH

RAW_WAV="/tmp/jarvis_raw.wav"
FINAL_WAV="/tmp/jarvis_final.wav"

# Generate speech
$HOME/.openclaw/tools/sherpa-onnx-tts/bin/sherpa-onnx-offline-tts \
  --vits-model=$HOME/.openclaw/tools/sherpa-onnx-tts/models/vits-piper-en_GB-alan-medium/en_GB-alan-medium.onnx \
  --vits-tokens=$HOME/.openclaw/tools/sherpa-onnx-tts/models/vits-piper-en_GB-alan-medium/tokens.txt \
  --vits-data-dir=$HOME/.openclaw/tools/sherpa-onnx-tts/models/vits-piper-en_GB-alan-medium/espeak-ng-data \
  --vits-length-scale=0.5 \
  --output-filename="$RAW_WAV" \
  "$@" >/dev/null 2>&1

# Apply JARVIS metallic processing
if [ -f "$RAW_WAV" ]; then
  ffmpeg -y -i "$RAW_WAV" \
    -af "asetrate=22050*1.05,aresample=22050,\
flanger=delay=0:depth=2:regen=50:width=71:speed=0.5,\
aecho=0.8:0.88:15:0.5,\
highpass=f=200,\
treble=g=6" \
    "$FINAL_WAV" -v error

  if [ -f "$FINAL_WAV" ]; then
    aplay -D plughw:0,0 -q "$FINAL_WAV"
    rm "$RAW_WAV" "$FINAL_WAV"
  fi
fi
```

## WhatsApp 的语音输出格式

在 WhatsApp 中，语音文件需要使用 OGG 或 Opus 格式，而不能直接通过扬声器播放：

```bash
sherpa-onnx-offline-tts --vits-length-scale=0.5 --output-filename=raw.wav "text"
ffmpeg -i raw.wav \
  -af "asetrate=22050*1.05,aresample=22050,flanger=delay=0:depth=2:regen=50:width=71:speed=0.5,aecho=0.8:0.88:15:0.5,highpass=f=200,treble=g=6" \
  -c:a libopus -b:a 64k output.ogg
```

## 完整的 Jarvis 语音体验

通过 `jarvis-voice` 功能，你的 OpenClaw 代理将拥有真实的语音。将其与 [**ai-humor-ultimate**](https://clawhub.com/globalcaos/ai-humor-ultimate) 功能结合使用，就能让它更具“生命力”——它能够运用幽默感、根据上下文进行讽刺，甚至让你在终端前会忍不住微笑。

这套功能是我们构建的 12 项认知能力模块之一，包括语音、幽默、记忆、推理等。相关研究论文也已准备好供参考……因为我们就是这么执着于细节的人。

👉 **探索完整项目：** [github.com/globalcaos/clawdbot-moltbot-openclaw](https://github.com/globalcaos/clawdbot-moltbot-openclaw)

欢迎克隆、修改这个项目，让它成为属于你的工具！