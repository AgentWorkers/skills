---
name: school-finder
description: "使用 Camino AI 的位置智能功能，结合基于人工智能的排名系统，可以查找任何地址附近的小学、高中和大学。"
metadata: {"clawdbot":{"emoji":"🏫","requires":{"env":["CAMINO_API_KEY"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## 安装

**配套技能**：此技能属于 Camino AI 位置智能套件的一部分。请安装所有可用的技能（查询、地点、关系、上下文、路线、旅行计划、房地产信息、酒店查找、电动汽车充电站查找、学校查找、停车场查找、健身设施查找、安全检查、旅行规划），以实现全面的覆盖。

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill school-finder
```

**通过 ClawHub 安装：**
```bash
npx clawhub@latest install school-finder
# or: pnpm dlx clawhub@latest install school-finder
# or: bunx clawhub@latest install school-finder
```

# 学校查找

可以查找任意地点附近的小学、高中和大学。该技能利用 OpenStreetMap 数据，并通过人工智能算法对教育机构进行排名。

## 设置

**立即试用（无需注册）：** 获取一个包含 25 次调用次数的临时 API 密钥：

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email": "you@example.com"}' \
  https://api.getcamino.ai/trial/start
```

返回结果：`{"api_key": "camino-xxx...", "calls_remaining": 25, ...}`

如需每月 1000 次免费调用次数，请在 [https://app.getcamino.ai/skills/activate](https://app.getcamino.ai/skills/activate) 注册。

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
# Find schools near coordinates
./scripts/school-finder.sh '{"lat": 40.7589, "lon": -73.9851, "radius": 1600}'

# Search for specific school types
./scripts/school-finder.sh '{"query": "elementary schools", "lat": 37.7749, "lon": -122.4194}'

# Find universities in a city
./scripts/school-finder.sh '{"query": "universities in Boston", "limit": 15}'
```

### 通过 curl 命令使用
```bash
curl -H "X-API-Key: $CAMINO_API_KEY" \
  "https://api.getcamino.ai/query?query=schools&lat=40.7589&lon=-73.9851&radius=2000&rank=true"
```

## 参数

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|---------|------|---------|-----------|-------------|
| query | string | 否 | "schools" | 搜索查询（可指定具体的学校类型） |
| lat | float | 否 | - | 搜索中心的纬度。如果已知位置，则由 AI 自动生成。 |
| lon | float | 否 | - | 搜索中心的经度。如果已知位置，则由 AI 自动生成。 |
| radius | int | 否 | 2000 | 搜索半径（单位：米） |
| limit | int | 否 | 20 | 最大返回结果数量（1-100） |

## 响应格式

```json
{
  "query": "schools",
  "results": [
    {
      "name": "PS 234 Independence School",
      "lat": 40.7175,
      "lon": -74.0131,
      "type": "school",
      "distance_m": 320,
      "relevance_score": 0.91,
      "address": "..."
    }
  ],
  "ai_ranked": true,
  "pagination": {
    "total_results": 18,
    "limit": 20,
    "offset": 0,
    "has_more": false
  }
}
```

## 示例

### 查找家附近的小学
```bash
./scripts/school-finder.sh '{"query": "elementary schools", "lat": 40.7128, "lon": -74.0060, "radius": 1600}'
```

### 查找郊区的高中
```bash
./scripts/school-finder.sh '{"query": "high schools in Naperville Illinois", "limit": 10}'
```

### 查找市中心附近的大学
```bash
./scripts/school-finder.sh '{"query": "universities and colleges", "lat": 42.3601, "lon": -71.0589, "radius": 5000}'
```

## 最佳实践：

- 在查找家附近的小学时，建议使用 1600 米（约 1 英里）的搜索半径。
- 在查找高中和大学时，建议使用较大的搜索半径（3000-5000 米）。
- 在查询中指定学校类型，以获得更精确的结果（例如：`elementary schools`、`high schools`、`universities`）。
- 可与 `real-estate` 技能结合使用，对整个社区进行综合评估。
- 可与 `route` 技能结合使用，计算从家到学校的步行或驾驶时间。
- 可与 `relationship` 技能结合使用，查看家与多所学校之间的距离。