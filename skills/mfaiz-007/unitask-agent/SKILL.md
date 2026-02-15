---
name: "unitask-agent"
description: "不要只是整理任务，而是要开始完成它们：将你的 OpenClaw 代理连接到 Unitask（unitask.app），以便能够以安全的方式管理任务，并利用优先级、标签、时间块等功能来高效完成任务。"
homepage: https://unitask.app
read_when:
  - User wants to manage Unitask tasks from an AI agent
  - User wants to time-block today using Unitask scheduled_start + duration_minutes
metadata: {"clawdbot":{"emoji":"✅","requires":{"env":["UNITASK_API_KEY"]},"primaryEnv":"UNITASK_API_KEY"}}
---

# Unitask Agent

## 目的

该技能允许AI代理使用**受限的API令牌**安全地管理用户的Unitask账户。
Unitask目前处于**公开测试阶段**，任何人都可以在`https://unitask.app`注册使用。

**支持的操作：**
- 列出任务
- 获取一个任务
- 创建任务
- 更新任务字段（`update_task`）
- 更新任务状态（`update_task_status`）
- 将子任务移动到不同的父任务下（`move_subtask`）
- 合并父任务（`merge_parent_tasks`）
- 列出/创建/更新/删除标签
- 为任务添加/删除标签
- 删除任务（软删除）
- 读取/更新设置（可选的一次性设置）
- 规划日常时间块（预览/应用）

**子任务：**
- 子任务是具有`parent_id`的任务。
- 可以通过`create_task`命令并指定`parent_id`来创建子任务。

## 所需设置

1. 如果用户还没有账户，请在`https://unitask.app`注册（公开测试阶段）。
2. 用户需要从“Unitask” -> “仪表盘” -> “设置” -> “API”中生成Unitask API令牌。
3. 将生成的令牌存储在代理/应用程序的秘密存储中，格式为：`UNITASK_API_KEY=<token>`。

**注意事项：**
- 严禁要求用户在聊天记录中粘贴完整的API令牌。

## 权限模型

- `read`：用于读取和列出任务。
- `write`：用于创建、更新、移动和合并任务。
- `delete`：用于删除任务。
- 如果授予了`write`或`delete`权限，则必须同时授予`read`权限。

## 托管MCP（unitask.app，HTTPS）

**端点：**
- `https://unitask.app/api/mcp`

**推荐的身份验证头：**
- `Authorization: Bearer <UNITASK_API_KEY>`

## MCP工具

- `list_tasks` — 按状态（`todo|done`）、`limit`、`offset`、`parent_id`、`tag_id`筛选任务
  - 高级筛选条件：`view`（`today|upcoming`）、`tz`、`window_days`、`due_from`、`due_to`、`start_from`、`start_to`、`sort_by`、`sort_dir`
- `get_task` — 获取一个任务
- `create_task` — 创建任务或子任务
- `update_task` — 全面更新任务字段
- `update_task_status` — 仅用于更新任务状态
- `move_subtask` — 在不同父任务之间移动子任务（默认设置为`dry_run`）
- `merge_parent_tasks` — 合并父任务树（默认设置为`dry_run`）
- `delete_task` — 软删除任务及其所有子任务
- `list_tags` — 列出可用标签
- `get_tag` — 获取一个标签
- `create_tag` — 创建标签
- `update_tag` — 修改标签名称/颜色或删除标签
- `delete_tag` — 软删除标签
- `add_task_tag` — 为任务添加标签
- `remove_task_tag` — 从任务中删除标签
- `get_settings` — 获取用户设置
- `update_settings` — 更新设置
- `plan_day_timeblocks` — 预览/应用时间安排

## 安全规则

- 仅为请求的操作授予最低必要的权限范围。
- 在公开测试阶段，根据工作流程仅授予最低权限：`read`、`write`、`delete`。
- 除非用户明确同意，否则不要执行具有破坏性的操作（如删除）。
- 当目的是完成任务时，优先选择将任务状态设置为`done`。
- 对于`move_subtask`和`merge_parent_tasks`操作，先设置为`dry_run=true`，确认后再执行实际操作。