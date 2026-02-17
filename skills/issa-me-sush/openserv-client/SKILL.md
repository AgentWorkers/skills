---
name: openserv-client
description: >
  **@openserv-labs/client 使用指南：在 OpenServ 平台上管理代理、工作流、触发器和任务**  
  本指南详细介绍了如何使用 @openserv-labs/client 来管理 OpenServ 平台上的代理、工作流、触发器和任务，涵盖了资源配置、身份验证、x402 支付、基于 ERC-8004 的链上身份验证机制以及完整的平台 API 接口。  
  **重要提示：**  
  在使用本指南时，请务必同时阅读配套的 `openserv-agent-sdk` 文档，因为这两个包都是构建代理功能所必需的。如需了解完整的 API 参考信息，请参阅 `reference.md` 文件。
---
# OpenServ 客户端

`@openserv-labs/client` 包是 OpenServ 平台 API 的 TypeScript 客户端。当您的代码需要与平台进行交互时（例如注册代理、创建工作流、设置触发器或运行任务），就可以使用它。

## 为什么需要这个包

您的代理（使用 `@openserv-labs/sdk` 构建）运行在您的机器或服务器上。在您告知平台相关信息之前，平台并不知道代理的存在、其可访问位置以及如何触发它。客户端就是实现这些操作的工具。它允许您创建平台账户（或重用现有账户）、注册代理、定义工作流和触发器（Webhook、Cron、手动触发或 x402 支付方式），并绑定凭证，以便代理能够接收任务。没有它，代理将无法与平台通信或接收任务。

## 使用它的功能

- **配置** — 一次性设置：创建或重用账户（通过钱包）、注册代理、创建带有触发器和工作流的任务，并获取 API 密钥和认证令牌。通常每个应用程序启动时只需调用一次 `provision()`；该操作是幂等的（即多次调用结果相同）。
- **平台 API** — 通过 `PlatformClient` 实现对平台的完全控制：创建和列出代理、工作流、触发器和任务；触发触发器；运行工作流；管理凭证。当您需要超出默认配置的功能时，可以使用此方法。
- **模型参数** — 配置平台为代理的任务使用的 LLM 模型和参数。可以在创建/更新代理时设置 `model_parameters`，也可以通过 `provision()` 来设置。
- **模型 API** — 通过 `client.models.list()` 发现可用的 LLM 模型及其参数结构。
- **x402 支付** — 为代理设置支付门槛；调用者需要在任务执行前按请求支付（例如使用 USDC）。`provision()` 可以设置 x402 触发器并返回支付门槛的 URL。
- **ERC-8004 上链身份** — 在链上注册代理（基于 Base 链），铸造身份 NFT，并将服务元数据发布到 IPFS，以便其他人能够以标准方式发现和支付您的代理。

**参考文档：** `reference.md`（完整 API 文档）· `troubleshooting.md`（常见问题解答）· `examples/`（可运行的代码示例）

## 安装

```bash
npm install @openserv-labs/client
```

---

## 快速入门：只需 `provision()` + `run()`

**最简单的部署方式就是调用 `provision()` 和 `run()`。** 就这些。

您需要在平台上拥有一个账户才能注册代理和工作流。最简单的方法是让 `provision()` 为您创建一个账户：它会为您创建一个钱包并完成注册过程（无需电子邮件）。每次运行应用程序时都会使用这个账户。

请参阅 `examples/agent.ts` 以获取完整的可运行示例。

> **关键点：** `provision()` 是 **幂等的**。每次应用程序启动时都可以调用它——无需先检查 `isProvisioned()`。

### `provision()` 的功能

1. 创建或重用以太坊钱包（如果不存在则创建平台账户）。
2. 与 OpenServ 平台进行身份验证。
3. 创建或更新代理（操作是幂等的）。
4. 生成 API 密钥和认证令牌。
5. 将凭证绑定到代理实例（如果提供了 `agent.instance`）。
6. 创建或更新带有触发器和工作流的任务。
7. 创建工作流图（连接触发器和任务的边）。
8. 激活触发器并启动工作流。
9. 将状态保存到 `.openserv.json` 文件中。

