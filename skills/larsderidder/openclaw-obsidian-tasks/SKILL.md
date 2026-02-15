---
name: obsidian-tasks
description: 使用 Kanban 和 Dataview 来设置和管理 Obsidian 任务板。创建一个名为 `Tasks/Board.md` 的管道文件（用于管理任务的状态：待办（Backlog）、进行中（In Progress）、审核中（Review）和已完成（Done）），并为每个任务添加使用 YAML 格式编写的备注（包括状态、优先级、类别和截止日期）。通过 Dataview 查询来生成仪表板，以便跟踪任务进度、在各个任务列之间移动卡片，并确保任务板与备注内容保持同步。同时，还可以将任务链接到相关的备注或研究资料。
---

# obsidian-tasks

在 Obsidian 文档库中，使用 Kanban 任务板、Dataview 仪表板和结构化的任务笔记来进行任务管理。

## 设置

运行设置脚本以在 Obsidian 文档库中初始化一个任务板：

```bash
python3 scripts/setup.py <vault-path> [--folder <name>] [--columns <col1,col2,...>]
```

- `vault-path`：Obsidian 文档库的根路径
- `--folder`：要创建的子文件夹（默认值：`Tasks`）
- `--columns`：Kanban 列（默认值：`Backlog`, `Todo`, `In Progress`, `Review`, `Done`）

这将创建以下文件：
- `<folder>/Board.md` – Kanban 任务板（需要安装 Kanban 社区插件）
- `<folder>/Dashboard.md` – Dataview 仪表板（需要安装 Dataview 社区插件）

如果尚未安装 **Kanban** 和 **Dataview** 社区插件，请告知用户进行安装。

## 任务笔记格式

每个任务都是一个独立的 markdown 文件，并包含 YAML 标头信息：

```markdown
---
status: todo
priority: P1
category: revenue
created: 2026-02-03
due: 2026-02-07
---

# Task Title

Description and notes here.

## References
- [[linked-document|Display Name]]

## Status
- [x] Step completed
- [ ] Step pending
```

### 标头信息字段

| 字段 | 值 | 是否必填 |
|-------|--------|----------|
| status | backlog, todo, in-progress, review, done | 是 |
| priority | P1, P2, P3 | 是 |
| category | 自由文本（例如：revenue, content, research, setup, project） | 是 |
| created | YYYY-MM-DD | 是 |
| due | YYYY-MM-DD | 否 |
| parked_until | YYYY-MM-DD | 否 |

### 任务板上的优先级标记

在 Kanban 任务板上使用表情符号前缀来表示任务的优先级：
- 🔴 P1（紧急）
- 🟡 P2（普通）
- 🟢 P3（待处理/暂存）

## 任务管理

### 创建任务

1. 在 `tasks` 文件夹中创建一个包含 YAML 标头信息的 markdown 文件。
2. 将该文件添加到 `Board.md` 文件中相应的列中：

```
- [ ] [[Task Name]] 🔴 P1 @{2026-02-07}
```

### 移动任务

1. 更新任务笔记中的 `status` 字段。
2. 将任务卡片在 `Board.md` 文件中移动到目标列。

### 完成任务

1. 在任务笔记的标头信息中设置 `status: done`。
2. 将任务卡片移动到 “Done” 列，并勾选完成复选框：

```
- [x] [[Task Name]] ✅ 2026-02-03
```

### 请始终同时更新 `Board.md` 和任务笔记的标头信息，以保持它们的一致性。

## 链接文档

使用 Obsidian 的 `[[wikilinks]]` 功能将任务与相关文档关联起来：

```markdown
## References
- [[2026-02-03-research-report|Research Report]]
- [[meeting-notes-jan|Meeting Notes]]
```

将引用的文档存储在同一个文件夹的子文件夹中（例如：`Research/`，位于 `Tasks/` 旁边）。

## 仪表板查询

设置脚本会创建一个 Dataview 仪表板。以下是核心查询示例：

**按优先级显示任务：**
```dataview
TABLE status, category, due
FROM "<tasks-folder>"
WHERE priority = "P1" AND status != "done"
SORT due ASC
```

**逾期任务：**
```dataview
TABLE priority, category
FROM "<tasks-folder>"
WHERE due AND due < date(today) AND status != "done"
SORT due ASC
```

**最近完成的任务：**
```dataview
TABLE category
FROM "<tasks-folder>"
WHERE status = "done"
SORT file.mtime DESC
LIMIT 10
```