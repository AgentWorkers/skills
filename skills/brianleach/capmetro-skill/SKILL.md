---
name: capmetro-skill
description: >
  **Austin CapMetro 公交/地铁交通服务**  
  提供实时车辆位置信息、预计到站时间、服务提醒、路线详情以及公交（MetroBus）和地铁（MetroRail/MetroRapid）的出行规划。适用于用户查询奥斯汀公共交通系统、公交时刻表、列车时刻、CapMetro服务更新或附近车站信息的情况。
homepage: "https://github.com/brianleach/capmetro-skill"
license: MIT
metadata:
  clawdbot:
    emoji: "🚌"
    tags: [transit, austin, capmetro, transportation, bus, train, schedule]
    requires:
      bins: ["node", "unzip"]
      env: []
    files: ["scripts/capmetro.mjs", "scripts/gtfs-realtime.proto"]
    install:
      - id: npm-deps
        kind: shell
        command: "npm install --prefix $SKILL_DIR protobufjs"
        label: "Install protobufjs Node.js dependency"
---
# CapMetro 奥斯汀公共交通

提供奥斯汀 CapMetro 的实时交通信息——包括车辆位置、下一班次到达时间、服务提醒以及路线详情。无需 API 密钥。

## 使用场景

- 当用户询问奥斯汀的公交或火车时刻表、到达时间或延误情况时
- 当用户询问“下一班公交车/火车是什么时候”或“801 路线还在运行吗”时
- 当用户询问 CapMetro 的服务提醒、绕行路线或交通中断情况时
- 当用户想知道公交车/火车当前的位置时
- 当用户询问附近的站点或路线信息时
- 当用户提到 MetroRail（红线）、MetroRapid（801/803 路线）或其他奥斯汀公交路线时
- 当用户询问 CapMetro 的票价、乘车方式或一般交通信息时

## 数据来源

所有数据均**公开可用，无需 API 密钥**，托管在德克萨斯州开放数据门户（Texas Open Data Portal）上。

### GTFS-RT（实时）数据源（每 15 秒更新一次）

| 数据源 | 格式 | URL |
|------|--------|-----|
| 车辆位置 | JSON | `https://data.texas.gov/download/cuc7-ywmd/text%2Fplain` |
| 车辆位置 | Protobuf | `https://data.texas.gov/download/eiei-9rpf/application%2Foctet-stream` |
| 行程更新 | Protobuf | `https://data.texas.gov/download/rmk2-acnw/application%2Foctet-stream` |
| 服务提醒 | Protobuf | `https://data.texas.gov/download/nusn-7fcn/application%2Foctet-stream` |

### GTFS 静态数据源（路线/站点/时刻表）

| 数据源 | 格式 | URL |
|------|--------|-----|
| GTFS 静态数据（ZIP 文件） | ZIP | `https://data.texas.gov/download/r4v4-vz24/application%2Fx-zip-compressed` |

## 实现方式

### 快速入门：使用辅助脚本

位于 `scripts/` 目录中的脚本负责获取、解析和展示 CapMetro 数据。

### 脚本：`scripts/capmetro.mjs`

该脚本是主要的入口点，支持以下命令：

```bash
# Get current service alerts
node scripts/capmetro.mjs alerts

# Get real-time vehicle positions (optionally filter by route)
node scripts/capmetro.mjs vehicles [--route 801]

# Get next arrivals at a stop (by stop_id)
node scripts/capmetro.mjs arrivals --stop <stop_id>

# Get arrivals by searching stop name (uses best match)
node scripts/capmetro.mjs arrivals --stop-search "lakeline" --route 550

# Get arrivals filtered by direction/headsign
node scripts/capmetro.mjs arrivals --stop-search "downtown" --route 550 --headsign "lakeline"

# Get arrivals filtered by route at a stop
node scripts/capmetro.mjs arrivals --stop <stop_id> --route 801

# Search for stops by name or location
node scripts/capmetro.mjs stops --search "domain" 
node scripts/capmetro.mjs stops --near 30.4,-97.7

# List all routes
node scripts/capmetro.mjs routes

# Get route details including stops
node scripts/capmetro.mjs route-info --route 801

# Download/refresh GTFS static data (run periodically)
node scripts/capmetro.mjs refresh-gtfs
```

### 设置：GTFS 静态数据

