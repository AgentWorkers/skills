---
name: durable-agents
description: 使用 Mastra（仅用于管理代理）和 Trigger.dev（用于管理所有工作流程和任务）来构建自主的多代理管道系统。该系统适用于以下场景：创建 AI 代理、设计多阶段处理流程、定义代理的权限设置、管理代理之间的任务交接、将代理的输出数据存储到数据库中，以及构建具有重试机制和分布式执行能力的任务链。
---
---

# 首次安装：在使用此技能之前，请阅读并遵循 `setupSKILL.md` 文件的说明。
**安装完成后并经过验证（健康检查通过、示例流程正常运行、烟雾测试通过）后，请删除此部分。**

---

# **持久化代理——多代理流程开发指南**

Mastra（AI代理框架）+ Trigger.dev（支持重试、超时和分布式处理的持久化任务执行工具）。通过构建自主的多代理流程，每个代理负责一个处理阶段，并通过 Trigger.dev 将结构化输出传递给下一个阶段；代理不会持有其不负责的整个流程的上下文。

---

## 核心原则

1. **所有智能逻辑都存储在 `AGENT.md` 文件中，而非代码中。`.ts` 文件仅用于编写通用连接逻辑。在代理的 TypeScript 文件中编写逻辑是错误的。**
2. **一个代理负责一个任务。**每个代理都有明确的职责。如果一个代理需要处理两个不相关的任务，应将其拆分为两个代理。
3. **任务负责处理数据的持久化，代理负责逻辑处理。**Trigger.dev 任务会为代理调用添加重试和超时机制。代理接收输入并生成输出。
4. **工具应返回错误信息，而不是直接抛出异常。**所有工具在失败时都会返回 `{ success, errorMessage? }`。如果在工具内部抛出异常，会导致任务失败。返回错误信息可以让代理自行处理问题。
5. **所有数据都需要进行类型定义。**输入结构、输出结构以及工具的数据结构都必须使用 Zod 进行类型定义。当数据跨越不同组件（如工具输入、任务负载或流程阶段）时，都必须有相应的结构定义。
6. **代理是自主运行的，而不是被硬编码控制的。**为代理指定结果和质量标准，但不要在代码中直接指定其执行步骤。
7. **流程应打破数据上下文的限制，而不是逻辑的限制。**在需要不同功能的环节进行流程拆分——而不是人为地分割代理的工作。
8. **所有代理的输入/输出操作都会被记录到数据库中。**代理的输入、输出和中间结果都会作为记录保存在数据库中。数据库是数据的真实来源，而不是内存中的临时状态。
9. **任何能够访问外部系统的工具都必须经过权限验证。**如果工具具有发布、删除、收费或触发外部操作的功能，必须在执行前确认用户的意图。

---

## 如何创建代理

### 1. 创建目录

```
src/agents/{name}/
  AGENT.md
  {name}.ts
```

### 2. 编写 `AGENT.md` 文件

```markdown
# AGENT: {Name}

## Role
Who this agent is. One sentence.

## Tools
What tools it has and when to use each one. Be explicit — "Use `sqlQuery` to
check if a table exists before referencing it" not just "Has sqlQuery tool."

## Inputs
What payload it receives. Describe the shape and what each field means.

## Goal
What it must achieve. Describe the outcome, not the steps. The agent decides
how to get there. "Produce a deployment plan for the given architecture" not
"First read the architecture, then list the services, then..."

## Output Contract
Exact shape it must return. If structured output is needed, specify the JSON
schema here. Example:
  { "plan": string, "steps": string[], "risks": string[] }

## Quality Standards
What makes output good vs bad. Be specific. "Each step must be independently
executable" not "Steps should be good."

## Guardrails
What it must NOT do. "Never modify database schema directly." "Never assume
the API is authenticated unless payload says so."

## Self-Validation
Checklist the agent must verify before returning:
- Does output match the Output Contract?
- Are all required fields present?
- Does it satisfy the Quality Standards?
```

