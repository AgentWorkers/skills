---
name: increment-work-router
description: 智能工作延续系统：能够识别开发者的实施意图，并进行相应的任务分配。当用户执行“实现X功能”、“继续工作”、“开发新特性”或“恢复当前开发任务”等操作时，该系统会自动检测当前正在进行的开发任务（increment），判断其相关性，并根据测试驱动开发（TDD）模式将用户请求路由到相应的任务页面（/sw:do 或 /sw:increment）。
---

# 增量工作路由器 - 智能工作延续系统

## 目的

增量工作路由器（Increment Work Router）是一种智能的工作延续系统，它能够：
- ✅ 检测用户的实施/延续意图（而不仅仅是新项目的启动）
- ✅ 自动检查是否有正在进行的增量任务
- ✅ 将用户请求路由到现有的增量任务中，或创建新的增量任务
- ✅ 搭建计划与执行之间的桥梁

**核心理念**：当用户表示“实施某个功能”或“完成某个任务”时，系统应能够自动进行智能路由，而无需用户手动下达命令。

## 何时激活

当用户表现出**实施/延续工作的意图**时，该系统会被激活：

### 高置信度触发条件（自动路由）

**具体动作动词**：
- “实施 [功能]”
- “完成 [任务]”
- “构建 [组件]”
- “添加 [功能]”
- “开发 [模块]”
- “创建 [功能]”

**表示延续工作的短语**：
- “继续处理 [功能]”
- “继续 [当前任务]”
- “完成 [工作]”
- “我们来实现 [X] 吧”
- “我们来构建 [Y] 吧”
- “开始处理 [Z] 吧”

**表示修复问题的短语**：
- “修复 [问题]”
- “解决 [漏洞]”
- “处理 [故障]”

### 中等置信度触发条件（需要进一步确认）

**意图不明确**（需要明确具体目标）：
- “我们继续吧”
- “继续工作”
- “接下来该做什么？”
- “从哪里继续？”

### 不应激活的情况

- **规划/讨论阶段**：此时应使用其他技能，例如 **增量规划器**（increment-planner）：
  - “我们应该构建什么？”
  - “X 是如何工作的？”
  - “我们应该使用 Y 吗？”
  - “规划一个新功能”

**系统已处于工作流程中**的情况**：
  - 用户已经在执行 `/sw:do` 命令
  - 增量任务的规划正在进行中
  - 有其他技能正在处理用户的请求

## 核心算法

### 第一步：检测意图

扫描用户消息，寻找与实施相关的关键词：
```
Action verbs: implement, complete, build, add, develop, create
Continuation: work on, continue, resume, finish, start
Bug/Fix: fix, resolve, address
```

**计算置信度**：
- **高置信度（>80%）**：包含具体的目标动作动词（如“实施用户认证”）
- **中等置信度（50-80%）**：仅包含动作动词（如“我们继续吧”）
- **低置信度（<50%）**：意图不明确

### 第二步：检查是否有正在进行的增量任务

**读取增量任务的状态**：
```bash
# Find all increments with status = "active"
find .specweave/increments -name "metadata.json" -type f \
  -exec jq -r 'select(.status == "active") | .id' {} \;
```

**三种情况**：
1. **只有一个正在进行的增量任务** → 检查请求的相关性并决定路由方式
2. **有多个正在进行的增量任务** → 请求用户选择继续处理哪个任务
3. **没有正在进行的增量任务** → 建议创建新的增量任务

### 第三步：检查相关性（如果存在正在进行的增量任务）

**相关性分析**：
- 将用户的请求与现有的增量任务进行对比：
  - 检查增量任务的标题/描述
  - 查看任务列表（tasks.md）
  - 查看规范文档（spec.md）中是否存在相关功能

**评分标准**：
- **高度匹配（>70%）**：请求与现有增量任务属于同一功能领域 → 自动继续执行
- **中等匹配（40-70%）**：请求与现有增量任务属于相关领域 → 请求用户确认
- **低度匹配（<40%）**：请求与现有增量任务无关 → 建议创建新的增量任务

### 第四步：智能路由

