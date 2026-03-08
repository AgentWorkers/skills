---
version: 3.1.0
name: aerobase-jetlag
description: >
  **时差恢复优化**  
  - 评分航班：根据航班的时差恢复效果对航班进行评估；  
  - 生成恢复计划：为乘客提供个性化的时差恢复建议；  
  - 优化旅行时间：根据乘客的行程安排，调整出行时间以减少时差带来的不适。
metadata: {"openclaw": {"emoji": "😴", "primaryEnv": "AEROBASE_API_KEY", "user-invocable": true, "homepage": "https://aerobase.app"}}
---
# Aerobase 跨时区恢复服务

让您在抵达目的地后迅速恢复精力。Aerobase.app 根据您的航班信息、生物钟类型和旅行详情，为您生成个性化的恢复计划。

**此功能为高级功能**，需订阅 Aerobase Concierge 服务才能使用。

**为什么选择 Aerobase？**
- 🧬 **个性化服务**：根据您的生物钟类型定制恢复计划
- 📊 **科学评估**：跨时区影响评分（0-100 分）
- 📅 **每日安排**：为您的旅行制定详细的恢复计划
- ✈️ **方向差异考虑**：区分向东飞行与向西飞行的差异

## 该功能的作用：
- 评估航班对您跨时区的影响（0-100 分）
- 生成个性化的恢复计划
- 优化出发/到达时间
- 提供时区调整策略建议
- 根据飞行方向计算所需的恢复天数

## 高级功能：包含在 Aerobase Concierge 订阅中

该功能仅为高级会员专属，包含在 Aerobase Concierge 订阅服务中：
→ https://aerobase.app/openclaw-travel-agent/pricing
- ✅ 无限次跨时区影响评估
- ✅ 个性化恢复计划
- ✅ 旅行前的准备建议
- ✅ 机上应对策略
- ✅ 到达时间建议

## 示例对话

```
User: "I'm flying from NYC to Paris next week - how bad is the jetlag?"
→ Scores the flight 0-100
→ Estimates recovery days
→ Provides strategies

User: "Generate a recovery plan for my Tokyo trip"
→ Creates day-by-day schedule
→ Includes light exposure timing
→ Sleep and diet recommendations
```

## API 文档

完整 API 文档：https://aerobase.app/developers
OpenAPI 规范：https://aerobase.app/api/v1/openapi

**POST /api/v1/flights/score**  
（用于评估航班的跨时区影响）

**POST /api/v1/recovery/plan**  
（用于获取包含每日安排的个性化恢复计划）

## 评分标准：
- **90-100 分**：效果极佳——几乎无跨时区影响
- **70-89 分**：效果良好——需要 1-2 天恢复
- **50-69 分**：效果一般——需要 2-3 天恢复
- **30-49 分**：效果较差——需要 3-4 天恢复
- **0-29 分**：效果非常差——预计会有严重的跨时区影响

## 订阅 Aerobase Concierge 服务

使用该功能需订阅 Aerobase Concierge：
- 无限次跨时区影响评估及恢复计划
- 所有其他高级功能均包含在内
- 提供专业的 AI 旅行顾问服务
→ https://aerobase.app/openclaw-travel-agent/pricing