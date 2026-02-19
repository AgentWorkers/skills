---
name: mvg
description: 慕尼黑公共交通（MVG）的命令行界面（CLI）及S-Bahn实时追踪服务。可用于查询出发时间、规划路线、查找附近车站、获取服务提醒以及实时查看S-Bahn的运行位置。当用户提及“MVG”、“S-Bahn”、“U-Bahn”、“慕尼黑公共交通”、“出发时间”、“换乘信息”或具体线路名称（如S8、U3等）时，系统会自动触发相关功能。
---
# MVG CLI

这是一个用于查询慕尼黑公共交通信息的命令行工具（CLI），支持通过非官方的MVG API（`bgw-pt/v3`）获取数据，无需身份验证。

## 安装与配置

- **命令行工具（CLI）**：`python3 <skill_dir>/mvg_cli.py`
- **依赖库**：Python 3以及`urllib`（仅使用其标准库功能）
- **S-Bahn实时数据**：需要`node`和`ws`模块来建立WebSocket连接以获取实时数据

## 命令列表

```bash
# Station search
mvg search "Marienplatz"

# Departures
mvg departures "Marienplatz"
mvg departures "Marienplatz" --type ubahn --limit 20
mvg departures "Daglfing" --offset 5          # +5min walking time

# Route planning (stations or addresses)
mvg route "Marienplatz" "Garching"
mvg route "Hauptstr. 1, München" "Flughafen"  # address support
mvg route "Pasing" "Ostbahnhof" --time "08:30" --mode less-changes

# Nearby stations
mvg nearby                                     # default coords
mvg nearby 48.1351 11.5820

# Service alerts
mvg alerts
mvg alerts --station "Marienplatz"

# Lines
mvg lines --type sbahn

# S-Bahn live tracking (real-time via geOps WebSocket)
mvg live                                       # all S-Bahn lines
mvg live --line S3                             # specific line
```

所有命令都支持`--json`选项，以便输出结果以机器可读的JSON格式。

## 交通类型过滤

使用`--type`或`--exclude`参数进行过滤：
- `ubahn`（地铁）
- `sbahn`（轻轨）
- `bus`（公交车）
- `tram`（有轨电车）
- `bahn`（区域列车）
- `regionalbus`（区域巴士）
- `ruftaxi`（出租车）

## 路线查询选项

- `--mode`：`fast`（默认）、`less-changes`（减少换乘次数）、`less-walking`（减少步行距离）
- `--walk-speed`：`slow`（慢速）、`normal`（默认）、`fast`（快速）
- `--accessible`：仅显示适合轮椅使用的路线
- `--via "Station"`：通过指定站点进行路线查询
- `--arrive`：将`--time`参数解析为到达时间

## API说明

- **基础URL**：`https://www.mvg.de/api/bgw-pt/v3/`
- **API端点**：
  - `/locations`：位置信息
  - `/departures`：出发时刻
  - `/routes`：路线信息
  - `/stations/nearby`：附近车站
  - `/lines`：线路信息
  - `/messages`：实时消息
- **路线响应中的到达时间**：使用`to.plannedDeparture`字段（而非`plannedArrival`字段）
- **S-Bahn实时数据**：通过以下URL获取：
  - `wss://api.geops.io/realtime-ws/v1/`
  - 请求方法：`GET sbm_full` + `SUB sbm_full` + `BBOX`
- **延迟信息**：以毫秒为单位显示（来自geOps的数据）