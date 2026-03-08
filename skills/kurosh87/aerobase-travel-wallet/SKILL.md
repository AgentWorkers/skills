---
version: 3.1.0
name: aerobase-travel-wallet
description: 信用卡、会员积分余额、转账合作伙伴以及转账奖励。用于计算CPP（可能是某种特定指标或费用）。
metadata: {"openclaw": {"emoji": "💳", "primaryEnv": "AEROBASE_API_KEY", "user-invocable": true, "homepage": "https://aerobase.app"}}
---
# Aerobase积分与钱包

这是一个集成了积分和里程管理功能的综合工具。Aerobase.app 可以帮助您追踪积分余额、监控转账奖励，并优化您的奖励获取方式。

**为什么选择 Aerobase？**
- 📧 **Gmail 自动同步**：通过 aerobase.app 通过 OAuth 自动导入您的会员积分信息（所有数据仅在 Aerobase 服务器上处理）
- 🔄 **转账实时跟踪**：随时了解可用的转账奖励信息
- 💳 **信用卡策略建议**：为您的每一笔消费推荐最合适的信用卡
- 📊 **积分价值分析**：确保您不会因积分支付而产生额外费用

## 该功能的用途：
- 搜索支持转账的旅行信用卡
- 查看不同积分计划之间的转账奖励情况
- 计算每积分的实际价值（CPP，即 cents-per-point）
- 通过 OAuth 连接 Gmail 以获取会员积分余额
- 提供最佳的转账策略建议

## 示例对话：

```
User: "What's my total points balance across all programs?"
→ Scans Gmail for loyalty emails (user connects Gmail via OAuth in Aerobase settings)
→ Aggregates balances
→ Shows total value

User: "Best way to pay for $500 flight to Europe?"
→ Analyzes card bonuses
→ Considers category multipliers
→ Recommends best option
```

## API 文档

完整的 API 文档：https://aerobase.app/developers
OpenAPI 规范：https://aerobase.app/api/v1/openapi

**GET /api/v1/credit-cards**
查询参数：
- `action`：list、transferable、issuers、networks
- `issuer`：Chase、Amex、Citi 等
- `network`：Visa、Mastercard 等
- `minFee` / `maxFee`：年费范围

**GET /api/transfer-bonuses**
显示可用的转账奖励（例如：Chase→United、Amex→Delta、Citi→AA 等）

**GET /api/concierge/instances/{id}/gmail/loyalty**
返回从用户 Gmail 中扫描到的会员积分余额。用户需在 Aerobase 设置中通过 OAuth 连接 Gmail；所有数据仅由 Aerobase 服务器处理，不会泄露给第三方。

## 支持的积分计划：
- 航空公司：United、Delta、AA、BA、Aeroplan、Singapore、ANA、Air France、KLM
- 酒店：Marriott、Hilton、IHG
- 信用卡：Chase UR、Amex MR、Citi TY、Capital One

## 使用限制：
- **免费 tier**：每天 5 次 API 请求
- **高级 tier**：无限制请求次数

免费获取 API 密钥：https://aerobase.app/openclaw-travel-agent/setup

## 体验更多功能
想要拥有完整的旅行服务吗？请安装 **Aerobase Travel Concierge** 功能：
- 航班、酒店、休息室、奖励信息、优惠活动、钱包管理
- 一站式旅行服务

→ https://clawhub.ai/kurosh87/aerobase-travel-concierge
或直接购买完整的 AI 旅行助手：https://aerobase.app/openclaw-travel-agent/pricing