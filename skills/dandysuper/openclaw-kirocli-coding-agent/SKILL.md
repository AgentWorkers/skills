---
name: coding-agent
description: 通过后台进程运行 Codex CLI、Claude Code、Kiro CLI、OpenCode 或 Pi Coding Agent，以实现程序化的控制。
metadata:
  {
    "openclaw": { "emoji": "🧩", "requires": { "anyBins": ["claude", "codex", "opencode", "pi", "kiro-cli"] } },
  }
---
# 编码代理（优先使用 bash）

所有编码代理任务均使用 **bash**（支持后台模式）进行。简单且高效。

## ⚠️ 必须启用 PTY 模式！

编码代理（如 Codex、Claude Code、Kiro、Pi）是 **交互式终端应用程序**，需要伪终端（PTY）才能正常工作。如果没有 PTY，输出可能会出现问题、颜色显示不正常，或者代理程序可能会挂起。

在运行编码代理时，**务必设置 `pty:true`**：

```bash
# ✅ Correct - with PTY
bash pty:true command:"codex exec 'Your prompt'"

# ❌ Wrong - no PTY, agent may break
bash command:"codex exec 'Your prompt'"
```

### Bash 工具参数

| 参数          | 类型        | 描述                                                                 |
|---------------|------------|---------------------------------------------------------------------------|
| `command`       | 字符串      | 要执行的 shell 命令                                      |
| `pty`          | 布尔值       | 用于编码代理！为交互式 CLI 分配伪终端                         |
| `workdir`       | 字符串      | 工作目录（代理仅能看到该目录下的内容）                          |
| `background`      | 布尔值       | 在后台运行，并返回 sessionId 以便监控                               |
| `timeout`       | 数字        | 超时时间（秒）；超时后终止进程                               |
| `elevated`      | 布尔值       | 在主机上运行（如果允许的话）                                   |

### 进程工具操作（用于后台会话）

| 操作            | 描述                                      |
|-----------------|----------------------------------------------------|
| `list`          | 列出所有正在运行或最近的会话                              |
| `poll`          | 检查会话是否仍在运行                                |
| `log`           | 获取会话输出（可指定偏移量/限制）                           |
| `write`          | 向标准输入发送原始数据                               |
| `submit`        | 发送数据并附加换行符                              |
| `send-keys`       | 发送键值对或十六进制字节                             |
| `paste`          | 粘贴文本（支持带括号的模式）                             |
| `kill`          | 终止会话                                    |

---

## 快速入门：一次性任务

对于简单的提示/聊天，可以创建一个临时 git 仓库并运行以下命令：

```bash
# Quick chat (Codex needs a git repo!)
SCRATCH=$(mktemp -d) && cd $SCRATCH && git init && codex exec "Your prompt here"

# Or in a real project - with PTY!
bash pty:true workdir:~/Projects/myproject command:"codex exec 'Add error handling to the API calls'"
```

**为什么需要使用 git init？** 因为 Codex 只能在受信任的 git 目录中运行。创建临时仓库可以解决这个问题，方便进行临时性的工作。

---

## 使用模式：`workdir + background + pty`

对于较长的任务，建议使用后台模式并启用 PTY：

```bash
# Start agent in target directory (with PTY!)
bash pty:true workdir:~/project background:true command:"codex exec --full-auto 'Build a snake game'"
# Returns sessionId for tracking

# Monitor progress
process action:log sessionId:XXX

# Check if done
process action:poll sessionId:XXX

# Send input (if agent asks a question)
process action:write sessionId:XXX data:"y"

# Submit with Enter (like typing "yes" and pressing Enter)
process action:submit sessionId:XXX data:"yes"

# Kill if needed
process action:kill sessionId:XXX
```

**为什么工作目录很重要？** 代理程序会在指定的工作目录中运行，不会随意访问其他文件（比如你的 `soul.md` 文件 😅）。

---

## Codex CLI

