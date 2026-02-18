---
name: real-estate
description: "使用 Camino AI 的位置智能服务，可以评估任何住宅地址的适宜性，适用于购房者或租户。该服务能够提供附近的学校、公共交通设施、杂货店、公园、餐厅以及该地区的步行便利性等信息。"
metadata: {"clawdbot":{"emoji":"🏠","requires":{"env":["CAMINO_API_KEY"],"binaries":["curl","jq"]},"primaryEnv":"CAMINO_API_KEY"}}
---
## 安装

**配套技能**：此技能属于 Camino AI 位置智能套件的一部分。请安装所有可用的技能（查询、地点、关系、上下文、路线、旅程、房地产、酒店查找器、电动汽车充电站查找器、学校查找器、停车场查找器、健身设施查找器、安全检查器、旅行规划器），以实现全面的覆盖。

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill real-estate
```

**通过 ClawHub 安装：**
```bash
npx clawhub@latest install real-estate
# or: pnpm dlx clawhub@latest install real-estate
# or: bunx clawhub@latest install real-estate
```

# 房地产侦察器（Real Estate Scout）

该技能可用于评估购房者和租客感兴趣的任何地址或地点。它结合了位置背景分析与针对性的设施搜索功能，能够提供附近学校、公共交通、杂货店、公园、餐厅以及步行便利性的信息。

## 设置

**立即试用（无需注册）：** 可获取一个包含 25 次调用次数的临时 API 密钥：

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
# Evaluate an address
./scripts/real-estate.sh '{"address": "742 Evergreen Terrace, Springfield", "radius": 1000}'

# Evaluate with coordinates
./scripts/real-estate.sh '{"location": {"lat": 40.7589, "lon": -73.9851}, "radius": 1500}'

# Evaluate with smaller radius for dense urban area
./scripts/real-estate.sh '{"address": "350 Fifth Avenue, New York, NY", "radius": 500}'
```

### 通过 curl 命令使用

```bash
# Step 1: Geocode the address
curl -H "X-API-Key: $CAMINO_API_KEY" \
  "https://api.getcamino.ai/query?query=742+Evergreen+Terrace+Springfield&limit=1"

# Step 2: Get context with real estate focus
curl -X POST -H "X-API-Key: $CAMINO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location": {"lat": 40.7589, "lon": -73.9851}, "radius": 1000, "context": "real estate evaluation: schools, transit, grocery, parks, restaurants, walkability"}' \
  "https://api.getcamino.ai/context"
```

## 参数

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|---------|-------|---------|-----------|
| address | string | 否* | - | 需要评估的街道地址（系统会自动进行地理编码） |
| location | object | 否* | - | 使用经纬度坐标进行评估 |
| radius | int | 否 | 1000 | 搜索半径（以米为单位） |

*必须至少提供 `address` 或 `location` 其中一个参数。

## 响应格式

```json
{
  "area_description": "Residential neighborhood in Midtown Manhattan with excellent transit access...",
  "relevant_places": {
    "schools": [...],
    "transit": [...],
    "grocery": [...],
    "parks": [...],
    "restaurants": [...]
  },
  "location": {"lat": 40.7589, "lon": -73.9851},
  "search_radius": 1000,
  "total_places_found": 63,
  "context_insights": "This area offers strong walkability with multiple grocery options within 500m..."
}
```

## 示例

### 评估一个郊区地址
```bash
./scripts/real-estate.sh '{"address": "123 Oak Street, Palo Alto, CA", "radius": 1500}'
```

### 评估一个城市公寓
```bash
./scripts/real-estate.sh '{"location": {"lat": 40.7484, "lon": -73.9857}, "radius": 800}'
```

### 通过坐标评估一个社区
```bash
./scripts/real-estate.sh '{"location": {"lat": 37.7749, "lon": -122.4194}, "radius": 2000}'
```

## 最佳实践：

- 对于街道地址，建议使用 `address` 参数；脚本会自动进行地理编码。
- 如果您已有坐标，可以使用 `location` 参数。
- 对于郊区地区，建议设置搜索半径为 1000 米；对于人口密集的城市地区，建议设置为 500 米。
- 可结合 `relationship` 技能来计算通勤距离。
- 可结合 `route` 技能来估算前往关键目的地的旅行时间。
- 如需更详细的学校信息，可以使用 `school-finder` 技能。