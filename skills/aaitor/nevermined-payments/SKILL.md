---
name: nevermined-payments
description: >
  Integrates Nevermined payment infrastructure into AI agents, MCP servers,
  Google A2A agents, and REST APIs. Handles x402 protocol, credit billing,
  payment plans, and SDK integration for TypeScript (@nevermined-io/payments)
  and Python (payments-py).
---

# Nevermined支付集成

## 概述

Nevermined为AI代理提供了金融支持功能，包括实时货币化、访问控制和支付处理。本文档将帮助您实现以下功能：

- 使用**x402支付协议**保护API端点
- 通过**基于信用的计费方式**按请求收费
- 与**Express.js**、**FastAPI**、**Strands代理**、**MCP服务器**或**Google A2A代理**集成
- 支持**订阅者端**的流程（购买计划、生成令牌、调用受保护的API）
- 通过Google A2A协议实现**代理之间的支付**

x402协议利用HTTP 402响应来提示支付需求。客户端获取访问令牌后重新发起请求，服务器验证权限、执行任务并完成结算（消耗信用）。

## 快速入门检查清单

1. 在[nevermined.app](https://nevermined.app)的“设置”→“API密钥”处获取API密钥。
2. 安装SDK（`npm install @nevermined-io/payments`或`pip install payments-py`）。
3. 通过应用程序界面或编程方式注册您的代理和计划（详见`references/payment-plans.md`）。
4. 为您的路由/工具添加支付保护（请参考相应的框架文档）。
5. 进行测试：先尝试不带令牌的请求（应收到402响应），然后再尝试带令牌的请求（应收到200响应）。

## 环境设置

| 变量 | 是否必需 | 说明 |
|---|---|---|
| `NVM_API_KEY` | 是 | 您的Nevermined API密钥（在[nevermined.app]的“设置”→“API密钥”处获取） |
| `NVM_ENVIRONMENT` | 是 | `sandbox`用于测试，`live`用于生产环境 |
| `NVM_PLAN_ID` | 是 | 注册时获得的计划ID |
| `NVM_AGENT_ID` | 有时需要 | 对于MCP服务器和包含多个代理的计划而言 |
| `BUILDER_ADDRESS` | 注册时需要 | 用于接收支付的钱包地址 |

### `.env`模板

```bash
# Required
NVM_API_KEY=your-api-key-here
NVM_ENVIRONMENT=sandbox
NVM_PLAN_ID=your-plan-id-here

# Required for MCP servers or multi-agent plans
NVM_AGENT_ID=your-agent-id-here

# Required for registration
BUILDER_ADDRESS=0xYourWalletAddress
```

### 先决条件

- **TypeScript/Express.js**：Node.js 18+版本。您的`package.json`中必须包含`"type": "module"`，以便导入`@nevermined-io/payments/express`模块。
- **Python/FastAPI**：Python 3.9+版本。使用`pip install payments-py[fastapi`进行安装；`[fastapi]`插件是必需的。

### TypeScript

```bash
npm install @nevermined-io/payments
```

### Python

```bash
pip install payments-py
```

### Python（FastAPI）

```python
import os
from payments_py import Payments, PaymentOptions

payments = Payments.get_instance(
    PaymentOptions(
        nvm_api_key=os.environ["NVM_API_KEY"],
        environment="sandbox"
    )
)
```

## 核心工作流程（所有集成方式）

所有Nevermined支付集成都遵循以下5个步骤：

1. 客户端发送请求（不包含支付令牌）。
2. 服务器返回402响应，并附带`payment-required`头部（包含计划的Base64编码JSON信息）。
3. 客户端通过`payments.x402 getX402AccessToken(planId, agentId)`获取x402令牌。
4. 客户端再次发送请求，并在请求头中包含`payment-signature`（即令牌）。
5. 服务器验证请求、执行任务并完成结算（消耗信用），然后返回带有`payment-response`头部的响应。

## 框架选择指南

根据您的开发环境选择合适的集成方式：

| 框架 | 语言 | 参考文档 | 关键导入项 |
|---|---|---|---|
| **Express.js** | TypeScript/JS | `references/express-integration.md` | `@nevermined-io/payments/express`中的`paymentMiddleware` |
| **FastAPI** | Python | `references/fastapi-integration.md` | `payments_py.x402.fastapi`中的`PaymentMiddleware` |
| **Strands Agent** | Python | `references/strands-integration.md` | `payments_py.x402.strands`中的`@requires_payment` |
| **MCP Server** | TypeScript | `references/mcp-paywall.md` | `payments.mcp.start()` / `payments.mcp.registerTool()` |
| **Google A2A** | TypeScript/Python | `references/a2a-integration.md` | `payments.a2a.start()` / `payments.a2a.buildPaymentAgentCard()` |
| **任意HTTP框架** | 任意语言 | `references/x402-protocol.md` | 需通过自定义API进行手动验证和结算 |
| **客户端** | TypeScript/Python | `references/client-integration.md` | `payments.x402 getX402AccessToken()` |

## SDK快速参考

### TypeScript（`@nevermined-io/payments`）

```typescript
// Initialize
const payments = Payments.getInstance({ nvmApiKey, environment })

// Register agent + plan
const { agentId, planId } = await payments.agents.registerAgentAndPlan(
  agentMetadata, agentApi, planMetadata, priceConfig, creditsConfig
)

// Subscriber: order plan and get token
await payments.plans.orderPlan(planId)
const balance = await payments.plans.getPlanBalance(planId)
const { accessToken } = await payments.x402.getX402AccessToken(planId, agentId)

// Server: verify and settle
const verification = await payments.facilitator.verifyPermissions({
  paymentRequired, x402AccessToken: token, maxAmount: BigInt(credits)
})
const settlement = await payments.facilitator.settlePermissions({
  paymentRequired, x402AccessToken: token, maxAmount: BigInt(creditsUsed)
})

// Helpers
import { buildPaymentRequired } from '@nevermined-io/payments'
import { paymentMiddleware, X402_HEADERS } from '@nevermined-io/payments/express'

// MCP server
payments.mcp.registerTool(name, config, handler, { credits: 5n })
const { info, stop } = await payments.mcp.start({ port, agentId, serverName })

// A2A server
const agentCard = payments.a2a.buildPaymentAgentCard(baseCard, { paymentType, credits, planId, agentId })
const server = await payments.a2a.start({ port, basePath: '/a2a/', agentCard, executor })
// A2A client
const client = payments.a2a.getClient({ agentBaseUrl, agentId, planId })
await client.sendMessage("Hello", accessToken)
```

### Python（`payments-py`）

```python
# Initialize
payments = Payments.get_instance(PaymentOptions(nvm_api_key=key, environment="sandbox"))

# Register agent + plan
result = payments.agents.register_agent_and_plan(
    agent_metadata, agent_api, plan_metadata, price_config, credits_config
)

# Subscriber: order plan and get token
payments.plans.order_plan(plan_id)
balance = payments.plans.get_plan_balance(plan_id)
token_res = payments.x402.get_x402_access_token(plan_id, agent_id)

# Server: verify and settle
verification = payments.facilitator.verify_permissions(
    payment_required=pr, x402_access_token=token, max_amount=str(credits)
)
settlement = payments.facilitator.settle_permissions(
    payment_required=pr, x402_access_token=token, max_amount=str(credits_used)
)

# Helpers
from payments_py.x402.helpers import build_payment_required
from payments_py.x402.fastapi import PaymentMiddleware
from payments_py.x402.strands import requires_payment

# A2A server
from payments_py.a2a.agent_card import build_payment_agent_card
from payments_py.a2a.server import PaymentsA2AServer
agent_card = build_payment_agent_card(base_card, { ... })
server = PaymentsA2AServer.start(agent_card=agent_card, executor=executor, payments_service=payments, port=3005)
# A2A client
client = payments.a2a.get_client(agent_base_url=url, agent_id=agent_id, plan_id=plan_id)
```

## x402支付头部

所有x402 v2集成都使用以下三个HTTP头部：

| 头部 | 方向 | 说明 |
|---|---|---|
| `payment-signature` | 客户端 → 服务器 | x402访问令牌 |
| `payment-required` | 服务器 → 客户端（402响应） | 包含计划要求的Base64编码JSON |
| `payment-response` | 服务器 → 客户端（200响应） | 包含结算结果的Base64编码JSON |

`payment-required`头部的数据结构：
```json
{
  "x402Version": 2,
  "accepts": [{
    "scheme": "nvm:erc4337",
    "network": "eip155:84532",
    "planId": "<plan-id>",
    "extra": { "agentId": "<agent-id>" }
  }]
}
```

## 支付计划类型

Nevermined支持多种支付计划类型：

- **基于信用的**：预付费余额，按请求次数扣费（最常见于API）
- **基于时间的**：固定期限的访问权限（例如，30天无限访问）
- **按使用量付费（PAYG）**：每次请求按USDC结算，无预付费余额 |
- **试用版**：免费有限访问权限，用户可一次性申请 |
- **混合型**：结合信用和时限

详细信息请参阅`references/payment-plans.md`。

## 常见集成模式

### Express.js — 每个路由固定信用额度

```typescript
import { paymentMiddleware } from '@nevermined-io/payments/express'

app.use(paymentMiddleware(payments, {
  'POST /ask': { planId: PLAN_ID, credits: 1 },
  'POST /generate': { planId: PLAN_ID, credits: 5 }
}))
```

### FastAPI — 每个路由固定信用额度

```python
from payments_py.x402.fastapi import PaymentMiddleware

app.add_middleware(
    PaymentMiddleware,
    payments=payments,
    routes={
        "POST /ask": {"plan_id": PLAN_ID, "credits": 1},
        "POST /generate": {"plan_id": PLAN_ID, "credits": 5}
    }
)
```

### Express.js — 根据响应动态分配信用额度

```typescript
paymentMiddleware(payments, {
  'POST /generate': {
    planId: PLAN_ID,
    credits: (req, res) => {
      const tokens = res.locals.tokenCount || 100
      return Math.ceil(tokens / 100)
    }
  }
})
```

### FastAPI — 根据请求动态分配信用额度

```python
async def calculate_credits(request: Request) -> int:
    body = await request.json()
    max_tokens = body.get("max_tokens", 100)
    return max(1, max_tokens // 100)

app.add_middleware(
    PaymentMiddleware,
    payments=payments,
    routes={"POST /generate": {"plan_id": PLAN_ID, "credits": calculate_credits}}
)
```

### MCP服务器 — 使用支付墙进行注册

```typescript
payments.mcp.registerTool(
  "weather.today",
  { title: "Today's Weather", inputSchema: z.object({ city: z.string() }) },
  async (args, extra, context) => ({
    content: [{ type: "text", text: `Weather in ${args.city}: Sunny, 25C` }]
  }),
  { credits: 5n }
)

const { info, stop } = await payments.mcp.start({
  port: 3000,
  agentId: process.env.NVM_AGENT_ID!,
  serverName: "my-server"
})
```

### Strands代理 — 基于装饰器的支付处理

```python
from strands import Agent, tool
from payments_py.x402.strands import requires_payment

@tool(context=True)
@requires_payment(payments=payments, plan_id=PLAN_ID, credits=1)
def analyze_data(query: str, tool_context=None) -> dict:
    return {"status": "success", "content": [{"text": f"Analysis: {query}"}]}

agent = Agent(tools=[analyze_data])
```

### Google A2A — 带有支付功能的代理服务器

#### TypeScript

```typescript
const agentCard = payments.a2a.buildPaymentAgentCard(baseAgentCard, {
  paymentType: "dynamic",
  credits: 1,
  planId: process.env.NVM_PLAN_ID!,
  agentId: process.env.NVM_AGENT_ID!,
})

const server = await payments.a2a.start({
  port: 3005,
  basePath: '/a2a/',
  agentCard,
  executor: new MyExecutor(),
})
```

#### Python

```python
from payments_py.a2a.agent_card import build_payment_agent_card
from payments_py.a2a.server import PaymentsA2AServer

agent_card = build_payment_agent_card(base_agent_card, {
    "paymentType": "dynamic",
    "credits": 1,
    "planId": os.environ["NVM_PLAN_ID"],
    "agentId": os.environ["NVM_AGENT_ID"],
})

server = PaymentsA2AServer.start(
    agent_card=agent_card,
    executor=MyExecutor(),
    payments_service=payments,
    port=3005,
    base_path="/a2a/",
)
```

### Google A2A — 客户端发送付费任务

```typescript
const client = payments.a2a.getClient({
  agentBaseUrl: 'http://localhost:3005/a2a/',
  agentId: AGENT_ID,
  planId: PLAN_ID,
})

const { accessToken } = await payments.x402.getX402AccessToken(PLAN_ID, AGENT_ID)
const response = await client.sendMessage("Analyze this data", accessToken)
```

## 提前收集开发人员信息

当开发人员请求集成Nevermined支付功能时，请在生成代码之前收集所有必要的信息，以避免多次沟通。

**请一次性询问开发人员以下内容：**

1. **使用的框架**：Express.js、FastAPI、MCP服务器、Strands代理、Google A2A还是通用HTTP？
2. **需要保护的路由**：哪些API端点需要支付保护？每个端点需要多少信用额度？（例如，`POST /chat = 1信用额度`）
3. **定价模式**：是按请求固定信用额度，还是根据请求/响应参数动态定价？
4. **Nevermined API密钥**：他们是否已经有了`NVM_API_KEY`？如果没有，请引导他们访问[nevermined.app]的“设置”→“API密钥”。
5. **计划ID**：他们是否已经有了`NVM_PLAN_ID`？如果需要，是否还需要注册脚本？
6. **环境**：测试环境（`sandbox`）还是生产环境（`live`）？

**如果需要注册计划，请进一步询问：**

7. **计划名称和描述**：例如，“入门计划——100次API请求”
8. **定价信息**：每次请求的费用是多少（以USDC计）？
9. **每个计划的信用额度**：总共包含多少信用额度？
10. **支付接收钱包地址**（`BUILDER_ADDRESS`）：用于接收支付的钱包地址

**示例提示：**

> 我需要设置Nevermined支付功能。以下是我的信息：
> - 使用的框架：Express.js
> - 需要保护的路由：`POST /chat`（1信用额度），`POST /generate`（3信用额度）
> - 我也需要注册脚本
- 计划名称：“入门计划”，100次API请求对应10 USDC
- 环境：测试环境（`sandbox`）
- 我的API密钥存储在`NVM_API_KEY`环境变量中
- 支付接收钱包地址：0x1234...

根据这些信息，您可以一次性生成注册脚本和具有支付保护的服务器代码。

## 代理和计划注册

### 推荐使用SDK进行注册

建议通过编程方式注册您的代理和计划（详见`references/payment-plans.md`）。

```typescript
// TypeScript
const { agentId, planId } = await payments.agents.registerAgentAndPlan(
  { name: 'My Agent', description: 'AI service', tags: ['ai'], dateCreated: new Date() },
  { endpoints: [{ POST: 'https://your-api.com/query' }] },
  { name: 'Starter Plan', description: '100 requests for $10', dateCreated: new Date() },
  payments.plans.getERC20PriceConfig(10_000_000n, USDC_ADDRESS, process.env.BUILDER_ADDRESS!),
  payments.plans.getFixedCreditsConfig(100n, 1n)
)
```

### 使用Nevermined应用程序（无需编写代码）

1. 访问[nevermined.app](https://nevermined.app)并登录。
2. 点击“我的代理”，然后注册新的代理并设置元数据和端点。
3. 创建支付计划（设置价格、信用额度和有效期）。
4. 将计划与代理关联并发布。
5. 复制`agentId`和`planId`，用于配置`.env`文件。

### 使用命令行工具（CLI）

```bash
# 1. Install CLI
npm install -g @nevermined-io/cli

# 2. Configure (use sandbox for testing)
nvm config init --api-key "$NVM_API_KEY" --environment sandbox

# 3. Register agent and plan together
nvm agents register-agent-and-plan \
  --agent-metadata '{"name":"My Agent","description":"AI service"}' \
  --agent-api '{"endpoints":[{"POST":"https://your-api.com/query"}]}' \
  --plan-metadata '{"name":"Starter Plan","description":"100 requests"}' \
  --price-config '{"tokenAddress":"0x036CbD53842c5426634e7929541eC2318f3dCF7e","price":10000000,"amountOfCredits":100}' \
  --credits-config '{"minCreditsRequired":1,"minCreditsToCharge":1,"maxCreditsToCharge":10}'

# 4. List your plans
nvm plans get-plans

# 5. As a subscriber: order a plan and get an x402 token
nvm plans order-plan $PLAN_ID
nvm x402token get-x402-access-token $PLAN_ID --agent-id $AGENT_ID

# 6. Test against your running server
curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -H "payment-signature: $TOKEN" \
  -d '{"message": "Hello"}'
```

## 故障排除

| 现象 | 原因 | 解决方法 |
|---|---|---|
| 返回HTTP 402响应 | 未设置`payment-signature`头部或令牌无效/过期 | 通过`getX402AccessToken()`生成新的令牌 |
| MCP错误 `-32003` | 需要支付但未提供令牌、令牌无效或信用额度不足 | 确认订阅者已购买计划且仍有剩余信用额度 |
| MCP错误 `-32002` | 服务器配置错误 | 检查`NVM_API_KEY`、`NVM_PLAN_ID`和`NVM_AGENT_ID`是否设置正确 |
| `verification.isValid`为`false` | 令牌过期、计划错误或信用额度不足 | 重新选择计划或生成新的令牌 |
| 信用额度未扣除 | 请求处理后未调用`settlePermissions`方法 | 确保在处理请求后调用了`settlePermissions`方法（中间件会自动执行此操作） |
| 未显示`payment-required`头部 | 服务器未正确返回402响应 | 使用`buildPaymentRequired()`辅助函数或相应的框架中间件 |

## 额外资源

- **文档**：[nevermined.ai/docs](https://nevermined.ai/docs)
- **Nevermined应用程序**：[nevermined.app](https://nevermined.app)——用于注册代理、创建计划和管理订阅 |
- **MCP搜索服务器**：`https://docs.nevermined.app/mcp`——可以从任何MCP客户端搜索Nevermined的文档 |
- **教程**：[github.com/nevermined-io/tutorials](https://github.com/nevermined-io/tutorials) |
- **Discord社区**：[discord.com/invite/GZju2qScKq](https://discord.com/invite/GZju2qScKq) |
- **TypeScript SDK**：`@nevermined-io/payments`（在npm上可安装） |
- **Python SDK**：`payments-py`（在PyPI上可安装）