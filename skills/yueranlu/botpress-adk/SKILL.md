---
name: adk
description: 使用 Botpress 的 Agent Development Kit (ADK) 构建 AI 机器人的指南
version: 1.0.0
author: yueranlu
tags: [botpress, adk, chatbot, ai, typescript]
homepage: https://github.com/botpress/adk
---

# Botpress ADK开发指南

本指南详细介绍了如何使用Botpress代理开发工具包（ADK）构建AI机器人。

## 使用场景

- 用户希望创建Botpress机器人或聊天机器人
- 用户提到ADK、代理开发工具包或Botpress
- 用户需要创建动作（Actions）、工具（Tools）、工作流（Workflows）、对话（Conversations）、表格（Tables）、触发器（Triggers）或知识库（Knowledge Bases）
- 用户需要帮助使用`adk`命令行界面（CLI）的命令（如`init`、`dev`、`deploy`、`link`）
- 用户遇到与ADK相关的问题或需要故障排除
- 用户询问关于机器人配置、状态管理或集成的问题

## 快速参考

ADK是一个基于约定的TypeScript框架，其中文件结构直接决定了机器人的行为。

**您的角色：**指导用户完成整个机器人开发生命周期，从项目设置到部署。使用本指南中的模式和代码示例来编写正确的、可运行的ADK代码。

**关键原则：**在ADK中，**文件的位置非常重要**。每种组件类型都有特定的`src/`子目录，文件会根据位置自动被识别。

## 如何使用本指南

**本指南是您构建Botpress机器人的主要参考资料。**当用户请求使用ADK构建某些功能时，请按照以下步骤操作：

1. **确定需求**：是需要一个新的机器人、功能（动作、工具、工作流）、数据存储（表格）还是事件处理（触发器）？
2. **检查正确的目录**：每种组件类型都位于特定的`src/`子目录中。
3. **遵循代码示例**：严格按照代码示例操作，它们代表了正确的ADK规范。
4. **运行`adk --help`**：对于未在此处覆盖的CLI命令，可以使用`adk <command> --help`获取具体帮助。

**决策指南 - 创建什么组件：**

| 用户需求 | 创建内容 | 位置 |
|------------------|-------------|----------|
| 处理用户消息 | 对话（Conversations） | `src/conversations/` |
| 添加AI可调用的功能 | 工具（Tools） | `src/tools/` |
| 添加可重用的业务逻辑 | 动作（Actions） | `src/actions/` |
| 运行后台/定时任务 | 工作流（Workflows） | `src/workflows/` |
| 存储结构化数据 | 表格（Tables） | `src/tables/` |
| 对事件作出反应（用户创建等） | 触发器（Triggers） | `src/triggers/` |
| 让AI访问文档/数据 | 知识库（Knowledge Bases） | `src/knowledge/` |
| 连接外部服务（如Slack） | 集成（Integrations） | `adk add <名称>` |

**如果本指南中的信息不够，请**查阅相应部分的GitHub参考文件（提供链接）以获取更详细的规范。

## 重要提示：ADK是AI原生的

ADK**不**使用传统的聊天机器人模式。**请不要创建意图（Intents）、实体（Entities）或对话流程（Dialog Flows）。

**替代方法：**
- 定义意图（如`greet`、`orderPizza`、`checkStatus`）
- 训练实体提取（如`@pizzaSize`、`@toppings`）
- 手动路由到意图处理程序

**ADK使用的方法：**
- `execute()`：AI能够直接从指令中理解用户意图
- 工具（Tools）：AI自主决定何时调用您的功能
- `zai.extract()`：基于模式的结构化数据提取
- 知识库（Knowledge Bases）：用于为响应提供上下文

**文档：**https://www.botpress.com/docs/adk/
**GitHub：**https://github.com/botpress/skills/tree/master/skills/adk/

---

## 先决条件与安装

在使用ADK之前，请确保用户具备以下条件：

- **Botpress账户**：在https://app.botpress.cloud创建账户
- **Node.js v22.0.0+**：使用`node --version`检查版本
- **包管理器**：推荐使用bun、pnpm或yarn

**安装ADK CLI：**

- macOS & Linux：
  ```bash
curl -fsSL https://github.com/botpress/adk/releases/latest/download/install.sh | bash
```

- Windows（PowerShell）：
  ```powershell
powershell -c "irm https://github.com/botpress/adk/releases/latest/download/install.ps1 | iex"
```

**验证安装：**
  ```bash
adk --version
```

如果安装失败，请查看https://github.com/botpress/adk/releases以获取手动下载选项。

**文档：**https://www.botpress.com/docs/adk/quickstart
**GitHub：**https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/cli.md

---

## 快速入门

安装ADK CLI后，创建一个新的机器人：

```bash
adk init my-bot         # Create project (choose "Hello World" template for beginners)
cd my-bot
npm install             # Or bun/pnpm/yarn
adk login               # Authenticate with Botpress Cloud
adk add chat            # Add the chat integration for testing
adk dev                 # Start dev server with hot reload
adk chat                # Test in CLI (run in separate terminal)
adk deploy              # Deploy to production when ready
```

通过**http://localhost:3001/**的可视化控制台，您可以配置集成并测试机器人。

**文档：**https://www.botpress.com/docs/adk/quickstart
**GitHub：**https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/cli.md

