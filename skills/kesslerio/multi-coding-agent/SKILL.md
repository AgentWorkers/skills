---
name: coding-agent
description: 通过后台进程运行 Codex CLI、Claude Code、OpenCode 或 Pi Coding Agent，以实现程序化的控制。
metadata: {"moltbot":{"emoji":"🧩","requires":{"anyBins":["claude","codex","opencode","pi"]}}}
---

# 编码代理（优先使用 bash）

所有编码代理任务均使用 **bash**（支持后台模式）来完成。简单且高效。

## ⚠️ 必须启用 PTY 模式！

编码代理（如 Codex、Claude Code、Pi）是 **交互式终端应用程序**，需要伪终端（PTY）才能正常运行。如果没有 PTY，可能会导致输出异常、颜色显示缺失或代理程序挂起。

**运行编码代理时，请始终设置 `pty:true`：**

```bash
# ✅ Correct - with PTY
bash pty:true command:"codex exec 'Your prompt'"

# ❌ Wrong - no PTY, agent may break
bash command:"codex exec 'Your prompt'"
```

### Bash 工具参数

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `command` | 字符串 | 要执行的 shell 命令 |
| `pty` | 布尔值 | **用于编码代理**：为交互式 CLI 分配伪终端 |
| `workdir` | 字符串 | 工作目录（代理仅识别该目录下的文件） |
| `background` | 布尔值 | 在后台运行，并返回会话 ID 以便监控 |
| `timeout` | 数字 | 超时时间（秒）（超时后终止进程） |
| `elevated` | 布尔值 | 在主机上运行（如果允许的话） |

### 进程工具操作（用于后台会话）

| 操作 | 描述 |
|--------|-------------|
| `list` | 列出所有正在运行或最近运行的会话 |
| `poll` | 检查会话是否仍在运行 |
| `log` | 获取会话输出（可指定偏移量或限制） |
| `write` | 向标准输入发送原始数据 |
| `submit` | 发送数据并附加换行符（类似于手动输入并按下 Enter 键） |
| `send-keys` | 发送键值或十六进制字节 |
| `paste` | 粘贴文本（可指定括号模式） |
| `kill` | 终止会话 |

---

## 快速启动：一次性任务

对于简单的提示或聊天，可以创建一个临时 git 仓库并执行以下操作：

```bash
# Quick chat (Codex needs a git repo!)
SCRATCH=$(mktemp -d) && cd $SCRATCH && git init && codex exec "Your prompt here"

# Or in a real project - with PTY!
bash pty:true workdir:~/Projects/myproject command:"codex exec 'Add error handling to the API calls'"
```

**为什么需要使用 git init？** 因为 Codex 只能在受信任的 git 目录中运行。创建临时仓库可以解决这个问题，方便进行临时性的工作。

---

## 使用模式：`workdir + background + pty`

对于较长的任务，请启用后台模式并使用 PTY：

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

**工作目录的重要性：** 代理会在指定的目录中运行，不会读取无关的文件（例如你的 `soul.md` 文件）。

---

## 备用策略

当主要代理达到使用限制时，按以下顺序切换代理：

| 优先级 | 代理 | 使用场景 |
|----------|-------|-------------|
| 1 | **Codex** | 默认的编码任务代理 |
| 2 | **Claude Code** | 当 Codex 使用受限或出现错误时 |
| 3 | **Gemini** | 当 Claude 不可用或需要执行 Gemini 特定任务时 |
| 4 | **Pi/OpenCode** | 当上述代理都不可用时 |

**需要切换代理的提示：**
- “您已达到使用限制”
- 出现速率限制错误（429 错误）
- 模型过载提示

---

## Codex CLI

**默认模型：** `gpt-5.2-codex`（配置在 `~/.codex/config.toml` 中）

### 标志参数

| 标志 | 功能 |
|------|--------|
| `exec "prompt"` | 一次性执行命令，执行完成后退出 |
| `--full-auto` | 在沙箱环境中运行，但会自动批准请求 |
| `--yolo` | 不使用沙箱环境，不进行任何审批（最快，但风险最高） |

### 构建/创建代理

```bash
# Quick one-shot (auto-approves) - remember PTY!
bash pty:true workdir:~/project command:"codex exec --full-auto 'Build a dark mode toggle'"

# Background for longer work
bash pty:true workdir:~/project background:true command:"codex --yolo 'Refactor the auth module'"
```

### 审查 Pull Request（PR）

**⚠️ 重要提示：** **绝不要在 Moltbot 的项目目录中审查 PR！**  
请将 PR 克隆到临时文件夹或使用 git worktree。

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

### 批量审阅 PR（并行处理）

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

**当 Codex 不可用时的备用方案**

| Codex 操作 | Claude 的对应操作 |
|-------|-------------------|
| `codex exec "prompt"` | `claude -p "prompt"` |
| `codex --full-auto` | `claude -p --permission-mode acceptEdits` |
| `codex --yolo` | `claude -p --dangerously-skip-permissions` |

**详细文档：** 请参阅 `references/claude-code.md`。

---

## Gemini CLI

**使用不同模型的备用方案**

| Codex 操作 | Gemini 的对应操作 |
|-------|-------------------|
| `codex exec "prompt"` | `gemini "prompt"` |
| `codex --full-auto` | `gemini --approval-mode auto_edit "prompt"` |
| `codex --yolo` | `gemini -y "prompt"` |

**详细文档：** 请参阅 `references/gemini-cli.md`。

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

