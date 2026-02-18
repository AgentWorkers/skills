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
**由于需求旺盛以及近期注册问题，我们特别推出了一项限时优惠：顶级 Business 计划，每月仅需 $19.90（按年计费），并提供无限使用额度。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
同时提供免费试用计划。 [立即注册](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow 管理技能  
用于管理 MoltFlow 的身份验证、计费、API 密钥、使用情况跟踪及租户设置。  

## 使用场景  
- 需要登录 MoltFlow（包括使用用户名/密码登录、刷新访问令牌或通过魔法链接登录）  
- 管理 API 密钥（创建、轮换、撤销）  
- 查看订阅状态、计划限制或使用情况  
- 创建 Stripe 结账会话或计费门户链接  

## 先决条件  
- **MOLTFLOW_API_KEY**：大多数 API 端点都需要此密钥。可在 [MoltFlow 仪表板 > API 密钥](https://molt.waiflow.app/api-keys) 生成。  
- 认证端点（`/auth/*`）支持使用电子邮件/密码进行初始登录，无需 API 密钥。  

## 基础 URL  
（此处应填写 MoltFlow 的基础 URL，但文档中未提供具体信息。）  

## 必需的 API 密钥权限范围  
| 权限范围 | 访问权限 |  
|---------|---------|  
| `settings` | `管理`    |  
| `usage` | `读取`    |  
| `billing` | `管理`    |  
| `account` | `管理`    |  

## 身份验证  
所有请求（登录/注册除外）都需要以下身份验证信息之一：  
- `Authorization: Bearer <access_token>`（来自登录的 JWT 令牌）  
- `X-API-Key: <api_key>`（来自仪表板的 API 密钥）  

---

## 认证端点  
| 方法      | 端点        | 描述                        |  
|---------|------------|-------------------------|  
| POST     | `/auth/login`   | 使用电子邮件/密码登录                |  
| POST     | `/auth/refresh`   | 刷新访问令牌                  |  
| GET      | `/auth/me`     | 获取当前用户信息                |  
| POST     | `/auth/logout`   | 注销会话                    |  
| POST     | `/auth/forgot-password` | 请求密码重置邮件                |  
| POST     | `/auth/reset-password` | 确认密码重置                |  
| POST     | `/auth/verify-email` | 验证电子邮件地址                |  
| POST     | `/auth/magic-link/request` | 请求魔法链接登录                |  
| POST     | `/auth/magic-link/verify` | 验证魔法链接令牌                |  
| POST     | `/auth/set-password` | 为使用魔法链接的用户设置密码            |  

### 登录 — 请求/响应  
（此处应包含登录相关的请求和响应格式，但文档中未提供具体内容。）  

---

## 用户管理  
（仅限已认证用户可使用的自我服务端点）  
| 方法      | 端点        | 描述                        |  
|---------|------------|-------------------------|  
| GET      | `/users/me`     | 获取个人资料                    |  
| PATCH     | `/users/me`     | 更新个人资料                    |  

## API 密钥  
| 方法      | 端点        | 描述                        |  
|---------|------------|-------------------------|  
| GET      | `/api-keys`     | 查看所有 API 密钥                |  
| POST     | `/api-keys`     | 创建新的 API 密钥                |  
| GET      | `/api-keys/{id}`     | 获取密钥详细信息                |  
| DELETE     | `/api-keys/{id}`     | 撤销密钥                    |  
| POST     | `/api-keys/{id}/rotate` | 旋转密钥（生成新密钥）              |  

### 创建 API 密钥 — 请求/响应  
（此处应包含创建 API 密钥的请求和响应格式，但文档中未提供具体内容。）  
- **必填参数**：`scopes`（权限范围数组，例如 `["sessions:read", "messages:send"]`）  
- **可选参数**：`expires_in_days`（密钥有效期，单位为天，默认为无有效期）  
**注意**：`raw_key` 仅在创建时返回，之后会以 SHA-256 哈希形式存储，无法再次获取。  

---

## 计费与订阅  
| 方法      | 端点        | 描述                        |  
|---------|------------|-------------------------|  
| GET      | `/billing/subscription` | 当前订阅计划、使用限制及使用情况        |  
| POST     | `/billing/checkout` | 创建 Stripe 结账会话                |  
| POST     | `/billing/portal` | 获取 Stripe 计费门户链接            |  
| POST     | `/billing/cancel` | 取消订阅                    |  
| GET      | `/billing/plans`     | 查看可用计划及价格信息            |  
| POST     | `/billing/signup-checkout` | 新用户注册时进行结算                |  

### 查看订阅信息 — 响应  
（此处应包含订阅相关的响应内容，但文档中未提供具体内容。）  

## 创建结算会话 — 请求  
（此处应包含创建结算会话的请求格式，但文档中未提供具体内容。）  

## 使用情况跟踪  
| 方法      | 端点        | 描述                        |  
|---------|------------|-------------------------|  
| GET      | `/usage/current` | 当月使用情况总结                |  
| GET      | `/usage/history` | 历史使用情况（按月显示）            |  
| GET      | `/usage/daily` | 当月每日使用情况明细            |  

## 租户设置  
（仅限所有者/管理员可修改的租户配置）  
| 方法      | 端点        | 描述                        |  
|---------|------------|-------------------------|  
| GET      | `/tenant/settings` | 获取当前租户设置                |  
| PATCH     | `/tenant/settings` | 更新租户设置（仅限所有者/管理员）        |  

#### 响应字段  
| 字段      | 类型        | 描述                        |  
|---------|------------|-------------------------|  
| `allowed_numbers` | `string[]` | 允许用于发送消息的电话号码            |  
| `require_approval` | `bool` | 是否需要管理员批准才能发送消息          |  
| `ai_consentenabled` | `bool` | 是否启用 AI 功能（自动回复、风格匹配等）        |  

#### 获取租户设置  
（此处应包含获取租户设置的响应内容，但文档中未提供具体内容。）  

### 更新租户设置  
（此处应包含更新租户设置的请求和响应格式，但文档中未提供具体内容。）  
**注意**：`ai_consentenabled` 会记录用户的 GDPR 同意信息（同意类型为 `ai_processing`，版本为 `1.0`），并包含用户的 IP 地址和用户代理信息。  
仅所有者或管理员角色才能更新这些设置。  

## curl 示例  
- **登录并获取令牌**  
- **创建特定权限范围的 API 密钥**  
- **查看订阅信息和使用情况**  
- **查看当月使用情况**  

---

## 错误响应  
| 状态码    | 含义                        |  
|---------|-------------------------|  
| 400     | 请求体或参数无效                |  
| 401     | 身份验证失败                    |  
| 403     | 权限不足                    |  
| 404     | 资源未找到                    |  
| 409     | 冲突（例如重复的电子邮件地址或计划 ID）          |  
| 422     | 验证失败                    |  
| 429     | 超过请求频率限制                |  

## 提示  
- **API 密钥安全**：`raw_key` 仅在创建时显示一次，应妥善存储在密钥管理工具中。  
- **令牌刷新**：访问令牌有效期为 30 分钟，可使用刷新端点获取新令牌而无需重新登录。  
- **魔法链接**：用于无密码登录，先使用 `magic-link/request`，再使用 `magic-link/verify`。  
- **计划限制**：在调用 API 之前，请使用 `GET /billing/subscription` 查看剩余使用额度。  
- **权限范围**：始终使用工作流程所需的最小权限范围。  

## 相关技能  
- **moltflow**：核心 API（会话管理、消息发送、群组管理、标签设置、Webhook 配置）  
- **moltflow-outreach**：批量发送消息、定时发送、自定义群组管理  
- **moltflow-leads**：潜在客户检测、流程跟踪、批量操作、CSV/JSON 导出  
- **moltflow-ai**：基于 AI 的自动回复功能、语音转录、知识库管理  
- **moltflow-a2a**：代理间通信协议、加密消息传输、内容策略管理  
- **moltflow-reviews**：评论收集与评价管理