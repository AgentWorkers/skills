---
name: media-player
description: "在主机上本地播放音频/视频"
metadata:
  {
    "openclaw":
      {
        "emoji": "🎵",
        "requires": { "bins": ["mpv"] },
        "install":
          [
            {
              "id": "dnf",
              "kind": "dnf",
              "package": "mpv",
              "bins": ["mpv"],
              "label": "Install via dnf",
            },
          ],
      },
  }
---

# 媒体播放器

使用 `mpv` 在主机上本地播放音频/视频。支持本地文件和远程 URL。

## 命令

```bash
# Play a local file or URL
media-player play "song.mp3"
media-player play "https://example.com/stream.m3u8"

# Pause playback
media-player pause

# Stop playback
media-player stop
```

## 安装

```bash
sudo dnf install mpv
```