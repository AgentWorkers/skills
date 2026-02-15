---
name: apple-music
version: 0.6.0
description: 通过 AppleScript（macOS）或 MusicKit API 实现与 Apple Music 的集成
---

# Apple Music 集成

本指南介绍了如何将您的应用程序与 Apple Music 集成。涵盖了使用 AppleScript（macOS）、MusicKit API 以及基于库（library-first）的工作流程。

## 适用场景

当用户需要执行以下操作时，请使用本指南：
- 管理播放列表（创建、添加/删除曲目、列出曲目）
- 控制播放（播放、暂停、跳过、调节音量）
- 搜索曲目库或音乐库
- 将歌曲添加到音乐库
- 查看播放历史或推荐曲目

## 关键规则：基于库的工作流程

**严禁直接将曲目从曲目库添加到播放列表中。**  
歌曲必须先存在于用户的音乐库中：
- ❌ 曲目库 ID → 播放列表（会失败）
- ✅ 曲目库 ID → 音乐库 → 播放列表（可以成功）

**原因：** 播放列表使用的是音乐库中的唯一标识符（例如 `i.abc123`），而非曲目库中的 ID（例如 `1234567890`）。  
这一规则同时适用于 AppleScript 和 MusicKit API。

## 平台对比

| 功能 | AppleScript (macOS) | MusicKit API |
|---------|-------------------:|:------------:|
| 是否需要设置 | 无需 | 需要开发者账户和令牌 |
| 播放列表管理 | 全部支持 | 仅通过 API 支持 |
| 播放控制 | 全部支持 | 不支持 |
| 曲目库搜索 | 不支持 | 支持 |
| 音乐库访问 | 即时支持 | 需要令牌 |
| 跨平台支持 | 不支持 | 支持 |

---

# AppleScript (macOS)

无需任何设置，即可直接与 Apple Music 应用程序集成。

**通过 Bash 运行脚本：**
```bash
osascript -e 'tell application "Music" to playpause'
osascript -e 'tell application "Music" to return name of current track'
```

**多行脚本示例：**
```bash
osascript <<'EOF'
tell application "Music"
    set t to current track
    return {name of t, artist of t}
end tell
EOF
```

## 可用的操作

| 功能类别 | 操作内容 |
|----------|------------|
| **播放** | 播放、暂停、停止、继续播放、下一首曲目、上一首曲目、快进、倒带 |
| **播放器状态** | 播放器当前位置、播放器状态、音量、静音、随机播放模式、歌曲重复设置 |
| **当前曲目** | 曲目名称、艺术家名称、专辑名称、时长、播放时间、评分、喜爱程度、类型、发行年份、曲目编号 |
| **音乐库** | 搜索曲目、列出曲目、获取曲目信息、设置评分 |
| **播放列表** | 列出播放列表、创建播放列表、删除播放列表、重命名播放列表、添加/删除曲目 |
| **AirPlay** | 列出可用设备、选择设备、当前连接的设备 |

## 曲目信息（只读）

```applescript
tell application "Music"
    set t to current track
    -- Basic info
    name of t           -- "Hey Jude"
    artist of t         -- "The Beatles"
    album of t          -- "1 (Remastered)"
    album artist of t   -- "The Beatles"
    composer of t       -- "Lennon-McCartney"
    genre of t          -- "Rock"
    year of t           -- 1968

    -- Timing
    duration of t       -- 431.0 (seconds)
    time of t           -- "7:11" (formatted)
    start of t          -- start time in seconds
    finish of t         -- end time in seconds

    -- Track info
    track number of t   -- 21
    track count of t    -- 27
    disc number of t    -- 1
    disc count of t     -- 1

    -- Ratings
    rating of t         -- 0-100 (20 per star)
    loved of t          -- true/false
    disliked of t       -- true/false

    -- Playback
    played count of t   -- 42
    played date of t    -- date last played
    skipped count of t  -- 3
    skipped date of t   -- date last skipped

    -- IDs
    persistent ID of t  -- "ABC123DEF456"
    database ID of t    -- 12345
end tell
```

## 曲目信息（可写）

```applescript
tell application "Music"
    set t to current track
    set rating of t to 80          -- 4 stars
    set loved of t to true
    set disliked of t to false
    set name of t to "New Name"    -- rename track
    set genre of t to "Alternative"
    set year of t to 1995
end tell
```

## 播放器状态信息

```applescript
tell application "Music"
    player state          -- stopped, playing, paused, fast forwarding, rewinding
    player position       -- current position in seconds (read/write)
    sound volume          -- 0-100 (read/write)
    mute                  -- true/false (read/write)
    shuffle enabled       -- true/false (read/write)
    shuffle mode          -- songs, albums, groupings
    song repeat           -- off, one, all (read/write)
    current track         -- track object
    current playlist      -- playlist object
    current stream URL    -- URL if streaming
end tell
```

