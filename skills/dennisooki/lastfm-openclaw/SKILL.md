---
name: lastfm
description: 访问 Last.fm 用户资料，查看当前正在播放的歌曲、按时间段分类的热门歌曲/艺术家/专辑、用户喜爱的歌曲，以及可选地标记歌曲为“喜爱”或“不喜欢”。
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["LASTFM_API_KEY", "LASTFM_USERNAME"], "bins": ["curl", "jq"] },
        "primaryEnv": "LASTFM_API_KEY",
        "emoji": "🎵"
      }
  }
---
# Last.fm 个人资料技能

该技能用于检索 Last.fm 用户的收听数据，包括当前正在播放的歌曲、按时间段划分的热门歌曲/艺术家/专辑，以及用户喜爱的歌曲。当配置了 `LASTFM_SESSION_KEY` 时，还支持写入操作（如添加/移除喜爱的歌曲、进行歌曲抓取）。

## 必需的环境变量

- `LASTFM_API_KEY`：您的 Last.fm API 密钥（可在 https://www.last.fm/api/account/create 获取）
- `LASTFM_USERNAME`：您的 Last.fm 用户名

## 可选的环境变量

- `LASTFM_SESSION_KEY`：写入操作（添加/移除喜爱的歌曲、进行歌曲抓取）所必需
- `LASTFM_API_SECRET`：用于签署写入操作（添加/移除喜爱的歌曲、进行歌曲抓取）的密钥

## 工作流程

1. 验证所需的环境变量是否已设置。
2. 确保依赖项（`jq`、`curl`）可用。
3. 确定用户请求的具体命令。
4. 构建发送到 `ws.audioscrobbler.com/2.0/` 的 API 请求。
5. 使用适当的请求方法和参数执行 HTTP GET 请求。
6. 解析 JSON 响应并将其格式化以供用户查看。

## 支持的命令

### 读取操作（无需认证）

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `now-playing`, `np` | 当前正在播放的歌曲 | `/lastfm np` |
| `top-tracks [period]` | 按时间段划分的热门歌曲 | `/lastfm top-tracks 7day` |
| `top-artists [period]` | 按时间段划分的热门艺术家 | `/lastfm top-artists 1month` |
| `top-albums [period]` | 按时间段划分的热门专辑 | `/lastfm top-albums overall` |
| `loved` | 用户喜爱的歌曲 | `/lastfm loved` |
| `recent [limit]` | 最近的歌曲（默认 10 首） | `/lastfm recent 20` |
| `profile` | 用户个人资料信息 | `/lastfm profile` |

### 时间段

- `7day`：过去 7 天
- `1month`：过去 30 天
- `3month`：过去 90 天
- `6month`：过去 180 天
- `12month`：过去 12 个月
- `overall`：所有时间（未指定时默认）

### 写入操作（需要认证）

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `love <artist> <track>` | 将歌曲添加到喜爱列表 | `/lastfm love "Radiohead" "Creep"` |
| `unlove <artist> <track>` | 从喜爱列表中移除歌曲 | `/lastfm unlove "Radiohead" "Creep"` |

## API 请求构建

基础 URL：`https://ws.audioscrobbler.com/2.0/`

所有请求都必须包含的参数：
- `api_key`：来自 `LASTFM_API_KEY` 的值
- `format`：`json`
- `method`：API 方法名称

针对用户的特定请求还需要：
- `user`：来自 `LASTFM_USERNAME` 的值

### 方法参数

| 方法 | 额外参数 |
|--------|----------------------|
| `user.getInfo` | `user` |
| `user.getRecentTracks` | `user`, `limit`（可选） |
| `user.getTopTracks` | `user`, `period`（可选） |
| `user.getTopArtists` | `user`, `period`（可选） |
| `user.getTopAlbums` | `user`, `period`（可选） |
| `user.getLovedTracks` | `user` |
| `track.love` | `artist`, `track`, `sk`（会话密钥） |
| `track.unlove` | `artist`, `track`, `sk`（会话密钥） |

## 响应解析

### 当前正在播放的歌曲

从 `recenttracks.track[0]` 中提取信息：
- 如果 `@attr.nowplaying === "true"`，则表示歌曲正在播放中。
- `artist.#text`：艺术家名称
- `name`：歌曲名称
- `album.#text`：专辑名称

### 热门歌曲/艺术家/专辑

从以下数组中提取信息：
- `toptracks.track[]`：热门歌曲
- `topartists.artist[]`：热门艺术家
- `topalbums.album[]`：热门专辑

每个项目包含以下信息：
- `name`：项目名称
- `playcount`：播放次数
- `artist.name`：艺术家名称（对于歌曲/专辑）
- `@attr.rank`：在排行榜中的排名

### 个人资料

从 `user` 中提取信息：
- `name`：用户名
- `realname`：真实姓名（如果已设置）
- `playcount`：总抓取次数
- `country`：国家
- `registered`：账户创建日期
- `url`：个人资料链接

## 安全规范

- 绝不要在输出中记录或暴露 API 密钥或会话密钥。
- 遵守 Last.fm 的每秒 5 次请求的限制。
- 如果未设置 `LASTFM_SESSION_KEY`，写入操作应优雅地失败。
- 所有用户输入在发送 API 请求之前必须进行 URL 编码。
- 仅连接到 `ws.audioscrobbler.com`，不得使用其他外部端点。
- 优雅地处理数据缺失的情况（例如，没有当前正在播放的歌曲、喜爱的歌曲为空）。
- 确保 `period` 参数值为 `7day`、`1month`、`3month`、`6month`、`12month` 或 `overall` 中的一个。
- 确保 `recent` 参数为数字且介于 1 到 200 之间。

## 错误处理

| 错误代码 | 含义 | 处理方式 |
|------------|---------|--------|
| 10 | API 密钥无效 | 告知用户检查 `LASTFM_API_KEY` |
| 6 | 参数无效 | 确保所需参数已提供 |
| 29 | 超过请求频率限制 | 等待片刻后重试，并通知用户 |
| 26 | API 密钥被暂停 | 将用户引导至 Last.fm 客服 |
| 4 | 认证失败 | 检查写入操作所需的会话密钥 |

## 示例输出格式

### 当前正在播放的歌曲

```
🎵 Now Playing:
"Track Name" by Artist Name
from Album Name
```

如果当前没有歌曲正在播放：

```
🎵 Last Played:
"Track Name" by Artist Name
Listened: [timestamp]
```

### 热门歌曲

```
🎵 Top Tracks (7 days):

1. "Track One" by Artist One (42 plays)
2. "Track Two" by Artist Two (38 plays)
3. "Track Three" by Artist Three (31 plays)
...
```

### 个人资料

```
🎵 Last.fm Profile: username

📊 15,432 total scrobbles
🌍 United Kingdom
📅 Member since: Nov 2002
🔗 last.fm/user/username
```

## 设置说明

1. 在 https://www.last.fm/api/account/create 获取 Last.fm API 密钥。
2. 将密钥添加到 `~/.openclaw/openclaw.json` 文件中：

```json5
{
  skills: {
    entries: {
      lastfm: {
        enabled: true,
        env: {
          LASTFM_API_KEY: "your_api_key_here",
          LASTFM_USERNAME: "your_username"
        }
      }
    }
  }
}
```

3. 关于写入操作，请参阅 `{baseDir}/references/auth-guide.md`。