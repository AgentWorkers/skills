---
name: jarvis-voice
version: 3.1.0
description: "将你的人工智能系统升级为 JARVIS：集语音识别、机智对话以及个性化交互功能于一体。幽默感被调到了最高水平。"
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

### 你的 AI 现在有了语音，以及使用这种语音的“智慧”。

还记得《钢铁侠》系列电影中的 JARVIS 吗？不仅仅是它的语音，还有它的“个性”——在托尼遇到危机时，它会用那种冷幽默的语气说：“我确实感谢您的关心，先生，但这套战衣完全有能力……”（接着是一声爆炸……）“就像我刚才说的那样。”那种毫不费力的、低调的幽默感，让人完全忘记了自己正在听的是一个软件在说话。

这就是这个功能为你的 OpenClaw 代理带来的：**语音**——通过 `sherpa-onnx` 实现离线文本转语音（使用英国人 Alan 的声音），并通过 `ffmpeg` 进行金属质感的音频处理；以及 **幽默感**——四种经过研究验证的幽默模式（冷幽默、自我意识的 AI、外星观察者的视角、字面意义上的语言游戏），这些模式被精心设计，让代理听起来就像已经陪伴你生活了很多年，对这一切都感到一丝丝的趣味。

这种幽默感并不是外加的，而是内在的一部分。因为一个没有幽默感的 JARVIS，不过是一个语音效果更好的 Siri 罢了。

