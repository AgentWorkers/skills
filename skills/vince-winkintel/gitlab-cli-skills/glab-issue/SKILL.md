---
name: glab-issue
description: 创建、查看、更新和管理 GitLab 问题。适用于问题跟踪、错误报告、功能请求或任务管理场景。相关操作包括：创建问题、使用过滤器筛选问题列表、查看问题详情、添加评论/备注、更新问题的标签/分配者/里程碑状态、关闭或重新打开问题，以及进行问题列表的管理。相关触发器包括：问题触发器（Issue Trigger）、错误触发器（Bug Trigger）、任务触发器（Task Trigger）、工单触发器（Ticket Trigger）和功能请求触发器（Feature Request Trigger）。
---

# GitLab 问题管理

在 GitLab 中，您可以创建、查看、更新和管理问题。

## 快速入门

```bash
# Create an issue
glab issue create --title "Fix login bug" --label bug

# List open issues
glab issue list --state opened

# View issue details
glab issue view 123

# Add comment
glab issue note 123 -m "Working on this now"

# Close issue
glab issue close 123
```

## 常见工作流程

### 错误报告流程

1. **创建错误问题：**
   ```bash
   glab issue create \
     --title "Login fails with 500 error" \
     --label bug \
     --label priority::high \
     --assignee @dev-lead
   ```

2. **添加问题复现步骤：**
   ```bash
   glab issue note 456 -m "Steps to reproduce:
   1. Navigate to /login
   2. Enter valid credentials
   3. Click submit
   Expected: Dashboard loads
   Actual: 500 error"
   ```

### 问题分类

1. **列出未分类的问题：**
   ```bash
   glab issue list --label needs-triage --state opened
   ```

2. **更新标签和分配负责人：**
   ```bash
   glab issue update 789 \
     --label backend,priority::medium \
     --assignee @backend-team \
     --milestone "Sprint 23"
   ```

3. **移除分类标签：**
   ```bash
   glab issue update 789 --unlabel needs-triage
   ```

**批量添加标签：**

若需同时为多个问题添加标签，可执行以下操作：
```bash
scripts/batch-label-issues.sh "priority::high" 100 101 102
scripts/batch-label-issues.sh bug 200 201 202 203
```

### 断裂计划（Sprint）管理

**查看当前冲刺中的问题：**
```bash
glab issue list --milestone "Sprint 23" --assignee @me
```

**将问题添加到冲刺中：**
```bash
glab issue update 456 --milestone "Sprint 23"
```

**使用看板视图：**
```bash
glab issue board view
```

### 将问题与工作关联

**为问题创建合并请求（Merge Request, MR）：**
```bash
glab mr for 456  # Creates MR that closes issue #456
```

**自动化工作流程（创建分支 + 起草合并请求）：**
该流程会自动执行以下操作：
- 根据问题标题创建分支
- 提交一个空提交
- 推送更改
- 生成合并请求的草稿

**通过提交或合并请求关闭问题：**
```bash
git commit -m "Fix login bug

Closes #456"
```

## 相关技能

**从问题创建合并请求：**
- 查看 `glab-mr` 以了解合并请求的相关操作
- 使用 `glab mr for <issue-id>` 来创建用于关闭问题的合并请求
- 脚本 `scripts/create-mr-from-issue.sh` 可自动完成分支创建和合并请求的起草

**标签管理：**
- 查看 `glab-label` 以了解标签的创建和管理方法
- 脚本 `scripts/batch-label-issues.sh` 可用于批量添加标签

**项目规划：**
- 查看 `glab-milestone` 以进行发布计划管理
- 查看 `glab-iteration` 以管理冲刺和迭代

## 命令参考

有关所有命令的详细信息，请参阅 [references/commands.md](references/commands.md)。

**可用命令：**
- `create` - 创建新问题
- `list` - 使用过滤器列出问题
- `view` - 显示问题详情
- `note` - 为问题添加注释
- `update` - 更新问题标题、标签和负责人
- `close` - 关闭问题
- `reopen` - 重新打开已关闭的问题
- `delete` - 删除问题
- `subscribe` / `unsubscribe` - 管理通知接收
- `board` - 管理问题看板