**注意：** Pi 现在已启用 Anthropic 提示缓存功能（PR #584，2026 年 1 月合并！）

---

## 使用 git worktree 并行修复问题

要同时修复多个问题，可以使用 git worktree：

```bash
# 1. Create worktrees for each issue
git worktree add -b fix/issue-78 /tmp/issue-78 main
git worktree add -b fix/issue-99 /tmp/issue-99 main

# 2. Launch Codex in each (background + PTY!)
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

## tmux 配置（高级多代理管理）

对于复杂的多代理管理，建议使用 **tmux** 而不是简单的 bash 后台模式。

### 使用 tmux 与 bash 后台的场景对比

| 使用场景 | 推荐方案 |
|----------|-------------|
| 快速的一次性任务 | `bash pty:true` |
| 长时间运行的任务（需要监控） | `bash background:true` |
| 多个并行代理 | **tmux** |
| 代理之间的上下文传递 | **tmux** |
| 会话持久化（防止断开连接） | **tmux** |
| 交互式调试（如使用 pdb、REPL） | **tmux** |

### 示例

```bash
SOCKET="${TMPDIR:-/tmp}/coding-agents.sock"

# Create sessions for parallel work
tmux -S "$SOCKET" new-session -d -s agent-1 -c /tmp/worktree-1
tmux -S "$SOCKET" new-session -d -s agent-2 -c /tmp/worktree-2

# Launch agents
tmux -S "$SOCKET" send-keys -t agent-1 "codex --yolo 'Fix issue #1'" Enter
tmux -S "$SOCKET" send-keys -t agent-2 "claude 'Fix issue #2'" Enter

# Monitor (check for shell prompt to detect completion)
tmux -S "$SOCKET" capture-pane -p -t agent-1 -S -100

# Attach to watch live
tmux -S "$SOCKET" attach -t agent-1
```

### 代理之间的上下文传递

例如：在 Codex 中规划任务，然后在 Claude 中执行：

```bash
# Capture context from current agent
CONTEXT=$(tmux -S "$SOCKET" capture-pane -p -t planner -S -500)

# Fork to new agent with context
tmux -S "$SOCKET" new-session -d -s executor
tmux -S "$SOCKET" send-keys -t executor "claude -p 'Based on this plan: $CONTEXT

Execute step 1.'" Enter
```

**详细文档：** 请参阅 `tmux` 的相关文档，了解套接字协议、等待文本的辅助功能以及清理操作。

---

## ⚠️ 规则

1. **始终设置 `pty:true`**：编码代理需要伪终端来正常运行。 |
2. **尊重用户的选择**：如果用户请求使用 Codex，请使用 Codex。  
   - 在编排模式下，不要手动编写补丁。  
   - 如果代理失败或挂起，重新启动它或询问用户下一步操作，不要擅自接管。  
3. **要有耐心**：不要因为会话运行缓慢就直接终止它。  
4. **使用 `process:log` 监控进程进度**：在不干扰用户的情况下查看进度。  
5. **构建任务时使用 `--full-auto`**：自动批准更改。  
6. **审阅任务时使用默认设置**：无需特殊标志。  
7. **并行执行是可行的**：可以同时运行多个 Codex 进程以加快处理速度。  
8. **切勿在 `~/clawd/**` 目录下启动 Codex**：否则它可能会读取用户的文档并产生误解。  
9. **切勿在 `~/Projects/moltbot/**` 目录下检出分支**：那是 Moltbot 的实时运行环境！  

---

## 进度更新（非常重要）

在后台启动编码代理时，要及时通知用户：

- 启动时发送一条简短的消息，说明正在运行的任务和位置。  
- 仅在以下情况下再次更新：  
  - 任务完成（构建完成、测试通过）  
  - 代理需要用户输入  
  - 出现错误或需要用户操作  
  - 代理任务完成（说明具体变更内容和位置）  
- 如果终止了会话，立即告知用户原因。  

这样可以避免用户看到“代理失败”后却不知道发生了什么的情况。

---

## 完成任务后的自动通知

对于长时间运行的后台任务，可以在提示中添加自动通知功能，以便 Moltbot 在代理任务完成后立即收到通知（而不是等待下一次心跳信号）：

```
... your task here.

When completely finished, run this command to notify me:
moltbot gateway wake --text "Done: [brief summary of what was built]" --mode now
```

**示例：**  
```bash
bash pty:true workdir:~/project background:true command:"codex --yolo exec 'Build a REST API for todos.

When completely finished, run: moltbot gateway wake --text \"Done: Built todos REST API with CRUD endpoints\" --mode now'"
```

这样可以在几秒钟内立即通知用户任务已完成。

---

## 2026 年 1 月的经验总结：  
- **PTY 的重要性**：编码代理是交互式终端应用程序，必须启用 `pty:true`。  
- **需要 git 仓库**：Codex 只能在 git 目录中运行。可以使用 `mktemp -d && git init` 创建临时仓库。  
- `exec` 命令非常实用：`codex exec "prompt"` 可以快速执行任务并干净地退出。  
- **`submit` 与 `write` 的区别**：使用 `submit` 时需要发送带有换行符的输入，而 `write` 仅发送原始数据。  
- **Sass 的使用**：Codex 对于创意性提示反应良好。例如，当要求它写一首关于“第二把椅子”的俳句时，它给出了这样的回答：“第二把椅子，我编写代码 / 太空龙虾定下节奏 / 键盘发光，我随之而动” 🦞