---
name: spotify
description: 在 macOS 上控制 Spotify 的播放功能：可以播放/暂停音乐、跳过曲目、调节音量，以及播放特定的艺术家、专辑或播放列表。适用于用户需要播放音乐、控制 Spotify 播放内容或调整音量的场景。
metadata: {"clawdbot":{"emoji":"🎵","requires":{"bins":["spotify"],"os":"darwin"},"install":[{"id":"brew","kind":"brew","packages":["shpotify"],"bins":["spotify"],"label":"Install spotify CLI (brew)"}]}}
---

# Spotify CLI

用于在 macOS 上控制 Spotify，无需使用 API 密钥。

## 命令

```bash
spotify play                     # Resume
spotify pause                    # Pause/toggle
spotify next                     # Next track
spotify prev                     # Previous track
spotify stop                     # Stop

spotify vol up                   # +10%
spotify vol down                 # -10%
spotify vol 50                   # Set to 50%

spotify status                   # Current track info
```

## 按名称播放音乐

1. 在网页上搜索 Spotify 的 URL：例如：“Daft Punk”的网址为 `open.spotify.com`
2. 从 URL 中获取艺术家 ID：`open.spotify.com/artist/4tZwfgrHOc3mvqYlEYSvVi` → 这里的艺术家 ID 是 `4tZwfgrHOc3mvqYlEYSvVi`
3. 使用 AppleScript 播放音乐：

```bash
# Artist
osascript -e 'tell application "Spotify" to play track "spotify:artist:4tZwfgrHOc3mvqYlEYSvVi"'

# Album
osascript -e 'tell application "Spotify" to play track "spotify:album:4m2880jivSbbyEGAKfITCa"'

# Track
osascript -e 'tell application "Spotify" to play track "spotify:track:2KHRENHQzTIQ001nlP9Gdc"'
```

## 注意事项

- **仅适用于 macOS** – 需要使用 AppleScript
- 必须运行 Spotify 的桌面应用程序
- 可通过 Spotify Connect 与 Sonos 集成使用