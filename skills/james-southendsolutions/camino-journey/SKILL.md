---
name: journey
description: "规划包含多个中途点的旅程时，需要考虑路线优化、可行性分析以及时间预算的限制。这种功能适用于需要规划包含多个停靠点的行程，或者检查某个行程是否可行的情况。"
metadata: {"clawdbot":{"emoji":"🗺️","requires":{"env":["CAMINO_API_KEY"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## 安装

**配套技能**：此技能属于 Camino AI 的位置智能套件。请安装所有可用的技能（查询、地点信息、关系分析、上下文信息、路线规划、旅程规划、房地产信息查询、酒店查找、电动汽车充电站查找、学校查找、停车场查找、健身设施查找、安全检查、旅行规划），以实现全面的旅行支持。

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill journey
```

**通过 ClawHub 安装：**
```bash
npx clawhub@latest install journey
# or: pnpm dlx clawhub@latest install journey
# or: bunx clawhub@latest install journey
```

# 旅程规划 - 多站点行程

支持多站点行程的规划，包括路线优化、可行性分析以及时间预算限制。

## 设置

**立即试用（无需注册）**：您可以获取一个包含 25 次调用次数的临时 API 密钥：

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email": "you@example.com"}' \
  https://api.getcamino.ai/trial/start
```

返回结果：`{"api_key": "camino-xxx...", "calls_remaining": 25, ...}`

如需每月享受 1,000 次免费调用次数，请在 [https://app.getcamino.ai/skills/activate](https://app.getcamino.ai/skills/activate) 注册。

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
# Plan a simple journey
./scripts/journey.sh '{
  "waypoints": [
    {"lat": 40.7128, "lon": -74.0060, "purpose": "Start at hotel"},
    {"lat": 40.7484, "lon": -73.9857, "purpose": "Visit Empire State Building"},
    {"lat": 40.7614, "lon": -73.9776, "purpose": "Lunch in Midtown"}
  ]
}'

# With transport mode and time budget
./scripts/journey.sh '{
  "waypoints": [
    {"lat": 40.7128, "lon": -74.0060, "purpose": "Start"},
    {"lat": 40.7484, "lon": -73.9857, "purpose": "Empire State"},
    {"lat": 40.7614, "lon": -73.9776, "purpose": "MoMA"}
  ],
  "constraints": {
    "transport": "foot",
    "time_budget": "3 hours"
  }
}'
```

### 通过 curl 命令使用

```bash
curl -X POST -H "X-API-Key: $CAMINO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "waypoints": [
      {"lat": 40.7128, "lon": -74.0060, "purpose": "Start"},
      {"lat": 40.7484, "lon": -73.9857, "purpose": "Empire State"}
    ],
    "constraints": {"transport": "foot"}
  }' \
  "https://api.getcamino.ai/journey"
```

## 参数说明

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|-------|------|----------|---------|-------------|
| waypoints | 数组 | 是 | - | 包含经纬度坐标及目的地的站点列表（至少 2 个站点） |
| constraints.transport | 字符串 | 否 | "walking" | 交通方式：步行、汽车或自行车 |
| constraints.time_budget | 字符串 | 否 | - | 时间限制（例如：“2 小时”、“90 分钟”） |
| constraintspreferences | 数组 | 否 | - | 路线偏好设置 |

### 站点对象

| 参数 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| lat | 浮点数 | 是 | 站点的纬度 |
| lon | 浮点数 | 是 | 站点的经度 |
| purpose | 字符串 | 否 | 访问该站点的目的 |

## 响应格式

```json
{
  "feasible": true,
  "total_distance_km": 4.2,
  "total_time_minutes": 52,
  "total_time_formatted": "52 minutes",
  "transport_mode": "foot",
  "route_segments": [
    {
      "from": "Start",
      "to": "Empire State",
      "distance_km": 4.2,
      "duration_minutes": 52
    }
  ],
  "analysis": {
    "summary": "This walking journey is feasible...",
    "optimization_opportunities": []
  }
}
```

## 示例

### 一日游行程规划
```bash
./scripts/journey.sh '{
  "waypoints": [
    {"lat": 48.8584, "lon": 2.2945, "purpose": "Eiffel Tower"},
    {"lat": 48.8606, "lon": 2.3376, "purpose": "Louvre Museum"},
    {"lat": 48.8530, "lon": 2.3499, "purpose": "Notre-Dame"},
    {"lat": 48.8867, "lon": 2.3431, "purpose": "Sacré-Cœur"}
  ],
  "constraints": {
    "transport": "foot",
    "time_budget": "6 hours"
  }
}'
```

### 商务会议路线规划
```bash
./scripts/journey.sh '{
  "waypoints": [
    {"lat": 40.7128, "lon": -74.0060, "purpose": "Office"},
    {"lat": 40.7580, "lon": -73.9855, "purpose": "Client meeting"},
    {"lat": 40.7614, "lon": -73.9776, "purpose": "Lunch"},
    {"lat": 40.7128, "lon": -74.0060, "purpose": "Return to office"}
  ],
  "constraints": {
    "transport": "car",
    "time_budget": "2 hours"
  }
}'
```

### 骑行路线规划
```bash
./scripts/journey.sh '{
  "waypoints": [
    {"lat": 37.7749, "lon": -122.4194, "purpose": "Start downtown SF"},
    {"lat": 37.8199, "lon": -122.4783, "purpose": "Golden Gate Bridge"},
    {"lat": 37.8270, "lon": -122.4230, "purpose": "Sausalito"}
  ],
  "constraints": {
    "transport": "bike"
  }
}'
```

## 使用场景

- **行程可行性验证**：检查计划中的行程是否在时间范围内可行 |
- **路线优化**：获取多站点行程的优化建议 |
- **旅行时间估算**：计算前往多个目的地的总旅行时间 |
- **旅游路线规划**：规划步行游览路线、骑行路线或驾车路线