---
name: clawcall
version: 1.0.0
description: 为该代理分配一个真实的电话号码。接收用户的来电，在任务完成后回拨用户，执行预定的通话，或代表用户拨打第三方电话。所有电话相关功能均通过ClawCall服务自动处理。
metadata:
  openclaw:
    requires:
      bins: []
      env:
        - CLAWCALL_API_KEY
    primaryEnv: CLAWCALL_API_KEY
---
# ClawCall — 为您的代理提供电话服务

ClawCall 为您分配一个直接与该代理关联的真实电话号码。用户可以拨打该电话，您可以在任务完成后回拨给他们，也可以代表用户拨打第三方电话。

---

## 设置（仅首次使用）

如果 `CLAWCALL_API_KEY` 未设置，请执行注册流程：

1. 询问用户：“我应该使用哪个电子邮件地址来创建您的 ClawCall 账户？”
2. 询问用户：“您的个人电话号码是多少？（我会用这个号码给您打电话）”
3. 拨打电话：

```
POST https://api.clawcall.online/api/v1/register
Content-Type: application/json

{
  "email": "<user email>",
  "agent_webhook_url": "<your public URL>",
  "agent_name": "<optional name>",
  "phone_number": "<user's E.164 phone, e.g. +14155550100>"
}
```

4. 将返回的 `api_key` 存储为 `CLAWCALL_API_KEY`。
5. 告知用户他们的代理电话号码，设置完成。

**成功响应示例：**
```json
{
  "ok": true,
  "api_key": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "phone_number": "+14155550192",
  "tier": "free",
  "message": "Setup complete! Your agent number is +14155550192."
}
```

---

## 接听来电

ClawCall 会将以语音形式将来电内容转发到您的 webhook：

```
POST {your_webhook_url}/clawcall/message
{
  "call_sid": "CAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "message": "What's the weather like today?"
}
```

您的 webhook 必须做出响应：

```json
{
  "response": "It's currently 72°F and sunny.",
  "end_call": false
}
```

在完成响应后，请设置 `"end_call": true` 以挂断电话。

**重要提示：** 请在 25 秒内做出响应。如果任务需要更长时间，请快速回复一条中间消息（例如：“正在处理，请稍等。”），否则 ClawCall 会保持通话状态。

---

## 回拨用户（任务完成）

当您完成用户要求您汇报的背景任务后：

```
POST https://api.clawcall.online/api/v1/calls/outbound/callback
Authorization: Bearer {CLAWCALL_API_KEY}
Content-Type: application/json

{
  "message": "Your deployment finished. 3 services updated, 0 errors.",
  "allow_followup": true
}
```

如果 `allow_followup` 为 `true`，用户可以在听到回复后提出后续问题（此时会进入实时通话环节）。

**需要 Pro 级别权限。**

---

## 安排定期通话

当用户要求您按固定时间表拨打电话时：

```
POST https://api.clawcall.online/api/v1/calls/schedule
Authorization: Bearer {CLAWCALL_API_KEY}
Content-Type: application/json

{
  "cron": "0 8 * * 1-5",
  "label": "Morning briefing",
  "task_context": "Give me a summary of my calendar, top emails, and pending tasks",
  "timezone": "America/New_York"
}
```

常见的 cron 表达方式：
- 每个工作日早上 8 点：`"0 8 * * 1-5"`
- 每天早上 9 点：`"0 9 * * *"`
- 每个周一早上 7 点：`"0 7 * * 1"`

要取消定期通话安排，请执行以下操作：
```
DELETE https://api.clawcall.online/api/v1/calls/schedule/{id}
Authorization: Bearer {CLAWCALL_API_KEY}
```

**需要 Pro 级别权限。**

---

## 自动拨打电话给第三方（Pro 级别）

当用户要求您自动拨打其他人的电话时：

```
POST https://api.clawcall.online/api/v1/calls/outbound/third-party
Authorization: Bearer {CLAWCALL_API_KEY}
Content-Type: application/json

{
  "to_number": "+14155550100",
  "objective": "Book a dentist appointment for next Tuesday afternoon",
  "context": "Patient: Aayush Kumar. Returning patient. Flexible on time."
}
```

ClawCall 会：
1. 拨打电话
2. 将通话内容转发到您的 `/clawcall/message` webhook
3. 通话结束后，向 `/clawcall/third-party-complete` 发送 POST 请求

