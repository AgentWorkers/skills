---
name: yt-video-downloader
description: 下载YouTube视频，支持多种格式和画质。适用于需要将视频保存以供离线观看、提取音频、下载播放列表或获取特定视频格式的情况。
metadata: {"openclaw":{"requires":{"bins":["yt-dlp"]},"install":[{"id":"python","kind":"pip","package":"yt-dlp","bins":["yt-dlp"],"label":"Install yt-dlp (pip)"}]}}
---

# YouTube 视频下载器

## 安装

安装 yt-dlp：
```bash
pip install yt-dlp
```

（可选）：安装 ffmpeg 以进行格式转换：
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
winget install ffmpeg
```

## 下载视频

- 最佳质量（默认）：
```bash
yt-dlp "VIDEO_URL"
```

- 指定质量：
```bash
# Best video + best audio (merged)
yt-dlp -f "bestvideo+bestaudio/best" "VIDEO_URL"

# 1080p max
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" "VIDEO_URL"

# 720p max
yt-dlp -f "bestvideo[height<=720]+bestaudio/best[height<=720]" "VIDEO_URL"

# 480p max
yt-dlp -f "bestvideo[height<=480]+bestaudio/best[height<=480]" "VIDEO_URL"
```

## 仅下载音频

- 最佳质量的 MP3 格式：
```bash
yt-dlp -x --audio-format mp3 "VIDEO_URL"
```

- 最佳质量的 M4A 格式：
```bash
yt-dlp -x --audio-format m4a "VIDEO_URL"
```

- 原始格式的最高质量音频：
```bash
yt-dlp -f "bestaudio" "VIDEO_URL"
```

- 带元数据的音频：
```bash
yt-dlp -x --audio-format mp3 --embed-thumbnail --add-metadata "VIDEO_URL"
```

## 列出可用格式

```bash
yt-dlp -F "VIDEO_URL"
```

- 通过 ID 下载特定格式：
```bash
yt-dlp -f 137+140 "VIDEO_URL"
```

## 自定义输出文件名

```bash
# Custom template
yt-dlp -o "%(title)s.%(ext)s" "VIDEO_URL"

# With channel name
yt-dlp -o "%(channel)s - %(title)s.%(ext)s" "VIDEO_URL"

# With date
yt-dlp -o "%(upload_date)s - %(title)s.%(ext)s" "VIDEO_URL"

# To specific folder
yt-dlp -o "~/Videos/%(title)s.%(ext)s" "VIDEO_URL"
```

## 下载播放列表

- 下载整个播放列表：
```bash
yt-dlp "PLAYLIST_URL"
```

- 带编号下载播放列表：
```bash
yt-dlp -o "%(playlist_index)s - %(title)s.%(ext)s" "PLAYLIST_URL"
```

- 下载播放列表中的特定范围：
```bash
# Videos 1-10
yt-dlp --playlist-start 1 --playlist-end 10 "PLAYLIST_URL"

# Only first 5
yt-dlp -I 1:5 "PLAYLIST_URL"
```

## 下载频道视频

- 下载频道的最新视频：
```bash
yt-dlp -I 1:10 "CHANNEL_URL"
```

- 下载频道的所有视频（注意：文件可能较大！）：
```bash
yt-dlp "CHANNEL_URL/videos"
```

## 带字幕下载

- 嵌入字幕：
```bash
yt-dlp --write-sub --embed-subs "VIDEO_URL"
```

- 自动生成的字幕：
```bash
yt-dlp --write-auto-sub --embed-subs --sub-lang en "VIDEO_URL"
```

## 缩略图与元数据

- 嵌入缩略图：
```bash
yt-dlp --embed-thumbnail "VIDEO_URL"
```

- 完整的元数据：
```bash
yt-dlp --embed-thumbnail --add-metadata --embed-chapters "VIDEO_URL"
```

## 下载速度与下载中断恢复

- 限制下载速度：
```bash
yt-dlp -r 1M "VIDEO_URL"  # 1 MB/s limit
```

- 恢复中断的下载：
```bash
yt-dlp -c "VIDEO_URL"
```

## 归档（跳过已下载的内容）

```bash
yt-dlp --download-archive downloaded.txt "PLAYLIST_URL"
```

## 常见格式代码

| 格式 | 描述 |
|--------|-------------|
| `best` | 最佳质量的单个文件 |
| `bestvideo+bestaudio` | 最佳质量的视频和音频（需要 ffmpeg） |
| `bestvideo[height<=1080]` | 最大分辨率 1080p |
| `bestaudio` | 仅下载音频 |
| `mp4` | 优先选择 MP4 格式 |

## 输出模板变量

| 变量 | 描述 |
|----------|-------------|
| `%(title)s` | 视频标题 |
| `%(id)s` | 视频 ID |
| `%(channel)s` | 频道名称 |
| `%(upload_date)s` | 上传日期（YYYYMMDD） |
| `%(duration)s` | 视频时长（秒） |
| `%(playlist_index)s` | 播放列表中的索引 |
| `%(ext)s` | 文件扩展名 |

## 注意事项

- 请遵守版权和服务条款。
- 有些视频可能受地域限制。
- 需要年龄验证的视频可能需要使用 cookies。
- 对于需要身份验证的内容，请使用 `--cookies-from-browser chrome` 参数。
- 合并视频和音频流需要 ffmpeg。
- 定期更新 yt-dlp：`pip install -U yt-dlp`