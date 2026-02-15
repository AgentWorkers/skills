---
name: youtube-pro
description: 高级YouTube分析功能，包括字幕提取和元数据获取。
metadata: {"clawdbot":{"emoji":"📺"}}
---

# YouTube Pro（Miss Kim 版）

深入分析 YouTube 内容。使用 `summarize` 工具生成字幕，使用 `web_fetch` 获取元数据。

## 工作流程

### 1. 快速总结/字幕生成
使用内置的 `summarize` 工具：
- **总结**：`summarize "URL"`
- **字幕**：`summarize "URL" --youtube auto --extract-only`

### 2. 视频分析（Miss Kim 分析）
当需要分析视频时：
- 通过 `summarize` 获取字幕。
- 使用 `gemini`（MiniPC）分析视频的核心内容、观众情绪（如果评论可用的话）以及实用的建议。

### 3. 音频/帧提取（可选）
如果需要提取音频或视频帧：
- 使用 `yt-dlp`（MiniPC）下载特定片段。
- 使用 `ffmpeg` 提取视频帧以进行视觉分析。

## 协议规则
- **简洁性**：首先将长字幕总结为“5条核心要点”。
- **实用性**：每条总结后面务必添加“Miss Kim 的建议”。
- **链接**：务必附上包含关键时间戳的原始视频链接。