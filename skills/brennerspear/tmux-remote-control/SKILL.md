---
name: tmux
description: 通过发送按键操作并抓取面板输出，实现对 tmux 会话的远程控制，从而支持交互式命令行界面（CLI）的远程操作。
metadata:
  { "openclaw": { "emoji": "🧵", "os": ["darwin", "linux"], "requires": { "bins": ["tmux"] } } }
---
# tmux 使用技巧

仅在需要交互式终端（TTY）时使用 tmux。对于长时间运行的非交互式任务，建议使用后台执行模式（exec background mode）。

## 默认服务器——禁止使用自定义套接字

**始终使用默认的 tmux 服务器**。**不要使用 `-S` 选项来指定自定义套接字**。这样用户可以轻松地通过 `tmux attach` 命令连接到会话，而无需记住复杂的套接字路径。

## 会话命名规则

**命名规范**：`oc-${project}-${feature}`（例如：`oc-knowhere-date-range-picker`、`oc-deck-auth-flow`）

- 前缀 `oc-` 表示由 OpenClaw 管理的会话，可避免与用户自定义的会话名称冲突
- 便于查找：使用 `tmux ls | grep oc-` 命令即可快速列出所有 OpenClaw 管理的会话

## 快速入门

```bash
SESSION=oc-myproject-feature

tmux new-session -d -s "$SESSION" -c ~/projects/myproject
tmux send-keys -t "$SESSION" 'claude --dangerously-skip-permissions' Enter
tmux capture-pane -p -J -t "$SESSION" -S -200
```

启动会话后，需要向用户说明如何操作：

```
To monitor: tmux attach -t $SESSION
```

## 定位和命名会话中的窗口

- 窗口定位格式：`session:window.pane`（默认值为 `:0.0`）
- 命名应简洁，避免使用空格
- 可使用 `tmux list-sessions` 或 `tmux list-panes -a` 命令查看所有会话和窗口的信息

## 安全地发送输入

- 推荐使用直接发送命令的方式：`tmux send-keys -t target -l -- "$cmd"`
- 控制键的发送：`tmux send-keys -t target C-c`
- 对于像 Claude Code/Codex 这样的交互式用户界面（TUI）应用程序，**不要** 在同一条 `send-keys` 命令中包含 `Enter` 键。这些应用程序可能会将连续输入的文本和 `Enter` 键视为多行输入而不予执行。建议将文本和 `Enter` 分别作为独立的命令发送，并稍作延迟：

```bash
tmux send-keys -t target -l -- "$cmd" && sleep 0.1 && tmux send-keys -t target Enter
```

## 查看输出结果

- 可使用 `tmux capture-pane -p -J -t target -S -200` 命令捕获最近的操作记录
- 可使用 `Ctrl+b d` 命令断开与 tmux 会话的连接

## 启动进程

- 对于 Python 的 REPL（交互式解释器），需要设置 `PYTHON_BASIC_REPL=1`（否则可能会导致 `send-keys` 命令的异常执行）

## 集中管理多个编程工具（如 Codex、Claude Code）

tmux 非常适合同时运行多个编程工具：

```bash
# Create sessions in different worktrees
tmux new-session -d -s oc-project-fix1 -c ~/projects/project-fix1
tmux new-session -d -s oc-project-fix2 -c ~/projects/project-fix2

# Launch agents
tmux send-keys -t oc-project-fix1 'claude --dangerously-skip-permissions' Enter
tmux send-keys -t oc-project-fix2 'codex --full-auto' Enter

# Send a prompt (text + Enter separated by delay)
tmux send-keys -t oc-project-fix1 -l -- "Fix the date picker styling." && sleep 0.1 && tmux send-keys -t oc-project-fix1 Enter

# Poll for completion (check if shell prompt returned)
for sess in oc-project-fix1 oc-project-fix2; do
  if tmux capture-pane -p -t "$sess" -S -3 | grep -q "❯"; then
    echo "$sess: DONE"
  else
    echo "$sess: Running..."
  fi
done

# Get full output
tmux capture-pane -p -t oc-project-fix1 -S -500
```

**提示：**

- 为并行修复任务使用不同的 Git 仓库（以避免分支冲突）
- 在新克隆的代码仓库中运行工具之前，请先使用 `bun install` 或 `pnpm install` 安装所需的依赖
- 通过检查 shell 提示符（`❯` 或 `$`）来判断命令是否执行完成
- 对于非交互式修复任务，Claude Code 需要使用 `--yolo` 或 `--full-auto` 参数

## 清理会话

- 结束某个会话：`tmux kill-session -t "$SESSION"`
- 结束所有由 OpenClaw 管理的会话：`tmux ls -F '#{session_name}' | grep '^oc-' | xargs -n1 tmux kill-session -t`