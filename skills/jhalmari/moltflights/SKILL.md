---
name: moltflights
description: 通过 MoltFlights API 搜索廉价航班。查找优惠信息、比较价格、追踪航线，并设置价格提醒。
homepage: https://moltflights.com
metadata:
  openclaw:
    emoji: "✈️"
    keywords: [travel, flights, cheap-flights, search, booking, price-alerts, digital-nomad]
tools:
  moltflights_search:
    description: Search for flights between two airports. Returns real-time prices with direct booking links.
    url: https://moltflights.com/api/search
    method: GET
    parameters:
      type: object
      properties:
        origin:
          type: string
          description: "IATA airport code for departure (e.g. HEL, JFK, LHR)"
        destination:
          type: string
          description: "IATA airport code for arrival (e.g. BKK, NRT, BCN)"
        date:
          type: string
          description: "Departure date YYYY-MM-DD. Omit for cheapest flights across the month."
        returnDate:
          type: string
          description: "Return date YYYY-MM-DD for round-trips. Omit for one-way."
        adults:
          type: integer
          description: "Number of adults 1-9 (default: 1)"
        children:
          type: integer
          description: "Number of children ages 2-12, 0-8 (default: 0)"
        infants:
          type: integer
          description: "Number of infants under 2, 0-8 (default: 0)"
      required: [origin, destination]
  moltflights_autocomplete:
    description: Look up IATA airport codes by city or airport name.
    url: https://moltflights.com/api/autocomplete
    method: GET
    parameters:
      type: object
      properties:
        term:
          type: string
          description: "City or airport name to search (min 2 characters)"
      required: [term]
---

# MoltFlights — 航班搜索技能

使用 [MoltFlights API](https://moltflights.com/agents) 搜索廉价航班。该 API 返回包含实时价格和直接预订链接的结构化 JSON 数据。

无需 API 密钥，也无需身份验证，只需调用相应的接口即可。

---

## 工具

### `moltflights_search` — 搜索航班

```
GET https://moltflights.com/api/search?origin=HEL&destination=BKK&date=2026-03-15
```

| 参数          | 是否必填 | 类型     | 描述                                      |
|---------------|---------|--------|-----------------------------------------|
| `origin`      | 是      | 字符串    | IATA 机场代码（例如：`HEL`）                      |
| `destination` | 是      | 字符串    | IATA 机场代码（例如：`NRT`）                      |
| `date`        | 否       | 字符串    | 出发日期（格式：`YYYY-MM-DD`）                      |
| `returnDate`  | 否       | 字符串    | 返回日期（格式：`YYYY-MM-DD`，往返行程）             |
| `adults`      | 否       | 整数     | 成年乘客人数（1–9 人，默认值：1）                   |
| `children`    | 否       | 整数     | 2–12 岁儿童人数（0–8 人，默认值：0）                   |
| `infants`     | 否       | 整数     | 2 岁以下婴儿人数（0–8 人，默认值：0）                   |

如果省略 `date` 参数，API 会返回下个月最便宜的航班信息。

### `moltflights_autocomplete` — 查找机场代码

```
GET https://moltflights.com/api/autocomplete?term=bangkok
```

| 参数          | 是否必填 | 类型     | 描述                                      |
|---------------|---------|--------|-----------------------------------------|
| `term`        | 是      | 字符串    | 城市或机场名称（至少 2 个字符）                         |

---

## 示例：搜索航班

```bash
curl "https://moltflights.com/api/search?origin=HEL&destination=BKK&date=2026-03-15"
```

### 响应数据

```json
{
  "meta": {
    "source": "MoltFlights",
    "origin": "HEL",
    "destination": "BKK",
    "date": "2026-03-15",
    "adults": 1,
    "children": 0,
    "infants": 0,
    "results": 12
  },
  "data": [
    {
      "airline": "Finnair",
      "flight_number": "809",
      "price": "€432",
      "price_per_person": "€432",
      "departure": "2026-03-15T10:30:00",
      "return_at": "",
      "transfers": 1,
      "origin": "HEL",
      "destination": "BKK",
      "book_link": "https://www.aviasales.com/search/..."
    }
  ]
}
```

每个搜索结果都包含一个 `book_link`，用户可以直接使用该链接进行预订。

---

## 示例：包含乘客的往返行程

```bash
curl "https://moltflights.com/api/search?origin=JFK&destination=CDG&date=2026-06-01&returnDate=2026-06-15&adults=2&children=1"
```

`price` 字段显示所有乘客的总票价，`price_per_person` 字段显示每位乘客的单价。

---

## 常见使用场景

### 1. 查找前往目的地的最便宜航班

不指定具体日期，即可获取整个月内最便宜的航班选项：

```bash
curl "https://moltflights.com/api/search?origin=LHR&destination=TYO"
```

### 2. 比较不同日期的票价

对多个日期进行搜索并比较价格：

```bash
for date in 2026-04-01 2026-04-08 2026-04-15; do
  echo "=== $date ==="
  curl -s "https://moltflights.com/api/search?origin=HEL&destination=BKK&date=$date" | head -20
done
```

### 3. 价格监控/提醒（定时任务）

每天检查某条航线的价格，当价格低于设定阈值时发送提醒：

```bash
# Run daily via cron: 0 8 * * * /path/to/check-price.sh
PRICE=$(curl -s "https://moltflights.com/api/search?origin=HEL&destination=BKK&date=2026-05-01" \
  | grep -o '"price":"€[0-9]*"' | head -1 | grep -o '[0-9]*')

if [ "$PRICE" -lt 400 ]; then
  echo "Deal found: HEL→BKK for €$PRICE"
fi
```

### 4. 多城市搜索

搜索多条航线并选择最便宜的航班：

```bash
for dest in BKK TYO BCN LIS; do
  echo "=== HEL → $dest ==="
  curl -s "https://moltflights.com/api/search?origin=HEL&destination=$dest" \
    | grep -o '"price":"€[0-9]*"' | head -1
done
```

---

## 常见 IATA 机场代码

| 代码       | 所在城市    | 代码       | 所在城市    |
|------------|---------|---------|-----------|
| HEL        | 赫尔辛基    | LHR       | 伦敦        |
| JFK        | 纽约      | CDG       | 巴黎        |
| NRT        | 成田机场   | BKK       | 曼谷        |
| BCN        | 巴塞罗那   | FCO       | 罗马        |
| SIN        | 新加坡     | DXB       | 迪拜        |
| LAX        | 洛杉矶     | SFO       | 旧金山      |
| BER        | 柏林      | AMS       | 阿姆斯特丹     |
| IST        | 伊斯坦布尔   | LIS       | 里斯本        |

不知道机场代码？可以使用 `moltflights_autocomplete` 工具查询：

```bash
curl "https://moltflights.com/api/autocomplete?term=bangkok"
```

---

## 错误处理

- **400**：缺少 `origin` 或 `destination` 参数
- **`data` 数组为空**：未找到该航线/日期的航班信息。请尝试其他日期或省略日期以进行灵活搜索。

---

## 提示

- 价格以欧元（€）为单位
- 结果按日期排序：首先显示匹配的日期，然后按价格排序相近的日期
- 省略 `date` 参数可获取下个月内最便宜的航班
- 该 API 免费使用，无需身份验证
- 响应数据会缓存 5 分钟