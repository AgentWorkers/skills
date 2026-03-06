---
name: tasks-md-sprint-sync
description: 将 `Sync TASKS.md` 文件中当前阶段的任务列表以及正在进行中的任务清单，同步到活跃的 `PLAN.md` 文件中的阶段，以确保冲刺执行的顺利进行。
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---
# Tasks.md 项目同步工具

使用此工具可确保项目的 `TASKS.md` 部分与 `PLAN.md` 中标记为 `IN PROGRESS`（进行中）的阶段保持一致。

## 该工具的功能：
- 从 `PLAN.md` 中读取当前进行中的阶段（状态为 `**Status: IN PROGRESS**` 的阶段）
- 从该阶段的 `### Work` 部分中提取任务列表
- 在 `TASKS.md` 中找到对应的目标项目部分
- 检查计划中的工作项与 `### In progress`（进行中）任务之间的差异
- 可选：更新 `TASKS.md` 以匹配计划中的阶段及相应的任务列表

## 输入参数：
- `PROJECT_NAME`（`TASKS.md` 文件中的项目名称，例如 `ClawHub Skills`）
- `PLAN_FILE`（可选参数，默认值为 `PLAN.md`）
- `TASKS_FILE`（可选参数，默认值为 `TASKS.md`）
- `SYNC_MODE`（可选参数，`report` 或 `apply`，默认值为 `report`）

## 使用方法：
- **生成差异报告：**
  ```bash
  ```bash
PROJECT_NAME="ClawHub Skills" \
PLAN_FILE=projects/clawhub-skills/PLAN.md \
TASKS_FILE=TASKS.md \
bash skills/tasks-md-sprint-sync/scripts/sync-tasks-phase.sh
```
  ```
- **更新 `TASKS.md`：**
  ```bash
  ```bash
PROJECT_NAME="ClawHub Skills" \
PLAN_FILE=projects/clawhub-skills/PLAN.md \
TASKS_FILE=TASKS.md \
SYNC_MODE=apply \
bash skills/tasks-md-sprint-sync/scripts/sync-tasks-phase.sh
```
  ```
- **针对指定文件进行同步：**
  ```bash
  ```bash
PROJECT_NAME="Demo Project" \
PLAN_FILE=skills/tasks-md-sprint-sync/fixtures/PLAN.sample.md \
TASKS_FILE=skills/tasks-md-sprint-sync/fixtures/TASKS.sample.md \
SYNC_MODE=apply \
bash skills/tasks-md-sprint-sync/scripts/sync-tasks-phase.sh
```
  ```

## 输出结果：
- 如果报告或更新操作完成，程序退出状态码 `0`
- 如果输入无效、缺少必要信息或没有正在进行中的阶段，程序退出状态码 `1`
- 在 `report` 模式下：仅输出差异报告，不修改文件内容
- 在 `apply` 模式下：更新 `TASKS.md` 中的 `Current phase` 部分，并替换 `In progress` 列表

---

（注：由于代码块内容通常包含具体的命令或脚本，这里仅保留了注释格式的说明。实际使用时需要替换为相应的命令。）