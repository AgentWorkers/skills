---
name: kilocli-coding-agent
description: 通过后台进程运行 Kilo CLI，以实现程序化的控制。
---

**重要提示：** 你必须安装并配置好 Kilo CLI，这样 OpenClaw 才能顺利使用它。

```sh
npm install -g @kilocode/cli
```

# 编码代理（优先使用后台模式）

对于非交互式的编码工作，请使用 **bash 后台模式**。对于交互式的编码会话，请始终使用 **tmux**（除非是简单的、一次性完成的操作）。

## 模式：工作目录 + 后台模式

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

**为什么工作目录很重要？** 代理会在一个专注的目录中启动，不会去读取无关的文件（比如你的 `soul.md` 文件 😅）。

---

## Kilo CLI

### 构建/创建（使用 `--full-auto` 或 `--yolo`）

```bash
bash workdir:~/project background:true command:"kilo run \"Build a snake game with dark theme\""
```

### 查看 PR（基础用法，无需任何参数）

**⚠️ 重要提示：** 绝不要在 Clawdbot 项目的文件夹内查看 PR！**
- 请使用 PR 被提交到的项目文件夹（如果它不在 `~/Projects/clawdbot` 中）；
- 或者先将其克隆到一个临时文件夹中。

```bash
# Option 1: Review in the actual project (if NOT clawdbot)
bash workdir:~/Projects/some-other-repo background:true command:"kilo run \"Review current branch against main branch\""

# Option 2: Clone to temp folder for safe review (REQUIRED for clawdbot PRs!)
REVIEW_DIR=$(mktemp -d)
git clone https://github.com/clawdbot/clawdbot.git $REVIEW_DIR
cd $REVIEW_DIR && gh pr checkout 130
bash workdir:$REVIEW_DIR background:true command:"kilo run \"Review current branch against main branch\""
# Clean up after: rm -rf $REVIEW_DIR

# Option 3: Use git worktree (keeps main intact)
git worktree add /tmp/pr-130-review pr-130-branch
bash workdir:/tmp/pr-130-review background:true command:"kilo run \"Review current branch against main branch\""
```

**为什么？** 在正在运行的 Clawdbot 仓库中检出分支可能会导致实例出问题！

### 批量查看 PR（并行处理）

```bash
# Fetch all PR refs first
git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'

# Deploy the army - one Kilo CLI per PR!
bash workdir:~/project background:true command:"kilo run \"Review PR #86. git diff origin/main...origin/pr/86\""
bash workdir:~/project background:true command:"kilo run \"Review PR #87. git diff origin/main...origin/pr/87\""
bash workdir:~/project background:true command:"kilo run \"Review PR #95. git diff origin/main...origin/pr/95\""
# ... repeat for all PRs

# Monitor all
process action:list

# Get results and post to GitHub
process action:log sessionId:XXX
gh pr comment <PR#> --body "<review content>"
```

### 查看 PR 的技巧：
- **先获取引用：** `git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'`
- **使用 `git diff`：** 告诉 Kilo CLI 使用 `git diff origin/main...origin/pr/XX`
- **不要检出分支：** 多个并行查看操作可能会导致分支被修改
- **发布结果：** 使用 `gh pr comment` 将评论发布到 GitHub

---

## tmux（交互式会话）

对于交互式的编码会话，请始终使用 tmux（除非是简单的、一次性完成的操作）。对于非交互式的运行，请优先使用 bash 后台模式。

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
SOCKET="${TMPDIR:-/tmp}/kilo-fixes.sock"
tmux -S "$SOCKET" new-session -d -s fix-78
tmux -S "$SOCKET" new-session -d -s fix-99

# 4. Launch Kilo CLI in each (after npm install!)
tmux -S "$SOCKET" send-keys -t fix-78 "cd /tmp/issue-78 && npm install && kilo run 'Fix issue #78: <description>. Commit and push.'" Enter
tmux -S "$SOCKET" send-keys -t fix-99 "cd /tmp/issue-99 && npm install && kilo run 'Fix issue #99: <description>. Commit and push.'" Enter

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

**为什么使用 worktrees？** 每个 Kilo CLI 都在隔离的分支中运行，不会产生冲突。可以同时进行 5 个以上的修复操作！

**为什么选择 tmux 而不是 bash 后台模式？** Kilo CLI 是交互式的——需要 TTY 来正确显示输出。tmux 可以提供持久的会话记录和完整的历史记录。

---

## ⚠️ 规则：
1. **尊重工具的选择** — 如果用户请求使用 Kilo CLI，就使用 Kilo CLI。**绝对不要主动建议用户自己构建它！**
2. **要有耐心** — 不要因为会话运行缓慢就终止它们
3. **使用 `process:log` 监控进度** — 在不干扰会话的情况下查看进度
4. **使用 `--full-auto` 进行构建** — 自动批准更改
5. **查看 PR 时使用基础配置** — 不需要任何特殊参数
6. **并行操作是允许的** — 可以同时运行多个 Kilo CLI 进程以进行批量处理
7. ****绝对不要在 `~/clawd/**` 目录下启动 Kilo CLI** — 那里会读取你的 `soul.md` 文件，可能会导致对组织结构产生误解！请使用目标项目目录或 `/tmp` 作为干净的讨论环境
8. ****绝对不要在 `~/Projects/clawdbot/**` 目录下检出分支** — 那里是 Clawdbot 的实时运行实例！请克隆到 `/tmp` 或使用 git worktree 进行 PR 查看**

---

## PR 模板（Razor 标准）

在向外部仓库提交 PR 时，请使用以下格式，以确保代码质量和便于维护者阅读：

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
````

**关键原则：**
1. 由人类编写的描述（避免使用 AI 生成的内容）
2. 向维护者说明功能的用途
3. 带时间戳的命令历史记录
4. 如果使用了 Kilo CLI 代理，请记录会话日志