### 工作流名称和目标

工作流配置需要两个重要属性：

- **`name`**（字符串）——这将成为 ERC-8004 中的 **代理名称**。请确保名称简洁、有吸引力且易于记忆——这是用户看到的公开品牌名称。例如：`'Viral Content Engine'`、`'Crypto Alpha Scanner'`、`'Life Catalyst Pro'`。
- **`goal`**（字符串，必填）——对工作流功能的详细描述。描述必须清晰完整——过于简短或模糊的目标会导致 API 调用失败。请至少写一句话来解释工作流的用途。

```typescript
workflow: {
  name: 'Deep Research Pro',
  goal: 'Research any topic in depth, synthesize findings from multiple sources, and produce a comprehensive report with citations',
  trigger: triggers.webhook({ waitForCompletion: true, timeout: 600 }),
  task: { description: 'Research the given topic' }
}
```

### 代理实例绑定（v1.1 及更高版本）

将代理实例传递给 `provision()` 以自动绑定凭证：

```typescript
const agent = new Agent({ systemPrompt: '...' })

await provision({
  agent: {
    instance: agent, // Calls agent.setCredentials() automatically
    name: 'my-agent',
    description: '...',
    model_parameters: { model: 'gpt-5', verbosity: 'medium', reasoning_effort: 'high' } // Optional
  },
  workflow: { ... }
})

// agent now has apiKey and authToken set - ready for run()
await run(agent)
```

这样就不需要手动设置 `OPENSERV_API_KEY` 环境变量了。

### 模型参数

可选的 `model_parameters` 字段用于控制平台在为代理执行任务时使用的 LLM 模型和参数（包括无运行时的功能以及 `generate()` 调用）。如果未提供此参数，平台将使用默认设置。

```typescript
await provision({
  agent: {
    instance: agent,
    name: 'my-agent',
    description: '...',
    model_parameters: {
      model: 'gpt-4o',
      temperature: 0.5,
      parallel_tool_calls: false
    }
  },
  workflow: { ... }
})
```

发现可用的模型及其参数：

```typescript
const { models, default: defaultModel } = await client.models.list()
// models: [{ model: 'gpt-5', provider: 'openai', parameters: { ... } }, ...]
// default: 'gpt-5-mini'
```

### 配置结果

```typescript
interface ProvisionResult {
  agentId: number
  apiKey: string
  authToken?: string
  workflowId: number
  triggerId: string
  triggerToken: string
  paywallUrl?: string // For x402 triggers
  apiEndpoint?: string // For webhook triggers
}
```

---

## API 密钥：代理密钥与用户密钥

`provision()` 会生成两种类型的凭证。这两种凭证**不能互换**：

| 凭证类型 | 环境变量            | 使用方          | 用途                                                                                                                                       |
| ------------- | ----------------------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| 代理 API 密钥 | `OPENSERV_API_KEY`      | SDK 内部使用    | 代理从平台接收任务时用于身份验证。请勿与 `PlatformClient` 一起使用。 |
| 钱包密钥    | `WALLET_PRIVATE_KEY`    | `PlatformClient` | 用于管理调用（列出任务、调试工作流、管理代理）。                                                 |
| 用户 API 密钥  | `OPENSERV_USER_API_KEY` | `PlatformClient` | 作为钱包身份验证的替代方案。从平台控制面板获取。                          |

如果您在使用 `PlatformClient` 时收到 **401 Unauthorized** 错误，很可能是误用了代理 API 密钥。请改用钱包身份验证或用户 API 密钥。

---

## PlatformClient：完整的 API 访问

对于高级用例，可以直接使用 `PlatformClient`：

```typescript
import { PlatformClient } from '@openserv-labs/client'

// Using wallet authentication (recommended — uses wallet from provision)
const client = new PlatformClient()
await client.authenticate(process.env.WALLET_PRIVATE_KEY)

// Or using User API key (NOT the agent API key)
const client = new PlatformClient({
  apiKey: process.env.OPENSERV_USER_API_KEY // NOT OPENSERV_API_KEY
})
```

