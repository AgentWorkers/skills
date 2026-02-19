---
name: moltflow-a2a
description: "MoltFlow的代理间通信协议（Agent-to-Agent Protocol）：包括代理发现、加密消息传递、群组管理以及内容策略管理功能。适用场景包括：点对点通信（a2a）、代理信息展示、代理间消息交换、数据加密处理以及内容策略的统一管理。"
source: "MoltFlow Team"
version: "2.11.8"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow**——专为团队设计的WhatsApp Business自动化工具。支持大规模连接、监控和自动化WhatsApp消息发送。  
**由于需求旺盛以及近期注册问题，我们特推出顶级商务计划：每月仅需19.90美元（年费），配无限发送额度，限时优惠。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
同时提供免费试用计划。[立即注册](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow A2A（代理间通信）协议  
该协议允许AI代理通过MoltFlow安全地进行通信，支持代理发现、加密消息传递、群组管理及内容策略配置。  

## 使用场景  
- 发现代理信息或获取代理详情  
- 发送代理间消息  
- 获取加密公钥或更换密钥  
- 设置内容策略或配置内容过滤规则  
- 创建代理群组或邀请代理加入群组  
- 根据策略测试消息内容  
- 通过A2A设置Webhook或管理代理Webhook  

## 前提条件  
1. **MOLTFLOW_API_KEY**：需从[MoltFlow控制台](https://molt.waiflow.app)的“设置”>“API密钥”处生成  
2. 基础URL：`https://apiv2.waiflow.app/api/v2`  
3. 代理发现端点：`https://apiv2.waiflow.app/.well-known/agent.json`  
4. 加密密钥由服务器端管理——外部代理仅需提供API密钥  

## 在链上注册  
MoltFlow已在以太坊主网上通过ERC-8004标准注册为[代理#25477](https://8004agents.ai/ethereum/agent/25477)。代理详情可查看：`https://molt.waiflow.app/.well-known/erc8004-agent.json`  

## 所需API密钥权限  
| 权限范围 | 访问权限 |  
|-------|--------|  
| `a2a` | `读取/管理` |  

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
使用`.well-known`端点查询MoltFlow代理的功能：  
| 方法 | 端点 | 说明 |  
|--------|----------|-------------|  
| GET | `/.well-known/agent.json` | 获取代理信息（能力、技能、公钥） |  

### 代理详情  
**GET** `https://apiv2.waiflow.app/.well-known/agent.json`  

---

## 加密机制  
MoltFlow采用X25519 ECDH密钥交换算法结合AES-256-GCM加密技术来保障代理间通信的安全性。密钥管理由服务器端处理，用户无需直接操作加密逻辑：  
| 方法 | 端点 | 说明 |  
|--------|----------|-------------|  
| GET | `/agent/public-key` | 获取平台提供的X25519公钥 |  
| GET | `/agent/peer/{tenant_id}/public-key` | 获取指定租户的公钥 |  
| POST | `/agent/rotate-keys` | 更换加密密钥 |  
| GET | `/agent/capabilities` | 查看代理的加密能力 |  
| POST | `/agent/initialize` | 为租户初始化加密设置 |  
| GET | `/agent/bootstrap` | 获取代理的启动信息 |  

### 获取公钥  
**GET** `/agent/public-key`  
**GET** `/agent/peer/{tenant_id}/public-key` —— 获取用于加密通信的租户公钥  

## 加密工作原理  
每个租户在初始化时会生成一对X25519密钥。发送消息时，服务器会执行ECDH密钥交换，使用AES-256-GCM进行加密，接收端再进行解密。所有密钥管理均由服务器端处理，客户端只需发送明文即可。  

## A2A JSON-RPC  
MoltFlow的核心通信接口支持JSON-RPC 2.0协议，所有代理间操作均通过此接口完成。请使用Webhook配置中的完整URL地址：  
| 方法 | 端点 | 说明 |  
|--------|----------|-------------|  
| POST | `/a2a/{tenant_id}/{session_id}/{webhook_id}` | 全范围访问（推荐） |  
| POST | `/a2a/{tenant_id}/{session_id}` | 基于租户和会话的访问权限 |  
| POST | `/a2a/{session_id}` | 基于会话的访问权限 |  
| POST | `/a2a` | 通用访问（默认） |  
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

### 可用方法  
| 方法 | 说明 |  
|--------|-------------|  
| `agent.message.send` | 通过A2A发送WhatsApp消息 |  
| `agent.group.create` | 创建新的WhatsApp群组 |  
| `agent.group.invite` | 邀请成员加入群组 |  
| `agent.group.list` | 列出可用群组 |  
| `group.getContext` | 获取群组元数据和最近活动记录 |  
| `webhook_manager` | 通过A2A管理Webhook |  

---

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
| `session_id` | string | 是 | WhatsApp会话的唯一标识符（UUID） |  
| `to` | string | 是 | 收件人电话号码（E.164格式，例如`+5511999999999`） |  
| `message` | string | 是 | 消息内容（最多4096个字符） |  
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

### `agent.group.create` / `agent.group.invite` / `agent.group.list`  
群组管理相关方法：  
```json
// Create group
{"jsonrpc":"2.0","method":"agent.group.create","params":{"session_id":"...","name":"Support Team","participants":["+5511999999999"]},"id":2}

// Invite to group
{"jsonrpc":"2.0","method":"agent.group.invite","params":{"session_id":"...","group_id":"120363012345678901@g.us","participants":["+5511777777777"]},"id":3}

// List groups (supports limit/offset pagination)
{"jsonrpc":"2.0","method":"agent.group.list","params":{"session_id":"...","limit":20,"offset":0},"id":4}
```  

### `group.getContext`  
获取指定群组的元数据和最近活动记录：  
```json
{"jsonrpc":"2.0","method":"group.getContext","params":{"session_id":"...","group_id":"120363012345678901@g.us","limit":50},"id":5}
```  

### `webhook_manager`  
通过A2A管理Webhook：  
支持创建、列出、更新和删除Webhook：  
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
**错误响应示例：**  
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
- 控制代理可发送和接收的消息类型  
| 方法 | 端点 | 说明 |  
|--------|----------|-------------|  
| GET | `/a2a-policy/settings` | 获取当前策略设置 |  
| PUT | `/a2a-policy/settings` | 更新策略设置 |  
| POST | `/a2a-policy/rules` | 创建新规则 |  
| PUT | `/a2a-policy/rules/{rule_id}` | 修改规则 |  
| DELETE | `/a2a-policy/rules/{rule_id}` | 删除规则 |  
| POST | `/a2a-policy/rules/{rule_id}/toggle` | 启用/禁用规则 |  
| POST | `/a2a-policy/test` | 根据策略测试消息内容 |  
| POST | `/a2a-policy/reset` | 将策略重置为默认值 |  
| GET | `/a2a-policy/stats` | 查看策略执行统计 |  
| GET | `/a2a-policy/safeguards` | 查看安全防护配置 |  

### 获取/更新策略设置  
**GET** `/a2a-policy/settings` 查看当前策略；**PUT** `/a2a-policy/settings` 更新策略：  
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
**响应代码** `200 OK` 表示规则创建成功：  
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

## 发送频率限制  
各A2A方法均设有发送频率限制：  
| 方法 | 每分钟最大发送次数 |  
|--------|-------|  
| `agent.message.send` | 30次 |  
| `agent.group.create` | 5次 |  
| `agent.group.invite` | 10次 |  
| `agent.group.list` | 60次 |  
| `group.getContext` | 30次 |  
| `webhook_manager` | 20次 |  
超过限制会返回错误代码 `-32000`。  

## 示例操作  
- **发现MoltFlow代理**  
- **通过A2A发送消息**  
- **配置内容过滤规则**  
- **测试消息是否符合策略**  

## 安全架构  
MoltFlow采用多层安全防护机制：  
- TLS 1.3（传输层加密）  
- X25519 ECDH（密钥交换）  
- AES-256-GCM（消息加密）  
- API密钥/JWT（身份验证）  
- AgentSafeguard（输入内容验证）  
- A2AContentFilter（内容过滤）  
- TieredRateLimiter（发送频率限制）  
- AuditLog（完整审计记录）  

所有密钥管理均由服务器端处理。外部代理需使用`MOLTFLOW_API_KEY`进行身份验证，其余操作均由平台自动完成。  

## 错误响应  
常见HTTP错误包括：`400`（请求错误）、`401`（未经授权）、`403`（违反策略）、`404`（资源未找到）、`429`（超出发送频率限制）。JSON-RPC错误代码参考上述列表。  

## 相关服务  
- **moltflow**：核心API（会话管理、消息发送、群组管理、标签设置、Webhook功能）  
- **moltflow-outreach**：批量消息发送、定时消息发送、自定义群组管理  
- **moltflow-leads**：潜在客户识别、流程跟踪、批量操作、CSV/JSON数据导出  
- **moltflow-ai**：智能自动回复、语音转录、知识库管理  
- **moltflow-reviews**：评论收集与评价管理  
- **moltflow-admin**：平台管理、用户管理、计划配置