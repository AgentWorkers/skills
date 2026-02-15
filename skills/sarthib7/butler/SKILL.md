# Butler - 人工智能代理的财务管理与任务编排技能

## 概述

**Butler** 是一个基于 OpenClaw 的技能，它能够将人工智能代理转变为自主的经济实体。该技能负责管理多提供者的代币预算，为复杂任务生成子代理，并在预算耗尽时自动处理代币购买。

可以将 Butler 视为你的 **人工智能代理的首席财务官**，它具备以下功能：
- 💰 实时监控 8 个 API 密钥和 6 个提供者的代币使用情况
- 🚀 根据预算自动分配资源来生成子代理
- 🔄 在密钥使用接近上限时自动更换密钥
- 📊 整合来自并行任务的执行结果
- 🛡️ 与 Code Reviewer 集成以确保安全性

## 快速入门

### 安装

```bash
npm install butler
# or
yarn add butler
```

### 基本使用

```typescript
import { Butler } from 'butler';

// Initialize
const butler = new Butler();

// Allocate tokens for a task
const allocation = butler.allocateTokens('PRD-my-task.md', 'anthropic');
console.log(`✅ Allocated ${allocation.allocated} tokens on ${allocation.provider}`);

// Spawn agents for complex work
const results = await butler.spawnAgent(
  'DataAnalysis',
  'Analyze sales data and write report',
  100000, // tokens
  { maxConcurrent: 3, retryOnFailure: true }
);

// Get status
const status = butler.getStatus();
console.log(`🎯 Status:`, status);
```

## 功能

### 1. 代币管理

Butler 可实时监控 6 个提供者下的 8 个 API 密钥的代币使用情况：

```typescript
// Get available keys
const keys = butler.getAvailableKeys();
// [
//   { id: 'nvidia-1', provider: 'nvidia', model: 'llama-3.1', ... },
//   { id: 'anthropic-1', provider: 'anthropic', model: 'claude-sonnet', ... },
//   { id: 'groq-1', provider: 'groq', model: 'llama-3.1', ... },
//   ...
// ]

// Estimate tokens for PRD
const estimate = butler.allocateTokens('PRD-integration.md');
// Analyzes PRD complexity and recommends optimal allocation

// Monitor usage
const status = butler.monitorUsage();
// { keys_by_provider: { nvidia: {...}, anthropic: {...}, ... } }
```

**支持的提供者：**
- **Nvidia**（3 个密钥，每天 500 万代币）- 免费 tier ✅
- **Groq**（1 个密钥，每天 1000 万代币）- 免费 tier ✅
- **Anthropic**（1 个密钥，每天 100 万代币）- 当前支持的模型
- **OpenAI**（1 个密钥，每天 50 万代币）
- **OpenRouter**（1 个密钥，每天 200 万代币）
- **Sokosumi**（1 个密钥）- 用于定制或研究用途

**总容量：** 每天 2850 万代币

### 2. 代理任务编排

能够生成多个子代理，并自动分配任务和预算：

```typescript
// Simple spawn (auto-decompose)
const results = await butler.spawnAgent(
  'ComplexResearch',
  `Research AI agent frameworks:
   1. Gather information from 5+ sources
   2. Analyze capabilities and limitations  
   3. Write detailed comparison report
   4. Validate findings with expert review`,
  250000 // tokens
);

// Advanced spawn with options
const results = await butler.spawnAgent(
  'DataPipeline',
  'Extract, transform, validate, load data',
  500000,
  {
    maxConcurrent: 4,        // Run up to 4 sub-agents in parallel
    retryOnFailure: true,    // Retry failed sub-tasks
    maxRetries: 3,           // Up to 3 retry attempts
    timeoutMs: 600000        // 10 minute timeout per sub-agent
  }
);

// Get results
results.forEach(result => {
  console.log(`Sub-task ${result.subTaskId}:`);
  console.log(`  Status: ${result.status}`);
  console.log(`  Tokens: ${result.tokensUsed}`);
  if (result.error) console.log(`  Error: ${result.error}`);
});
```

**任务分解算法：**
```
Input: "Research AI frameworks, analyze patterns, write report"
         ↓
1. Keyword detection: "research", "analyze", "write"
         ↓
2. Sub-task creation:
   - Subtask 1: "research AI frameworks" (30% budget)
   - Subtask 2: "analyze patterns" (40% budget)
   - Subtask 3: "write report" (30% budget)
         ↓
3. Priority boost (if specified)
         ↓
4. Concurrent execution (respects maxConcurrent)
         ↓
5. Result aggregation
```

