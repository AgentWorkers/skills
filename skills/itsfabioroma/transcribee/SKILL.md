---
name: transcribee
description: **功能说明：**  
该工具支持将YouTube视频以及本地音频/视频文件进行转录，并同时标注发言者的身份信息（即“说话者身份”）。当用户提供YouTube视频链接、播客、视频文件或音频文件时，该工具可将其转录为包含发言者标签的文本文件，这些文本文件可直接用于大型语言模型（LLM）的分析。  

**使用场景：**  
- 当用户需要将YouTube视频或本地音频/视频文件转录为文本时，可利用该工具快速生成带有发言者标签的转录结果。  
- 生成的转录文本格式清晰，便于后续的语言模型分析或处理。  

**技术细节：**  
- 该工具能够自动识别视频/音频中的语音内容，并将其转换为文本形式。  
- 在转录过程中，会为每个发言者标注其身份信息（例如：“用户A”、“用户B”等）。  
- 转录结果可用于自然语言处理、语音识别等相关场景。  

**注意事项：**  
- 请确保提供的视频/音频文件质量良好，以便准确地进行语音识别和转录。  
- 该工具不支持实时转录，仅适用于静态文件的处理。
---

# Transcribee

使用 ElevenLabs 工具将 YouTube 视频和本地媒体文件转录为带有说话者标注的文本。

## 使用方法

```bash
# YouTube video
transcribee "https://www.youtube.com/watch?v=..."

# Local video
transcribee ~/path/to/video.mp4

# Local audio
transcribee ~/path/to/podcast.mp3
```

**请务必引用** 包含 `&` 或特殊字符的 URL。

## 输出结果

转录文件保存路径：`~/Documents/transcripts/{category}/{title}-{date}/`

| 文件名 | 用途 |
|------|-----|
| `transcription.txt` | 带有说话者标注的转录文本 |
| `transcription-raw.txt` | 未标注说话者的纯文本文件 |
| `transcription-raw.json` | 单词级别的时间戳信息 |
| `metadata.json` | 视频信息、语言和分类 |

## 支持的格式

- **音频格式：** mp3、m4a、wav、ogg、flac
- **视频格式：** mp4、mkv、webm、mov、avi
- **URL 格式：** youtube.com、youtu.be

## 所需依赖库

```bash
brew install yt-dlp ffmpeg
```

## 常见问题及解决方法

| 错误 | 解决方案 |
|-------|-----|
| 未找到 `yt-dlp` | 使用 `brew install yt-dlp` 安装该工具 |
| 未找到 `ffmpeg` | 使用 `brew install ffmpeg` 安装该工具 |
| API 错误 | 请检查 `transcribee` 目录下的 `.env` 文件 |