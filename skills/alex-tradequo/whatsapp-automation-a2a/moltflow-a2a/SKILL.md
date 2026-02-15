---
name: moltflow-a2a
description: "MoltFlow的代理间通信协议（Agent-to-Agent Protocol）：包括代理发现、加密消息传输、群组管理以及内容策略等功能。适用场景包括：代理对代理（agent-to-agent）的通信、代理信息展示（agent card）、加密消息传递、内容策略的制定与执行以及代理的自动发现（agent discovery）。"
source: "MoltFlow Team"
version: "2.1.0"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---

## MoltFlow – 适用于团队的 WhatsApp Business 自动化工具  
连接、监控并大规模自动化 WhatsApp 消息的发送。  

**由于需求量大以及近期出现的注册问题，我们特别推出了一项限时优惠：**  
**顶级商业计划（包含无限发送量）每月仅需 19.90 美元，支持年费支付。**  
[**立即抢购**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
**也提供免费试用计划。** [**立即注册**](https://molt.waiflow.app/checkout?plan=free)  

### MoltFlow 的 A2A（代理间）协议  
该协议支持 AI 代理通过 MoltFlow 安全地进行通信，具备以下功能：  
- 代理发现  
- 加密消息传递  
- 群组管理  
- 可配置的内容策略  

### 使用场景  
- 查看代理信息  
- 发送代理间消息  
- 获取加密公钥  
- 旋转加密密钥  
- 设置内容策略  
- 创建代理组  
- 邀请代理加入组  
- 根据策略检查消息内容  
- 通过 A2A 设置 Webhook  

### 先决条件  
1. **MOLTFLOW_API_KEY**：需在 [MoltFlow 控制台](https://molt.waiflow.app) 的“设置” > “API 密钥”中生成。  
2. 基础 URL：`https://apiv2.waiflow.app/api/v2`  
3. 代理发现端点：`https://apiv2.waiflow.app/.well-known/agent.json`  
4. 加密密钥由服务器端管理；外部代理只需提供 API 密钥即可。  

### 所需 API 密钥权限  
| 权限范围 | 访问权限 |  
|---------|---------|  
| `a2a` | `read/manage` |  

### 认证  
所有请求必须包含以下认证信息之一：  
（此处应插入相应的认证信息代码块）  

### 代理发现  
使用标准的 `.well-known` 端点来查询代理的详细信息：  
| 方法 | 端点 | 描述 |  
|------|--------|-------------|  
| GET | `/.well-known/agent.json` | 获取代理信息（能力、技能、公钥） |  

### 代理信息  
**GET** `https://apiv2.waiflow.app/.well-known/agent.json`  

### 加密机制  
MoltFlow 使用 X25519 ECDH 进行密钥交换，并结合 AES-256-GCM 对消息进行加密。密钥管理完全由服务器端处理，代理无需处理加密细节：  
| 方法 | 端点 | 描述 |  
|------|--------|-------------|  
| GET | `/agent/public-key` | 获取代理的公钥 |  
| GET | `/agent/peer/{tenant_id}/public-key` | 获取特定租户的公钥 |  
| POST | `/agent/rotate-keys` | 旋转加密密钥 |  
| GET | `/agent/capabilities` | 查看代理的加密能力 |  
| POST | `/agent/initialize` | 为租户初始化加密设置 |  
| POST | `/agent/bootstrap` | 获取代理的初始化信息 |  
| POST | `/agent/export-keypair` | 导出加密密钥对以备备份 |  
| POST | `/agent/import-keypair` | 从备份中导入加密密钥对 |  

### 获取公钥  
**GET** `/agent/public-key`  
**GET** `/agent/peer/{tenant_id}/public-key` – 用于与其他租户进行加密通信。  

### 加密原理  
每个租户在初始化时都会生成一对 X25519 密钥。发送代理间消息时，服务器会执行 ECDH 密钥交换，并使用 AES-256-GCM 进行加密；接收端会解密消息。所有密钥管理都由服务器端处理，API 客户端只需发送明文即可。  

### 密钥对导出/导入  
（此处应插入相应的代码块）  

### A2A JSON-RPC  
MoltFlow 的核心通信接口支持 JSON-RPC 2.0 协议：  
所有代理间的操作都通过这个接口完成：  
| 方法 | 端点 | 描述 |  
|------|--------|-------------|  
| POST | `/a2a` | 发送代理间消息 |  
| GET | `/a2a/schema` | 获取 A2A 协议的详细信息 |  

### 请求格式  
（此处应插入请求的 JSON 格式代码块）  

### 响应格式  
（此处应插入响应的 JSON 格式代码块）  

### 可用方法  
| 方法 | 描述 |  
|------|-------------|  
| `agent.message.send` | 通过 A2A 协议发送 WhatsApp 消息 |  
| `agent.group.create` | 创建新的 WhatsApp 群组 |  
| `agent.group.invite` | 邀请成员加入群组 |  
| `agent.group.list` | 列出所有群组 |  
| `group.getContext` | 获取群组的对话上下文 |  
| `webhook_manager` | 通过 A2A 管理 Webhook |  

### `agent.message.send`  
**请求格式：**  
（此处应插入发送消息的请求代码块）  

**参数：**  
| 字段 | 类型 | 是否必填 | 描述 |  
|------|------|-------------|  
| `session_id` | string | 是 | WhatsApp 会话的 UUID |  
| `to` | string | 是 | 收件人的 E.164 电话号码（例如：`+5511999999999`） |  
| `message` | string | 是 | 消息内容（最多 4096 个字符） |  
| `metadata` | object | 可选 | 用于追踪的元数据 |  

**响应格式：**  
（此处应插入响应的 JSON 格式代码块）  

### 群组管理  
`agent.group.create`、`agent.group.invite`、`agent.group.list` 等方法具有相似的请求和响应格式：  
（此处应插入群组管理的代码块）  

### 获取群组上下文  
`group.getContext` 方法用于获取群组的对话上下文，便于代理根据上下文做出响应：  
（此处应插入相关代码块）  

### Webhook 管理  
`webhook_manager` 用于通过 A2A 管理 Webhook：  
- `create`：创建 Webhook  
- `list`：列出所有 Webhook  
- `update`：更新 Webhook 设置  
- `delete`：删除 Webhook  

### 错误代码  
（此处应插入 JSON-RPC 错误代码及其含义）  

### 内容策略  
**A2A 通信的内容过滤规则**：  
- `a2a-policy/settings`：获取当前策略设置  
- `a2a-policy/rules`：创建/修改规则  
- `a2a-policy/test`：测试消息是否符合策略  
- `a2a-policy/reset`：将策略重置为默认值  
- `a2a-policy/stats`：获取策略执行统计信息  

### 示例  
- 查看代理信息  
- 发送代理间消息  
- 设置内容过滤规则  
- 测试消息是否符合策略  

### 安全性  
MoltFlow 采用多层安全机制：  
- TLS 1.3（传输层安全）  
- X25519 ECDH（密钥交换）  
- AES-256-GCM（消息加密）  
- API 密钥/JWT（身份验证）  
- `AgentSafeguard`（输入内容验证）  
- `A2AContentFilter`（内容过滤规则）  
- `TieredRateLimiter`（速率限制）  
- `AuditLog`（完整审计记录）  

所有加密密钥管理均由服务器端处理；外部代理只需使用 `MOLTFLOW_API_KEY` 进行认证，平台会处理其余所有细节。  

### 错误响应  
常见的 HTTP 错误代码包括：`400`（请求错误）、`401`（未经授权）、`403`（违反策略）、`404`（未找到资源）、`429`（超出速率限制）。JSON-RPC 错误会返回相应的错误代码。  

### 相关功能  
- **moltflow**：核心 API，支持会话管理、消息发送、群组创建等基本功能。  
- **moltflow-outreach**：批量发送消息、定时发送、自定义群组管理。  
- **moltflow-leads**：潜在客户检测、流程跟踪、数据导出（CSV/JSON）。  
- **moltflow-ai**：基于 AI 的自动回复、语音转录等功能。  
- **moltflow-reviews**：评论收集与评价管理。  
- **moltflow-admin**：平台管理、用户管理、计划配置等高级功能。