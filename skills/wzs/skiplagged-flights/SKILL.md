---
name: skiplagged-flights
description: >
  **使用场景：**  
  当用户请求“查找航班”、“比较行程安排”、“搜索偏远城市的航线”、“查询最便宜的出行日期”、“探索目的地”、“搜索酒店”、“规划旅行”等与航班或旅行相关的操作时，本功能会以 Skiplagged 的官方 MCP（My Flight Planner）结果作为输出。
homepage: https://skiplagged.com
metadata: {"openclaw":{"emoji":"✈️","homepage":"https://skiplagged.com","requires":{"bins":["mcporter"]},"install":[{"id":"node","kind":"node","package":"mcporter","bins":["mcporter"],"label":"Install mcporter (node)"}]}}
---
# Skiplagged Flights (MCP)

该技能通过查询 **Skiplagged 的公共 MCP 服务器** 来搜索航班、酒店、汽车以及灵活的日期安排信息。

- **服务器地址：** `https://mcp.skiplagged.com/mcp`
- **认证方式：** 无需认证（公共服务器）

## 先决条件

1) 确保 `mcporter` CLI 已经添加到系统的 PATH 环境变量中（该技能将其列为必需的运行工具）。

2) 建议使用 **自定义的 HTTPS 请求**（无需配置本地的 `mcporter` 配置文件）：

```bash
# Inspect tools + schemas (recommended)
mcporter list https://mcp.skiplagged.com/mcp --schema
```

## 快速入门

```bash
mcporter call https://mcp.skiplagged.com/mcp.sk_flights_search origin=WAW destination=LHR departureDate=2026-03-15 --output json
```

> 如果您的环境中已经配置了 `skiplagged` 作为服务器名称，那么可以使用 `mcporter call skiplagged.sk_flights_search ...` 来执行相同操作。使用显式的 HTTPS 地址更为推荐，因为它可以避免依赖或查看本地的 MCP 配置文件。

## 工具

### sk_flights_search

用于搜索两个地点之间的航班信息。

**必需参数：** `origin`（出发地）、`destination`（目的地）、`departureDate`（出发日期）

**常用选项（请通过 `--schema` 参数确认具体含义）：**

* `returnDate` - 往返日期
* `sort` - 排序方式（`price`、`duration`、`value`，默认为 `value`）
* `limit` - 最大返回结果数量（默认为 12 条）
* `maxStops` - 停靠次数（`none`、`one`、`many`）
* `fareClass` - 航班等级（`basic-economy`、`economy`、`premium`、`business`、`first`）
* `preferredAirlines` / `excludedAirlines` - 以逗号分隔的 IATA 航空公司代码（例如 `UA,DL`）
* `departureTimeEarliest` / `departureTimeLatest` - 起飞时间（以分钟为单位，范围为 `0–1439`）

**示例：**

```bash
# Cheapest one-way
mcporter call https://mcp.skiplagged.com/mcp.sk_flights_search origin=NYC destination=LAX departureDate=2026-03-15 sort=price limit=5

# Round-trip, nonstop only
mcporter call https://mcp.skiplagged.com/mcp.sk_flights_search origin=WAW destination=CDG departureDate=2026-04-10 returnDate=2026-04-17 maxStops=none limit=5

# Exclude budget airlines, morning only (6am–12pm)
mcporter call https://mcp.skiplagged.com/mcp.sk_flights_search origin=LHR destination=JFK departureDate=2026-05-01 excludedAirlines=F9,NK departureTimeEarliest=360 departureTimeLatest=720 limit=5
```

### sk_flex_departure_calendar

用于查找指定出发日期附近的最低票价。

```bash
mcporter call https://mcp.skiplagged.com/mcp.sk_flex_departure_calendar origin=WAW destination=BCN departureDate=2026-06-15 sort=price --output json
```

### sk_flex_return_calendar

用于查找固定行程长度内的最低往返票价。

```bash
mcporter call https://mcp.skiplagged.com/mcp.sk_flex_return_calendar origin=WAW destination=NYC departureDate=2026-07-01 returnDate=2026-07-08 --output json
```

### sk_destinations_anywhere

用于在日期安排灵活的情况下寻找便宜的目的地。

```bash
mcporter call https://mcp.skiplagged.com/mcp.sk_destinations_anywhere from=WAW depart=2026-03-15 --output json
```

## 结果展示格式

在向用户展示结果时，请注意以下几点：

* **不要使用 Markdown 表格**，而是使用项目符号列表或带标签的文本格式。
* 在 Telegram 风格的聊天频道中回复时，请使用兼容 MarkdownV2 的格式。
* 保持回复内容简洁、易于阅读（适合移动设备）。
* 默认显示前 3–5 个最优选项，并提供展开查看的链接。
* 返回的结果中应包含预订链接。
* 如果出现包含隐藏城市的行程安排，请明确说明相关限制（如行李携带限制或错过中转站可能带来的问题）。
* 强调票价优惠、航线选择以及关键权衡因素（如停靠次数、行程时长和价格）。

**示例回复：**

```
Found 3 flights WAW → LHR on Mar 15:

• $90 · 2h 35m · nonstop
  LOT
  05:40 WAW → 07:15 LHR
  [Book](link)

• $91 · 4h 20m · 1 stop
  SAS
  06:10 WAW → 09:30 LHR
  [Book](link)
```

## 使用技巧

* 尽可能使用 IATA 航空公司代码（例如 `WAW`、`LHR`、`JFK`）。
* 如果需要结构化的数据进行后续处理，请使用 `--output json` 选项。
* 结果中通常会包含用于预订或验证的链接（`deepLink`）。
* 如果查询失败（非因无结果导致），建议直接访问 `https://skiplagged.com` 查看详细信息。
* 价格和可用性可能会随时变化，请将结果视为即时信息，并鼓励用户通过预订链接进行确认。

## 参考资料 / 来源

* Skiplagged MCP 的官方文档及隐私政策：[https://skiplagged.github.io/mcp/](https://skiplagged.github.io/mcp/)
* MCPorter CLI 的使用说明及自定义 URL 格式：[https://raw.githubusercontent.com/steipete/mcporter/main/README.md](https://raw.githubusercontent.com/steipete/mcporter/main/README.md)