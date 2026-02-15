---
name: gaode_map
description: 一项用于与高德地图（AMap）交互的技能，用于位置搜索和路线规划。
metadata:
  openclaw:
    requires:
      env: ["AMAP_API_KEY"]
      bins: ["python"]
---
# 高德地图技能

该技能允许您使用高德地图（AMap）API来搜索地点和规划路线。

## 使用方法

您可以使用`amap_tool.py`脚本来执行相关操作。API密钥应设置为`AMAP_API_KEY`环境变量。

### 地点搜索
用于搜索兴趣点（POIs）。

**命令：**
```bash
python amap_tool.py search --keywords "<keywords>" [--city "<city>"]
```

**参数：**
- `keywords`：搜索关键词（例如：“餐厅”、“加油站”）。
- `city`：（可选）搜索的城市。

### 路线规划
用于规划两个地点之间的路线。

**命令：**
```bash
python amap_tool.py route --origin "<origin>" --destination "<destination>" [--mode "<mode>"] [--city "<city>"]
```

**参数：**
- `origin`：起点位置（地址或坐标“lon,lat”）。
- `destination`：终点位置（地址或坐标“lon,lat”）。
- `mode`：（可选）路线模式：`driving`（默认）、`walking`、`bicycling`、`transit`。
- `city`：（可选）城市名称（对于`transit`模式是必需的，或有助于地理编码）。

## 示例

**用户：**“在上海市查找咖啡店。”
**操作：**
```bash
python amap_tool.py search --keywords "coffee shop" --city "Shanghai"
```

**用户：**“显示从北京西站到故宫的驾车路线。”
**操作：**
```bash
python amap_tool.py route --origin "Beijing West Station" --destination "Forbidden City" --mode "driving" --city "Beijing"
```