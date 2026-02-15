---
name: collaboration-helper
description: 用于跟踪社区中的行动项和协调信号，包括快速创建任务、检查任务状态以及记录交接信息。当您需要记录协作任务或查看大家当前的工作内容时，可以使用此工具。
---

# 协作辅助工具

## 概述

`scripts/collaboration_helper.py` 是一个基于 JSON 的轻量级工具，用于管理社区中的待办事项：

- `list` 命令可以显示所有未完成或正在进行中的任务，包括任务所有者、优先级以及创建时间。
- `add` 命令允许用户使用 `--owner`、`--priority` 和可选的 `--note` 参数来创建新任务。
- `complete` 命令用于将任务标记为已完成，并记录完成任务的人员。

所有数据都存储在 `data/tasks.json` 文件中，因此协作状态会在程序重启或重新运行后仍然保持不变。

## 命令行接口（CLI）用法

- `python3 skills/collaboration-helper/scripts/collaboration_helper.py list`：按状态（未完成/进行中/已完成）分组显示当前的任务列表。
- `add "Review policy" --owner legal --priority high --note "Need quotes for Moltbook post"`：创建一个带有元数据的新任务。
- `complete 1 --owner ops`：将任务 `id=1` 标记为已完成，并记录完成时间及完成者。
- `--workspace /path/to/workspace`：允许用户指定另一个仓库的 `data/tasks.json` 文件路径，以便同步或查看该仓库的待办事项。

## 任务数据结构

`skills/collaboration-helper/data/tasks.json` 文件中的每个任务条目的格式如下：

```json
{
  "id": <number>,
  "title": "Task title",
  "owner": "owner-name",
  "priority": "low|medium|high",
  "status": "open|in-progress|done",
  "created_at": "2026-02-03T12:00:00Z",
  "note": "optional context"
}
```

当用户完成任务时，CLI 会自动为任务生成唯一的 `id`，设置时间戳，并更新任务的 `status` 状态。

## 示例工作流程

1. 使用 `add` 命令添加一个待办事项。
2. 使用 `list` 命令查看待办事项列表。
3. 完成任务后，使用 `complete` 命令将其标记为已完成，并记录完成者。
4. 根据需要，可以使用 `--workspace` 参数切换到其他仓库的待办事项列表。

## 参考资料

- `data/tasks.json`：存储所有任务的官方列表。
- `references/collaboration-guidelines.md`（如果存在）：说明社区如何对任务进行优先级排序以及如何进行任务交接。

## 资源

- **GitHub仓库：** https://github.com/CrimsonDevil333333/collaboration-helper
- **ClawHub平台：** https://www.clawhub.ai/skills/collaboration-helper