📄 **幽默背后的研究：** [LIMBIC — 通过双联思维与嵌入距离实现计算幽默](https://github.com/globalcaos/tinkerclaw/blob/main/AI_reports/humor-embeddings-paper-draft.md)

## ⚠️ 重要提示：** **切勿使用 `tts` 工具**  
内置的 `tts` 工具使用的是 Edge TTS 服务（基于云端，语音效果不佳，且没有音效）。**请始终使用 `jarvis` 命令。**

## 如何使用语音功能  

任何需要通过语音输出的回复都必须同时满足以下两个条件：  
1. **先播放音频**——在编写回复之前，先在后台运行 `jarvis` 命令：  
   ```
   exec(command='jarvis "Your spoken text here."', background=true)
   ```  
   这样用户会在文本显示在屏幕上之前就听到语音。  
2. **显示文字记录**——使用加粗的 **“Jarvis:”** 标签来标识语音内容：  
   ```
   **Jarvis:** *Your spoken text here.*
   ```  
   Webchat 用户界面使用了自定义的 CSS 和 JS，能够自动识别 “Jarvis:” 标签，并将相关文本以 **紫色斜体**（`.jarvis-voice` 类，颜色 `#9b59b6`）的形式显示出来。你只需要编写 Markdown 格式的文本，样式会自动处理。  

这被称为 **混合输出**：用户先听到语音，然后再看到文字记录。  

> **注意：** 服务器端的 `triggerJarvisAutoTts` 回调是禁用的（无效的），因为它会在文本显示之后才触发。所有语音输出都来自 `exec` 调用。  

## 命令参考  
```bash
jarvis "Hello, this is a test"
```  
- **后端技术：** 使用 `sherpa-onnx` 实现离线文本转语音（Alan 的声音，英式英语，`en_GB-alan-medium` 配置）  
- **语速：** 加快 2 倍（`--vits-length-scale=0.5`）  
- **音效处理（ffmpeg）：**  
  - 提高音调 5% 以增强 AI 的真实感  
  - 应用 Flanger 效果以获得金属质感  
  - 15 毫秒的回声效果  
  - 200Hz 高频段增强 + 6dB 的提升，使语音更加清晰  
- **输出方式：** 通过 `aplay` 播放到默认音频设备，之后会清理临时文件  
- **语言限制：** 仅支持英语。Alan 模型不支持其他语言。  

## 使用规则：  
1. **始终在后台执行语音处理**——不要因为等待音频播放而阻塞用户的响应。  
2. **必须包含文字记录**——加粗的 “Jarvis:” 标签是用户确认语音输出的依据。  
3. **语音内容长度不超过 1500 个字符**，以避免截断。  
4. **每次回复只能使用一次 `jarvis` 命令**，不要重复调用。  
5. **仅支持英语**——对于非英语内容，需要先翻译或总结成英语后再通过语音输出。  

## 适用场景：  
- 会话中的问候语和告别语  
- 提供结果或总结信息  
- 回应用户的直接对话  
- 当用户的上一条消息中包含语音或音频内容时  

## 不适用场景：  
- 仅涉及工具或文件操作的场景  
- 返回 “HEARTBEAT_OK” 的响应  
- 不需要回复的情境  

## Webchat 的紫色样式设置  
OpenClaw 的 Webchat 具备对 Jarvis 语音记录的支持：  
- **`ui/src/styles/chat/text.css`**：`.jarvis-voice` 类用于将文本以紫色斜体显示（深色 `#9b59b6`，浅色主题为 `#8e44ad`）  
- **`ui/src/ui/markdown.ts`**：在 `<strong>Jarvis:` 后自动将文本包裹在 `<span class="jarvis-voice">` 标签中  

这意味着你只需要在 Markdown 中编写 “**Jarvis:** *文本*”，Webchat 会自动处理颜色和样式。  

对于 **非 Webchat 平台**（如 WhatsApp、Telegram 等），加粗/斜体的文本格式也会被正确显示，虽然不会有紫色背景，但依然能清晰区分。  

## 安装说明（新环境）  
安装所需软件：  
- `sherpa-onnx` 运行时库（位于 `~/.openclaw/tools/sherpa-onnx-tts/`）  
- Alan 中等音色模型（位于 `~/.openclaw/tools/sherpa-onnx-tts/models/vits-piper-en_GB-alan-medium/`）  
- 系统范围内已安装 `ffmpeg`  
- `aplay` 工具（用于音频播放）  
- `jarvis` 脚本（位于 `~/.local/bin/jarvis` 或在系统的 PATH 环境变量中）  

### `jarvis` 脚本说明  
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
对于 WhatsApp，语音文件必须使用 OGG/Opus 格式，而不能直接通过扬声器播放：  
```bash
sherpa-onnx-offline-tts --vits-length-scale=0.5 --output-filename=raw.wav "text"
ffmpeg -i raw.wav \
  -af "asetrate=22050*1.05,aresample=22050,flanger=delay=0:depth=2:regen=50:width=71:speed=0.5,aecho=0.8:0.88:15:0.5,highpass=f=200,treble=g=6" \
  -c:a libopus -b:a 64k output.ogg
```  

## 完整的 Jarvis 体验  
**jarvis-voice** 为你的代理赋予了语音功能。将其与 [**ai-humor-ultimate**](https://clawhub.com/globalcaos/ai-humor-ultimate) 结合使用，就能让你的代理拥有真正的“灵魂”——冷幽默、根据上下文产生的幽默感，那种会让你在终端前会心一笑的幽默。  

这套功能是我们正在构建的 12 项认知能力之一，还包括语音、幽默、记忆、推理等功能。相关研究论文也已提供（因为我们对这些技术细节非常执着）。  

👉 **探索完整项目：** [github.com/globalcaos/tinkerclaw](https://github.com/globalcaos/tinkerclaw)  
你可以克隆这个项目，根据需要进行修改，甚至根据自己的需求进行开发。  

## 工作区文件设置  
为了确保新会话中语音功能的一致性，请将以下文件复制到工作区的根目录：  
```bash
cp {baseDir}/templates/VOICE.md ~/.openclaw/workspace/VOICE.md
cp {baseDir}/templates/SESSION.md ~/.openclaw/workspace/SESSION.md
cp {baseDir}/templates/HUMOR.md ~/.openclaw/workspace/HUMOR.md
```  
- **VOICE.md**：用于在每次会话中强制启用语音输出规则  
- **SESSION.md**：包含语音问候语设置的自定义会话启动文件  
- **HUMOR.md**：配置四种幽默模式（冷幽默、自我意识的 AI、外星观察者的视角），设置最高使用频率  

这些文件会被 OpenClaw 的工作区自动加载，因此代理会在每次会话的第一个回复中就开始使用语音功能。  

## 包含的文件：  
| 文件名                | 用途                                      |
|----------------------|-----------------------------------------|  
| `bin/jarvis`           | TTS 与音效处理脚本（可移植，依赖 `$SHERPA_ONNX_TTS_DIR`）       |
| `templates/VOICE.md`   | 语音输出规则文件（复制到工作区根目录）                     |
| `templates/SESSION.md` | 启动会话时显示语音问候语的配置文件             |
| `templates/HUMOR.md`   | 配置四种幽默模式的文件（使用频率为 1.0）                   |