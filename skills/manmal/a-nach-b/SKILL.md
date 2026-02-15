---
name: anachb
description: 奥地利公共交通（VOR AnachB）服务覆盖整个奥地利。您可以查询实时发车信息、搜索车站/站点、规划两地之间的路线，以及查看交通服务是否中断。该服务适用于查询奥地利的火车、公交车、有轨电车（U-Bahn）的相关信息，或获取涉及奥地利公共交通的出行指引。
---

# VOR AnachB - 奥地利公共交通API

通过HAFAS API查询奥地利的公共交通信息，包括实时发车信息、路线规划以及服务中断情况。

## 快速参考

| 脚本 | 功能 |
|--------|---------|
| `search.sh` | 按名称查找车站/站点 |
| `departures.sh` | 查看车站的实时发车信息 |
| `route.sh` | 规划两个地点之间的行程 |
| `disruptions.sh` | 查看当前的服务中断情况 |

**API:** HAFAS（Hacon Fahrplan-Auskunfts-System）  
**端点:** `https://vao.demo.hafas.de/gate`

---

## 1. 查找车站/站点

按名称查找车站ID：

```bash
./search.sh "Stephansplatz"
./search.sh "Wien Hauptbahnhof"
./search.sh "Linz"
./search.sh "Salzburg Hbf"
```

返回车站名称、ID（extId）和坐标。

**响应字段：**
- `name`: 车站名称
- `extId`: 用于其他查询的车站ID
- `type`: S（车站）、A（地址）、P（兴趣点）
- `coordinates`: WGS84坐标（经纬度，格式为1e-6）

---

## 2. 实时发车信息

获取车站的下一班次发车信息：

```bash
./departures.sh <station-id> [count]

# Examples:
./departures.sh 490132000        # Wien Stephansplatz, 10 departures
./departures.sh 490132000 20     # Wien Stephansplatz, 20 departures
./departures.sh 490060200        # Wien Hauptbahnhof
./departures.sh 444130000        # Linz Hbf
./departures.sh 455000100        # Salzburg Hbf
```

**响应字段：**
- `line`: 车线名称（U1、S1、RJ等）
- `direction`: 最终目的地
- `departure`: 预定发车时间
- `delay`: 延误时间（如有）
- `platform`: 站台/轨道编号

---

## 3. 路线规划

规划两个车站之间的行程：

```bash
./route.sh <from-id> <to-id> [results]

# Examples:
./route.sh 490132000 490060200        # Stephansplatz → Hauptbahnhof
./route.sh 490132000 444130000 5      # Wien → Linz, 5 results
./route.sh "Graz Hbf" "Wien Hbf"      # Search by name (slower)
```

**响应字段：**
- `departure`: 出发时间
- `arrival`: 到达时间
- `duration`: 行程时长
- `changes`: 中转次数
- `legs`: 行程段数组，包含每段的线路信息

---

## 4. 查看服务中断情况

检查当前的服务中断情况：

```bash
./disruptions.sh [category]

# Examples:
./disruptions.sh            # All disruptions
./disruptions.sh TRAIN      # Train disruptions only
./disruptions.sh BUS        # Bus disruptions only
```

---

## 常见车站ID

| 车站 | ID |
|---------|-----|
| 维也纳圣斯蒂芬广场站 | 490132000 |
| 维也纳中央火车站 | 490134900 |
| 维也纳西火车站 | 490024300 |
| 维也纳普拉特斯特恩站 | 490056100 |
| 维也纳卡尔广场站 | 490024600 |
| 维也纳施韦登广场站 | 490119500 |
| 林茨中央火车站 | 444116400 |
| 萨尔茨堡中央火车站 | 455000200 |
| 格拉茨中央火车站 | 460086000 |
| 因斯布鲁克中央火车站 | 481070100 |
- 克拉根福中央火车站 | 492019500 |
- 圣珀尔滕中央火车站 | 431543300 |
- 维也纳新市中央火车站 | 430521000 |
- 克雷姆斯-阿德-多瑙河站 | 431046400 |

**提示：**始终使用`./search.sh`来查找正确的车站ID。

---

## 交通类型

| 代码 | 类型 |
|------|------|
| ICE/RJ/RJX | 高速列车 |
| IC/EC | 城际列车/欧洲城际列车 |
| REX/R | 区域快车/区域列车 |
| S | S-Bahn（城郊铁路） |
| U | U-Bahn（维也纳地铁） |
| STR | 有轨电车/街道电车 |
| BUS | 公交 |
| AST | 需求响应式交通 |

---

## API详细信息（高级用法）

这些脚本使用HAFAS JSON API。对于自定义查询，可以使用以下方法：

```bash
curl -s -X POST "https://vao.demo.hafas.de/gate" \
  -H "Content-Type: application/json" \
  -d '{
    "svcReqL": [{
      "req": { ... },
      "meth": "METHOD_NAME",
      "id": "1|1|"
    }],
    "client": {"id": "VAO", "v": "1", "type": "AND", "name": "nextgen"},
    "ver": "1.73",
    "lang": "de",
    "auth": {"aid": "nextgen", "type": "AID"}
  }'
```

**可用方法：**
- `LocMatch` - 位置/车站搜索
- `StationBoard` - 发车/到站信息
- `TripSearch` - 路线规划
- `HimSearch` - 服务中断/消息查询
- `JourneyDetails` - 具体行程详情

---

## 提示

1. **先查找车站ID**：在查询发车信息或路线之前，务必使用`search.sh`找到正确的车站ID。
2. **车站与站点**：主要车站通常有多个站台——使用主车站ID即可覆盖所有站台。
3. **实时数据**：发车信息会包含实时延误情况（如有的话）。
4. **覆盖范围**：该API覆盖整个奥地利的公共交通，不仅限于维也纳。
5. **跨境服务**：部分线路延伸至邻国（德国、捷克共和国等）。