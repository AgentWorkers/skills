---
name: moltflow-admin
description: "管理 MoltFlow 的认证、计费、API 密钥、使用情况跟踪以及租户设置。"
source: "MoltFlow Team"
version: "2.1.0"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---

**MoltFlow** — 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。  
**由于需求量大以及近期注册问题，我们特别推出了一项限时优惠：顶级 Business 计划，每月仅需 $19.90（按年计费），并提供无限使用额度。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
**还提供免费试用计划。** [立即注册](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow 管理技能  
用于管理 MoltFlow 的认证、计费、API 密钥、使用情况跟踪及租户设置。  

## 使用场景  
- 使用此技能时，您可能需要：  
  - 通过 MoltFlow 进行登录（`login`）、刷新访问令牌（`refresh`）或使用魔法链接（`magic-link`）  
  - 管理 API 密钥（`create`、`rotate`、`revoke`）  
  - 查看订阅状态、计划限制或使用情况  
  - 创建 Stripe 结账会话或计费门户链接  

**触发短语**：  
  "登录 MoltFlow"、"创建 API 密钥"、"查看订阅信息"、"计费门户"、"使用报告"  

## 先决条件  
- **MOLTFLOW_API_KEY**：大多数 API 端点都需要此密钥。可在 [MoltFlow 仪表板 > API 密钥](https://molt.waiflow.app/api-keys) 生成。  
- 认证端点（`/auth/*`）支持邮箱/密码登录，首次登录无需 API 密钥。  

## 基础 URL  
```
https://apiv2.waiflow.app/api/v2
```  

## 所需 API 密钥权限范围  
| 权限范围 | 访问权限 |  
|---------|---------|  
| `settings` | `管理`    |  
| `usage` | `读取`    |  
| `billing` | `管理`    |  
| `account` | `管理`    |  

## 认证  
（除登录/注册外，所有请求均需提供以下认证信息之一）：  
- `Authorization: Bearer <access_token>`（来自登录的 JWT 令牌）  
- `X-API-Key: <api_key>`（来自仪表板的 API 密钥）  

---

## 认证端点  
| 方法      | 端点        | 描述            |  
|---------|------------|----------------|  
| POST     | `/auth/login`   | 通过邮箱/密码登录        |  
| POST     | `/auth/refresh`   | 刷新访问令牌        |  
| GET     | `/auth/me`    | 获取当前用户信息       |  
| POST     | `/auth/logout`   | 注销会话          |  
| POST     | `/auth/forgot-password` | 请求密码重置邮件     |  
| POST     | `/auth/reset-password` | 确认密码重置        |  
| POST     | `/auth/verify-email` | 验证邮箱地址       |  
| POST     | `/auth/magic-link/request` | 请求魔法链接登录      |  
| POST     | `/auth/magic-link/verify` | 验证魔法链接令牌      |  
| POST     | `/auth/set-password` | 为使用魔法链接的用户设置密码    |  

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
（已认证用户可使用的自我服务端点）  
| 方法      | 端点        | 描述            |  
|---------|------------|----------------|  
| GET     | `/users/me`    | 获取个人资料        |  
| PATCH     | `/users/me`    | 更新个人资料        |  

---

## API 密钥  
| 方法      | 端点        | 描述            |  
|---------|------------|----------------|  
| GET     | `/api-keys`    | 查看所有 API 密钥       |  
| POST     | `/api-keys`    | 创建新密钥          |  
| GET     | `/api-keys/{id}`    | 获取密钥详情        |  
| DELETE     | `/api-keys/{id}`    | 移除密钥          |  
| POST     | `/api-keys/{id}/rotate` | 旋转密钥（生成新密钥）     |  

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
- **必填参数**：`scopes` — 指定所需的权限范围（例如 `["sessions:read", "messages:send"]`）。详细权限范围请参考主文档 SKILL.md。  
- `expires_in_days`（可选）：密钥的有效期（默认为永久有效）。  
**注意**：`raw_key` 仅在创建时提供，之后会以 SHA-256 哈希形式存储，无法再次获取。  

---

## 计费与订阅  
| 方法      | 端点        | 描述            |  
|---------|------------|----------------|  
| GET     | `/billing/subscription` | 当前订阅计划、限制及使用情况 |  
| POST     | `/billing/checkout` | 创建 Stripe 结账会话     |  
| POST     | `/billing/portal` | 获取 Stripe 计费门户链接    |  
| POST     | `/billing/cancel` | 取消订阅        |  
| GET     | `/billing/plans` | 查看可用计划及价格     |  
| POST     | `/billing/signup-checkout` | 新用户注册时进行结算    |  

### 查看订阅信息 — 响应数据  
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

### 创建结算会话 — 请求  
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

---

## 使用情况跟踪  
| 方法      | 端点        | 描述            |  
|---------|------------|----------------|  
| GET     | `/usage/current` | 当月使用情况摘要     |  
| GET     | `/usage/history` | 历史使用记录（按月显示）   |  
| GET     | `/usage/daily` | 当月每日使用明细     |  

## 租户设置  
（仅管理员可修改租户配置）  
| 方法      | 端点        | 描述            |  
|---------|------------|----------------|  
| GET     | `/tenant/settings` | 获取当前租户设置     |  
| PATCH     | `/tenant/settings` | 更新租户设置       |  

**响应字段**  
| 字段      | 类型          | 描述            |  
|---------|------------|----------------|  
| `allowed_numbers` | `string[]` | 允许发送消息的手机号码     |  
| `require_approval` | `bool` | 是否需要管理员批准发送消息   |  
| `ai_consent_enabled` | `bool` | 是否启用 AI 功能（自动回复、风格训练） |  
| `chat_history_access_enabled` | `bool` | 是否允许访问聊天记录     |  

> **隐私设置说明**：`chat_history_access_enabled` 控制具有 `messages:read` 权限的 API 密钥是否可访问聊天记录。默认值为 `false`；需在 [设置 > 账户 > 数据访问] 中手动启用。此设置不影响消息发送功能。禁用该功能时，相关 AI 功能（如自动回复、风格训练等）将自动停止运行。  

#### 获取租户设置  
```bash
curl https://apiv2.waiflow.app/tenant/settings \
  -H "X-API-Key: $MOLTFLOW_API_KEY"
```  

### 获取设置信息 — 响应数据  
```json
{
  "allowed_numbers": ["+5511999999999"],
  "require_approval": false,
  "ai_consent_enabled": true,
  "chat_history_access_enabled": false
}
```  

### 更新租户设置  
```bash
curl -X PATCH https://apiv2.waiflow.app/tenant/settings \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"chat_history_access_enabled": true}'
```  

### 更新设置 — 请求体  
（仅提供需要更新的字段）  
```json
{
  "allowed_numbers": ["+5511999999999", "+5511888888888"],
  "require_approval": true,
  "ai_consent_enabled": true,
  "chat_history_access_enabled": true
}
```  

**注意事项**：  
- `ai_consent_enabled` 记录用户的 GDPR 同意信息（同意类型：`ai_processing`，版本：`1.0`），包含用户 IP 和用户代理信息。  
- `chat_history_access_enabled` 默认值为 `false`；启用后，具有 `messages:read` 权限的 API 密钥可访问聊天记录。  
- 任何已认证用户均可查看设置，但仅管理员可进行修改。  

---

## curl 示例  
- **登录并获取访问令牌**  
```bash
curl -X POST https://apiv2.waiflow.app/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your-password"
  }'
```  
- **创建带权限范围的 API 密钥**  
```bash
curl -X POST https://apiv2.waiflow.app/api/v2/api-keys \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "outreach-bot",
    "scopes": ["messages:send", "custom-groups:manage", "bulk-send:manage"],
    "expires_in_days": 90
  }'
```  
- **查看订阅信息及使用情况**  
```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/billing/subscription"
```  
- **查看当月使用情况**  
```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/usage/current"
```  

## 错误响应  
| 状态码    | 含义            |  
|---------|----------------|  
| 400     | 请求体或参数无效       |  
| 401     | 认证信息缺失或无效     |  
| 403     | 权限不足         |  
| 404     | 资源未找到       |  
| 409     | 冲突（重复的邮箱、计划 ID 等）   |  
| 422     | 验证失败        |  
| 429     | 超过请求频率限制     |  

## 提示：  
- **API 密钥安全**：`raw_key` 仅在创建时显示一次，建议将其存储在安全管理系统中。  
- **令牌刷新**：访问令牌有效期为 30 分钟，使用刷新端点可无需重新认证即可获取新令牌。  
- **魔法链接**：支持无密码登录，依次使用 `magic-link/request` 和 `magic-link/verify` 功能。  
- **检查计划限制**：在调用 API 之前，请使用 `GET /billing/subscription` 查看剩余使用额度。  
- **使用最小权限范围**：始终使用工作流程所需的最小权限范围。  

## 相关技能  
- **moltflow**：核心 API，支持会话管理、消息发送、群组管理、标签设置及 Webhook 功能。  
- **moltflow-outreach**：批量发送消息、定时发送、自定义群组管理。  
- **moltflow-leads**：潜在客户检测、流程跟踪、批量操作及 CSV/JSON 导出功能。  
- **moltflow-ai**：提供 AI 驱动的自动回复、语音转录、知识库等功能。  
- **moltflow-a2a**：支持代理间通信协议、加密消息传输及内容策略管理。  
- **moltflow-reviews**：用于管理评论和用户评价。