---
name: red-alert
version: 1.2.0
description: **Israel Red Alert API** — 提供实时及历史火箭/导弹警报数据。支持按城市、时间范围查询警报信息，并生成避难所需时间的统计报告。该API通过 `redalert.orielhaim.com`（使用 Socket.IO 协议实现实时数据传输）和 `tzevaadom.co.il`（提供历史数据，采用 REST 接口）来获取数据。
provides:
  - capability: israel-alerts
    methods: [history, realtime, shelter-stats]
credentials:
  - name: RED_ALERT_API_KEY
    required: false
    description: API key from redalert.orielhaim.com — optional, used for authenticated socket.io real-time connection. History via tzevaadom works without any key.
dependencies:
  - name: socket.io-client
    type: npm
    required: false
    description: Only needed for real-time alerts (realtime.mjs). History analysis works without it.
---
# Red Alert — 以色列紧急警报系统

提供以色列各城市的实时和历史警报数据，支持追踪火箭弹警报、计算避难时间以及生成图表。

## 获取 API 密钥

请访问 **<https://redalert.orielhaim.com/>** 注册以获取您的 API 密钥，并将其设置为环境变量 `RED_ALERT_API_KEY`。

该工具基于 RedAlert API 开发，提供了便捷的命令行界面（CLI）工具，用于查询、分析和可视化警报数据。

## 端点参考

有关该工具使用的完整端点信息（包括 REST、Socket.IO 和认证机制），请参阅：`references/ENDPOINTS.md`

## 数据来源

| 数据源 | 数据类型 | 认证方式 | 用途 |
|--------|------|------|---------|
| `api.tzevaadom.co.il` | REST | 无 | 最近 24 小时的警报历史记录（50 条记录） |
| `redalert.orielhaim.com` | Socket.IO | `RED_ALERT_API_KEY` | 实时警报信息及系统状态 |

## 设置

```bash
# API key is stored as Fly secret: RED_ALERT_API_KEY
# Socket.io client needed for real-time
cd /data/clawd/skills/red-alert/scripts && npm install
```

## 快速使用方法

### 获取警报历史记录（REST 请求）
```bash
# Last ~24h of alerts nationwide (50 most recent alert groups)
curl -s "https://api.tzevaadom.co.il/alerts-history" -o /tmp/alerts.json
```

响应格式：
```json
[{
  "id": 5718,
  "description": null,
  "alerts": [{
    "time": 1772352828,     // Unix timestamp
    "cities": ["כפר סבא", "תל אביב"],
    "threat": 0,            // 0=rockets, 1=aircraft, 5=infiltration
    "isDrill": false
  }]
}]
```

### 检查系统状态
```bash
curl -s -H "Accept: application/json" "https://redalert.orielhaim.com/api/status"
```

### 实时警报（Socket.IO）
```bash
node /data/clawd/skills/red-alert/scripts/realtime.mjs
# Listens for: alert, rockets, hostileAircraftIntrusion, tsunami, earthquake
```

### 分析特定城市的避难时间
```bash
node /data/clawd/skills/red-alert/scripts/analyze.mjs --city "כפר סבא" --since "2026-02-28T08:00"
# Outputs: alert count, shelter sessions, total shelter time, hourly data as JSON
```

## 预警类型

| 预警代码 | 希伯来语类型 | 英语类型 | 避难时间 |
|------|---------------|----------------|--------------|
| 0 | רקטות וטילים | Rockets & Missiles | 15 秒至 90 秒（因城市而异） |
| 1 | חדירת כלי טיס עוין | Hostile Aircraft | 10 分钟 |
| 2 | רעידת אדמה | Earthquake | 直到安全为止 |
| 3 | צונאמי | Tsunami | 立即撤离海岸 |
| 5 | חדירת מחבלים | Terrorist Infiltration | 坚持待在室内 |

## 各地区的避难时间（针对火箭弹警报）

| 地区 | 避难时间 |
|--------|------|
| 加沙地带 | 15 秒 |
| 阿什凯隆、斯德罗特 | 30 秒 |
| 比尔谢巴、阿什多德 | 45 秒 |
| 特拉维夫、克法尔萨巴、内坦亚 | 90 秒 |
| 海法、哈德拉 | 60 秒 |
| 北部地区（边境） | 30 秒 |

## 与图表/表格工具结合使用

```bash
# Generate hourly alert chart
node /data/clawd/skills/red-alert/scripts/analyze.mjs --city "כפר סבא" --since "2026-02-28T08:00" --format chart-json \
  | node /data/clawd/skills/chart-image/scripts/chart.mjs --type bar --dark --title "Kfar Saba Alerts" --output alerts.png

# Generate shelter session table
node /data/clawd/skills/red-alert/scripts/analyze.mjs --city "כפר סבא" --since "2026-02-28T08:00" --format table-json \
  | node /data/clawd/skills/table-image/scripts/table.mjs --dark --title "Shelter Sessions" --output shelter.png
```

## 架构说明

- **redalert.orielhaim.com**：Oriel Haim 提供的服务，通过 Socket.IO 从 Pikud HaOref 获取数据。该服务具有更完善的 API 密钥管理机制。部分 REST 端点受到 Cloudflare 的访问限制（`/api/status` 端点除外）。
- **api.tzevaadom.co.il**：免费 REST API，无需认证，可查询最近 24 小时的警报历史记录。
- **Pikud HaOref（oref.org.il）**：来自云服务器的请求会被 Akamai WAF 拒绝。

## 限制事项

- 历史数据仅保留最近 24 小时的记录（约 50 条记录）；
- 如需更长时间的记录，需通过 Socket.IO 监听器自行存储数据；
- 实时警报功能需要保持稳定的 Socket.IO 连接。