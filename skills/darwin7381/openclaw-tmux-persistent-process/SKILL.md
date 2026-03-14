---
name: openclaw-tmux-persistent-process
description: 通过 tmux 运行能够在 OpenClaw 执行会话清理或网关重启后仍然继续运行的程序。适用于需要长时间运行的服务器、开发服务器、隧道（如 ngrok 或 cloudflared）、编码代理，或任何必须在当前执行会话结束后仍继续运行的进程。该解决方案可以防止后台进程在会话清理时收到 SIGKILL 信号。强烈推荐所有使用 OpenClaw 且需要运行长时间进程的用户使用。
---
# OpenClaw 的 Tmux 持久化进程

使用 Tmux 可以运行那些在 OpenClaw 会话清理或网关重启后仍能继续运行的程序。

## 为什么每个 OpenClaw 用户都应该使用 Tmux

OpenClaw 通过 `exec` 命令来执行 shell 命令。然而，`exec` 有一个许多用户直到出现问题时才意识到的关键限制：

- **后台进程与会话绑定。** 当会话被清理（例如因为空闲超时、上下文压缩或网关重启）时，所有后台进程都会收到 SIGKILL 信号并立即终止。
- **网关重启会导致所有进程终止。** 无论是更新、配置更改还是网关重启，所有正在运行的 `exec` 进程都会消失。
- **没有任何警告。** 你的隧道、开发服务器或构建任务可能会在没有任何提示的情况下突然停止运行。

这意味着任何你希望持续运行的进程（例如用于客户端演示的隧道、开发服务器或长时间运行的构建任务）都可能在任何时候突然停止。

**解决方案：** 使用 **tmux** 来创建与 OpenClaw 会话完全解耦的虚拟终端。在 tmux 中运行的程序可以在网关重启、会话清理或会话超时时继续运行。tmux 可以独立于 OpenClaw 运行——即使网关出现故障，你的进程也会继续执行。

**经验法则：** 如果某个命令的执行时间可能超过 2 分钟，就使用 tmux。

---

## 套接字使用规范

所有操作都使用专用套接字，以避免干扰用户自己的 tmux 会话：

```bash
SOCK="/tmp/openclaw-tmux/openclaw.sock"
mkdir -p /tmp/openclaw-tmux
```

## 启动一个进程

```bash
SESSION="my-server"

# Check if already running
if tmux -S "$SOCK" has-session -t "$SESSION" 2>/dev/null; then
  echo "already running"
else
  tmux -S "$SOCK" new -d -s "$SESSION" \
    "cd /path/to/project && npm run dev"
  echo "started"
fi
```

## 监控进程

```bash
# List all sessions
tmux -S "$SOCK" list-sessions

# View last 30 lines of output
tmux -S "$SOCK" capture-pane -t "$SESSION" -p -S -30

# Check if process is idle (back to shell prompt)
tmux -S "$SOCK" capture-pane -t "$SESSION" -p -S -3 \
  | grep -qE '\$\s*$|❯' && echo "IDLE" || echo "RUNNING"
```

## 与进程交互

```bash
# Send a command
tmux -S "$SOCK" send-keys -t "$SESSION" "command" Enter

# Send literal text (recommended, no special key parsing)
tmux -S "$SOCK" send-keys -t "$SESSION" -l -- "literal text"
tmux -S "$SOCK" send-keys -t "$SESSION" Enter

# Ctrl+C to interrupt
tmux -S "$SOCK" send-keys -t "$SESSION" C-c
```

## 停止/清理进程

```bash
# Kill one session
tmux -S "$SOCK" kill-session -t "$SESSION"

# Kill all
tmux -S "$SOCK" kill-server

# Clean stale socket
rm -f "$SOCK"
```

## 启动需要启动时间的交互式程序（等待程序准备好）

对于需要启动时间的程序（例如代码执行代理、REPL 环境）：

```bash
SESSION="my-task"
tmux -S "$SOCK" new -d -s "$SESSION"
tmux -S "$SOCK" send-keys -t "$SESSION" "cd ~/project && node" Enter

# Wait for prompt before sending commands
for i in $(seq 1 15); do
  OUTPUT=$(tmux -S "$SOCK" capture-pane -t "$SESSION" -p -S -5)
  if echo "$OUTPUT" | grep -qE '❯|>\s*$|ready'; then
    break
  fi
  sleep 1
done

# Now safe to send input
tmux -S "$SOCK" send-keys -t "$SESSION" -l "your command"
tmux -S "$SOCK" send-keys -t "$SESSION" Enter
```

## 常见使用场景

| 使用场景 | 会话名称 | 命令示例 |
|----------|-------------|-----------------|
| 开发服务器 | `dev-server` | `npm run dev` |
| 隧道（使用 ngrok） | `tunnel-ngrok` | `ngrok http 3000` |
| 隧道（使用 localhost.run） | `tunnel-lr` | `ssh -R 80:localhost:3000 nokey@localhost.run` |
| 后台工作进程 | `worker` | `python worker.py` |
| 构建任务 | `build-app` | `npm run build` |

## 会话命名规则

使用小写字母加连字符（-）来命名会话，不要使用空格。

```
dev-server       — development servers
tunnel-{name}    — tunnels (ngrok, cloudflared, etc.)
build-{project}  — build tasks
worker-{name}    — background workers
```

## 重要注意事项

- **系统重启会导致会话丢失。** tmux 无法在系统重启后继续运行，因此需要重新创建会话。
- **滚动缓冲区限制。** 默认为 2000 行。可以通过 `tmux set-option -t "$SESSION" history-limit 10000` 来增加缓冲区大小。
- **套接字可能失效。** 如果 `list-sessions` 命令显示“连接错误”，请删除旧的套接字并重新创建一个新的。
- **环境变量。** tmux 会继承创建会话时的环境变量。你可以在启动命令中设置环境变量：`tmux new -d -s name "export KEY=value && cmd"`。
- **无冲突。** 专用套接字确保不会干扰用户自己的 tmux 会话。

## 所需软件

- **tmux 2.6 或更高版本**（以支持 `send-keys -l` 命令）
- 检查版本：`tmux -V`
- 安装方法：`brew install tmux`（macOS）或 `apt install tmux`（Linux）