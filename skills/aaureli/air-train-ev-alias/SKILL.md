---
name: air_train_ev
description: Alias of air-train-ev. Unified travel + mobility skill: (1) flight pricing with Amadeus (flight offers), (2) public transport/train journey planning with Navitia (journeys, departures), and (3) find nearby EV charge points using Open Charge Map. Use when Alessandro asks for flight prices, train itineraries/schedules, or EV charging stations.
---

# 别名 — air_train_ev → air-train-ev

此技能是以下官方技能的**别名**：
- `skills/air-train-ev/SKILL.md`

请使用相同的脚本（避免重复逻辑）：
- 航班查询（Amadeus）：`skills/air-train-ev/scripts/flight_offers.py`
- 火车/PT查询（Navitia）：`skills/air-train-ev/scripts/navitia.py`
- 电动汽车充电站查询（Open Charge Map）：`skills/air-train-ev/scripts/ev_charge_points.py`

## 凭据（环境变量）
与 `air-train-ev` 相同：
- `AMADEUS_CLIENT_ID`
- `AMADEUS_CLIENT_SECRET`
- `NAVITIA_TOKEN`
- `OPENCHARGEMAP_API_KEY`