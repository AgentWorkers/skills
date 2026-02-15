# **Colony Orchestration Skill**

该技能支持多智能体任务分配、流程协调，并具备审计日志记录和智能体学习功能。

## **快速入门**

```bash
# Single task - auto-routed
node scripts/colony.mjs dispatch "find top 5 time-series databases"

# Multi-stage process
node scripts/colony.mjs process validate-idea --context "AI meal planning for parents"
node scripts/colony.mjs process-status  # check progress
node scripts/colony.mjs approve abc123  # continue past checkpoint

# Check audit stats
node scripts/colony.mjs audit

# View agent memory
node scripts/colony.mjs memory scout
```

## **智能体**

| 智能体 | 角色 | 专长 |
|-------|------|----------------|
| **scuttle** | 研究员 | 快速搜索、信息查询、事实收集 |
| **scout** | 研究员 | 深度市场/竞争对手研究、情报收集 |
| **forecast** | 分析师 | 数据分析、趋势预测 |
| **pincer** | 编程员 | 代码编写、调试、代码重构 |
| **shell** | 操作员 | Git管理、部署、系统任务处理 |
| **forge** | 产品经理 | 产品需求文档（PRD）编写、规格制定、路线图规划 |
| **ledger** | 财务人员 | 定价、成本核算、商业案例分析 |
| **muse** | 创意团队成员 | 头脑风暴、命名建议、创意生成 |
| **scribe** | 写作人员 | 博文撰写、文档编写、长篇内容创作 |
| **quill** | 文案撰写专家 | 登陆页设计、销售文案、广告文案撰写 |
| **echo** | 社交媒体专员 | 推文发布、社交媒体内容管理 |
| **sentry** | 质量保证（QA） | 测试、错误验证 |

## **任务命令**

### **任务调度（自动路由）**
```bash
node scripts/colony.mjs dispatch "research best practices for API rate limiting"
```
根据任务关键词自动选择最合适的智能体来执行任务。

### **分配给特定智能体**
```bash
node scripts/colony.mjs assign scout "find top 5 time-series databases"
node scripts/colony.mjs assign pincer "refactor the auth module to use JWT"
node scripts/colony.mjs assign shell "deploy the staging branch"
```

### **检查状态**
```bash
node scripts/colony.mjs status
```
显示所有智能体及其当前任务。

### **获取结果**
```bash
node scripts/colony.mjs results              # Latest completed task
node scripts/colony.mjs results abc123       # Specific task by ID
```

### **查看历史记录**
```bash
node scripts/colony.mjs history              # Last 10 completed/failed
node scripts/colony.mjs history --limit 20   # Custom limit
```

## **流程命令**

流程是由多个阶段组成的工作流，这些阶段通过智能体相互连接。

### **列出可用流程**
```bash
node scripts/colony.mjs processes
```

### **启动流程**
```bash
node scripts/colony.mjs process <process-name> --context "description"
```

### **检查流程状态**
```bash
node scripts/colony.mjs process-status           # Show latest run
node scripts/colony.mjs process-status abc123    # Specific run
```

显示流程的当前阶段、已完成阶段、检查点以及输出文件。

### **批准检查点**
当流程到达检查点时，会暂停以等待人工审批：
```bash
node scripts/colony.mjs approve abc123
```

该命令也可用于重试失败的阶段。

### **取消流程**
```bash
node scripts/colony.mjs cancel abc123
```

## **审计命令**

跟踪智能体性能、任务统计数据和系统健康状况。

### **仪表盘**
```bash
node scripts/colony.mjs audit
```
显示全局统计数据、各智能体的详细信息以及近期事件。

### **智能体详情**
```bash
node scripts/colony.mjs audit agent scout
node scripts/colony.mjs audit agent pincer
```
显示特定智能体的详细信息，包括：
- 总任务数、成功率
- 平均处理时间
- 令牌使用情况
- 最近的失败记录

### **事件日志**
```bash
node scripts/colony.mjs audit log              # Last 20 events
node scripts/colony.mjs audit log --limit 50   # More events
```

