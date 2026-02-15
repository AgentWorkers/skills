---
name: clips-machine
description: 将长视频转换为流行的短视频片段。自动检测最佳画面，添加时尚的标题字幕，适用于TikTok/Reels/Shorts平台。该工具完全独立，无需依赖任何外部模块，且完全免费。
version: 1.1.0
author: Mayank8290
homepage: https://github.com/Mayank8290/openclaw-video-skills
tags: video, clips, tiktok, reels, shorts, viral, captions, transcription
metadata: { "openclaw": { "requires": { "bins": ["ffmpeg", "yt-dlp", "whisper-cpp"] } } }
---

# Clips Machine

这款工具可将长视频剪辑成适合在TikTok、Reels或Shorts平台上分享的短视频片段。它能够自动识别视频中的精彩瞬间，添加时尚的文字字幕，并支持导出到这些平台。

**完全免费的工具**——完全在您的电脑上运行。

> **喜欢这个工具吗？** 请支持开发者，让它继续免费使用：**[给我买杯咖啡吧](https://buymeacoffee.com/mayank8290)**

## 工具功能

1. **输入** 任意长视频（YouTube链接、播客、直播或本地文件）
2. 使用Whisper（免费且本地运行的工具）进行字幕转录，并标注时间戳
3. 通过人工智能分析识别具有病毒式传播潜力的片段
4. 剪辑出30-60秒的最佳片段
5. 为视频添加动画效果丰富的文字字幕
6. 以9:16的竖屏格式导出，可直接上传到相关平台

## 快速入门

```
Turn this podcast into viral clips: https://youtube.com/watch?v=xyz
```

```
Extract the 5 best moments from my-interview.mp4 and add captions
```

## 命令说明

### 从YouTube链接导入视频
```
/clips-machine https://youtube.com/watch?v=VIDEO_ID
```

### 从本地文件导入视频
```
/clips-machine /path/to/video.mp4
```

### 自定义剪辑片段数量
```
/clips-machine VIDEO --clips 10
```

### 字幕样式选项
```
/clips-machine VIDEO --style [style]
```

可选字幕样式：
- `hormozi`：Alex Hormozi风格的字幕（加粗显示，逐字高亮）——最受用户欢迎
- `minimal`：简洁的白色文字字幕
- `karaoke`：文字颜色随背景变化
- `news`：底部三分之一显示字幕的样式
- `meme`：使用醒目的字体显示字幕（顶部或底部）

## 病毒式传播检测原理

人工智能会分析字幕内容，重点关注以下元素：
1. **吸引人的开场白**
2. **充满情感的高潮部分**
3. **值得铭记的台词**
4. **具有争议性的观点**
5. **令人惊讶的事实**
6. **实用的建议**

每个片段都会被赋予一个1-100分的“病毒传播潜力评分”。

## 输出格式

```
~/Videos/OpenClaw/clips-[video-name]/
├── transcript.json      # Full transcript with timestamps
├── viral_moments.json   # Detected moments with scores
├── clip_001.mp4         # First viral clip (vertical, captioned)
├── clip_002.mp4         # Second viral clip
├── clip_003.mp4         # ...
└── summary.md           # Overview of all clips
```

## 支持的视频来源

| 来源 | 示例 |
|--------|---------|
| YouTube | `https://youtube.com/watch?v=...` |
| TikTok | `https://tiktok.com/@user/video/...` |
| Twitter/X | `https://twitter.com/user/status/...` |
| Twitch视频 | `https://twitch.tv/videos/...` |
| 本地MP4文件 | `/path/to/file.mp4` |

## 系统要求

- FFmpeg（需通过`brew install ffmpeg`安装）
- yt-dlp（需通过`brew install yt-dlp`安装）
- Whisper.cpp（需通过`brew install whisper-cpp`安装）

## 安装步骤

```bash
# Install dependencies
brew install ffmpeg yt-dlp whisper-cpp

# Or on Linux
sudo apt install ffmpeg
pip install yt-dlp
# Build whisper.cpp from source
```

## 盈利方式

| 盈利方式 | 潜在收益 |
|--------|-----------|
| 为创作者提供视频剪辑服务 | 每个视频50-150美元 |
| 提供月度订阅服务 | 每个客户500-2000美元 |
| 为播客提供剪辑服务 | 每月2000-5000美元 |
| 在ClawHub平台上出售该工具 | 每个工具100-300美元 |

## 使用示例

- **将播客转换为短视频片段**
```
Take this 2-hour podcast and find the 10 best moments:
https://youtube.com/watch?v=PODCAST_ID
Make them Hormozi-style with bold captions.
```

- **提取采访中的精彩部分**
```
/clips-machine interview.mp4 --clips 5 --style minimal
```

- **剪辑游戏直播内容**
```
Extract funny moments from my Twitch VOD:
https://twitch.tv/videos/12345
Add meme-style captions
```

---

## 支持本项目

如果这个工具帮您节省了时间或带来了收益，欢迎考虑给我买杯咖啡！

**[给我买杯咖啡吧](https://buymeacoffee.com/mayank8290)**

每一杯咖啡都能帮助我为社区开发更多免费工具。

---

本工具由OpenClaw平台开发，基于Whisper和FFmpeg技术实现。**支持开发者，请点击这里购买咖啡！** [https://buymeacoffee.com/mayank8290]