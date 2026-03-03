---
name: moltflow
description: "WhatsApp Business自动化API，支持会话管理、消息发送、群组管理、联系人标签设置以及Webhook功能。适用场景包括：发送消息、创建会话、生成二维码、监控群组活动、为联系人添加标签以及设置Webhook触发器。"
source: "MoltFlow Team"
version: "2.16.1"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow**——专为团队打造的WhatsApp Business自动化工具。支持大规模连接、监控和自动化管理WhatsApp消息。

**由于需求旺盛以及近期注册问题，我们特推出顶级商务计划：每月仅需19.90美元（按年计费），并提供无限使用额度——此优惠仅限限时期间。** [**立即抢购**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
**也提供免费试用计划。** [**立即注册**](https://molt.waiflow.app/checkout?plan=free)

# MoltFlow核心API

通过该API，您可以管理WhatsApp会话、发送消息、监控群组、使用标签进行分类，并通过Webhook接收实时事件。

## 实际应用场景

**牙科诊所**：患者预约后发送确认通知，并在就诊前24小时发送提醒。  
**物业经理**：监控租户的WhatsApp群组，及时发现“漏水”、“损坏”等需要维修的关键词并标记出来。  
**电子商务商店**：当客户联系客服时，自动将聊天标记为“新咨询”并转接给相应团队。  
**物流公司**：设置Webhook，以便在司机发送送货确认照片时立即收到通知。

## 使用场景

- **连接WhatsApp**或**创建会话**  
- **发送WhatsApp消息**  
- **监控WhatsApp群组**  
- **为联系人添加标签**  
- **设置Webhook**  
- **获取二维码**  
- **列出聊天记录**  

## 前提条件

1. **MOLTFLOW_API_KEY**：请从[MoltFlow控制台](https://molt.waiflow.app)的“设置”>“API密钥”中生成。  
2. 所有请求都需要通过`Authorization: Bearer <token>`或`X-API-Key: <key>`进行身份验证。  
3. 基本URL：`https://apiv2.waiflow.app/api/v2`  

## 所需API权限范围

| 权限范围 | 操作内容 |
|---------|-----------|
| `sessions` | 读取/管理会话信息 |
| `messages` | 读取/发送消息 |
| `groups` | 读取/管理群组信息 |
| `labels` | 读取/管理标签信息 |
| `webhooks` | 读取/管理Webhook信息 |

## 身份验证

每个请求都必须包含以下之一：  
```
Authorization: Bearer <jwt_token>
```  
或  
```
X-API-Key: <your_api_key>
```  

---

## 会话管理

会话代表通过二维码关联的WhatsApp账户。  

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
| GET | `/sessions/{id}/events` | 获取会话事件的流式数据（Server-Sent Events, SSE） |

### 会话状态

会话的状态会经历：`stopped` -> `starting` -> `qr_code` -> `working` -> `failed`  

### 创建会话

**POST** `/sessions`  

**响应** `201 Created`：  

### 启动会话并获取二维码

创建会话后，需要启动会话并获取二维码：  
1. `POST /sessions/{id}/start` —— 启动会话  
2. 等待状态变为`qr_code`（可以使用SSE事件或轮询方式）  
3. `GET /sessions/{id}/qr` —— 获取二维码图像  

### Server-Sent Events (SSE)

`GET /sessions/{id}/events?token=<jwt>` 可获取服务器发送的事件流。事件包括会话状态变化、收到的消息和连接更新。  

### 会话设置

**PATCH** `/sessions/{id}/settings`  

配置会话的特定行为。设置信息存储在会话的`config` JSON字段中。  

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

通过已连接的会话发送和检索WhatsApp消息。  

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| POST | `/messages/send` | 发送文本消息 |
| POST | `/messages/send/poll` | 发送投票消息 |
| POST | `/messages/send/sticker` | 发送贴纸 |
| POST | `/messages/send/gif` | 发送GIF图片 |
| GET | `/messages/chats/{session_id}` | 列出该会话的所有聊天记录 |
| GET | `/messages/chat/{session_id}/{chat_id}` | 获取特定聊天的消息 |
| GET | `/messages/{message_id}` | 获取单条消息 |

### 发送文本消息

**POST** `/messages/send`  

**响应** `201 Created`：  

### 聊天ID格式

- 单个联系人：`<phone>@c.us`（例如：`5511999999999@c.us`）  
- 群组：`<group_id>@g.us`（例如：`120363012345678901@g.us`）  

### 发送投票消息

**POST** `/messages/send/poll`  

---

## 群组管理

监控WhatsApp群组中的关键词、消息和活动。  

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| GET | `/groups` | 列出所有被监控的群组 |
| GET | `/groups/available/{session_id}` | 列出可使用的WhatsApp群组 |
| POST | `/groups` | 将群组添加到监控列表 |
| GET | `/groups/{id}` | 获取被监控群组的详细信息 |
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
- `ai_analysis`：基于AI的意图分析和潜在客户评分（仅限Pro+计划）  

### 群组消息（AI分析）

**GET** `/groups/{group_id}/messages`  

获取被监控群组的消息（分页显示），包含AI分析结果。  
查询参数：`limit`（默认50条，最多100条），`offset`（默认0）  
**需要权限范围：** `groups:read`  

**注：** 如果AI尚未处理消息或未启用AI监控，`ai_analysis`字段将为`null`。  

### MCP工具：moltflow_get_group_messages

通过Claude或任何MCP客户端获取被监控WhatsApp群组的消息。  
**参数：**  
- `group_id`（必填）：被监控群组的UUID  
- `limit`（可选）：最多获取1-100条消息（默认50条）  
- `offset`（可选）：分页跳过条数（默认0）  
- `response_format`（可选）：`"markdown"`或`"json"`  
**返回值：** 分页显示的消息列表，包含发送者信息、内容预览、时间戳以及AI分析结果（如意图、潜在客户评分、置信度、原因）。  
**需要权限范围：** `groups:read`  

---

## 标签管理

使用彩色标签对联系人和聊天记录进行分类。支持与WhatsApp Business的标签同步。  

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| GET | `/labels` | 列出所有标签 |
| POST | `/labels` | 创建标签 |
| GET | `/labels/{id}` | 获取标签详情 |
| PATCH | `/labels/{id}` | 更新标签 |
| DELETE | `/labels/{id}` | 删除标签 |
| POST | `/labels/sync` | 将标签同步到WhatsApp |
| POST | `/labels/sync-from-whatsapp` | 从WhatsApp导入标签 |
| GET | `/labels/business-check` | 检查WhatsApp Business账户的状态 |
| GET | `/labels/{id}/chats` | 列出带有该标签的聊天记录 |
| PUT | `/labels/chat/{chat_id}` | 为特定聊天设置标签 |

### 创建标签

**POST** `/labels`  

**响应** `201 Created`：  

**注意：** 将标签同步到WhatsApp需要一个WhatsApp Business账户。使用`GET /labels/business-check`进行验证。  

---

## Webhook

在WhatsApp会话中发生事件时接收实时通知。  

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| GET | `/webhooks` | 列出所有Webhook |
| POST | `/webhooks` | 创建Webhook |
| GET | `/webhooks/{id}` | 获取Webhook详情 |
| PATCH | `/webhooks/{id}` | 更新Webhook设置 |
| DELETE | `/webhooks/{id}` | 删除Webhook |
| POST | `/webhooks/{id}/test` | 发送测试通知 |

### 支持的事件类型

| 事件类型 | 描述 |
|--------|-------------|
| `message.received` | 收到新消息 |
| `message.sent` | 发出消息 |
| `session.connected` | 会话连接到WhatsApp |
| `session.disconnected` | 会话断开连接 |
| `lead.detected` | 检测到潜在客户（包含AI分析结果） |
| `group.message` | 被监控群组中的消息 |
| `group.message.analyzed` | 群组消息的AI分析完成（仅限Pro/Business计划） |

### 创建Webhook

**POST** `/webhooks`  

**安全提示：** Webhook地址会在服务器端进行验证——禁止使用私有IP、云元数据端点和非HTTPS协议。仅配置您能够控制的端点。务必设置`secret`字段以进行HMAC签名验证。  
**响应** `201 Created`：  

### Webhook数据格式

Webhook响应中包含`X-Webhook-Signature`头部，其中包含HMAC-SHA256签名（如果配置了`secret`字段）。请验证该签名以确保请求的真实性。  

---

## 示例

- **完整工作流程：创建会话并发送第一条消息**  
- **为收到的消息设置Webhook**  
- **监控群组中的关键词**  

---

## 错误响应

所有API请求都会返回标准错误代码：  

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求无效 |
| 401 | 未经授权（缺少或无效的认证信息） |
| 403 | 被禁止（超出计划使用限制或权限问题） |
| 404 | 资源未找到 |
| 429 | 请求频率超出限制 |
| 500 | 服务器内部错误 |

## 请求频率限制

每个租户的API请求频率是有限制的。不同计划对应的限制如下：  
| 计划类型 | 每分钟请求次数 |
|------|-------------|
| 免费 | 10次 |
| 起始计划 | 20次 |
| Pro计划 | 40次 |
| Business计划 | 60次 |

请求频率限制信息包含在每个响应中：`X-RateLimit-Remaining`、`X-RateLimit-Reset`  

## 相关服务

- **moltflow-outreach**：批量发送消息、定时发送消息、自定义群组管理  
- **moltflow-leads**：潜在客户检测、流程跟踪、批量操作、CSV/JSON导出  
- **moltflow-ai**：基于AI的自动回复、语音转录、知识库管理  
- **moltflow-a2a**：代理间通信协议、加密消息传输、内容策略管理  
- **moltflow-reviews**：评论收集和评价管理  
- **moltflow-admin**：平台管理、用户管理、计划配置