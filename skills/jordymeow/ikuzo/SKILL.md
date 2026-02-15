---
name: ikuzo
description: 在 Ikuzo (ikuzo.app) 这款基于位置的探索应用中，您可以管理地图、地点以及旅行计划。该应用适用于创建/编辑地图、添加/搜索地点、制定每日行程的旅行计划、查找附近的场所，以及管理旅行相关的事务。相关功能包括地图管理、地点追踪、旅行规划、地点发现，以及解决“我该去哪里”这类问题。
---

# Ikuzo

Ikuzo 是一款地图与旅行规划应用程序，可通过 MCP（基于 HTTP POST 的 JSON-RPC 2.0 协议）进行访问。

## 连接

```
Endpoint: https://ikuzo.app/api/mcp
Auth: Bearer token (from TOOLS.md or user config)
Protocol: JSON-RPC 2.0 — POST with {"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"<tool>","arguments":{...}}}
```

## 工具

### 地图
- `maps_list` — 列出所有地图（用户拥有的地图和共享的地图）
- `maps_get(mapId)` — 获取地图详情
- `maps_create(title)` — 创建新的空白地图，并返回地图的 ID

### 地点（Spots）
- `spots_list(mapId, ...)` — 列出或过滤地图中的地点。过滤条件包括：`status[]`, `type[]`, `period[]`, `momentFrom/To`, `text`, `limit`, `offset`, `fields[]`
- `spots_get(spotId)` — 获取地点详情
- `spots_create(mapId, title, gps{lat, lng}, ...)` — 创建新的地点。可选参数：`description`, `type`, `status`, `period[]`, `moment{date, repeat, reminder[]}`
- `spots_update(spotId, ...)` — 更新地点的任何字段（包括 `moment` 和 `rating`）
- `spots_delete(spotId)` — 软删除地点（可恢复）
- **`spots_nearby(lat, lng, ...)`** — 在所有可访问的地图中查找指定位置附近的地点。可选参数：`radius`（千米，默认值 10，最大值 500），`mapIds[]`；返回结果按距离排序。
- `spots_box(north, south, east, west, ...)` — 在指定边界框内查找地点。过滤条件与 `spots_nearby` 相同。

### 旅行计划（Travel Plans）
- `travels_list` — 列出所有旅行计划
- `travels_get(travelId)` — 获取旅行计划的详细信息
- `travels_create(title)` — 创建新的旅行计划
- `travels_update(travelId, title)` — 重命名旅行计划
- `travels_delete(travelId)` — 删除旅行计划

### 旅行计划中的步骤（Steps within a Travel Plan）
- `steps_add(travelId, type, ...)` — 添加步骤。`type="spot"` 需要提供 `spotId`；`type="day"` 需要提供 `title`。可选参数：`orderKey`
- `steps_update(stepId, ...)` — 更新步骤的位置或标题
- `steps_delete(stepId)` — 删除步骤

### 其他工具
- `ping` — 测试连接是否正常
- `schema` — 查询 `type`, `status`, `period` 的有效取值
- `quota` — 检查 API 使用情况（此操作不会消耗配额）

## 架构参考（Schema Reference）

有关有效的地点类型、状态和时间段，请参阅 `references/schema.md`。如果不确定，请在运行时使用 `schema` 工具进行查询。

## 关键模式（Key Patterns）

### 查找附近的地点
```
spots_nearby(lat, lng, radius=20, status=["a","b"])
```
- 状态 `a` 表示“推荐访问”（优先级较高）；`b` 表示“待访问”

### 具有即将发生的活动的季节性地点
```
spots_list(mapId, momentFrom="2026-03-01", momentTo="2026-04-30")
```

### 创建旅行行程
1. `travels_create(title)` — 创建旅行计划并获取其 ID
2. `steps_add(travelId, type="day", title="Day 1 - 到达")` — 添加到达当天的步骤
3. 为每一天重复上述步骤，为每个地点添加相应的步骤

### 高效的数据请求（减少请求次数）
使用 `fields` 参数仅请求所需的信息：
```
spots_list(mapId, fields=["_id","title","gps","status","type"])
```

### 图片 URL
地点的图片通过 Ikuzo 的 CDN 提供：
```
https://ik.offbeatjapan.org/ikuzo/{imageId}.{ext}?tr=h-{height},w-{width}
```
其中 `imageId` 和 `ext` 来自地点的 `image[]` 数组。