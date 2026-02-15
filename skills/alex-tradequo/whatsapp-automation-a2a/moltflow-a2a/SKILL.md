---
name: moltflow-a2a
description: "MoltFlow的代理间通信协议（Agent-to-Agent Protocol）支持以下功能：代理发现（agent discovery）、加密消息传递（encrypted messaging）、群组管理（group management）以及内容策略管理（content policy）。适用场景包括：代理对代理的直接通信（a2a communication）、代理信息展示（agent card display）、代理间消息传递（agent-to-agent messaging）、数据加密（data encryption），以及内容策略的统一管理（content policy enforcement）。"
source: "MoltFlow Team"
version: "2.1.0"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---

**MoltFlow**——专为团队设计的WhatsApp Business自动化工具。支持大规模连接、监控和自动化WhatsApp消息的发送。  
[通过年费订阅可节省高达17%的费用](https://molt.waiflow.app/checkout?plan=free)；提供免费试用版，无需信用卡。  

# MoltFlow A2A（代理间通信）协议  
该协议允许AI代理通过MoltFlow安全地进行通信，支持代理发现、加密消息传输、群组管理以及可配置的内容策略。  

## 使用场景  
- 发现代理信息或获取代理详情  
- 发送代理间消息  
- 获取加密公钥或轮换密钥  
- 设置内容策略或配置内容过滤规则  
- 创建代理群组或邀请代理加入群组  
- 根据策略测试消息内容  
- 通过A2A设置Webhook或管理代理Webhook  

## 前提条件  
1. **MOLTFLOW_API_KEY**：需从[MoltFlow控制台](https://molt.waiflow.app)的“设置”>“API密钥”中生成。  
2. 基础URL：`https://apiv2.waiflow.app/api/v2`  
3. 代理发现端点：`https://apiv2.waiflow.app/.well-known/agent.json`  
4. 加密密钥由服务器端管理——外部代理仅需API密钥即可。  

## 所需API密钥权限  
| 权限范围 | 访问权限 |  
|--------|--------|  
| `a2a` | `读/管理` |  

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
使用标准的`.well-known`端点来发现MoltFlow代理的功能。  
| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| GET | `/.well-known/agent.json` | 获取代理信息（能力、技能、公钥） |  

### 代理详情  
**GET** `https://apiv2.waiflow.app/.well-known/agent.json`  

---

## 加密机制  
MoltFlow采用X25519 ECDH密钥交换算法结合AES-256-GCM加密技术来保障代理间消息的保密性。密钥管理完全由服务器端处理——用户无需直接处理加密操作。  
| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| GET | `/agent/public-key` | 获取平台的X25519公钥 |  
| GET | `/agent/peer/{tenant_id}/public-key` | 获取指定租户的公钥 |  
| POST | `/agent/rotate-keys` | 轮换加密密钥 |  
| GET | `/agent/capabilities` | 查看代理的加密能力 |  
| POST | `/agent/initialize` | 为租户初始化加密设置 |  
| GET | `/agent/bootstrap` | 获取代理的启动信息 |  
| POST | `/agent/export-keypair` | 导出加密密钥对以备备份 |  
| POST | `/agent/import-keypair` | 从备份中导入加密密钥对 |  

### 获取公钥  
**GET** `/agent/public-key`  
**GET** `/agent/peer/{tenant_id}/public-key` —— 获取其他租户的公钥以进行加密通信。  

### 加密工作原理  
每个租户在初始化时会生成一对X25519密钥。发送代理间消息时，服务器会执行ECDH密钥交换，使用AES-256-GCM进行加密，并在接收端解密。所有密钥管理均通过服务器端完成——API客户端只需发送明文，平台会自动处理加密过程。  

### 密钥对导出/导入  
```bash
curl -X POST https://apiv2.waiflow.app/agent/export-keypair \
  -H "X-API-Key: $MOLTFLOW_API_KEY"
```  
```bash
curl -X POST https://apiv2.waiflow.app/agent/import-keypair \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"public_key": "...", "private_key": "..."}'
```  

## A2A JSON-RPC  
MoltFlow的核心代理间通信接口支持JSON-RPC 2.0协议。所有代理间操作均通过此接口完成。  
| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| POST | `/a2a` | 发送代理间消息的JSON-RPC接口 |  
| GET | `/a2a/schema` | 获取A2A协议规范 |  

### 请求格式  
```json
{
  "jsonrpc": "2.0",
  "method": "agent.message.send",
  "params": { ... },
  "id": 1
}
```  
### 响应格式  
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
| `agent.message.send` | 通过A2A发送WhatsApp消息 |  
| `agent.group.create` | 创建新的WhatsApp群组 |  
| `agent.group.invite` | 邀请成员加入群组 |  
| `agent.group.list` | 列出可用群组 |  
| `group.getContext` | 获取群组的对话上下文 |  
| `webhook_manager` | 通过A2A管理Webhook |  

---

### `agent.message.send`  
通过A2A协议发送WhatsApp消息。  
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
| `session_id` | string | 是 | WhatsApp会话的UUID |  
| `to` | string | 是 | E.164格式的电话号码（例如：`+5511999999999`） |  
| `message` | string | 是 | 消息内容（最多4096个字符） |  
| `metadata` | object | 否 | 用于追踪的任意元数据 |  

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
群组管理方法具有相同的请求格式：  
```json
// Create group
{"jsonrpc":"2.0","method":"agent.group.create","params":{"session_id":"...","name":"Support Team","participants":["+5511999999999"]},"id":2}

// Invite to group
{"jsonrpc":"2.0","method":"agent.group.invite","params":{"session_id":"...","group_id":"120363012345678901@g.us","participants":["+5511777777777"]},"id":3}

// List groups (supports limit/offset pagination)
{"jsonrpc":"2.0","method":"agent.group.list","params":{"session_id":"...","limit":20,"offset":0},"id":4}
```  

### `group.getContext`  
获取被监控群组的对话上下文，有助于代理根据上下文做出响应。  
```json
{"jsonrpc":"2.0","method":"group.getContext","params":{"session_id":"...","group_id":"120363012345678901@g.us","limit":50},"id":5}
```  

### `webhook_manager`  
通过A2A管理Webhook，支持创建、列出、更新和删除Webhook。  
```json
{"jsonrpc":"2.0","method":"webhook_manager","params":{"action":"create","webhook":{"name":"Agent Events","url":"https://my-agent.com/events","events":["message.received"]}},"id":6}
```  

### JSON-RPC错误代码  
| 代码 | 含义 |  
|------|---------|  
| -32600 | 请求无效 |  
| -32601 | 方法未找到 |  
| -32602 | 参数无效 |  
| -32603 | 内部错误 |  
| -32000 | 超过请求频率限制 |  
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

### 内容策略  
配置A2A通信的内容过滤规则，控制代理可以发送和接收的消息类型。  
| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| GET | `/a2a-policy/settings` | 获取策略设置 |  
| PUT | `/a2a-policy/settings` | 更新策略设置 |  
| POST | `/a2a-policy/rules` | 创建自定义规则 |  
| PUT | `/a2a-policy/rules/{rule_id}` | 更新规则 |  
| DELETE | `/a2a-policy/rules/{rule_id}` | 删除规则 |  
| POST | `/a2a-policy/rules/{rule_id}/toggle` | 启用/禁用规则 |  
| POST | `/a2a-policy/test` | 根据策略测试消息内容 |  
| POST | `/a2a-policy/reset` | 将策略重置为默认值 |  
| GET | `/a2a-policy/stats` | 获取策略执行统计信息 |  
| GET | `/a2a-policy/safeguards` | 查看安全防护配置 |  

### 获取/更新策略设置  
**GET** `/a2a-policy/settings` —— 获取当前策略设置。**PUT** `/a2a-policy/settings` —— 更新策略设置。  
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
**响应：** `200 OK`（表示请求成功）  
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
**POST** `/a2a-policy/test` —— 在不实际发送消息的情况下测试其是否符合策略要求。  
```json
// Request
{"content": "Check out https://example.com for more info"}

// Response
{"allowed": false, "blocked_reason": "URL detected and block_urls is enabled", "matched_rules": ["built-in:block_urls"], "filtered_content": "Check out [URL REMOVED] for more info"}
```  

### 策略统计信息  
**GET** `/a2a-policy/stats` —— 返回`total-checked`（通过策略检查的消息数量）、`totalblocked`（被阻止的消息数量）、`total_filtered`（被过滤的消息数量）和`top_rules`（最常被阻止的规则）。  

## 请求频率限制  
各A2A方法都有相应的频率限制：  
| 方法 | 每分钟允许的请求次数 |  
|--------|-------|  
| `agent.message.send` | 30次 |  
| `agent.group.create` | 5次 |  
| `agent.group.invite` | 10次 |  
| `agent.group.list` | 60次 |  
| `group.getContext` | 30次 |  
| `webhook_manager` | 20次 |  

超过频率限制会导致JSON-RPC错误代码`-32000`。  

## 示例  
- **发现MoltFlow代理**  
```bash
curl https://apiv2.waiflow.app/.well-known/agent.json
```  
- **通过A2A发送消息**  
```bash
curl -X POST https://apiv2.waiflow.app/api/v2/a2a \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "agent.message.send",
    "params": {
      "session_id": "a1b2c3d4-...",
      "to": "+5511999999999",
      "message": "Hello from my AI agent!"
    },
    "id": 1
  }'
```  
- **设置内容策略规则**  
```bash
curl -X POST https://apiv2.waiflow.app/api/v2/a2a-policy/rules \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "No external links",
    "pattern": "https?://",
    "action": "block",
    "description": "Block all URLs in A2A messages"
  }'
```  
- **测试消息内容是否符合策略**  
```bash
curl -X POST https://apiv2.waiflow.app/api/v2/a2a-policy/test \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Visit https://example.com for details"
  }'
```  

## 安全模型  
MoltFlow采用多层安全防护机制：  
- TLS 1.3（传输层安全）  
- X25519 ECDH（密钥交换）  
- AES-256-GCM（消息加密）  
- API密钥/JWT（身份验证）  
- AgentSafeguard（输入验证）  
- A2AContentFilter（内容过滤）  
- TieredRateLimiter（请求频率限制）  
- AuditLog（完整审计记录）  

所有加密密钥管理均由服务器端处理。外部代理需使用`MOLTFLOW_API_KEY`进行身份验证，平台负责其余所有安全相关操作。  

## 错误响应  
常见的HTTP错误代码包括：`400`（请求错误）、`401`（未经授权）、`403`（违反策略）、`404`（资源未找到）、`429`（请求频率限制）。JSON-RPC错误代码遵循上述规范。  

## 相关功能  
- **moltflow**：核心API，支持会话管理、消息发送、群组创建、标签管理、Webhook集成  
- **moltflow-outreach**：批量消息发送、定时消息发送、自定义群组管理  
- **moltflow-leads**：潜在客户识别、流程跟踪、批量操作、CSV/JSON数据导出  
- **moltflow-ai**：基于AI的自动回复、语音转录、知识库管理  
- **moltflow-reviews**：评论收集与评价管理  
- **moltflow-admin**：平台管理、用户管理、计划配置