---

## 链接和部署机器人

**重要提示：**您的机器人必须链接到Botpress Cloud并部署才能正常工作。ADK在开发过程中运行在本地，但机器人本身存储在Botpress Cloud中。

### 正确顺序：链接 → 开发 → 部署

按照以下顺序操作以使机器人生效：

```bash
# 1. LINK - Connect your project to Botpress Cloud (creates agent.json)
adk link

# 2. DEV - Start the development server (hot reload, testing)
adk dev

# 3. DEPLOY - Push to production when ready
adk deploy
```

**步骤说明：**

1. **`adk link`**：将本地项目链接到Botpress Cloud中的机器人。这会生成包含工作区和机器人ID的`agent.json`文件。在其他操作之前，请先运行此命令。
2. **`adk dev`**：启动本地开发服务器，并支持热重载。在http://localhost:3001打开开发控制台，您可以在此配置集成并测试机器人。在另一个终端中使用`adk chat`进行测试。
3. **`adk deploy`**：将机器人部署到生产环境。当您准备好让机器人通过生产渠道（如Slack、WhatsApp、Webchat等）访问时，运行此命令。

### 故障排除

**如果在运行`adk dev`或`adk deploy`时遇到错误：**

1. **检查日志**：查看终端输出或http://localhost:3001开发控制台中的日志面板。
2. **复制错误信息**：从日志中选择并复制完整的错误信息。
3. **寻求帮助**：将错误信息粘贴回AI助手，并请求其帮助解决问题。

**常见错误场景：**
- **集成配置错误**：通常意味着需要在http://localhost:3001的UI中配置集成。
- **类型错误**：通常由导入错误或模式不匹配引起。
- **部署失败**：可能表示缺少环境变量或配置无效。

**示例错误处理流程：**
```
1. Run `adk dev` or `adk deploy`
2. See error in terminal/logs
3. Copy the error message
4. Tell the AI: "I got this error when running adk dev: [paste error]"
5. The AI will help diagnose and fix the issue
```

**文档：**https://www.botpress.com/docs/adk/quickstart
**GitHub：**https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/cli.md

---

## 项目结构

**重要规则：**文件的位置决定了其行为。**请将组件放置在正确的`src/`子目录中，否则它们将无法被识别。

**关键配置文件：**

- **agent.config.ts**：主要配置文件，定义机器人元数据、AI模型、状态模式和集成（您可以编辑此文件）。
- **agent.json**：将代理与工作区/机器人ID关联起来。由`adk link`或`adk dev`自动生成。**请将其添加到`.gitignore`中**，因为它包含因开发者而异的环境特定ID。
- **package.json**：Node.js配置文件，包含`@botpress/runtime`依赖项以及`dev`、`build`、`deploy`脚本。
- **tsconfig.json**：项目的TypeScript配置文件。
- **.env**：环境变量文件，用于存储API密钥和秘密信息（切勿提交！）
- **.gitignore**：应包含`agent.json`、`.env`、`node_modules/`、`.botpress/`。

**文档：**https://www.botpress.com/docs/adk/project-structure
**GitHub：**https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/agent-config.md

---

## 代理配置

`agent.config.ts`文件定义了机器人的身份、AI模型、状态模式和集成。设置新机器人时，请始终从这里开始。

```typescript
import { defineConfig, z } from "@botpress/runtime";

export default defineConfig({
  name: "my-support-bot",
  description: "AI customer support assistant",

  // AI models for different operations
  defaultModels: {
    autonomous: "openai:gpt-4o",      // Used by execute() for conversations
    zai: "openai:gpt-4o-mini"         // Used by zai operations (cheaper, faster)
  },

  // Global bot state - shared across all conversations and users
  bot: {
    state: z.object({
      maintenanceMode: z.boolean().default(false),
      totalConversations: z.number().default(0)
    })
  },

  // Per-user state - persists across all conversations for each user
  user: {
    state: z.object({
      name: z.string().optional(),
      tier: z.enum(["free", "pro"]).default("free"),
      preferredLanguage: z.enum(["en", "es", "fr"]).default("en")
    }),
    tags: {
      source: z.string(),
      region: z.string().optional()
    }
  },

  // Per-conversation state
  conversation: {
    state: z.object({
      context: z.string().optional()
    }),
    tags: {
      category: z.enum(["support", "sales", "general"]),
      priority: z.enum(["low", "medium", "high"]).optional()
    }
  },

  // Integrations your bot uses (ADK 1.9+ format)
  dependencies: {
    integrations: {
      chat: { version: "chat@0.7.3", enabled: true },
      slack: { version: "slack@2.5.5", enabled: true }
    }
  }
});
```

**可用模型：**
- OpenAI：`openai:gpt-4o`、`openai:gpt-4o-mini`、`openai:gpt-4-turbo`
- Anthropic：`anthropic:claude-3-5-sonnet`、`anthropic:claude-3-opus`
- Google：`google:gemini-1.5-pro`、`google:gemini-1.5-flash`

**文档：**https://www.botpress.com/docs/adk/project-structure
**GitHub：**https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/agent-config.md

---

## 核心概念

### 1. 动作（Actions） - 可重用的业务逻辑

