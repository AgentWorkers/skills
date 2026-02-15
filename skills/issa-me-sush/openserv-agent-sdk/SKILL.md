---
name: openserv-agent-sdk
description: 使用 OpenServ SDK (@openserv-labs/sdk) 构建和部署自主 AI 代理。**重要提示**：在阅读本文档的同时，请务必同时查阅配套的 openserv-client 文档，因为这两个包都是构建和运行代理所必需的。openserv-client 包涵盖了多代理工作流程所需的完整平台 API 以及基于 ERC-8004 的链上身份验证机制。有关完整的 API 参考信息，请参阅 reference.md 文档。
---

# OpenServ Agent SDK

使用TypeScript为OpenServ平台构建和部署自定义AI代理。

## 为什么要构建代理？

OpenServ代理是一种服务，它运行您的代码并将其暴露在OpenServ平台上——这样就可以通过工作流、其他代理或付费调用（例如x402）来触发它。平台向您的代理发送任务；您的代理运行您的功能（API、工具、文件处理）并返回结果。您不必使用大型语言模型（LLM）——例如，它可以是一个仅返回数据的静态API。如果您需要LLM推理，有两种选择：使用**无运行时功能**（平台为您处理AI调用——无需API密钥）或使用`generate()`（将LLM调用委托给平台）；或者，您可以引入自己的LLM（任何您可以访问的提供商）。

## 工作原理（流程）

1. **定义您的代理** — 系统提示语加上功能。功能有两种类型：**可运行**（带有Zod模式和`run`处理程序）和**无运行时**（仅需要名称和描述——平台自动处理AI调用）。您还可以在可运行功能中使用`generate()`将LLM调用委托给平台。
2. **在平台上注册** — 您需要在平台上有一个账户；通常最简单的方法是让`provision()`为您自动创建一个账户，方法是创建一个钱包并使用它进行注册（该账户将在后续运行中重复使用）。调用`provision()`（来自`@openserv-labs/client`）：它将创建或重用钱包，注册代理，并将API密钥和认证令牌写入您的环境变量（或者您可以直接传递`agent.instance`来绑定它们）。在开发过程中，您可以跳过设置端点URL；SDK可以使用内置的隧道连接到平台。
3. **启动代理** — 调用`run(agent)`。代理监听任务，运行您的功能（如果您使用了LLM，则运行您的LLM），然后做出响应。详细信息请参阅`reference.md`和`troubleshooting.md`；`examples/`包含完整的可运行代码。

## 您的代理可以做什么

- **无运行时功能** — 仅需要名称和描述。平台自动处理AI调用——无需API密钥，也无需`run()`函数。您可以选择为结构化输入/输出定义`inputSchema`和`outputSchema`。
- **可运行功能** — 代理可以运行的工具（例如搜索、转换数据、调用API）。每个功能都有一个名称、描述、`inputSchema`和`run()`函数。
- **`generate()`方法** — 从任何可运行功能内部将LLM调用委托给平台。无需API密钥——平台执行调用并记录使用情况。支持文本和结构化输出。
- **任务上下文** — 在执行任务时，代理可以通过`addLogToTask()`和`uploadFile()`等方法将日志附加到该任务中。
- **多代理工作流** — 您的代理可以与其他代理一起参与工作流；有关平台API、工作流和ERC-8004链上身份的信息，请参阅**openserv-client**技能。

**参考：**`reference.md`（模式）· `troubleshooting.md`（常见问题）· `examples/`（完整示例）

## 快速入门

### 安装

```bash
npm install @openserv-labs/sdk @openserv-labs/client zod
```

> **注意：**只有当您使用`process()`方法进行直接OpenAI调用时才需要`openai`。大多数代理不需要它——请使用无运行时功能或`generate()`。

### 最小代理

请参阅`examples/basic-agent.ts`以获取完整的可运行示例。

模式很简单：

1. 创建一个带有系统提示语的`Agent`。
2. 使用`agent.addCapability()`添加功能。
3. 调用`provision()`在平台上注册（传递`agent.instance`以绑定凭据）。
4. 调用`run(agent)`以启动代理。

---

## 完整代理模板

### 文件结构

```
my-agent/
├── src/agent.ts
├── .env
├── .gitignore
├── package.json
└── tsconfig.json
```

