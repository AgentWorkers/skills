---
name: video-understanding
description: >
  Analyze videos with Google Gemini multimodal AI. Download from any URL (Loom, YouTube, TikTok,
  Vimeo, Twitter/X, Instagram, 1000+ sites) and get transcripts, descriptions, and answers to
  questions. Use when asked to watch, analyze, summarize, or transcribe a video, or answer
  questions about video content. Triggers on video URLs or requests involving video understanding.
compatibility: "Requires yt-dlp, ffmpeg, and GEMINI_API_KEY environment variable. Python 3.10+ with uv."
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins: ["yt-dlp", "ffmpeg"]
      env: ["GEMINI_API_KEY"]
    primaryEnv: "GEMINI_API_KEY"
    install:
      - id: "yt-dlp-brew"
        kind: "brew"
        formula: "yt-dlp"
        bins: ["yt-dlp"]
        label: "Install yt-dlp (brew)"
      - id: "ffmpeg-brew"
        kind: "brew"
        formula: "ffmpeg"
        bins: ["ffmpeg"]
        label: "Install ffmpeg (brew)"
---

# 视频理解（Gemini）

使用 Google Gemini 的多模态视频理解功能来分析视频。支持通过 `yt-dlp` 下载 1000 多种视频来源。

## 所需工具

- `yt-dlp` — 使用 `brew install yt-dlp` 或 `pip install yt-dlp` 安装
- `ffmpeg` — 使用 `brew install ffmpeg` （用于合并视频和音频流）
- 环境变量 `GEMINI_API_KEY`

## 默认输出结果

返回结构化的 JSON 数据：
- **transcript**：包含时间戳 `[MM:SS]` 的逐字转录内容
- **description**：视频中的视觉元素描述（人物、场景、用户界面、屏幕上的文字、视频流程）
- **summary**：2-3 句的总结
- **duration_seconds**：视频时长（以秒为单位）
- **speakers**：识别出的说话者

## 使用方法

### 分析视频（返回结构化 JSON 数据）

```bash
uv run {baseDir}/scripts/analyze_video.py "<video-url>"
```

### 提出问题（输出中包含 “answer” 字段）

```bash
uv run {baseDir}/scripts/analyze_video.py "<video-url>" -q "What product is shown?"
```

### 完全替换提示语

```bash
uv run {baseDir}/scripts/analyze_video.py "<video-url>" -p "Custom prompt" --raw
```

### 仅下载视频（不进行分析）

```bash
uv run {baseDir}/scripts/analyze_video.py "<video-url>" --download-only -o video.mp4
```

## 选项

| 选项 | 描述 | 默认值 |
|------|-------------|---------|
| `-q` / `--question` | 需要回答的问题（添加到默认输出字段中） | 无 |
| `-p` / `--prompt` | 完全替换提示语（忽略 `-q` 选项） | 结构化 JSON 数据 |
| `-m` / `--model` | 使用的 Gemini 模型 | `gemini-2.5-flash` |
| `-o` / `--output` | 将输出结果保存到文件 | `stdout` |
| `--keep` | 保留下载的视频文件 | `false` |
| `--download-only` | 仅下载视频，不进行分析 | `false` |
| `--max-size` | 文件最大大小（MB） | 500 |
| `--raw` | 输出原始文本而非 JSON 格式 | `false` |

## 工作原理

1. **YouTube 链接**：直接传递给 Gemini（无需下载）
2. **其他所有链接**：通过 `yt-dlp` 下载后上传到 Gemini 的文件 API，然后等待处理结果
3. Gemini 使用结构化的提示语分析视频，并返回 JSON 数据
4. 使用过程中生成的临时文件会自动清理

## 支持的视频来源

所有支持 [yt-dlp](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) 的视频来源：Loom、YouTube、TikTok、Vimeo、Twitter/X、Instagram、Dailymotion、Twitch 等。

## 使用技巧

- 使用 `-q` 选项可以针对特定内容提出问题
- YouTube 的分析速度最快（无需下载视频）
- 大文件（超过 10 分钟）也能正常处理 — Gemini File API 支持免费存储 2GB 的视频，付费用户可存储 20GB
- 该脚本会通过 `uv` 自动安装 Python 依赖库