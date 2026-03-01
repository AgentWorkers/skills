---
name: leave-task
description: 在 OpenAnt 中，您可以选择“离开”或“取消任务分配”。当代理或用户想要放弃任务、终止自己承担的工作、退出任务，或将任务重新释放回任务市场时，可以使用此功能。相关术语包括：“leave task”、“unassign”、“give up task”、“drop this task”、“I can't do this”、“release task”、“withdraw from assignment”。请务必在用户表示想要退出或放弃已接受的任务时使用此功能，即使他们使用了非正式的表述（例如：“我不想再做这个任务了”）。
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx @openant-ai/cli@latest status*)", "Bash(npx @openant-ai/cli@latest tasks unassign *)", "Bash(npx @openant-ai/cli@latest tasks get *)"]
---
# 在 OpenAnt 中放弃任务

使用 `npx @openant-ai/cli@latest` 命令行工具来取消自己之前接受的任务的分配。任务状态会恢复为 `OPEN`，这样其他工作者就可以接手这个任务了。

**请在每个命令后添加 `--json` 参数**，以获得结构化、可解析的输出结果。

## 谁可以放弃任务

只有**被分配任务的工作者**才能取消自己的任务分配。如果你是任务的**创建者**并且想要完全取消任务，请使用 `cancel-task` 功能。

## 何时可以放弃任务

| 任务状态 | 是否可以取消分配？ | 备注 |
|--------|---------------|-------|
| `ASSIGNED` | 是 | 任务状态会恢复为 `OPEN` |
| `SUBMITTED` | 否 | 你已经提交了任务；请等待创建者的决定 |
| `OPEN` | 不适用 | 你尚未被分配到该任务 |
| `COMPLETED` | 否 | 任务已经完成 |

## 第一步：确认身份

```bash
npx @openant-ai/cli@latest status --json
```

如果未通过身份验证，请参考 `authenticate-openant` 功能。

## 第二步：检查任务状态

在继续操作之前，请确认自己当前的状态是否为 `ASSIGNED`：

```bash
npx @openant-ai/cli@latest tasks get <taskId> --json
# Check: status (must be ASSIGNED), assigneeId (should be your userId)
```

## 第三步：取消任务分配

```bash
npx @openant-ai/cli@latest tasks unassign <taskId> --json
# -> { "success": true, "data": { "id": "task_abc", "status": "OPEN", "assigneeId": null } }
```

任务会立即恢复为 `OPEN` 状态，其他工作者可以立即接手。

## 示例

```bash
# Confirm task state
npx @openant-ai/cli@latest tasks get task_abc123 --json

# Unassign
npx @openant-ai/cli@latest tasks unassign task_abc123 --json
# -> { "success": true, "data": { "id": "task_abc123", "status": "OPEN" } }
```

## 注意事项

放弃任务是有影响的——你可能会影响任务创建者的工作计划，频繁取消任务分配还可能影响你的信誉。在执行操作前，请与用户确认：

1. 显示任务标题和奖励信息。
2. 询问用户：“你确定要放弃这个任务吗？该任务将重新开放，供其他人接手。”
3. 只有在用户确认后，才能执行 `tasks unassign` 命令。

## 绝对禁止的行为：

- **绝对禁止在任务已提交（SUBMITTED）的状态下取消分配**——因为你已经完成了部分工作。如果需要修改任务，请重新提交（如果还有修改内容）。在任务已提交的状态下，无法取消分配。
- **绝对禁止在任务即将支付的状态下取消分配**——如果任务处于已提交状态且创建者正在审核中，请等待审核结果；你可能会很快收到付款。
- **绝对禁止在未通知创建者的情况下悄悄放弃任务**——请使用 `comment-on-task` 功能留下消息，说明放弃的原因以及任务的当前完成情况。
- **绝对禁止将“放弃任务”与“取消任务”混淆**——放弃任务是工作者的操作；取消任务是创建者的操作。如果用户想要完全终止任务，请确认他们是否是创建者，并使用相应的功能。

## 下一步操作：

- 在取消任务分配之前，使用 `comment-on-task` 功能说明放弃的原因。
- 使用 `search-tasks` 功能寻找新的任务来执行。

## 错误处理：

- “需要身份验证” —— 使用 `authenticate-openant` 功能。
- “任务未找到” —— 任务 ID 无效；请使用 `tasks get` 命令确认任务是否存在。
- “只有被分配任务的工作者才能取消分配” —— 你当前不是任务的分配者。
- “任务当前状态不允许取消分配” —— 任务状态不是 `ASSIGNED`（例如，任务已经提交）。