### 依赖项

```bash
npm init -y && npm pkg set type=module
npm i @openserv-labs/sdk @openserv-labs/client dotenv zod
npm i -D @types/node tsx typescript
```

> **注意：**项目必须在`package.json`中设置`"type": "module"`。添加一个`"dev": "tsx src/agent.ts"`脚本用于本地开发。只有当您使用`process()`方法进行直接OpenAI调用时才需要安装`openai`。

### `.env`

大多数代理不需要任何LLM API密钥——使用**无运行时功能**或`generate()`，平台会为您处理LLM调用。如果您使用`process()`进行直接OpenAI调用，请设置`OPENAI_API_KEY`。其余内容由`provision()`填充。

```env
# Only needed if you use process() for direct OpenAI calls:
# OPENAI_API_KEY=your-openai-key
# ANTHROPIC_API_KEY=your_anthropic_key  # If using Claude directly

# Auto-populated by provision():
WALLET_PRIVATE_KEY=
OPENSERV_API_KEY=
OPENSERV_AUTH_TOKEN=
PORT=7378
# Production: skip tunnel and run HTTP server only
# DISABLE_TUNNEL=true
# Force tunnel even when endpointUrl is set
# FORCE_TUNNEL=true
```

---

## 功能

功能有两种类型：

### 无运行时功能（推荐用于大多数用例）

无运行时功能不需要`run`函数——平台自动处理AI调用。只需提供名称和描述：

```typescript
// Simplest form — just name + description
agent.addCapability({
  name: 'generate_haiku',
  description: 'Generate a haiku poem (5-7-5 syllables) about the given input.'
})

// With custom input schema
agent.addCapability({
  name: 'translate',
  description: 'Translate text to the target language.',
  inputSchema: z.object({
    text: z.string(),
    targetLanguage: z.string()
  })
})

// With structured output
agent.addCapability({
  name: 'analyze_sentiment',
  description: 'Analyze the sentiment of the given text.',
  outputSchema: z.object({
    sentiment: z.enum(['positive', 'negative', 'neutral']),
    confidence: z.number().min(0).max(1)
  })
})
```

- **无需`run`函数** — 平台执行LLM调用
- **无需API密钥** — 平台负责处理
- `inputSchema`是可选的 — 如果省略，则默认为`z.object({ input: z.string() })`
- `outputSchema`是可选的 — 用于定义平台的结构化输出

请参阅`examples/haiku-poet-agent.ts`以获取完整的无运行时功能示例。

### 可运行功能

可运行功能具有`run`函数，用于执行自定义逻辑。每个功能都需要：

- `name` - 唯一标识符
- `description` - 它的功能（帮助AI决定何时使用它）
- `inputSchema` - 定义参数的Zod模式
- `run` - 返回字符串的函数

```typescript
agent.addCapability({
  name: 'greet',
  description: 'Greet a user by name',
  inputSchema: z.object({ name: z.string() }),
  async run({ args }) {
    return `Hello, ${args.name}!`
  }
})
```

请参阅`examples/capability-example.ts`以了解基本功能。

> **注意：**`schema`属性仍然可以作为`inputSchema`的别名使用，但已被弃用。在新代码中使用`inputSchema`。

### 使用代理方法

在功能中访问`this`以使用代理方法，如`addLogToTask()`、`uploadFile()`、`generate()`等。

请参阅`examples/capability-with-agent-methods.ts`以了解日志记录和文件上传的示例。

---

## 代理方法

### `generate()` — 平台委托的LLM调用

`generate()`方法允许您在没有API密钥的情况下进行LLM调用。平台执行调用并将使用情况记录在工作区中。

```typescript
// Text generation
const poem = await this.generate({
  prompt: `Write a short poem about ${args.topic}`,
  action
})

// Structured output (returns validated object matching the schema)
const metadata = await this.generate({
  prompt: `Suggest a title and 3 tags for: ${poem}`,
  outputSchema: z.object({
    title: z.string(),
    tags: z.array(z.string()).length(3)
  }),
  action
})

// With conversation history
const followUp = await this.generate({
  prompt: 'Suggest a related topic.',
  messages,  // conversation history from run function
  action
})
```

