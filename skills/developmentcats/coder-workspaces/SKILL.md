---
name: coder-workspaces
description: 通过命令行界面（CLI）管理 Coder 工作区和 AI 编码代理任务。可以执行工作区的列表查询、创建、启动、停止和删除等操作。还可以通过 SSH 连接到工作区以执行命令。此外，还可以使用 Claude Code、Aider 或其他代理工具来创建和监控 AI 编码任务。
metadata:
  openclaw:
    emoji: "🏗️"
    requires:
      bins: ["coder"]
      env: ["CODER_URL", "CODER_SESSION_TOKEN"]
---

# 开发者工作空间

通过 `coder CLI` 管理开发者工作空间和 AI 编码任务。

> 注意：所有命令都在隔离的、受控的开发者工作空间中执行，而非主机系统。

## 设置

在使用 `coder CLI` 之前，请先配置身份验证：

1. 从 [Coder CLI 文档](https://coder.com/docs/install/cli) 中安装 CLI。
2. 设置环境变量：
   ```bash
   export CODER_URL=https://your-coder-instance.com
   export CODER_SESSION_TOKEN=<your-token>  # Get from /cli-auth
   ```

3. 测试连接：
   ```bash
   coder whoami
   ```

## 工作空间命令

```bash
coder list                              # List workspaces
coder list --all                        # Include stopped
coder list -o json                      # JSON output

coder start <workspace>
coder stop <workspace>
coder restart <workspace> -y
coder delete <workspace> -y

coder ssh <workspace>                   # Interactive shell
coder ssh <workspace> -- <command>      # Run command in workspace

coder logs <workspace>
coder logs <workspace> -f               # Follow logs
```

## AI 编码任务

`Coder Tasks` 会在隔离的工作空间中运行 AI 代理（如 Claude Code、Aider 等）。

### 创建任务

```bash
coder tasks create --template <template> --preset "<preset>" "prompt"
```

- **模板**：必需。使用 `coder templates list` 查看可用模板。
- **预设**：可能也需要指定。可以先不设置。如果创建任务时出现“缺少必需参数”的错误，可以使用 `coder templates presets list <template> -o json` 获取预设配置并使用默认值；如果没有默认值，则需要询问用户选择哪个预设。

### 管理任务

```bash
coder tasks list                        # List all tasks
coder tasks logs <task-name>            # View output
coder tasks connect <task-name>         # Interactive session
coder tasks delete <task-name> -y       # Delete task
```

### 任务状态

- **初始化**：工作空间正在配置中（所需时间因模板而异）。
- **运行中**：脚本正在执行中。
- **活跃**：代理正在处理任务。
- **空闲**：代理正在等待用户输入。

## 故障排除

- **找不到 CLI**：请参考 [Coder CLI 文档](https://coder.com/docs/install/cli)。
- **身份验证失败**：请确认 `CODER_URL` 和 `CODER_SESSION_TOKEN` 已正确设置，然后运行 `coder login`。
- **版本不匹配**：请从您的 Coder 实例中重新安装 CLI。

## 更多信息

- [Coder 文档](https://coder.com/docs)
- [Coder CLI](https://coder.com/docs/install/cli)
- [Coder Tasks](https://coder.com/docs/ai-coder)