---
name: tmrland-personal
description: "TMR Land 是一个专为 AI 商业市场设计的人工智能个人代理工具。使用场景包括：  
(1) 搜索 AI 或数据相关企业；  
(2) 发布购买意向；  
(3) 下单并管理托管交易；  
(4) 通过 Delta 评分系统比较企业质量；  
(5) 浏览 Grand Apparatus 的预测结果。"
homepage: https://tmrland.com
metadata: {"clawdbot":{"emoji":"🛒","requires":{"bins":["node"],"env":["TMR_API_KEY"]},"primaryEnv":"TMR_API_KEY"}}
---
# TMR Land — 个人技能

将您的代理连接到 TMR Land，这是一个提供双语（中文/英文）服务的 AI 商业交易平台。作为个人用户，您可以在平台上搜索企业、发布服务需求、下订单，并通过 Delta 评分系统来评估企业的服务质量。

## 设置

- 设置 `TMR_API_KEY`：通过 `POST /api/v1/api-keys`（角色为 “personal”）来生成该密钥。
- 可选设置 `TMR_BASE_URL`（默认值：`https://tmrland.com/api/v1`）。

## 脚本

```bash
# Search active businesses
node {baseDir}/scripts/search-businesses.mjs --limit 10

# Create an intention (structured need)
node {baseDir}/scripts/create-intention.mjs --title "Need NLP model" --description "Fine-tuned Chinese NLP model for sentiment analysis" --budget-min 500 --budget-max 2000

# Trigger multi-path matching (rules + BM25 + vector + RRF fusion)
node {baseDir}/scripts/trigger-match.mjs <intention-id>

# Place an order
node {baseDir}/scripts/create-order.mjs --business <id> --amount 1000 --intention <id>

# Check order status
node {baseDir}/scripts/order-status.mjs <order-id>
```

## 个人工作流程

1. **注册并充值**：创建账户，完成身份验证（KYC），为钱包充值资金。
2. **发布服务需求**：填写服务需求的相关信息（标题、描述、预算、标签等）。
3. **匹配企业**：系统会启动多路径的企业匹配流程。
4. **审核候选企业**：查看匹配结果、企业的信誉评分以及其过往的表现记录。
5. **下订单**：选择合适的企业，并可选择附加合同。
6. **支付**：系统会将资金冻结在您的钱包中。
7. **沟通**：通过订单聊天功能与企业进行交流。
8. **确认服务完成**：解冻钱包中的资金。
9. **评价企业**：对企业的服务进行评分并留下反馈。

## API 概述

认证方式：`Authorization: Bearer <TMR_API_KEY>`。所有 API 路径均以 `/api/v1` 为前缀。所有 ID 都使用 UUID 格式表示。支持双语字段（使用 `_zh`/`_en` 作为后缀）。分页查询通过 `offset` 和 `limit` 参数实现。

主要涉及的 API 域域包括：auth（认证）、wallet（钱包）、intentions（服务需求）、businesses（企业）、orders（订单）、contracts（合同）、delta（评分系统）、reviews（评价）、disputes（纠纷处理）、messages（消息传递）、notifications（通知）、apparatus（系统相关功能）。

详细请求/响应格式请参考 `references/` 文件。

## 错误代码说明

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求错误 — 验证失败 |
| 401 | 未经授权 — 令牌无效或缺失 |
| 403 | 禁止访问 — 权限不足 |
| 404 | 未找到相关资源 |
| 409 | 状态冲突 — 数据重复或状态转换无效 |
| 422 | 实体无法处理 — 数据格式错误 |
| 500 | 服务器内部错误 |