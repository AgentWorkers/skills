---
name: apple-music-dj
description: 这是一款专为Apple Music设计的终极个性化工具。它通过分析用户的收听历史、Apple Music的回放数据、音乐库信息以及个人音乐品味，利用MusicKit API在用户的Apple Music音乐库中自动生成智能播放列表。该工具支持以下功能：深度挖掘隐藏的优质歌曲、根据用户情绪或活动创建播放列表、追踪音乐趋势、提供惊喜推荐（“Surprise Me”功能）、定期自动更新播放列表、生成个性化的音乐推荐卡、评估歌曲的兼容性、提供详细的专辑分析、引导用户探索艺术家作品、推送每日新歌、协助用户准备音乐会演出，以及提供个性化的新歌推荐。无论用户提到Apple Music、播放列表、音乐推荐、收听习惯、音乐品味、寻找新音乐、创建适合不同场景的播放列表（如运动时使用的播放列表）、发现热门歌曲或隐藏的宝藏曲目，还是任何与音乐体验定制相关的内容，都可以使用这款工具。此外，当用户在对话中提到“DJ”、“混音”、“为[某场景]制作播放列表”、“类似[某歌曲]的歌曲”、“当前热门歌曲”、“适合我的新歌”、“音乐品味分析”、“歌曲兼容性”、“年度音乐回顾”、“收听统计”、“我错过了哪些歌曲”、“深入分析专辑”、“探索艺术家作品”、“准备观看[某艺术家]的演唱会”、“每日推荐歌曲”或“OpenClaw”等关键词时，该工具也会自动触发并提供相应的帮助。
version: 3.1.0
emoji: 🎧
author: Andernet (Matthew Anderson) <and3rn3t@icloud.com>
homepage: https://github.com/and3rn3t/apple-music-dj
license: MIT
tags:
  - music
  - apple-music
  - playlists
  - personalization
  - musickit
  - discovery
category: music
icon: assets/icon.svg
metadata:
  openclaw:
    requires:
      env:
        - APPLE_MUSIC_DEV_TOKEN
        - APPLE_MUSIC_USER_TOKEN
      bins:
        - curl
        - jq
        - python3
    primaryEnv: APPLE_MUSIC_DEV_TOKEN
    platforms:
      - macos
      - linux
    minVersion: "1.0.0"
    permissions:
      - network
      - filesystem
---
# Apple Music DJ 🎧

这是一个专为 OpenClaw 设计的智能 Apple Music 个性化引擎。它会分析您的听歌历史、播放统计、评分以及音乐库内容，从而构建出一个详细的音乐品味档案，并基于五种策略生成播放列表。同时，该引擎还会提供关于您音乐偏好的洞察，并将所有结果直接更新到您的 Apple Music 库中。此外，它还支持生成可分享的音乐品味卡片、兼容性评分、音乐库分析、专辑深度探索、艺术家推荐等功能。

## 架构

```
User Request
     │
     ▼
┌─────────────┐    ┌──────────────────────────────────────────────┐
│  Taste       │◄──│  Apple Music API (read)                      │
│  Profiler    │    │  · recently played    · library songs/artists│
│  (cached)    │    │  · heavy rotation     · ratings (loved/hated)│
│              │    │  · recommendations    · Replay summaries     │
└──────┬───────┘    └──────────────────────────────────────────────┘
       │
       ▼
┌─────────────┐    ┌──────────────────────────────────────────────┐
│  Strategy    │───▶│  Apple Music API (catalog)                   │
│  Engine      │    │  · search · charts · artist albums/top songs │
│              │    │  · genres · new releases                     │
└──────┬───────┘    └──────────────────────────────────────────────┘
       │
       ▼
┌─────────────┐    ┌──────────────────────────────────────────────┐
│  Playlist    │───▶│  Apple Music API (write)                     │
│  Builder     │    │  · POST /me/library/playlists                │
│              │    │  · POST /me/library/playlists/{id}/tracks     │
└─────────────┘    └──────────────────────────────────────────────┘
```

