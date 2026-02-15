---
name: tasks
description: "使用 `todoist` CLI 管理 Todoist 任务。可以通过命令行添加、列出和完成任务。"
metadata:
  {
    "openclaw":
      {
        "emoji": "✅",
        "requires": { "bins": ["todoist"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "todoist-api-python",
              "bins": ["todoist"],
              "label": "Install Todoist API (pip)",
            },
          ],
      },
  }
---

# 任务技能

该技能封装了 Todoist 和 Microsoft To-Do 的 API，用于添加、列出和完成任务。需要使用环境变量 `TODOIST_API_TOKEN` 或 `MSGRAPH_TOKEN`。

## 列出任务

显示所有待办任务：

```bash
todoist list
```

## 添加任务

创建一个新任务（可选设置截止日期）：

```bash
todoist add "Review PR #42" --due "2026-02-05"
```

## 完成任务

将任务标记为已完成：

```bash
todoist complete <task_id>
```

## 安装

```bash
pip install todoist-api-python
```