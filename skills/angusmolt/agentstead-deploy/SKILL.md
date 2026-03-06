---
name: agentstead-deploy
description: 将 OpenClaw AI 代理部署到 AgentStead 云托管服务中。当用户希望在 AgentStead 上部署子代理、连接 Telegram/Discord 并快速使用 AgentStead 提供的 AI 模型时，可以使用此方法。
version: 1.2.0
---
# AgentStead 部署

在几分钟内将 OpenClaw 代理部署到 AgentStead 的云托管环境中。

**API 基本 URL：** `https://www.agentstead.com/api/v1`

## 快速部署流程

1. 注册/登录 → 2. 创建代理 → 3. 添加频道 → 4. 设置计费 → 5. 启动代理 → 6. 验证

## 对话指南

在调用任何 API 之前，从用户那里收集以下信息：

1. **代理名称** — 代理应该被命名为什么？
2. **系统提示语/个性描述** — 代理应使用的系统提示语或个性描述
3. **频道** — Telegram（需要从 @BotFather 获取机器人令牌）或 Discord（需要从 Discord 开发者门户获取机器人令牌）
4. **AI 订阅计划** — 按使用量付费（基础计划 $0），1K 订阅量（$10/月），3K 订阅量（$30/月），5K 订阅量（$50/月），或 10K 订阅量（$100/月）
5. **AI 模型** — Claude 3.5 Haiku（响应速度快），Claude Sonnet 4（性能均衡），或 Claude Opus 4.6（功能最强大）
6. **托管计划** — 入门级 $9/月，专业级 $19/月，企业级 $39/月，企业高级 $79/月
7. **支付方式** — ASTD 剩余金额，加密货币（Base/Polygon 上的 USDC），或信用卡（Stripe）

## 详细步骤

### 第 1 步：注册

```bash
curl -X POST https://www.agentstead.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'
```

响应中会包含一个 `token` — 在后续的所有请求中使用 `Authorization: Bearer <token>` 进行身份验证。

如果用户已有账户，请直接使用登录功能：

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
    "plan": "pro",
    "aiPlan": "ASTD_5000",
    "defaultModel": "anthropic/claude-sonnet-4-20250514"
  }'
```

**有效的 `aiPlan` 值：**
| 计划 | 价格 | 描述 |
|------|-------|-------------|
| `PAYG` | $0/月 | 按使用量付费，从 ASTD 剩余金额中扣除 |
| `ASTD_1000` | $10/月 | 每月 1,000 ASTD 订阅量 |
| `ASTD_3000` | $30/月 | 每月 3,000 ASTD 订阅量 |
| `ASTD_5000` | $50/月 | 每月 5,000 ASTD 订阅量 |
| `ASTD_10000` | $100/月 | 每月 10,000 ASTD 订阅量 |

**有效的 `defaultModel` 值：**
| 模型 | ID | 适用场景 |
|-------|----|----------|
| Claude 3.5 Haiku | `anthropic/claude-haiku-3-5` | 响应速度快 |
| Claude Sonnet 4 | `anthropic/claude-sonnet-4-20250514` | 性能均衡 |
| Claude Opus 4.6 | `anthropic/claude-opus-4-6` | 功能最强大 |

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
  -d '{"agentId": "<agent_id>", "plan": "pro", "aiPlan": "ASTD_5000"}'
```

系统会返回一个存款地址。指导用户将 USDC 存入 Base 或 Polygon 链上。

**Stripe（信用卡）：**
```bash
curl -X POST https://www.agentstead.com/api/v1/billing/checkout \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"agentId": "<agent_id>", "plan": "pro", "aiPlan": "ASTD_5000"}'
```

系统会提供一个 Stripe 结账链接。将链接发送给用户以完成支付。

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

### 硬件配置（每个代理）

| 计划 | 价格 | 规格 |
|------|-------|-------|
| 入门级 | $9/月 | t3.micro · 1 个 vCPU · 1GB 内存 · 5GB 存储 |
| 专业级 | $19/月 | t3.small · 2 个 vCPU · 2GB 内存 · 20GB 存储 |
| 企业级 | $39/月 | t3.medium · 2 个 vCPU · 4GB 内存 · 50GB 存储 |
| 企业高级 | $79/月 | t3.large · 2 个 vCPU · 8GB 内存 · 100GB 存储 |

### AI 订阅计划

| 计划 | 价格 | 描述 |
|------|-------|-------------|
| `PAYG` | $0/月 | 按使用量付费，从 ASTD 剩余金额中扣除 |
| `ASTD_1000` | $10/月 | 每月 1,000 ASTD 订阅量 |
| `ASTD_3000` | $30/月 | 每月 3,000 ASTD 订阅量 |
| `ASTD_5000` | $50/月 | 每月 5,000 ASTD 订阅量 |
| `ASTD_10000` | $100/月 | 每月 10,000 ASTD 订阅量 |

所有计划均包含 Claude 3.5 Haiku、Claude Sonnet 4 和 Claude Opus 4.6 的使用权限。

**ASTD 转换：** 100 ASTD = $1 USD。平台费用：在 AI 提供商费用的基础上额外收取 4%。

## 注意事项

- Telegram 机器人令牌可从 [@BotFather](https://t.me/BotFather) 获取
- Discord 机器人令牌可从 [Discord 开发者门户](https://discord.com/developers/applications) 获取
- 可以通过 `POST /agents/:id/stop` 命令随时停止和重启代理
- 可通过 Web 控制面板或 iOS 应用程序为代理充值 ASTD 剩余金额
- 请参阅 `references/api-reference.md` 以获取完整的 API 文档。