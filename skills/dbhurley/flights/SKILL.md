---
name: flights
description: 跟踪航班状态、延误情况，并搜索航线。该工具使用 FlightAware 提供的数据。
homepage: https://flightaware.com
metadata: {"clawdis":{"emoji":"✈️","requires":{"bins":[],"env":[]}}}
---

# 飞行技能

使用 FlightAware 数据来跟踪航班状态、搜索航线以及监控航班延误情况。

## 快速命令

```bash
cd skills/flights

# Search flights by route
uv run python scripts/flights.py search PVD ORF --airline MX

# Get specific flight status
uv run python scripts/flights.py status MXY704
```

## 使用示例

**搜索从 PVD 到 ORF 的 Breeze 航班：**
```bash
flights.py search PVD ORF --airline MX
```

**查询特定航班：**
```bash
flights.py status AA100
flights.py status MXY704 --date 2026-01-08
```

## 输出格式

```json
{
  "flight": "MXY704",
  "airline": "Breeze Airways",
  "origin": "PVD",
  "destination": "ORF",
  "departure": "Thu 05:04PM EST",
  "arrival": "06:41PM EST",
  "status": "Scheduled / Delayed",
  "aircraft": "BCS3"
}
```

## 状态值

- `Scheduled` - 航班准点
- `Scheduled / Delayed` - 预计延误
- `En Route / On Time` - 已在飞行中且准点
- `En Route / Delayed` - 已在飞行中但延误
- `Arrived / Gate Arrival` - 已降落并到达登机口
- `Cancelled` - 航班取消

## 航空公司代码

| 代码 | 航空公司 |
|------|---------|
| MX/MXY | Breeze Airways |
| AA | American Airlines |
| DL | Delta Air Lines |
| UA | United Airlines |
| WN | Southwest Airlines |
| B6 | JetBlue Airways |

## 可选：AviationStack API

如需更详细的数据，请设置 `AVIATIONSTACK_API_KEY`（免费 tier 可在 aviationstack.com 获取）。

## 依赖项

```bash
cd skills/flights && uv sync
```