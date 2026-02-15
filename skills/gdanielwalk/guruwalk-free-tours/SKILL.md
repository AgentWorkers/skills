---
name: guruwalk-free-tours
description: >
  Search GuruWalk free tours through the GuruWalk MCP server and return bookable options
  by city, dates, and language. Use this skill when the user asks for free tours, walking
  tours, guided city tours, plans in a city, or availability of tours on specific dates.
---

# GuruWalk 免费旅游服务

您可以使用 GuruWalk MCP 服务器来搜索免费旅游活动：

`https://guruwalk-api-44909317956.europe-southwest1.run.app/mcp`

该服务器目前提供一个工具：`search`。

## 工具接口规范

**`search` 接口参数：**
- `city`（字符串）：英文形式的城市名称，其中的空格需替换为 `-`。
- `start_date`（字符串）：日期格式为 `yyyy-mm-dd`。
- `end_date`（字符串）：日期格式为 `yyyy-mm-dd`。
- `language`（字符串）：两位字母的语言代码（例如 `es`、`en`、`de`、`it`）。

**`search` 接口返回值：**
- 该工具返回 `content[0].text`，其中包含一个 JSON 字符串。
- 解析该 JSON 字符串可获取旅游活动的列表。
- 每个旅游活动包含以下信息：
  - `title`（旅游活动名称）
  - `url`（预订链接）
  `meetpoint_address`（集合地点地址）
  `average_rating`（平均评分）
  `duration`（活动时长）
  `guru.name`（导游姓名）
  `image_url`（活动图片链接）
  `events`（活动详情数组，包含以下字段）：
    - `start_time`（活动开始时间，UTC 格式）
    `available_spots`（可用名额）
    `language`（活动语言）

## 执行流程：**
1. 从用户请求中获取城市名称、日期范围和偏好语言。
2. 将城市名称转换为标准的 Slug 格式（例如：`new york` → `new-york`）。
3. 确保日期格式符合 ISO 标准（`yyyy-mm-dd`）。
4. 调用 `search` 接口。
5. 解析 `content[0].text` 中的 JSON 数据。
6. 对搜索结果进行筛选和排序，以便用户查看：
  - 仅保留 `available_spots` 大于 0 的活动。
  - 尽量优先显示用户所需语言的活动。
  - 按评分从高到低排序，同时考虑活动开始时间。
7. 返回包含预订链接和下一个可用时间的旅游活动信息。

## 默认设置：**
- 如果用户未指定语言，系统将使用 `es`（西班牙语）。
- 如果用户未指定日期，系统会在调用接口前提示用户输入日期。
- 如果用户提供的日期格式不正确，系统会自动将其转换为 ISO 标准格式。

## 向用户展示的结果格式：**
- 每个推荐的旅游活动应包含以下信息：
  - 活动名称
  - 评分
  - 活动时长
  - 导游姓名
  - 集合地点
  - 下一个可用的活动时间（包含时区信息）
  - 预订链接

**如果未找到旅游活动：**
- 向用户说明在指定城市/日期范围内未找到符合条件的旅游活动。
- 建议用户调整以下参数之一：城市名称、日期或语言。

## 注意事项（基于实际使用情况）：
- `search` 是唯一的可用工具；MCP 服务器不提供其他资源、提示或模板。
- 包含空格的城市名称（如 `New York`）可能导致搜索结果为空。
- 如果 `start_date` 大于 `end_date`，系统可能返回空结果，但不会显示错误提示。
- 虽然非 ISO 格式的日期也能被后端接受，但建议始终使用 `yyyy-mm-dd` 格式。
- 某些语言组合可能导致某些旅游活动的 `title` 为空，系统应能优雅地处理这种情况。

## 验证说明：**
- 验证相关功能的正确性可以通过以下方式完成：
  - 确认 MCP 服务器确实提供了 `search` 接口。
  - 检查搜索结果是否以 JSON 字符串的形式存储在 `content[0].text` 中。