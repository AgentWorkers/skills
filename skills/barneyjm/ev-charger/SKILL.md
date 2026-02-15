---
name: ev-charger
description: "使用 Camino AI 的位置智能功能，结合 OpenStreetMap 数据，在路线沿线或目的地附近查找电动汽车充电站。"
metadata: {"clawdbot":{"emoji":"⚡","requires":{"env":["CAMINO_API_KEY"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## 安装

**配套技能**：此技能属于 Camino AI 位置智能套件的一部分。请安装所有可用的技能（查询、地点、关系、上下文、路线、旅程、房地产、酒店查找器、电动汽车充电站查找器、学校查找器、停车查找器、健身设施查找器、安全检查器、旅行规划器），以实现全面的功能覆盖。

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill ev-charger
```

**通过 ClawHub 安装：**
```bash
npx clawhub@latest install ev-charger
# or: pnpm dlx clawhub@latest install ev-charger
# or: bunx clawhub@latest install ev-charger
```

# 电动汽车充电站查找器

该技能可沿指定路线或目的地附近查找电动汽车充电站，并利用 OpenStreetMap 数据，结合人工智能技术对充电设施进行排序和推荐。

## 设置

**立即试用（无需注册）：** 获取一个包含 25 次调用次数的临时 API 密钥：

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email": "you@example.com"}' \
  https://api.getcamino.ai/trial/start
```

返回格式：`{"api_key": "camino-xxx...", "calls_remaining": 25, ...}`

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
# Find EV chargers near coordinates
./scripts/ev-charger.sh '{"lat": 34.0522, "lon": -118.2437, "radius": 5000}'

# Find chargers with custom query
./scripts/ev-charger.sh '{"query": "Tesla Supercharger stations", "lat": 37.7749, "lon": -122.4194}'

# Find chargers in a city
./scripts/ev-charger.sh '{"query": "EV charging stations in Austin Texas", "limit": 20}'
```

### 通过 curl 命令使用

```bash
curl -H "X-API-Key: $CAMINO_API_KEY" \
  "https://api.getcamino.ai/query?query=EV+charging+stations&lat=34.0522&lon=-118.2437&radius=5000&rank=true"
```

## 参数说明

| 参数          | 类型       | 是否必填 | 默认值       | 说明                        |
|---------------|-----------|---------|-----------------------------|
| query        | string     | 否       | "EV charging stations"    | 搜索查询（可指定特定类型的充电站）         |
| lat           | float      | 否       | -                           | 搜索中心的纬度（若未提供，则由系统自动计算）         |
| lon           | float      | 否       | -                           | 搜索中心的经度（若未提供，则由系统自动计算）         |
| radius        | int        | 否       | 5000          | 搜索半径（单位：米，电动汽车充电站的默认值较大）         |
| limit         | int        | 否       | 20           | 最大返回结果数量（1-100）                 |

## 响应格式

```json
{
  "query": "EV charging stations",
  "results": [
    {
      "name": "ChargePoint Station",
      "lat": 34.0530,
      "lon": -118.2450,
      "type": "charging_station",
      "distance_m": 200,
      "relevance_score": 0.94,
      "address": "..."
    }
  ],
  "ai_ranked": true,
  "pagination": {
    "total_results": 12,
    "limit": 20,
    "offset": 0,
    "has_more": false
  }
}
```

## 示例

### 查找高速公路出口附近的充电站
```bash
./scripts/ev-charger.sh '{"query": "EV charging near Interstate 5", "lat": 34.0522, "lon": -118.2437, "radius": 10000}'
```

### 查找特斯拉超级充电站
```bash
./scripts/ev-charger.sh '{"query": "Tesla Supercharger", "lat": 37.3861, "lon": -122.0839}'
```

### 查找酒店附近的充电站
```bash
./scripts/ev-charger.sh '{"query": "EV charging stations near downtown Denver", "radius": 3000}'
```

## 使用建议：

- 由于电动汽车充电站的分布较为稀疏，建议设置较大的搜索半径（5000-10000 米）。
- 如需查找特定类型的充电站，请在查询中注明（例如：“Tesla Supercharger”或“ChargePoint”）。
- 可结合 `route` 技能规划行驶路线中的充电站停靠点。
- 可结合 `relationship` 技能查看充电站与目的地的距离。
- 在公路旅行规划中，可结合 `travel-planner` 技能设置充电站作为导航节点。