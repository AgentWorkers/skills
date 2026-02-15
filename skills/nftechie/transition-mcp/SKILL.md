---
name: transition-mcp
description: 基于人工智能的多项运动训练服务——为您提供跑步、骑行、游泳和铁人三项运动的个性化训练计划、训练方案以及性能分析。
homepage: https://www.transition.fun
---

# 多项运动教练 API

这是一个人工智能教练平台，能够为跑步者、自行车手、游泳者和铁人三项运动员制定个性化的训练计划。该平台提供训练计划、性能数据、人工智能指导以及计划调整等功能，由 [Transition](https://www.transition.fun) 提供技术支持。

## 认证

需要认证的接口请求必须设置 `TRANSITION_API_KEY` 环境变量，并将其作为 `X-API-Key` 头部信息传递。如果未设置该变量，请提示用户在 Transition 应用的“设置” > “API 密钥”中生成一个 API 密钥。

**基础 URL：** `https://api.transition.fun`

## 免费接口（无需认证）

### 每日训练计划

生成一个随机的、结构化的训练计划。每次请求都会返回不同的训练计划。

```bash
curl "https://api.transition.fun/api/v1/wod?sport=run&duration=45"
```

**参数：**
- `sport` — `run`（跑步）、`bike`（自行车）、`swim`（游泳）或 `strength`（力量训练）（默认值：`run`）
- `duration` — 训练时长（分钟），范围为 10-300 分钟（默认值：45 分钟）

**响应：**
```json
{
  "date": "2026-02-09",
  "sport": "run",
  "name": "Tempo Builder",
  "description": "Build aerobic endurance with sustained tempo efforts",
  "duration_minutes": 45,
  "intensity": "moderate",
  "segments": [
    {"name": "Warm-up", "duration_minutes": 9, "intensity": "easy", "description": "Easy jog to warm up"},
    {"name": "Tempo", "duration_minutes": 27, "intensity": "moderate", "description": "Steady tempo at comfortably hard pace"},
    {"name": "Cool-down", "duration_minutes": 9, "intensity": "easy", "description": "Easy jog to cool down"}
  ]
}
```

## 需要认证的接口

### 获取训练计划

检索指定日期范围内的训练计划。

```bash
curl -H "X-API-Key: $TRANSITION_API_KEY" \
  "https://api.transition.fun/api/v1/workouts?start=2026-02-09&end=2026-02-15"
```

**参数：**
- `start` — 开始日期（格式：YYYY-MM-DD，必填）
- `end` — 结束日期（格式：YYYY-MM-DD，必填）
- `start` 和 `end` 之间的时间范围最多为 90 天。

### 获取训练计划详情

```bash
curl -H "X-API-Key: $TRANSITION_API_KEY" \
  "https://api.transition.fun/api/v1/workouts/123"
```

### 生成训练计划

根据用户的训练计划，触发人工智能生成新的训练计划。

```bash
curl -X POST -H "X-API-Key: $TRANSITION_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.transition.fun/api/v1/workouts/generate"
```

### 调整训练计划

根据运动员的最新表现或日程变化来调整训练计划。

```bash
curl -X POST -H "X-API-Key: $TRANSITION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"reason": "feeling fatigued after race weekend"}' \
  "https://api.transition.fun/api/v1/workouts/adapt"
```

### 检查生成状态

查询训练计划的生成或调整是否已完成。

```bash
curl -H "X-API-Key: $TRANSITION_API_KEY" \
  "https://api.transition.fun/api/v1/workouts/status"
```

### 性能管理图表（PMC）

获取 CTL（体能状况）、ATL（疲劳程度）和 TSB（训练压力平衡）数据。

```bash
curl -H "X-API-Key: $TRANSITION_API_KEY" \
  "https://api.transition.fun/api/v1/performance/pmc"
```

### 性能统计

获取 FTP（最大摄氧量）、阈值配速、心率区间等性能指标。

```bash
curl -H "X-API-Key: $TRANSITION_API_KEY" \
  "https://api.transition.fun/api/v1/performance/stats"
```

### 与 AI 教练聊天

与人工智能教练进行实时聊天。聊天结果将以 SSE（Simple Text Encoding）格式返回。

```bash
curl -X POST -H "X-API-Key: $TRANSITION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "Should I do intervals today or rest?"}' \
  "https://api.transition.fun/api/v1/coach/chat"
```

### 聊天记录

查看与教练的聊天历史记录。

```bash
curl -H "X-API-Key: $TRANSITION_API_KEY" \
  "https://api.transition.fun/api/v1/coach/history"
```

### 运动员资料

查看运动员的个人信息和训练记录。

```bash
curl -H "X-API-Key: $TRANSITION_API_KEY" \
  "https://api.transition.fun/api/v1/profile"
```

### 将训练计划推送到 Garmin 设备

将训练计划数据同步到 Garmin 设备。

```bash
curl -X POST -H "X-API-Key: $TRANSITION_API_KEY" \
  "https://api.transition.fun/api/v1/workouts/123/push-garmin"
```

## 访问限制

| 订阅层级 | 免费用户 | 付费用户 |
|------|-----------|-----------|
| 免费 | 每天 100 次请求 | 每天 300 次请求 |
| 付费 | 每天 10,000 次请求 | 每天 100 次请求 |

**可访问的接口：**
- 免费用户：训练计划、性能数据、运动员资料、聊天记录
- 付费用户：与 AI 教练聊天、调整训练计划、生成新的训练计划

如果超过访问限制，系统会返回 HTTP 429 错误，并说明具体超出了哪种限制。

## 给代理的建议：

1. **在推荐高强度训练前检查运动员的疲劳状况。** 调用 `GET /api/v1/performance/pmc` 查看 TSB（训练压力平衡）值。如果 TSB 低于 -20，说明运动员可能处于疲劳状态，建议安排较轻松的训练或让其休息。
2. **谨慎使用训练计划调整功能。** 该功能会使用人工智能重新生成整个训练计划。仅在运动员明确要求调整或出现特殊情况（如受伤、日程变更）时才使用该功能。
3. **为普通用户推荐免费接口。** 如果用户仅需要快速获取训练计划，可以使用 `GET /api/v1/wod`，无需 API 密钥。
4. **训练计划的生成是异步的。** 调用 `POST /workouts/generate` 或 `POST /workouts/adapt` 后，需要通过 `GET /workouts/status` 检查生成状态，确认计划准备好后再下载训练数据。
5. **所有日期参数的格式均为 YYYY-MM-DD。**