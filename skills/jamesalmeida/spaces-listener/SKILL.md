---
name: spaces-listener
description: **功能概述：**  
记录、转录并总结 X/Twitter Spaces 的内容（无论是直播还是回放）。通过 `yt-dlp` 自动下载音频文件，使用 `Whisper` 进行转录，并生成人工智能生成的摘要。  

**核心功能：**  
1. **实时记录与转录**：实时捕捉并转录 X/Twitter Spaces 的音频内容。  
2. **自动下载音频**：利用 `yt-dlp` 工具将音频文件下载到本地。  
3. **智能转录**：通过 `Whisper` 技术实现高效、准确的音频转录。  
4. **摘要生成**：利用人工智能算法生成内容的简洁摘要。  

**技术实现细节：**  
- **音频下载**：使用 `yt-dlp` 从 YouTube 下载音频文件。  
- **转录工具**：采用 `Whisper` 进行音频转录，支持多种语言。  
- **摘要生成**：利用自然语言处理技术（NLP）提取音频内容的精华并生成摘要。  

**应用场景：**  
- **媒体编辑**：适用于媒体机构或个人，用于整理和编辑直播内容。  
- **内容分析**：帮助分析师快速理解直播内容的核心信息。  
- **教育用途**：支持教师和学生回顾直播课程。  

**注意事项：**  
- **版权问题**：确保遵守相关版权法规，仅使用公开可用的音频资源。  
- **技术限制**：部分功能可能受平台限制或网络条件影响。
version: 1.6.0
author: jamesalmeida
tags: [twitter, x, spaces, transcription, summarization, audio, recording]
when: "User asks to record, transcribe, or listen to an X/Twitter Space"
examples:
  - "Record this Space"
  - "Transcribe this X Space"
  - "Listen to this Twitter Space and transcribe it"
  - "Download this Space audio"
metadata:
  openclaw:
    requires:
      bins: ["yt-dlp", "ffmpeg"]
    emoji: "🎧"
---

# spaces-listener

该工具用于录制、转录并总结X/Twitter Spaces的内容（无论是实时直播还是回放），同时支持多个任务同时进行。

## 命令

```bash
# Start recording (runs in background)
spaces listen <url>

# Record multiple Spaces at once
spaces listen "https://x.com/i/spaces/1ABC..."
spaces listen "https://x.com/i/spaces/2DEF..."

# List all active recordings
spaces list

# Check specific recording status
spaces status 1

# Stop a recording
spaces stop 1
spaces stop all

# Clean stale pid/meta files
spaces clean

# Transcribe when done
spaces transcribe ~/Desktop/space.m4a --model medium

# Summarize an existing transcript
spaces summarize ~/Desktop/space_transcript.txt

# Skip summarization
spaces transcribe ~/Desktop/space.m4a --no-summarize
```

## 系统要求

```bash
brew install yt-dlp ffmpeg openai-whisper
```

如需生成内容摘要，请设置 `OPENAI_API_KEY`（即使不设置该参数，转录功能仍可正常使用）。

## 工作原理

1. 每次执行 `spaces listen` 命令时，系统会启动一个新的后台录制任务，并为该任务分配一个唯一的ID。
2. 即使关闭终端，录制任务也会继续进行。
3. 可通过运行 `spaces list` 命令查看所有正在进行的录制任务。
4. 完成录制后，可以使用 `spaces stop <id>` 或 `spaces stop all` 命令停止特定任务或所有任务。
5. 使用 `spaces transcribe <file>` 命令对音频文件进行转录。
6. 转录完成后，系统会自动生成内容摘要（如需跳过摘要生成，可使用 `--no-summarize` 选项）。

## 输出结果

每个录制的Space内容都会被保存在 `~/Dropbox/ClawdBox/XSpaces/` 目录下的单独文件夹中：
```
~/Dropbox/ClawdBox/XSpaces/
  space_username_2026-02-03_1430/
    recording.m4a     — audio
    recording.log     — progress log
    transcript.txt    — transcript
    summary.txt       — summary
```

## 重要提示：代理使用规则

**切勿为Space内容的下载设置超时**——某些Space的录制时长可能长达数小时。yt-dlp工具会在Space内容播放结束后自动停止下载，切勿提前终止下载进程。

正确的工作流程如下：
1. 运行 `spaces listen <url>` 命令，该命令会启动一个后台进程并立即返回结果。
2. 设置一个 **定时任务**（每5–10分钟执行一次），用于检查是否有正在进行的录制任务。
3. 当系统显示“没有正在进行的录制任务”时，表示录制已完成。
4. 对音频文件进行转录并生成摘要，然后通知用户。
5. 删除定时任务。

**禁止的操作**：
- 不要使用带有下载超时的 `exec` 命令。
- 不要为同一个Space同时运行多个下载进程。
- 除非用户明确要求，否则不要手动终止下载进程。

在录制过程中，音频文件会暂存于 `/tmp/spaces-listener-staging/` 目录中，完成后会自动复制到最终的Dropbox输出目录。这样可以避免长时间下载时导致Dropbox文件锁定问题。

## Whisper模型性能对比

| 模型 | 下载速度 | 准确率 |
|-------|-------|----------|
| tiny | ⚡⚡⚡⚡ | ⭐ |
| base | ⚡⚡⚡ | ⭐⭐ |
| small | ⚡⚡ | ⭐⭐⭐ |
| medium | ⚡ | ⭐⭐⭐⭐ |
| large | 🐢 | ⭐⭐⭐⭐⭐ |