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
## MoltFlow – 为团队打造的 WhatsApp Business 自动化工具  
> **MoltFlow** 可帮助您大规模地连接、监控和自动化 WhatsApp 操作。  
> **由于需求量大以及近期注册问题，我们特推出高级商业计划：每月仅需 19.90 美元（按年计费），并提供无限使用量——此优惠仅限限时有效。** [**立即抢购**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
> **也提供免费试用计划。** [**立即注册**](https://molt.waiflow.app/checkout?plan=free)  

### MoltFlow 核心 API  
MoltFlow 提供了一套丰富的 API，用于管理 WhatsApp 会话、发送消息、监控群组、使用标签进行分类，并通过 Webhook 接收实时事件。  

#### 使用场景  
- **连接 WhatsApp** 或 **创建会话**  
- **发送 WhatsApp 消息**  
- **监控 WhatsApp 群组**  
- **为联系人添加标签**  
- **设置 Webhook**  
- **获取 QR 码**  
- **列出聊天记录**  

#### 前提条件  
1. **MOLTFLOW_API_KEY**：请从 [MoltFlow 控制台](https://molt.waiflow.app) 的“设置” > “API 密钥” 中生成。  
2. 所有请求均需通过 `Authorization: Bearer <token>` 或 `X-API-Key: <key>` 进行身份验证。  
3. 基本 URL：`https://apiv2.waiflow.app/api/v2`  

#### 必需的 API 密钥权限  
| 权限范围 | 可操作内容 |  
|---------|----------------|  
| `sessions` | 读取/管理会话信息 |  
| `messages` | 读取/发送消息 |  
| `groups` | 读取/管理群组信息 |  
| `labels` | 读取/管理标签信息 |  
| `webhooks` | 读取/管理 Webhook 配置 |  

#### 身份验证  
所有请求都必须包含以下身份验证信息之一：  
```
Authorization: Bearer <jwt_token>
```  
或  
```
X-API-Key: <your_api_key>
```  

### 会话管理  
**会话** 是通过 QR 码关联的 WhatsApp 账户的集合。  
- **方法** | **端点** | **描述**  
|-------|----------|-------------|  
| `GET` | `/sessions` | 列出所有会话 |  
| `POST` | `/sessions` | 创建新会话 |  
| `GET` | `/sessions/{id}` | 获取会话详情 |  
| `DELETE` | `/sessions/{id}` | 删除会话 |  
| `POST` | `/sessions/{id}/start` | 启动会话（触发 QR 码扫描） |  
| `POST` | `/sessions/{id}/stop` | 停止正在运行的会话 |  
| `POST` | `/sessions/{id}/restart` | 重新启动会话 |  
| `POST` | `/sessions/{id}/logout` | 登出并清除认证状态 |  
| `GET` | `/sessions/{id}/qr` | 获取用于配对的 QR 码 |  
| `GET` | `/sessions/{id}/events` | 获取会话事件的流式数据（Server-Sent Events, SSE） |  

#### 会话状态  
会话会经历以下状态：`stopped` → `starting` → `qr_code` → `working` → `failed`  

#### 创建会话  
**POST** `/sessions`  
**响应**：`201 Created`  

#### 启动会话并获取 QR 码  
创建会话后，需要启动会话并获取其 QR 码：  
1. `POST /sessions/{id}/start` – 启动会话  
2. 等待状态变为 `qr_code`（可通过 SSE 事件或轮询获取）  
3. `GET /sessions/{id}/qr` – 返回 QR 码图像  

#### 会话事件  
`GET /sessions/{id}/events?token=<jwt>` 可获取服务器发送的事件流，包括会话状态变化、收到的消息和连接更新。  

#### 会话设置  
**PATCH** `/sessions/{id}/settings`  
用于配置会话的详细行为。设置信息存储在会话的 `config` JSON 字段中。  
**示例：**  
| **字段** | **类型** | **描述** |  
|-------|------|-------------|  
| `auto_transcribe` | `boolean` | 是否自动转录语音消息 |  

#### 消息发送  
**POST** `/messages/send`  
用于发送 WhatsApp 消息：  
- **文本消息**  
- **投票消息**  
- **贴纸**  
- **GIF 动画**  
**示例：**  
**POST** `/messages/send`  
**响应**：`201 Created`  

#### 联系人 ID 格式  
- **个人联系人**：`<phone>@c.us`（例如：`5511999999999@c.us`）  
- **群组**：`<group_id>@g.us`（例如：`120363012345678901@g.us`）  

#### 监控群组  
**POST** `/groups`  
用于监控 WhatsApp 群组中的关键词、消息和活动：  
- **方法** | **端点** | **描述** |  
|-------|----------|-------------|  
| `GET` | `/groups` | 列出所有被监控的群组 |  
| `POST` | `/groups` | 将群组添加到监控列表 |  
| `GET` | `/groups/{id}` | 获取群组详情 |  
| `PATCH` | `/groups/{id}` | 更新监控设置 |  
- **示例：**  
**POST** `/groups`  

#### 标签管理  
**POST** `/labels`  
用于为联系人或聊天记录添加颜色编码的标签：  
- **方法** | **端点** | **描述** |  
|-------|----------|-------------|  
| `GET` | `/labels` | 列出所有标签 |  
| `POST` | `/labels` | 创建新标签 |  
| `GET` | `/labels/{id}` | 获取标签详情 |  
- **示例：**  
**POST** `/labels`  

#### Webhook  
用于在 WhatsApp 会话中发生事件时接收实时通知：  
- **方法** | **端点** | **描述** |  
|-------|----------|-------------|  
| `GET` | `/webhooks` | 列出所有 Webhook |  
- **POST** | `/webhooks` | 创建新的 Webhook |  
- **示例：**  
**POST** `/webhooks`  

****安全提示：**  
Webhook URL 会在服务器端进行验证；禁止使用私有 IP、云元数据端点和非 HTTPS 协议。仅配置您能够控制的端点，并务必设置 `secret` 参数以验证签名。  
**响应**：`201 Created`  

#### Webhook 数据传输  
Webhook 数据会包含 `X-Webhook-Signature` 头部的 HMAC-SHA256 签名（如果配置了 `secret` 参数）。请验证此签名以确保数据真实性。  

#### 示例  
- **完整工作流程：** 创建会话并发送第一条消息  
- **为收到的消息设置 Webhook**  
- **监控群组中的特定关键词**  

#### 错误响应  
所有 API 请求都会返回标准错误代码：  
**代码示例：**  
| **状态码** | **含义** |  
|---------|---------|  
| 400 | 请求无效 |  
| 401 | 未经授权 |  
| 403 | 超出使用限制 |  
| 404 | 资源未找到 |  
| 429 | 请求频率过高 |  
| 500 | 服务器内部错误 |  

#### 使用限制  
API 请求受到使用频率的限制（根据套餐不同而有所差异）：  
| **套餐** | **每分钟请求次数** |  
|------|-------------|  
| 免费 | 10 次 |  
| 入门级 | 20 次 |  
| 专业级 | 40 次 |  
| 商业级 | 60 次 |  
**限制信息包含在响应中：** `X-RateLimit-Remaining`, `X-RateLimit-Reset`  

#### 相关服务  
- **moltflow-outreach**：批量发送消息、定时发送、自定义群组管理  
- **moltflow-leads**：潜在客户检测、流程跟踪、批量操作、CSV/JSON 导出  
- **moltflow-ai**：基于 AI 的自动回复、语音转录、知识库管理  
- **moltflow-a2a**：代理间通信协议、加密消息传输  
- **moltflow-reviews**：评论收集与评价管理  
- **moltflow-admin**：平台管理、用户管理、套餐配置