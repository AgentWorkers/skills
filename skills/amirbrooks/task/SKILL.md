---
name: task
description: 通过 `tool-dispatch` 管理 Tasker 的文档存储（docstore）中的任务。可用于查看任务列表、判断任务是否为今日到期/逾期任务、进行周计划安排，以及执行添加、移动、完成任务等操作，或直接使用 `/task` 命令来管理任务。
user-invocable: true
disable-model-invocation: false
command-dispatch: tool
command-tool: tasker_cmd
command-arg-mode: raw
metadata: {"clawdbot":{"emoji":"🗂️"}}
---

将与任务相关的请求路由到 `tasker_cmd`（仅传递原始参数，不要包含前缀 `tasker`）。

- 对于自然语言输入，将其转换为 CLI 参数。
- 对于形如 `/task ...` 的请求，直接传递参数，不做任何修改。
- 优先选择易于人类阅读的输出格式。除非用户明确要求，否则避免使用 `--stdout-json`/`--stdout-ndjson`。
- 为了适应聊天应用（如 Telegram/WhatsApp）的输出格式，添加 `--format telegram`。仅在用户明确请求显示所有任务或已归档的任务时使用 `--all`。
- 这是针对自然语言输入的默认处理方式；如果用户仅使用斜杠（/）来输入命令，请使用 `skills/task-slash/`。
- 如果用户输入了 ` | `（空格-管道-空格），建议使用 `--text "<title | details | due 2026-01-23>"`，以便 CLI 能够正确解析任务的详细信息、截止日期和标签。只有在用户明确指定 ` | ` 作为分隔符时才进行分割，以避免损坏标题信息。
- 不要自行猜测分隔符（如 "but" 或 "—"）；仅根据用户输入的 ` | ` 进行分割。
- 如果用户询问为什么使用 `tasker` 而不是简单的 Markdown 列表，可以解释如下：“Tasker 保留了 Markdown 的格式，同时添加了结构化的元数据和可预测的输出格式，并且会隐藏机器生成的唯一标识符（ID），从而让用户更易于理解任务信息。”
- 如果某个选择器的输入看起来不完整，可以运行 `resolve "<query>"`（该命令会使用智能的默认处理方式；`--match search` 会包含任务的备注和正文内容），然后在找到唯一匹配项时根据其 ID 来执行相应的操作。在最终输出中绝不要显示任务的 ID。
- 对于添加任务备注的操作，建议使用 `note add <selector...> -- <text...>` 的格式，以避免歧义；如果不使用 `--` 参数，`tasker` 会尝试自动判断分隔符的位置。

常见命令映射：
- "tasks today" / "overdue" -> `tasks --open --format telegram`（显示今日的所有任务及逾期任务）
- "what's our week" -> `week --days 7 --format telegram`（显示本周的所有任务）
- "show tasks for Work" -> `tasks --project Work --format telegram`（显示属于 "Work" 项目的所有任务）
- "show board" -> `board --project <name> --format telegram`（显示指定项目的任务列表）
- "add <task> today" -> `add "<task>" --today [--project <name>] --format telegram`（今天添加名为 `<task>` 的任务）
- "add <task> | <details>" -> `add --text "<task> | <details>" --format telegram`（添加名为 `<task>` 的任务，并附上详细信息）
- "capture <text>" -> `capture "<text>" --format telegram`（捕获并显示文本内容）
- "mark <title> done" -> `done "<title>"`（将任务 `<title>` 标记为已完成）
- "show config" -> `config show`（显示配置信息）