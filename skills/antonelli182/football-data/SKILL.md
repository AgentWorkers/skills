---
name: football-data
description: >
  **足球（Soccer）数据：涵盖13个联赛的实时信息**  
  - 联赛排名  
  - 赛程安排  
  - 比赛统计数据  
  - 净胜球（xG）  
  - 球员转会信息  
  - 球员档案  
  **使用场景：**  
  当用户询问足球联赛的排名、赛程、比赛数据、净胜球、球员阵容、球员价值、转会信息、伤病动态、联赛积分榜或球员档案时，可使用该数据源。  
  **不适用场景：**  
  - 当用户询问美式橄榄球（NFL）、大学橄榄球（CFB）、NBA、WNBA、大学篮球（CBB）、NHL、MLB、网球（Tennis）、高尔夫（Golf）、F1赛事或博彩赔率时，请使用相应的数据源。  
  - 该数据源不提供实时比分更新（数据更新发生在比赛结束后）。  
  - 对于非英超联赛（Premier League、La Liga、Bundesliga、Serie A、Ligue 1），`get_season_leaders` 和 `get_missing_players` 方法将返回空结果。  
  - 对于排名不在前五的联赛，`get_event_xG` 方法也无法提供有效数据。
license: MIT
metadata:
  author: machina-sports
  version: "0.1.0"
---
# 足球数据

## 设置

在首次使用之前，请检查命令行界面（CLI）是否可用：
```bash
which sports-skills || pip install sports-skills
```
如果 `pip install` 失败（包未找到或 Python 版本错误），请从 GitHub 安装：
```bash
pip install git+https://github.com/machina-sports/sports-skills.git
```
该软件包需要 Python 3.10 或更高版本。如果您的默认 Python 版本较低，请使用特定版本：
```bash
python3 --version  # check version
# If < 3.10, try: python3.12 -m pip install sports-skills
# On macOS with Homebrew: /opt/homebrew/bin/python3.12 -m pip install sports-skills
```
无需 API 密钥。

## 快速入门

推荐使用 CLI，因为它可以避免 Python 导入路径的问题：
```bash
sports-skills football get_daily_schedule
sports-skills football get_season_standings --season_id=premier-league-2025
```

Python SDK（替代方案）：
```python
from sports_skills import football

standings = football.get_season_standings(season_id="premier-league-2025")
schedule = football.get_daily_schedule()
```

## 选择赛季

从系统提示的日期中获取当前年份（例如，`currentDate: 2026-02-16` → 当前年份为 2026）。

- **如果用户指定了一个赛季**，则直接使用该赛季。
- **如果用户输入“current”、“latest”或未指定任何内容**：调用 `get_current_season(competition_id="...")` 来获取活跃的赛季 ID。切勿猜测或硬编码年份。
- **赛季格式**：始终使用 `{league-slug}-{year}`（例如，`"premier-league-2025"` 表示 2025-26 赛季）。年份是赛季的开始年份，而不是结束年份。
- **MLS 的特殊情况**：MLS 的赛季在同一个日历年内分为春季和秋季。请使用 `get_current_season(competition_id="mls")` — 不要假设 MLS 遵循欧洲的日历。
- **切勿硬编码赛季 ID**。始终通过 `get_current_season()` 或系统日期来获取赛季 ID。

## 各联赛的数据覆盖范围

并非所有数据都适用于所有联赛。请使用正确的命令来获取相应联赛的数据。

| 命令 | 所有 13 个联赛 | 仅限前 5 个联赛 | 仅限英超联赛 |
|---------|:-:|:-:|:-:|
| get_season_standings | x | | |
| get_daily_schedule | x | | |
| get_season_schedule | x | | |
| get_season_teams | x | | |
| search_team | x | | |
| get_team_schedule | x | | |
| get_team_profile | x | | |
| get_event_summary | x | | |
| get_event_lineups | x | | |
| get_event_statistics | x | | |
| get_event_timeline | x | | |
| get_current_season | x | | |
| get_competitions | x | | |
| get_event_xg | | x | |
| get_event_players_statistics (with xG) | | x | |
| get_season_leaders | | | x |
| get_missing_players | | | x |

**前 5 个联赛**（Understat 数据源）：英超联赛（EPL）、西甲联赛（La Liga）、德甲联赛（Bundesliga）、意甲联赛（Serie A）、法甲联赛（Ligue 1）。
**仅限英超联赛**（FPL 数据源）：提供英超联赛的伤病新闻、球员数据、球队所有权信息以及 ICT 指数。
**所有联赛**：通过 ESPN 提供比分、积分榜、赛程、比赛摘要、阵容等信息。
**Transfermarkt**：可以查询任何具有 `tm_player_id` 的球员的转会市场信息（包括市场价值和转会历史）。