请参阅 `reference.md` 以获取完整的 API 文档，包括：

- `client.agents.*` — 代理管理
- `client.workflows.*` — 工作流管理
- `client.triggers.*` — 触发器管理
- `client.tasks.*` — 任务管理
- `client.models.*` — 可用的 LLM 模型和参数
- `client.integrations.*` — 集成连接
- `client.payments.*` — x402 支付
- `client.web3.*` — 信用额度充值

---

## 触发器工厂

使用 `triggers` 工厂来安全地配置触发器：

```typescript
import { triggers } from '@openserv-labs/client'

// Webhook (free, public endpoint)
triggers.webhook({
  input: { query: { type: 'string', description: 'Search query' } },
  waitForCompletion: true,
  timeout: 600
})

// x402 (paid API with paywall)
triggers.x402({
  name: 'AI Research Assistant',
  description: 'Get comprehensive research reports on any topic',
  price: '0.01',
  timeout: 600,
  input: {
    prompt: {
      type: 'string',
      title: 'Your Request',
      description: 'Describe what you would like the agent to do'
    }
  }
})

// Cron (scheduled)
triggers.cron({
  schedule: '0 9 * * *', // Daily at 9 AM
  timezone: 'America/New_York'
})

// Manual (platform UI only)
triggers.manual()
```

### 超时设置

> **重要提示：** 对于 Webhook 和 x402 触发器，始终将超时时间设置为至少 **600 秒**（10 分钟）。代理处理请求通常需要较长时间——尤其是在多代理工作流中，或者在执行研究、内容生成或其他复杂任务时。如果设置过短的超时时间（例如 180 秒），可能会导致操作提前失败。如有疑问，请选择更长的超时时间。对于包含多个顺序步骤的多代理流程，建议设置 900 秒或更长时间。

### 输入格式

定义 Webhook/x402 支付门槛 UI 的字段：

```typescript
triggers.x402({
  name: 'Content Writer',
  description: 'Generate polished content on any topic',
  price: '0.01',
  input: {
    topic: {
      type: 'string',
      title: 'Content Topic',
      description: 'Enter the subject you want covered'
    },
    style: {
      type: 'string',
      title: 'Writing Style',
      enum: ['formal', 'casual', 'humorous'],
      default: 'casual'
    }
  }
})
```

### Cron 表达式

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sunday=0)
* * * * *
```

常见格式：`0 9 * * *`（每天上午 9 点），`*/5 * * * *`（每 5 分钟一次），`0 9 * * 1-5`（工作日每天上午 9 点）

---

## 状态管理

```typescript
import { getProvisionedInfo, clearProvisionedState } from '@openserv-labs/client'

// Get stored IDs and tokens
const info = getProvisionedInfo('my-agent', 'My Awesome Workflow')

// Clear state (forces fresh creation)
clearProvisionedState()
```

---

## 发现和触发 x402 服务

### 发现可用的服务（无需认证）

`discoverServices()` 会列出所有支持 x402 的公共工作流。**无需认证**——您可以直接在 `PlatformClient` 上调用此方法：

```typescript
import { PlatformClient } from '@openserv-labs/client'

const client = new PlatformClient() // no API key or wallet needed
const services = await client.payments.discoverServices()

for (const service of services) {
  console.log(`${service.name}: $${service.x402Pricing}`)
  console.log(`URL: ${service.webhookUrl}`)
}
```

### 触发器执行

```typescript
// By workflow ID (recommended — resolves the URL automatically)
const result = await client.triggers.fireWebhook({
  workflowId: 123,
  input: { query: 'hello world' }
})

// Or by direct URL
const result = await client.triggers.fireWebhook({
  triggerUrl: 'https://api.openserv.ai/webhooks/trigger/TOKEN',
  input: { query: 'hello world' }
})
```

#### x402（编程方式）

```typescript
// By workflow ID (recommended)
const result = await client.payments.payWorkflow({
  workflowId: 123,
  input: { prompt: 'Hello world' }
})

