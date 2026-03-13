---
name: snooker
description: 您可以通过 api.snooker.org 查阅斯诺克排名、比赛结果、球员资料、实时比赛以及球员之间的对战记录。
version: 0.3.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    primaryEnv: SNOOKER_API_KEY
---
# 斯诺克

查询实时斯诺克数据——包括排名、比赛结果、球员资料等。

需要从 api.snooker.org 获取 API 密钥。请将环境变量 `SNOOKER_API_KEY` 设置为您的 API 密钥。请注意，当前的 API 使用限制为每分钟 10 次请求。

## 脚本

```bash
{baseDir}/snooker.py <command> [options]
```

## 命令

```bash
# Current world rankings (top 20)
{baseDir}/snooker.py rankings

# Rankings for a specific season
{baseDir}/snooker.py rankings --season 2024

# Player profile (search by name)
{baseDir}/snooker.py player "O'Sullivan"
{baseDir}/snooker.py player "Ronnie"

# Player profile by numeric ID (faster — use when you already have the ID)
{baseDir}/snooker.py player-id 16

# Recent results (returns Player1ID, Player2ID, EventID — use player-id/event to resolve names)
{baseDir}/snooker.py results
{baseDir}/snooker.py results --days 3

# Event details by numeric ID
{baseDir}/snooker.py event 2205

# Live matches in progress
{baseDir}/snooker.py live

# Matches scheduled for tomorrow (default) or a specific date
{baseDir}/snooker.py upcoming
{baseDir}/snooker.py upcoming --date 2026-03-15

# Upcoming matches for a specific player (all future matches, not just tomorrow)
{baseDir}/snooker.py upcoming --player "Hawkins"
{baseDir}/snooker.py upcoming --player "Ronnie O'Sullivan"

# Tournaments active tomorrow (default) or a specific date
{baseDir}/snooker.py tournaments
{baseDir}/snooker.py tournaments --date 2026-03-15

# Full schedule (tournaments + matches) for tomorrow or a specific date
{baseDir}/snooker.py schedule
{baseDir}/snooker.py schedule --date 2026-03-15

# Head-to-head record (split name pairs by position)
{baseDir}/snooker.py h2h Ronnie O'Sullivan Mark Selby
```

## 说明

- 所有数据均来自主要的职业巡回赛（巡回赛 ID：main）
- 排名显示当前赛季按奖金排名前 20 的选手
- 当球员名称不明确时，`player` 命令最多返回 3 个匹配结果
- `h2h` 命令可通过姓氏或全名进行搜索；如果名称不明确，请提供更具体的信息