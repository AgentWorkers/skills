---
name: piper-tts
description: 使用 Piper 进行本地文本转语音（Text-to-Speech, TTS）功能，以发送语音消息。当用户需要语音回复、音频消息、TTS 服务、语音笔记，或者希望听到文本被朗读时，可以使用该功能。该服务会本地将文本转换为语音（无需使用云 API，无费用，无延迟），并通过 Telegram、Discord 或任何支持音频传输的渠道将语音消息发送给用户。
---
# Piper TTS — 本地语音消息生成工具

使用 [Piper](https://github.com/rhasspy/piper) 生成语音消息。Piper 是一个快速的本地语音合成引擎，无需连接云端，无需支付费用，也无需使用 API 密钥。

## 安装

如果尚未安装 Piper，请运行安装脚本：

```bash
scripts/setup-piper.sh
```

该脚本会通过 pip 安装 `piper-tts` 并下载默认的语音文件（`en_US-kusal-medium`）。

## 生成语音消息

使用 `scripts/piper-speak.sh` 脚本来生成并发送语音消息：

```bash
scripts/piper-speak.sh "<text>" [voice]
```

- `text`：需要朗读的文本（必填）
- `voice`：Piper 选择的语音类型（默认为 `en_US-kusal-medium`）

脚本会输出生成的 MP3 文件路径。你可以在回复中这样使用该路径：

```
[[audio_as_voice]]
MEDIA:<path-to-mp3>
```

系统会将生成的音频文件作为本地语音消息发送到支持的渠道（如 Telegram、Discord 等）。

## 示例工作流程

1. 用户请求：“用语音讲一个笑话。”
2. 运行 `scripts/piper-speak.sh "Why do programmers prefer dark mode? Because light attracts bugs!"`
3. 从脚本输出中获取 MP3 文件路径
4. 使用 `[[audio_as_voice]] + <MP3路径>` 的格式进行回复

## 可用的语音类型

安装完成后，你可以下载更多语音文件：

```bash
scripts/setup-piper.sh --voice en_US-ryan-high
scripts/setup-piper.sh --voice en_GB-northern_english_male-medium
```

常用语音类型：
- `en_US-kusal-medium`：清晰的男性声音（默认推荐）
- `en_US-ryan-high`：高质量的美国男性声音
- `en_US-hfc_male-medium`：美国男性声音
- `en_GB-northern_english_male-medium`：英国男性声音
- 查看所有语音：https://huggingface.co/rhasspy/piper-voices

## 重要说明

- **生成速度**：本地生成语音的速度约为 0.5–1 秒，远快于云端语音合成服务。
- **无需 API 密钥**：安装完成后可完全离线使用。
- **支持平台**：macOS（Apple Silicon 和 Intel 处理器）、Linux。需要 Python 3.9 或更高版本。
- **注意**：不要在 OpenClaw 配置中设置 `messages.tts.auto: "always"`，否则会导致所有回复的响应速度变慢。请保持语音合成按需触发。