### **最慢的任务**
```bash
node scripts/colony.mjs audit slow             # Top 10 slowest
node scripts/colony.mjs audit slow --limit 20
```

### **最近的失败记录**
```bash
node scripts/colony.mjs audit failures         # Last 10 failures
node scripts/colony.mjs audit failures --limit 20
```

## **学习命令**

智能体通过经验学习并分享知识。

### **提供反馈**
为已完成的任务记录反馈：
```bash
node scripts/colony.mjs feedback abc123 "Great research, but needed more pricing data"
```

### **智能体记忆**
每个智能体都拥有一个持久化的记忆文件，用于存储学习到的经验：

```bash
# View an agent's memory
node scripts/colony.mjs memory scout

# Add a lesson
node scripts/colony.mjs memory scout add "Always check publication dates on research sources"

# Add to specific sections
node scripts/colony.mjs memory scout add "Use bullet points for clarity" --pattern
node scripts/colony.mjs memory scout add "Missed competitor X in analysis" --mistake
node scripts/colony.mjs memory scout add "Prefers markdown tables over lists" --pref
```

### **共享学习成果**
智能体之间可以交流学习心得：

```bash
# View all shared learnings
node scripts/colony.mjs learn

# Add a learning
node scripts/colony.mjs learn add "validate-idea works better with 3 competitors max" --category process
node scripts/colony.mjs learn add "Always verify API rate limits early" --category technical --source run-abc123
```

### **全局上下文**
所有智能体都可以访问共享的上下文信息：

```bash
# View global context
node scripts/colony.mjs context

# Set preferences
node scripts/colony.mjs context set preferences.codeStyle "TypeScript, functional"
node scripts/colony.mjs context set preferences.timezone "America/Chicago"

# Add active facts (temporary context)
node scripts/colony.mjs context add-fact "We're targeting enterprise customers"
node scripts/colony.mjs context add-fact "Launch deadline is Q2 2024"

# Add decisions
node scripts/colony.mjs context add-decision "Use Postgres over MySQL" --project "life-lunch"

# Add projects
node scripts/colony.mjs context add-project "life-lunch"
```

### **回顾性分析**
回顾近期活动并生成分析报告：

```bash
node scripts/colony.mjs retro              # Last 7 days
node scripts/colony.mjs retro --days 14    # Last 14 days
```

显示以下内容：
- 任务完成总结
- 各智能体的统计信息
- 失败模式
- 建议的学习内容

## **可用流程**

### **validate-idea**  
**端到端验证商业想法**  
- 阶段：头脑风暴 → 研究 → 分析 → 规格制定 → 估算  
- 检查点：分析阶段结束后  
- 输出：business-case.md  

### **product-launch**  
**端到端产品发布**  
- 阶段：研究 → 规格制定 → 开发 → 文案编写  
- 检查点：规格制定阶段结束后、文案编写阶段结束后  
- 输出：market-brief.md, prd.md, code/, landing-copy.md  

### **content-pipeline**  
**内容研究、撰写、发布、推广**  
- 阶段：研究 → 草稿撰写 → 审核 → 发布 → 推广  
- 检查点：审核阶段（人工审核草稿）  
- 输出：research.md, draft.md, social-posts.md  

### **bug-triage**  
**重现问题、修复错误、部署修复方案**  
- 阶段：问题重现 → 修复 → 测试 → 部署  
- 检查点：无（快速流程）  
- 输出：bug-report.md, fix-summary.md  

### **customer-research**  
**深入研究客户群体**  
- 阶段：客户群体识别 → 痛点分析 → 结果整合  
- 检查点：无  
- 输出：customer-profile.md, insights.md  

### **landing-page**  
**创建完整的登录页**  
- 阶段：策略制定 → 文案编写 → 审核 → 页面开发  
- 检查点：文案审核阶段结束后  
- 输出：strategy.md, copy.md, landing.html, landing.css  

## **流程工作原理**

