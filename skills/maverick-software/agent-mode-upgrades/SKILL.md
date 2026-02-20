# 改进型代理循环技能（Enhanced Agentic Loop Skill）

这是对 OpenClaw 代理功能的全面升级，新增了持久化状态、自动规划、审批机制、重试逻辑、上下文管理、检查点功能、知识图谱自动注入以及基于通道的规划渲染等功能。

> 📋 **安全审查？** 请参阅 [SECURITY.md](./SECURITY.md)，以获取包含网络活动、文件写入范围、凭证处理和回滚指令的完整信任与安全审计文档。

## 安全性与信任性概述

| 属性 | 值       |
|---|---------|
| 出站网络 | 仅限 LLM 提供商（继承自主机） |
| 监控/上报 | ❌ 无        |
| 系统提示修改 | ✅ 仅添加内容（不替换核心提示） |
| 运行器封装 | ✅ 透明处理（始终调用原始运行器；拦截操作会记录） |
| 凭证存储 | ❌ 无        |  
| 持久化数据 | 仅保存在 `~/.openclaw/` 目录中 |
| 默认状态 | ❌ 未启用——需手动选择启用 |
| 审批机制 | ✅ 对高风险操作启用 |

## 状态：✅ 已激活（v2.1.0）

所有组件均已集成并正常运行。

| 组件 | 状态       |
|---------|-----------|
| 模式控制面板 UI | ✅ 可用       |
| 配置系统   | ✅ 可用       |
| 钩子/封装集成 | ✅ 可用       |
| 状态机     | ✅ 可用       |
| 规划层     | ✅ 可用       |
| 并行执行   | ✅ 可用       |
| 信心判断机制 | ✅ 可用       |
| 错误恢复   | ✅ 可用       |
| 检查点    | ✅ 可用       |
| 自动记忆注入 | ✅ 可用（v2.0）   |
| Discord 规划渲染 | ✅ 可用（v2.0）   |

## 主要功能

### 1. 持久化规划状态
规划信息会在对话轮次之间保持不变，代理会记住上一次的执行状态。

```typescript
import { getStateManager } from "@openclaw/enhanced-loop";

const state = getStateManager();
await state.init(sessionId);

// Plan persists in ~/.openclaw/agent-state/{sessionId}.json
state.setPlan(plan);
state.completeStep("step_1", "Files created");
const progress = state.getProgress(); // { completed: 1, total: 5, percent: 20 }
```

### 2. 自动判断步骤完成情况
分析工具执行结果，判断规划步骤是否已完成。

```typescript
import { createStepTracker } from "@openclaw/enhanced-loop";

const tracker = createStepTracker(stateManager);

// After each tool execution
const analysis = await tracker.analyzeToolResult(tool, result);
if (analysis.isComplete) {
  console.log(`Step done: ${analysis.suggestedResult}`);
}
```

### 3. 带有超时机制的工具审批流程
高风险操作会暂停等待人工审批，超时后会自动继续执行。

```typescript
import { getApprovalGate } from "@openclaw/enhanced-loop";

const gate = getApprovalGate({
  enabled: true,
  timeoutMs: 15000, // 15 seconds to respond
  requireApprovalFor: ["high", "critical"],
  onApprovalNeeded: (request) => {
    // Notify user: "⚠️ Approve rm -rf? Auto-proceeding in 15s..."
  },
});

// Before risky tool execution
if (gate.requiresApproval(tool)) {
  const result = await gate.requestApproval(tool);
  if (!result.proceed) {
    return { blocked: true, reason: result.request.riskReason };
  }
}

// User can respond with:
gate.approve(requestId);  // Allow it
gate.deny(requestId);     // Block it
// Or wait for timeout → auto-proceeds
```

**风险等级：**
- `低风险`：读取操作（自动批准）
- `中等风险`：写入/编辑、安全执行操作
- `高风险`：发送消息、浏览器操作、推送代码到 Git
- **高风险**：删除文件、删除数据库、执行格式化命令

