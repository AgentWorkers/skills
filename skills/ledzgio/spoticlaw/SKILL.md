---
name: spoticlaw
description: Spotify Web API client for Nyx agents. Use when interacting with Spotify: search, playback, playlists, library, tracks, artists, albums, shows, podcasts.
metadata: {"openclaw":{"homepage":"https://github.com/ledzgio/spoticlaw"},"requirements":{"env":["SPOTIFY_CLIENT_ID","SPOTIFY_CLIENT_SECRET","SPOTIFY_REDIRECT_URI"],"files":[".spotify_cache"]},"security":{"notes":"Providing .env and .spotify_cache grants Spotify account access to the agent; use isolated environments and least-privilege app scopes."}}
---

# Spoticlaw - Spotify Web API 客户端

这是一个轻量级的 Spotify Web API 客户端，它直接使用 HTTP 请求进行数据交互，无需依赖 Spotipy。

## 快速入门

```bash
# Install dependencies
pip install requests python-dotenv

# Add to path
import sys
sys.path.insert(0, "skills/spoticlaw/scripts")

from spoticlaw import player, search, playlists, library

# Search for music
results = search().query("coldplay", types=["track"], limit=10)

# Play a track
player().play(uris=["spotify:track:..."])

# Manage playlists
playlists().create("My Playlist")
playlists().add_items("playlist_id", ["spotify:track:..."])

# Save to library
library().save(["spotify:track:..."])
```

或者从脚本目录中运行：
```bash
cd skills/spoticlaw/scripts
python -c "from spoticlaw import player; player().play(...)"
```

## 所需配置

在代理程序运行时需要设置以下环境变量：
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIFY_REDIRECT_URI`（推荐值：`http://127.0.0.1:8888/callback`

所需文件：
- `.spotify_cache`（用于存储 OAuth 令牌）

## 认证

**安全提示：** 令牌不会被传递给 AI 模型。认证过程在本地完成，令牌文件会手动复制到代理程序中。

### 设置流程

1. 在 [https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) 上创建一个 Spotify 应用。
2. 获取 `CLIENT_ID` 和 `CLIENT_SECRET`。
3. 将 `http://127.0.0.1:8888/callback` 设置为回调 URI。
4. 在本地机器上创建一个 `.env` 文件：

```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

5. 在本地机器上执行认证流程：

```bash
cd skills/spoticlaw/scripts
pip install -r requirements.txt
python auth.py
```

6. 在浏览器中打开显示的 URL，完成授权。
7. **将生成的令牌文件复制到代理程序中：**

```bash
# Linux/Mac - copy to agent's skill folder
cp .spotify_cache /path/to/agent/skills/spoticlaw/.spotify_cache

# Or if agent is remote, copy via scp, USB, etc.
scp .spotify_cache user@agent:/path/to/skills/spoticlaw/.spotify_cache
```

**就这样！** 令牌永远不会被传递给 AI 模型，代理程序仅读取该文件中的令牌信息。

### 令牌自动刷新

只有当代理程序的 `.env` 文件中包含正确的应用凭证时，该库才会自动刷新令牌：
- 访问令牌的有效期为约 1 小时。
- 令牌过期后，系统会使用 `refresh_token` 和客户端凭证来请求新的访问令牌。
- 代理程序的环境中必须设置 `SPOTIFY_CLIENT_ID` 和 `SPOTIFY_CLIENT_SECRET`。
- 如果 `.spotify_cache` 文件存在但 `.env` 文件缺失或内容不匹配，刷新令牌会失败（提示错误 `invalid_client`）。
- 如果出现错误，请在本地重新运行 `auth.py` 并复制更新后的 `.spotify_cache` 文件。

有关 Spotify 的 OAuth 流程的更多信息，请参阅：[https://developer.spotify.com/documentation/web-api/tutorials/code-flow](https://developer.spotify.com/documentation/web-api/tutorials/code-flow)

### 所需的权限范围

`auth.py` 脚本会请求以下权限范围：
- `user-read-playback-state`：读取播放状态
- `user-modify-playback-state`：控制播放
- `playlist-read-private`：读取私有播放列表
- `playlist-modify-public`：修改公共播放列表
- `playlist-modify-private`：修改私有播放列表
- `user-library-read`：读取用户音乐库
- `user-library-modify`：修改用户音乐库
- `user-read-recently-played`：查看最近播放的歌曲
- `user-top-read`：查看热门歌曲/艺术家
- `user-follow-read`：查看用户关注的艺术家

---

## 基本功能

**重要提示：** 首先需要添加模块路径并安装依赖项：
```bash
pip install requests python-dotenv  # Install dependencies

