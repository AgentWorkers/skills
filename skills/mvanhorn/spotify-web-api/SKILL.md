---
name: spotify-web-api
description: 通过 Web API 控制 Spotify：支持播放、查看播放历史记录、查看热门歌曲以及进行搜索。支持跨平台使用（无需 Mac 设备）。
homepage: https://spotify.com
metadata: {"clawdbot":{"emoji":"🎵","requires":{"env":["SPOTIFY_CLIENT_ID","SPOTIFY_CLIENT_SECRET"]}}}
---

# Spotify Web API（跨平台）

通过 Web API 控制 Spotify，支持在任何平台上使用——无需 Mac 设备。

## 设置

### 1. 创建 Spotify 应用程序：

1. 访问 https://developer.spotify.com/dashboard
2. 创建一个新的应用程序
3. 设置回调 URI：`http://localhost:8888/callback`
4. 复制 **客户端 ID** 和 **客户端密钥**

### 2. 设置环境变量：

```bash
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"
```

### 3. 验证身份：

```bash
python3 {baseDir}/scripts/spotify.py auth
```

系统会打开浏览器进行 OAuth 验证。生成的令牌会保存在 `~/.spotify_cache.json` 文件中。

## 命令

```bash
# Currently playing
python3 {baseDir}/scripts/spotify.py now

# Recently played
python3 {baseDir}/scripts/spotify.py recent

# Top tracks/artists
python3 {baseDir}/scripts/spotify.py top tracks --period month
python3 {baseDir}/scripts/spotify.py top artists --period year

# Playback control
python3 {baseDir}/scripts/spotify.py play
python3 {baseDir}/scripts/spotify.py play "bohemian rhapsody"
python3 {baseDir}/scripts/spotify.py pause
python3 {baseDir}/scripts/spotify.py next
python3 {baseDir}/scripts/spotify.py prev

# Search
python3 {baseDir}/scripts/spotify.py search "daft punk"

# List devices
python3 {baseDir}/scripts/spotify.py devices
```

## 聊天示例：

- “我正在听什么音乐？”
- “我最近听了哪些歌？”
- “我这个月的热门歌曲有哪些？”
- “播放《波西米亚狂想曲》”
- “跳过这首歌”
- “暂停音乐”

## 使用要求：

- 需要订阅 Spotify Premium 订阅服务才能控制音乐播放功能
- 免费账户仍可以查看播放历史和热门歌曲列表

## API 参考文档：

更多关于 Spotify Web API 的信息，请参考：
https://developer.spotify.com/documentation/web-api