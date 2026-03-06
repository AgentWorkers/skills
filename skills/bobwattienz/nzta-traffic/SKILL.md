---
name: nzta-traffic
description: 通过 Waka Kotahi NZTA 交通与旅行 API 查询新西兰各州高速公路的实时交通状况。该 API 可用于查看道路事件、事故、封闭情况、道路施工信息以及交通摄像头数据，适用于新西兰所有 14 个地区（从北地到南地）。无需 API 密钥即可使用。示例查询语句包括：“交通情况如何？”、“是否有道路封闭？”、“查看 SH1 公路的交通状况？”或“惠灵顿附近的交通摄像头情况”。
---
# NZTA 交通信息

通过 Waka Kotahi 交通与旅行 REST API 查询新西兰各地的高速公路实时路况。

## 快速入门

- 检查某个地区的道路事件：  
  ```bash
scripts/nzta-traffic.sh --region Wellington
```

- 检查特定的高速公路：  
  ```bash
scripts/nzta-traffic.sh --journey 10
```

- 检查某个地区的交通摄像头：  
  ```bash
scripts/nzta-traffic.sh --cameras --region Wellington
```

## 脚本使用方法  

```
scripts/nzta-traffic.sh [options]

Options:
  --region <name|id>    Region name or ID (e.g. "Wellington" or "9")
  --journey <id>        Journey/highway ID (e.g. 10 for SH1 Wellington)
  --bbox <minlon,minlat,maxlon,maxlat>  Bounding box query
  --cameras             List traffic cameras instead of events
  --list-regions        List all region names and IDs
  --list-journeys       List journeys for a region (requires --region)
  --json                Output raw JSON instead of formatted summary
  --zoom <level>        Geometry zoom level, -1 for no geometry (default: -1)
```

## 地区与行程查询  

运行 `--list-regions` 命令获取地区 ID，然后使用 `--list-journeys --region <地区名称>` 命令查找该地区的高速公路行程 ID。  
常见的惠灵顿地区行程包括：SH1（ID 10）、SH2（ID 9）、SH58（ID 12）、SH59（ID 341）。  

有关完整的端点参考和响应字段描述，请参阅 [references/api-endpoints.md](references/api-endpoints.md)。  

## 事件影响等级  

- **封闭** — 道路已封闭  
- **严重延误** — 预计会有严重延误  
- **轻微延误** — 有部分延误  
- **注意** — 请谨慎行驶  
- **观察情况** — 仅供参考  

## 注意事项  

- API 基址：`https://trafficnz.info/service/traffic/rest/4/`  
- 无需身份验证  
- 返回的数据格式为 JSON，请求头需设置为 `Accept: application/json`  
- 如果响应内容为空（`"response": ""`），则表示没有活跃的事件——这是个好消息