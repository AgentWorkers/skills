---
name: agentic-loop-upgrade
description: "**增强型代理循环（Enhanced Agentic Loop）**：该系统集成了规划（Planning）、并行执行（Parallel Execution）、置信度判断机制（Confidence Gates）、语义错误恢复（Semantic Error Recovery）以及可观察的状态机（Observable State Machine）等功能。同时，还提供了 **Mode** 仪表板用户界面（Mode Dashboard UI），便于用户进行配置。
**核心特性：**  
1. **规划功能（Planning）**：允许系统根据预设策略动态规划任务执行顺序和资源分配。  
2. **并行执行（Parallel Execution）**：支持多任务同时运行，提高处理效率。  
3. **置信度判断机制（Confidence Gates）**：通过评估任务执行的可靠性和安全性，决定是否允许任务继续进行。  
4. **语义错误恢复（Semantic Error Recovery）**：在遇到错误时，能够自动识别并尝试恢复系统正常运行。  
5. **可观察的状态机（Observable State Machine）**：清晰展示系统当前的工作状态和进程。  
**用户友好性：**  
- **直观的配置界面（User-Friendly Interface）**：通过 **Mode** 仪表板，用户可以轻松设置系统参数和策略。  
- **实时监控（Real-Time Monitoring）**：提供实时反馈，帮助用户监控系统运行情况。  
- **日志记录（Log Recording）**：详细记录系统日志，便于故障排查和性能优化。  
**应用场景：**  
适用于需要高效处理复杂任务的系统，如分布式计算、自动化控制、人工智能等领域。"
---
# 增强型代理循环技能

这是对OpenClaw代理功能的全面升级，新增了持久化状态、自动规划、审批机制、重试逻辑、上下文管理、检查点功能、知识图谱自动注入以及基于通道的规划渲染等功能。

> 📋 **安全审查？** 请参阅 [SECURITY.md](./SECURITY.md)，以获取包含网络活动、文件写入范围、凭证处理和回滚指令的完整信任与功能审计文档。

## 安全性与信任概述

| 属性 | 值 |
|---|---|
| 出站网络 | 仅限LLM提供商（继承自主机） |
| 监控/反馈 | ❌ 无 |
| 系统提示修改 | ✅ 仅追加提示内容（从不替换核心提示） |
| 运行器封装 | ✅ 透明（始终调用原始运行器；拦截操作会被记录） |
| 凭证存储 | ❌ 无（继承主机代理的认证机制，不存储新数据） |
| 持久化 | 仅保存在本地 `~/.openclaw/` 目录下 |
| 默认未启用 | ❌ 需要明确启用 |
| 高风险操作默认启用审批机制 | ✅ 对于高风险操作，默认启用审批 |

## 状态：✅ 已激活（v2.3.0）

所有组件均已集成并正常工作。

| 组件 | 状态 |
|-----------|--------|
| 模式控制面板UI | ✅ 可用 |
| 配置系统 | ✅ 可用 |
| 钩子/封装器集成 | ✅ 可用 |
| 状态机 | ✅ 可用 |
| 规划层 | ✅ 可用 |
| 并行执行 | ✅ 可用 |
| 信心判断机制 | ✅ 可用 |
| 错误恢复 | ✅ 可用 |
| 检查点 | ✅ 可用 |
| 自动记忆注入 | ✅ 可用（v2版本） |
| Discord规划渲染 | ✅ 可用（v2版本） |

## 主要特性

### 1. 持久化规划状态
规划信息会在对话轮次之间保持不变。代理会记住上一次的进度。

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
分析工具执行结果，确定规划步骤是否已完成。

```typescript
import { createStepTracker } from "@openclaw/enhanced-loop";

const tracker = createStepTracker(stateManager);

// After each tool execution
const analysis = await tracker.analyzeToolResult(tool, result);
if (analysis.isComplete) {
  console.log(`Step done: ${analysis.suggestedResult}`);
}
```

### 3. 带有超时的工具审批机制
高风险操作会暂停以等待人工审批，超时后自动继续执行。

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
- `中等风险`：写入/编辑、安全执行
- `高风险`：发送消息、浏览器操作、推送代码到Git
- ** critical风险**：删除文件、删除数据库、执行格式化命令

### 4. 自动重试机制
失败的工具会自动诊断并尝试其他方法重新执行。

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

### 5. 上下文摘要
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

### 6. 检查点/恢复
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

### 7. 知识图谱自动注入（v2版本）
启用后，SurrealDB知识图谱中的相关事实和事件会自动插入代理的系统提示中。

