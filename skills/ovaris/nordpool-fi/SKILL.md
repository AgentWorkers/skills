---
name: nordpool-fi
description: 芬兰的每小时电价以及最优电动汽车充电时间窗口计算（3小时、4小时、5小时）
metadata: {"tags": ["energy", "finland", "nordpool", "electricity", "ev-charging"]}
---

# Nordpool 芬兰能源价格 🇫🇮

提供芬兰的每小时电价信息，并计算最佳的电动汽车充电时间段（3小时、4小时、5小时）。

该技能通过使用 Porssisahko.net API 来获取芬兰的每小时电价数据。它能够将 UTC 时间转换为芬兰当地时间，并为需要大量电力的任务（如电动汽车充电）提供有用的信息。

## 工具

### nordpool-fi

用于获取当前价格、每日统计数据以及最佳充电时间段。

**使用方法：**
`public-skills/nordpool-fi/bin/nordpool-fi.py`

**输出格式（JSON）：**
- `current_price`: 当前小时电价（snt/kWh）
- `best_charging_windows`: 最佳的连续充电时间段（3小时、4小时、5小时）
- `today_stats`: 当日的平均电价、最低电价和最高电价。

## 示例

获取最佳的4小时充电时间段：
```bash
public-skills/nordpool-fi/bin/nordpool-fi.py | jq .best_charging_windows.4h
```