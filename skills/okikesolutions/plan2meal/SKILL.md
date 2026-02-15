---
name: plan2meal
description: 在 Plan2Meal 中，您可以通过聊天功能来管理食谱和购物清单：添加食谱链接、列出/搜索/显示/删除食谱，以及创建/管理购物清单。此功能专为需要执行特定食谱操作或管理购物清单的用户设计。请勿将其用于提供通用烹饪建议、营养指导，或与 Plan2Meal 无关的待办事项/购物工具。成功的操作应表现为命令执行后能够提供清晰的结果信息（如食谱 ID、数量、链接或错误信息），同时确保数据传输的准确性。
requiredEnv:
  - CONVEX_URL
  - AUTH_GITHUB_ID
  - AUTH_GITHUB_SECRET
  - GITHUB_CALLBACK_URL
  - CLAWDBOT_URL
optionalEnv:
  - AUTH_GOOGLE_ID
  - AUTH_GOOGLE_SECRET
  - GOOGLE_CALLBACK_URL
  - AUTH_APPLE_ID
  - AUTH_APPLE_SECRET
  - APPLE_CALLBACK_URL
  - ALLOW_DEFAULT_BACKEND
primaryEnv: CONVEX_URL
---

# Plan2Meal 技能

这是一个用于通过 Plan2Meal 管理食谱和购物清单的 ClawdHub 技能。

## 数据路由与安全规范（强制要求）

- 共享的后端/API 地址：`https://gallant-bass-875.convex.cloud`
- 认证以及食谱/购物清单相关的 API 请求会发送到配置的 `CONVEX_URL`。
- 除非设置了 `ALLOW_DEFAULT_BACKEND=true`，否则禁止使用共享后端。
- 在涉及后端调用时，严禁声称数据仅在前端进行处理。

## 使用场景与禁止使用场景（路由规则）

**使用场景：**
- 用户请求添加、查看、搜索或删除 Plan2Meal 食谱。
- 用户请求创建、查看或更新 Plan2Meal 购物清单。
- 用户请求对 Plan2Meal 相关的操作进行身份验证。

**禁止使用场景：**
- 用户请求获取一般的用餐建议（未请求 Plan2Meal 相关的操作）。
- 用户请求获取与 Plan2Meal 存储数据无关的健康/营养分析信息。
- 用户请求管理 Apple 提示、笔记或其他系统相关的内容。

## 设置步骤

1. 安装：
   ```bash
   clawdhub install plan2meal
   ```

2. 配置环境：
   ```bash
   cp .env.example .env
   ```

3. 环境变量：
   - `CONVEX_URL`（**必填**，建议使用自托管后端）
   - `ALLOW_DEFAULT_BACKEND=true`（仅在明确使用共享后端时设置）
   - OAuth 提供商凭证：
     - GitHub（必填）：`AUTH_GITHUB_ID`、`AUTH_GITHUB_SECRET`、`GITHUB Callback_URL`
     - Google（可选）：`AUTH_GOOGLE_ID`、`AUTH_GOOGLE_SECRET`、`GOOGLE Callback_URL`
     - Apple（可选）：`AUTH_APPLE_ID`、`AUTH_APPLE_SECRET`、`APPLE Callback_URL`
   - `CLAWDBOT_URL`（必填，用于机器人回调）

## 命令列表

- `plan2meal login`  
- `plan2meal logout`  
- `plan2meal add <url>`  
- `plan2meal list`  
- `plan2meal search <term>`  
- `plan2meal show <id>`  
- `plan2meal delete <id>`  
- `plan2meal lists`  
- `plan2meal list-show <id>`  
- `plan2meal list-create <name>`  
- `plan2meal list-add <listId> <recipeId>`  
- `plan2meal help`  

## 输出模板

请使用 `references/output-templates.md` 中提供的响应格式模板。

## 回复前的安全检查事项

- 如果命令因认证或配置问题失败，需提供具体的下一步操作建议。
- 如果涉及后端服务，必须如实说明数据来源（是共享后端还是自定义后端）。
- 绝不允许在输出中泄露任何敏感信息或令牌。