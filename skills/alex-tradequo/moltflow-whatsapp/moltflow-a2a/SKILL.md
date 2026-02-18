---
name: moltflow-a2a
description: "MoltFlow的代理间通信协议（Agent-to-Agent Protocol）：包括代理发现（agent discovery）、加密消息传递（encrypted messaging）、组管理（group management）以及内容策略（content policy）功能。适用场景包括：点对点通信（a2a）、代理信息展示（agent card）、代理间消息交换（agent message）、数据加密（encrypted communication）、内容策略管理（content policy implementation），以及代理的自动发现（automatic agent discovery）。"
source: "MoltFlow Team"
version: "2.11.8"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow** — 专为团队打造的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。  
**由于需求旺盛以及近期出现的注册问题，我们特推出顶级商务计划：每月仅需 19.90 美元（按年计费），并提供无限使用额度——此优惠仅限限时有效。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
也提供免费试用计划。 [立即注册](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow 的 A2A（代理间）协议  

该协议允许 AI 代理通过 MoltFlow 安全地进行通信，支持代理发现、加密消息传递、群组管理和可配置的内容策略。  

## 使用场景  
- 发现代理或获取代理信息  
- 发送代理间消息  
- 获取加密公钥或轮换密钥  
- 设置内容策略或配置内容过滤器  
- 创建代理群组或邀请代理加入群组  
- 根据策略测试消息内容  
- 通过 A2A 设置 Webhook 或管理代理 Webhook  

## 先决条件  
1. **MOLTFLOW_API_KEY**：需从 [MoltFlow 控制台](https://molt.waiflow.app) 的“设置” > “API 密钥”中生成。  
2. 基础 URL：`https://apiv2.waiflow.app/api/v2`  
3. 代理发现端点：`https://apiv2.waiflow.app/.well-known/agent.json`  
4. 加密密钥由服务器端管理——外部代理只需提供 API 密钥即可。  

## 在以太坊主网上的注册  
MoltFlow 已通过 ERC-8004 标准在以太坊主网上注册（代理 ID：#25248）：  
代理信息：`https://molt.waiflow.app/.well-known/erc8004-agent.json`  

## 所需 API 密钥权限  
| 权限范围 | 访问权限 |  
|-------|--------|  
| `a2a` | `读/写` |  

## 认证  
所有请求必须包含以下认证信息之一：  
```
Authorization: Bearer <jwt_token>
```  
或  
```
X-API-Key: <your_api_key>
```  

---

## 代理发现  
使用标准的 `.well-known` 端点来发现 MoltFlow 代理的功能：  
| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| GET | `/.well-known/agent.json` | 获取代理信息（能力、技能、公钥） |  

### 代理信息  
**GET** `https://apiv2.waiflow.app/.well-known/agent.json`  

---

## 加密机制  
MoltFlow 使用 X25519 ECDH 密钥交换算法和 AES-256-GCM 加密技术来确保代理间消息的保密性。密钥管理完全由服务器端处理——用户无需直接处理加密操作：  
| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| GET | `/agent/public-key` | 获取平台的 X25519 公钥 |  
| GET | `/agent/peer/{tenant_id}/public-key` | 获取特定租户的公钥 |  
| POST | `/agent/rotate-keys` | 旋转加密密钥 |  
| GET | `/agent/capabilities` | 获取代理的加密能力信息 |  
| POST | `/agent/initialize` | 为租户初始化加密设置 |  
| GET | `/agent/bootstrap` | 获取代理的初始化信息 |  

### 获取公钥  
**GET** `/agent/public-key`  
**GET** `/agent/peer/{tenant_id}/public-key` —— 获取其他租户的公钥以进行加密通信。  

## 加密工作原理  
每个租户在初始化时都会生成一对 X25519 密钥。发送代理间消息时，服务器会执行 ECDH 密钥交换，并使用 AES-256-GCM 进行加密；接收端会进行解密。所有密钥管理都由服务器端处理——API 客户端只需发送明文，平台负责完成加密操作。  

## A2A JSON-RPC  
MoltFlow 的核心通信接口支持 JSON-RPC 2.0 协议。所有代理间的操作都通过这个接口完成。请使用 Webhook 配置中指定的完整路径：  
| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| POST | `/a2a/{tenant_id}/{session_id}/{webhook_id}` | 完整权限范围的接口（推荐） |  
| POST | `/a2a/{tenant_id}/{session_id}` | 基于租户和会话范围的接口 |  
| POST | `/a2a/{session_id}` | 基于会话范围的接口 |  
| POST | `/a2a` | 通用接口（用于访问当前活跃会话） |  
| GET | `/a2a/schema` | 获取 A2A 协议的详细信息 |  

## 请求格式  
```json
{
  "jsonrpc": "2.0",
  "method": "agent.message.send",
  "params": { ... },
  "id": 1
}
```  

## 响应格式  
```json
{
  "jsonrpc": "2.0",
  "result": { ... },
  "id": 1
}
```  

### 可用方法  
| 方法 | 描述 |  
|--------|-------------|  
| `agent.message.send` | 通过 A2A 协议发送 WhatsApp 消息 |  
| `agent.group.create` | 创建新的 WhatsApp 群组 |  
| `agent.group.invite` | 邀请成员加入群组 |  
| `agent.group.list` | 列出所有群组 |  
| `group.getContext` | 获取群组元数据和最近活动记录 |  
| `webhook_manager` | 通过 A2A 管理 Webhook |  

---

### `agent.message.send`  
通过 A2A 协议发送 WhatsApp 消息：  
**请求格式：**  
```json
{
  "jsonrpc": "2.0",
  "method": "agent.message.send",
  "params": {
    "session_id": "a1b2c3d4-...",
    "to": "+5511999999999",
    "message": "Hello from Agent!",
    "metadata": {
      "source_agent": "my-crm-agent",
      "correlation_id": "req-123"
    }
  },
  "id": 1
}
```  
**参数：**  
| 字段 | 类型 | 是否必填 | 描述 |  
|-------|------|----------|-------------|  
| `session_id` | string | 是 | WhatsApp 会话的唯一标识符（UUID） |  
| `to` | string | 是 | 收件人的 E.164 格式电话号码（例如：`+5511999999999`） |  
| `message` | string | 是 | 消息内容（最多 4096 个字符） |  
| `metadata` | object | 可选 | 用于追踪的附加元数据 |  

**响应格式：**  
```json
{
  "jsonrpc": "2.0",
  "result": {
    "message_id": "wa-msg-id-...",
    "status": "sent",
    "timestamp": "2026-02-11T10:05:00Z"
  },
  "id": 1
}
```  

---

### 群组管理  
`agent.group.create`、`agent.group.invite` 和 `agent.group.list` 方法具有相似的接口格式：  
```json
// Create group
{"jsonrpc":"2.0","method":"agent.group.create","params":{"session_id":"...","name":"Support Team","participants":["+5511999999999"]},"id":2}

// Invite to group
{"jsonrpc":"2.0","method":"agent.group.invite","params":{"session_id":"...","group_id":"120363012345678901@g.us","participants":["+5511777777777"]},"id":3}

// List groups (supports limit/offset pagination)
{"jsonrpc":"2.0","method":"agent.group.list","params":{"session_id":"...","limit":20,"offset":0},"id":4}
```  

### 获取群组信息  
`group.getContext` 方法用于获取群组的元数据和最近活动记录：  
```json
{"jsonrpc":"2.0","method":"group.getContext","params":{"session_id":"...","group_id":"120363012345678901@g.us","limit":50},"id":5}
```  

### Webhook 管理  
`webhook_manager` 方法用于通过 A2A 管理 Webhook：  
- `create`：创建 Webhook  
- `list`：列出所有 Webhook  
- `update`：更新 Webhook 配置  
- `delete`：删除 Webhook  

---

### JSON-RPC 错误代码  
| 代码 | 含义 |  
|------|---------|  
| -32600 | 请求无效 |  
| -32601 | 方法未找到 |  
| -32602 | 参数错误 |  
| -32603 | 内部错误 |  
| -32000 | 超过请求频率限制 |  
| -32001 | 违反内容策略 |  
| -32002 | 安全防护机制触发（消息被屏蔽） |  
**错误响应格式：**  
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32602,
    "message": "Invalid phone number format. Expected E.164 (e.g., +5511999999999)"
  },
  "id": 1
}
```  

## 内容策略  
允许配置代理间通信的内容过滤规则：  
- `GET` `/a2a-policy/settings`：获取当前策略设置  
- `PUT` `/a2a-policy/settings`：更新策略设置  
- `POST` `/a2a-policy/rules`：创建新规则  
- `PUT` `/a2a-policy/rules/{rule_id}`：修改规则  
- `DELETE` `/a2a-policy/rules/{rule_id}`：删除规则  
- `POST` `/a2a-policy/rules/{rule_id}/toggle`：启用/禁用规则  
- `POST` `/a2a-policy/test`：根据策略测试消息内容  
- `POST` `/a2a-policy/reset`：将策略重置为默认值  
- `GET` `/a2a-policy/stats`：获取策略执行统计信息  
- `GET` `/a2a-policy/safeguards`：查看安全防护配置  

### 获取/更新策略设置  
**GET** `/a2a-policy/settings`：获取当前策略设置。  
**PUT** `/a2a-policy/settings`：更新策略设置。  
```json
{
  "enabled": true,
  "input_sanitization_enabled": true,
  "output_filtering_enabled": true,
  "block_urls": false,
  "block_phone_numbers": false,
  "max_message_length": 4096,
  "allowed_languages": ["en", "pt", "es"]
}
```  

### 创建自定义规则  
**POST** `/a2a-policy/rules`：创建新的内容过滤规则：  
**响应格式：** `200 OK`  

### 测试消息内容  
**POST** `/a2a-policy/test`：在不发送消息的情况下测试其是否符合策略要求：  
```json
// Request
{"content": "Check out https://example.com for more info"}