**情况一：请求与正在进行的增量任务高度相关**
```
User: "Implement user authentication"
Active: 0031-user-authentication-system

✅ High match → Auto-resume:

"I see you have an active increment for user authentication (0031).
Resuming work on that increment now with /sw:do..."

[Automatically invokes /sw:do]
```

**情况二：请求与正在进行的增量任务无关**
```
User: "Implement payment processing"
Active: 0031-user-authentication-system

⚠️  Low match → Ask:

"I see you have an active increment (0031-user-authentication-system).

Your request for payment processing seems unrelated. Would you like to:
1. **Create new increment** for payment processing (recommended)
2. **Continue current increment** (0031) and add payment to it
3. **Pause current** and create new increment

What would you prefer?"
```

**情况三：没有正在进行的增量任务**
```
User: "Implement user authentication"
Active: None

→ Suggest new increment:

"No active increment found. Let's create one for user authentication.

I'm going to create a SpecWeave increment with:
- Specification (WHAT & WHY)
- Technical plan (HOW)
- Task breakdown (STEPS with embedded tests)

Creating increment now with /sw:increment..."

[Automatically invokes /sw:increment "user authentication"]
```

**情况四：存在多个正在进行的增量任务**
```
User: "Continue working"
Active: 0031-user-auth, 0032-payment-system

→ Ask to clarify:

"You have 2 active increments:
1. **0031-user-authentication-system** (3/10 tasks complete)
2. **0032-payment-processing** (1/8 tasks complete)

Which one would you like to work on?"
```

**情况五：意图不明确**
```
User: "Let's continue"
Active: 0031-user-authentication-system

✅ Auto-resume (only one active):

"Resuming increment 0031-user-authentication-system...
Progress: 3/10 tasks complete (30%)

Next task: T-004 Implement password hashing

[Automatically invokes /sw:do]"
```

## 集成架构

**工作流程**：
```
User: "Implement [feature]"
        ↓
increment-work-router (detects intent)
        ↓
[Check .specweave/increments/*/metadata.json]
        ↓
┌───────────────────┬──────────────────┬────────────────┐
│ Active increment  │ Multiple active  │ No active      │
│ (relevant)        │ (ambiguous)      │ (none)         │
└─────┬─────────────┴──────┬───────────┴──────┬─────────┘
      │                    │                  │
      ↓                    ↓                  ↓
/sw:do        Ask to select    /sw:increment
(auto-resume)        (clarify)        (create new)
```

**调用的接口**：
- `/sw:do` - 继续执行现有的增量任务
- `/sw:increment` - 创建新的增量任务
- `/sw:status` - 检查增量任务的状态（如有需要）
- `/sw:tdd-cycle` - 在启用 TDD（测试驱动开发）模式时使用

**被调用的接口**：
- 在检测到实施意图时自动调用
- 与 **增量规划器**（increment-planner）和 **检测器**（detector）协同工作

## TDD 意识下的路由规则（至关重要）

**在路由到正在进行的增量任务时，首先检查 TDD 模式**：
```bash
# Check if increment uses TDD
CONFIG_PATH=".specweave/config.json"
METADATA_PATH=".specweave/increments/<id>/metadata.json"

# Check global config
TDD_MODE=$(cat "$CONFIG_PATH" | jq -r '.testing.defaultTestMode // "test-after"')

# Check increment-specific override
INCREMENT_TDD=$(cat "$METADATA_PATH" | jq -r '.testMode // ""')
[[ -n "$INCREMENT_TDD" ]] && TDD_MODE="$INCREMENT_TDD"
```

**如果启用了 TDD 模式，调整路由行为**：

| 情况 | 未启用 TDD | 启用了 TDD |
|---------|-------------|----------|
| “实施 X”（新功能） | → 直接执行 `/sw:do` | → 先建议执行 `/sw:tdd-cycle` |
| “我们继续吧” | → 直接执行 `/sw:do` | → 显示 TDD 阶段提示 |
| “为 X 添加测试用例” | → 直接执行 `/sw:do` | → 确认是否已进入测试阶段（RED 阶段） |
| “修复实现代码” | → 直接执行 `/sw:do` | → 检查是否已完成测试阶段（GREEN 阶段） |

