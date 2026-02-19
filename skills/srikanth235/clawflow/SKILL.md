---
name: clawflow
description: >
  **通过 OpenClaw 的消息传递和递归任务有向无环图（DAG）实现多代理协作的协议**  
  每当用户需要协调多个 OpenClaw 代理之间的工作、将复杂任务分解为具有依赖关系的子任务，或构建任何类型的多代理流水线时，请使用此技能。此外，在用户提到“代理编排”、“任务有向无环图（DAG）”、“多代理”、“任务调度”、“代理流水线”、“任务委托”、“代理协作”，或希望将项目分解为可由不同代理并行处理的步骤时，也应触发该协议。即使用户只是简单地说“我需要多个代理协同工作”，也请使用此协议。
---
# Clawflow

这是一个用于 OpenClaw 代理之间通过消息传递和递归任务有向无环图（DAG）进行协作的协议。

**工作原理**：可以将其想象成一个咨询公司。任何人都可以接收到一个项目。如果他们能够独自完成这个项目，就会直接处理；如果项目规模太大，就会将其分解成若干部分，分别交给同事处理，然后收集各部分的成果并进行综合分析。这些同事也可能采取同样的方式。系统中没有固定的“管理者”和“工作者”角色，所有代理都遵循相同的协议。

## 需要查阅的参考资料

- 消息格式、任务文件结构、状态代码 → `references/schemas.md`
- 每个代理执行的决策流程 → `references/agent-loop.md`
- 有向无环图的分解、上下文传递、结果合成 → `references/coordinating.md`

---

## 核心原则

1. **统一协议，灵活的角色分配**：所有代理在结构上是相同的。任何代理都可以直接执行任务，或者将任务分解并委托给其他代理。代理的角色是由具体任务决定的。
2. **OpenClaw 是核心**：代理的身份信息来自 `openclaw.json` 配置文件，代理之间的发现通过 `openclaw agents list` 实现，消息传输则通过命令 `openclaw agent --agent <id> --message "..."` 完成。系统不支持自定义的代理身份文件或专门用于代理间通信的文件。
3. **递归的有向无环图**：当代理将任务委托给其他代理时，它就成为了该子有向无环图的协调者；其上级代理对此并不知情，也不需要关心。有向无环图可以自然地嵌套使用。
4. **工作空间即工作内存**：每个代理的 OpenClaw 工作空间是它的私有临时存储区域。任务的状态保存在工作空间文件中，任何代理都无法读取其他代理的工作空间内容。

---

## 工作原理（代码示例）

```
Agent A receives a task
  → Can I do this alone?
     YES → Execute, reply with results
     NO  → Decompose into sub-DAG
           → Dispatch subtasks to Agents B, C via openclaw agent
           → Agent B receives its subtask
              → Can I do this alone?
                 YES → Execute, reply to A
                 NO  → Decompose further, dispatch to D, E...
           → Agent C executes, replies to A
           → A collects all replies, synthesises, replies to *its* parent
```

无论处于哪个层级，代理的处理流程都是相同的。所有代理都遵循相同的处理循环。

---

## 与 OpenClaw 的集成

### 代理身份的确定

代理的身份信息来自 OpenClaw 的配置文件。**禁止**创建自定义的身份文件。

- **配置来源**：`openclaw.json`（其中包含 `agents.list[].id` 和 `agents.list[].identity`）
- **工作空间来源**：代理工作空间根目录下的 `IDENTITY.md` 文件
- **获取方式**：通过 `openclaw agents list` 或者从启动时注入的上下文信息中获取

每个代理都清楚自己的身份信息（`id`、`name`、`emoji` 和 `theme`），这些信息会通过工作空间启动文件（`IDENTITY.md`、`SOUL.md`、`AGENTS.md`）在每次会话开始时被注入到会话上下文中。

### 代理间的发现

代理可以从 OpenClaw 的配置文件中获取其他可用的代理信息。**禁止**维护单独的代理列表文件。

```bash
# List all configured agents
openclaw agents list

# The config defines them:
# agents.list[].id        → agent identifier (used in --agent flag)
# agents.list[].workspace → their workspace path
# agents.list[].model     → their model
```

代理的 `subagents.allowAgents` 配置决定了它可以委托给哪些代理。`["*"]` 表示它可以委托给任何代理。

### 向其他代理发送任务

使用 OpenClaw 的命令行界面（CLI）向其他代理发送任务消息：

```bash
# Send a task to a specific agent
openclaw agent --agent data-extractor --message "Extract Q3 sales from sales.csv"

# The receiving agent gets this in its session, processes it,
# and the response comes back through the same mechanism
```

对于需要元数据的结构化任务调度，需要将任务信息写入文件并进行引用：

```bash
openclaw agent --agent data-extractor \
  --message "$(cat workspace/tasks/task-abc/dispatch-st-extract.md)"
```