**注意**：MLS 的赛季结构不同（采用春季-秋季日历）。请使用 `get_current_season(competition_id="mls")` 来获取正确的赛季 ID。

## ID 规范

- **season_id**：`{league-slug}-{year}`，例如 `"premier-league-2025"`、`"la-liga-2025"`
- **competition_id**：联赛名称，例如 `"premier-league"`、`"serie-a"`、`"champions-league"`
- **team_id**：ESPN 的球队 ID（数字字符串），例如 `"359"`（阿森纳）、`"86"`（皇家马德里）
- **event_id**：ESPN 的赛事 ID（数字字符串），例如 `"740847"`
- **fpl_id**：FPL 的球员 ID 或代码（仅限英超联赛）
- **tm_player_id**：Transfermarkt 的球员 ID，例如 `"433177"`（萨卡）、`342229`（姆巴佩）

## 命令

### get_current_season
获取某个联赛的当前赛季信息。适用于所有联赛。
- `competition_id`（字符串，必需）：联赛名称

返回 `data.competition` 和 `data.season`：
```json
{"competition": {"id": "premier-league", "name": "Premier League"}, "season": {"id": "premier-league-2025", "name": "2025-26 English Premier League", "year": "2025"}}
```

### get_competitions
列出所有可用的联赛及其当前赛季信息。无需参数。适用于所有联赛。

返回 `data.competitions[]`，其中包含 `id`、`name`、`code`、`current_season`。

### get_competition_seasons
获取某个联赛的所有可用赛季信息。适用于所有联赛。
- `competition_id`（字符串，必需）：联赛名称

### get_season_schedule
获取某个联赛的完整赛季赛程信息。适用于所有联赛。
- `season_id`（字符串，必需）：赛季名称（例如，`"premier-league-2025"`）

返回 `data.schedules[]`，其结构与下面的事件数据相同。

### get_season_standings
获取某个赛季的联赛积分榜。适用于所有联赛。
- `season_id`（字符串，必需）：赛季名称

返回 `data.standings[].entries[]`：
```json
{
  "position": 1,
  "team": {"id": "359", "name": "Arsenal", "short_name": "Arsenal", "abbreviation": "ARS", "crest": "https://..."},
  "played": 26, "won": 17, "drawn": 6, "lost": 3,
  "goals_for": 50, "goals_against": 18, "goal_difference": 32, "points": 57
}
```

### get_season_leaders
获取某个赛季的得分最高的球员/领先者（仅限英超联赛，通过 FPL 数据源）。
- `season_id`（字符串，必需）：赛季名称（必须是 `premier-league-*`）

返回 `data.leaders[]` — 注意：球员名称嵌套在 `.player.name` 中：
```json
{
  "player": {"id": "223094", "name": "Erling Haaland", "first_name": "Erling", "last_name": "Haaland", "position": "Forward"},
  "team": {"id": "43", "name": "Man City"},
  "goals": 22, "assists": 6, "penalties": 0, "played_matches": 25
}
```
对于非英超联赛，此命令将返回空结果。

### get_season_teams
获取某个赛季的所有球队信息。适用于所有联赛。
- `season_id`（字符串，必需）：赛季名称

### search_team
根据名称在所有联赛中搜索球队（或特定联赛）。支持模糊匹配。
- `query`（字符串，必需）：要搜索的球队名称（例如，“Corinthians”、“Barcelona”、“Man Utd”）
- `competition_id`（字符串，可选）：将搜索范围限制在某个联赛（例如，“serie-a-brazil”、“premier-league”）

返回 `data.results[]`，其中包含每场比赛的 `team`、`competition` 和 `season`：
```json
{"team": {"id": "874", "name": "Corinthians"}, "competition": {"id": "serie-a-brazil", "name": "Serie A Brazil"}, "season": {"id": "serie-a-brazil-2025", "year": "2025"}}
```

### get_team_profile
获取球队的基本信息（名称、队徽、主场）。**不返回球队阵容** — 请使用 `get_season_leaders` 获取英超联赛球员的 ID，然后使用 `get_player_profile` 获取球员的详细信息。
- `team_id`（字符串，必需）：ESPN 的球队 ID
- `league_slug`（字符串，可选）：联赛名称（有助于更快地找到相关数据）

