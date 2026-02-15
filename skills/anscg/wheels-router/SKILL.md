---
name: wheels-router
description: 使用 Wheels Router（香港）和 Transitous（全球）在全球范围内规划公共交通行程。
license: MIT
compatibility: opencode
metadata:
  transport: mcp
  coverage: global
  specialty: hong-kong
---

## 我的功能

我通过连接到 Wheels Router MCP 服务器来帮助您规划全球任何地方的公共交通行程。

**对于香港的行程**，我使用 Wheels Router API，该 API 提供以下服务：
- 详细的交通路线信息（包括地铁、公交车、电车、渡轮和步行路线）
- 实时时刻表和准确的票价
- 车站信息和出口详情
- 可用的换乘优惠（轉乘優惠）

**对于全球的行程**，我使用 Transitous API，该 API 涵盖以下内容：
- 全球主要城市的公共交通数据
- 基本的公共交通路线规划
- 步行路线和换乘建议

## 何时使用我

在以下情况下可以使用我的功能：
- 需要使用公共交通规划行程
- 查找两个地点之间的最佳路线
- 查看公共交通时刻表和换乘信息
- 获取香港交通的票价估算
- 在规划路线前搜索地点

**示例**：
- “我该如何从油塘地铁站前往香港机场？”
- “现在从铜锣湾去中环的最佳方式是什么？”
- “规划从东京站到涩谷的行程”
- “搜索维多利亚公园附近的地点”

## 如何使用我

### 如果您使用的是 mcporter（如 clawdbot 等）

请按照您的 mcporter 技能进行操作；如果没有，请按照以下步骤操作：
1. 在 `config/mcporter.json` 文件中添加相应的配置：
   ```json
{
  "mcpServers": {
    "wheels-router": {
      "description": "Plan public transit trips globally",
      "baseUrl": "https://mcp.justusewheels.com/mcp"
    }
  }
}
```

2. 然后直接调用相关工具：
   ```bash
npx mcporter call wheels-router.search_location query="Hong Kong Airport"
npx mcporter call wheels-router.plan_trip origin="22.28,114.24" destination="22.31,113.92"
```

### 对于其他 MCP 客户端

**Claude Desktop**（`~/Library/Application Support/Claude/claude_desktop_config.json`）：
   ```json
{
  "mcpServers": {
    "wheels-router": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.justusewheels.com/mcp"]
    }
  }
}
```

**Cursor/Windsurf/VS Code**（`.cursor/mcp.json` 或类似配置文件）：
   ```json
{
  "mcpServers": {
    "wheels-router": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.justusewheels.com/mcp"]
    }
  }
}
```

## 可用的工具

### `search_location`

在规划行程前先搜索地点。如果没有确切的坐标，请务必先使用此工具。

**参数**：
- `query`（必填）：地点名称或地址（例如：“香港机场”、“油塘地铁站 A2 出口”）
- `limit`（可选）：结果数量（1-10，默认为 5）

**示例**：
```javascript
search_location({
  query: "Hong Kong International Airport",
  limit: 3
})
```

**返回内容**：
- `display_name`：完整地址
- `lat`, `lon`：用于 `plan_trip` 的坐标
- `type`, `class`：地点类别

### `plan_trip`

规划两个地点之间的公共交通路线。

**参数**：
- `origin`（必填）：起点，格式为 `"lat,lon"` 或 `"stop:ID"`
- `destination`（必填）：终点，格式为 `"lat,lon"` 或 `"stop:ID"`
- `depart_at`（可选）：ISO 8601 格式的出发时间（例如：“2026-01-26T10:00:00+08:00”）
- `arrive_by`（可选）：ISO 8601 格式的到达截止时间
- `modes`（可选）：用逗号分隔的交通方式（例如：“mtr,bus,ferry”）
- `max_results`（可选）：返回的路线选项数量（1-5）

**示例**：
```javascript
plan_trip({
  origin: "22.2836,114.2358",
  destination: "22.3080,113.9185",
  depart_at: "2026-01-26T14:30:00+08:00",
  max_results: 3
})
```

**返回内容**：
- `plans`：路线选项数组
  - `duration_seconds`：总行程时间
  - `fares_min`, `fares_max`：票价范围（仅适用于香港）
  - `legs`：详细的步行或公共交通路线信息，包括：
    - `type`：步行、公共交通、等待、车站换乘
    - 公共交通路线包括：路线名称、方向指示、站点信息
    - 步行路线包括：距离和步行时间

## 最佳实践

1. **始终先搜索**：在使用 `plan_trip` 之前，先用 `search_location` 查找坐标。
2. **使用坐标**：使用 `lat,lon` 格式进行路线规划以获得最佳结果。
3. **指定时间**：提供 `depart_at` 或 `arrive_by` 以确保时刻表的准确性。
4. **查看多个选项**：请求 2-3 个路线选项。
5. **了解票价**：`fares_min` 和 `fares_max` 显示票价范围；换乘优惠会在适用时单独显示。

## 重要说明

- **换乘优惠**：仅在香港的路线中显示，并非所有路线都提供换乘优惠。
- **实时数据**：香港的路线使用实时时刻表；全球范围内的数据覆盖情况可能有所不同。
- **时区**：使用 UTC 或当地时区偏移量（香港时间为 UTC+8）。
- **覆盖范围**：香港的覆盖范围最全面；全球其他城市的覆盖情况因城市而异。

## 示例工作流程

```javascript
// 1. Search for locations
const origins = await search_location({ 
  query: "Yau Tong MTR Station", 
  limit: 1 
});

const destinations = await search_location({ 
  query: "Hong Kong Airport", 
  limit: 1 
});

// 2. Plan the trip
const routes = await plan_trip({
  origin: `${origins[0].lat},${origins[0].lon}`,
  destination: `${destinations[0].lat},${destinations[0].lon}`,
  depart_at: "2026-01-26T15:00:00+08:00",
  max_results: 2
});

// 3. Present the best options to the user or present specific results but only if user asked specifically. By default just give them something like "[walk] > [3D] > [walk] > [Kwun Tong Line] > [walk]"- unless they ask for specifics.
```

## 错误处理

- **“无法找到地点”**：尝试使用更具体的搜索查询。
- **“未找到路线”**：检查坐标是否有效以及是否在服务覆盖范围内。
- **“时间格式无效”**：确保时间格式符合 ISO 8601 标准，并包含时区信息。
- **使用限制**：注意 API 的使用频率，适当缓存结果。

## 覆盖范围

- ✅ **全面覆盖**：香港（地铁、公交车、电车、渡轮，提供详细票价）
- ✅ **良好覆盖**：全球主要城市（通过 Transitous API 提供公共交通数据）
- ⚠️ **覆盖范围有限**：较小城市的公共交通数据可能不完整