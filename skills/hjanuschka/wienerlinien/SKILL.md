---
name: wienerlinien
description: 维也纳公共交通（Wiener Linien）的实时数据。可用于查询出发时间、时刻表、交通延误情况、电梯运行状态，以及获取维也纳地铁（U-Bahn）、有轨电车（Tram）、公交车和夜间公交车的路线信息。还可以查询车站、线路及交通状况。
---

# Wiener Linien 实时 API

查询维也纳公共交通的实时发车信息、服务中断情况、电梯故障以及相关服务详情。

## 快速参考

| 端点 | 功能 |
|----------|---------|
| `/monitor` | 查看某个站点的实时发车信息 |
| `/trafficInfoList` | 获取所有当前的服务中断信息 |
| `/trafficInfo` | 查看特定服务中断的详细信息 |
| `/newsList` | 查看服务新闻和电梯维护信息 |

**基础 URL:** `https://www.wienerlinien.at/ogd_realtime`

---

## 查找站点 ID

站点通过 **RBL 编号**（Rechnergestütztes Betriebsleitsystem）进行标识。请使用以下参考数据：

```bash
# Search stops by name
curl -s "https://www.wienerlinien.at/ogd_realtime/doku/ogd/wienerlinien-ogd-haltepunkte.csv" | grep -i "stephansplatz"

# Format: StopID;DIVA;StopText;Municipality;MunicipalityID;Longitude;Latitude
```

**常见站点 ID（RBL）：**

| 站点 | RBL 编号 | 所属线路 |
|------|---------|-------|
| Stephansplatz | 252, 4116, 4119 | U1, U3 |
| Karlsplatz | 143, 144, 4101, 4102 | U1, U2, U4 |
| Westbahnhof | 1346, 1350, 1368 | U3, U6 |
| Praterstern | 4205, 4210 | U1, U2 |
| Schwedenplatz | 1489, 1490, 4103 | U1, U4 |
| Schottentor | 40, 41, 4118 | U2, 有轨电车 |

---

## 1. 实时发车信息（`/monitor`）

查询一个或多个站点的下一班次发车时间。

### 请求方式

```bash
# Single stop
curl -s "https://www.wienerlinien.at/ogd_realtime/monitor?stopId=252"

# Multiple stops
curl -s "https://www.wienerlinien.at/ogd_realtime/monitor?stopId=252&stopId=4116"

# With disruption info
curl -s "https://www.wienerlinien.at/ogd_realtime/monitor?stopId=252&activateTrafficInfo=stoerungkurz&activateTrafficInfo=stoerunglang&activateTrafficInfo=aufzugsinfo"
```

### 参数

| 参数 | 是否必填 | 描述 |
|-------|----------|-------------|
| `stopId` | 是（1-n个） | 站点 RBL 编号 |
| `activateTrafficInfo` | 否 | 是否包含服务中断信息：`stoerungkurz`、`stoerunglang`、`aufzugsinfo` |
| `aArea` | 否 | `1` = 包含所有具有相同 DIVA 编号的站台 |

### 响应结构

```json
{
  "data": {
    "monitors": [{
      "locationStop": {
        "properties": {
          "name": "60201234",      // DIVA number
          "title": "Stephansplatz", // Stop name
          "attributes": { "rbl": 252 }
        },
        "geometry": {
          "coordinates": [16.3726, 48.2085]  // lon, lat (WGS84)
        }
      },
      "lines": [{
        "name": "U1",
        "towards": "Leopoldau",
        "direction": "H",           // H=hin, R=retour
        "type": "ptMetro",
        "barrierFree": true,
        "realtimeSupported": true,
        "trafficjam": false,
        "departures": {
          "departure": [{
            "departureTime": {
              "timePlanned": "2025-01-08T19:30:00.000+0100",
              "timeReal": "2025-01-08T19:31:30.000+0100",
              "countdown": 3  // minutes until departure
            }
          }]
        }
      }]
    }]
  },
  "message": { "value": "OK", "messageCode": 1 }
}
```

### 关键字段

| 字段 | 描述 |
|-------|-------------|
| `countdown` | 发车前剩余时间（分钟） |
| `timePlanned` | 预计发车时间 |
| `timeReal` | 实时预测时间（如有） |
| `barrierFree` | 是否适合轮椅使用者通行 |
| `trafficjam` | 是否存在影响到达的交通拥堵 |
| `type` | `ptMetro`、`ptTram`、`ptBusCity`、`ptBusNight` |

---

## 2. 服务中断（`/trafficInfoList`）

获取所有当前的服务中断信息。

### 请求方式

```bash
# All disruptions
curl -s "https://www.wienerlinien.at/ogd_realtime/trafficInfoList"

# Filter by line
curl -s "https://www.wienerlinien.at/ogd_realtime/trafficInfoList?relatedLine=U3&relatedLine=U6"

# Filter by stop
curl -s "https://www.wienerlinien.at/ogd_realtime/trafficInfoList?relatedStop=252"

# Filter by type
curl -s "https://www.wienerlinien.at/ogd_realtime/trafficInfoList?name=aufzugsinfo"
```

### 参数

| 参数 | 描述 |
| `relatedLine` | 线路名称（如 U1、13A 等） | 可重复输入 |
| `relatedStop` | 相关站点 RBL 编号 | 可重复输入 |
| `name` | 中断类型：`stoerunglang`、`stoerungkurz`、`aufzugsinfo`、`fahrtreppeninfo` |

### 响应内容

