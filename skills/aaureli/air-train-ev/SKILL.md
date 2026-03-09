---
name: air-train-ev
description: Unified travel + mobility skill: (1) flight pricing with Amadeus (flight offers), (2) public transport/train journey planning with Navitia (journeys, departures), and (3) find nearby EV charge points using Open Charge Map. Use when Alessandro asks for flight prices, train itineraries/schedules, or EV charging stations.
---

# 航空 + 火车 + 电动汽车

## 凭据（环境变量）
切勿在脚本中硬编码密钥。

### 航班（Amadeus）
- `AMADEUS_CLIENT_ID`
- `AMADEUS_CLIENT_SECRET`
- 可选：`AMADEUS_HOST`（默认值：`https://api.amadeus.com`）

### 火车/公共交通（Navitia）
- `NAVITIA_TOKEN`
- 可选：`NAVITIA_HOST`（默认值：`https://api.navitia.io`）
- 可选：`NAVITIA_COVERAGE`（默认值：`sandbox`）

### 电动汽车充电站（Open Charge Map）
- `OPENCHARGEMAP_API_KEY`
- 可选：`OPENCHARGEMAP_HOST`（默认值：`https://api.openchargemap.io`）

## 航班——快速使用方法
```bash
python3 skills/air-train-ev/scripts/flight_offers.py \
  --origin ZRH --destination IST \
  --departure 2026-03-10 \
  --adults 1 --travel-class ECO \
  --non-stop true \
  --included-airlines PC,VF,TK \
  --max 6
```

输出格式固定：
- 日期/时间：`DD/MM/YY HH:MM`
- 欧元价格使用 `€` 表示

## 火车行程——快速使用方法
```bash
python3 skills/air-train-ev/scripts/navitia.py coverage
python3 skills/air-train-ev/scripts/navitia.py places --q "Strasbourg"
python3 skills/air-train-ev/scripts/navitia.py journeys --from "Strasbourg" --to "Rennes" --datetime "2026-03-07T08:00:00" --count 5
```

## 电动汽车充电站——快速使用方法
```bash
python3 skills/air-train-ev/scripts/ev_charge_points.py \
  --lat 48.5839 --lon 7.7455 \
  --km 5 --max 10
```

注意事项：
- 该功能使用 Open Charge Map 的 `GET /v3/poi/` API。
- 返回的结果包括充电站运营商/名称、地址、距离（如有提供）、连接器类型以及坐标信息。