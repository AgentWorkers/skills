---
name: youtube-watcher
description: 从 YouTube 视频中获取并读取字幕。当你需要总结视频内容、回答有关视频的问题或从中提取信息时，可以使用此功能。
author: michael gathara
version: 1.0.0
triggers:
  - "watch youtube"
  - "summarize video"
  - "video transcript"
  - "youtube summary"
  - "analyze video"
metadata: {"clawdbot":{"emoji":"📺","requires":{"bins":["yt-dlp"]},"install":[{"id":"brew","kind":"brew","formula":"yt-dlp","bins":["yt-dlp"],"label":"Install yt-dlp (brew)"},{"id":"pip","kind":"pip","package":"yt-dlp","bins":["yt-dlp"],"label":"Install yt-dlp (pip)"}]}}
---

# YouTube 观看器

从 YouTube 视频中获取字幕，以便进行内容摘要、质量评估（QA）和信息提取。

## 使用方法

### 获取字幕

检索视频的文字字幕。

```bash
python3 {baseDir}/scripts/get_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

## 示例

**对视频进行摘要：**

1. 获取字幕：
   ```bash
   python3 {baseDir}/scripts/get_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
   ```
2. 阅读输出内容并为用户生成摘要。

**查找特定信息：**

1. 获取字幕。
2. 在文本中搜索关键词，或根据内容回答用户的问题。

## 注意事项

- 需要安装 `yt-dlp` 并将其添加到系统的 PATH 环境变量中。
- 该工具支持带有字幕（CC）或自动生成字幕的视频。
- 如果视频没有字幕，脚本将失败并显示错误信息。