```json
{
  "data": {
    "trafficInfos": [{
      "name": "eD_23",
      "title": "Gumpendorfer Straße",
      "description": "U6 Bahnsteig Ri. Siebenhirten - Aufzug außer Betrieb",
      "priority": "1",
      "time": {
        "start": "2025-01-08T06:00:00.000+0100",
        "end": "2025-01-08T22:00:00.000+0100"
      },
      "relatedLines": ["U6"],
      "relatedStops": [4611],
      "attributes": {
        "status": "außer Betrieb",
        "station": "Gumpendorfer Straße",
        "location": "U6 Bahnsteig Ri. Siebenhirten"
      }
    }],
    "trafficInfoCategories": [{
      "id": 1,
      "name": "aufzugsinfo",
      "title": "Aufzugsstörungen"
    }]
  }
}
```

### 中断类型

| 类型 | 描述 |
|------|-------------|
| `stoerunglang` | 长期中断 |
| `stoerungkurz` | 短期中断 |
| `aufzugsinfo` | 电梯故障 |
| `fahrtreppeninfo` | 自动扶梯故障 |

---

## 3. 查看特定中断的详细信息（`/trafficInfo`）

根据中断类型查询具体中断的详细信息。

```bash
curl -s "https://www.wienerlinien.at/ogd_realtime/trafficInfo?name=eD_265&name=eD_37"
```

---

## 4. 服务新闻（`/newsList`）

查看计划中的维护工作、电梯维护时间以及服务相关新闻。

```bash
# All news
curl -s "https://www.wienerlinien.at/ogd_realtime/newsList"

# Filter by line/stop/category
curl -s "https://www.wienerlinien.at/ogd_realtime/newsList?relatedLine=U6&name=aufzugsservice"
```

### 分类

| 类型 | 描述 |
|------|-------------|
| `aufzugsservice` | 电梯维护计划 |
| `news` | 一般服务新闻 |

---

## 参考数据（CSV 文件）

### 站点信息（Haltepunkte）

```bash
curl -s "https://www.wienerlinien.at/ogd_realtime/doku/ogd/wienerlinien-ogd-haltepunkte.csv"
# StopID;DIVA;StopText;Municipality;MunicipalityID;Longitude;Latitude
```

**注意：`StopID` 是在 API 请求中使用的 RBL 编号。**

### 车站信息（Haltestellen）

```bash
curl -s "https://www.wienerlinien.at/ogd_realtime/doku/ogd/wienerlinien-ogd-haltestellen.csv"
# DIVA;PlatformText;Municipality;MunicipalityID;Longitude;Latitude
```

### 线路信息

```bash
curl -s "https://www.wienerlinien.at/ogd_realtime/doku/ogd/wienerlinien-ogd-linien.csv"
# LineID;LineText;SortingHelp;Realtime;MeansOfTransport
```

**交通方式**：`ptMetro`、`ptTram`、`ptBusCity`、`ptBusNight`

---

## 常见使用场景

### “Stephansplatz 站的下一班 U1 什么时候出发？”
```bash
# Stephansplatz U1 platform RBL: 4116
curl -s "https://www.wienerlinien.at/ogd_realtime/monitor?stopId=4116" | jq '.data.monitors[].lines[] | select(.name=="U1") | {line: .name, towards: .towards, departures: [.departures.departure[].departureTime.countdown]}'
```

### “有 U-Bahn 中断吗？”
```bash
curl -s "https://www.wienerlinien.at/ogd_realtime/trafficInfoList?relatedLine=U1&relatedLine=U2&relatedLine=U3&relatedLine=U4&relatedLine=U6" | jq '.data.trafficInfos[] | {title, description, lines: .relatedLines}'
```

### “哪些电梯无法使用？”
```bash
curl -s "https://www.wienerlinien.at/ogd_realtime/trafficInfoList?name=aufzugsinfo" | jq '.data.trafficInfos[] | {station: .attributes.station, location: .attributes.location, status: .attributes.status}'
```

### “Karlsplatz 站的所有发车信息及中断详情”
```bash
curl -s "https://www.wienerlinien.at/ogd_realtime/monitor?stopId=143&stopId=144&stopId=4101&stopId=4102&activateTrafficInfo=stoerungkurz&activateTrafficInfo=stoerunglang&activateTrafficInfo=aufzugsinfo"
```

---

## 错误代码

| 代码 | 含义 |
|------|---------|
| 311 | 数据库不可用 |
| 312 | 站点不存在 |
| 316 | 超过请求频率限制 |
| 320 | 参数无效 |
| 321 | 缺少必填参数 |
| 322 | 数据库中无相关信息 |

---

## 车辆类型

| 类型 | 描述 |
|------|-------------|
| `ptMetro` | 地铁 |
| `ptTram` | 有轨电车 |
| `ptBusCity` | 市区公交车 |
| `ptBusNight` | 夜间公交车（特定线路） |

---

## 提示：

1. **多个站台**：一个站点可能有多个 RBL 编号（每个站台/方向一个编号）。需查询所有编号以获取完整发车信息。
2. **实时可用性**：请查看 `realtimeSupported` 字段——部分线路仅提供预定发车时间。
3. **显示方式**：使用 `countdown` 查看预计发车时间，使用 `timeReal` 获取精确时间。
4. **无障碍通行**：通过 `barrierFree: true` 过滤适合轮椅使用者的路线。
5. **查找站点 ID**：先在 CSV 文件中搜索站点名称，然后使用该名称作为 `stopId` 参数进行查询。