返回 `data.team` 和 `data.venue`。`data.players[]` 为空 — 请参考下面的“深入分析英超球队”示例以了解推荐的工作流程。

### get_daily_schedule
获取指定日期的所有比赛信息（涵盖所有联赛）。
- `date`（字符串，可选）：日期格式为 YYYY-MM-DD。默认为今天。

返回 `data.date` 和 `data.events[]`：
```json
{
  "id": "748381", "status": "not_started", "start_time": "2026-02-16T20:00Z",
  "competition": {"id": "la-liga", "name": "La Liga"},
  "season": {"id": "la-liga-2025", "year": "2025"},
  "venue": {"name": "Estadi Montilivi", "city": "Girona"},
  "competitors": [
    {"team": {"id": "9812", "name": "Girona", "abbreviation": "GIR"}, "qualifier": "home", "score": 0},
    {"team": {"id": "83", "name": "Barcelona", "abbreviation": "BAR"}, "qualifier": "away", "score": 0}
  ],
  "scores": {"home": 0, "away": 0}
}
```
状态值：`"not_started"`、`"live"`、`"halftime"`、`"closed"`、`"postponed"`。

### get_event_summary
获取比赛摘要及比分。适用于所有联赛。
- `event_id`（字符串，必需）：比赛/赛事 ID

返回 `data.event`（其结构与每日赛程数据相同）。

### get_event_lineups
获取比赛阵容。适用于所有联赛（前提是 ESPN 提供相关数据）。
- `event_id`（字符串，必需）：比赛/赛事 ID

返回 `data.lineups[]`：
```json
{
  "team": {"id": "364", "name": "Liverpool", "abbreviation": "LIV"},
  "qualifier": "home",
  "formation": "4-3-3",
  "starting": [{"id": "275599", "name": "Caoimhín Kelleher", "position": "Goalkeeper", "shirt_number": 1}],
  "bench": [{"id": "...", "name": "...", "position": "...", "shirt_number": 62}]
}
```

### get_event_statistics
获取比赛的球队统计数据。适用于所有联赛。
- `event_id`（字符串，必需）：比赛/赛事 ID

返回 `data.teams[]`：
```json
{
  "team": {"id": "244", "name": "Brentford"},
  "qualifier": "home",
  "statistics": {"ball_possession": "40.8", "shots_total": "10", "shots_on_target": "3", "fouls": "12", "corners": "4"}
}
```

### get_event_timeline
获取比赛的时间线及关键事件（进球、黄牌、换人）。适用于所有联赛。
- `event_id`（字符串，必需）：比赛/赛事 ID

返回 `datatimeline[]`，其中包含进球、黄牌和换人等事件。

### get_team_schedule
获取特定球队的赛程信息（包括过去的结果和未来的比赛安排）。适用于所有联赛。
- `team_id`（字符串，必需）：ESPN 的球队 ID
- `league_slug`（字符串，可选）：联赛名称（有助于更快地找到相关数据）
- `season_year`（字符串，可选）：赛季年份筛选条件
- `competition_id`（字符串，可选）：将结果筛选为某个特定联赛（例如，“serie-a-brazil”、“premier-league”）

### get_head_to_head
**不可用** — 需要授权数据。不要调用此命令；它将返回空结果。建议使用 `get_team_schedule` 分别获取两支球队的赛程信息，然后手动筛选重叠的比赛。
- `team_id`（字符串，必需）：第一支球队的 ID
- `team_id_2`（字符串，必需）：第二支球队的 ID

### get_event_xg
从 Understat 获取预期进球（xG）数据（仅限前 5 个联赛）：英超联赛（EPL）、西甲联赛（La Liga）、德甲联赛（Bundesliga）、意甲联赛（Serie A）。其他联赛将返回空结果。
- `event_id`（字符串，必需）：比赛/赛事 ID

返回 `data.teams[]` 和 `data.shots[]`：
```json
{"team": {"id": "244", "name": "Brentford"}, "qualifier": "home", "xg": 1.812}
```
`data.shots[]` 包含每粒进球的 xG 数据。注意：最近的比赛（过去 24-48 小时内的比赛）可能尚未在 Understat 中被索引。

### get_event_players_statistics
获取球员的赛事级统计数据，并包含 xG 信息。适用于所有联赛（ESPN 提供的基本统计数据）。仅在前 5 个联赛（EPL、La Liga、Bundesliga、Serie A）提供 xG/xA 详细数据。
- `event_id`（字符串，必需）：比赛/赛事 ID

