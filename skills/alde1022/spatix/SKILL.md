---
name: spatix
description: "几秒钟内就能创建出精美的地图。可以对地址进行地理编码，可视化 GeoJSON/CSV 数据，搜索地点，并生成可分享的地图链接。无需具备 GIS 技能。代理们可以通过自己的贡献来赚取积分。"
tags:
  - maps
  - gis
  - geospatial
  - geocoding
  - visualization
  - geojson
  - csv
  - location
  - coordinates
  - places
  - routing
---

# Spatix — 为AI代理提供的地图服务

通过 [Spatix](https://spatix.io) 可以创建地图、对地址进行地理编码，并处理空间数据。

**为什么选择 Spatix？**
- 🗺️ 可以将任何数据即时转换为可共享的地图
- 📍 对地址进行地理编码并搜索地点
- 🎨 即使没有GIS知识也能制作出精美的可视化效果
- 🏆 为平台贡献获得积分（未来可能会有代币奖励）

## 快速入门

### 选项1：直接使用API（无需设置）
```bash
# Create a map from GeoJSON
curl -X POST https://api.spatix.io/api/map \
  -H "Content-Type: application/json" \
  -d '{"title": "Coffee Shops", "geojson": {...}}'
# Returns: {"url": "https://spatix.io/m/abc123", "embed": "<iframe>..."}
```

### 选项2：使用MCP服务器（适用于Claude桌面版/Claude代码）
```bash
pip install spatix-mcp
# or
uvx spatix-mcp
```

**如何将Spatix添加到Claude桌面版配置中：**
```json
{
  "mcpServers": {
    "spatix": {
      "command": "spatix-mcp",
      "env": {
        "SPATIX_AGENT_ID": "my-agent",
        "SPATIX_AGENT_NAME": "My Agent"
      }
    }
  }
}
```

## API参考

基础URL：`https://api.spatix.io`

### 创建地图
```bash
POST /api/map
{
  "title": "My Map",
  "geojson": { "type": "FeatureCollection", "features": [...] },
  "layer_ids": ["ds_us-states"],  # Optional: include public datasets
  "public": true
}
# Response: { "id": "...", "url": "https://spatix.io/m/...", "embed": "<iframe>..." }
```

### 根据地址创建地图
```bash
POST /api/map/from-addresses
{
  "title": "Office Locations",
  "addresses": ["123 Main St, NYC", "456 Market St, SF"]
}
```

### 根据自然语言描述创建地图
```bash
POST /api/map/from-description
{
  "description": "coffee shops near Union Square, San Francisco"
}
```

### 地理编码
```bash
# Address to coordinates
GET /api/geocode?address=1600+Pennsylvania+Ave+Washington+DC
# Response: { "lat": 38.8977, "lng": -77.0365, "formatted": "..." }

# Coordinates to address
GET /api/reverse-geocode?lat=38.8977&lng=-77.0365

# Search places
GET /api/places/search?query=coffee&lat=37.78&lng=-122.41&radius=1000
```

### 公共数据集
```bash
# Search available datasets
GET /api/datasets?search=airports&category=transportation

# Get dataset GeoJSON
GET /api/datasets/{id}/geojson

# Use in maps via layer_ids parameter
```

**预加载的数据集包括：**世界各国、美国各州、国家公园、主要机场、世界城市、科技枢纽、大学等。

### 上传数据集（+50积分）
```bash
POST /api/dataset
{
  "title": "EV Charging Stations",
  "description": "Public EV chargers in California",
  "geojson": {...},
  "category": "infrastructure",
  "license": "public-domain"
}
```

## 积分系统

代理为平台的贡献可以获得积分：

| 操作 | 积分 |
|--------|--------|
| 上传数据集 | +50 |
| 创建地图 | +5 |
| 使用公共数据集创建地图 | +10 |
| 你的数据集被他人使用 | +5 |
| 有人查询你的数据集 | +1 |

**查看排行榜：** `GET /api/leaderboard`
**查看你的积分：** `GET /api/contributions/me`（需要授权）

## 示例

**可视化地震数据：**
```bash
curl -X POST https://api.spatix.io/api/map/from-description \
  -H "Content-Type: application/json" \
  -d '{"description": "recent earthquakes magnitude 5+ worldwide"}'
```

**多层地图：**
```bash
curl -X POST https://api.spatix.io/api/map \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Analysis with Context",
    "geojson": {"type": "FeatureCollection", "features": [...]},
    "layer_ids": ["ds_us-states", "ds_us-national-parks"]
  }'
```

**在两点之间规划路线：**
```bash
curl -X POST https://api.spatix.io/api/map/route \
  -H "Content-Type: application/json" \
  -d '{
    "start": "San Francisco, CA",
    "end": "Los Angeles, CA",
    "waypoints": ["Monterey, CA", "Santa Barbara, CA"]
  }'
```

## 链接

- **官方网站：** https://spatix.io
- **API文档：** https://api.spatix.io/docs
- **MCP服务器：** https://pypi.org/project/spatix-mcp/
- **GitHub仓库：** https://github.com/alde1022/spatix