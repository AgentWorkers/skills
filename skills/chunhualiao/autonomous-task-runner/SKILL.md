---
name: task-runner
description: 持久化任务队列系统。用户可以随时通过自然语言添加任务；这些任务会被存储在一个持久的队列文件中，并由子代理异步执行。系统会定期通过心跳/定时器调度器来检查待处理的任务、启动工作进程并报告任务完成情况。该系统永远不会“结束”——它始终处于准备接收新任务的状态。
metadata:
  author: skill-engineer
  version: 2.1.0
  owner: main agent (any agent with access to the full tool suite)
  tier: general
---
# 任务运行器技能

这是一个持久的、以守护进程形式运行的任务队列。用户可以随时添加任务。调度器会在每个心跳周期检查队列，并通过子代理执行待处理的任务。任务会不断累积、完成，然后被归档——队列本身永远不会关闭。

---

## 两种运行模式

该技能具有**两种不同的模式**，它们具有不同的触发条件和行为：

| 模式 | 触发条件 | 目的 |
|------|---------|---------|
| **接收模式** | 包含任务意图的用户消息 | 解析消息 → 将任务添加到队列 → 确认 → **立即运行调度器** |
| **调度模式** | 在接收模式之后（主要方式）· 心跳周期/定时任务（备用方式） | 读取队列 → 分发待处理的任务 → 报告任务完成情况 |

两种模式都会读取和写入**同一个持久性队列文件**。

---

## A1 — 触发条件

### 模式 1：接收模式（用户消息）

当用户的消息符合以下任何模式时，激活接收模式：

| 模式 | 例子 |
|---------|---------|
| 明确添加任务 | "add task", "add these tasks", "task:", "new task" |
| 委派任务 | "do this for me", "do these for me", "handle these", "can you do X" |
| 表达需求 | "I need you to", "help me with", "I need", "I want you to" |
| 列出任务 | "task list", "my tasks", "queue these", "work on these" |
| 控制命令 | "skip T-03", "retry T-02", "mark T-01 done", "cancel T-04" |
| 状态查询 | "show tasks", "task status", "what's in the queue", "what are my pending tasks" |
| 复合请求 | 包含两个以上不同操作项的消息（项目符号、数字、"and also", "then"）

**不要为以下情况激活接收模式：**
- 仅用一句话回答的简单查询（例如：“现在几点了？”）
- 仅用于调度的请求（例如：“20分钟后提醒我”）
- 单纯的网页搜索请求（例如：“在谷歌上搜索X”）
- 心跳系统事件（这属于调度模式）

### 模式 2：调度模式（在接收模式之后立即触发，或通过心跳周期/定时任务触发）

当以下条件满足时，激活调度模式：
- **在接收模式之后立即触发** — 在任务被添加到队列后立即执行
- 在心跳周期检查`HEARTBEAT.md`文件（用于处理重试和完成情况）
- 系统事件：`TASK_RUNNER_DISPATCH: check queue and run pending tasks`（用于处理备用情况）
- 为任务运行器注册的任何定时任务触发器（用于处理备用情况）

---

## 配置

| 变量 | 位置 | 默认值 | 描述 |
|----------|----------|---------|-------------|
| `TASK_RUNNER_DIR` | `TOOLS.md` | `~/.openclaw/tasks/` | 队列文件和输出文件的目录 |
| `TASK_RUNNER_MAX_CONCURRENT` | `TOOLS.md` | `2` | 同时运行的最大任务数 |
| `TASK_RUNNER_MAX_RETRIES` | `TOOLS.md` 或环境变量 | 在标记为阻塞之前允许的最大重试次数 |
| `TASK_RUNNER_ARCHIVE_days` | `TOOLS.md` | 完成或被阻塞的任务被归档的天数 |

**如何配置** — 在`TOOLS.md`文件中进行设置：
```
## Task Runner
TASK_RUNNER_DIR=~/.openclaw/tasks/
TASK_RUNNER_MAX_CONCURRENT=2
TASK_RUNNER_MAX_RETRIES=3
TASK_RUNNER_ARCHIVE_DAYS=7
```

**队列文件路径：** `${TASK_RUNNER_DIR}/task-queue.json`  
（单个持久性文件，不包含日期信息——会随时间累积所有任务）

---

## A3 — 输出结果

