---
name: claude-code-cli
version: "0.1.0"
description: "通过后台进程将编码任务委托给 Claude Code CLI。适用于以下场景：构建新功能、审核 Pull Request（PR）、重构代码库，或需要文件探索的迭代性编码工作。该工具支持交互式的 PTY（Python Terminal Window）模式以获取确认或权限信息，同时也支持无头（headless）的管道（pipe）模式以实现自动化操作。**不适用于**以下场景：简单的单行代码修改（直接编辑即可）、代码阅读（请使用专门的阅读工具），以及任何与 ~/.openclaw/ 工作区相关的工作。"
author: "AtelyPham"
license: "MIT"
homepage: "https://github.com/AtelyPham/openclaw-claude-code-skill"
metadata: {"openclaw":{"emoji":"✻","requires":{"bins":["claude"]},"install":[{"id":"node","kind":"node","package":"@anthropic-ai/claude-code","bins":["claude"],"label":"Install Claude Code (npm)"}]}}
---
# Claude Code 技能

您可以通过后台进程（使用 PTY 或无头管道模式）将编码任务委托给 **Claude Code CLI**。

## 需要 PTY 模式（交互式）

Claude Code 是一个 **交互式终端应用程序**，需要一个伪终端（PTY）。如果没有 PTY，输出可能会中断或代理程序会挂起。

**在交互式模式下，请始终使用 `pty:true`：**

```bash
# ✅ Correct - with PTY
exec pty:true command:"claude 'Your prompt'"

# ❌ Wrong - no PTY, agent may break
exec command:"claude 'Your prompt'"
```

---

## 两种模式

### 1. 交互式 PTY 模式

适用于 Claude Code 需要确认、输入或显示权限提示的任务。

```bash
# Foreground (waits for completion)
exec pty:true workdir:~/project command:"claude 'Add dark mode toggle'"

# Background (returns sessionId)
exec pty:true workdir:~/project background:true command:"claude 'Build REST API for todos'"
```

### 2. 无头管道模式

适用于自动化、脚本编写或类似持续集成（CI）的用途。使用 `-p` 标志表示非交互式模式。

```bash
# Simple one-shot
exec command:"claude -p 'Explain what src/main.ts does' --output-format json"

# With structured output validation
exec command:"claude -p 'List all exported functions in src/' --output-format json --json-schema '{\"type\":\"object\",\"properties\":{\"functions\":{\"type\":\"array\",\"items\":{\"type\":\"string\"}}}}'"

# Budget-capped automation
exec command:"claude -p 'Refactor auth module' --max-budget-usd 5.00 --output-format json"

# Real-time streaming output (JSON chunks as they arrive)
exec command:"claude -p 'Build a helper function' --output-format stream-json"
```

---

## 执行与进程工具参考

### 执行工具参数

| 参数          | 类型    | 描述                                                                 |
|---------------|-------| ---------------------------------------------------------------------------|
| `command`       | string  | 要运行的 shell 命令                                                    |
| `pty`          | boolean | **交互式模式必须使用！** 分配一个伪终端                              |
| `workdir`       | string  | 工作目录（代理程序仅看到该目录的内容）                                   |
| `background`      | boolean | 在后台运行，并返回 sessionId 以便监控                         |
| `timeout`       | number  | 超时时间（秒，实际任务默认为 1800 秒以上）                          |
| `elevated`     | boolean | 在主机上运行（如果允许的话）                                 |

### 进程工具操作（用于后台会话）

| 操作           | 描述                                                          |
|---------------|----------------------------------------------------|
| `list`         | 列出所有正在运行或最近的会话                                     |
| `poll`         | 检查会话是否仍在运行                                      |
| `log`          | 获取会话输出（可选偏移量/限制）                                      |
| `write`        | 向标准输入（stdin）发送原始数据                                 |
| `submit`       | 发送数据 + 换行符（类似于按键并按下 Enter）                             |
| `send-keys`     | 发送键值对或十六进制字节                                   |
| `paste`        | 粘贴文本（可选使用括号模式）                                    |
| `kill`         | 终止会话                                         |

---

## 主要 CLI 标志

