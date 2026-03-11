---
name: multi-agent-protocol
version: 1.0.0
description: OpenClaw 中多智能体协作的生产协议。该协议结合了“规范优先”的任务定义方式、两阶段审核流程（规范审核 + 质量审核）、用于表示任务依赖关系的“珠子图”（bead dependency graph）、用于智能体间直接通信的 `blackboard.json` 文件、以及用于实现并行处理的“断路器重试策略”（Circuit Breaker retry strategy）。适用于需要协调多个子智能体完成复杂任务、设置质量检查点（quality gates）并确保系统容错性的场景。
author: lebo
license: MIT
keywords:
  - multi-agent
  - orchestration
  - spec-first
  - circuit-breaker
  - blackboard
  - beads
  - review
  - fault-tolerance
  - parallel-agents
  - sessions_spawn
---
# 多代理协作协议

本方案用于在 OpenClaw 中协调多个子代理，实现结构化的任务流程、质量控制、代理间通信以及自动故障恢复功能。该协议综合了社区中的多种设计模式，包括 `subagent-driven-development`、`beads`、`swarm-self-heal`、`agent-team-orchestration` 和 `http-retry-circuit-breaker`。

---

## 适用场景

- 当需要在复杂任务中启动 2 个或多个子代理时
- 任务之间存在代理间的依赖关系
- 对任务的质量有严格要求（不仅要求任务完成，还要确保其正确性和规范性）
- 需要具备无需人工干预的容错能力
- 多个代理需要共享状态信息，且无需通过协调器进行中间传递

**不适用场景：**
- 单个代理的任务（不必要的开销）
- 一次性任务（无需代理间的协作）
- 简单的任务分配

---

## 核心原则

1. **规范先行**：在没有规范文件的情况下，不得启动任何代理。没有规范，任务就无法开始。
2. **两阶段审核**：所有实现方案首先需经过规范审核，然后再进行质量审核。
3. **串行执行**：同一时间只能有一个实现者执行任务；并行执行仅用于研究或分析阶段。
4. **直接通信**：代理直接读写共享文件，协调器不充当信息中转者。
5. **故障限制机制**：当故障达到预设阈值时，系统会触发警报并停止无限循环。
6. **固定的 sessionKey**：相同角色的代理使用相同的 sessionKey，以确保其状态在多次启动过程中得以保留。

---

## 目录结构

```
{project-root}/
  .beads/              ← beads task graph (git-tracked, auto-managed)
  specs/
    {task-id}.md       ← Task spec (MUST exist before spawning Implementer)
  shared/
    blackboard.json    ← Live state bus (any agent reads/writes directly)
    artifacts/
      {role}/          ← Each agent's output artifacts
```

---

## 任务生命周期

```
Write Spec → bd create → bd ready → Claim → Implement → Self-Review
  → Spec Review → Quality Review → bd close → bd sync
```

---

## 第一步：编写规范文件

在启动任何代理之前，需创建 `specs/{task-id}.md` 文件：

```markdown
## Goal
What is the final state? (observable, verifiable)

## Scope
What is included / explicitly excluded?

## Inputs
Files, paths, dependencies, environment requirements.

## Outputs
Exact artifact paths and formats expected.

## Acceptance Criteria
Checklist. Each item must be independently verifiable.
- [ ] criterion 1
- [ ] criterion 2

## Risks
Known unknowns, edge cases, things to watch out for.
```

**如果没有明确的验收标准，说明规范文件尚未完成，此时不得启动代理。**

---

## 第二步：在 `beads` 中创建任务

```bash
# Initialize beads in project (first time only)
bd init --quiet

# Create task
bd create "Task title" -p 1 --json
# → returns task id like bd-a1b2

# Add dependencies if needed
bd dep add bd-child bd-parent     # child is blocked by parent

# Check what's ready to start
bd ready --json
```

---

## 第三步：启动实现者

任务提示信息必须**独立完整**——代理无法查看之前的对话记录。