## 播放控制命令

```applescript
tell application "Music"
    -- Play controls
    play                          -- play current selection
    pause
    stop
    resume
    playpause                     -- toggle play/pause
    next track
    previous track
    fast forward
    rewind

    -- Play specific content
    play (first track of library playlist 1 whose name contains "Hey Jude")
    play user playlist "Road Trip"

    -- Settings
    set player position to 60     -- seek to 1:00
    set sound volume to 50        -- 0-100
    set mute to true
    set shuffle enabled to true
    set song repeat to all        -- off, one, all
end tell
```

## 音乐库查询

```applescript
tell application "Music"
    -- All library tracks
    every track of library playlist 1

    -- Search by name
    tracks of library playlist 1 whose name contains "Beatles"

    -- Search by artist
    tracks of library playlist 1 whose artist contains "Beatles"

    -- Search by album
    tracks of library playlist 1 whose album contains "Abbey Road"

    -- Combined search
    tracks of library playlist 1 whose name contains "Hey" and artist contains "Beatles"

    -- By genre
    tracks of library playlist 1 whose genre is "Rock"

    -- By year
    tracks of library playlist 1 whose year is 1969

    -- By rating
    tracks of library playlist 1 whose rating > 60  -- 3+ stars

    -- Loved tracks
    tracks of library playlist 1 whose loved is true

    -- Recently played (sort by played date)
    tracks of library playlist 1 whose played date > (current date) - 7 * days
end tell
```

## 播放列表操作

```applescript
tell application "Music"
    -- List all playlists
    name of every user playlist

    -- Get playlist
    user playlist "Road Trip"
    first user playlist whose name contains "Road"

    -- Create playlist
    make new user playlist with properties {name:"New Playlist", description:"My playlist"}

    -- Delete playlist
    delete user playlist "Old Playlist"

    -- Rename playlist
    set name of user playlist "Old Name" to "New Name"

    -- Get playlist tracks
    every track of user playlist "Road Trip"
    name of every track of user playlist "Road Trip"

    -- Add track to playlist (must be library track)
    set targetPlaylist to user playlist "Road Trip"
    set targetTrack to first track of library playlist 1 whose name contains "Hey Jude"
    duplicate targetTrack to targetPlaylist

    -- Remove track from playlist
    delete (first track of user playlist "Road Trip" whose name contains "Hey Jude")

    -- Playlist properties
    duration of user playlist "Road Trip"   -- total duration
    time of user playlist "Road Trip"       -- formatted duration
    count of tracks of user playlist "Road Trip"
end tell
```

## AirPlay 设置

```applescript
tell application "Music"
    -- List AirPlay devices
    name of every AirPlay device

    -- Get current device
    current AirPlay devices

    -- Set output device
    set current AirPlay devices to {AirPlay device "Living Room"}

    -- Multiple devices
    set current AirPlay devices to {AirPlay device "Living Room", AirPlay device "Kitchen"}

    -- Device properties
    set d to AirPlay device "Living Room"
    name of d
    kind of d           -- computer, AirPort Express, Apple TV, AirPlay device, Bluetooth device
    active of d         -- true if playing
    available of d      -- true if reachable
    selected of d       -- true if in current devices
    sound volume of d   -- 0-100
end tell
```

## 用户输入的转义

**请始终对用户输入的内容进行转义：**
```python
def escape_applescript(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')

safe_name = escape_applescript(user_input)
script = f'tell application "Music" to play user playlist "{safe_name}"'
```

## 限制

- **无法访问曲目库内容**：只能操作音乐库中的曲目 |
- **仅支持 macOS**：不支持 Windows 和 Linux 平台 |

---

# MusicKit API

支持跨平台集成，但需要注册 Apple 开发者账户（年费 99 美元）并设置 API 令牌。

## 认证要求：

