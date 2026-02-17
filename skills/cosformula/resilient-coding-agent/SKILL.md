---
name: resilient-coding-agent
description: "在 tmux 会话中运行长时间运行的编码代理程序（如 Codex、Claude Code 等），这些会话能够在编排器重启后继续运行，并且在中断时能够自动恢复。"
metadata:
  openclaw:
    emoji: "🛡️"
    requires:
      bins: [tmux]
      anyBins: [codex, claude, opencode, pi]
---
# 弹性编码代理

长时间运行的编码代理任务（如 Codex CLI、Claude Code、OpenCode、Pi）容易受到中断的影响：例如编排器重启、进程崩溃或网络连接中断。本技能通过使用 tmux 将编码代理进程与编排器分离，并利用代理自身的会话恢复功能来实现任务的继续执行。

**占位符说明：**  
- `<task-name>` 和 `<project-dir>` 由编排器填充。`<task-name>` 必须仅包含字母、数字和下划线（`[a-z0-9-]`）。`<project-dir>` 必须是存在的有效目录路径。  

**提示安全性：**  
任务提示不会被直接插入到 shell 命令中。相反，使用编排器的 `write` 工具将提示内容写入临时文件（不涉及 shell），然后在 tmux 命令中通过 `“(cat /tmp/<agent>-<task-name>.prompt)”` 来引用该文件。shell 会将双引号内的内容视为一个完整的参数，从而防止注入攻击。  

## 先决条件  
本技能假设编排器已配置为使用编码代理 CLI（如 Codex、Claude Code 等）来执行编码任务，而不是使用传统的会话管理方式。如果编排器仍在使用 `sessions_spawn` 来处理编码任务，请通过 `agents.md` 或相应配置文件将其优先设置为使用编码代理。具体设置方法请参考 `coding-agent` 技能文档。  

## 适用场景  
- 任务预计耗时超过 5 分钟  
- 编排器可能在任务执行过程中重启  
- 需要执行一次性的任务并接收完成通知  

对于耗时不到 5 分钟的快速任务，可以直接运行编码代理。  

## 启动任务  
创建一个具有描述性名称的 tmux 会话。使用相应的代理前缀（如 `codex-`、`claude-` 等）以便于识别。  

### Codex CLI  
```bash
# Step 1: Write prompt to file (use orchestrator's write tool, not echo/shell)
# File: /tmp/codex-<task-name>.prompt

# Step 2: Launch in tmux
tmux new-session -d -s codex-<task-name>
tmux send-keys -t codex-<task-name> 'cd <project-dir> && set -o pipefail && codex exec --full-auto --json "$(cat /tmp/codex-<task-name>.prompt)" | tee /tmp/codex-<task-name>.events.jsonl && echo "__TASK_DONE__"' Enter

# Capture this task's Codex session ID at start; resume --last is unsafe with concurrent tasks.
until [ -s /tmp/codex-<task-name>.codex-session-id ]; do
  sed -nE 's/.*"thread_id":"([^"]+)".*/\1/p' /tmp/codex-<task-name>.events.jsonl 2>/dev/null | head -n 1 > /tmp/codex-<task-name>.codex-session-id
  sleep 1
done
```  

### Claude Code  
```bash
# Write prompt to /tmp/claude-<task-name>.prompt first
tmux new-session -d -s claude-<task-name>
tmux send-keys -t claude-<task-name> 'cd <project-dir> && claude -p "$(cat /tmp/claude-<task-name>.prompt)" && echo "__TASK_DONE__"' Enter
```  

### OpenCode / Pi  
```bash
# Write prompt to /tmp/opencode-<task-name>.prompt first
tmux new-session -d -s opencode-<task-name>
tmux send-keys -t opencode-<task-name> 'cd <project-dir> && opencode run "$(cat /tmp/opencode-<task-name>.prompt)" && echo "__TASK_DONE__"' Enter

# Write prompt to /tmp/pi-<task-name>.prompt first
tmux new-session -d -s pi-<task-name>
tmux send-keys -t pi-<task-name> 'cd <project-dir> && pi -p "$(cat /tmp/pi-<task-name>.prompt)" && echo "__TASK_DONE__"' Enter
```  