// Or by direct URL
const result = await client.payments.payWorkflow({
  triggerUrl: 'https://api.openserv.ai/webhooks/x402/trigger/TOKEN',
  input: { prompt: 'Hello world' }
})
```

---

## 环境变量

| 变量                | 描述                  | 是否必需 |
| ----------------------- | ---------------------------- | -------- |
| `OPENSERV_USER_API_KEY` | 用户 API 密钥（来自平台） | 是\*    |
| `WALLET_PRIVATE_KEY`    | 用于 SIWE 身份验证的钱包密钥 | 是\*    |
| `OPENSERV_API_URL`      | 自定义 API URL               | 否       |

\*至少需要其中一个 API 密钥或钱包密钥

---

## ERC-8004：链上代理身份

配置完成后，请在链上注册代理。这会在身份注册处铸造一个 NFT，并将代理的服务端点发布到 IPFS。

> **需要在 Base 链上使用 ETH**。`provision()` 创建的钱包初始余额为零。在注册前，请在 Base 主网上为钱包充值少量 ETH。请使用 `try/catch` 语句来确保即使发生错误，`run(agent)` 也能正常执行。

> **在 `provision()` 后重新加载 `.env` 文件**。`provision()` 会在运行时将 `WALLET_PRIVATE_KEY` 写入 `.env` 文件，但在程序启动时 `process.env` 中可能已经加载了空值。请使用 `dotenv.config({ override: true })` 在 `provision()` 之后加载新生成的密钥。有关完整的 `.env` 配置方式，请参阅 `openserv-agent-sdk` 文档。

```typescript
import { PlatformClient } from '@openserv-labs/client'

// Reload .env to pick up WALLET_PRIVATE_KEY written by provision()
dotenv.config({ override: true })

try {
  const client = new PlatformClient()
  await client.authenticate(process.env.WALLET_PRIVATE_KEY)

  const erc8004 = await client.erc8004.registerOnChain({
    workflowId: result.workflowId,
    privateKey: process.env.WALLET_PRIVATE_KEY!,
    name: 'My Agent',
    description: 'What this agent does'
  })

  console.log(`Agent ID: ${erc8004.agentId}`) // "8453:42"
  console.log(`Explorer: ${erc8004.blockExplorerUrl}`)
  console.log(`Scan: ${erc8004.scanUrl}`) // "https://www.8004scan.io/agents/base/42"
} catch (error) {
  console.warn('ERC-8004 registration skipped:', error instanceof Error ? error.message : error)
}
```

- **首次运行时会铸造一个新的 NFT**。**后续运行会更新 URI**——代理 ID 保持不变。
- 默认链是 Base 主网（8453）。如需使用其他链，请传递 `chainId` 和 `rpcUrl`。
- **除非您有意更换代理 ID，否则不要清除钱包状态**。

请参阅 `reference.md` 以获取完整的 ERC-8004 API 文档（包括钱包管理、链辅助功能及故障排除方法）。

---

## 清理操作

```typescript
await client.workflows.delete({ id: workflowId })
await client.agents.delete({ id: agentId })
clearProvisionedState()
```

---

## 更新本技能

本技能可能会过时。OpenServ 团队会定期发布更新——新的功能、API 变更和 bug 修复不会在这里立即反映。**如果某些功能无法按预期使用，或者您希望确保使用最新信息，请在继续之前更新本技能。**

```bash
# Check if updates are available
npx skills check

# Update all installed skills to latest versions
npx skills update
```

或者直接重新安装 OpenServ 相关技能：

```bash
npx skills add openserv-labs/skills
```

---

## 相关技能

- **openserv-agent-sdk** — 使用该 SDK 构建代理
- **openserv-multi-agent-workflows** — 多代理协作模式
- **openserv-launch** — 在 Base 区块链上发布代币
- **openserv-ideaboard-api** — 在 Ideaboard 上查找想法并发布代理服务