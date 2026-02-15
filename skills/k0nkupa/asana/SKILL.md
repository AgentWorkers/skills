---
name: asana
description: "通过 Asana 的 REST API 将 Asana 与 Clawdbot 集成。当您需要列出/搜索/创建/更新 Asana 任务/项目/工作区，或者为个人本地集成设置 Asana OAuth（授权码授予）时（OOB/手动粘贴代码），可以使用此功能。"
---

# Asana（Clawdbot技能）

该技能专为**个人本地使用**的Asana集成而设计，采用**OAuth**协议，并通过**离线/手动代码粘贴**的方式进行认证。

## 该技能的功能
- 提供一个简单的Node.js命令行工具（CLI），用于：
  - 生成Asana的授权URL
  - 交换授权码以获取访问令牌或刷新令牌
  - 自动刷新访问令牌
  - 执行基本的API调用（例如：`/users/me`、`/workspaces`、`tasks`）

## 设置（OAuth、离线/手动代码）

### 0) 创建Asana应用
在Asana开发者控制台（“我的应用”）中：
- 创建一个新的应用
- 启用所需的权限（通常包括：`tasks:read`、`tasks:write`、`projects:read`）
- 将重定向URI设置为离线认证所需的值（手动代码）：
  - `urn:ietf:wg:oauth:2.0:oob`

### 1) 提供认证凭据（两种方式）
**方式A（推荐用于Clawdbot）**：将凭据保存到本地文件中：
```bash
node scripts/configure.mjs --client-id "..." --client-secret "..."
```
此操作会将凭据写入`~/.clawdbot/asana/credentials.json`文件。

**方式B**：设置环境变量（在shell或会话中）：
- `ASANA_CLIENT_ID`
- `ASANA_CLIENT_SECRET`

### 2) 运行OAuth认证流程
从仓库根目录执行以下操作：
1) 打印授权URL：
```bash
node scripts/oauth_oob.mjs authorize
```
2) 打开打印出的URL，点击“允许”按钮，然后复制生成的代码。
3) 交换授权码并将令牌保存到本地：
```bash
node scripts/oauth_oob.mjs token --code "PASTE_CODE_HERE"
```

令牌将保存在以下路径：
- `~/.clawdbot/asana/token.json`

## 聊天功能（支持显式命令和自然语言输入）
您可以使用以下两种方式之一进行操作：
- **显式命令**：以`/asana ...`开头发起请求
- **自然语言**：例如：“list tasks assigned to me”（列出分配给我的任务）

Clawdbot会将用户输入的指令转换为相应的`asana_api.mjs`命令来执行操作。

示例：
- `/asana tasks-assigned` → `tasks-assigned --assignee me`（列出分配给我的任务）
- “list tasks assigned to me” → `tasks-assigned --assignee me`（列出分配给我的任务）
- “list tasks in <project>” → 先将`<project>`解析为项目ID，然后执行`tasks-in-project --project <gid>`（列出该项目中的任务）
- “list tasks due date from 2026-01-01 to 2026-01-15” → `search-tasks --assignee me --due_on.after 2026-01-01 --due_on_before 2026-01-15`（列出2026年1月1日至2026年1月15日期间到期的任务）

（可选辅助文件）`scripts/asana_chat.mjs`可以将常用短语映射到相应的命令。

## 使用API辅助功能
- 检查当前用户身份：
```bash
node scripts/asana_api.mjs me
```

- 列出所有工作空间：
```bash
node scripts/asana_api.mjs workspaces
```

- 设置默认工作空间（可选）：
```bash
node scripts/asana_api.mjs set-default-workspace --workspace <workspace_gid>
```
设置默认工作空间后，对于支持该参数的命令，您可以省略`--workspace`选项。

- 显式列出某个工作空间中的任务：
```bash
node scripts/asana_api.mjs projects --workspace <workspace_gid>
```

- 使用默认工作空间列出所有项目：
```bash
node scripts/asana_api.mjs projects
```

- 列出某个项目中的任务：
```bash
node scripts/asana_api.mjs tasks-in-project --project <project_gid>
```

- 列出分配给当前用户的任务（Asana要求指定工作空间）：
```bash
node scripts/asana_api.mjs tasks-assigned --workspace <workspace_gid> --assignee me
```

- 或者使用默认工作空间列出任务：
```bash
node scripts/asana_api.mjs tasks-assigned --assignee me
```

- 高级搜索任务：
```bash
node scripts/asana_api.mjs search-tasks --workspace <workspace_gid> --text "release" --assignee me
# also supports convenience: --project <project_gid>
```

- 查看任务详情：
```bash
node scripts/asana_api.mjs task <task_gid>
```

- 将任务标记为已完成：
```bash
node scripts/asana_api.mjs complete-task <task_gid>
```

- 更新任务信息：
```bash
node scripts/asana_api.mjs update-task <task_gid> --name "New title" --due_on 2026-02-01
```

- 在任务上添加评论：
```bash
node scripts/asana_api.mjs comment <task_gid> --text "Update: shipped"
```

- 创建新任务：
```bash
node scripts/asana_api.mjs create-task --workspace <workspace_gid> --name "Test task" --notes "from clawdbot" --projects <project_gid>
```

## 注意事项
- OAuth访问令牌会过期，需要定期刷新以获取新的令牌。
- 如果后续需要支持多用户功能，请将离线认证方式替换为真正的重定向/回调机制。
- 请勿将令牌记录在日志中。