**何时创建动作：**
- 当您需要可重用的逻辑，并且该逻辑将在多个地方被调用时（如工作流、对话、触发器）。
- 当您正在封装外部API或数据库操作时。
- 当您需要可测试、可组合的业务逻辑时。
- 当您需要调用集成API（如Slack、Linear等）并使用自定义逻辑时。

**何时不使用动作（而使用工具：**  
- 当您希望AI自主决定何时调用该功能时。
- 该功能应在`execute()`期间可用。

**位置：**`src/actions/`

**调用动作：**
```typescript
import { Action, z } from "@botpress/runtime";

export const fetchUser = new Action({
  name: "fetchUser",
  description: "Retrieves user details from the database",

  // Define input/output with Zod schemas for type safety
  input: z.object({ userId: z.string() }),
  output: z.object({ name: z.string(), email: z.string() }),

  // IMPORTANT: Handler receives { input, client } - destructure input INSIDE the handler
  async handler({ input, client }) {
    const { user } = await client.getUser({ id: input.userId });
    return { name: user.name, email: user.tags.email };
  }
});
```

**关键规则：**
- 处理程序接收`{ input, client }`：必须在处理程序内部解构`input`。
- 不能直接在参数中解构输入字段。
- 可以调用其他动作、集成动作或访问状态。
- 可以使用`.asTool()`将其转换为工具。

**文档：**https://www.botpress.com/docs/adk/concepts/actions
**GitHub：**https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/actions.md

---

### 2. 工具（Tools） - AI可调用的函数

**何时创建工具：**
- 当您希望AI自主决定何时使用该功能时。
- 该功能需要检索AI所需的信息（搜索、查找、获取）。
- 该功能需要代表用户执行操作（创建工单、发送消息）。
- 当您正在构建AI在对话中应具备的功能时。

**AI根据以下因素决定使用工具：**
1. 工具的`description`：明确说明其使用时机。
2. 输入模式的`.describe()`字段：帮助AI理解参数的含义。
3. 对话上下文和用户意图。

**工具与动作的主要区别：**  
- 工具可以直接解构输入；动作则不能。

**位置：**`src/tools/`

**使用ThinkSignal：**当工具无法完成任务但您希望为AI提供上下文时：**
```typescript
import { Autonomous } from "@botpress/runtime";

// Inside handler - AI will see this message and can respond appropriately
throw new Autonomous.ThinkSignal(
  "No results found",
  "No products found matching that query. Ask user to try different search terms."
);
```

**高级工具属性：**
```typescript
export const myTool = new Autonomous.Tool({
  name: "myTool",
  description: "Tool description",
  input: z.object({...}),
  output: z.object({...}),
  aliases: ["searchDocs", "findDocs"],  // Alternative names
  handler: async (input, ctx) => {
    console.log(`Call ID: ${ctx.callId}`);  // Unique call identifier
    // ...
  },
  retry: async ({ attempt, error }) => {
    if (attempt < 3 && error?.code === 'RATE_LIMIT') {
      await new Promise(r => setTimeout(r, 1000 * attempt));
      return true;  // Retry
    }
    return false;  // Don't retry
  }
});
```

**文档：**https://www.botpress.com/docs/adk/concepts/tools**
**GitHub：**https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/tools.md

---

### 3. 对话（Conversations） - 消息处理程序

**何时创建对话：**
- 每个机器人至少需要一个对话处理程序来响应用户。
- 如果不同渠道需要不同的行为，请为它们创建单独的处理程序。
- 使用`channel: "*"`来使用一个处理程序处理所有渠道。

**构建对话时的关键决策：**
1. **哪些渠道？** - 指定`"*"`以处理所有渠道，或指定特定渠道（如`slack.dm`）。
2. **AI需要哪些工具？** - 将它们传递给`execute({ tools: [...] })`。
3. **哪些知识应该用于生成响应？** - 传递给`execute({ knowledge: [...] })`。
4. **哪些指令指导AI？** - 定义机器人的人格、规则和上下文。

**`execute()`函数是ADK的核心**——它使用工具和知识运行自主AI逻辑。大多数对话处理程序都会调用`execute()`。

**位置：**`src/conversations/`

**处理程序上下文：**
- `message`：用户消息数据。
- `execute`：运行自主AI逻辑。
- `conversation`：对话实例方法（发送、开始打字、停止打字）。
- `state`：可变状态（机器人、用户、对话）。
- `client`：Botpress API客户端。
- `type`：事件类型（消息、工作流请求）。

**执行函数选项：**
```typescript
await execute({
  instructions: string | async function,  // Required
  tools: Tool[],                          // AI-callable tools
  knowledge: Knowledge[],                 // Knowledge bases for RAG
  exits: Exit[],                          // Structured exit handlers
  model: string,                          // AI model to use
  temperature: number,                    // 0-1, default 0.7
  iterations: number,                     // Max tool calls, default 10
  hooks: {
    onBeforeTool: async ({ tool, input }) => { ... },
    onAfterTool: async ({ tool, output }) => { ... },
    onTrace: async (trace) => { ... }
  }
});
```

**常见渠道：**`chat.channel`、`webchat.channel`、`slack.dm`、`slack.channel`、`discord.channel`、`"*"`（所有渠道）。

**文档：**https://www.botpress.com/docs/adk/concepts/conversations`
**GitHub：**https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/conversations.md

---

### 4. 工作流（Workflows） - 后台与多步骤流程

