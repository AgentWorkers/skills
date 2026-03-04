---
name: arrivelah
description: Get Singapore bus arrivals from a source location to a destination. Trigger: "bus from <source> to <destination>"
homepage: https://github.com/abhay/arrivelah
metadata: {"openclaw":{"emoji":"🚌","requires":{"bins":["curl"]},"tags":["singapore","transport","bus","sg"]}}
---

# ArriveLah - 新加坡公交车查询服务

这是一个用于查询新加坡公交信息的自然语言查询系统。

## 使用格式

```
bus from <source location> to <destination location>
```

示例：
- “从Silat Road Sikh Temple到Queens condo的公交车”
- “从Tanjong Pagar MRT到VivoCity的公交车”
- “从我的办公室到家的公交车”

## 详细工作流程

### 第1步：对起始位置进行地理编码
使用`web_fetch`通过OneMap API将起始位置转换为坐标：
```
https://www.onemap.gov.sg/api/common/elastic/search?searchVal=<source>&returnGeom=Y&getAddrDetails=Y&pageNum=1
```
从第一个查询结果中提取`LATITUDE`和`LONGITUDE`。

### 第2步：查找距离起始位置最近的公交车站
获取新加坡所有公交车站的列表，并找出距离起始位置最近的公交车站：
```
https://busrouter.sg/data/2/bus-stops.json
```
该操作会返回一个JSON对象，其中每个键代表一个公交车站的代码，包含以下字段：`description`（车站名称）、`road`（车站所在道路）、`lat`（纬度）、`lng`（经度）。
使用公式`sqrt((lat2-lat1)^2 + (lng2-lng1)^2)`计算距离（短距离时使用近似值即可）。
选择距离最近的**3个**车站。

### 第3步：对目的地位置进行地理编码
与第1步相同，对目的地位置进行地理编码，并提取其坐标。

### 第4步：查找从起始车站出发、经过目的地的公交车
对于距离最近的3个车站，分别查询每条公交车的到站信息：
```
https://arrivelah2.busrouter.sg/?id=<stop_code>
```

然后，检查每条公交车的路线，判断是否有公交车经过目的地附近：
```
https://busrouter.sg/data/2/routes.json
```
将公交车的服务编号与`bus-stops.json`文件中的车站代码进行匹配，获取沿途每个车站的坐标，并判断是否有车站距离目的地在400米范围内。
只保留满足以下条件的公交车：
1. 起始车站在路线中位于目的地车站之前（方向正确）
2. 路线经过距离目的地400米以内的车站

### 第5步：获取实时到站信息
对于每条符合条件的公交车，从`arrivelah2`接口获取以下信息：
- `next.duration_ms`：下一班公交车到达的时间（以分钟为单位）
- `subsequent.duration_ms`：下一班之后的公交车到达的时间（以分钟为单位）
- `next.load`：座位情况：`SEA` = 有座位可用，`SDA` = 可站立，`LSD` = 限站立
- `next.feature`：`WAB` = 可供轮椅使用
- `next.type`：`DD` = 双层巴士，`SD` = 单层巴士，`BD` = 弯道巴士

### 第6步：格式化结果并返回
```
🚌 Buses from [Source Stop Name] → [Destination]

Bus [XX]
  ⏰ Next: X min | Then: Y min
  💺 [Seats Available / Standing / Limited Standing]
  🚌 [Double Decker / Single Deck]

Bus [YY]
  ⏰ Next: X min | Then: Y min
  💺 [Seats Available / Standing / Limited Standing]

📍 Stop: [Stop Description], [Road Name] (Stop code: XXXXX)
```

如果没有找到直达的公交车，应提示用户选择最近的地铁站或其他替代交通方式。

## 代码中使用的符号说明：
- `SEA` = 有座位可用 🟢
- `SDA` = 可站立 🟡  
- `LSD` = 限站立 🔴

## 公交车类型说明：
- `DD` = 双层巴士
- `SD` = 单层巴士
- `BD` = 弯道巴士
- `WAB` = 可供轮椅使用的公交车

## 所需API接口（无需认证）：
- OneMap地理编码：`https://www.onemap.gov.sg/api/common/elastic/search`
- 公交车站信息：`https://busrouter.sg/data/2/bus-stops.json`
- 路线信息：`https://busrouter.sg/data/2/routes.json`
- 实时到站信息：`https://arrivelah2.busrouter.sg/?id=<stop_code>`