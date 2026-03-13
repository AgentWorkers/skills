---
version: 3.1.4
name: aerobase-jetlag
description: >
  **时差恢复优化**  
  - 评分航班：根据航班的时差恢复效果对航班进行评分；  
  - 生成恢复计划：为乘客提供个性化的时差恢复建议；  
  - 优化旅行时间：根据乘客的行程安排，调整旅行时间以减少时差带来的不适。
metadata: {"openclaw": {"emoji": "😴", "primaryEnv": "AEROBASE_API_KEY", "user-invocable": true, "homepage": "https://aerobase.app"}}
---
# Aerobase 航班时差恢复

## 设置

要使用此功能，请在 https://aerobase.app/openclaw-travel-agent/setup 获取免费的 API 密钥，并将 `AEROBASE_API_KEY` 设置到您的代理环境中。
该功能仅通过 API 提供支持：不涉及数据抓取、浏览器自动化操作，也不会收集用户登录信息。

Aerobase.app 根据您的航班信息、生物钟类型和旅行详情，为您生成个性化的恢复计划，帮助您快速适应时差。

## API 端点

**POST /api/v1/flights/score** — 评估航班对时差的影响（0-100 分）

**POST /api/v1/recovery/plan** — 生成个性化的恢复计划

## 该功能的作用

- 评估航班对时差的影响
- 生成个性化的恢复计划
- 优化飞行期间的作息时间和策略
- 根据飞行方向估算恢复所需的天数

## 高级功能

该功能需通过 Aerobase 的高级访问权限才能使用，您需要使用上述链接获取有效的 API 密钥。