```
sessions_spawn({
  task: "
    You are implementing task {task-id}.

    ## Spec
    {paste full spec content here — do not tell agent to read a file}

    ## Working Directory
    {absolute path}

    ## Output Path
    shared/artifacts/implementer/

    ## Context from Dependencies
    {paste relevant artifacts from blackboard.json if any}

    ## Before Starting
    If anything in the spec is unclear, ask now before writing code.

    ## Your Responsibilities
    1. Implement exactly what the spec says (nothing more, nothing less)
    2. Write tests
    3. Commit your work
    4. Self-review against spec acceptance criteria
    5. Update shared/blackboard.json with your status and artifact path
    6. Report: what you built, test results, artifact paths, known issues
  ",
  sessionKey: "implementer",
  runTimeoutSeconds: 600
})
```

**启动代理后，需要更新共享文件（blackboard）：**
```json
{
  "agents": {
    "implementer": { "status": "running", "task": "bd-a1b2", "artifact": null, "ts": "..." }
  }
}
```

---

## 第四步：规范审核

**不要仅依赖实现者的自我报告，必须亲自阅读其代码。**

```
sessions_spawn({
  task: "
    You are a Spec Compliance Reviewer.

    ## Your Job
    Verify the implementation matches the spec — by reading the actual code,
    not by trusting the implementer's report.

    ## Spec (the standard)
    {paste full spec}

    ## Implementer's Report
    {paste implementer output}

    ## Artifact Location
    shared/artifacts/implementer/

    ## What to Check
    - MISSING: Requirements in spec not implemented
    - EXTRA: Things implemented that weren't requested
    - MISUNDERSTOOD: Implementation interprets spec differently than intended

    ## Output Format
    ✅ Spec compliant — all requirements verified by code inspection
    OR
    ❌ Issues found:
    - [file:line] Missing: {requirement}
    - [file:line] Extra: {what was added}
    - [file:line] Misunderstood: {intended vs actual}
  ",
  sessionKey: "spec-reviewer",
  runTimeoutSeconds: 300
})
```

**规则：**
- 规范审核必须通过后，才能进行质量审核。
- 如果发现错误，由同一实现者（使用相同的 sessionKey）负责修复，然后重新进行审核。
- “勉强合格”是不被接受的。

---

## 第五步：质量审核

只有在规范审核通过后，才能继续执行任务。

```
sessions_spawn({
  task: "
    You are a Code Quality Reviewer. The spec compliance has already been verified.
    Your job is to check implementation quality.

    ## Artifact Location
    shared/artifacts/implementer/

    ## What to Check
    - Names match behavior (not implementation details)
    - No over-engineering (YAGNI)
    - Follows existing project patterns
    - Tests verify behavior, not mock internals
    - No magic numbers or unexplained inline constants
    - No leftover debug code or TODOs

    ## Output Format
    ✅ Approved
    OR
    ❌ Issues:
    - [CRITICAL] {issue} — must fix before merge
    - [IMPORTANT] {issue} — should fix
    - [MINOR] {issue} — optional
  ",
  sessionKey: "quality-reviewer",
  runTimeoutSeconds: 300
})
```

---

## 第六步：完成任务

```bash
bd close bd-a1b2 --reason "Implemented and reviewed" --json
bd sync    # Always sync before ending session
```

---

## 共享文件（Blackboard 协议）

`shared/blackboard.json` 是代理间用于传递状态的共享文件。所有代理都可以直接读写该文件。协调器不负责信息的中转。

### 文件结构示例

```json
{
  "agents": {
    "{role}": {
      "status": "idle | running | done | failed",
      "task": "bd-xxxx",
      "artifact": "shared/artifacts/{role}/output.md",
      "ts": "ISO-8601 timestamp"
    }
  },
  "tasks": {
    "bd-xxxx": {
      "retry_count": 0,
      "last_error": null,
      "circuit_status": "closed"
    }
  },
  "signals": [
    {
      "from": "{role}",
      "to": "{role}",
      "type": "ready_for_review | blocked | artifact_ready",
      "payload": "path or message",
      "ts": "ISO-8601 timestamp"
    }
  ]
}
```