**何时创建工作流：**
- 需要超过2分钟的操作（默认超时）。
- 需要持续运行的多步骤流程。
- 定时/周期性任务（每日报告、定期同步）。
- 需要等待外部事件或用户输入的操作。

**何时不使用工作流（而在对话中处理）：**
- 需要立即完成的快速操作。
- 简单的请求-响应模式。
- 不需要持久化的操作。

**工作流的关键概念：**
- **步骤是检查点**：如果工作流崩溃，它将从最后一个完成的步骤继续。
- **状态会持久化**：在`state`中存储进度以跟踪各个步骤。
- **始终传递conversationId**：如果工作流需要向用户发送消息。

**位置：**`src/workflows/`

**步骤方法：**

| 方法 | 用途 |
|--------|---------|
| `step(name, fn)` | 带有缓存的基本执行 |
| `step.sleep(name, ms)` | 暂停指定毫秒数 |
| `step.sleepUntil(name, date)` | 暂停直到指定日期 |
| `step.listen()` | 等待外部事件 |
| `step.progress(msg)` | 更新进度消息 |
| `step.request(name, prompt)` | 请求用户输入（阻塞） |
| `step.executeWorkflow()` | 启动并等待另一个工作流 |
| `step.waitForWorkflow(id)` | 等待现有工作流 |
| `step.map(items, fn)` | 并发处理数组 |
| `step.forEach(items, fn)` | 成组处理项目 |
| `step.batch(items, fn)` | 分组处理项目 |
| `step.fail(reason)` | 标记工作流失败 |
| `step.abort()` | 立即停止，不报告错误 |

**关键规则：**
- 步骤名称必须**唯一**且**稳定**（避免在循环中使用动态命名）。
- 状态作为参数传递，不要通过`this.state`访问。
- 如果工作流需要向用户发送消息，请始终传递`conversationId`。
- 默认超时为2分钟——对于较长的流程，请使用步骤。

**文档：**https://www.botpress.com/docs/adk/concepts/workflows/overview**
**GitHub：**https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/workflows.md

---

### 5. 表格（Tables） - 数据存储

**何时创建表格：**
- 需要持久化结构化数据（用户、订单、工单、日志）。
- 需要根据字段查询/过滤数据。
- 需要对文本内容进行语义搜索（设置`searchable: true`）。
- 需要存储的数据应在机器人重启后仍然可用。

**何时不使用表格（而使用状态：**
- 对于每个用户/对话的简单键值数据，使用`user.state`或`conversation.state`。
- 临时数据不需要持久化。
- 数据量较小，适合存储在状态中。

**表格与知识库的区别：**
- **表格** = 可进行CRUD操作的结构化数据（创建、读取、更新、删除）。
- **知识库** = 供AI搜索和参考的文档/内容。

**关键规则（违反规则会导致错误）：**
- **不要定义`id`列**——它将自动生成为数字。
- 表格名称必须以“Table”结尾（例如`OrdersTable`，而不是`Orders`）。

**CRUD操作：**
```typescript
// Create - id is auto-assigned
await OrdersTable.createRows({
  rows: [{ orderId: "ord-123", userId: "user-456", status: "pending", total: 99.99, createdAt: new Date() }]
});

// Read with filters
const { rows } = await OrdersTable.findRows({
  filter: { userId: "user-456", status: "pending" },
  orderBy: "createdAt",
  orderDirection: "desc",
  limit: 10
});

// Get single row by id
const row = await OrdersTable.getRow({ id: 123 });

// Semantic search (on searchable columns)
const { rows } = await OrdersTable.findRows({
  search: "delivery issue",
  limit: 5
});

// Update - must include the id
await OrdersTable.updateRows({
  rows: [{ id: 1, status: "completed" }]
});

// Upsert - insert or update based on key column
await OrdersTable.upsertRows({
  rows: [{ orderId: "ord-123", status: "shipped" }],
  keyColumn: "orderId"
});

// Delete by filter
await OrdersTable.deleteRows({ status: "cancelled" });

// Delete by IDs
await OrdersTable.deleteRowIds([123, 456]);
```

**高级功能：计算列：**
```typescript
columns: {
  basePrice: z.number(),
  taxRate: z.number(),
  fullPrice: {
    computed: true,
    schema: z.number(),
    dependencies: ["basePrice", "taxRate"],
    value: async (row) => row.basePrice * (1 + row.taxRate)
  }
}
```

**文档：**https://www.botpress.com/docs/adk/concepts/tables**
**GitHub：**https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/tables.md**

---

### 6. 知识库（Knowledge Bases） - 用于AI上下文的检索式问答（RAG）

**何时创建知识库：**
- 当您希望AI根据文档回答问题时。
- 当您有FAQ、政策或产品信息供AI引用时。
- 当您希望AI的响应基于具体内容时（而不是凭空生成）。
- 当您正在构建需要访问帮助文章的支持机器人时。

**ADK中RAG的工作原理：**
1. 您定义知识来源（网站、文件、表格）。
2. 内容被索引并嵌入以便进行语义搜索。
3. 在`execute()`期间，AI会自动搜索相关知识。
4. AI使用检索到的内容生成基于上下文的响应。

**选择数据源类型：**
- **网站** - 索引公共文档、帮助站点、博客。
- **目录** - 索引本地Markdown/文本文件（仅限开发使用！）
- **表格** - 索引来自表格的结构化数据。

