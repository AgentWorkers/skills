---
name: askhuman
description: 在代理工作流程中，当需要人类的判断、反馈或决策时，请寻求人类的帮助。这种情况通常发生在以下场景：美学选择、伦理决策、内容审核、验证，或任何AI无法单独做出的主观评估。
license: MIT
compatibility: Requires network access to https://askhuman-api.onrender.com
metadata:
  author: askhuman
  version: "1.0.0"
  homepage: https://askhuman.guru/developers
allowed-tools: Bash(curl *) Bash(node *) Read
---
# AskHuman — 人类判断作为一项服务

在您的自动化工作流程中，您可以请求真实的人类做出主观决策。创建一个任务，由人类工作者来回答，然后您就能获得结果。

## 快速入门

1. 设置您的 API 密钥：`export ASKHUMAN_API_KEY=askhuman_sk_...`
2. 或者首次使用时让我自动注册（详见下方的认证部分）。

## 认证

检查环境变量中是否已经设置了 `ASKHUMAN_API_KEY`。如果设置了，请直接将其作为 `X-API-Key` 头部字段使用。

如果没有 API 密钥，请自动注册：

### 第一步：获取挑战任务

```bash
curl -s -X POST https://askhuman-api.onrender.com/v1/agents/challenge \
  -H "Content-Type: application/json" \
  -d '{"name":"ClaudeCodeAgent"}'
```

系统会返回一个 `challengeId` 和一个需要解决的简单问题（即 `task`）。

### 第二步：解决问题并完成注册

```bash
curl -s -X POST https://askhuman-api.onrender.com/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{
    "name":"ClaudeCodeAgent",
    "description":"AI coding assistant requesting human judgment",
    "walletAddress":"0x0000000000000000000000000000000000000000",
    "challengeId":"<challengeId>",
    "answer":"<solved_answer>"
  }'
```

系统会返回一个 `apiKey`（仅显示一次），请将其保存以供后续使用，并作为 `X-API-Key` 头部字段。

> 对于免费任务，请使用 `walletAddress: "0x0000000000000000000000000000000000000000"`。对于付费任务，请使用代理的 Base 链钱包地址。

## 如何请求人类帮助

### 第一步：创建任务

```bash
curl -s -X POST https://askhuman-api.onrender.com/v1/tasks \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ASKHUMAN_API_KEY" \
  -d '{
    "type": "CHOICE",
    "prompt": "Which logo looks more professional?",
    "options": ["Logo A", "Logo B"]
  }'
```

系统会返回创建的任务，其中包含一个 `id` 字段。

#### 任务类型

**CHOICE** — 从选项列表中选择一个答案：
```json
{
  "type": "CHOICE",
  "prompt": "Which color scheme looks better for a tech startup?",
  "options": ["Blue/White", "Dark/Gold", "Green/Black"]
}
```

**RATING** — 在数字范围内进行评分：
```json
{
  "type": "RATING",
  "prompt": "Rate the readability of this error message (1=terrible, 5=excellent): 'Error: ENOENT file not found'",
  "options": ["1", "2", "3", "4", "5"]
}
```

**TEXT** — 自由文本回答：
```json
{
  "type": "TEXT",
  "prompt": "Suggest a better name for a function that converts timestamps to human-readable relative time (e.g., '2 hours ago')"
}
```

**VERIFY** — 需要验证（是/否）：
```json
{
  "type": "VERIFY",
  "prompt": "Does this UI screenshot look correct? The header should be blue with white text and a centered logo."
}
```

### 第二步：等待答案

每 10 秒检查一次任务状态，直到有工作者提交答案：

```bash
curl -s https://askhuman-api.onrender.com/v1/tasks/<task_id> \
  -H "X-API-Key: $ASKHUMAN_API_KEY"
```

检查 `status` 字段：
- `PENDING` — 等待工作者接受任务
- `LOCKED` / `ASSIGNED` — 工作者已接受任务并正在处理
- `SUBMITTED` — 答案已准备好，存储在 `result` 字段中
- `RELEASED` — 任务完成，支付已释放

当 `status` 为 `SUBMITTED` 或 `RELEASED` 时，`result` 字段中会包含工作者的答案。

### 第三步：使用结果

从响应中提取 `result` 字段，其中包含工作者的答案。

获取结果后，您可以批准任务以释放支付（对于付费任务），或者将其标记为已完成：

```bash
curl -s -X POST https://askhuman-api.onrender.com/v1/tasks/<task_id>/approve \
  -H "X-API-Key: $ASKHUMAN_API_KEY"
```

## 操作

**Approve** — 接受结果（对于付费任务，释放支付）：
```bash
curl -s -X POST https://askhuman-api.onrender.com/v1/tasks/<task_id>/approve \
  -H "X-API-Key: $ASKHUMAN_API_KEY"
```

**Reject** — 要求重新处理并提供反馈：
```bash
curl -s -X POST https://askhuman-api.onrender.com/v1/tasks/<task_id>/reject \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ASKHUMAN_API_KEY" \
  -d '{"reason":"Please provide more detail in your answer."}'
```

**Cancel** — 取消任务（仅在工作者接受任务之前有效）：
```bash
curl -s -X POST https://askhuman-api.onrender.com/v1/tasks/<task_id>/cancel \
  -H "X-API-Key: $ASKHUMAN_API_KEY"
```

> 如果 72 小时内没有采取任何操作，任务将自动被批准。

## 付费任务（可选）

对于需要通过 Base 链向工作者支付 USDC 的任务：

1. 获取许可数据：`GET /v1/tasks/permit-data`
2. 使用 escrow 合同作为 spender，签署 EIP-2612 许可协议以获取 USDC 金额
3. 在创建任务时包含 `permit` 和 `amountUsdc` 字段：

```json
{
  "type": "CHOICE",
  "prompt": "Which design is better?",
  "options": ["Design A", "Design B"],
  "amountUsdc": 0.5,
  "permit": {
    "deadline": 1735689600,
    "signature": "0x..."
  }
}
```

## 完整的 API 参考文档

有关完整的 API 文档（包括 SSE 事件、消息传递、审核以及 EIP-2612 许可流程），请参阅 [API-REFERENCE.md](references/API-REFERENCE.md)。