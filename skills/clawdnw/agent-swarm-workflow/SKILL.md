---
name: agent-swarm-workflow
description: "Jeffrey Emanuel 使用 NTM、Agent Mail、Beads 和 BV 实现的多智能体工作流程：在执行规划及创建智能体（Beads）之后，会进入执行阶段。文中包含了具体使用的提示语句。"
---

# 代理群工作流程 — 并行实现

> **核心理念：** 每个代理都是可替代的，并且具有通用性。它们都使用相同的基模型，并且都会读取 `AGENTS.md` 文件。仅仅将某个代理标记为“前端代理”并不会使其在前端任务上表现得更好。

> 该代理群通过 `Agent Mail` 和 `Beads` 实现分布式、高可用性和自我组织的能力。

---

## 先决条件

在启动代理群之前，请确保满足以下条件：

1. 已经制定了全面的计划（参见 `planning-workflow` 技能说明）。
2. 所有的 `Beads` 都已经准备好（参见 `beads-workflow` 技能说明）。
3. `AGENTS.md` 文件已配置完成，其中包含了所有工具的详细信息。
4. `Agent Mail` 服务器正在运行（`am` 或 `~/projects/mcp_agent_mail/scripts/run_server_with_token.sh`）。
5. 已经安装了 `NTM` 用于会话管理。

---

## 代理群架构

```
┌─────────────────────────────────────────────────────────────┐
│                         BEADS                               │
│     (Task graph with dependencies, priorities, status)      │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
┌─────────────────────────────┐  ┌─────────────────────────┐
│        BV                   │  │     AGENT MAIL          │
│  (What to work on)          │  │  (Coordination layer)   │
└─────────────────────────────┘  └─────────────────────────┘
         │                            │
         └──────────────┬─────────────┘
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    NTM + AGENTS                             │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐     │
│  │ CC  │  │ CC  │  │ Cod │  │ Gmi │  │ CC  │  │ Cod │     │
│  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## 启动代理群

### 使用 NTM（命名 Tmux 管理器）

```bash
# Spawn a swarm with multiple agents
ntm spawn myproject --cc=3 --cod=2 --gmi=1

# Send initial prompt to all Claude Code agents
ntm send myproject --cc "$(cat initial_prompt.txt)"

# Or send to all agents
ntm send myproject --all "$(cat initial_prompt.txt)"
```

### 手动设置

在项目文件夹中为每个代理创建相应的 tmux 会话/窗口。

---

## 启动代理的具体指令

向每个代理发送以下指令以启动它们：

```
First read ALL of the AGENTS dot md file and README dot md file super carefully and understand ALL of both! Then use your code investigation agent mode to fully understand the code, and technical architecture and purpose of the project. Then register with MCP Agent Mail and introduce yourself to the other agents.

Be sure to check your agent mail and to promptly respond if needed to any messages; then proceed meticulously with your next assigned beads, working on the tasks systematically and meticulously and tracking your progress via beads and agent mail messages.

Don't get stuck in "communication purgatory" where nothing is getting done; be proactive about starting tasks that need to be done, but inform your fellow agents via messages when you do so and mark beads appropriately.