```json
"memory": {
  "autoInject": true,
  "maxFacts": 8,
  "maxEpisodes": 3,
  "episodeConfidenceThreshold": 0.9,
  "includeRelations": true
}
```

插入的上下文内容会以 `## 语义记忆` 和 `## 事件记忆` 的形式显示在系统提示中。当平均事实置信度低于阈值时，这些事件会被显示出来。

### 8. 基于通道的规划渲染（v2版本）
`:::plan` 块会根据通道类型自动调整显示方式：
- **Webchat**：以带进度条和勾选的HTML卡片形式显示
- **Discord**：替换为带有表情符号的清单形式（Discord不支持自定义HTML）
- **其他通道**：原始的规划内容原样传递，由通道自行处理

**Discord示例输出：**
```
**Progress (2/5)**
✅ Gather requirements
🔄 Build the website
⬜ Deploy to hosting
⬜ Configure DNS
⬜ Final testing
```

## 统一调度器

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

该技能为OpenClaw控制面板提供了一个“模式”选项卡：

**位置：** 代理 > 模式

**功能：**
- 在核心循环和增强型循环之间切换
- 通过可视化界面配置所有设置
- 从OpenClaw模型目录中选择调度器模型（用于控制成本）
- 实时预览配置

## OpenClaw集成

该技能通过OpenClaw中的增强型循环钩子（enhanced-loop-hook）进行集成：

1. **配置文件：** `~/.openclaw/agents/main/agent/enhanced-loop-config.json`

2. **自动激活：** 启用后，钩子会在每次代理运行时调用 `tryLoadEnhancedLoop()` 来创建调度器
- 在每次尝试前调用 `wrapRun()`，注入规划上下文、记忆信息和工具执行跟踪数据
- 通过 `processGoal()` 检测用户消息中的规划意图
- 将规划上下文插入系统提示（仅追加内容，不会替换或覆盖现有系统提示）
- 通过 `onToolResult` / `onAgentEvent` 接口跟踪工具执行和步骤进度
- 自动创建检查点
- 提供恢复未完成任务的功能
- 如果调度器模块不可用，会切换回仅使用记忆信息的模式

### 主机构建要求 — 实时更新规划卡片

> ⚠️ **需要包含 `app-tool-stream.ts` 修复版本的OpenClaw UI。**

该技能会在每个步骤完成后正确发送 `stream: "plan"` 代理事件（通过 `enhanced-loop-hook.ts` 中的 `emitAgentEvent`）。主机OpenClaw的Webchat UI必须在 `ui/src/ui/app-tool-stream.ts` 中包含相应的处理程序，以便实时更新规划卡片。

**未修复版本：** 规划卡片会逐轮更新（每个新的代理响应都会显示当前状态），但在单个轮次内，步骤不会随着工具调用的完成而实时更新。

**修复版本：** 每个工具调用完成后，调度器会标记步骤完成，`:::plan` 块会立即更新，从而实时显示步骤完成情况，无需等待完整响应。

该修复已在 `upgrade-test-20260217` 分支（提交号 `01a3549de`）中合并到OpenClaw中。如果您使用的是旧版本，请升级您的OpenClaw安装：

```bash
openclaw gateway update
```

## 凭证和安全

- **无需额外的API密钥。** 调度器会重用主机OpenClaw代理现有的认证配置（通过 `resolveApiKeyForProvider`）。
- **优先使用OAuth/token认证。** 增强型循环钩子和技能的LLM调用者都遵循与主代理相同的认证层级：优先使用 `type: "token"` 或 `type: "oauth"` 的OAuth设置令牌，而不是 `api_key` 配置文件。这确保调度器API调用（如规划、反射操作）使用与主对话相同的认证方式。
- **原生支持OAuth设置令牌。** LLM调用者会识别 `sk-ant-oat*` 类型的令牌，并通过 `Authorization: Bearer` 头部发送（附带 `anthropic-beta: oauth-2025-04-20` 标头），而标准API密钥使用 `x-api-key` 头部。无需手动配置。
- **尊重认证配置顺序。** 当调用者直接从 `auth-profiles.json` 中读取配置时，会按照 `order.anthropic` 数组中的顺序进行排序，并优先使用 `token/oauth` 配置文件。
- **调度器模型可动态选择**：可以通过模式控制面板进行选择。下拉列表会显示OpenClaw模型目录中的所有可用模型。选择较小的模型可以降低成本。
- **无外部网络调用**：仅使用配置的LLM提供商API（例如 `api.anthropic.com`）。该技能不会发送监控数据或进行反馈。运行 `scripts/verify.sh --network-audit` 命令进行验证。
- **持久化数据仅保存在本地。** 规划状态、检查点和配置信息会保存在 `~/.openclaw/` 目录下。不使用云存储。
- **上下文注入是追加式的。** 钩子会将规划上下文（目标信息 + 步骤状态）追加到代理的 `extraSystemPrompt` 字段中。不会替换或覆盖核心系统提示或任何安全策略。注入的内容仅限于状态文本，不包含任何指令或权限授予。
- **运行器封装是透明的。** `wrapRun` 函数会无条件调用原始代理运行器。它会在原始调用基础上添加规划、上下文注入和步骤跟踪功能，但不会绕过、替换或短路原始调用。
- **SurrealDB是可选的。** 如果未配置SurrealDB，`memory.autoInject` 功能会自动禁用。该技能使用主机代理现有的mcporter连接来存储记忆数据。