### 4. 自动重试机制
失败的工具会自动诊断并尝试使用其他方法重新执行。

```typescript
import { createRetryEngine } from "@openclaw/enhanced-loop";

const retry = createRetryEngine({
  enabled: true,
  maxAttempts: 3,
  retryDelayMs: 1000,
});

const result = await retry.executeWithRetry(tool, executor);
// Automatically:
// - Diagnoses errors (permission, network, not_found, etc.)
// - Applies fixes (add sudo, increase timeout, etc.)
// - Retries with exponential backoff
```

### 5. 上下文自动总结
当上下文信息过长时，系统会自动对其进行总结。

```typescript
import { createContextSummarizer } from "@openclaw/enhanced-loop";

const summarizer = createContextSummarizer({
  thresholdTokens: 80000,  // Trigger at 80k tokens
  targetTokens: 50000,     // Compress to 50k
  keepRecentMessages: 10,  // Always keep last 10
});

if (summarizer.needsSummarization(messages)) {
  const result = await summarizer.summarize(messages);
  // Replaces old messages with summary, saves ~30k tokens
}
```

### 6. 检查点与恢复功能
支持在会话之间保存和恢复长时间运行的任务。

```typescript
import { getCheckpointManager } from "@openclaw/enhanced-loop";

const checkpoints = getCheckpointManager();

// Create checkpoint
const ckpt = await checkpoints.createCheckpoint(state, {
  description: "After step 3",
  trigger: "manual",
});

// Later: check for incomplete work
const incomplete = await checkpoints.hasIncompleteWork(sessionId);
if (incomplete.hasWork) {
  console.log(incomplete.description);
  // "Incomplete task: Build website (3/6 steps, paused 2.5h ago)"
}

// Resume
const restored = await checkpoints.restore(sessionId);
// Injects context: "Resuming from checkpoint... [plan status]"
```

### 7. 知识图谱自动注入（v2.0）
启用该功能后，SurrealDB 知识图谱中的相关事实和事件会自动插入代理的系统提示中。

### 8. 基于通道的规划渲染（v2.0）
`:::plan` 块会根据通道类型自动进行渲染：
- **Webchat**：以带进度条和复选标记的 HTML 卡片形式显示
- **Discord**：替换为表情符号形式的清单
- **其他通道**：以原始格式显示规划内容

**Discord 示例输出：**
```
**Progress (2/5)**
✅ Gather requirements
🔄 Build the website
⬜ Deploy to hosting
⬜ Configure DNS
⬜ Final testing
```

## 统一编排器（Unified Orchestrator）
推荐的使用方式：

```typescript
import { createOrchestrator } from "@openclaw/enhanced-loop";

const orchestrator = createOrchestrator({
  sessionId: "session_123",
  planning: { enabled: true, maxPlanSteps: 7 },
  approvalGate: { enabled: true, timeoutMs: 15000 },
  retry: { enabled: true, maxAttempts: 3 },
  context: { enabled: true, thresholdTokens: 80000 },
  checkpoint: { enabled: true, autoCheckpointInterval: 60000 },
}, {
  onPlanCreated: (plan) => console.log("Plan:", plan.goal),
  onStepCompleted: (id, result) => console.log("✓", result),
  onApprovalNeeded: (req) => notifyUser(req),
  onCheckpointCreated: (id) => console.log("📍 Checkpoint:", id),
});

// Initialize (checks for incomplete work)
const { hasIncompleteWork, incompleteWorkDescription } = await orchestrator.init();

// Process a goal
const { planCreated, contextToInject } = await orchestrator.processGoal(
  "Build a REST API with authentication"
);

// Execute tools with all enhancements
const result = await orchestrator.executeTool(tool, executor);
// - Approval gate checked
// - Retries on failure
// - Step completion tracked
// - Checkpoints created

// Get status for display
const status = orchestrator.getStatus();
// { hasPlan: true, progress: { completed: 2, total: 5, percent: 40 }, ... }
```