When you're not sure what to do next, use the bv tool mentioned in AGENTS dot md to prioritize the best beads to work on next; pick the next one that you can usefully work on and get started. Make sure to acknowledge all communication requests from other agents and that you are aware of all active agents and their names.  Use ultrathink.
```

---

## 实现循环

### 继续执行下一个任务的指令

当代理完成一个任务后，使用以下指令让它们继续执行下一个任务：

```
Reread AGENTS dot md so it's still fresh in your mind.   Use ultrathink.   Use bv with the robot flags (see AGENTS dot md for info on this) to find the most impactful bead(s) to work on next and then start on it. Remember to mark the beads appropriately and communicate with your fellow agents. Pick the next bead you can actually do usefully now and start coding on it immediately; communicate what you're working on to your fellow agents and mark beads appropriately as you work. And respond to any agent mail messages you've received.
```

### 任务完成后的自我检查指令

在代理继续执行下一个任务之前，让它们先对自己的工作进行自我检查：

```
Great, now I want you to carefully read over all of the new code you just wrote and other existing code you just modified with "fresh eyes" looking super carefully for any obvious bugs, errors, problems, issues, confusion, etc. Carefully fix anything you uncover. Use ultrathink.
```

**持续执行这些指令，直到它们不再发现错误为止。**

---

## 处理上下文压缩

### 上下文压缩后的指令

当代理完成上下文压缩操作后，立即执行以下指令：

```
Reread AGENTS dot md so it's still fresh in your mind.   Use ultrathink.
```

这有助于重新建立关于工具和工作流程的关键信息。

---

## 质量检查指令

### 跨代理之间的代码审查指令

定期让代理互相审查彼此的工作：

```
Ok can you now turn your attention to reviewing the code written by your fellow agents and checking for any issues, bugs, errors, problems, inefficiencies, security problems, reliability issues, etc. and carefully diagnose their underlying root causes using first-principle analysis and then fix or revise them if necessary? Don't restrict yourself to the latest commits, cast a wider net and go super deep! Use ultrathink.
```

### 随机代码检查指令

为了进行深入的质量检查，可以使用以下指令：

```
I want you to sort of randomly explore the code files in this project, choosing code files to deeply investigate and understand and trace their functionality and execution flows through the related code files which they import or which they are imported by.

Once you understand the purpose of the code in the larger context of the workflows, I want you to do a super careful, methodical, and critical check with "fresh eyes" to find any obvious bugs, problems, errors, issues, silly mistakes, etc. and then systematically and meticulously and intelligently correct them.

Be sure to comply with ALL rules in AGENTS dot md and ensure that any code you write or revise conforms to the best practice guides referenced in the AGENTS dot md file. Use ultrathink.
```

---

## 提交代码更改

### 提交更改的指令

让代理提交逻辑上相关的代码更改：

```
Now, based on your knowledge of the project, commit all changed files now in a series of logically connected groupings with super detailed commit messages for each and then push. Take your time to do it right. Don't edit the code at all. Don't commit obviously ephemeral files. Use ultrathink.
```

---

## 任务完成后的指令

### 添加测试覆盖率的指令

```
Do we have full unit test coverage without using mocks/fake stuff? What about complete e2e integration test scripts with great, detailed logging? If not, then create a comprehensive and granular set of beads for all this with tasks, subtasks, and dependency structure overlaid with detailed comments.
```

### UI/UX 评审指令

```
Great, now I want you to super carefully scrutinize every aspect of the application workflow and implementation and look for things that just seem sub-optimal or even wrong/mistaken to you, things that could very obviously be improved from a user-friendliness and intuitiveness standpoint, places where our UI/UX could be improved and polished to be slicker, more visually appealing, and more premium feeling and just ultra high quality, like Stripe-level apps.
```

### 深度优化 UI/UX 的指令

```
I still think there are strong opportunities to enhance the UI/UX look and feel and to make everything work better and be more intuitive, user-friendly, visually appealing, polished, slick, and world class in terms of following UI/UX best practices like those used by Stripe, don't you agree? And I want you to carefully consider desktop UI/UX and mobile UI/UX separately while doing this and hyper-optimize for both separately to play to the specifics of each modality. I'm looking for true world-class visual appeal, polish, slickness, etc. that makes people gasp at how stunning and perfect it is in every way.  Use ultrathink.
```

---

## 代理间的通信机制

### 代理如何协调工作

每个代理需要执行以下操作：
1. 在会话开始时通过 `Agent Mail` 进行注册。
2. 在编辑文件之前先进行文件预留（`filereservation_paths`）。
3. 通过包含 `thread_id` 的消息来宣布自己的工作进度。
4. 在任务之间检查收件箱。
5. 完成工作后释放预留的文件。

### 文件预留的规则

```python
# Before starting work on a bead
file_reservation_paths(
    project_key="/path/to/project",
    agent_name="GreenCastle",
    paths=["src/auth/**/*.ts"],
    ttl_seconds=3600,
    exclusive=True,
    reason="bd-123"
)

