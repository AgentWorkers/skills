---
name: coding-agent
description: 通过后台进程运行 Codex CLI、Claude Code、Kiro CLI、OpenCode 或 Pi Coding Agent，以实现程序化的控制。
metadata:
  {
    "openclaw": { "emoji": "🧩", "requires": { "anyBins": ["claude", "codex", "opencode", "pi", "kiro-cli"] } },
  }
---
# 编码代理

您可以使用 bash 在 OpenClaw 中启动和管理 AI 编码代理（如 Codex、Claude Code、Kiro CLI、OpenCode、Pi），并控制它们的后台进程。

## 必需使用 PTY（伪终端）模式

编码代理是 **交互式终端应用程序**，需要一个伪终端（PTY）。如果没有 PTY，输出可能会中断或代理会挂起。

**请始终设置 `pty:true`：**

```bash
# Correct — with PTY
bash pty:true command:"codex exec 'Your prompt'"

# Wrong — agent may break or hang
bash command:"codex exec 'Your prompt'"
```

## 工具参考

### Bash 参数

| 参数 | 类型 | 描述 |
| ---- | ---- | --- |
| `command` | 字符串 | 要运行的 Shell 命令 |
| `pty` | 布尔值 | 分配一个伪终端（**编码代理必需**） |
| `workdir` | 字符串 | 工作目录（代理仅能看到这个文件夹） |
| `background` | 布尔值 | 在后台运行；返回 `sessionId` 以便监控 |
| `timeout` | 数字 | 超时时间（以秒为单位，超时后将终止进程） |
| `elevated` | 布尔值 | 在主机上运行（如果允许的话） |

### 进程操作（后台会话）

| 操作 | 描述 |
| ---- | --- |
| `list` | 列出所有正在运行/最近的会话 |
| `poll` | 检查会话是否仍在运行 |
| `log` | 获取会话输出（可选偏移量/限制） |
| `write` | 向标准输入发送原始数据（不添加换行符） |
| `submit` | 发送数据 + 换行符（类似于输入内容并按 Enter） |
| `send-keys` | 发送键码或十六进制字节 |
| `paste` | 粘贴文本（可选，需要括号） |
| `kill` | 终止会话 |

---

## 快速入门：一次性任务

```bash
# Codex needs a git repo — create a temp one for scratch work
SCRATCH=$(mktemp -d) && cd $SCRATCH && git init && codex exec "Your prompt"

# Run inside an existing project (with PTY)
bash pty:true workdir:~/project command:"codex exec 'Add error handling to the API calls'"
```

---

## 核心模式：workdir + background + pty

对于较长的任务，请结合这三个选项：

```bash
# 1. Start the agent
bash pty:true workdir:~/project background:true command:"codex exec --full-auto 'Build a snake game'"
# → returns sessionId

# 2. Monitor progress
process action:log sessionId:XXX

# 3. Check completion
process action:poll sessionId:XXX

# 4. Send input if the agent asks a question
process action:submit sessionId:XXX data:"yes"     # text + Enter
process action:write sessionId:XXX data:"y"         # raw keystroke

# 5. Kill if stuck
process action:kill sessionId:XXX
```

**为什么需要 `workdir`？** 代理会在指定的工作目录中启动，不会随意访问其他文件。

---

## Codex CLI

**默认模型：`gpt-5.2-codex`（在 `~/.codex/config.toml` 中设置）

### 标志

| 标志 | 效果 |
| ---- | --- |
| `exec "prompt"` | 一次性执行，执行完成后退出 |
| `--full-auto` | 在沙箱环境中运行，自动批准请求 |
| `--yolo` | 不使用沙箱，不进行自动批准（最快，但最危险） |

### 构建/创建

```bash
# One-shot with auto-approve
bash pty:true workdir:~/project command:"codex exec --full-auto 'Build a dark mode toggle'"

# Background for longer work
bash pty:true workdir:~/project background:true command:"codex --yolo 'Refactor the auth module'"
```

### 审查 PR（Pull Request）

**切勿在 OpenClaw 的项目文件夹中直接审查 PR。** 请将其克隆到临时目录或使用 git 工作树。

