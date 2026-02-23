---
name: jarvis-voice
version: 3.1.0
description: "将你的人工智能系统升级为 JARVIS：集语音交互、机智幽默以及独特个性于一身的完美解决方案。其幽默感被调至最高水平。"
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

### 你的 AI 现在有了语音，同时也拥有了使用这种语音的“智慧”。

还记得《钢铁侠》系列电影中的 JARVIS 吗？不仅仅是它的语音，还有它的“个性”——在托尼遇到危机时，它会给出冷冰冰的评论：“我确实感谢您的关心，先生，但这套战衣完全有能力……”（接着是一声爆炸声），然后继续说：“正如我刚才所说。”那种毫不费力、低调的幽默感，让人完全忘记了自己正在听的是一个软件在说话。

这就是这个功能为你的 OpenClaw 代理带来的：**语音**——通过 `sherpa-onnx` 实现的离线文本转语音功能（使用的是英国人艾伦的配音），并通过 `ffmpeg` 对音频进行处理，使其听起来更具金属质感；**幽默感**——则基于四种经过研究的幽默模式（冷幽默、自我意识的 AI、外星观察者的视角、以及对成语的巧妙运用），这些模式被精心调整，让代理听起来就像已经陪伴你多年一样，对这一切感到一丝丝的“趣味”。

这种幽默感并非后期添加的，而是内置在系统中的。因为一个没有幽默感的 JARVIS，不过是一个语音更好的 Siri 罢了。