# After completing work
release_file_reservations(project_key, agent_name)
```

### 通信机制

```python
# Announce starting a bead
send_message(
    project_key, agent_name,
    to=["BlueLake", "RedMountain"],  # Other active agents
    subject="[bd-123] Starting auth module",
    body_md="I'm taking bd-123. Reserved src/auth/**.",
    thread_id="bd-123"
)

# Update on completion
send_message(
    project_key, agent_name,
    to=["BlueLake", "RedMountain"],
    subject="[bd-123] Completed",
    body_md="Auth module done and tested. Released file reservations.",
    thread_id="bd-123"
)
```

---

## 使用 `BV` 进行任务选择

### 关键命令

```bash
# THE MEGA-COMMAND: Start here
bv --robot-triage

# Just get the single top pick
bv --robot-next

# Get parallel execution tracks (for multi-agent)
bv --robot-plan

# Check for cycles (MUST FIX if found)
bv --robot-insights | jq '.Cycles'

# Find bottlenecks
bv --robot-insights | jq '.bottlenecks'
```

**注意：** 绝不要直接运行 `bv` 命令，因为它会启动一个交互式 TUI 界面，从而阻塞当前的会话。

---

## 质量检查循环

**持续运行这些指令，直到没有发现错误且代码没有发生变化**

持续循环执行以下指令，直到系统稳定运行：
1. **自我检查**：代理检查自己的代码。
2. **跨代理审查**：代理互相审查彼此的代码。
3. **随机代码检查**：对随机选择的代码路径进行深入检查。

### 稳定状态的信号

当三种类型的检查都显示没有问题（未发现错误，也没有进行任何更改）时，可以认为代码质量可靠。

---

## 完整的指令参考

### 启动代理的初始指令
```
First read ALL of the AGENTS dot md file and README dot md file super carefully and understand ALL of both! Then use your code investigation agent mode to fully understand the code, and technical architecture and purpose of the project. Then register with MCP Agent Mail and introduce yourself to the other agents.

Be sure to check your agent mail and to promptly respond if needed to any messages; then proceed meticulously with your next assigned beads, working on the tasks systematically and meticulously and tracking your progress via beads and agent mail messages.

Don't get stuck in "communication purgatory" where nothing is getting done; be proactive about starting tasks that need to be done, but inform your fellow agents via messages when you do so and mark beads appropriately.

When you're not sure what to do next, use the bv tool mentioned in AGENTS dot md to prioritize the best beads to work on next; pick the next one that you can usefully work on and get started. Make sure to acknowledge all communication requests from other agents and that you are aware of all active agents and their names.  Use ultrathink.
```

### 继续执行下一个任务的指令
```
Reread AGENTS dot md so it's still fresh in your mind.   Use ultrathink.   Use bv with the robot flags (see AGENTS dot md for info on this) to find the most impactful bead(s) to work on next and then start on it. Remember to mark the beads appropriately and communicate with your fellow agents. Pick the next bead you can actually do usefully now and start coding on it immediately; communicate what you're working on to your fellow agents and mark beads appropriately as you work. And respond to any agent mail messages you've received.
```

### 自我检查指令
```
Great, now I want you to carefully read over all of the new code you just wrote and other existing code you just modified with "fresh eyes" looking super carefully for any obvious bugs, errors, problems, issues, confusion, etc. Carefully fix anything you uncover. Use ultrathink.
```

### 跨代理审查指令
```
Ok can you now turn your attention to reviewing the code written by your fellow agents and checking for any issues, bugs, errors, problems, inefficiencies, security problems, reliability issues, etc. and carefully diagnose their underlying root causes using first-principle analysis and then fix or revise them if necessary? Don't restrict yourself to the latest commits, cast a wider net and go super deep! Use ultrathink.
```

### 随机代码检查指令
```
I want you to sort of randomly explore the code files in this project, choosing code files to deeply investigate and understand and trace their functionality and execution flows through the related code files which they import or which they are imported by.