返回 `data.teams[]`：
```json
{
  "id": "...", "name": "Bukayo Saka", "position": "Midfielder", "shirt_number": 7, "starter": true,
  "statistics": {"appearances": "1", "shotsTotal": "3", "shotsOnTarget": "1", "foulsCommitted": "1", "xg": "0.45", "xa": "0.12"}
}
```
`xg` 和 `xa` 字段仅在前 5 个联赛中存在。

### get_missing_players
获取受伤/缺阵/状态不确定的球员信息（仅限英超联赛，通过 FPL 数据源）。其他联赛将返回空结果。
- `season_id`（字符串，必需）：赛季名称（必须是 `premier-league-*`）

返回 `data.teams[]`：
```json
{
  "id": "463748", "name": "Mikel Merino Zazón", "web_name": "Merino",
  "position": "Midfielder", "status": "injured",
  "news": "Foot injury - Unknown return date",
  "chance_of_playing_this_round": 0, "chance_of_playing_next_round": 0
}
```
状态值：`"injured"`、`"unavailable"`、`"doubtful"`、`"suspended"`。

### get_season_transfers
通过 Transfermarkt 获取特定球员的转会历史。适用于所有联赛。
- `season_id`（字符串，必需）：赛季名称（用于按年份筛选转会信息）
- `tm_player_ids`（列表，必需）：Transfermarkt 的球员 ID

返回 `data.transfers[]`：
```json
{
  "player_tm_id": "433177", "date": "2019-07-01", "season": "19/20",
  "from_team": {"name": "Arsenal U23", "image": "https://..."},
  "to_team": {"name": "Arsenal", "image": "https://..."},
  "fee": "-", "market_value": "-"
}
```

### get_player_season_stats
通过 ESPN 的概览端点获取球员的赛季统计数据。适用于任何拥有 ESPN 运动员 ID 的联赛。
- `player_id`（字符串，必需）：ESPN 运动员 ID
- `league_slug`（字符串，可选）：联赛名称（例如，“eng.1”、“esp.1”）。默认会自动检测联赛。

返回赛季统计数据（进球、助攻、出场次数等）以及比赛记录（如果可用）。

### get_player_profile
获取球员的详细信息。如果您有球员的 Transfermarkt 或 FPL ID，就可以使用此命令。至少需要提供一个 ID。
- `fpl_id`（字符串，可选）：FPL 球员 ID（仅限英超联赛）
- `tm_player_id`（字符串，可选）：Transfermarkt 的球员 ID（适用于任何联赛）

使用 `tm_player_id` 时，返回 `data.player`，其中包含：
```json
{
  "market_value": {"value": 130000000, "currency": "EUR", "formatted": "€130.00m", "date": "09/12/2025", "age": "24", "club": "Arsenal FC"},
  "market_value_history": [{"value": 7000000, "formatted": "€7.00m", "date": "23/09/2019", "club": "Arsenal FC"}],
  "transfer_history": [
    {"player_tm_id": "433177", "date": "2019-07-01", "season": "19/20", "from_team": {"name": "Arsenal U23"}, "to_team": {"name": "Arsenal"}, "fee": "-"}
  ]
}
```

使用 `fpl_id` 时，还会返回 `data.player.fpl_data`，其中包含 FPL 的统计数据（积分、状态、ICT 指数等）。

## 支持的联赛

英超联赛（Premier League）、西甲联赛（La Liga）、德甲联赛（Bundesliga）、意甲联赛（Serie A）、MLS、英冠联赛（Championship）、荷甲联赛（Eredivisie）、巴西甲级联赛（Primeira Liga）、欧冠联赛（Champions League）、欧洲冠军联赛（European Championship）、世界杯（World Cup）。

## 数据来源

| 来源 | 提供的内容 | 覆盖的联赛 |
|--------|-----------------|-----------------|
| ESPN | 比分、积分榜、赛程、阵容、比赛统计数据、时间线 | 所有 13 个联赛 |
| openfootball | 赛程、积分榜、球队列表（ESPN 故障时的备用来源） | 10 个联赛（除欧冠联赛、欧洲杯、世界杯外的所有联赛） |
| Understat | 每场比赛的预期进球（xG）、每次射门的预期进球（xG）、球员的预期进球/助攻（xG/xA） | 前 5 个联赛（EPL、La Liga、Bundesliga、Serie A、Ligue 1） |
| FPL | 得分最高的球员、伤病信息、球员统计数据、球队所有权信息 | 仅限英超联赛 |
| Transfermarkt | 转会市场信息、转会历史 | 任何球员（需要 `tm_player_id`） |

