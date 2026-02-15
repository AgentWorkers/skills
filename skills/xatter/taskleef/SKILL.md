---
name: taskleef
description: **使用场景：**  
适用于通过 Taskleef.com 管理待办事项（todos）、任务（tasks）、项目（projects）或看板（kanban boards）的场景。支持添加、查看、完成待办事项，以及将待办事项与项目关联并进行组织。同时，也支持使用看板工作流程来跟踪任务、管理待办列表或按项目划分工作内容。
metadata: {"clawdbot":{"emoji":"✅","requires":{"bins":["todo","curl","jq"],"env":["TASKLEEF_API_KEY"]},"primaryEnv":"TASKLEEF_API_KEY","homepage":"https://taskleef.com","install":[{"id":"todo-cli","kind":"download","url":"https://raw.githubusercontent.com/Xatter/taskleef/main/taskleef-cli/todo","bins":["todo"],"label":"Install Taskleef CLI (todo)"},{"id":"jq-brew","kind":"brew","formula":"jq","bins":["jq"],"label":"Install jq via Homebrew","os":["darwin"]},{"id":"jq-linux-amd64","kind":"download","url":"https://github.com/jqlang/jq/releases/download/jq-1.7.1/jq-linux-amd64","bins":["jq"],"label":"Install jq (Linux x86_64)","os":["linux"]},{"id":"jq-linux-arm64","kind":"download","url":"https://github.com/jqlang/jq/releases/download/jq-1.7.1/jq-linux-arm64","bins":["jq"],"label":"Install jq (Linux ARM64)","os":["linux"]}]}}
---

# Taskleef

使用 Taskleef CLI 管理待办事项、项目和看板。Taskleef.com 是一个功能灵活的待办事项管理工具，支持简单的任务列表、项目组织和看板工作流程。

## 先决条件

`todo` CLI 需要以下工具：
- `curl` - 用于发送 API 请求
- `jq` - 用于解析 JSON 响应
- `TASKLEEF_API_KEY` 环境变量

## 认证

CLI 使用 `TASKLEEF_API_KEY` 环境变量进行认证。用户可以从 https://taskleef.com 获取自己的 API 密钥。

可选地，用户可以使用 `--auth-file` 标志来指定认证文件：
```bash
todo --auth-file ~/.taskleef.auth list
todo -a ~/.taskleef.auth list
```

## 核心命令

### 待办事项管理

**列出所有待办事项：**
```bash
todo list           # List pending todos
todo ls             # Alias for list
todo list -a        # List all todos including completed
```

**添加待办事项：**
```bash
todo add "Buy groceries"
todo "Buy groceries"    # Quick add without 'add' keyword
```

**查看待办事项详情：**
```bash
todo show <title-or-id>
```

**完成待办事项：**
```bash
todo complete <title-or-id>
todo done <title-or-id>
```

**删除待办事项：**
```bash
todo delete <title-or-id>
todo rm <title-or-id>
```

**查看收件箱：**
```bash
todo inbox    # List todos not assigned to any project
```

### 子任务

**添加子任务：**
```bash
todo subtask <parent-title-or-id> "Subtask title"
```

### 项目

**列出项目：**
```bash
todo project list
```

**创建项目：**
```bash
todo project add "Project Name"
```

**查看项目详情：**
```bash
todo project show <project-name-or-id>
```

**删除项目：**
```bash
todo project delete <project-name-or-id>
```

**将待办事项分配给项目：**
```bash
todo project add-todo <project-name-or-id> <todo-title-or-id>
```

**从项目中移除待办事项：**
```bash
todo project remove-todo <project-name-or-id> <todo-title-or-id>
```

### 看板

**查看看板：**
```bash
todo board                           # Show default board (ASCII view)
todo board show <board-name-or-id>   # Show specific board
```

**列出所有看板：**
```bash
todo board list
```

**列出看板中的卡片：**
```bash
todo board column <column-name-or-id>
```

**移动卡片：**
```bash
todo board move <card-title-or-id> <column-name-or-id>
```

**标记卡片为已完成：**
```bash
todo board done <card-title-or-id>
```

**分配卡片负责人：**
```bash
todo board assign <card-title-or-id>
```

**清除某一列的卡片：**
```bash
todo board clear <column-name-or-id>
```

## 标识符匹配规则

命令支持以下匹配方式：
- **ID 前缀**：UUID 的前几个字符（例如 `abc12`）
- **标题匹配**：不区分大小写的标题匹配（例如，`groceries` 匹配 “Buy groceries”）

## 优先级指示

在列出待办事项时，优先级会以以下方式显示：
- ○ 无优先级
- ● （绿色）低优先级
- ● （黄色）中等优先级
- ● （红色）高优先级

## 使用技巧

1. **查找项目/卡片**：可以通过部分标题或 ID 前缀来查找待办事项、项目、看板和卡片。
2. **快速操作**：使用 `todo "task"` 可以快速添加新任务。
3. **项目组织**：将相关待办事项归类到项目中，以便更好地管理。
4. **看板管理**：利用看板进行可视化的任务流程管理。
5. **子任务**：将复杂任务分解为子任务，以便更清晰地跟踪进度。

## 示例

```bash
# Add and complete a todo
todo add "Review pull request"
todo done "pull request"

# Create a project and add todos
todo project add "Website Redesign"
todo project add-todo "Website" "Fix login"

# View kanban board and move cards
todo board
todo board move "Feature A" "Done"
```

## 错误处理

如果未设置 `TASKLEEF_API_KEY` 或 API 密钥无效，命令将无法执行。请确保在运行命令前配置好 API 密钥。

## 额外资源

- 官网：https://taskleef.com
- 生成 API 密钥：https://taskleef.com（用户控制台）