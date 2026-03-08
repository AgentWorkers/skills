---
description: 实时多伦多公共交通信息：公交车和有轨电车的到站时间、车辆追踪、警报系统以及车站查询功能
allowed-tools: Bash, Read
name: ttc
version: 0.1.3
metadata:
  openclaw:
    requires:
      bins:
        - ttc
    install:
      - kind: node
        package: "@lucasygu/ttc"
        bins: [ttc]
    os: [macos, linux, windows]
    homepage: https://github.com/lucasygu/ttc-cli
tags:
  - ttc
  - toronto
  - transit
  - gtfs
  - bus
  - streetcar
  - realtime
  - productivity
---
# TTC CLI — 多伦多交通委员会（Toronto Transit Commission）

这是一个用于查询多伦多公交和有轨电车实时信息的命令行工具。你可以通过该工具查看公交车的下一班次、车辆位置、服务提醒以及车站信息等。

## 先决条件

- 需要安装 Node.js 22 及更高版本。
- 无需身份验证——所有数据源都是公开的。

## 快速参考

```bash
ttc next "king spadina"           # Next arrivals at a stop
ttc next 8126                     # By stop code
ttc route 504                     # Route info + active vehicles
ttc vehicles 504                  # Live positions on a route
ttc alerts                        # Service alerts
ttc alerts --broad                # Include subway alerts
ttc nearby                        # Auto-detect location (macOS)
ttc nearby 43.6453,-79.3806       # Or provide coordinates
ttc stops 504                     # Active stops on a route
ttc routes                        # List all surface routes
ttc routes --type streetcar       # Filter by type
ttc search "broadview station"    # Fuzzy stop search
ttc status                        # System overview
ttc loop 3m nearby                # Live monitor (refreshes every 3m)
```

## 命令说明

### `ttc next <车站名称>`
显示指定车站的下一班次信息。支持输入车站名称（支持模糊匹配）、车站 ID 或车站代码。

### `ttc route <路线编号>`
显示路线信息：包括路线类型（公交车/有轨电车）、行驶方向、当前在运行的车辆数量以及任何服务提醒。

### `ttc vehicles [路线编号>`
查看指定路线的车辆实时位置，包括车辆编号、路线名称、车辆状态、当前所在车站以及车内乘客数量。

### `ttc alerts [路线编号>`
获取该路线的服务中断信息。使用 `--broad` 选项可同时获取地铁的相关提醒。

### `ttc nearby [纬度, 经度]`
查找最近的车站及其预计到达时间。默认搜索半径为 500 米；在 macOS 系统上，若未提供坐标，工具会自动检测用户位置。

### `ttc routes`
列出所有地面交通路线。可以使用 `--type bus` 或 `--type streetcar` 进行筛选。

### `ttc search <查询内容>`
根据名称进行模糊搜索。系统会自动去除无关词汇（如 “St”、“Ave”、“At” 等），以提高搜索准确性。

### `ttc stops <路线编号>`
列出该路线上当前正在运行的车站列表（信息来源于实时车辆数据和预测数据）。

### `ttc status`
查看系统整体运行状态：包括正在运行的车辆数量、活跃路线数量以及数据更新的频率。

## 全局选项

所有命令都支持以下选项：
- `--json` — 以 JSON 格式输出结果，便于脚本或自动化工具使用。

### `ttc loop <间隔时间> <命令> [参数...]`
定期重复执行指定的命令。工具会自动清除屏幕内容并更新数据。按 Ctrl+C 可停止循环执行。
- 间隔时间格式示例：`30s`、`3m`、`1h` 或纯数字（例如 `180`）。

```bash
ttc loop 3m next "king spadina"    # Watch arrivals while getting ready
ttc loop 5m alerts                 # Monitor disruptions during storms
ttc loop 2m vehicles 504           # Track vehicles approaching your stop
ttc loop 30s nearby                # Refresh nearby arrivals as you walk
```

## 数据来源

- **实时数据**：来自 `bustime.ttc.ca` 的 GTFS-RT 协议数据（无需身份验证）。
- **静态数据**：来自 Open Toronto GTFS 的预打包车站/路线/行程数据。
- **覆盖范围**：仅包含地面交通（公交车和有轨电车）；地铁相关信息可通过 `--broad` 选项获取。