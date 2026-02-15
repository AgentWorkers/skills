---
name: x-video-transcribe
description: 使用 bird CLI 和 Gemini 音频转录工具来转录并总结 X/Twitter 视频的内容。
---

# X 视频转录工具

该工具可将 X（Xigua）或 Twitter 上的视频帖子转录为文本。它首先下载视频文件，提取音频内容，然后使用 Gemini 人工智能引擎进行准确的转录。

## 使用场景

- 用户分享了包含视频的 X/Twitter 链接。
- 用户请求“转录这条推文”或“这个视频说了什么”。
- 用户希望获取某个 X 视频的摘要。

## 使用方法

```bash
# Basic transcript
~/agent-workspace/skills/x-video-transcribe/scripts/transcribe.sh "https://x.com/user/status/123"

# With summary
~/agent-workspace/skills/x-video-transcribe/scripts/transcribe.sh "https://x.com/user/status/123" --summary

# Save to file
~/agent-workspace/skills/x-video-transcribe/scripts/transcribe.sh "https://x.com/user/status/123" --summary --output /tmp/transcript.md
```

## 工作流程

1. **bird CLI**：获取推文的 JSON 数据，并从中提取视频链接。
2. **curl**：下载视频文件（格式为 MP4）。
3. **ffmpeg**：将视频文件转换为 MP3 格式（音频文件通常比视频文件小得多）。
4. **Gemini API**：使用 `gemini-2.0-flash` 模型对提取的音频文件进行转录。

## 所需软件/环境

- **bird CLI**（需具备身份验证功能；认证信息存储在 `~/agent-workspace/secrets/bird.env` 文件中）。
- **ffmpeg**：用于视频文件处理。
- **GEMINI_API_KEY**：Google Gemini API 的访问密钥（作为环境变量设置）。

## 环境配置

| 变量        | 默认值         | 说明                          |
|-------------|--------------|-------------------------------------------|
| `GEMINI_API_KEY` | （必填）       | Google Gemini API 的访问密钥                |
| `BIRD_ENV`    | `~/agent-workspace/secrets/bird.env` | 存储 bird 认证信息的路径                |
| `GEMINI_MODEL` | `gemini-2.0-flash` | 用于转录的 Gemini 模型                    |