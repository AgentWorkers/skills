---
name: moltflow-admin
description: "通过管理API来管理MoltFlow平台的认证、用户、计费、API密钥以及租户设置。"
source: "MoltFlow Team"
version: "2.1.0"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---

**MoltFlow** — 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。  
**由于需求量大以及近期出现的注册问题，我们特别推出了一项限时优惠：顶级 Business 计划，每月仅需 19.90 美元（按年计费），并提供无限使用额度。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
**也提供免费试用计划。** [立即注册](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow 管理技能  
用于管理 MoltFlow 的认证、用户、计费、API 密钥、使用情况跟踪及平台配置。  

## 使用场景  
- 登录 MoltFlow（登录、刷新访问令牌、请求魔法链接）  
- 管理 API 密钥（创建、轮换、撤销）  
- 查看订阅状态、计划限制或使用情况  
- 创建 Stripe 结账会话或计费门户链接  
- 以管理员身份管理用户（列出、暂停、激活用户）  
- 查看平台统计数据、租户信息或审计日志（超级管理员权限）  
- 管理计划和定价信息（超级管理员权限）  

**触发语句**：  
“登录 MoltFlow”、“创建 API 密钥”、“查看订阅信息”、“计费门户”、“管理员统计数据”、“列出用户”、“管理计划”、“使用报告”  

## 前提条件  
- **MOLTFLOW_API_KEY**：大多数接口都需要此密钥。可在 [MoltFlow 控制台 > API 密钥](https://molt.waiflow.app/api-keys) 生成。  
- 认证接口（`/auth/*`）支持邮箱/密码登录，初次登录无需 API 密钥。  
- 管理接口需要超级管理员权限。  

## 基础 URL  
```
https://apiv2.waiflow.app/api/v2
```  

## 必需的 API 密钥权限范围  
| 权限范围 | 访问权限 |  
|---------|---------|  
| `settings` | `管理` |  
| `usage` | `读取` |  
| `billing` | `管理` |  
| `account` | `管理` |  

## 认证  
所有请求（登录/注册除外）都需要以下认证信息之一：  
- `Authorization: Bearer <access_token>`（来自登录的 JWT 令牌）  
- `X-API-Key: <api_key>`（来自控制台的 API 密钥）  

---

## 认证接口  
| 方法 | 接口地址 | 描述 |  
|--------|---------|-------------|  
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
```json
// POST /auth/login
{
  "email": "user@example.com",
  "password": "your-password"
}

// Response
{
  "access_token": "eyJhbGciOi...",
  "refresh_token": "eyJhbGciOi...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "owner",
    "tenant_id": "uuid"
  }
}
```  

---

## 用户管理  
**自我服务用户界面（已认证用户）**：  
| 方法 | 接口地址 | 描述 |  
|--------|---------|-------------|  
| GET | `/users/me` | 获取个人资料 |  
| PATCH | `/users/me` | 更新个人资料 |  
| DELETE | `/users/me` | 删除个人账户（涉及 32 个以上数据库表） |  

**管理员用户管理（仅限超级管理员）**：  
| 方法 | 接口地址 | 描述 |  
|--------|---------|-------------|  
| GET | `/admin/users` | 列出所有用户（可分页、搜索） |  
| GET | `/admin/users/{id}` | 获取用户详情 |  
| PATCH | `/admin/users/{id}` | 更新用户信息 |  
| POST | `/admin/users/{id}/suspend` | 暂停用户账户 |  
| POST | `/admin/users/{id}/activate` | 恢复用户账户 |  
| DELETE | `/admin/users/{id}` | 删除用户账户（仅限管理员） |  

---

## API 密钥  
| 方法 | 接口地址 | 描述 |  
|--------|---------|-------------|  
| GET | `/api-keys` | 列出所有 API 密钥 |  
| POST | `/api-keys` | 创建新密钥 |  
| GET | `/api-keys/{id}` | 获取密钥详情 |  
| DELETE | `/api-keys/{id}` | 撤销密钥 |  
| POST | `/api-keys/{id}/rotate` | 旋转密钥（生成新密钥） |  

### 创建 API 密钥 — 请求/响应  
```json
// POST /api-keys
{
  "name": "outreach-bot",
  "scopes": ["messages:send", "custom-groups:manage", "bulk-send:manage"],
  "expires_in_days": 90
}

// Response (raw key shown ONCE — save it immediately)
{
  "id": "uuid",
  "name": "outreach-bot",
  "key_prefix": "mf_abc1",
  "raw_key": "mf_abc1234567890abcdef...",
  "scopes": ["messages:send", "custom-groups:manage", "bulk-send:manage"],
  "expires_at": "2026-04-15T10:00:00Z",
  "created_at": "2026-01-15T10:00:00Z",
  "is_active": true
}
```  
- **必需的权限范围**：指定所需的范围（例如 `["sessions:read", "messages:send"]`）。详细权限范围请参阅主文档 SKILL.md。  
- `expires_in_days`：可选的密钥有效期（默认为无有效期）。  
**注意**：`raw_key` 仅在创建时返回，之后会以 SHA-256 哈希形式存储，无法再次获取。  

---

## 计费与订阅  
| 方法 | 接口地址 | 描述 |  
|--------|---------|-------------|  
| GET | `/billing/subscription` | 查看当前计划、使用限制和用量信息 |  
| POST | `/billing/checkout` | 创建 Stripe 结账会话 |  
| POST | `/billing/portal` | 获取 Stripe 计费门户链接 |  
| POST | `/billing/cancel` | 取消订阅 |  
| GET | `/billing/plans` | 查看可用计划和定价信息 |  
| POST | `/billing/signup-checkout` | 为新用户创建计费会话 |  

### 查看订阅信息 — 响应  
```json
{
  "plan_id": "pro",
  "display_name": "Pro",
  "status": "active",
  "billing_cycle": "monthly",
  "current_period_end": "2026-02-15T00:00:00Z",
  "limits": {
    "max_sessions": 3,
    "max_messages_per_month": 5000,
    "max_groups": 10,
    "max_labels": 50,
    "ai_replies_per_month": 500
  },
  "usage": {
    "sessions": 2,
    "messages_this_month": 1247,
    "groups": 5,
    "labels": 12,
    "ai_replies_this_month": 89
  }
}
```  

### 创建结账会话 — 请求  
```json
// POST /billing/checkout
{
  "plan_id": "pro",
  "billing_cycle": "monthly"
}

// Response
{
  "checkout_url": "https://checkout.stripe.com/c/pay/cs_live_...",
  "session_id": "cs_live_..."
}
```  

## 使用情况跟踪  
| 方法 | 接口地址 | 描述 |  
|--------|---------|-------------|  
| GET | `/usage/current` | 当月使用情况总结 |  
| GET | `/usage/history` | 按月查看历史使用记录 |  
| GET | `/usage/daily` | 当月每日使用明细 |  

## 租户设置  
**仅限所有者/管理员修改租户配置**：  
| 方法 | 接口地址 | 描述 |  
|--------|---------|-------------|  
| GET | `/tenant/settings` | 获取当前租户设置 |  
| PATCH | `/tenant/settings` | 更新租户设置（仅限所有者/管理员） |  

**响应字段**：  
| 字段 | 类型 | 描述 |  
|-------|------|-------------|  
| `allowed_numbers` | `string[]` | 允许发送消息的电话号码 |  
| `require_approval` | `bool` | 发送消息是否需要管理员批准 |  
| `ai_consent_enabled` | `bool` | 是否启用 AI 功能（自动回复、风格训练） |  
| `chat_history_access_enabled` | `bool` | 是否允许访问聊天记录（仅限超级管理员） |  

> **隐私设置说明**：`chat_history_access_enabled` 控制具有 `messages:read` 权限的 API 密钥是否可以访问聊天记录。默认值为 `false`；需在 **设置 > 账户 > 数据访问** 中手动启用。发送消息功能不受影响。禁用该功能时，相关功能（如自动回复、AI 模式等）将自动跳过。  

#### 获取租户设置  
```bash
curl https://apiv2.waiflow.app/tenant/settings \
  -H "X-API-Key: $MOLTFLOW_API_KEY"
```  

### 更新租户设置  
```json
{
  "allowed_numbers": ["+5511999999999"],
  "require_approval": false,
  "ai_consent_enabled": true,
  "chat_history_access_enabled": false
}
```  

### 更新设置 — 请求体  
仅提供需要更新的字段。  

**备注**：  
- `ai_consent_enabled` 记录用户的 GDPR 同意信息（同意类型 `ai_processing`，版本 `1.0`），包含用户 IP 和用户代理信息。  
- `chat_history_access_enabled` 默认值为 `false`。启用该功能后，具有 `messages:read` 权限的 API 密钥才能访问聊天记录。  
- 任何已认证用户均可查看设置，但仅所有者或管理员才能进行修改。  

## GDPR — 数据删除  
**删除租户内的特定电话号码数据**：  
此功能支持 GDPR 的“数据删除权”（第 17 条）。  
| 方法 | 接口地址 | 描述 |  
|--------|---------|-------------|  
| POST | `/gdpr/contact-erasure` | 删除指定电话号码的所有数据 |  

**请求体**：  
```json
{
  "phone": "972501234567@c.us",
  "reason": "gdpr_request"
}
```  
| 字段 | 类型 | 是否必填 | 描述 |  
|-------|------|-------------|  
| `phone` | `string` | 要删除的电话号码（可包含或不含 `@c.us` 后缀） |  
| `reason` | `string` | 删除原因（默认：`gdpr_request`） |  

**删除内容**：  
- **消息**：永久删除（包括明文和加密内容）  
- **评论**：匹配的发送者评论记录将被永久删除  
- **聊天记录**：联系电话和姓名会被屏蔽（匿名处理）  
- **群组成员**：联系电话和姓名会被屏蔽（匿名处理）  
- **审计日志**：记录电话号码的 SHA-256 哈希值及删除操作详情  

**注意**：删除操作仅针对指定租户生效。加密字段会在内存中解密后进行删除。  

## 账户删除  
**不可逆操作**。请确保充分了解后果后执行。删除操作需要输入密码进行确认。  
此操作会删除您的账户及所有关联数据。  

**删除账户后**：  
账户信息将永久删除，涉及 32 个以上数据库表（包括消息、会话记录、API 密钥、用户资料等）。  

## 管理接口（仅限超级管理员）  
**高权限操作**。这些接口需要超级管理员权限，仅应使用专用管理员账户访问。切勿将超级管理员凭据泄露给第三方集成服务。  
| 方法 | 接口地址 | 描述 |  
|--------|---------|-------------|  
| GET | `/admin/stats` | 查看平台整体统计数据 |  
| GET | `/admin/health` | 检查服务运行状态 |  
| GET | `/admin/audit-logs` | 查看审计日志 |  
| GET | `/admin/tenants` | 列出所有租户 |  
| GET | `/admin/tenants/{id}` | 查看租户详情 |  
| PATCH | `/admin/tenants/{id}` | 更新租户信息 |  
| DELETE | `/admin/tenants/{id}` | 删除租户账户（仅限管理员） |  
| POST | `/admin/tenants/{id}/reset-limits` | 重置使用限制 |  
| GET | `/admin/tenants/{id}/effective-limits` | 查看当前计划限制 |  
| GET | `/admin/plans` | 查看所有计划 |  
| POST | `/admin/plans` | 创建新计划 |  
| PATCH | `/admin/plans/{id}` | 更新计划信息 |  
| DELETE | `/admin/plans/{id}` | 删除计划 |  
| POST | `/admin/plans/{id}/stripe-sync` | 将计划信息同步到 Stripe |  
| POST | `/admin/plans/stripe-sync-all` | 同步所有计划到 Stripe |  

## curl 示例  
### 1. 登录并获取令牌  
```bash
curl -X POST https://apiv2.waiflow.app/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "your-password"
  }'
```  

### 2. 创建 API 密钥  
```bash
curl -X POST https://apiv2.waiflow.app/api/v2/api-keys \
  -H "Authorization: Bearer eyJhbGciOi..." \
  -H "Content-Type: application/json" \
  -d '{"name": "outreach-bot", "scopes": ["messages:send", "custom-groups:manage", "bulk-send:manage"], "expires_in_days": 90}'
```  

### 3. 查看订阅信息和限制  
```bash
curl https://apiv2.waiflow.app/api/v2/billing/subscription \
  -H "X-API-Key: mf_your_api_key_here"
```  

### 4. 查看平台统计数据（超级管理员）  
```bash
curl https://apiv2.waiflow.app/api/v2/admin/stats \
  -H "Authorization: Bearer eyJhbGciOi..."
```  

## 错误响应  
| 状态码 | 含义 |  
|--------|---------|  
| 400 | 请求体或参数无效 |  
| 401 | 认证失败 |  
| 403 | 权限不足（非管理员/超级管理员） |  
| 404 | 资源未找到 |  
| 409 | 冲突（重复的邮箱地址、计划 ID 等） |  
| 422 | 验证失败 |  
| 429 | 超过请求频率限制 |  

## 提示：  
- **API 密钥安全**：`raw_key` 仅在创建时显示一次，建议存储在安全管理系统中。  
- **令牌刷新**：访问令牌有效期为 30 分钟，可使用刷新接口获取新令牌而无需重新认证。  
- **魔法链接**：用于无密码登录，先调用 `magic-link/request`，再调用 `magic-link/verify`。  
- **计划限制**：在调用 API 之前，请使用 `GET /billing/subscription` 查看剩余使用额度。  
- **管理员操作**：所有管理接口都需要超级管理员权限，普通用户会收到 403 错误。  

## 相关技能：  
- **moltflow**：核心 API（会话管理、消息发送、群组管理、标签设置、Webhook 配置）  
- **moltflow-outreach**：批量发送消息、定时发送、自定义群组管理  
- **moltflow-leads**：潜在客户检测、流程跟踪、CSV/JSON 导出功能  
- **moltflow-ai**：基于 AI 的自动回复、语音转录、知识库管理  
- **moltflow-a2a**：代理间通信协议、加密消息传输、内容策略管理  
- **moltflow-reviews**：评论收集与评价管理