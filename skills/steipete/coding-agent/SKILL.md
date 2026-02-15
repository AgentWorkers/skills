---
name: coding-agent
description: 通过后台进程运行 Codex CLI、Claude Code、OpenCode 或 Pi Coding Agent，以实现程序化控制。
metadata: {"clawdbot":{"emoji":"🧩","requires":{"anyBins":["claude","codex","opencode","pi"]}}}
---

# 编码助手（优先使用后台模式）

对于非交互式的编码任务，请使用 **bash 的后台模式**。对于交互式的编码会话，请始终使用 **tmux**（除非是简单的、一次性完成的命令）。

## 使用模式：工作目录 + 后台模式

```bash
# Create temp space for chats/scratch work
SCRATCH=$(mktemp -d)

# Start agent in target directory ("little box" - only sees relevant files)
bash workdir:$SCRATCH background:true command:"<agent command>"
# Or for project work:
bash workdir:~/project/folder background:true command:"<agent command>"
# Returns sessionId for tracking

# Monitor progress
process action:log sessionId:XXX

# Check if done  
process action:poll sessionId:XXX

# Send input (if agent asks a question)
process action:write sessionId:XXX data:"y"

# Kill if needed
process action:kill sessionId:XXX
```

**为什么工作目录很重要？** 编码助手会在一个特定的工作目录中启动，不会去读取与当前任务无关的文件（比如你的 `soul.md` 文件 😅）。

---

## Codex CLI

**默认模型：** `gpt-5.2-codex`（配置在 `~/.codex/config.toml` 中）

### 构建/创建项目（使用 `--full-auto` 或 `--yolo` 参数）
```bash
# --full-auto: sandboxed but auto-approves in workspace
bash workdir:~/project background:true command:"codex exec --full-auto \"Build a snake game with dark theme\""

# --yolo: NO sandbox, NO approvals (fastest, most dangerous)
bash workdir:~/project background:true command:"codex --yolo \"Build a snake game with dark theme\""

# Note: --yolo is a shortcut for --dangerously-bypass-approvals-and-sandbox
```

### 查看 Pull Request（基础用法，无需任何特殊参数）

**⚠️ 重要提示：** **绝对不要在 Clawdbot 项目的目录中查看 Pull Request！**  
- 请使用 Pull Request 被提交到的项目目录（如果该目录不是 `~/Projects/clawdbot`）；  
- 或者先将其克隆到一个临时文件夹中。

```bash
# Option 1: Review in the actual project (if NOT clawdbot)
bash workdir:~/Projects/some-other-repo background:true command:"codex review --base main"

# Option 2: Clone to temp folder for safe review (REQUIRED for clawdbot PRs!)
REVIEW_DIR=$(mktemp -d)
git clone https://github.com/clawdbot/clawdbot.git $REVIEW_DIR
cd $REVIEW_DIR && gh pr checkout 130
bash workdir:$REVIEW_DIR background:true command:"codex review --base origin/main"
# Clean up after: rm -rf $REVIEW_DIR

# Option 3: Use git worktree (keeps main intact)
git worktree add /tmp/pr-130-review pr-130-branch
bash workdir:/tmp/pr-130-review background:true command:"codex review --base main"
```

**为什么这样做？** 在正在运行的 Clawdbot 仓库中切换分支可能会导致系统崩溃！

### 批量查看 Pull Request（并行处理）

```bash
# Fetch all PR refs first
git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'

# Deploy the army - one Codex per PR!
bash workdir:~/project background:true command:"codex exec \"Review PR #86. git diff origin/main...origin/pr/86\""
bash workdir:~/project background:true command:"codex exec \"Review PR #87. git diff origin/main...origin/pr/87\""
bash workdir:~/project background:true command:"codex exec \"Review PR #95. git diff origin/main...origin/pr/95\""
# ... repeat for all PRs

# Monitor all
process action:list

# Get results and post to GitHub
process action:log sessionId:XXX
gh pr comment <PR#> --body "<review content>"
```

### 查看 Pull Request 的建议：
- **先获取引用信息：** `git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'`  
- **使用 `git diff`：** 告诉 Codex 使用 `git diff origin/main...origin/pr/XX` 来比较差异  
- **不要切换分支：** 并行查看多个 Pull Request 时，避免它们互相影响分支状态  
- **发布审核结果：** 使用 `gh pr comment` 将审核结果发布到 GitHub 上

---

## Claude 代码

```bash
bash workdir:~/project background:true command:"claude \"Your task\""
```

---

## OpenCode

```bash
bash workdir:~/project background:true command:"opencode run \"Your task\""
```

---

## Pi 编码助手

```bash
# Install: npm install -g @mariozechner/pi-coding-agent
bash workdir:~/project background:true command:"pi \"Your task\""
```

---

