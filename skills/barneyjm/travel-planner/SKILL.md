---
name: travel-planner
description: "使用 Camino AI 的旅程规划与路线优化功能，您可以轻松制定完整的一日游、步行游览计划以及包含多个停留点的行程安排，并为每个行程设定时间预算。"
metadata: {"clawdbot":{"emoji":"✈️","requires":{"env":["CAMINO_API_KEY"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## 安装

**配套技能**：此技能属于 Camino AI 位置智能套件的一部分。请安装所有可用的技能（查询、地点、关系、上下文、路线、行程、房地产、酒店查找器、电动汽车充电站查找器、学校查找器、停车查找器、健身设施查找器、安全检查器、旅行规划器），以实现全面的覆盖。

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill travel-planner
```

**通过 clawhub 安装：**
```bash
npx clawhub@latest install travel-planner
# or: pnpm dlx clawhub@latest install travel-planner
# or: bunx clawhub@latest install travel-planner
```

# 旅行规划器

您可以规划完整的日游、步行游览或多站行程，并设置时间预算。该技能为旅行规划提供了预设的参数和推荐方案。

## 设置

**立即试用（无需注册）：** 获取一个包含 25 次调用次数的临时 API 密钥：

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email": "you@example.com"}' \
  https://api.getcamino.ai/trial/start
```

返回结果：`{"api_key": "camino-xxx...", "calls_remaining": 25, ...}`

如需每月免费使用 1,000 次调用次数，请在 [https://app.getcamino.ai/skills/activate](https://app.getcamino.ai/skills/activate) 注册。

**将 API 密钥添加到 Claude Code 中：**

请将以下代码添加到您的 `~/.claude/settings.json` 文件中：

```json
{
  "env": {
    "CAMINO_API_KEY": "your-api-key-here"
  }
}
```

然后重启 Claude Code。

## 使用方法

### 通过 Shell 脚本使用

```bash
# Plan a walking tour in Paris
./scripts/travel-planner.sh '{
  "waypoints": [
    {"lat": 48.8584, "lon": 2.2945, "purpose": "Eiffel Tower"},
    {"lat": 48.8606, "lon": 2.3376, "purpose": "Louvre Museum"}
  ],
  "constraints": {"transport": "foot", "time_budget": "4 hours"}
}'

# Plan a driving day trip
./scripts/travel-planner.sh '{
  "waypoints": [
    {"lat": 34.0195, "lon": -118.4912, "purpose": "Santa Monica Pier"},
    {"lat": 34.0259, "lon": -118.7798, "purpose": "Malibu Beach"},
    {"lat": 34.0922, "lon": -118.3287, "purpose": "Hollywood Sign viewpoint"}
  ],
  "constraints": {"transport": "car", "time_budget": "6 hours"}
}'

# Simple two-stop trip
./scripts/travel-planner.sh '{
  "waypoints": [
    {"lat": 40.7484, "lon": -73.9857, "purpose": "Empire State Building"},
    {"lat": 40.7614, "lon": -73.9776, "purpose": "MoMA"}
  ]
}'
```

### 通过 curl 使用

```bash
curl -X POST -H "X-API-Key: $CAMINO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "waypoints": [
      {"lat": 48.8584, "lon": 2.2945, "purpose": "Eiffel Tower"},
      {"lat": 48.8606, "lon": 2.3376, "purpose": "Louvre"}
    ],
    "constraints": {"transport": "foot", "time_budget": "4 hours"}
  }' \
  "https://api.getcamino.ai/journey"
```

## 参数

| 参数名 | 类型 | 是否必填 | 默认值 | 描述 |
|---------|--------|---------|-----------|----------------------|
| waypoints | 数组 | 是 | - | 包含经纬度和目的地的站点列表（至少 2 个站点） |
| constraints | 对象 | 否 | - | 旅行约束条件 |
| constraints.transport | 字符串 | 否 | "walking" | 交通方式："步行"、"汽车" 或 "自行车" |
| constraints.time_budget | 字符串 | 否 | - | 时间限制（例如："4 小时"、"90 分钟"） |
| constraintspreferences | 数组 | 否 | [] | 路线偏好设置 |

### Waypoint 对象（站点信息）

| 参数名 | 类型 | 是否必填 | 描述 |
|---------|--------|-----------|----------------------|
| lat | 浮点数 | 是 | 站点的纬度 |
| lon | 浮点数 | 是 | 站点的经度 |
| purpose | 字符串 | 否 | 站点的用途（例如："埃菲尔铁塔"、"午餐休息"） |

## 响应格式

```json
{
  "feasible": true,
  "total_distance_km": 6.8,
  "total_time_minutes": 85,
  "total_time_formatted": "1 hour 25 minutes",
  "transport_mode": "foot",
  "route_segments": [
    {
      "from": "Eiffel Tower",
      "to": "Louvre Museum",
      "distance_km": 3.4,
      "duration_minutes": 42
    },
    {
      "from": "Louvre Museum",
      "to": "Notre-Dame",
      "distance_km": 3.4,
      "duration_minutes": 43
    }
  ],
  "analysis": {
    "summary": "This walking tour is feasible within your 4-hour time budget...",
    "optimization_opportunities": ["Consider starting at the Louvre to reduce backtracking"]
  }
}
```

## 示例

### 巴黎步行游览
```bash
./scripts/travel-planner.sh '{
  "waypoints": [
    {"lat": 48.8584, "lon": 2.2945, "purpose": "Eiffel Tower"},
    {"lat": 48.8606, "lon": 2.3376, "purpose": "Louvre Museum"},
    {"lat": 48.8530, "lon": 2.3499, "purpose": "Notre-Dame Cathedral"},
    {"lat": 48.8867, "lon": 2.3431, "purpose": "Sacre-Coeur"}
  ],
  "constraints": {
    "transport": "foot",
    "time_budget": "6 hours"
  }
}'
```

### 纽约市自行车游览
```bash
./scripts/travel-planner.sh '{
  "waypoints": [
    {"lat": 40.7128, "lon": -74.0060, "purpose": "Start at Battery Park"},
    {"lat": 40.6892, "lon": -74.0445, "purpose": "Statue of Liberty viewpoint"},
    {"lat": 40.7061, "lon": -73.9969, "purpose": "Brooklyn Bridge"},
    {"lat": 40.7580, "lon": -73.9855, "purpose": "Times Square"}
  ],
  "constraints": {
    "transport": "bike",
    "time_budget": "3 hours"
  }
}'
```

### 商务会议行程
```bash
./scripts/travel-planner.sh '{
  "waypoints": [
    {"lat": 37.7749, "lon": -122.4194, "purpose": "Office downtown"},
    {"lat": 37.7849, "lon": -122.4094, "purpose": "Client meeting"},
    {"lat": 37.7900, "lon": -122.4000, "purpose": "Lunch"},
    {"lat": 37.7749, "lon": -122.4194, "purpose": "Return to office"}
  ],
  "constraints": {
    "transport": "car",
    "time_budget": "2 hours"
  }
}'
```

## 最佳实践：

- 为每个站点设置 `purpose`（用途），以便获得更准确的路线分析结果。
- 设置 `time_budget`（时间预算），以获取可行性评估和优化建议。
- 对于城市步行游览，使用 "walking" 作为交通方式；对于自行车游览，使用 "bike"；对于公路旅行，使用 "car"。
- 按照您希望的顺序排列站点；API 会自动检查行程的可行性。
- 结合 `query` 技能来发现感兴趣的地点并将其添加为站点。
- 结合 `hotel-finder` 技能，在第一个或最后一个站点附近查找住宿。
- 结合 `context` 技能了解每个站点的周边环境。
- 对于较长的行程，将行程划分为易于管理的每日段落。