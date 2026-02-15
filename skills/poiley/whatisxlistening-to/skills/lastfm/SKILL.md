---
name: lastfm
description: 可以访问 Last.fm 的收听历史记录、音乐统计信息以及发现功能。可以查询最近的歌曲、热门艺术家/专辑/歌曲、用户喜爱的歌曲、相似的艺术家，以及全球音乐排行榜。
---

# Last.fm API 技能

用于访问 Last.fm 的收听历史记录、音乐统计信息以及新发现的音乐。

## 配置

**必需的环境变量**（请将其添加到您的 shell 配置文件中，或可选地添加到 `~/.clawdbot/.env` 文件中）：
- `LASTFM_API_KEY` — 您的 Last.fm API 密钥（[在此处获取](https://www.last.fm/api/account/create)）
- `LASTFM_USER` — 您的 Last.fm 用户名

**基础 URL**：`http://ws.audioscrobbler.com/2.0/`  
**文档**：https://lastfm-docs.github.io/api-docs/

## 示例输出

以下是 17 年以上音乐收听记录的示例：

```
Total scrobbles: 519,778
Unique artists: 13,763
Unique tracks: 68,435
Unique albums: 33,637

Top Artists (all time):
• System of a Down (52,775 plays)
• Eminem (15,400 plays)
• Dashboard Confessional (10,166 plays)
• Edguy (10,161 plays)
• Metallica (9,927 plays)

Top Tracks (all time):
• System of a Down - Aerials (1,405 plays)
• System of a Down - Toxicity (1,215 plays)
• System of a Down - Sugar (1,149 plays)
• System of a Down - Chop Suey (1,116 plays)
• System of a Down - Prison Song (1,102 plays)
```

## 快速参考

所有请求均使用 GET 方法，并包含以下基础参数：

```
?api_key=$LASTFM_API_KEY&format=json&user=$LASTFM_USER
```

### 用户端点

#### 最新播放的歌曲
```bash
curl -s "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=$LASTFM_USER&api_key=$LASTFM_API_KEY&format=json&limit=10"
```
- 其中第一条满足 `@attr.nowplaying=true` 条件的歌曲正在播放
- 返回内容：艺术家名称、歌曲名称、专辑名称、时间戳以及图片

#### 用户信息（个人资料统计）
```bash
curl -s "http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user=$LASTFM_USER&api_key=$LASTFM_API_KEY&format=json"
```
- 返回内容：播放次数、艺术家数量、歌曲数量、专辑数量、注册日期

#### 热门艺术家
```bash
curl -s "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=$LASTFM_USER&api_key=$LASTFM_API_KEY&format=json&period=7day&limit=10"
```
- 时间范围：全部 | 7 天 | 1 个月 | 3 个月 | 6 个月 | 12 个月

#### 热门专辑
```bash
curl -s "http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user=$LASTFM_USER&api_key=$LASTFM_API_KEY&format=json&period=7day&limit=10"
```

#### 热门歌曲
```bash
curl -s "http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user=$LASTFM_USER&api_key=$LASTFM_API_KEY&format=json&period=7day&limit=10"
```

#### 用户喜爱的歌曲
```bash
curl -s "http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user=$LASTFM_USER&api_key=$LASTFM_API_KEY&format=json&limit=10"
```

#### 周排行榜
```bash
# Weekly artist chart
curl -s "http://ws.audioscrobbler.com/2.0/?method=user.getweeklyartistchart&user=$LASTFM_USER&api_key=$LASTFM_API_KEY&format=json"

# Weekly track chart
curl -s "http://ws.audioscrobbler.com/2.0/?method=user.getweeklytrackchart&user=$LASTFM_USER&api_key=$LASTFM_API_KEY&format=json"

# Weekly album chart
curl -s "http://ws.audioscrobbler.com/2.0/?method=user.getweeklyalbumchart&user=$LASTFM_USER&api_key=$LASTFM_API_KEY&format=json"
```

### 艺术家/歌曲/专辑信息

#### 艺术家信息
```bash
curl -s "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=Tame+Impala&api_key=$LASTFM_API_KEY&format=json&username=$LASTFM_USER"
```
- 添加 `username` 参数后，会显示该艺术家的个人播放次数

#### 类似艺术家
```bash
curl -s "http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist=Tame+Impala&api_key=$LASTFM_API_KEY&format=json&limit=10"
```

#### 艺术家的热门歌曲
```bash
curl -s "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist=Tame+Impala&api_key=$LASTFM_API_KEY&format=json&limit=10"
```

#### 歌曲信息
```bash
curl -s "http://ws.audioscrobbler.com/2.0/?method=track.getinfo&artist=Tame+Impala&track=The+Less+I+Know+The+Better&api_key=$LASTFM_API_KEY&format=json&username=$LASTFM_USER"
```

#### 类似歌曲
```bash
curl -s "http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist=Tame+Impala&track=Elephant&api_key=$LASTFM_API_KEY&format=json&limit=10"
```

#### 专辑信息
```bash
curl -s "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&artist=Tame+Impala&album=Currents&api_key=$LASTFM_API_KEY&format=json&username=$LASTFM_USER"
```

### 搜索

#### 搜索艺术家
```bash
curl -s "http://ws.audioscrobbler.com/2.0/?method=artist.search&artist=tame&api_key=$LASTFM_API_KEY&format=json&limit=5"
```

#### 搜索歌曲
```bash
curl -s "http://ws.audioscrobbler.com/2.0/?method=track.search&track=elephant&api_key=$LASTFM_API_KEY&format=json&limit=5"
```

#### 搜索专辑
```bash
curl -s "http://ws.audioscrobbler.com/2.0/?method=album.search&album=currents&api_key=$LASTFM_API_KEY&format=json&limit=5"
```

### 全球排行榜
```bash
# Top artists globally
curl -s "http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key=$LASTFM_API_KEY&format=json&limit=10"

# Top tracks globally
curl -s "http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key=$LASTFM_API_KEY&format=json&limit=10"
```

### 标签
```bash
# Top albums for a tag/genre
curl -s "http://ws.audioscrobbler.com/2.0/?method=tag.gettopalbums&tag=psychedelic&api_key=$LASTFM_API_KEY&format=json&limit=10"

# Top artists for a tag
curl -s "http://ws.audioscrobbler.com/2.0/?method=tag.gettopartists&tag=brazilian&api_key=$LASTFM_API_KEY&format=json&limit=10"
```

## 有用的 jq 过滤器

有关 JSON 处理的更多信息，请参阅 [ClawdHub 上的 jq 技能文档](https://clawdhub.com/skills/jq)。

```bash
# Recent tracks: artist - track
jq '.recenttracks.track[] | "\(.artist["#text"]) - \(.name)"'

# Top artists: name (playcount)
jq '.topartists.artist[] | "\(.name) (\(.playcount))"'

# Check if currently playing
jq '.recenttracks.track[0] | if .["@attr"].nowplaying == "true" then "Now playing: \(.artist["#text"]) - \(.name)" else "Last played: \(.artist["#text"]) - \(.name)" end'
```

## 注意事项

- 仅读取数据的端点无需身份验证（只需提供 API 密钥即可）
- 请合理使用请求频率，暂无明确的请求限制
- 艺术家/歌曲/专辑名称需要使用 URL 编码（空格替换为 `+` 或 `%20`）
- 图片提供小、中、大、特大四种尺寸