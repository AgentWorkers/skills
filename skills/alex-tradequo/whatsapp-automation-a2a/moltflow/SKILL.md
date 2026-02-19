---
name: moltflow
description: "WhatsApp Business自动化API，支持会话管理、消息发送、群组管理、联系人标签设置以及Webhook功能。适用场景包括：发送消息、创建会话、生成二维码、监控群组动态、为联系人添加标签以及设置Webhook触发事件。"
source: "MoltFlow Team"
version: "2.11.8"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow** — 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。

**由于需求量大以及近期出现的注册问题，我们特别推出了一项限时优惠：** **顶级商业计划（Business Plan）**，每月仅需 $19.90（按年计费），并提供无限使用额度。[立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)！** **同时，我们也提供免费试用计划。** [立即注册](https://molt.waiflow.app/checkout?plan=free)。

# MoltFlow 核心 API

通过该 API，您可以管理 WhatsApp 会话、发送消息、监控群组、使用标签对联系人进行分类，并通过 Webhook 接收实时事件。

## 实际应用场景

- **牙科诊所**：在患者预约后向他们发送确认通知，并在就诊前 24 小时发送提醒。
- **物业经理**：监控租户的 WhatsApp 群组，及时发现“漏水”、“损坏”或“紧急”等需要维修的线索。
- **电子商务商店**：当客户联系客服时，自动将对话标记为“新咨询”并转发给相应的团队。
- **物流公司**：设置 Webhook，以便在司机发送送货确认照片时立即收到通知。

## 使用场景

- **连接 WhatsApp** 或 **创建会话**
- **发送 WhatsApp 消息** 或 **向联系人发送文本消息**
- **监控 WhatsApp 群组** 或 **列出所有群组**
- **为联系人添加标签** 或 **从 WhatsApp 同步标签**
- **设置 Webhook** 或 **监听 WhatsApp 事件**
- **生成 QR 码** 或 **启动会话**
- **查看聊天记录** 或 **获取对话内容**

## 先决条件

1. **MOLTFLOW_API_KEY**：请在 [MoltFlow 控制台](https://molt.waiflow.app) 的“设置” > “API 密钥”中生成。
2. 所有请求都需要通过 `Authorization: Bearer <token>` 或 `X-API-Key: <key>` 进行身份验证。
3. 基本 URL：`https://apiv2.waiflow.app/api/v2`

## 必需的 API 密钥权限

| 权限范围 | 可操作内容 |
|---------|------------|
| `sessions` | 读取/管理会话信息 |
| `messages` | 读取/发送消息 |
| `groups` | 读取/管理群组信息 |
| `labels` | 读取/管理标签信息 |
| `webhooks` | 读取/管理 Webhook 设置 |

## 身份验证

所有请求都必须包含以下认证信息之一：

```
Authorization: Bearer <jwt_token>
```

或

```
X-API-Key: <your_api_key>
```

---

## 会话管理

会话用于表示通过 QR 码连接的 WhatsApp 账户。

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| GET | `/sessions` | 列出所有会话 |
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

会话会经历以下状态：`stopped` -> `starting` -> `qr_code` -> `working` -> `failed`

### 创建会话

**POST** `/sessions`

**响应**：`201 Created`（表示会话创建成功）

### 启动会话并获取 QR 码

创建会话后，可以启动会话并获取其 QR 码：

1. `POST /sessions/{id}/start` — 启动会话。
2. 等待会话状态变为 `qr_code`（可以通过 SSE 事件或轮询获取）。
3. `GET /sessions/{id}/qr` — 获取 QR 码图像。

### 会话事件

`GET /sessions/{id}/events?token=<jwt>` 可以获取服务器发送的事件流。事件包括会话状态变化、收到的消息和连接更新。

### 会话设置

**PATCH** `/sessions/{id}/settings`

可以配置每个会话的设置。这些设置存储在会话的 `config` JSON 字段中。

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
| `auto_transcribe` | 布尔值 | 是否自动转录收到的语音消息 |

---

## 消息发送

通过已连接的会话发送和接收 WhatsApp 消息。

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| POST | `/messages/send` | 发送文本消息 |
| POST | `/messages/send/poll` | 发送投票消息 |
| POST | `/messages/send/sticker` | 发送贴纸 |
| POST | `/messages/send/gif` | 发送 GIF 图片 |
| GET | `/messages/chats/{session_id}` | 列出该会话的所有聊天记录 |
| GET | `/messages/chat/{session_id}/{chat_id}` | 获取特定聊天的内容 |
| GET | `/messages/{message_id}` | 获取单条消息 |

### 发送文本消息

**POST** `/messages/send`

**响应**：`201 Created`（表示消息发送成功）

### 聊天 ID 格式

- 单个联系人：`<phone>@c.us`（例如：`5511999999999@c.us`）
- 群组：`<group_id>@g.us`（例如：`120363012345678901@g.us`）

### 发送投票消息

**POST** `/messages/send/poll`

---

## 群组管理

监控 WhatsApp 群组中的关键词、消息和活动。

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| GET | `/groups` | 列出所有被监控的群组 |
| GET | `/groups/available/{session_id}` | 查看可使用的群组 |
| POST | `/groups` | 将群组添加到监控列表 |
| GET | `/groups/{id}` | 获取群组详情 |
| PATCH | `/groups/{id}` | 更新监控设置 |
| DELETE | `/groups/{id}` | 从监控列表中移除群组 |
| POST | `/groups/create` | 创建新的 WhatsApp 群组 |
| POST | `/groups/{wa_group_id}/participants/add` | 向群组添加成员 |
| POST | `/groups/{wa_group_id}/participants/remove` | 从群组中移除成员 |
| POST | `/groups/{wa_group_id}/admin/promote` | 提升成员为管理员 |
| POST | `/groups/{wa_group_id}/admin/demote` | 降低成员的权限 |

### 将群组添加到监控列表

**POST** `/groups`

---

## 标签管理

使用颜色编码的标签对联系人及聊天记录进行分类。支持与 WhatsApp Business 的原生标签同步。

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| GET | `/labels` | 列出所有标签 |
| POST | `/labels` | 创建新标签 |
| GET | `/labels/{id}` | 获取标签详情 |
| PATCH | `/labels/{id}` | 更新标签信息 |
| DELETE | `/labels/{id}` | 删除标签 |
| POST | `/labels/sync` | 将标签同步到 WhatsApp |
| POST | `/labels/sync-from-whatsapp` | 从 WhatsApp 导入标签 |
| GET | `/labels/business-check` | 检查 WhatsApp Business 的账户状态 |
| GET | `/labels/{id}/chats` | 列出使用该标签的聊天记录 |
| PUT | `/labels/chat/{chat_id}` | 为特定聊天设置标签 |

### 创建标签

**POST** `/labels`

**响应**：`201 Created`（表示标签创建成功）

**注意：** 将标签同步到 WhatsApp 需要一个 WhatsApp Business 账户。请使用 `GET /labels/business-check` 进行验证。

---

## Webhook

当 WhatsApp 会话中发生事件时，可以接收实时通知。

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| GET | `/webhooks` | 列出所有已配置的 Webhook |
| POST | `/webhooks` | 创建新的 Webhook |
| GET | `/webhooks/{id}` | 获取 Webhook 详情 |
| PATCH | `/webhooks/{id}` | 更新 Webhook 设置 |
| DELETE | `/webhooks/{id}` | 删除 Webhook |
| POST | `/webhooks/{id}/test` | 发送测试请求 |

### 支持的事件类型

| 事件类型 | 描述 |
|--------|-------------|
| `message.received` | 收到新消息 |
| `message.sent` | 发送消息 |
| `session.connected` | 会话连接到 WhatsApp |
| `session.disconnected` | 会话断开连接 |
| `lead.detected` | 检测到新潜在客户 |
| `group.message` | 监控群组中的消息 |

### 创建 Webhook

**注意：** Webhook URL 会在服务器端进行验证。仅允许使用受控制的私有 IP 地址、云服务端点以及 HTTPS 协议。务必为 HMAC 签名配置一个安全的 `secret` 值。

**响应**：`201 Created`（表示 Webhook 创建成功）

**Webhook 的响应数据中包含 `X-Webhook-Signature` 头部，其中包含 HMAC-SHA256 签名。请验证该签名以确保请求的真实性。**

---

## 示例

- **完整工作流程：** 创建会话并发送第一条消息。
- **为收到的消息设置 Webhook。**
- **监控群组中的特定关键词。**

---

## 错误响应

所有 API 请求都会返回标准的错误代码和相应的错误信息：

| 状态码 | 错误原因 |
|--------|---------|
| 400 | 请求无效 |
| 401 | 未经授权（缺少或无效的认证信息） |
| 403 | 超过使用限制 |
| 404 | 资源未找到 |
| 429 | 请求频率超出限制 |
| 500 | 服务器内部错误 |

## 使用限制

API 请求的使用频率受到每个租户的限制。不同套餐的请求限制如下：

| 所用套餐 | 每分钟请求次数 |
|--------|-------------|
| 免费计划 | 10 次 |
| 起始计划 | 20 次 |
| 专业计划 | 40 次 |
| 商业计划 | 60 次 |

每个响应中都会包含以下速率限制相关头部信息：`X-RateLimit-Remaining` 和 `X-RateLimit-Reset`。

## 相关服务

- **moltflow-outreach**：批量发送消息、定时发送消息、自定义群组管理。
- **moltflow-leads**：潜在客户检测、流程跟踪、批量操作、CSV/JSON 数据导出。
- **moltflow-ai**：基于 AI 的自动回复功能、语音转录、知识库管理。
- **moltflow-a2a**：代理间通信协议、加密消息传输、内容策略管理。
- **moltflow-reviews**：评论收集与评价管理。
- **moltflow-admin**：平台管理、用户管理、套餐配置。