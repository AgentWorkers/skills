---
name: zellij
description: 通过发送按键输入并抓取面板输出，实现对 Zellij 会话的远程控制，从而支持交互式命令行界面（CLI）的操作。
homepage: https://zellij.dev
metadata: {"moltbot":{"emoji":"🪟","os":["darwin","linux"],"requires":{"bins":["zellij","jq"]},"install":[{"id":"brew","kind":"brew","formula":"zellij","bins":["zellij"],"label":"Install Zellij (brew)"},{"id":"cargo","kind":"cargo","crate":"zellij","bins":["zellij"],"label":"Install Zellij (Cargo)"}]}}
---

# zellij 技能（Moltbot）

仅在需要交互式终端（TTY）时使用 zellij。对于长时间运行的非交互式任务，建议使用后台执行模式（exec）。

## 快速入门（数据目录、执行工具）

```bash
DATA_DIR="${CLAWDBOT_ZELLIJ_DATA_DIR:-${TMPDIR:-/tmp}/moltbot-zellij-data}"
mkdir -p "$DATA_DIR"
SESSION=moltbot-python

zellij --data-dir "$DATA_DIR" new-session --session "$SESSION" --layout "default" --detach
zellij --data-dir "$DATA_DIR" run --session "$SESSION" --name repl -- python3 -q
zellij --data-dir "$DATA_DIR" pipe --session "$SESSION" --pane-id 0
```

启动会话后，务必打印监控命令：

```
To monitor:
  zellij --data-dir "$DATA_DIR" attach --session "$SESSION"
  zellij --data-dir "$DATA_DIR" pipe --session "$SESSION" --pane-id 0
```

## 数据目录约定

- 使用 `CLAWDBOT_ZELLIJ_DATA_DIR`（默认值为 `${TMPDIR:-/tmp}/moltbot-zellij-data`）。
- Zellij 将会话状态（包括插件等）存储在该目录中。

## 定位特定窗口和命名

- Zellij 使用 `pane-id`（数字）来定位特定的窗口。
- 查找窗口 ID：`zellij --data-dir "$DATA_DIR" list-sessions --long` 或使用 `list-panes.sh`。
- 保持会话名称简短；避免使用空格。

## 查找会话

- 在当前数据目录中列出会话：`zellij --data-dir "$DATA_DIR" list-sessions`。
- 在所有数据目录中列出会话：`{baseDir}/scripts/find-sessions.sh --all`（使用 `CLAWDBOT_ZELLIJ_DATA_DIR`）。

## 安全地发送输入

- 使用 `zellij action` 来发送按键：`zellij --data-dir "$DATA_DIR" action --session "$SESSION" write-chars --chars "$cmd"`。
- 控制键：`zellij --data-dir "$DATA_DIR" action --session "$SESSION" write 2`（相当于按下 Ctrl+C）。

## 查看输出

- 捕获窗口输出：`zellij --data-dir "$DATA_DIR" pipe --session "$SESSION" --pane-id 0`。
- 等待提示信息：`{baseDir}/scripts/wait-for-text.sh -s "$SESSION" -p 0 -p 'pattern'`。
- 可以通过 `Ctrl+p d` 来断开连接（zellij 的默认断开方式）。

## 启动进程

- 对于 Python REPL，zellij 可以很好地与标准命令 `python3 -q` 配合使用。
- 不需要像 tmux 中的 `PYTHON_BASIC_REPL=1` 这样的特殊标志。

## Windows / WSL

- zellij 支持 macOS/Linux。在 Windows 上，可以使用 WSL 并在 WSL 中安装 zellij。
- 该技能仅适用于 `darwin`/`linux` 环境，并要求 `zellij` 在系统路径（PATH）中。

## 编程代理的协调（Codex、Claude Code）

zellij 在并行运行多个编程代理方面表现出色：

```bash
DATA_DIR="${TMPDIR:-/tmp}/codex-army-data"

# Create multiple sessions
for i in 1 2 3 4 5; do
  zellij --data-dir "$DATA_DIR" new-session --session "agent-$i" --layout "compact" --detach
done

# Launch agents in different workdirs
zellij --data-dir "$DATA_DIR" action --session "agent-1" write-chars --chars "cd /tmp/project1 && codex --yolo 'Fix bug X'\n"
zellij --data-dir "$DATA_DIR" action --session "agent-2" write-chars --chars "cd /tmp/project2 && codex --yolo 'Fix bug Y'\n"

# Poll for completion (check if prompt returned)
for sess in agent-1 agent-2; do
  pane_id=$(zellij --data-dir "$DATA_DIR" list-sessions --long | grep "\"$sess\"" | jq -r '.tabs[0].panes[0].id')
  if zellij --data-dir "$DATA_DIR" pipe --session "$sess" --pane-id "$pane_id" | grep -q "❯"; then
    echo "$sess: DONE"
  else
    echo "$sess: Running..."
  fi
done

# Get full output from completed session
zellij --data-dir "$DATA_DIR" pipe --session "agent-1" --pane-id 0
```

**提示：**
- 为并行修复任务使用不同的 Git 工作目录（以避免分支冲突）。
- 在新克隆的代码仓库中运行 Codex 之前，请先执行 `pnpm install`。
- 通过检查 shell 提示符（`❯` 或 `$`）来判断操作是否完成。
- 对于非交互式修复任务，Codex 需要使用 `--yolo` 或 `--full-auto` 参数。

## 清理

- 结束一个会话：`zellij --data-dir "$DATA_DIR" delete-session --session "$SESSION"`。
- 结束某个数据目录下的所有会话：使用 `{baseDir}/scripts/cleanup-sessions.sh "$DATA_DIR"`。

## zellij 与 tmux 的快速对比

| 任务 | tmux | zellij |
|------|------|--------|
| 列出会话 | `list-sessions` | `list-sessions` |
| 创建会话 | `new-session -d` | `new-session --detach` |
| 连接窗口 | `attach -t` | `attach --session` |
| 发送按键 | `send-keys` | `action write-chars` |
- 捕获窗口输出 | `capture-pane` | `pipe` |
- 结束会话 | `kill-session` | `delete-session` |
- 断开连接 | `Ctrl+b d` | `Ctrl+p d` |

## 帮助工具：wait-for-text.sh

`{baseDir}/scripts/wait-for-text.sh` 会定期检查窗口内容，以匹配指定的正则表达式或固定字符串。

```bash
{baseDir}/scripts/wait-for-text.sh -s session -p pane-id -r 'pattern' [-F] [-T 20] [-i 0.5]
```

- `-s`/`--session`：会话名称（必填）
- `-p`/`--pane-id`：窗口 ID（必填）
- `-r`/`--pattern`：要匹配的正则表达式（必填）；使用 `-F` 表示固定字符串
- `-T`：超时时间（秒，默认为 15 秒）
- `-i`：检查间隔时间（秒，默认为 0.5 秒）

## 帮助工具：find-panes.sh

`{baseDir}/scripts/find-panes.sh` 会列出指定会话的所有窗口。

```bash
{baseDir}/scripts/find-panes.sh -s session [-d data-dir]
```

- `-s`/`--session`：会话名称（必填）
- `-d`/`--data-dir`：zellij 的数据目录（如果未指定，则使用 `CLAWDBOT_ZELLIJ_DATA_DIR`）