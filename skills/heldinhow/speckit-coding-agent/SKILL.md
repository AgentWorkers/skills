# SpecKit 编码代理

**版本:** 1.1.0

---

## 概述

这是一个完整的 **规范驱动开发（Spec-Driven Development, SDD）** 工作流程，它改变了您构建软件的方式。从想法开始 → 创建规范 → 生成计划 → 执行任务。该工具由 spec-kit 和 OpenCode CLI 提供支持，确保每一行代码都有可追溯的需求依据。

### 主要特性

- **六阶段工作流程**：创建规范 → 规范制定 → 计划制定 → 任务分配 → 实施 → 进度跟踪
- **人工智能辅助的文档生成**：每个阶段都会通过 OpenCode 生成 Markdown 文档
- **动态文档更新**：随着任务的实施，TASKS.md 会自动更新
- **支持多代理协作**：可以委托给子代理，并保留所有上下文信息
- **内置最佳实践**：代码规范、测试驱动开发（TDD）和增量交付被纳入工作流程

### 适用人群

- 需要在编写代码之前先制定规范的开发者
- 需要可追溯需求的团队
- 需要结构化上下文支持的 AI 辅助项目
- 使用 OpenCode CLI 进行开发的任何人

### 快速示例

```bash
# Initialize spec-kit
cd my-project && specify init --here --ai opencode

# Generate all artifacts
echo "/speckit.constitution" | opencode run  # Principles
echo "/speckit.specify" | opencode run       # Requirements
echo "/speckit.plan" | opencode run          # Architecture
echo "/speckit.tasks" | opencode run         # Action items

# Delegate to subagents → then update tracking
echo "/speckit.implement" | opencode run     # Marks completed tasks
```

---

该工具将 **spec-kit** 工作流程与 OpenCode 结合，实现规范驱动的开发。使用此流程可以在编码前创建规范、计划和任务。

### 先决条件：安装并初始化 Spec-Kit

在使用任何 spec-kit 命令之前，必须完成以下步骤：

#### 第一步：安装 spec-kit
```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

#### 第二步：在项目中初始化 spec-kit
```bash
cd /root/.openclaw/workspace/my-project
specify init --here --ai opencode
```

初始化完成后，您的项目目录中将可以使用 `/speckit.*` 命令。

---

### 规范驱动开发工作流程

**必须按顺序执行每个命令！**

#### 第一步：创建规范
```bash
echo "/speckit.constitution
Create a project constitution focused on clean code principles, simplicity, and test-driven development.
" | opencode run
```
✅ 生成：`CONSTITUTION.md`

#### 第二步：创建规范
```bash
echo "/speckit.specify
Create a baseline specification for a Python function that calculates factorial numbers recursively.
" | opencode run
```
✅ 生成：`SPECIFICATION.md`

#### 第三步：制定计划
```bash
echo "/speckit.plan" | opencode run
```
✅ 生成：`PLAN.md`

#### 第四步：生成任务
```bash
echo "/speckit.tasks" | opencode run
```
✅ 生成：`TASKS.md`

#### 第五步：执行实施并更新任务

子代理完成实施后，使用以下命令更新 tasks.md 的执行状态：

**选项 A：直接运行 `/speckit.implement`**
```bash
echo "/speckit.implement" | /root/.opencode/bin/opencode run
```
**结果：** 更新 TASKS.md，标记已完成的任务

**选项 B：如果实施是在外部完成的，则手动更新**
```bash
# Manually update TASKS.md to mark completed tasks
# or let /speckit.implement scan and update
```

**关键优势：** `/speckit.implement` 可维护一个包含执行历史的动态任务列表

---

### 完整工作流程图

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. /speckit.constitution → CONSTITUTION.md (principles)         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. /speckit.specify → SPECIFICATION.md (requirements)            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. /speckit.plan → PLAN.md (implementation phases)              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. /speckit.tasks → TASKS.md (actionable tasks)                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 5. Subagents read all artifacts and implement                   │
│    - CONSTITUTION.md, SPECIFICATION.md, PLAN.md, TASKS.md       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 6. /speckit.implement → Updates TASKS.md with status            │
│    - Marks [x] completed tasks                                  │
│    - Adds timestamps and metadata                               │
│    - Maintains living task list                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 7. Code implementation complete with tracked progress           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 快速入门

### 先决条件（必须先完成！）

1. **安装 spec-kit：**
   ```bash
   uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
   ```

2. **在项目中初始化 spec-kit：**
   ```bash
   cd ~/project
   specify init --here --ai opencode
   ```

3. **按顺序执行工作流程：**

   - 创建规范
   ```bash
   echo "/speckit.constitution
   Create a project constitution focused on clean code principles.
   " | opencode run
   ```

   - 创建计划
   ```bash
   echo "/speckit.plan" | opencode run
   ```

   - 生成任务
   ```bash
   echo "/speckit.tasks" | opencode run
   ```

4. **委托给子代理：**
   - 阅读所有文档（CONSTITUTION.md、SPECIFICATION.md、PLAN.md、TASKS.md）
   - 根据 TASKS.md 中的任务进行实施

5. **更新任务状态：**
   ```bash
   echo "/speckit.implement" | /root/.opencode/bin/opencode run
   ```
   这将更新 TASKS.md，以便跟踪已实施的内容。

---

## 完整工作流程示例

### 示例：完整的规范驱动开发流程

```bash
# Prerequisites (MUST DO FIRST!)
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