## 先决条件

必须设置两个环境变量。如果您尚未设置，请先参考 `references/auth-setup.md` 文件进行配置。

| 变量 | 用途 |
|---|---|
| `APPLE_MUSIC_DEV_TOKEN` | 用 MusicKit 私钥签名的 JWT（来自 Apple 开发者门户） |
| `APPLE_MUSIC_USER_TOKEN` | 每个用户的授权令牌（通过 MusicKit 的 `authorize()` 函数获取） |

使用以下命令验证这些变量：`scripts/apple_music_api.sh verify`

## 音乐品味分析

在生成任何播放列表之前，首先需要构建（或从缓存中加载）您的音乐品味档案。运行以下命令：

```
python3 scripts/taste_profiler.py [--cache ~/.apple-music-dj/taste_profile.json] [--max-age 0] [--storefront us]
```

使用 `--max-age 0` 选项可以强制刷新档案，忽略任何缓存内容。

该分析工具会从以下所有可用数据源中提取信息：

| 数据源 | 端点 | 信息类型 |
|---|---|---|
| 喜欢/不喜欢的歌曲 | `GET /v1/me/ratings/songs` | 明确的喜好偏好 |
| 高频播放的歌曲 | `GET /v1/me/history/heavy-rotation` | 频繁播放的歌曲 |
| 最近播放的歌曲 | `GET /v1/me/recent/played/tracks` | 当前的音乐情绪 |
| 播放摘要 | `GET /v1/me/music-summaries` | 年度播放统计 |
| 音乐库中的歌曲 | `GET /v1/me/library/songs?include=catalog` | 广泛的音乐品味 |
| 音乐库中的艺术家 | `GET /v1/me/library/artists` | 对艺术家的偏好 |
| 推荐歌曲 | `GET /v1/me/recommendations` | Apple 的推荐算法 |

分析结果会保存在 `~/.apple-music-dj/taste_profile.json` 文件中（默认缓存有效期为 7 天）。

该档案包含以下内容：热门艺术家、音乐类型分布、时代特征、能量等级、音乐多样性、喜欢/不喜欢的歌曲 ID、音乐库中的歌曲 ID 以及播放亮点。

### 稀疏数据处理

如果用户的听歌历史记录较少：
1. 优先参考 `GET /v1/me/recommendations` 提供的推荐歌曲。
2. 请求用户提供 3–5 位他们喜欢的艺术家或歌曲作为手动种子。
3. 使用这些种子通过音乐库搜索来生成新的播放列表。

## 播放列表策略

共有五种策略。详细算法请参阅 `references/playlist-strategies.md` 文件。

### 策略 1：深度探索（Deep Cuts Explorer）
**触发条件**：使用关键词如 "deep cuts", "hidden gems", "B-sides", "underrated", "album tracks"
该策略会寻找用户喜欢但尚未听过的艺术家作品，排除热门歌曲、单曲以及音乐库中的现有歌曲。

### 策略 2：情绪/活动匹配（Mood / Activity Matcher）
**触发条件**：根据用户选择的情绪或活动（如 "workout", "chill", "focus", "party", "sleep", "cooking", "running", "morning", "sad", "study", "dinner"）来推荐歌曲。
该策略会根据用户的音乐偏好筛选相应的歌曲。

### 策略 3：趋势雷达（Trend Radar）
**触发条件**：使用关键词如 "trending", "what's hot", "charts", "popular", "new releases"
该策略会根据用户的音乐类型偏好推荐当前的热门歌曲。

### 策略 4：音乐品味拓展（Constellation Discovery）
**触发条件**：使用关键词如 "surprise me", "something new", "expand my taste", "I'm bored", "discovery"
该策略会从用户熟悉的艺术家开始，逐步探索新的音乐风格。