**默认模型：** `gpt-5.2-codex`（配置在 `~/.codex/config.toml` 中）

### 标志参数

| 标志            | 功能                                      |
|-----------------|-----------------------------------------|
| `exec "prompt"`     | 执行一次性任务，完成后退出                          |
| `--full-auto`     | 在沙箱环境中运行，但会自动批准请求                   |
| `--yolo`        | 不使用沙箱环境，不进行任何验证（最快但最危险的方式）           |

### 构建/创建新代理

```bash
# Quick one-shot (auto-approves) - remember PTY!
bash pty:true workdir:~/project command:"codex exec --full-auto 'Build a dark mode toggle'"

# Background for longer work
bash pty:true workdir:~/project background:true command:"codex --yolo 'Refactor the auth module'"
```

### 审查 Pull Request（PR）

**⚠️ 重要提示：** **切勿在 OpenClaw 的项目文件夹内直接审查 PR！**  
请将 PR 克隆到临时文件夹或使用 git worktree 进行审查。

```bash
# Clone to temp for safe review
REVIEW_DIR=$(mktemp -d)
git clone https://github.com/user/repo.git $REVIEW_DIR
cd $REVIEW_DIR && gh pr checkout 130
bash pty:true workdir:$REVIEW_DIR command:"codex review --base origin/main"
# Clean up after: trash $REVIEW_DIR

# Or use git worktree (keeps main intact)
git worktree add /tmp/pr-130-review pr-130-branch
bash pty:true workdir:/tmp/pr-130-review command:"codex review --base main"
```

### 批量审查 Pull Request（并行处理）

```bash
# Fetch all PR refs first
git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'

# Deploy the army - one Codex per PR (all with PTY!)
bash pty:true workdir:~/project background:true command:"codex exec 'Review PR #86. git diff origin/main...origin/pr/86'"
bash pty:true workdir:~/project background:true command:"codex exec 'Review PR #87. git diff origin/main...origin/pr/87'"

# Monitor all
process action:list

# Post results to GitHub
gh pr comment <PR#> --body "<review content>"
```

---

## Claude Code

```bash
# With PTY for proper terminal output
bash pty:true workdir:~/project command:"claude 'Your task'"

# Background
bash pty:true workdir:~/project background:true command:"claude 'Your task'"
```

---

## Kiro CLI（AWS）

Kiro 是一个基于 AWS 的 AI 编码助手，支持会话持久化、自定义代理、任务指导以及与 MCP 的集成。

**安装方式：** https://kiro.dev/docs/cli/installation

### 基本用法

```bash
kiro-cli                           # Start interactive chat (default)
kiro-cli chat "Your question"      # Direct question
kiro-cli --agent my-agent          # Use specific agent
kiro-cli chat --resume             # Resume last session (per-directory)
kiro-cli chat --resume-picker      # Pick from saved sessions
kiro-cli chat --list-sessions      # List all sessions
```

### 非交互式模式（脚本/自动化）

```bash
# Single response to STDOUT, then exit
kiro-cli chat --no-interactive "Show current directory"

# Trust all tools (no confirmation prompts)
kiro-cli chat --no-interactive --trust-all-tools "Create hello.py"

# Trust specific tools only (comma-separated)
kiro-cli chat --no-interactive --trust-tools "fs_read,fs_write" "Read package.json"
```

**🔐 工具信任设置：**  
使用 `--trust-all-tools` 可以启用自动化功能（默认设置）。对于不可信的输入或敏感系统，可以使用 `--trust-tools "fs_read,fs_write,shell"` 来限制工具的权限。

### OpenClaw 集成

```bash
# Interactive session (background)
bash pty:true workdir:~/project background:true command:"kiro-cli"

# One-shot query (non-interactive)
bash pty:true workdir:~/project command:"kiro-cli chat --no-interactive --trust-all-tools 'List all TODO comments in src/'"

# With specific agent
bash pty:true workdir:~/project background:true command:"kiro-cli --agent aws-expert 'Set up Lambda'"

# Resume previous session
bash pty:true workdir:~/project command:"kiro-cli chat --resume"
```

