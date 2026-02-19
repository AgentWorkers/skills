---
name: ryanair-fare-finder
description: 构建并解析 Ryanair 的机票查询 URL，用于搜索廉价航班。当用户希望从特定的英国机场出发、设置出发/返回时间窗口、选择过夜或多晚的旅行安排、按星期几筛选航班，或根据价格和货币限制搜索结果时，可以使用该功能。该系统支持所有机票查询参数，包括乘客人数、日期范围、灵活的日期设置以及促销代码。
compatibility: Requires network access to reach ryanair.com fare-finder pages.
metadata:
  author: Callum Kemp
  version: "1.0"
  base-url: "https://www.ryanair.com/gb/en/fare-finder"
---
# Ryanair 航班查询工具

根据用户需求，生成、修改并解释 Ryanair 的航班查询 URL。

## 基础 URL

```
https://www.ryanair.com/gb/en/fare-finder
```

以下所有参数均以查询字符串的形式（键值对）附加到基础 URL 后。

## 参数说明

### 航线信息

| 参数            | 类型    | 示例      | 说明                                                                                         |
|----------------------|---------|---------|----------------------------------------------------------------------------------------------|
| `originIata`         | string  | `MAN`   | 出发机场的 IATA 代码（例如：MAN、STN、LTN、EDI、BHX、LPL）。         |
| `destinationIata`    | string  | `ANY`   | 到达机场的 IATA 代码；或输入 `ANY` 以查询所有目的地。         |
| `isMacDestination`   | boolean | `false` | 当设置为 `true` 时，仅查询包含多个机场的城市目的地。         |

### 旅行类型

| 参数            | 类型    | 示例      | 说明                                                                                         |
|----------------------|---------|---------|----------------------------------------------------------------------------------------------|
| `isReturn`  | boolean | `true`  | `true` 表示往返旅行；`false` 表示单程旅行。         |

### 乘客信息

| 参数            | 类型    | 示例      | 说明                                                                                         |
|----------------------|---------|---------|----------------------------------------------------------------------------------------------|
| `adults`          | int      | `1`     | 成年乘客数量（16 岁及以上）。                         |
| `teens`          | int      | `0`     | 青少年乘客数量（12–15 岁）。                         |
| `children`        | int      | `0`     | 儿童乘客数量（2–11 岁）。                         |
| `infants`        | int      | `0`     | 婴儿乘客数量（2 岁以下）。                         |

### 日期范围

| 参数            | 类型    | 示例      | 说明                                                                                         |
|----------------------|---------|---------|----------------------------------------------------------------------------------------------|
| `dateOut`        | date    | `2026-02-01` | 搜索窗口的开始日期（YYYY-MM-DD）。                         |
| `dateIn`        | date    | `2027-01-31` | 搜索窗口的结束日期（YYYY-MM-DD）。                         |
| `isExactDate`     | boolean | `false`      | `true` 仅搜索指定日期；`false` 搜索整个日期范围。                         |

### 时间安排与灵活性

| 参数            | 类型    | 示例      | 说明                                                                                         |
|----------------------|---------|---------|----------------------------------------------------------------------------------------------|
| `dayOfWeek`      | enum    | `SATURDAY` | 将出发时间限制在特定星期六。可选值：`MONDAY` 到 `SUNDAY`。         |
| `isFlexibleDay`     | boolean | `false`     | 当设置为 `true` 时，Ryanair 会将出发时间范围放宽 1 天。         |

### 住宿时长

| 参数            | 类型    | 示例      | 说明                                                                                         |
|----------------------|---------|---------|----------------------------------------------------------------------------------------------|
| `daysTrip`        | int      | 总旅行天数（出发当天计为 1 天）。                         |
| `nightsFrom`       | int      | 在目的地的最低住宿天数。                         |
| `nightsTo`       | int      | 在目的地的最高住宿天数。                         |

### 出发/返回时间

| 参数            | 类型    | 示例      | 说明                                                                                         |
|----------------------|---------|---------|----------------------------------------------------------------------------------------------|
| `outboundFromHour`    | string | `00:00` | 可接受的最早出发时间。                         |
| `outboundToHour`    | string | `11:00` | 可接受的最晚出发时间。                         |
| `inboundFromHour`    | string | `13:00` | 可接受的最早返回时间。                         |
| `inboundToHour`    | string | `23:59` | 可接受的最晚返回时间。                         |

### 价格设置

| 参数            | 类型    | 示例      | 说明                                                                                         |
|----------------------|---------|---------|----------------------------------------------------------------------------------------------|
| `currency`      | string | `GBP`   | 货币代码（例如：GBP、EUR 等）。                         |
| `priceValueTo`     | int      | 最高总返回票价。留空表示无价格限制。                     |
| `promoCode`      | string | *(空)*   | Ryanair 的促销代码（如有）。                         |

## 示例：从曼彻斯特出发的周末过夜旅行

以下 URL 用于查询从曼彻斯特到任意目的地的往返航班：
- 出发时间为周六上午，
- 返回时间为当天下午或次日傍晚，
- 航行日期为全年任意时间，
- 总票价需低于 80 英镑：

```
https://www.ryanair.com/gb/en/fare-finder?originIata=MAN&destinationIata=ANY&isReturn=true&isMacDestination=false&promoCode=&adults=1&teens=0&children=0&infants=0&dateOut=2026-02-01&dateIn=2027-01-31&daysTrip=1&nightsFrom=0&nightsTo=1&dayOfWeek=SATURDAY&isExactDate=false&outboundFromHour=00:00&outboundToHour=11:00&inboundFromHour=13:00&inboundToHour=23:59&priceValueTo=80&currency=GBP&isFlexibleDay=false
```

### 这些时间安排为何适合过夜旅行：

- **出发时间：00:00–11:00** — 可确保在目的地有充足的时间进行一日或一晚的停留。
- **返回时间：13:00–23:59** — 可在次日退房/午餐后返回家中。

## 从零开始构建 URL 的步骤：

1. 以基础 URL 为起点。
2. 设置 `originIata` 为用户的出发机场 IATA 代码。
3. 设置 `destinationIata` 为具体的目的地 IATA 代码或 `ANY`。
4. 根据旅行类型选择 `isReturn` 的值（`true` 表示往返，`false` 表示单程）。
5. 输入乘客数量（`adults`、`teens`、`children`、`infants`）。
6. 使用 `dateOut` 和 `dateIn` 定义搜索日期范围。
7. 选择出发星期，并设置 `isExactDate` 为 `false` 以查询所有符合条件的日期。
8. 设置住宿时长（`daysTrip`、`nightsFrom`、`nightsTo`）。
9. 根据需要设置出发/返回时间。
10. 设置货币代码（`currency`）和可选的价格上限（`priceValueTo`）。
11. 如果用户有促销代码，可以添加 `promoCode`。

## 英国常见的出发机场

| IATA | 机场名称            |
|------|---------------------|
| MAN  | 曼彻斯特          |
| STN  | 伦敦斯坦斯特德         |
| LTN  | 伦敦卢顿           |
| LGW  | 伦敦盖特威克         |
| EDI  | 爱丁堡           |
| BHX  | 伯明翰           |
| LPL  | 利物浦           |
| BRS  | 布里斯托尔           |
| EMA  | 东米德兰兹         |
| GLA  | 格拉斯哥           |
| BFS  | 贝尔法斯特国际         |
| LBA  | 利兹布拉德福德         |
| NCL  | 纽卡斯尔           |
| ABZ  | 阿伯丁           |