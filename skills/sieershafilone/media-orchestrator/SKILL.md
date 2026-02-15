---
name: media-orchestrator
description: 一种用于在聊天平台上解析、下载和传输媒体内容（音频/视频）的统一工具。该工具集成了 yt-dlp 来处理视频分辨率转换，并支持与 Spotify 的元数据同步功能。
---

# 媒体编排器（Media Orchestrator）

该技能负责处理来自 WhatsApp 和 Telegram 等聊天平台的所有媒体请求（音频、视频、Spotify 曲目）。它利用 `yt-dlp` 来从 YouTube 进行高效的搜索和下载，并处理 Spotify 的元数据以支持 WebUI 的集成。

## ⚙️ 工作原理

1. **搜索与下载**：收到媒体请求后，媒体编排器会使用 `yt-dlp` 的 `ytsearch1:` 功能从 YouTube 中查找质量最高的媒体资源。
2. **下载**：选定的媒体文件（音频或视频）会被直接下载到 OpenClaw 的工作区中。
3. **传输**：下载完成后，文件会通过 `message` 工具的 `filePath` 参数被发送到请求的聊天平台（WhatsApp/Telegram），确保传输过程符合相关协议要求（静默传输）。
4. **Spotify 数据同步**：对于特定于 Spotify 的请求，媒体编排器会通过 Zero-Auth 技术获取曲目元数据，并将这些数据以 JSON 格式保存在工作区中，从而实现 OpenClaw WebUI 的同步播放功能。

## 📂 工作区路径

- **主工作区**：`/home/ky11rie/.openclaw/workspace/`
  - 这里临时存放下载的原始媒体文件（如 `.mp4`、`.mp3` 等）。
- **Spotify 元数据**：`/home/ky11rie/.openclaw/workspace/media/spotify/`
  - 存储由 `spotify-surface` 组件生成的 Spotify 曲目元数据文件（例如 `track_id.json`）。
- **技能脚本**：`/home/ky11rie/.openclaw/workspace/skills/spotify-surface/scripts/`
  - 包含用于 Spotify 集成的专用逻辑代码。

## 🛠️ 命令

该技能作为底层编排器，负责处理各种自然语言请求。它支持的命令示例包括：
- `send audio file song: [歌曲名称]`：发送指定歌曲的音频文件。
- `send video file mp4 480p: [视频名称]`：发送指定分辨率（480p）的视频文件。
- `play [spotify track or url]`：通过 `spotify-surface` 播放指定的 Spotify 曲目或 URL。