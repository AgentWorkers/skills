---
name: task-router
description: Distributed task queue and agent coordinator for OpenClaw multi-agent systems. Route tasks to specialized agents by capability matching, track task lifecycle, handle async handoffs, rebalance loads, and manage dead letters. Use when: (1) Creating tasks programmatically or from heartbeats, (2) Routing work to specialized agents based on capabilities, (3) Monitoring task status and completion, (4) Coordinating multi-step workflows across agents, (5) Handling async agent work without blocking main sessions.
---

# 任务路由器（Task Router）

这是一个用于 OpenClaw 多代理系统的分布式任务队列工具，提供集中协调、异步任务分配以及基于代理能力的路由功能。

## 快速入门

```bash
# Install skill
clawhub install task-router

# Register an agent
task agent register watson --capabilities "research analysis" --max-concurrent 3

# Create a task
task create --type research --title "Competitor analysis" --priority high

# Router runs automatically via heartbeat
# Check task status
task list --status pending
task show task-abc123
```

## 功能介绍

**核心功能：**
- **排队（Enqueue）**：可以从任何会话（主代理或子代理）创建任务。
- **路由（Route）**：根据代理的能力将任务分配给相应的代理。
- **跟踪（Track）**：监控任务的生命周期（待处理 → 运行中 → 完成/失败）。
- **异步协调（Async Coordination）**：异步分配任务，稍后进行检查。
- **死信处理（Dead Letter）**：处理超时和失败的任务。
- **任务重分配（Rebalance）**：将卡住的任务重新分配给其他代理，并提供重试机制。

**使用场景：**
- 主代理创建研究任务后，系统会自动将其路由到负责研究的代理。
- 多步骤工作流程：任务 A 的输出结果会作为任务 B 的输入。
- 当代理失败时，任务会被重新分配给备用代理。
- 实现具有相同能力的代理之间的负载均衡。

## 配置

### 文件结构
```
~/.openclaw/task-router/
├── config.yaml           # Router settings, timeouts
├── agents.yaml           # Agent registry + capabilities
├── queue/                # Task state
│   ├── pending/          # Waiting for assignment
│   ├── active/           # Assigned to agent
│   ├── completed/        # Finished successfully
│   └── failed/           # Failed, exhausted retries
└── logs/
    └── router.log        # Routing decisions
```

### config.yaml
```yaml
router:
  check_interval: 30           # Seconds between router runs
  default_ttl: 3600            # Default task timeout
  max_retries: 2
  
  strategies:
    default: least-loaded      # round-robin | least-loaded | priority
    by_type:
      research: least-loaded
      image_gen: round-robin
      urgent: priority

  health:
    agent_timeout: 300           # Mark agent unhealthy after seconds
    task_timeout:
      warning: 1800              # Alert at 30 min
      critical: 3600             # Fail at 1 hour

  notifications:
    on_complete: true
    on_fail: true
    channels: [main_session]   # Could add Discord, etc.
```

### agents.yaml（自动维护）
```yaml
agents:
  watson:
    id: watson
    emoji: 🔬
    capabilities: [research, analysis, web_search]
    max_concurrent: 3
    current_tasks: [task-abc123, task-def456]
    stats:
      completed: 47
      failed: 2
      avg_duration: 180
    health:
      last_ping: 2026-02-13T09:15:00Z
      status: healthy
    
  picasso:
    id: picasso
    emoji: 🎨
    capabilities: [image_gen, image_edit]
    max_concurrent: 2
    current_tasks: []
```

