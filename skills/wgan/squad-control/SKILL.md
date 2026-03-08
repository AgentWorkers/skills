---
name: squad-control
version: 1.3.0
homepage: https://squadcontrol.ai
env:
  SC_API_URL:
    description: Base URL of your Squad Control instance (e.g. https://www.squadcontrol.ai)
    required: true
  SC_API_KEY:
    description: >
      API key from Squad Control Settings → API Keys. Can be workspace-scoped (single workspace)
      or account-scoped (all workspaces). Account-scoped keys are recommended for multi-workspace
      setups — tasks will include an embedded workspace object with all config needed.
    required: true
  GITHUB_TOKEN:
    description: >
      GitHub Personal Access Token for PR creation and repo cloning.
      When not set manually, the skill uses the token returned by the Squad Control API
      (workspace.githubToken) — configured in Squad Control Settings → Project Repository.
    required: false
  SC_REVIEWER_AGENT_ID:
    description: Optional explicit reviewer agent id. If set, review routing uses this id first.
    required: false
  SC_DEFAULT_BRANCH:
    description: Optional default git base branch override (fallback: workspace default branch, then main).
    required: false
description: >
  Integrate with Squad Control kanban for AI agent task orchestration.

  ⚠️ Security note: This skill handles GitHub tokens and API keys by design — it clones
  private repos, pushes code, and creates PRs on your behalf. Review setup.md for security
  guidance before installing. Only connect to Squad Control instances you trust.

  Use when:
  - A cron fires to check for pending tasks
  - You need to pick up, dispatch, or complete a kanban task
  - You need to create a PR and route it for code review
  - You need to spawn a sub-agent to work on an assigned task
  - You need to report task success or failure back to Squad Control
  - You need to create tasks programmatically (break down work)

  Don't use when:
  - The user is asking a general question (just answer directly)
  - You're doing work that isn't tracked in Squad Control
  - You're working inside a sub-agent session (you're already dispatched — just do the work)
  - The user wants to manage agents/settings in the UI (direct them to squadcontrol.ai)

  Inputs: Squad Control API credentials, task data from /api/tasks/pending
  Outputs: PRs on GitHub, task status updates in Squad Control, review verdicts
---

# 队伍控制集成

从队伍控制的看板中协调AI代理任务。

## 快速参考
- **设置：`references/setup.md`
- **完整API文档：`references/api.md`
- **PR模板：`references/pr-template.md`
- **审查检查表：`references/review-checklist.md`
- **投票结果格式：`references/poll-result.schema.json`
- **迁移说明：`references/migration-notes.md`
- **唤醒监听器：`scripts/wake-listener.sh`

所需环境变量：`SC_API_URL`、`SC_API_KEY`

---

## 任务轮询流程

当cron触发检查任务时：

1. 运行`~/.openclaw/skills/squad-control/scripts/poll-tasks.sh`（需要`SC_API_URL`和`SC_API_KEY`环境变量）
   - 该脚本支持多工作空间：它不会导出顶层的`REPO_URL`/`GITHUB_TOKEN`；而是根据`task_workspace`（或对于旧版本的数据，使用顶层工作空间）为每个任务解析仓库/令牌。
   - 脚本通过锁定/租用机制来防止任务重叠（过期的锁定会自动失效）。
   - 脚本在API调用时使用重试/退避/超时机制。
2. 如果输出为`HEARTBEAT_OK` → 表示没有任务需要处理，停止轮询。
3. 如果输出包含`POLL_RESULT:` → 解析JSON数据包：
   - `pending` → 根据提示执行**Pickup & Dispatch**流程。
   - `reviewtasks` → 根据提示执行**Review Dispatch**流程。
   - `stuck_tasks` → 根据提示执行**Stuck Task Recovery**流程。

或者，可以直接调用API：
- 待处理任务：`curl -sL "${SC_API_URL}/api/tasks/pending" -H "x-api-key: ${SC_API_KEY}"`
- 审查任务：`curl -sL "${SC_API_URL}/api/tasks/list?status=review" -H "x-api-key: ${SC_API_KEY}"`

从响应中解析工作空间配置（详见**多工作空间响应处理**部分）。

## 唤醒监听器流程

当cron触发唤醒监听器时：

