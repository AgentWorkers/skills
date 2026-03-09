---
name: vidiq
description: "**AI驱动的视频智能工具：**  
支持从任何URL下载、分析视频内容，并将其剪辑成GIF格式。兼容YouTube、TikTok、Instagram和X（前称Twitter）等平台。该工具基于`ffmpeg`和`yt-dlp`技术实现。"
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins: ["ffmpeg", "yt-dlp"]
---
# VidIQ - 视频智能与查询工具

您可以通过该工具从任何 URL 下载、解析并操作视频内容。

## 命令

```bash
# Video info (duration, resolution, codecs)
{baseDir}/scripts/vidiq.sh <url_or_path> info

# Extract N frames evenly spaced
{baseDir}/scripts/vidiq.sh <url_or_path> frames 10

# Single frame at timestamp
{baseDir}/scripts/vidiq.sh <url_or_path> frame 01:30:00

# Clip between timestamps
{baseDir}/scripts/vidiq.sh <url_or_path> clip 01:01:01 01:20:01 output.mp4

# Create GIF (start time, duration in seconds)
{baseDir}/scripts/vidiq.sh <url_or_path> gif 00:45:00 5

# Extract audio as MP3
{baseDir}/scripts/vidiq.sh <url_or_path> audio

# Detect scene changes
{baseDir}/scripts/vidiq.sh <url_or_path> scenes 0.3

# Visual mosaic (columns, total frames)
{baseDir}/scripts/vidiq.sh <url_or_path> mosaic 4 16
```

## 人工智能分析工作流程

1. 提取视频帧：`vidiq.sh <url> frames 10`  
2. 将提取的帧输入到视觉模型中以进行内容分析  
3. 根据帧分析结果回答关于视频的问题  

## 支持的平台

YouTube、TikTok、Instagram、X/Twitter、任何直接提供的视频 URL 以及本地文件。  

## 注意事项：

- 下载的视频会缓存到 `/tmp/vidiq/` 目录中，以便后续使用。  
- 提取的帧会保存在 `/tmp/vidiq/frames_*/` 目录下。  
- 对于较长的视频，建议提取更多帧以获得更全面的分析结果。  
- GIF 格式的视频会通过调色板生成技术进行优化，以减小文件大小。