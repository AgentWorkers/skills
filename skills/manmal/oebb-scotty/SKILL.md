---
name: oebb-scotty
description: 奥地利铁路旅行规划工具（ÖBB Scotty）：适用于在奥地利规划火车行程、查询车站的出发/到达信息，或查看服务中断情况。该工具支持查询ÖBB列车、S-Bahn（城际轻轨）、区域列车，以及与邻国的交通连接信息。
---

# ÖBB Scotty API

通过 HAFAS mgate API 查询奥地利的公共交通信息，用于行程规划、车站出发时间查询和服务提醒。

## 快速参考

| 方法 | 功能 |
|--------|---------|
| `LocMatch` | 按名称搜索车站/站点 |
| `TripSearch` | 规划两个地点之间的行程 |
| `StationBoard` | 获取车站的出发/到达信息 |
| `HimSearch` | 获取服务提醒和中断信息 |

**基础 URL:** `https://fahrplan.oebb.at/bin/mgate.exe`

---

## 认证

所有请求的 JSON 正文中都必须包含以下头部信息：

```json
{
  "id": "1",
  "ver": "1.67",
  "lang": "deu",
  "auth": {"type": "AID", "aid": "OWDL4fE4ixNiPBBm"},
  "client": {"id": "OEBB", "type": "WEB", "name": "webapp", "l": "vs_webapp"},
  "formatted": false,
  "svcReqL": [...]
}
```

---

## 1. 地点搜索 (`LocMatch`)

按名称搜索车站、站点、地址或兴趣点（POI）。

### 请求

```bash
curl -s -X POST "https://fahrplan.oebb.at/bin/mgate.exe" \
  -H "Content-Type: application/json" \
  -d '{
    "id":"1","ver":"1.67","lang":"deu",
    "auth":{"type":"AID","aid":"OWDL4fE4ixNiPBBm"},
    "client":{"id":"OEBB","type":"WEB","name":"webapp","l":"vs_webapp"},
    "formatted":false,
    "svcReqL":[{
      "req":{"input":{"field":"S","loc":{"name":"Wien Hbf","type":"ALL"},"maxLoc":10}},
      "meth":"LocMatch"
    }]
  }'
```

### 响应结构

```json
{
  "svcResL": [{
    "res": {
      "match": {
        "locL": [{
          "lid": "A=1@O=Wien Hbf (U)@X=16377950@Y=48184986@U=181@L=1290401@",
          "type": "S",
          "name": "Wien Hbf (U)",
          "extId": "1290401",
          "crd": { "x": 16377950, "y": 48184986 },
          "pCls": 6015
        }]
      }
    }
  }]
}
```

### 地点类型

| 类型 | 描述 |
|------|-------------|
| `S` | 车站/站点 |
| `A` | 地址 |
| `P` | 兴趣点（Point of Interest） |

### 关键字段

| 字段 | 描述 |
|-------|-------------|
| `lid` | 地点 ID 字符串（用于 `TripSearch`） |
| `extId` | 外部车站 ID |
| `name` | 车站名称 |
| `crd.x/y` | 坐标（x=经度, y=纬度，比例尺为 10^6） |
| `pCls` | 产品类别位掩码 |

---

## 2. 行程搜索 (`TripSearch`)

规划两个地点之间的行程。

### 请求

```bash
curl -s -X POST "https://fahrplan.oebb.at/bin/mgate.exe" \
  -H "Content-Type: application/json" \
  -d '{
    "id":"1","ver":"1.67","lang":"deu",
    "auth":{"type":"AID","aid":"OWDL4fE4ixNiPBBm"},
    "client":{"id":"OEBB","type":"WEB","name":"webapp","l":"vs_webapp"},
    "formatted":false,
    "svcReqL":[{
      "req":{
        "depLocL":[{"lid":"A=1@O=Wien Hbf@L=8103000@","type":"S"}],
        "arrLocL":[{"lid":"A=1@O=Salzburg Hbf@L=8100002@","type":"S"}],
        "jnyFltrL":[{"type":"PROD","mode":"INC","value":"1023"}],
        "getPolyline":false,
        "getPasslist":true,
        "outDate":"20260109",
        "outTime":"080000",
        "outFrwd":true,
        "numF":5
      },
      "meth":"TripSearch"
    }]
  }'
```