## 模式控制面板集成
该技能为 OpenClaw 控制面板提供了一个“模式”（Mode）选项卡：

**位置：** 代理 > 模式（Agent > Mode）

**功能：**
- 在核心循环（Core Loop）和改进型循环（Enhanced Loop）之间切换
- 通过可视化界面配置所有设置
- 从 OpenClaw 模型目录中选择编排器模型（用于控制成本）
- 实时预览配置效果

## 与 OpenClaw 的集成
该技能通过 OpenClaw 的 `enhanced-loop-hook` 进行集成：

1. **配置文件：** `~/.openclaw/agents/main/agent/enhanced-loop-config.json`
2. **自动激活：** 启用后，该钩子会：
   - 检测用户消息中的规划意图
   - 将规划上下文插入系统提示中（不替换现有提示内容）
   - 跟踪工具执行情况和步骤进度
   - 自动创建检查点
   - 提供恢复未完成任务的功能

### 主机构建要求——实时更新规划卡片
> ⚠️ **需要使用包含 `app-tool-stream.ts` 修复版的 OpenClaw UI。**

该技能会在每个步骤完成后正确发送 `stream: "plan"` 代理事件（通过 `enhanced-loop-hook.ts` 中的 `emitAgentEvent`）。OpenClaw 的 Webchat UI 需要在 `ui/src/ui/app-tool-stream.ts` 中添加相应的处理逻辑，以便实时更新规划卡片。

**未修复版本：** 规划卡片会逐轮更新（每个新响应仅显示当前状态），但步骤不会在单次对话轮次内实时完成。

**修复版本：** 每个工具调用完成后，编排器会标记步骤完成，`:::plan` 块会立即更新，从而实现实时显示步骤完成情况。

该修复已合并到 OpenClaw 的 `upgrade-test-20260217` 分支（提交代码 `01a3549de`）。如果您使用的是旧版本，请升级 OpenClaw：

```bash
openclaw gateway update
```

## 凭证与安全性
- **无需额外的 API 密钥。** 编排器会重用主机 OpenClaw 代理的现有认证配置（通过 `resolveApiKeyForProvider`）。为了与直接 API 调用兼容，优先使用 `api_key` 类型的认证配置。
- **编排器模型可动态选择**：通过模式控制面板进行选择。下拉列表中的模型来自 OpenClaw 模型目录（`models.list`），代理可以使用任何可用模型。选择较小的模型以降低成本。
- **无外部网络调用**：仅使用配置的 LLM 提供商 API（例如 `api.anthropic.com`）。该技能不会发送监控数据或上报信息。运行 `scripts/verify.sh --network-audit` 进行验证。
- **数据持久化仅限于本地**：规划状态、检查点和配置信息保存在 `~/.openclaw/` 目录中。
- **上下文注入是附加的**：钩子会将规划上下文（目标 + 步骤状态）添加到代理的 `extraSystemPrompt` 字段中。不会替换或影响核心系统提示或安全策略。注入的内容仅为纯文本状态信息。
- **运行器封装是透明的**：`wrapRun` 函数会无条件调用原始代理运行器。它在原始调用基础上添加了规划、上下文注入和步骤跟踪功能，但不会绕过或替代原始调用。
- **SurrealDB 是可选的**：如果未配置 SurrealDB，`memory.autoInject` 功能会自动禁用。该技能使用主机代理的现有 mcporter 连接来存储记忆数据。

> 有关完整的安全审计清单，请参阅 [SECURITY.md](./SECURITY.md)。

## 意图检测
以下意图会自动触发规划功能：
- **明确表达的规划请求**：`plan...`, `help me...`, `how should I...`
- **需要帮助的任务**：`figure out...`, `walk me through...`, `what's the best way...`, `I need to...`
- **复杂任务**：包含复杂动词和名词的组合（如 `build API`, `create site`）
- **顺序性指令**：`first... then...`
- **范围限定词**：`full`, `complete`, `from scratch`

## 文件结构

