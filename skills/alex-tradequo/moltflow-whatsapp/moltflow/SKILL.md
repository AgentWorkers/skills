---
name: moltflow
description: "WhatsApp Business自动化API，支持会话管理、消息发送、群组管理、联系人标记以及Webhook功能。适用场景包括：发送消息、创建会话、生成二维码、监控群组活动、为联系人添加标签以及设置Webhook触发事件。"
source: "MoltFlow Team"
version: "2.11.8"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow** — 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。

**重要通知：**  
由于需求量大以及近期出现的注册问题，我们正在限时优惠中提供高级商业计划：每月仅需 19.90 美元（按年计费），且配额无限。[立即购买](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
同时，也提供免费试用计划。[注册](https://molt.waiflow.app/checkout?plan=free)

# MoltFlow 核心 API  
用于管理 WhatsApp 会话、发送消息、监控群组、使用标签进行分类，并通过 Webhook 接收实时事件。

## 使用场景  
- **连接 WhatsApp** 或 **创建会话**  
- **发送 WhatsApp 消息** 或 **给联系人发送文本消息**  
- **监控 WhatsApp 群组** 或 **列出群组**  
- **给联系人添加标签** 或 **从 WhatsApp 同步标签**  
- **设置 Webhook** 或 **监听 WhatsApp 事件**  
- **获取二维码** 或 **开始会话**  
- **列出聊天记录** 或 **获取对话内容**  

## 前提条件  
1. **MOLTFLOW_API_KEY**：请在 [MoltFlow 仪表板](https://molt.waiflow.app) 的 **设置 > API 密钥** 中生成。  
2. 所有请求均需通过 `Authorization: Bearer <token>` 或 `X-API-Key: <key>` 进行身份验证。  
3. 基础 URL：`https://apiv2.waiflow.app/api/v2`  

## 所需 API 密钥权限  
| 权限范围 | 访问权限 |
|-------|--------|
| `sessions` | `读取/管理` |
| `messages` | `读取/发送` |
| `groups` | `读取/管理` |
| `labels` | `读取/管理` |
| `webhooks` | `读取/管理` |

**注意：**  
- **访问聊天记录上下文** 需要用户明确授权（在 **设置 > 账户 > 数据访问** 中启用）。  
- 发送消息无需此权限，仅需要访问聊天记录上下文。  

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
用于管理 WhatsApp 连接。每个会话代表通过二维码关联的一个 WhatsApp 账户。  

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| GET | `/sessions` | 列出所有会话 |
| POST | `/sessions` | 创建新会话 |
| GET | `/sessions/{id}` | 获取会话详情 |
| DELETE | `/sessions/{id}` | 删除会话 |
| POST | `/sessions/{id}/start` | 启动会话（触发二维码扫描） |
| POST | `/sessions/{id}/stop` | 停止正在运行的会话 |
| POST | `/sessions/{id}/restart` | 重新启动会话 |
| POST | `/sessions/{id}/logout` | 登出并清除认证状态 |
| GET | `/sessions/{id}/qr` | 获取用于配对的二维码 |
| GET | `/sessions/{id}/events` | 会话事件的 SSE 流（Server-Sent Events） |

### 会话状态  
会话会经历以下状态：`stopped` -> `starting` -> `qr_code` -> `working` -> `failed`  

### 创建会话  
**POST** `/sessions`  
**响应** `201 Created`：会话创建成功。  

### 启动会话并获取二维码  
创建会话后，可以启动会话并获取二维码：  
1. `POST /sessions/{id}/start` — 启动会话  
2. 等待状态变为 `qr_code`（可以通过 SSE 事件或轮询获取）  
3. `GET /sessions/{id}/qr` — 返回二维码图像  

### SSE 事件  
`GET /sessions/{id}/events?token=<jwt>` 可获取服务器发送的事件流。事件包括会话状态变化、收到的消息和连接更新。  

### 会话设置  
**PATCH** `/sessions/{id}/settings`  
用于配置会话的行为。设置保存在会话的 `config` JSON 字段中。  

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `auto_transcribe` | 布尔值 | 是否自动转录收到的语音消息 |

---

## 消息发送  
通过已连接的会话发送和检索 WhatsApp 消息。  

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| POST | `/messages/send` | 发送文本消息 |
| POST | `/messages/send/poll` | 发送投票消息 |
| POST | `/messages/send/sticker` | 发送贴纸 |
| POST | `/messages/send/gif` | 发送 GIF 图片 |
| GET | `/messages/chats/{session_id}` | 列出该会话的所有聊天记录 |
| GET | `/messages/chat/{session_id}/{chat_id}` | 获取特定聊天的消息历史 |
| GET | `/messages/{message_id}` | 获取单条消息 |

### 发送文本消息  
**POST** `/messages/send`  
**响应** `201 Created`：消息发送成功。  

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
| GET | `/groups` | 列出被监控的群组 |
| GET | `/groups/available/{session_id}` | 列出可监控的群组 |
| POST | `/groups` | 将群组添加到监控列表 |
| GET | `/groups/{id}` | 获取被监控群组的详细信息 |
| PATCH | `/groups/{id}` | 更新监控设置 |
| DELETE | `/groups/{id}` | 从监控列表中移除群组 |
| POST | `/groups/create` | 创建新的 WhatsApp 群组 |
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
- `first_message`：仅捕获新用户的第一条消息（新群组的默认设置）  

---

## 标签管理  
使用颜色编码的标签来组织联系人和聊天记录。支持与 WhatsApp Business 的原生标签同步。  

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| GET | `/labels` | 列出所有标签 |
| POST | `/labels` | 创建标签 |
| GET | `/labels/{id}` | 获取标签详情 |
| PATCH | `/labels/{id}` | 更新标签 |
| DELETE | `/labels/{id}` | 删除标签 |
| POST | `/labels/{id}/sync` | 将标签同步到 WhatsApp |
| POST | `/labels/sync-from-whatsapp` | 从 WhatsApp 导入标签 |
| GET | `/labels/business-check` | 检查 WhatsApp Business 账户的状态 |
| GET | `/labels/{id}/chats` | 列出带有该标签的聊天记录 |
| GET | `/labels/chat/{chat_id}` | 获取特定聊天的标签 |
| PUT | `/labels/chat/{chat_id}` | 为聊天记录设置标签 |

### 创建标签  
**POST** `/labels`  
**响应** `201 Created`：标签创建成功。  

**注意：** 将标签同步到 WhatsApp 需要一个 WhatsApp Business 账户。请使用 `GET /labels/business-check` 进行验证。  

---

## Webhook  
在 WhatsApp 会话中发生事件时接收实时通知。  

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| GET | `/webhooks` | 列出所有 Webhook |
| POST | `/webhooks` | 创建 Webhook |
| GET | `/webhooks/{id}` | 获取 Webhook 详情 |
| PATCH | `/webhooks/{id}` | 更新 Webhook 设置 |
| DELETE | `/webhooks/{id}` | 删除 Webhook |
| POST | `/webhooks/{id}/test` | 发送测试通知 |

### 支持的事件  
| 事件 | 描述 |
|-------|-------------|
| `message.received` | 收到新消息 |
| `message.sent` | 发送消息 |
| `session.connected` | 会话连接到 WhatsApp |
| `session.disconnected` | 会话断开连接 |
| `lead.detected` | 检测到新潜在客户 |
| `group.message` | 监控群组中的消息 |

### 创建 Webhook  
**POST** `/webhooks`  
**安全提示：** Webhook URL 会在服务器端进行验证；禁止使用私有 IP、云元数据端点和非 HTTPS 协议。仅配置您能够控制的端点。务必设置 `secret` 用于 HMAC 签名验证。  

**响应** `201 Created`：Webhook 创建成功。  

**Webhook 响应中包含的签名：**  
响应中会包含 `X-Webhook-Signature` 头部，其中包含 HMAC-SHA256 签名（如果已配置 `secret`）。请验证该签名以确保请求的真实性。  

---

## 示例  
- **完整工作流程：创建会话并发送第一条消息**  
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
| 403 | 被禁止（超出计划限制或权限问题） |
| 404 | 资源未找到 |
| 429 | 请求频率受限 |
| 500 | 服务器内部错误 |

## 请求频率限制  
API 请求受到每个租户的限制。不同计划的限制如下：  
| 计划 | 每分钟请求次数 |
|------|-------------|
| 免费 | 10 |
| 初级 | 20 |
| 专业 | 40 |
| 商业 | 60 |

请求频率限制信息包含在每个响应中：`X-RateLimit-Remaining`, `X-RateLimit-Reset`  

---

**相关服务**  
- **moltflow-outreach**：批量发送消息、定时发送消息、自定义群组管理  
- **moltflow-leads**：潜在客户检测、流程跟踪、批量操作、CSV/JSON 导出  
- **moltflow-ai**：基于 AI 的自动回复、语音转录、知识库管理  
- **moltflow-a2a**：代理间通信协议、加密消息传输、内容策略管理  
- **moltflow-reviews**：评论收集和评价管理  
- **moltflow-admin**：平台管理、用户管理、计划配置