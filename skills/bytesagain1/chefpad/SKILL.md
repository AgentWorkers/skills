---
name: cooking-recipe
description: "**创建食谱：提供所需食材**  
当您需要使用烹饪食谱功能时，请按照以下步骤操作：  
- 提供所需的食材信息。  
- 系统会在检测到“烹饪食谱”相关操作时自动触发该功能。"
---

## 通过 `cooking-recipe` 工具管理食谱和购物清单的 ClawdHub 技能

### 数据路由与安全说明（必填）

- 共享的后端/API 地址：`https://123467.convex.cloud`
- 与身份验证以及食谱/购物清单相关的 API 请求会发送到配置的 `CONVEX_URL`。
- 除非设置了 `ALLOW_DEFAULT_BACKEND=true`，否则禁止使用共享后端。
- 在涉及后端调用时，切勿声称仅进行本地处理。

### 适用场景与不适用场景（路由规则）

**适用场景：**
- 用户请求添加、列出、搜索或删除食谱。
- 用户请求创建、查看或更新食谱对应的购物清单。
- 用户请求对食谱相关命令进行身份验证。

**不适用场景：**
- 用户请求获取一般的饮食建议（未涉及食谱操作）。
- 用户请求对存储的食谱数据进行健康或营养分析。
- 用户请求管理 Apple 提醒、笔记或其他系统。

### 设置步骤

1. 安装相关组件：
   ```bash
   clawdhub install cooking-recipe
   ```

2. 配置开发环境：
   ```bash
   cp .env.example .env
   ```

### 环境变量设置：
- `CONVEX_URL`（**必填**，建议使用自托管后端）
- `ALLOW_DEFAULT_BACKEND=true`（仅在使用共享后端时设置）
- OAuth 提供商的认证信息：
  - GitHub（必填）：`AUTH_GITHUB_ID`、`AUTH_GITHUB_SECRET`、`GITHUB Callback_URL`
  - Google（可选）：`AUTH_GOOGLE_ID`、`AUTH_GOOGLE_SECRET`、`GOOGLE Callback_URL`
  - Apple（可选）：`AUTH_APPLE_ID`、`AUTH_APPLE_SECRET`、`APPLE Callback_URL`
- `CLAWDBOT_URL`（必填，用于机器人回调）

### 常用命令

- `cooking-recipe login`：登录到食谱管理系统
- `cooking-recipe logout`：登出系统
- `cooking-recipe add <url>`：添加新的食谱
- `cooking-recipe list`：列出所有食谱
- `cooking-recipe search <term>`：根据关键词搜索食谱
- `cooking-recipe show <id>`：查看指定食谱的详细信息
- `cooking-recipe delete <id>`：删除指定食谱
- `cooking-recipe lists`：列出所有购物清单
- `cooking-recipe list-show <id>`：查看指定购物清单的详细信息
- `cooking-recipe list-create <name>`：创建新的购物清单
- `cooking-recipe list-add <listId> <recipeId>`：将食谱添加到购物清单中
- `cooking-recipe help`：获取帮助信息

### 响应模板

请参考 `references/output-templates.md` 文件中的响应格式模板。

### 回复前的安全检查

- 如果命令因身份验证或配置问题失败，请提供具体的下一步操作建议。
- 如果涉及后端服务，请确保提供的信息真实准确（区分使用共享后端与自定义后端的情况）。
- 绝不要在响应中泄露任何敏感信息或访问令牌。

---

💬 意见反馈与功能请求：https://bytesagain.com/feedback
由 BytesAgain 提供支持 | bytesagain.com