---
name: garmin-skill
description: 与您的 Garmin 设备进行交流——利用人工智能询问有关您的活动、训练负荷、最大摄氧量（VO2 Max）、心率区间等方面的信息。
homepage: https://www.transition.fun
---

# Garmin Skill

通过AI与您的Garmin Connect数据进行交互。您可以查询自己的跑步、骑行、游泳记录、训练负荷、最大摄氧量（VO2 Max）、心率区间以及运动表现趋势等信息。该功能由[Transition](https://www.transition.fun)提供支持，该平台与Garmin Connect同步，使AI代理能够访问您的训练数据。

## 设置

1. 下载[Transition](https://www.transition.fun)并关联您的Garmin账户。
2. 进入**设置 > API密钥**，然后点击**生成新密钥**。
3. 设置环境变量：

```bash
export TRANSITION_API_KEY="tr_live_xxxxxxxxxxxxxxxxxxxxx"
```

## 无需认证

### 当日训练计划

生成一个随机的结构化训练计划——无需注册账户即可使用。

```bash
curl "https://api.transition.fun/api/v1/wod?sport=run&duration=45"
```

**参数：**
- `sport`：`run`（跑步）、`bike`（骑行）、`swim`（游泳）或`strength`（力量训练）（默认：`run`）
- `duration`：训练时长（分钟），范围为10-300分钟（默认：45分钟）

## 需要认证的接口

**基础URL：** `https://api.transition.fun`
**认证方式：** 在每个请求中添加`X-API-Key`头部。

### AI教练聊天

您可以就自己的Garmin数据提出问题。AI教练会全面了解您的活动情况、训练负荷和运动表现。

```bash
curl -X POST -H "X-API-Key: $TRANSITION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "How has my running volume changed this month compared to last?"}' \
  "https://api.transition.fun/api/v1/coach/chat"
```

示例问题：
- “我这周最长的跑步距离是多少？”
- “我的最大摄氧量（VO2 Max）有什么变化趋势？”
- “根据我最近的Garmin数据，我是否存在过度训练的情况？”
- “比较一下我这个月和上个月的骑行功率？”
- “我的心率数据能反映我的健康状况吗？”

### 获取训练计划

检索指定日期范围内的训练计划。

```bash
curl -H "X-API-Key: $TRANSITION_API_KEY" \
  "https://api.transition.fun/api/v1/workouts?start=2026-02-09&end=2026-02-15"
```

**参数：**
- `start`：开始日期（格式为YYYY-MM-DD，必填）
- `end`：结束日期（格式为YYYY-MM-DD，必填）
- `start`和`end`之间的时间范围最多为90天。

### 运动表现管理图表（Performance Management Chart, PMC）

根据您的Garmin活动数据，计算出CTL（健康状况）、ATL（疲劳程度）和TSB（身体状态）。

```bash
curl -H "X-API-Key: $TRANSITION_API_KEY" \
  "https://api.transition.fun/api/v1/performance/pmc"
```

### 运动表现统计

获取FTP（最大摄氧量）、阈值配速、心率区间等从Garmin数据中得出的各项指标。

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

### 将训练计划推送到Garmin设备

将生成的训练计划直接发送到您的Garmin设备上。

```bash
curl -X POST -H "X-API-Key: $TRANSITION_API_KEY" \
  "https://api.transition.fun/api/v1/workouts/123/push-garmin"
```

## 访问限制

| 订阅等级 | 免费用户可访问的接口 | 需付费用户可访问的接口 |
|------|------------------|-------------------|
| 免费 | 每天100个接口 | 每天300个接口 |
| 付费 | 每天10,000个接口 | 每天100个接口 |

## 代理使用提示

1. **优先使用AI教练聊天功能。**该功能能全面了解用户的Garmin活动、训练负荷和运动表现，只需提出自然的问题即可。
2. **在推荐高强度训练计划前请先检查疲劳情况。**调用`GET /api/v1/performance/pmc`查看TSB值。如果TSB低于-20，说明运动员处于疲劳状态。
3. **如需快速获取训练建议，可以使用免费的WOD接口。**无需认证，非常适合仅需要训练建议的用户。
4. **所有日期参数的格式均为YYYY-MM-DD。**