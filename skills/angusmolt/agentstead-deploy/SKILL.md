---
name: agentstead-deploy
description: 将 OpenClaw 子代理的 API 部署到 AgentStead 云托管平台上，并配置为生产环境就绪的状态。当用户希望在 AgentStead 上自动部署子代理、连接 Telegram/Discord 服务，并通过 Stripe（信用卡）、加密货币（USDC）或 ASTD 帐户余额进行快速支付时，可以使用此功能。
version: 1.1.0
---
# AgentStead 部署

几分钟内即可将 OpenClaw 代理部署到 AgentStead 的云托管环境中。

**API 基本 URL:** `https://www.agentstead.com/api/v1`

## 快速部署流程

1. 注册/登录 → 2. 创建代理 → 3. 添加频道 → 4. 设置计费 → 5. 启动代理 → 6. 验证

## 对话指南

在调用任何 API 之前，需要从用户那里获取以下信息：

1. **代理名称** — 代理应被命名为什么？
2. **系统提示/个性** — 系统提示语或个性描述
3. **频道** — Telegram（需要从 @BotFather 获取机器人令牌）或 Discord（需要从 Discord 开发者门户获取机器人令牌）
4. **AI 计划** — 用户自备 API 密钥（BYOK）或由 AgentStead 提供（按使用量计费，费用为 1K/3K/5K/10K ASTD/月）
5. **如果选择 BYOK** — 使用哪个提供商及其 API 密钥？（Anthropic、OpenAI、Google、OpenRouter、xAI、Groq、Mistral、Bedrock、Venice 等）
6. **托管计划** — 入门级 $9/月、专业级 $19/月、企业级 $39/月、企业高级 $79/月
7. **支付方式** — ASTD 余额、加密货币（USDC）或信用卡（Stripe）

## 逐步操作流程

### 第 1 步：注册

```bash
curl -X POST https://www.agentstead.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'
```

响应中会包含一个 `token` — 在后续的所有请求中，使用 `Authorization: Bearer <token>` 作为身份验证。

如果用户已有账户，请直接登录：

```bash
curl -X POST https://www.agentstead.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'
```

### 第 2 步：创建代理

```bash
curl -X POST https://www.agentstead.com/api/v1/agents \
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

对于由 AgentStead 提供的 AI 服务（使用 ASTD 信用点数）：
```json
{
  "name": "MyAgent",
  "personality": "You are a helpful assistant...",
  "plan": "pro",
  "aiPlan": "ASTD_5000"
}
```

有效的 `aiPlan` 值：`BYOK`、`PAYG`、`ASTD_1000`、`ASTD_3000`、`ASTD_5000`、`ASTD_10000`

响应中会包含代理的 `id` — 请将其保存以用于后续步骤。

### 第 3 步：添加频道

**Telegram：**
```bash
curl -X POST https://www.agentstead.com/api/v1/agents/<agent_id>/channels \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"type": "telegram", "botToken": "123456:ABC-DEF..."}'
```

**Discord：**
```bash
curl -X POST https://www.agentstead.com/api/v1/agents/<agent_id>/channels \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"type": "discord", "botToken": "MTIz..."}'
```

### 第 4 步：设置计费

**加密货币（USDC）：**
```bash
curl -X POST https://www.agentstead.com/api/v1/billing/crypto/create-invoice \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"agentId": "<agent_id>", "plan": "starter", "aiPlan": "PAYG"}'
```

系统会返回一个支付地址/URL。指导用户将 USDC（Base 或 Polygon 链路）发送到该地址。

**Stripe（信用卡）：**
```bash
curl -X POST https://www.agentstead.com/api/v1/billing/checkout \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"agentId": "<agent_id>", "plan": "starter", "aiPlan": "PAYG"}'
```

系统会返回一个 Stripe 结账 URL。将此 URL 发送给用户以完成支付。

### 第 5 步：启动代理

```bash
curl -X POST https://www.agentstead.com/api/v1/agents/<agent_id>/start \
  -H "Authorization: Bearer <token>"
```

### 第 6 步：验证

```bash
curl -X GET https://www.agentstead.com/api/v1/agents/<agent_id> \
  -H "Authorization: Bearer <token>"
```

检查代理的状态是否为 `"RUNNING"`。如果不是，请等待几秒钟后重试。

## 价格参考

### 硬件计划（每个代理）

| 计划 | 价格 | 规格 |
|------|-------|-------|
| 入门级 | $9/月 | t3.micro · 1 个 vCPU · 1GB 内存 · 5GB 存储空间 |
| 专业级 | $19/月 | t3.small · 2 个 vCPU · 2GB 内存 · 20GB 存储空间 |
| 企业级 | $39/月 | t3.medium · 2 个 vCPU · 4GB 内存 · 50GB 存储空间 |
| 企业高级 | $79/月 | t3.large · 2 个 vCPU · 8GB 内存 · 100GB 存储空间 |

### AI 计划

| 计划 | 价格 | 描述 |
|------|-------|-------------|
| BYOK | $0 | 使用用户自备的 API 密钥（支持 20 多个提供商） |
| 按使用量计费 | $0 基础费用 | 根据 ASTD 余额按使用量计费 |
| ASTD_1000 | $10/月 | 每月 1,000 ASTD 信用点数 |
| ASTD_3000 | $30/月 | 每月 3,000 ASTD 信用点数 |
| ASTD_5000 | $50/月 | 每月 5,000 ASTD 信用点数 |
| ASTD_10000 | $100/月 | 每月 10,000 ASTD 信用点数 |

AgentStead 提供的 AI 计划包括：Claude 3.5 Haiku、Claude Sonnet 4、Claude Opus 4.6

### 支付方式
- **ASTD 余额** — 向钱包充值，将在计费周期自动扣款
- **Stripe** — 信用卡/借记卡订阅
- **USDC** — Base 或 Polygon 链路的加密货币支付
- **Apple IAP** — 仅适用于 iOS 应用

**支持的 BYOK 提供商：** Anthropic、OpenAI、Google Gemini、OpenRouter、xAI、Groq、Mistral、AWS Bedrock、Together AI、Hugging Face、Venice AI、Z.AI、Moonshot/Kimi、Cerebras、MiniMax、Xiaomi 以及更多提供商。

## 注意事项

- Telegram 机器人令牌可从 [@BotFather](https://t.me/BotFather) 获取
- Discord 机器人令牌可从 [Discord 开发者门户](https://discord.com/developers/applications) 获取
- 可以通过 `POST /agents/:id/stop` 命令随时停止并重新启动代理
- 有关完整的 API 文档，请参阅 `references/api-reference.md`