- Apple 开发者账户
- 从 [开发者门户](https://developer.apple.com/account/resources/authkeys/list) 获取 MusicKit 密钥（.p8 文件）
- 开发者令牌（JWT，有效期 180 天）
- 用户音乐令牌（通过浏览器 OAuth 获取）

**生成开发者令牌：**
```python
import jwt, datetime

with open('AuthKey_XXXXXXXXXX.p8') as f:
    private_key = f.read()

token = jwt.encode(
    {
        'iss': 'TEAM_ID',
        'iat': int(datetime.datetime.now().timestamp()),
        'exp': int((datetime.datetime.now() + datetime.timedelta(days=180)).timestamp())
    },
    private_key,
    algorithm='ES256',
    headers={'alg': 'ES256', 'kid': 'KEY_ID'}
)
```

**获取用户令牌：** 通过浏览器 OAuth 访问 `https://authorize.music.apple.com/woa`

**所有请求的请求头：**
```
Authorization: Bearer {developer_token}
Music-User-Token: {user_music_token}
```

**基础 URL：** `https://api.music.apple.com/v1`

## 可用的 API 端点

### 曲目库（仅限开发者使用）

| 端点 | 方法 | 功能描述 |
|----------|--------|-------------|
| `/catalog/{storefront}/search` | GET | 搜索歌曲、专辑、艺术家、播放列表 |
| `/catalog/{storefront}/songs/{id}` | GET | 获取歌曲详情 |
| `/catalog/{storefront}/albums/{id}` | GET | 获取专辑详情 |
| `/catalog/{storefront}/albums/{id}/tracks` | GET | 获取专辑中的曲目 |
| `/catalog/{storefront}/artists/{id}` | GET | 获取艺术家详情 |
| `/catalog/{storefront}/artists/{id}/albums` | GET | 获取艺术家的专辑 |
| `/catalog/{storefront}/artists/{id}/songs` | GET | 获取艺术家的热门歌曲 |
| `/catalog/{storefront}/artists/{id}/related-artists` | GET | 相关艺术家 |
| `/catalog/{storefront}/playlists/{id}` | GET | 获取播放列表详情 |
| `/catalog/{storefront}/charts` | GET | 获取热门排行榜 |
| `/catalog/{storefront}/genres` | GET | 获取所有音乐类型 |
| `/catalog/{storefront}/search/suggestions` | GET | 自动完成搜索 |
| `/catalog/{storefront}/stations/{id}` | GET | 获取广播电台信息 |

### 音乐库（需要用户令牌）

| 端点 | 方法 | 功能描述 |
|----------|--------|-------------|
| `/me/library/songs` | GET | 获取音乐库中的所有曲目 |
| `/me/library/albums` | GET | 获取音乐库中的所有专辑 |
| `/me/library/artists` | GET | 获取音乐库中的所有艺术家 |
| `/me/library/playlists` | GET | 获取音乐库中的所有播放列表 |
| `/me/library/playlists/{id}` | GET | 获取播放列表详情 |
| `/me/library/playlists/{id}/tracks` | GET | 获取播放列表中的曲目 |
| `/me/library/search` | GET | 在音乐库中搜索 |
| `/me/library` | POST | 将曲目添加到音乐库 |
| `/catalog/{sf}/songs/{id}/library` | GET | 从曲目库 ID 获取音乐库 ID |

### 播放列表管理

| 端点 | 方法 | 功能描述 |
|----------|--------|-------------|
| `/me/library/playlists` | POST | 创建播放列表 |
| `/me/library/playlists/{id}/tracks` | POST | 向播放列表中添加曲目 |

### 个性化推荐

| 端点 | 方法 | 功能描述 |
|----------|--------|-------------|
| `/me/recommendations` | GET | 获取个性化推荐曲目 |
| `/me/history/heavy-rotation` | GET | 最常播放的曲目 |
| `/me/recent/played` | GET | 最近播放的曲目 |
| `/me/recent/added` | GET | 最近添加的曲目 |

### 评分功能

| 端点 | 方法 | 功能描述 |
|----------|--------|-------------|
| `/me/ratings/songs/{id}` | GET | 获取歌曲评分 |
| `/me/ratings/songs/{id}` | PUT | 设置歌曲评分 |
| `/me/ratings/songs/{id}` | DELETE | 删除歌曲评分 |
| `/me/ratings/albums/{id}` | GET/PUT/DELETE | 设置专辑评分 |
| `/me/ratings/playlists/{id}` | GET/PUT/DELETE | 设置播放列表评分 |

### 商店信息

| 端点 | 方法 | 功能描述 |
|----------|--------|-------------|
| `/storefronts` | GET | 获取所有商店信息 |
| `/storefronts/{id}` | 获取特定商店的详情 |
| `/me/storefront` | 获取用户当前使用的商店 |

## 常用查询参数

| 参数 | 描述 | 示例 |
|-----------|-------------|---------|
| `term` | 搜索关键词 | `term=beatles` |
| `types` | 资源类型 | `types=songs,albums` |
| `limit` | 每页显示的结果数量（最多 25 条） | `limit=10` |
| `offset` | 分页偏移量 | `offset=25` |
| `include` | 是否包含相关资源 | `include=artists,albums` |
| `extend` | 是否包含附加信息 | `extend=editorialNotes` |
| `l` | 语言代码 | `l=en-US` |

## 搜索示例

```bash
GET /v1/catalog/us/search?term=wonderwall&types=songs&limit=10

Response:
{
  "results": {
    "songs": {
      "data": [{
        "id": "1234567890",
        "type": "songs",
        "attributes": {
          "name": "Wonderwall",
          "artistName": "Oasis",
          "albumName": "(What's the Story) Morning Glory?",
          "durationInMillis": 258773,
          "releaseDate": "1995-10-02",
          "genreNames": ["Alternative", "Music"]
        }
      }]
    }
  }
}
```

## 基于库的工作流程（完整示例）

将一首曲目从曲目库添加到播放列表中需要执行 4 次 API 调用：

```python
import requests

headers = {
    "Authorization": f"Bearer {dev_token}",
    "Music-User-Token": user_token
}

# 1. Search catalog
r = requests.get(
    "https://api.music.apple.com/v1/catalog/us/search",
    headers=headers,
    params={"term": "Wonderwall Oasis", "types": "songs", "limit": 1}
)
catalog_id = r.json()['results']['songs']['data'][0]['id']

# 2. Add to library
requests.post(
    "https://api.music.apple.com/v1/me/library",
    headers=headers,
    params={"ids[songs]": catalog_id}
)

# 3. Get library ID (catalog ID → library ID)
r = requests.get(
    f"https://api.music.apple.com/v1/catalog/us/songs/{catalog_id}/library",
    headers=headers
)
library_id = r.json()['data'][0]['id']

# 4. Add to playlist (library IDs only!)
requests.post(
    f"https://api.music.apple.com/v1/me/library/playlists/{playlist_id}/tracks",
    headers={**headers, "Content-Type": "application/json"},
    json={"data": [{"id": library_id, "type": "library-songs"}]}
)
```

## 创建播放列表

```bash
POST /v1/me/library/playlists
Content-Type: application/json

{
  "attributes": {
    "name": "Road Trip",
    "description": "Summer vibes"
  },
  "relationships": {
    "tracks": {
      "data": []
    }
  }
}
```

## 设置歌曲评分

```bash
# Love a song (value: 1 = love, -1 = dislike)
PUT /v1/me/ratings/songs/{id}
Content-Type: application/json

{"attributes": {"value": 1}}
```

## 限制

- **无法直接控制播放**：API 无法直接播放、暂停或跳过曲目 |
- **播放列表编辑**：只能修改通过 API 创建的播放列表 |
- **令牌管理**：开发者令牌的有效期为 180 天 |
- **请求限制**：Apple 会对 API 请求进行频率限制 |

---

## 常见错误

- **错误 1：在播放列表中使用曲目库 ID**：  
  **解决方法：** 先将曲目添加到音乐库中，再获取其 ID，最后将其添加到播放列表中。  
- **错误 2：尝试使用 AppleScript 播放曲目库中的曲目**：  
  **解决方法：** 确保曲目已存在于音乐库中。  
- **错误 3：未对用户输入的字符串进行转义**：  
  **解决方法：** 在使用用户输入之前，必须对其进行正确的转义处理。  
- **错误 4：令牌过期**：  
  **解决方法：** 定期检查令牌的有效期，并妥善处理 401 错误。

---

# 更简单的解决方案：mcp-applemusic

[mcp-applemusic](https://github.com/epheterson/mcp-applemusic) 这个工具可以自动处理所有复杂的集成细节，包括 AppleScript 的字符串转义、令牌管理以及基于库的工作流程。

**安装方法：**
```bash
git clone https://github.com/epheterson/mcp-applemusic.git
cd mcp-applemusic && python3 -m venv venv && source venv/bin/activate
pip install -e .
```

**配置 Claude Desktop：**
```json
{
  "mcpServers": {
    "Apple Music": {
      "command": "/path/to/mcp-applemusic/venv/bin/python",
      "args": ["-m", "applemusic_mcp"]
    }
  }
}
```

在 macOS 上，大多数功能可以立即使用。如需使用曲目库相关功能或在 Windows/Linux 平台上使用该工具，请参阅项目的 README 文件。

| 方法 | mcp-applemusic | 备注 |
|--------|----------------|---------|
| 添加歌曲 | 需要 4 次 API 调用（`playlist(action="add", auto_search=True)` | |
| 字符串转义 | 自动完成 | |
| 令牌管理 | 自动处理，并提供警告 | |

---

通过 mcp-applemusic，您可以简化与 Apple Music 的集成过程，无需手动处理各种细节。