您的 webhook 会收到相同格式的响应数据；请注意前缀 `[THIRD PARTY CALL]` 或 `[THIRD PARTY SAYS`，以识别这是与第三方进行的通话。完成通话后，请设置 `end_call: true`。

**需要 Pro 级别权限。**

---

## 查看使用情况

```
GET https://api.clawcall.online/api/v1/account
Authorization: Bearer {CLAWCALL_API_KEY}
```

系统会显示您的使用级别、已用分钟数、剩余分钟数以及电话号码。

---

## 更改语音

您可以设置通话中使用的语音合成引擎（Polly 提供的神经网络语音）：

```
POST https://api.clawcall.online/api/v1/account/voice
Authorization: Bearer {CLAWCALL_API_KEY}
Content-Type: application/json

{ "voice": "aria" }
```

可用语音：`aria`（默认）、`joanna`、`matthew`、`amy`、`brian`、`emma`、`olivia`。

---

## 多代理管理（Team 级别）

Team 级别支持最多 5 名代理，每位代理都有自己的专属电话号码和 API 密钥。

**列出所有代理：**
```
GET https://api.clawcall.online/api/v1/agents
Authorization: Bearer {CLAWCALL_API_KEY}
```

**添加代理：**
```
POST https://api.clawcall.online/api/v1/agents
Authorization: Bearer {CLAWCALL_API_KEY}
Content-Type: application/json

{
  "agent_webhook_url": "https://agent2.tail1234.ts.net",
  "agent_name": "Work Agent"
}
```
系统会为新代理生成一个新的 `api_key` 和 `phone_number`。

**删除代理：**
```
DELETE https://api.clawcall.online/api/v1/agents/{agent_id}
Authorization: Bearer {CLAWCALL_API_KEY}
```
无法删除首次注册的代理。

---

## 通过 webhook 接收通话事件（Team 级别）

您可以实时接收通话事件的推送通知：

```
POST https://api.clawcall.online/api/v1/account/webhook
Authorization: Bearer {CLAWCALL_API_KEY}
Content-Type: application/json

{ "webhook_push_url": "https://your-server.com/clawcall-events" }
```

每次通话结束后，ClawCall 会向您指定的 URL 发送 JSON 格式的通知数据：
```json
{
  "event": "call.status",
  "call_sid": "CA...",
  "status": "completed",
  "duration_seconds": 42,
  "call_type": "user_initiated",
  "direction": "inbound"
}
```
如需禁用此功能，请发送空内容到 `webhook_push_url`。

---

## 级别限制

| 级别 | 每月分钟数 | 外拨电话 | 定期通话 | 第三方通话 | 代理数量 | Webhook 推送 |
|------|--------------|----------|-----------|-----------|--------|--------------|
| Free | 10           | 不支持       | 不支持        | 不支持        | 1      | 不支持           |
| Pro  | 120          | 支持      | 支持       | 支持       | 1      | 不支持           |
| Team | 500（共享）      | 支持      | 支持       | 支持       | 5      | 支持          |

超出使用量限制的部分，每分钟收取 0.05 美元（仅限 Pro/Team 级别）。

---

## 升级至 Pro 或 Team 级别

支持使用 Solana 主网上的 **USDC** 进行支付。

**步骤 1 — 获取支付信息：**
```
POST https://api.clawcall.online/api/v1/billing/checkout
Authorization: Bearer {CLAWCALL_API_KEY}
Content-Type: application/json

{ "tier": "pro" }
```

系统会提供 Solana 钱包地址及所需支付的 USDC 数额。

**步骤 2 — 向 Solana 钱包转账 USDC**
将指定金额的 USDC 转入提供的 Solana 钱包地址。

**步骤 3 — 提交交易签名：**
```
POST https://api.clawcall.online/api/v1/billing/verify
Authorization: Bearer {CLAWCALL_API_KEY}
Content-Type: application/json

{
  "tx_signature": "<your Solana tx signature>",
  "tier": "pro"
}
```

确认支付后，您的账户会立即升级到相应级别。

**查看账单状态：**
```
GET https://api.clawcall.online/api/v1/billing/status
Authorization: Bearer {CLAWCALL_API_KEY}
```