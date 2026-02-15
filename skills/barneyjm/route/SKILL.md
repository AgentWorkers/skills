---
name: route
description: "获取两点之间的详细路线信息，包括距离、行驶时间以及可选的逐向导航指示。当您需要导航指引或估算两地之间的行驶时间时，可以使用此功能。"
metadata: {"clawdbot":{"emoji":"🧭","requires":{"env":["CAMINO_API_KEY"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## 安装

**配套技能**：此技能属于 Camino AI 的位置智能套件。请安装所有可用的技能（查询、地点、关系、上下文、路线、旅程、房地产、酒店查找器、电动汽车充电站查找器、学校查找器、停车场查找器、健身设施查找器、安全检查器、旅行规划器），以实现全面的覆盖。

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill route
```

**通过 clawhub 安装：**
```bash
npx clawhub@latest install route
# or: pnpm dlx clawhub@latest install route
# or: bunx clawhub@latest install route
```

# 路线 - 点对点导航

获取两点之间的详细路线信息，包括距离、行驶时间以及可选的逐向导航指令。

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

将密钥添加到您的 `~/.claude/settings.json` 文件中：

```json
{
  "env": {
    "CAMINO_API_KEY": "your-api-key-here"
  }
}
```

重启 Claude Code。

## 使用方法

### 通过 Shell 脚本使用
```bash
# Get driving directions
./scripts/route.sh '{
  "start_lat": 40.7128,
  "start_lon": -74.0060,
  "end_lat": 40.7589,
  "end_lon": -73.9851
}'

# Walking directions
./scripts/route.sh '{
  "start_lat": 40.7128,
  "start_lon": -74.0060,
  "end_lat": 40.7589,
  "end_lon": -73.9851,
  "mode": "foot"
}'

# With route geometry for mapping
./scripts/route.sh '{
  "start_lat": 40.7128,
  "start_lon": -74.0060,
  "end_lat": 40.7589,
  "end_lon": -73.9851,
  "mode": "bike",
  "include_geometry": true
}'
```

### 通过 curl 使用
```bash
curl -H "X-API-Key: $CAMINO_API_KEY" \
  "https://api.getcamino.ai/route?start_lat=40.7128&start_lon=-74.0060&end_lat=40.7589&end_lon=-73.9851&mode=car"
```

## 参数

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|---------|------|---------|-----------|
| start_lat | float | 是 | - | 起始纬度 |
| start_lon | float | 是 | - | 起始经度 |
| end_lat | float | 是 | - | 结束纬度 |
| end_lon | float | 是 | - | 结束经度 |
| mode | string | 否 | "car" | 交通方式："car"（汽车）、"bike"（自行车）或 "foot"（步行） |
| include_geometry | bool | 否 | false | 是否包含用于地图绘制的详细路线几何数据 |
| include_imagery | bool | 否 | false | 是否在路点处显示街道级图像 |

## 响应格式

```json
{
  "distance_km": 6.8,
  "duration_minutes": 18,
  "mode": "car",
  "summary": "Head north on Broadway, then east on 42nd Street",
  "steps": [
    {
      "instruction": "Head north on Broadway",
      "distance_m": 2400,
      "duration_s": 420
    },
    {
      "instruction": "Turn right onto 42nd Street",
      "distance_m": 1800,
      "duration_s": 300
    }
  ]
}
```

## 示例

### 步行路线指引
```bash
./scripts/route.sh '{
  "start_lat": 51.5074,
  "start_lon": -0.1278,
  "end_lat": 51.5014,
  "end_lon": -0.1419,
  "mode": "foot"
}'
```

### 带有地理信息的骑行路线指引
```bash
./scripts/route.sh '{
  "start_lat": 37.7749,
  "start_lon": -122.4194,
  "end_lat": 37.8199,
  "end_lon": -122.4783,
  "mode": "bike",
  "include_geometry": true
}'
```

### 带有图像的驾驶路线指引
```bash
./scripts/route.sh '{
  "start_lat": 40.7128,
  "start_lon": -74.0060,
  "end_lat": 40.7589,
  "end_lon": -73.9851,
  "mode": "car",
  "include_imagery": true
}'
```

## 使用场景

- **导航**：获取任何交通方式的逐向导航指令
- **旅行时间估算**：计算两点之间的行驶时间
- **地图可视化**：使用地理数据在地图上显示路线
- **通勤规划**：比较不同交通方式的出行时间