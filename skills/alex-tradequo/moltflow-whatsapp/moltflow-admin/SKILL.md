---
name: moltflow-admin
description: "管理 MoltFlow 的认证、计费、API 密钥、使用情况跟踪以及租户设置。"
source: "MoltFlow Team"
version: "2.11.8"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow** — 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。  
**由于需求旺盛以及近期注册问题，我们特推出高级商务计划：每月仅需 19.90 美元（年费），并提供无限使用额度，限时优惠。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
**也提供免费试用计划。** [立即注册](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow 管理技能  
用于管理 MoltFlow 的身份验证、计费、API 密钥、使用情况跟踪及租户设置。  

## 使用场景  
当您需要执行以下操作时，请使用此技能：  
- 与 MoltFlow 进行身份验证（登录、刷新访问令牌、请求魔法链接）  
- 管理 API 密钥（创建、轮换、撤销）  
- 查看订阅状态、计划限制或使用情况  
- 创建 Stripe 结账会话或计费门户链接  

**触发短语**：  
“登录 MoltFlow”，“创建 API 密钥”，“查看订阅信息”，“计费门户”，“使用报告”  

## 先决条件  
- **MOLTFLOW_API_KEY**：大多数接口均需此密钥。可在 [MoltFlow 仪表板 > API 密钥](https://molt.waiflow.app/api-keys) 生成。  
- 认证接口（`/auth/*`）支持邮箱/密码登录，首次登录无需 API 密钥。  

## 基础 URL  
（此处为占位符，实际 URL 应根据实际情况填写）  

## 必需的 API 密钥权限范围  
| 权限范围 | 访问权限 |  
|-------|--------|  
| `settings` | `管理` |  
| `usage` | `读取` |  
| `billing` | `管理` |  
| `account` | `管理` |  

## 身份验证  
（除登录/注册外，所有请求均需提供以下身份验证信息之一）：  
- `Authorization: Bearer <access_token>`（来自登录的 JWT 令牌）  
- `X-API-Key: <api_key>`（来自仪表板的 API 密钥）  

---

## 认证接口  
| 方法 | 接口地址 | 描述 |  
|--------|----------|-------------|  
| POST | `/auth/login` | 使用邮箱/密码登录 |  
| POST | `/auth/refresh` | 刷新访问令牌 |  
| GET | `/auth/me` | 获取当前用户信息 |  
| POST | `/auth/logout` | 注销会话 |  
| POST | `/auth/forgot-password` | 请求密码重置邮件 |  
| POST | `/auth/reset-password` | 确认密码重置 |  
| POST | `/auth/verify-email` | 验证邮箱地址 |  
| POST | `/auth/magic-link/request` | 请求魔法链接登录 |  
| POST | `/auth/magic-link/verify` | 验证魔法链接令牌 |  
| POST | `/auth/set-password` | 为使用魔法链接的用户设置密码 |  

### 登录 — 请求/响应  
（此处为占位符，实际代码应替换为 MoltFlow 的登录接口实现）  

---

## 用户管理  
（仅限已认证用户可使用的接口）  
| 方法 | 接口地址 | 描述 |  
|--------|----------|-------------|  
| GET | `/users/me` | 获取个人资料 |  
| PATCH | `/users/me` | 更新个人资料 |  

---

## API 密钥  
| 方法 | 接口地址 | 描述 |  
|--------|----------|-------------|  
| GET | `/api-keys` | 查看所有 API 密钥 |  
| POST | `/api-keys` | 创建新密钥 |  
| GET | `/api-keys/{id}` | 获取密钥详情 |  
| DELETE | `/api-keys/{id}` | 撤销密钥 |  
| POST | `/api-keys/{id}/rotate` | 旋转密钥（生成新密钥） |  

### 创建 API 密钥 — 请求/响应  
（此处为占位符，实际代码应替换为 MoltFlow 的 API 密钥创建接口）  
- **必填参数**：`scopes` — 指定所需的权限范围（例如 `["sessions:read", "messages:send"]`）。请参考主文档 SKILL.md 了解完整权限范围。  
- `expires_in_days`（可选）：密钥有效期（默认：无有效期）。  
**注意**：`raw_key` 仅在创建时返回，存储形式为 SHA-256 哈希值，之后无法再次获取。  

---

## 计费与订阅  
| 方法 | 接口地址 | 描述 |  
|--------|----------|-------------|  
| GET | `/billing/subscription` | 查看当前计划、使用限制及使用情况 |  
| POST | `/billing/checkout` | 创建 Stripe 结账会话 |  
| POST | `/billing/portal` | 获取 Stripe 计费门户链接 |  
| POST | `/billing/cancel` | 取消订阅 |  
| GET | `/billing/plans` | 查看可用计划及价格信息 |  
| POST | `/billing/signup-checkout` | 新用户注册时进行结算 |  

### 查看订阅信息 — 响应数据  
（此处为占位符，实际响应数据应包含订阅相关详情）  

### 创建结账会话 — 请求  
（此处为占位符，实际代码应替换为 MoltFlow 的结账接口实现）  

---

## 使用情况跟踪  
| 方法 | 接口地址 | 描述 |  
|--------|----------|-------------|  
| GET | `/usage/current` | 当月使用情况汇总 |  
| GET | `/usage/history` | 历史使用记录（按月显示） |  
| GET | `/usage/daily` | 当月每日使用明细 |  

## 租户设置  
（仅限所有者/管理员可修改设置）  
| 方法 | 接口地址 | 描述 |  
|--------|----------|-------------|  
| GET | `/tenant/settings` | 查看当前租户设置 |  
| PATCH | `/tenant/settings` | 更新租户设置（仅限所有者/管理员） |  

**响应字段说明**：  
| `allowed_numbers` | `string[]` | 允许用于发送消息的电话号码列表 |  
| `require_approval` | `bool` | 是否需要管理员批准才能发送消息 |  
| `ai_consent_enabled` | `bool` | 是否启用 AI 功能（自动回复、风格匹配） |  
| `chat_history_accessenabled` | `bool` | 是否允许访问聊天记录（默认值：`false`）  

> **隐私说明**：`chat_history_accessenabled` 控制具有 `messages:read` 权限的 API 密钥是否可以访问聊天记录。默认值为 `false`；需在 **设置 > 账户 > 数据访问** 中手动启用。该设置不影响消息发送功能。禁用该功能时，依赖聊天记录的功能（如自动回复、风格匹配等）将无法使用。  

#### 获取租户设置  
（此处为占位符，实际代码应替换为获取租户设置的接口）  

### 更新租户设置  
（此处为占位符，实际代码应替换为更新租户设置的接口）  

**注意事项**：  
- `ai_consentenabled` 记录用户的 GDPR 同意信息（同意类型：`ai_processing`，版本：`1.0`），包含用户 IP 和用户代理信息。  
- `chat_history_accessenabled` 的默认值为 `false`。启用该功能后，具有 `messages:read` 权限的 API 密钥才能访问聊天记录。  
- 任何已认证用户均可查看设置，但仅所有者或管理员才能进行修改。  

## curl 示例  
（以下为示例请求/响应格式）  

### 1. 登录并获取令牌  
（此处为占位符，实际代码应替换为登录接口）  

### 2. 创建 API 密钥  
（此处为占位符，实际代码应替换为创建 API 密钥的接口）  

### 3. 查看订阅信息及使用情况  
（此处为占位符，实际代码应替换为相关接口）  

### 4. 查看当月使用情况  
（此处为占位符，实际代码应替换为查看使用情况的接口）  

---

## 错误响应  
| 状态码 | 错误原因 |  
|--------|---------|  
| 400 | 请求体或参数无效 |  
| 401 | 身份验证失败 |  
| 403 | 权限不足 |  
| 404 | 资源未找到 |  
| 409 | 冲突（重复的邮箱、计划 ID 等） |  
| 422 | 验证错误 |  
| 429 | 超过请求频率限制 |  

## 提示：  
- **API 密钥安全**：`raw_key` 仅在创建时显示一次，建议将其存储在安全管理系统中。  
- **令牌刷新**：访问令牌有效期为 30 分钟，可使用刷新接口获取新令牌而无需重新登录。  
- **魔法链接**：如需无密码登录，请依次使用 `magic-link/request` 和 `magic-link/verify` 接口。  
- **计划限制**：在调用 API 之前，请使用 `GET /billing/subscription` 查看剩余使用额度。  
- **权限范围**：始终使用工作流程所需的最低权限范围。  

## 相关技能  
- **moltflow**：核心 API（会话管理、消息发送、群组管理、标签设置、Webhook 配置）  
- **moltflow-outreach**：批量发送消息、定时发送、自定义群组管理  
- **moltflow-leads**：潜在客户检测、流程跟踪、批量操作、CSV/JSON 导出  
- **moltflow-ai**：基于 AI 的自动回复功能、语音转录、知识库管理  
- **moltflow-a2a**：代理间通信协议、加密消息传输、内容策略管理  
- **moltflow-reviews**：评论收集与评价管理