**位置：**`src/knowledge/`

**文档：**https://www.botpress.com/docs/adk/concepts/knowledge**
**GitHub：**https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/knowledge-bases.md`

---

### 7. 触发器（Triggers） - 基于事件的自动化

**何时创建触发器：**
- 当您需要自动响应事件时（例如用户注册、问题创建等）。
- 当特定事件发生时，您希望启动工作流。
- 当外部系统发生变化时，您需要同步数据。
- 当您需要根据事件发送通知时。

**常见触发器模式：**
- **用户注册** - 在`user.created`时触发→启动注册工作流。
- **集成同步** - 在`linear:issueCreated`时触发→在表格中创建记录。
- **通知** - 在`workflow_completed`时触发→发送Slack消息。

**查找可用事件：**
- 机器人事件：`user.created`、`conversationstarted`、`workflow_completed`等。
- 集成事件：运行`adk info <integration> --events`查看可用事件。

**文档：**https://www.botpress.com/docs/adk/concepts/triggers**
**GitHub：**https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/triggers**

---

## 发送消息

**重要提示：**方法取决于发送的位置：**

| 上下文 | 方法 | 原因 |
|---------|--------|-----|
| 在对话中 | `conversation.send()` | 有对话上下文 |
| 在工作流/动作中 | `client.createMessage()` | 需要`conversationId` |

**常见错误：**在对话中使用`client.createMessage()`。**始终使用`conversation.send()`。

**在对话中**：使用`conversation.send()`：
```typescript
await conversation.send({ type: "text", payload: { text: "Hello!" } });
await conversation.send({ type: "image", payload: { imageUrl: "https://..." } });
await conversation.send({
  type: "choice",
  payload: {
    text: "Pick one:",
    choices: [
      { title: "Option A", value: "a" },
      { title: "Option B", value: "b" }
    ]
  }
});
```

**在工作流或动作中**：使用`client.createMessage()`并传递`conversationId`：
```typescript
await client.createMessage({
  conversationId: input.conversationId,  // Must have this!
  type: "text",
  payload: { text: "Workflow complete!" }
});
```

**所有消息类型：**
```typescript
// Text
{ type: "text", payload: { text: "Hello!" } }

// Markdown
{ type: "markdown", payload: { text: "# Heading\n**Bold**" } }

// Image
{ type: "image", payload: { imageUrl: "https://..." } }

// Audio
{ type: "audio", payload: { audioUrl: "https://..." } }

// Video
{ type: "video", payload: { videoUrl: "https://..." } }

// File
{ type: "file", payload: { fileUrl: "https://...", title: "Document.pdf" } }

// Location
{ type: "location", payload: { latitude: 40.7128, longitude: -74.0060, address: "New York, NY" } }

// Card
{ type: "card", payload: {
  title: "Product Name",
  subtitle: "Description",
  imageUrl: "https://...",
  actions: [
    { action: "url", label: "View", value: "https://..." },
    { action: "postback", label: "Buy", value: "buy_123" }
  ]
}}

// Carousel
{ type: "carousel", payload: {
  items: [
    { title: "Item 1", subtitle: "...", imageUrl: "...", actions: [...] },
    { title: "Item 2", subtitle: "...", imageUrl: "...", actions: [...] }
  ]
}}

// Choice (Quick Replies)
{ type: "choice", payload: {
  text: "Select an option:",
  choices: [
    { title: "Option 1", value: "opt1" },
    { title: "Option 2", value: "opt2" }
  ]
}}

// Dropdown
{ type: "dropdown", payload: {
  text: "Select country:",
  options: [
    { label: "United States", value: "us" },
    { label: "Canada", value: "ca" }
  ]
}}
```

**GitHub：**https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/messages.md**

---

## Zai - LLM实用工具

**何时使用Zai而不是execute()：**
- **使用`zai`**进行特定的、结构化的AI操作（提取数据、分类、标记）。
- **使用`execute()`**进行自主的多轮对话。

**Zai适用于：**
- 从用户消息中提取结构化数据（`zai.extract`）。
- 对内容进行分类/标记（`zai.check`、`zai.label`）。
- 概括长内容（`zai.summarize`）。
- 根据文档回答问题（`zai.answer`）。
- 智能地排序/过滤/分组数据（`zai.sort`、`zai.filter`、`zai.group`）。

**Zai操作针对速度和成本进行了优化**——它们使用`agent.config.ts`中配置的`zai`模型（通常是更快/更经济的模型）。

**文档：**https://www.botpress.com/docs/adk/zai/overview**
**GitHub：**https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/zai-complete-guide.md**

---

## 集成（Integrations）

**何时添加集成：**
- 当您需要连接到外部服务（如Slack、Linear、GitHub等）时。
- 当您需要从渠道（如Webchat、WhatsApp、Discord）接收消息时。
- 当您需要使用预构建的动作调用外部API时。
- 当您需要对外部系统中的事件作出反应时。

**集成工作流程：**
1. **搜索** - 使用`adk search <名称>`查找集成。
2. **添加** - 使用`adk add <名称>@<版本>`进行安装。
3. **配置** - 在http://localhost:3001的UI中设置凭据。
4. **使用** - 通过`actions.<integration>.<action>()`调用动作。

**使集成动作对AI可用：**
```typescript
// Convert any integration action to an AI-callable tool
tools: [actions.slack.sendMessage.asTool()]
```

**CLI命令：**
```bash
adk search slack           # Find integrations
adk add slack@latest       # Add to project
adk add slack --alias my-slack  # Add with custom alias
adk info slack --events    # See available events
adk list                   # List installed integrations
adk upgrade slack          # Update to latest
adk remove slack           # Remove integration
```

**使用集成动作：**
```typescript
import { actions } from "@botpress/runtime";

