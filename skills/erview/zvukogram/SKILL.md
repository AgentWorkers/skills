---
name: zvukogram
description: 通过 Zvukogram API 进行文本转语音（Text-to-Speech），该 API 支持 SSML（Speech Synthesis Markup Language）格式。当您需要将文本转换为语音、制作播客、生成语音通知或处理音频文件时，可以使用该服务。该服务支持调整语音播放速度、添加重音符号、进行英文单词的转写以及合并音频片段等功能。
requires:
  env: [ZVUKOGRAM_TOKEN, ZVUKOGRAM_EMAIL]
  credentials: zvukogram_api
---
# Zvukogram TTS

通过 Zvukogram API 生成语音，支持 SSML 标记语言。

## 使用要求

要使用此功能，您需要：
- **Zvukogram API 令牌** — 可在 [https://zvukogram.com/](https://zvukogram.com/) 获取
- **Zvukogram 账户邮箱**

### 设置

创建文件 `~/.config/zvukogram/config.json`：
```bash
mkdir -p ~/.config/zvukogram
```

### 或者使用环境变量：
```bash
export ZVUKOGRAM_TOKEN=your_api_token_here
export ZVUKOGRAM_EMAIL=your_email@example.com
```

## 快速入门

```bash
# Simple TTS
python3 scripts/tts.py --text "Hello, world!" --voice Алена --output hello.mp3

# With +20% speed
python3 scripts/tts.py --text "Fast text" --voice Алена --speed 1.2 --output fast.mp3

# Check balance
python3 scripts/balance.py
```

## 主要功能

- **语音生成** — 将文本转换为语音
- **SSML 支持** — 重音标记、停顿、语速控制
- **音频合并** — 使用 ffmpeg 合并音频片段
- **转录** — 确保英文单词的发音正确

## SSML 标记语言

### 重音标记

在需要重读的元音前使用 `+`：
```
З+амок — stress on "a"
зам+ок — stress on "o"
```

### 别名（用于转录）

```xml
<sub alias="Оупен Эй Ай">OpenAI</sub>
<sub alias="Самсунг">Samsung</sub>
<sub alias="Ал+ьтман">Альтман</sub>
```

### 语速控制

```xml
<prosody rate="1.2">20% faster</prosody>
<prosody rate="fast">Fast text</prosody>
```

### 停顿设置

```xml
<break time="500ms"/>
```

## 可用语音

- **Алена**（Alena）—— 女性，中性音色（推荐）
- **Андрей**（Andrey）—— 男性，中性音色（推荐）
- **Александра**（Alexandra）—— 女性，柔和音色
- **Антон**（Anton）—— 男性，商务音色

完整列表：请参阅 [references/VOICES.md](references/VOICES.md)

## 示例

更多示例请参阅 [references/EXAMPLES.md](references/EXAMPLES.md)：
- 对话场景
- 播客配音
- 语音通知
- 长文本处理

## 发音指南

有关正确的发音规则，请参阅 [references/TRANSCRIPTION.md](references/TRANSCRIPTION.md)：
- OpenAI → Оупен Эй Ай (OpenAI → Open AI)
- GPT → Джи Пи Ти (GPT → GPT)
- Samsung → Самсунг (Samsung → Samsung)
- Altman → Ал+ьтман (Altman → Altman)

## SSML 参考资料

- 完整的、易于理解的 SSML 文档：[references/SSML.md](references/SSML.md)（推荐阅读）
- 快速参考：[references/SSML_CHEATSHEET.md](references/SSML_CHEATSHEET.md)
- Zvukogram 官方 SSML 文档：https://zvukogram.com/node/ssml/

## 故障排除

有关 API 错误、音频问题及诊断信息，请参阅 [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)

## API 限制

- 每个请求的最大字符数为 1000 个字符（`/text` 方法）
- 使用 `/longtext` 方法最多可处理 100 万个字符
- 在使用 API 时，请勿依赖 `<voice>` 或 `<speak>` 标签。对于多语音场景，需要分别生成每个语音片段并合并它们（每个语音片段对应一个请求）。

## 链接

- API 文档：https://zvukogram.com/node/api/
- 语音评分：https://zvukogram.com/rating/
- 技术支持：https://t.me/zvukogram