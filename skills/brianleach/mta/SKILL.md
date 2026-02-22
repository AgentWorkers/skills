---
name: mta
description: NYC MTA交通服务：提供纽约市地铁和公交系统的实时列车到站信息、公交预测、服务提醒以及路线详情。当用户询问有关纽约市公共交通、地铁时刻表、MTA公交到站时间、服务提醒或附近车站的信息时，可使用该服务。
homepage: "https://github.com/brianleach/mta-skill"
license: MIT
metadata:
  clawdbot:
    emoji: "🚇"
    tags: [transit, nyc, mta, transportation, subway, bus, train, schedule]
    requires:
      bins: ["node"]
      env: ["MTA_BUS_API_KEY"]
    files: ["scripts/mta.mjs", "proto/gtfs-realtime.proto", "proto/nyct-subway.proto"]
    install:
      - id: npm-deps
        kind: shell
        command: "npm install --prefix $SKILL_DIR"
        label: "Install Node.js dependencies (protobufjs)"
---
# 纽约市交通管理局（NYC MTA）交通信息

提供纽约市交通管理局（MTA）的实时交通数据，包括地铁到站信息（GTFS-RT 协议格式）、公交车预测（SIRI JSON API）、服务警报以及路线信息。地铁相关功能无需任何配置即可使用；而公交车数据则需要一个免费的 API 密钥。

## 使用场景

- 用户查询纽约市的地铁、MTA 系统、具体线路（如 1/2/3 号线、A/C/E 线、N/Q/R/W 线等）  
- 用户询问“下一班地铁何时到达”  
- 用户提及特定的纽约市地铁站（如时代广场、宾州车站、中央车站、联合广场等）  
- 用户询问纽约市的公交路线（如 M1、B52、Bx12、Q44、S79 等线路）  
- 用户询问 MTA 的服务警报、延误情况、计划中的维修工作或周末的运营变更  
- 用户询问 MTA 的票价、MetroCard 或 OMNY 支付方式  
- 用户询问地铁的运行状态或周末的运营安排  
- 用户询问纽约市附近的地铁站或公交车站  

## 数据来源

纽约市交通管理局由多个交通机构组成，它们提供不同格式的数据：

### 地铁实时数据（GTFS-RT 协议格式，无需 API 密钥）

数据按线路分组提供。每个数据源返回一个包含 NYCT 扩展名的 protobuf 格式文件：

| 数据源 | 所服务线路 | URL |
|------|-------|-----|
| 1234567/GS | 1、2、3、4、5、6、7 号线及中央车站班车 | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs` |
| ACE | A、C、E 线及洛克威班车 | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs-ace` |
| BDFM | B、D、F、M 号线 | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs-bdfm` |
| G | G 号线 | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs-g` |
| JZ | J、Z 号线 | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs-jz` |
| L | L 号线 | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs-l` |
| NQRW | N、Q、R、W 号线 | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs-nqrw` |
| SIR | 斯坦顿岛铁路 | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs-si` |

数据更新频率约为每 30 秒，无需 API 密钥。

### 公交实时数据（SIRI JSON API，需要 `MTA_BUS_API_KEY`）

您可以在以下链接获取免费 API 密钥：  
https://register.developer.obanyc.com/

| API 端点 | 功能描述 |  
|----------|-------------|  
| SIRI StopMonitoring | 查看特定公交车站的到站信息 |  
| SIRI VehicleMonitoring | 查看某条公交线路上的所有车辆信息 |  
| OneBusAway Stop Info | 提供车站详情及附近车站信息 |  
| OneBusAway Routes | 查询公交路线信息 |  

请求频率限制为每 30 秒 1 次。

### 服务警报（GTFS-RT 协议格式，无需 API 密钥）

| 数据源 | URL |  
|------|-----|  
| Subway Alerts | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys/subway-alerts` | 地铁服务警报 |  
| Bus Alerts | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys/bus-alerts` | 公交服务警报 |  
| All Alerts | `https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys/all-alerts` | 所有服务警报 |  

### GTFS 静态数据（仅限下载）

| 数据源 | URL |  
|------|-----|  
| Subway | `http://web.mta.info/developers/data/nyct/subway/google_transit.zip` | 地铁静态数据（ZIP 文件） |  

## 实现方式

### 脚本：`scripts/mta.mjs`

这是主要的脚本入口点，支持以下命令：