### 3. 预算分配

根据任务的复杂性和优先级自动分配预算：

```typescript
// High-priority task gets more budget
const task = {
  totalBudget: 100000,
  subTasks: [
    {
      id: 'low-priority-task',
      estimatedTokens: 50000,
      priority: 'low'      // 0.5x multiplier = 25k tokens
    },
    {
      id: 'critical-task',
      estimatedTokens: 50000,
      priority: 'critical' // 2.0x multiplier = 100k tokens (capped)
    }
  ]
};

// Allocation: { 'low-priority-task': 33k, 'critical-task': 67k }
```

**优先级系数：**
- `low`：0.5 倍（预计需求的 50%）
- `medium`：1.0 倍（预计需求的 100%）
- `high`：1.5 倍（预计需求的 150%）
- `critical`：2.0 倍（预计需求的 200%）

### 4. 自动轮换密钥

当密钥使用率达到 75% 的阈值时，系统会自动更换密钥，以防止资源耗尽：

```typescript
// Automatic tracking and alerts
const status = butler.getStatus();
// When session reaches 75% of allocated budget:
// ✅ Alert issued
// 🔄 New key auto-selected
// 📊 Session updated with new key
// 📝 Change logged to history

// Manual rotation if needed
butler.rotateKey('session-id-123', 'anthropic-1');
```

### 5. 结果聚合

自动汇总来自各个代理的任务执行结果：

```typescript
const results = await butler.spawnAgent('ComplexTask', 'task description', 100000);

// After execution, aggregate results:
const aggregated = butler.aggregateTaskResults(results[0].taskId);
// {
//   taskId: 'task-...',
//   totalSubTasks: 5,
//   successful: 4,
//   failed: 1,
//   totalTokensUsed: 87500,
//   successRate: 80,
//   details: [
//     { id: 'subtask-1', status: 'success', tokensUsed: 18000 },
//     { id: 'subtask-2', status: 'success', tokensUsed: 22000 },
//     { id: 'subtask-3', status: 'success', tokensUsed: 19500 },
//     { id: 'subtask-4', status: 'success', tokensUsed: 21000 },
//     { id: 'subtask-5', status: 'failure', tokensUsed: 7000, error: 'timeout' }
//   ]
// }
```

## 示例

### 示例 1：为复杂任务分配代币

```typescript
import { Butler } from 'butler';

const butler = new Butler();

// Create PRD file
const prd = `
# AI Agent Integration Task

## Requirements
- Integrate OpenAI API
- Build agent orchestration
- Write unit tests
- Deploy to production

## Constraints
- Budget: $100/day
- Timeline: 1 week
- Team: 2 engineers
`;

fs.writeFileSync('PRD-integration.md', prd);

// Get smart allocation
const allocation = butler.allocateTokens('PRD-integration.md');

if (allocation.success) {
  console.log(`
✅ Recommended:
   Key: ${allocation.key_id} (${allocation.provider})
   Budget: ${allocation.allocated.toLocaleString()} tokens
   Cost: $${allocation.cost_estimate.toFixed(2)}
   Rotate at: ${allocation.rotation_threshold.toLocaleString()} tokens
   Available: ${allocation.available_capacity.toLocaleString()} tokens
  `);
}
```

### 示例 2：并行执行代理任务

```typescript
import { Butler } from 'butler';

const butler = new Butler();

async function analyzeDataset() {
  const results = await butler.spawnAgent(
    'DatasetAnalysis',
    `
    1. Extract data from sources
    2. Clean and validate data
    3. Run statistical analysis
    4. Create visualizations
    5. Write findings report
    `,
    300000,
    { maxConcurrent: 3, retryOnFailure: true }
  );

  // Process results
  const aggregated = butler.aggregateTaskResults(results[0].taskId);
  
  console.log(`
📊 Analysis Complete:
   Successful: ${aggregated.successful}/${aggregated.totalSubTasks}
   Success Rate: ${aggregated.successRate.toFixed(1)}%
   Total Tokens: ${aggregated.totalTokensUsed.toLocaleString()}
  `);

  return aggregated;
}

analyzeDataset().then(result => {
  console.log('Results:', result.details);
});
```

### 示例 3：错误处理与重试

