---
name: moltflow
description: "WhatsApp Business自动化API，支持会话管理、消息发送、群组管理、联系人标记以及Webhook功能。适用场景包括：发送消息、创建会话、生成二维码、监控群组动态、为联系人添加标签以及设置Webhook触发器。"
source: "MoltFlow Team"
version: "2.0.0"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---

> **MoltFlow** – 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。  
> [年费订阅可节省高达 17% 的费用](https://molt.waiflow.app/checkout?plan=free)；提供免费试用计划，无需信用卡。  

# MoltFlow 核心 API  

用于管理 WhatsApp 会话、发送消息、监控群组、使用标签进行分类，并通过 Webhook 接收实时事件。  

## 使用场景  

- 连接 WhatsApp 或创建新会话  
- 向联系人发送文本消息  
- 监控 WhatsApp 群组  
- 为联系人添加标签  
- 设置 Webhook 以接收 WhatsApp 事件  
- 生成 QR 码  
- 查看聊天记录  

## 前提条件  

1. **MOLTFLOW_API_KEY**：在 [MoltFlow 控制台](https://molt.waiflow.app) 的“设置”>“API 密钥”中生成。  
2. 所有请求都需要通过 `Authorization: Bearer <token>` 或 `X-API-Key: <key>` 进行身份验证。  
3. 基本 URL：`https://apiv2.waiflow.app/api/v2`  

## 身份验证  

每个请求都必须包含以下身份验证信息之一：  
```
Authorization: Bearer <jwt_token>
```  
或  
```
X-API-Key: <your_api_key>
```  

---

## 会话管理  

会话表示通过 QR 码关联的 WhatsApp 账户。  

| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| GET | `/sessions` | 查看所有会话 |  
| POST | `/sessions` | 创建新会话 |  
| GET | `/sessions/{id}` | 获取会话详情 |  
| DELETE | `/sessions/{id}` | 删除会话 |  
| POST | `/sessions/{id}/start` | 启动会话（触发 QR 码扫描） |  
| POST | `/sessions/{id}/stop` | 停止正在运行的会话 |  
| POST | `/sessions/{id}/restart` | 重新启动会话 |  
| POST | `/sessions/{id}/logout` | 登出并清除认证状态 |  
| GET | `/sessions/{id}/qr` | 获取用于配对的 QR 码 |  
| GET | `/sessions/{id}/events` | 获取会话事件的流式数据（SSE） |  

### 会话状态  

会话的状态变化顺序为：`stopped` -> `starting` -> `qr_code` -> `working` -> `failed`  

### 创建会话  

**POST** `/sessions`  

```json
{
  "name": "My WhatsApp"
}
```  

**响应** `201 Created`：会话创建成功。  

### 启动会话并获取 QR 码  

创建会话后，需要启动会话并获取其 QR 码：  
1. `POST /sessions/{id}/start` – 启动会话  
2. 等待状态变为 `qr_code`（可以通过 SSE 事件或轮询获取）  
3. `GET /sessions/{id}/qr` – 获取 QR 码图像  

### 会话事件（SSE）  

`GET /sessions/{id}/events?token=<jwt>` 可获取服务器发送的事件流。事件包括会话状态变化、收到的消息和连接更新。  

### 会话设置  

**PATCH** `/sessions/{id}/settings`  

配置会话的特定行为。设置信息存储在会话的 `config` JSON 字段中。  

```json
// Request
{
  "auto_transcribe": true
}

// Response
{
  "status": "ok",
  "config": {
    "auto_transcribe": true
  }
}
```  

| 字段 | 类型 | 描述 |  
|-------|------|-------------|  
| `auto_transcribe` | boolean | 自动转录收到的语音消息 |  

---

## 消息发送与接收  

通过已连接的会话发送和接收 WhatsApp 消息。  

| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| POST | `/messages/send` | 发送文本消息 |  
| POST | `/messages/send/poll` | 发送投票消息 |  
| POST | `/messages/send/sticker` | 发送贴纸 |  
| POST | `/messages/send/gif` | 发送 GIF 图片 |  
| GET | `/messages/chats/{session_id}` | 查看会话中的所有聊天记录 |  
| GET | `/messages/chat/{session_id}/{chat_id}` | 获取特定聊天的消息历史 |  
| GET | `/messages/{message_id}` | 获取单条消息 |  

### 发送文本消息  

**POST** `/messages/send`  

```json
{
  "session_id": "a1b2c3d4-...",
  "chat_id": "5511999999999@c.us",
  "message": "Hello from MoltFlow!"
}
```  

**响应** `201 Created`：消息发送成功。  

### 聊天 ID 格式  

- 单个联系人：`<phone>@c.us`（例如：`5511999999999@c.us`）  
- 群组：`<group_id>@g.us`（例如：`120363012345678901@g.us`）  

### 发送投票消息  

**POST** `/messages/send/poll`  

```json
{
  "session_id": "a1b2c3d4-...",
  "chat_id": "5511999999999@c.us",
  "title": "Preferred meeting time?",
  "options": ["Morning", "Afternoon", "Evening"],
  "allow_multiple": false
}
```  

---

## 群组管理  

监控 WhatsApp 群组中的关键词、消息和活动。  

| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| GET | `/groups` | 查看所有被监控的群组 |  
| GET | `/groups/available/{session_id}` | 查看可监控的群组 |  
| POST | `/groups` | 将群组添加到监控列表 |  
| GET | `/groups/{id}` | 获取群组详情 |  
| PATCH | `/groups/{id}` | 更新监控设置 |  
| DELETE | `/groups/{id}` | 从监控列表中移除群组 |  
| POST | `/groups/create` | 创建新的 WhatsApp 群组 |  
| POST | `/groups/{wa_group_id}/participants/add` | 添加群组成员 |  
| POST | `/groups/{wa_group_id}/participants/remove` | 移除群组成员 |  
| POST | `/groups/{wa_group_id}/admin/promote` | 提升群组管理员权限 |  
| POST | `/groups/{wa_group_id}/admin/demote` | 降低群组管理员权限 |  

### 将群组添加到监控列表  

**POST** `/groups`  

---  

## 监控模式  

- `all`：捕获群组中的所有消息  
- `keywords`：仅捕获包含指定关键词的消息  
- `mentions`：仅当您的账户被提及时捕获消息  
- `first_message`：仅捕获新用户的初始消息（新群组的默认设置）  

---

## 标签管理  

使用彩色标签对联系人和聊天记录进行分类。支持与 WhatsApp Business 的原生标签同步。  

| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| GET | `/labels` | 查看所有标签 |  
| POST | `/labels` | 创建新标签 |  
| GET | `/labels/{id}` | 获取标签详情 |  
| PATCH | `/labels/{id}` | 更新标签 |  
| DELETE | `/labels/{id}` | 删除标签 |  
| POST | `/labels/{id}/sync` | 将标签同步到 WhatsApp |  
| POST | `/labels/sync-from-whatsapp` | 从 WhatsApp 导入标签 |  
| GET | `/labels/business-check` | 检查 WhatsApp Business 账户的状态 |  
| GET | `/labels/{id}/chats` | 查看带有该标签的聊天记录 |  
| PUT | `/labels/chat/{chat_id}` | 为聊天记录设置标签 |  

### 创建标签  

**POST** `/labels`  

```json
{
  "name": "VIP Customer",
  "color": "#FF6B35",
  "description": "High-value accounts"
}
```  

**响应** `201 Created`：标签创建成功。  

> **注意：** 将标签同步到 WhatsApp 需要拥有 WhatsApp Business 账户。请使用 `GET /labels/business-check` 进行验证。  

---

## Webhook  

在 WhatsApp 会话中发生事件时接收实时通知。  

| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| GET | `/webhooks` | 查看所有 Webhook |  
| POST | `/webhooks` | 创建新的 Webhook |  
| GET | `/webhooks/{id}` | 获取 Webhook 详情 |  
| PATCH | `/webhooks/{id}` | 更新 Webhook 设置 |  
| DELETE | `/webhooks/{id}` | 删除 Webhook |  
| POST | `/webhooks/{id}/test` | 测试 Webhook 的发送功能 |  

### 支持的事件类型  

| 事件 | 描述 |  
|-------|-------------|  
| `message.received` | 收到新消息 |  
| `message.sent` | 发送消息 |  
| `session.connected` | 会话连接到 WhatsApp |  
| `session.disconnected` | 会话断开连接 |  
| `lead-detected` | 检测到新潜在客户 |  
| `group.message` | 监控群组中的消息 |  

### 创建 Webhook  

**POST** `/webhooks`  

```json
{
  "name": "CRM Integration",
  "url": "https://example.com/webhooks/moltflow",
  "events": ["message.received", "lead.detected"],
  "secret": "whsec_mysecretkey123"
}
```  

**响应** `201 Created`：Webhook 创建成功。  

### Webhook 数据传输  

Webhook 的响应数据中包含 `X-Webhook-Signature` 头部，其中包含 HMAC-SHA256 签名（如果配置了密钥）。请验证该签名以确保数据真实性。  

```json
{
  "event": "message.received",
  "timestamp": "2026-02-11T10:05:00Z",
  "data": {
    "session_id": "a1b2c3d4-...",
    "chat_id": "5511999999999@c.us",
    "message": "Hello!",
    "direction": "inbound"
  }
}
```  

---

## 示例  

- **完整工作流程：** 创建会话并发送第一条消息  
- **为收到的消息设置 Webhook**  
- **监控群组中的特定关键词**  

---

## 错误响应  

所有 API 端点都会返回标准错误响应：  

```json
{
  "detail": "Session not found"
}
```  

| 状态码 | 含义 |  
|--------|---------|  
| 400 | 请求无效 |  
| 401 | 未经授权（缺少或无效的认证信息） |  
| 403 | 被禁止（超出使用限制或权限问题） |  
| 404 | 资源未找到 |  
| 429 | 请求频率限制 |  
| 500 | 服务器内部错误 |  

---

## 请求频率限制  

API 请求受到每个租户的使用频率限制。不同套餐的频率限制如下：  

| 套餐 | 每分钟请求次数 |  
|------|-------------|  
| 免费 | 10 |  
| 初级 | 20 |  
| 专业 | 40 |  
| 商业 | 60 |  

每个响应中都会包含频率限制相关信息：`X-RateLimit-Remaining` 和 `X-RateLimit-Reset`。  

---

## 相关服务  

- **moltflow-outreach**：批量发送消息、定时发送消息、自定义群组管理  
- **moltflow-leads**：潜在客户检测、流程跟踪、批量操作、CSV/JSON 导出  
- **moltflow-ai**：基于 AI 的自动回复功能、语音转录、知识库管理  
- **moltflow-a2a**：代理间通信协议、加密消息传输、内容策略管理  
- **moltflow-reviews**：评论收集与评价管理  
- **moltflow-admin**：平台管理、用户管理、套餐配置