```bash
# Subway arrivals
node scripts/mta.mjs arrivals --stop-search "times square"
node scripts/mta.mjs arrivals --stop-search "penn station" --line A
node scripts/mta.mjs arrivals --stop 127N
node scripts/mta.mjs arrivals --station "Grand Central"

# Bus arrivals (requires MTA_BUS_API_KEY)
node scripts/mta.mjs bus-arrivals --stop MTA_308209
node scripts/mta.mjs bus-arrivals --stop MTA_308209 --route M1

# Vehicle tracking
node scripts/mta.mjs vehicles --line 1
node scripts/mta.mjs bus-vehicles --route B52

# Service alerts
node scripts/mta.mjs alerts
node scripts/mta.mjs alerts --subway
node scripts/mta.mjs alerts --bus
node scripts/mta.mjs alerts --line A

# Routes and stops
node scripts/mta.mjs routes
node scripts/mta.mjs bus-routes
node scripts/mta.mjs stops --search "grand central"
node scripts/mta.mjs stops --near 40.7484,-73.9856
node scripts/mta.mjs bus-stops --near 40.7484,-73.9856
node scripts/mta.mjs bus-stops --route M1
node scripts/mta.mjs route-info --line A

# Maintenance
node scripts/mta.mjs refresh-gtfs
```

### 公交 API 密钥设置

地铁和警报相关功能无需任何配置。对于公交车相关功能，请按照以下步骤设置 API 密钥：

