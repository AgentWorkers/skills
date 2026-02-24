---
name: edge-tts-unlimited
version: 1.0.0
description: >
  使用 Python 的 `edge-tts` 库，可以通过 Microsoft Edge 的神经语音功能实现免费、无限制的文本转语音服务。无需 API 密钥，无需支付费用，也没有字符长度限制。该工具能够处理较长形式的文本（已测试过超过 55 分钟的文本）。适用场景包括：  
  (1) 将文本转换为语音，用于制作音频简报、播客或语音笔记；  
  (2) 生成长篇音频内容（如新闻简报、文章、故事），同时不会超出 API 的使用限制；  
  (3) 在无头服务器（如 Fly.io、VPS、Docker）上使用该服务，且无需任何额外的设置成本。  
  **不适用场景**：  
  - 实时流媒体语音转录；  
  - 语音克隆；  
  - 高质量的配音服务（请使用 ElevenLabs）。
---
# Edge TTS Unlimited

免费、无限制的神经语音合成服务。无需API密钥，也无需消耗任何信用额度或字符限制。

## 为什么选择这个语音合成工具？

| 问题 | 其他工具 | Edge TTS |
|---------|-------------|------------|
| 长文本（超过5000个字符） | 可能失败或需要分块处理 | 可通过`--file`选项直接处理长文本 |
| 成本 | ElevenLabs每月费用为5美元（仅适用于4次使用） | 免费，永久使用 |
| API密钥 | 必需 | Edge TTS无需API密钥 |
| 服务器部署 | 部分工具需要额外的依赖库 | Edge TTS完全基于Python开发，可在Fly.io或Docker上运行 |
| 55分钟的音频文件 | 未经过测试/不支持 | 已经过测试，可以正常处理 |

## 快速入门

- 从文本生成语音：```bash
scripts/speak.sh "Hello world" -o output.mp3
```
- 从文件生成语音（推荐用于长文本）：```bash
scripts/speak.sh --file /tmp/my-script.txt -o output.mp3
```
- 可自定义语音和语速：```bash
scripts/speak.sh --file script.txt -v en-US-GuyNeural -r "+5%" -o brief.mp3
```

## 系统要求

- Python 3.8及以上版本（大多数系统已预装）
- `uv`包管理器或`pip`——脚本会自动检测并安装所需依赖

首次运行时，脚本会通过`uv run --with edge-tts`自动安装`edge-tts`（无需创建虚拟环境）。

## 语音预设

使用`--preset`选项快速选择语音风格：

| 预设 | 语音 | 风格 |
|--------|-------|-------|
| `news-us` | en-US-GuyNeural +5% | 活泼的美国新闻播音风格 |
| `news-bbc` | en-GB-RyanNeural | 专业的英国播音风格 |
| `calm` | en-US-AndrewNeural -10% | 温和、放松的语气 |
| `fast` | en-US-ChristopherNeural +20% | 快速阅读的语速 |

## 全部功能选项

```
scripts/speak.sh [TEXT] [OPTIONS]
  TEXT              Text to speak (or use --file)
  --file, -f FILE   Read text from file (recommended for long content)
  --voice, -v NAME  Voice name (default: en-US-GuyNeural)
  --rate, -r RATE   Speed adjustment: "+5%", "-10%", etc.
  --preset, -p NAME Use a voice preset (see above)
  --output, -o FILE Output path (default: /tmp/tts-{timestamp}.mp3)
  --list            List available voices
  --list-filter STR Filter voice list (e.g. "british", "female")
```

## 热门语音列表

运行`scripts/speak.sh --list`可查看所有可用语音，或使用特定条件进行筛选：```bash
scripts/speak.sh --list-filter british
scripts/speak.sh --list-filter female
```

**英文语音推荐：**
- `en-US-GuyNeural`：男性，适合新闻播报或激情演讲
- `en-US-ChristopherNeural`：男性，语气权威
- `en-US-AriaNeural`：女性，自信的语气
- `en-GB-RyanNeural`：男性，英国风格，语调稳重
- `en-GB-SoniaNeural`：女性，英国风格

## 测试结果

- 最长文本处理能力：
  | 字符数 | 生成时长 | 文件大小 | 结果 |
  |--------|----------|-----------|--------|
  | 7,400   | 约6分钟   | 2.6 MB   | 可正常生成 |
  | 18,000   | 约21分钟   | 7.3 MB   | 可正常生成 |
  | 46,200   | 约55分钟 | 18.8 MB   | 可正常生成 |

Edge TTS服务能够处理任意长度的文本，目前未发现性能瓶颈。

## 使用技巧：
- 对于超过一个句子的文本，请务必使用`--file`选项，以避免shell引号问题。
- 语速设置`+5%`适合新闻播报；`+20%`适合快速阅读。
- Edge TTS会将`[短停顿]`视为普通文本，因此请使用逗号或句号来表示自然停顿。
- 默认生成的音频为48kbps的单声道MP3格式，音质不错，文件体积较小。