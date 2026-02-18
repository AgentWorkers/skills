---
name: relationship
description: "计算两点之间的空间关系，包括距离、方向、旅行时间以及易于理解的描述。当需要了解各个位置之间的相对关系时，可以使用此功能。"
metadata: {"clawdbot":{"emoji":"📐","requires":{"env":["CAMINO_API_KEY"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## 安装

**配套技能**：此技能属于 Camino AI 位置智能套件的一部分。请安装所有可用的技能（查询、地点、关系、上下文、路线、旅程、房地产、酒店查找器、电动汽车充电站查找器、学校查找器、停车场查找器、健身设施查找器、安全检查器、旅行规划器），以实现全面的功能覆盖。

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill relationship
```

**通过 clawhub 安装：**
```bash
npx clawhub@latest install relationship
# or: pnpm dlx clawhub@latest install relationship
# or: bunx clawhub@latest install relationship
```

# 关系 - 空间计算

计算两点之间的距离、方向、行驶时间以及易于人类理解的描述信息。

## 设置

**立即试用（无需注册）：** 获取一个包含 25 次调用次数的临时 API 密钥：

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email": "you@example.com"}' \
  https://api.getcamino.ai/trial/start
```

返回格式：`{"api_key": "camino-xxx...", "calls_remaining": 25, ...}`

如需每月享受 1,000 次免费调用，请在 [https://app.getcamino.ai/skills/activate](https://app.getcamino.ai/skills/activate) 注册。

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
# Calculate relationship between two points
./scripts/relationship.sh '{
  "start": {"lat": 40.7128, "lon": -74.0060},
  "end": {"lat": 40.7589, "lon": -73.9851}
}'

# Include specific calculations
./scripts/relationship.sh '{
  "start": {"lat": 40.7128, "lon": -74.0060},
  "end": {"lat": 40.7589, "lon": -73.9851},
  "include": ["distance", "direction", "travel_time", "description"]
}'
```

### 通过 curl 使用
```bash
curl -X POST -H "X-API-Key: $CAMINO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"start": {"lat": 40.7128, "lon": -74.0060}, "end": {"lat": 40.7589, "lon": -73.9851}}' \
  "https://api.getcamino.ai/relationship"
```

## 参数

| 参数名 | 类型 | 是否必填 | 描述 |
|---------|--------|---------|-------------|
| start    | object   | 是       | 起始点（包含经纬度） |
| end     | object   | 是       | 终点（包含经纬度） |
| include | array   | 否       | 需要返回的信息类型：距离、方向、行驶时间、描述 |

## 响应格式

```json
{
  "distance": {
    "meters": 5420,
    "kilometers": 5.42,
    "miles": 3.37
  },
  "direction": {
    "bearing": 42,
    "cardinal": "NE",
    "description": "northeast"
  },
  "travel_time": {
    "walking_minutes": 68,
    "driving_minutes": 15,
    "cycling_minutes": 22
  },
  "description": "5.4 km northeast, about 15 minutes by car"
}
```

## 示例

### 简单的距离查询
```bash
./scripts/relationship.sh '{
  "start": {"lat": 51.5074, "lon": -0.1278},
  "end": {"lat": 48.8566, "lon": 2.3522}
}'
```

### 仅获取距离和方向
```bash
./scripts/relationship.sh '{
  "start": {"lat": 40.7128, "lon": -74.0060},
  "end": {"lat": 40.7589, "lon": -73.9851},
  "include": ["distance", "direction"]
}'
```

## 使用场景

- **距离判断**：确定两个地点是否在指定范围内
- **方向指引**：提供方向信息（如北、东南等）
- **旅行规划**：估算不同交通方式的行驶时间
- **位置描述**：生成易于理解的空间关系描述