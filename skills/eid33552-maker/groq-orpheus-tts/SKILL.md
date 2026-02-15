---
name: openclaw-groq-orpheus-tts
description: 快速且免费的阿拉伯语（沙特阿拉伯）和英语人工智能语音服务。通过 Groq API 每天可免费发送 100 次请求。采用 Orpheus 模型提供专业、高质量的文本转语音（TTS）服务。
metadata: {"openclaw":{"emoji":"🎙️","requires":{"bins":["curl","ffmpeg"],"env":["GROQ_API_KEY"]},"primaryEnv":"GROQ_API_KEY"}}
---

# Groq Orpheus TTS

这是一个功能强大且响应速度快的文本转语音（Text-to-Speech, TTS）服务，它利用了Groq的Orpheus模型。

**主要特点：**
- **完全免费：** 支持使用Groq的免费API密钥（每天100次请求）。
- **超快生成速度：** 音频生成几乎可以瞬间完成。
- **高质量语音：** 采用专业的生成式AI技术制作的语音。

**支持的语言：**
- **阿拉伯语：** 真实的沙特阿拉伯方言（语音库包括：`fahad`、`sultan`、`noura`、`lulwa`、`aisha`）。
- **英语：** 表情丰富、音质高的语音（语音库包括：`autumn`、`diana`、`hannah`、`austin`、`daniel`、`troy`）。

## 使用要求

- **API密钥：** 需要从[Groq控制台](https://console.groq.com/keys)获取`GROQ_API_KEY`。该密钥是免费提供的。
- **使用条款：** 在使用英语模型之前，您必须在[Groq Playground](https://console.groq.com/playground?model=canopylabs%2Forpheus-v1-english)上同意`orpheus-v1-english`模型的使用条款。
- **工具要求：** 系统上必须安装`ffmpeg`软件，以便进行音频转换。

## 使用方法

您可以命令该服务说出某些内容，或者直接生成音频文件。

### 可用的语音库

- **阿拉伯语（`ar`）：`fahad`（男性）、`sultan`（男性）、`noura`（女性）、`lulwa`（女性）、`aisha`（女性）。
- **英语（`en`）：`autumn`、`diana`、`hannah`、`austin`、`daniel`、`troy`。

### 命令示例

```bash
# General usage
./groq-tts.sh "Text" output.mp3 [voice] [lang]

# Examples
./groq-tts.sh "أهلا بك" welcome.mp3 fahad ar
./groq-tts.sh "Hello world" hello.mp3 troy en
```

## 聊天互动方式

如果您希望助手以语音形式回复您，请使用以下命令：
```bash
./groq-tts.sh "Your message" /tmp/reply.mp3 fahad ar
# Then include MEDIA:/tmp/reply.mp3 in the response.
```