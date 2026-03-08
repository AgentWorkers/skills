---
name: statsfm
description: 这款音乐数据工具基于 stats.fm API 运行，无需注册账户即可查询专辑曲目列表、艺术家作品集以及全球音乐排行榜。使用 stats.fm 的用户名，用户还可以查询个人在 Spotify 上的收听历史、歌曲播放次数、热门艺术家/曲目/专辑信息，以及每月的收听数据统计和当前正在播放的内容。
---
# stats.fm CLI

这是一个全面的Python命令行工具（CLI），用于查询stats.fm API（提供Spotify的收听数据分析服务）。

**系统要求：** Python 3.6及以上版本（仅需要标准库，无需安装pip）。

**脚本位置：** 位于该工具目录下的`scripts/statsfm.py`文件。示例中使用了`./statsfm.py`，假设你位于`scripts`文件夹内。

## 先决条件

**Stats.fm账户（可选）**
- 如果需要查看个人收听数据（如历史记录、热门歌曲、当前播放列表等），则需要拥有Stats.fm账户。
- 即使没有账户，也可以使用公共功能：专辑曲目列表、艺术家作品集、搜索以及全球排行榜。
- 如果还没有账户？请访问[stats.fm](https://stats.fm)并使用Spotify或Apple Music注册（Apple Music的功能尚未测试，Plus会员状态未知）。
- 如果已有账户，请复制你的用户名。

## 设置

对于公共命令（`search`、`album`、`artist-albums`、`charts-top-tracks`、`charts-top-artists`、`charts-top-albums`），无需账户。

对于个人统计信息（`profile`、`top-artists`、`top-tracks`、`recent`等），需要使用`--user USERNAME`或`-u USERNAME`参数传递你的用户名。如果没有提供用户名，这些命令会以代码1退出。

## 快速入门

```bash
# View your profile
./statsfm.py profile

# Top tracks this month
./statsfm.py top-tracks --limit 10

# Track stats for 2025
./statsfm.py track-stats 188745898 --start 2025 --end 2026
```

## 所有命令

### 用户个人信息
- `profile` - 显示用户名、代词、个人简介、Plus会员状态、时区以及Spotify同步信息

### 热门列表
- `top-tracks` - 你播放次数最多的歌曲
- `top-artists` - 你播放次数最多的艺术家
- `top-albums` - 你播放次数最多的专辑
- `top-genres` - 你最常收听的音乐类型

### 当前活动
- `now-playing`（别名：`now`、`np`） - 当前正在播放的歌曲
- `recent` - 最近播放的歌曲

### 详细统计信息
- `artist-stats <artist_id>` - 该艺术家的播放次数、收听时长及月度统计
- `track-stats <track_id>` - 该歌曲的播放次数、收听时长及月度统计（会显示歌曲名称和所属专辑）
- `album-stats <album_id>` - 该专辑的播放次数、收听时长及月度统计
- `stream-stats` - 你的整体流媒体播放统计（总播放次数、总时长、平均歌曲时长、最长/最短播放时长、歌曲/艺术家/专辑的独特播放次数）

### 查询
- `artist <artist_id>` - 艺术家信息及作品集。会显示音乐类型、粉丝数量、人气得分（100表示非常受欢迎，50表示小众，0表示无数据）。
  - `--type album|single|all`（默认：全部）
  - `--limit N` - 每个部分的显示条目数量（默认：15）

### 进一步查询
- `top-tracks-from-artist <artist_id>` - 该艺术家创作的热门歌曲
- `top-tracks-from-album <album_id>` - 该专辑的热门歌曲
- `top-albums-from-artist <artist_id>` - 该艺术家创作的热门专辑

### 全球排行榜
- `charts-top-tracks` - 全球热门歌曲排行榜
- `charts-top-artists` - 全球热门艺术家排行榜
- `charts-top-albums` - 全球热门专辑排行榜

### 搜索
- `search <query>` - 搜索艺术家、歌曲或专辑。使用`--type artist|track|album`来过滤结果

## 常用参数

### 时间范围
所有统计命令都支持预定义的时间范围和自定义时间范围：

**预定义时间范围：**
- `--range today` 或 `--range 1d` - 仅今天
- `--range 4w` - 过去4周
- `--range 6m` - 过去6个月
- `--range lifetime` 或 `--range all` - 全部时间

**自定义时间范围：**
- `--start YYYY` - 开始年份（例如：`--start 2025`
- `--start YYYY-MM` - 开始月份（例如：`--start 2025-07`
- `--start YYYY-MM-DD` - 开始日期（例如：`--start 2025-07-15`
- `--end YYYY[-MM[-DD]]` - 结束日期（格式相同）

**示例：**
```bash
# All of 2025
./statsfm.py top-artists --start 2025 --end 2026

# Just July 2025
./statsfm.py top-tracks --start 2025-07 --end 2025-08

# Q1 2025
./statsfm.py artist-stats 39118 --start 2025-01-01 --end 2025-03-31
```

### 细粒度
- `--granularity monthly` - 每月统计（默认）
- `--granularity weekly` - 每周统计（会显示周数和开始日期）
- `--granularity daily` - 每日统计（会显示日期和星期几）
- 适用于`artist-stats`、`track-stats`、`album-stats`命令

### 其他参数
- `--limit N` / `-l N` - 限制结果数量（默认：15）
- `--user USERNAME` / `-u USERNAME` - 指定要查询的stats.fm用户名
- `--no-album` - 在歌曲列表中隐藏专辑名称（默认会显示专辑名称）

## 使用示例

```bash
# Search for an artist, then drill down
./statsfm.py search "madison beer" --type artist
./statsfm.py artist-stats 39118 --start 2025
./statsfm.py top-tracks-from-artist 39118 --limit 20

# Weekly breakdown of a track
./statsfm.py track-stats 188745898 --start 2025 --end 2026 --granularity weekly

# Custom date range
./statsfm.py top-artists --start 2025-06 --end 2025-09

# Album tracklist and discography
./statsfm.py album 1365235
./statsfm.py artist-albums 39118 --type album

# Global charts
./statsfm.py charts-top-tracks --limit 20
```

## 输出格式

### 自动月度统计
统计命令（`artist-stats`、`track-stats`、`album-stats`）会自动显示：
- 总播放次数和总收听时长
- 每月的播放次数和时长统计

示例输出：
```
Total: 505 plays  (29h 53m)

Monthly breakdown:
  2025-02:   67 plays  (3h 52m)
  2025-03:  106 plays  (6h 21m)
  2025-04:   40 plays  (2h 24m)
  ...
```

### 显示信息
- **歌曲列表：** 显示歌曲排名、歌曲名称、艺术家名称、专辑名称（默认）、播放次数和时长
- **专辑列表：** 显示专辑排名、专辑名称、艺术家名称、播放次数和时长
- **艺术家列表：** 显示艺术家排名、艺术家名称、播放次数和时长、音乐类型
- **排行榜：** 显示全球排名及流媒体播放次数
- **最近播放的歌曲：** 显示播放时间戳、歌曲名称和艺术家名称（默认）

## Plus会员与免费用户的区别

- 需要Stats.fm Plus会员才能查看：
  - 热门列表中的播放次数
  - 收听时长（播放时长）
  - 详细统计信息

- 免费用户可以查看：
  - 排名/位置
  - 歌曲/艺术家/专辑名称
  - 当前播放的歌曲
  - 搜索功能
  - 月度统计信息（通过每日统计接口获取）

脚本会优雅地处理这些差异，对于缺失的数据会显示“[需要Plus会员]”的提示。

## API信息

**基础URL：** `https://api.stats.fm/api/v1`

**身份验证：** 公共查询无需身份验证

**响应格式：** JSON格式，数据以`item`（单个条目）或`items`（列表）的形式返回

**请求限制：** 请合理使用请求次数。在进行深度查询时，避免连续发送超过10次请求。

## 错误处理

所有错误都会输出到**stderr**，并导致程序以代码1退出。

| 错误情况 | stderr输出 | 处理方法 |
|----------|--------------|------------|
| 未设置用户 | `Error: No user specified.` | 使用`--user USERNAME`参数 |
| API错误（4xx/5xx） | `API Error (code): message` | 检查用户是否存在、个人资料是否公开或ID是否有效 |
| 连接失败 | `Connection Error: reason` | 稍后重试并检查网络连接 |
| 结果为空 | 无错误，但无输出 | 可能是因为用户设置了隐私设置，或者该时间段没有数据——尝试使用`--range lifetime` |
- 仅限Plus会员的数据 | 在结果中显示“[需要Plus会员]”的提示 | 优雅地告知用户并显示可用的信息 |

## 查找ID

使用搜索功能来查找艺术家/歌曲/专辑的ID：

```bash
# Find artist
./statsfm.py search "sabrina carpenter" --type artist
# Returns: [22369] Sabrina Carpenter [pop]

# Find track
./statsfm.py search "espresso" --type track
# Returns: [188745898] Espresso by Sabrina Carpenter

# Find album
./statsfm.py search "short n sweet" --type album
# Returns: [56735245] Short n' Sweet by Sabrina Carpenter
```

然后在其他命令中使用这些ID。

## 使用技巧

1. **使用自定义日期进行分析：** `--start 2025 --end 2026` 可查看全年的统计数据
2. **逐步探索：** 先搜索 → 获取ID → 查看详细统计 → 进一步深入查询
3. **比较不同时间段的数据：** 使用不同的时间范围运行相同的命令
4. **导出数据：** 将输出结果导出到文件：`./statsfm.py top-tracks --start 2025 > 2025_top_tracks.txt`
5. **专辑默认会显示名称：** 输出格式与stats.fm用户界面一致（专辑封面会突出显示）
6. **月度统计：** 所有统计命令都会自动显示每月的统计数据变化

## 适用于AI代理

**设置：** 检查系统内存中是否有stats.fm用户的用户名。如果没有，可以询问用户。所有涉及个人数据的命令都需要使用`--user USERNAME`参数。

**核心原则：** 将数据转化为有意义的见解。用户需要的是洞察力，而不仅仅是数据表格。帮助他们发现数据中的模式。

**务必查看多个时间范围的数据。** 仅查看“全部时间”的数据无法全面了解情况。请同时查看`--range today`、`7d`、`30d`、`4w`、`90d`和`lifetime`的时间范围，以了解用户喜好的变化。对于音乐类型和艺术家也是如此。单一的时间范围无法提供完整的信息。

### 查询示例

**“我想了解关于[艺术家]的信息”** → 先使用`search`搜索，然后使用`artist-stats`查看该艺术家的播放历史（包括首次发现的月份和最近几个月的播放情况）。`top-tracks-from-artist`可以显示用户持续关注的歌曲。
**“我的音乐品味是怎样的？”** → 使用`top-artists --range 7d`、`--range 30d`、`--range 90d`、`--range lifetime`来获取多个时间段的统计数据并进行比较。一个在当月排名外部的艺术家或音乐类型可能更具参考价值。
**“我最近在听什么？”** → 使用`now-playing`查看当前正在播放的歌曲；使用`recent --limit 15`查看最近一段时间的播放记录，以了解用户的音乐偏好。
**关于专辑的问题：** 使用`album`获取专辑曲目列表；使用`album-stats`查看收听历史；月度统计可以显示用户的长期喜好变化。

### 时间范围示例

- “今年” → `--start 2025 --end 2026`
- “去年夏天” → `--start 2025-06 --end 2025-09`
- “我是什么时候发现X的？” → `artist-stats <id> --range lifetime`（查看首次发现的月份）

### 数据解读技巧

- **一个月内播放超过200次** = 表示用户对该歌曲有持续的兴趣
- **首次出现** = 表示用户发现了该歌曲
- **播放次数突然下降** = 可能表示用户已经转移了兴趣
- **最近播放列表中出现的老歌** = 可能表示用户重新发现了这首歌或对该歌曲有怀旧情绪
- **某首歌的播放次数是其他歌曲的5倍** = 这首歌可能是用户的经典歌曲

**注意数据的实际含义：** “30小时的播放量”并不意味着每天实际播放30小时，而是指在这30天内的累计播放次数。

### 命令参考

| 功能 | 命令 | 关键参数 |
|--------|---------|-----------|
| 查看某首歌曲的播放情况 | `track-stats <id>` | `--start/--end`, `--granularity` |
| 查看某位艺术家的播放情况 | `artist-stats <id>` | `--start/--end`, `--granularity` |
| 查看某张专辑的播放情况 | `album-stats <id>` | `--start/--end`, `--granularity` |
| 查看整体播放情况 | `stream-stats` | `--range`, `--start/--end` |
| 查看排名 | `top-tracks`, `top-artists`, `top-albums`, `top-genres` | `--range`, `--start/--end`, `--limit` |
| 查看当前正在播放的歌曲 | `now-playing` | |
| 查看最近播放的歌曲 | `recent` | `--limit` |
| 查看艺术家信息 | `artist <id>` | `--limit` |
- 查看艺术家的作品集 | `artist-albums <id>` | `--limit` |
- 查看专辑的曲目列表 | `album <id>` | |
- 查看某位艺术家创作的热门歌曲 | `top-tracks-from-artist <id>` | `--range`, `--limit` |
- 查看某张专辑的热门歌曲 | `top-tracks-from-album <id>` | `--range`, `--limit` |
- 查看某位艺术家创作的热门专辑 | `top-albums-from-artist <id>` | `--range`, `--limit` |
- 查看全球排行榜 | `charts-top-tracks`, `charts-top-artists`, `charts-top-albums` | `--range`, `--limit` |
- 查找ID | `search <query>` | `--type artist\|track\|album` |

### 特殊情况处理

- **免费用户：** 热门歌曲的播放次数无法查看——但排名和统计信息仍然可用 |
- **结果为空：** 尝试使用`--range lifetime`作为备用方案。也可能是用户设置了隐私设置。
- **搜索结果重复：** 使用第一个搜索结果
- **Apple Music数据：** 功能尚未测试，可能存在数据缺失的情况

## 参考资料
- Github仓库：[statsfm/statsfm-cli](https://github.com/Beat-YT/statsfm-cli)
- API接口文档：[references/api.md]
- 官方JavaScript客户端：[statsfm/statsfm.js](https://github.com/statsfm/statsfm.js)