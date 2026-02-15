---
name: spotify-player
description: 通过 spogo 或 spotify_player 在终端中播放/搜索 Spotify 内容（推荐使用 spogo）。
homepage: https://www.spotify.com
metadata: {"clawdbot":{"emoji":"🎵","requires":{"anyBins":["spogo","spotify_player"]},"install":[{"id":"brew","kind":"brew","formula":"spogo","tap":"steipete/tap","bins":["spogo"],"label":"Install spogo (brew)"},{"id":"brew","kind":"brew","formula":"spotify_player","bins":["spotify_player"],"label":"Install spotify_player (brew)"}]}}
---

# spogo / spotify_player

推荐使用 `spogo` 来播放或搜索 Spotify 内容；如有需要，可退而使用 `spotify_player`。

**使用要求：**
- 拥有 Spotify Premium 账户。
- 已安装 `spogo` 或 `spotify_player`。

**spogo 的设置步骤：**
- 导入浏览器 cookies：`spogo auth import --browser chrome`

**常见的 CLI 命令：**
- 搜索歌曲：`spogo search track "查询内容"`
- 播放/暂停/下一首/上一首：`spogo play|pause|next|prev`
- 查看设备列表：`spogo device list`
- 设置设备：`spogo device set "<设备名称|设备ID>"
- 查看设备状态：`spogo status`

**spotify_player 的命令（备用方案）：**
- 搜索歌曲：`spotify_player search "查询内容"`
- 播放/暂停/下一首/上一首：`spotify_player playback play|pause|next|previous`
- 连接设备：`spotify_player connect`
- 给歌曲添加“喜欢”标记：`spotify_player like`

**注意事项：**
- 配置文件路径：`~/.config/spotify-player`（例如：`app.toml`）。
- 如需集成 Spotify Connect，需在配置文件中设置 `client_id`。
- 应用程序内可通过 `?` 符号访问 TUI（图形用户界面）的快捷功能。