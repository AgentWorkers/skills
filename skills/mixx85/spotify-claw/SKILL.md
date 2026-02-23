---
name: spotify-claw
description: "**完整版 Spotify Premium 功能：**  
- 全面控制 Spotify Premium 的各项功能：播放/暂停/下一首/上一首/调节音量/随机播放/添加到播放列表。  
- 音乐分析功能：查看热门歌曲、顶级艺术家、用户喜爱的歌曲、音乐类型概览以及个人音乐偏好分析。  
- 发现新音乐：无需依赖推荐 API 即可找到相似的艺术家和音乐。  
- 播放列表管理：创建自定义播放列表、查看艺术家推荐的歌曲、探索新音乐。  
- 自动启动功能：若应用程序关闭，会自动重新打开 Spotify。  
- 认证方式：通过 macOS 的 Keychain 系统进行身份验证。  
**常用指令：**  
- 开启/关闭功能：**включи**  
- 设置播放内容：**поставь**  
- 暂停播放：**пауза**  
- 下一首歌曲：**следующий**  
- 当前播放的歌曲：**что играет**  
- 热门歌曲列表：**топ треки**  
- 音乐类型：**жанры**  
- 查找相似音乐：**похожая музыка**  
- 自动打开 Spotify：**открой спотифай**"
homepage: https://github.com/mixx85/spotify-claw
metadata:
  {
    "openclaw":
      {
        "emoji": "🎵",
        "requires": { "bins": [] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "spotipy",
              "label": "Install spotipy (pip)",
            },
          ],
      },
  }
---
# spotify-claw

这是一个用于完全控制 Spotify Premium 功能的工具，支持音乐分析和智能推荐功能。

> **务必运行 `python3 ~/.openclaw/scripts/spotify.py [cmd]`** —— 切勿仅输出文本响应。

---

## 设置（首次使用）

1. 在 [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) 上创建应用程序。
   —— 添加回调 URI：`http://127.0.0.1:8888/callback`

2. 将该应用程序添加到 macOS 的 Keychain 中：
```bash
security add-generic-password -a openclaw -s openclaw.spotify.client_id -w "CLIENT_ID"
security add-generic-password -a openclaw -s openclaw.spotify.client_secret -w "CLIENT_SECRET"
```

3. 首次登录：运行 `now`，浏览器会自动打开 Spotify 并完成登录：
```bash
python3 ~/.openclaw/scripts/spotify.py now
```

---

## 播放命令

```bash
python3 ~/.openclaw/scripts/spotify.py play                          # resume
python3 ~/.openclaw/scripts/spotify.py play "track name"             # search & play
python3 ~/.openclaw/scripts/spotify.py play spotify:track:URI        # by URI
python3 ~/.openclaw/scripts/spotify.py play spotify:playlist:ID      # playlist
python3 ~/.openclaw/scripts/spotify.py pause
python3 ~/.openclaw/scripts/spotify.py next
python3 ~/.openclaw/scripts/spotify.py prev
python3 ~/.openclaw/scripts/spotify.py volume 70
python3 ~/.openclaw/scripts/spotify.py volume up
python3 ~/.openclaw/scripts/spotify.py volume down
python3 ~/.openclaw/scripts/spotify.py shuffle on
python3 ~/.openclaw/scripts/spotify.py shuffle off
python3 ~/.openclaw/scripts/spotify.py queue "track name"
python3 ~/.openclaw/scripts/spotify.py now
python3 ~/.openclaw/scripts/spotify.py devices
```

**自动启动**：如果 Spotify 已关闭，`play` 命令会自动打开应用程序，等待初始化完成后开始播放。

---

## 分析命令

```bash
python3 ~/.openclaw/scripts/spotify.py top-tracks [short|medium|long] [limit]
python3 ~/.openclaw/scripts/spotify.py top-artists [short|medium|long] [limit]
python3 ~/.openclaw/scripts/spotify.py recent [limit]
python3 ~/.openclaw/scripts/spotify.py liked [limit]
python3 ~/.openclaw/scripts/spotify.py liked-all
python3 ~/.openclaw/scripts/spotify.py liked-by-artist "Artist Name"
python3 ~/.openclaw/scripts/spotify.py genres [short|medium|long]
python3 ~/.openclaw/scripts/spotify.py playlists
python3 ~/.openclaw/scripts/spotify.py search "query" [track|artist|album] [limit]
python3 ~/.openclaw/scripts/spotify.py track-info URI
```

时间范围：
- `short`：4 周
- `medium`：6 个月
- `long`：所有时间

---

## 音乐发现与播放列表构建

```bash
# Find new music by genre profile
python3 ~/.openclaw/scripts/spotify.py discover

# Expand from specific artist (depth=hops, n=tracks per artist)
python3 ~/.openclaw/scripts/spotify.py discover "Portishead" 3 3

# Related artists
python3 ~/.openclaw/scripts/spotify.py related-artists "The Cure" 10

# Top tracks of any artist
python3 ~/.openclaw/scripts/spotify.py artist-top-tracks "Massive Attack" 5

# Create playlist from top tracks (one command: creates + fills)
python3 ~/.openclaw/scripts/spotify.py make-playlist "Top March 2026" short 20

# Manage playlists
python3 ~/.openclaw/scripts/spotify.py create-playlist "My Playlist" "Description"
python3 ~/.openclaw/scripts/spotify.py add-to-playlist PLAYLIST_ID URI1 URI2
```

> **注意**：对于新的开发者应用程序，Spotify 的 `recommendations` 和 `audio_features` API 是被禁止使用的（会返回 403/404 错误）。因此，本工具使用 `related_artists` 和 `artist_top_tracks` 来进行音乐推荐。

---

## 使用技巧

- 使用 `playlists` 命令查看用户现有的播放列表及其 ID，然后再进行播放。
- 使用 `now` 命令在播放歌曲后确认当前正在播放的内容。
- 使用 `liked-by-artist` 命令查找特定艺术家的热门歌曲，以创建主题播放列表。
- 通过以下命令链实现智能播放列表构建：`related-artists` → `artist-top-tracks` → `add-to-playlist`。
- 设置 `genres long` 可以获得最准确的音乐品味分析结果。