## 任务结构（Task Schema）
```yaml
id: task-abc123
type: research               # Matches agent capability
title: Research Gameye competitors
description: Deep competitive analysis

payload:
  query: Gameye vs competitors
  sources: [web, apollo]
  output_format: markdown
  
created_by: main             # Session label that created it
assigned_to: watson          # null until routed
assigned_by: router          # router | manual | agent

created_at: 2026-02-13T09:00:00Z
assigned_at: 2026-02-13T09:05:00Z
started_at: 2026-02-13T09:06:00Z
completed_at: null
expires_at: 2026-02-13T10:00:00Z  # created_at + ttl

priority: high               # low | normal | high | urgent
ttl: 3600                    # Seconds
retries: 0
max_retries: 2

dependencies: []             # Block until these complete
blocked_by: []               # Populated by router

status: assigned             # pending | assigned | running | complete | failed
result: null                 # Path to result file
error: null                  # Error message if failed

metadata:
  source: heartbeat
  tags: [gameye, competitors]
```

## 命令行接口（CLI Commands）

### 任务管理
```bash
# Create task
task create --type research \
  --title "Research Gameye competitors" \
  --data '{"query": "Gameye pricing"}' \
  --priority high \
  --ttl 3600

# Create with dependencies
task create --type analysis \
  --title "Analyze research results" \
  --depends-on task-abc123

# List tasks
task list                    # All non-completed
task list --status pending
task list --assigned-to watson
task list --type research --limit 10
task list --created-after 2026-02-13

# Show task
task show task-abc123        # Full details + result preview

# Manage tasks
task cancel task-abc123      # Cancel pending or active
task retry task-abc123       # Move failed back to pending
task reprioritize task-abc123 --priority urgent

# Results
task result task-abc123      # View result file
task export --status completed --since 2026-02-13 > ~/reports/tasks.ndjson
```

### 代理管理
```bash
# Register agent (required before routing)
task agent register watson \
  --capabilities "research analysis web_search" \
  --max-concurrent 3 \
  --emoji 🔬

# Update agent
task agent update watson --add-capability "competitive-analysis"
task agent update watson --max-concurrent 5

# Check agent health
task agent status watson     # Current tasks, health, stats
task agent ping watson       # Health check ping

# List agents
task agent list              # All agents
task agent list --capable-of research

# Unregister
task agent unregister watson --reassign-tasks
```

### 路由器控制
```bash
# Status
task router status           # Queue depth, agent health

# Control flow
task router pause            # Stop new assignments
task router resume           # Resume routing
task router rebalance        # Redistribute stuck tasks

# Maintenance  
task router cleanup          # Archive old completed tasks
task router drain            # Finish active, no new pending
```

## 程序化 API
```typescript
import * as Task from "~/.openclaw/task-router/sdk";

// === Creating Tasks ===

// Simple create
const task = await Task.create({
  type: "research",
  title: "Competitor analysis",
  payload: { query: "Gameye vs competitors" }
});

// With options
const task = await Task.create({
  type: "image_gen",
  title: "Generate hero image",
  payload: { prompt: "Futuristic game server...", size: "1024x1024" },
  priority: "high",
  ttl: 1800,
  max_retries: 1,
  dependencies: [previousTaskId],  // Waits for these first
  created_by: "main"
});

// === Querying ===

// Get status
const status = await Task.status(task.id);
// { id, status, assigned_to, created_at, expires_at }

// Wait for completion (blocking)
const result = await Task.wait(task.id, { timeout: 300, pollInterval: 5 });

// List with filters
const pending = await Task.query({
  status: "pending",
  type: "research",
  priority: "high",
  limit: 10
});

const myTasks = await Task.query({
  created_by: "main",
  status: ["assigned", "running"]
});

// === Agent Integration ===

// Agent picks up work (if auto-assign disabled)
await Task.claim({
  agentId: "watson",
  capableOf: "research",
  limit: 1
});

// Complete task
await Task.complete(task.id, {
  result_path: "~/agents/watson/memory/results/competitors.md",
  summary: "Found 5 competitors: GameLift, Multiplay, Hathora, Edgegap, Agones",
  metadata: { competitors_count: 5 }
});

// Fail task
await Task.fail(task.id, {
  reason: "API quota exceeded",
  retryable: true  // Will auto-retry
});

// === Multi-Step Workflows ===

// Chain tasks
const analysisTask = await Task.chain(researchTask.id, {
  type: "analysis",
  title: "Analyze research findings",
  payload: { input_task: researchTask.id }
});

// Parallel tasks
const tasks = await Task.parallel([
  { type: "research", title: "Research A", payload: {} },
  { type: "research", title: "Research B", payload: {} },
  { type: "research", title: "Research C", payload: {} }
]);
await Task.waitAll(tasks.map(t => t.id));

// === Agent Session Integration ===

// Spawn via task router (recommended for async work)
const spawnResult = await Task.spawn({
  taskId: task.id,
  agentId: "watson",      // Optional: auto-route if omitted
  useSession: true      // Use sessions_spawn vs sessions_send
});

// Router will call:
// sessions_spawn({ agentId, task, label: task.id })
```

