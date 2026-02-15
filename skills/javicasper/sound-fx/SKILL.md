---
name: sound-fx
description: 通过 ElevenLabs 的 SFX 工具（text-to-sound）生成简短的声音效果。当你需要掌声、预设笑声、风声、环境音效或短促的音效片段时，可以使用该工具；同时还可以选择将这些音效转换为适合在 WhatsApp 上使用的 .ogg 或 .opus 格式。
---

# 音效（ElevenLabs）

## 概述
使用 ElevenLabs 的 SFX API 根据文本提示生成音效。默认输出格式为 MP3；如需在 WhatsApp 手机上播放，可将其转换为 .ogg/opus 格式。

## 快速入门
1) 设置 API 密钥：
- `ELEVENLABS_API_KEY`（推荐）或 `XI_API_KEY`
- 或在 `~/.clawdbot/clawdbot.json` 文件中设置 `skills."sound-fx".env.ELEVENLABS_API_KEY`

2) 生成音效（MP3 格式）：
```bash
scripts/generate_sfx.sh --text "short audience applause" --out "/tmp/applause.mp3" --duration 1.2
```

3) （如需要）将音效转换为适合 WhatsApp 播放的 .ogg/opus 格式：
```bash
ffmpeg -y -i /tmp/applause.mp3 -c:a libopus -b:a 48k /tmp/applause.ogg
```

## 脚本：scripts/generate_sfx.sh
**使用方法**
```bash
scripts/generate_sfx.sh --text "canned laughter" --out "/tmp/laugh.mp3" --duration 1.5
```

**注意事项**
- 使用 `POST https://api.elevenlabs.io/v1/sound-generation` 进行请求
- 支持可选的 `--duration` 参数（0.5–30 秒）。如果省略该参数，系统会自动设置合适的时长。
- 成功生成音效后，脚本会输出 `MEDIA: <path>`，以便自动将音效文件附加到消息中。

## 示例
- 鼓掌：`"short audience applause"`
- 笑声：`"canned audience laughter"`
- 风声：`"fast whoosh"`
- 环境音效：`"soft rain ambience"`