```bash
# Clone to temp
REVIEW_DIR=$(mktemp -d)
git clone https://github.com/user/repo.git $REVIEW_DIR
cd $REVIEW_DIR && gh pr checkout 130
bash pty:true workdir:$REVIEW_DIR command:"codex review --base origin/main"

# Or use git worktree (keeps main intact)
git worktree add /tmp/pr-130-review pr-130-branch
bash pty:true workdir:/tmp/pr-130-review command:"codex review --base main"
```

### 批量审查 PR

```bash
# Fetch all PR refs
git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'

# Launch one Codex per PR (all background + PTY)
bash pty:true workdir:~/project background:true command:"codex exec 'Review PR #86. git diff origin/main...origin/pr/86'"
bash pty:true workdir:~/project background:true command:"codex exec 'Review PR #87. git diff origin/main...origin/pr/87'"

# Monitor
process action:list

# Post results
gh pr comment <PR#> --body "<review content>"
```

---

## Claude Code

```bash
# One-shot
bash pty:true workdir:~/project command:"claude 'Your task'"

# Background
bash pty:true workdir:~/project background:true command:"claude 'Your task'"
```

---

## Kiro CLI（AWS）

Kiro 是一个 AWS AI 编码助手，支持会话持久化、自定义代理、技能、钩子、规划模式以及与 MCP 的集成。

**安装：** https://kiro.dev/docs/cli/installation

### 基本用法

```bash
kiro-cli                           # Interactive chat (default)
kiro-cli chat "Your question"      # Direct question
kiro-cli --agent my-agent          # Use a specific agent
kiro-cli chat --resume             # Resume last session (per-directory)
kiro-cli chat --resume-picker      # Pick from saved sessions
kiro-cli chat --list-sessions      # List all sessions
```

### 非交互式模式

用于脚本编写和自动化——向标准输出输出一个响应后退出。

```bash
# Single response
kiro-cli chat --no-interactive "Show current directory"

# Trust all tools (no confirmation prompts)
kiro-cli chat --no-interactive --trust-all-tools "Create hello.py"

# Trust specific tools only
kiro-cli chat --no-interactive --trust-tools "fs_read,fs_write" "Read package.json"
```

**工具信任设置：** 使用 `--trust-all-tools` 进行完全自动化。对于不可信的输入，使用 `--trust-tools "fs_read,fs_write,shell"` 来限制工具权限。

### OpenClaw 集成

```bash
# Interactive session (background)
bash pty:true workdir:~/project background:true command:"kiro-cli"

# One-shot query (non-interactive)
bash pty:true workdir:~/project command:"kiro-cli chat --no-interactive --trust-all-tools 'List all TODO comments in src/'"

# With a specific agent
bash pty:true workdir:~/project background:true command:"kiro-cli --agent aws-expert 'Set up Lambda'"

# Resume previous session
bash pty:true workdir:~/project command:"kiro-cli chat --resume"
```

### 技能（Agent Skills）

技能是 **可移植的指令包**，用于扩展 Kiro 的功能。当请求与技能描述匹配时，Kiro 会自动加载并执行相应的指令——无需使用 `/` 命令。

#### 技能的位置

| 位置 | 作用范围 | 备注 |
| --- | --- | --- |
| `.kiro/skills/<name>/` | 工作区（特定项目） | 通过版本控制共享 |
| `~/.kiro/skills/<name>/` | 全局（所有项目） | 个人工作流程 |

当名称相同的情况下，工作区中的技能优先被使用。

#### 创建技能

技能是一个包含 `SKILL.md` 文件的文件夹：

```
my-skill/
├── SKILL.md          # Required — frontmatter + instructions
└── references/       # Optional — detailed docs loaded on demand
    └── guide.md
```

**SKILL.md 格式：**

````markdown
---
name: pr-review
description: Review pull requests for code quality, security issues, and test coverage.
---

## Review checklist

1. Check for vulnerabilities, injection risks, exposed secrets
2. Verify edge cases and failure modes are handled
3. Confirm new code has appropriate tests

For detailed patterns, see `references/guide.md`.
````

