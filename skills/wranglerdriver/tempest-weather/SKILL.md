---
name: tempest-weather
description: 使用 Tempest REST API 从 WeatherFlow 的 Tempest 站点获取当前天气状况。该功能适用于以下场景：查询后院/家中的天气信息、特定站点的风速/阵风/降雨/雷电数据，或基于 Tempest 数据生成的快速本地天气概要。
version: 1.0.6
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

使用此技能可以从 Tempest 站点或设备获取当前天气信息，并以清晰的方式对其进行汇总。

## 运行获取脚本

使用以下命令：

```bash
python3 scripts/get_tempest_weather.py
```

该脚本默认从环境变量中读取配置信息。如果同时设置了站点 ID（station_id）和设备 ID（device_id），则会使用设备 ID：

- `TEMPEST_API_TOKEN`（必需）
- `TEMPEST_STATION_ID`（如果设置了 `TEMPEST_DEVICE_ID`，则可选）
- `TEMPEST_DEVICE_ID`（如果设置了 `TEMPEST_STATION_ID`，则可选）
- `TEMPEST_units`（可选：`metric` 或 `us`，默认为 `us`）

## 有用的命令选项

```bash
# Explicit station/token
python3 scripts/get_tempest_weather.py --station-id 12345 --token "$TEMPEST_API_TOKEN"

# Explicit device/token
python3 scripts/get_tempest_weather.py --device-id 67890 --token "$TEMPEST_API_TOKEN"

# Metric output
python3 scripts/get_tempest_weather.py --units metric

# JSON only (machine-friendly)
python3 scripts/get_tempest_weather.py --json
```

## 输出格式

- 始终以简洁的 JSON 格式输出数据
- 除非使用了 `--json` 选项，否则会提供简短的人类可读性摘要
- 会包含时间戳和数据来源 URL 以便追踪

## 如果数据获取失败

- 检查 API 密钥（token）的有效性以及站点/设备 ID 的正确性
- 对于短暂的网络问题，尝试重新获取一次数据
- 返回一条简短且易于理解的错误信息

## 字段映射参考

有关 Tempest 观测数据的字段映射和响应格式的详细信息，请参阅：

- `references/tempest-api.md`

## 许可证

- 使用 MIT 许可证（License: MIT）

## 代码来源

- https://github.com/wranglerdriver/tempest-weather