---
name: task-father
description: 用于生成基于文件的任务状态机（包括注册表、任务文件夹、生命周期状态、队列文件以及定时任务规范/作业）的工具，适用于长时间运行的工作场景。
---
# task-father

在 OpenClaw 工作空间下创建和管理基于文件的、持久化的任务状态机。

**目标文件结构：**

- `TASK_REGISTRY.md`（全局索引）
- `tasks/<task_slug>/`
  - `TASK.md`（任务的前言信息、目的、决策、障碍、变更日志以及所需技能/插件/工具）
  - `TODOS.md`（待办事项列表）
  - `scripts/`（脚本文件夹）
  - `crons/`（定时任务文件夹）
  - `artifacts/`（任务生成的文件）
  - 可选的队列状态文件（`queue.jsonl`、`done.jsonl`、`failed.jsonl`、`lock.json`）

## 先决条件

确保在运行 OpenClaw 的主机上满足以下条件：
- 可以执行 `python3 --version`
- 可以运行 `openclaw status` 和 `openclaw cron --help`

## 配置（可移植配置）

**技能相关的配置文件：**
- 示例配置文件：`config.env.example`
- 实际机器配置文件：`config.env`

**配置参数：**
- `WORKSPACE_DIR`（默认值：`/home/miles/.openclaw/workspace`）
- `TASKS_DIR`（默认值：`tasks`）
- `REGISTRY_FILE`（默认值：`TASK_REGISTRY.md`）
- `DEFAULT_AGENT_ID`（默认值：`main`）
- `DEFAULT_CRON_TZ`（默认值：`America/Indianapolis`）

## 初始化/安装/上手指南

**推荐方式（通过聊天进行配置）：**

1. 在聊天中提供以下信息：
   - 任务的唯一标识符（确保该标识符在文件系统中是唯一的）
   - 任务名称
   - 任务的目的
   - 该任务所需的技能/插件/工具
   - 是否需要使用队列文件
   - 是否需要立即创建定时任务

2. 然后运行以下命令进行初始化：
   ```bash
   python3 scripts/task_father.py init <slug> --title "..." --purpose "..." --skills "a,b" --plugins "x,y" --tools "read,write,exec"
   ```

**可选操作：**
- 启用队列功能：
   ```bash
   python3 scripts/task_father.py enable-queue <slug>
   ```
   - 设置定时任务：
   ```bash
   python3 scripts/task_father.py cron-add <slug> --cron "*/10 * * * *" --message "<worker prompt>" --name "task-<slug>"
   ```

**可选方式（通过终端操作）：**
- 复制配置文件：`cp config.env.example config.env`
- 修改配置文件：`edit config.env`
- 初始化任务：
   ```bash
   python3 scripts/task_father.py init <slug> --title "..."
   ```

## 任务生命周期管理命令

- 设置任务状态（更新 `state.json` 和变更日志）：
   ```bash
   python3 scripts/task_father.py set-state <slug> active
   ```
- 添加变更日志：
   ```bash
   python3 scripts/task_father.py log <slug> "blocked by API quota"
   ```
- 启用队列文件：
   ```bash
   python3 scripts/task_father.py enable-queue <slug>
   ```
- 添加定时任务：
   ```bash
   python3 scripts/task_father.py cron-add <slug> --cron "*/5 * * * *" --message "..." --name "task-<slug>"
   ```
- 删除定时任务：
   ```bash
   python3 scripts/task_father.py cron-rm <slug> --name "task-<slug>"
   ```

## 任务文档规范

每个任务必须包含以下文件：
- `TASK.md`：包含任务的前言信息及以下内容：
  - 任务目的
  - 重要的决策
  - 障碍因素
  - 所需的技能/插件/工具
  - 变更日志（包含时间戳和简要描述）
- `TODOS.md`：包含待办事项列表
- 如果使用队列进行长时间处理，还需包含以下文件：
  - `queue.jsonl`（队列状态文件）
  - `done.jsonl`（已完成任务列表）
  - `failed.jsonl`（失败任务列表）
  - `lock.json`（任务锁定状态文件）
- 脚本文件：存放在 `<task_folder>/scripts/` 目录下
- 定时任务脚本：存放在 `<task_folder>/crons/` 目录下

## 可复现性注意事项：
- 将机器特定的配置信息保存在 `config.env` 文件中，而非 `SKILL.md` 中。
- 尽可能使用只追加内容的日志记录方式。
- 对于耗时较长的任务，应采用分批处理的方式以提高可复现性。