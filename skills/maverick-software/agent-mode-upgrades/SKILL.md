# 增强型代理循环技能（Enhanced Agentic Loop Skill）

这是对Clawdbot代理功能的全面升级，新增了持久化状态、自动规划、审批机制、重试逻辑、上下文管理以及检查点功能。

## 状态：✅ 已激活（Status: ✅ Active）

所有组件均已集成并正常运行。

| 组件 | 状态 |  
|-----------|--------|  
| 模式控制面板UI（Mode Dashboard UI） | ✅ 可用 |  
| 配置系统（Configuration System） | ✅ 可用 |  
| 钩子/包装器集成（Hook/Wrapper Integration） | ✅ 可用 |  
| 状态机（State Machine） | ✅ 可用 |  
| 规划层（Planning Layer） | ✅ 可用 |  
| 并行执行（Parallel Execution） | ✅ 可用 |  
| 信任度检查（Confidence Gates） | ✅ 可用 |  
| 错误恢复（Error Recovery） | ✅ 可用 |  
| 检查点（Checkpointing） | ✅ 可用 |  

## 主要特性：  
### 1. 持久化计划状态（Persistent Plan State）  
计划信息会在对话轮次之间保持不变。代理能够记住上一次的执行状态。  

```typescript
import { getStateManager } from "@clawdbot/enhanced-loop";

const state = getStateManager();
await state.init(sessionId);

// Plan persists in ~/.clawdbot/agent-state/{sessionId}.json
state.setPlan(plan);
state.completeStep("step_1", "Files created");
const progress = state.getProgress(); // { completed: 1, total: 5, percent: 20 }
```  

### 2. 自动步骤完成检测（Automatic Step Completion Detection）  
分析工具执行结果，判断计划步骤是否已完成。  

```typescript
import { createStepTracker } from "@clawdbot/enhanced-loop";

const tracker = createStepTracker(stateManager);

// After each tool execution
const analysis = await tracker.analyzeToolResult(tool, result);
if (analysis.isComplete) {
  console.log(`Step done: ${analysis.suggestedResult}`);
}
```  

### 3. 带有超时机制的工具审批流程（Tool Approval Gates with Timeout）  
高风险操作会暂停等待人工审批，超时后自动继续执行。  

```typescript
import { getApprovalGate } from "@clawdbot/enhanced-loop";

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

**风险等级（Risk Levels）：**  
- `低风险`：读取操作（自动批准）  
- `中等风险`：写入/编辑、安全执行  
- `高风险`：发送消息、浏览器操作、推送代码到Git  
- **高风险**：删除文件、删除数据库、执行格式化命令  

### 4. 自动重试机制（Automatic Retry）  
遇到失败的工具会自动诊断并尝试其他方法重新执行。  

```typescript
import { createRetryEngine } from "@clawdbot/enhanced-loop";

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

### 5. 上下文摘要（Context Summarization）  
当上下文信息过长时，系统会自动对其进行总结。  

```typescript
import { createContextSummarizer } from "@clawdbot/enhanced-loop";

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

### 6. 检查点与恢复功能（Checkpoint/Restore）  
支持在会话之间保存和恢复长时间运行的任务。  

```typescript
import { getCheckpointManager } from "@clawdbot/enhanced-loop";

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

## 统一编排器（Unified Orchestrator）  
推荐的使用方式：  

```typescript
import { createOrchestrator } from "@clawdbot/enhanced-loop";

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

## 模式控制面板集成（Mode Dashboard Integration）  
该技能为Clawdbot的控制面板提供了“模式”（Mode）选项卡：  
**位置：** 代理 > 模式（Location: Agent > Mode）  
**功能：**  
- 在“核心循环”（Core Loop）和“增强型循环”（Enhanced Loop）之间切换  
- 通过可视化界面配置所有设置  
- 从Clawdbot模型目录中选择合适的编排器模型（用于成本控制）  
- 实时预览配置内容  

## 与Clawdbot的集成（Integration with Clawdbot）  
该技能通过Clawdbot中的“增强型循环钩子”（enhanced-loop-hook）进行集成：  
1. **配置文件：** `~/.clawdbot/agents/main/agent/enhanced-loop-config.json`  
2. **自动激活：** 启用后，该钩子会：  
   - 检测用户消息中的规划意图  
   - 将计划上下文添加到系统提示中（不会替换或覆盖现有系统提示）  
   - 跟踪工具执行情况和步骤进度  
   - 自动创建检查点  
   - 提供恢复未完成任务的功能  

## 凭据与安全机制（Credentials and Security）：  
- **无需额外API密钥。** 编排器会使用Clawdbot代理现有的认证信息（通过`resolveApiKeyForProvider`函数）。为兼容直接API调用，优先使用`api_key`类型的认证信息。  
- **编排器模型可动态选择：** 通过模式控制面板从Clawdbot模型目录（`models.list`）中选择模型。选择较小的模型可以降低成本（尤其是用于规划或反射调用时）。  
- **无外部网络请求：** 仅使用配置好的大型语言模型（LLM）提供商的API（例如`api.anthropic.com`），不进行其他网络通信。  
- **数据持久化仅限于本地：** 计划状态、检查点和配置信息保存在`~/.clawdbot/`目录下，不使用云存储。  
- **系统提示的修改方式：** 该钩子会在代理的`extraSystemPrompt`字段中添加计划上下文和步骤进度，不会替换或覆盖核心系统提示或安全策略。  
- **包装器透明性：** `wrapRun`函数始终调用原始的代理执行逻辑，仅在原有调用基础上添加编排功能（如规划、上下文注入和进度跟踪）。  

## 意图检测（Intent Detection）  
以下情况会自动触发规划流程：  
**明确表达的意图：**  
- “plan...”、“help me...”、“how should I...”  
- “figure out...”、“walk me through...”  
- “what’s the best way...”、“I need to...”  

**复杂任务的处理：**  
- 包含复杂动词和名词的组合（如“build API”、“create site”）  
- 顺序性指令（如“first... then...”）  
- 表示范围的词汇（如“full”、“complete”、“from scratch”）  

## 文件结构（File Structure）  
```
~/.clawdbot/
├── agents/main/agent/
│   └── enhanced-loop-config.json    # Configuration
├── agent-state/                      # Persistent plan state
│   └── {sessionId}.json
└── checkpoints/                      # Checkpoint files
    └── {sessionId}/
        └── ckpt_*.json
```  

## 源代码结构（Source Structure）  
```
src/
├── index.ts                 # Main exports
├── orchestrator.ts          # Unified orchestrator
├── types.ts                 # Type definitions
├── clawdbot-hook.ts         # Clawdbot integration hook
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

## 用户界面结构（UI Structure）  
```
ui/
├── views/
│   └── mode.ts              # Mode page view (Lit)
└── controllers/
    └── mode.ts              # Mode page controller
```  

## 版本信息（Version）  
v1.0.0 – 全功能代理循环，包含模式控制面板UI