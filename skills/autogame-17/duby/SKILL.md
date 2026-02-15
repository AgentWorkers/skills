---
name: duby
description: 使用 Duby.so API 将文本转换为语音。支持多种语音和情感表达。
tags: [tts, audio, voice, duby]
---

# Duby TTS 技能

使用 Duby.so API 将文本转换为语音。

## 工具

### duby_tts
将文本转换为语音，并返回生成的媒体文件路径。

- **text**（必填）：需要转换的文本。
- **voice_id**（可选）：要使用的语音 ID。默认值为 `2719350d-9f0c-40af-83aa-b3879a115ca1`（Xinduo）。

## 示例

```bash
# Default voice
duby_tts "Hello world"

# Specific voice
duby_tts "Hello world" "some-voice-id"
```

## 实现方式
该功能通过 `tts.sh` 脚本结合 `curl` 和 `jq` 来实现。
脚本中需要设置 `API_KEY`。