## Pi 命令行参数（常用选项）：
- `--print` / `-p`：非交互模式；执行命令后直接退出。  
- `--provider <名称>`：选择代码生成服务（默认为 google）。  
- `--model <ID>`：选择使用的语言模型（默认为 gemini-2.5-flash）。  
- `--api-key <密钥>`：覆盖 API 密钥（默认使用环境变量中的密钥）。  

**示例：**  
```bash
# Set provider + model, non-interactive
bash workdir:~/project background:true command:"pi --provider openai --model gpt-4o-mini -p \"Summarize src/\""
```

---

## tmux（交互式会话）

对于交互式的编码会话，请始终使用 tmux（除非是简单的、一次性完成的命令）。对于非交互式的任务，建议使用 bash 的后台模式。

---

## 使用 git worktrees 和 tmux 并行修复问题

要同时修复多个问题，可以使用 git worktrees（创建隔离的分支）和 tmux 会话：

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
tmux -S "$SOCKET" send-keys -t fix-78 "cd /tmp/issue-78 && pnpm install && codex --yolo 'Fix issue #78: <description>. Commit and push.'" Enter
tmux -S "$SOCKET" send-keys -t fix-99 "cd /tmp/issue-99 && pnpm install && codex --yolo 'Fix issue #99: <description>. Commit and push.'" Enter

# 5. Monitor progress
tmux -S "$SOCKET" capture-pane -p -t fix-78 -S -30
tmux -S "$SOCKET" capture-pane -p -t fix-99 -S -30

# 6. Check if done (prompt returned)
tmux -S "$SOCKET" capture-pane -p -t fix-78 -S -3 | grep -q "❯" && echo "Done!"

# 7. Create PRs after fixes
cd /tmp/issue-78 && git push -u origin fix/issue-78
gh pr create --repo user/repo --head fix/issue-78 --title "fix: ..." --body "..."

# 8. Cleanup
tmux -S "$SOCKET" kill-server
git worktree remove /tmp/issue-78
git worktree remove /tmp/issue-99
```

**为什么使用 git worktrees？** 每个 Codex 实例都在独立的分支上运行，不会产生冲突，可以同时进行多个修复任务！  
**为什么选择 tmux 而不是 bash 的后台模式？** 因为 Codex 是交互式的，需要 TTY 来正确显示输出；tmux 可以保持会话的持久性，并记录完整的操作历史。

---

## ⚠️ 规则：
1. **尊重用户的选择**：如果用户请求使用 Codex，就使用 Codex；**绝对不要自行尝试构建它！**  
2. **要有耐心**：不要因为会话运行缓慢就终止它们。  
3. **使用 `process:log` 监控进程进度**：在不干扰会话的情况下查看进度。  
4. **使用 `--full-auto` 参数进行自动构建**：自动批准代码更改。  
5. **查看 Pull Request 时使用基础参数**：不需要任何特殊参数。  
6. **并行处理是可行的**：可以同时运行多个 Codex 实例来处理批量任务。  
7. ****绝对不要在 `~/clawd/** 目录下启动 Codex**：否则它可能会读取你的 `soul.md` 文件并产生错误的组织结构理解！** 请使用目标项目目录或 `/tmp` 作为新的工作环境。  
8. ****绝对不要在 `~/Projects/clawdbot/** 目录下切换分支**：那里是 Clawdbot 的运行实例！** 请将代码克隆到 `/tmp` 或使用 git worktree 来查看 Pull Request。

---

## Pull Request 模板（推荐格式）

在向外部仓库提交 Pull Request 时，请使用以下格式，以确保代码质量和便于维护者阅读：

````markdown
## Original Prompt
[Exact request/problem statement]

## What this does
[High-level description]

**Features:**
- [Key feature 1]
- [Key feature 2]

**Example usage:**
```bash
# 示例
command example
```

## Feature intent (maintainer-friendly)
[Why useful, how it fits, workflows it enables]

## Prompt history (timestamped)
- YYYY-MM-DD HH:MM UTC: [Step 1]
- YYYY-MM-DD HH:MM UTC: [Step 2]

## How I tested
**Manual verification:**
1. [Test step] - Output: `[result]`
2. [Test step] - Result: [result]

**Files tested:**
- [Detail]
- [Edge cases]

## Session logs (implementation)
- [What was researched]
- [What was discovered]
- [Time spent]

## Implementation details
**New files:**
- `path/file.ts` - [description]

**Modified files:**
- `path/file.ts` - [change]

**Technical notes:**
- [Detail 1]
- [Detail 2]

---
*Submitted by Razor 🥷 - Mariano's AI agent*
````

**关键原则：**
1. 由人工编写的描述（避免使用 AI 生成的文本）。  
2. 向维护者清晰说明功能的目的。  
3. 提供带有时间戳的命令执行历史记录。  
4. 如果使用了 Codex 或编码助手，记录会话日志。  

**示例：** https://github.com/steipete/bird/pull/22