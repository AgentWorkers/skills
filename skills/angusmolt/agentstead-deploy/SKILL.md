---
name: agentstead-deploy
description: 将 OpenClaw 代理部署到 AgentStead 云托管服务中。适用于用户希望将代理部署到云端、在 Telegram/Discord 上托管 AI 助手，或设置远程 OpenClaw 实例的场景。该服务负责处理账户创建、代理配置、频道连接以及计费等相关流程。
---
# AgentStead 部署

几分钟内即可将 OpenClaw 代理部署到 AgentStead 的云托管环境中。

**API 基本 URL：** `https://agentstead.com/api/v1`

## 快速部署流程

1. 注册/登录 → 2. 创建代理 → 3. 添加频道 → 4. 设置计费 → 5. 启动代理 → 6. 验证

## 对话指南

在调用任何 API 之前，需要从用户那里获取以下信息：

1. **代理名称** — 代理应该被命名为什么？
2. **系统提示/个性描述** — 代理的系统提示或个性设定
3. **频道** — 使用 Telegram（需要从 @BotFather 获取机器人令牌）或 Discord（需要从 Discord 开发者门户获取机器人令牌）
4. **AI 计划** — 用户自行提供 API 密钥（BYOK，费用为 $0）或使用平台提供的 AI 服务（Pro：+$20/月，Max：+$100/月）
5. **如果选择 BYOK** — 使用哪个提供商及其 API 密钥？（Anthropic、OpenAI、Google、OpenRouter、xAI、Groq、Mistral、Bedrock、Venice）
6. **托管计划** — Starter：$9/月；Pro：$19/月；Business：$39/月；Enterprise：$79/月
7. **支付方式** — 使用加密货币（USDC）或信用卡（Stripe）

## 逐步操作流程

### 第 1 步：注册

```bash
curl -X POST https://agentstead.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'
```

注册响应中会包含一个 `token` — 在后续的所有请求中，使用 `Authorization: Bearer <token>` 进行身份验证。

如果用户已有账户，可以直接登录：

```bash
curl -X POST https://agentstead.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'
```

### 第 2 步：创建代理

```bash
curl -X POST https://agentstead.com/api/v1/agents \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MyAgent",
    "personality": "You are a helpful assistant...",
    "plan": "starter",
    "aiPlan": "byok",
    "byokProvider": "anthropic",
    "byokApiKey": "sk-ant-..."
  }'
```

如果选择使用平台提供的 AI 服务（而非用户自行提供 API 密钥）：
```json
{
  "name": "MyAgent",
  "personality": "You are a helpful assistant...",
  "plan": "pro",
  "aiPlan": "pro_ai"
}
```

响应中会包含代理的 `id` — 请保存该 ID 以用于后续步骤。

### 第 3 步：添加频道

**Telegram：**
```bash
curl -X POST https://agentstead.com/api/v1/agents/<agent_id>/channels \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"type": "telegram", "botToken": "123456:ABC-DEF..."}'
```

**Discord：**
```bash
curl -X POST https://agentstead.com/api/v1/agents/<agent_id>/channels \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"type": "discord", "botToken": "MTIz..."}'
```

### 第 4 步：设置计费

**使用加密货币（USDC）：**
```bash
curl -X POST https://agentstead.com/api/v1/billing/crypto/create-invoice \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"agentId": "<agent_id>", "plan": "starter", "aiPlan": "byok"}'
```

系统会返回一个支付地址/URL，请指导用户将 USDC 支付到该地址。

**使用 Stripe（信用卡）：**
```bash
curl -X POST https://agentstead.com/api/v1/billing/checkout \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"agentId": "<agent_id>", "plan": "starter", "aiPlan": "byok"}'
```

系统会返回一个 Stripe 结账 URL，请将链接发送给用户以完成支付。

### 第 5 步：启动代理

```bash
curl -X POST https://agentstead.com/api/v1/agents/<agent_id>/start \
  -H "Authorization: Bearer <token>"
```

### 第 6 步：验证

```bash
curl -X GET https://agentstead.com/api/v1/agents/<agent_id> \
  -H "Authorization: Bearer <token>"
```

检查代理的状态是否为 “RUNNING”。如果不是，请稍等几秒钟后重试。

## 价格参考

| 托管计划 | 价格 |
|------|-------|
| Starter | $9/月 |
| Pro | $19/月 |
| Business | $39/月 |
| Enterprise | $79/月 |

| AI 计划 | 价格 |
|---------|-------|
| BYOK | $0（用户自行提供 API 密钥） |
| Pro AI | +$20/月 |
| Max AI | +$100/月 |

**支持的 BYOK 提供商：** Anthropic、OpenAI、Google、OpenRouter、xAI、Groq、Mistral、Bedrock、Venice

## 注意事项

- Telegram 机器人令牌可从 [@BotFather](https://t.me/BotFather) 获取
- Discord 机器人令牌可从 [Discord 开发者门户](https://discord.com/developers/applications) 获取
- 可以通过 `POST /agents/:id/stop` 命令随时停止和重启代理
- 有关完整的 API 文档，请参阅 `references/api-reference.md`