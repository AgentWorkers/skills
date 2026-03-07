---
name: bahn
description: 一套用于追踪德国铁路（Deutsche Bahn）列车信息的综合命令集
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - node
    install:
      - kind: node
        package: db-vendo-client
      - kind: node
        package: devalue
      - kind: node
        package: fast-xml-parser
    emoji: "🚆"
    homepage: https://github.com/ableitung/openclaw-bahn
    os:
      - macos
      - linux
---
# Bahn  
这是一个专为德国铁路（Deutsche Bahn）列车设计的综合命令工具集，提供实时列车出发信息、延误跟踪、施工/运营中断警报、行程规划、列车连接信息解析、历史延误数据以及延误预测等功能。无需使用API密钥。  

## 命令参数（Flags）  
| 参数 | 功能 | 使用场景 |  
|------|-------------|-------------|  
| `--predict` | 运行指数延误模型（transferProb、zugbindungProb） | 用户需要查询换乘概率或列车连接状态的变化情况 |  
| `--stats` | 获取特定列车的历史延误数据 | 用户需要了解某列车的历史延误情况 |  

## 使用示例  
```bash
# Search for a train station
node scripts/bahn.mjs --search "Wuppertal" [--json]

# Find latest departures from a given station
node scripts/bahn.mjs --departures "Wuppertal Hbf" [--results N] [--json]

# Default: Parse and show live data
echo '<raw Navigator share text>' | node scripts/bahn.mjs --parse [--json]

# With prediction model (transferProb, zugbindungProb)
echo '<text>' | node scripts/bahn.mjs --parse --predict [--json]

# With historical stats from bahn.expert
node scripts/bahn.mjs --parse connections/active.json --stats [--json]

# Both
node scripts/bahn.mjs --parse connections/active.json --predict --stats [--json]

# Find a given journey in timetable
node scripts/bahn.mjs --journey "From" "To" [--date YYYY-MM-DD] [--time HH:MM] [--results N] [--days N] [--json]

# Get current delays
node scripts/bahn.mjs --live --current-leg N [--delay M] connections/active.json [--json]

# Find a specific train by number and category (example: ICE 933)
node scripts/bahn.mjs --category CAT --train NUM [--date YYYY-MM-DD] [--json]
```  

## 文件结构  
```
scripts/
├── bahn.mjs                    ← thin CLI dispatcher (~60 lines)
├── lib/
│   ├── commands/             ← one module per mode
│   │   ├── search.mjs        ← --search: station lookup
│   │   ├── departures.mjs    ← --departures: live departure board
│   │   ├── parse.mjs         ← --parse: connection parsing + enrichment
│   │   ├── journey.mjs       ← --journey: route search
│   │   ├── live.mjs          ← --live: real-time transfer check
│   │   └── track.mjs         ← --track: train tracking
│   ├── helpers.mjs           ← shared helpers (envelope, transfers, assessment)
│   ├── data.mjs              ← source router (IRIS/Vendo/bahn.expert)
│   ├── predict.mjs           ← probability model (opt-in via --predict)
│   ├── stats.mjs             ← delay profiles + historical stats (opt-in via --stats)
│   ├── parse.mjs             ← connection text parser
│   ├── format.mjs            ← output formatter
│   ├── messageLookup.mjs     ← IRIS delay code lookup
│   └── sources/
│       ├── bahn-expert.mjs   ← bahn.expert tRPC source
│       ├── iris.mjs          ← IRIS XML source
│       └── vendo.mjs         ← db-vendo-client source
```  

## JSON 数据格式  
所有命令均支持 `--json` 选项：  
```json
{
  "mode": "string",
  "timestamp": "ISO8601",
  "connection": { "date", "from", "to", "legs", "transfers" },
  "journeyOptions": { "from", "to", "date", "options" },
  "departures": { "station", "entries" },
  "stations": { "query", "results" },
  "liveStatus": { "currentLeg", "nextTransfer", "zugbindungStatus", "recommendation", "remainingTransfers" },
  "trackStatus": { "train", "from", "to", "stops", "maxDelay", "zugbindungStatus" },
  "assessment": null,
  "errors": [],
  "warnings": []
}
```  

`assessment` 字段仅在使用 `--predict` 时才会被填充；否则，该字段的值为 `null`。  

## 预测模型（predict.mjs）（可选）  
该文件包含按列车类别划分的指数延误分布数据，仅在调用 `--predict` 时才会被加载：  
| 列车类别 | 平均延误时间 | 取消率 |  
|--------|------------|-----------|  
| ICE     | 5.0分钟     | 5.5%       |  
| IC/EC    | 4.0分钟     | 4.0%       |  
| RE      | 2.5分钟     | 2.0%       |  
| RB      | 2.0分钟     | 1.5%       |  
| S       | 1.5分钟     | 1.0%       |  
| 公交     | 3.0分钟     | 2.0%       |  

每段行程的列车连接概率（P(Zugbindung）的计算公式为：`exp(-20/平均延误时间)`；  
整体列车连接概率（P(Zugbindung)）的计算公式为：`1 - ∏(1 - P(每段行程延误时间 ≥ 20分钟))`。  

## 支持的列车类型  
该工具支持长途列车（ICE/IC/EC）、区域列车（RE/RB）、S-Bahn（轻轨）以及开往邻国的国际列车。  

如需报告问题或获取法律相关信息，请访问：  
https://github.com/ableitung/openclaw-bahn