### 自定义代理

预先定义工具的权限、上下文资源及行为：

```bash
kiro-cli agent list              # List available agents
kiro-cli agent create my-agent   # Create new agent
kiro-cli agent edit my-agent     # Edit agent config
kiro-cli agent validate ./a.json # Validate config file
kiro-cli agent set-default my-agent  # Set default
```

**好处：**  
- 预先批准可信任的工具；  
- 限制工具的访问权限；  
- 自动加载项目文档；  
- 在团队间共享配置文件。

### 任务指导（项目上下文）

通过 `.kiro/steering/` 目录中的 markdown 文件提供持久化的任务指导信息：

```
.kiro/steering/
├── product.md       # Product overview
├── tech.md          # Tech stack
├── structure.md     # Project structure
└── api-standards.md # API conventions
```

- **工作区指导：** `.kiro/steering/` 仅适用于当前项目；  
- **全局指导：`~/.kiro/steering/` 适用于所有项目；  
- **AGENTS.md 文件的放置位置：** 可放在项目根目录或 `~/.kiro/steering/` 下。  

**在自定义代理中配置：** 在配置文件中添加 `"resources": ["file://.kiro/steering/**/*.md"]`。

### MCP 集成

通过 Model Context Protocol 连接外部工具和数据源：

```bash
kiro-cli mcp add --name my-server --command "node server.js" --scope workspace
kiro-cli mcp list [workspace|global]
kiro-cli mcp status --name my-server
kiro-cli mcp remove --name my-server --scope workspace
```

### Plan Agent

Plan Agent 是一个内置的代理工具，用于在执行任务前进行结构化的规划。它可以帮助将想法转化为详细的实施计划。

**何时建议使用 Plan Agent：**  
- 需要处理复杂的多步骤任务（例如构建用户认证系统）；  
- 需要明确或澄清需求；  
- 需要对任务进行分解的大型项目。  

**何时不使用 Plan Agent：**  
- 对于简单的查询或单步骤任务；  
- 用户已有明确的具体指令；  
- 需要快速修复或进行小规模修改的任务。  

**使用方法：**  
（此处应提供具体的使用步骤。）

**Plan Agent 的工作流程（4 个阶段）：**  
1. **需求收集** — 通过结构化的问题收集用户需求；  
2. **研究与分析** — 查阅代码库、分析现有模式；  
3. **实施计划** — 制定详细的任务分解方案；  
4. **移交执行** — 得到用户批准后，将计划传递给执行代理。  

**Plan Agent 的限制：**  
- 可以读取文件、搜索代码、查阅文档；  
- 无法写入文件或执行命令（直到任务移交给执行代理）。  

---

## OpenCode

```bash
bash pty:true workdir:~/project command:"opencode run 'Your task'"
```

---

## Pi 编码代理

```bash
# Install: npm install -g @mariozechner/pi-coding-agent
bash pty:true workdir:~/project command:"pi 'Your task'"

# Non-interactive mode (PTY still recommended)
bash pty:true command:"pi -p 'Summarize src/'"

# Different provider/model
bash pty:true command:"pi --provider openai --model gpt-4o-mini -p 'Your task'"
```

**注意：** Pi 现在已启用了 Anthropic 提示缓存功能（PR #584，2026 年 1 月合并！）

---

## 使用 git worktree 并行修复多个问题

要同时修复多个问题，可以使用 git worktree：

