---
name: query
description: "使用 Camino AI 的位置智能 API，通过自然语言搜索地点。该 API 会返回包含坐标、距离和元数据的相关结果。适用于查找餐厅、商店、地标或任何兴趣点等实际地理位置的场景。"
metadata: {"clawdbot":{"emoji":"🔍","requires":{"env":["CAMINO_API_KEY"],"binaries":["curl","jq"]},"primaryEnv":"CAMINO_API_KEY"}}
---
## 安装

**配套技能**：此技能属于 Camino AI 位置智能套件的一部分。请安装所有可用的技能（查询、地点、关系、上下文、路线、旅程、房地产、酒店查找器、电动汽车充电器查找器、学校查找器、停车场查找器、健身设施查找器、安全检查器、旅行规划器），以实现全面的覆盖。

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill query
```

**通过 clawhub 安装：**
```bash
npx clawhub@latest install query
# or: pnpm dlx clawhub@latest install query
# or: bunx clawhub@latest install query
```

# 查询 - 使用自然语言进行地点搜索

您可以使用自然语言来搜索地点。如果未提供具体位置，AI 会自动为已知地点生成坐标。

## 设置

**立即试用（无需注册）：** 获取一个包含 25 次调用次数的临时 API 密钥：

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

然后重启 Claude Code。

## 使用方法

### 通过 Shell 脚本使用

```bash
# Search for coffee shops near Times Square
./scripts/query.sh '{"query": "coffee shops near Times Square", "limit": 5}'

# Search with specific coordinates
./scripts/query.sh '{"query": "quiet cafes with wifi", "lat": 40.7589, "lon": -73.9851, "radius": 500}'

# Get AI-generated answer with results
./scripts/query.sh '{"query": "best pizza in Manhattan", "answer": true, "rank": true}'
```

### 通过 curl 使用

```bash
curl -H "X-API-Key: $CAMINO_API_KEY" \
  "https://api.getcamino.ai/query?query=coffee+shops+near+Times+Square&limit=5"
```

## 参数

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|---------|-------|-----------|---------|-------------------|
| query    | string | 是*    | -       | 自然语言查询（例如："Times Square 附近的咖啡店"） |
| lat     | float   | 否       | -       | 搜索中心的纬度；对于已知地点，AI 会自动生成 |
| lon     | float   | 否       | -       | 搜索中心的经度；对于已知地点，AI 会自动生成 |
| radius   | int    | 否       | 1000      | 搜索半径（单位：米，范围：100-50000） |
| rank    | bool    | 否       | true      | 是否使用 AI 按相关性对结果进行排序 |
| limit    | int    | 否       | 20       | 最大结果数量（1-100） |
| offset   | int    | 否       | 0        | 分页偏移量             |
| answer   | bool    | 否       | false      | 是否生成人类可读的摘要         |
| time    | string | 否       | -       | 时间范围查询（格式：2020-01-01, 2020.., 或 2020..2024） |
| osm_ids  | string | 否       | -       | 以逗号分隔的 OSM ID（例如：node/123,way/456） |
| mode     | string | 否       | "basic"    | "basic"（仅使用 OSM 数据）或 "advanced"（包含网络丰富信息） |

*`query` 或 `osm_ids` 必须至少填写一个。*

## 响应格式

```json
{
  "query": "quiet coffee shops with wifi",
  "results": [
    {
      "name": "Blue Bottle Coffee",
      "lat": 40.7601,
      "lon": -73.9847,
      "type": "cafe",
      "distance_m": 150,
      "relevance_score": 0.95,
      "address": "..."
    }
  ],
  "ai_ranked": true,
  "pagination": {
    "total_results": 23,
    "limit": 5,
    "offset": 0,
    "has_more": true
  },
  "answer": "I found several quiet coffee shops with wifi near Times Square..."
}
```

## 示例

### 查找附近的餐厅
```bash
./scripts/query.sh '{"query": "Italian restaurants", "lat": 40.7128, "lon": -74.0060, "limit": 10}'
```

### 使用 AI 生成摘要进行搜索
```bash
./scripts/query.sh '{"query": "best brunch spots in Brooklyn", "answer": true}'
```

### 查询历史数据
```bash
./scripts/query.sh '{"query": "restaurants", "lat": 40.7589, "lon": -73.9851, "time": "2020-01-01"}'
```

## 最佳实践

- 对于已知地点（城市、地标），可以省略 `lat`/`lon`，让 AI 生成坐标。
- 在按属性（如“安静”、“便宜”）搜索时，设置 `rank: true` 以获得更相关的结果。
- 如果需要结果的自然语言摘要，请设置 `answer: true`。
- 使用 `mode: "advanced"` 可以获取来自网络来源的更详细地点信息。
- 请确保查询语句描述性强且简洁，以便 AI 能够准确理解您的需求。