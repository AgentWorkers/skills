---
name: project-router
description: "这是一个以终端操作为核心的项目启动工具和工作区上下文管理器。当用户请求使用“/project-style”工作流程时，该工具会执行以下任务：检测当前项目、读取项目的相关信息/简介、运行标准化的操作（构建、测试、代码检查、部署），通过“plan/apply”命令初始化项目的`.project`包，管理项目生成的各种文件/资源，并通过MCP服务器的`mcp-project-router`以及CLI（命令行界面）来执行这些操作。"
---

# project-router

该技能是Safa的**标准化项目管理及上下文切换控制平台**。

**核心理念：**
- **标准化的项目管理（Canonical PM）是本地的，并且可以通过SQLite进行查询**：包括项目、任务和上下文包的信息。
- **Trello作为跟踪后端和用户界面**：Trello中的卡片对应于标准化任务；列表反映任务的状态；标签表示任务的优先级。
- **最核心的功能是上下文切换**：能够快速且可靠地为某个项目或任务加载相应的文档、代码或索引。

**提供的功能包括：**
- 命令行界面（CLI）：`project <verb> ...`
- MCP服务器：`mcp-project-router`（其工具与CLI功能相同）
- 每个项目的数据包存储在`.project/`目录下（包含项目简介、目标信息和工件索引）
- 标准化的任务存储系统（基于SQLite）以及与Trello的同步机制

## 项目数据包结构（版本1）

`.project/`目录是项目数据的核心存储位置。标准化的项目管理数据库会引用这些数据包。

在项目根目录下：
- `.project/project.json` — 项目结构化配置文件
- `.project/PROJECT.md` — 项目的最新简介
- `.project/targets.json` — 任务定义
- `.project/index/artifacts.json` — 工件索引
- `.project/history/plans/*.json` — 项目计划信息
- `.project/history/applies/*.json` — 任务执行记录

## 命令行界面快速入门

**基本命令：**
在仓库或工作区的任意位置，可以执行以下命令：
- `project detect` — 检测项目状态
- `project context` — 查看项目上下文信息
- `project target list` — 列出所有任务
- `project target run <name>` — 运行指定任务

**初始化项目数据包（仅用于测试）：**
- `project init` — 打印项目计划
- `project apply <planId>` — 应用项目计划

**工件管理：**
- `project artifact add <path|url> [--tags a,b,c]` — 添加工件（并应用到项目中）

**标准化项目管理及上下文切换（新功能）：**
> 注意：这些命令是用户界面的主要接口。实际实现应确保操作的可重复性和安全性。

**项目注册：**
- `project pm project add <slug> --name "..." --root <path>` — 注册新项目
- `project pm project list` — 查看所有项目列表

**任务管理：**
- `project pm task add <slug> "<title>" --priority P0|P1|P2|P3 --status inbox|next|doing|blocked|waiting|done>` — 添加新任务
- `project pm task list [--project <slug>]` — 查看指定项目的任务列表
- `project pm task set-status <taskId> <status>` — 修改任务状态

**上下文切换：**
- `project pm switch <slug>` — 显示固定显示的文档、重要任务及当前活跃任务
- `project pm focus <taskId>` — 加载与任务关联的文件/工件，并更新任务活动日志

**Trello同步：**
- `project pm trello sync [--project <slug>]` — 确保Trello上存在名为“Safa — PM”的看板
- 确保看板中的列表（Inbox/Next/Doing/Blocked/Waiting/Done）与项目状态一致
- 为标准化任务创建或更新卡片
- 根据优先级（P0..P3）为卡片添加标签

## MCP快速入门（通过mcporter工具）：**
- `mcporter list mcp-project-router --schema --timeout 120000 --json` — 列出所有可用的项目和服务

**示例：**
- 检测项目：`mcporter call --server mcp-project-router --tool project_detect --args '{}'`
- 查看项目上下文：`mcporter call --server mcp-project-router --tool project_context_read --args '{}'`
- 运行任务：`mcporter call --server mcp-project-router --tool project_target_run --args '{"target":"test"}`

## Trello后端规范：
- 看板名称：`Safa — PM`（可自定义）
- 列表与项目状态对应关系：
  - `Inbox`（收件箱）、`Next`（待处理）、`Doing`（进行中）、`Blocked`（阻塞）、`Waiting`（等待）、`Done`（已完成）
- 卡片标题格式：`[<project_slug>] <task_title>`
- 卡片描述以特定格式开头，以确保操作的不可重复性（使用````yaml
  --- pm ---
  task_id: <stable-id>
  project: <slug>
  status: <status>
  priority: P0|P1|P2|P3
  ---
  ````标记）

**标准化项目管理数据库（SQLite）：**
**建议的数据库存储位置（在工作区内）：**
- `/home/safa/clawd/data/pm/pm.sqlite`

**最低要求的数据库表结构（版本0）：**
- `projects`：`slug PRIMARY KEY, name, root_path, created_at, updated_at`
- `tasks`：`task_id PRIMARY KEY, project_slug, title, status, priority, created_at, updated_at`
- `task_refs`：`task_id, kind, ref`（文件路径/URL/工件链接）
- `external_refs`：`task_id, system, external_id, meta_json`（例如Trello卡片ID/列表ID）

**安全性要求：**
- 项目数据的写入操作应保持不可重复性（例如，执行相同的操作不会产生不同结果），并且应可审计（记录时间戳和操作日志）。
- Trello同步操作应能够安全地重复执行（通过`task_id`进行唯一性检查，避免重复创建卡片）。
- `project_target_run`命令会执行`.project/targets.json`中定义的指令。