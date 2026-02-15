---
name: flights
description: 通过 Google Flights 搜索航班。可以查找直飞/中转航班，根据时间和舱位等级进行筛选，并获取预订链接。
---

# 航班搜索

通过 Google Flights 数据实时查询航班时刻表和价格。

## 先决条件

```bash
pip install fast-flights
```

`flights-search` CLI 已安装在 `~/.local/bin/flights-search` 目录下。

## CLI 使用方法

```bash
flights-search <origin> <destination> <date> [options]
```

### 示例

```bash
# Basic search (auto-shows fewest stops available)
flights-search YYZ EWR 2026-02-06

# Nonstop flights only
flights-search YYZ JFK 2026-02-06 --nonstop

# Filter by departure time (24h format)
flights-search YYZ EWR 2026-02-06 --after 18        # After 6pm
flights-search YYZ EWR 2026-02-06 --before 12       # Before noon
flights-search YYZ EWR 2026-02-06 --after 9 --before 14

# Cabin class
flights-search YYZ EWR 2026-02-06 --class economy   # default
flights-search YYZ EWR 2026-02-06 --class premium   # premium economy
flights-search YYZ EWR 2026-02-06 --class business
flights-search YYZ EWR 2026-02-06 --class first

# Get Google Flights booking link
flights-search YYZ EWR 2026-02-06 --class business --link

# Multiple passengers
flights-search YYZ EWR 2026-02-06 --passengers 2

# Show all flights (ignore stop minimization)
flights-search YYZ EWR 2026-02-06 --all-stops
```

### 选项

| 选项 | 描述 |
|--------|-------------|
| `--nonstop` | 仅显示直飞航班 |
| `--all-stops` | 无论中途停靠多少次，都显示所有航班 |
| `--after HH` | 在指定时间（24小时格式）之后出发的航班 |
| `--before HH` | 在指定时间（24小时格式）之前出发的航班 |
| `--class` | 航班舱位：经济舱、高级经济舱、商务舱、头等舱 |
| `--passengers N` | 乘客人数 |
| `--link` | 打印 Google Flights 的完整链接 |

## 默认行为

默认情况下，CLI 仅显示**中途停留次数最少的航班**：
- 如果有直飞航班 → 仅显示直飞航班
- 如果没有直飞航班 → 仅显示中途停留一次的航班
- 使用 `--all-stops` 可以查看所有航班信息

## 输出结果

```
Depart                       Arrive                       Airline         Price      Duration
----------------------------------------------------------------------------------------------------
6:00 PM Fri, Feb 6           7:38 PM Fri, Feb 6           Air Canada      $361       1 hr 38 min
9:10 PM Fri, Feb 6           10:48 PM Fri, Feb 6          Air Canada      $361       1 hr 38 min

2 nonstop flight(s) found.
```

## 数据来源

通过 `fast-flights` 库（基于 Google Flights 的反向工程 protobuf API）获取数据。无需 API 密钥。

## 注意事项

- 日期格式：`YYYY-MM-DD`
- 机场代码：标准 IATA 代码（如 JFK、LAX、YYZ 等）
- 价格以美元（USD）显示
- 时间显示为当地机场的时区