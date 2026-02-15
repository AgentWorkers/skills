---
name: ffmpeg-master
version: 1.0.0
description: **使用说明：**  
在使用 FFmpeg 执行视频/音频处理任务时（如转码、过滤、流媒体传输、元数据操作或复杂的过滤图操作），请参考以下说明。
triggers:
  - ffmpeg
  - ffprobe
  - video processing
  - audio conversion
  - codec
  - transcoding
  - filter_complex
  - h264
  - h265
  - mp4
  - mkv
  - hardware acceleration
role: specialist
scope: implementation
output-format: shell-command
---

# FFmpeg 使用指南

本指南提供了使用 FFmpeg 和 FFprobe 进行专业视频和音频处理的全面指导。

## 核心概念

FFmpeg 是领先的多媒体处理框架，能够**解码、编码、转码、复用、解复用、流处理、过滤以及播放**几乎所有由人类或机器生成的媒体文件。它是一个命令行工具，通过一系列解复用器、解码器、过滤器和编码器来处理媒体流。

## 常见操作

```bash
# Basic Transcoding (MP4 to MKV)
ffmpeg -i input.mp4 output.mkv

# Change Video Codec (to H.265/HEVC)
ffmpeg -i input.mp4 -c:v libx265 -crf 28 -c:a copy output.mp4

# Extract Audio (No Video)
ffmpeg -i input.mp4 -vn -c:a libmp3lame -q:a 2 output.mp3

# Resize/Scale Video
ffmpeg -i input.mp4 -vf "scale=1280:720" output.mp4

# Cut Video (Start at 10s, Duration 30s)
ffmpeg -i input.mp4 -ss 00:00:10 -t 00:00:30 -c copy output.mp4

# Fast Precise Cut (Re-encoding only the cut points is complex, so standard re-encoding is safer for precision)
ffmpeg -ss 00:00:10 -i input.mp4 -to 00:00:40 -c:v libx264 -crf 23 -c:a aac output.mp4

# Concatenate Files (using demuxer)
# Create filelist.txt: file 'part1.mp4' \n file 'part2.mp4'
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4

# Speed Up/Slow Down Video (2x speed)
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" output.mp4
```

---

## 处理类别及使用场景

### 编解码器与画质
| 选项 | 使用场景 |
|-----------|----------|
| `-c:v libx264` | 标准的 H.264 编码（最佳兼容性） |
| `-c:v libx265` | H.265/HEVC 编码（最佳压缩比/画质） |
| `-crf [0-51]` | 常量比特率因子（数值越低，画质越高，推荐范围为 18-28） |
| `-preset` | 编码速度与压缩质量的平衡（超快、中等、非常慢） |
| `-c:a copy` | 直接传输音频数据（避免重新编码，节省时间和保持画质） |

### 过滤器与视频处理
| 过滤器 | 使用场景 |
|-----------|----------|
| `scale` | 更改视频分辨率（例如：`scale=1920:-1` 可得到 1080p 分辨率） |
| `crop` | 剪裁视频边框（例如：`crop=w:h:x:y`） |
| `transpose` | 旋转视频（1=顺时针 90 度，2=逆时针 90 度） |
| `fps` | 更改帧率（例如：`fps=30`） |
| `drawtext` | 添加文字叠加层或水印 |
| `overlay` | 图像叠加或添加图片水印 |
| `fade` | 添加淡入/淡出效果（例如：`fade=in:0:30` 表示前 30 帧淡入） |
| `volume` | 调整音频音量（例如：`volume=1.5` 表示音量放大 150%） |
| `setpts` | 改变视频播放速度（例如：`setpts=0.5*PTS` 表示速度加倍） |
| `atempo` | 改变音频播放速度（不改变音调） |

### 文件检查与元数据
| 工具/选项 | 使用场景 |
|-----------|----------|
| `ffprobe -v error -show_format -show_streams` | 获取文件的详细技术信息 |
| `-metadata title="Name"` | 设置全局元数据标签 |
| `-map` | 选择特定的媒体流（例如：`-map 0:v:0 -map 0:a:1`） |

---

## 高级用法：复杂的过滤链

当需要处理多个输入或创建非线性的过滤链时，可以使用 `filter_complex`。

```bash
# Example: Adding a watermark at the bottom right
ffmpeg -i input.mp4 -i watermark.png -filter_complex "overlay=main_w-overlay_w-10:main_h-overlay_h-10" output.mp4

# Example: Vertical Stack (2 videos)
ffmpeg -i top.mp4 -i bottom.mp4 -filter_complex "vstack=inputs=2" output.mp4

# Example: Side-by-Side (2 videos)
ffmpeg -i left.mp4 -i right.mp4 -filter_complex "hstack=inputs=2" output.mp4

# Example: Grid (4 videos 2x2)
ffmpeg -i v1.mp4 -i v2.mp4 -i v3.mp4 -i v4.mp4 -filter_complex "[0:v][1:v]hstack=inputs=2[top];[2:v][3:v]hstack=inputs=2[bottom];[top][bottom]vstack=inputs=2" output.mp4

# Example: Fade Transition (Simple crossfade between two clips)
# Requires manual offset calculation, using xfade is better
ffmpeg -i input1.mp4 -i input2.mp4 -filter_complex "xfade=transition=fade:duration=1:offset=9" output.mp4
```

## 硬件加速

| 平台 | 编解码器 | 命令 |
|----------|-------|---------|
| NVIDIA (NVENC) | H.264 | `-c:v h264_nvenc` |
| Intel (QSV) | H.264 | `-c:v h264_qsv` |
| Apple (VideoToolbox) | H.265 | `-c:v hevc_videotoolbox` |

## 注意事项与错误处理

- **流映射**：对于复杂的文件，务必使用 `-map` 选项以确保正确获取音频和字幕轨道。
- **快速定位**：使用 `-ss` 选项时，若需快速定位文件中的某个位置（输入定位），请将其放在 `-i` 之前；若需精确定位输出文件中的某个位置，则将其放在 `-i` 之后。
- **格式兼容性**：确保输出文件的格式（扩展名）支持所选用的编码器。