| 标志          | 作用                                                         |
|---------------|---------------------------------------------------------|
| `-p`          | 非交互式管道模式（无头模式）                                        |
| `--output-format json` | 结构化 JSON 输出（仅限无头模式）                                   |
| `--output-format stream-json` | 实时流式输出（仅限无头模式）                                   |
| `--resume [SESSION_ID]` | 通过 ID 恢复会话，或打开带有可选搜索词的交互式选择器                 |
| `--continue`     | 继续最新的会话                                         |
| `--fork-session`    | 恢复会话时创建新的会话 ID（与 `--resume` 或 `--continue` 一起使用）           |
| `--from-pr [value]` | 通过编号/URL 恢复与 PR 关联的会话                             |
| `--allowedTools 'Bash,Read,Edit,Write,Glob,Grep'` | 限制可使用的工具                                      |
| `--permission-mode acceptEdits` | 自动接受编辑，防止提示卡住                                   |
| `--permission-mode plan` | 只读探索模式（不允许写入）                                    |
| `--dangerously-skip-permissions` | 完全自动执行，无任何限制（⚠️ 危险）                             |
| `--max-budget-usd N` | 自动化运行的预算上限（美元）                                   |
| `--json-schema '<schema>'` | 结构化输出验证（与 `-p` 一起使用）                                   |
| `--append-system-prompt '...'` | 在系统提示中添加内容（不会替换原有提示）                             |
| `--system-prompt '...'` | 替换整个系统提示                                         |
| `--agents '<json>'` | 内联动态子代理定义                                      |
| `--model <model>` | 覆盖模型（sonnet, haiku, opus）                                    |
| `--add-dir <path>` | 向上下文中添加额外的目录                                   |

### 权限模式

| 模式            | 行为                                                          |
|---------------|---------------------------------------------------------|
| `default`         | 每次操作都询问权限                                         |
| `acceptEdits`      | 自动接受文件编辑（推荐用于后台任务）                                   |
| `plan`           | 只读探索模式，不允许写入                                      |
| `dontAsk`        | 除非预先批准，否则自动拒绝                                      |
| `bypassPermissions`    | 跳过所有权限提示（⚠️ 效果与 `--dangerously-skip-permissions` 相同）           |

### 系统提示模式

| 标志          | 行为                                                          |
|---------------|---------------------------------------------------------|
| `--append-system-prompt '...'` | 在系统提示中添加内容或限制                                      |
| `--system-prompt '...'` | 替换整个系统提示                                         |

使用 `--append-system-prompt` 来添加上下文或限制。仅在需要完全控制提示时使用 `--system-prompt`（这种情况很少见）。

### 详细工具限制

您可以限制 Claude Code 使用的 Bash 工具的具体子命令：

```bash
exec pty:true command:"claude --allowedTools 'Bash(git:*,npm:*),Read,Edit,Write,Glob,Grep' 'Your task'"
```

---

## 会话连续性

跟踪并在不同对话之间恢复会话。

```bash
# Start a task
exec pty:true workdir:~/project background:true command:"claude --permission-mode acceptEdits 'Build feature X'"

# Continue latest session
exec pty:true workdir:~/project command:"claude --continue"

# Resume specific session by ID
exec pty:true workdir:~/project command:"claude --resume abc123"

# Resume with interactive search (finds sessions matching the term)
exec pty:true workdir:~/project command:"claude --resume 'auth module'"

# Fork when resuming (creates new session ID, preserves original)
exec pty:true workdir:~/project command:"claude --continue --fork-session"

# Resume session linked to a PR
exec pty:true workdir:~/project command:"claude --from-pr 130"

# List recent sessions (find session IDs)
exec command:"claude sessions list"
```

### HANDOFF.md 模式（长时间会话）

对于超出上下文限制的任务，将进度写入 handoff 文件：

```bash
# In the Claude Code session, ask it to write progress
# Then start a fresh session picking up from the handoff
exec pty:true workdir:~/project command:"claude 'Read HANDOFF.md and continue the work described there'"
```

---

## 模式示例

### 快速启动：一次性任务

```bash
# Foreground with PTY
exec pty:true workdir:~/project command:"claude --permission-mode acceptEdits 'Add error handling to API calls'"

# Headless one-shot
exec command:"claude -p 'Summarize the codebase structure' --output-format json"
```

### 带监控的后台任务

```bash
# 1. Start
exec pty:true workdir:~/project background:true timeout:3600 command:"claude --permission-mode acceptEdits 'Build a complete auth module with JWT tokens'"

# 2. Monitor
process action:log sessionId:XXX
process action:poll sessionId:XXX

# 3. Send input if needed
process action:submit sessionId:XXX data:"yes"

# 4. Kill if stuck
process action:kill sessionId:XXX
```

### PR 审查（安全提示：**切勿在 OpenClaw 的项目文件夹中审查 PR！**）

**⚠️ 重要提示：**切勿在 OpenClaw 的项目文件夹中审查 Pull Request（PR）！

