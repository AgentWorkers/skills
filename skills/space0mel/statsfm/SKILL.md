---
name: statsfm
description: 这款音乐数据工具基于 stats.fm API 运行，支持查询专辑曲目列表、艺术家作品集以及全球音乐排行榜。使用 stats.fm 的用户名，用户还可以查看个人听歌历史、歌曲播放次数、热门艺术家/曲目/专辑的排名情况、每月的播放数据，以及当前正在播放的音乐内容。
---
# stats.fm CLI

这是一个全面的Python命令行工具（CLI），用于查询stats.fm API（Spotify的收听分析数据）。

**系统要求：** 需要Python 3.6及以上版本（仅需要标准库，无需安装pip）。

**脚本位置：** 位于该工具目录下的`scripts/statsfm.py`文件。示例中使用了`./statsfm.py`，假设你位于`scripts`文件夹中。

## 先决条件

**Stats.fm账户（免费）**
- 如果还没有账户？请访问[stats.fm](https://stats.fm)并使用Spotify或Apple Music注册（Apple Music的功能尚未测试，Plus会员状态未知）。
- 如果已经拥有账户，请从个人资料中复制用户名。
- 该工具支持Spotify和Apple Music的数据查询。

## 设置

使用`--user USERNAME`或`-u USERNAME`参数传递你的用户名。如果没有提供用户名，脚本将以代码1退出。

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

### 用户资料
- `profile` - 显示用户资料和stats.fm会员信息

### 热门榜单
- `top-tracks` - 用户播放次数最多的歌曲
- `top-artists` - 用户播放次数最多的艺术家
- `top-albums` - 用户播放次数最多的专辑
- `top-genres` - 用户最常收听的音乐流派

### 当前活动
- `now-playing`（别名：`now`、`np`） - 当前正在播放的歌曲
- `recent` - 最近播放的歌曲

### 详细统计
- `artist-stats <artist_id>` - 指定艺术家的详细统计信息（包含月度数据）
- `track-stats <track_id>` - 指定歌曲的详细统计信息（包含月度数据）
- `album-stats <album_id>` - 指定专辑的详细统计信息（包含月度数据）
- `stream-stats` - 总体流媒体播放统计

### 查询
- `album <album_id>` - 专辑信息及完整曲目列表（发布日期、唱片公司、流派、歌曲及其时长和[E]标签）
- `artist-albums <artist_id>` - 艺术家的所有专辑/单曲，按类型分类（专辑、单曲和EP，最新作品优先显示）。默认每个类别显示15条记录，超过数量时显示“(N more)”。
  - `--type album|single|all`（默认：全部）
  - `--limit N` - 每个类别的显示条数

### 进一步查询
- `top-tracks-from-artist <artist_id>` - 指定艺术家的热门歌曲
- `top-tracks-from-album <album_id>` - 指定专辑的热门歌曲
- `top-albums-from-artist <artist_id>` - 指定艺术家的热门专辑

### 全球排行榜
- `charts-top-tracks` - 全球热门歌曲排行榜
- `charts-top-artists` - 全球热门艺术家排行榜
- `charts-top-albums` - 全球热门专辑排行榜

### 搜索
- `search <query>` - 搜索艺术家、歌曲或专辑

## 常用参数

### 时间范围
所有统计命令都支持预定义的时间范围和自定义时间范围：

**预定义时间范围：**
- `--range today` - 仅今天
- `--range weeks` - 过去4周（默认）
- `--range months` - 过去6个月
- `--range lifetime` - 全部时间

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

### 其他参数
- `--limit N` / `-l N` - 限制结果数量（默认：15条）
- `--user USERNAME` / `-u USERNAME` - 指定要查询的stats.fm用户名
- `--no-album` - 在歌曲列表中隐藏专辑名称（默认显示专辑名称）

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
- 总播放次数和总播放时长
- 每个月的播放次数和时长统计

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
- **艺术家列表：** 显示艺术家排名、艺术家名称、播放次数和时长、流派
- **排行榜：** 显示全球排名和播放次数
- **最近播放的歌曲：** 显示播放时间戳、歌曲名称和艺术家名称（默认）

## Plus会员与免费用户的区别

**需要Stats.fm Plus会员才能获取：**
- 热门榜单中的播放次数
- 收听时长（播放总时长）
- 详细统计信息

**免费用户可以获取：**
- 排名/位置信息
- 歌曲/艺术家/专辑名称
- 当前正在播放的歌曲
- 搜索功能
- 月度统计信息（通过每日统计接口获取）

脚本会优雅地处理这些差异，对于缺失的数据会显示“[需要Plus会员]”。

## API信息

**基础URL：** `https://api.stats.fm/api/v1`

**认证：** 公共账户无需认证

**响应格式：** JSON格式，数据以`item`（单个条目）或`items`（列表）的形式返回

**请求限制：** 请合理使用请求频率。在进行深度查询时，避免连续发送超过10次请求。

## 错误处理

所有错误都会输出到**stderr**，并导致脚本以代码1退出。

| 错误情况 | 输出内容 | 处理方法 |
|----------|--------------|------------|
| 未设置用户 | `Error: No user specified.` | 使用`--user USERNAME`参数 |
| API错误（4xx/5xx） | `API Error (code): message` | 检查用户是否存在、个人资料是否公开或ID是否有效 |
| 连接失败 | `Connection Error: reason` | 稍后重试并检查网络连接 |
| 结果为空 | 无错误，但无输出 | 可能是因为用户设置了隐私设置，或者该时间段没有数据——尝试使用`--range lifetime` |
| 仅限Plus会员的数据 | 直接显示“[需要Plus会员]” | 优雅地告知用户并显示可用的信息 |

## 查找ID

使用搜索功能查找艺术家/歌曲/专辑的ID：

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

1. **使用自定义时间范围进行分析：** 使用`--start 2025 --end 2026`查看全年的统计数据
2. **逐步探索：** 先搜索 → 获取ID → 查看详细统计 → 进一步查询
3. **比较不同时间段的数据：** 使用不同的时间范围运行相同的命令
4. **导出数据：** 将输出结果导出到文件：`./statsfm.py top-tracks --start 2025 > 2025_top_tracks.txt`
5. **专辑默认显示方式：** 与stats.fm的用户界面显示方式一致（专辑封面会突出显示）
6. **月度统计：** 所有统计命令都会自动显示每月的统计数据变化

## 适用于AI代理

### 设置

检查系统中是否存储了stats.fm用户名。如果没有，请询问用户。所有涉及用户数据的命令都需要`--user USERNAME`参数。

### 该工具的用途

该工具允许你直接查看某人的音乐收听历史。这涉及个人隐私。其价值不在于简单地展示数据，而在于帮助用户了解自己之前不知道的信息。

当有人询问他们的音乐喜好时，他们并不是在请求数据库查询结果，而是希望了解自己的音乐品味、回顾过去的经历或发现某种模式。你的任务是将这些数据转化为有意义的信息。

### 使用建议

**当有人提到某位艺术家时：** 了解他们与这位艺术家的关系——他们听了这位艺术家多久了，是在哪个时期发现的这位艺术家，哪些歌曲让他们印象深刻。使用`search` → `artist-stats`来了解这些信息，`top-tracks-from-artist`可以展示哪些歌曲让他们产生共鸣，`artist-albums`可以提供该艺术家的完整作品列表。不要只是列出所有内容，先阅读第一个结果，再决定哪些内容值得深入探究。

**当有人询问他们的音乐品味时：** 他们需要的是一个直观的展示，而不仅仅是数据表格。`top-artists`和`top-genres`可以帮助他们了解自己的音乐品味是如何变化的。比较不同时间范围的查询结果（`--range weeks`、`--range months`、`--range lifetime`），其中的差异会揭示很多信息。例如，某首歌在历史上排名第一，但本月却不在前20名中，这可能很有意思。

**当有人提到某张专辑时：** 他们可能想了解这张专辑或回忆起关于它的信息。`album`可以提供专辑的曲目列表和元数据。如果用户也有收听数据，`album-stats`可以显示他们何时以及播放了多少次。月度统计可以揭示这种喜好是短暂的热潮还是长期的兴趣。

**当有人询问他们正在听什么时：** `now-playing`可以直接给出答案。但`recent`命令可以显示最近10-15首歌曲，帮助了解当前的播放氛围。如果存在某种模式（比如总是播放同一位艺术家或同一流派的歌曲），请注意这一点。

### 时间范围的转换

当用户提供时间范围时，按以下方式转换：
- “今年” → `--start 2025 --end 2026`
- “去年夏天” → `--start 2025-06 --end 2025-09`
- “我是什么时候开始听X的？” → 使用`artist-stats <id>`并设置`--range lifetime`——月度统计可以显示开始听这首歌的月份

### 数据解读

数字本身蕴含着信息：
- 如果某个月份的播放次数超过200次，说明这位艺术家在用户的音乐生活中占有重要地位。
- 如果某首歌首次出现在月度统计中，说明用户是在那个月份发现这位艺术家的。
- 如果播放次数突然下降，可能是因为新的喜好取代了它，或者用户已经转向了其他音乐。
- 如果最近播放的歌曲中包含多年前的老歌，可能是出于怀旧或重新发现的原因。
- 如果某首歌的播放次数是其他歌曲的5倍，那么这很可能就是用户最喜欢的歌曲。

**注意报告方式：** “你播放了847首歌”这样的数字没有实际意义。而“你在3月份听了Madison Beer 30个小时——相当于每天听一个小时”则能传达更多信息。

### 命令参考

| 功能 | 命令 | 关键参数 |
|--------|---------|-----------|
| 查看歌曲的播放次数 | `track-stats <id>` | `--start/--end`, `--granularity` |
| 查看艺术家的播放次数 | `artist-stats <id>` | `--start/--end`, `--granularity` |
| 查看排行榜 | `top-tracks`, `top-artists`, `top-albums`, `top-genres` | `--range`, `--start/--end`, `--limit` |
| 查看当前正在播放的歌曲 | `now-playing` | |
| 查看最近播放的歌曲 | `recent` | `--limit` |
- 查看艺术家的作品列表 | `artist-albums <id>` | `--limit` |
- 查看专辑的曲目列表 | `album <id>` | |
- 查看艺术家的热门歌曲 | `top-tracks-from-artist <id>` | `--range`, `--limit` |
- 查看专辑的热门歌曲 | `top-tracks-from-album <id>` | `--range`, `--limit` |
- 查看艺术家的热门专辑 | `top-albums-from-artist <id>` | `--range`, `--limit` |
- 查看全球排行榜 | `charts-top-tracks`, `charts-top-artists`, `charts-top-albums` | `--range`, `--limit` |
- 查找ID | `search <query>` | `--type artist\|track\|album` |
- 查看总体统计 | `stream-stats` | `--range`, `--start/--end` |

### 特殊情况处理**
- **免费用户：** 热门歌曲的播放次数无法获取，但排名和统计信息仍然可用 |
- **结果为空：** 尝试使用`--range lifetime`作为备用方案。也可能是用户设置了隐私设置。
- **搜索结果重复：** 使用第一个结果。
- **Apple Music数据：** 功能尚未测试，可能存在数据缺失的情况。

## 参考资料
- Github仓库：[statsfm/statsfm-cli](https://github.com/Beat-YT/statsfm-cli)
- API接口文档：[references/api.md]
- 官方JavaScript客户端：[statsfm/statsfm.js](https://github.com/statsfm/statsfm.js)