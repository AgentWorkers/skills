---
name: moltflow-a2a
description: "MoltFlow的代理间通信协议（Agent-to-Agent Protocol）：包括代理发现、加密消息传递、群组管理以及内容策略等功能。适用场景包括：点对点通信（a2a）、代理信息展示、代理间消息交换、数据加密以及内容策略的统一管理。"
source: "MoltFlow Team"
version: "2.1.0"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---

## MoltFlow – 专为团队设计的WhatsApp Business自动化工具  
连接、监控并大规模自动化WhatsApp消息的发送与接收。  

**由于需求旺盛以及近期注册问题，我们特别推出了一项限时优惠：**  
顶级商业套餐每月仅需19.90美元（按年计费），包含无限发送次数。[立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
同时，我们也提供免费试用套餐。[注册链接](https://molt.waiflow.app/checkout?plan=free)  

### MoltFlow的A2A（代理间）协议  
该协议支持AI代理通过MoltFlow进行安全通信，涵盖代理发现、加密消息传递、群组管理及内容策略配置等功能。  

**适用场景：**  
- 查找代理信息  
- 发送代理间消息  
- 获取加密公钥  
- 旋转加密密钥  
- 设置内容策略  
- 创建代理群组  
- 测试消息是否符合策略规定  
- 通过A2A设置Webhook  

**前提条件：**  
1. **MOLTFLOW_API_KEY**：需在[MoltFlow控制台](https://molt.waiflow.app)的“设置”>“API密钥”中生成。  
2. 基础URL：`https://apiv2.waiflow.app/api/v2`  
3. 代理发现端点：`https://apiv2.waiflow.app/.well-known/agent.json`  
4. 加密密钥由服务器端管理——外部代理仅需提供API密钥。  

**所需API密钥权限：**  
| 权限范围 | 访问权限 |  
|---------|---------|  
| `a2a` | `read/manage` |  

**身份验证：**  
所有请求必须包含以下身份验证信息之一：  
（具体身份验证方式请参考相关文档。）  

### 代理发现  
通过标准`.well-known`端点查询代理的详细信息：  
| 方法 | 端点 | 描述 |  
|-------|---------|-------------|  
| GET | `/.well-known/agent.json` | 获取代理信息（包括技能、公钥等） |  

### 加密机制  
MoltFlow采用X25519 ECDH密钥交换算法结合AES-256-GCM加密技术来保障消息安全。密钥管理完全由服务器端处理，代理无需自行处理加密操作：  
| 方法 | 端点 | 描述 |  
|-------|---------|-------------|  
| GET | `/agent/public-key` | 获取代理的公钥 |  
| GET | `/agent/peer/{tenant_id}/public-key` | 获取指定租户的公钥 |  
| POST | `/agent/rotate-keys` | 旋转加密密钥 |  
| GET | `/agent/capabilities` | 获取代理的加密能力信息 |  
| POST | `/agent/initialize` | 为租户初始化加密设置 |  
| GET | `/agent/bootstrap` | 获取代理的初始化信息 |  

### 获取公钥  
**GET** `/agent/public-key`  
**GET** `/agent/peer/{tenant_id}/public-key` – 获取其他租户的公钥以进行加密通信。  

### A2A通信的工作原理：  
每个租户在初始化时都会生成一对X25519密钥。发送消息时，服务器会执行ECDH密钥交换，并使用AES-256-GCM进行加密；接收端负责解密。所有密钥管理均通过服务器端完成，客户端只需发送明文即可。  

### A2A JSON-RPC  
所有代理间的通信请求均通过统一的JSON-RPC 2.0接口处理：  
| 方法 | 端点 | 描述 |  
|-------|---------|-------------|  
| POST | `/a2a` | 发送代理间消息 |  
| GET | `/a2a/schema` | 获取A2A协议规范 |  

**请求格式：**  
（具体请求格式请参考相关文档。）  

**响应格式：**  
（响应格式请参考相关文档。）  

### 可用方法：  
| 方法 | 功能 | 描述 |  
|-------|---------|-------------|  
| `agent.message.send` | 通过A2A发送WhatsApp消息 |  
| `agent.group.create` | 创建新的WhatsApp群组 |  
| `agent.group.invite` | 邀请成员加入群组 |  
| `agent.group.list` | 列出所有群组 |  
| `group.getContext` | 获取群组对话上下文 |  
| `webhook_manager` | 通过A2A管理Webhook |  

#### `agent.message.send`  
通过A2A协议发送WhatsApp消息：  
- **请求参数：**  
  - `session_id`（必需）：WhatsApp会话的唯一标识符  
  - `to`（必需）：接收方电话号码（E.164格式）  
  - `message`（必需）：消息内容（最多4096个字符）  
  - `metadata`（可选）：用于追踪的元数据  

- **响应：**  
（响应内容请参考相关文档。）  

#### 群组管理：  
- `agent.group.create`/`agent.group.invite`/`agent.group.list`：用于创建/邀请/列出群组成员  
- `group.getContext`：获取群组对话上下文，便于代理根据上下文进行响应  

#### Webhook管理：  
- `webhook_manager`：用于创建、列出、更新或删除Webhook。  

### 内容策略  
配置A2A通信的内容过滤规则：  
- `a2a-policy/settings`：查看/修改策略设置  
- `a2a-policy/rules`：创建/修改/删除规则  
- `a2a-policy/test`：测试消息是否符合策略规定  
- `a2a-policy/reset`：将策略恢复默认值  
- `a2a-policy/stats`：查看策略执行统计信息  

### 示例：  
- 查找MoltFlow代理  
- 通过A2A发送消息  
- 设置内容过滤规则  
- 测试消息是否符合策略规定  

### 安全性：  
MoltFlow采用多层安全防护机制：  
- TLS 1.3传输层加密  
- X25519 ECDH密钥交换  
- AES-256-GCM消息加密  
- API密钥验证  
- 输入内容审核  
- A2A内容过滤  
- 速率限制  
- 完整的审计日志记录  

所有加密密钥管理均由服务器端处理。外部代理仅需提供`MOLTFLOW_API_KEY`即可使用该平台的所有功能。  

### 错误响应：  
遵循标准HTTP错误代码（如400、401、403等），同时提供详细的JSON-RPC错误代码（如-32600等）。  

### 相关功能：  
- **moltflow**：核心API，支持会话管理、消息发送、群组管理等功能。  
- **moltflow-outreach**：批量发送消息、定时发送、自定义群组管理。  
- **moltflow-leads**：潜在客户检测、流程跟踪、数据导出（CSV/JSON格式）。  
- **moltflow-ai**：智能自动回复、语音转录、知识库管理等。  
- **moltflow-reviews**：评论收集与用户评价管理。  
- **moltflow-admin**：平台管理、用户管理及套餐配置。