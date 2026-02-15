---
name: trimet
description: 获取波特兰的公共交通信息，包括列车到达时间、行程规划以及相关提醒。当用户询问关于波特兰的公交车、MAX（轻轨系统）或火车的交通情况时，可以使用此功能。
homepage: https://trimet.org
metadata:
  clawdbot:
    emoji: "🚃"
    requires:
      bins: ["trimet"]
      env: ["TRIMET_APP_ID"]
---

# TriMet CLI

TriMet CLI 是一个用于查询波特兰公共交通数据的命令行工具，支持查看列车到站信息、规划出行路线以及获取服务提醒等功能。

## 安装

```bash
npm install -g trimet-cli
```

## 设置

1. 从 [https://developer.trimet.org/](https://developer.trimet.org/) 获取免费的 API 密钥。
2. 设置环境变量：`export TRIMET_APP_ID="your-key"`。

## 命令

### 查看列车到站信息

```bash
trimet arrivals <stop-id>              # Real-time arrivals
trimet arrivals 8383 --line 90         # Filter by route
trimet arrivals 8383 --json
```

### 规划出行路线

```bash
trimet trip -f <from> -t <to>
trimet trip -f 8383 -t 9969
trimet trip -f "Pioneer Square" -t "PDX Airport"
trimet trip -f 8383 -t 9969 --arrive-by "5:30 PM"
trimet trip -f 8383 -t 9969 --depart-at "2:00 PM"
trimet trip -f 8383 -t 9969 --json
```

### 查看下一班列车发车时间

```bash
trimet next -f <from> -t <to>          # Simplified view
trimet next -f 8383 -t 9969 -c 5       # Show 5 options
trimet next -f 8383 -t 9969 --line 90  # Filter by route
```

### 查看服务提醒

```bash
trimet alerts                          # All alerts
trimet alerts --route 90               # Alerts for route
trimet alerts --json
```

## 常见站点代码

- Pioneer Courthouse Square: 8383（西行），8384（东行）
- PDX 机场: 10579
- 波特兰联合车站: 7787
- Beaverton TC: 9969

## 使用示例

**用户：“下一班 MAX 列车是什么时候？”**
```bash
trimet arrivals 8383
```

**用户：“我怎么去机场？”**
```bash
trimet trip -f "Pioneer Square" -t "PDX Airport"
```

**用户：“我需要在下午 5 点前到达市中心。”**
```bash
trimet trip -f <user-location-stop> -t 8383 --arrive-by "5:00 PM"
```

**用户：“蓝线有延误吗？”**
```bash
trimet alerts --route 100
```

**用户：“下一班去 Beaverton 的列车是哪一班？”**
```bash
trimet next -f 8383 -t 9969
```

## 路线编号

- MAX 蓝线: 100
- MAX 红线: 90
- MAX 黄线: 190
- MAX 橙线: 290
- MAX 绿线: 200

## 注意事项

- 站点代码可以在 TriMet 的站点标识牌以及 [trimet.org](https://developer.trimet.org/) 上找到。
- 地址可用于规划出行路线（例如：“Pioneer Square, Portland”）。
- 时间支持自然格式（如 “5:30 PM” 或 “17:30”）。