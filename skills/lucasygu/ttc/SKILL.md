---
description: 实时多伦多公共交通信息：公交车和有轨电车的到站时间、车辆追踪、警报通知以及车站查询功能
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

**重要提示：**  
始终直接使用 `ttc` 命令行工具来执行操作（例如：`ttc nearby`）。切勿使用 `node src/cli.js` 或 `node dist/cli.js`——`ttc` 命令已全局安装，随时可用。

该工具可实时追踪多伦多的公交车和有轨电车信息：提供下一班车的到达时间、车辆位置、服务公告以及车站查询功能，所有信息均可在终端中获取。

## 先决条件  
- Node.js 22 及更高版本  
- 无需身份验证——所有数据源均为公开信息  

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
显示指定车站的下一班车的到达时间。支持输入车站名称（支持模糊匹配）、车站 ID 或车站代码。  

### `ttc route <路线编号>`  
显示路线信息：包括路线类型（公交车/有轨电车）、行驶方向/路标、在运行中的车辆数量以及服务公告。  

### `ttc vehicles [路线编号]`  
显示车辆的实时位置信息：包括车队编号、路线名称、车辆状态、当前所在车站及载客率。  

### `ttc alerts [路线编号]`  
查看该路线的服务中断情况及相关公告。使用 `--broad` 选项可同时获取地铁的相关信息。  

### `ttc nearby [纬度, 经度]`  
查找最近的车站及其预计到达时间。默认搜索半径为 500 米；在 macOS 系统上，若未提供坐标，会自动检测用户位置。  

### `ttc routes`  
列出所有地面交通路线。可通过 `--type bus` 或 `--type streetcar` 进行筛选。  

### `ttc search <查询内容>`  
根据名称进行模糊搜索；系统会自动去除不必要的词汇（如 “St”、“Ave”、“At” 等），以提高搜索准确性。  

### `ttc stops <路线编号>`  
列出该路线上当前正在运行的车站列表（数据来源于实时车辆信息和预测结果）。  

### `ttc status`  
系统概览：显示在运行的车辆数量、活跃路线数量以及公告数量；同时还会显示静态数据的更新频率。  

## 全局选项  
所有命令均支持以下选项：  
- `--json`：以 JSON 格式输出结果，便于脚本或自动化工具使用。  

### `ttc loop <间隔时间> <命令> [参数...]`  
按指定间隔重复执行指定的 `ttc` 命令。系统会自动清除屏幕内容并更新结果。按下 Ctrl+C 可停止循环执行。  
间隔时间格式示例：`30s`、`3m`、`1h` 或纯数字（例如：`180`）。  

```bash
ttc loop 3m next "king spadina"    # Watch arrivals while getting ready
ttc loop 5m alerts                 # Monitor disruptions during storms
ttc loop 2m vehicles 504           # Track vehicles approaching your stop
ttc loop 30s nearby                # Refresh nearby arrivals as you walk
```  

## 数据来源  
- **实时数据**：来自 `bustime.ttc.ca` 的 GTFS-RT 协议数据（无需身份验证）  
- **静态数据**：来自 Open Toronto GTFS 的预打包车站/路线/行程信息  
- **覆盖范围**：仅包括地面交通（公交车和有轨电车）；地铁相关公告可通过 `--broad` 选项获取。