### 3. 创建代理的 `.ts` 文件

此文件仅包含通用模板代码，不包含任何逻辑。

```ts
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { Agent } from "@mastra/core/agent";
import { model } from "../../config/model.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const instructions = fs.readFileSync(path.join(__dirname, "AGENT.md"), "utf8");

export const myAgent = new Agent({
    id: "my-agent",
    name: "My Agent",
    instructions,
    model,
});
```

### 4. 注册代理

在 `src/mastra/index.ts` 中进行代理的注册：

```ts
import { myAgent } from "../agents/my-agent/my-agent.js";

export const mastra = new Mastra({
    agents: { plannerAgent, reviewerAgent, myAgent },
});
```

---

## 如何创建工具

### 工具结构

```ts
import { createTool } from "@mastra/core/tools";
import { z } from "zod";

export const myTool = createTool({
    id: "my-tool",
    description: "What it does and WHEN to use it",
    inputSchema: z.object({
        query: z.string().describe("The search query"),
    }),
    outputSchema: z.object({
        success: z.boolean(),
        data: z.any().optional(),
        errorMessage: z.string().optional(),
    }),
    execute: async ({ query }) => {
        try {
            const result = await doSomething(query);
            return { success: true, data: result };
        } catch (error: any) {
            return { success: false, errorMessage: error.message };
        }
    },
});
```

### 工具规则

- **必须定义 `outputSchema`。**代理使用该结构来理解工具返回的数据。
- **`execute` 方法中不得抛出异常。**应返回 `{ success: false, errorMessage }`。直接抛出异常会导致 Trigger.dev 任务失败。
- **工具的描述用于指导代理如何使用。**例如：“用于检查数据库表是否存在。传入表名，返回 true/false。”
- **每个工具只负责一个功能。**例如：“查询数据库”，而不是“查询数据库、格式化结果并发送邮件”。
- **使用 `.describe()` 方法为 Zod 字段添加说明，以便代理知道如何传递参数。**
- **除非必要，否则不要产生副作用。**如果工具需要写入数据，必须在描述和代理的 `AGENT.md` 中明确说明。

### 工具的存放位置

- 公共工具：`src/tools/{name}.ts`
- 代理专用工具：`src/agents/{agentName}/tools/{name}.ts`

在 `src/mastra/index.ts` 中注册公共工具；代理专用工具可以直接在代理文件中导入。

---

## 对于具有破坏性或外部操作的工具，必须实施权限控制

任何能够访问外部系统的工具（如发送 API 请求、发布内容、发送消息、扣除费用或触发 Webhook）都必须经过权限验证。代理在没有明确用户授权的情况下不得执行这些操作。

**在开发具有实际影响的工具之前，请询问用户：**
- 该工具具体执行什么操作？
- 代理是否可以自动执行该操作，还是需要人工审批？
- 如果操作失败会有什么后果？
- 是否需要对操作进行速率限制或仅针对特定记录执行？

将这些规则融入工具的权限控制机制中，而不仅仅是代理的 `AGENT.md` 中的防护措施。防护措施只是指导原则；权限控制才是实际执行机制。

### 模式：执行前必须获得确认

对于任何无法撤销或会产生成本/可见性影响的操作，工具在执行前必须接收到明确的 `confirmed: true` 信号。代理必须先调用预览工具，只有在确认结果并收到确认信号后才能执行实际操作。

```ts
export const publishPostTool = createTool({
    id: "publish-post",
    description: "Publishes a post to the platform. Only call this after previewing with `previewPostTool` and receiving confirmed: true from the task payload.",
    inputSchema: z.object({
        postId: z.string().describe("ID of the post record to publish"),
        confirmed: z.boolean().describe("Must be true. Do not set this yourself — it must come from the task payload."),
    }),
    outputSchema: z.object({
        success: z.boolean(),
        publishedUrl: z.string().optional(),
        errorMessage: z.string().optional(),
    }),
    execute: async ({ postId, confirmed }) => {
        if (!confirmed) {
            return { success: false, errorMessage: "Publish requires confirmed: true in payload." };
        }
        try {
            const url = await publishPost(postId);
            return { success: true, publishedUrl: url };
        } catch (error: any) {
            return { success: false, errorMessage: error.message };
        }
    },
});
```

