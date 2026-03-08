# AgentCall — 用于 AI 代理的电话号码服务

您可以使用 AgentCall API 来管理电话号码、短信、语音通话以及 AI 语音通话。

## 认证

所有请求都需要包含以下认证信息：`Authorization: Bearer <AGENTCALL_API_KEY>`

API 密钥存储在 `AGENTCALL_API_KEY` 环境变量中。

## 基本 URL

`https://api.agentcall.co`

完整的纯文本 API 参考文档请访问：`GET https://api.agentcall.co/llms.txt`

## 电话号码

**获取电话号码：**
```json
POST /v1/numbers/provision
Body: {
  "type": "local",
  "country": "US",
  "label": "my-agent"
}
```
可用类型：`local`（每月 $2）、`tollfree`（每月 $4）、`mobile`（每月 $3）、`sim`（每月 $8，仅限高级计划）

**列出所有电话号码：**
```json
GET /v1/numbers
Query: ?limit=20&country=US&type=local
```

**获取电话号码详情：**
```json
GET /v1/numbers/:id
```

**永久释放电话号码（不可恢复）：**
```json
DELETE /v1/numbers/:id
```

## 短信

**发送短信：**
```json
POST /v1/sms/send
Body: {
  "from": "num_xxx",
  "to": "+14155551234",
  "body": "Hello!"
}
```
`from` 可以是电话号码 ID 或 E.164 格式的电话字符串。

**查看短信收件箱：**
```json
GET /v1/sms/inbox/:numberId
Query: ?limit=20&otpOnly=true
```

**获取特定短信：**
```json
GET /v1/sms/:messageId
```

**获取验证码（最长等待 60 秒）：**
```json
GET /v1/sms/otp/:numberId
Query: ?timeout=60000
Response: {
  "otp": "482913",
  "message": { ... }
}
```

## 语音通话

**发起外拨电话：**
```json
POST /v1/calls/initiate
Body: {
  "from": "num_xxx",
  "to": "+14155551234",
  "record": false
}
```

**发起 AI 语音通话（高级计划，每分钟 $0.20）：**
AI 会根据您提供的 `systemPrompt` 自动完成整个通话过程。

```json
POST /v1/calls/ai
Body: {
  "from": "num_xxx",
  "to": "+14155551234",
  "systemPrompt": "您正在拨打电话预约周二下午的牙医服务。",
  "voice": "alloy",  // 语音类型
  "firstMessage": "您好，我想预约一个时间。",
  "maxDurationSecs": 600  // 最长通话时长（秒）
}
```
可选语音类型：
- `alloy`：中性、平衡的语调（默认）
- `ash`：温暖、亲切的语调
- `ballad`：富有表现力、旋律优美的语调
- `coral`：清晰、专业的语调
- `echo`：深沉、富有共鸣的语调
- `sage`：冷静、权威、自信的语调
- `shimmer`：明亮、充满活力的语调
- `verse`：流畅、表达清晰的语调

**查看通话记录：**
```json
GET /v1/calls
Query: ?limit=20
```

**获取通话详情：**
```json
GET /v1/calls/:callId
```

**获取 AI 通话的文字记录：**
```json
GET /v1/calls/:callId/transcript
Response: {
  "entries": [
    { "role": "assistant", "text": "...", "timestamp": "..." },
    "summary": "..."
  ],
  "summary": "..."
}
```

**挂断正在进行的通话：**
```json
POST /v1/calls/:callId/hangup
```

## Webhook

**注册 Webhook：**
```json
POST /v1/webhooks
Body: {
  "url": "https://example.com/hook",
  "events": ["sms.inbound", "sms.otp", "call.status"]
}
```
支持的事件类型：`sms.inbound`、`sms.otp`、`call.inbound`、`call.ringing`、`call.status`、`call.recording`、`number.released`

**列出所有 Webhook：**
```json
GET /v1/webhooks
```

**轮换 Webhook 密钥：**
```json
POST /v1/webhooks/:id/rotate
```

**删除 Webhook：**
```json
DELETE /v1/webhooks/:id
```

## 使用与计费

**查看使用情况：**
```json
GET /v1/usage
Query: ?period=2026-02
```

## 电话号码格式

所有电话号码必须采用 E.164 格式：`+{国家代码}{电话号码}`，例如 `+14155551234`。

## 常见工作流程

### 测试应用程序的短信验证功能（质量保证）
1. 使用 `POST /v1/numbers/provision`（`type`: `local`）获取测试电话号码。
2. 将该号码输入到应用程序的验证界面中。
3. 发送请求 `GET /v1/sms/otp/:numberId?timeout=60000` 以获取验证码。
4. 确认验证码到达后，应用程序应正确接收并处理它。
5. 使用 `DELETE /v1/numbers/:id` 删除测试电话号码。

### AI 语音通话
1. 使用 `POST /v1/numbers/provision`（`type`: `local`）获取电话号码（如尚未拥有）。
2. 发送请求 `POST /v1/calls/ai`（包含 `from`、`to` 和 `systemPrompt` 参数）以发起通话。
3. 等待通话结束。
4. 使用 `GET /v1/calls/:callId/transcript` 获取通话的完整文字记录。

## 错误代码
- **401**：API 密钥无效或缺失。
- **403 plan_limit**：计划使用量达到上限（请在 agentcall.co 控制台升级计划）。
- **404**：资源未找到。
- **422**：验证错误（请检查请求内容）。
- **429**：请求频率超过限制（每分钟 100 次）。