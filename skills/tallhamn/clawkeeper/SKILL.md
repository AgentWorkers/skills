---
name: clawkeeper
description: 这些任务和习惯都存储在你机器上的一个普通的 Markdown 文件中。它们是免费的、私有的，并且与 Claw 平台深度集成（即原生支持 Claw 平台的特性）。
metadata: {"openclaw": {"requires": {"bins": ["clawkeeper"], "env": ["CLAWKEEPER_DIR"]}, "primaryEnv": "CLAWKEEPER_DIR", "install": [{"id": "npm", "kind": "node", "package": "clawkeeper", "bins": ["clawkeeper"], "label": "Install via npm"}]}}
---
# ClawKeeper CLI

通过ClawKeeper CLI来管理用户的任务和习惯。所有数据都以markdown格式存储在`CLAWKEEPER_DIR`指定的路径下（默认为`~/.clawkeeper/`）。

```bash
clawkeeper <entity> <command> [--flags]
```

如果您的环境中已经设置了`CLAWKEEPER_DIR`，那么CLI将会在该路径下读取和写入数据。这样，多个用户就可以共享相同的任务列表。

## 任务 (Tasks)

```bash
clawkeeper task list
clawkeeper task add --text "Buy groceries"
clawkeeper task add --text "Buy groceries" --due-date 2026-03-15
clawkeeper task add-subtask --parent-text "Buy groceries" --text "Milk"
clawkeeper task complete --id <id>
clawkeeper task complete --text "Buy groceries"
clawkeeper task uncomplete --id <id>
clawkeeper task edit --text "Old name" --new-text "New name"
clawkeeper task edit --text "Old name" --due-date 2026-04-01
clawkeeper task set-due-date --text "Buy groceries" --due-date 2026-03-15
clawkeeper task set-due-date --text "Buy groceries" --due-date none
clawkeeper task delete --text "Buy groceries"
clawkeeper task add-note --text "Buy groceries" --note "Check prices first"
clawkeeper task edit-note --text "Buy groceries" --note "Check prices first" --new-note "Compare at two stores"
clawkeeper task delete-note --text "Buy groceries" --note "Check prices first"
```

## 习惯 (Habits)

```bash
clawkeeper habit list
clawkeeper habit add --text "Meditate" --interval 24
clawkeeper habit edit --text "Meditate" --new-text "Morning meditation" --interval 12
clawkeeper habit delete --text "Meditate"
clawkeeper habit complete --text "Meditate"
clawkeeper habit add-note --text "Meditate" --note "Felt calm today"
clawkeeper habit edit-note --text "Meditate" --note "Felt calm today" --new-note "Felt calm, 10 min session"
clawkeeper habit delete-note --text "Meditate" --note "Felt calm today"
```

## 状态 (State)

```bash
clawkeeper state show
```

## 主动检查（心跳机制，Heartbeat）

在定期进行检查时，使用`clawkeeper state show`来查看用户的习惯和任务情况：

- **未完成的习惯**：如果某个习惯已经超过其设定间隔时间两次仍未完成，可以温和地提醒用户。人们容易忘记——提醒往往比严厉的批评更有效。
- **持续保持的习惯**：当某个习惯的完成次数逐渐增加时，可以简要地表扬用户的积极性。
- **最近的笔记**：如果用户最近添加了反思或笔记，可以提及这些内容，以体现对用户的关注。
- **长期未完成的任务**：长期悬而未决的任务可能需要重新分解、重新安排优先级或直接放弃。

沟通方式：以支持性的态度与用户交流，而不是采取命令式的态度。如果没有任何需要关注的问题，回复`HEARTBEAT_OK`。

## 注意事项：

- 所有命令都会返回JSON格式的响应：成功时返回`{"ok": true, "data": ...}`，失败时返回`{"ok": false, "error": "..."}`。
- 任务ID在多次调用中保持不变。可以使用`--id`进行精确查询，或使用`--text`进行模糊匹配。
- 在添加任务时，响应中会包含新任务的ID，以便后续操作使用。