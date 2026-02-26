---
name: flights
version: 1.2.0
description: 通过 Google Flights 搜索航班：可以查找直飞或中转航班，按时间和舱位等级进行筛选，并获取预订链接。支持使用城市名称（如 NYC、London、Tokyo）进行搜索，系统会自动在多个机场中查找相应的航班信息。无需使用 API 密钥。
---
# 航班搜索

通过 Google Flights 数据实时查询航班时刻表和价格。

## 先决条件

- **Python 3.9 或更高版本**
- **[uv](https://docs.astral.sh/uv/)**（推荐）——使用以下命令安装：`curl -LsSf https://astral.sh/uv/install.sh | sh`

`flights-search` 命令行工具（CLI）位于该技能目录的 `scripts/flights-search` 文件夹中。

`fast-flights` 库会在首次运行时通过 `uvx` 自动安装（之后会缓存）。也可以手动安装：`pip install fast-flights`

## 命令行工具使用方法

```bash
uvx --with fast-flights python3 scripts/flights-search <origin> <destination> <date> [options]
```

起始地和目的地可以输入 **IATA 代码**（如 JFK、LAX）或 **城市名称**（如 NYC、London、Tokyo）。输入城市名称时，系统会自动搜索该城市所在地区的所有机场。

### 示例

```bash
# Search all NYC airports to LAX
flights-search NYC LAX 2026-03-15

# Nonstop flights from NYC to Berlin
flights-search NYC Berlin 2026-03-15 --nonstop

# Evening departures only
flights-search JFK LHR 2026-03-15 --after 17 --before 22

# Business class
flights-search NYC London 2026-03-15 --class business

# Multiple passengers with booking link
flights-search SF Tokyo 2026-04-01 --passengers 2 --link
```

### 选项

| 选项 | 描述 |
|--------|-------------|
| `--nonstop` | 仅显示直飞航班 |
| `--all-stops` | 显示所有航班（无论是否中途停靠） |
| `--after HH` | 在指定时间之后出发（24 小时格式） |
| `--before HH` | 在指定时间之前出发（24 小时格式） |
| `--class` | 航班舱位：经济舱、高级舱、商务舱、头等舱 |
| `--passengers N` | 乘客人数（默认值：1） |
| `--link` | 打印 Google Flights 的链接 |

### 支持的城市名称

输入城市名称时，系统会搜索该城市所在地区的所有机场：

| 城市 | 机场 |
|------|----------|
| NYC / 纽约 | JFK、EWR、LGA |
| LA / 洛杉矶 | LAX、BUR、LGB、ONT、SNA |
| SF / 旧金山 | SFO、OAK、SJC |
| 芝加哥 | ORD、MDW |
| DC / 华盛顿 | DCA、IAD、BWI |
| 伦敦 | LHR、LGW、STN、LTN、LCY |
| 巴黎 | CDG、ORY |
| 东京 | NRT、HND |
| 多伦多 | YYZ、YTZ |

支持 60 多个城市地区。对于未在列表中的机场，可以直接使用相应的 IATA 代码。

## 默认行为

默认情况下，命令行工具仅显示 **中途停靠次数最少** 的航班：
- 如果有直飞航班 → 仅显示直飞航班
- 如果没有直飞航班 → 仅显示中途停靠一次的航班
- 使用 `--all-stops` 可以查看所有航班

## 输出结果

```
Searching from NYC: JFK, EWR, LGA

Route        Depart                       Arrive                       Airline          Price       Duration
------------------------------------------------------------------------------------------------------------
EWR→LAX      6:00 AM on Sat, Mar 7        9:07 AM on Sat, Mar 7        United           $289        6 hr 7 min
EWR→LAX      12:00 PM on Sat, Mar 7       3:14 PM on Sat, Mar 7        United           $289        6 hr 14 min
JFK→LAX      8:00 AM on Sat, Mar 7        11:30 AM on Sat, Mar 7       Delta            $304        5 hr 30 min

3 flight(s) found.
```

## 注意事项

- 日期格式：`YYYY-MM-DD`
- 机场代码：标准 IATA 代码（如 JFK、LAX、LHR 等）
- 价格以美元显示
- 时间显示为当地机场的时间区
- 不需要 API 密钥——通过反向工程的 protobuf API 使用 Google Flights 数据
- 由于上游数据解析的限制，某些航线可能只返回价格信息（缺少出发/到达时间）

## 数据来源

通过 `fast-flights`（https://github.com/AWeirdDev/flights）Python 包获取 Google Flights 数据。