---
name: ralph-loop
description: 生成可复制的 Bash 脚本，用于实现 Ralph Wiggum 或 AI 代理的循环执行流程（适用于 Codex、Claude Code、OpenCode、Goose 等平台）。当需要根据 PROMPT.md、AGENTS.md、SPECS 和 IMPLEMENTATION_PLAN.md 文件来规划或构建代码时，可以使用这些脚本。脚本应支持规划（PLANNING）和构建（BUILDING）两种模式，并具备回压（backpressure）控制、沙箱（sandboxing）功能以及完成条件（completion conditions）的设置。
---

# Ralph 循环（事件驱动）

这是一个增强了的 Ralph 模式，它采用**事件驱动的通知机制**：当需要关注时，Codex/Claude 会直接调用 OpenClaw，而不是进行轮询。

## 关键概念

### 清新的会话
每次迭代都会创建一个具有**全新上下文**的代理会话。这样做有以下原因：
- 避免上下文窗口的限制
- 每次 `codex exec` 都是一个新的进程，不会保留之前运行的任何信息
- 信息会通过文件进行持久化存储：`IMPLEMENTATION_PLAN.md`、`AGENTS.md` 和 git 历史记录

### 基于文件的通知机制（备用方案）
如果 OpenClaw 在接收唤醒通知时受到速率限制：
1. 通知会被写入 `.ralph/pending-notification.txt` 文件
2. 会尝试唤醒 OpenClaw（可能会失败）
3. 当 OpenClaw 恢复后，它会检查是否有未处理的通知
4. 所有工作都不会丢失——所有信息都保存在 git 文件中

## 文件结构

```
project/
├── PROMPT.md                      # Loaded each iteration (mode-specific)
├── AGENTS.md                      # Project context, test commands, learnings
├── IMPLEMENTATION_PLAN.md         # Task list with status
├── specs/                         # Requirements specs
│   ├── overview.md
│   └── <feature>.md
└── .ralph/
    ├── ralph.log                  # Execution log
    ├── pending-notification.txt   # Current pending notification (if any)
    └── last-notification.txt      # Previous notification (for reference)
```

## 通知格式

`.ralph/pending-notification.txt` 文件的内容如下：
```json
{
  "timestamp": "2026-02-07T02:30:00+01:00",
  "project": "/home/user/my-project",
  "message": "DONE: All tasks complete.",
  "iteration": 15,
  "max_iterations": 20,
  "cli": "codex",
  "status": "pending"
}
```

状态值：
- `pending`：唤醒失败或未尝试
- `delivered`：唤醒成功

---

## OpenClaw 恢复流程
当 OpenClaw 在受到速率限制或停机后重新上线时，它会**检查是否有未处理的通知**：

```bash
# Find all pending notifications across projects
find ~/projects -name "pending-notification.txt" -path "*/.ralph/*" 2>/dev/null

# Or check a specific project
cat /path/to/project/.ralph/pending-notification.txt
```

### 根据消息前缀执行不同的恢复操作

| 前缀 | 操作 |
|--------|--------|
| `DONE:` | 向用户报告完成情况，并总结已完成的工作 |
| `PLANNING COMPLETE:` | 通知用户，询问是否准备好进入构建模式 |
| `PROGRESS:` | 记录进度，并在有重要进展时通知用户 |
| `DECISION:` | 向用户展示选项，等待回复，并将结果更新到 `AGENTS.md` 中 |
| `ERROR:` | 查看日志（`.ralph/ralph.log`），分析问题并协助解决或升级问题 |
| `BLOCKED:` | 立即向用户报告问题，并提供完整的信息 |
| `QUESTION:` | 向用户提问以获取澄清，并将结果更新到 `AGENTS.md` 中 |

### 提交响应
为了在下次迭代中处理用户的决策或问题，需要将用户的回复保存到 `AGENTS.md` 中：
```bash
echo "## Human Decisions
- [$(date '+%Y-%m-%d %H:%M')] Q: <question>? A: <answer>" >> AGENTS.md
```

下一次 Codex 会话会读取 `AGENTS.md` 文件以获取用户的回复。

### 清除通知
处理完通知后，需要将其从系统中清除：
```bash
mv .ralph/pending-notification.txt .ralph/last-notification.txt
```

---

## 工作流程

### 1. 收集需求
（如果尚未提供，请询问以下信息：）
- **目标/待办事项**：需要实现什么结果？
- **命令行工具**：`codex`、`claude`、`opencode`、`goose`
- **运行模式**：`PLANNING`（规划）、`BUILDING`（构建）或 `BOTH`（同时进行）
- **技术栈**：使用的语言、框架、数据库
- **测试命令**：如何验证代码的正确性
- **最大迭代次数**：默认为 20 次

### 2. 生成规范
将目标分解为多个**相关主题**，并分别生成对应的 `.spec/*.md` 文件：

```markdown
# specs/overview.md
## Goal
<one-sentence JTBD>

## Tech Stack
- Language: Python 3.11
- Framework: FastAPI
- Database: SQLite
- Frontend: HTMX + Tailwind

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

### 3. 生成 `AGENTS.md`
```markdown
# AGENTS.md

## Project
<brief description>

## Commands
- **Install**: `pip install -e .`
- **Test**: `pytest`
- **Lint**: `ruff check .`
- **Run**: `python -m app`

## Backpressure
Run after each implementation:
1. `ruff check . --fix`
2. `pytest`

## Human Decisions
<!-- Decisions made by humans are recorded here -->

## Learnings
<!-- Agent appends operational notes here -->
```

### 4. 生成特定于运行模式的提示文件（`PROMPT.md`）

#### 规划模式（PLANNING Mode）
```markdown
# Ralph PLANNING Loop

## Goal
<JTBD>

