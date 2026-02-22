---
name: baseball
description: 通过 MLB Stats API 获取 MLB 比赛日程、实时比赛状态、比分统计、球员查询以及赛季数据。当用户询问关于棒球比赛、比分、当天的参赛球员、比赛结果、实时更新、投手对决、MLB 赛程信息、球员查询或球员统计数据时，可以使用该接口。
metadata: {"openclaw":{"emoji":"⚾","requires":{"bins":["python3"]}}}
---
# 棒球 — MLB比赛追踪器

通过MLB Stats API获取实时的MLB比赛日程、比赛状态、比分记录、球员搜索结果以及赛季统计数据。

## 快速入门

```bash
# List today's games
python scripts/baseball.py games

# Live game status for the Phillies
python scripts/baseball.py live PHI

# Box score for a specific game
python scripts/baseball.py score 718415

# Box score for last Tuesday's Phillies game
python scripts/baseball.py score PHI --date 02/15/2026

# Search for a player
python scripts/baseball.py player Judge

# Search with team filter
python scripts/baseball.py player Wheeler --team PHI

# Player season stats by ID
python scripts/baseball.py stats 592450

# Player season stats by name
python scripts/baseball.py stats Aaron Judge --season 2025
```

## 使用方法

### 列出球队

```bash
# Show all team abbreviations
python scripts/baseball.py teams
```

### 列出比赛

```bash
# Today's games
python scripts/baseball.py games

# Games on a specific date
python scripts/baseball.py games --date 09/15/2025

# Next 7 days of games
python scripts/baseball.py games --days 7

# Upcoming week for a specific team
python scripts/baseball.py games --team PHI --days 7

# Filter by team
python scripts/baseball.py games --team PHI

# JSON output
python scripts/baseball.py games --format json
```

### 比赛状态

显示正在进行中的比赛的实时比分、跑垒员情况、击球手/投手的对战信息以及比分。

```bash
# By team abbreviation (finds today's game)
python scripts/baseball.py live PHI

# By game PK
python scripts/baseball.py live 718415

# Game status from a specific date
python scripts/baseball.py live NYY --date 02/10/2026

# JSON output
python scripts/baseball.py live PHI --format json
```

### 比分记录

显示任何比赛（进行中或已结束）的比分。

```bash
# By team abbreviation (today's game)
python scripts/baseball.py score PHI

# By game PK (works for any game, past or present)
python scripts/baseball.py score 718415

# By team abbreviation for a past date
python scripts/baseball.py score PHI --date 02/15/2026

# JSON output
python scripts/baseball.py score PHI --format json
```

### 搜索球员

```bash
# Search by last name
python scripts/baseball.py player Judge

# Search by full name
python scripts/baseball.py player Aaron Judge

# Filter by team
python scripts/baseball.py player Wheeler --team PHI

# JSON output
python scripts/baseball.py player Judge --format json
```

### 球员统计信息

```bash
# By player ID (from player search results)
python scripts/baseball.py stats 592450

# By player name (auto-resolves if unique match)
python scripts/baseball.py stats Aaron Judge

# Specific season
python scripts/baseball.py stats Aaron Judge --season 2024

# JSON output
python scripts/baseball.py stats 592450 --format json
```

## 输出格式

### 文本格式（默认）

**games:**

```
MLB Games - 09/15/2025
Away              Record     Home              Record     Time       Status               Game ID
-----------------------------------------------------------------------------------------------
PHI Phillies      85-62      NYM Mets          80-67      7:10 PM    In Progress          718415
BOS Red Sox       72-75      TB Rays           78-69      6:40 PM    Final (5-3)          718420
```

**live:**

```
PHI Phillies 3  @  NYM Mets 5
  Top 6th  |  1 out  |  2-1 count
  Bases: 1B [X]  2B [ ]  3B [X]
  AB: Kyle Schwarber  vs  P: Sean Manaea
  Last: Trea Turner singled on a line drive to left field.

       1  2  3  4  5  6  7  8  9    R  H  E
PHI    0  1  0  2  0  0  -  -  -    3  7  1
NYM    2  0  0  1  2  0  -  -  -    5  9  0
```

**score:**

```
Final: PHI Phillies 6  @  NYM Mets 4

       1  2  3  4  5  6  7  8  9    R  H  E
PHI    0  1  0  2  0  0  2  0  1    6  11  0
NYM    2  0  0  1  2  0  0  0  0    4   9  1
```

**player:**

```
Player Search: "Judge"
ID         Name                      Pos   Team                 #     B/T   Age
--------------------------------------------------------------------------------
592450     Aaron Judge               RF    NYY Yankees          99    R/R   33
```

**stats (batting):**

