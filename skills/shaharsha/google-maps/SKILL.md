---
name: google-maps
description: >
  Google Maps integration for OpenClaw with Routes API. Use for: (1) Distance/travel time calculations 
  with traffic prediction, (2) Turn-by-turn directions, (3) Distance matrix between multiple points, 
  (4) Geocoding addresses to coordinates and reverse, (5) Places search and details, (6) Transit 
  planning with arrival times. Supports future departure times, traffic models (pessimistic/optimistic), 
  avoid options (tolls/highways), and multiple travel modes (driving/walking/bicycling/transit).
version: 3.1.2
author: Leo 🦁
tags: [maps, places, location, navigation, google, traffic, directions, geocoding, routes-api]
metadata: {"clawdbot":{"emoji":"🗺️","requires":{"env":["GOOGLE_API_KEY"]},"primaryEnv":"GOOGLE_API_KEY","secondaryEnv":["GOOGLE_MAPS_API_KEY"],"install":[{"id":"pip","kind":"pip","package":"requests","label":"Install requests library"}]}}
allowed-tools: [exec]
---

# Google Maps 🗺️

Google Maps的集成功能由Routes API提供支持。

## 必备条件

- 需要设置`GOOGLE_API_KEY`环境变量。
- 在Google Cloud Console中启用Routes API、Places API和Geocoding API。

## 配置参数

| 环境变量 | 默认值 | 说明 |
|--------------|---------|-------------|
| `GOOGLE_API_KEY` | - | 必需的Google Maps API密钥 |
| `GOOGLE_MAPS_API_KEY` | - | `GOOGLE_API_KEY`的备用选项（仅作为备用） |
| `GOOGLE_MAPS_LANG` | `en` | 响应语言（如en、he、ja等） |

请在OpenClaw配置文件中设置这些参数：
```json
{
  "env": {
    "GOOGLE_API_KEY": "AIza...",
    "GOOGLE_MAPS_LANG": "en"
  }
}
```

## 脚本位置

```bash
python3 skills/google-maps/lib/map_helper.py <action> [options]
```

---

## 功能说明

### `distance` - 计算旅行时间

```bash
python3 lib/map_helper.py distance "origin" "destination" [options]
```

**参数说明：**
| 参数 | 可选值 | 说明 |
|--------|--------|-------------|
| `--mode` | driving, walking, bicycling, transit | 旅行方式（默认：driving） |
| `--depart` | now, +30m, +1h, 14:00, 2026-02-07 08:00 | 出发时间 |
| `--arrive` | 14:00 | 到达时间（仅适用于交通方式） |
| `--traffic` | best_guess, pessimistic, optimistic | 交通模型 |
| `--avoid` | tolls, highways, ferries | 需要避免的交通方式（用逗号分隔） |

**使用示例：**
```bash
python3 lib/map_helper.py distance "New York" "Boston"
python3 lib/map_helper.py distance "Los Angeles" "San Francisco" --depart="+1h"
python3 lib/map_helper.py distance "Chicago" "Detroit" --depart="08:00" --traffic=pessimistic
python3 lib/map_helper.py distance "London" "Manchester" --mode=transit --arrive="09:00"
python3 lib/map_helper.py distance "Paris" "Lyon" --avoid=tolls,highways
```

**返回结果：**
```json
{
  "distance": "215.2 mi",
  "distance_meters": 346300,
  "duration": "3 hrs 45 mins",
  "duration_seconds": 13500,
  "static_duration": "3 hrs 30 mins",
  "duration_in_traffic": "3 hrs 45 mins"
}
```

---

### `directions` - 详细路线指引

```bash
python3 lib/map_helper.py directions "origin" "destination" [options]
```

**附加参数：**
| 参数 | 说明 |
|--------|-------------|
| `--alternatives` | 返回多条路线 |
| `--waypoints` | 中间停留点（用管道符号分隔） |
| `--optimize` | 优化停留点顺序（采用TSP算法） |

**使用示例：**
```bash
python3 lib/map_helper.py directions "New York" "Washington DC"
python3 lib/map_helper.py directions "San Francisco" "Los Angeles" --alternatives
python3 lib/map_helper.py directions "Miami" "Orlando" --waypoints="Fort Lauderdale|West Palm Beach" --optimize
```

**返回结果包括：** 路线概要、各个停留点的名称、行驶时间、总行驶时间、交通警告信息以及详细的行驶路径。

---

### `matrix` - 距离矩阵

用于计算多个起点与终点之间的距离：

```bash
python3 lib/map_helper.py matrix "orig1|orig2" "dest1|dest2"
```

**使用示例：**
```bash
python3 lib/map_helper.py matrix "New York|Boston" "Philadelphia|Washington DC"
```

**返回结果：**
```json
{
  "origins": ["New York", "Boston"],
  "destinations": ["Philadelphia", "Washington DC"],
  "results": [
    {"origin_index": 0, "destination_index": 0, "distance": "97 mi", "duration": "1 hr 45 mins"},
    {"origin_index": 0, "destination_index": 1, "distance": "225 mi", "duration": "4 hrs 10 mins"}
  ]
}
```

---

### `geocode` - 将地址转换为坐标

```bash
python3 lib/map_helper.py geocode "1600 Amphitheatre Parkway, Mountain View, CA"
python3 lib/map_helper.py geocode "10 Downing Street, London"
```

### `reverse` - 将坐标转换为地址

```bash
python3 lib/map_helper.py reverse 40.7128 -74.0060  # New York City
python3 lib/map_helper.py reverse 51.5074 -0.1278  # London
```

---

### `search` - 查找地点

```bash
python3 lib/map_helper.py search "coffee near Times Square"
python3 lib/map_helper.py search "pharmacy in San Francisco" --open
```

### `details` - 地点详细信息

```bash
python3 lib/map_helper.py details "<place_id>"
```

---

## 交通模型

| 交通模型 | 适用场景 |
|-------|----------|
| `best_guess` | 默认的平衡预测模型 |
| `pessimistic` | 用于重要会议等需要考虑最坏情况的场景 |
| `optimistic` | 用于最佳情况的预测 |

---

## 地区限制

某些功能可能并非在所有国家都可用：

| 功能 | 可用地区 |
|---------|--------------|
| `--fuel-efficient` | 美国、欧盟及部分国家 |
| `--shorter` | 可用性有限 |
| `--mode=two_wheeler` | 亚洲部分国家 |

详情请参考[Google Maps的覆盖范围](https://developers.google.com/maps/coverage)。

---

## 多语言支持

支持使用任何语言的地址进行查询：

```bash
# Hebrew
python3 lib/map_helper.py distance "תל אביב" "ירושלים"
python3 lib/map_helper.py geocode "דיזנגוף 50, תל אביב"

# Japanese
python3 lib/map_helper.py distance "東京" "大阪"

# Arabic
python3 lib/map_helper.py distance "دبي" "أبو ظبي"
```

**语言配置方法：**
1. 通过环境变量设置默认语言：`GOOGLE_MAPS_LANG=he`（永久生效）
2. 每次请求时手动指定语言：`--lang=ja`

```bash
# Set Hebrew as default in OpenClaw config
GOOGLE_MAPS_LANG=he

# Override for specific request
python3 lib/map_helper.py distance "Tokyo" "Osaka" --lang=ja
```

---

## 帮助文档

```bash
python3 lib/map_helper.py help
```