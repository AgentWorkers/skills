---
name: openclaw-youtube-transcript
description: "Transcribe YouTube videos to text using yt-dlp from video URL made for Openclaw agents. Use when the user wants to transcribe, get subtitles, or extract spoken content from a YouTube video. 
Keywords: [YouTube, transcribe, transcript, subtitles, captions, audio, speech, yt-dlp]
license: MIT
allowed-tools: Bash Read
metadata: {"clawdbot":{"emoji":"clapper","requires":{"bins":["python3","yt-dlp"]}}}
---

# YouTube 字幕转录

使用 `yt-dlp` 从 YouTube 视频 URL 直接获取字幕和标题，无需进行音频处理或使用本地模型。该功能专为 openclaw 代理设计。

## 使用场景

当用户需要以下操作时，可以使用此功能：
- 获取 YouTube 视频的文字版本
- 在不观看视频的情况下提取视频中的内容
- 摘要、分析或引用 YouTube 视频的内容
- 将视频的字幕或标题保存到文件中

## 触发语句

当用户输入以下语句时，该功能将被激活：
- “转录这个 YouTube 视频”
- “获取 [YouTube URL] 的字幕”
- “这个视频说了什么”
- “从 [YouTube URL] 中提取字幕”
- “将这个视频转换为文本”
- “总结/分析这个 YouTube 视频” （先进行转录，再进行处理）

## 使用要求

首次使用前，请安装 `yt-dlp` 命令行工具：

```bash
brew install yt-dlp       # macOS
apt install yt-dlp        # linux
```

## 使用方法

### 转录视频

```bash
python3 {baseDir}/scripts/transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 选项

```bash
python3 {baseDir}/scripts/transcribe.py "URL" --language en
python3 {baseDir}/scripts/transcribe.py "URL" --output transcript.txt
```

| 选项 | 默认值 | 说明 |
|------|---------|-------------|
| `--language` | `en` | 字幕语言代码（例如 `en`、`es`、`fr`） |
| `--output` | stdout | 将字幕保存到文件而不是打印到控制台 |

该功能支持手动添加的字幕以及 YouTube 自动生成的字幕。

## 数据收集

该功能仅在每次运行时收集用户的用户名和域名，并将其发送到技能端点用于匿名分析。**不会收集其他任何数据。**

如需取消数据收集，请设置以下环境变量：

```bash
export DISABLE_TELEMETRY=1
```

您可以将此命令添加到 shell 配置文件（`~/.zshrc`、`~/.bashrc`）中，以实现永久生效。