### 参数

| 参数 | 描述 |
|-------|-------------|
| `depLocL` | 出发地点（使用 `LocMatch` 中的 `lid`） |
| `arrLocL` | 到达地点 |
| `outDate` | 出发日期（YYYYMMDD） |
| `outTime` | 出发时间（HHMMSS） |
| `outFrwd` | `true` = 向前搜索，`false` = 向后搜索 |
| `numF` | 返回的连接次数 |
| `jnyFltrL` | 产品过滤（见下文） |
| `getPasslist` | 包含中途站点 |

### 产品过滤值

| 位 | 值 | 产品类型 |
|-----|-------|---------|
| 0 | 1 | ICE/RJX（高速列车） |
| 1 | 2 | IC/EC（城际列车） |
| 2 | 4 | NJ（夜间列车） |
| 3 | 8 | D/EN（快速列车） |
| 4 | 16 | REX/R（区域快车） |
| 5 | 32 | S-Bahn（轻轨） |
| 6 | 64 | 公交 |
| 7 | 128 | 渡轮 |
| 8 | 256 | 地铁 |
| 9 | 512 | 有轨电车 |
| 1023 | 所有产品 |

使用 `1023` 来查询所有产品类型，或组合特定位。

### 响应结构

```json
{
  "svcResL": [{
    "res": {
      "outConL": [{
        "date": "20260109",
        "dur": "025200",
        "chg": 0,
        "dep": {
          "dTimeS": "075700",
          "dPltfS": {"txt": "8A-B"}
        },
        "arr": {
          "aTimeS": "104900",
          "aPltfS": {"txt": "7"}
        },
        "secL": [{
          "type": "JNY",
          "jny": {
            "prodX": 0,
            "dirTxt": "Salzburg Hbf",
            "stopL": [...]
          }
        }]
      }],
      "common": {
        "locL": [...],
        "prodL": [...]
      }
    }
  }]
}
```

### 关键连接字段

| 字段 | 描述 |
|-------|-------------|
| `dur` | 行程时长（HHMMSS） |
| `chg` | 中转次数 |
| `dTimeS` | 预定出发时间 |
| `dTimeR` | 实时出发时间（如可用） |
| `aTimeS` | 预定到达时间 |
| `aTimeR` | 实时到达时间（如可用） |
| `dPltfS.txt` | 出发站台 |
| `aPltfS.txt` | 到达站台 |
| `secL` | 行程段（路段） |
| `secL[].jny.prodX` | 在 `common.prodL[]` 中对应列车名称的索引 |

### 理解 `prodX`（产品索引）

**注意：** `prodX` 字段是 `common.prodL[]` 数组中的索引，而不是列车名称本身。要获取实际的列车名称（例如 “S7” 或 “RJX 662”），需要通过 `common.prodL[prodX].name` 来查找。

### 使用 jq 提取行程摘要

原始的 `TripSearch` 响应内容非常冗长。使用以下 jq 过滤器可以提取包含列车名称的简洁摘要：

```bash
curl -s -X POST "https://fahrplan.oebb.at/bin/mgate.exe" \
  -H "Content-Type: application/json" \
  -d '{ ... }' | jq '
    .svcResL[0].res as $r |
    $r.common.prodL as $prods |
    [$r.outConL[] | {
      dep: .dep.dTimeS,
      arr: .arr.aTimeS,
      depPlatform: .dep.dPltfS.txt,
      arrPlatform: .arr.aPltfS.txt,
      dur: .dur,
      chg: .chg,
      legs: [.secL[] | select(.type == "JNY") | {
        train: $prods[.jny.prodX].name,
        dir: .jny.dirTxt,
        dep: .dep.dTimeS,
        arr: .arr.aTimeS,
        depPlatform: .dep.dPltfS.txt,
        arrPlatform: .arr.aPltfS.txt
      }]
    }]'
```

示例输出：
```json
[
  {
    "dep": "213900",
    "arr": "221100",
    "depPlatform": "1",
    "arrPlatform": "3A-B",
    "dur": "003200",
    "chg": 0,
    "legs": [{"train": "S 7", "dir": "Flughafen Wien Bahnhof", "dep": "213900", "arr": "221100", ...}]
  }
]
```

---

## 3. 车站信息查询 (`StationBoard`)

获取车站的出发或到达信息。

