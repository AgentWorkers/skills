---
name: Joan Workflow
description: 当用户询问关于“joan”、“pods”、“workspace”、“domain knowledge”、“context sync”、“joan init”、“joan todo”的问题，或者需要了解Joan的知识管理系统的工作原理时，应使用此技能。该技能为pod管理、待办事项管理、计划制定以及工作空间管理提供工作流程指导。
version: 0.1.0
---

# Joan 工作流程

Joan 是一个基于工作空间的知识与任务管理系统，专为人工智能辅助开发而设计。本文档介绍了如何以及何时使用 Joan 的核心功能。

## 核心概念

### 工作空间（Workspaces）

工作空间是 Joan 的最高级组织单元。每个工作空间包含以下内容：
- **Pods**：版本化的领域知识文档
- **Todos**：属于该工作空间的任务
- **Plans**：与 Todos 相关联的实施规范
- **Members**：具有不同角色的团队成员（管理员、普通成员）

### Pods

Pods 是版本化的 Markdown 文档，用于存储领域知识。可以通过 Pods 来：
- 记录项目架构和设计决策
- 存储特定领域的术语和业务规则
- 在团队成员和人工智能助手之间共享知识
- 维护随项目发展而不断更新的文档

**Pod 的生命周期：**
1. 使用 `joan pod create` 在本地创建 Pods
2. 在 `.joan/pods/` 目录下编辑 Markdown 文件
3. 使用 `joan pod push` 将更改推送到服务器
4. 使用 `joan pod pull` 从服务器拉取最新版本

### Todos

Todos 是属于某个工作空间的任务。可以通过 Todos 来：
- 跟踪团队成员的工作进度
- 分配任务并设置优先级
- 将实施计划与任务关联起来

**Todo 的工作流程：**
1. 使用 `joan todo create` 创建任务
2. 使用 `joan todo list` 查看任务列表
3. 随着工作进展更新任务状态
4. 完成任务后将其归档

### Plans

Plans 是与 Todos 相关联的实施规范。可以通过 Plans 来：
- 记录功能的实现方式
- 将复杂任务分解为具体的步骤
- 与团队分享实施方案

## 命令行接口（CLI）命令参考

### 项目初始化

```bash
joan init                    # Interactive workspace selection
joan init -w <workspace-id>  # Non-interactive with specific workspace
joan status                  # Show project and auth status
```

### Pods 管理

```bash
joan pod list               # List tracked pods
joan pod list --all         # List all workspace pods
joan pod add                # Add workspace pods to project
joan pod create             # Create new pod locally
joan pod pull               # Pull pods from server
joan pod push               # Push local pods to server
joan pod open               # Open pod in browser
```

### Todos 管理

```bash
joan todo list              # List todos for tracked pods
joan todo list --mine       # List todos assigned to me
joan todo create            # Create new todo
joan todo update <id>       # Update todo fields
joan todo archive <id>      # Archive completed todo
```

### Plans 管理

```bash
joan plan list <todo-id>    # List plans for a todo
joan plan create <todo-id>  # Create implementation plan
joan plan pull <todo-id>    # Pull plans from server
joan plan push <todo-id>    # Push plans to server
```

### 上下文生成

```bash
joan context claude         # Generate CLAUDE.md with Joan context
```

## 适用场景与使用方法

### 启动新项目

1. 运行 `joan init` 将项目连接到工作空间
2. 选择与项目领域相关的 Pods
3. 运行 `joan context claude` 将上下文信息注入 CLAUDE.md 文件
4. 在编码前阅读生成的 Pod 参考信息

### 在开始编码之前

1. 检查是否存在相关的 Pods：`joan pod list --all`
2. 添加缺失的 Pods：`joan pod add`
3. 拉取最新版本：`joan pod pull`
4. 阅读 Pods 以了解领域背景知识

### 完成工作后

1. 考虑是否需要将新学到的知识整理成 Pods
2. 更新或创建 Todos 以反映工作进展
3. 将本地更改推送到服务器：`joan pod push` 和 `joan todo push`

### 记录新知识

1. 创建一个新的 Pod：`joan pod create`
2. 用 Markdown 编写领域知识
3. 将更改推送到服务器：`joan pod push`
4. 更新 CLAUDE.md 文件中的上下文信息：`joan context claude`

## MCP 集成

Joan 提供了一个名为 `https://joan.land/mcp/joan` 的 MCP 服务器，其中包含以下工具：
- `list_workspaces` - 列出可访问的工作空间
- `list_pods` - 列出工作空间内的 Pods
- `get_pod` - 获取 Pod 的内容

MCP 服务器支持 OAuth 2.1 认证。首先需要通过 CLI 使用 `joan auth login` 进行身份验证。

## 项目配置

Joan 将项目配置存储在 `.joan/config.yaml` 文件中：

```yaml
workspace_id: <uuid>
tracked_pods:
  - name: "Pod Name"
    id: <uuid>
```

Pods 以 Markdown 文件的形式存储在本地目录 `.joan/pods/` 中。

## 最佳实践

### Pods 的编写规范

- 使用清晰、描述性强的标题
- 包括知识适用范围的上下文信息
- 每个 Pod 都应专注于一个具体的领域概念
- 随着知识的更新及时更新 Pods
- 在需要时引用相关的 Pods

### Todos 的管理

- 以适当的粒度创建 Todos（既不要过大也不要过小）
- 将 Todos 与相关的 Pods 关联起来以提供上下文信息
- 及时更新任务状态以保持团队成员的知情
- 将已完成的任务归档以减少信息冗余

### 上下文同步

- 在修改了相关 Pods 后运行 `joan context claude`
- 在开始重要工作之前拉取最新的 Pods
- 及时推送更改以便与团队共享