---
name: tempest-weather
description: 使用 WeatherFlow 的 Tempest REST API 获取当前天气状况。适用于以下场景：用户查询“tempest weather”（推荐触发方式）；用户询问后院/家中的天气情况；用户请求特定气象站的風速、阵风、降雨量、闪电等数据；或用户需要基于 Tempest 数据生成的快速本地天气概要。
license: MIT
metadata:
  openclaw:
    requires:
      env:
        - TEMPEST_API_TOKEN
        - TEMPEST_STATION_ID
        - TEMPEST_DEVICE_ID
        - TEMPEST_UNITS
      anyBins:
        - python3
    primaryEnv: TEMPEST_API_TOKEN
    homepage: https://github.com/wranglerdriver/tempest-weather
---
# Tempest Weather

使用此技能可以从 Tempest 站点/设备获取当前天气信息，或通过 Tempest Stats API 获取历史天气数据（按天/月/年划分）。

## 运行数据获取脚本

使用以下命令：

```bash
python3 scripts/get_tempest_weather.py
```

该脚本默认从环境变量中读取配置信息。如果同时设置了站点 ID（station_id）和设备 ID（device_id），则使用设备 ID：

- `TEMPEST_API_TOKEN`（必填）
- `TEMPEST_STATION_ID`（如果设置了 `TEMPEST_DEVICE_ID`，则可选）
- `TEMPEST_DEVICE_ID`（如果设置了 `TEMPEST_STATION_ID`，则可选）
- `TEMPEST_units`（可选：`metric` 或 `us`，默认为 `us`）

## 有用的命令选项

```bash
# Explicit station/token (current observations)
python3 scripts/get_tempest_weather.py --station-id 12345 --token "$TEMPEST_API_TOKEN"

# Explicit device/token (current observations)
python3 scripts/get_tempest_weather.py --device-id 67890 --token "$TEMPEST_API_TOKEN"

# Historical stats for current local day/month/year (defaults to "now")
python3 scripts/get_tempest_weather.py --stats day
python3 scripts/get_tempest_weather.py --stats month
python3 scripts/get_tempest_weather.py --stats year

# Historical stats for a specific target date period
python3 scripts/get_tempest_weather.py --stats day --date 2026-02-23
python3 scripts/get_tempest_weather.py --stats month --date 2026-02
python3 scripts/get_tempest_weather.py --stats year --date 2025

# Metric output
python3 scripts/get_tempest_weather.py --units metric

# JSON only (machine-friendly)
python3 scripts/get_tempest_weather.py --json
```

## 输出格式

- 始终以简洁的 JSON 格式输出数据
- 除非使用了 `--json` 选项，否则会提供简短的文字描述
- 会包含时间戳和数据来源的 URL 以便追踪
- 使用 `--stats` 选项时，会返回 `stats_day`、`stats_month` 或 `stats_year` 中匹配的历史数据记录

## 如果数据获取失败

- 检查 API 令牌的有效性以及站点/设备 ID 是否正确
- 对于短暂的网络问题，尝试重试一次
- 返回一条简洁的错误信息

## 字段映射参考

有关 Tempest 观测数据的字段映射和响应格式的详细信息，请参阅：

- `references/tempest-api.md`

## 许可证

- 使用 MIT 许可证（MIT License）

## 代码来源

- https://github.com/wranglerdriver/tempest-weather