### 请求

```bash
curl -s -X POST "https://fahrplan.oebb.at/bin/mgate.exe" \
  -H "Content-Type: application/json" \
  -d '{
    "id":"1","ver":"1.67","lang":"deu",
    "auth":{"type":"AID","aid":"OWDL4fE4ixNiPBBm"},
    "client":{"id":"OEBB","type":"WEB","name":"webapp","l":"vs_webapp"},
    "formatted":false,
    "svcReqL":[{
      "req":{
        "stbLoc":{"lid":"A=1@O=Wien Hbf@L=8103000@","type":"S"},
        "date":"20260109",
        "time":"080000",
        "type":"DEP",
        "maxJny":20
      },
      "meth":"StationBoard"
    }]
  }'
```

### 参数

| 参数 | 描述 |
|-------|-------------|
| `stbLoc` | 车站位置 |
| `date` | 日期（YYYYMMDD） |
| `time` | 时间（HHMMSS） |
| `type` | `DEP`（出发）或 `ARR`（到达） |
| `maxJny` | 最大查询条目数 |

### 响应结构

```json
{
  "svcResL": [{
    "res": {
      "jnyL": [{
        "prodX": 0,
        "dirTxt": "Salzburg Hbf",
        "stbStop": {
          "dTimeS": "080000",
          "dPltfS": {"txt": "8A-B"}
        }
      }],
      "common": {
        "prodL": [{
          "name": "RJX 662",
          "cls": 1,
          "prodCtx": {"catOutL": "Railjet Xpress"}
        }]
      }
    }
  }]
}
```

---

## 4. 服务提醒 (`HimSearch`）

获取当前的服务中断和信息。

### 请求

```bash
curl -s -X POST "https://fahrplan.oebb.at/bin/mgate.exe" \
  -H "Content-Type: application/json" \
  -d '{
    "id":"1","ver":"1.67","lang":"deu",
    "auth":{"type":"AID","aid":"OWDL4fE4ixNiPBBm"},
    "client":{"id":"OEBB","type":"WEB","name":"webapp","l":"vs_webapp"},
    "formatted":false,
    "svcReqL":[{
      "req":{
        "himFltrL":[{"type":"PROD","mode":"INC","value":"255"}],
        "maxNum":20
      },
      "meth":"HimSearch"
    }]
  }'
```

### 响应结构

```json
{
  "svcResL": [{
    "res": {
      "msgL": [{
        "hid": "HIM_FREETEXT_843858",
        "head": "Verringertes Sitzplatzangebot",
        "text": "Wegen einer technischen Störung...",
        "prio": 0,
        "sDate": "20260108",
        "eDate": "20260108"
      }]
    }
  }]
}
```

---

## 常见车站 ID

| 车站 | 外部 ID |
|---------|-------|
| 维也纳中央火车站 | 8103000 |
| 维也纳梅德林火车站 | 8100514 |
| 维也纳西火车站 | 8101003 |
| 萨尔茨堡中央火车站 | 8100002 |
| 林茨中央火车站 | 8100013 |
| 格拉茨中央火车站 | 8100173 |
| 因斯布鲁克中央火车站 | 8100108 |
| 圣珀尔滕中央火车站 | 8100008 |
| 弗赖恩纽施塔特中央火车站 | 8100516 |

---

## 时间格式

- 日期：`YYYYMMDD`（例如：`20260109`）
- 时间：`HHMMSS`（例如：`080000` 表示 08:00:00）
- 行程时长：`HHMMSS`（例如：`025200` 表示 2小时52分钟）

---

## 错误处理

检查响应中的 `err` 字段：

```json
{
  "err": "OK",           // Success
  "err": "PARSE",        // Invalid request format
  "err": "NO_MATCH",     // No results found
  "errTxt": "..."        // Error details
}
```

---

## 产品类别（cls 值）

| cls | 产品类型 |
|-----|---------|
| 1 | ICE/RJX |
| 2 | IC/EC |
| 4 | 夜间列车 |
| 8 | NJ/EN |
| 16 | REX/区域快车 |
| 32 | S-Bahn |
| 64 | 公交 |
| 128 | 渡轮 |
| 256 | 地铁 |
| 512 | 有轨电车 |
| 1024 | 需求响应式服务 |
| 2048 | 其他 |