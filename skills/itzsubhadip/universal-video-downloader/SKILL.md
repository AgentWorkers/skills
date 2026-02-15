---
name: universal-video-downloader
description: 使用 yt-dlp 从 YouTube、Instagram、TikTok、Twitter/X 以及 1000 多个其他网站下载视频。支持选择视频质量并自动处理下载后的文件（如去除广告等）。当用户提供来自任意平台的视频链接并希望下载该视频时，可以使用此工具。
metadata: {"openclaw":{"emoji":"🎥","requires":{"bins":["yt-dlp","ffmpeg"]}}}
---

# 通用视频下载器

使用强大的 `yt-dlp` 工具，可以从几乎所有平台下载视频。

## 主要功能
- **平台支持：** YouTube、Instagram、TikTok、Twitter/X、Facebook 等众多平台。
- **画质选择：** 可选择从 144p 到 4K/8K 不同的分辨率。
- **自动清理：** 视频成功上传到聊天区后，会立即从服务器上删除。
- **智能合并：** 自动将高质量的视频和音频流合并成一个 MP4 文件。

## 工作流程
1. **触发：** 用户提供视频链接（例如来自 YouTube 或 Instagram）。
2. **信息收集：** 代理使用 `scripts/download.py info` 获取可用的视频画质和标题。
3. **用户选择：** 代理向用户展示可用的画质选项，并询问用户偏好哪种。
4. **下载：** 选择好画质后，代理会使用 `scripts/download.py download` 命令进行下载。
5. **文件传输：** 代理通过 `message` 工具将下载完成的文件发送给用户。
6. **文件清理：** 代理必须在文件成功发送给用户后，立即使用 `rm` 命令删除服务器上的文件，以释放磁盘空间。

## 代理使用说明

### 1. 获取视频信息
```bash
python3 scripts/download.py info "URL"
```

### 2. 下载特定格式的视频
```bash
python3 scripts/download.py download "URL" "FORMAT_ID"
```

## 安全性与存储
- 本功能仅用于临时处理。
- **重要提示：** 为确保磁盘空间不被占用，用户收到文件后必须立即删除下载的文件。