# For agent execution, add to path:
import sys
sys.path.insert(0, "skills/spoticlaw/scripts")
```

### User（用户信息）

```python
from spoticlaw import user

user().me()  # Get current user profile
```

返回的数据结构：`{id, display_name, email, country, ...}`

---

### Search（搜索）

```python
from spoticlaw import search

# Search for tracks
search().query("song name", types=["track"], limit=10)

# Search for artists
search().query("artist name", types=["artist"], limit=10)

# Search multiple types
search().query("coldplay", types=["track", "artist", "album"], limit=10)
```

**参数：**
- `q`：搜索查询字符串
- `types`：搜索类型（`track`、`artist`、`album`、`playlist`、`show`、`episode`、`audiobook`）
- `limit`：最多返回 10 个结果（Spotify 的默认限制）
- `offset`：分页偏移量

---

### Tracks（歌曲）

```python
from spoticlaw import tracks

tracks().get("track_id")  # Get single track
tracks().get_multiple(["id1", "id2"])  # Get multiple tracks
```

返回歌曲元数据：`{name, artists, album, duration_ms, uri, ...}`

---

### Artists（艺术家）

```python
from spoticlaw import artists

artists().get("artist_id")  # Get artist details
artists().get_albums("artist_id", limit=10)  # Get artist albums
```

**专辑筛选条件（包含分组）：**
- `album`、`single`、`compilation`、`appears_on`

---

### Albums（专辑）

```python
from spoticlaw import albums

albums().get("album_id")  # Get album details
albums().get_tracks("album_id")  # Get album tracks
```

---

### Shows（播客）

```python
from spoticlaw import shows

shows().get("show_id")  # Get show details
shows().get_episodes("show_id", limit=10)  # Get show episodes
```

---

### Episodes（剧集）

```python
from spoticlaw import episodes

episodes().get("episode_id")  # Get episode details
```

---

### Playlists（播放列表）

```python
from spoticlaw import playlists, user_playlists

# Get user's playlists
user_playlists().get(limit=50)

# Get playlist details
playlists().get("playlist_id")

# Get playlist tracks
# Note: Each item has 'item' key (not 'track'), e.g. item['item']['name']
# Also can contain episodes (podcasts), not just tracks
playlists().get_items("playlist_id", limit=50)

# Create playlist
playlists().create(name="My Playlist", description="...", public=False)

# Update playlist
playlists().update("playlist_id", name="New Name")

# Add tracks
playlists().add_items("playlist_id", ["spotify:track:...", "spotify:track:..."])

# Remove tracks
playlists().remove_items("playlist_id", ["spotify:track:..."])

# Delete playlist (unfollow)
playlists().delete("playlist_id")
```

---

### Library（音乐库）

```python
from spoticlaw import library

library().save(["spotify:track:..."])  # Save to library
library().remove(["spotify:track:..."])  # Remove from library
library().check(["spotify:track:..."])  # Check if saved, returns [True, False]
```

---

### Player（播放器）

```python
from spoticlaw import player

# Get playback state
player().get_playback_state()  # Returns {} if nothing playing
player().get_currently_playing()

# Get devices
player().get_devices()  # Returns list of devices with IDs

# Transfer playback to device
player().transfer("device_id", play=True)

