---
name: context
description: "获取关于某个地点的全面信息，包括附近的场所、区域描述以及可选的天气情况。当您需要了解某个地点周围的设施或提供与地点相关的建议时，可以使用此功能。"
metadata: {"clawdbot":{"emoji":"📍","requires":{"env":["CAMINO_API_KEY"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## 安装

**配套技能**：该技能属于 Camino AI 位置智能套件的一部分。请安装所有可用的技能（查询、地点、关系、上下文、路线、旅程、房地产、酒店查找、电动汽车充电站查找、学校查找、停车场查找、健身设施查找、安全检查、旅行规划），以实现全面的覆盖。

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill context
```

**通过 ClawHub 安装：**
```bash
npx clawhub@latest install context
# or: pnpm dlx clawhub@latest install context
# or: bunx clawhub@latest install context
```

# 上下文 - 位置分析

获取关于某个位置的详细上下文信息，包括附近的地点、区域描述以及可选的天气信息。

## 设置

**立即试用（无需注册）**：您可以获取一个包含 25 次调用次数的临时 API 密钥：

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email": "you@example.com"}' \
  https://api.getcamino.ai/trial/start
```

返回格式：`{"api_key": "camino-xxx...", "calls_remaining": 25, ...}`

如需每月获得 1,000 次免费调用次数，请在 [https://app.getcamino.ai/skills/activate](https://app.getcamino.ai/skills/activate) 注册。

**将 API 密钥添加到 Claude Code 中：**

请将以下代码添加到您的 `~/.claude/settings.json` 文件中：

```json
{
  "env": {
    "CAMINO_API_KEY": "your-api-key-here"
  }
}
```

重启 Claude Code 后即可使用该技能。

## 使用方法

### 通过 Shell 脚本使用

```bash
# Get context about a location
./scripts/context.sh '{
  "location": {"lat": 40.7589, "lon": -73.9851},
  "radius": 500
}'

# With specific context for tailored insights
./scripts/context.sh '{
  "location": {"lat": 40.7589, "lon": -73.9851},
  "radius": 500,
  "context": "lunch options"
}'

# Include weather data
./scripts/context.sh '{
  "location": {"lat": 40.7589, "lon": -73.9851},
  "include_weather": true,
  "weather_forecast": "hourly"
}'
```

### 通过 curl 命令使用

```bash
curl -X POST -H "X-API-Key: $CAMINO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location": {"lat": 40.7589, "lon": -73.9851}, "radius": 500, "context": "lunch options"}' \
  "https://api.getcamino.ai/context"
```

## 参数

| 参数名 | 参数类型 | 是否必填 | 默认值 | 描述 |
|---------|-----------|---------|-------------|
| location | object | 是 | - | 包含经纬度的坐标 |
| radius | int | 否 | 500 | 搜索半径（单位：米） |
| context | string | 否 | - | 用于定制化查询的上下文信息（例如：“户外用餐”） |
| time | string | 否 | - | 时间查询格式 |
| include_weather | bool | 否 | false | 是否包含天气数据 |
| weather_forecast | string | 否 | "daily" | 可选值："daily" 或 "hourly"（表示天气预报的频率） |

## 响应格式

```json
{
  "area_description": "Busy commercial district in Midtown Manhattan...",
  "relevant_places": {
    "restaurants": [...],
    "cafes": [...],
    "transit": [...]
  },
  "location": {"lat": 40.7589, "lon": -73.9851},
  "search_radius": 500,
  "total_places_found": 47,
  "context_insights": "For lunch, you have many options including..."
}
```

## 示例

### 旅游场景
```bash
./scripts/context.sh '{
  "location": {"lat": 48.8584, "lon": 2.2945},
  "radius": 1000,
  "context": "tourist visiting Paris"
}'
```

### 商务会议地点查询
```bash
./scripts/context.sh '{
  "location": {"lat": 40.7589, "lon": -73.9851},
  "radius": 500,
  "context": "business meeting",
  "include_weather": true
}'
```

### 户外活动规划
```bash
./scripts/context.sh '{
  "location": {"lat": 37.7749, "lon": -122.4194},
  "context": "outdoor activities",
  "include_weather": true,
  "weather_forecast": "hourly"
}'
```

## 使用场景

- **行程规划**：在前往目的地之前了解周边环境。
- **会议场地选择**：为不同类型的会议寻找合适的场所。
- **本地推荐**：根据用户需求提供基于上下文的建议。
- **考虑天气的规划**：在规划户外活动时包含天气数据。