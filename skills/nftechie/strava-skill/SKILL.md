---
name: strava-skill
description: 与您的 Strava 数据进行互动——利用人工智能来询问有关您的活动、健康状况趋势、个人训练计划（PRs）以及训练负荷的问题。
homepage: https://www.transition.fun
---

# Strava Skill

通过人工智能与您的 Strava 数据进行交流。您可以查询自己的活动记录、健康状况、个人最佳成绩、训练负荷等信息。该功能由 [Transition](https://www.transition.fun) 提供支持，该平台会与 Strava 同步数据，从而让 AI 代理能够访问您的训练信息。

## 设置

1. 下载 [Transition](https://www.transition.fun) 并连接您的 Strava 账户。
2. 进入 **设置 > API 密钥**，然后点击 **生成新密钥**。
3. 设置环境变量：

```bash
export TRANSITION_API_KEY="tr_live_xxxxxxxxxxxxxxxxxxxxx"
```

## 无需身份验证

### 当日训练计划

生成一个随机的、结构化的训练计划——无需注册账户即可使用。

```bash
curl "https://api.transition.fun/api/v1/wod?sport=run&duration=45"
```

**参数：**
- `sport` — `run`（跑步）、`bike`（骑行）、`swim`（游泳）或 `strength`（力量训练）（默认值：`run`）
- `duration` — 时间（分钟），范围为 10–300 分钟（默认值：45 分钟）

## 需要身份验证的接口

**基础 URL：** `https://api.transition.fun`
**认证方式：** 在每个请求中添加 `X-API-Key` 头部字段。

### AI 教练聊天

您可以就自己的 Strava 数据提出问题。AI 教练会全面了解您的活动情况和表现。

```bash
curl -X POST -H "X-API-Key: $TRANSITION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "How did my long run this week compare to last week?"}' \
  "https://api.transition.fun/api/v1/coach/chat"
```

示例问题：
- “我上个月的周里程趋势如何？”
- “我的骑行 FTP（Functional Threshold Power）水平有什么变化？”
- “这周我的跑步量比平时多还是少？”
- “我最近最快的 5K 成绩是多少？”
- “根据我最近的活动情况，今天应该休息还是继续训练？”

### 获取训练计划

您可以查询指定日期范围内的训练计划。

```bash
curl -H "X-API-Key: $TRANSITION_API_KEY" \
  "https://api.transition.fun/api/v1/workouts?start=2026-02-09&end=2026-02-15"
```

**参数：**
- `start` — 开始日期（格式：YYYY-MM-DD，必填）
- `end` — 结束日期（格式：YYYY-MM-DD，必填）
- `start` 和 `end` 之间的时间范围最多为 90 天。

### 表现管理图表（Performance Management Chart, PMC）

根据您的 Strava 活动数据，计算 CTL（健康状况）、ATL（疲劳程度）和 TSB（身体状态）。

```bash
curl -H "X-API-Key: $TRANSITION_API_KEY" \
  "https://api.transition.fun/api/v1/performance/pmc"
```

### 表现统计数据

您可以获取 FTP（Functional Threshold Power）、阈值配速、心率区间等从 Strava 数据中得出的各项指标。

```bash
curl -H "X-API-Key: $TRANSITION_API_KEY" \
  "https://api.transition.fun/api/v1/performance/stats"
```

### 运动员个人资料

```bash
curl -H "X-API-Key: $TRANSITION_API_KEY" \
  "https://api.transition.fun/api/v1/profile"
```

### 聊天记录

```bash
curl -H "X-API-Key: $TRANSITION_API_KEY" \
  "https://api.transition.fun/api/v1/coach/history"
```

## 访问限制

| 订阅等级 | 免费用户可访问的接口 | 需付费用户可访问的接口 |
|------|------------------|----------------------|
| 免费 | 每天 100 个接口 | 每天 3 个接口 |
| 付费 | 每天 10,000 个接口 | 每天 100 个接口 |

## 代理使用提示

1. **优先使用教练聊天功能。** 该功能能提供用户 Strava 活动、训练负荷和表现的全面信息，只需提出自然的问题即可。
2. **在推荐高强度训练计划前，请先检查疲劳状况。** 调用 `GET /api/v1/performance/pmc` 并查看 TSB（身体状态）值。如果 TSB 低于 -20，说明运动员处于疲劳状态。
3. **如需快速获取训练建议，可以使用免费的训练计划接口。** 无需身份验证，非常适合只想获取训练建议的用户。
4. 所有日期参数的格式均为 YYYY-MM-DD。