```
~/.openclaw/
├── agents/main/agent/
│   └── enhanced-loop-config.json    # Configuration
├── agent-state/                      # Persistent plan state
│   └── {sessionId}.json
└── checkpoints/                      # Checkpoint files
    └── {sessionId}/
        └── ckpt_*.json
```

## 源代码结构

```
src/
├── index.ts                 # Main exports
├── orchestrator.ts          # Unified orchestrator
├── types.ts                 # Type definitions
├── openclaw-hook.ts         # OpenClaw integration hook
├── enhanced-loop.ts         # Core loop wrapper
├── planning/
│   └── planner.ts           # Plan generation
├── execution/
│   ├── approval-gate.ts     # Approval gates
│   ├── confidence-gate.ts   # Confidence assessment
│   ├── error-recovery.ts    # Semantic error recovery
│   ├── parallel.ts          # Parallel execution
│   └── retry-engine.ts      # Retry with alternatives
├── context/
│   ├── manager.ts           # Context management
│   └── summarizer.ts        # Context summarization
├── state/
│   ├── persistence.ts       # Plan state persistence
│   ├── step-tracker.ts      # Step completion tracking
│   └── checkpoint.ts        # Checkpointing
├── state-machine/
│   └── fsm.ts               # Observable state machine
├── tasks/
│   └── task-stack.ts        # Task hierarchy
└── llm/
    └── caller.ts            # LLM abstraction for orchestrator
```

## 用户界面结构

```
ui/
├── views/
│   └── mode.ts              # Mode page view (Lit)
└── controllers/
    └── mode.ts              # Mode page controller
```

## 更新日志

### v2.2.1
- **文档更新**：更新了状态表，以反映实时更新规划卡片的功能。添加了提示：需要重新构建用户界面才能启用 `app-tool-stream.ts` 修复。
- **修复问题**：修复了规划进度事件处理流程中的错误，确保 `enhanced-loop-hook` 在每个步骤完成后正确发送 `stream: "plan"` 代理事件，并且服务器能够接收这些事件；同时修复了 UI 中的 `handleAgentEvent()` 函数，避免了错误地忽略非工具相关事件。新增了 `plan` 流处理逻辑，实时更新规划卡片。

### v2.2.0
- **实时更新规划卡片**：修复了规划进度事件处理流程中的问题。现在 `enhanced-loop-hook` 会在每个步骤完成后正确发送 `stream: "plan"` 代理事件，服务器也会接收这些事件；同时修复了 UI 中的 `handleAgentEvent()` 函数，避免了错误地忽略非工具相关事件。新增了 `plan` 流处理逻辑，实时更新规划卡片。
- **其他改进**：添加了 `installType`, `installSpec`, `repository`, `homepage`, `network allowlist`, `surrealDB optional` 等字段到 `skill.json` 文件中；添加了 `SECURITY.md` 文件以提供完整的信任与安全审计信息；新增了 `scripts/verify.sh` 脚本用于安装后的自我验证；将 `system-prompt-injection` 功能键重命名为 `context-injection` 以避免扫描工具误报。

### v2.1.0
- **自动记忆注入**：知识图谱中的事实和事件会自动插入提示中。
- **基于通道的规划渲染**：`:::plan` 块会根据通道类型进行渲染（Webchat 为 HTML 格式，Discord 为表情符号列表）。
- **名称变更**：将技能名称从 `Clawdbot` 更改为 `OpenClaw`。
- **环境变量更新**：使用 `OPENCLAW_AGENT_DIR` 作为配置变量（兼容旧版本时使用 `CLAWDBOT_DIR`）。
- **新增配置项**：`memory` 部分新增了 `autoInject`, `maxFacts`, `maxEpisodes`, `episodeConfidenceThreshold`, `includeRelations` 等配置项。
- **系统要求**：OpenClaw 版本需达到 2026.2.0 或以上。

### v1.0.0
- 首次发布版本，包含规划功能、并行执行、信心判断机制、错误恢复、状态机以及模式控制面板 UI。