# Playback control
player().play(uris=["spotify:track:..."])  # Start playing
player().play(context_uri="spotify:album:...")  # Play album/playlist
player().pause()
player().next()
player().previous()
player().seek(60000)  # Seek to 1:00 (milliseconds)
player().set_volume(80)  # Set volume 0-100

# Queue
player().add_to_queue("spotify:track:...")
player().get_queue()

# Modes
player().set_shuffle(True)
player().set_repeat("off")  # off, track, context

# Recently played
player().get_recently_played(limit=50)
```

---

### Personalisation（个性化设置）

```python
from spoticlaw import personalisation

personalisation().get_top("tracks", time_range="medium_term", limit=20)
personalisation().get_top("artists", time_range="long_term", limit=20)

# time_range: short_term (4 weeks), medium_term (6 months), long_term (years)
```

---

### Follow（关注）

```python
from spoticlaw import follow

follow().get_followed(limit=50)  # Get followed artists
```

---

## 组合工作流程

可以通过组合这些基本功能来创建强大的自动化脚本。以下是一些实际示例：

### 工作流程 1：播放特定歌曲

```python
from spoticlaw import search, player

# 1. Search for the song
results = search().query("stairway to heaven", types=["track"], limit=5)
song = results["tracks"]["items"][0]
song_uri = song["uri"]
print(f"Playing: {song['name']} by {song['artists'][0]['name']}")

# 2. Play it
player().play(uris=[song_uri])
```

### 工作流程 2：根据搜索结果创建播放列表

```python
from spoticlaw import search, playlists

# 1. Search for songs
results = search().query("led zeppelin", types=["track"], limit=10)
track_uris = [t["uri"] for t in results["tracks"]["items"][:5]]

# 2. Create playlist
pl = playlists().create("Led Zeppelin Mix", public=False)
playlist_id = pl["id"]

# 3. Add tracks
playlists().add_items(playlist_id, track_uris)
print(f"Created playlist: {pl['name']}")
```

### 工作流程 3：将专辑添加到音乐库

```python
from spoticlaw import artists, albums, library

# 1. Find artist
artist = search().query("the weeknd", types=["artist"], limit=1)["artists"]["items"][0]

# 2. Get albums
albums_list = artists().get_albums(artist["id"], include_groups="album", limit=5)

# 3. Save first album
album = albums_list["items"][0]
library().save([album["uri"]])
print(f"Saved album: {album['name']}")
```

### 工作流程 4：播放播客剧集

```python
from spoticlaw import search, shows, player

# 1. Find podcast
podcast = search().query("joe rogan", types=["show"], limit=1)["shows"]["items"][0]
show_id = podcast["id"]

# 2. Get latest episode
episodes = shows().get_episodes(show_id, limit=1)
episode = episodes["items"][0]
episode_uri = episode["uri"]

# 3. Get device and play
devices = player().get_devices()
if devices.get("devices"):
    device_id = devices["devices"][0]["id"]
    player().transfer(device_id, play=True)
    player().play(uris=[episode_uri])
    print(f"Playing: {episode['name']}")
```

### 工作流程 5：转移播放状态并开始播放

```python
from spoticlaw import player, search

# 1. Get available devices
devices = player().get_devices()
print("Available devices:", [d["name"] for d in devices.get("devices", [])])

# 2. Transfer to phone
if devices.get("devices"):
    device_id = devices["devices"][0]["id"]
    player().transfer(device_id, play=True)
    
    # 3. Search and play
    results = search().query("dream on", types=["track"], limit=1)
    track_uri = results["tracks"]["items"][0]["uri"]
    player().play(uris=[track_uri])
```

### 工作流程 6：获取用户的热门艺术家并关注他们

```python
from spoticlaw import personalisation, search, library

# 1. Get top artists
top = personalisation().get_top("artists", limit=10)
print("Your top artists:")
for i, a in enumerate(top["items"], 1):
    print(f"  {i}. {a['name']}")

# 2. Search for a new artist
new_artist = search().query("tame impala", types=["artist"], limit=1)["artists"]["items"][0]
print(f"\nFound: {new_artist['name']}")

