---
name: flight-tracker
description: **航班追踪与调度**  
通过 OpenSky Network，您可以按地区、呼号或机场实时追踪航班动态。您还可以查询不同机场之间的航班时刻表，例如：  
- “有哪些航班正在瑞士上空飞行？”  
- “从汉堡出发的航班什么时候会到达苏黎世？”  
- “追踪航班 SWR123 的飞行情况。”
homepage: https://openskynetwork.github.io/opensky-api/
---

# 航班追踪器

实时追踪航班，并查询机场之间的航班时刻表。

## 快捷命令

### 实时航班追踪

#### 追踪指定区域内的航班（使用边界框）
```bash
# Switzerland (lat_min, lat_max, lon_min, lon_max)
curl -s "https://opensky-network.org/api/states/all?lamin=45.8&lomin=5.9&lamax=47.8&lomax=10.5" | \
  jq -r '.states[] | "\(.[1]) - \(.[2]) | Alt: \(.[7])m | Speed: \(.[9])m/s | From: \(.[5])"'
```

### 通过呼号追踪特定航班
```bash
curl -s "https://opensky-network.org/api/states/all?icao24=<aircraft-icao>" | jq .
```

#### 获取航班实时信息
```bash
# Use helper script
python3 scripts/track.py --region switzerland
python3 scripts/track.py --callsign SWR123
python3 scripts/track.py --airport LSZH
```

### 航班时刻表

查询机场之间的预定航班：

```bash
# Basic usage (shows search links)
python3 scripts/schedule.py HAM ZRH

# With specific date
python3 scripts/schedule.py --from HAM --to ZRH --date 2026-01-15

# With API key (optional, for detailed results)
export AVIATIONSTACK_API_KEY='your_key_here'
python3 scripts/schedule.py HAM ZRH
```

**无需API密钥：** 显示有用的搜索链接（Google Flights、FlightRadar24、航空公司官网）

**使用API密钥：** 获取包含起飞/到达时间、航站楼、登机口和航班状态的实时时刻表数据

免费API密钥可在 [aviationstack.com](https://aviationstack.com) 获取（每月100次请求）

## 地区

脚本中预定义的地区包括：

- **switzerland**：瑞士领空
- **europe**：欧洲领空（大致范围）
- **zurich**：苏黎世周边地区
- **geneva**：日内瓦周边地区

## API接口

### 所有地区
```bash
GET https://opensky-network.org/api/states/all
```

可选参数：
- `lamin`, `lomin`, `lamax`, `lomax`：边界框
- `icao24`：特定航班的ICAO代码
- `time`：Unix时间戳（0 = 当前时间）

### 响应格式

每个航班的状态信息包含：
```
[0]  icao24      - Aircraft ICAO24 address (hex)
[1]  callsign    - Flight callsign (e.g., "SWR123")
[2]  origin_country - Country name
[5]  origin      - Origin airport (if available)
[7]  baro_altitude - Altitude in meters
[9]  velocity    - Speed in m/s
[10] heading     - Direction in degrees
[11] vertical_rate - Climb/descent rate in m/s
```

## 机场代码

### ICAO代码（用于实时追踪）
- **LSZH** - 苏黎世
- **LSGG** - 日内瓦
- **LSZB** - 伯尔尼
- **LSZA** - 卢加诺
- **LFSB** - 巴塞尔-米卢斯（EuroAirport）

### IATA代码（用于查询时刻表）
- **ZRH** - 苏黎世
- **GVA** - 日内瓦
- **BSL** - 巴塞尔
- **BRN** - 伯尔尼
- **LUG** - 卢加诺
- **HAM** - 汉堡
- **FRA** - 法兰克福
- **MUC** - 慕尼黑
- **BER** - 柏林
- **LHR** - 伦敦希思罗机场
- **CDG** - 巴黎戴高乐机场
- **AMS** - 阿姆斯特丹

## 注意事项

### 实时追踪（OpenSky Network）
- 免费API，但有使用限制（匿名用户：每天400次请求）
- 数据来自全球的ADS-B接收器，实时更新
- 无需API密钥
- 数据每10秒更新一次
- 如需更高请求次数或历史数据，请创建账户

### 航班时刻表（AviationStack）
- 需要API密钥以获取详细时刻表信息
- 免费 tier：每月100次请求
- 无需API时，提供Google Flights、FlightRadar24等网站的搜索链接
- 支持按日期查询航班信息