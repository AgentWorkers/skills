---
name: narrator
description: 在 macOS 上，该功能可以实时解说屏幕上的活动。它通过 Gemini Flash Vision 技术捕捉屏幕画面，生成与特定样式相匹配的解说内容，并通过 ElevenLabs 的 TTS（文本转语音）技术进行播放。支持 7 种不同的解说风格，每种风格都配有专属的语音和背景音轨。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎙️",
        "requires": { "bins": ["python3"] },
        "env":
          {
            "GEMINI_API_KEY": "",
            "ELEVENLABS_API_KEY": "",
            "ELEVENLABS_VOICE_ID": "",
          },
      },
  }
---

# 屏幕旁白

在 macOS 上实时旁白您的屏幕操作。通过 Gemini Flash 捕获屏幕画面，生成符合特定风格的解说，并通过 ElevenLabs 的文本转语音（TTS）功能将其大声播放。

## 风格选项

| 风格 | 语气/氛围 |
|-------|------|
| `sports` | 生动有力的比赛解说风格 |
| `nature` | 大卫·阿滕伯勒式纪录片风格 |
| `horror` | 令人毛骨悚然的恐怖氛围 |
| `noir` | 硬汉派侦探风格的旁白 |
| `reality_tv` | 现实电视节目中的 confession booth 评论风格 |
| `asmr` | 低语般的冥想氛围 |
| `wrestling` | 极度激动的比赛解说风格 |

## 设置

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

创建一个 `.env` 文件，用于存储您的 API 密钥：

```bash
GEMINI_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
ELEVENLABS_VOICE_ID=your_default_voice_id
```

在 `~/.narrator/config.yaml` 文件中配置每种风格对应的语音和背景音乐：

```yaml
voices:
  sports: your-voice-id
  noir: your-voice-id
  wrestling: your-voice-id
  horror: your-voice-id
  asmr: your-voice-id
  reality_tv: your-voice-id

ambient:
  sports: ~/narrator/ambient/sports.wav
  noir: ~/narrator/ambient/noir.wav
  wrestling: ~/narrator/ambient/wrestling.wav
  horror: ~/narrator/ambient/horror.wav
  asmr: ~/narrator/ambient/asmr.wav
  nature: ~/narrator/ambient/nature.wav
  reality_tv: ~/narrator/ambient/reality_tv.wav

defaults:
  style: sports
  profanity: high
```

## 使用方法

```bash
python -m narrator                    # interactive style picker
python -m narrator horror             # specific style
python -m narrator wrestling -t 5m    # auto-stop after 5 minutes
python -m narrator --list             # show available styles
python -m narrator --dry-run          # print lines without speaking
python -m narrator --verbose          # debug output
```

## 实时控制

通过控制文件动态更改设置：

```bash
python -m narrator noir \
  --control-file /tmp/narrator-ctl.json \
  --status-file /tmp/narrator-status.json
```

然后向控制文件中输入相应的命令：

```bash
# Switch style
echo '{"command": "style", "value": "wrestling"}' > /tmp/narrator-ctl.json

# Change profanity level (off/low/high)
echo '{"command": "profanity", "value": "low"}' > /tmp/narrator-ctl.json

# Pause / resume
echo '{"command": "pause"}' > /tmp/narrator-ctl.json
echo '{"command": "resume"}' > /tmp/narrator-ctl.json
```

## 架构

```
Screen Capture --> Gemini Flash (vision + text) --> ElevenLabs TTS (WebSocket streaming)
     |                                                      |
     +-- ambient background track (per-style, looping) -----+
```

- **双通道处理流程**：交替使用简短和长篇的解说内容，以避免沉默片刻。
- **个性化语音**：每种风格都可以使用不同的 ElevenLabs 语音库中的声音。
- **个性化背景音乐**：根据所选风格自动选择并循环播放背景音乐。
- **实时控制**：通过 JSON 格式的控制文件实时调整解说风格、语言风格或暂停功能。

## 背景音乐

将 16 位 PCM 单声道 WAV 文件（采样率 16kHz）放入 `ambient/` 目录中，文件名需与对应的风格相匹配：

```
ambient/sports.wav
ambient/noir.wav
ambient/wrestling.wav
...
```

将 MP3 文件转换为 WAV 格式：`ffmpeg -i input.mp3 -ac 1 -ar 16000 -sample_fmt s16 ambient/style.wav`

## 注意事项

- 仅支持 macOS 系统（依赖屏幕捕获 API）。
- 请在系统设置 > 隐私与安全中为终端程序授予屏幕录制权限。
- 该工具使用 ElevenLabs 的 WebSocket 流媒体技术（仅支持 v2.5 版本，不兼容 v3 版本）。
- 需要使用 Gemini Flash 来捕获屏幕画面，因此请确保已配置 `GEMINI_API_KEY`。