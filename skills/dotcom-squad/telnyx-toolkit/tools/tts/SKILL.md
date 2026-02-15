---
name: telnyx-tts
description: 使用 Telnyx 的文本转语音（Text-to-Speech）API 从文本生成语音音频。适用于需要将文本转换为语音、创建语音消息或生成音频内容的情况。
metadata: {"openclaw":{"emoji":"🔊","requires":{"bins":["python3"],"env":["TELNYX_API_KEY"]},"primaryEnv":"TELNYX_API_KEY"}}
---

# Telnyx 文本转语音（Text-to-Speech）

使用 Telnyx 的 TTS API 从文本生成高质量的语音音频。

## 使用方法

要将文本转换为语音，请运行以下脚本：

```bash
{baseDir}/scripts/telnyx-tts.py "Your text here" -o /tmp/output.mp3
```

脚本在成功执行后会输出生成的音频文件的路径。

## 选项

- `-o, --output PATH`：输出文件路径（默认值：output.mp3）
- `--voice VOICE`：语音 ID（默认值：Telnyx.NaturalHD.astra）

## 可用的语音选项

Telnyx 提供多种语音选项：

- **Telnyx NaturalHD**：具有精致语调的高级语音
  - `Telnyx.NaturalHD.astra`（默认值）
  - `Telnyx.NaturalHD.luna`
  - `Telnyx.NaturalHD.andersen_johan`
- **Telnyx KokoroTTS**：适合大量使用的经济型语音
  - `Telnyx.KokoroTTS.af`
  - `Telnyx.KokoroTTS.am`

## 示例

生成语音并将其作为媒体文件返回：

```bash
{baseDir}/scripts/telnyx-tts.py "Hello! This is a test of Telnyx text to speech." -o /tmp/tts-output.mp3
```

然后返回生成的音频文件：

```
MEDIA: /tmp/tts-output.mp3
```

对于 Telegram 的语音消息功能，音频将以语音消息的形式发送。

## 环境要求

需要设置 `TELNYX_API_KEY` 环境变量。