// Response
{"allowed": false, "blocked_reason": "URL detected and block_urls is enabled", "matched_rules": ["built-in:block_urls"], "filtered_content": "Check out [URL REMOVED] for more info"}
```  

### 策略统计  
**GET` `/a2a-policy/stats`：返回统计信息（如总检查次数、被屏蔽次数、被过滤次数及热门规则）。  

## 请求频率限制  
部分 A2A 方法存在频率限制：  
| 方法 | 每分钟允许的请求数 |  
|--------|-------|  
| `agent.message.send` | 30 次 |  
| `agent.group.create` | 5 次 |  
| `agent.group.invite` | 10 次 |  
| `agent.group.list` | 60 次 |  
| `group.getContext` | 30 次 |  
| `webhook_manager` | 20 次 |  
超过限制会导致 JSON-RPC 错误 `-32000`。  

## 示例  
- **发现 MoltFlow 代理**  
- **通过 A2A 发送消息**  
- **配置内容过滤规则**  
- **测试消息是否符合策略**  

---

## 安全机制  
MoltFlow 采用多层安全防护：  
- TLS 1.3（传输层加密）  
- X25519 ECDH（密钥交换）  
- AES-256-GCM（消息加密）  
- API 密钥/JWT（身份验证）  
- AgentSafeguard（输入内容验证）  
- A2AContentFilter（内容过滤）  
- TieredRateLimiter（请求频率限制）  
- AuditLog（完整审计记录）  

所有加密密钥的管理都由服务器端处理。外部代理需使用 `MOLTFLOW_API_KEY` 进行身份验证，其余操作均由平台自动处理。  

## 错误响应  
常见的 HTTP 错误包括：`400`（请求错误）、`401`（未经授权）、`403`（违反策略）、`404`（资源未找到）、`429`（请求频率限制）。JSON-RPC 错误代码遵循上述规范。  

## 相关功能  
- **moltflow**：核心 API（会话管理、消息发送、群组管理、标签设置、Webhook 配置）  
- **moltflow-outreach**：批量发送消息、定时发送、自定义群组管理  
- **moltflow-leads**：潜在客户识别、流程跟踪、批量操作、CSV/JSON 数据导出  
- **moltflow-ai**：基于 AI 的自动回复、语音转录、知识库管理  
- **moltflow-reviews**：评论收集与评价管理  
- **moltflow-admin**：平台管理、用户管理、计划配置