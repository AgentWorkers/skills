---
name: resilient-coding-agent
description: "在 tmux 会话中运行长时间运行的编码代理程序（如 Codex、Claude Code 等），这些会话能够在编排器重启后继续运行，并在任务中断时自动恢复。"
metadata:
  openclaw:
    emoji: "🛡️"
    requires:
      bins: [tmux]
      anyBins: [codex, claude, opencode, pi]
---
# 弹性编码代理

长时间运行的编码代理任务（如 Codex CLI、Claude Code、OpenCode、Pi）容易受到中断的影响：例如编排器重启、进程崩溃或网络连接中断。本方案通过 tmux 将编码代理进程与编排器分离，并利用代理自身的会话恢复功能来实现任务的持续执行。

**注意事项：**
- `<task-name>` 和 `<project-dir>` 由编排器填充。`<task-name>` 必须仅包含字母、数字和下划线（`[a-z0-9-]`）。`<project-dir>` 必须是存在的有效目录路径。
- **临时目录**：每个任务会使用 `mktemp -d` 命令创建一个安全的临时目录，将该目录路径存储为 `<tmpdir>`，并用于存储所有任务相关文件（包括提示信息、事件记录、会话 ID 和完成标记）。这样可以避免文件名过于容易被预测，从而避免潜在的安全问题。例如：`TMPDIR=$(mktemp -d)` 会生成类似 `/var/folders/xx/.../T/tmp.aBcDeFgH` 的目录。
- **提示信息的安全性**：任务提示信息不会被直接插入到 shell 命令中。而是通过编排器的 `write` 工具将提示信息写入临时文件（不涉及 shell），然后在 tmux 命令中使用 `“(cat $TMPDIR/prompt)”` 来引用该文件。这样，shell 会将双引号内的内容视为一个普通的字符串参数，从而防止注入攻击。这依赖于编排器的 `write` 工具不调用 shell；OpenClaw 的内置 `write` 工具符合这一要求。
- **敏感数据**：tmux 的滚动记录和事件日志文件可能包含代理输出的敏感信息（如 API 密钥）。在共享机器上，应限制文件的权限（使用 `chmod 600`），并在任务完成后清理临时目录。

## 先决条件**

本方案假设编排器已经配置为使用编码代理的 CLI（如 Codex、Claude Code 等）来执行编码任务，而不是使用传统的会话模式。如果编排器仍在使用 `sessions_spawn` 来执行编码任务，请通过 `agents.md` 或相应配置文件将其优先设置为使用编码代理。具体配置方法请参考相关文档。

## 适用场景**

- 任务预计耗时超过 5 分钟。
- 编排器在执行过程中可能会重启。
- 需要实现“一键执行并接收完成通知”的功能。

对于耗时少于 5 分钟的快速任务，可以直接运行编码代理。

## 启动任务

创建一个具有描述性名称的 tmux 会话，并使用相应的代理前缀（如 `codex-`、`claude-` 等）以便于识别。

### Codex CLI
```bash
# Step 1: Create secure temp directory
TMPDIR=$(mktemp -d)
chmod 700 "$TMPDIR"

# Step 2: Write prompt to file (use orchestrator's write tool, not echo/shell)
# File: $TMPDIR/prompt

# Step 3: Launch in tmux (pass TMPDIR via env)
tmux new-session -d -s codex-<task-name> -e "TASK_TMPDIR=$TMPDIR"
tmux send-keys -t codex-<task-name> 'cd <project-dir> && set -o pipefail && codex exec --full-auto --json "$(cat $TASK_TMPDIR/prompt)" | tee $TASK_TMPDIR/events.jsonl && echo "__TASK_DONE__"' Enter

# Step 4: Capture this task's Codex session ID; resume --last is unsafe with concurrent tasks.
# Uses jq for reliable JSON parsing (falls back to grep if jq unavailable).
until [ -s "$TMPDIR/codex-session-id" ]; do
  if command -v jq &>/dev/null; then
    jq -r 'select(.thread_id) | .thread_id' "$TMPDIR/events.jsonl" 2>/dev/null | head -n 1 > "$TMPDIR/codex-session-id"
  else
    grep -oE '"thread_id":"[^"]+"' "$TMPDIR/events.jsonl" 2>/dev/null | head -n 1 | cut -d'"' -f4 > "$TMPDIR/codex-session-id"
  fi
  sleep 1
done
```

### Claude Code
```bash
# Create secure temp directory and write prompt to $TMPDIR/prompt first
TMPDIR=$(mktemp -d) && chmod 700 "$TMPDIR"
tmux new-session -d -s claude-<task-name> -e "TASK_TMPDIR=$TMPDIR"
tmux send-keys -t claude-<task-name> 'cd <project-dir> && claude -p "$(cat $TASK_TMPDIR/prompt)" && echo "__TASK_DONE__"' Enter
```

### OpenCode / Pi
```bash
# Create secure temp directory and write prompt to $TMPDIR/prompt first
TMPDIR=$(mktemp -d) && chmod 700 "$TMPDIR"

# OpenCode
tmux new-session -d -s opencode-<task-name> -e "TASK_TMPDIR=$TMPDIR"
tmux send-keys -t opencode-<task-name> 'cd <project-dir> && opencode run "$(cat $TASK_TMPDIR/prompt)" && echo "__TASK_DONE__"' Enter

# Pi (separate temp dir)
TMPDIR=$(mktemp -d) && chmod 700 "$TMPDIR"
tmux new-session -d -s pi-<task-name> -e "TASK_TMPDIR=$TMPDIR"
tmux send-keys -t pi-<task-name> 'cd <project-dir> && pi -p "$(cat $TASK_TMPDIR/prompt)" && echo "__TASK_DONE__"' Enter
```