### 策略 5：播放列表更新（Playlist Refresh / Evolution）
**触发条件**：使用关键词如 "refresh my [playlist]", "update my [playlist]", "evolve", "getting stale"
该策略会分析现有播放列表的风格，并添加新的推荐歌曲，同时删除播放次数过多的歌曲。

## 互动功能

除了播放列表策略外，这些功能还能促进用户的日常音乐探索和更深入的音乐发现：

### 音乐品味卡片（Taste DNA Card）
**触发条件**：使用关键词如 "taste card", "taste DNA", "share my taste", "my music identity", "listener profile"
该功能会生成一张可分享的视觉卡片（SVG 或文本格式），总结用户的音乐品味：例如 "Deep Catalog Digger" 或 "Genre Drifter" 等标签。卡片会显示热门音乐类型、顶级艺术家、时代特征以及相关数据。

运行以下命令生成卡片：
```
python3 scripts/taste_card.py <profile.json> [--format svg|text] [--output card.svg]
```

卡片中的类型标签会根据用户的品味档案自动生成。聊天界面会同时提供文本版本和 SVG 格式的卡片（便于截图分享）。

### 兼容性评分（Compatibility Score）
**触发条件**：使用关键词如 "how compatible am I with [artist]", "compatibility", "do I match [artist]", "compare my taste with", "would I like [artist]"
该功能会评估用户的音乐品味与特定艺术家的音乐风格之间的匹配程度（0–100%）。

运行以下命令进行比较：
```
python3 scripts/compatibility.py artist <profile.json> <storefront> <artist_name>
python3 scripts/compatibility.py profile <profile1.json> <profile2.json>
```

结果会显示匹配程度（如 "Deeply compatible", "Strong overlap", "Wild card"）以及匹配的音乐类型，还会指出艺术家是否已经存在于用户的音乐库中。

### 音乐聆听洞察（Listening Insights）
提供以下功能来帮助用户更深入地了解自己的音乐喜好：

**时间线（Timeline）**：
```
python3 scripts/listening_insights.py timeline <profile.json>
```
该功能会展示用户多年来的音乐品味变化：例如 "2022 年你偏爱 shoegaze 风格，到 2024 年转向了 jazz"。

**播放习惯（Streaks）**：
```
python3 scripts/listening_insights.py streaks <profile.json>
```
该功能会展示用户的播放习惯和关键里程碑，例如艺术家忠诚度、音乐类型占比、发现的新歌曲数量等。

**年度回顾（Year in Review）**：
```
python3 scripts/listening_insights.py year-review <profile.json> [--year 2025]
```
该功能会提供全面的年度分析，包括歌曲的播放频率、音乐类型多样性等详细信息。

### 音乐库分析（Catalog Gap Analysis）
**触发条件**：使用关键词如 "what have I missed", "what am I missing from [artist]", "catalog gaps", "albums I haven't heard"
该功能会扫描用户喜欢的艺术家的完整作品集，找出用户音乐库中尚未拥有的专辑，并按发布日期排序推荐。

运行以下命令：
```
python3 scripts/catalog_explorer.py gap-analysis <profile.json> <storefront>
```
结果会显示用户可能错过的专辑，并按推荐顺序列出。

### 专辑深度探索（Album Deep Dive）
**触发条件**：使用关键词如 "tell me about [album]", "album deep dive", "what's on [album]", "should I listen to [album]", "break down [album]"
该功能会提供专辑的详细信息，包括曲目列表、曲目分类（单曲/深度推荐曲目）、专辑在艺术家作品集中的位置，以及推荐的首选曲目。

运行以下命令：
```
python3 scripts/catalog_explorer.py album-dive <storefront> <album_name> [--artist <name>}
```

### 艺术家探索（Artist Rabbit Hole）
**触发条件**：使用关键词如 "rabbit hole from [artist]", "take me on a journey from [artist]", "artist chain", "explore from [artist]"
该功能会从用户喜欢的艺术家开始，逐步探索相关艺术家及其作品。

