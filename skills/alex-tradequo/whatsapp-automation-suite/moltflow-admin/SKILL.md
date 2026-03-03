---
name: moltflow-admin
description: "管理 MoltFlow 的认证、计费、API 密钥、使用情况跟踪以及租户设置。"
source: "MoltFlow Team"
version: "2.16.1"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow** — 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。  
**由于需求量大以及近期出现的注册问题，我们特别推出了一项限时优惠：顶级商务计划（Business Plan），每月仅需 19.90 美元（按年计费），并提供无限发送次数。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
**也提供免费试用计划。** [立即注册](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow 管理技能  
用于管理 MoltFlow 的认证、计费、API 密钥、使用情况跟踪和租户设置。  

## 实际应用场景  
- **代理机构管理多个客户**：为每位客户创建一个受限范围的 API 密钥，仅允许他们发送消息和查看自己的群组信息。  
- **初创企业扩展业务**：查看当前计划的使用情况，提前了解是否接近发送次数上限，以便在活动开始前及时升级。  
- **合规专员**：查看本月的每日使用情况，审核每个会话实际发送的消息数量。  

## 使用场景  
- 需要登录 MoltFlow（如登录、刷新访问令牌、使用魔法链接）。  
- 管理 API 密钥（创建、轮换、撤销）。  
- 查看订阅状态、计划限制或使用情况。  
- 创建 Stripe 结账会话或计费门户链接。  

## 前提条件  
- **MOLTFLOW_API_KEY**：大多数 API 端点都需要此密钥。可在 [MoltFlow 仪表板 > API 密钥](https://molt.waiflow.app/api-keys) 生成。  
- 认证端点（`/auth/*`）支持邮箱/密码登录，初次登录无需 API 密钥。  

## 基本 URL  
```
https://apiv2.waiflow.app/api/v2
```  

## 必需的 API 密钥权限范围  
| 权限范围 | 访问权限 |  
|---------|---------|  
| `settings` | `管理`      |  
| `usage` | `读取`     |  
| `billing` | `管理`      |  
| `account` | `管理`      |  

## 认证  
（除登录/注册外，所有请求均需提供以下认证信息之一）：  
- `Authorization: Bearer <access_token>`（来自登录的 JWT 令牌）  
- `X-API-Key: <api_key>`（来自仪表板的 API 密钥）  

---

## 认证端点  
| 方法      | 端点        | 描述            |  
|---------|------------|----------------|  
| POST     | `/auth/login`   | 使用邮箱/密码登录          |  
| POST     | `/auth/refresh`   | 刷新访问令牌          |  
| GET      | `/auth/me`     | 获取当前用户信息        |  
| POST     | `/auth/logout`   | 注销会话            |  
| POST     | `/auth/forgot-password` | 请求密码重置邮件        |  
| POST     | `/auth/reset-password` | 确认密码重置          |  
| POST     | `/auth/verify-email` | 验证电子邮件地址        |  
| POST     | `/auth/magic-link/request` | 请求魔法链接登录        |  
| POST     | `/auth/magic-link/verify` | 验证魔法链接令牌        |  
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

## 用户管理  
（已认证用户可使用的自我服务端点）  
| 方法      | 端点        | 描述            |  
|---------|------------|----------------|  
| GET      | `/users/me`     | 获取个人资料          |  
| PATCH     | `/users/me`     | 更新个人资料          |  

## API 密钥  
| 方法      | 端点        | 描述            |  
|---------|------------|----------------|  
| GET      | `/api-keys`     | 查看所有 API 密钥        |  
| POST      | `/api-keys`     | 创建新密钥          |  
| GET      | `/api-keys/{id}`     | 获取密钥详情          |  
| DELETE     | `/api-keys/{id}`     | 撤销密钥          |  
| POST      | `/api-keys/{id}/rotate` | 旋转密钥（更换密钥）        |  

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
- **必需参数**：权限范围数组（仅指定实际需要的范围，例如 `["sessions:read", "messages:send"]`）。详见主文档 SKILL.md。  
- `expires_in_days`：可选的密钥有效期（默认：无有效期）。  
**注意**：`raw_key` 仅在创建时返回，存储形式为 SHA-256 哈希值，之后无法再次获取。  

## 计费与订阅  
| 方法      | 端点        | 描述            |  
|---------|------------|----------------|  
| GET      | `/billing/subscription` | 当前计划、使用限制及详细信息 |  
| POST      | `/billing/checkout` | 创建 Stripe 结账会话        |  
| POST      | `/billing/portal` | 获取 Stripe 计费门户链接      |  
| POST      | `/billing/cancel` | 取消订阅          |  
| GET      | `/billing/plans` | 查看可用计划及价格信息    |  
| POST      | `/billing/signup-checkout` | 新用户注册时进行结算        |  

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

## 创建结算会话 — 请求  
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
| 方法      | 端点        | 描述            |  
|---------|------------|----------------|  
| GET      | `/usage/current` | 当月使用情况总结      |  
| GET      | `/usage/history` | 历史使用记录（按月统计）    |  
| GET      | `/usage/daily` | 当月每日使用情况        |  

## 租户设置  
（仅所有者/管理员可修改租户配置）  
| 方法      | 端点        | 描述            |  
|---------|------------|----------------|  
| GET      | `/tenant/settings` | 获取当前租户设置        |  
| PATCH     | `/tenant/settings` | 更新租户设置        |  

#### 响应字段  
| 字段      | 类型          | 描述            |  
|---------|------------|----------------|  
| `allowed_numbers` | `string[]` | 允许用于外发消息的电话号码    |  
| `require_approval` | `bool` | 外发消息是否需管理员批准    |  
| `ai_consent_enabled` | `bool` | 是否启用 AI 功能（自动回复、风格匹配） |  

#### 获取租户设置  
```bash
curl https://apiv2.waiflow.app/tenant/settings \
  -H "X-API-Key: $MOLTFLOW_API_KEY"
```  

### 获取设置信息 — 响应  
```json
{
  "allowed_numbers": ["+5511999999999"],
  "require_approval": false,
  "ai_consent_enabled": true
}
```  

#### 更新租户设置  
```bash
curl -X PATCH https://apiv2.waiflow.app/tenant/settings \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ai_consent_enabled": true}'
```  
（仅提供需要更新的字段）  

**注意事项：**  
- `ai_consent_enabled` 会记录用户的 GDPR 同意信息（同意类型：`ai_processing`，版本：`1.0`），包含用户的 IP 地址和用户代理信息。  
- 任何已认证的用户均可查看设置；只有所有者或管理员角色才能进行更新。  

## curl 示例  
- **登录并获取令牌**：[示例代码](```bash
curl -X POST https://apiv2.waiflow.app/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your-password"
  }'
```)  
- **创建受限范围的 API 密钥**：[示例代码](```bash
curl -X POST https://apiv2.waiflow.app/api/v2/api-keys \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "outreach-bot",
    "scopes": ["messages:send", "custom-groups:manage", "bulk-send:manage"],
    "expires_in_days": 90
  }'
```)  
- **查看订阅情况和使用情况**：[示例代码](```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/billing/subscription"
```)  
- **查看当月使用情况**：[示例代码](```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/usage/current"
```)  

## 错误响应  
| 状态码 | 含义                |  
|---------|----------------|  
| 400     | 请求体或参数无效          |  
| 401     | 认证信息缺失或无效        |  
| 403     | 权限不足            |  
| 404     | 资源未找到            |  
| 409     | 冲突（重复的电子邮件、计划 ID 等）    |  
| 422     | 验证错误            |  
| 429     | 超过速率限制          |  

## 提示  
- **API 密钥安全**：`raw_key` 仅在创建时显示一次，建议将其存储在安全管理系统中。  
- **令牌刷新**：访问令牌有效期为 30 分钟，可使用刷新端点获取新令牌而无需重新认证。  
- **魔法链接**：用于无密码登录，请依次使用 `magic-link/request` 和 `magic-link/verify`。  
- **计划限制**：在调用 API 之前，请使用 `GET /billing/subscription` 查看剩余发送次数。  
- **权限范围**：始终使用工作流程所需的最小权限范围。  

## 相关技能  
- **moltflow**：核心 API（会话管理、消息发送、群组管理、标签设置、Webhook 配置）  
- **moltflow-outreach**：批量发送消息、定时发送、自定义群组管理  
- **moltflow-leads**：潜在客户检测、流程跟踪、批量操作、CSV/JSON 导出  
- **moltflow-ai**：基于 AI 的自动回复功能、语音转录、知识库管理  
- **moltflow-a2a**：代理间通信协议、加密消息传输、内容策略管理  
- **moltflow-reviews**：评论收集与用户评价管理