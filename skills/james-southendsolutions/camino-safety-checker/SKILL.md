---
name: safety-checker
description: "查找任何地点附近的24小时营业场所、照明良好的公共区域、交通枢纽、警察局和医院，以提高夜间出行的安全性。"
metadata: {"clawdbot":{"emoji":"🔦","requires":{"env":["CAMINO_API_KEY"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## 安装

**配套技能**：此技能属于 Camino AI 位置智能套件的一部分。请安装所有可用的技能（查询、地点、关系、上下文、路线、旅程、房地产、酒店查找器、电动汽车充电站查找器、学校查找器、停车查找器、健身设施查找器、安全检查器、旅行规划器），以实现全面的覆盖。

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill safety-checker
```

**通过 ClawHub 安装：**
```bash
npx clawhub@latest install safety-checker
# or: pnpm dlx clawhub@latest install safety-checker
# or: bunx clawhub@latest install safety-checker
```

# 深夜安全

查找任何地点附近的 24 小时营业场所、照明良好的公共区域、交通站点和医院。为夜间出行提供以安全为中心的情境感知服务。

## 设置

**立即试用（无需注册）：** 获取一个包含 25 次调用次数的临时 API 密钥：

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email": "you@example.com"}' \
  https://api.getcamino.ai/trial/start
```

返回结果：`{"api_key": "camino-xxx...", "calls_remaining": 25, ...}`

如需每月免费使用 1,000 次调用次数，请在 [https://app.getcamino.ai/skills/activate](https://app.getcamino.ai/skills/activate) 注册。

**将 API 密钥添加到 Claude Code 中：**

将密钥添加到您的 `~/.claude/settings.json` 文件中：

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
# Check safety resources near a location
./scripts/safety-checker.sh '{"location": {"lat": 40.7506, "lon": -73.9935}, "radius": 500}'

# Check with larger radius
./scripts/safety-checker.sh '{"location": {"lat": 37.7749, "lon": -122.4194}, "radius": 800}'
```

### 通过 curl 使用

```bash
curl -X POST -H "X-API-Key: $CAMINO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location": {"lat": 40.7506, "lon": -73.9935}, "radius": 500, "context": "late night safety: 24-hour businesses, transit, police, hospitals"}' \
  "https://api.getcamino.ai/context"
```

## 参数

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|-----------|------|----------|---------|-------------|
| location | 对象 | 是 | - | 带有经纬度的坐标 |
| radius | 整数 | 否 | 500 | 搜索半径（单位：米） |

## 响应格式

```json
{
  "area_description": "Busy commercial area in Midtown Manhattan with 24-hour businesses...",
  "relevant_places": {
    "hospitals": [...],
    "police": [...],
    "transit": [...],
    "24_hour_businesses": [...],
    "pharmacies": [...]
  },
  "location": {"lat": 40.7506, "lon": -73.9935},
  "search_radius": 500,
  "total_places_found": 34,
  "context_insights": "This area has good late-night safety resources including..."
}
```

## 示例

### 检查酒店附近的夜间安全情况
```bash
./scripts/safety-checker.sh '{"location": {"lat": 40.7506, "lon": -73.9935}, "radius": 500}'
```

### 检查陌生社区的安全状况
```bash
./scripts/safety-checker.sh '{"location": {"lat": 34.0407, "lon": -118.2468}, "radius": 600}'
```

### 检查交通站点附近的夜间安全情况
```bash
./scripts/safety-checker.sh '{"location": {"lat": 41.8827, "lon": -87.6233}, "radius": 400}'
```

## 使用场景

- **夜间抵达**：查看您的酒店或 Airbnb 酒店附近的安全设施
- **夜间步行**：识别沿途照明良好的区域、营业中的场所以及紧急服务
- **旅行安全**：在夜间前往陌生社区前评估安全环境
- **紧急情况应对**：了解最近的医院和警察站的位置
- **交通安全**：查看您夜间将使用的交通站点附近有哪些可用资源