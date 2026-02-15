---
name: claude-code-supervisor
description: >
  Supervise Claude Code sessions running in tmux. Uses Claude Code hooks with
  bash pre-filtering (Option D) and fast LLM triage to detect errors, stuck
  agents, and task completion. Harness-agnostic — works with OpenClaw, webhooks,
  ntfy, or any notification backend. Use when: (1) launching long-running Claude
  Code tasks that need monitoring, (2) setting up automatic nudging for API
  errors or premature stops, (3) getting progress reports from background coding
  agents, (4) continuing work after session/context limits reset.
  Requires: tmux, claude CLI.
metadata:
  {
    "openclaw":
      {
        "emoji": "👷",
        "os": ["darwin", "linux"],
        "requires": { "bins": ["tmux"], "anyBins": ["claude"] },
      },
  }
---

# Claude Code Supervisor

作为 Claude Code 生命周期钩子（lifecycle hooks）与您的代理系统（agent harness）之间的桥梁。

## 架构

```
Claude Code (in tmux)
  │  Stop / Error / Notification
  ▼
Bash pre-filter (Option D)
  │  obvious cases handled directly
  │  ambiguous cases pass through
  ▼
Fast LLM triage (claude -p with Haiku, or local LLM)
  │  classifies: FINE | NEEDS_NUDGE | STUCK | DONE | ESCALATE
  │  FINE → logged silently
  ▼
Notify command (configurable)
  │  openclaw wake, webhook, ntfy, script, etc.
  ▼
Agent harness decides + acts
  │  nudge (send-keys to tmux), wait, escalate to human
```

## 快速入门

### 1. 将钩子（hooks）安装到项目中

```bash
{baseDir}/scripts/install-hooks.sh /path/to/your/project
```

安装后，项目目录下会生成以下文件：
- `.claude/hooks/supervisor/`：包含钩子脚本及问题分类逻辑
- `.claude/settings.json`：用于配置 Claude Code 的生命周期事件
- `.claude-code-supervisor.yml`：配置文件（请编辑此文件）

### 2. 配置

编辑 `.claude-code-supervisor.yml` 文件以配置 Claude Code Supervisor 的行为：

```yaml
triage:
  command: "claude -p --no-session-persistence"  # or: ollama run llama3.2
  model: "claude-haiku-4-20250414"

notify:
  command: "openclaw gateway call wake --params"  # or: curl, ntfy, script
```

### 3. 注册被监控的会话

在您的代理系统中创建一个文件 `~/.openclaw/workspace/supervisor-state.json`（或根据实际情况选择其他存储位置）来保存会话状态：

```json
{
  "sessions": {
    "my-task": {
      "socket": "/tmp/openclaw-tmux-sockets/openclaw.sock",
      "tmuxSession": "my-task",
      "projectDir": "/path/to/project",
      "goal": "Fix issue #42",
      "successCriteria": "Tests pass, committed",
      "maxNudges": 5,
      "escalateAfterMin": 60,
      "status": "running"
    }
  }
}
```

### 4. 在 tmux 中启动 Claude Code

```bash
SOCKET="/tmp/openclaw-tmux-sockets/openclaw.sock"
tmux -S "$SOCKET" new -d -s my-task
tmux -S "$SOCKET" send-keys -t my-task "cd /path/to/project && claude 'Fix issue #42'" Enter
```

钩子会自动触发，问题分类逻辑会进行评估，只有在情况重要时才会向您发送通知。

## 预过滤机制的工作原理（选项 D）

并非所有钩子事件都需要调用大型语言模型（LLM）进行处理。Bash 会先处理一些显而易见的场景：

### on-stop.sh
| 信号类型 | Bash 的处理方式 | 是否需要 LLM 进行问题分类？ |
|--------|--------------|-------------|
| `max_tokens` | 总是需要处理 | ✅ 是 |
| `end_turn` + 命令行提示返回 | 代理可能已完成任务 | ✅ 是 |
| `end_turn` + 无提示 | 代理仍在执行任务 | ❌ 跳过 |
| `stop_sequence` | 普通情况 | ❌ 跳过 |