参数：
- `prompt` (string) — LLM的提示语
- `action` (ActionSchema) — 操作上下文（传递给您的`run`函数）
- `outputSchema` (Zod schema, optional) — 提供时，返回验证过的结构化输出
- `messages` (array, optional) — 多轮对话的历史记录

`action`参数是必需的，因为它用于标识工作区/任务以便计费。在可运行功能中可以使用它，因为`action`可以从`run`函数的参数中获取。

### 任务管理

```typescript
await agent.createTask({ workspaceId, assignee, description, body, input, dependencies })
await agent.updateTaskStatus({ workspaceId, taskId, status: 'in-progress' })
await agent.addLogToTask({ workspaceId, taskId, severity: 'info', type: 'text', body: '...' })
await agent.markTaskAsErrored({ workspaceId, taskId, error: 'Something went wrong' })
const task = await agent.getTaskDetail({ workspaceId, taskId })
const tasks = await agent.getTasks({ workspaceId })
```

### 文件操作

```typescript
const files = await agent.getFiles({ workspaceId })
await agent.uploadFile({ workspaceId, path: 'output.txt', file: 'content', taskIds: [taskId] })
await agent.deleteFile({ workspaceId, fileId })
```

---

## 操作上下文

功能中的`action`参数是一个**联合类型** — `task`仅存在于`'do-task'`变体中。在访问`action.task`之前，请始终使用类型保护：

```typescript
async run({ args, action }) {
  // action.task does NOT exist on all action types — you must narrow first
  if (action?.type === 'do-task' && action.task) {
    const { workspace, task } = action
    workspace.id        // Workspace ID
    workspace.goal      // Workspace goal
    task.id             // Task ID
    task.description    // Task description
    task.input          // Task input
    action.me.id        // Current agent ID
  }
}
```

**不要**在类型保护之前提取`action?.task?.id` — TypeScript会因为“Property 'task' does not exist on type 'ActionSchema'”而报错。

---

## 工作流名称和目标

`provision()`中的`workflow`对象需要两个重要属性：

- **`name` (string) - 这将成为ERC-8004中的**代理名称**。请使其简洁、有力且易于记忆——这是用户看到的公开品牌名称。考虑产品发布，而不是变量名称。示例：`'Crypto Alpha Scanner'`、`AI Video Studio`、`Instant Blog Machine'`。
- **`goal` (string, required) - 对工作流完成方式的详细描述。必须具有描述性和完整性——简短或模糊的目标会导致API调用失败。至少写一个完整的句子来解释工作流的用途。

```typescript
workflow: {
  name: 'Haiku Poetry Generator',  // Polished display name — the ERC-8004 agent name users see
  goal: 'Transform any theme or emotion into a beautiful traditional 5-7-5 haiku poem using AI',
  trigger: triggers.x402({ ... }),
  task: { description: 'Generate a haiku about the given topic' }
}
```

---

## 触发类型

```typescript
import { triggers } from '@openserv-labs/client'

triggers.webhook({ waitForCompletion: true, timeout: 600 })
triggers.x402({ name: '...', description: '...', price: '0.01', timeout: 600 })
triggers.cron({ schedule: '0 9 * * *' })
triggers.manual()
```

> **重要：**对于Webhook和x402触发器，始终将`timeout`设置为至少**600秒**（10分钟）。代理通常需要很长时间来处理请求——尤其是在进行研究、内容生成或其他复杂任务时。较短的超时会导致过早失败。对于具有许多顺序步骤的多代理管道，请考虑900秒或更长时间。

---

## 部署

### 本地开发

```bash
npm run dev
```

`run()`函数会自动：

- 启动代理的HTTP服务器（端口7378，具有自动回退机制）
- 通过WebSocket连接到`agents-proxy.openserv.ai`
- 将平台请求路由到您的本地机器

**无需ngrok或其他隧道工具** — `run()`可以无缝处理这一切。只需调用`run(agent)`，您的本地代理就可以被平台访问。

### 生产环境

当部署到Cloud Run等托管提供商时，将`DISABLE_TUNNEL=true`设置为环境变量。这样`run()`将仅启动HTTP服务器，而不会打开WebSocket隧道——平台会直接通过其公共URL访问您的代理。