cd ~/my-new-project
specify init --here --ai opencode

# Step 1: Create Constitution
echo "/speckit.constitution
Create a project constitution focused on clean code principles.
" | opencode run

# Step 2: Create Specification
echo "/speckit.specify
Create a REST API for user management.
" | opencode run

# Step 3: Generate Plan
echo "/speckit.plan" | opencode run

# Step 4: Generate Tasks
echo "/speckit.tasks" | opencode run

# Step 5: Delegate to subagent (read all artifacts first)

# Step 6: Update tasks.md with execution status
echo "/speckit.implement" | /root/.opencode/bin/opencode run
# This updates TASKS.md marking completed tasks
```

### 示例：添加新功能

```bash
# Step 1: Create specification for new feature
echo "/speckit.specify
Add authentication endpoints with JWT support.
" | opencode run

# Step 2: Generate plan
echo "/speckit.plan" | opencode run

# Step 3: Generate tasks
echo "/speckit.tasks" | opencode run

# Step 4: Delegate to subagent (read all artifacts first)

# Step 5: Update tasks.md with execution status
echo "/speckit.implement" | /root/.opencode/bin/opencode run
# This updates TASKS.md marking completed tasks
```

---

## 应避免的错误做法

❌ **不要在初始化之前尝试使用 spec-kit 命令：**
```bash
cd /root/.openclaw/workspace/new-project
echo "/speckit.constitution" | opencode run  # Won't work!
```

✅ **请改为：**
```bash
cd /root/.openclaw/workspace/new-project
specify init --here --ai opencode  # DO THIS FIRST
echo "/speckit.constitution" | opencode run  # NOW it works
```

❌ **不要连续执行多个命令：**
```bash
{ echo "/speckit.constitution"; echo "/speckit.specify"; } | opencode run
```

❌ **实施完成后不要跳过运行 `/speckit.implement`：**
```bash
# Wrong: TASKS.md stays with checkboxes empty
# Right: 
echo "/speckit.implement" | opencode run  # Updates TASKS.md
```

**原因：** 如果不更新 TASKS.md，您将无法区分实际完成的内容和计划中的内容。

❌ **在未阅读规范内容的情况下不要执行任务：**
```bash
# Wrong: Subagent doesn't have spec context
sessions_spawn task="Implement authentication"
# Right: Subagent reads all artifacts
sessions_spawn task="Read CONSTITUTION.md, SPECIFICATION.md, PLAN.md, TASKS.md first."
```

---

## 为什么使用 `/speckit.implement？**

**优势：**
1. **自动跟踪**：TASKS.md 会自动更新执行状态
2. **进度可视化**：清晰地了解已完成和待完成的任务
3. **审计追踪**：记录实施步骤的历史
4. **未来参考**：便于维护时查看已完成的工作

**最佳实践：**
- 在子代理完成任务后运行 `/speckit.implement`
- 或定期运行它以更新进度
- 该文件将成为项目状态的实时文档

---

## `/speckit.implement` - 执行跟踪

**用途：** 更新 TASKS.md 的执行状态，标记已完成的任务并跟踪实施进度。

### 工作原理

当您运行 `/speckit.implement` 时，系统会：
1. 扫描项目目录中已完成的任务
2. 读取当前的 TASKS.md
3. 根据实际实施情况将任务标记为 [x] 完成
4. 更新文件中的执行元数据

### 使用方法

```bash
echo "/speckit.implement" | /root/.opencode/bin/opencode run
```

### 示例：更新后的 TASKS.md

运行 `/speckit.implement` 后，TASKS.md 的内容会发生变化：

