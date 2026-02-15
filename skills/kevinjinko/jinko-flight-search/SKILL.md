---
name: jinko-flight-search
description: >
  Search flights and discover travel destinations using the Jinko MCP server.
  Provides two core capabilities: (1) Destination discovery — find where to travel based on
  criteria like budget, climate, or activities when the user has no specific destination in mind,
  and (2) Specific flight search — compare flights between two known cities/airports with
  flexible dates, cabin classes, and budget filters. Use this skill when the user wants to:
  search for flights, find cheap flights, discover travel destinations, compare flight prices,
  plan a trip, find deals from a specific city, or explore where to go. Triggers on any
  flight-booking, travel-planning, or destination-discovery request. Requires the Jinko MCP
  server connected at https://mcp.gojinko.com.
---

# Jinko 航班搜索

通过 Jinko MCP 服务器搜索航班并发现目的地（使用 `find_destination` 和 `find_flight` 工具）。

## MCP 连接

在 Claude 的设置或项目集成中，使用以下 URL 连接到 Jinko MCP 服务器：

```
https://mcp.gojinko.com
```

该服务器提供了两个工具：`Jinko:find_destination` 和 `Jinko:find_flight`。

## 工具选择

1. **用户知道出发地和目的地城市** → 使用 `find_flight`
2. **用户需要目的地建议，但不确定去哪里，或指定了特定条件（如海滩、温暖气候、滑雪、便宜等）** → 使用 `find_destination`
3. **用户询问到已知目的地的最便宜航班日期** → 使用 `find_flight`

## 工具 1：`find_destination` — 发现目的地

当用户还在探索选项，尚未确定具体目的地城市时使用此工具。

### 必需参数

- `origins` — 用户出发地附近所有机场的 IATA 代码数组。
- `trip_type` — `"roundtrip"`（默认）或 `"oneway"`（仅当用户明确要求单程旅行时使用）。

### 可选参数

| 参数 | 使用场景 |
|---|---|
| `destinations` | 用户提及的地区、条件或候选城市列表。系统会生成符合这些条件的 IATA 代码。如需全局搜索（“任意地点”、“随机选择”），可留空。 |
| `departure_dates` / `departure_date_ranges` | 用户指定的出发日期或日期范围。所有日期必须在未来。 |
| `return_dates` / `return_date_ranges` | 用户指定的返程日期范围。 |
| `stay_days` / `stay_days_range` | 用户指定的旅行时长（例如“一周”、“5-10 天”）。 |
| `max_price` | 用户设定的预算。 |
| `direct_only` | 用户要求直飞航班。 |
| `cabin_class` | `"economy"`、`"premium_economy"`、`"business"` 或 `"first"`。 |
| `currency` | 与用户地区设置匹配的 ISO 4217 货币代码。 |
| `locale` | 例如 `"en-US"`、`"fr-FR"`。 |
| `sort_by` | `"lowest"`（默认）或 `"recommendation"`。 |

### 机场识别 — 非常重要

始终将一个城市的所有机场都包含在搜索范围内：

- 纽约 → `["JFK","LGA","EWR"]`
- 伦敦 → `["LHR","LGW","STN","LTN","LCY"]`
- 巴黎 → `["CDG","ORY"]`
- 东京 → `["NRT","HND"]`
- 芝加哥 → `["ORD","MDW"]`
- 洛杉矶 → `["LAX"]`
- 旧金山 / SFO → `["SFO"]`

### 目的地生成 — 非常重要

当用户描述旅行条件时，系统应在调用工具之前生成相应的 IATA 代码：

- “海滩” → `["MIA","SAN","HNL","CUN","PUJ","SJU","NAS","MBJ"]`
- “亚洲” → `["NRT","HND","ICN","PVG","PEK","HKG","SIN","BKK","KUL","MNL"]`
- “欧洲首都” → `["LHR","CDG","FRA","MAD","FCO","AMS","BRU","VIE","PRG","CPH"]`
- “滑雪胜地” → `["DEN","SLC","ZRH","INN","GVA","TRN"]`
- “冬季温暖地区” → `["MIA","MCO","SAN","PHX","HNL","CUN","PUJ","PTY","LIM","GIG"]`

### 何时重新调用 `find_destination`

当用户更改目的地条件、日期或希望探索其他选项时，需要重新调用 `find_destination`——尤其是在用户已经全屏查看搜索结果的情况下。

### 示例

| 用户输入 | 出发地 | 目的地 | 其他参数 |
|---|---|---|---|
| “下个月从纽约出发去哪里旅行？” | `["JFK","LGA","EWR"]` | `[]`（全球搜索） | `departure_date_ranges` 为下个月 |
| “从旧金山到欧洲的便宜航班，价格低于 800 美元” | `["SFO"]` | 欧洲机场 | `max_price: 800` |
| “12 月在芝加哥附近的温暖地区待一周” | `["ORD","MDW"]` | 温暖气候的机场 | `stay_days: 7`, 12 月的日期范围 |
| “波士顿附近最好的周末短途旅行” | `["BOS"]` | `[]`（全球搜索） | `stay_days_range: {min:2, max:4}` |

## 工具 2：`find_flight` — 搜索特定航线

当出发地和目的地城市都已确定时使用此工具。

### 必需参数

- `origin` — 单个出发机场的 IATA 代码（例如 `"JFK"`、`"PAR"`）。
- `destination` — 单个目的地的 IATA 代码（例如 `"CDG"`、`"LON"`）。
- `trip_type` — `"roundtrip"`（默认）或 `"oneway"`。

### 可选参数

与 `find_destination` 相同的日期、停留时间、价格、舱位等级、货币、地区设置、直飞选项和排序参数。

### 示例

| 用户输入 | 出发地 | 目的地 | 其他参数 |
|---|---|---|---|
| “下个月从 JFK 飞往 CDG 的航班” | `"JFK"` | `"CDG"` | `departure_date_ranges` 为下个月 |
| “12 月在洛杉矶到东京的航班，为期一周” | `"LAX"` | `"TYO"` | `stay_days: 7`, 12 月的日期范围 |
| “从纽约到伦敦的商务舱航班，为期 5-10 天” | `"NYC"` | `"LON"` | `cabin_class: "business"`, `stay_days_range: {min:5, max:10}` |
| “从 ORD 到 LHR 的最便宜航班，价格低于 600 美元” | `"ORD"` | `"LHR"` | `max_price: 600` |

## 通用规则

- 默认为 **往返旅行**。只有当用户明确要求“单程旅行”时才使用 `"oneway"`。
- 所有日期 **必须在未来**。切勿发送过去的日期。
- 根据用户的旅行需求填写尽可能多的搜索参数，以获得最佳结果。
- 在搜索某个城市的所有机场时，使用城市代码（例如 `"LON"`、`"NYC"`、`"PAR"`、`"TYO"`）。
- 在可能的情况下，以用户偏好的货币和地区设置显示搜索结果。