首次使用时，运行 `node scripts/capmetro.mjs refresh-gtfs` 命令，将 GTFS 静态数据（路线、站点、时刻表）下载并解压到 `~/.capmetro/gtfs/` 目录。只需在 CapMetro 更新时刻表时（通常每季度或服务变更时）重新下载这些数据。

### 主要路线参考

| 路线 | 名称 | 类型 |
|-------|------|------|
| 550 | MetroRail 红线 | 地铁（Leander ↔ 奥斯汀市中心） |
| 801 | MetroRapid 北线/南线 | 快速公交（Tech Ridge ↔ Southpark Meadows） |
| 803 | MetroRapid Burnet/South Lamar | 快速公交（Domain ↔ Westgate） |
| 1 | N Lamar/S Congress | 本地公交 |
| 7 | Duval/Dove Springs | 本地公交 |
| 10 | S 1st/Red River | 本地公交 |
| 20 | Manor Rd/Riverside | 本地公交 |
| 300 | Oltorf/Riverside Crosstown | 城市间公交 |
| 325 | Ohlen/Loyola | 城市间公交 |
| 985 | 夜间公交（Night Owl） | 夜间服务 |

### 用户提示

- **站点 ID** 可以在 CapMetro 的站点标识牌上找到，也可以通过 Transit 应用程序查询，或使用 `stops` 命令搜索获得
- **MetroRapid 801/803** 的班次最为频繁（高峰时段每 10-12 分钟一班）
- **MetroRail 红线（550）** 从 Leander 开往奥斯汀市中心，班次较少
- 服务提醒中通常会包含绕行信息——在提供路线建议前请先查看提醒
- 车辆位置数据每约 15 秒更新一次，因此位置信息几乎实时

### 错误处理

- 如果数据源返回错误或为空数据，应告知用户实时数据可能暂时不可用
- 如果 Protobuf 解析失败，JSON 格式的车辆位置数据更易于解析，可作为备用方案
- 获取站点名称、路线名称和时刻表信息需要 GTFS 静态数据——请确保已成功下载这些数据

### 响应格式

在向用户展示交通信息时：
- 首先提供最实用的信息（下一班次到达时间、当前服务提醒）
- 包括路线编号和名称（例如：“801 MetroRapid 路线”）
- 以 12 小时制显示时间（含 AM/PM）
- 对于延误情况，同时显示计划到达时间和预计到达时间
- 对于车辆位置，尽可能结合地标描述具体位置
- 如果用户查询的路线有服务提醒，务必提及这些提醒

## 票价信息（截至 2025 年）

| 票价类型 | 价格 |
|-----------|-------|
| 本地公交 / MetroRapid | $1.25 |
| MetroRail | $3.50（单程） |
| 日票 | $2.50 |
| 7 天票 | $11.25 |
| 31 天票 | $41.25 |

支持通过 Umo 应用程序、扫码支付或票卡支付。2 小时内可免费换乘其他线路。

## 外部接口

| 接口 | 发送的数据 | 接收的数据 |
|----------|-----------|---------------|
| `data.texas.gov/download/cuc7-ywmd/...` | 无（仅 GET 请求） | 车辆位置（JSON 格式） |
| `data.texas.gov/download/eiei-9rpf/...` | 无（仅 GET 请求） | 车辆位置（Protobuf 格式） |
| `data.texas.gov/download/rmk2-acnw/...` | 无（仅 GET 请求） | 行程更新（Protobuf 格式） |
| `data.texas.gov/download/nusn-7fcn/...` | 无（仅 GET 请求） | 服务提醒（Protobuf 格式） |
| `data.texas.gov/download/r4v4-vz24/...` | 无（仅 GET 请求） | GTFS 静态数据（ZIP 文件） |

所有接口均来自德克萨斯州开放数据门户，无需 API 密钥、身份验证或用户数据传输。

## 安全与隐私

- **无需任何凭证**——所有数据源均公开可用，无需 API 密钥或令牌 |
- **不传输用户数据**——所有请求均为匿名 GET 请求，不包含用户信息 |
- **仅使用本地存储**——GTFS 静态数据会缓存在 `~/.capmetro/gtfs/` 目录中，不会写入其他地方 |
- **无数据传输**——该功能不会发送任何使用数据 |
- **输入处理**——用户输入的站点名称和路线 ID 仅用于本地过滤，不会用于构建 URL 或 shell 命令

## 信任声明

本功能仅从德克萨斯州开放数据门户获取公开可用的交通数据，不会访问、存储或传输任何个人信息。所有网络请求均为只读的 GET 请求，用于获取政府公开数据。