**更新前：**
```markdown
## Tasks

- [ ] Create HTML structure
- [ ] Implement CSS styling
- [ ] Add JavaScript functionality
```

**更新后：**
```markdown
## Tasks

- [x] Create HTML structure (completed 2026-02-11 19:42 UTC)
- [ ] Implement CSS styling (in progress)
- [ ] Add JavaScript functionality (pending)
```

### 何时运行

| 时间点 | 操作 |
|--------|--------|
| 子代理完成任务后 | 运行 `/speckit.implement` 以跟踪进度 |
| 审查之前 | 检查哪些任务已完成，哪些待完成 |
| 每个功能完成后 | 更新任务状态 |
| 会话结束时 | 最终更新以记录审计痕迹 |

### 手动更新替代方案

如果实施是在外部完成的：

```bash
# Edit TASKS.md manually to mark completed tasks:
- [x] Task completed
- [ ] Task pending
```

或者使用子代理自动扫描和更新。

### 一致使用的优势

1. **动态文档**：TASKS.md 成为项目的实时状态
2. **进度可视化**：立即了解已完成、进行中和待完成的任务
3. **责任追溯**：时间戳记录每个任务完成的时间
4. **上下文保留**：未来的团队成员可以查看实施历史
5. **防止回归**：准确了解更改的内容和时间

### 最佳实践

- 在每个子代理完成任务后运行 `/speckit.implement`
- 将其纳入日常工作流程中
- 即使是小的更改，也要更新 TASKS.md
- 使用时间戳进行审计追踪
- 在寻求帮助或进行审查时参考更新后的 TASKS.md

---

## 备用策略

当使用 OpenCode 进行编码任务时，系统采用以下备用策略：

| 优先级 | 模型 | 提供者 | 角色 |
|----------|-------|----------|------|
| **主要** | `opencode/kimi-k2.5-free` | OpenCode | 主要的编码任务模型 |
| **备用 1** | `opencode/minimax-m2.1-free` | OpenCode | 高质量的备用模型 |
| **备用 2** | `opencode/glm-4.7-free` | OpenCode | 高效的标准任务模型 |
| **次要** | `openrouter/xiaomi/mimo-v2-flash` | OpenRouter | 备用模型，用于跨提供者的兼容性 |

### Opencode 任务执行的模型顺序

```json
{
  "primary": "opencode/kimi-k2.5-free",
  "fallbacks": [
    "opencode/minimax-m2.1-free",
    "opencode/glm-4.7-free"
  ]
}
```

**跨提供者备用：** 当 OpenCode 模型受到速率限制或不可用时，系统会切换到 `openrouter/xiaomi/mimo-v2-flash`（OpenRouter）以确保兼容性。

首先使用主要模型（`kimi-k2.5-free`），如果该模型不可用，系统会按顺序切换到其他模型。

### 为什么这样排序？

- **主要模型（Kimi K.25）：** 在编码和复杂推理任务方面具有最佳性能
- **备用模型 1（MiniMax M2.1）：** 性能类似，适用于复杂推理任务
- **备用模型 2（GLM 4.7）：** 在主要模型达到上限时，用于高效处理标准任务
- **次要模型（Xiaomi Mimo v2 Flash）：** 来自不同提供者，确保在 OpenCode 模型受限时的兼容性

---

## OpenCode

**默认模型：** `opencode/kimi-k2.5-free`

OpenCode 是此工作空间的首选编码工具。它使用 `kimi-k2.5-free` 作为主要模型，并在其他免费模型不可用时自动切换。

```bash
# Basic usage (uses default kimi-k2.5-free model)
bash workdir:~/project background:true command:"opencode run \"Your task\""

# Explicit model specification (optional, defaults to kimi-k2.5-free)
bash workdir:~/project background:true command:"opencode run --model opencode/kimi-k2.5-free \"Your task\""

# If primary is unavailable, it automatically falls back:
# minimax-m2.1-free → glm-4.7-free → (openrouter/xiaomi/mimo-v2-flash as cross-provider backup)
```

---

## `workdir` 的重要性

**为什么 `workdir` 很重要？** 代理会在指定的目录中启动，不会读取无关文件。

---

## Codex CLI

**默认模型：** `gpt-5.2-codex`（设置在 `~/.codex/config.toml` 中）

### 构建/创建（使用 `--full-auto` 或 `--yolo`）
```bash
# --full-auto: sandboxed but auto-approves in workspace
bash workdir:~/project background:true command:"codex exec --full-auto \"Build a snake game with dark theme\""

# --yolo: NO sandbox, NO approvals (fastest, most dangerous)
bash workdir:~/project background:true command:"codex --yolo \"Build a snake game with dark theme\""
```