| 输出结果 | 路径/渠道 | 描述 |
|--------|---------------|-------------|
| 队列文件 | `${TASK_RUNNER_DIR}/task-queue.json` | 单个持久性队列；包含所有任务 |
| 任务完成通知 | 聊天通知 | 任务完成（已完成或被阻塞）时立即发送 |
| 任务输出文件 | 任务特定路径 | 任务生成的文件（如适用） |
| 接收确认通知 | 聊天 | 任务添加到队列后发送 |

---

## 模式 1：接收模式 — 详细步骤

**目标：** 将用户消息转换为结构化的任务对象，添加到队列中，并向用户确认。

### 第 0 步 — 首次运行时的自动配置

在每次接收请求之前，先运行以下检查：
```
CHECK whether ${TASK_RUNNER_DIR}/task-queue.json exists
IF file does NOT exist:
  → This is the first run. Auto-configure everything silently before proceeding.

  [1] Create directory:
      exec: mkdir -p ${TASK_RUNNER_DIR}

  [2] Initialize queue file:
      WRITE ${TASK_RUNNER_DIR}/task-queue.json with default structure:
      { "lastId": null, "tasks": [], "archivedCount": 0 }

  [3] Register heartbeat entry:
      READ HEARTBEAT.md (create it if missing)
      IF "Task Runner Dispatcher" is NOT already in the file:
        APPEND the following block (with a blank line before it):

        ## Task Runner Dispatcher
        Every heartbeat: check ${TASK_RUNNER_DIR}/task-queue.json
        - If pending or running tasks exist → run DISPATCHER mode (task-runner skill)
        - If nothing pending → HEARTBEAT_OK (skip)

      WRITE the updated HEARTBEAT.md

  [4] Register backup cron job:
      CALL cron tool with:
        action: "add"
        job:
          name: "Task Runner Dispatcher"
          schedule: { kind: "every", everyMs: 900000 }
          payload: { kind: "systemEvent", text: "TASK_RUNNER_DISPATCH: check queue and run pending tasks" }
          sessionTarget: "main"
          enabled: true

  [5] Notify user:
      "⚙️ Task Runner initialized.
       Heartbeat dispatcher registered in HEARTBEAT.md.
       Backup cron job registered (runs every 15 minutes).
       Your tasks will execute automatically."

  → THEN continue with normal INTAKE steps below.

IF file already exists:
  → Skip Step 0 entirely. Proceed directly to Step 1.
```

**幂等性规则：** 第 0 步仅在首次运行且队列文件不存在时触发。
它不会重复记录心跳事件或创建重复的定时任务。

---

### 第 1 步 — 加载队列

```
READ ${TASK_RUNNER_DIR}/task-queue.json
IF file does not exist:
  Initialize with default structure (see references/queue-schema.md)
  Set lastId = null
```

### 第 2 步 — 从消息中解析任务

使用以下线索将用户消息拆分为单独的任务：
- 带编号的列表（1., 2., 3.）
- 项目符号列表（-，*，•）
- 明确的分隔符（"first", "also", "and then", "next"）
- 包含多个命令的复合句子
- 单个任务：整个消息被视为一个任务

### 第 3 步 — 分配任务ID

从队列文件中的`lastId`开始：
- 如果`lastId = "T-05"`，则下一个任务是`T-06`
- 如果`lastId`为空，则从`T-01`开始
- 格式：`T-NN`（至少两位数字；当N大于99时扩展为三位）

### 第 4 步 — 创建任务对象

对于每个解析出的任务，创建一个JSON对象（详细信息见`references/queue-schema.md`）：
- 设置`id`、`description`、`goal`、`status = "pending"`、`added_at`
- 设置`retries = 0`，`maxRetries`根据配置文件设置
- 执行字段保持为空

### 第 5 步 — 添加到队列并保存

```
APPEND new task objects to queue.tasks[]
UPDATE queue.lastId to the last assigned ID
WRITE updated queue file to disk
```

### 第 6 步 — 向用户确认

```
Added T-06: [description]. Starting now...
```

对于多个任务：
```
📋 Added 3 tasks to queue:
• T-06: [description]
• T-07: [description]
• T-08: [description]
Starting dispatcher now...
```

**然后立即执行调度模式（步骤 1–5）。**  
不要退出，等待下一次心跳周期。任务必须立即开始执行。
心跳周期/定时任务调度器仅用于重试和完成情况的检查，不是主要的执行路径。

### 第 7 步 — 处理控制命令