运行以下命令：
```
python3 scripts/catalog_explorer.py rabbit-hole <profile.json> <storefront> <artist_name> [--depth 4]
```
每个探索步骤都会显示相关艺术家的名称、音乐类型以及推荐曲目。用户可以选择继续探索或生成播放列表。

### 每日推荐（Daily Song Drop）
**触发条件**：使用关键词如 "daily song", "song of the day", "give me one track", "daily pick"
该功能会根据用户偏好每天推荐一首歌曲。

运行以下命令：
```
python3 scripts/daily_pick.py daily <profile.json> <storefront>
```

### 即时推荐（What Should I Listen To Now?）
**触发条件**：根据当前时间和用户偏好提供即时推荐。
该功能会考虑时间因素（如早晨适合轻松的音乐，夜晚适合氛围音乐），并据此推荐合适的歌曲。

运行以下命令：
```
python3 scripts/daily_pick.py now <profile.json> <storefront>
```

### 演唱会准备（Concert Prep Playlist）
**触发条件**：使用关键词如 "seeing [artist] live", "concert prep", "going to [artist] show", "setlist for [artist]", "get ready for [artist]"
该功能会根据用户的音乐喜好生成演唱会前的播放列表。

运行以下命令：
```
scripts/concert_prep.sh <storefront> <artist_name> [playlist_name]
```

### 个性化新专辑推荐（Personalized New Release Radar）
**触发条件**：使用关键词如 "new releases", "what's new from my artists", "any new music", "release radar", "new albums this week"
该功能会扫描用户最近喜欢的 20 位艺术家在过去 7 天内的新专辑，并推荐相关的新作品。

运行以下命令：
```
python3 scripts/new_releases.sh <profile.json> <storefront> [--create-playlist]
```

## 快速命令

| 用户指令 | 功能 |
|---|---|
| "Analyze my taste" | 分析用户的音乐品味并生成报告 |
| "Show my taste card" | 生成并显示音乐品味卡片 |
| "Make me a playlist" | 询问播放列表类型并选择生成策略 |
| "Surprise me" | 生成随机推荐的播放列表 |
| "More like [artist]" | 结合用户喜欢的艺术家生成播放列表 |
| "Refresh my workout playlist" | 更新用户的运动场景播放列表 |
| "What have I been into?" | 显示最近的听歌记录 |
| "How compatible am I with [artist]?" | 评估用户与特定艺术家的兼容性 |
| "What have I missed from [artist]?" | 查找用户未听过的艺术家作品 |
| "Tell me about [album]" | 详细分析用户未听过的专辑 |
| "Take me on a rabbit hole from [artist]" | 探索相关艺术家的作品 |
| "Give me one song" | 提供每日推荐歌曲 |
| "What should I listen to right now?" | 根据当前时间和偏好提供即时推荐 |
| "I'm seeing [artist] next week" | 生成演唱会前的播放列表 |
| "Any new releases for me?" | 推荐用户最近喜欢的艺术家的新作品 |
| "My year in review" | 提供过去一年的音乐回顾 |
| "Set up weekly playlists" | 配置每周自动播放列表 |

## 自动化播放列表

OpenClaw 支持高级的 cron 和心跳功能。以下是一些常见的自动化设置：

**每周混合播放（Weekly Mix）**：
```
Schedule: Every Sunday at 9:00 AM (user's local time)
Task:
  1. Refresh taste profile cache
  2. Run Trend Radar (15 tracks)
  3. Run Constellation Discovery (10 tracks)
  4. Merge into "Weekly Mix · {date}" playlist
  5. Create in library
  6. Notify user: "🎧 Your weekly mix is ready — 25 fresh tracks"
```

**新专辑推荐（New Release Watch）**：
```
Schedule: Daily at 8:00 AM
Task:
  1. scripts/new_releases.sh <profile> <storefront>
  2. If found: notify user with artist + album/single name
  3. Optionally: --create-playlist to auto-create a playlist
```

