---
name: moltflow
description: "WhatsApp Business自动化API，支持会话管理、消息发送、群组管理、联系人标记以及Webhook功能。适用场景包括：发送消息、创建会话、生成二维码、监控群组动态、为联系人添加标签以及设置Webhook触发事件。"
source: "MoltFlow Team"
version: "2.1.0"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---

**MoltFlow**——专为团队设计的WhatsApp Business自动化工具。支持大规模连接、监控和自动化管理WhatsApp消息。

**重要通知：**  
由于需求量大以及近期注册问题，我们特别推出了一项限时优惠：顶级商务计划（包含无限发送量），每月仅需19.90美元（按年计费）。[立即购买](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)！  
同时，我们也提供免费试用计划。[立即注册](https://molt.waiflow.app/checkout?plan=free)。

# MoltFlow核心API  
用于管理WhatsApp会话、发送消息、监控群组、使用标签进行分类，并通过Webhook接收实时事件。

## 使用场景  
- 连接WhatsApp账户  
- 发送WhatsApp消息  
- 监控WhatsApp群组  
- 给联系人添加标签  
- 设置Webhook以接收事件通知  
- 生成二维码  
- 查看聊天记录  

## 前提条件  
1. **MOLTFLOW_API_KEY**：需从[MoltFlow控制台](https://molt.waiflow.app)的“设置”>“API密钥”中生成。  
2. 所有请求均需通过`Authorization: Bearer <token>`或`X-API-Key: <key>`进行身份验证。  
3. 基本URL：`https://apiv2.waiflow.app/api/v2`  

## 必需的API权限  
| 权限范围 | 可操作内容 |  
|-------|--------|  
| `sessions` | 读取/管理会话信息 |  
| `messages` | 读取/发送消息 |  
| `groups` | 读取/管理群组信息 |  
| `labels` | 读取/管理标签信息 |  
| `webhooks` | 读取/管理Webhook配置 |  

> **聊天记录访问**：  
读取聊天记录需用户明确授权（在“设置”>“账户”>“数据访问”中启用）。  
发送消息无需授权，仅读取聊天记录时需要授权。  

## 身份验证  
所有请求必须包含以下认证信息之一：  
```
Authorization: Bearer <jwt_token>
```  
或  
```
X-API-Key: <your_api_key>
```  

---

## 会话管理  
每个会话代表一个通过二维码关联的WhatsApp账户。  

| 方法 | 端点 | 功能描述 |  
|--------|----------|-------------|  
| GET | `/sessions` | 列出所有会话 |  
| POST | `/sessions` | 创建新会话 |  
| GET | `/sessions/{id}` | 获取会话详情 |  
| DELETE | `/sessions/{id}` | 删除会话 |  
| POST | `/sessions/{id}/start` | 启动会话（生成二维码） |  
| POST | `/sessions/{id}/stop` | 停止会话 |  
| POST | `/sessions/{id}/restart` | 重新启动会话 |  
| POST | `/sessions/{id}/logout` | 登出并清除认证状态 |  
| GET | `/sessions/{id}/qr` | 获取用于配对的二维码 |  
| GET | `/sessions/{id}/events` | 获取会话事件流（Server-Sent Events） |  

### 会话状态  
会话状态会经历以下变化：`stopped` → `starting` → `qr_code` → `working` → `failed`  

### 创建会话  
**POST** `/sessions`  
**响应**：`201 Created`  

### 启动会话并获取二维码  
创建会话后，可通过以下方式启动并获取二维码：  
1. `POST /sessions/{id}/start`  
2. 等待状态变为`qr_code`（可通过监听事件或轮询获取）  
3. `GET /sessions/{id}/qr`  

### 会话事件  
`GET /sessions/{id}/events?token=<jwt>` 可获取会话事件流。事件包括状态变化、新消息和连接状态更新。  

### 会话设置  
**PATCH** `/sessions/{id}/settings`  
用于配置会话行为。设置信息保存在会话的`config` JSON字段中。  

| 字段 | 类型 | 描述 |  
|-------|------|-------------|  
| `auto_transcribe` | 布尔值 | 是否自动转录语音消息 |  

---

## 消息发送  
通过已连接的会话发送和接收WhatsApp消息。  

| 方法 | 端点 | 功能描述 |  
|--------|----------|-------------|  
| POST | `/messages/send` | 发送文本消息 |  
| POST | `/messages/send/poll` | 发送投票消息 |  
| POST | `/messages/send/sticker` | 发送贴纸 |  
| POST | `/messages/send/gif` | 发送GIF图片 |  
| GET | `/messages/chats/{session_id}` | 查看该会话的所有聊天记录 |  
| GET | `/messages/chat/{session_id}/{chat_id}` | 获取特定聊天的历史记录 |  
| GET | `/messages/{message_id}` | 获取单条消息 |  

### 发送文本消息  
**POST** `/messages/send`  
**响应**：`201 Created`  

### 聊天ID格式  
- 单个联系人：`<phone>@c.us`（例如：`5511999999999@c.us`）  
- 群组：`<group_id>@g.us`（例如：`120363012345678901@g.us`）  

### 发送投票消息  
**POST** `/messages/send/poll`  

---

## 群组管理  
监控WhatsApp群组中的关键词、消息和活动。  

| 方法 | 端点 | 功能描述 |  
|--------|----------|-------------|  
| GET | `/groups` | 列出所有被监控的群组 |  
| GET | `/groups/available/{session_id}` | 查看可监控的群组列表 |  
| POST | `/groups` | 将群组添加到监控列表 |  
| GET | `/groups/{id}` | 获取群组详情 |  
| PATCH | `/groups/{id}` | 更新监控设置 |  
| DELETE | `/groups/{id}` | 从监控列表中移除群组 |  
| POST | `/groups/create` | 创建新的WhatsApp群组 |  
| POST | `/groups/{wa_group_id}/participants/add` | 添加群组成员 |  
| POST | `/groups/{wa_group_id}/participants/remove` | 移除群组成员 |  
| POST | `/groups/{wa_group_id}/admin/promote` | 提升群组管理员权限 |  
| POST | `/groups/{wa_group_id}/admin/demote` | 降低群组管理员权限 |  

### 将群组添加到监控列表  
**POST** `/groups`  

### 监控模式  
- `all`：捕获群组中的所有消息  
- `keywords`：仅捕获包含指定关键词的消息  
- `mentions`：仅当您的账户被提及时捕获消息  
- `first_message`：仅捕获新用户的初始消息（新群组的默认设置）  

## 标签管理  
使用颜色编码的标签来分类联系人和聊天记录。支持与WhatsApp Business的标签同步。  

| 方法 | 端点 | 功能描述 |  
|--------|----------|-------------|  
| GET | `/labels` | 列出所有标签 |  
| POST | `/labels` | 创建新标签 |  
| GET | `/labels/{id}` | 获取标签详情 |  
| PATCH | `/labels/{id}` | 更新标签信息 |  
| DELETE | `/labels/{id}` | 删除标签 |  
| POST | `/labels/sync` | 将标签同步到WhatsApp |  
| POST | `/labels/sync-from-whatsapp` | 从WhatsApp导入标签 |  
| GET | `/labels/business-check` | 检查WhatsApp Business账户状态 |  
| GET | `/labels/{id}/chats` | 查看使用该标签的聊天记录 |  
| PUT | `/labels/chat/{chat_id}` | 为特定聊天设置标签 |  

### 创建标签  
**POST** `/labels`  
**响应**：`201 Created`  

> **注意：** 将标签同步到WhatsApp需要使用WhatsApp Business账户。请使用`GET /labels/business-check`进行验证。  

## Webhook  
当WhatsApp会话中发生事件时，会收到实时通知。  

| 方法 | 端点 | 功能描述 |  
|--------|----------|-------------|  
| GET | `/webhooks` | 列出所有Webhook配置 |  
| POST | `/webhooks` | 创建新的Webhook |  
| GET | `/webhooks/{id}` | 获取Webhook详情 |  
| PATCH | `/webhooks/{id}` | 更新Webhook配置 |  
| DELETE | `/webhooks/{id}` | 删除Webhook |  
| POST | `/webhooks/{id}/test` | 测试Webhook功能 |  

### 支持的事件类型  
- `message.received`：收到新消息  
- `message.sent`：发送消息  
- `session.connected`：会话连接到WhatsApp  
- `session.disconnected`：会话断开连接  
- `lead.detected`：检测到新潜在客户  
- `group.message`：群组中有新消息  

### 创建Webhook  
**POST** `/webhooks`  
**安全提示：** Webhook地址会在服务器端进行验证；禁止使用私有IP、云服务端点和非HTTPS协议。仅配置您可控的Webhook地址，并设置`secret`参数用于HMAC签名验证。  
**响应**：`201 Created`  

### Webhook响应数据  
响应数据中包含`X-Webhook-Signature`头部，其中包含HMAC-SHA256签名（如果配置了`secret`参数）。请验证该签名以确保请求的真实性。  

---

## 示例  
- **完整工作流程：** 创建会话并发送第一条消息  
- **为新消息设置Webhook通知**  
- **监控群组中的特定关键词**  

---

## 错误响应  
所有API请求都会返回标准错误代码：  
```json
{
  "detail": "Session not found"
}
```  
| 状态码 | 错误原因 |  
|--------|---------|  
| 400 | 请求无效 |  
| 401 | 未经授权 |  
| 403 | 访问受限（超出计划限制或权限问题） |  
| 404 | 资源未找到 |  
| 429 | 请求频率过高 |  
| 500 | 服务器内部错误 |  

## 请求频率限制  
API请求受到每个用户的频率限制。不同套餐的请求限制如下：  
| 计划类型 | 每分钟请求次数 |  
|------|-------------|  
| 免费 | 10次 |  
| 初级 | 20次 |  
| 专业 | 40次 |  
| 商务 | 60次 |  
请求限制信息包含在响应中的`X-RateLimit-Remaining`和`X-RateLimit-Reset`字段中。  

## 相关服务  
- **moltflow-outreach**：批量发送消息、定时发送、自定义群组管理  
- **moltflow-leads**：潜在客户检测、流程跟踪、批量操作、CSV/JSON数据导出  
- **moltflow-ai**：基于AI的自动回复、语音转录、知识库管理  
- **moltflow-a2a**：代理间通信协议、加密消息传输  
- **moltflow-reviews**：评论收集与评价管理  
- **moltflow-admin**：平台管理、用户管理、计划配置