- **`name`** — 技能的唯一标识符。
- **`description`** — 决定 Kiro 何时激活该技能。描述要具体明确，并包含与请求匹配的关键词。
- **参考文件** — 存储在 `references/` 目录中。Kiro 仅会在指令中明确要求时才会加载这些文件。

#### 在自定义代理中使用技能

默认代理会自动发现技能。自定义代理需要明确声明所需使用的技能：

```json
{
  "name": "my-agent",
  "resources": [
    "skill://.kiro/skills/*/SKILL.md",
    "skill://~/.kiro/skills/*/SKILL.md"
  ]
}
```

#### 技能的最佳实践

- **精确的描述** — 如 “审查 Pull Request 以检测安全漏洞和测试覆盖率” 可靠地触发技能；“帮助代码审查” 则不会触发。
- **保持 SKILL.md 文件的可操作性** — 将冗长的参考资料放在 `references/` 文件中。
- **正确的适用范围** — 全局技能适用于个人工作流程；工作区技能适用于团队/项目规范。
- **版本控制** — 提交 `.kiro/skills/` 文件，以便团队共享相同的工作流程。
- **检查可用性** — 使用 `/context show` 查看当前会话中加载了哪些技能。

### 规划模式（Plan Agent）

Plan Agent 是一个 **只读的代理**，用于在执行前进行结构化规划。它通过交互式工作流程将想法转化为详细的实施计划。

#### 适用场景

- 复杂的多步骤任务（例如，“构建用户认证系统”）
- 需要细化的不明确或不断变化的需求
- 需要在编码前进行任务分解的大型项目

#### 不适用场景

- 简单的查询或单步任务
- 用户已有明确的具体指令
- 快速修复或小规模修改

#### 如何进入规划模式

```bash
# Slash command
> /plan

# With an immediate prompt
> /plan Build a REST API for user authentication

# Keyboard shortcut (toggles plan ↔ execution)
Shift + Tab
```

当 Plan Agent 活动时，提示符会显示 `[plan]` 标志。

#### 规划工作流程（4 个阶段）

1. **需求收集** — 通过结构化的问题来明确您的想法。使用 `1=a, 2=b` 的语法或自由文本回答。
2. **研究与分析** — 利用代码智能、grep 和 glob 工具来分析代码库。
3. **实施计划** — 生成包含明确目标、实施指南和每个任务演示描述的详细计划。
4. **审批与移交** — 您审核计划。如果批准（输入 `y`），计划会自动传递给执行代理。

**注意：Plan Agent 是只读的**——它可以读取文件、搜索代码和进行研究，但在移交之前不能写入文件或执行命令。

#### OpenClaw 中的规划模式集成

对于交互式规划会话，请在后台运行 Kiro 并传递 `/plan` 命令：

```bash
# Start interactive Kiro session
bash pty:true workdir:~/project background:true command:"kiro-cli chat --trust-all-tools"

# Enter planning mode
process action:submit sessionId:XXX data:"/plan Build a REST API for user authentication"

# Relay the user's answers to requirement questions
process action:submit sessionId:XXX data:"1=a, 2=d I'm using Rust with Axum"

# Approve the plan
process action:submit sessionId:XXX data:"y"

# Monitor output
process action:log sessionId:XXX
```

#### 规划会话示例

```
> /plan Add user authentication to my web app

[plan] > I understand you want to add user authentication.
[1]: What authentication method?
  a. Email/Password   b. OAuth   c. Magic Links   d. Multi-factor
> 1=a

[plan] > Great! Email/password it is.
[2]: What's your tech stack?
  a. React + Node.js   b. Next.js   c. Django/Flask   d. Other
> 2=d, I'm using Rust with Axum

[plan] > Researching Axum authentication patterns...

**Implementation Plan — User Authentication System**
[Detailed task breakdown...]

Does this plan look good? Ready to exit [plan] agent? [y/n]: y
[default] > Implement this plan: [Plan transferred]
```

### 钩子（Hooks）

钩子在代理生命周期和工具执行的特定时刻执行自定义命令。这些钩子在代理配置文件中定义。

#### 钩子类型