---

## 代理职责

| 事件 | 执行操作 |
|-------|--------|
| 代理启动 | 写入 `status: running` |
| 任务完成 | 写入 `status: done` 以及任务成果文件的路径 |
| 任务失败 | 写入 `status: failed` 以及错误信息 |
| 需要其他代理的输出结果 | 从共享文件中读取 `agents.{role}.artifact` 文件的内容 |

---

## 故障恢复机制（Circuit Breaker）与重试策略

```
On task failure:

L1 — Auto-retry (same agent, same sessionKey)
  When: retry_count < 2
  Delay: 30s backoff
  For: transient errors, timeouts

L2 — Escalate (stronger model, same sessionKey)
  When: retry_count == 2
  Action: override model to a higher-reasoning option
  For: task is hard, needs better reasoning

L3 — Circuit Open (stop, alert human)
  When: retry_count >= 3
  Action:
    - Write blackboard tasks.{id}.circuit_status = "circuit_open"
    - Alert user: task name, failure reason, retry history
    - bd update {id} --status blocked
  For: task itself is broken, retrying won't help
```

---

## 并行执行规则

| 任务类型 | 是否支持并行 | 原因 |
|-----------|-----------|--------|
| 代码实现 | ✌ 仅支持串行执行 | 避免代码冲突 |
| 研究/分析 | ✅ 支持并行 | 数据互不影响 |
| 文档编写（不同文件） | ✅ 支持并行 | 文件相互独立 |
| 审核工作 | ✅ 支持并行 | 需要独立阅读不同任务的内容 |

### 在确实需要并行执行时（使用 Git Worktree）

```bash
git worktree add ../workspace-{role} -b agent/{role}/{task-id}
```

- 在启动代理时，将工作目录设置为 Git Worktree 的路径。
- 完成任务后，提交代码变更（PR），由协调器审核差异并最终合并代码。

---

## 固定的 sessionKey 规则

相同角色的代理使用相同的 sessionKey，这样它们就能在多次启动过程中保持之前的工作状态。

| 角色 | sessionKey | 保留的信息 |
|------|-----------|---------|
| 实现者 | `implementer` | 代码库中的信息、之前的决策 |
| 规范审核者 | `spec-reviewer` | 审核标准、之前的发现结果 |
| 质量审核者 | `quality-reviewer` | 代码风格规范、项目惯例 |
| 研究人员 | `researcher` | 研究背景信息、参考资料 |

---

## 协调器的职责范围

**协调器的任务：**
- 编写规范文件
- 管理任务节点（`bd create`、`bd dep add`、`bd ready`、`bd close`、`bd sync`）
- 启动相应角色的代理
- 读取共享文件（blackboard）以确定下一步操作
- 执行故障恢复机制（Circuit Breaker）
- 向用户报告任务进度

**协调器不得：**
- 直接编写实现代码
- 在代理之间传递信息（代理应直接从共享文件中获取信息）
- 在没有规范文件的情况下启动代理

---

## 监控机制（可选但推荐）

安装 `swarm-self-heal` 并定期进行检查：

```bash
bash skills/swarm-self-heal/scripts/check.sh
```

配置定时任务（例如每 30 分钟执行一次），用于检测以下情况：
- 代理长时间无活动（未更新共享文件）
- 需要人工干预的失败任务
- 系统组件的运行状态

---

## 任务结束时的操作

```bash
bd sync            # Flush all task state to git
bd ready --json    # Show next unblocked tasks (for handoff notes)
```

在任务完成后，需将任务状态更新到共享文件中：`status: done | paused`。

---

## 快速参考

```bash
# Initialize
bd init --quiet

# Task management
bd create "Title" -p 1 --json
bd dep add bd-child bd-parent
bd ready --json
bd update bd-xxxx --status in_progress --assignee implementer --json
bd close bd-xxxx --reason "done" --json
bd sync

# Dependency visualization
bd dep tree bd-xxxx
bd blocked --json
```