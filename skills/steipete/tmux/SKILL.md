---
name: tmux
description: 通过发送按键和抓取面板输出来远程控制 tmux 会话，从而实现交互式命令行界面（CLI）的远程操作。
metadata: {"clawdbot":{"emoji":"🧵","os":["darwin","linux"],"requires":{"bins":["tmux"]}}}
---

# tmux 技能（Clawdbot）

仅在需要交互式 TTY 时使用 tmux。对于长时间运行的非交互式任务，建议使用 bash 的后台模式。

## 快速入门（隔离的 socket，bash 工具）

```bash
SOCKET_DIR="${CLAWDBOT_TMUX_SOCKET_DIR:-${TMPDIR:-/tmp}/clawdbot-tmux-sockets}"
mkdir -p "$SOCKET_DIR"
SOCKET="$SOCKET_DIR/clawdbot.sock"
SESSION=clawdbot-python

tmux -S "$SOCKET" new -d -s "$SESSION" -n shell
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- 'PYTHON_BASIC_REPL=1 python3 -q' Enter
tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200
```

启动会话后，务必打印监控命令：

```
To monitor:
  tmux -S "$SOCKET" attach -t "$SESSION"
  tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200
```

## Socket 规约

- 使用 `CLAWDBOT_TMUX SOCKET_DIR`（默认值为 `${TMPDIR:-/tmp}/clawdbot-tmux-sockets`）。
- 默认 socket 路径：`"$CLAWDBOT_TMUX SOCKET_DIR/clawdbot.sock"`。

## 目标窗格的命名规则

- 目标格式：`session:window.pane`（默认为 `:0.0`）。
- 命名应简洁，避免使用空格。
- 查看会话和窗格：`tmux -S "$SOCKET" list-sessions`，`tmux -S "$SOCKET" list-panes -a`。

## 查找会话

- 在指定 socket 上列出会话：`{baseDir}/scripts/find-sessions.sh -S "$SOCKET"`。
- 扫描所有 socket：`{baseDir}/scripts/find-sessions.sh --all`（会使用 `CLAWDBOT_TMUX SOCKET_DIR`）。

## 安全地发送输入

- 建议使用字面值进行输入发送：`tmux -S "$SOCKET" send-keys -t target -l -- "$cmd"`。
- 控制键的发送：`tmux -S "$SOCKET" send-keys -t target C-c`。

## 查看输出

- 捕获最近的输出记录：`tmux -S "$SOCKET" capture-pane -p -J -t target -S -200`。
- 等待命令提示符：`{baseDir}/scripts/wait-for-text.sh -t session:0.0 -p 'pattern'`。
- 可以通过 `Ctrl+b d` 来断开连接。

## 启动进程

- 对于 Python REPL，需要设置 `PYTHON_BASIC_REPL=1`（否则会影响 `send-keys` 的正常工作）。

## Windows / WSL

- tmux 在 macOS/Linux 上可用。在 Windows 上，建议使用 WSL 并在 WSL 内安装 tmux。
- 该技能仅适用于 `darwin`/`linux` 环境，并要求 `tmux` 在系统的 PATH 环境变量中。

## 编程代理的协调（Codex, Claude Code）

tmux 非常适合同时运行多个编程代理：

```bash
SOCKET="${TMPDIR:-/tmp}/codex-army.sock"

# Create multiple sessions
for i in 1 2 3 4 5; do
  tmux -S "$SOCKET" new-session -d -s "agent-$i"
done

# Launch agents in different workdirs
tmux -S "$SOCKET" send-keys -t agent-1 "cd /tmp/project1 && codex --yolo 'Fix bug X'" Enter
tmux -S "$SOCKET" send-keys -t agent-2 "cd /tmp/project2 && codex --yolo 'Fix bug Y'" Enter

# Poll for completion (check if prompt returned)
for sess in agent-1 agent-2; do
  if tmux -S "$SOCKET" capture-pane -p -t "$sess" -S -3 | grep -q "❯"; then
    echo "$sess: DONE"
  else
    echo "$sess: Running..."
  fi
done

# Get full output from completed session
tmux -S "$SOCKET" capture-pane -p -t agent-1 -S -500
```

**提示：**
- 为并行修复任务使用不同的 git 仓库（以避免分支冲突）。
- 在新克隆的代码库中运行 Codex 之前，请先使用 `pnpm install` 安装依赖。
- 通过检查 shell 提示符（`❯` 或 `$`）来判断命令是否执行完成。
- 对于非交互式修复任务，Codex 需要使用 `--yolo` 或 `--full-auto` 参数。

## 清理

- 结束某个会话：`tmux -S "$SOCKET" kill-session -t "$SESSION"`。
- 结束指定 socket 上的所有会话：`tmux -S "$SOCKET" list-sessions -F '${session_name}' | xargs -r -n1 tmux -S "$SOCKET" kill-session -t`。
- 清除 socket 上的所有数据：`tmux -S "$SOCKET" kill-server`。

## 辅助工具：wait-for-text.sh

`{baseDir}/scripts/wait-for-text.sh` 可用于定时检查某个窗格中是否包含指定的正则表达式或固定字符串。

```bash
{baseDir}/scripts/wait-for-text.sh -t session:0.0 -p 'pattern' [-F] [-T 20] [-i 0.5] [-l 2000]
```

- `-t`/`--target`：指定要检查的窗格（必需参数）。
- `-p`/`--pattern`：要匹配的正则表达式（必需参数）；使用 `-F` 可以匹配固定字符串。
- `-T`：超时时间（秒，默认为 15 秒）。
- `-i`：轮询间隔（秒，默认为 0.5 秒）。
- `-l`：要搜索的历史记录行数（默认为 1000 行）。