```bash
# 1. Create worktrees for each issue
git worktree add -b fix/issue-78 /tmp/issue-78 main
git worktree add -b fix/issue-99 /tmp/issue-99 main

# 2. Launch agent in each (background + PTY!)
bash pty:true workdir:/tmp/issue-78 background:true command:"pnpm install && codex --yolo 'Fix issue #78: <description>. Commit and push.'"
bash pty:true workdir:/tmp/issue-99 background:true command:"pnpm install && codex --yolo 'Fix issue #99: <description>. Commit and push.'"

# 3. Monitor progress
process action:list
process action:log sessionId:XXX

# 4. Create PRs after fixes
cd /tmp/issue-78 && git push -u origin fix/issue-78
gh pr create --repo user/repo --head fix/issue-78 --title "fix: ..." --body "..."

# 5. Cleanup
git worktree remove /tmp/issue-78
git worktree remove /tmp/issue-99
```

---

## 规则说明：

1. **务必启用 `pty:true`** — 编码代理需要伪终端；  
2. **尊重用户的选择** — 用户请求使用 Kiro 时使用 Kiro，请求使用 Codex 时使用 Codex；  
   - 不要手动编写补丁；  
   - 如果代理程序失败或挂起，重新启动它或询问用户下一步操作，切勿擅自接管；  
3. **保持耐心** — 不要因为会话运行缓慢就终止它；  
4. **使用 `process:log` 监控进程进度** — 在不干扰会话的情况下查看进度；  
5. **使用 `--full-auto` 或 `--yolo` 配置 Codex** — 自动批准更改；  
6. **对于 Kiro 的自动化操作，使用 `--trust-all-tools`** — 跳过确认提示；  
7. **对于 Kiro 的一次性任务，使用 `--no-interactive`** — 采用单次响应模式；  
8. **可以并行运行多个代理进程** — 适用于批量处理任务；  
9. **切勿在 `~/clawd/**` 目录下启动代理** — 那里存放的是 OpenClaw 的核心配置文件；  
10. **切勿在 `~/Projects/openclaw/**` 目录下检出分支** — 那里是 OpenClaw 的实时运行环境！  
11. **对于复杂任务，建议使用 Kiro 或 Plan Agent** — 当需求不明确或任务涉及多个步骤时，建议用户使用 Plan Agent 并由用户自行决定。  

---

## 进度更新（非常重要）

在后台运行编码代理时，要随时让用户了解进度：

- 启动代理时发送一条简短的消息，说明正在运行的任务及位置；  
- 仅在以下情况下再次更新：  
  - 任务完成（例如构建完成、测试通过）；  
  - 代理需要用户输入；  
  - 出现错误或需要用户操作；  
  - 代理任务完成（说明具体变更内容及位置）。  
- 如果终止了会话，立即告知用户原因。  

这样可以避免用户看到“代理失败”后却不知道具体发生了什么的情况。

---

## 完成任务后自动通知用户

对于长时间运行的后台任务，可以在提示信息中添加一个唤醒触发器，以便 OpenClaw 在代理任务完成后立即收到通知（而不是等待下一次心跳信号）：

```
... your task here.

When completely finished, run this command to notify me:
openclaw gateway wake --text "Done: [brief summary of what was built]" --mode now
```

**示例（使用 Codex）：**

```bash
bash pty:true workdir:~/project background:true command:"codex --yolo exec 'Build a REST API for todos.

When completely finished, run: openclaw gateway wake --text \"Done: Built todos REST API with CRUD endpoints\" --mode now'"
```

这样可以在几秒钟内收到通知，而不会等待 10 分钟。

---

## 2026 年 1 月的经验总结：  
- **PTY 的重要性**：编码代理是交互式终端应用程序，必须启用 `pty:true`；  
- **必须使用 git 仓库**：Codex 无法在非 git 目录中运行；  
- `exec` 参数非常实用：`codex exec "prompt"` 可快速执行任务并干净地退出；  
- **`submit` 与 `write` 的区别**：使用 `submit` 时需要输入换行符，`write` 用于发送原始数据；  
- **Sass 的使用建议**：Codex 对于创意性提示响应良好。例如，当要求它写一首关于“第二把椅子”的俳句时，它给出了这样的回答：_“Second chair, I code / Space lobster sets the tempo / Keys glow, I follow”_ 🦞