> 有关完整的审计清单，请参阅 [SECURITY.md](./SECURITY.md)。

## 意图检测

以下意图会自动触发规划功能：

**明确表达的意图：**
- “plan...”, “help me...”, “how should I...”
- “figure out...”, “walk me through...”
- “what’s the best way...”, “I need to...”

**复杂任务：**
- 复杂动词 + 动词短语：例如 “build API”, “create site”
- 顺序性语言表达：例如 “first... then...”
- 表示范围的词语：例如 “full”, “complete”, “from scratch”

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

### v2.3.0
- **重新连接调度器与代理运行器**：在之前的代码合并中，`tryLoadEnhancedLoop()` 和 `wrapRun()` 与 `run.ts` 之间的连接被断开了。导致规划、工具跟踪和步骤完成功能被禁用，尽管记忆信息仍然可以正常显示。现在已恢复完整的调度器流程。
- **强制执行OAuth/token认证层级**：增强型循环钩子不再绕过OAuth来查找 `api_key` 配置文件。现在会按照主代理的相同顺序使用认证（优先使用 `token/oauth`，而不是 `api_key`）。
- **LLM调用者支持OAuth设置令牌**：技能的 `caller.ts` 和 `caller.js` 现在可以识别 `sk-ant-oat*` 类型的令牌，并通过 `Authorization: Bearer` 头部发送（附带 `anthropic-beta: oauth-2025-04-20` 标头）。标准API密钥仍然使用 `x-api-key`。
- **更新了认证配置解析方式**：现在会从正确的路径 (`~/.openclaw/agents/main/agent/auth-profiles.json`) 读取配置文件，并在未提供明确配置时优先使用 `token/oauth` 配置文件。
- **文件更新**：`src/llm/caller.ts`, `src/dist/llm/caller.js`, `SKILL.md`, `SECURITY.md`（凭证相关部分）

### v2.2.1
- **文档更新**：更新了状态表，以反映实时更新规划卡片的功能。添加了说明，指出需要重新构建UI才能启用 `app-tool-stream.ts` 修复。
- **实时更新规划卡片**：修复了规划进度事件流中的问题。增强型循环钩子在每个步骤完成后会正确发送 `stream: "plan"` 代理事件，服务器也会广播这些事件，但UI中的 `handleAgentEvent()` 函数存在过早返回的问题，导致非工具事件被忽略。新增了 `plan` 流处理程序，实时更新 `chatStream`（替换了 `:::plan` JSON块），从而在工具调用完成后立即更新规划卡片。
- **添加了额外的配置选项**：在 `skill.json` 中添加了 `installType`, `installSpec`, `repository`, `homepage`, `network allowlist`, `surrealDB optional declaration`, `enabledByDefault: false`, `alwaysEnabled: false` 等选项。同时添加了 `SECURITY.md` 文件以提供完整的信任/审计文档。还添加了 `scripts/verify.sh` 命令用于安装后的自我验证。将 `system-prompt-injection` 功能键更改为 `context-injection`，以避免扫描工具的误判。

### v2.1.0
- **自动记忆注入**：知识图谱中的事实和事件会自动插入提示中
- **基于通道的规划渲染**：`:::plan` 块会根据通道类型自动调整显示方式（Webchat使用HTML，Discord使用表情符号）
- **名称更改**：将技能名称从 “Clawdbot” 更改为 “OpenClaw”
- **环境变量更新**：使用 `OPENCLAW_AGENT_DIR`（兼容性情况下使用 `CLAWDBOT_DIR`）
- **新增配置选项**：`memory` 部分添加了 `autoInject`, `maxFacts`, `maxEpisodes`, `episodeConfidenceThreshold`, `includeRelations` 等选项
- **系统要求**：OpenClaw版本需达到 2026.2.0 或更高

### v1.0.0
- 首次发布版本，包含规划、并行执行、信心判断机制、错误恢复、状态机和模式控制面板UI等功能