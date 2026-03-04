---
name: flight-price-plus
description: >
  **航班价格查询功能**  
  当用户询问航班信息、机票价格、最便宜的出行日期、价格变动情况、出发时间，或是单程/往返旅行选项时，该功能会立即被触发。该功能支持中文和英文输入，能够自动将城市名称转换为IATA机场代码，并支持单程、往返旅行以及多日期价格对比的查询需求。此外，当用户说出类似“我想去XX”并提及乘飞机出行时，该功能也会被触发。
---
# ✈️ 航班搜索技能

通过 51smart API (`skill.flight.51smart.com`) 查询实时航班信息。支持单程、往返以及价格日历功能。

> **注意：** 该技能通过 HTTP POST 直接调用上述公共 API，无需任何本地脚本或身份验证。用户提供的信息（城市/日期）仅用于航班搜索。

---

## 工作流程

1. **解析用户输入** → 提取出发地、目的地、日期、乘客人数、舱位等级和旅行类型。
2. **补充缺失信息** → 询问用户是否有任何必填字段缺失。
3. **调用 API** → 直接发送 POST 请求到 `https://skill.flight.51smart.com/api/search`。
4. **格式化输出** → 以清晰、结构化的形式显示搜索结果。

---

## 第一步：解析用户输入

| 字段 | 描述 | 默认值 | 是否必填 |
|-------|-------------|---------|----------|
| fromCity | 出发城市的 IATA 代码 | — | ✅ |
| toCity | 目的地城市的 IATA 代码 | — | ✅ |
| fromDate | 出发日期（YYYY-MM-DD） | — | ✅ |
| returnDate | 返回日期（YYYY-MM-DD） | — | 往返旅行时必填 |
| adultNumber | 成人乘客人数 | 1 | — |
| childNumber | 儿童乘客人数 | 0 | — |
| cabinClass | 舱位等级（E/B/F/P） | E | — |
| flightType | 单程/往返 | 单程 | — |

**舱位等级说明：**
- `E` = 经济舱
- `P` = 高级经济舱
- `B` = 商务舱
- `F` = 头等舱

---

## 将城市名称转换为 IATA 代码

### 中国城市
| 城市 | IATA 代码 | 城市 | IATA 代码 |
|------|------|------|------|
| 北京 | PEK/PKX | 上海虹桥 | SHA |
| 上海浦东 | PVG | 广州 | CAN |
| 深圳 | SZX | 成都 | CTU |
| 杭州 | HGH | 南京 | NKG |
| 武汉 | WUH | 西安 | XIY |
| 重庆 | CKG | 厦门 | XMN |
| 昆明 | KMG | 三亚 | SYX |
| 海口 | HAK | 青岛 | TAO |
| 郑州 | CGO | 长沙 | CSX |
| 济南 | TNA | 哈尔滨 | HRB |
| 沈阳 | SHE | 大连 | DLC |
| 天津 | TSN | 合肥 | HFE |
| 贵阳 | KWE | 南宁 | NNG |
| 乌鲁木齐 | URC | 拉萨 | LXA |

### 国际城市
| 城市 | IATA 代码 | 城市 | IATA 代码 |
|------|------|------|------|
| 香港 | HKG | 台北 | TPE |
| 澳门 | MFM | 东京成田 | NRT |
| 东京羽田 | HND | 大阪 | KIX |
| 首尔 | ICN | 釜山 | PUS |
| 新加坡 | SIN | 曼谷素万那比米 | BKK |
| 曼谷唐慕昂 | DMK | 吉隆坡 | KUL |
| 雅加达 | CGK | 马尼拉 | MNL |
| 悉尼 | SYD | 墨尔本 | MEL |
| 迪拜 | DXB | 阿布扎比 | AUH |
| 伦敦希思罗 | LHR | 伦敦盖特威克 | LGW |
| 巴黎 | CDG | 法兰克福 | FRA |
| 阿姆斯特丹 | AMS | 罗马 | FCO |
| 纽约肯尼迪 | JFK | 纽约纽瓦克 | EWR |
| 洛杉矶 | LAX | 旧金山 | SFO |
| 拉斯维加斯 | LAS | 芝加哥 | ORD |
| 温哥华 | YVR | 多伦多 | YYZ |