**每日推荐（Daily Song Drop）**：
```
Schedule: Daily at 9:00 AM
Task:
  1. python3 scripts/daily_pick.py daily <profile> <storefront>
  2. Notify user: "🎧 Today's pick: {song} by {artist} — {reason}"
```

**播放列表维护（Playlist Health Check）**：
```
Schedule: Weekly (Saturday)
Task:
  1. Scan user's playlists
  2. Flag any tracks removed from Apple Music catalog (404 on lookup)
  3. Suggest replacements
```

当用户需要设置自动化播放列表时，请通过 OpenClaw 的 cron 系统进行配置，并在激活前确认时间表。

## 播放列表生成规则

在生成播放列表之前，需要遵循以下规则：

1. 播放列表的前 3–8 首曲应具有强烈的音乐风格和较高的可信度。
2. 随后的曲目应增加音乐多样性。
3. 接下来的曲目应提升整体氛围。
4. 接下来的曲目应保持音乐的连贯性。
5. 最后的曲目应作为回忆性的收尾曲目。

**硬性规则**：
- 同一位艺术家的歌曲之间至少间隔 5 首。
- 同一专辑的歌曲最多只能出现 2 首。
- 不推荐用户不喜欢的艺术家的歌曲。
- 所有推荐的曲目都必须是音乐库中的正式曲目（而非临时添加的曲目）。
- 播放列表通常包含 25–40 首歌曲（用户可自行调整）。

**播放列表命名规则**：
```
{策略} · {场景} · {年份}
```

## 应用场景检测

不同的音乐库需要使用不同的 storefront 代码（如 "us", "gb", "jp" 等）。检测顺序如下：
1. 首先检查 `APPLE_MUSIC_DEV_TOKEN` 环境变量。
2. 如果未找到，则自动检测 `GET /v1/me/storefront` 并缓存结果。
3. 如果仍未找到，则使用默认的 "us" 代码，并向用户发出警告。

## 错误处理

| 错误代码 | 含义 | 处理方式 |
|---|---|---|
| 401 | 开发者令牌无效/过期 | 重新生成 JWT（参考 `references/auth-setup.md`）。 |
| 403 | 用户令牌过期（约 6 个月） | 用户需要重新授权。 |
| 404 | 资源已从音乐库中移除 | 跳过错误，继续执行。 |
| 429 | 请求次数限制 | 采用指数级退避策略（1 秒 → 2 秒 → 4 秒 → 8 秒，最多尝试 3 次）。 |
| 数据为空 | 新用户或隐私设置导致的数据缺失 | 退回到默认推荐列表或手动推荐。 |

## 结果展示

生成播放列表后，会进行以下操作：
1. 确认播放列表的名称。
2. 简要解释播放列表的生成依据（与用户的音乐品味相关）。
3. 显示曲目列表（包含曲目名称、艺术家信息）。
4. 提供优化建议（如调整播放列表的节奏、更换曲目或调整长度）。

**沟通方式**：
以音乐爱好者的身份与用户交流，具体说明选择曲目的原因。例如：“我发现您最近偏爱 shoegaze 风格，因此推荐了 Slowdive 乐队的深度推荐曲目。”

## 参考文件

