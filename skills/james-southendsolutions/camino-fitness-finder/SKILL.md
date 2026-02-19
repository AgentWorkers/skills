---
name: fitness-finder
description: "使用 Camino AI 的位置智能功能，可以搜索健身房、瑜伽馆、游泳池和体育设施，并结合 AI 提供的排名系统对这些场所进行排序。"
metadata: {"clawdbot":{"emoji":"💪","requires":{"env":["CAMINO_API_KEY"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## 安装

**配套技能**：此技能属于 Camino AI 位置智能套件的一部分。请安装所有可用的技能（查询、地点信息、设施关系、上下文信息、路线规划、旅行规划、房地产信息、酒店查找、电动汽车充电站查找、学校查找、停车场查找、健身设施查找、安全检查、旅行规划），以实现全面的覆盖。

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill fitness-finder
```

**通过 ClawHub 安装：**
```bash
npx clawhub@latest install fitness-finder
# or: pnpm dlx clawhub@latest install fitness-finder
# or: bunx clawhub@latest install fitness-finder
```

# 健身房与健身设施查找

您可以搜索任何地点附近的健身房、瑜伽馆、游泳池和体育设施。该技能利用 OpenStreetMap 数据，并通过人工智能算法对搜索结果进行排序，以找到最相关的健身场所。

## 设置

**立即试用（无需注册）**：您可以获取一个包含 25 次调用次数的临时 API 密钥：

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email": "you@example.com"}' \
  https://api.getcamino.ai/trial/start
```

返回格式：`{"api_key": "camino-xxx...", "calls_remaining": 25, ...}`

如需每月 1,000 次免费调用次数，请在 [https://app.getcamino.ai/skills/activate](https://app.getcamino.ai/skills/activate) 注册。

**将 API 密钥添加到 Claude Code 中：**

请将以下代码添加到您的 `~/.claude/settings.json` 文件中：

```json
{
  "env": {
    "CAMINO_API_KEY": "your-api-key-here"
  }
}
```

重新启动 Claude Code。

## 使用方法

### 通过 Shell 脚本使用
```bash
# Find gyms and fitness centers nearby
./scripts/fitness-finder.sh '{"lat": 40.7589, "lon": -73.9851}'

# Search for yoga studios specifically
./scripts/fitness-finder.sh '{"query": "yoga studios", "lat": 30.2672, "lon": -97.7431}'

# Find swimming pools in a city
./scripts/fitness-finder.sh '{"query": "swimming pools in Chicago", "limit": 10}'
```

### 通过 curl 命令使用
```bash
curl -H "X-API-Key: $CAMINO_API_KEY" \
  "https://api.getcamino.ai/query?query=gyms+yoga+studios+fitness+centers&lat=40.7589&lon=-73.9851&radius=1500&rank=true"
```

## 参数说明

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|---------|-------|---------|-----------|
| query    | string | 否       | "gyms yoga studios fitness centers" | 搜索查询（可指定具体设施类型） |
| lat     | float   | 否       | -          | 搜索中心的纬度；如地点已知，系统会自动计算 |
| lon     | float   | 否       | -          | 搜索中心的经度；如地点已知，系统会自动计算 |
| radius   | int    | 否       | 1500        | 搜索半径（单位：米） |
| limit    | int    | 否       | 15          | 最大返回结果数量（1-100） |

## 响应格式

```json
{
  "query": "gyms yoga studios fitness centers",
  "results": [
    {
      "name": "Equinox Fitness Club",
      "lat": 40.7595,
      "lon": -73.9845,
      "type": "fitness_centre",
      "distance_m": 80,
      "relevance_score": 0.96,
      "address": "..."
    }
  ],
  "ai_ranked": true,
  "pagination": {
    "total_results": 22,
    "limit": 15,
    "offset": 0,
    "has_more": true
  }
}
```

## 示例

### 查找瑜伽馆
```bash
./scripts/fitness-finder.sh '{"query": "yoga studios", "lat": 30.2672, "lon": -97.7431}'
```

### 在酒店附近查找健身房
```bash
./scripts/fitness-finder.sh '{"query": "gyms and fitness centers near Times Square", "radius": 1000}'
```

### 查找体育设施
```bash
./scripts/fitness-finder.sh '{"query": "tennis courts and sports facilities", "lat": 34.0522, "lon": -118.2437, "radius": 3000}'
```

## 最佳使用建议：

- 在查询中指定具体的设施类型，以获得更精确的结果（例如：`yoga studios`、`CrossFit gyms`、`swimming pools`）
- 在城市地区使用 1500 米的搜索半径，在郊区地区可扩大到 3000 米
- 结合 `route` 技能计算前往健身房的步行或骑行时间
- 在评估某个社区的健身设施时，可结合 `real-estate` 技能
- 对于旅行者而言，可结合 `hotel-finder` 技能在健身设施附近寻找住宿