### 审查 PR（基础模式，无需额外参数）

避免在正在运行的 Clawdbot 项目文件夹中审查 PR。请在 PR 提交的项目文件夹中查看（如果不在 `~/Projects/clawdbot` 中），或者先克隆到一个临时文件夹中。

```bash
# Option 1: Review in the actual project (if NOT clawdbot)
bash workdir:~/Projects/some-other-repo background:true command:"codex review --base main"

# Option 2: Clone to temp folder for safe review (REQUIRED for clawdbot PRs!)
REVIEW_DIR=$(mktemp -d)
git clone https://github.com/clawdbot/clawdbot.git $REVIEW_DIR
cd $REVIEW_DIR && gh pr checkout 130
bash workdir:$REVIEW_DIR background:true command:"codex review --base origin/main"
```

**为什么？** 在运行中的 Clawdbot 仓库中查看分支可能会导致系统崩溃！

---

## Claude 编码代理

```bash
bash workdir:~/project background:true command:"claude \"Your task\""
```

---

## Pi 编码代理

```bash
# Install: npm install -g @mariozechner/pi-coding-agent
bash workdir:~/project background:true command:"pi \"Your task\""
```

---

## Pi 命令参数（常用）

- `--print` / `-p`：非交互式模式；运行提示后退出。
- `--provider <名称>`：选择提供者（默认：google）。
- `--model <id>`：选择模型（默认：gemini-2.5-flash）。

示例：

```bash
# Set provider + model, non-interactive
bash workdir:~/project background:true command:"pi --provider openai --model gpt-4o-mini -p \"Summarize src/\""
```

---

## tmux（交互式会话）

对于交互式编码会话，请使用 tmux（除非是非常简单的单次操作）。对于非交互式运行，建议使用 bash 背景模式。

---

## 使用 git worktrees 和 tmux 并行修复问题

要并行修复多个问题，可以使用 git worktrees（隔离的分支）和 tmux 会话：

```bash
# 1. Clone repo to temp location
cd /tmp && git clone git@github.com:user/repo.git repo-worktrees
cd repo-worktrees

# 2. Create worktrees for each issue (isolated branches!)
git worktree add -b fix/issue-78 /tmp/issue-78 main
git worktree add -b fix/issue-99 /tmp/issue-99 main

# 3. Set up tmux sessions
SOCKET="${TMPDIR:-/tmp}/codex-fixes.sock"
tmux -S "$SOCKET" new-session -d -s fix-78
tmux -S "$SOCKET" new-session -d -s fix-99

# 4. Launch Codex in each (after pnpm install!)
tmux -S "$SOCKET" send-keys -t fix-78 "cd /tmp/issue-78 && pnpm install && codex --yolo 'Fix issue #78.'" Enter
tmux -S "$SOCKET" send-keys -t fix-99 "cd /tmp/issue-99 && pnpm install && codex --yolo 'Fix issue #99.'" Enter

# 5. Monitor progress
tmux -S "$SOCKET" capture-pane -p -t fix-78 -S -30

# 6. Cleanup
tmux -S "$SOCKET" kill-server
git worktree remove /tmp/issue-78
git worktree remove /tmp/issue-99
```

**为什么使用 worktrees？** 每个 Codex 都在隔离的分支中运行，不会产生冲突。可以同时运行多个修复任务！

---

## 指南

1. **尊重工具选择** — 如果用户请求使用 Codex，请使用 Codex。不要主动建议用户自行构建。
2. **保持耐心** — 即使会话运行缓慢，也不要强制关闭它们。
3. **使用 `process:log` 监控进度** — 在不干扰会话的情况下查看进度。
4. **使用 `--full-auto` 进行构建** — 自动批准更改。
5. **并行操作是可行的** — 可以同时运行多个 Codex 进程以批量处理任务。
6. **避免在 `~/clawd/**` 目录中启动 Codex** — 该目录可能包含敏感文档。请使用目标项目目录或 `/tmp` 作为临时工作区。
7. **避免在 `~/Projects/clawdbot/**` 目录中查看分支** — 该目录包含正在运行的实例。请克隆到 `/tmp` 或使用 git worktree 进行 PR 审查。

---

## 参考资料

- **Spec-Kit GitHub 仓库**：https://github.com/github/spec-kit
- **OpenCode CLI 文档**：https://opencode.ai/docs

### 相关工具

- **opencode-controller**：用于通过命令控制 OpenCode
- **freeride-opencode**：用于配置 OpenCode Zen 提供的免费模型