---
name: f1-cli
license: MIT
description: 使用 `f1-cli` 命令行工具（基于 OpenF1 API）查询一级方程式（Formula 1）的数据。当用户询问 F1 比赛结果、单圈时间、车手排名、进站次数、遥测数据、天气情况、车队通讯内容、超车情况、轮胎策略或任何与 F1 相关的统计数据时，可以使用此工具。此外，在需要比较车手表现、分析比赛成绩、查找比赛数据或获取实时 F1 信息时，也可以使用该工具。该功能会在用户提及 “F1”、“Formula 1”、“Grand Prix”、“特定车手名称”（如 Verstappen、Hamilton、Norris）或赛车数据相关内容时自动触发。即便是像 “谁赢得了上一场比赛？” 或 “Max 的最快单圈成绩是多少？” 这样的非专业性问题，也可以通过此技能来获取答案。
metadata:
  {
    "openclaw":
      {
        "emoji": "🏎️",
        "requires": { "bins": ["f1"] },
      },
  }
---
# f1-cli — F1 数据命令行工具

这是一个用 Go 语言编写的命令行工具（CLI），它封装了 [OpenF1 API](https://openf1.org)，用于查询 F1 车队的遥测数据、比赛计时信息以及比赛会话详情。

## 可执行文件的位置

可执行文件应该位于以下路径之一：
- `f1`（如果已添加到系统的 PATH 环境变量中）
- `/Users/barron/Developer/f1-cli/f1`（从源代码编译而成）

如果找不到该文件，请先编译它：
```bash
cd /Users/barron/Developer/f1-cli && go build -o f1 ./cmd/f1
```

## 快速参考

### 全局参数（适用于所有命令）

| 参数 | 说明 |
|---|---|
| `--json` | 以 JSON 格式输出结果（默认为表格格式） |
| `--csv` | 以 CSV 格式输出结果 |
| `--session KEY` | 会话键（可以是数字或 `latest`） |
| `--meeting KEY` | 比赛会话键（可以是数字或 `latest`） |
| `--driver DRIVER` | 车手编号（44 位数字）或 3 个字母的缩写（例如：HAM） |
| `--limit N` | 限制返回的结果数量 |
| `--filter EXPR` | 原始 API 过滤条件（可重复使用，例如：`speed>=300`） |

### 命令与对应的 API 端点

| 命令 | API 端点 | 返回的数据 |
|---|---|---|
| `f1 drivers` | `/drivers` | 车手信息：姓名、车队、编号、缩写 |
| `f1 sessions` | `/sessions` | 比赛会话列表（包括 FP1、Quali、Sprint、Race 环节） |
| `f1 meetings` | `/meetings` | 大奖赛周末的相关信息（可添加 `--year` 或 `--country` 参数） |
| `f1 laps` | `/laps` | 单圈时间、各赛段时间、速度监测数据 |
| `f1 telemetry` | `/car_data` | 车速、转速、挡位、油门踏板位置、刹车使用情况（数据更新频率约 3.7 Hz） |
| `f1 pit` | `/pit` | 进站时间与持续时间 |
| `f1 positions` | `/position` | 比赛会话中的车辆位置变化情况 |
| `f1 intervals` | `/intervals` | 与领先车辆及前方车辆之间的差距（仅限比赛数据） |
| `f1 standings drivers` | `/championship_drivers` | 车手积分排名（比赛会话数据） |
| `f1 standings teams` | `/championship_teams` | 车队积分排名（比赛会话数据） |
| `f1 weather` | `/weather` | 赛道温度、空气温度、湿度、风速、降雨情况 |
| `f1 race-control` | `/race_control` | 比赛控制相关信息（如安全车出动、事故等） |
| `f1 radio` | `/team_radio` | 车队无线电通讯记录的 URL |
| `f1 stints` | `/stints` | 轮胎类型及每段赛程的行驶数据 |
| `f1 overtakes` | `/overtakes` | 车手之间的超车情况 |
| `f1 location` | `/location` | 车辆在赛道上的实时位置（数据更新频率约 3.7 Hz） |
| `f1 doctor` | — | 检查 API 连接是否正常 |

## 常见使用场景

### 查找特定的比赛会话

大多数命令都需要使用 `--session` 参数。可以使用 `--latest` 来获取最新的会话数据，或者指定具体的会话 ID：
```bash
# List sessions for the latest meeting
f1 sessions --meeting latest

# Find a specific Grand Prix
f1 meetings --year 2025 --country Singapore

# Then use the session_key from the output
f1 laps --session 9161 --driver VER
```

### 车手识别

`--driver` 参数可以接受数字或 3 个字母的缩写。该工具会通过 API 自动解析这些缩写对应的车手信息。
```bash
# These are equivalent
f1 laps --session latest --driver 1
f1 laps --session latest --driver VER
```

常见的车手缩写示例：VER（Verstappen）、NOR（Norris）、HAM（Hamilton）、LEC（Leclerc）、PIA（Piastri）、SAI（Sainz）、RUS（Russell）、ALO（Alonso）。

### 使用比较运算符进行过滤

`--filter` 参数会将用户输入的过滤条件直接传递给 API。支持 `>=`、`<=`、`>`、`<` 等运算符，且可以重复使用该参数进行过滤。
```bash
# Cars going over 315 km/h
f1 telemetry --session 9159 --driver 55 --filter "speed>=315"

# Pit stops under 2.5 seconds
f1 pit --session latest --filter "stop_duration<2.5"

# Combine multiple filters
f1 telemetry --session latest --driver VER --filter "speed>=300" --filter "throttle>=95"

# Laps under 90 seconds
f1 laps --session latest --filter "lap_duration<90"
```

### 输出格式

```bash
# Default: aligned table
f1 drivers --session latest

# JSON for piping to jq or other tools
f1 telemetry --session latest --driver VER --json | jq '.[0].speed'

# CSV for spreadsheets
f1 laps --session latest --driver HAM --csv > hamilton_laps.csv
```

## 常见使用示例

### “谁赢得了上一场比赛？”
**请不要使用 `f1 positions` 命令来获取比赛结果。**`f1 positions` 返回的是车辆在整个比赛会话中的位置变化情况，而非最终排名。请使用 `f1 standings drivers` 命令来获取最终排名。**

### “比较两位车手的单圈成绩”
```bash
f1 laps --session latest --driver VER --json > /tmp/ver.json
f1 laps --session latest --driver NOR --json > /tmp/nor.json
# Then compare the JSON files
```

### “比赛中发生了什么？”（例如：事故、安全车出动等事件）
```bash
f1 race-control --session latest
```

### “轮胎策略分析”
```bash
f1 stints --session latest --driver VER
```

### “比赛会话期间的天气情况”
```bash
f1 weather --session latest --limit 10
```

### “最快的进站策略”
```bash
f1 pit --session latest --filter "stop_duration<3" --json | jq 'sort_by(.stop_duration)'
```

## 重要注意事项

- **`--limit` 参数仅在客户端生效。**OpenF1 API 不支持 `limit` 参数，因此 CLI 会先获取所有数据后再在本地进行筛选。对于大规模的数据查询，建议使用 `--filter` 参数在服务器端进行过滤。
- **`--filter` 参数在服务器端生效。**使用 `--filter` 可以有效减少 API 的数据传输量，从而提高查询效率。因此，在可能的情况下，请优先使用 `--filter` 而不是 `--limit`。
- **`f1 positions` 返回的是车辆位置的变化情况，而非最终比赛结果。**若需获取最终排名，请使用 `f1 standings drivers --session <key>` 命令。使用 `f1 positions --limit N` 只能获取第 1 圈的发车顺序，而非最终排名。
- **车手编号在不同赛季可能会有所变化。**请使用车手的缩写（如 VER、HAM、NOR），因为 CLI 会根据比赛会话自动解析这些缩写。
- **2026 赛季，Lando Norris 驾驶 1 号赛车（作为卫冕冠军）。Verstappen 驾驶 3 号赛车。**

## API 相关说明

- **数据可用性：**自 2023 赛季起的历史数据均可查询，无需身份验证。
- **请求限制：**免费账户每秒最多发送 3 次请求，每分钟最多发送 30 次请求。CLI 会内部处理请求限制，并在请求失败时尝试重试（错误代码为 429）。
- `--latest` 关键字：无论用于 `--session` 还是 `--meeting`，均可获取最新的数据。
- **某些功能（如 `intervals` 和 `overtakes`）仅在比赛会话期间可用，练习赛或排位赛期间不可用。**
- **积分排名数据：**仅适用于比赛会话。
- **遥测数据和车辆位置数据更新频率很高（约 3.7 Hz）**：建议使用 `--filter` 在服务器端进行筛选，然后再使用 `--limit` 来限制输出结果数量。
- **非赛季期间：**如果当前没有比赛会话，使用 `--session latest` 会返回 404 错误。此时请使用过去赛季的有效会话 ID。