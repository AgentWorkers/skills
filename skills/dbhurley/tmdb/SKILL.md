---
name: tmdb
description: 通过 TMDb API 搜索电影/电视剧，获取演员阵容、评分、流媒体播放信息以及个性化推荐。
homepage: https://www.themoviedb.org/
metadata: {"clawdis":{"emoji":"🎬","requires":{"bins":["uv"],"env":["TMDB_API_KEY"]},"primaryEnv":"TMDB_API_KEY"}}
---

# TMDb - 电影数据库

提供全面的电影和电视信息，包括流媒体播放功能、推荐内容以及个性化服务。

## 设置

设置环境变量：
- `TMDB_API_KEY`：您的 TMDb API 密钥（可在 themoviedb.org 免费获取）

## 快速命令

### 搜索
```bash
# Search movies
uv run {baseDir}/scripts/tmdb.py search "Inception"

# Search TV shows
uv run {baseDir}/scripts/tmdb.py search "Breaking Bad" --tv

# Search people (actors, directors)
uv run {baseDir}/scripts/tmdb.py person "Christopher Nolan"
```

### 电影/电视详情
```bash
# Full movie info
uv run {baseDir}/scripts/tmdb.py movie 27205

# With cast
uv run {baseDir}/scripts/tmdb.py movie 27205 --cast

# TV show details
uv run {baseDir}/scripts/tmdb.py tv 1396

# By name (searches first, then shows details)
uv run {baseDir}/scripts/tmdb.py info "The Dark Knight"
```

### 流媒体播放平台
```bash
# Find streaming availability
uv run {baseDir}/scripts/tmdb.py where "Inception"
uv run {baseDir}/scripts/tmdb.py where 27205

# Specify region
uv run {baseDir}/scripts/tmdb.py where "Inception" --region GB
```

### 新发现
```bash
# Trending this week
uv run {baseDir}/scripts/tmdb.py trending
uv run {baseDir}/scripts/tmdb.py trending --tv

# Recommendations based on a movie
uv run {baseDir}/scripts/tmdb.py recommend "Inception"

# Advanced discover
uv run {baseDir}/scripts/tmdb.py discover --genre action --year 2024
uv run {baseDir}/scripts/tmdb.py discover --genre sci-fi --rating 7.5
```

### 个性化设置
```bash
# Get personalized suggestions (uses Plex history + preferences)
uv run {baseDir}/scripts/tmdb.py suggest <user_id>

# Set preferences
uv run {baseDir}/scripts/tmdb.py pref <user_id> --genres "sci-fi,thriller,drama"
uv run {baseDir}/scripts/tmdb.py pref <user_id> --directors "Christopher Nolan,Denis Villeneuve"
uv run {baseDir}/scripts/tmdb.py pref <user_id> --avoid "horror,romance"

# View preferences
uv run {baseDir}/scripts/tmdb.py pref <user_id> --show
```

### 观看列表
```bash
# Add to watchlist
uv run {baseDir}/scripts/tmdb.py watchlist <user_id> add 27205
uv run {baseDir}/scripts/tmdb.py watchlist <user_id> add "Dune: Part Two"

# View watchlist
uv run {baseDir}/scripts/tmdb.py watchlist <user_id>

# Remove from watchlist
uv run {baseDir}/scripts/tmdb.py watchlist <user_id> rm 27205
```

## 集成

### Plex
如果支持 Plex 功能，`suggest` 命令会根据用户的近期观看记录提供推荐内容。

### ppl.gift (CRM)
如果支持 ppl 功能，用户的偏好设置会保存在联系人信息中，以便在不同会话间保持一致。

## 类型ID

用于 `--genre` 过滤的常见类型：
- 动作 (28), 冒险 (12), 动画 (16)
- 喜剧 (35), 犯罪 (80), 纪录片 (99)
- 戏剧 (18), 家庭 (10751), 幻想 (14)
- 恐怖 (27), 神秘 (9648), 浪漫 (10749)
- 科幻 (878), 惊悚 (53), 战争 (10752)

## 注意事项

- TMDb API：每 10 秒允许 40 次请求（免费 tier）
- 流媒体播放平台因地区而异（默认为美国）
- 推荐内容结合了 TMDb 数据、用户偏好和观看记录生成。