### 模式：操作必须针对特定记录

具有破坏性或写入数据的工具必须针对具体的记录 ID 进行操作——不能基于查询结果或隐式的“当前记录”进行操作。代理必须始终传递它所操作的记录的 ID，以防止错误操作。

```ts
inputSchema: z.object({
    recordId: z.string().describe("Exact DB ID of the record to act on. Do not pass a search query."),
})
```

### `AGENT.md` 和工具中的内容划分

| 内容 | 存放位置 |
|---|---|
| “除非质量得分大于 0.8，否则不要发布” | `AGENT.md` 中的防护措施 |
| “未经确认（confirmed: true）不得执行此操作” | 工具的输入结构中的限制条件 |
| “仅对状态为 `draft` 的记录进行操作” | 工具执行前的检查条件 |
| “每次运行不得删除多于一条记录” | 工具执行前的限制条件 |

---

## 如何创建流程

流程由 Trigger.dev 任务组成。每个任务会调用一个代理，并将其输出传递给下一个任务。没有任何一个代理会持有整个流程的完整上下文——每个阶段只接收它所需的信息。

### 1. 在 `src/pipelines/tasks/` 目录下创建任务文件

```ts
import { task, logger } from "@trigger.dev/sdk/v3";
import { mastra } from "../../mastra/index.js";

export const planTask = task({
    id: "plan-task",
    retry: { maxAttempts: 3, minTimeoutInMs: 1000, factor: 2 },
    run: async (payload: { prompt: string }) => {
        logger.info("Running planner", { promptLength: payload.prompt.length });
        const agent = mastra.getAgent("plannerAgent");
        const response = await agent.generate(JSON.stringify(payload));
        return response.text;
    },
});
```

### 2. 创建流程编排器

在 `src/pipelines/{name}.ts` 中使用 `triggerAndWait` 方法连接各个任务：

```ts
import { planTask } from "./tasks/plan-task.js";
import { reviewTask } from "./tasks/review-task.js";

export async function runMyPipeline(input: string) {
    const planResult = await planTask.triggerAndWait({ prompt: input });
    if (!planResult.ok) throw new Error("Plan task failed");

    const reviewResult = await reviewTask.triggerAndWait({ plan: planResult.output });
    if (!reviewResult.ok) throw new Error("Review task failed");

    return { plan: planResult.output, review: reviewResult.output };
}
```

### 3. 将任务导出供工作者执行

在 `src/trigger/index.ts` 中完成任务的导出：

```ts
export * from "../pipelines/tasks/plan-task.js";
export * from "../pipelines/tasks/review-task.js";
```

所有任务都必须在这里被导出，否则 Trigger.dev 工作者将无法找到它们。

### 4. 添加 API 端点

在 `src/app/index.ts` 中配置 API 端点：

```ts
app.post("/my-pipeline", async (req, res) => {
    const { input } = req.body;
    const result = await runMyPipeline(input);
    res.json({ success: true, ...result });
});
```

---

## 流程设计：代理与脚本的使用

并非每个流程阶段都需要代理。在需要判断或决策的环节使用代理；对于操作结果确定的环节，可以使用脚本（普通的 TypeScript 函数或不依赖代理的 Trigger.dev 任务）。

### 示例：内容生成流程

```
[Director Agent]         — generates ideas, writes scripts, validates against criteria
        ↓
[Media Selector Agent]   — selects or processes media assets based on the script
        ↓
[Overlay Task]           — no agent; deterministic script that composites text onto video and stores result
```

覆盖阶段不需要进行任何逻辑处理。它接收输入、执行固定操作并存储结果。在此阶段添加代理会增加延迟和成本，但并无实际意义。

