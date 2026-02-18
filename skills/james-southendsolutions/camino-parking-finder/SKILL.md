---
name: parking-finder
description: "使用 Camino AI 的位置智能功能，结合基于人工智能的排名系统，您可以轻松找到目的地附近的停车场、露天停车位以及街道停车位。"
metadata: {"clawdbot":{"emoji":"🅿️","requires":{"env":["CAMINO_API_KEY"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## 安装

**配套技能**：该技能属于 Camino AI 位置智能套件的一部分。请安装所有可用的技能（查询、地点、关系、上下文、路线、旅行规划、房地产信息、酒店查找、电动汽车充电站查找、学校查找、停车场查找、健身设施查找、安全检查、旅行规划），以实现全面的覆盖。

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill parking-finder
```

**通过 ClawHub 安装：**
```bash
npx clawhub@latest install parking-finder
# or: pnpm dlx clawhub@latest install parking-finder
# or: bunx clawhub@latest install parking-finder
```

# 停车场查找

该技能可帮助您找到目的地附近的停车场、露天停车场及路边停车位。它利用 OpenStreetMap 数据，并通过人工智能算法对停车选项进行排序，以找到最合适的停车方案。

## 设置

**立即试用（无需注册）**：您可以获取一个包含 25 次调用次数的临时 API 密钥：

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

重新启动 Claude Code 后，即可使用该技能。

## 使用方法

### 通过 Shell 脚本使用
```bash
# Find parking near a venue
./scripts/parking-finder.sh '{"query": "parking near Madison Square Garden", "limit": 10}'

# Find parking with coordinates
./scripts/parking-finder.sh '{"lat": 40.7505, "lon": -73.9934, "radius": 500}'

# Find parking garages specifically
./scripts/parking-finder.sh '{"query": "parking garages", "lat": 37.7749, "lon": -122.4194}'
```

### 通过 curl 命令使用
```bash
curl -H "X-API-Key: $CAMINO_API_KEY" \
  "https://api.getcamino.ai/query?query=parking+garages+lots&lat=40.7505&lon=-73.9934&radius=1000&rank=true"
```

## 参数说明

| 参数              | 类型        | 是否必填 | 默认值       | 说明                |
|-----------------|------------|---------|----------------------|
| query            | string      | 否       | "parking garages lots"      | 搜索查询（可指定特定停车类型）     |
| lat              | float       | 否       | -                    | 搜索中心的纬度（未知位置时由系统自动生成） |
| lon              | float       | 否       | -                    | 搜索中心的经度（未知位置时由系统自动生成） |
| radius           | int        | 否       | 1000                | 搜索半径（单位：米）           |
| limit            | int        | 否       | 15                   | 最大返回结果数量（1-100）         |

## 响应格式

```json
{
  "query": "parking garages lots",
  "results": [
    {
      "name": "Icon Parking - West 33rd Street",
      "lat": 40.7502,
      "lon": -73.9930,
      "type": "parking",
      "distance_m": 120,
      "relevance_score": 0.93,
      "address": "..."
    }
  ],
  "ai_ranked": true,
  "pagination": {
    "total_results": 11,
    "limit": 15,
    "offset": 0,
    "has_more": false
  }
}
```

## 使用示例

### 在体育场附近寻找停车位
```bash
./scripts/parking-finder.sh '{"query": "parking near Dodger Stadium", "radius": 2000}'
```

### 在机场附近寻找停车位
```bash
./scripts/parking-finder.sh '{"query": "long term parking near SFO airport", "radius": 3000}'
```

### 在市中心区域寻找停车位
```bash
./scripts/parking-finder.sh '{"lat": 41.8781, "lon": -87.6298, "radius": 800, "limit": 10}'
```

## 使用建议：

- 在停车资源密集但难以找到的城区，建议使用较小的搜索半径（500-1000 米）；
- 在体育场、机场或郊区目的地附近，建议使用较大的搜索半径（2000-3000 米）；
- 在查询中包含场所名称，以获得更精准的搜索结果（例如：`parking near Madison Square Garden`）；
- 可结合 `route` 技能获取从停车场到目的地的步行路线；
- 可结合 `relationship` 技能比较多个停车选项之间的距离；
- 如需更精确的结果，请在查询中明确指定停车类型（如 `parking garages` 或 `street parking`）。