| 钩子 | 触发条件 | 是否会阻止工具执行？ |
| ---- | ---- | ---- |
| `AgentSpawn` | 代理启动时 | 不会 |
| `UserPromptSubmit` | 用户发送提示时 | 不会 |
| `PreToolUse` | 工具运行前 | 会（返回退出代码 2） |
| `PostToolUse` | 工具运行后 | 不会 |
| `Stop` | 代理完成一个步骤时 | 不会 |

#### 退出代码

- **0** — 成功。输出内容会被捕获（添加到 AgentSpawn/UserPromptSubmit 的上下文中）。
- **2** — （仅限 PreToolUse）阻止工具执行；错误信息会返回给大型语言模型（LLM）。
- **其他** — 失败。错误信息会以警告的形式显示给用户。

#### 工具匹配

使用 `matcher` 字段来指定目标工具：

| 匹配器 | 匹配条件 |
| ---- | ---- |
| `"fs_write"` 或 `"write"` | 写入工具 |
| `"execute_bash"` 或 `"shell"` | Shell 执行 |
| `"@git"` | 所有来自 git MCP 服务器的工具 |
| `"@git/status"` | 特定的 MCP 工具 |
| `"*"` | 所有工具（内置工具 + MCP 工具） |
| `"@builtin"` | 仅限内置工具 |

#### 配置

- **`timeout_ms` | 默认值 30,000 毫秒（30 秒） |
- **`cache_ttl_seconds` | `0` = 不缓存（默认）；`> 0` = 缓存成功的结果。AgentSpawn 的钩子永远不会被缓存。