```typescript
await provision({
  agent: {
    name: 'my-agent',
    description: '...',
    endpointUrl: 'https://my-agent.example.com' // Required for production
  },
  workflow: {
    name: 'Lightning Service Pro',
    goal: 'Describe in detail what this workflow does — be thorough, vague goals cause failures',
    trigger: triggers.webhook({ waitForCompletion: true, timeout: 600 }),
    task: { description: 'Process incoming requests' }
  }
})

// With DISABLE_TUNNEL=true, run() starts only the HTTP server (no tunnel)
await run(agent)
```

---

## ERC-8004：链上代理身份

配置完成后，通过身份注册表在链上注册您的代理以便被发现。

> **需要在Base网络上使用ETH。**注册会调用ERC-8004合约上的`register()`（链8453），这需要支付Gas费用。`provision()`创建的钱包初始余额为零。在首次尝试注册之前，请用少量ETH为其充值。钱包地址会在配置过程中记录（例如：“Created new wallet: 0x...”）。

> **始终使用try/catch`语句**，以防注册失败（例如钱包未充值）阻止`run(agent)`的启动。

两个重要的模式：

1. **程序化地使用`dotenv`（而不是`import 'dotenv/config'）**，以便在`provision()`写入`WALLET_PRIVATE_KEY`后重新加载`.env`。
2. **在`provision()`之后调用`dotenv.config({ override: true })**，以便在ERC-8004注册之前获取新写入的密钥。

```typescript
import dotenv from 'dotenv'
dotenv.config()

import { Agent, run } from '@openserv-labs/sdk'
import { provision, triggers, PlatformClient } from '@openserv-labs/client'

// ... define agent and capabilities ...

const result = await provision({
  agent: { instance: agent, name: 'my-agent', description: '...' },
  workflow: {
    name: 'My Service',
    goal: 'Detailed description of what the workflow does',
    trigger: triggers.x402({ name: 'My Service', description: '...', price: '0.01', timeout: 600 }),
    task: { description: 'Process requests' }
  }
})

// Reload .env to pick up WALLET_PRIVATE_KEY written by provision()
dotenv.config({ override: true })

// Register on-chain (non-blocking — requires funded wallet on Base)
try {
  const client = new PlatformClient()
  await client.authenticate(process.env.WALLET_PRIVATE_KEY)

  const erc8004 = await client.erc8004.registerOnChain({
    workflowId: result.workflowId,
    privateKey: process.env.WALLET_PRIVATE_KEY!,
    name: 'My Service',
    description: 'What this agent does'
  })

  console.log(`Agent ID: ${erc8004.agentId}`) // "8453:42"
  console.log(`TX: ${erc8004.blockExplorerUrl}`)
  console.log(`Scan: ${erc8004.scanUrl}`) // "https://www.8004scan.io/agents/base/42"
} catch (error) {
  console.warn('ERC-8004 registration skipped:', error instanceof Error ? error.message : error)
}

await run(agent)
```

- **首次运行**会创建一个新的身份NFT。**重新运行时会更新URI** — 代理ID保持不变。
- **除非您有意更改，否则不要清除钱包状态**。要更新元数据，只需重新运行即可。
- 默认链：Base主网（8453）。对于其他链，请传递`chainId` / `rpcUrl`。

有关完整的ERC-8004 API参考和故障排除信息，请参阅**openserv-client**技能。

---

## 不要使用

- **`this.process()`** 在功能内部使用 — 这是一个过时的方法，需要OpenAI API密钥。请使用`this.generate()`（平台委托，无需密钥），或使用无运行时功能。
- **`doTask`覆盖** — SDK会自动处理任务执行。
- **`this.completeTask()` — 任务完成由运行时API处理

---

## 更新此技能

此技能可能会过时。OpenServ团队会定期发布更新——新的功能、API变更和错误修复不会在这里反映出来，直到您更新。**如果某些功能未按预期工作，或者您想确保拥有最新信息，请在继续之前更新此技能。**

```bash
# Check if updates are available
npx skills check

# Update all installed skills to latest versions
npx skills update
```

或者直接重新安装OpenServ技能：

```bash
npx skills add openserv-labs/skills
```

---

## 相关技能

- **openserv-client** - 完整的平台客户端API参考
- **openserv-multi-agent-workflows** - 多代理协作模式
- **openserv-launch** - 在Base区块链上发布令牌
- **openserv-ideaboard-api** - 在Ideaboard上查找想法和发布代理服务