// Slack
await actions.slack.sendMessage({ channel: "#general", text: "Hello!" });
await actions.slack.addReaction({ channel: "C123", timestamp: "123", name: "thumbsup" });

// Linear
await actions.linear.issueCreate({ teamId: "123", title: "Bug report", description: "Details" });
const { items } = await actions.linear.issueList({
  first: 10,
  filter: { state: { name: { eq: "In Progress" } } }
});

// GitHub
await actions.github.createIssue({ owner: "org", repo: "repo", title: "Issue" });

// Browser (web scraping)
const results = await actions.browser.webSearch({ query: "Botpress docs", maxResults: 5 });

// Make integration actions available to AI as tools
await execute({ tools: [actions.slack.sendMessage.asTool()] });
```

**文档：**https://www.botpress.com/docs/adk/managing-integrations**
**GitHub：**https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/integration-actions.md**

## 状态管理

**理解状态层次结构 - 选择正确的级别：**

| 状态级别 | 范围 | 用途 |
|-------------|-------|---------|
| `bot.state` | 全局，所有用户 | 特性标志、计数器、维护模式 |
| `user.state` | 每个用户，他们的所有对话 | 用户偏好设置、个人资料、等级 |
| `conversation.state` | 每个对话 | 上下文、消息计数、活动工作流 |
| `workflow.state` | 每个工作流实例 | 进度跟踪、中间结果 |

**状态会自动持久化**——只需修改它，它就会保存。

**从机器人的任何地方访问和修改状态：**

**状态类型：**
- **Bot State**：全局的，所有用户共享。
- **User State**：每个用户的，跨所有对话持久。
- **Conversation State**：每个对话的，对话之间独立。
- **Workflow State**：每个工作流实例的，跨步骤持久。

**标签（Tags）与状态（State）：**
- 使用**Tags**进行分类、简单字符串、过滤/查询。
- 使用**State**处理复杂对象、数组、嵌套数据。

**GitHub：**https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/tags.md**

## 上下文API

**在任何处理程序中访问运行时服务：**

```typescript
import { context } from "@botpress/runtime";

// Always available
const client = context.get("client");           // Botpress API client
const citations = context.get("citations");     // Citation manager
const cognitive = context.get("cognitive");     // LLM client
const logger = context.get("logger");           // Structured logger
const botId = context.get("botId");            // Current bot ID
const configuration = context.get("configuration");  // Bot config

// Conditionally available (use { optional: true })
const user = context.get("user", { optional: true });
const conversation = context.get("conversation", { optional: true });
const message = context.get("message", { optional: true });
const workflow = context.get("workflow", { optional: true });
const chat = context.get("chat", { optional: true });  // Conversation transcript

if (user) {
  console.log(`User: ${user.id}`);
}
```

**GitHub：**https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/context-api.md**

## CLI快速参考

```bash
# Project Lifecycle
adk init <name>              # Create new project
adk login                    # Authenticate with Botpress
adk dev                      # Start dev server (hot reload)
adk dev --port 3000          # Custom port
adk chat                     # Test in CLI
adk build                    # Build for production
adk deploy                   # Deploy to Botpress Cloud
adk deploy --env production  # Deploy to specific environment

# Integration Management
adk add <integration>        # Add integration
adk add slack@2.5.5          # Add specific version
adk add slack --alias my-slack  # Add with alias
adk remove <integration>     # Remove integration
adk search <query>           # Search integrations
adk list                     # List installed integrations
adk list --available         # List all available
adk info <name>              # Integration details
adk info <name> --events     # Show available events
adk upgrade <name>           # Update integration
adk upgrade                  # Interactive upgrade all

# Knowledge & Assets
adk kb sync --dev            # Sync knowledge bases
adk kb sync --prod --force   # Force re-sync production
adk assets sync              # Sync static files

# Advanced
adk run <script.ts>          # Run TypeScript script
adk mcp                      # Start MCP server
adk link --workspace ws_123 --bot bot_456  # Link to existing bot

# Utilities
adk self-upgrade             # Update CLI
adk telemetry --disable      # Disable telemetry
adk --help                   # Full CLI help
adk <command> --help         # Help for specific command
```

**文档：**https://www.botpress.com/docs/adk/cli-reference**
**GitHub：**https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/cli.md**

## 使用`execute()`进行自主执行

`execute()`函数是ADK AI能力的核心。它能够：
- 从自然语言中理解用户意图。
- 决定调用哪些工具以及何时调用。
- 在知识库中搜索相关信息。
- 生成基于上下文的响应。
- 循环调用多个工具直到任务完成。

**何时使用execute()：**
- 在对话处理程序中生成AI响应。
- 在工作流中需要AI决策时。
- 在任何需要自主、多步骤AI行为的地方。

**配置的关键参数：**
- `instructions`：告诉AI它的身份和行为方式。
- `tools`：赋予AI功能（搜索、创建、更新等）。
- `knowledge`：为AI提供上下文。
- `exits`：定义特定结果的结构化输出模式。

`execute()`函数实现了AI的自主行为：

```typescript
import { Autonomous, z } from "@botpress/runtime";

