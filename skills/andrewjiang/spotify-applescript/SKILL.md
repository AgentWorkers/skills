---
name: spotify-applescript
description: 通过 AppleScript 控制 Spotify 桌面应用程序：可以播放播放列表、单曲、专辑以及剧集，并管理播放功能。该方法在无需 API 密钥或 OAuth 认证的情况下，能够稳定地与 macOS 上的 Spotify 应用程序配合使用。
homepage: https://github.com/andrewjiang/HoloClawd-Open-Firmware
metadata: {"clawdbot":{"emoji":"🎵","os":["darwin"]}}
triggers:
  - spotify
  - play music
  - play playlist
  - play episode
  - pause music
  - next track
  - previous track
---

# 使用 AppleScript 控制 Spotify

通过 AppleScript 来控制 Spotify 桌面应用程序。该脚本在 macOS 上的 Spotify 应用中稳定运行，无需担心 API 使用频率限制或 OAuth 认证的问题。

## 使用要求

- 确保已安装并运行 macOS 版本的 Spotify 桌面应用程序。
- 无需额外设置，即可直接使用。

## 快速入门

```bash
# Play a playlist
spotify play "spotify:playlist:665eC1myDA8iSepZ0HOZdG"
spotify play "https://open.spotify.com/playlist/665eC1myDA8iSepZ0HOZdG"

# Play an episode
spotify play "spotify:episode:5yJKH11UlF3sS3gcKKaUYx"
spotify play "https://open.spotify.com/episode/5yJKH11UlF3sS3gcKKaUYx"

# Play a track
spotify play "spotify:track:7hQJA50XrCWABAu5v6QZ4i"

# Playback control
spotify pause          # Toggle play/pause
spotify next           # Next track
spotify prev           # Previous track
spotify status         # Current track info

# Volume control
spotify volume 50      # Set volume (0-100)
spotify mute           # Mute
spotify unmute         # Unmute
```

## Spotify 命令行接口（CLI）封装

`spotify` 命令是一个封装脚本，位于 `{baseDir}/spotify.sh` 文件中。

### 常用命令

| 命令            | 功能                | 示例                |
|------------------|------------------|-------------------|
| `play <uri>`       | 播放指定的曲目/专辑/播放列表/剧集 | `spotify play spotify:track:xxx` |
| `pause`         | 暂停播放              | `spotify pause`           |
| `next`          | 播放下一首曲目           | `spotify next`          |
| `prev`          | 播放上一首曲目           | `spotify prev`          |
| `status`         | 显示当前曲目信息           | `spotify status`         |
| `volume <0-100>`     | 设置音量（0-100 之间）       | `spotify volume 75`         |
| `mute`          | 静音                | `spotify mute`           |
| `unmute`         | 取消静音              | `spotify unmute`           |

### URI 格式

支持两种格式的 URI：
- Spotify 自定义 URI（例如：`spotify:track:7hQJA50XrCWABAu5v6QZ4i`
- open.spotify.com 格式的 URL（例如：`https://open.spotify.com/track/7hQJA50XrCWABAu5v6QZ4i`

脚本会自动将输入的 URL 转换为正确的 Spotify URI 格式。

## 直接使用 AppleScript

如需更精细的控制，可以直接使用 AppleScript 发送相应命令：

```bash
# Play
osascript -e 'tell application "Spotify" to play track "spotify:playlist:xxx"'

# Pause/Play toggle
osascript -e 'tell application "Spotify" to playpause'

# Next/Previous
osascript -e 'tell application "Spotify" to next track'
osascript -e 'tell application "Spotify" to previous track'

# Get current track
osascript -e 'tell application "Spotify"
  set trackName to name of current track
  set artistName to artist of current track
  return trackName & " by " & artistName
end tell'

# Get player state
osascript -e 'tell application "Spotify" to player state'

# Set volume (0-100)
osascript -e 'tell application "Spotify" to set sound volume to 75'

# Get current position (in seconds)
osascript -e 'tell application "Spotify" to player position'

# Set position (in seconds)
osascript -e 'tell application "Spotify" to set player position to 30'
```

## 可用的属性

```applescript
tell application "Spotify"
  name of current track          -- Track name
  artist of current track        -- Artist name
  album of current track         -- Album name
  duration of current track      -- Duration in ms
  player position                -- Position in seconds
  player state                   -- playing/paused/stopped
  sound volume                   -- 0-100
  repeating                      -- true/false
  repeating enabled              -- true/false
  shuffling                      -- true/false
  shuffling enabled              -- true/false
end tell
```

## 使用示例

### 通过语音命令控制

- 用户说：“播放我的‘Power Hour’播放列表” → 脚本会提取播放列表的 URI 并执行 `spotify play <uri>` 命令。
- 用户说：“暂停音乐” → 脚本会执行 `spotify pause` 命令。
- 用户说：“下一首曲目” → 脚本会执行 `spotify next` 命令。
- 用户问：“正在播放什么？” → 脚本会显示当前曲目的信息。

### 播放特定剧集

```bash
spotify play https://open.spotify.com/episode/5yJKH11UlF3sS3gcKKaUYx
```

### 获取曲目的详细信息

```bash
osascript -e 'tell application "Spotify"
  return "Track: " & (name of current track) & "\nArtist: " & (artist of current track) & "\nAlbum: " & (album of current track) & "\nState: " & (player state as string)
end tell'
```

## 安装方法

该脚本是独立可执行的。若想让 `spotify` 命令在整个系统中可用，可以：

1. 将 `spotify.sh` 文件复制到系统的 `PATH` 环境变量指定的目录中。
2. 或者将整个脚本目录添加到 `PATH` 中。

## 常见问题及解决方法

- **“Spotify 出现错误”**：请确认 Spotify 桌面应用程序正在运行，并且至少启动过一次才能接收 AppleScript 命令。
- **播放命令无效**：检查 URI 格式是否正确；也可以先尝试通过 Spotify 应用本身播放该内容。
- **没有音频输出**：检查系统音量和 Spotify 应用的音量设置；确保在 Spotify 首选项中选择了正确的输出设备。
- **其他问题**：根据具体情况排查原因。

## 限制事项

- 必须运行 Spotify 桌面应用程序。
- 仅支持 macOS 系统（因依赖 AppleScript）。
- 无法通过脚本搜索或浏览音乐库（请使用 Spotify 的网页界面或应用程序进行操作）。
- 无法直接管理播放列表（添加/删除曲目）。

如需管理播放列表或进行搜索，请使用 Spotify 的网页界面，或考虑使用 `spotify-player` 这个技能（该技能需要先完成 OAuth 设置）。