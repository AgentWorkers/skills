---
name: social-video-analyzer
description: "您可以从 Instagram、YouTube、TikTok、X/Twitter、Reddit、Facebook、Vimeo、Twitch 以及 1000 多个其他平台下载并分析任何社交媒体视频。利用 Gemini 的原生视频理解功能，您可以获取完整的视频字幕、视觉场景描述、关键要点以及内容格式分析结果。该工具支持自定义分析需求，适用于竞争分析、内容再利用、广告分析以及影响者追踪等场景。它基于 yt-dlp 进行视频下载，并使用 Google Gemini 进行内容分析。适用于视频转录、社交媒体监控、内容分析、竞争对手研究、视频摘要生成以及多媒体智能分析等任务。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["GOOGLE_AI_API_KEY"]}, "primaryEnv": "GOOGLE_AI_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🎬 社交媒体视频分析工具

您可以下载并分析来自各种社交媒体的视频——包括 Instagram、YouTube、TikTok、X（Twitter 的前身）、Reddit 以及 1000 多个其他平台。

## 主要功能

- **从 1000 多个平台下载视频**：支持使用 yt-dlp 工具下载视频（YouTube、Instagram、TikTok、X、Reddit、Facebook、Vimeo、Twitch）。
- **完整转录音频**：能够提取视频中的所有语音内容。
- **详细分析视频画面**：逐帧解析视频中的场景。
- **提取关键信息**：总结视频的主要内容。
- **分析视频格式**：包括平台、时长、制作风格和视频质量。
- **自定义查询**：可以对视频提出具体问题。
- **原生视频处理**：Gemini 可以直接处理视频内容（而非仅提取帧数据）。
- **支持 Shell 和 Python 接口**：提供简洁的 Shell 脚本或完整的 Python 控制方式。
- **自动清理临时文件**：系统会自动管理临时下载的文件。
- **支持大文件**：每个视频的大小限制为 2GB（Gemini API 的规定）。

## 必需的配置项

| 变量          | 是否必需 | 说明                          |
|-----------------|---------|---------------------------------------------|
| `GOOGLE.AI_API_KEY` | ✅      | 请从 [Google AI Studio](https://aistudio.google.com/apikey) 获取 API 密钥。 |

## 快速入门

```bash
# Quick analysis (shell)
./skills/social-video-analyzer/scripts/analyze_video.sh "https://www.youtube.com/watch?v=VIDEO_ID"

# Full control (Python)
GOOGLE_AI_API_KEY=your_key python3 skills/social-video-analyzer/scripts/analyze_video.py "https://youtube.com/watch?v=VIDEO_ID"

# Custom question
python3 skills/social-video-analyzer/scripts/analyze_video.py "https://tiktok.com/@user/video/123" --prompt "What product is being advertised?"
```

## 命令说明

### Shell 脚本（快速使用）
```bash
./scripts/analyze_video.sh "VIDEO_URL"
```

### Python 脚本（完全控制）
```bash
# Default analysis
python3 scripts/analyze_video.py "VIDEO_URL"

# Custom prompt
python3 scripts/analyze_video.py "VIDEO_URL" --prompt "Your question"

# Competitive analysis
python3 scripts/analyze_video.py "VIDEO_URL" --prompt "What hooks and CTAs are used?"

# Content repurposing
python3 scripts/analyze_video.py "VIDEO_URL" --prompt "Extract quotes suitable for social media posts"
```

## 输出格式

```
## Transcript
[Full spoken content]

## Visual Description
[Scene-by-scene breakdown]

## Key Takeaways
- Point 1
- Point 2

## Content Format Analysis
- Platform: YouTube
- Duration: ~3:20
- Style: Tutorial/explainer
- Production: Professional
```

## 支持的平台

YouTube、Instagram、TikTok、X（Twitter 的前身）、Reddit、Facebook、Vimeo、Twitch 以及 [1000 多个其他平台](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)。

## 脚本参考

| 脚本          | 说明                          |
|---------------|---------------------------------------------|
| `{baseDir}/scripts/analyze_video.sh` | 用于视频分析的简单 Shell 脚本。            |
| `{baseDir}/scripts/analyze_video.py` | 提供自定义查询功能的完整 Python CLI 程序。         |

## 注意事项

- 视频的最大大小限制为 2GB（Gemini API 的规定）。
- 部分私密或需要登录才能访问的视频可能无法被下载。
- 不同平台可能有不同的数据使用限制。

## 数据政策

视频会被临时下载用于分析，随后上传至 Google Gemini API 进行处理，并在 48 小时后自动删除。

---

开发者：[M. Abidi](https://www.agxntsix.ai)

[LinkedIn](https://www.linkedin.com/in/mohammad-ali-abidi) · [YouTube](https://youtube.com/@aiwithabidi) · [GitHub](https://github.com/aiwithabidi) · [预约咨询](https://cal.com/agxntsix/abidi-openclaw)