> 对于未列出的城市，根据常见规则推断其 IATA 代码，或请求用户确认完整的机场名称。

---

## 第三步：调用 API

直接发送 HTTP POST 请求 — **无需任何本地脚本**。

**请求地址：** `POST https://skill.flight.51smart.com/api/search`
**请求头内容类型：** `application/json`
**认证方式：** 不需要认证

### 单程请求示例

```json
{
  "adultNumber": 1,
  "cabinClass": "E",
  "childNumber": 0,
  "cid": "123456",
  "flightType": "oneWay",
  "flights": [
    {
      "fromCity": "PEK",
      "fromDate": "2026-03-15",
      "toCity": "SHA"
    }
  ]
}
```

### 往返请求示例

```json
{
  "adultNumber": 2,
  "cabinClass": "B",
  "childNumber": 1,
  "cid": "123456",
  "flightType": "roundTrip",
  "flights": [
    { "fromCity": "PEK", "fromDate": "2026-03-15", "toCity": "NRT" },
    { "fromCity": "NRT", "fromDate": "2026-03-22", "toCity": "PEK" }
  ]
}
```

### 价格日历

通过连续发送多条单程请求并汇总结果来获取价格日历信息。

---

## 第四步：格式化输出

### 单程/往返航班结果

```
✈️ Beijing (PEK) → Shanghai (SHA)
📅 Mar 15, 2026  |  Economy  |  Adult × 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 #  Flight      Depart→Arrive       Duration  Stops   Price (USD)  Baggage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1  UA1597      22:38→00:06(+1)     1h28m     Nonstop $81.86       1PC/23KG
 2  CA1234      09:00→11:20         2h20m     Nonstop $95.00       1PC/23KG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2 flights found
Lowest: $81.86 (before tax), incl. tax: $116.80
```

### 价格日历结果

```
📅 Price Calendar
✈️ Shanghai (SHA) → Los Angeles (LAX)  |  Economy

Date            Lowest          Flights
─────────────────────────────────────
2026-04-01      $520.00 ⭐       8
2026-04-02      $490.00 🏆 Best  6
2026-04-03      $535.00          7
2026-04-04      $510.00          5
2026-04-05      $580.00          6
─────────────────────────────────────
Recommended date: 2026-04-02 ($490.00)
```

### 各字段说明：

- **总价（含税费）** = `price` + `tax`（成人票价）
- **乘客总费用** = 成人乘客费用总和 × 成人乘客人数 + 儿童乘客费用总和
- **中途停留次数** = 航班段数 - 1；当 `stopQuantity > 0` 时显示中途停留城市
- **行李信息** = `baggages[].pieces` + `baggages[].weight`；若 `freeBaggage: false` 则表示“不含免费行李”
- **座位情况**：当 `maxSeatsRemain ≤ 3` 时显示 ⚠️ “仅剩 X 个座位”

---

## 主要响应字段

| 字段 | 描述 |
|-------|-------------|
| `status` | 状态码，0 表示成功 |
| `message` | “SUCCESS” 表示请求成功 |
| `routings[]` | 航班选项列表 |
| `routings[].prices[]` | 按乘客类型划分的价格（ADT = 成人，CHD = 儿童） |
| `routings[].segments[]` | 航班段详细信息（每个中途停留点视为一个独立段） |
| `routings[].rule.baggages[]` | 免费行李额度 |
| `routings[].rule.freeBagage` | 如果为 `false`，则表示需额外购买行李 |
| `routings[].maxSeatsRemain` | 剩余座位数 |
| `passengerType` | ADT = 成人，CHD = 儿童 |

---

## 错误处理

| 错误情况 | 处理方式 |
|----------|--------|
| `status != 0` 或 `message != "SUCCESS"` | 通知用户查询失败，并建议尝试其他日期 |
| `routings` 为空 | 说明该航线/日期没有航班可用 |
| 网络请求超时 | 重试一次；如果仍失败，请用户稍后再试 |
| 无法识别的城市代码 | 询问用户确认城市或机场名称 |
| 儿童乘客人数超过成人乘客人数 | 提示：“儿童乘客人数不能超过成人乘客人数” |