Once you understand the purpose of the code in the larger context of the workflows, I want you to do a super careful, methodical, and critical check with "fresh eyes" to find any obvious bugs, problems, errors, issues, silly mistakes, etc. and then systematically and meticulously and intelligently correct them.

Be sure to comply with ALL rules in AGENTS dot md and ensure that any code you write or revises conforms to the best practice guides referenced in the AGENTS dot md file. Use ultrathink.
```

### 上下文压缩后的指令
```
Reread AGENTS dot md so it's still fresh in your mind.   Use ultrathink.
```

### 提交代码更改的指令
```
Now, based on your knowledge of the project, commit all changed files now in a series of logically connected groupings with super detailed commit messages for each and then push. Take your time to do it right. Don't edit the code at all. Don't commit obviously ephemeral files. Use ultrathink.
```

### 添加测试覆盖率的指令
```
Do we have full unit test coverage without using mocks/fake stuff? What about complete e2e integration test scripts with great, detailed logging? If not, then create a comprehensive and granular set of beads for all this with tasks, subtasks, and dependency structure overlaid with detailed comments.
```

### UI/UX 评审指令
```
Great, now I want you to super carefully scrutinize every aspect of the application workflow and implementation and look for things that just seem sub-optimal or even wrong/mistaken to you, things that could very obviously be improved from a user-friendliness and intuitiveness standpoint, places where our UI/UX could be improved and polished to be slicker, more visually appealing, and more premium feeling and just ultra high quality, like Stripe-level apps.
```

### 深度优化 UI/UX 的指令
```
I still think there are strong opportunities to enhance the UI/UX look and feel and to make everything work better and be more intuitive, user-friendly, visually appealing, polished, slick, and world class in terms of following UI/UX best practices like those used by Stripe, don't you agree? And I want you to carefully consider desktop UI/UX and mobile UI/UX separately while doing this and hyper-optimize for both separately to play to the specifics of each modality. I'm looking for true world-class visual appeal, polish, slickness, etc. that makes people gasp at how stunning and perfect it is in every way.  Use ultrathink.
```

---

## 代理群的工作流程

每个循环都会带来以下改进：
- **CASS**（代码自适应系统）会记录解决方案。
- **CM**（代码模式分析系统）会提炼出最佳实践。
- **UBS**（错误检测系统）会发现更多问题。
- **BV**（代码健康检查工具）会显示系统的运行状态。

---

## 常见问题解答

**Q：代理如何知道该执行哪些任务？**
**A：** 它们使用 `bv --robot-triage` 或 `bv --robot-next` 命令来选择影响最大的、可以执行的任务。

**Q：如何避免任务冲突？**
**A：** 通过 `Agent Mail` 进行文件预留。独占的文件预留机制可以防止冲突；提交前的检查机制会确保这一点。

**Q：如果某个代理崩溃或忘记了任务怎么办？**
**A：** 每个代理都是可替代的。只需重新启动一个新的会话，读取 `AGENTS.md` 文件，查看任务状态，然后继续执行任务即可。

**Q：应该运行多少个代理？**
**A：** 这取决于项目的复杂度。建议从 3 个到 6 个代理开始。代理数量越多，执行速度越快，但协调开销也会增加。

**Q：哪种模型组合效果最好？**
**A：** 建议混合使用不同的模型。例如：3 个 Claude Code（Opus）、2 个 Codex（GPT 5.2）和 1 个 Gemini。这些模型各有优势。

**Q：代理是否需要具备特定的专业技能？**
**A：** 不需要。每个代理都是通用的。仅仅将某个代理标记为“前端代理”并不会使其在前端任务上表现得更好。

**Q：git 提交和任务之间有追溯关系吗？**
**A：** 是的。`bv` 会自动分析数据流，并通过逻辑推理将任务与相关的 git 提交关联起来。