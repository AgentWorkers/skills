---
name: kilocli-coding-agent
description: 通过后台进程运行 Kilo CLI 以实现程序化控制。
version: 0.0.9
metadata:
  openclaw:
    requires:
      env:
        - GITHUB_TOKEN
      bins:
        - kilo
        - git
        - gh
        - tmux
    primaryEnv: GITHUB_TOKEN
------

**重要提示：** 你需要先安装并配置好 Kilo CLI，这样 OpenClaw 才能顺利使用它。

```sh
npm install -g @kilocode/cli
```

如果你想自动化向 Github 提交 Pull Request（PR），那么还需要在项目中认证 Github CLI：https://github.com/cli/cli#installation

# **编码代理（优先使用后台模式）**

对于非交互式的编码工作，请使用 **bash 的后台模式**。对于交互式的编码会话，始终使用 **tmux**（除非是简单的、一次性完成的操作）。

## **工作目录的重要性：** 代理会在一个特定的工作目录中启动，不会去读取无关的文件（比如你的 `soul.md` 文件 😅）。

---

## **Kilo CLI**

### **构建/创建（使用自主模式）**

```bash
bash workdir:~/project background:true command:"kilo run --auto \"Build a snake game with dark theme\""
```

### **审阅 Pull Request（基础用法，无需任何参数）**

**⚠️ 重要提示：** **绝对不要在 OpenClaw 的项目文件夹内审阅 Pull Request！**  
- 要么使用提交 PR 的项目文件夹（如果它不在 `~/Projects/openclaw` 目录下）；  
- 要么先克隆到一个临时文件夹中。

```bash
# Option 1: Review in the actual project (if NOT OpenClaw)
bash workdir:~/Projects/some-other-repo background:true command:"kilo run \"Review current branch against main branch\""

# Option 2: Clone to temp folder for safe review (REQUIRED for OpenClaw PRs!)
REVIEW_DIR=$(mktemp -d)
git clone https://github.com/openclaw/openclaw.git $REVIEW_DIR
cd $REVIEW_DIR && gh pr checkout 130
bash workdir:$REVIEW_DIR background:true command:"kilo run \"Review current branch against main branch\""
# Clean up after: rm -rf $REVIEW_DIR

# Option 3: Use git worktree (keeps main intact)
git worktree add /tmp/pr-130-review pr-130-branch
bash workdir:/tmp/pr-130-review background:true command:"kilo run \"Review current branch against main branch\""
```

**为什么？** 在正在运行的 OpenClaw 仓库中检出分支可能会导致系统崩溃！

### **批量审阅 Pull Request（并行处理）**

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

### **审阅 Pull Request 的小技巧：**
- **先获取引用信息：** `git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'`  
- **使用 `git diff`：** 告诉 Kilo CLI 使用 `git diff origin/main...origin/pr/XX`  
- **不要检出分支：** 多个并行审阅会改变分支的状态  
- **发布审阅结果：** 使用 `gh pr comment` 将审阅意见发布到 GitHub 上

---

## **tmux（交互式会话）**

对于交互式的编码会话，请始终使用 tmux（除非是简单的、一次性完成的操作）。对于非交互式的任务，建议使用 bash 的后台模式。

---

## **使用 git worktrees 和 tmux 并行修复问题**

要同时修复多个问题，可以使用 git worktrees（隔离的分支）和 tmux 会话：

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

**为什么使用 worktrees？** 每个 Kilo CLI 实例都在一个隔离的分支中工作，因此不会产生冲突。可以同时进行多个修复操作！

**为什么选择 tmux 而不是 bash 的后台模式？** Kilo CLI 是交互式的，需要 TTY 来正确显示输出；tmux 可以保持会话的持久性，并记录完整的操作历史。

---

## **重要规则：**

1. **尊重工具的选择** — 如果用户请求使用 Kilo CLI，就使用 Kilo CLI；**绝对不要主动建议用户自己构建它！**  
2. **要有耐心** — 即使会话运行缓慢，也不要直接终止它们。  
3. **使用 `process:log` 监控进程进度** — 在不干扰会话的情况下查看进度。  
4. **使用 `--full-auto` 参数进行构建** — 会自动批准更改。  
5. **审阅时使用基础配置** — 不需要任何特殊参数。  
6. **并行处理是允许的** — 可以同时运行多个 Kilo CLI 实例以进行批量处理。  
7. ****绝对不要在 `~/openclaw/** 目录下启动 Kilo CLI** — 那里包含 OpenClaw 的核心代码，可能会引发不必要的操作！** 使用目标项目目录或 `/tmp` 作为临时工作空间。  
8. ****绝对不要在 `~/Projects/openclaw/** 目录下检出分支** — 那是 OpenClaw 的运行中的实例！** 对于 PR 审阅，先克隆到 `/tmp` 或使用 git worktree。

---

## **Pull Request 模板（Razor 标准格式）**

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
````

**关键原则：**
1. 由人工编写的描述（避免使用 AI 生成的文本）。  
2. 向维护者明确说明功能的目的。  
3. 提交历史记录需带有时间戳。  
4. 如果使用了 Kilo CLI，需要记录会话日志。