# Note: Follow functionality requires additional scope (not in current scope list)
# Use Spotify app to follow manually
```

### 工作流程 7：根据专辑创建播放列表

```python
from spoticlaw import albums, player

# 1. Get album tracks
album_id = "4aawyAB9vmqN3uQ7FjRGTy"  # Example album
tracks = albums().get_tracks(album_id)

# 2. Add all tracks to queue
for track in tracks["items"][:5]:  # First 5 tracks
    player().add_to_queue(track["uri"])

print("Added 5 tracks to queue")
```

### 工作流程 8：检查音乐库中的多首歌曲

```python
from spoticlaw import library, search

# 1. Search for tracks
results = search().query("classic rock", types=["track"], limit=20)
track_uris = [t["uri"] for t in results["tracks"]["items"]]

# 2. Check which are in library
saved = library().check(track_uris)

# 3. Show results
for i, (track, is_saved) in enumerate(zip(results["tracks"]["items"], saved)):
    status = "✓ saved" if is_saved else "○ not saved"
    print(f"{i+1}. {track['name']} - {status}")
```

### 工作流程 9：获取最近播放的歌曲并保存

```python
from spoticlaw import player, library

# 1. Get recently played
recent = player().get_recently_played(limit=10)

print("Recently played:")
for i, item in enumerate(recent["items"], 1):
    track = item["track"]
    print(f"  {i}. {track['name']} - {track['artists'][0]['name']}")

# 2. Save the first one
if recent["items"]:
    track_uri = recent["items"][0]["track"]["uri"]
    library().save([track_uri])
    print(f"\nSaved: {recent['items'][0]['track']['name']}")
```

### 工作流程 10：从播放列表中播放歌曲

```python
from spoticlaw import playlists, player

# 1. Get user's playlists
my_playlists = user_playlists().get(limit=10)

print("Your playlists:")
for p in my_playlists["items"]:
    print(f"  - {p['name']} ({p['tracks']['total']} tracks)")

# 2. Pick first playlist and play
if my_playlists["items"]:
    playlist_id = my_playlists["items"][0]["id"]
    # Get device first
    devices = player().get_devices()
    if devices.get("devices"):
        player().transfer(devices["devices"][0]["id"], play=True)
        
        # Play playlist
        player().play(context_uri=f"spotify:playlist:{playlist_id}")
        print(f"Playing: {my_playlists['items'][0]['name']}")
```

---

## 错误处理

```python
from spoticlaw import player, SpotifyException

try:
    player().play(uris=["spotify:track:..."])
except SpotifyException as e:
    if "NO_ACTIVE_DEVICE" in str(e):
        print("No device found. Open Spotify and try again.")
    elif "Invalid token" in str(e):
        print("Token expired. Re-authenticate: python auth.py")
    else:
        print(f"Error: {e}")
```

---

## 常见问题

| 错误 | 解决方案 |
|-------|----------|
| 未获取到令牌 | 重新执行认证（运行 `python auth.py`） |
| 访问令牌过期 | 应该自动刷新令牌；如果未自动刷新，请重新运行 `python auth.py` |
| 客户端权限范围不足 | 使用更多权限范围重新认证 |
| 无活跃设备 | 打开 Spotify 应用后再尝试 |
| 无效的 `limit` 值 | 搜索时使用最大值 10，播放列表时使用最大值 50 |
| 资源未找到 | ID 无效或资源不可用 |

---

## API 限制

- **搜索**：最多返回 10 个结果
- **播放列表项**：最多返回 50 个
- **分页**：使用 `offset` 参数
- **播放器**：需要处于活跃的 Spotify 会话状态

---

## 相关文件

- `scripts/spoticlaw.py`：主要的 API 客户端代码
- `scripts/auth.py`：认证辅助函数
- `scripts/requirements.txt`：项目依赖项列表

---

## 更多信息

有关设置、故障排除和贡献信息，请访问：
https://github.com/your-org/spoticlaw