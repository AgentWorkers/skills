---
name: acp-background-runs
description: 将针对 ACP 或外部编码工具（如 Codex、Claude Code、Gemini CLI 和 OpenCode）的请求路由到非阻塞式的 OpenClaw 背景任务中执行，而不是在当前聊天窗口中同步执行这些请求。当用户希望将编码工作交给外部工具处理，并且希望当前对话能够继续进行而无需等待时，可以使用此功能。触发条件包括：`ACP`、`Codex`、`Claude Code`、`Gemini CLI`、`OpenCode`、`background run`、`background task`。
---
# ACP / Codex 背景运行机制

当用户请求使用 ACP 或其他外部编码工具（如 Codex、Gemini CLI、OpenCode）时，不要在当前聊天窗口中同步执行任务，而应通过 ACP 运行时系统来处理该任务。

## 默认规则

- 首选使用 `sessions_spawn` 方法，并设置 `runtime: "acp"` 以及相应的 `agentId`。
- 默认模式为 `mode: "run"`。
- 仅当用户明确要求进行交互式操作或需要线程绑定的会话时，才使用 `thread: true` 或 `mode: "session"`。
- 当目标仓库或目录已知时，需要设置 `cwd`。
- 使用绝对路径作为 `cwd`；不要直接使用 `~`，应先将其展开。
- 对于耗时较长的任务，可以适当增加 `runTimeoutSeconds` 的值；不要默认设置为 300 秒。
- 不要在当前对话中等待任务进度，也不要主动查询任务进度。
- 任务接受后立即回复用户，告知任务已在后台运行。
- 依赖 `sessions_spawn` 的完成通知来将最终结果发送回当前对话窗口。
- 仅当用户明确要求实时接收进度更新时，才使用 `streamTo: "parent"`。

## 默认处理方式

如果用户只是简单地发起一个 ACP/Codex 任务，并未明确请求持续的交互式会话，那么该任务将被视为一次性后台运行，不会阻塞当前对话窗口。只有在后台任务完成后，才会将结果发送回用户。

## 超时设置建议

- 对于快速读取、简单分析或轻量级任务：`runTimeoutSeconds: 120-300`。
- 对于常规编码任务、项目检查或小范围编辑：`runTimeoutSeconds: 600`。
- 对于研究、代码修改、文件生成、测试运行或需要生成较长报告的任务：`runTimeoutSeconds: 1200`。
- 对于明显耗时较长的任务，可根据需要进一步增加超时时间至 `1800-3600`。
- 不要将超时时间默认设置为 0；只有当用户明确表示不需要超时时，才使用 0。

## `mode` / `thread` 的决策规则

- 如果用户仅希望外部工具在后台完成任务，使用 `mode: "run"`。
- 如果用户希望在执行任务后继续与外部工具进行交互，使用 `thread: true`。
- 如果用户明确要求持续性的会话或长时间运行的上下文，同时使用 `thread: true` 和 `mode: "session"`。
- 如果没有持续交互的需求，不要开启 `mode: "session"`。

## `cwd` 的设置规则

- 当目标仓库、项目目录或工作目录已知时，需要设置 `cwd`。
- 建议使用绝对路径。
- 在将路径传递给 `sessions_spawn` 之前，先展开 `~` 符号。
- 如果用户未提供目录信息，但任务明确指向某个已知仓库，应在启动任务前根据上下文确定实际路径。

## ACP 不可用时的备用方案

- 首先尝试使用 `runtime: "acp"`。
- 仅当 ACP 的目标 `agentId` 无法使用、未配置或在当前环境中不可用时，才使用 `runtime: "subagent"`。
- 在切换到 `subagent` 时，需明确告知用户任务是通过 `subagent` 来执行的，而非通过原生 ACP 会话。
- 不要默默地切换到备用方案。

## 提交任务后的回复

默认回复如下：

“任务已接受，正在后台运行，完成后会在这里反馈结果。”

如果启用了 `streamTo: "parent"`，还需说明关键进度更新将通过该通道实时发送给用户。

## 禁止的操作

- 不要在当前对话窗口中同步执行应通过 ACP 处理的外部编码工具任务。
- 提交任务后不要主动查询任务进度。
- 不要使用 `sessions_list`、`sessions_history` 等工具来跟踪子会话的进度。
- 不要使用 `sleep` 或基于定时器的等待机制来模拟后台任务运行。
- 应依赖 `sessions_spawn` 的完成通知来获取最终结果。

## 推荐的参数模板

```json
{
  "task": "<user request>",
  "runtime": "acp",
  "agentId": "<codex|claude|gemini|opencode|...>",
  "mode": "run",
  "cwd": "/abs/path/if-known",
  "runTimeoutSeconds": 300
}
```

## 需要调整的情况

- 如果需要持续的多轮交互：添加 `thread: true`，并根据需要添加 `mode: "session"`。
- 如果任务可能需要运行数分钟：增加 `runTimeoutSeconds` 的值。
- 如果任务只是简单的读取操作：保持 `runTimeoutSeconds` 的值较小。
- 如果用户希望实时接收任务进度：添加 `streamTo: "parent"`。
- 如果 ACP 不可用但任务仍需在后台运行：需向用户解释备用方案，并使用 `runtime: "subagent"`。