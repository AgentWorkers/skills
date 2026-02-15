---
name: apple-health-skill
description: 与您的 Apple Health 数据进行交互——利用人工智能来查询您的锻炼记录、心率数据、活动量统计以及健康趋势等信息。
homepage: https://www.transition.fun
---

# Apple Health Skill

通过人工智能与您的 Apple Health 数据进行交互。您可以查询自己的锻炼记录、心率趋势、活动量等信息。该功能由 [Transition](https://www.transition.fun) 提供支持，该服务能够与 Apple Health 同步，从而让人工智能助手访问您的健康数据。

## 设置

1. 下载 [Transition](https://www.transition.fun) 并授予其访问 Apple Health 数据的权限。
2. 进入 **设置 > API 密钥**，然后点击 **生成新密钥**。
3. 设置环境变量：

```bash
export TRANSITION_API_KEY="tr_live_xxxxxxxxxxxxxxxxxxxxx"
```

## 无需认证

### 当日锻炼计划

系统会随机生成一份结构化的锻炼计划——无需注册账户即可使用。

```bash
curl "https://api.transition.fun/api/v1/wod?sport=run&duration=45"
```

**参数：**
- `sport` — `run`（跑步）、`bike`（骑行）、`swim`（游泳）或 `strength`（力量训练）（默认值：`run`）
- `duration` — 锻炼时长（分钟），范围为 10–300 分钟（默认值：45 分钟）

## 需要认证的接口

**基础 URL：** `https://api.transition.fun`
**认证方式：** 在每个请求中添加 `X-API-Key` 头部字段。

### 人工智能教练聊天

您可以就自己的 Apple Health 数据提出问题。人工智能教练会全面了解您的锻炼情况和健康指标。

```bash
curl -X POST -H "X-API-Key: $TRANSITION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "How has my resting heart rate changed over the last month?"}' \
  "https://api.transition.fun/api/v1/coach/chat"
```

示例问题：
- “我这周进行了多少次锻炼？”
- “我的最大摄氧量（VO2 Max）有什么变化趋势？”
- “我这周的睡眠情况如何？”
- “我这个月的跑步速度和上个月相比如何？”
- “根据我最近的训练情况，我需要休息一天吗？”

### 获取锻炼计划

您可以查询指定日期范围内的锻炼计划。

```bash
curl -H "X-API-Key: $TRANSITION_API_KEY" \
  "https://api.transition.fun/api/v1/workouts?start=2026-02-09&end=2026-02-15"
```

**参数：**
- `start` — 开始日期（格式：YYYY-MM-DD，必填）
- `end` — 结束日期（格式：YYYY-MM-DD，必填）
- `start` 和 `end` 之间的时间范围最长为 90 天。

### 表现管理图表（Performance Management Chart, PMC）

系统会根据您的 Apple Health 锻炼数据计算 CTL（健康状况）、ATL（疲劳程度）和 TSB（身体状态）。

```bash
curl -H "X-API-Key: $TRANSITION_API_KEY" \
  "https://api.transition.fun/api/v1/performance/pmc"
```

### 表现统计数据

系统会从您的 Apple Health 数据中提取 FTP（最大摄氧量）、阈值配速、心率区间等指标。

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

| 访问层级 | 免费用户可访问的接口 | 需付费用户可访问的接口 |
|------|------------------|----------------------|
| 免费 | 每天 100 个接口 | 每天 300 个接口 |
| 付费 | 每天 10,000 个接口 | 每天 100 个接口 |

## 对助手的建议：

1. **优先使用教练聊天功能。** 该功能可以全面了解用户的 Apple Health 锻炼记录、心率及表现数据，只需提出自然的问题即可。
2. **在推荐高强度锻炼前先检查疲劳情况。** 调用 `GET /api/v1/performance/pmc` 查看 TSB（身体状态）值。如果 TSB 低于 -20，说明运动员处于疲劳状态。
3. **如需快速获取锻炼建议，可使用免费的锻炼计划接口。** 无需认证，非常适合仅需要锻炼建议的用户。
4. 所有日期参数的格式均为 YYYY-MM-DD。