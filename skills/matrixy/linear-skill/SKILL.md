---
name: linear
description: 通过 Linear API 管理 Linear 项目、问题（issues）和任务（tasks）。当您需要创建、更新、搜索或管理 Linear 项目、问题、团队（teams）、里程碑（milestones）、评论（comments）或标签（labels）时，请使用该 API。它支持所有的 Linear 操作，包括项目管理、问题跟踪、任务分配、状态转换以及协作工作流程。
---

# 线性项目管理

使用官方的 Linear SDK 来管理线性项目、问题和工作流程。

## 快速入门

所有命令都依赖于 `skills/linear/scripts/linear-cli.js` 文件：

```bash
node skills/linear/scripts/linear-cli.js <command> [args]
```

## 核心命令

### 团队与项目

**列出团队：**
```bash
node skills/linear/scripts/linear-cli.js teams
```

**列出项目：**
```bash
node skills/linear/scripts/linear-cli.js projects
```

**创建项目：**
```bash
node skills/linear/scripts/linear-cli.js createProject "Project Name" "Description" "teamId1,teamId2"
```

### 问题

**列出问题：**
```bash
node skills/linear/scripts/linear-cli.js issues
# With filter:
node skills/linear/scripts/linear-cli.js issues '{"state":{"name":{"eq":"In Progress"}}}'
```

**获取问题详情：**
```bash
node skills/linear/scripts/linear-cli.js issue ENG-123
```

**创建问题：**
```bash
node skills/linear/scripts/linear-cli.js createIssue "Title" "Description" "teamId"
# With options (priority, projectId, assigneeId, etc.):
node skills/linear/scripts/linear-cli.js createIssue "Title" "Description" "teamId" '{"priority":2,"projectId":"project-id"}'
```

**更新问题：**
```bash
node skills/linear/scripts/linear-cli.js updateIssue "issueId" '{"stateId":"state-id","priority":1}'
```

### 评论

**添加评论：**
```bash
node skills/linear/scripts/linear-cli.js createComment "issueId" "Comment text"
```

### 状态与标签

**获取团队状态：**
```bash
node skills/linear/scripts/linear-cli.js states "teamId"
```

**获取团队标签：**
```bash
node skills/linear/scripts/linear-cli.js labels "teamId"
```

### 用户信息

**获取当前用户：**
```bash
node skills/linear/scripts/linear-cli.js user
```

## 参考资料

- **API.md**：优先级级别、过滤示例以及常见的工作流程
- 当需要复杂过滤或工作流程模式的示例时，请参考此文档

## 常见工作流程

### 为特定项目创建任务

1. 获取你的团队 ID：`node skills/linear/scripts/linear-cli.js teams`
2. 获取你的项目 ID：`node skills/linear/scripts/linear-cli.js projects`
3. 使用这些 ID 创建问题：

```bash
node skills/linear/scripts/linear-cli.js createIssue "Implement login" "Add OAuth login flow" "your-team-id" '{"projectId":"your-project-id","priority":2}'
```

### 将问题状态更改

1. 获取所有可用的状态：`node skills/linear/scripts/linear-cli.js states "teamId"`
2. 更新问题状态：`node skills/linear/scripts/linear-cli.js updateIssue "issueId" '{"stateId":"state-uuid"}'`

### 将问题分配给自己

1. 获取你的用户 ID：`node skills/linear/scripts/linear-cli.js user`
2. 将问题分配给自己：`node skills/linear/scripts/linear-cli.js updateIssue "issueId" '{"assigneeId":"your-user-id"}'`

## 输出格式

所有命令返回 JSON 格式的数据。你可以根据需要解析这些数据以供程序使用或直接显示给用户。