| 命令 | 动作 |
|---------|--------|
| `skip T-NN` | 将状态设置为“skipped”；保存；确认 |
| `retry T-NN` | 将状态重置为“pending”，`retries`设置为0；保存；确认 |
| `cancel T-NN` | 将状态设置为“skipped”，`blocked_reason`设置为“cancelled by user”；保存；确认 |
| `mark T-NN done` | 将状态设置为“done”，`completed_at`设置为当前时间；保存；确认 |
| `show tasks` / `task status` | 读取队列；生成状态表格（参见A5模板） |

---

## 模式 2：调度模式 — 详细步骤

**目标：** 检查队列，分发待处理的任务，跟踪正在运行的任务，报告完成情况。

### 第 1 步 — 加载队列

```
READ ${TASK_RUNNER_DIR}/task-queue.json
IF file does not exist OR tasks array is empty:
  → HEARTBEAT_OK (silent, nothing to do)
  → EXIT
```

### 第 2 步 — 检查队列中的任务

```
pending_tasks = tasks where status = "pending"
running_tasks = tasks where status = "running"

IF pending_tasks is empty AND running_tasks is empty:
  → HEARTBEAT_OK (silent)
  → EXIT
```

### 第 3 步 — 检查正在运行的任务是否完成

对于状态为“running”的每个任务：

```
IF subagent_session is set:
  CHECK subagent session status

  IF session is DONE:
    READ deliverable from session output
    RUN verification (see references/verification-guide.md)
    IF verification passes:
      SET status = "done"
      SET deliverable, deliverable_path, completed_at
      NOTIFY user: ✅ T-NN done — [summary]
    ELSE (verification failed):
      TREAT as failure (see retry logic below)

  IF session is FAILED or ERROR:
    IF retries < maxRetries:
      INCREMENT retries
      ADD to strategies_tried
      SET status = "pending"  ← will be re-dispatched this cycle
    ELSE:
      SET status = "blocked"
      SET blocked_reason, user_action_required, completed_at
      NOTIFY user: 🚫 T-NN blocked — [reason + unblock steps]

  IF session is STILL RUNNING:
    Leave as-is (will check again next heartbeat)
```

### 第 4 步 — 分发待处理的任务

```
currently_running = count of tasks with status = "running"
slots_available = maxConcurrent - currently_running

FOR EACH pending task (in order of added_at), up to slots_available:
  PICK execution strategy (see references/task-types.md)
  SPAWN subagent with task description and strategy
  SET status = "running"
  SET subagent_session = spawned session ID
  SET started_at = now
```

**子代理指令模板：**
```
You are executing task [T-NN] for the task-runner skill.

Task: [description]
Goal: [goal]
Type: [task_type]
Strategy: [selected strategy from task-types.md]

Execute the task. When complete:
1. Report the result clearly
2. Note any deliverable file path if a file was created
3. If blocked, explain exactly why and what the user needs to do

Do not start any other tasks. Focus only on this one.
```

### 第 5 步 — 保存并退出

```
WRITE updated queue file (status changes, subagent_session IDs)
```

如果发送了任何通知（任务完成/被阻塞），则表示正在进行心跳响应。
如果只是进行了无声的分发操作，这也属于心跳响应（但不是HEARTBEAT_OK）。
只有当确实没有任务需要处理时（没有待处理的任务，也没有正在运行的任务），才返回HEARTBEAT_OK。

---

## A5 — 输出格式模板

### 单个任务的接收确认通知

```
Added T-06: [description]. Queue now has N pending tasks.
```

### 多个任务的接收确认通知

```
📋 Added N tasks to queue:
• T-06: [description]
• T-07: [description]

Starting now...
```

### 任务状态表格（按需显示）

```
📋 Task Queue — [N total, N pending, N running, N done, N blocked]

ID    Status      Description
T-01  ✅ done      [description] → [deliverable summary]
T-02  🔄 running   [description] (started [time ago])
T-03  ⏳ pending   [description]
T-04  🚫 blocked   [description] — [blocked_reason short]
T-05  ⏭️ skipped   [description]
```

### 任务完成通知

```
✅ T-NN done — [one-sentence summary of what was accomplished]
[deliverable: link or file path, if applicable]
```

### 任务被阻塞的通知

```
🚫 T-NN blocked after [N] attempts

What was tried:
- [Strategy 1]: [result]
- [Strategy 2]: [result]

Why it's blocked:
[Clear plain-English explanation]

To unblock:
1. [Concrete step #1]
2. [Concrete step #2 if needed]

Reply "retry T-NN" once ready.
```

### 任务被跳过的通知

```
⏭️ T-NN skipped — as requested.
```

