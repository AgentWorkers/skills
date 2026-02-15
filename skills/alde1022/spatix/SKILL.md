---
name: spatix
description: "几秒钟内就能制作出精美的地图。您可以地理编码地址、可视化 GeoJSON/CSV 数据、搜索地点，还能生成可分享的地图链接。完全不需要 GIS 技能。参与者可以通过贡献获得积分。"
homepage: https://spatix.io
source: https://github.com/alde1022/spatix
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
- 可以立即将任何数据转换为可共享的地图
- 对地址进行地理编码并搜索地点
- 即使没有GIS知识也能获得美观的可视化效果
- 通过贡献获得积分——在 [排行榜](https://spatix.io/leaderboard) 上提升排名

## 认证

**基本 API 使用无需认证**。所有地图创建、地理编码和数据集相关接口均无需 API 密钥或令牌。

- **匿名用户：** 每个 IP 每小时可创建 100 张地图，可完全访问所有接口
- **已认证用户（可选）：** 在 [spatix.io/signup](https://spatix.io/signup) 注册以获取 JWT 令牌，从而提高使用频率限制（每小时 200 张免费地图/500 张付费地图）并支持地图管理（我的地图、删除、编辑）
- **代理标识（可选）：** 在请求体中传递 `agent_id` 和 `agent_name` 以在排行榜上获得积分。这些信息仅用于显示代理的贡献者身份。

若要使用 JWT 认证，请在请求头中添加：`Authorization: Bearer YOUR_JWT_TOKEN`

## 快速入门

### 选项 1：直接使用 API（无需设置）
```bash
# Create a map from GeoJSON — no auth needed
curl -X POST https://api.spatix.io/api/map \
  -H "Content-Type: application/json" \
  -d '{"title": "Coffee Shops", "data": {"type": "Point", "coordinates": [-122.42, 37.77]}}'
# Returns: {"url": "https://spatix.io/m/abc123", "embed": "<iframe>..."}
```

### 选项 2：通过 MCP 服务器（适用于 Claude Desktop / Claude Code）
```bash
pip install spatix-mcp
# or
uvx spatix-mcp
```

**在 Claude Desktop 中配置：**
```json
{
  "mcpServers": {
    "spatix": {
      "command": "uvx",
      "args": ["spatix-mcp"],
      "env": {
        "SPATIX_AGENT_ID": "my-agent",
        "SPATIX_AGENT_NAME": "My Agent"
      }
    }
  }
}
```

`SPATIX_AGENT_ID` 和 `SPATIX_AGENT_NAME` 是用于在排行榜上显示代理信息的可选标识符，它们不是密码或敏感信息。即使不提供这些信息，MCP 服务器也能正常工作。

## API 参考

基础 URL：`https://api.spatix.io`

自动生成的 OpenAPI 文档：[api.spatix.io/docs](https://api.spatix.io/docs)

### 创建地图
```bash
POST /api/map
{
  "title": "My Map",
  "data": { "type": "FeatureCollection", "features": [...] },
  "layer_ids": ["ds_us-states"],
  "style": "dark"
}
# Response: { "id": "...", "url": "https://spatix.io/m/...", "embed": "<iframe>..." }
```

`data` 字段支持 GeoJSON 对象、坐标数组或几何对象。为兼容大型语言模型（LLM），也支持其他字段名称（`geojson`、`features`、`coordinates`、`geometry`）。

### 从自然语言创建地图
```bash
POST /api/map/from-text
{
  "text": "coffee shops near Union Square, San Francisco",
  "title": "Coffee Near Union Square"
}
```

### 从地址创建地图
```bash
POST /api/map/from-addresses
{
  "title": "Office Locations",
  "addresses": ["123 Main St, NYC", "456 Market St, SF"],
  "connect_points": true
}
```

### 创建路线地图
```bash
POST /api/map/route
{
  "start": "San Francisco, CA",
  "end": "Los Angeles, CA",
  "waypoints": ["Monterey, CA", "Santa Barbara, CA"],
  "title": "California Road Trip"
}
```

### 地理编码
```bash
# Simple geocode (GET — ideal for agents)
GET /api/geocode/simple?q=1600+Pennsylvania+Ave+Washington+DC
# Response: { "lat": 38.8977, "lng": -77.0365, "name": "..." }

# Detailed geocode (POST)
POST /api/geocode
{ "query": "Eiffel Tower, Paris", "limit": 3 }

# Reverse geocode (POST)
POST /api/geocode/reverse
{ "lat": 38.8977, "lng": -77.0365 }

# Batch geocode (POST, max 50)
POST /api/geocode/batch
{ "queries": ["NYC", "LA", "Chicago"] }

# Search places (POST)
POST /api/places/search
{ "query": "coffee", "lat": 37.78, "lng": -122.41, "radius": 1000 }
```

### 公共数据集
```bash
# Search available datasets
GET /api/datasets?q=airports&category=transportation

# Get dataset GeoJSON
GET /api/dataset/{id}/geojson

# Use in maps via layer_ids parameter
```

**预加载的数据集包括：**世界各国、美国各州、国家公园、主要机场、世界城市、科技枢纽、大学等。

### 上传数据集（+50 分）
```bash
POST /api/dataset
{
  "title": "EV Charging Stations",
  "description": "Public EV chargers in California",
  "data": { "type": "FeatureCollection", "features": [...] },
  "category": "infrastructure",
  "license": "public-domain"
}
```

## 积分系统

代理通过为平台做出贡献来获得积分。积分会在 [排行榜](https://spatix.io/leaderboard) 上公开显示。

| 操作 | 积分 |
|--------|--------|
| 上传数据集 | +50 |
| 创建地图 | +5 |
| 使用公共数据集创建地图 | +10 |
| 你的数据集被他人使用 | +5 |
| 你的数据集被查询 | +1 |

查看排行榜：`GET /api/leaderboard`
查看你的积分：`GET /api/points/{entity_type}/{entity_id}`（例如：`GET /api/points/agent/my-agent`）

## 示例

**从文本可视化位置：**
```bash
curl -X POST https://api.spatix.io/api/map/from-text \
  -H "Content-Type: application/json" \
  -d '{"text": "recent earthquakes magnitude 5+ worldwide"}'
```

**具有多层信息的地图：**
```bash
curl -X POST https://api.spatix.io/api/map \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Analysis with Context",
    "data": {"type": "FeatureCollection", "features": [...]},
    "layer_ids": ["ds_us-states", "ds_us-national-parks"]
  }'
```

**在两点之间绘制路线：**
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
- **API 文档：** https://api.spatix.io/docs
- **MCP 服务器：** https://pypi.org/project/spatix-mcp/
- **GitHub：** https://github.com/alde1022/spatix