```typescript
import { Butler } from 'butler';

const butler = new Butler();

async function reliableProcessing() {
  try {
    const results = await butler.spawnAgent(
      'RobustProcessing',
      'Process data with validation and error handling',
      200000,
      {
        retryOnFailure: true,
        maxRetries: 3,  // Retry up to 3 times
        maxConcurrent: 2,
        timeoutMs: 120000  // 2 minute timeout
      }
    );

    const aggregated = butler.aggregateTaskResults(results[0].taskId);

    if (aggregated.failed > 0) {
      console.log(`⚠️  ${aggregated.failed} sub-tasks failed:`);
      aggregated.details
        .filter((d: any) => d.status === 'failure')
        .forEach((d: any) => {
          console.log(`   - ${d.id}: ${d.error}`);
        });

      // Optionally retry failed tasks
      await butler.retryFailedTasks(results[0].taskId);
    }

    return aggregated;
  } catch (error) {
    console.error('Task failed:', error);
    throw error;
  }
}

reliableProcessing();
```

### 示例 4：监控代币使用情况

```typescript
import { Butler } from 'butler';

const butler = new Butler();

// Check current status
const status = butler.getStatus();

console.log(`
📊 Token Status:
   Total Keys: ${status.tokens.total_keys}
   Active: ${status.tokens.active_keys}
   Sessions: ${status.tokens.active_sessions}
   Pending Alerts: ${status.tokens.pending_alerts}
`);

// Get detailed provider breakdown
Object.entries(status.tokens.keys_by_provider).forEach(([provider, stats]: any) => {
  const usage = ((stats.used_today / stats.total_capacity) * 100).toFixed(1);
  console.log(`
${provider.toUpperCase()}:
   Capacity: ${stats.total_capacity.toLocaleString()} tokens/day
   Used: ${stats.used_today.toLocaleString()} (${usage}%)
   Remaining: ${stats.remaining.toLocaleString()}
   Cost: $${stats.cost_today.toFixed(2)}
  `);
});

// Available keys for next allocation
const available = butler.getAvailableKeys();
console.log(`\nAvailable keys: ${available.length}`);
available.forEach(key => {
  console.log(`   - ${key.id} (${key.provider}): ${key.limits.tokens_per_day.toLocaleString()} tokens/day`);
});
```

## API 参考

### Butler 类

#### `constructor(keysPath?: string, statePath?: string)`
使用可选的自定义路径来初始化 Butler，指定 API 密钥和状态文件的路径。

#### `allocateTokens(prdPath: string, preferredProvider?: string): AllocationResult`
分析项目需求（PRD）并推荐最佳的代币分配方案。

**返回值：**
```typescript
{
  success: boolean;
  key_id?: string;        // Recommended key ID
  key?: string;           // API key
  provider?: string;      // Provider name
  model?: string;         // Model to use
  allocated?: number;     // Allocated tokens
  rotation_threshold?: number;  // Alert threshold (75%)
  available_capacity?: number;  // Current available tokens
  cost_estimate?: number; // Estimated cost
}
```

#### `spawnAgent(name: string, description: string, budget: number, options?: AgentOptions): Promise<TaskResult[]>`
生成子代理以执行任务。

**参数：**
```typescript
{
  maxConcurrent?: number;    // Default: 3
  retryOnFailure?: boolean;  // Default: true
  maxRetries?: number;       // Default: 2
  timeoutMs?: number;        // Default: 300000
}
```

**返回值：** 包含任务结果、使用的代币数量以及错误信息的数组。

#### `getStatus(): Status`
获取系统的整体运行状态。

#### `getAvailableKeys(): APIKey[]`
列出所有可用的 API 密钥。

#### `monitorUsage(): MonitorStatus`
获取按提供者划分的详细代币使用情况。

#### `rotateKey(sessionId: string, newKeyId?: string): RotationResult`
手动更换 API 密钥。

#### `aggregateTaskResults(taskId: string): AggregatedResult`
汇总已完成任务的执行结果。

#### `retryFailedTasks(taskId: string): Promise<TaskResult[]>`
重试失败的任务。

## 架构

详细系统设计请参阅 [ARCHITECTURE.md](./ARCHITECTURE.md)。

