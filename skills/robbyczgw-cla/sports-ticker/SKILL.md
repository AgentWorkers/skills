---
name: sports-ticker
version: 3.0.5
description: 实时体育赛事提醒，涵盖足球、NFL、NBA、NHL、MLB、F1等运动项目。通过免费的ESPN API提供实时比分更新。您可以追踪全球任何主要联赛中的任意一支球队。
metadata: {"openclaw":{"requires":{"bins":["python3"],"note":"No API keys needed. Uses free ESPN API."}}}
---

# 体育赛事实时更新工具

您可以免费追踪您喜爱的**多个体育项目**的球队动态，并接收实时提醒！

支持的运动项目：⚽ 足球 • 🏈 美国国家橄榄球联盟（NFL）• 🏀 美国职业篮球联赛（NBA）• 🏒 国家冰球联盟（NHL）• ⚾ 美国职业棒球大联盟（MLB）• 🏎️ 一级方程式赛车（F1）

## 首次使用（设置流程）

如果系统中不存在 `config.json` 文件，运行设置脚本会启动一个交互式向导：

```bash
python3 scripts/setup.py
```

**向导会询问：**
1. 📺 **选择关注的运动项目？** — 可选足球、NFL、NBA、NHL、MLB 或 F1
2. 🏆 **选择关注的球队？** — 可从热门球队列表中选择，或自行搜索球队名称
3. 🔔 **提醒方式？** — 实时比分更新、仅显示最终结果，还是每日总结
4. ⏰ **比赛日提醒？** — 在比赛开始前 30 分钟收到提醒
5. 🌙 **静音时段？** — 在您睡觉时暂停提醒功能

设置完成后，`config.json` 文件会自动生成，您就可以开始追踪球队动态了！

**随时可以重新运行设置脚本：**
```bash
python3 scripts/setup.py --force  # Overwrites existing config
```

## 快速入门指南

```bash
# First time? Just run setup!
python3 scripts/setup.py  # Interactive wizard

# Find team IDs (any sport)
python3 scripts/setup.py find "Lakers" basketball
python3 scripts/setup.py find "Chiefs" football
python3 scripts/setup.py find "Barcelona" soccer

# Test
python3 scripts/ticker.py
```

## 配置示例

```json
{
  "teams": [
    {
      "name": "Barcelona",
      "emoji": "🔵🔴",
      "sport": "soccer",
      "espn_id": "83",
      "espn_leagues": ["esp.1", "uefa.champions"]
    },
    {
      "name": "Lakers",
      "emoji": "🏀💜💛",
      "sport": "basketball",
      "espn_id": "13",
      "espn_leagues": ["nba"]
    }
  ]
}
```

## 命令操作

```bash
# Ticker for all teams
python3 scripts/ticker.py

# Live monitor (for cron)
python3 scripts/live_monitor.py

# League scoreboard
python3 scripts/ticker.py league nba basketball
python3 scripts/ticker.py league nfl football
python3 scripts/ticker.py league eng.1 soccer

# 📅 Schedule - View upcoming fixtures (NEW in v3!)
python3 scripts/schedule.py                    # All teams, next 14 days
python3 scripts/schedule.py --days 30          # Look further ahead
python3 scripts/schedule.py --team spurs       # Specific team
python3 scripts/schedule.py --compact          # One-liner format
python3 scripts/schedule.py --json             # JSON output

# 🤖 Auto Setup Crons - Generate match-day crons (NEW in v3!)
python3 scripts/auto_setup_crons.py            # All teams, next 7 days
python3 scripts/auto_setup_crons.py --team spurs --days 14
python3 scripts/auto_setup_crons.py --json     # Machine-readable
python3 scripts/auto_setup_crons.py --commands # OpenClaw CLI commands

# ESPN direct
python3 scripts/espn.py leagues
python3 scripts/espn.py scoreboard nba basketball
python3 scripts/espn.py search "Chiefs" football
```

## 提醒类型：
- 🏟️ 比赛开始（开球/比赛开始）
- ⚽🏈🏀⚾ 重要得分（进球、达阵、三分球、本垒打）
- 🟥 红牌/球员被罚下
- ⏸️ 半场休息/节间休息
- 🏁 最终比赛结果（胜/负/平）

## ESPN API（免费使用！）

无需任何密钥即可使用。该 API 覆盖全球所有主要体育项目和 50 多个联赛的数据。

**支持的运动项目：**
- 足球：英超联赛、西甲联赛、欧冠联赛、MLS 等
- 美式橄榄球：NFL
- 篮球：NBA、WNBA、NCAA
- 冰球：NHL
- 棒球：MLB
- 赛车：一级方程式赛车