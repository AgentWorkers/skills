---
name: occ
description: 控制 OpenCode 以执行开发任务。提供会话管理和任务执行功能。
---
# OCC（OpenCode控制器）

通过命令行界面（CLI）控制OpenCode来执行开发任务。

## 使用场景

在以下情况下使用此功能：
- 当您希望将编码任务委托给OpenCode时
- 当您需要从外部系统（如OpenCLAW）控制OpenCode时
- 当您希望自动化开发工作流程时

## 快速入门

### 先决条件

必须已安装OpenCode CLI，并确保它位于系统的PATH环境变量中。

## 工作流程

### 第1步：选择工作目录

⚠️ **重要提示**：请在希望OpenCode运行的目录中运行此脚本。会话将在当前目录中创建。

### 第2步：选择会话模式

- **新建会话**：使用`create`命令（仅创建会话，然后使用`continue`命令来执行任务）
- **继续现有会话**：使用`continue`命令（会话ID由调用者提供）

### 第3步：运行命令

```bash
# Query existing sessions
node skills/occ/scripts/bin/opencode-server.js query

# Create a new session
node skills/occ/scripts/bin/opencode-server.js create "Create a React login page"

# Continue a session
node skills/occ/scripts/bin/opencode-server.js continue <session-id> "Add password reset"
```



## 工作原理

该脚本自动管理OpenCode服务器：
1. **端口检测**：扫描4096-4200端口以查找现有的OpenCode服务器
2. **自动启动**：如果未找到服务器，则自动启动一个新的服务器
3. **会话管理**：通过OpenCode的会话API创建和管理开发会话