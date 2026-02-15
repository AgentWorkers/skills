# 技能：项目经理（Vivi OS）

## 描述
该技能用于管理基于 JSON 的内部项目系统。支持创建任务、在看板中移动任务，并与 Apple Reminders 进行同步。

## 数据存储位置
数据库：`/Users/fz1/clawd/data/pm/projects.json`

## 命令（思维模型）

### 1. 列出任务
*   **操作**：读取 JSON 数据，并按列分组或按项目筛选任务。
*   **用途**：用于查看待办事项或了解 SaaS 项目的状态。

### 2. 添加任务（Add）
*   **操作**：将任务对象添加到 `tasks` 数组中。
*   **所需字段**：`projectId`、`title`、`priority`（低/中/高/紧急）、`sync`（true/false）。
*   **附加效果**：如果 `sync: true`，则会触发 `apple-reminders` 技能来创建提醒。

### 3. 移动任务（Move）
*   **操作**：更新任务的状态。
*   **状态**：`todo` -> `in_progress` -> `review` -> `done`（或 `blocked`）。
* **通知**：如果任务状态变为 `review` 或 `blocked`，需通过聊天通知 David。

### 4. 同步（Sync）
*   **操作**：当任务状态发生变化时，使用 `sync: true` 强制更新 Apple Reminders 中的任务信息。

## 业务规则
1. **审核**：只有在使用 David 的明确批准后，才能将任务状态从 `todo` 更改为 `review`。
2. **专注原则**：同一时间最多只能有 3 个任务处于 `in_progress` 状态。
3. **夜间值班**：夜间值班人员需要查看此 JSON 文件，以便在没有明确任务安排时确定优先处理事项。