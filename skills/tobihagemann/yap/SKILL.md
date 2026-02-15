---
name: yap
description: 使用 Apple Speech.framework（适用于 macOS 26 及更高版本）实现快速的设备内语音转文本功能。
homepage: https://github.com/finnvoor/yap
metadata: {"openclaw":{"emoji":"🗣️","os":["darwin"],"requires":{"bins":["yap"]},"install":[{"id":"brew","kind":"brew","formula":"finnvoor/tools/yap","bins":["yap"],"label":"Install yap (brew)"}]}}
---

# yap

使用 `yap` 可以在 macOS 上通过 Apple 的 Speech.framework 快速进行设备上的语音转录。

## 快速入门

```bash
yap transcribe /path/to/audio.mp3
yap transcribe /path/to/audio.m4a --locale de-DE
yap transcribe /path/to/video.mp4 --srt -o captions.srt
```

## 选项

- `--locale <locale>` — 语言区域设置（例如：`de-DE`、`en-US`、`zh-CN`）
- `--censor` — 遮盖某些单词/短语
- `--txt` / `--srt` — 输出格式（默认：txt）
- `-o, --output-file` — 将结果保存到文件而不是标准输出（stdout）

## 相比 Whisper 的优势

- 使用原生 Apple Speech.framework（针对 Apple Silicon 优化）
- 无需下载任何模型
- 处理速度更快
- 内存占用更低

## 注意事项

- 需要 macOS 26 (Tahoe) 或更高版本
- 支持的语言取决于已安装的 Apple Speech 模型