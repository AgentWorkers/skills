---
name: video-subtitles
description: 该工具可以从视频/音频文件中生成SRT字幕，并支持翻译功能。它可以识别并转录希伯来语（ivrit.ai）和英语（whisper）文本，实现语言之间的互译，并将生成的字幕嵌入到视频中。这些字幕可用于制作视频字幕、文本记录，或作为WhatsApp/社交媒体的固定字幕。
---

# 视频字幕

从视频或音频文件中生成电影风格的字幕。支持转录、翻译以及将字幕直接嵌入到视频中。

## 特点

- **希伯来语**：使用 ivrit.ai 优化过的模型（最佳的希伯来语转录效果）  
- **英语**：使用 OpenAI Whisper large-v3 模型  
- **自动检测**：自动检测语言并选择最合适的模型  
- **翻译**：将希伯来语翻译成英语  
- **嵌入视频**：将字幕硬编码到视频中（在所有平台上均可见，包括 WhatsApp）  
- **电影风格**：字幕行长度为 42 个字符，每行间隔 1-7 秒  

## 快速入门

```bash
# Plain transcript
./scripts/generate_srt.py video.mp4

# Generate SRT file
./scripts/generate_srt.py video.mp4 --srt

# Burn subtitles into video (always visible)
./scripts/generate_srt.py video.mp4 --srt --burn

# Translate to English + burn in
./scripts/generate_srt.py video.mp4 --srt --burn --translate en

# Force language
./scripts/generate_srt.py video.mp4 --lang he    # Hebrew
./scripts/generate_srt.py video.mp4 --lang en    # English
```

## 参数选项

| 参数 | 说明 |
|------|-------------|
| `--srt` | 生成 SRT 格式的字幕文件 |
| `--burn` | 将字幕嵌入到视频中（字幕始终可见） |
| `--embed` | 嵌入软字幕（在播放器中可切换显示） |
| `--translate en` | 将文本翻译成英语 |
| `--lang he/en` | 强制指定输入语言 |
| `-o FILE` | 自定义输出路径 |

## 输出结果

- **默认**：将转录结果以纯文本形式输出到标准输出（stdout）  
- **使用 `--srt` 选项**：会生成 `video.srt` 文件  
- **使用 `--burn` 选项**：会生成包含硬编码字幕的 `video_subtitled.mp4` 文件  

## 系统要求

- **uv**：Python 包管理工具（用于自动安装依赖库）  
- **ffmpeg-full**：用于将字幕嵌入视频（需通过 `brew install ffmpeg-full` 安装）  
- **模型文件**：每个模型约 3GB 大小，首次使用时会自动下载  

## 字幕样式

- 字体大小：12 号  
- 文字颜色：白色  
- 字幕边框：黑色  
- 字幕位置：底部对齐  
- 每行最多 42 个字符  
- 在标点符号和停顿处自动换行