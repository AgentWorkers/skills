---
name: f1-cli
license: MIT
description: 使用 `f1-cli` 命令行工具（该工具封装了 OpenF1 API）来查询 Formula 1 的数据。当用户询问 F1 赛事结果、单圈成绩、车手排名、进站情况、遥测数据、天气信息、车队通讯内容、超车情况、轮胎策略或任何与 Formula 1 相关的统计数据时，都可以使用此功能。此外，在需要比较车手表现、分析比赛成绩、查找比赛数据或获取实时 F1 信息时，也可以使用该工具。该功能会在用户提及 “F1”、“Formula 1”、“大奖赛”（Grand Prix）、特定车手名称（如 Verstappen、Hamilton、Norris）或赛车数据相关内容时自动触发。即使是像 “谁赢得了上一场比赛？” 或 “Max 的最快单圈成绩是多少？” 这样的非专业性问题，也可以通过此功能来获取答案。
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

这是一个用 Go 语言编写的命令行工具（CLI），它封装了 [OpenF1 API](https://openf1.org)，用于查询 F1 车队的遥测数据、比赛计时信息以及赛事会话详情。

## 安装

```bash
brew tap barronlroth/tap
brew install f1-cli
```

或者通过源代码进行安装：
```bash
go install github.com/barronlroth/f1-cli/cmd/f1@latest
```

该工具的二进制文件名为 `f1`。

## 快速参考

### 全局参数（适用于所有命令）

| 参数 | 说明 |
|---|---|
| `--json` | 以 JSON 格式输出结果（默认为表格格式） |
| `--csv` | 以 CSV 格式输出结果 |
| `--session KEY` | 会话键（可以是数字或 `latest`） |
| `--meeting KEY` | 比赛周键（可以是数字或 `latest`） |
| `--driver DRIVER` | 车手编号（4位数字）或 3 个字母的缩写（例如：HAM） |
| `--limit N` | 限制返回的结果数量 |
| `--filter EXPR` | 原始 API 过滤条件（可重复使用，例如：`speed>=300`） |

### 命令与对应的 API 端点

| 命令 | API 端点 | 返回内容 |
|---|---|---|
| `f1 drivers` | `/drivers` | 车手信息：姓名、车队、编号、缩写 |
| `f1 sessions` | `/sessions` | 赛事会话列表（包括 FP1、排位赛、冲刺赛、正赛） |
| `f1 meetings` | `/meetings` | 大奖赛周末的相关信息（可选参数：`--year`、`--country`） |
| `f1 laps` | `/laps` | 单圈时间、各赛段时间、速度检测点数据 |
| `f1 telemetry` | `/car_data` | 车辆的转速、油门开度、刹车使用情况等数据（更新频率约 3.7 Hz） |
| `f1 pit` | `/pit` | 进站次数及每次进站的时间 |
| `f1 positions` | `/position` | 赛事会话期间车手的排名变化 |
| `f1 intervals` | `/intervals` | 与领先车手的差距以及前方车辆的距离（仅限正赛数据） |
| `f1 standings drivers` | `/championship_drivers` | 车手积分排名（仅限正赛数据） |
| `f1 standings teams` | `/championship_teams` | 车队积分排名（仅限正赛数据） |
| `f1 weather` | `/weather` | 跑道温度、空气温度、湿度、风速、降雨情况 |
| `f1 race-control` | `/race_control` | 赛事控制相关信息（如安全车出动情况） |
| `f1 radio` | `/team_radio` | 车队无线电通讯记录的 URL |
| `f1 stints` | `/stints` | 轮胎类型及每段赛程的行驶数据 |
| `f1 overtakes` | `/overtakes` | 车手之间的超车情况 |
| `f1 location` | `/location` | 车辆在赛道上的位置信息（更新频率约 3.7 Hz） |
| `f1 doctor` | — | 检查 API 连接是否正常 |

## 使用示例

### 查找相应的赛事会话

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

常见的车手缩写包括：VER（Verstappen）、NOR（Norris）、HAM（Hamilton）、LEC（Leclerc）、PIA（Piastri）、SAI（Sainz）、RUS（Russell）、ALO（Alonso）。

### 使用比较运算符进行过滤

`--filter` 参数会将用户输入的过滤条件直接传递给 API，支持 `>=`、`<=`、`>`、`<` 等运算符，且可以多次使用。

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

## 常见使用场景

### “谁赢得了上一场比赛？”
**请不要使用 `f1 positions` 命令来获取比赛结果。`f1 positions` 返回的是车手在整个会话期间的排名变化情况，而非最终的比赛结果。** 应使用 `f1 standings drivers` 命令来获取最终排名。

### “比较两位车手的单圈时间”
```bash
f1 laps --session latest --driver VER --json > /tmp/ver.json
f1 laps --session latest --driver NOR --json > /tmp/nor.json
# Then compare the JSON files
```

### “比赛中发生了什么？”（例如：事故、安全车出动等情况）
```bash
f1 race-control --session latest
```

### “轮胎策略分析”
```bash
f1 stints --session latest --driver VER
```

### “比赛期间的天气状况”
```bash
f1 weather --session latest --limit 10
```

### “最快的进站记录”
```bash
f1 pit --session latest --filter "stop_duration<3" --json | jq 'sort_by(.stop_duration)'
```

## 重要注意事项

- **`--limit` 参数仅在客户端生效。** OpenF1 API 自身不支持 `limit` 参数，因此 CLI 会在获取所有数据后自行限制返回结果的数量。对于大量数据的查询，建议使用 `--filter` 在服务器端进行过滤。
- **`--filter` 参数在服务器端生效。** 使用 `--filter` 可以有效减少 API 的请求量，从而提高性能。
- `f1 positions` 返回的是车手在整个会话期间的排名变化情况，而非最终的比赛结果。要获取最终排名，请使用 `f1 standings drivers --session <key>` 命令。
- 车手编号会随着赛季的变化而调整，请使用缩写（如 VER、HAM、NOR），CLI 会自动根据当前赛季解析正确的编号。
- 2026 赛季中，Lando Norris 驾驶 1 号赛车（作为卫冕冠军），Verstappen 驾驶 3 号赛车。

## API 相关说明

- **数据可用性：** 自 2023 赛季起的历史数据均可查询，无需身份验证。
- **请求限制：** 每秒 3 次请求，每分钟 30 次请求（免费账户限制）。CLI 会在内部实现请求限制，并在请求失败时尝试重试（错误代码 429）。
- `--latest` 关键字：无论用于 `--session` 还是 `--meeting`，都能获取最新的数据。
- **某些功能仅限于正赛期间：** 如 `intervals` 和 `overtakes`，在排位赛或练习赛中不可用。
- **积分排名数据：** 仅适用于正赛数据。
- **高频率数据传输：** 遥测数据更新频率约为 3.7 Hz，建议使用 `--filter` 在服务器端过滤数据，再使用 `--limit` 限制输出结果数量。
- **非赛季期间：** 如果当前没有比赛会话，使用 `--session latest` 会返回 404 错误。此时请使用过去赛季的会话 ID。