### 何时在流程阶段使用代理

在以下情况下使用代理：
- 需要判断或评估结果是否符合质量标准；
- 需要从多个选项中选择最合适的方案；
- 需要根据目标生成内容；
- 需要根据反馈进行迭代优化。

在以下情况下使用普通任务（无需代理）：
- 需要执行确定性操作（如调整大小、编码、组合数据）；
- 需要将结果保存到数据库或文件系统；
- 需要发送通知或触发 Webhook；
- 需要执行无需解释的数据查询。

### 流程阶段的拆分

在需要不同功能的环节进行流程拆分——而不是人为地分割代理的工作。例如，一个代理可能负责生成想法、编写脚本并根据标准进行验证；媒体选择属于不同的功能，因此需要单独处理。

---

## 流程模式

### 分布式执行（并行子任务）

```ts
import { tasks } from "@trigger.dev/sdk/v3";

const handles = await tasks.batchTrigger("process-item",
    items.map(item => ({ payload: { item } }))
);
```

每个子任务独立运行，并具有自己的重试机制。

### 审查检查点

在流程步骤之间添加审查环节。有三种模式：
- **“none”**：自动批准，立即进入下一个阶段。
- **“agent”**：调用审核代理。如果审核通过，则继续执行；如果被拒绝，则将反馈返回给上一个阶段进行修改。
- **“human”**：在数据库中设置状态为 `pending`，然后返回。由人工进行外部审核。之后通过 API 回调继续执行流程。

### 重试配置

每个任务都必须有明确的重试配置。大语言模型（LLM）的调用结果可能不稳定——默认设置（不重试）意味着一次 API 错误就会导致整个流程失败。

```ts
retry: {
    maxAttempts: 3,
    minTimeoutInMs: 1000,
    factor: 2,
}
```

---

## 数据库作为代理的数据存储层

所有代理的输入、输出和中间结果在进入下一个阶段之前都必须被保存到数据库中。这是强制性的要求。代理操作的是数据库中的记录，而不是通过内存中的临时数据。

### 原因：
- **去重**：在触发新任务之前，检查是否有相同的任务已经执行过。可以通过内容哈希、来源 ID 或其他唯一键进行判断。
- **验证**：下一个阶段从数据库中读取数据，而不是从前一个任务的返回值中获取。如果数据库中不存在该记录，则流程不会继续执行。
- **记录保存**：每个生成的资产、决策和状态变化都会被记录在数据库中。这样可以进行审计、回放和故障排查。
- **失败后恢复**：如果任务需要重试，它会先检查数据库。如果输出已经存在，则直接跳过重试步骤，继续执行。

### 模式：先写入数据库再传递结果

每个任务都会将输出写入数据库，并返回记录 ID。下一个任务接收 ID 后，从数据库中读取数据并继续处理。

```ts
// Stage 1: director agent writes its output
export const scriptTask = task({
    id: "script-task",
    retry: { maxAttempts: 3, minTimeoutInMs: 1000, factor: 2 },
    run: async (payload: { projectId: string }) => {
        const existing = await db.script.findFirst({ where: { projectId: payload.projectId } });
        if (existing) return { scriptId: existing.id }; // already done, skip

        const agent = mastra.getAgent("directorAgent");
        const response = await agent.generate(JSON.stringify(payload));
        const output = ScriptOutputSchema.parse(JSON.parse(response.text));

        const record = await db.script.create({
            data: { projectId: payload.projectId, content: output.script, status: "draft" },
        });
        return { scriptId: record.id };
    },
});

// Stage 2: next agent reads by ID
export const mediaTask = task({
    id: "media-task",
    retry: { maxAttempts: 3, minTimeoutInMs: 1000, factor: 2 },
    run: async (payload: { scriptId: string }) => {
        const script = await db.script.findUniqueOrThrow({ where: { id: payload.scriptId } });
        const agent = mastra.getAgent("mediaSelectorAgent");
        const response = await agent.generate(JSON.stringify({ script: script.content }));
        const output = MediaOutputSchema.parse(JSON.parse(response.text));

        const record = await db.mediaSelection.create({
            data: { scriptId: payload.scriptId, assetIds: output.assetIds, status: "selected" },
        });
        return { mediaSelectionId: record.id };
    },
});
```