```
Aaron Judge  #99  RF  |  New York Yankees  |  R/R  |  Age 33
2025 Season Batting Statistics
  G     AB    R     H    2B   3B   HR   RBI   SB   BB    K    AVG    OBP    SLG    OPS
  152   541   137   179  30   2    53   114   12   124   160  .331   .457   .688   1.145
```

**stats (pitching):**

```
Zack Wheeler  #45  P  |  Philadelphia Phillies  |  L/R  |  Age 35
2025 Season Pitching Statistics
  G    GS   W    L    ERA    IP      H    R    ER   HR   SO   BB   SV   HLD  WHIP   K/9    BB/9
  30   30   14   6    2.85   198.1   155  68   63   18   210  42   0    0    0.99   9.55   1.91
```

### JSON格式

```json
{
  "date": "09/15/2025",
  "games": [
    {
      "game_pk": 718415,
      "status": "In Progress",
      "away_team": {"id": 143, "name": "Philadelphia Phillies", "abbreviation": "PHI"},
      "home_team": {"id": 121, "name": "New York Mets", "abbreviation": "NYM"},
      "away_record": "85-62",
      "home_record": "80-67",
      "away_score": 3,
      "home_score": 5,
      "venue": "Citi Field",
      "start_time": "2025-09-15T19:10:00-04:00"
    }
  ]
}
```

**player search (JSON):**

```json
{
  "query": "Judge",
  "players": [
    {
      "id": 592450,
      "full_name": "Aaron Judge",
      "position": "RF",
      "position_name": "Right Fielder",
      "primary_number": "99",
      "bats": "R",
      "throws": "R",
      "age": 33,
      "team": "New York Yankees",
      "team_abbreviation": "NYY",
      "active": true
    }
  ]
}
```

## 输出字段

- **game_pk** — 独特的MLB比赛标识符
- **status** — 比赛状态：已安排、赛前、热身、进行中、已结束、延期等
- **away_team / home_team** — 对战球队ID、全称及缩写
- **away_record / home_record** — 胜败记录（仅适用于比赛日程）
- **away_score / home_score** — 当前或最终比分
- **inning / inning_half** — 当前局数（上半局/下半局）
- **balls / strikes / outs** — 当前比赛计数
- **runners** — 跑垒员情况：一垒/二垒/三垒上有无跑垒员（true/false）
- **matchup** — 当前击球手和投手的姓名
- **last_play** — 最后一次完成的比赛情况的描述
- **line_score** — 每局的得分情况（包括得分、安打、出局数）
- **venue** — 球场名称
- **start_time** — 当地时间安排的开始时间（ISO 8601格式）
- **id** — MLB球员标识符（用于`stats`命令）
- **full_name** — 球员的全名
- **position** — 球员位置缩写（如RF、P、C、SS等）
- **primary_number** — 球员球衣号码
- **bats / throws** — 击球手惯用手和投手投球手惯用手（R、L、S）
- **batting** — 赛季击球数据（平均打击率、上垒率、长打率、OPS、本垒打数等）
- **pitching** — 赛季投球数据（自责分率、胜场数、失败次数、三振数等）

## 球队缩写

运行`python scripts/baseball.py teams`命令可列出所有球队缩写。也可以使用部分球队名称（例如：“Phillies”、“Dodgers”、“Red Sox”）。

ARI、ATL、BAL、BOS、CHC、CWS、CIN、CLE、COL、DET、HOU、KC、LAA、LAD、MIA、MIL、MIN、NYM、NYY、OAK、PHI、PIT、SD、SF、SEA、STL、TB、TEX、TOR、WSH

## 注意事项

- 数据来源于MLB Stats API。请参阅[版权信息](http://gdx.mlb.com/components/copyright.txt)。
- MLB Stats API是免费且开放的——无需API密钥或身份验证。请勿滥用该API。过度请求（如快速轮询、批量抓取等）可能会导致您的IP被封禁。在查看比赛状态时，每15秒内请不要多次请求。
- `live`和`score`命令可以接受数字形式的比赛ID或球队缩写。使用缩写时，脚本会查询当天的比赛日程以确定对应的球队。使用`--date MM/DD/YYYY`可以查询指定日期的比赛。
- `games`文本输出包含一个“Game ID”字段。可以使用此ID与`score`或`live`命令来查看特定比赛的信息——这对于区分同名球队（如双场赛）非常有用。
- `player`命令用于搜索现役MLB球员。可以使用搜索结果中的球员ID通过`stats <ID>`命令查看其赛季统计数据。
- `stats`命令可以接受数字形式的球员ID或球员姓名。如果有多名球员同名，系统会提示您使用具体的ID。
- 在休赛期，可以使用`--season`参数查看上一年的统计数据（例如：`--season 2025`）。