### 完成通知（可选）

在代理任务执行完成后，添加一个通知命令，以便及时获取任务完成信息。在 `echo "__TASK_DONE__"` 命令前使用分号（`;`），以确保即使通知命令失败，完成标记也能正常显示：
```bash
# Generic: touch a marker file
tmux send-keys -t codex-<task-name> 'cd <project-dir> && codex exec --full-auto "$(cat $TASK_TMPDIR/prompt)" && touch $TASK_TMPDIR/done; echo "__TASK_DONE__"' Enter

# macOS: system notification
tmux send-keys -t codex-<task-name> 'cd <project-dir> && codex exec --full-auto "$(cat $TASK_TMPDIR/prompt)" && osascript -e "display notification \"Task done\" with title \"Codex\""; echo "__TASK_DONE__"' Enter

# OpenClaw: system event (immediate wake)
tmux send-keys -t codex-<task-name> 'cd <project-dir> && codex exec --full-auto "$(cat $TASK_TMPDIR/prompt)" && openclaw system event --text "Codex done: <task-name>" --mode now; echo "__TASK_DONE__"' Enter
```

## 监控进度

- 当用户请求进度更新时。
- 当需要主动报告任务进展时。

## 健康监控

对于长时间运行的任务，应使用主动监控机制，而不仅仅是按需检查。

**定期检查流程：**
1. 运行 `tmux has-session -t <agent-task>` 以确认 tmux 会话仍在运行。
2. 运行 `tmux capture-pane -t <agent-task> -p -S -<N>` 以捕获最近的输出内容。
3. 通过检查最后 `N` 行来判断代理是否正常退出：
   - 是否返回了 shell 提示信息（例如 `$`、`%` 或 `>` 等字符）。
   - 是否有退出提示（如 `exit code`、`status <non-zero>`、`exited` 等）。
  - 是否有完成标记（如 `__TASK_DONE__`）。
4. 如果检测到异常退出，可以在同一个 tmux 会话中执行代理的恢复命令。

在启动任务时，使用一个完成标记（done marker），以便监控系统能够区分正常完成和异常退出：
```bash
tmux send-keys -t codex-<task-name> 'cd <project-dir> && codex exec --full-auto "$(cat $TASK_TMPDIR/prompt)" && echo "__TASK_DONE__"' Enter
```

对于 Codex 任务，在任务开始时将会话 ID 保存到 `$TMPDIR/codex-session-id` 文件中（参见上面的 **Codex CLI** 部分）。监控系统可以通过读取该文件来恢复相应的任务会话。

编排器应定期（每 3-5 分钟）执行上述检查。如果连续多次失败，可以逐步延长检查间隔（3 分钟、6 分钟、12 分钟等），并在代理恢复正常运行后恢复正常的检查频率。整个监控过程最多持续 5 小时。

## 中断后的恢复

对于自动检测到的异常情况，可以使用上述的 **健康监控** 机制进行恢复。如果需要手动干预，可以参考以下内容：
```bash
# Codex (prefer explicit session ID from $TMPDIR/codex-session-id)
tmux send-keys -t codex-<task-name> 'codex exec resume <session-id> "Continue the previous task"' Enter

# Claude Code
tmux send-keys -t claude-<task-name> 'claude --resume' Enter

# OpenCode
tmux send-keys -t opencode-<task-name> 'opencode run "Continue"' Enter

# Pi: no native resume; re-run the task prompt manually
```

## 清理

任务完成后，终止 tmux 会话：
```bash
tmux kill-session -t codex-<task-name>
```

列出所有正在运行的编码代理 tmux 会话：
```bash
tmux list-sessions 2>/dev/null | grep -E '^(codex|claude|opencode|pi)-'
```

## 命名规则

tmux 会话的命名格式为 `<agent>-<task-name>`，例如：
- `codex-refactor-auth`
- `claude-review-pr-42`
- `codex-bus-sim-physics`

建议使用简短、小写的名称，并用连字符分隔各个部分。

## 检查清单

在启动长时间运行的任务之前，请遵循以下步骤：
1. 如果任务耗时超过 5 分钟，优先使用 tmux 会话而非直接执行任务。
2. 为 tmux 会话指定一个包含代理前缀的名称。
3. （可选）添加完成通知功能。
4. 向用户告知任务内容、tmux 会话名称及预计完成时间。
5. 根据需要使用 `tmux capture-pane` 功能监控任务进度。

## 限制因素**
- tmux 会话无法在机器重启后继续运行（tmux 本身会被终止）。对于需要抵抗重启影响的任务，应使用代理自身的恢复功能（如 `codex exec resume <session-id>`、`claude --resume`）。
- tmux 中的交互式确认提示需要手动执行 `tmux attach` 或 `tmux send-keys` 命令。如果可能的话，建议使用 `--full-auto`、`--yolo` 或 `-p` 等选项来简化操作。