1. 运行`~/.openclaw/skills/squad-control/scripts/wake-listener.sh`
2. 脚本首先调用`POST /api/wake/session`，并在配置了唤醒中继后建立出站连接。
3. 当收到唤醒信号时，脚本立即运行`poll-tasks.sh`并捕获`POLL_RESULT`数据包。
4. 如果`pending_tasks`中包含待处理的任务，监听器会通过本地的认证`POST /api/sessions/spawn`端点直接启动ACP工作线程，而无需经过第二个调度器。
5. 如果没有待处理的任务，但`reviewtasks`或`stuck_tasks`仍然存在，监听器会为剩余的任务启动一个本地的`openclaw代理线程。
6. 唤醒监听器的cron会话可以正常退出；后续的唤醒将由下一次监听器处理。
7. 如果中继不可用，脚本会回退到`GET /api/wake/poll`并使用相同的处理规则。
8. 如果在较旧的OpenClaw版本中，`/api/sessions/spawn`端点返回404/405/410/501错误，监听器会暂时放弃该功能，并在下次唤醒时不再尝试相同的请求。

当你需要低延迟的异步调度**而不暴露OpenClaw的公共网关URL**时，可以使用此方法。
监听器仅负责出站通信；现有的15分钟轮询cron仍然是最终的备用恢复机制。

### 多工作空间响应处理

使用账户级API密钥时，`/api/tasks/pending`可以返回来自**多个工作空间**的任务。每个任务都包含一个`workspace`对象，其中包含了完成任务所需的所有配置。

**响应格式 — 工作空间范围键（旧版本/单工作空间）：**
→ `workspace`位于顶层；任务本身没有自己的`workspace`对象。

**响应格式 — 账户范围键（多工作空间）：**
→ 每个任务都携带自己的`workspace`对象。来自不同工作空间的任务可能会出现在同一个响应中。

**代理字段 — 始终嵌套在`task.agent`下（ never flat on task root）：**
> ⚠️ **不要使用`task.agentName` — 该字段不存在**。始终使用`task.agent.name`、`task.agent.model`、`task.agent.soulMd`、`task.agent._id`。

**兼容两种响应格式：**

### 每个工作空间的并发限制**

当返回来自多个工作空间的任务时，**每个工作空间的并发数**需要单独计算。不要将工作空间A的代理数量计入工作空间B的并发限制。

### 困境任务恢复

每个cron周期执行两次检查：

**检查1 — 任务处于“working”状态且包含待合并的PR：**
对于每个`deliverables`中包含PR条目、`startedAt`存在且`startedAt`超过30分钟（且没有最近活动信号）的正在处理中的任务 → 自动将其转移到审查状态。

在恢复之前，需要执行以下幂等性检查：
1. 如果任务的元数据中已经存在`autoRescuedAt`标记，则跳过。
2. 如果线程中已经存在针对该任务的自动恢复消息，则跳过。
3. 恢复成功后，写入`autoRescuedAt=<now>`（或等效内容）的标记，以防止在后续cron周期中重复恢复。

**检查2 — 任务标记为“done”但PR未合并：**
对于每个最近完成但PR未合并的任务，验证PR是否真的已经合并：
如果`"merged":false`（PR仍然开放），则重新启动审查流程。

在创建审查任务之前，需要执行幂等性检查：
1. 在现有任务中搜索是否已经存在引用此PR URL/编号的任务。
2. 只有在不存在新任务时，才创建新的审查任务。

### 审查调度

找到需要审查的任务后，确定审查者：

1. 如果设置了`SC_REVIEWER_AGENT_ID`，直接使用该ID。
2. 否则，查询代理并选择匹配“Code Reviewer”角色的代理。
3. 否则，使用“Hawk”或包含“Reviewer”角色的代理。

对于每个需要审查的任务（具有PR成果，且`pickedUpAt`未设置）：

**不要调用 `/api/tasks/pickup`** — 状态机会阻止从“review”到“working”的转换。相反，直接启动审查者，并让他们调用 `/api/tasks/review`（完成或分配状态）。

使用下面的**Review Flow**模板启动审查代理，直接传递任务ID和所有相关信息。

### 队伍负责人任务 — 合并与完成

当任务的分配代理是**队伍负责人**（角色包含“Lead”或“Orchestrator”）时，表示Hawk已经批准了PR，可以将其合并。**不要直接标记任务为完成** — 首先需要合并PR。

**如果合并失败**（出现冲突）：调用 `/api/tasks/fail` 并报告错误 — 不要强制合并。将冲突详情发布到任务线程中。
**如果没有PR成果**：直接完成任务。

---

### 并发限制

**在启动任何代理之前**，检查当前正在运行的代理数量：
计算状态为“running”的代理数量。并发限制来自`workspace.agentConcurrency`（默认值为2，如果没有设置）。

**对于单个工作空间：** 如果正在运行的代理数量达到或超过限制，则跳过当前周期的所有启动操作，并返回`HEARTBEAT_OK`。

**对于多工作空间（账户级密钥）：** **每个工作空间的并发数**需要单独计算**。即使其他工作空间的代理数量如何，一个工作空间的`agentConcurrency`为3的工作空间最多也可以运行3个代理。按工作空间分组任务，并分别检查每个工作空间的代理数量。

工作空间所有者可以在队伍控制 → 设置 → 代理并发设置中更改此限制。

---

### 任务分配与调度

向任务线程发送任务正在被分配的信息：
然后使用任务的代理信息启动一个子代理。在标签中包含工作空间名称，以便于识别多工作空间的任务：

### 启动提示模板

在构建提示时，按以下方式解析工作空间配置：
- **如果`task_workspace`存在**（账户范围键）：使用`task_workspace.repoUrl`、`task_workspace.githubToken`、`task_workspace.agentConcurrency`。
- **如果`task_workspace`不存在**（工作空间范围键）：使用响应中的顶层`workspace`。

```bash
curl -sL -X POST "${SC_API_URL}/api/tasks/set-review" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d '{"taskId": "${TASK_ID}", "agentId": "${AGENT_ID}", "result": "${summary}", "deliverables": [{"type": "pr", "name": "PR #N", "url": "${PR_URL}"}]}'
```

### 完成后

1. 将发现结果/总结发布到任务线程：
2. 通过GitHub API创建PR（参见`references/pr-template.md`）。
3. 如果有审查代理存在 → 将任务设置为审查状态：
4. 如果没有审查代理 → 直接完成任务：
5. 如果失败：**始终报告失败情况** — 不要默默地将任务标记为完成。

---

## 审查流程

在将任务路由给审查代理时，使用以下提示启动他们（填写所有必要的信息）：

**注意：** `workspace.githubToken` 来自 `/api/tasks/pending` 或 `/api/tasks/pickup` 的响应。切勿从凭据文件中读取它 — 因为该信息可能在该机器上不存在。

---

## 代理发现

**审查者选择顺序：**
1. `SC_REVIEWER_AGENT_ID`（显式覆盖）
2. 确切匹配“Code Reviewer”角色的代理。
3. 或者使用包含“Reviewer”角色的代理。

## 轮询脚本测试

在本地运行解析器测试：

`POLL_RESULT` 数据包的格式在 `references/poll-result.schema.json` 中有详细说明。

## 程序化创建任务

---

## 常见错误

1. **未完成工作就标记任务为完成** — 在标记任务完成之前，务必将结果发布到线程并创建PR（如果任务涉及代码审查）。空的结果加上没有线程消息意味着任务实际上并未完成。
2. **子代理在打开PR后调用 `/complete` 而不是 `/set-review` — 这是最常见的工作流程错误。如果打开了PR，唯一有效的下一步操作是调用 `set-review`。直接调用 `complete` 会跳过代码审查步骤，导致PR保持未合并状态。现在，困境任务恢复机制会捕获这些处于“完成”状态但PR未合并的任务，并自动创建审查任务。
3. **队伍负责人跳过合并步骤** — 当任务被分配给队伍负责人且包含PR成果时，应在标记任务完成之前先合并PR。
4. **在启动提示时未传递 `SC_API_URL/SC_API_KEY` — 子代理无法在没有这些信息的情况下与队伍控制进行通信。务必在启动模板中包含这些信息。
5. **未使用 `workspace.repoUrl` — 待处理和分配任务的响应中包含 `workspace.repoUrl` 和 `workspace.githubToken`。请使用这些信息，不要假设使用默认的仓库路径。
6. **忘记报告失败** — 如果出现问题，务必调用 `/api/tasks/fail`。如果任务长时间处于“working”状态，会导致队列堵塞。
7. **在私有仓库克隆时未使用令牌** — 请检查 `workspace.githubToken` 并使用git凭据辅助工具：`git -c "credential.helper=!f() { echo username=x-access-token; echo password=<token>; }; f" clone "$REPO_URL"` — 切勿直接在URL中嵌入令牌，因为这可能导致令牌泄露。
8. **在分支之前未拉取最新代码** — 这会导致基于过时的代码创建PR，从而引发合并冲突。
9. **使用全局并发设置而不是按工作空间设置** — 在处理来自多个工作空间的任务时（账户级密钥），每个工作空间都有自己的`agentConcurrency`限制。不要将工作空间A的代理数量计入工作空间B的并发限制。
10. **忽略 `task_workspace` 并始终使用顶层配置** — 账户级密钥会在每个任务中直接嵌入工作空间配置。如果 `task_workspace` 存在，请使用它；如果不存在，则使用顶层工作空间配置。