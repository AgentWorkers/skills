---
name: flightclaw
description: 使用 Google Flights 数据来追踪航班价格。您可以搜索航班、查找最便宜的出行日期、根据航空公司、出行时间、旅行时长或价格进行筛选，同时可以随时间跟踪航班路线变化，并在价格下降时收到提醒。该工具还可以作为 MCP 服务器运行。需要 Python 3.10 及以上的版本，以及 `flights` 和 `mcp` 这两个 Python 包。请运行 `setup.sh` 命令来安装所需的依赖项。
---
# flightclaw

这是一个用于跟踪谷歌航班价格的工具。你可以搜索航班路线、监控价格变化，并在价格下降时收到提醒。

## 安装

```bash
npx skills add jackculpan/flightclaw
```

或者手动安装：

```bash
bash skills/flightclaw/setup.sh
```

## 脚本

### 搜索航班
根据指定的路线和日期查找航班。支持多个机场和日期范围。

```bash
python skills/flightclaw/scripts/search-flights.py LHR JFK 2025-07-01
python skills/flightclaw/scripts/search-flights.py LHR JFK 2025-07-01 --cabin BUSINESS
python skills/flightclaw/scripts/search-flights.py LHR JFK 2025-07-01 --return-date 2025-07-08
python skills/flightclaw/scripts/search-flights.py LHR JFK 2025-07-01 --stops NON_STOP --results 10
# Multiple airports (searches all combinations)
python skills/flightclaw/scripts/search-flights.py LHR,MAN JFK,EWR 2025-07-01
# Date range (searches each day)
python skills/flightclaw/scripts/search-flights.py LHR JFK 2025-07-01 --date-to 2025-07-05
# Both
python skills/flightclaw/scripts/search-flights.py LHR,MAN JFK,EWR 2025-07-01 --date-to 2025-07-03
```

参数：
- `origin` - 起飞机场的IATA代码（用逗号分隔，例如：LHR 或 LHR,MAN）
- `destination` - 目的地机场的IATA代码（用逗号分隔，例如：JFK 或 JFK,EWR）
- `date` - 出发日期（YYYY-MM-DD）
- `--date-to` - 日期范围的结束日期（YYYY-MM-DD）：从指定日期开始每天进行搜索，包括该日期。
- `--return-date` - 往返旅行的返回日期（YYYY-MM-DD）
- `--cabin` - 航班舱位类型（默认：ECONOMY；可选：PREMIUM_ECONOMY, BUSINESS, FIRST）
- `--stops` - 中途停留次数（默认：ANY；可选：NON_STOP, ONE_STOP, TWO_STOPS）
- `--results` - 显示的结果数量（默认：5）

### 跟踪航班
将某条航线添加到价格跟踪列表中，并记录当前价格。支持多个机场和日期范围（每种组合都会创建一个单独的跟踪记录）。

```bash
python skills/flightclaw/scripts/track-flight.py LHR JFK 2025-07-01
python skills/flightclaw/scripts/track-flight.py LHR JFK 2025-07-01 --target-price 400
python skills/flightclaw/scripts/track-flight.py LHR JFK 2025-07-01 --return-date 2025-07-08 --cabin BUSINESS
# Track multiple airports and dates
python skills/flightclaw/scripts/track-flight.py LHR,MAN JFK,EWR 2025-07-01 --date-to 2025-07-03 --target-price 400
```

参数：
与 `search_flights` 相同，另外需要提供：
- `--target-price` - 当价格低于此金额时触发提醒

### 检查价格
定期检查所有被跟踪航班的价格变化。该脚本可以按照预设的时间表（cron）自动运行。

```bash
python skills/flightclaw/scripts/check-prices.py
python skills/flightclaw/scripts/check-prices.py --threshold 5
```

参数：
- `--threshold` - 触发提醒的价格下降百分比（默认：10%）

输出：报告被跟踪航班的价格变化情况，突出显示价格下降的情况，并在达到目标价格时发出提醒。

### 列出被跟踪的航班
显示所有被跟踪的航班及其当前价格与原始价格。

```bash
python skills/flightclaw/scripts/list-tracked.py
```

## MCP 服务器

FlightClaw 还可以作为 MCP 服务器使用，提供更丰富的搜索功能：

```bash
pip install flights "mcp[cli]"
claude mcp add flightclaw -- python3 server.py
```

MCP 命令包括：`search_flights`、`search_dates`、`track_flight`、`check_prices`、`list_tracked`、`remove_tracked`。

额外的 MCP 过滤选项包括：乘客类型（成人/儿童/婴儿）、航空公司筛选、价格范围、最长飞行时间限制、出发/到达时间限制、中途停留时间限制、排序方式以及按最便宜日期搜索的功能。

## 货币

价格会根据用户的 IP 地址自动转换为用户当地的货币进行显示。货币类型会从谷歌航班 API 的响应中自动检测并使用正确的符号（例如：$、£、฿、€）。被跟踪航班的价格信息会存储在 `tracked.json` 文件中。

## 数据存储

价格历史数据保存在 `skills/flightclaw/data/tracked.json` 文件中，并通过 R2 备份系统进行持久化存储。