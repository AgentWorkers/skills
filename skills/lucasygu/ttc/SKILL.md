---
description: 实时多伦多公共交通信息：公交车和有轨电车的到站时间、车辆追踪、实时警报以及车站查询功能
allowed-tools: Bash, Read
name: ttc
version: 0.1.0
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

提供多伦多公交和有轨电车的实时追踪服务。您可以查询下一班车的到达时间、车辆位置、服务状态信息以及车站查询等功能，所有操作均可在终端界面完成。

## 前提条件

- 需要安装 Node.js 22 及更高版本。
- 无需身份验证——所有数据源均为公开信息。

## 快速参考

```bash
ttc next "king spadina"           # Next arrivals at a stop
ttc next 8126                     # By stop code
ttc route 504                     # Route info + active vehicles
ttc vehicles 504                  # Live positions on a route
ttc alerts                        # Service alerts
ttc alerts --broad                # Include subway alerts
ttc nearby 43.6426,-79.4002       # Nearest stops + arrivals
ttc stops 504                     # Active stops on a route
ttc routes                        # List all surface routes
ttc routes --type streetcar       # Filter by type
ttc search "broadview station"    # Fuzzy stop search
ttc status                        # System overview
```

## 命令说明

### `ttc next <车站名称>`
显示指定车站的下一班公交车/有轨电车的到达时间。支持输入车站名称（支持模糊匹配）、车站 ID 或车站代码。

### `ttc route <路线编号>`
显示路线信息：包括路线类型（公交/有轨电车）、行驶方向/路标、在运行中的车辆数量以及任何服务异常情况。

### `ttc vehicles [路线编号>`
查看车辆的实时位置信息，包括车辆编号、所属路线、当前行驶状态、当前所在车站以及车内乘客人数。

### `ttc alerts [路线编号>`
查询该路线的服务异常情况。使用 `--broad` 选项可同时获取地铁的相关警报信息。

### `ttc nearby <纬度, 经度>`
查找最近的公交/有轨电车站点及其预计到达时间。默认搜索半径为 500 米。

### `ttc routes`
列出所有地面交通路线。可通过 `--type bus` 或 `--type streetcar` 进行筛选。

### `ttc search <查询内容>`
通过名称进行模糊搜索。系统会自动去除无关词汇（如 “St”、“Ave”、“At” 等），以提高搜索精度。

### `ttc stops <路线编号>`
列出该路线上当前正在运行的车站列表（数据来源于车辆实时位置信息和预测数据）。

### `ttc status`
查看系统整体运行状态：包括在运行中的车辆数量、活跃路线数量以及数据更新的频率。

## 全局选项

所有命令均支持以下选项：
- `--json` — 以 JSON 格式输出结果，便于脚本或自动化工具使用。

## 数据来源

- **实时数据**：来自 `bustime.ttc.ca` 的 GTFS-RT 协议数据（无需身份验证）。
- **静态数据**：预打包的公交/有轨电车站点/路线/行程数据（来自 Open Toronto GTFS）。
- **覆盖范围**：仅包含地面交通（公交和有轨电车）。地铁相关警报信息可通过 `--broad` 选项获取。