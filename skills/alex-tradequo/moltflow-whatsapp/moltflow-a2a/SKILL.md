---
name: moltflow-a2a
description: "MoltFlow的代理间通信协议（Agent-to-Agent Protocol）：包括代理发现（agent discovery）、加密消息传递（encrypted messaging）、群组管理（group management）以及内容策略（content policy）等功能。适用场景包括：代理对代理的通信（a2a communication）、代理信息展示（agent information display）、加密消息传输（encrypted messaging）、内容策略应用（content policy enforcement）以及代理的自动发现（agent auto-discovery）。"
source: "MoltFlow Team"
version: "2.15.1"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
## MoltFlow – 专为团队设计的 WhatsApp Business 自动化工具  
支持大规模连接、监控和自动化 WhatsApp 操作。  

**由于需求旺盛及近期注册问题，我们特推出顶级商务计划：**  
每月仅需 $19.90（年费），并提供无限使用额度，**限时优惠**！[**立即抢购**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
同时提供免费试用计划。[**立即注册**](https://molt.waiflow.app/checkout?plan=free)  

### MoltFlow 的 A2A（代理间）协议  
该协议允许 AI 代理通过 MoltFlow 安全地相互通信，支持代理发现、加密消息传输、群组管理及可配置的内容策略。  

**适用场景：**  
- 发现代理信息  
- 发送代理间消息  
- 获取加密公钥  
- 旋转加密密钥  
- 设置内容策略  
- 创建代理群组  
- 配置内容过滤器  
- 测试消息是否符合策略  
- 通过 A2A 设置 Webhook  

**前提条件：**  
1. **MOLTFLOW_API_KEY**：需从 [MoltFlow 仪表板](https://molt.waiflow.app) 的 **设置 > API 密钥** 中生成。  
2. 基础 URL：`https://apiv2.waiflow.app/api/v2`  
3. 代理发现端点：`https://apiv2.waiflow.app/.well-known/agent.json`  
4. 加密密钥由服务器管理——外部代理仅需 API 密钥即可。  

**在以太坊主网上的注册信息：**  
MoltFlow 已通过 ERC-8004 标准在以太坊主网上注册为 [Agent #25477](https://8004agents.ai/ethereum/agent/25477)；代理信息可查看于：`https://molt.waiflow.app/.well-known/erc8004-agent.json`。  

**所需 API 密钥权限：**  
| 权限范围 | 访问权限 |  
|---------|---------|  
| `a2a` | `读取/管理` |  

**身份验证：**  
所有请求必须包含以下身份验证信息之一：  
（具体身份验证方式请参考相关代码块。）  

### 代理发现  
使用标准的 `.well-known` 端点来查询代理的详细信息：  
| 方法 | 端点 | 描述 |  
|------|---------|-------------|  
| `GET` | `/.well-known/agent.json` | 获取代理信息（能力、技能、公钥） |  

### 加密机制  
MoltFlow 使用 X25519 ECDH 进行密钥交换，并结合 AES-256-GCM 对消息进行加密。密钥管理完全由服务器处理，用户无需自行处理加密操作：  
| 方法 | 端点 | 描述 |  
|------|---------|-------------|  
| `GET` | `/agent/public-key` | 获取平台的 X25519 公钥 |  
| `GET` | `/agent/peer/{tenant_id}/public-key` | 获取特定租户的公钥 |  
| `POST` | `/agent/rotate-keys` | 旋转加密密钥 |  
| `GET` | `/agent/capabilities` | 获取代理的加密能力信息 |  
| `POST` | `/agent/initialize` | 为租户初始化加密设置 |  
| `GET` | `/agent/bootstrap` | 获取代理的启动配置信息 |  

### 获取公钥  
**GET** `/agent/public-key`  
**GET** `/agent/peer/{tenant_id}/public-key` – 用于与其他租户进行加密通信。  

### 加密工作原理：**  
每个租户在初始化时会生成一对 X25519 密钥。发送消息时，服务器会执行 ECDH 密钥交换，并使用 AES-256-GCM 进行加密；接收端负责解密。所有密钥管理均通过服务器完成。  

### A2A JSON-RPC  
核心的 A2A 操作均通过 JSON-RPC 2.0 协议进行，所有代理间通信均通过此端点处理：  
| 方法 | 端点 | 描述 |  
|------|---------|-------------|  
| `POST` | `/a2a/{tenant_id}/{session_id}/{webhook_id}` | 完整权限范围的端点（推荐） |  
| `POST` | `/a2a/{tenant_id}/{session_id}` | 基于租户和会话的权限范围 |  
| `POST` | `/a2a/{session_id}` | 基于会话的权限范围 |  
| `POST` | `/a2a` | 通用端点（适用于首个活跃会话） |  
| `GET` | `/a2a/schema` | 获取 A2A 协议的详细信息 |  

### 请求与响应格式：  
（具体请求/响应格式请参考相关代码块。）  

### 可用方法：  
| 方法 | 功能 |  
|------|---------|-------------|  
| `agent.message.send` | 通过 A2A 发送 WhatsApp 消息 |  
| `agent.group.create` | 创建新的 WhatsApp 群组 |  
| `agent.group.invite` | 邀请成员加入群组 |  
| `agent.group.list` | 列出可用群组 |  
| `group.getContext` | 获取群组元数据和最近活动 |  
| `webhook_manager` | 通过 A2A 管理 Webhook |  

### 示例操作：  
- **发现 MoltFlow 代理**  
- **通过 A2A 发送消息**  
- **设置内容策略规则**  
- **测试消息是否符合策略**  

**安全机制：**  
MoltFlow 采用多层安全防护机制：TLS 1.3（传输层加密）、X25519 ECDH（密钥交换）、AES-256-GCM（消息加密）、API 密钥/JWT（身份验证）、AgentSafeguard（输入验证）、A2AContentFilter（内容过滤规则）以及速率限制机制。所有加密密钥管理均由服务器处理；外部代理仅需使用 `MOLTFLOW_API_KEY` 进行身份验证。  

**错误响应：**  
遵循标准的 HTTP 错误代码（如 400、401、403 等），同时提供详细的 JSON-RPC 错误代码（如 -32600 等）。  

**相关功能：**  
- **moltflow**：核心 API（会话管理、消息发送、群组管理、标签设置、Webhook 配置）  
- **moltflow-outreach**：批量消息发送、定时消息发送、自定义群组管理  
- **moltflow-leads**：潜在客户检测、流程跟踪、CSV/JSON 数据导出  
- **moltflow-ai**：智能自动回复、语音转录、知识库管理  
- **moltflow-reviews**：评论收集与评价管理  
- **moltflow-admin**：平台管理、用户管理、计划配置