| 文件 | 适用场景 | 说明 |
|---|---|---|
| `references/auth-setup.md` | 用户需要设置令牌时参考 |
| `references/api-reference.md` | 需要了解 API 端点详情、格式和音乐类型 ID 时参考 |
| `references/playlist-strategies.md` | 在执行任何播放列表策略前参考 |
| `references/troubleshooting.md | 用户遇到问题时参考 |

## 隐私与数据保护

该功能通过 Apple Music API 访问用户数据。具体来说，它会读取、存储和传输以下数据：

**通过 Apple Music API 读取的数据：**
- `GET /v1/me/recent/played/tracks`：最近播放的歌曲
- `GET /v1/me/history/heavy-rotation`：高频播放的歌曲
- `GET /v1/me/library/songs`, `/artists`：音乐库中的歌曲和艺术家信息
- `GET /v1/me/ratings/songs`：用户的喜好评分
- `GET /v1/me/recommendations`：Apple 的推荐算法
- `GET /v1/me/music-summaries`：年度播放统计
- `GET /v1/me/storefront`：用户所在地区信息

**本地存储的数据：**
- `~/.apple-music-dj/taste_profile.json`：用户的音乐品味档案（JSON 格式）
- 生成的 Taste DNA 卡片（SVG 或文本格式）

**注意事项：**
- 该功能不会将任何数据发送给第三方服务。
- 不会进行任何数据分析或 telemetry 操作。
- 所有数据请求都直接发送给 Apple，不会在用户设备上存储。
- 令牌仅用于临时存储，不会被记录或保存。

**缓存管理：**
- 音乐品味档案的缓存有效期为 7 天。
- 可使用 `rm -rf ~/.apple-music-dj/` 清除缓存。
- 使用 `--max-age 0` 选项可以忽略缓存并获取最新数据。

## 脚本说明

| 脚本 | 语言 | 功能 |
|---|---|---|
| `scripts/_common.py` | Python | 公共工具（API 调用、档案加载等） |
| `scripts/apple_music_api.sh` | Bash | API 调用封装和处理逻辑 |
| `scripts/taste_profiler.py` | Python | 生成音乐品味档案 |
| `scripts/build_playlist.sh` | Bash | 创建和更新播放列表 |
| `scripts/generate_dev_token.py` | Python | 生成开发者专用 JWT |
| `scripts/taste_card.py` | Python | 生成可分享的音乐品味卡片 |
| `scripts/compatibility.py` | Python | 评估用户品味与艺术家的兼容性 |
| `scripts/listening_insights.py` | Python | 提供时间线、播放习惯分析等 |
| `scripts/catalog_explorer.py` | Python | 音乐库分析、专辑深度探索等 |
| `scripts/daily_pick.py` | Python | 每日推荐和即时推荐 |
| `scripts/playlist_history.py` | Python | 记录播放列表的生成历史 |
| `scripts/concert_prep.sh` | Bash | 生成演唱会前的播放列表 |
| `scripts/new_releases.sh` | Python | 推荐用户最近喜欢的艺术家新专辑 |
| `scripts/verify_setup.sh` | Bash | 配置自动化任务 |

## 示例交互场景：

- “我最近心情低落，推荐一些振奋人心的音乐。” → 使用策略 2（根据用户的情绪推荐振奋人心的歌曲）。
- “我总是听同样的 20 首歌。” → 使用策略 4（根据用户的音乐偏好推荐新的歌曲）。
- “为我生成一个适合跑步时的播放列表。” → 使用策略 2（根据用户的活动偏好推荐适合跑步的音乐）。
- “最近有什么热门歌曲？” → 使用策略 3（根据用户的音乐风格推荐热门歌曲）。
- “我喜欢 Radiohead 和 Björk，但已经听过了他们的所有作品。” → 结合策略 1 和 4 生成新的播放列表。
- “我的运动播放列表太单一了。” → 使用策略 5 更新播放列表。
- “设置每周自动播放列表。” → 配置自动播放列表。
- “展示我的音乐品味卡片。” → 生成音乐品味卡片。
- “我和 Tyler, the Creator 的音乐风格匹配度如何？” → 评估兼容性。
- “我错过了 Radiohead 的哪些专辑？” → 查找用户未听过的专辑。
- “详细介绍一下 In Rainbows 这张专辑。” → 生成专辑深度分析。
- “从 Radiohead 开始探索相关艺术家。” → 提供艺术家推荐列表。
- “今天推荐一首歌。” → 提供每日推荐歌曲。
- “我现在应该听什么？” → 根据当前时间和偏好提供即时推荐。
- “下周有 Radiohead 的演唱会，需要准备播放列表吗？” → 生成演唱会前的播放列表。
- “我的 2025 年音乐回顾。” → 提供过去一年的音乐总结。