1. **启动**：流程创建一个运行记录，并启动第一个阶段的智能体。  
2. **执行**：每个阶段根据前一个阶段的输出结果进行运行。  
3. **检查点**：如果某个阶段是检查点，流程会暂停以等待人工审批。  
4. **继续**：获得审批后，进入下一个阶段。  
5. **完成**：所有阶段完成后，输出结果将保存在 `colony/context/<run-id/>` 目录下。  

### **上下文传递**

- 任务模板中的 `{context}` 会被替换为实际的 `--context` 参数值。  
- 各阶段的输出结果会被保存在 `colony/context/<run-id>/<output-file>` 目录下。  
- 下一个阶段会从前一个阶段的输出文件中读取输入数据。  
- 智能体的记忆信息和全局上下文会被纳入其工作流程中。  
- 完整的任务历史记录保存在 `tasks.json` 文件中。  

### **并行阶段**

具有相同 `parallel_group` 的阶段会同时执行：  
```yaml
stages:
  - id: spec
    agent: forge
    inputs: [analysis.md]
    parallel_group: "final"  # Stages with same group run together
    
  - id: estimate
    agent: ledger
    inputs: [analysis.md]
    parallel_group: "final"  # Same group = parallel execution
```

当流程遇到并行阶段时：
1. 所有属于同一 `parallel_group` 的阶段会同时启动。  
2. 使用 `Promise.all()` 确保所有并行阶段同时完成。  
3. 如果有任何阶段失败，整个流程都会失败。  
4. 检查点的处理是按组进行的（所有并行阶段完成后才会继续执行）。  

**使用并行阶段的场景：**  
- 需要读取相同输入数据的阶段（彼此之间没有依赖关系）。  
- 开发和文案编写任务（都依赖于规格制定阶段，但彼此之间没有依赖关系）。  
- 对相同数据的多次分析。  
- 独立的调研任务。  

**示例流程：**  
- `validate-idea`：规格制定和估算阶段会并行执行。  
- `product-launch`：开发和文案编写阶段会并行执行。  

### **通知**  
当流程到达检查点、完成或失败时，系统会发送通知。通知通过 `openclaw cron wake` 功能发送。  

**配置**（`colony/config.yaml`）：  
```yaml
notifications:
  enabled: true         # Master switch for all notifications
  on_checkpoint: true   # Notify when process pauses at checkpoint
  on_complete: true     # Notify when process finishes
  on_failure: true      # Notify when process/stage fails
```  

**通过 CLI 进行管理：**  
```bash
# View current config
node scripts/colony.mjs config

# Disable all notifications
node scripts/colony.mjs config set notifications.enabled false

# Enable only failure notifications
node scripts/colony.mjs config set notifications.on_checkpoint false
node scripts/colony.mjs config set notifications.on_complete false
node scripts/colony.mjs config set notifications.on_failure true
```  

**通知示例：**  
- 🛑 `Colony checkpoint: Process "validate-idea" 已在 "analyze" 阶段暂停。要继续，请输入：colony approve abc123`  
- ✅ `Colony complete: Process "validate-idea" 已在 120 秒内完成。运行 ID：abc123`  
- ❌ `Colony failed: Process "validate-idea" 在 "research" 阶段失败。错误原因：智能体超时。运行 ID：abc123`  

### **检查点**  
检查点会暂停流程以等待人工审核。有两种定义方式：  
1. 在流程的 `checkpoints` 数组中设置（该阶段完成后触发）。  
2. 作为独立的阶段设置 `checkpoint: true`（仅需要人工审核）。  