**TDD 意识下的继续执行结果**：
```
✅ Resuming increment 0031-user-authentication-system...

🔴 TDD MODE ACTIVE

Current TDD Status:
├─ T-001: [RED] Write login test ✅ completed
├─ T-002: [GREEN] Implement login ⏳ in progress
└─ T-003: [REFACTOR] Clean up login ⏸️ blocked (waiting for GREEN)

Current Phase: 🟢 GREEN - Making test pass

💡 You're in the GREEN phase. Implement just enough to make T-001's test pass.
   After GREEN completes, you can proceed to REFACTOR.

[Proceeding with /sw:do...]
```

**针对新工作的 TDD 工作流程建议**：
```
User: "Implement user registration"

🔴 TDD MODE DETECTED

This increment uses Test-Driven Development.

For new features, I recommend using the TDD workflow:
1. /sw:tdd-red "user registration" - Write failing test first
2. /sw:tdd-green - Implement to pass the test
3. /sw:tdd-refactor - Clean up the code

Would you like to:
1. Start TDD cycle (/sw:tdd-cycle) - Recommended
2. Continue with regular /sw:do - Skip TDD guidance

[1/2]:
```

## 决策矩阵

| 用户意图 | 正在进行的增量任务数量 | 任务相关性 | 应采取的动作 |
|-------------|------------------|-----------|--------|
| “实施用户认证” | 1（与认证相关） | 高度相关（>70%） | 自动执行 `/sw:do` |
| “实施用户认证” | 1（无关） | 低度相关（<40%） | 询问用户：是创建新任务还是添加到现有任务中？ |
| “实施用户认证” | 0 | 无关 | 自动执行 `/sw:increment` |
| “实施用户认证” | 多于 1 个增量任务 | 无关 | 询问用户希望继续处理哪个增量任务 |
| “我们继续吧” | 1 | 无关 | 自动执行 `/sw:do` |
| “我们继续吧” | 多于 1 个增量任务 | 无关 | 询问用户希望继续处理哪个增量任务 |
| “我们继续吧” | 0 | 无正在进行的增量任务 | 询问用户应该构建什么？ |

## 相关性判断逻辑

**如何判断请求与正在进行的增量任务是否相关**：
```typescript
function calculateRelevance(userRequest: string, increment: Increment): number {
  let score = 0;

  // 1. Title/ID match (strongest signal)
  if (increment.title.toLowerCase().includes(extractKeywords(userRequest))) {
    score += 40;
  }

  // 2. Tasks match (check tasks.md)
  const tasks = readTasksFile(increment);
  const matchingTasks = tasks.filter(t =>
    t.title.toLowerCase().includes(extractKeywords(userRequest))
  );
  score += (matchingTasks.length / tasks.length) * 30;

  // 3. Spec match (check spec.md user stories)
  const spec = readSpecFile(increment);
  if (spec.includes(extractKeywords(userRequest))) {
    score += 20;
  }

  // 4. Type match (feature vs bug vs hotfix)
  const requestType = detectType(userRequest);
  if (requestType === increment.type) {
    score += 10;
  }

  return score; // 0-100
}
```

**示例**：
```
User: "Implement JWT token refresh"
Active: 0031-user-authentication-system

Checks:
✅ Title contains "authentication" (user mentions "JWT token") → +40 points
✅ Tasks.md has "T-005: Implement JWT refresh logic" → +30 points
✅ Spec.md mentions "token management" → +20 points
✅ Both are "feature" type → +10 points

Total: 100/100 → High relevance → Auto-resume
```

## 示例

### 示例 1：自动继续执行（高度相关）

**场景**：
```
Active: 0031-user-authentication-system
Progress: 3/10 tasks complete
```

**用户**：
```
Implement JWT token refresh
```

**增量工作路由器**：
```
✅ Intent detected: "implement" + specific target
✅ Active increment found: 0031-user-authentication-system
✅ Relevance check: 95% match (authentication-related)

→ AUTO-RESUME

"I see you have an active increment for user authentication (0031).
Task T-005 'Implement JWT token refresh' is already in your plan.

Resuming increment 0031 now with /sw:do...

[Automatically invokes /sw:do]
```

