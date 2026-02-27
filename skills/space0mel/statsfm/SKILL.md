---
name: statsfm
description: 通过公开的 REST API 查询 stats.fm（Spotify 的收听统计信息）。该 API 提供音乐收听数据、Spotify 统计信息、热门艺术家/曲目/专辑、当前正在播放的音乐、流媒体播放历史、音乐类型分布以及音乐品味分析。对于公开账号而言，无需进行身份验证即可使用该 API。
---
# stats.fm CLI

这是一个全面的Python命令行工具（CLI），用于查询stats.fm API（Spotify的收听数据分析服务）。

**系统要求：** Python 3.6及以上版本（仅需要标准库，无需安装pip）。

**脚本位置：** 位于本技能目录下的`scripts/statsfm.py`文件。示例中使用的命令为`./statsfm.py`，假设你位于`scripts`文件夹中。

## 先决条件

**Stats.fm账户（免费）**
- 如果还没有账户？请访问[stats.fm](https://stats.fm)并使用Spotify或Apple Music注册（Apple Music功能尚未测试，Plus会员状态未知）。
- 如果已有账户，请复制你的用户名。

**支持的音乐平台：** Spotify和Apple Music。

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

### 用户信息
- `profile` - 显示用户个人信息和stats.fm会员信息

### 热门榜单
- `top-tracks` - 你播放次数最多的歌曲
- `top-artists` - 你播放次数最多的艺术家
- `top-albums` - 你播放次数最多的专辑
- `top-genres` - 你最常收听的音乐类型

### 当前播放内容
- `now-playing`（别名：`now`、`np`） - 当前正在播放的歌曲
- `recent` - 最近播放的歌曲

### 详细统计
- `artist-stats <artist_id>` - 指定艺术家的详细统计信息（包含月度数据）
- `track-stats <track_id>` - 指定歌曲的详细统计信息（包含月度数据）
- `album-stats <album_id>` - 指定专辑的详细统计信息（包含月度数据）
- `stream-stats` - 总体流媒体播放统计

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
- `--limit N` / `-l N` - 限制结果数量（默认值因命令而异）
- `--user USERNAME` / `-u USERNAME` - 指定要查询的stats.fm用户名
- `--no-album` - 在歌曲列表中隐藏专辑名称（默认显示专辑名称）

## 使用示例

### 基本查询
```bash
# Your top 10 tracks this week (default range)
./statsfm.py top-tracks --limit 10

# Top 10 artists of all time
./statsfm.py top-artists --range lifetime --limit 10

# What's playing now
./statsfm.py now-playing

# Last 15 tracks played
./statsfm.py recent --limit 15
```

### 使用预定义时间范围
```bash
# Today's top tracks
./statsfm.py top-tracks --range today --limit 20

# Last 4 weeks top artists
./statsfm.py top-artists --range weeks --limit 10

# Last 6 months top albums
./statsfm.py top-albums --range months --limit 15

# All-time top genres
./statsfm.py top-genres --range lifetime --limit 10
```

### 自定义时间范围
```bash
# How many times did I listen to Espresso in 2025?
./statsfm.py track-stats 188745898 --start 2025 --end 2026

# My top artists in summer 2025
./statsfm.py top-artists --start 2025-06 --end 2025-09

# Sabrina Carpenter stats for Q2 2025
./statsfm.py artist-stats 22369 --start 2025-04 --end 2025-07
```

### 详细查询
```bash
# Search for Madison Beer
./statsfm.py search "madison beer" --type artist
# Returns: [39118] Madison Beer [pop]

# Get her detailed stats with monthly breakdown
./statsfm.py artist-stats 39118 --start 2025

# See your top tracks from her
./statsfm.py top-tracks-from-artist 39118 --limit 20

# Check a specific album's stats
./statsfm.py album-stats 16211936 --start 2025
```

### 排行榜查询
```bash
# What's hot globally today?
./statsfm.py charts-top-tracks --limit 20

# Top albums over the last 6 months
./statsfm.py charts-top-albums --range months --limit 15

# Top artists this week
./statsfm.py charts-top-artists --range weeks
```

### 隐藏专辑名称
```bash
# Compact view without album names
./statsfm.py top-tracks --no-album --limit 10
./statsfm.py recent --no-album
```

## 输出格式

### 自动月度统计
`artist-stats`、`track-stats`、`album-stats`等统计命令会自动显示：
- 总播放次数和总播放时长
- 每个月的播放次数和时长分布

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
- **歌曲列表：** 显示歌曲排名、歌曲名称、艺术家名称、专辑名称（默认显示）、播放次数和播放时长
- **专辑列表：** 显示专辑排名、专辑名称、艺术家名称、播放次数和播放时长
- **艺术家列表：** 显示艺术家排名、艺术家名称、播放次数、播放时长和音乐类型
- **排行榜：** 显示包含流媒体播放次数的全球排名
- **最近播放的歌曲：** 显示播放时间戳、歌曲名称和艺术家名称（默认显示）

## Plus会员与免费用户的区别

**需要Stats.fm Plus会员才能查看：**
- 热门榜单中的播放次数
- 收听时长（播放总时长）
- 详细统计信息

**免费用户可以查看：**
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

**请求限制：** 请合理使用请求，避免连续快速发送超过10次请求。

## 错误处理

所有错误都会输出到**stderr**，并导致脚本以代码1退出。

| 错误情况 | 输出信息 | 处理方法 |
|----------|--------------|------------|
| 未设置用户 | `Error: No user specified.` | 使用`--user USERNAME`参数 |
| API错误（4xx/5xx） | `API Error (code): message` | 检查用户是否存在、个人资料是否公开或ID是否有效 |
| 连接失败 | `Connection Error: reason` | 稍后重试或检查网络连接 |
| 结果为空 | 无错误提示，但无输出 | 可能是因为用户账户为私密账户或该时间段没有数据——尝试使用`--range lifetime` |
| 仅限Plus会员的数据 | 显示“[需要Plus会员]”提示 | 优雅地告知用户并显示可用的信息 |

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

1. **使用自定义时间范围进行分析：** `--start 2025 --end 2026` 可查看全年的统计数据
2. **逐步查询：** 先搜索 → 获取ID → 查看详细统计 → 进一步查询
3. **比较不同时间段的数据：** 使用不同的时间范围运行相同命令
4. **导出数据：** 将输出结果导出到文件：`./statsfm.py top-tracks --start 2025 > 2025_top_tracks.txt`
5. **专辑名称的显示方式：** 与stats.fm的UI显示方式一致（专辑封面会显示在列表中）
6. **月度统计：** 所有统计命令都会自动显示每月的统计数据

## 适用于AI代理的提示

### 快速参考 — 意图 → 命令

| 用户需求 | 命令 | 关键参数 |
|-----------|---------|-----------|
| 查看某首歌曲的播放次数 | `track-stats <id>` | `--start/--end` 指定时间范围 |
| 查看某位艺术家的播放次数 | `artist-stats <id>` | `--start/--end` 指定时间范围 |
| 查看排行榜 | `top-tracks`、`top-artists`、`top-albums`、`top-genres` | `--range` 或 `--start/--end`、`--limit` |
| 查看当前正在播放的歌曲 | `now-playing` | |
| 查看最近播放的歌曲 | `recent` | `--limit` |
| 查看播放历史 | `artist-stats` 或 `track-stats` | 自动显示月度统计 |
| 查找艺术家/歌曲/专辑的ID | `search <query>` | `--type artist\|track\|album` |
| 详细查询艺术家信息 | `search` → `artist-stats` → `top-tracks-from-artist` | 连续使用多个命令 |
| 查看全球排行榜 | `charts-top-tracks`、`charts-top-artists` | `--range`、`--limit` |

### 首次使用前的注意事项

1. 检查系统中是否已保存用户用户名
2. 如果没有找到用户名，请求用户提供stats.fm用户名
3. 根据需要通过`--user USERNAME`参数传递用户名

## 工作流程示例

1. **探索 → 详细查询：** 先搜索 → 获取ID → 查看艺术家详细信息 → 查看热门歌曲
2. **时间线分析：** 使用统计命令的月度统计数据追踪播放趋势
3. **对比不同时间段的数据：** 使用不同的时间范围运行相同命令以观察变化
4. **检测变化趋势：** 查看每月的统计数据，发现播放次数的突然波动（可能表示新专辑发布）

## 最佳实践

- 使用自定义时间范围（`--start/--end`）以获取更精确的数据
- 当用户询问“今年”或特定年份时，使用`--start YYYY --end YYYY+1`
- 统计命令会自动显示月度统计数据，可用于识别高峰和趋势
- 始终先使用`search`命令获取ID，避免手动记忆或硬编码ID
- 歌曲列表中默认会显示专辑名称，如需简洁输出可使用`--no-album`参数

## 数据解读技巧

- **常见模式：**
  - **持续高播放量：** 多个月份内播放次数持续较高
  - **波动：** 播放次数突然增加或减少，通常表示新专辑发布或音乐趋势变化
  - **替代现象：** 一位艺术家的数据下降，另一位艺术家的数据上升，可能表示听众喜好变化
  - **经典作品：** 旧专辑的歌曲出现在最近的热门榜单中，说明用户正在探索更多作品
  - **入门曲目：** 时间线中的首支歌曲可能引导用户发现新的艺术家

## 数据展示方式

- 在月度统计数据中突出显示高峰和趋势
- 将分钟数转换为小时数进行对比
- 在适当的情况下，对比不同时间段的数据变化
- 强调显著的数据点，如单月播放次数的异常高值或快速增长

## 特殊情况处理

- 免费用户查看数据时，如果显示“[需要Plus会员]”，请优雅地告知用户并显示可用的信息
- 有时搜索结果可能重复，请使用第一个结果
- 如果结果为空，可能是用户账户为私密账户或该时间段没有数据，可以尝试使用`--range lifetime`
- Apple Music功能尚未测试

## 贡献方式

如果发现错误或希望添加新命令，请在[https://github.com/Beat-YT/statsfm-cli](https://github.com/Beat-YT/statsfm-cli)提交问题或Pull Request。

## 参考资料

- API接口：[references/api.md](references/api.md)
- 官方JavaScript客户端：[statsfm/statsfm.js](https://github.com/statsfm/statsfm.js)