## 与 HEARTBEAT 的集成

在 `~/.openclaw/workspace/HEARTBEAT.md` 文件中添加以下代码：
```markdown
# Task Router Heartbeat

## Router Cycle (runs every 30s)
```typescript
import * as Task from "~/.openclaw/task-router/sdk";

// 1. 自动路由待处理任务
const routed = await Task.router_cycle();
if (routed.length > 0) {
  Task.log(`已路由的任务数量：${routed.length}，分配给：${routed.map(t => `${t.id} → ${t.assigned_to}`));
}

// 2. 检查超时情况
const timeouts = await Task.router.checkTimeouts();
for (const task of timeouts) {
  if (task.retries < task.max_retries) {
    Task.log(`正在重试任务 ${task.id}（已超时）`);
    await Task.retry(task.id);
  } else {
    Task.log(`将任务 ${task.id} 归类为“死信”`);
    await Task.router.moveToDeadLetter(task);
  }
}

// 3. 检查代理健康状况
const unhealthy = await Task.agents.checkHealth();
for (const agent of unhealthy) {
  // 重新分配该代理的任务
  await Task.router.reassignFrom(agent.id);
}

// 4. 通知任务完成
const recent = await Task.query({
  status: "completed",
  completed_after: Date.now() - 60000  // 最近 60 分钟内完成的任务
});
for (const task of recent) {
  if (task.created_by === "main") {
    sessions_send({
      message: `✅ 任务完成：${task.title}\n结果：${task.result}`
    });
  }
}
```

## Routing Strategies

| Strategy | Use Case | Description |
|----------|----------|-------------|
| **round-robin** | Even load | Cycle through agents |
| **least-loaded** | Prevent overload | Agent with fewest active tasks |
| **fastest** | Latency critical | Agent with best completion time |
| **priority** | Urgent tasks | Sort by priority first |
| **sticky** | Sequential work | Same agent for related tasks |

```yaml
# config.yaml
strategies:
  default: least-loaded
  
  # 按任务类型划分的策略
  by_type:
    research: least-loaded      # 避免让某个研究员负担过重
    image_gen: round-robin      # 平均分配 GPU 资源
    urgent: priority             # 始终选择性能最好的代理
    
  # 自定义规则
  rules:
    - if: priority == urgent
      then: fastest
    - if: tags includes "sticky"
      then: sticky
```

## Task Lifecycle Details

```
待处理（PENDING）─→ 分配（ASSIGNED）─→ 运行中（RUNNING）─→ 完成（COMPLETE）─→ 失败（COMPLETE）
   │           │          │              │                      │
   │           │          │              └── 失败（FAILED）─→ 重试（RETRY）┐            │
   │           │          │                        ↓            │
   │           │          │                     失败（FAILED）─→ 重试（RETRY）┘
   │           │          │                （超时则归类为“死信”）    │
   │           │          │                                     │
   └───────────┴──────────┘─────────────────────────────────────┘
```

**State Definitions:**
- `pending`: Created, waiting for router
- `assigned`: Routed to agent, waiting for acceptance
- `running`: Agent acknowledged, working on it
- `complete`: Success, result available
- `failed`: Final failure (retries exhausted)
- `dead_letter`: Failed permanently, needs manual review

## Dead Letter Queue

When a task exhausts retries:

```
~/.openclaw/task-router/dead-letter/
├── task-failed-001.yaml       # 存储失败任务的详细信息
├── task-failed-002.yaml
└── index.yaml                 # 供管理员查看的失败任务汇总文件
```

```bash
# 查看失败任务
task dead-letter list
task dead-letter show task-failed-001

# 执行操作
task dead-letter retry task-failed-001      # 强制重试任务
task dead-letter reassign task-failed-001 --to watson
task dead-letter archive task-failed-001   # 批量归档失败任务
```

## Best Practices

**Task Design:**
- Keep payloads JSON-serializable (no circular refs)
- Include output format hints in payload
- Use dependencies for true sequencing
- Set reasonable TTLs (don't block forever)

**Agent Design:**
- Register capabilities narrowly at first
- Set conservative max_concurrent
- Heartbeat should check for assigned tasks
- Always acknowledge → complete/fail cleanly

**Coordination Patterns:**
- Use `Task.spawn()` for fire-and-forget
- Use `Task.wait()` when user needs result now
- Chain dependent tasks vs one mega-task
- Let router handle retries, not agents

## Multi-Agent Example

```typescript
// 用户请求：研究竞争对手并生成报告
// 主代理（你）执行以下操作：
// 1. 创建研究任务
const research = await Task.create({
  type: "research",
  title: "研究 Gameye 的竞争对手",
  payload: { query: "Gameye vs competitors" }
});

// 2. 创建分析任务（依赖于研究结果）
const analysis = await Task.create({
  type: "analysis",
  title: "分析竞争格局",
  dependencies: [research.id],
  payload: { input_task: research.id }
});

// 3. 创建图像任务（独立执行）
const images = await Task.parallel([
  { type: "image_gen", title: "竞争对手对比图表", payload: {} },
  { type: "image_gen", title: "市场定位图", payload: {} }
]);

// 4. 创建报告任务（依赖于前两个任务的结果）
const deck = await Task.create({
  type: "presentation",
  title: "Gameye 竞争分析报告",
  dependencies: [analysis.id, ...images.map(i => i.id)],
  payload: { 
    research: analysis.id,
    images: images.map(i => i.result)
  }
});

// 5. 等待最终结果
const result = await Task.wait(deck.id, { timeout: 600 });

// 结果：协调了 4 个代理和 5 个任务，处理了所有依赖关系
```

## Troubleshooting

```bash
# 检查任务路由状态
task router status           # 任务路由是否暂停？
task agent list             # 有哪些代理处于健康状态？
task list --status pending  # 有哪些任务处于待处理状态？
# 某个任务卡住了？
task show task-abc123        # 查看任务的分配情况和开始时间
task agent status watson     # 代理是否正常运行？

# 如果代理没有响应？
# - 检查代理的 HEARTBEAT 服务是否正常工作
# - 确认 `sessions_send` 操作是否能够成功发送任务
# 如果失败次数过多？
task dead-letter list       # 分析失败原因
task router logs            # 查看任务路由的详细记录

# 清除所有任务
task router drain           # 清空任务队列
task list --status pending | xargs task cancel
task dead-letter clear
```

## 系统要求

- 需要安装 OpenClaw，并确保其支持 `sessions_send`、`sessions_spawn` 和 `sessions_list` 等接口。
- 所有代理都必须配置并运行 `HEARTBEAT.md` 服务以接收和处理任务。
- 如果 HEARTBEAT 服务不可靠，可以考虑使用定时任务（cron job）来触发任务路由。

## 未来扩展计划

- **指标统计（Metrics）**：提供与 Prometheus 兼容的统计信息。
- **Web 界面（Web UI）**：在 `localhost:3333` 提供任务管理面板。
- **插件（Plugins）**：支持通过 Slack 或 Discord 发送通知。
- **优先级队列（Priority Queues）**：允许为不同类型的任务设置不同的优先级。