### 完成通知（可选）  
在代理任务执行完成后，添加一个通知命令，以便了解任务是否已完成。在 `echo "__TASK_DONE__"` 命令前添加分号（`;`），这样即使通知命令失败，该标记也会被显示：  
```bash
# Generic: touch a marker file
tmux send-keys -t codex-<task-name> 'cd <project-dir> && codex exec --full-auto "$(cat /tmp/codex-<task-name>.prompt)" && touch /tmp/codex-<task-name>.done; echo "__TASK_DONE__"' Enter

# macOS: system notification
tmux send-keys -t codex-<task-name> 'cd <project-dir> && codex exec --full-auto "$(cat /tmp/codex-<task-name>.prompt)" && osascript -e "display notification \"Task done\" with title \"Codex\""; echo "__TASK_DONE__"' Enter

# OpenClaw: system event (immediate wake)
tmux send-keys -t codex-<task-name> 'cd <project-dir> && codex exec --full-auto "$(cat /tmp/codex-<task-name>.prompt)" && openclaw system event --text "Codex done: <task-name>" --mode now; echo "__TASK_DONE__"' Enter
```  

## 监控进度  
在以下情况下检查任务进度：  
- 用户请求状态更新  
- 需要主动报告任务进展  

## 健康检查  
对于长时间运行的任务，应定期检查任务状态：  
1. 运行 `tmux has-session -t <agent-task>` 以确认 tmux 会话仍在运行。  
2. 运行 `tmux capture-pane -t <agent-task> -p -S -<N>` 以捕获最近的输出信息。  
3. 通过检查最后 `N` 行来判断任务是否完成：  
   - 是否返回了 shell 提示符（例如 `$`、`%` 或 `>`）  
   - 是否存在退出信号（如退出代码、状态码 `<非零>`、`exited`）  
   - 是否有完成标记（`__TASK_DONE__`）  
4. 如果检测到任务崩溃，在同一 tmux 会话中执行代理的恢复命令。  

在启动任务时，可以使用特定的标记来区分正常完成和崩溃情况：  
```bash
tmux send-keys -t codex-<task-name> 'cd <project-dir> && codex exec --full-auto "$(cat /tmp/codex-<task-name>.prompt)" && echo "__TASK_DONE__"' Enter
```  

对于 Codex 任务，在任务开始时将会话 ID 保存到 `/tmp/<session>.codex-session-id` 文件中（参见上述 **Codex CLI** 部分）。监控程序会读取该文件以恢复相应的任务会话。  
编排器应定期（每 3-5 分钟）执行此检查流程（可通过 cron 或后台定时器实现）。如果连续多次失败，可逐渐延长检查间隔（3 分钟、6 分钟、12 分钟等），并在代理恢复正常运行后停止检查。  

## 中断后的恢复  
对于自动检测到的崩溃情况，请参考上述 **健康检查** 部分进行恢复。  
如果需要手动干预，请参考以下内容：  
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

## 会话命名规则  
tmux 会话的命名格式为 `<agent>-<task-name>`：  
- `codex-refactor-auth`  
- `claude-review-pr-42`  
- `codex-bus-sim-physics`  
会话名称应简短、使用小写字母，并用连字符分隔。  

## 检查清单  
在启动长时间运行的任务之前，请执行以下操作：  
1. 如果任务耗时超过 5 分钟，优先选择使用 tmux 而不是直接执行任务。  
2. 为 tmux 会话指定相应的代理前缀。  
3. （可选）添加完成通知功能。  
4. 告知用户任务内容、tmux 会话名称及预计完成时间。  
5. 根据需要使用 `tmux capture-pane` 命令监控任务进度。  

## 限制  
- tmux 会话在系统重启时不会自动恢复（tmux 本身会被终止）。对于需要抵抗重启影响的任务，应使用编码代理自身的恢复功能（如 `codex exec resume <session-id>`、`claude --resume`）。  
- tmux 中的交互式提示需要手动执行 `tmux attach` 或 `tmux send-keys` 来处理。尽可能使用 `--full-auto`、`--yolo` 或 `-p` 标志来简化操作。