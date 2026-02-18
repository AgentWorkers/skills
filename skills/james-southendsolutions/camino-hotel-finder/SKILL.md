---
name: hotel-finder
description: "使用 Camino AI 的位置智能功能，您可以搜索位于地标、会议场所或特定社区附近的酒店、旅舍及其他住宿设施。该系统还提供基于人工智能的排名服务，帮助您更轻松地找到最合适的住宿选择。"
metadata: {"clawdbot":{"emoji":"🏨","requires":{"env":["CAMINO_API_KEY"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## 安装

**配套技能**：此技能属于 Camino AI 位置智能套件的一部分。请安装所有可用的技能（查询、地点、关系、上下文、路线、旅程、房地产、酒店查找器、电动汽车充电器查找器、学校查找器、停车查找器、健身设施查找器、安全检查器、旅行规划器），以实现全面的覆盖。

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill hotel-finder
```

**通过 clawhub 安装：**
```bash
npx clawhub@latest install hotel-finder
# or: pnpm dlx clawhub@latest install hotel-finder
# or: bunx clawhub@latest install hotel-finder
```

# 酒店查找器

您可以搜索地标、会议场所或周边地区的酒店、青年旅社及其他住宿设施。搜索结果会根据相关性由 AI 进行排序，并附有易于阅读的摘要。

## 设置

**立即试用（无需注册）**：您可以获取一个包含 25 次调用次数的临时 API 密钥：

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email": "you@example.com"}' \
  https://api.getcamino.ai/trial/start
```

返回格式：`{"api_key": "camino-xxx...", "calls_remaining": 25, ...}`

如需每月 1000 次免费调用，请在 [https://app.getcamino.ai/skills/activate](https://app.getcamino.ai/skills/activate) 注册。

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
# Search for hotels near a landmark
./scripts/hotel-finder.sh '{"query": "hotels near the Eiffel Tower", "limit": 5}'

# Search with specific coordinates
./scripts/hotel-finder.sh '{"query": "boutique hotels", "lat": 40.7589, "lon": -73.9851, "radius": 1000}'

# Search for hostels in a city
./scripts/hotel-finder.sh '{"query": "hostels in Barcelona", "limit": 10}'
```

### 通过 curl 使用

```bash
curl -H "X-API-Key: $CAMINO_API_KEY" \
  "https://api.getcamino.ai/query?query=hotels+near+the+Eiffel+Tower&limit=5&rank=true&answer=true"
```

## 参数

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|---------|------|---------|-----------|-------------|
| query | string | 是 | - | 自然语言查询（例如：Eiffel Tower 附近的酒店） |
| lat | float | 否 | - | 搜索中心的纬度。如果已知位置，则 AI 会自动生成该值。 |
| lon | float | 否 | - | 搜索中心的经度。如果已知位置，则 AI 会自动生成该值。 |
| radius | int | 否 | 2000 | 搜索半径（单位：米） |
| limit | int | 否 | 10 | 最大结果数量（1-100） |

## 响应格式

```json
{
  "query": "hotels near the Eiffel Tower",
  "results": [
    {
      "name": "Hotel du Champ de Mars",
      "lat": 48.8555,
      "lon": 2.3005,
      "type": "hotel",
      "distance_m": 350,
      "relevance_score": 0.92,
      "address": "..."
    }
  ],
  "ai_ranked": true,
  "pagination": {
    "total_results": 15,
    "limit": 5,
    "offset": 0,
    "has_more": true
  },
  "answer": "I found several hotels near the Eiffel Tower. The closest is..."
}
```

## 示例

### 在会议场所附近的酒店
```bash
./scripts/hotel-finder.sh '{"query": "hotels near Moscone Center San Francisco", "limit": 10}'
```

### 某城市内的经济型青年旅社
```bash
./scripts/hotel-finder.sh '{"query": "hostels in Amsterdam", "radius": 3000, "limit": 15}'
```

### 机场附近的住宿设施
```bash
./scripts/hotel-finder.sh '{"query": "hotels near JFK airport", "radius": 5000}'
```

## 最佳实践

- 在查询中包含地标或具体区域名称，以获得更准确的结果。
- 对于郊区或机场附近的搜索，建议使用较大的搜索半径（3000-5000 米）。
- 对于人口密集的城市中心，建议使用较小的搜索半径（500-1000 米）。
- 可结合 `route` 技能计算从酒店到目的地的旅行时间。
- 可结合 `context` 技能获取每家酒店周边的详细环境信息。
- AI 的排序结果会优先考虑与查询意图的匹配度和相关性。