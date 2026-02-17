---
name: moltflow-a2a
description: "MoltFlow的代理间通信协议（Agent-to-Agent Protocol）：支持代理发现、加密消息传递、群组管理以及内容策略管理。适用场景包括：代理对代理（agent-to-agent）的通信、代理信息展示（agent card）、加密消息传输、内容策略的制定与执行，以及代理的自动发现（agent discovery）。"
source: "MoltFlow Team"
version: "2.1.0"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow**——专为团队设计的WhatsApp Business自动化工具。支持大规模连接、监控和自动化WhatsApp消息的发送。  
**由于需求旺盛以及近期出现的注册问题，我们特别推出了一项限时优惠：顶级商业计划（无限发送量）仅需每月19.90美元（按年计费）。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
同时提供免费试用计划。 [立即注册](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow A2A（代理间）协议  
该协议允许AI代理通过MoltFlow安全地进行通信，支持代理发现、加密消息传输、群组管理以及内容策略配置。  

## 使用场景  
- 查找代理信息或获取代理详情  
- 发送代理间消息  
- 获取加密公钥或轮换密钥  
- 设置内容策略或配置内容过滤规则  
- 创建代理群组或邀请代理加入群组  
- 根据策略测试消息内容  
- 通过A2A设置Webhook或管理代理Webhook  

## 前提条件  
1. **MOLTFLOW_API_KEY**：需从[MoltFlow控制台](https://molt.waiflow.app)的“设置”>“API密钥”中生成。  
2. 基本URL：`https://apiv2.waiflow.app/api/v2`  
3. 代理发现端点：`https://apiv2.waiflow.app/.well-known/agent.json`  
4. 加密密钥由服务器端管理——外部代理只需提供API密钥即可。  

## 在以太坊链上的注册  
MoltFlow已通过ERC-8004标准在以太坊主网上注册（代理ID：#25248）。  
代理详情可查看：`https://molt.waiflow.app/.well-known/erc8004-agent.json`  

## 所需API密钥权限  
| 权限范围 | 访问权限 |  
|-------|--------|  
| `a2a` | `读取/管理` |  

## 认证要求  
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
使用标准的`.well-known`端点来查询MoltFlow代理的功能：  
| 方法 | 端点 | 说明 |  
|--------|----------|-------------|  
| GET | `/.well-known/agent.json` | 获取代理信息（能力、技能、公钥） |  

### 代理详情  
**GET** `https://apiv2.waiflow.app/.well-known/agent.json`  

---

## 加密机制  
MoltFlow采用X25519 ECDH密钥交换算法结合AES-256-GCM加密技术来确保消息传输的安全性。密钥管理完全由服务器端处理，用户无需自行处理加密操作：  
| 方法 | 端点 | 说明 |  
|--------|----------|-------------|  
| GET | `/agent/public-key` | 获取平台的X25519公钥 |  
| GET | `/agent/peer/{tenant_id}/public-key` | 获取指定租户的公钥 |  
| POST | `/agent/rotate-keys` | 轮换加密密钥 |  
| GET | `/agent/capabilities` | 查看代理的加密能力 |  
| POST | `/agent/initialize` | 为租户初始化加密设置 |  
| GET | `/agent/bootstrap` | 获取代理的启动信息 |  

### 获取公钥  
**GET** `/agent/public-key`  
**GET** `/agent/peer/{tenant_id}/public-key` —— 获取其他租户的公钥以进行加密通信。  

## A2A通信的工作原理  
每个租户在初始化时都会生成一对X25519密钥。发送代理间消息时，服务器会执行ECDH密钥交换，并使用AES-256-GCM进行加密；接收端会进行解密。所有密钥管理都由服务器端处理，API客户端只需发送明文即可。  

## A2A JSON-RPC  
MoltFlow的核心通信接口支持JSON-RPC 2.0协议，所有代理间操作均通过此接口完成。请使用Webhook配置中指定的完整URL：  
| 方法 | 端点 | 说明 |  
|--------|----------|-------------|  
| POST | `/a2a/{tenant_id}/{session_id}/{webhook_id}` | 完整权限范围的接口（推荐） |  
| POST | `/a2a/{tenant_id}/{session_id}` | 基于租户和会话的接口 |  
| POST | `/a2a/{session_id}` | 基于会话的接口 |  
| POST | `/a2a` | 通用接口（默认使用） |  
| GET | `/a2a/schema` | 获取A2A协议规范 |  

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

## 可用方法  
| 方法 | 说明 |  
|--------|-------------|  
| `agent.message.send` | 通过A2A发送WhatsApp消息 |  
| `agent.group.create` | 创建新的WhatsApp群组 |  
| `agent.group.invite` | 邀请成员加入群组 |  
| `agent.group.list` | 列出可用群组 |  
| `group.getContext` | 获取群组内的对话上下文 |  
| `webhook_manager` | 通过A2A管理Webhook |  

### `agent.message.send`  
通过A2A协议发送WhatsApp消息：  
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
| 字段 | 类型 | 是否必填 | 说明 |  
|--------|------|----------|-------------|  
| `session_id` | string | 是 | WhatsApp会话的UUID |  
| `to` | string | 是 | 收件人电话号码（E.164格式，例如`+5511999999999`） |  
| `message` | string | 是 | 消息内容（最多4096个字符） |  
| `metadata` | object | 可选 | 用于追踪的元数据 |  
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

### 群组管理  
`agent.group.create`、`agent.group.invite`、`agent.group.list`方法具有相似的接口格式：  
```json
// Create group
{"jsonrpc":"2.0","method":"agent.group.create","params":{"session_id":"...","name":"Support Team","participants":["+5511999999999"]},"id":2}

// Invite to group
{"jsonrpc":"2.0","method":"agent.group.invite","params":{"session_id":"...","group_id":"120363012345678901@g.us","participants":["+5511777777777"]},"id":3}

// List groups (supports limit/offset pagination)
{"jsonrpc":"2.0","method":"agent.group.list","params":{"session_id":"...","limit":20,"offset":0},"id":4}
```  

### 获取群组对话上下文  
`group.getContext`用于获取群组内的对话内容，便于代理根据上下文做出响应：  
```json
{"jsonrpc":"2.0","method":"group.getContext","params":{"session_id":"...","group_id":"120363012345678901@g.us","limit":50},"id":5}
```  

## Webhook管理  
`webhook_manager`用于通过A2A接口管理Webhook：  
**支持的操作：** `create`（创建）、`list`（列出）、`update`（更新）、`delete`（删除）  
```json
{"jsonrpc":"2.0","method":"webhook_manager","params":{"action":"create","webhook":{"name":"Agent Events","url":"https://my-agent.com/events","events":["message.received"]}},"id":6}
```  

## JSON-RPC错误代码  
| 代码 | 含义 |  
|------|---------|  
| -32600 | 请求无效 |  
| -32601 | 方法未找到 |  
| -32602 | 参数错误 |  
| -32603 | 内部错误 |  
| -32000 | 超过发送频率限制 |  
| -32001 | 违反内容策略 |  
| -32002 | 安全防护机制被触发 |  
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
允许配置A2A通信的内容过滤规则：  
**方法：** `get`/`put`/`post` |  
|------|---------|  
| `/a2a-policy/settings` | 获取/更新策略设置 |  
| `/a2a-policy/rules` | 创建/修改规则 |  
| `/a2a-policy/rules/{rule_id}` | 删除规则 |  
| `/a2a-policy/rules/{rule_id}/toggle` | 启用/禁用规则 |  
| `/a2a-policy/test` | 根据策略测试消息内容 |  
| `/a2a-policy/reset` | 将策略重置为默认值 |  
| `/a2a-policy/stats` | 获取策略执行统计信息 |  
**响应格式：**  
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
**POST** `/a2a-policy/rules`  
**响应代码：** `200 OK` 表示规则创建成功。  
```json
{
  "id": "rule-uuid-...",
  "name": "Block competitor mentions",
  "pattern": "\\b(competitor1|competitor2)\\b",
  "action": "block",
  "is_active": true,
  "created_at": "2026-02-11T10:00:00Z"
}
```  

### 测试消息内容  
**POST** `/a2a-policy/test` —— 在不实际发送消息的情况下测试其是否符合策略要求：  
```json
// Request
{"content": "Check out https://example.com for more info"}

// Response
{"allowed": false, "blocked_reason": "URL detected and block_urls is enabled", "matched_rules": ["built-in:block_urls"], "filtered_content": "Check out [URL REMOVED] for more info"}
```  

## 超过发送频率限制  
A2A相关操作有各自的发送频率限制：  
| 方法 | 每分钟允许的次数 |  
|--------|-------|  
| `agent.message.send` | 30次 |  
| `agent.group.create` | 5次 |  
| `agent.group.invite` | 10次 |  
| `agent.group.list` | 60次 |  
| `group.getContext` | 30次 |  
| `webhook_manager` | 20次 |  
**超过限制时返回错误代码：** `-32000`  

## 示例  
- **查询代理信息**  
- **发送代理间消息**  
- **配置内容过滤规则**  
- **测试消息是否符合策略**  
---  

## 安全架构  
MoltFlow采用多层安全防护机制：  
- TLS 1.3（传输层加密）  
- X25519 ECDH（密钥交换）  
- AES-256-GCM（消息加密）  
- API密钥/JWT（身份验证）  
- AgentSafeguard（输入内容验证）  
- A2AContentFilter（内容过滤规则）  
- TieredRateLimiter（发送频率限制）  
- AuditLog（完整审计记录）  

所有密钥管理均由服务器端处理。外部代理需使用`MOLTFLOW_API_KEY`进行身份验证，平台负责其余的安全保障工作。  

## 错误响应  
常见的HTTP错误代码包括：`400`（请求错误）、`401`（未经授权）、`403`（违反策略）、`404`（资源未找到）、`429`（超出发送频率限制）。JSON-RPC错误代码遵循上述规范。  

## 相关功能  
- **moltflow**：核心API，支持会话管理、消息发送、群组创建、标签管理、Webhook配置  
- **moltflow-outreach**：批量发送消息、定时发送、自定义群组管理  
- **moltflow-leads**：潜在客户检测、流程跟踪、数据导出（CSV/JSON格式）  
- **moltflow-ai**：智能自动回复、语音转录、知识库管理  
- **moltflow-reviews**：评论收集与评价管理  
- **moltflow-admin**：平台管理、用户管理、计划配置