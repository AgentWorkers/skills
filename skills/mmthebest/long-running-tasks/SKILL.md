---
name: long-running-tasks
description: Orchestrate multi-phase background development using coding agents. Use when: (1) a project has multiple sequential tasks that should run autonomously without human intervention between steps, (2) the user wants continuous background work with crash recovery, stall detection, and progress reporting, (3) the user mentions "long-running tasks", "autonomous development", "background orchestration", or "multi-phase project". Not for: single one-shot tasks, interactive pairing, or work requiring human review between every step.
---

# 长期运行任务的编排

使用编码代理作为工作节点，以及 cron 作业作为编排器，来自动执行多阶段项目。

## 问题

编码代理是一次性使用的：它们完成任务后就会退出，且不会自动启动下一个任务。如果没有编排机制，任务之间的执行会陷入停滞状态，直到有人发现为止。

## 架构

```
Orchestrator (cron, every 10-30 min)
  │
  ├─ Stale lock?         → clean up, continue
  ├─ Live lock?          → another orchestrator running, exit
  ├─ .pause file?        → skip spawning, report paused
  ├─ Worker PID alive?   → check for stall, report status
  └─ No worker?          → read TODO.md → spawn next task
                               │
                               ▼
                          Worker (coding agent session)
                            - Read project context + TODO.md
                            - Implement one task
                            - Run tests
                            - Commit + push
                            - Update TODO.md
                            - Exit
```

## 文件规范

所有运行时文件都使用项目名称作为文件名前缀，以避免在编排多个项目时发生冲突：

```
/tmp/lrt-<project>-worker.pid         # worker PID
/tmp/lrt-<project>-orchestrator.lock  # orchestrator lock (contains orchestrator PID)
/tmp/lrt-<project>-last-commit        # last reported commit hash
/tmp/lrt-<project>-worker.log         # worker stdout/stderr
```

为每个项目选择一个简短且唯一的名称（例如 `myapp`、`ra`、`blog`）。

## 设置

### 1. 在项目根目录下创建 `TODO.md`

创建一个结构化的任务队列。每个任务都必须足够独立，以便能够被代理程序从零开始执行：

```markdown
# TODO

## Phase 1 — Name (IN PROGRESS)
- [x] Completed task
- [ ] **Task title**
      What to do, which files to touch, acceptance criteria.
- [ ] BLOCKED: Task waiting on external input

## Phase 2 — Name (QUEUED)
- [ ] Task...
```

以 `BLOCKED:` 为前缀的任务会被编排器跳过。

### 2. 创建项目上下文文件

为代理程序创建一个上下文文件（通常命名为 `CLAUDE.md` 或 `AGENTS.md`），其中包含以下内容：技术栈、架构、可执行的命令、当前执行阶段以及环境配置。文件长度应控制在 100 行以内。

请参考 `assets/context-file-template.md` 以获取可用于项目的模板文件。

### 3. 配置编排器的 cron 作业

使用 OpenClaw 的 `cron` 工具，并设置 `sessionTarget: "isolated"` 和 `payload.kind: "agentTurn"`。

详细配置信息、提示模板以及任务暂停/恢复的逻辑请参阅 `references/orchestrator-cron.md`。

### 4. 手动启动第一个工作节点

首先以安全模式（默认模式）启动第一个任务。之后编排器会接管任务执行：

```bash
cd /path/to/project && nohup <agent-command> '<task prompt>' > /tmp/lrt-<project>-worker.log 2>&1 &
echo $! > /tmp/lrt-<project>-worker.pid
```

初始运行时请使用代理程序的默认权限设置。有关代理命令示例和安全指南，请参阅 `references/orchestrator-cron.md`。

## 工作节点规则

每个工作节点的提示信息都必须包含以下指令。具体模板请参阅 `references/worker-prompt-template.md`：

1. **先读取上下文信息** — 读取项目上下文文件 `CLAUDE.md` 和 `TODO.md`。
2. **仅执行一个任务** — 选择第一个未完成且未被标记为 `BLOCKED` 的任务。
3. **执行测试后再提交** — 运行测试套件；修复错误后再继续执行。
4. **更新 `TODO.md` — 将已完成的任务从列表中移除。
5. **提交代码并推送** — 遵循项目的提交规范。
6. **发送完成信号** — 使用命令 `openclaw system event --text "Done: <summary>" --mode now`。
7. **切勿静默退出** — 如果任务被阻塞，提交已完成的代码，并附上原因说明。

注意：工作节点会尽力清理自己的进程 ID（PID）文件，但真正的安全保障还是依赖于编排器——编排器会检查进程是否仍然存活，而不管文件是否已被清理。

## 暂停与恢复

```bash
touch /path/to/project/.pause    # pause — orchestrator skips spawning
rm /path/to/project/.pause       # resume
```

编排器仍会按照计划运行，但会显示为“暂停”状态，而不会自动启动新的任务。

## 进度报告

- 在 `/tmp/lrt-<project>-last-commit` 文件中记录最后一次提交的哈希值。
- 仅在有新的提交时发送详细报告。
- 报告中应包含差异统计信息（`git diff --stat HEAD~1`），而不是所有文件的完整差异列表。
- 如果没有变化，只需显示一行：“自 [hash] 以来没有新的提交”。

## 安全性

- **先在测试环境中验证**。在将编排器和代理程序应用于实际项目之前，先在测试仓库中运行它们，确保它们能够按预期工作。
- **限制权限**：负责提交和推送的代理程序需要具备 Git 访问权限。使用专门的部署密钥或具有最小写入权限的机器账户；切勿使用个人账户的广泛权限。
- **不要在上下文文件中存储敏感信息**。项目上下文文件（`CLAUDE.md`、`TODO.md`）中不得包含 API 密钥、令牌或密码。应明确指出敏感信息的存储位置（例如：“API 密钥存储在 ~/.zshrc 中”），切勿将它们直接写入文件中。
- **避免绕过权限检查的选项**：代理程序的命令行工具通常提供跳过安全提示的选项。在确认流程安全可靠之前，请勿使用这些选项。详情请参阅 `references/orchestrator-cron.md`。
- **手动审核后再自动推送**：在初始运行期间，可以考虑禁用工作节点的自动 `git push` 功能。让工作节点先在本地提交代码，然后手动审核后再进行推送。只有在确认结果可靠后，才能启用自动推送功能。
- **安全机制：终止阻塞的进程**：编排器可以通过进程 ID 杀死阻塞的任务。请使用唯一的项目名称前缀（参见文件规范）以避免与其他进程冲突。

## 避免的错误做法

- **仅用于报告状态的 cron 作业** — 只检查状态而不启动任务。
- **给定过多任务的统一提示** — 给工作节点分配过多任务会导致其只完成其中几个任务后立即退出。
- **缺少 `TODO.md` 文件** — 没有结构化的任务列表，编排器无法确定下一个任务是什么。
- **不跟踪进程 ID** — 使用 `pgrep` 命令可能会误判其他进程的 PID。
- **共享 `/tmp` 目录** — 如果多个项目使用相同的目录路径，可能会导致进程 ID 冲突。
- **在主会话中轮询** — 不要在循环中手动执行任务调度；让 cron 作业负责任务调度。