```bash
# Clone to temp dir and checkout PR
exec command:"git clone https://github.com/user/repo.git /tmp/pr-review && cd /tmp/pr-review && gh pr checkout 130"

exec pty:true workdir:/tmp/pr-review command:"claude --permission-mode plan 'Review this PR. Focus on bugs, security issues, and performance. Show diff summary.'"

# Clean up
exec command:"rm -rf /tmp/pr-review"
```

### 使用 Git Worktree 并行修复问题

```bash
# 1. Create worktrees
exec command:"git worktree add -b fix/issue-78 /tmp/issue-78 main"
exec command:"git worktree add -b fix/issue-99 /tmp/issue-99 main"

# 2. Launch Claude Code in each (background + PTY)
exec pty:true workdir:/tmp/issue-78 background:true command:"claude --permission-mode acceptEdits 'Fix issue #78: <description>. Commit when done.

When finished, run: openclaw system event --text \"Done: Fixed issue #78\" --mode now'"

exec pty:true workdir:/tmp/issue-99 background:true command:"claude --permission-mode acceptEdits 'Fix issue #99: <description>. Commit when done.

When finished, run: openclaw system event --text \"Done: Fixed issue #99\" --mode now'"

# 3. Monitor
process action:list

# 4. Create PRs
exec command:"cd /tmp/issue-78 && git push -u origin fix/issue-78"
exec command:"gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'"

# 5. Cleanup
exec command:"git worktree remove /tmp/issue-78"
exec command:"git worktree remove /tmp/issue-99"
```

### 分布式操作模式

将任务分配到多个无头进程中进行执行：

```bash
# Migrate multiple files in parallel (shell script via exec)
exec command:"for file in \$(cat files-to-migrate.txt); do claude -p \"Migrate \$file to new API\" --output-format json --max-budget-usd 1.00 & done; wait"
```

### 编写者/审阅者模式（双会话）

同时进行两个会话：一个负责实现，另一个负责审阅：

```bash
# Session A: implement
exec pty:true workdir:~/project background:true command:"claude --permission-mode acceptEdits 'Implement the feature described in SPEC.md'"

# Session B: review (read-only)
exec pty:true workdir:~/project background:true command:"claude --permission-mode plan 'Watch for new changes and review them. Focus on correctness and test coverage.'"
```

### 内联动态子代理

无需在磁盘上保存任何文件即可定义代理程序：

```bash
exec pty:true command:"claude --agents '{
  \"code-reviewer\": {
    \"description\": \"Expert code reviewer\",
    \"prompt\": \"You are a senior code reviewer. Focus on correctness, security, and performance.\",
    \"tools\": [\"Read\", \"Grep\", \"Glob\", \"Bash\"],
    \"model\": \"sonnet\"
  },
  \"implementer\": {
    \"description\": \"Feature implementer\",
    \"prompt\": \"You implement features following existing patterns.\",
    \"tools\": [\"Read\", \"Edit\", \"Write\", \"Bash\", \"Glob\", \"Grep\"],
    \"model\": \"sonnet\"
  }
}'"
```

---

## 完成后自动通知

对于长时间运行的后台任务，添加一个唤醒触发器，以便 OpenClaw 可以立即收到通知：

```bash
exec pty:true workdir:~/project background:true command:"claude --permission-mode acceptEdits 'Build a REST API for todos.

When completely finished, run this command to notify me:
openclaw system event --text \"Done: Built todos REST API with CRUD endpoints\" --mode now'"
```

---

## 进度更新

在启动后台代理时，及时通知用户：

- 启动时发送一条简短消息（正在运行的任务及位置）
- 仅在发生以下情况时更新：里程碑完成、代理需要输入、出现错误或任务完成
- 如果终止会话，立即说明原因
- 绝不要让用户看到“代理失败”且没有任何上下文信息

---

## 安全规则

1. **在交互式模式下始终使用 `pty:true`**
2. **对于后台任务，使用 `--permission-mode acceptEdits` 以防止提示卡住**
3. **切勿在 `~/.openclaw/` 工作目录中运行**
4. **切勿在 OpenClaw 项目目录中检出分支**
5. **使用 `--dangerously-skip-permissions` 时会有明确的安全警告——建议使用 `acceptEdits`**
6. **尊重用户的工具选择**——如果代理失败，不要擅自接管用户的操作
7. **要有耐心**——不要因为任务运行缓慢就终止会话
8. **为自动化设置预算上限**——使用 `--max-budget-usd` 来限制无人值守任务的运行时间
9. **同时运行最多 3-4 个会话**——超过这个数量会导致资源竞争
10. **设置超时时间**——对于实际任务，建议使用 1800 秒以上的超时时间，避免任务在运行中途因超时而终止