## Context
- Read: specs/*.md
- Read: Current codebase structure
- Update: IMPLEMENTATION_PLAN.md

## Rules
1. Do NOT implement code
2. Do NOT commit
3. Analyze gaps between specs and current state
4. Create/update IMPLEMENTATION_PLAN.md with prioritized tasks
5. Each task should be small (< 1 hour of work)
6. If requirements are unclear, list questions

## Notifications
When you need input or finish planning:
```bash
openclaw gateway wake --text "PLANNING: <你的消息>" --mode now
```

Use prefixes:
- `DECISION:` — Need human input on a choice
- `QUESTION:` — Requirements unclear
- `DONE:` — Planning complete

## Completion
When plan is complete and ready for building, add to IMPLEMENTATION_PLAN.md:
```
STATUS: PLANNINGCOMPLETE
```
Then notify:
```bash
openclaw gateway wake --text "DONE: 规划完成。已识别出 X 项任务。" --mode now
```
```

#### 构建模式（BUILDING Mode）
```markdown
# Ralph BUILDING Loop

## Goal
<JTBD>

## Context
- Read: specs/*.md, IMPLEMENTATION_PLAN.md, AGENTS.md
- Implement: One task per iteration
- Test: Run backpressure commands from AGENTS.md

## Rules
1. Pick the highest priority incomplete task from IMPLEMENTATION_PLAN.md
2. Investigate relevant code before changing
3. Implement the task
4. Run backpressure commands (lint, test)
5. If tests pass: commit with clear message, mark task done
6. If tests fail: try to fix (max 3 attempts), then notify
7. Update AGENTS.md with any operational learnings
8. Update IMPLEMENTATION_PLAN.md with progress

## Notifications
Call OpenClaw when needed:
```bash
openclaw gateway wake --text "<前缀>: <消息>" --mode now
```

Prefixes:
- `DECISION:` — Need human input (e.g., "SQLite vs PostgreSQL?")
- `ERROR:` — Tests failing after 3 attempts
- `BLOCKED:` — Missing dependency, credentials, or unclear spec
- `PROGRESS:` — Major milestone complete (optional)
- `DONE:` — All tasks complete

## Completion
When all tasks are done:
1. Add to IMPLEMENTATION_PLAN.md: `STATUS: COMPLETE`
2. Notify:
```bash
openclaw gateway wake --text "DONE: 所有任务已完成。总结：<已完成的工作>" --mode now
```
```

### 5. 运行循环
使用提供的 `scripts/ralph.sh` 脚本来执行整个流程：

```bash
# Default: 20 iterations with Codex
./scripts/ralph.sh 20

# With Claude Code
RALPH_CLI=claude ./scripts/ralph.sh 10

# With tests
RALPH_TEST="pytest" ./scripts/ralph.sh
```

---

## 并行执行
对于独立的任务，可以使用 git 的工作树（worktrees）来管理任务：
```bash
# Create worktrees for parallel work
git worktree add /tmp/task-auth main
git worktree add /tmp/task-upload main

# Spawn parallel sessions (each is clean/fresh)
exec pty:true background:true workdir:/tmp/task-auth command:"codex exec --full-auto 'Implement user authentication...'"
exec pty:true background:true workdir:/tmp/task-upload command:"codex exec --full-auto 'Implement image upload...'"
```

任务状态跟踪：
| 会话 ID | 工作树 | 任务 | 状态 |
|------------|----------|------|--------|
| abc123 | /tmp/task-auth | 认证模块 | 正在运行 |
| def456 | /tmp/task-upload | 图像上传 | 正在运行 |

每个 Codex 会独立地执行任务。请检查每个工作树中的 `.ralph/pending-notification.txt` 文件，以获取通知信息。

---

## 与命令行工具（CLI）相关的注意事项

### Codex
- 需要一个 git 仓库
- 每次 `codex exec` 都是一个全新的会话，不会保留之前的执行信息
- `--full-auto`：在工作区中自动批准任务（在沙箱环境中）
- `--yolo`：不使用沙箱，也不进行自动批准（风险较高但执行速度快）
- 默认使用的模型：gpt-5.2-codex

### Claude
- `--dangerously-skip-permissions`：自动批准任务（仅在沙箱环境中使用）
- 不需要 git 仓库
- 每次调用都是全新的会话

### OpenCode
- 使用 `opencode run "$(cat PROMPT.md)"` 来执行任务

### Goose
- 使用 `goose run "$(cat PROMPT.md)"` 来执行任务

---

## 安全注意事项
⚠️ **自动批准功能具有风险**。务必遵循以下规则：
1. 将相关代码放在专门的目录或分支中运行
2. 对于不可信的项目，使用沙箱环境（如 Docker 或虚拟机）
3. 准备好 `git reset --hard` 命令作为应急措施
4. 在提交代码之前仔细审查所有的更改

---

## 快速入门指南

```bash
# 1. Create project directory
mkdir my-project && cd my-project && git init

# 2. Copy templates from skill
cp /path/to/ralph-loop/templates/* .
mv PROMPT-PLANNING.md PROMPT.md

# 3. Create specs
mkdir specs
cat > specs/overview.md << 'EOF'
## Goal
Build a web app that...

## Tech Stack
- Python 3.11 + FastAPI
- SQLite
- HTMX + Tailwind

## Features
1. Feature one
2. Feature two
EOF

# 4. Edit PROMPT.md with your goal

# 5. Run the loop
./ralph.sh 20
```

---

## 示例：Antique Catalogue 项目
在这个项目中，代理会执行以下操作：
1. （规划阶段）将任务分解为 10-15 个部分
2. （构建阶段）每次迭代完成一个任务
3. 每个任务成功完成后都会提交代码
4. 在任务完成或遇到问题时发送通知