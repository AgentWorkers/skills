---
name: moltflow-admin
description: "通过管理员API来管理MoltFlow平台的认证、用户、计费、API密钥以及租户设置。"
source: "MoltFlow Team"
version: "1.6.0"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disableModelInvocation: true
---

> **MoltFlow** — 专为团队设计的 WhatsApp Business 自动化工具。支持大规模地连接、监控和自动化 WhatsApp 操作。  
> 限时优惠：[年度套餐 $239.90/年 — 节省 71%](https://molt.waiflow.app/signup)

# MoltFlow 管理员技能  
用于管理 MoltFlow 的认证、用户、计费、API 密钥、使用情况跟踪以及平台配置。  

## 使用场景  
当您需要执行以下操作时，请使用此技能：  
- 使用 MoltFlow 进行登录（login）、刷新访问令牌（token refresh）或请求魔法链接（magic link）  
- 管理 API 密钥（create、rotate、revoke）  
- 查看订阅状态、套餐限制或使用情况  
- 创建 Stripe 结账会话或计费门户链接  
- 以管理员身份管理用户（list、suspend、activate）  
- 查看平台统计数据、租户信息或审计日志（仅限超级管理员）  
- 管理套餐和定价信息（仅限超级管理员）  

**触发短语**：  
“登录 MoltFlow”（login to MoltFlow）、“创建 API 密钥”（create API key）、“检查订阅状态”（check subscription）、“计费门户”（billing portal）、“管理员统计数据”（admin stats）、“列出用户”（list users）、“管理套餐”（manage plans）、“使用情况报告”（usage report）  

## 先决条件  
- **MOLTFLOW_API_KEY**：大多数 API 端点都需要此密钥。可在 [MoltFlow 仪表板 > API 密钥](https://molt.waiflow.app/api-keys) 生成。  
- 认证端点（`/auth/*`）支持电子邮件/密码登录，初次登录无需 API 密钥。  
- 管理员端点需要超级管理员权限（superadmin role）。  

## 基本 URL  
```
https://apiv2.waiflow.app/api/v2
```  

## 认证  
所有请求（登录/注册除外）都需要提供以下认证信息之一：  
- `Authorization: Bearer <access_token>`（来自登录的 JWT 令牌）  
- `X-API-Key: <api_key>`（来自仪表板的 API 密钥）  

---

## 认证端点  
| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| POST | `/auth/login` | 使用电子邮件/密码登录 |  
| POST | `/auth/refresh` | 刷新访问令牌 |  
| GET | `/auth/me` | 获取当前用户信息 |  
| POST | `/auth/logout` | 注销会话 |  
| POST | `/auth/forgot-password` | 请求密码重置邮件 |  
| POST | `/auth/reset-password` | 确认密码重置 |  
| POST | `/auth/verify-email` | 验证电子邮件地址 |  
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
**已认证用户的自我服务功能**：  
| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| GET | `/users/me` | 获取个人资料 |  
| PATCH | `/users/me` | 更新个人资料 |  
| DELETE | `/users/me` | 删除个人账户（仅限管理员） |  

**管理员用户管理（仅限超级管理员）**：  
| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| GET | `/admin/users` | 列出所有用户（可分页、搜索） |  
| GET | `/admin/users/{id}` | 获取用户详情 |  
| PATCH | `/admin/users/{id}` | 更新用户信息 |  
| POST | `/admin/users/{id}/suspend` | 暂停用户账户 |  
| POST | `/admin/users/{id}/activate` | 恢复用户账户 |  
| DELETE | `/admin/users/{id}` | 删除用户账户（仅限管理员） |  

---

## API 密钥  
| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| GET | `/api-keys` | 查看所有 API 密钥 |  
| POST | `/api-keys` | 创建新密钥 |  
| GET | `/api-keys/{id}` | 获取密钥详情 |  
| DELETE | `/api-keys/{id}` | 取消密钥 |  
| POST | `/api-keys/{id}/rotate` | 旋转密钥（生成新密钥） |  

### 创建 API 密钥 — 请求/响应  
**注意**：`raw_key` 仅在创建密钥时显示一次，之后会以 SHA-256 哈希值的形式存储，无法再次获取。  

---

## 计费与订阅  
| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| GET | `/billing/subscription` | 查看当前套餐、使用限制和用量情况 |  
| POST | `/billing/checkout` | 创建 Stripe 结账会话 |  
| POST | `/billing/portal` | 获取 Stripe 计费门户链接 |  
| POST | `/billing/cancel` | 取消订阅 |  
| GET | `/billing/plans` | 查看可用套餐和价格信息 |  
| POST | `/billing/signup-checkout` | 为新用户创建计费会话 |  

### 查看订阅状态 — 响应  
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

---

## 使用情况跟踪  
| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| GET | `/usage/current` | 当月使用情况总结 |  
| GET | `/usage/history` | 按月份划分的历史使用记录 |  
| GET | `/usage/daily` | 当月每日使用明细 |  

---

## 管理员端点（仅限超级管理员）  
这些端点需要超级管理员权限：  
| 方法 | 端点 | 描述 |  
|--------|----------|-------------|  
| GET | `/admin/stats` | 全平台统计数据 |  
| GET | `/admin/health` | 服务健康检查 |  
| GET | `/admin/audit-logs` | 审计日志查看器 |  
| GET | `/admin/tenants` | 列出所有租户 |  
| GET | `/admin/tenants/{id}` | 获取租户详情 |  
| PATCH | `/admin/tenants/{id}` | 更新租户信息 |  
| DELETE | `/admin/tenants/{id}` | 删除租户账户（仅限管理员） |  
| POST | `/admin/tenants/{id}/reset-limits` | 重置租户使用限制 |  
| GET | `/admin/tenants/{id}/effective-limits` | 查看已解决的套餐限制 |  
| GET | `/admin/plans` | 查看所有套餐 |  
| POST | `/admin/plans` | 创建新套餐 |  
| PATCH | `/admin/plans/{id}` | 更新套餐信息 |  
| DELETE | `/admin/plans/{id}` | 删除套餐 |  
| POST | `/admin/plans/{id}/stripe-sync` | 将套餐信息同步到 Stripe |  
| POST | `/admin/plans/stripe-sync-all` | 同步所有套餐到 Stripe |  

---

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
  -d '{"name": "CI/CD Pipeline"}'
```  

### 3. 查看订阅状态和限制  
```bash
curl https://apiv2.waiflow.app/api/v2/billing/subscription \
  -H "X-API-Key: mf_your_api_key_here"
```  

### 4. 查看平台统计数据（超级管理员）  
```bash
curl https://apiv2.waiflow.app/api/v2/admin/stats \
  -H "Authorization: Bearer eyJhbGciOi..."
```  

---

## 错误响应  
| 状态码 | 含义 |  
|--------|---------|  
| 400 | 请求体或参数无效 |  
| 401 | 认证信息缺失或无效 |  
| 403 | 权限不足（非管理员/超级管理员） |  
| 404 | 资源未找到 |  
| 409 | 冲突（重复的电子邮件、套餐 ID 等） |  
| 422 | 验证错误 |  
| 429 | 超过请求频率限制 |  

## 提示  
- **API 密钥安全**：`raw_key` 仅在创建时显示一次，请将其存储在安全密钥管理工具中。  
- **令牌刷新**：访问令牌有效期为 30 分钟，使用刷新端点可无需重新认证即可获取新令牌。  
- **魔法链接**：用于无密码登录，请依次使用 `magic-link/request` 和 `magic-link/verify` 功能。  
- **套餐限制**：在进行 API 调用前，请使用 `GET /billing/subscription` 查看剩余配额。  
- **管理员操作**：所有管理员端点需要超级管理员权限，普通用户会收到 403 错误。  

---

## 相关技能  
- **moltflow-core**：会话管理、联系人管理和消息发送功能  
- **moltflow-ai**：基于 AI 的自动回复和风格训练功能  
- **moltflow-a2a**：多代理协作的代理间通信协议  
- **moltflow-reviews**：评论收集和情感分析工具