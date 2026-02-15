---
name: swiss-transport
description: 瑞士公共交通实时信息。适用于查询瑞士的火车、公交车、有轨电车或轮船的班次信息。支持车站搜索、出发时间查询、从A地到B地的行程规划以及换乘详情。可用来回答诸如“下一班从苏黎世出发的火车是什么时候？”、“我该如何从伯尔尼前往日内瓦？”或“显示巴塞尔SBB车站的出发信息？”之类的问题。
homepage: https://transport.opendata.ch
---

# 瑞士公共交通

您可以使用官方的 `transport.opendata.ch` API 查询瑞士的公共交通信息（包括 SBB、BLS、ZVV 等）。

## 快速命令

### 搜索车站
```bash
curl -s "https://transport.opendata.ch/v1/locations?query=Zürich" | jq -r '.stations[] | "\(.name) (\(.id))"'
```

### 查看下一班次
```bash
curl -s "https://transport.opendata.ch/v1/stationboard?station=Zürich%20HB&limit=10" | \
  jq -r '.stationboard[] | "\(.stop.departure[11:16]) \(.category) \(.number) → \(.to)"'
```

### 从 A 地点到 B 地点规划行程
```bash
curl -s "https://transport.opendata.ch/v1/connections?from=Zürich&to=Bern&limit=3" | \
  jq -r '.connections[] | "Departure: \(.from.departure[11:16]) | Arrival: \(.to.arrival[11:16]) | Duration: \(.duration[3:]) | Changes: \(.transfers)"'
```

### 获取途经站点的详细连接信息
```bash
curl -s "https://transport.opendata.ch/v1/connections?from=Zürich%20HB&to=Bern&limit=1" | \
  jq '.connections[0].sections[] | {from: .departure.station.name, to: .arrival.station.name, departure: .departure.departure, arrival: .arrival.arrival, transport: .journey.category, line: .journey.number}'
```

## API 端点

### `/v1/locations` - 搜索车站
```bash
curl "https://transport.opendata.ch/v1/locations?query=<station-name>"
```

参数：
- `query`（必填）：要搜索的车站名称
- `type`（可选）：按类型筛选（车站、地址、兴趣点）

### `/v1/stationboard` - 车站时刻表
```bash
curl "https://transport.opendata.ch/v1/stationboard?station=<station>&limit=<number>"
```

参数：
- `station`（必填）：车站名称或 ID
- `limit`（可选）：结果数量（默认为 40）
- `transportations[]`（可选）：按交通方式筛选（ice_tgv_rj、ec_ic、ir、re_d、ship、s_sn_r、bus、cableway、arz_ext、tramway_underground）
- `datetime`（可选）：ISO 格式的日期/时间

### `/v1/connections` - 行程规划
```bash
curl "https://transport.opendata.ch/v1/connections?from=<start>&to=<destination>&limit=<number>"
```

参数：
- `from`（必填）：出发站
- `to`（必填）：目的地站
- `via[]`（可选）：途经站
- `date`（可选）：日期（YYYY-MM-DD）
- `time`（可选）：时间（HH:MM）
- `isArrivalTime`（可选）：0（出发）或 1（到达）
- `limit`（可选）：返回的连接数量（最多 16 个）

## 帮助脚本

使用 `scripts/journey.py` 脚本可以格式化行程规划结果：

```bash
python3 scripts/journey.py "Zürich HB" "Bern"
python3 scripts/journey.py "Basel" "Lugano" --limit 5
```

## 注意事项

- 所有时间均以瑞士当地时间（CET/CEST）显示
- 车站名称支持自动补全（例如，“Zürich”会匹配“Zürich HB”）
- API 默认返回 JSON 格式的数据
- 无需 API 密钥
- 实时数据包含延误信息和站台变更信息