1. 在 [https://register.developer.obanyc.com/](https://register.developer.obanyc.com/) 获取免费 API 密钥。
2. 将密钥设置为环境变量 `MTA_BUS_API_KEY`。

### GTFS 静态数据更新

首次使用脚本时，运行 `node scripts/mta.mjs refresh-gtfs` 命令，将地铁车站/路线数据下载到 `~/.mta/gtfs/` 目录中。数据每小时更新一次。

### 纽约市地铁线路参考

| 线路 | 颜色 | 路线名称 | 起终点站 |
|------|-------|-------|-----------|
| 1 | 红色 | 7th Ave Local | Van Cortlandt Park-242 St ↔ South Ferry |  
| 2 | 红色 | 7th Ave Express | Wakefield-241 St ↔ Flatbush Ave-Brooklyn College |  
| 3 | 红色 | 7th Ave Express | Harlem-148 St ↔ New Lots Ave |  
| 4 | 绿色 | Lexington Ave Express | Woodlawn ↔ Crown Heights-Utica Ave |  
| 5 | 绿色 | Lexington Ave Express | Eastchester-Dyre Ave ↔ Flatbush Ave-Brooklyn College |  
| 6 | 绿色 | Lexington Ave Local | Pelham Bay Park ↔ Brooklyn Bridge-City Hall |  
| 7 | 紫色 | Flushing | Flushing-Main St ↔ 34 St-Hudson Yards |  
| A | 蓝色 | 8th Ave Express | Inwood-207 St ↔ Far Rockaway / Ozone Park-Lefferts Blvd |  
| C | 蓝色 | 8th Ave Local | 168 St ↔ Euclid Ave |  
| E | 蓝色 | 8th Ave Local | Jamaica Center ↔ World Trade Center |  
| B | 橙色 | 6th Ave Express | Bedford Park Blvd ↔ Brighton Beach |  
| D | 橙色 | 6th Ave Express | Norwood-205 St ↔ Coney Island-Stillwell Ave |  
| F | 橙色 | 6th Ave Local | Jamaica-179 St ↔ Coney Island-Stillwell Ave |  
| M | 橙色 | 6th Ave Local | Middle Village-Metropolitan Ave ↔ Forest Hills-71 Ave |  
| G | 浅绿色 | Brooklyn-Queens Crosstown | Court Sq ↔ Church Ave |  
| J | 棕色 | Nassau St | Jamaica Center ↔ Broad St |  
| Z | 棕色 | Nassau St Express | Jamaica Center ↔ Broad St（仅高峰时段） |  
| L | 灰色 | 14th St-Canarsie | 8 Ave ↔ Canarsie-Rockaway Pkwy |  
| N | 黄色 | Broadway Express | Astoria-Ditmars Blvd ↔ Coney Island-Stillwell Ave |  
| Q | 黄色 | Broadway Express | 96 St ↔ Coney Island-Stillwell Ave |  
| R | 黄色 | Broadway Local | Forest Hills-71 Ave ↔ Bay Ridge-95 St |  
| W | 黄色 | Broadway Local | Astoria-Ditmars Blvd ↔ Whitehall St-South Ferry |  
| S | 灰色 | 42nd St Shuttle | Times Sq-42 St ↔ Grand Central-42 St |  
| S | 灰色 | Franklin Ave Shuttle | Franklin Ave ↔ Prospect Park |  
| S | 灰色 | Rockaway Park Shuttle | Broad Channel ↔ Rockaway Park-Beach 116 St |  
| SIR | 蓝色 | 斯坦顿岛铁路 | St George ↔ Tottenville |  

### 主要公交路线参考

| 路线 | 名称 | 所在行政区 |  
|-------|------|---------|  
| M1 | 5th Ave / Madison Ave | 曼哈顿 |  
| M15 | 1st Ave / 2nd Ave | 曼哈顿 |  
| M34 | 34th Street Crosstown | 曼哈顿 |  
| M42 | 42nd Street Crosstown | 曼哈顿 |  
| M60 | 拉瓜迪亚机场专线 | 曼哈顿/皇后区 |  
| B44 | Nostrand Ave | 布鲁克林 |  
| B52 | Gates Ave/Greene Ave | 布鲁克林 |  
| Bx12 | Fordham Road/Pelham Pkwy | 布朗克斯 |  
| Q44 | Merrick Blvd/Cross Island | 皇后区 |  
| S79 | Hylan Blvd | 斯坦顿岛 |  
| X27 | Bay Ridge-曼哈顿市中心专线 | 布鲁克林 |  

### MTA 票价参考（2025 年）

| 票价类型 | 价格 |  
|-----------|-------|  
| 地铁/公交车（使用 OMNY 或 MetroCard） | $2.90 |  
| 公交转地铁/地铁转公交 | 2 小时内免费 |  
| 快速公交 | $7.00 |  
| 7 天无限次票 | $34.00 |  
| 单次乘车（仅限自动售票机） | $3.25 |  
| 减价票 | $1.45 |  

支付方式包括 OMNY（非接触式支付）、MetroCard 或 Ventra。使用 OMNY 可在 2 小时内免费换乘地铁和公交车。

### 用户提示

- **地铁车站编号** 以 `N`（北行/上城方向）或 `S`（南行/下城方向）结尾，例如：`127N` 表示时代广场北行方向。  
- **地铁功能无需配置**——任何地铁相关命令均无需 API 密钥。  
- **公交车需要免费 API 密钥**——请在 [https://register.developer.obanyc.com/](https://register.developer.obanyc.com/) 获取。  
- **服务警报始终可用**——无需密钥。  
- 存在多个地铁数据源，该技能会自动选择正确的数据源。  
- 使用 `--stop-search` 参数进行模糊搜索，使用 `--stop` 参数查询具体车站编号。  

### 错误处理

- 如果未设置 `MTA_BUS_API_KEY`，公交车相关命令会显示注册链接；地铁相关命令仍可正常使用。  
- 如果输入的车站/车站编号无效，系统会显示“未找到匹配的车站”。  
- 网络错误或 API 错误会显示友好的提示信息。  
- 如果地铁数据源返回空数据，可能表示实时数据暂时不可用。

### 数据展示格式

向用户展示交通信息时：

- 首先显示最实用的信息（如下一班车的到站时间、当前的服务警报）。  
- 显示线路名称及行驶方向（例如：“A 线列车即将到达 Far Rockaway，预计 3 分钟后到达”。  
- 如有轨道信息，会同时显示实际轨道与计划轨道。  
- 始终会显示所查询线路的当前服务警报。  
- 对于公交车，会显示路线、终点站及预计到达时间（以 12 小时制显示，包含 AM/PM）。  

## 外部 API 端点

| 端点 | 发送的数据 | 接收的数据 |  
|----------|-----------|---------------|  
| `api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs*` | 无（仅用于 GET 请求） | 地铁位置/到站信息（protobuf 格式） |  
| `api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys/*-alerts` | 无（仅用于 GET 请求） | 服务警报（protobuf 格式） |  
| `bustime.mta.info/api/siri/*` | 需要 API 密钥（查询参数） | 公交到站信息（JSON 格式） |  
| `bustime.mta.info/api/where/*` | 需要 API 密钥（查询参数） | 车站/路线查询（JSON 格式） |  
| `web.mta.info/developers/data/nyct/subway/*` | 无（仅用于 GET 请求） | 地铁静态数据（ZIP 文件） |  

地铁和警报相关的 API 可公开访问，无需认证。公交车 API 需要通过查询参数传递免费的 API 密钥。

## 安全与隐私政策

- **地铁数据**：无需提供任何凭证，数据可公开获取，无需 API 密钥或令牌。  
- **公交车数据**：需要使用免费的 API 密钥（通过 URL 查询参数传递给 MTA 的 BusTime API）。  
- **不传输用户数据**：请求内容仅包含 API 密钥、路线/车站标识符，不包含个人信息。  
- **数据存储**：GTFS 静态数据仅缓存在本地的 `~/.mta/gtfs/` 目录中，不会写入其他地方。  
- **无数据传输**：该技能不会发送任何数据到外部服务器，也不会收集用户使用情况。  
- **输入处理**：用户输入的车站名称和路线编号仅用于本地过滤，不会用于其他用途。  

## 信任声明

该技能仅从 MTA 官方提供的数据源获取交通信息。公交车 API 密钥仅用于 MTA BusTime API 的身份验证，不会访问、存储或传输用户的任何个人信息。