---
name: snooker
description: 您可以通过 api.snooker.org 查阅斯诺克排名、比赛结果、球员资料、实时赛事以及球员之间的对战记录。
version: 0.2.5
metadata:
  openclaw:
    requires:
      env:
        - SNOOKER_API_KEY
      bins:
        - python3
    primaryEnv: SNOOKER_API_KEY
---
# 斯诺克

查询实时的斯诺克数据——包括排名、比赛结果、球员资料等。

需要从 api.snooker.org 获取 API 密钥。请注意，当前的 API 使用频率限制为每分钟 10 次请求。

## 脚本

```bash
{baseDir}/scripts/snooker.py <command> [options]
```

## 命令

```bash
# Current world rankings (top 20)
{baseDir}/scripts/snooker.py rankings

# Rankings for a specific season
{baseDir}/scripts/snooker.py rankings --season 2024

# Player profile (search by name)
{baseDir}/scripts/snooker.py player "O'Sullivan"
{baseDir}/scripts/snooker.py player "Ronnie"

# Player profile by numeric ID (faster — use when you already have the ID)
{baseDir}/scripts/snooker.py player-id 16

# Recent results (returns Player1ID, Player2ID, EventID — use player-id/event to resolve names)
{baseDir}/scripts/snooker.py results
{baseDir}/scripts/snooker.py results --days 3

# Event details by numeric ID
{baseDir}/scripts/snooker.py event 2205

# Live matches in progress
{baseDir}/scripts/snooker.py live

# Matches scheduled for tomorrow (default) or a specific date
{baseDir}/scripts/snooker.py upcoming
{baseDir}/scripts/snooker.py upcoming --date 2026-03-15

# Upcoming matches for a specific player (all future matches, not just tomorrow)
{baseDir}/scripts/snooker.py upcoming --player "Hawkins"
{baseDir}/scripts/snooker.py upcoming --player "Ronnie O'Sullivan"

# Tournaments active tomorrow (default) or a specific date
{baseDir}/scripts/snooker.py tournaments
{baseDir}/scripts/snooker.py tournaments --date 2026-03-15

# Full schedule (tournaments + matches) for tomorrow or a specific date
{baseDir}/scripts/snooker.py schedule
{baseDir}/scripts/snooker.py schedule --date 2026-03-15

# Head-to-head record (split name pairs by position)
{baseDir}/scripts/snooker.py h2h Ronnie O'Sullivan Mark Selby
```

## 设置（仅首次使用）

需要从 api.snooker.org 获取经过审核的 `X-Requested-By` API 密钥。
请发送邮件至 webmaster@snooker.org 申请访问权限，然后运行以下命令：

```bash
{baseDir}/scripts/snooker.py setup --api-key YOUR_KEY
```

配置信息存储在 `~/.nanobot/workspace/snooker/config.json` 文件中（位于 Docker 卷中）。

## 注意事项

- 所有数据均来自主要的职业斯诺克巡回赛（巡回赛 ID：main）。
- 排名显示当前赛季奖金最高的 20 名选手。
- 当球员名称存在歧义时，`player` 命令会返回最多 3 条匹配结果。
- `h2h` 命令支持按姓氏或全名进行搜索；如果名称存在歧义，请提供更具体的信息。