---
name: taskwarrior
description: 由 Taskwarrior 提供的工作区本地任务管理功能。您可以按项目、标签、截止日期和优先级来添加、组织和跟踪任务，所有数据都会存储在当前活动的工作区内。
metadata: |
  {
    "openclaw": {
      "requires": {
        "bins": ["task"]
      },
      "install": [
        {
          "kind": "apt",
          "bins": ["task"],
          "packages": ["taskwarrior"]
        },
        {
          "kind": "brew",
          "bins": ["task"],
          "packages": ["task"]
        }
      ]
    }
  }
---# Taskwarrior（工作区本地任务）——AgentSkill

## 技能名称
taskwarrior

## 功能
该技能使用 Taskwarrior 作为后端来管理任务，数据存储在当前工作区内。它为常见的 Taskwarrior 操作（添加、列出、修改、完成、标记、设置截止日期、调整优先级、添加注释等）提供了一个安全的工作区级封装。

## 运行时要求（ClawHub）
该技能 **需要 Taskwarrior 已经在运行时环境中可用**（例如，包含在基础镜像中）。
- 验证方式：运行 `task --version`
- 如果缺少：报告依赖关系，并指示环境所有者安装系统包 **taskwarrior**（某些发行版可能将其命名为 **task**）。

该技能 **不会执行系统级别的安装操作**（不使用 `apt`、`brew`、`dnf` 等工具）。

## 工作区根路径的确定（可移植性）
该技能在运行时确定工作区的根路径：
1) 如果设置了工作区根路径，优先使用以下路径中的第一个：
   - OPENCLAW_WORKSPACE
   - WORKSPACE
   - PROJECT_DIR
   - REPO_ROOT
2) 否则，使用当前工作目录。

所有 Taskwarrior 数据存储在以下路径：
`<workspace>/.openclaw/taskwarrior/`

## 工作区本地的 Taskwarrior 配置文件
- 配置文件：`<workspace>/.openclaw/taskwarrior/taskrc`
- 数据目录：`<workspace>/.openclaw/taskwarrior/.task/`

每个 Taskwarrior 命令都必须使用以下参数运行：
- `TASKRC=<workspace>/.openclaw/taskwarrior/taskrc`
- （可选）`TASKDATA=<workspace>/.openclaw/taskwarrior/.task`

除非用户明确要求使用全局存储，否则切勿写入全局目录 `~/.task` 或 `~/.taskrc`。

## 核心工作流程
1) **检查依赖关系**
   - 运行：`task --version`
   - 如果缺少依赖关系：停止执行并返回相关提示（详见参考文档 `/references/clawhub_notes.md`）。

2) **初始化工作区存储**
   - 确保以下目录存在：
     - `<workspace>/.openclaw/taskwarrior/`
     - `<workspace>/.openclaw/taskwarrior/.task/`
   - 确保 `<workspace>/.openclaw/taskwarrior/taskrc` 至少包含以下内容：
     - `data.location=<workspace>/.openclaw/taskwarrior/.task`
     - `confirmation=off`
     - `verbose=off`

3) **执行请求的操作**
   - 建议使用稳定且常用的命令（详见参考文档 `/references/taskwarrior_cheatsheet.md`）。

4) **验证结果**
   - 在任何数据变更后，显示特定任务的详细信息（`task <id> info`）或过滤后的任务列表（`task <filter> list`）。

## 支持的操作（常用功能）
- 添加任务：`task add ...`
- 列出任务：`task list`, `task <filter> list`
- 修改任务：`task <id> modify ...`
- 完成任务：`task <id> done`
- 启动/停止任务：`task <id> start|stop`（根据需要）
- 为任务添加标签：`task projects`, `task tags`, `project:<name>`, `+tag`, `-tag`
- 设置截止日期/优先级：`due:<date>`, `priority:H|M|L`
- 添加注释：`task <id> annotate "..."`

## 安全性
请遵循参考文档 `/references/safe_command_policy.md` 中的规定：
- 除非用户明确要求，否则不得删除或清除数据。
- 在进行大规模数据修改前，请先预览相关数据。
- 默认情况下，该技能不会写入全局配置文件。

## 参考文档
- `references/workspace_data_layout.md`
- `references/taskwarrior_cheatsheet.md`
- `references/safe_command_policy.md`
- `references/examples.md`
- `references/clawhub_notes.md`