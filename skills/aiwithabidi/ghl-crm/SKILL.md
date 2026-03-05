---
name: ghl-crm
description: GoHighLevel CRM integration — manage contacts, pipelines, conversations (SMS/email/WhatsApp), calendars, appointments, and workflows through the GHL API v2. The definitive GHL skill for OpenClaw. Use when managing leads, booking appointments, sending follow-ups, or automating your CRM.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, GoHighLevel account with API v2 access
metadata: {"openclaw": {"emoji": "\ud83d\udcde", "requires": {"env": ["GHL_API_KEY"]}, "primaryEnv": "GHL_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# GHL CRM — 专为 OpenClaw 设计的 GoHighLevel 集成方案

本方案实现了与 GHL CRM 的全面集成，您可以通过 GHL API v2 管理联系人、销售流程、对话记录、预约信息以及工作流程。

## 快速入门

```bash
export GHL_API_KEY="your-private-integration-token"
export GHL_LOCATION_ID="your-location-id"
python3 {baseDir}/scripts/ghl_api.py contacts search "john@example.com"
```

## 认证

GHL 使用 **私有集成令牌**（API v2）进行身份验证。请按照以下步骤获取您的令牌：
1. 登录您的 GHL 子账户，进入 **设置 → 集成 → 私有集成**。
2. 创建一个新的集成配置，启用所需的权限。
3. 复制 API 密钥（即 `GHL_API_KEY`）。

**GHL_LOCATION_ID** 是您的子账户/地点 ID（可在 **设置 → 业务信息** 中找到，或通过相关 URL 获取）。

**基础 URL：** `https://services.leadconnectorhq.com`

**认证请求头：** `Authorization: Bearer <GHL_API_KEY>` + `Version: 2021-07-28`

## 可用命令

### 联系人管理
```bash
# Search contacts by email, phone, or name
python3 {baseDir}/scripts/ghl_api.py contacts search "query"

# Get contact by ID
python3 {baseDir}/scripts/ghl_api.py contacts get <contactId>

# Create a new contact
python3 {baseDir}/scripts/ghl_api.py contacts create '{"firstName":"John","lastName":"Doe","email":"john@example.com","phone":"+15551234567"}'

# Update contact
python3 {baseDir}/scripts/ghl_api.py contacts update <contactId> '{"tags":["vip","hot-lead"]}'

# Delete contact
python3 {baseDir}/scripts/ghl_api.py contacts delete <contactId>

# List contacts (with optional limit)
python3 {baseDir}/scripts/ghl_api.py contacts list --limit 20
```

### 销售流程与机会管理
```bash
# List all pipelines
python3 {baseDir}/scripts/ghl_api.py pipelines list

# List opportunities in a pipeline
python3 {baseDir}/scripts/ghl_api.py opportunities list <pipelineId>

# Get opportunity details
python3 {baseDir}/scripts/ghl_api.py opportunities get <opportunityId>

# Create opportunity
python3 {baseDir}/scripts/ghl_api.py opportunities create '{"pipelineId":"...","stageId":"...","contactId":"...","name":"Deal Name","monetaryValue":5000}'

# Update opportunity (move stage, update value)
python3 {baseDir}/scripts/ghl_api.py opportunities update <opportunityId> '{"stageId":"new-stage-id","status":"won"}'

# Delete opportunity
python3 {baseDir}/scripts/ghl_api.py opportunities delete <opportunityId>
```

### 对话记录（短信、电子邮件、WhatsApp）
```bash
# List recent conversations
python3 {baseDir}/scripts/ghl_api.py conversations list

# Get conversation messages
python3 {baseDir}/scripts/ghl_api.py conversations get <conversationId>

# Send SMS
python3 {baseDir}/scripts/ghl_api.py conversations send-sms <contactId> "Hello! Following up on our call."

# Send email
python3 {baseDir}/scripts/ghl_api.py conversations send-email <contactId> '{"subject":"Follow Up","body":"<p>Hi there!</p>","emailFrom":"you@domain.com"}'
```

### 日历与预约
```bash
# List calendars
python3 {baseDir}/scripts/ghl_api.py calendars list

# Get free slots
python3 {baseDir}/scripts/ghl_api.py calendars slots <calendarId> --start 2026-02-16 --end 2026-02-17

# Create appointment
python3 {baseDir}/scripts/ghl_api.py appointments create '{"calendarId":"...","contactId":"...","startTime":"2026-02-16T10:00:00Z","endTime":"2026-02-16T10:30:00Z","title":"Discovery Call"}'

# List appointments
python3 {baseDir}/scripts/ghl_api.py appointments list <calendarId>

# Update appointment
python3 {baseDir}/scripts/ghl_api.py appointments update <appointmentId> '{"status":"confirmed"}'

# Delete appointment
python3 {baseDir}/scripts/ghl_api.py appointments delete <appointmentId>
```

### 工作流程
```bash
# Add contact to workflow
python3 {baseDir}/scripts/ghl_api.py workflows add-contact <workflowId> <contactId>

# Remove contact from workflow  
python3 {baseDir}/scripts/ghl_api.py workflows remove-contact <workflowId> <contactId>
```

## 主要 API 端点参考

| 资源 | 方法 | 端点          |
|--------|--------------|--------------|
| 搜索联系人 | GET | `/contacts/search?query=...&locationId=...` |
| 获取联系人信息 | GET | `/contacts/{id}` |
| 创建联系人 | POST | `/contacts/` |
| 更新联系人信息 | PUT | `/contacts/{id}` |
| 查看销售流程 | GET | `/opportunities/pipelines?locationId=...` |
| 查看销售机会 | GET | `/opportunities/search?location_id=...&pipeline_id=...` |
| 创建销售机会 | POST | `/opportunities/` |
| 查看对话记录 | GET | `/conversations/search?locationId=...` |
| 发送消息 | POST | `/conversations/messages` |
| 查看日历 | GET | `/calendars/?locationId=...` |
| 查找可用时间 | GET | `/calendars/{id}/free-slots?startDate=...&endDate=...` |
| 预约事件 | POST | `/calendars/events/appointments` |

## 速率限制

GHL API v2 实施了以下速率限制：
- **通用请求：** 每个地点每 10 秒最多 100 次请求。
- **批量操作：** 每 10 秒最多 10 次请求。
- 如果遇到 429 错误，脚本会自动重试，采用指数级退避策略（最多重试 3 次）。

## 集成模式

### 招揽线索 → 销售流程
1. 通过表单或聊天机器人捕获线索。
2. 使用捕获到的线索数据创建联系人（`contacts create`）。
3. 为该线索创建销售机会（`opportunities create`）。
4. 通过工作流程触发后续跟进操作（`workflows add-contact`）。

### 预约流程
1. 查看日历以选择合适的日期和时间（`calendars list`）。
2. 获取日历的可用时间（`calendars slots`）。
3. 预约事件（`appointments create`）。
4. GHL 会通过配置的工作流程自动发送确认通知。

### 自动跟进
1. 查找未回复的对话记录（`conversations list`）。
2. 获取相关联系人信息（`contacts get`）。
3. 使用人工智能生成跟进内容。
4. 通过短信或电子邮件发送跟进消息（`conversations send-sms` 或 `send-email`）。

## 开发者信息

本方案由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。
更多相关信息请访问 [YouTube](https://youtube.com/@aiwithabidi) 和 [GitHub](https://github.com/aiwithabidi)。
本方案属于 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)