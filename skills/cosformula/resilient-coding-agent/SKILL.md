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
# 弹性编码代理（Resilient Coding Agent）

长时间运行的编码代理任务（如 Codex CLI、Claude Code、OpenCode、Pi）容易受到中断的影响：例如编排器重启、进程崩溃或网络连接中断。本方案通过 tmux 将编码代理进程与编排器分离，并利用代理自身的会话恢复功能来实现任务的继续执行。

## 前提条件

本方案假设编排器已配置为使用编码代理的 CLI（如 Codex、Claude Code 等）来执行编码任务，而非传统的会话管理方式。如果编排器仍在使用 `sessions_spawn` 来管理编码任务，请先通过 `AGENTS.md` 或相应配置文件将其设置为优先使用编码代理。具体配置方法请参考 “coding-agent” 部分。

## 适用场景

以下情况下建议使用本方案：
- 任务预计耗时超过 5 分钟；
- 编排器可能在任务执行过程中重启；
- 需要实现“一次启动、无需人工干预、任务完成后自动通知”的执行模式。

对于耗时少于 5 分钟的快速任务，直接运行编码代理即可。

## 启动任务

创建一个具有描述性名称的 tmux 会话。会话名称前缀应使用相应的代理名称（如 `codex-`、`claude-` 等），以便于识别。

### Codex CLI
```bash
tmux new-session -d -s codex-<task-name>
tmux send-keys -t codex-<task-name> 'cd <project-dir> && set -o pipefail && codex exec --full-auto --json "<task prompt>" | tee /tmp/codex-<task-name>.events.jsonl && echo "__TASK_DONE__"' Enter

# Capture this task's Codex session ID at start; resume --last is unsafe with concurrent tasks.
until [ -s /tmp/codex-<task-name>.codex-session-id ]; do
  sed -nE 's/.*"thread_id":"([^"]+)".*/\1/p' /tmp/codex-<task-name>.events.jsonl 2>/dev/null | head -n 1 > /tmp/codex-<task-name>.codex-session-id
  sleep 1
done
```

### Claude Code
```bash
tmux new-session -d -s claude-<task-name>
tmux send-keys -t claude-<task-name> 'cd <project-dir> && claude -p "<task prompt>" && echo "__TASK_DONE__"' Enter
```

### OpenCode / Pi
```bash
tmux new-session -d -s opencode-<task-name>
tmux send-keys -t opencode-<task-name> 'cd <project-dir> && opencode run "<task prompt>" && echo "__TASK_DONE__"' Enter

tmux new-session -d -s pi-<task-name>
tmux send-keys -t pi-<task-name> 'cd <project-dir> && pi -p "<task prompt>" && echo "__TASK_DONE__"' Enter
```

### 完成通知（可选）

在编码代理任务执行完成后，添加一个通知命令，以便及时获取任务完成信息。在 `echo "__TASK_DONE__"` 命令前加上分号（`;`），这样即使通知命令失败，该标记也会被正确显示：
```bash
# Generic: touch a marker file
tmux send-keys -t codex-<task-name> 'cd <project-dir> && codex exec --full-auto "<prompt>" && touch /tmp/codex-<task-name>.done; echo "__TASK_DONE__"' Enter

# macOS: system notification
tmux send-keys -t codex-<task-name> 'cd <project-dir> && codex exec --full-auto "<prompt>" && osascript -e "display notification \"Task done\" with title \"Codex\""; echo "__TASK_DONE__"' Enter

# OpenClaw: system event (immediate wake)
tmux send-keys -t codex-<task-name> 'cd <project-dir> && codex exec --full-auto "<prompt>" && openclaw system event --text "Codex done: <summary>" --mode now; echo "__TASK_DONE__"' Enter

# Webhook / curl
tmux send-keys -t codex-<task-name> 'cd <project-dir> && codex exec --full-auto "<prompt>" && curl -s -X POST <webhook-url> -d "task=done"; echo "__TASK_DONE__"' Enter
```

## 监控进度

在以下情况下需要监控任务进度：
- 用户请求进度更新；
- 需要主动报告任务的关键节点进展。

## 健康状态监控

对于长时间运行的任务，应采用主动监控机制，而不仅仅是按需检查：
1. 运行 `tmux has-session -t <agent-task>` 以确认 tmux 会话仍在运行。
2. 运行 `tmux capture-pane -t <agent-task> -p -S -<N>` 以捕获最近的输出信息。
3. 通过检查最后 `N` 行来判断任务是否正常完成：
   - 是否返回了 Shell 提示符（例如 `$`、`%` 或 `>`）；
   - 是否存在退出信号（如退出代码、非零状态码或 `exited`）；
  - 是否有任务完成的标记（`__TASK_DONE__`）。
4. 如果检测到任务崩溃，需在同一 tmux 会话中执行代理自身的恢复命令。

在启动任务时，使用特定的标记（如 `__TASK_DONE__`）以便监控脚本能够区分正常完成和崩溃情况：
```bash
tmux send-keys -t codex-<task-name> 'cd <project-dir> && codex exec --full-auto "<prompt>" && echo "__TASK_DONE__"' Enter
```

对于 Codex 任务，在任务开始时将会话 ID 保存到 `/tmp/<session>.codex-session-id` 文件中（具体方法参见上述 “Codex CLI” 部分）。监控脚本会读取该文件以恢复相应的任务会话。

在后台运行监控脚本：
```bash
./scripts/monitor.sh codex-<task-name> codex
# or: ./scripts/monitor.sh claude-<task-name> claude
```

脚本每 3 分钟检查一次任务进度。如果连续多次检测到任务失败，检查间隔会逐渐延长（3 分钟、6 分钟、12 分钟……），并在任务恢复正常后停止监控。监控脚本会在任务运行 5 小时后自动停止。

在启动长时间运行的任务时，建议通过 `&`、`nohup` 或编排器的 cron 任务在后台运行监控脚本，以确保任务能够自动恢复。

## 中断后的恢复

对于自动检测到的任务崩溃情况，可参考上述 “健康状态监控” 部分进行处理。如果需要手动干预，可参考以下内容：
```bash
# Codex (prefer explicit session ID from /tmp/<session>.codex-session-id)
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

## 命名规则

tmux 会话的命名格式为 `<agent>-<task-name>`，例如：
- `codex-refactor-auth`
- `claude-review-pr-42`
- `codex-bus-sim-physics`

会话名称应简短、使用小写字母，并通过连字符分隔。

## 检查清单

在启动长时间运行的任务之前，请遵循以下步骤：
1. 如果任务耗时超过 5 分钟，优先选择使用 tmux 而不是直接执行任务；
2. 为 tmux 会话添加相应的代理前缀；
3. （可选）添加完成通知功能；
4. 向用户告知任务内容、tmux 会话名称及预计完成时间；
5. 根据需要使用 `tmux capture-pane` 命令监控任务进度。

## 限制事项
- tmux 会话无法在系统重启后继续运行（tmux 本身会被终止）。对于需要抵抗重启影响的任务，应使用编码代理的本地恢复功能（如 `codex exec resume <session-id>`、`claude --resume`）。
- tmux 中的交互式确认操作需要手动执行 `tmux attach` 或 `tmux send-keys` 命令。如果可能，请使用 `--full-auto`、`--yolo` 或 `-p` 标志来简化操作。