📄 **幽默背后的研究：** [LIMBIC — 通过双联思维与嵌入距离实现计算幽默](https://github.com/globalcaos/clawdbot-moltbot-openclaw/blob/main/AI_reports/humor-embeddings-paper-draft.md)

## ⚠️ 重要提示：** **切勿使用 `tts` 工具**  
内置的 `tts` 工具使用的是 Edge TTS 服务（基于云端，语音效果不佳，且没有特殊效果）。**请始终使用 `jarvis` 命令来播放语音。**

## 如何实现语音输出

任何需要语音输出的回复都必须同时满足以下两个条件：

1. **先播放音频**——在输出文本之前，先在后台运行 `jarvis` 命令：
   ```
   exec(command='jarvis "Your spoken text here."', background=true)
   ```  
   这个命令会立即执行，用户会在文本出现在屏幕上之前听到语音。

2. **显示文本记录**——文本前要加上加粗的 “Jarvis：”：
   ```
   **Jarvis:** *Your spoken text here.*
   ```  
   Webchat 用户界面使用了自定义的 CSS 和 JS，能够自动识别 “Jarvis：” 并以 **紫色斜体**（`.jarvis-voice` 类，颜色 `#9b59b6`）显示文本。你只需要编写 Markdown 格式的文本，样式会自动处理。

这种输出方式被称为 **混合输出**：用户先听到语音，然后再看到文本记录。

> **注意：** 服务器端的 `triggerJarvisAutoTts` 触发器是禁用的（无效的），因为它会在文本显示之后才执行。所有语音都由 `exec` 命令直接生成。

## 命令参考

```bash
jarvis "Hello, this is a test"
```  
- **后端技术：** 使用 `sherpa-onnx` 实现离线文本转语音（艾伦的配音，英式英语，`en_GB-alan-medium` 配置）  
- **语速：** 加快 2 倍（`--vits-length-scale=0.5`）  
- **音频效果链（ffmpeg）：**  
  - 提高音调 5% 以增强 AI 的“真实感”  
  - 应用“Flanger”效果以增加音频的金属质感  
  - 添加 15 毫秒的回声效果  
  - 通过高通滤波器提升 200Hz 频段的音量 +6dB，使语音更加清晰  
- **输出方式：** 通过 `aplay` 播放到默认音频设备，播放完成后会清理临时文件  
- **语言限制：** 仅支持英语。艾伦模型不支持其他语言。

## 使用规则：  
1. **始终在后台执行语音处理**——不要因为等待音频播放而阻塞用户的响应。  
2. **必须包含文本记录**——加粗的 “Jarvis：” 行是用户确认语音输出的依据。  
3. **确保语音文本长度不超过 1500 个字符**，以避免文本被截断。  
4. **每个回复只能使用一次 `jarvis` 命令**，不要重复调用。  
5. **仅支持英语**——对于非英语内容，需要先翻译或总结成英语后再进行语音输出。  

## 何时使用语音功能：  
- 用于会话中的问候语和告别语  
- 用于展示结果或总结信息  
- 用于回应用户的直接对话  
- 用于处理用户发送的包含语音或音频的消息  

## 何时不使用语音功能：  
- 仅用于纯工具或文件操作（不涉及对话内容）  
- 对于表示系统状态的响应（如 “HEARTBEAT_OK”）  
- 对于不需要语音回应的消息  

## Webchat 的紫色文本样式  

OpenClaw 的 Webchat 界面内置了对 Jarvis 语音记录的支持：  
- **`ui/src/styles/chat/text.css`**：使用 `.jarvis-voice` 类将文本以紫色斜体显示（深色主题为 `#9b59b6`，浅色主题为 `#8e44ad`）  
- **`ui/src/ui/markdown.ts`**：在 `<strong>Jarvis:` 后自动将文本包裹在 `<span class="jarvis-voice">` 标签中  

这意味着你只需要在 Markdown 中编写 “Jarvis：*文本*”，Webchat 会自动处理文本的渲染。无需额外的标记格式。  

对于 **非 Webchat 平台**（如 WhatsApp、Telegram 等），加粗/斜体的文本格式会以原生方式显示——虽然没有紫色背景，但依然能够清晰地区分语音和文本。  

## 安装说明（新环境）  

安装所需工具：  
- `sherpa-onnx` 运行时库，位于 `~/.openclaw/tools/sherpa-onnx-tts/`  
- 英国人艾伦的配音模型，位于 `~/.openclaw/tools/sherpa-onnx-tts/models/vits-piper-en_GB-alan-medium/`  
- 系统中已安装 `ffmpeg`  
- 需要 `aplay`（用于音频播放的 ALSA 库）  
- `jarvis` 脚本，位于 `~/.local/bin/jarvis`（或添加到系统的 PATH 环境变量中）  

### `jarvis` 脚本  

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

## WhatsApp 的语音输出设置  

对于 WhatsApp，语音文件需要使用 OGG/Opus 格式，而不能直接通过扬声器播放：  
```bash
sherpa-onnx-offline-tts --vits-length-scale=0.5 --output-filename=raw.wav "text"
ffmpeg -i raw.wav \
  -af "asetrate=22050*1.05,aresample=22050,flanger=delay=0:depth=2:regen=50:width=71:speed=0.5,aecho=0.8:0.88:15:0.5,highpass=f=200,treble=g=6" \
  -c:a libopus -b:a 64k output.ogg
```  

## 完整的 Jarvis 语音体验  

通过 `jarvis-voice` 功能，你的代理将拥有真实的语音。将其与 [**ai-humor-ultimate**](https://clawhub.com/globalcaos/ai-humor-ultimate) 功能结合使用，你的代理将具备更丰富的“个性”：冷幽默、根据语境生成的幽默，以及那种让人会心一笑的讽刺语。  

这套功能是我们正在开发的 12 项认知能力模块之一，还包括语音识别、幽默生成、记忆功能、推理能力等等。相关的研究论文也已准备好供你查阅（因为我们对此非常执着）。  

👉 **探索完整项目：** [github.com/globalcaos/clawdbot-moltbot-openclaw](https://github.com/globalcaos/clawdbot-moltbot-openclaw)  
你可以克隆这个项目，根据需要进行修改，甚至可以将其据为己有。  

## 设置工作区文件  

为了让语音功能在新的会话中始终正常工作，请将以下文件复制到工作区的根目录：  
```bash
cp {baseDir}/templates/VOICE.md ~/.openclaw/workspace/VOICE.md
cp {baseDir}/templates/SESSION.md ~/.openclaw/workspace/SESSION.md
cp {baseDir}/templates/HUMOR.md ~/.openclaw/workspace/HUMOR.md
```  
- **VOICE.md**：用于在每个会话中强制启用语音输出功能  
- **SESSION.md**：包含语音问候语的会话启动配置文件  
- **HUMOR.md**：配置幽默效果，支持四种幽默模式（冷幽默、自我意识的 AI、外星观察者的视角、以及对成语的巧妙运用），使用频率为 1.0  

这两个文件会由 OpenClaw 的工作区自动加载，因此代理会在每个会话的第一个回复中就开始使用语音功能。  

## 包含的文件：  
| 文件 | 用途 |  
|------|---------|  
| `bin/jarvis` | 负责语音转换和效果处理的脚本（可移植，依赖于 `$SHERPA_ONNX_TTS_DIR`）  
| `templates/VOICE.md` | 规定语音输出的规则（需复制到工作区根目录）  
| `templates/SESSION.md` | 包含语音问候语的会话启动配置文件（需复制到工作区根目录）  
| `templates/HUMOR.md` | 配置四种幽默模式（使用频率为 1.0，需复制到工作区根目录）