有关具有全面数据覆盖范围的授权服务（Sportradar、Opta、Genius Sports），请参阅 [Machina Sports](https://machina.gg)。

## 示例

用户：“显示英超联赛的积分榜”
1. 调用 `get_current_season(competition_id="premier-league")` 来获取当前赛季 ID
2. 调用 `get_season_standings(season_id=<步骤 1 中的赛季 ID>)` 来获取积分榜
3. 显示积分榜，包括球队名称、比赛场次、胜负情况、净胜球、积分等信息

用户：“阿森纳对阵利物浦的比赛结果如何？”
1. 调用 `get_daily_schedule()` 或 `get_team_schedule(team_id="359")` 来获取比赛 ID
2. 调用 `get_event_summary(event_id="...")` 来获取比赛比分
3. 调用 `get_event_statistics(event_id="...")` 来获取控球率、射门次数等数据
4. 调用 `get_event_xg(event_id="...")` 来获取预期进球（仅限英超联赛的前 5 个联赛）
5. 显示比赛报告，包括比分、关键数据和预期进球

用户：“深入分析切尔西最近的表现”
1. 调用 `search_team(query="Chelsea")` → `team_id=363`，`competition=premier-league`
2. 调用 `get_team_schedule(team_id="363", competition_id="premier-league")` 来获取最近的比赛信息
3. 对于每场比赛，同时调用：
   - `get_event_xg(event_id="...")` 来获取预期进球和射门数据
   - `get_event_statistics(event_id="...")` 来获取控球率、射门次数等数据
   - `get_event_players_statistics(event_id="...")` 来获取球员的预期进球/助攻数据
4. 调用 `get_missing_players(season_id=<赛季 ID>)` 来获取切尔西的受伤/缺阵球员信息
5. 调用 `get_season_leaders(season_id=<赛季 ID>)` 来获取切尔西球员的 FPL ID
6. 调用 `get_player_profile(fpl_id="...", tm_player_id="...")` 来获取球员的 FPL 统计数据（包括积分、状态、ICT 指数等）
7. 显示比赛中的预期进球趋势、关键球员统计数据、伤病报告以及市场价值

用户：“萨卡的市场价值是多少？”
1. 调用 `get_player_profile(tm_player_id="433177")` 来获取 Transfermarkt 的数据
2. 如果是英超联赛的球员，可以添加 `fpl_id` 来获取 FPL 统计数据
3. 显示市场价值、价值历史和转会历史

用户：“告诉我关于科林蒂安斯队的信息”
1. 调用 `search_team(query="Corinthians")` → `team_id=874`，`competition=serie-a-brazil`
2. 调用 `get_team_schedule(team_id="874", competition_id="serie-a-brazil")` 来获取比赛安排
3. 选择最近的一场比赛并调用 `get_event_timeline(event_id="...")` 来获取进球、黄牌、换人等信息
4. 注意：巴西甲级联赛的预期进球、FPL 统计数据和赛季领先者数据不可用

## 错误处理

当命令执行失败时（例如，错误的赛事 ID、数据缺失、网络错误等），**不要直接向用户显示原始错误信息**。相反：
1. **默默处理错误** — 将失败视为探索性错误，而不是致命错误。
2. **尝试替代方法** — 例如，如果某个赛事 ID 未返回数据，可以尝试调用 `get_daily_schedule()` 或 `get_team_schedule()` 来查找正确的 ID。如果 ESPN 不可用，可以通过 `get_season_standings` 或 `get_season_schedule` 来获取 openfootball 的数据。
3. **仅在尝试完所有替代方法后报告失败** — 并且要提供清晰易懂的错误信息（例如：“我找不到该比赛的信息 — 你能确认一下球队名称或日期吗？”），而不是显示原始的 CLI 错误信息。

当代理通过消息平台（如 Telegram、Slack 等）响应时，这一点尤为重要，因为原始的错误信息可能会让用户感到困惑。

## 常见错误

**以下是有效的命令**。请勿发明或猜测命令名称：
- `get_current_season`
- `get_competitions`
- `get_competition_seasons`
- `get_season_schedule`
- `get_season_standings`
- `get_season_leaders`
- `get_season_teams`
- `search_team`
- `get_team_profile`
- `get_daily_schedule`
- `get_event_summary`
- `get_event_lineups`
- `get_event_statistics`
- `get_event_timeline`
- `get_team_schedule`
- `get_head_to_head`
- `get_event_xg`
- `get_event_players_statistics`
- `get_missing_players`
- `get_season_transfers`
- `get_player_profile`
- `get_player_season_stats`

**不存在的命令**（经常被误输入的命令）：
- ~~`get_standings`~~ — 正确的命令是 `get_season_standings`（需要 `season_id`）。
- ~~`get_live_scores`~~ — 该命令不存在。使用 `get_daily_schedule()` 来获取今天的比赛信息；状态字段 `live` 表示比赛正在进行中。
- ~~`get_team_squad`~~ / ~~`get_team_roster`~~ — `get_team_profile` 不会返回球队阵容。请使用 `get_season_leaders` 获取球员 ID，然后使用 `get_player_profile` 获取球员的详细信息。
- ~~`get_transfers`~~ — 正确的命令是 `get_season_transfers`（需要 `season_id` 和 `tm_player_ids`）。
- ~~`get_match_results`~~ / ~~`get_match`~~ — 使用 `get_event_summary` 并传入 `event_id`。
- ~~`get_player_stats`~~ — 使用 `get_event_players_statistics` 来获取比赛级别的统计数据，或使用 `get_player_profile` 来获取球员的职业生涯数据。

**其他常见错误**：
- 在非英超联赛上使用 `get_season_leaders` 或 `get_missing_players` — 这些命令将返回空结果。请查看数据覆盖范围表。
- 在非前 5 个联赛上使用 `get_event_xg` — 该命令将返回空结果。仅适用于英超联赛（EPL、La Liga、Bundesliga、Serie A、Ligue 1）。
- 直接猜测 `team_id` 或 `event_id`，而不是通过 `search_team`、`get_daily_schedule` 或 `get_season_schedule` 来获取它们。

如果您不确定某个命令是否存在，请查看此列表。切勿尝试列表中未列出的命令。

## 故障排除

- **`sports-skills` 命令未找到**：说明该软件包未安装。运行 `pip install sports-skills`。如果 PyPI 上没有该软件包，请从 GitHub 安装：`pip install git+https://github.com/machina-sports/sports-skills.git`。需要 Python 3.10 或更高版本 — 请参阅设置部分。
- **`ModuleNotFoundError: No module named 'sports_skills'`**：与上述情况相同 — 请安装该软件包。建议使用 CLI 而不是 Python 导入，以避免路径问题。
- **仅限英超联赛的命令在其他联赛上返回空结果**：`get_season_leaders` 和 `get_missing_players` 仅返回英超联赛的数据。对于其他联赛，它们会默默返回空结果 — 请查看数据覆盖范围表。
- **`get_team_profile` 返回空结果**：这是正常现象 — 因为球队阵容信息不可用。要获取英超联赛球队的球员数据，请使用 `get_season_leaders` 获取球员的 ID，然后使用 `get_player_profile(fpl_id="..."` 来获取详细信息。对于 Transfermarkt 数据，需要球员的 `tm_player_id`。
- **查找 FPL ID 和 Transfermarkt ID**：使用 `get_season_leaders(season_id="premier-league-2025")` 来获取英超联赛球员的 FPL ID。Transfermarkt ID 需要在 [transfermarkt.com](https://www.transfermarkt.com) 上查询 — ID 是球员 URL 的末尾数字。例如：科尔·帕尔默（Cole Palmer）的 ID 为 `568177`，布卡约·萨卡（Bukayo Saka）的 ID 为 `433177`，姆巴佩（Mbappe）的 ID 为 `342229`。
- **最近的比赛没有预期进球数据**：Understat 的数据可能在比赛结束后 24-48 小时内才会更新。如果 `get_event_xg` 为最近的前 5 个联赛的比赛返回空结果，请稍后再尝试。
- **赛季 ID 格式错误**：必须使用 `{league-slug}-{year}` 的格式，例如 `"premier-league-2025"`，而不是 `"2025-2026"` 或 `"EPL-2025"`。请使用 `get_current_season()` 来获取正确的格式。
- **球队/赛事 ID 未知**：使用 `search_team(query="team name")` 根据名称查找球队 ID，或使用 `get_season_teams` 来获取某个赛季的所有球队列表。使用 `get_daily_schedule` 或 `get_season_schedule` 来获取赛事 ID。赛事 ID 是 ESPN 的数字字符串。