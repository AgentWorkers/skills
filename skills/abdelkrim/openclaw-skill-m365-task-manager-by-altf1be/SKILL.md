---
name: openclaw-skill-m365-task-manager-by-altf1be
description: "使用 Microsoft To Do 和 Planner 来管理轻量级的 Microsoft 365 任务工作流。当用户需要在 Microsoft 365 中快速创建、分配、跟踪和跟进操作性任务时，这些工具非常实用。这些任务会明确指定负责人、截止日期、状态，并提供每日提醒功能。"
homepage: https://github.com/ALT-F1-OpenClaw/openclaw-skill-m365-task-manager
metadata:
  {"openclaw": {"emoji": "✅", "requires": {"env": ["M365_TENANT_ID", "M365_CLIENT_ID"]}, "primaryEnv": "M365_TENANT_ID"}}
---
# M365 任务管理器

使用此技能可以对 Microsoft To-Do 任务执行实际的 Microsoft Graph CRUD 操作（创建、读取、更新、删除操作）。

## 设置

1. 为委托登录创建一个 Entra 应用程序注册。
2. 添加 Microsoft Graph 委托权限：
   - `Tasks.ReadWrite`
   - `User.Read`
   - `offline_access`
3. 配置环境变量：

```bash
M365_TENANT_ID=your-tenant-id-or-common
M365_CLIENT_ID=your-public-client-app-id
# optional
M365_TOKEN_CACHE_PATH=/home/user/.cache/openclaw/m365-task-manager-token.json
```

4. 在仓库根目录下安装依赖项：

```bash
npm install
```

脚本在首次运行时使用设备代码进行登录，并缓存令牌以供后续使用。

## 命令

```bash
# profile connection
node skills/m365-task-manager/scripts/m365-todo.mjs info

# list Microsoft To Do lists
node skills/m365-task-manager/scripts/m365-todo.mjs lists

# list tasks
node skills/m365-task-manager/scripts/m365-todo.mjs tasks:list --list-name "Tasks"

# create task
node skills/m365-task-manager/scripts/m365-todo.mjs tasks:create --list-name "Tasks" --title "2026-03-01-submit-weekly-status-report" --due 2026-03-01

# update task
node skills/m365-task-manager/scripts/m365-todo.mjs tasks:update --list-name "Tasks" --task-id <TASK_ID> --status inProgress

# delete task
node skills/m365-task-manager/scripts/m365-todo.mjs tasks:delete --list-name "Tasks" --task-id <TASK_ID>
```

## 操作规范

- 任务标题格式：`YYYY-MM-DD-简短操作-所有者`
- 必填字段：标题、所有者、截止日期、状态
- 状态值：`Open`（开放）、`In Progress`（进行中）、`Blocked`（已阻止）、`Done`（已完成）

## 参考资料

- `references/playbook.md`：操作指南。

## 脚本

- `scripts/m365-todo.mjs`：用于对 Microsoft To-Do 任务执行 Microsoft Graph CRUD 操作的脚本。
- `scripts/format-task-name.sh`：用于生成任务名称的脚本。

## 作者

Abdelkrim BOUJRAF - ALT-F1 SRL - https://www.alt-f1.be

## 许可证

MIT