### on-error.sh
| 信号类型 | Bash 的处理方式 | 是否需要 LLM 进行问题分类？ |
|--------|--------------|-------------|
| API 429 / 超时限制 | 是暂时性错误，会自动恢复 | ❌ 仅记录日志 |
| API 500 | 代理可能卡住了 | ✅ 是 |
| 其他工具错误 | 严重程度未知 | ✅ 是 |

### on-notify.sh
| 信号类型 | Bash 的处理方式 | 是否需要 LLM 进行问题分类？ |
|--------|--------------|-------------|
| `auth_*` | 内部错误，暂时性问题 | ❌ 跳过 |
| `permission_prompt` | 需要人工决策 | ✅ 是 |
| `idle.prompt` | 代理处于等待状态 | ✅ 是 |

## 问题分类结果

大型语言模型会返回以下几种分类结果之一：

| 分类结果 | 含义 | 常见处理方式 |
|---------|---------|----------------|
| **FINE** | 代理运行正常 | 静默记录日志，不发送通知 |
| **NEEDS_NUDGE** | 是暂时性错误，可以继续执行 | 向 tmux 发送 “continue” 命令 |
| **STUCK** | 代理陷入循环或无法进展 | 尝试其他方法或请求人工协助 |
| **DONE** | 任务成功完成 | 向人工报告 |
| **ESCALATE** | 需要人工判断 | 带上下文信息通知人工 |

## 通知处理（针对代理系统开发者）

通知消息的前缀为 `cc-supervisor:`，后跟问题分类结果：

```
cc-supervisor: NEEDS_NUDGE | error:api_500 | cwd=/home/user/project | ...
cc-supervisor: DONE | stopped:end_turn:prompt_back | cwd=/home/user/project | ...
```

### 通过 tmux 发送提示

```bash
tmux -S "$SOCKET" send-keys -t "$SESSION" "continue — the API error was transient" Enter
```

### 升级处理流程

请参考 `references/escalation-rules.md` 以了解何时需要发送提示或升级处理，以及哪些时间段适合静默处理。

## 监控机制（谁来监控这些过程？）

钩子的正常运行依赖于 Claude Code 的状态。如果会话突然崩溃、达到账户使用限制或进程被操作系统终止（OOM），钩子将不会被触发。此时，监控机制会发挥作用。

`scripts/watchdog.sh` 是一个纯 Bash 脚本（不依赖大型语言模型或 Claude Code）：
1. 读取 `supervisor-state.json` 文件中所有处于 “running” 状态的会话信息
2. 检查 tmux 套接字是否存活、会话是否存在以及 Claude Code 是否仍在运行
3. 如果发现有问题但钩子未触发通知，则通过配置的命令进行通知
4. 更新 `lastWatchdogAt` 变量以记录监控时间

您可以选择以下方式来定时运行该脚本：
- **系统 cron**：```bash
*/15 * * * * /path/to/claude-code-supervisor/scripts/watchdog.sh
```
- **OpenClaw cron**：```json
{
  "schedule": { "kind": "every", "everyMs": 900000 },
  "payload": { "kind": "systemEvent", "text": "cc-supervisor: watchdog — run /path/to/scripts/watchdog.sh and report" },
  "sessionTarget": "main"
}
```
- **systemd、launchd 或其他定期执行的工具**

监控机制的设计非常简单：不依赖大型语言模型或复杂逻辑，仅检查进程是否仍在运行。这意味着即使在问题分类模型出现故障、API 无法正常工作或账户使用限制的情况下，它也能持续工作。

## 相关文件

- `scripts/install-hooks.sh`：用于为每个项目设置钩子的脚本
- `scripts/hooks/on-stop.sh`：处理停止事件的脚本（包含 Bash 预过滤逻辑）
- `scripts/hooks/on-error.sh`：处理错误事件的脚本（包含 Bash 预过滤逻辑）
- `scripts/hooks/on-notify.sh`：处理通知事件的脚本（包含 Bash 预过滤逻辑）
- `scripts/triage.sh`：负责问题分类的脚本（在不确定的情况下会被调用）
- `scripts/lib.sh`：包含配置加载和通知功能的共享库
- `scripts/watchdog.sh`：用于检测会话是否异常的脚本（纯 Bash 脚本）
- `references/state-patterns.md`：终端输出模式匹配指南
- `references/escalation-rules.md`：判断何时需要发送提示、升级处理或静默处理的规则
- `supervisor.yml.example`：配置文件示例