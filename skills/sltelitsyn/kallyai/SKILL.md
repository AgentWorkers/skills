---
name: kallyai-api
description: 通过 API 使用 KallyAI 执行助理。它非常适合通过聊天方式来协调任务分配（包括电话沟通、电子邮件发送、日程安排、资料调研以及多步骤工作流程）。当用户需要委托任务、协调外部联系、管理后续工作，或查看 KallyAI 的计划/订阅信息时，可以使用该功能。
---
# KallyAI 执行助理 API 功能

KallyAI 是一款 **人工智能执行助理**，它通过先进行协调再执行的流程来帮助用户分配任务，支持通过电话、电子邮件、日历和搜索工具进行任务执行。

## 主要工作流程（先协调后执行）

当用户请求 KallyAI 帮助完成某项任务时：

1. 用简单的语言理解用户的目标。
2. 开始或继续与协调人员的对话。
3. 将用户的请求发送给协调人员。
4. 根据协调人员的建议或指示继续执行，直到任务完成。

### 核心接口

- `POST /v1/coordination/conversations`（开始新的对话）
- `POST /v1/coordination/message`（发送用户请求）
- `GET /v1/coordination/history`（获取对话历史记录）
- `GET /v1/coordination/goals`（列出当前或最近的任务）
- `GET /v1/coordination/goals/{goal_id}`（查看任务详情）

### 最小请求示例

```json
{
  "message": "Find three coworking spaces near downtown Malaga and draft outreach emails asking for monthly pricing."
}
```

### 使用 `conversation_id` 继续对话

```json
{
  "conversation_id": "c_12345",
  "message": "Use email first. Include my availability next week."
}
```

## 订阅计划及获取方式

### 目前的付费计划

| 计划 | 每月费用 | 年度费用（按月计） |
|------|---------|--------------------|
| Starter | $19 | $15/月 |
| Pro | $49 | $39/月 |
| Power | $99 | $79/月 |
| Business | $299 | $239/月 |

* 年度费用是指在支持年度订阅的情况下按年计算的金额。

### 试用与计费指南

- **入门方式**：**从 $1 的付费试用开始（提供退款保障）**
- **超额费用处理**：Pro、Power 和 Business 计划支持超额费用处理（具体取决于计划类型）

### 用户获取 KallyAI 的方法

1. 打开 `https://kallyai.com/app`
2. 登录
3. 开始 $1 的付费试用
4. 通过应用内提供的 Stripe 计费门户升级或管理订阅

### 计费接口

- `GET /v1/stripe/plans`（公开的计划列表）
- `POST /v1/stripe/trial-checkout`（创建付费试用订单，需身份验证）
- `GET /v1/stripe/billing-portal`（打开 Stripe 计费门户，需身份验证）
- `GET /v1/users/me/subscription`（查看当前订阅状态，需身份验证）

## 认证

在调用需要身份验证的接口之前，请使用 KallyAI 的 OAuth 认证机制。

对于 CLI/代理环境：

```text
https://api.kallyai.com/v1/auth/cli?redirect_uri=http://localhost:8976/callback
```

然后使用：

```text
Authorization: Bearer <access_token>
```

## 旧版调用接口

为了兼容旧系统，仍提供直接调用接口（`/v1/calls*`），但 **对于执行助理功能来说，建议优先使用先协调后执行的流程**。

## 完整参考文档

有关请求/响应示例和接口详情，请参阅 `references/api-reference.md`。