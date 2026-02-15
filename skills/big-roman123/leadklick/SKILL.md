# Lead Inbox Automator

该工具能够将潜在客户信息自动捕获并存储到中央化的 Supabase 数据库中，并通过 Make.com 实现自动发送电子邮件回复。

## 描述

此功能为 Clawd 代理提供了一个完整的潜在客户管理系统。它将潜在客户信息保存在 Supabase 中，触发 Make.com 的 Webhook 以自动发送回复邮件，并跟踪潜在客户从“新客户”到“已转化”状态的整个对话流程。

## 配置

```json
{
  "supabaseUrl": "https://your-project.supabase.co",
  "supabaseKey": "eyJ...your-service-role-key",
  "orgId": "550e8400-e29b-41d4-a716-446655440000",
  "defaultPriority": "medium"
}
```

**重要提示：** 请使用“Service Role Key”而非“Anon Key”以获取完整的数据库访问权限。

## 功能操作

### createLead

创建一个新的潜在客户记录，并自动触发自动化工作流程。

**参数：**
- `email` (字符串，必填)：联系人的电子邮件地址
- `name` (字符串，可选)：联系人姓名
- `phone` (字符串，可选)：电话号码
- `source` (字符串，可选)：信息来源渠道（默认值：`clawd_agent`）
- `priority` (字符串，可选)：优先级（“low”、“medium”、“high”、“urgent”）
- `custom_fields` (对象，可选)：其他附加信息

**返回值：**
```json
{
  "success": true,
  "lead_id": "uuid",
  "status": "new",
  "automation_triggered": true,
  "message": "Lead captured. Auto-reply will be sent within 60 seconds."
}
```

**示例：**
```typescript
const result = await skill.createLead({
  email: "customer@example.com",
  name: "Max Mustermann",
  source: "chat_bot",
  custom_fields: { product: "saas_basic" }
});
```

### getLead

检索潜在客户详细信息，包括完整的对话记录。

**参数：**
- `id` (字符串，必填)：潜在客户的 UUID

**返回值：** 包含 `conversations` 数组和 `reply_pending` 布尔值的潜在客户对象。

### listLeads

列出潜在客户列表，并提供过滤选项。

**参数：**
- `status` (字符串，可选)：按状态过滤
- `priority` (字符串，可选)：按优先级过滤
- `limit` (数字，可选)：最大返回结果数量（默认值：50）
- `dateFrom` (字符串，可选)：ISO 日期格式的过滤条件

**返回值：** 潜在客户列表及总记录数。

### updateStatus

更新潜在客户的生命周期状态。

**参数：**
- `id` (字符串，必填)：潜在客户的 UUID
- `status` (字符串，必填)：状态（如“qualified”、“won”、“lost”等）
- `notes` (字符串，可选)：转化备注

### addConversation

向潜在客户的对话记录中添加手动回复或备注。

**参数：**
- `leadId` (字符串，必填)：潜在客户的 UUID
- `content` (字符串，必填)：回复内容
- `subject` (字符串，可选)：回复主题

### getAutomationStatus

检查自动回复邮件是否已成功发送。

**参数：**
- `leadId` (字符串，必填)：潜在客户的 UUID

**返回值：**
```json
{
  "auto_reply_sent": true,
  "minutes_since_creation": 2,
  "automation_ok": true
}
```

## 使用流程

1. **捕获潜在客户信息：** 当用户表现出兴趣时，调用 `createLead()`。
2. **确认回复：** 60-120 秒后，调用 `getAutomationStatus()` 以确认自动回复是否已发送。
3. **转化潜在客户：** 在对话过程中，若用户表示感兴趣，将状态更新为“qualified”。
4. **记录对话：** 使用 `addConversation()` 存储代理的回复内容。

## 错误处理**

常见错误：
- 电子邮件格式无效
- 24 小时内存在重复的潜在客户记录
- 未提供 Supabase 访问凭证
- 自动化流程超时（超过 5 分钟未收到回复）

## 数据结构

**Leads 表：**
- id, email, name, phone, source, status, priority
- custom_fields (JSON), metadata (JSON)
- first_reply_sent_at, created_at

**Conversations 表：**
- id, lead_id, direction (inbound/outbound/automated)
- content, subject, channel, sent_at

## 标签**

lead, crm, sales, automation, email, supabase

## 版本**

1.0.0