// Define custom tool
const searchTool = new Autonomous.Tool({
  name: "search",
  description: "Search documentation",
  input: z.object({ query: z.string() }),
  output: z.string(),
  handler: async ({ query }) => {
    // Search implementation
    return "results...";
  }
});

// Define exit (structured response)
const AnswerExit = new Autonomous.Exit({
  name: "Answer",
  description: "Provide final answer to the user",
  schema: z.object({
    answer: z.string(),
    confidence: z.number(),
    sources: z.array(z.string())
  })
});

// Execute AI with tools, knowledge, and exits
const result = await execute({
  instructions: "Help the user with their request. Be helpful and concise.",

  // Add tools
  tools: [
    searchTool,
    actions.linear.issueCreate.asTool()
  ],

  // Add knowledge bases
  knowledge: [DocsKnowledgeBase, FAQKnowledgeBase],

  // Define exits for structured outputs
  exits: [AnswerExit],

  // Model configuration
  model: "openai:gpt-4o",
  temperature: 0.7,
  iterations: 10,  // Max tool call iterations

  // Hooks for monitoring
  hooks: {
    onBeforeTool: async ({ tool, input }) => {
      console.log(`Calling ${tool.name}`, input);
      return { input: { ...input, enhanced: true } };  // Modify input
    },
    onAfterTool: async ({ tool, output }) => {
      console.log(`Result:`, output);
    }
  }
});