### 示例 2：创建新任务（没有正在进行的增量任务）

**场景**：
```
Active: None
```

**用户**：
```
Implement payment processing with Stripe
```

**增量工作路由器**：
```
✅ Intent detected: "implement" + specific target
❌ No active increment found

→ CREATE NEW

"No active increment found. Let's create one for payment processing.

I'm going to create a SpecWeave increment with:
- Specification (Stripe integration requirements)
- Technical plan (API integration, webhooks, security)
- Task breakdown (implementation steps with tests)

Creating increment now with /sw:increment...

[Automatically invokes /sw:increment "payment processing with Stripe"]
```

### 示例 3：请求与正在进行的任务无关（需要用户确认）

**场景**：
```
Active: 0031-user-authentication-system
Progress: 3/10 tasks complete
```

**用户**：
```
Implement email notifications
```

**增量工作路由器**：
```
✅ Intent detected: "implement" + specific target
✅ Active increment found: 0031-user-authentication-system
⚠️  Relevance check: 15% match (unrelated)

→ ASK FOR CLARIFICATION

"I see you have an active increment (0031-user-authentication-system) with 3/10 tasks complete.

Your request for email notifications seems unrelated. Would you like to:
1. **Create new increment** for email notifications (recommended - keeps work focused)
2. **Add to current increment** (0031) - if notifications are for auth emails
3. **Pause current increment** and start notifications

SpecWeave works best with focused increments. What would you prefer?"
```

### 示例 4：存在多个正在进行的任务（需要用户确认）

**场景**：
```
Active: 0031-user-authentication-system (3/10 tasks)
Active: 0032-payment-processing (1/8 tasks)
```

**用户**：
```
Let's continue working
```

**增量工作路由器**：
```
✅ Intent detected: "continue" (vague)
✅ Multiple active increments found: 2

→ ASK TO SELECT

"You have 2 active increments:

1. **0031-user-authentication-system**
   - Progress: 3/10 tasks (30%)
   - Next: T-004 Implement password hashing

2. **0032-payment-processing**
   - Progress: 1/8 tasks (12%)
   - Next: T-002 Set up Stripe SDK

Which one would you like to work on?"

[Wait for user selection, then invoke /sw:do {selected-id}]
```

### 示例 5：意图不明确（自动继续执行）

**场景**：
```
Active: 0031-user-authentication-system (3/10 tasks)
```

**用户**：
```
What's next?
```

**增量工作路由器**：
```
✅ Intent detected: "what's next" (continuation)
✅ One active increment: 0031-user-authentication-system

→ AUTO-RESUME

"Resuming increment 0031-user-authentication-system...
Progress: 3/10 tasks complete (30%)

Next task: **T-004 Implement password hashing**

[Automatically invokes /sw:do]"
```

## 用户自定义机制

用户可以通过明确指令来覆盖自动路由规则：
- “不要继续执行，创建新任务” → 强制创建新任务
- “先讨论一下” → 保持当前讨论状态
- “先进行规划，不立即执行” → 直接路由到 `/sw:increment` 接口
- “显示当前任务的状态” → 使用 `/sw:status` 接口

## 成功标准

- 用户可以简单地说“实施 X”，系统就能自动开始工作
- 系统能够智能地将请求路由到相关的增量任务中（无需用户手动执行 `/sw:do`）
- 系统能够识别无关的请求，防止工作范围扩大
- 在意图不明确的情况下（如存在多个正在进行的任务或请求与现有任务无关时），系统能提供清晰的选项
- 该系统能与现有的技能（如 **增量规划器**、**检测器**）无缝集成

## 相关技能

- **增量规划器**（increment-planner）：用于创建增量任务的结构（该技能会为新项目调用该规划器）
- **检测器**（detector）：用于检查任务的相关性

---

**关键区别**：
- **增量规划器**（increment-planner）：主要用于规划阶段，例如“计划这个增量任务”或“我想构建一个新产品”
- **增量工作路由器**（increment-work-router）：主要用于执行阶段，例如“实施这个功能/任务”

该系统通过自动检测用户的实施意图，实现了从规划到执行的无缝衔接。