### Clawflow 的工作空间布局

每个代理使用其原有的 OpenClaw 工作空间。Clawflow 会在工作空间中添加一个 `tasks/` 目录：

```
<agent-workspace>/                   ← OpenClaw workspace root
  IDENTITY.md                        ← Agent identity (OpenClaw-managed)
  AGENTS.md                          ← Operating instructions (OpenClaw-managed)
  SOUL.md                            ← Persona (OpenClaw-managed)
  mailbox/                           ← Agent-level message log (all tasks)
    inbox/                           ← Incoming messages before processing
    outbox/                          ← Outgoing messages (dispatches + replies sent)
    archive/                         ← Processed messages (durable audit trail)
  tasks/                             ← Clawflow working directory
    {task-id}/
      task.md                        ← DAG definition + progress + results
  skills/
    clawflow/                        ← This skill
      SKILL.md
      ...
```

Clawflow 会在工作空间中添加两个顶级目录：

- **`mailbox/`：用于存储代理级别的消息日志，与具体任务无关。代理发送或接收的所有消息都会被记录在这里。`inbox/` 存储未处理的消息，`outbox/` 存储已发送的消息，`archive/` 存储已处理的消息。这是一个持久性的审计记录；OpenClaw 会话历史会随着时间被压缩，但 `mailbox` 中的消息会一直保留。
- **`tasks/`：每个任务都有一个子目录，其中包含 `task.md` 文件，用于记录任务的状态、子任务的结果以及最终的综合输出。

---

## 代理的工作流程

当代理接收到一个任务时（通过命令 `openclaw agent --message`）：

```
1. Parse the message
2. Is it a TASK from a parent?
   → Create task.md in workspace/tasks/{task-id}/
   → DECIDE: execute directly or decompose?
     → Direct: do the work, reply with results
     → Decompose: build sub-DAG in task.md, dispatch subtasks via openclaw agent
3. Is it a REPLY from a peer I delegated to?
   → Update sub-DAG in task.md (mark subtask done, store results)
   → Dispatch any newly unblocked subtasks
   → If all subtasks done → synthesise results, reply to parent
```

请参考 `references/agent-loop.md` 以了解完整的决策逻辑和特殊情况处理方式。

---

## 任务委托决策

当代理收到一个任务时，需要决定是自行处理还是委托给其他代理：

- **直接执行的情况**：
  - 任务在代理的能力范围内；
  - 任务简单到分解任务会增加额外的开销；
  - 系统中没有可用的代理来协助处理。

- **分解并委托的情况**：
  - 任务需要代理不具备的能力；
  - 任务具有可以并行处理的子任务；
  - 任务规模较大，分解任务可以降低处理难度。

这个决策完全由代理自行判断，协议并不强制规定必须采取某种方式。

---

## 有向无环图的依赖关系处理

在协调子任务时，代理会通过 `task.md` 文件跟踪子任务的状态：

```python
def get_ready_subtasks(dag):
    """Subtasks whose dependencies are all done and haven't been dispatched yet."""
    return [
        sid for sid, st in dag.subtasks.items()
        if st.status == 'pending'
        and all(dag.subtasks[dep].status == 'done' for dep in st.depends_on)
    ]
```

每当有新的子任务完成处理后，系统会立即重新调度这些子任务。

---

## 错误处理（版本 1）

系统采用“快速失败”策略：不支持重试，也无法部分恢复任务状态。

| 错误类型 | 处理方式 |
|---|---|
| 对方代理未能完成子任务 | 代理会标记自己的任务为失败，并向上级代理发送错误信息 |
| 接收到重复的消息 | 系统会检查任务是否已经在进行中或已经完成，如果是，则忽略该消息 |
| 代理崩溃 | 代理的工作空间中的任务文件会保留任务状态；重启后系统会从 `task.md` 文件中恢复任务状态 |

错误会向上层代理传播。未来的版本将添加重试机制和部分任务恢复的功能。

---

## 实现检查清单

1. **验证代理配置**：使用 `openclaw agents list` 确认可用的代理列表。
2. **检查代理的权限设置**：确保 `subagents.allowAgents` 中包含目标代理的名称。
3. **实现代理的决策逻辑**：遵循 `references/agent-loop.md` 中的流程。
4. **使用消息模板**：`scripts/message.py` 负责生成结构化的任务/回复消息。
5. **测试两级任务链**：代理 A 委托任务给代理 B，B 执行任务并回复结果。
6. **测试并行处理**：代理 A 同时委托任务给代理 B 和 C。
7. **测试递归处理**：代理 A → B → C 的任务流程。

---

## 不在本次文档范围内的内容（版本 1）

- 大型结果的存储（例如使用 Google Drive）
- 任务的重试机制或部分任务的恢复
- 代理的健康检查
- 进度信息的实时推送
- 跨代理的工作空间访问（根据设计，该功能是永久支持的）