---
name: video-analyzer
description: 从 YouTube、X/Twitter 和 TikTok 下载视频，对其进行转录和分析，并利用本地 Whisper 处理技术进行处理。非常适合提取视频的精华内容（TL;DR）、时间戳以及有用的信息。
homepage: https://github.com/minilozio/video-analyzer-skill
metadata:
  {
    "openclaw":
      {
        "emoji": "🎥",
        "requires": { "bins": ["uv", "yt-dlp", "ffmpeg", "whisper-cli"] },
        "install":
          [
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
            {
              "id": "yt-dlp-brew",
              "kind": "brew",
              "formula": "yt-dlp",
              "bins": ["yt-dlp"],
              "label": "Install yt-dlp (brew)",
            },
            {
              "id": "ffmpeg-brew",
              "kind": "brew",
              "formula": "ffmpeg",
              "bins": ["ffmpeg"],
              "label": "Install ffmpeg (brew)",
            },
            {
              "id": "whisper-cpp-brew",
              "kind": "brew",
              "formula": "ggerganov/ggerganov/whisper-cpp",
              "bins": ["whisper-cli"],
              "label": "Install whisper-cpp (brew)",
            },
          ],
      },
  }
---
# 视频分析工具 🎥

这是一个用于从任何平台下载、转录和分析视频的工具，它采用了智能的双层系统：使用 `yt-dlp` 来快速获取字幕，同时使用 `local-whisper-cpp` 作为可靠的备用方案。

## 使用方法

当用户要求您对视频或音频进行总结、转录或下载时，请使用随工具提供的 Python 脚本：

```bash
uv run {baseDir}/scripts/analyze_video.py --action <ACTION> --url "<URL>" [--quality <normal|max>] [--lang <en|it|etc>]
```

### 支持的操作：
- `transcript`：提取带有时间戳的文本。**当用户请求摘要或转录内容时，请使用此选项。**
- `download-video`：将视频下载为 MP4 格式到桌面。
- `download-audio`：将音频下载为 M4A/MP3 格式到桌面。

### 视频分析（重要提示）

如果用户要求您提供视频的摘要、分析结果或关键片段：
1. 使用 `--action transcript` 参数运行脚本。
2. 脚本会生成一个包含时间戳的文本文件（格式为 `.txt`）。
3. 读取该文件内容。
4. 请严格按照以下 Markdown 格式回复用户：

```markdown
## 📝 TL;DR
[A punchy 3-sentence summary of the video's core message]

## ⏱️ Key Moments
- [MM:SS] [Brief description of what is discussed]
- [MM:SS] [Brief description of what is discussed]
- [MM:SS] [Brief description of what is discussed]
*(Extract 3 to 7 key moments depending on video length)*

## 💡 Actionable Insights
1. [Practical takeaway 1]
2. [Practical takeaway 2]
3. [Practical takeaway 3]

---
```

### Local Whisper 的质量设置
如果脚本需要使用 `local-whisper` 来处理视频（例如来自 X 或 Twitter 的视频），默认会使用 `normal` 质量设置：
- `normal`：快速处理（30 分钟的视频大约需要 1 分钟）——**默认设置**
- `max`：最高质量（30 分钟的视频大约需要 5 分钟）——在需要高精度时请使用 `--quality max` 参数。

### 多语言支持
所有 `local-whisper` 模型默认支持多种语言。该工具可以转录任何语言的视频（如意大利语、西班牙语、日语等）。

**重要提示：** 请始终用用户的语言回复他们，而不是视频本身的语言。例如，如果用户使用意大利语交流，但发送的是英语视频，那么请用意大利语提供摘要。

### 查找特定片段
转录结果中包含精确的时间戳（例如 `[05:53] text...`）。如果用户询问“他们在何时提到了某个内容？”，请在转录文本中使用 `grep` 命令查找该时间戳，并返回相应的具体时间。