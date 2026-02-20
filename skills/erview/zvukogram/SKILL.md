---
name: zvukogram
description: 通过 Zvukogram API 实现文本转语音功能，该 API 支持 SSML（Speech Synthesis Markup Language）格式。适用于需要将文本转换为语音、制作播客、生成语音通知或处理音频文件的场景。支持调整语速、添加重音符号、进行英文单词的转写以及合并音频片段等功能。
requires:
  env: [ZVUKOGRAM_TOKEN, ZVUKOGRAM_EMAIL]
  credentials: zvukogram_api
---
# Zvukogram TTS

通过 Zvukogram API 生成语音，支持 SSML 标记语言。

## 使用要求

要使用此功能，您需要：
- **Zvukogram API 令牌** — 可在 https://zvukogram.com/ 获取
- **Zvukogram 账户邮箱**

### 设置

创建文件 `~/.config/zvukogram/config.json`：
```bash
mkdir -p ~/.config/zvukogram
```

### 或使用环境变量：
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
- **SSML 支持** — 重音符号、停顿、语速控制
- **音频合并** — 可使用 ffmpeg 合并音频片段
- **转录** — 确保英语单词的发音准确

## SSML 标记语言

### 重音符号
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

- **Алена** — 女性，中性音色（推荐）
- **Андрей** — 男性，中性音色（推荐）
- **Александра** — 女性，柔和音色
- **Антон** — 男性，商务音色

完整列表：请参阅 [references/VOICES.md](references/VOICES.md)

## 示例

请参阅 [references/EXAMPLES.md](references/EXAMPLES.md)，了解以下应用场景：
- 对话和播客
- 新闻旁白
- 语音通知
- 长文本朗读

## 发音规则

请参阅 [references/TRANSCRIPTION.md](references/TRANSCRIPTION.md)，了解正确的发音规则：
- OpenAI → Оупен Эй Ай (OpenAI)
- GPT → Джи Пи Ти (GPT)
- Samsung → Самсунг (Samsung)
- Altman → Ал+ьтман (Altman)

## SSML 标记语言参考

请参阅 [references/SSML_CHEATSHEET.md](references/SSML_CHEATSHEET.md)，快速查找相关标签说明。

## 故障排除

请参阅 [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)，了解以下问题的解决方法：
- API 错误
- 音频问题
- 故障诊断

## API 限制

- 每次请求的最大字符数为 1000 个
- 通过 `/longtext` 接口可处理最多 100 万个字符
- API 不支持带有 `<voice>` 标签的 SSML 标记（仅支持网页端）
- 如需使用多种语音，请合并音频片段

## 链接

- API 文档：https://zvukogram.com/node/api/
- 语音评分：https://zvukogram.com/rating/
- 技术支持：https://t.me/zvukogram