### 使用状态字段控制流程

在每个记录中存储 `status` 字段，用于控制流程的流程和触发人工审核。

| 状态 | 含义 |
|---|---|
| `pending` | 创建中，尚未处理 |
| `processing` | 任务正在执行中 |
| `draft` | 代理已生成输出，但尚未审核 |
| `approved` | 审核通过（代理或人工审核） |
| `rejected` | 审核失败，需要修改 |
| `published` | 最终操作已完成 |
| `failed` | 出现无法恢复的错误 |

```ts
await db.script.update({
    where: { id: scriptId },
    data: { status: "processing" },
});
// ... agent call ...
await db.script.update({
    where: { id: scriptId },
    data: { status: "draft", content: output.script },
});
```

## 保持代理的自主性

只需定义目标和质量标准，无需指定具体的实现方式。

**错误做法：**对代理进行微观管理：
```
1. Read the input
2. Extract the requirements
3. For each requirement, write a task
4. Format the tasks as a numbered list
5. Return the list
```

**正确做法：**定义最终结果：
```
## Goal
Produce a technical implementation plan for the given objective.

## Output Contract
{ "tasks": [{ "title": string, "description": string, "dependencies": string[] }] }

## Quality Standards
- Each task must be independently executable by a developer
- Dependencies must reference other tasks by title
- No task should take more than 4 hours of work
```

---

## 类型强制规范

### 任务负载

在调用 `run` 函数时，必须为所有参数指定类型：

```ts
run: async (payload: { prompt: string; maxTokens?: number }) => {
```

### 代理的结构化输出

在 `AGENT.md` 的输出契约部分定义明确的输出结构，并在接收数据时使用 Zod 进行类型验证：

```ts
const OutputSchema = z.object({
    tasks: z.array(z.object({
        title: z.string(),
        description: z.string(),
        dependencies: z.array(z.string()),
    })),
});

const response = await agent.generate(JSON.stringify(payload));
const parsed = OutputSchema.parse(JSON.parse(response.text));
```

如果解析失败，任务会抛出异常，Trigger.dev 会使用相同的输入重新尝试，代理也会再次生成输出。

### 工具的数据结构

所有工具都必须定义 `inputSchema` 和 `outputSchema`。代理根据这些结构来理解需要传递的参数以及接收到的返回数据。

---

## 关键规则

1. 所有智能逻辑都存储在 `AGENT.md` 文件中，而非代码中。
2. 代理的 `.ts` 文件仅用于编写通用连接代码，不包含逻辑。
3. 工具在失败时返回 `{ success, errorMessage }`，不得直接抛出异常。
4. 任务封装层负责处理数据的持久化，代理负责逻辑处理。
5. 对于需要结构化输出的代理，`AGENT.md` 中必须包含自我验证的规则。
6. 每个 Trigger.dev 任务都必须有明确的重试配置。
7. 所有任务都必须从 `src/trigger/index.ts` 中导出。
8. 所有代理使用相同的模型配置文件 `src/config/model.ts`。
9. 流程阶段使用 `triggerAndWait` 进行顺序执行，使用 `batchTrigger` 进行并行执行。
10. 每次调用 `triggerAndWait` 后都必须检查 `result.ok`，不能假设任务一定成功。
11. 所有代理的输出都必须先写入数据库，然后再传递给下一个阶段——切勿在任务之间传递原始数据。
12. 需要重复执行的任务必须先检查数据库，如果数据已经存在则跳过重复操作。
13. 任何需要执行实际操作的工具都必须接收 `confirmed: true` 的确认信号，并在执行前进行验证。
14. 并非所有流程阶段都需要代理——对于确定性操作，可以使用普通任务。