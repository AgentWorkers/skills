---
name: travelclaw
description: 使用 Google Flights 数据来追踪航班价格。您可以搜索航班信息、随时间跟踪航线变化，并在价格下降时收到提醒。该功能需要 Python 3.10 及以上的版本以及 `flights` 这个 Python 包。请运行 `setup.sh` 命令来安装所需的依赖项。
---

# 航班价格追踪器

从 Google Flights 中追踪航班价格。搜索航线、监控价格变化，并在价格下降时收到警报。

## 设置

```bash
bash skills/flight-tracker/setup.sh
```

## 脚本

### 搜索航班
查找特定航线和日期的航班信息。

```bash
python skills/flight-tracker/scripts/search-flights.py LHR JFK 2025-07-01
python skills/flight-tracker/scripts/search-flights.py LHR JFK 2025-07-01 --cabin BUSINESS
python skills/flight-tracker/scripts/search-flights.py LHR JFK 2025-07-01 --return-date 2025-07-08
python skills/flight-tracker/scripts/search-flights.py LHR JFK 2025-07-01 --stops NON_STOP --results 10
```

参数：
- `origin` - 起飞机场的 IATA 代码（例如：LHR、JFK、SFO）
- `destination` - 目的地机场的 IATA 代码
- `date` - 出发日期（YYYY-MM-DD）
- `--return-date` - 往返旅行的返回日期（YYYY-MM-DD）
- `--cabin` - 航班等级（ECONOMY、PREMIUM_ECONOMY、BUSINESS、FIRST）
- `--stops` - 停靠次数（ANY、NON_STOP、ONE_STOP、TWO_STOPS）
- `--results` - 显示结果的数量（默认：5）

### 追踪航班
将航线添加到价格追踪列表中，并记录当前价格。

```bash
python skills/flight-tracker/scripts/track-flight.py LHR JFK 2025-07-01
python skills/flight-tracker/scripts/track-flight.py LHR JFK 2025-07-01 --target-price 400
python skills/flight-tracker/scripts/track-flight.py LHR JFK 2025-07-01 --return-date 2025-07-08 --cabin BUSINESS
```

参数：
与搜索航班的参数相同，另外需要提供：
- `--target-price` - 当价格低于此金额时触发警报

### 检查价格
定期检查所有被追踪航班的价格变化（建议使用 cron 任务自动执行）。

```bash
python skills/flight-tracker/scripts/check-prices.py
python skills/flight-tracker/scripts/check-prices.py --threshold 5
```

参数：
- `--threshold` - 触发警报的价格下降百分比（默认：10%）

输出：报告被追踪航班的价格变化情况，突出显示价格下降的情况，并在达到目标价格时发出警报。

### 列出被追踪的航班
显示所有被追踪的航班及其当前价格与原始价格。

```bash
python skills/flight-tracker/scripts/list-tracked.py
```

## 数据存储
价格历史数据存储在 `skills/flight-tracker/data/tracked.json` 文件中，并通过 R2 备份机制进行持久化。