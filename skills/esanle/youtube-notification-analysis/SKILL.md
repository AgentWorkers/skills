---
name: youtube-notification-analysis
description: 分析 YouTube 通知以获取投资和交易相关的信息。适用于用户希望从 YouTube 获取投资建议、分析股票、加密货币或金融相关内容的情况，或者执行 `/ytb_trade` 命令，以及通过 `yt-dlp` 和 `whisper-cpp` 获取视频字幕的场景。工作流程如下：用户点击 YouTube 通知，系统提取视频 ID，然后下载视频并获取字幕；接着使用 `whisper-cpp` 进行分析，最后执行相应的交易操作。
---
# YouTube通知分析

分析YouTube通知以获取投资线索。

## 工作流程

1. **打开YouTube**：使用浏览器执行以下操作：`browser action=open profile=openclaw targetUrl=https://www.youtube.com`
2. **点击通知图标**：找到标有`ref="e8"`的按钮。
3. **提取视频ID**：从视频截图中找出与投资相关的视频。
4. **获取字幕**：
   - 首次尝试：使用命令 `yt-dlp --write-subs --skip-download --sub-lang zh-Hans,en <video_url>`
   - 如果没有字幕，则下载视频并使用`whisper-cpp`进行分析。
5. **分析内容**：总结投资建议。
6. **执行交易**：使用`tiger-trade`技能进行交易操作。

## 字幕提取

```bash
# Try yt-dlp first
yt-dlp --write-subs --skip-download --sub-lang zh-Hans,en "https://www.youtube.com/watch?v=VIDEO_ID" -o /tmp/sub

# If no subtitles, download + whisper
yt-dlp -f best "https://www.youtube.com/watch?v=VIDEO_ID" -o /tmp/video.mp4
whisper-cpp/bin/main -m whisper-cpp/models/ggml-base.bin -f /tmp/video.mp4 --language ZH
```

## 投资分析

专注于从YouTube通知中提取的与投资和交易相关的视频。分析这些视频的内容，以了解股票、加密货币、宏观金融和市场趋势。

## 日志记录

所有日志均保存在`/tmp/youtube_investment_*.log`文件中。