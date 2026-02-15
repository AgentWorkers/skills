---
name: ohio-state-api
description: 从俄亥俄州立大学的内容API（content.osu.edu）中获取公共数据，这些数据涵盖了校园内的各项服务（包括公交、建筑、餐饮、活动、学术日历、图书馆、娱乐体育、停车、学生组织、体育赛事、食品车以及BuckID商户等信息）。当您需要俄亥俄州立大学的校园数据、希望构建与该校数据相关的功能，或者需要一种可重复使用的方式来获取/检查该校API返回的JSON数据时，都可以使用这些API。
compatibility: Requires outbound internet access to content.osu.edu. Optional: Node.js + npm for the bundled MCP server.
---

## 使用方法

### 选项 A：直接通过 HTTP 请求获取数据（最快）

使用内置的 `fetch` 助手工具从俄亥俄州立大学（OSU）的内容 API 中获取 JSON 数据。

- 通过完整 URL 获取数据：
  - `node ohio-state-api/scripts/osu-fetch.mjs https://content.osu.edu/v2/api/v1/dining/locations`
- 通过服务名称 + 路径获取数据：
  - `node ohio-state-api/scripts/osu-fetch.mjs --service dining --path /locations`

**注意**：`--path` 参数可以带或不带前导 `/`（两种方式均可使用）。

如果响应数据量较大，可以使用 `--extract <路径>` 参数（例如：`--extract data`）来仅获取部分数据。

### 选项 A2：使用 `curl`（无需 Node.js）

如果您只需要原始 JSON 数据，并且系统中已经安装了 `curl`，请参考 `ohio-state-api/references/OSU_API.md`：

- 通过完整 URL 获取数据：
  - `curl -sS -H 'accept: application/json' 'https://content.osu.edu/v2/api/v1/dining/locations'
- 带查询参数获取数据：
  - `curl -sS -H 'accept: application/json' 'https://content.osu.edu/v2/classes/search?q=cse&p=1'`

**可选**：将输出结果通过 `jq` 工具进行处理，以便于阅读：
  - `curl -sS -H 'accept: application/json' 'https://content.osu.edu/v2/api/v1/dining/locations' | jq .`

### 选项 B：使用 MCP 服务器（适用于兼容 MCP 协议的客户端）

该功能将原始的 MCP 服务器代码打包在 `ohio-state-api/mcp-server/` 目录下。

**构建步骤**：
- `cd ohio-state-api/mcp-server`  
- `npm install`  
- `npm run build`

配置您的 MCP 客户端后，执行以下命令：
- 命令：`node`  
- 参数：`["/ABSOLUTE/PATH/TO/ohio-state-api/mcp-server/build/index.js"]`

启动客户端后，可以使用以下工具：
- `get_bus_routes`、`get_bus_vehicles`  
- `get_buildings`、`search_buildings`、`get_building_details`  
- `get_dining_locations`、`get_dining_menu`  
- `get_campus_events`、`get_events_by_date_range`  
- `search_classes`  
- `get_parking_availability`

**详细信息请参阅**：`ohio-state-api/mcp-server/README.md` 以及 `ohio-state-api/mcp-server/src/` 目录下的工具说明。

## 获取 OSU 数据的推荐工作流程

1. 确定所需的数据服务（如餐饮、公交、建筑、活动等）。
2. 首先尝试使用列表或搜索接口获取数据，然后再通过具体 ID 进入详细信息接口。
3. 对于基于时间的数据，务必提供以下信息：
   - 查询的时间范围（具体日期/时间）  
   - 数据获取的时间戳。
4. 在将数据返回给用户时，尽量总结关键字段，并将原始 JSON 数据作为附件一并提供。

## 常用的基础 URL（公共接口）

这些 URL 被内置的 MCP 服务器使用，同时也可以与 `osu-fetch.mjs` 工具配合使用：

- 体育赛事：`https://content.osu.edu/v3/athletics`
- 公交信息：`https://content.osu.edu/v2/bus`
- 建筑信息：`https://content.osu.edu/v2/api`
- 日历信息：`https://content.osu.edu/v2/calender`
- 课程信息：`https://content.osu.edu/v2/classes`
- 餐饮信息：`https://content.osu.edu/v2/api/v1/dining`
- 通用目录：`https://content.osu.edu`
- 活动信息：`https://content.osu.edu/v2`
- 食品车信息：`https://content.osu.edu/v2/foodtruck`
- 图书馆信息：`https://content.osu.edu/v2/library`
- 商店信息：`https://content.osu.edu/v2/merchants`
- 停车信息：`https://content.osu.edu/v2/parking/garages`
- 休闲体育活动：`https://content.osu.edu/v3`
- 学生组织信息：`https://content.osu.edu/v2/student-org`

## 示例（可直接复制粘贴）

- 获取餐饮地点信息：
  - `curl -sS -H 'accept: application/json' 'https://content.osu.edu/v2/api/v1/dining/locations'
- 获取停车可用性信息：
  - `curl -sS -H 'accept: application/json' 'https://content.osu.edu/v2/parking/garages/availability'
- 使用 `jq` 在客户端过滤建筑信息：
  - `curl -sS -H 'accept: application/json' 'https://content.osu.edu/v2/api/buildings' | jq -r '.data.buildings[] | select((.name // \"\") | test(\"union\";\"i\")) | \"\\(.buildingNumber)\\t\\(.name)\"'`

## 额外参考资料

- API 参考文档：`ohio-state-api/references/OSU_API.md`