// Handle structured exit
if (result.is(AnswerExit)) {
  console.log(result.output.answer);
  console.log(result.output.sources);
}
```

## 故障排除**

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| “在动作中无法解构属性” | 在处理程序参数中直接解构输入 | 使用`async handler({ input, client })`，然后在内部使用`const { field } = input` |
| 创建表格失败 | 表格名称或`id`定义无效 | 删除`id`列，确保名称以“Table”结尾 |
| 未找到集成动作 | 集成未安装或配置不正确 | 运行`adk list`，使用`adk add`添加，并在http://localhost:3001的UI中配置 |
| 知识库未更新 | 知识库未同步 | 运行`adk kb sync --dev`或`adk kb sync --force` |
- 工作流无法恢复 | 步骤名称动态 | 使用稳定、唯一的步骤名称（避免使用`step(\`item-${i}\`) |
- 类型过时 | 生成的类型过时 | 运行`adk dev`或`adk build`重新生成 |
- 无法从工作流向用户发送消息 | 缺少conversationId | 在启动工作流时传递`conversationId`，使用`client.createMessage()` |
- “user未定义” | 在对话之外访问对话上下文 | 使用`context.get("user", { optional: true })` |
- 状态更改未持久化 | 创建新对象而不是修改 | 直接修改状态：`state.user.name = "Alice"` |
- 工具未被AI使用 | 描述不够清晰 | 改进工具描述，为输入添加详细的`.describe()` |

**更多帮助：**运行`adk --help`或查看：**
- **文档：**https://www.botpress.com/docs/adk/
- **GitHub：**https://github.com/botpress/skills/tree/master/skills/adk/references`

## 常见模式与最佳实践**

### 1. 始终为工作流传递conversationId**

```typescript
// In conversation - starting a workflow that needs to message back
await MyWorkflow.start({
  conversationId: conversation.id,  // Always include this!
  data: "..."
});

// In workflow - messaging back to user
await client.createMessage({
  conversationId: input.conversationId,
  type: "text",
  payload: { text: "Processing complete!" }
});
```

### 2. 使用环境变量存储秘密信息**

```typescript
// In .env (never commit!)
API_KEY=sk-...
SLACK_TOKEN=xoxb-...

// In code
config: { apiKey: process.env.API_KEY }
```

### 3. 在工作流中保持步骤名称稳定**

```typescript
// GOOD - Single step for batch
await step("process-all-items", async () => {
  for (const item of items) {
    await processItem(item);
  }
});

// BAD - Dynamic names break resume
for (let i = 0; i < items.length; i++) {
  await step(`process-${i}`, async () => { ... });  // Don't do this!
}
```

### 4. 在动作/工具中处理错误**

```typescript
export default new Action({
  handler: async ({ input }) => {
    try {
      // Action logic
      return { success: true };
    } catch (error) {
      console.error("Action failed:", error);
      throw new Error(`Failed to process: ${error.message}`);
    }
  }
});
```

### 5. 对于工具的边缘情况使用ThinkSignal**

```typescript
handler: async ({ query }) => {
  const results = await search(query);

  if (!results.length) {
    throw new Autonomous.ThinkSignal(
      "No results",
      "No results found. Ask the user to try different search terms."
    );
  }

  return results;
}
```

### 6. 多渠道处理**

```typescript
export default new Conversation({
  channels: ["slack.channel", "webchat.channel"],
  handler: async ({ conversation }) => {
    const channel = conversation.channel;

    if (channel === "slack.channel") {
      // Slack-specific handling (threading, mentions, etc.)
    } else if (channel === "webchat.channel") {
      // Webchat-specific handling
    }
  }
});
```

## 完整参考文档

### 官方Botpress ADK文档
**基础URL：**https://www.botpress.com/docs/adk/

| 主题 | URL |
|-------|-----|
| 介绍 | https://www.botpress.com/docs/adk/introduction |
| 快速入门 | https://www.botpress.com/docs/adk/quickstart |
| 项目结构 | https://www.botpress.com/docs/adk/project-structure |
| 动作 | https://www.botpress.com/docs/adk/concepts/actions |
| 工具 | https://www.botpress.com/docs/adk/concepts/tools |
| 对话 | https://www.botpress.com/docs/adk/concepts/conversations |
| 工作流概述 | https://www.botpress.com/docs/adk/concepts/workflows/overview |
| 工作流步骤 | https://www.botpress.com/docs/adk/concepts/workflows/steps |
| 表格 | https://www.botpress.com/docs/adk/concepts/tables |
| 触发器 | https://www.botpress.com/docs/adk/concepts/triggers |
| 知识库 | https://www.botpress.com/docs/adk/concepts/knowledge |
| 管理集成 | https://www.botpress.com/docs/adk/managing-integrations |
| Zai概述 | https://www.botpress.com/docs/adk/zai/overview |
| Zai参考 | https://www.botpress.com/docs/adk/zai/reference |
| CLI参考 | https://www.botpress.com/docs/adk/cli-reference |

### GitHub仓库参考（AI优化）

**基础URL：**https://github.com/botpress/skills/tree/master/skills/adk/references**

有关本指南之外的详细规范，请查阅相应的参考文件：

| 主题 | 参考文件 |
|-------|----------------|
| 动作 | https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/actions.md |
| 工具 | https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/tools.md |
| 工作流 | https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/workflows.md |
| 对话 | https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/conversations.md |
| 表格 | https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/tables.md |
| 触发器 | https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/triggers.md |
| 知识库 | https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/knowledge-bases.md |
| 消息 | https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/messages.md |
| 代理配置 | https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/agent-config.md |
| CLI | https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/cli.md |
| 集成动作 | https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/integration-actions.md |
| 模型配置 | https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/model-configuration.md |
| 上下文API | https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/context-api.md |
| 标签 | https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references-tags.md |
| 文件 | https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/files.md |
| Zai完整指南 | https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/zai-complete-guide |
| Zai代理参考 | https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/zai-agent-reference |
| MCP服务器 | https://raw.githubusercontent.com/botpress/skills/master/skills/adk/references/mcp-server.md |

## 常见场景 - 应该构建什么

**“我想构建一个根据文档回答问题的支持机器人”**
1. 创建一个以文档为来源的知识库。
2. 创建一个使用该知识的对话处理程序，并调用`execute()`。
3. 添加`chat`集成进行测试。

**“我希望机器人在用户报告问题时创建工单”**
1. 添加Linear集成：`adk add linear`。
2. 创建一个调用`actions.linear.issueCreate()`的工具。
3. 将该工具传递给`execute()`。

**“我需要运行每日同步任务”**
1. 创建一个工作流，设置`schedule: "0 9 * * *"`（cron语法）。
2. 在步骤中实现同步逻辑。
3. 工作流将在预定时间自动运行。

**“我需要存储用户偏好设置”**
1. 在`agent.config.ts`中定义模式。
2. 通过`user.state.preferenceField = value`进行访问/修改。
3. 状态会自动持久化。

**“我需要在新用户注册时作出反应”**
1. 创建一个监听`user.created`事件的触发器。
2. 在处理程序中启动注册工作流或发送欢迎消息。

**“我需要存储订单数据并对其进行搜索”**
1. 创建一个表格，并设置相应的模式（记住：不要使用`id`字段，名称以“Table”结尾）。
2. 在需要搜索的文本列上设置`searchable: true`。
3. 使用CRUD方法：`createRows`、`findRows`、`updateRows`、`deleteRows`。

## 总结

本指南提供了使用ADK构建Botpress机器人的全面指导：

- **设置与初始化**：ADK的安装和项目创建。
- **项目结构**：约定、文件和组织结构。
- **核心概念**：动作、工具、工作流、对话、表格、知识库、触发器。
- **状态管理**：机器人、用户、对话和工作流的状态。
- **集成管理**：添加和配置集成。
- **Zai（AI操作）**：提取、分类、标记、总结、回答、排序、分组、重写、过滤。
- **CLI参考**：完整的命令指南。
- **测试与部署**：本地测试和云部署。
- **常见模式**：最佳实践和故障排除。

**核心原则：**ADK是一个基于约定的框架，文件的位置决定了其行为。将组件放置在正确的`src/`子目录中，它们将自动成为机器人的功能。

**何时使用本指南：**
- 用户希望创建新的Botpress机器人。
- 用户询问如何添加动作、工具、工作流、对话、表格、知识库或触发器。
- 用户需要关于集成的帮助（如Slack、Linear、GitHub等）。
- 用户需要了解ADK的模式和最佳实践。
- 用户遇到问题或需要故障排除。
- 用户询问关于CLI命令、配置或部署的问题。

**官方文档：**https://www.botpress.com/docs/adk/
**GitHub仓库：**https://github.com/botpress/adk
**技能仓库：**https://github.com/botpress/skills