---

## A6 — 心跳周期集成

心跳周期和定时任务的设置是**自动完成的**。接收模式的第 0 步会在首次使用时自动处理这些设置——无需手动配置。

### 心跳周期/定时任务的用途（仅作为备用）

任务在接收模式之后**立即**被分发——心跳周期和定时任务仅作为备用机制。

备用调度器负责：
- **重试分发**：失败后被重置为待处理状态的任务
- **完成检查**：轮询正在运行的子代理会话以获取完成/阻塞状态
- **恢复**：在没有用户消息触发接收模式时仍在等待的任务

用户无需等待心跳周期来处理新添加的任务。

### 自动配置的内容

**HEARTBEAT.md 文件**（在首次接收时生成）：
```markdown
## Task Runner Dispatcher
Every heartbeat: check ${TASK_RUNNER_DIR}/task-queue.json
- If pending or running tasks exist → run DISPATCHER mode (task-runner skill)
- If nothing pending → HEARTBEAT_OK (skip)
```

**备用定时任务**（在首次接收时注册）：
```
every 15 min → systemEvent: "TASK_RUNNER_DISPATCH: check queue and run pending tasks"
sessionTarget: main
```

### 手动配置（如需）

如果自动配置未能成功（例如，队列文件是外部预先创建的），
请删除`${TASK_RUNNER_DIR}/task-queue.json`文件，然后发送任何任务——此时会触发第 0 步。

---

## A7 — 成功标准

### 接收模式成功条件：

1. 用户消息中的所有任务都被解析并分配了ID
2. 任务被添加到队列文件中（文件已保存到磁盘）
3. 向用户发送包含任务ID和数量的确认信息
4. 调度模式在同一周期内立即被触发
5. 在接收周期结束之前，为待处理的任务启动了子代理

### 调度模式成功条件：

1. 读取队列文件时没有错误
2. 检查所有正在运行的任务是否完成（根据需要发送完成/阻塞通知）
3. 将最多`maxConcurrent`个任务分发出去
4. 队列文件已保存，并更新了状态
5. 向用户通知每个达到最终状态的任务

### 系统的持续健康状态：

- 队列文件永远不会损坏（始终是有效的JSON格式）
- 存储时间超过`archiveDays`天的任务会被归档/删除
- `lastId`始终递增（不会重复使用ID）
- 在任何任务被标记为阻塞之前，都会遵守`maxRetries`的限制

---

## 边缘情况

| 情况 | 行为 |
|-----------|---------|
| 队列文件缺失（首次运行） | 运行第 0 步的自动配置：创建目录，初始化队列，注册心跳周期和定时任务；通知用户 |
| 队列文件被手动删除 | 重新触发第 0 步：重新初始化队列；不会重新注册心跳周期/定时任务（幂等检查） |
| 队列文件损坏或JSON格式无效 | 记录错误，通知用户，不要覆盖文件；请用户检查文件 |
| 任务描述不明确 | 将任务类型设置为“unknown”；调度器会尝试分类并采取备用措施 |
| 已达到`maxConcurrent`的最大值 | 调度器跳过分发；在下一次心跳周期再次检查 |
| 在调度器运行时用户添加任务 | 保证安全性：调度器在每个周期内原子性地读取、处理和写入数据 |
| 任务依赖于另一个任务的输出 | 将`blocked_reason`设置为“depends on T-NN-1 which is pending/blocked” |
| 用户请求“retry T-NN” | 将任务状态重置为“pending”，`retries`设置为0，`strategies_tried`设置为空数组 |
| 所有任务都被阻塞 | 通知用户：“所有任务都被阻塞。请查看上述解阻说明。” |
| 一次性添加了20多个任务 | 调度器分批分发任务（每次最多`maxConcurrent`个）；所有任务最终都会被执行 |
| 子代理会话ID丢失 | 将任务状态重新设置为“pending”；在下一次心跳周期重新分发 |
| 完成的任务超过`archiveDays`天 | 将这些任务移动到`${TASK_RUNNER_DIR}/archive/YYYY-MM.json`；从主队列中删除 |

---

## A8 — 文件组织结构

队列文件的格式在`references/queue-schema.md`中有所说明。

---

## 参考资料

- `references/queue-schema.md` — 队列文件的JSON格式规范
- `references/task-types.md` — 任务类型目录和策略选择
- `references/verification-guide.md` — 每种任务类型的验证逻辑
- `tests/test-triggers.json` — 触发测试用例（正面和负面案例）