## **文件结构**  
```
skills/colony/
├── SKILL.md              # This file
├── package.json          # Dependencies (js-yaml)
├── colony/
│   ├── agents.yaml       # Agent definitions
│   ├── processes.yaml    # Process definitions
│   ├── config.yaml       # Notification & behavior config
│   ├── tasks.json        # Task queue and history
│   ├── runs.json         # Process run tracking
│   ├── feedback.json     # Task feedback storage
│   ├── learnings.yaml    # Shared cross-agent learnings
│   ├── global-context.json  # Shared context for all agents
│   ├── audit/
│   │   ├── log.jsonl     # Append-only event log
│   │   ├── global.json   # Aggregate statistics
│   │   └── agents/       # Per-agent statistics
│   │       ├── scout.json
│   │       ├── pincer.json
│   │       └── ...
│   ├── memory/           # Per-agent persistent memory
│   │   ├── scout.md
│   │   ├── pincer.md
│   │   └── ...
│   └── context/          # Per-task and per-run outputs
│       └── <run-id>/
└── scripts/
    ├── colony.mjs         # Main CLI
    ├── colony-worker.mjs  # Background agent executor
    ├── agent-wrapper.mjs # Task lifecycle utilities
    ├── audit.mjs         # Audit system functions
    └── learning.mjs      # Learning system functions
```  

## **审计日志**  
审计日志记录以下事件：  
| 事件 | 字段 |  
|-------|--------|  
| `task_started` | taskId, agent, processRunId?, stage? |  
| `task_completed` | taskId, agent, durationMs, tokens, success |  
| `task_failed` | taskId, agent, durationMs, error |  
| `checkpoint_waiting` | runId, stage |  
| `checkpoint_approved` | runId, stage |  
| `checkpoint_rejected` | runId, stage, reason |  
| `process_started` | runId, processId, context |  
| `process_completed` | runId, processId, durationMs |  
| `feedback_received` | taskId, agent, feedback |  

## **自定义设置**  

### **添加新智能体**  
编辑 `colony/agents.yaml` 文件：  
```yaml
agents:
  myagent:
    role: specialist
    description: >
      What this agent does...
    model: anthropic/claude-sonnet-4
    triggers:
      - keyword1
      - keyword2
```  
添加新智能体后，需要为其创建对应的记忆文件：  
```bash
touch colony/memory/myagent.md
```  

### **添加新流程**  
编辑 `colony/processes.yaml` 文件：  
```yaml
processes:
  my-process:
    description: "What this process does"
    triggers: [keyword1, keyword2]
    stages:
      - id: stage1
        agent: scout
        task: "Do something with: {context}"
        outputs: [output1.md]
      - id: stage2
        agent: pincer
        task: "Next step based on previous"
        inputs: [output1.md]
        outputs: [output2.md]
    checkpoints: [stage1]  # Optional: pause after these stages
```  

## **集成**  
该系统可与 OpenClaw 的智能体会话集成。  
- **任务调度/分配（异步）**：任务在后台启动，CLI 会立即返回结果。可以使用 `colony status` 命令监控进度，使用 `colony results <task-id>` 查看输出结果。  
- **流程阶段（阻塞式执行）**：多阶段流程按顺序执行，每个阶段完成后才会进入下一个阶段。这样可以确保数据在各阶段之间正确传递，并正确处理检查点。  

每个智能体会收到以下信息：  
- 自己的角色描述  
- 来自记忆文件的学到的经验  
- 全局上下文中的相关信息  
- 项目相关的背景信息  

## **示例**  

### **验证创业想法**  
```bash
node scripts/colony.mjs process validate-idea \
  --context "Subscription box for home coffee brewing experiments"
```  
流程流程如下：头脑风暴 → 研究 → 分析 → （检查点） → 规格制定 → 估算  

### **撰写并发布博客文章**  
```bash
node scripts/colony.mjs process content-pipeline \
  --context "Why RAG is eating traditional search"
```  
流程步骤：研究 → 草稿撰写 → （人工审核） → 发布 → 推广  

### **快速研究任务**  
```bash
node scripts/colony.mjs dispatch "compare Pinecone vs Weaviate vs Milvus"
```  
任务会自动分配给 `scout` 智能体执行，并返回研究结果。  

### **跟踪智能体性能**  
```bash
# After several tasks, check overall health
node scripts/colony.mjs audit

# Deep dive into a struggling agent
node scripts/colony.mjs audit agent pincer
node scripts/colony.mjs audit failures

# Add learnings from issues
node scripts/colony.mjs memory pincer add "Handle file not found errors gracefully" --mistake
```