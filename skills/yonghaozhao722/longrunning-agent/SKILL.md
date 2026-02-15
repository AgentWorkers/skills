# OpenClaw 长期运行代理技能

该技能使 AI 代理能够在多个会话中持续处理长期运行的项目。

## 目的

长期运行代理技能提供了以下结构化的工作流程：
- 跨会话跟踪项目进度
- 管理具有优先级和依赖关系的任务列表
- 对复杂项目进行逐步、原子级的开发
- 确保在恢复工作时能够保持工作的连续性

## 安装

1. 将此技能目录复制到您的 OpenClaw 技能文件夹中。
2. 确保已安装并配置了 Claude Code CLI。
3. 创建一个包含工作流程文件的项目目录。

## 使用方法

### 初始化新项目

```bash
# Create project directory
mkdir my-project && cd my-project

# Initialize workflow files
claude -p "Initialize this project using the longrunning-agent workflow"
```

### 工作流程文件

该技能要求项目目录中包含以下文件：
- `CLAUDE.md` - 项目说明和工作流程指南
- `task.json` - 包含优先级和依赖关系的任务列表
- `progress.txt` - 完成工作的记录
- `init.sh` - 环境设置脚本（可选）

### 任务格式

```json
{
  "tasks": [
    {
      "id": "task-1",
      "description": "Set up project structure",
      "priority": 1,
      "dependencies": [],
      "passes": false
    },
    {
      "id": "task-2",
      "description": "Implement core features",
      "priority": 2,
      "dependencies": ["task-1"],
      "passes": false
    }
  ]
}
```

### 进度记录格式

```
[2024-01-15 10:30:00] Started session
[2024-01-15 10:35:00] Completed task: Set up project structure
[2024-01-15 10:40:00] Milestone: Core features implemented
```

## 工作流程步骤

1. **查看进度** - 查看 `progress.txt` 以了解最近的工作进展。
2. **选择任务** - 找到下一个 `passes: false` 且依赖关系已满足的任务。
3. **初始化** - 如有需要，运行 `init.sh`。
4. **实施** - 逐步完成一个任务。
5. **测试** - 运行代码检查（lint）、构建（build）和测试（tests）。
6. **记录进度** - 更新 `progress.txt`。
7. **标记为已完成** - 在 `task.json` 中将 `passes` 设置为 `true`。
8. **提交** - 执行原子级的 Git 提交。

## 最佳实践

- 每个会话仅处理一个任务。
- 每个任务完成后立即提交代码。
- 保持 `progress.txt` 简洁但信息丰富。
- 使用依赖关系来管理任务的执行顺序。
- 在标记任务为已完成之前进行彻底的测试。

## 与 Web UI 的集成

该技能与代理工作流 Web 应用程序集成：
- 任务会与 Web 数据库同步。
- 进度记录会被捕获。
- 会话输出会被记录。
- Git 提交会被跟踪。

## 模板

工作流程文件的模板位于 `templates/` 目录中：
- `CLAUDE.md.tpl` - 项目模板
- `task.json.tpl` - 任务列表模板