```
┌─────────────────────────────────────┐
│         Butler Skill                 │
├─────────────────────────────────────┤
│                                     │
│  Token Manager                      │
│  ├─ 8 API Keys (6 providers)       │
│  ├─ Real-time usage tracking        │
│  ├─ 75% threshold alerts            │
│  └─ Automatic rotation              │
│                                     │
│  Agent Orchestrator                 │
│  ├─ Task decomposition              │
│  ├─ Budget allocation               │
│  ├─ Sub-agent spawning              │
│  ├─ Parallel execution              │
│  └─ Result aggregation              │
│                                     │
│  Treasury Manager (v0.2)            │
│  ├─ USDC balance monitoring         │
│  ├─ Circle API integration          │
│  ├─ Auto-buy triggers               │
│  └─ Transaction logging             │
│                                     │
│  Security Gate                      │
│  ├─ Code Reviewer integration       │
│  ├─ Pre-commit scanning             │
│  └─ Credential leak prevention      │
│                                     │
└─────────────────────────────────────┘
```

## 配置

### 环境变量

```bash
# Optional - defaults to ~/.openclaw/workspace/api-keys.json
BUTLER_KEYS_PATH=/path/to/keys.json

# Optional - defaults to ~/.openclaw/workspace/token-manager-state.json
BUTLER_STATE_PATH=/path/to/state.json

# Treasury config (v0.2)
CIRCLE_API_KEY=your_circle_key
STRIPE_API_KEY=your_stripe_key
AUTO_BUY_ENABLED=true
AUTO_BUY_THRESHOLD=50    # USDC
AUTO_BUY_AMOUNT=200      # USDC
```

## 测试

运行完整的测试套件：

```bash
npm test                  # Run all tests
npm run test:watch      # Watch mode
npm run test:coverage   # Coverage report
```

**测试覆盖范围：**
- ✅ 45 个以上的测试用例
- ✅ TokenManager 相关测试：15 个以上
- AgentOrchestrator 相关测试：20 个以上
- Butler 集成测试：15 个以上
- 模拟 API 调用测试
- 错误场景测试
- 负载测试
- 代码覆盖率超过 80%

## 故障排除

### 无可用密钥
```
Error: No keys available with sufficient capacity
```
**解决方案：** 等待每天 00:00 UTC 的自动重置，或使用多个预算较小的密钥。

### 密钥轮换阈值被超过
```
⚠️ [session-id] 75% budget used - Rotation recommended
```
**解决方案：** Butler 会自动切换到下一个可用的密钥。请通过 `getStatus()` 查看详细警告信息。

### 任务预算不足
```
Error: No single key has 999999 tokens available
```
**解决方案：** 将任务拆分为更小的子任务，或等待每天自动重置。

## 安全性

- ✅ 与 Code Reviewer 集成，防止凭证泄露
- ✅ 所有状态文件安全存储（不存储在 git 中）
- ✅ API 密钥从不记录（仅记录密钥 ID）
- ✅ 提交前会通过预提交钩子进行验证

**最佳实践：**
1. 始终将 `api-keys.json` 文件添加到 `.gitignore` 文件中
2. 为财务管理功能创建私有仓库
3. 提交前使用 Code Reviewer 进行代码审查
4. 定期更换密钥（手动或自动轮换）

## 性能

- ⚡ 代币分配时间：<100 毫秒
- ⚡ 代理生成时间：<500 毫秒
- ⚡ 结果汇总时间：O(n) 复杂度
- ⚡ 支持同时执行多个任务

## 发展计划（v0.2 及后续版本）

- [ ] 加入支持 USDC 的财务管理模块
- [ ] 集成 Circle 的 CCTP 服务
- [ ] 提供 Web 仪表板进行监控
- [ ] 实现基于机器学习的代币预测功能
- [ ] 支持多签名钱包
- [ ] 实现代理之间的费用分摊
- [ ] 开发移动应用程序

## 支持方式

- 📖 文档：[docs/](./docs/)
- 🐛 问题报告：[GitHub Issues](https://github.com/zoro-jiro-san/butler/issues)
- 💬 讨论区：[GitHub Discussions](https://github.com/zoro-jiro-san/butler/discussions)
- 📧 电子邮件：support@openclaw.dev

## 许可证

MIT 许可证 - 详细信息请参阅 [LICENSE](../LICENSE)

## 贡献方式

欢迎贡献！请参阅 [CONTRIBUTING.md](../CONTRIBUTING.md)

---

**Butler v0.1.0** | Circle USDC 霸客赛 | 截止日期：2026 年 2 月 8 日