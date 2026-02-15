---
name: skiplagged-flights
description: 通过 Skiplagged MCP 搜索最便宜的航班。该平台可用于查找优惠机票、比较价格、选择灵活的出行日期以及探索目的地信息。
---

# Skiplagged 航班搜索

通过 `mcporter` 使用 Skiplagged MCP 搜索航班。

## 快速入门

```bash
mcporter call skiplagged.sk_flights_search origin=WAW destination=LHR departureDate=2026-02-15
```

## 工具

### `sk_flights_search`
在指定地点之间搜索航班。

**必需参数：**
- `origin`（起点）
- `destination`（目的地）
- `departureDate`（出发日期）

**常用选项：**
- `returnDate`（返程日期）
- `sort`（排序方式）：`price`（价格）、`duration`（航程时长）、`value`（性价比，默认）
- `limit`（结果数量上限，默认为 12）
- `maxStops`（中途停留次数）：`none`（无）、`one`（一次）、`many`（多次）
- `fareClass`（舱位等级）：`basic-economy`（经济舱）、`economy`（经济舱）、`premium`（高级经济舱）、`business`（商务舱）、`first`（头等舱）
- `preferredAirlines`/`excludedAirlines`（优先/排除的航空公司，例如：`['UA','DL']`）
- `departureTimeEarliest`/`departureTimeLatest`（出发时间范围）：以午夜为基准的分钟数（0-1439）

**示例：**
```bash
# Cheapest one-way
mcporter call skiplagged.sk_flights_search origin=NYC destination=LAX departureDate=2026-03-15 sort=price

# Round-trip, nonstop only
mcporter call skiplagged.sk_flights_search origin=WAW destination=CDG departureDate=2026-04-10 returnDate=2026-04-17 maxStops=none

# Exclude budget airlines, morning only (6am-12pm)
mcporter call skiplagged.sk_flights_search origin=LHR destination=JFK departureDate=2026-05-01 excludedAirlines=F9,NK departureTimeEarliest=360 departureTimeLatest=720
```

### `sk_flex_departure_calendar`
查找指定出发日期附近的最低票价。

```bash
mcporter call skiplagged.sk_flex_departure_calendar origin=WAW destination=BCN departureDate=2026-06-15 sort=price
```

### `sk_flex_return_calendar`
查找固定航程长度下的最低往返票价。

```bash
mcporter call skiplagged.sk_flex_return_calendar origin=WAW destination=NYC departureDate=2026-07-01 returnDate=2026-07-08
```

### `sk_destinations_anywhere`
在出行时间灵活的情况下，寻找便宜的目的地。

```bash
mcporter call skiplagged.sk_destinations_anywhere from=WAW depart=2026-02-15
```

## 结果展示格式

向用户展示航班结果时，请注意：
- **切勿使用 Markdown 表格**，而应使用项目符号列表或带标签的文本。
- 采用与 MarkdownV2 兼容的格式（适用于 Telegram）。
- 保持回复内容简洁、易于阅读（适合移动设备）。
- 仅显示前 3-5 条结果，如有需要可提供更多信息。

**示例：**
```
Found 3 flights WAW → LHR on Feb 15:

• $90 · 28h 15m · 1 stop
  Wizz Air + SAS
  05:40 WAW → 08:55+1 LHR
  [Book](link)

• $91 · 12h 20m · 1 stop
  Wizz Air + SAS  
  05:40 WAW → 17:00 LHR
  [Book](link)
```

## 提示：
- 使用 IATA 代码（例如：`WAW`、`LHR`、`JFK`）。
- 系统默认会包含途经隐藏城市的航班（这些航班通常价格更低）。
- 使用 `--output json` 参数可获取结构化数据。
- 结果中包含用于预订的 `deepLink`。

## 参考资料：
- 工具架构：`mcporter list skiplagged --schema`
- MCP 文档：https://skiplagged.github.io/mcp/