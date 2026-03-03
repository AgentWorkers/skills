---
name: supportforge
description: 通过 SupportForge API 提供 AI 客户支持服务——包括工单创建、自动回复、工单路由以及知识库搜索功能。适用于需要自动化客户支持、工单管理、自动生成回复或使用支持知识库的场景。提供免费 tier（每天 100 次请求）。
---
# SupportForge

由 Voss Consulting Group 提供的 AI 客户支持 API。

## 设置

设置 `SUPPORTFORGE_API_KEY` 或 `SUPPORTFORGE_EMAIL` 以实现自动注册（免费，无需信用卡）。

```bash
curl -X POST https://anton.vosscg.com/v1/keys -H 'Content-Type: application/json' -d '{"email":"you@example.com"}'
```

## 使用方法

```bash
curl -X POST https://anton.vosscg.com/v1/tickets/create \
  -H "Authorization: Bearer $SUPPORTFORGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"subject": "Login issue", "message": "Cannot reset password", "priority": "high"}'
```

## 功能
- `POST /v1/tickets/create` — 创建支持工单
- `POST /v1/tickets/:id/reply` — 回复工单（人工回复或 AI 自动回复）
- `POST /v1/kb/search` — 搜索知识库
- `POST /v1/keys` — 获取 API 密钥（免费 tier 仅限通过电子邮件获取）
- `GET /v1/health` — 系统健康检查