有关完整语法，请参阅 [代理配置参考](https://kiro.dev/docs/cli/custom-agents/configuration-reference)。

### 子代理（Subagents）

Kiro 可以将任务委托给 **子代理**——这些子代理具有独立的上下文，可以自主运行并返回结果。

```bash
> Use the backend agent to refactor the payment module
```

**主要功能：**
- 具有独立上下文的自主执行
- 实时进度跟踪
- 多任务并行执行
- 适用于特定工作流程的自定义代理配置

**子代理可使用的工具：** read、write、shell、代码智能、MCP 工具。
**不可使用的工具：** web_search、web_fetch、use_aws、grep、glob、thinking、todo_list。

### 自定义代理（Custom Agents）

预先定义工具权限、上下文资源和行为：

```bash
kiro-cli agent list              # List available agents
kiro-cli agent create my-agent   # Create new agent
kiro-cli agent edit my-agent     # Edit agent config
kiro-cli agent validate ./a.json # Validate config file
kiro-cli agent set-default my-agent
```

**优势：** 预先批准工具的使用权限；限制工具访问；自动加载项目文档；可共享的团队配置。

### 指导（Project Context）

通过 markdown 文件提供持久的项目信息：

| 路径 | 作用范围 |
| ---- | ---- |
| `.kiro/steering/` | 仅适用于当前项目 |
| `~/.kiro/steering/` | 全局（所有项目） |

示例结构：

```
.kiro/steering/
├── product.md           # Product overview
├── tech.md              # Tech stack
├── structure.md         # Project structure
└── api-standards.md     # API conventions
```

也可以在项目根目录或 `~/.kiro/steering/` 中创建 `AGENTS.md` 文件。

**在自定义代理中：** 在配置文件中添加 `"resources": ["file://.kiro/steering/**/*.md"]`。

### MCP 集成

通过 Model Context Protocol 连接外部工具和数据源：

```bash
kiro-cli mcp add --name my-server --command "node server.js" --scope workspace
kiro-cli mcp list [workspace|global]
kiro-cli mcp status --name my-server
kiro-cli mcp remove --name my-server --scope workspace
```

---

## OpenCode

```bash
bash pty:true workdir:~/project command:"opencode run 'Your task'"
```

---

## Pi 编码代理

```bash
# Install: npm install -g @mariozechner/pi-coding-agent

# Interactive
bash pty:true workdir:~/project command:"pi 'Your task'"

# Non-interactive (single response)
bash pty:true command:"pi -p 'Summarize src/'"

# Different provider/model
bash pty:true command:"pi --provider openai --model gpt-4o-mini -p 'Your task'"
```

---

## 并行问题修复（git 工作树）

使用隔离的工作树同时修复多个问题：

```bash
# 1. Create worktrees
git worktree add -b fix/issue-78 /tmp/issue-78 main
git worktree add -b fix/issue-99 /tmp/issue-99 main

# 2. Launch agents (background + PTY)
bash pty:true workdir:/tmp/issue-78 background:true command:"pnpm install && codex --yolo 'Fix issue #78: <description>. Commit and push.'"
bash pty:true workdir:/tmp/issue-99 background:true command:"pnpm install && codex --yolo 'Fix issue #99: <description>. Commit and push.'"

# 3. Monitor
process action:list
process action:log sessionId:XXX

# 4. Create PRs
cd /tmp/issue-78 && git push -u origin fix/issue-78
gh pr create --repo user/repo --head fix/issue-78 --title "fix: ..." --body "..."

# 5. Clean up
git worktree remove /tmp/issue-78
git worktree remove /tmp/issue-99
```

---

## 规则

1. **始终使用 `pty:true`** — 编码代理需要一个伪终端。
2. **尊重用户的选择** — 如果用户请求使用 Kiro，就使用 Kiro；如果请求使用 Codex，就使用 Codex。在协调代理时不要手动编写代码补丁。如果代理失败或挂起，重新启动它或询问用户，不要擅自接管。
3. **要有耐心** — 不要因为会话运行缓慢就终止它们。
4. **使用 `process:log` 监控进度** — 在不干扰的情况下检查进度。
5. **Codex 的自动批准选项** — 使用 `--full-auto`（在沙箱环境中）或 `--yolo`（不使用沙箱）来执行任务。
6. **Kiro 的工具信任设置** — 使用 `--trust-all-tools` 进行自动化；使用 `--trust-tools` 来限制工具权限。
7. **对于一次性任务，使用 `--no-interactive`**。
8. **并行执行是可行的** — 可以同时运行多个代理进程来处理批量任务。
9. **不要在 `~/clawd/` 目录下启动代理** — 代理会读取系统文档，可能导致不可预测的行为。
10. **不要在 `~/Projects/openclaw/` 目录下检出分支** — 那里是 OpenClaw 的实时实例。
11. **对于复杂任务，建议使用 Kiro 的 `plan` 功能** — 当需求不明确或多步骤时，建议使用 Plan Agent 并让用户做出选择。
12. **利用 Kiro 的技能** — 如果项目有 `.kiro/skills/` 文件或用户有 `~/.kiro/skills/` 文件，相关技能会自动激活。无需额外设置标志。

---

## 进度更新

在后台启动编码代理时，要及时通知用户：

- **启动时** — 发送一条简短消息：正在运行的代理、位置以及代理的名称。
- **发生变化时** — 仅在以下情况下更新：
  - 里程碑完成（构建完成、测试通过）
  - 代理需要用户输入或提问
  - 发生错误或需要用户操作
  - 代理完成（包括更改的内容和位置）
- **终止代理时** — 立即告知用户代理已被终止及其原因。

---

## 完成后自动通知

对于长时间运行的任务，添加一个唤醒触发器，以便在代理完成时立即通知 OpenClaw：

```
... your task here.

When completely finished, run this command to notify me:
openclaw gateway wake --text "Done: [brief summary]" --mode now
```

**示例：**

```bash
bash pty:true workdir:~/project background:true command:"codex --yolo exec 'Build a REST API for todos.

When completely finished, run: openclaw gateway wake --text \"Done: Built todos REST API with CRUD endpoints\" --mode now'"
```

这样可以在代理完成时立即触发通知，而无需等待下一次心跳信号。

---

## 经验总结

- **PTY 是必不可少的** — 没有 `pty:true`，输出可能会中断或代理会挂起。
- **Codex 需要 Git 仓库** — 对于临时工作，可以使用 `mktemp -d && git init` 命令。
- **一次性任务的使用** — 使用 `codex exec "prompt"` 可以干净地执行并立即退出。
- **`submit` 与 `write` 的区别** — `submit` 会发送输入内容及换行符；`write` 会直接发送原始数据（不添加换行符）。
- **技能会自动激活** — 无需使用 `/` 命令；Kiro 会根据请求描述自动选择合适的技能。
- **在复杂任务前进行规划** — 使用 `/plan` 可以在开始之前明确需求，从而节省时间。