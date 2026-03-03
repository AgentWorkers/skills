---
name: edge-tts-english
description: 使用 Microsoft Edge TTS 生成高质量的英语（以及多种语言）音频。当用户请求“将这段文字读出来”、“用英语发音”、“大声朗读”、“用英语说这个内容”时，可以使用该功能。该功能还支持使用美式和英式英语（男性和女性声音）。需要通过 `pipx` 安装 `edge-tts` 插件。生成的 MP3 文件会直接发送给用户。
---
# Edge TTS（英语）

使用 Microsoft Edge TTS 生成原生质量的英语音频（路径：`/root/.local/bin/edge-tts`）。

## 工作流程

1. 运行命令：`scripts/speak.sh "<text>" [voice] [output_path]`
2. 通过 `message` 工具将生成的 MP3 文件发送给用户，同时指定媒体文件路径为 `media=<output_path>`。

```bash
bash scripts/speak.sh "Hello, world!" en-US-AriaNeural /tmp/tts_out.mp3
```

## 可用语音

| 语音 | 风格 |
|---|---|
| `en-US-AriaNeural` | 女性，美国口音（默认） |
| `en-US-JennyNeural` | 女性，美国口音，温暖的语调 |
| `en-US-GuyNeural` | 男性，美国口音 |
| `en-GB-SoniaNeural` | 女性，英国口音 |
| `en-GB-RyanNeural` | 男性，英国口音 |

查看所有可用语音的列表：`/root/.local/bin/edge-tts --list-voices | grep en-`

## 注意事项

- 脚本路径：相对于当前技能目录计算。
- Edge TTS 可执行文件：`/root/.local/bin/edge-tts`
- 默认输出文件路径：`/tmp/edge_tts_output.mp3`
- 请始终通过 `message` 工具发送音频文件（使用 `media` 参数），而不是以文本形式发送。