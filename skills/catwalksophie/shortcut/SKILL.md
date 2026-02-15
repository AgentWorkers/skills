---
name: shortcut
version: 1.4.1
description: 在 Shortcut.com 的看板（kanban boards）上管理任务/故事。适用于在 Shortcut 项目管理看板上创建、更新或列出任务/故事。支持创建带有描述和类型（功能/漏洞/杂务）的任务/故事，更新任务/故事的状态，以及列出活跃/已完成的任务/故事。具备完整的任务管理功能（包括待办事项列表）和评论支持。
---

# 快捷Kanban集成

通过API在Shortcut.com的项目看板上管理任务和故事。

## 先决条件

- 通过以下方式配置了SHORTCUT_API_TOKEN：
  - 环境变量：`SHORTCUT_API_TOKEN`
  - 文件：`~/.config/shortcut/api-token`
- 具有适当权限的Shortcut工作空间访问权限

### 设置

1. 从Shortcut.com获取API令牌（设置 → API令牌）
2. 将其存储为：
   - 环境变量：`export SHORTCUT_API_TOKEN="your-token"`
   - 文件：`echo "your-token" > ~/.config/shortcut/api-token && chmod 600 ~/.config/shortcut/api-token`
3. 为你的工作空间初始化工作流状态：
   ```bash
   scripts/shortcut-init-workflow.sh
   ```
   这将创建`~/.config/shortcut/workflow-states`文件，其中包含你工作空间的实际状态ID。
4. （可选）将其添加到`~/.bashrc`中以实现持久化：
   ```bash
   export SHORTCUT_API_TOKEN=$(cat ~/.config/shortcut/api-token 2>/dev/null | tr -d '\n')
   source ~/.config/shortcut/workflow-states
   ```

## 可用的操作

### 列出故事

```bash
scripts/shortcut-list-stories.sh [--active|--completed|--all] [--json]
```

选项：
- `--active` - 仅显示未完成的故事（默认）
- `--completed` - 仅显示已完成的故事
- `--all` - 包括已归档的故事
- `--json` - 输出原始JSON

### 显示故事详情

```bash
scripts/shortcut-show-story.sh <story-id>
```

显示完整的故事信息，包括：
- 故事名称和状态
- 描述（如果有的话）
- 检查表项及其完成状态

### 创建故事

```bash
scripts/shortcut-create-story.sh "Story name" [--description "text"] [--type feature|bug|chore]
```

故事类型：
- `feature`（默认）- 新功能
- `bug` - 错误修复
- `chore` - 维护任务

### 更新故事

```bash
scripts/shortcut-update-story.sh <story-id> [--complete|--todo|--in-progress] [--description "new text"]
```

**工作流状态：** 脚本使用`~/.config/shortcut/workflow-states`中的状态ID（由`shortcut-init-workflow.sh`创建）。如果未配置，则使用默认值：
- 待办事项：`500000006`
- 进行中：`500000007`
- 审查中：`500000008`
- 完成：`500000010`

**注意：** 不同的Shortcut工作空间可能使用不同的状态ID。务必运行`shortcut-init-workflow.sh`来配置你工作空间的实际ID。

### 管理检查表任务

**创建任务：**
```bash
scripts/shortcut-create-task.sh <story-id> "task description"
```

**更新任务完成状态：**
```bash
scripts/shortcut-update-task.sh <story-id> <task-id> [--complete|--incomplete]
```

**编辑任务描述：**
```bash
scripts/shortcut-edit-task.sh <story-id> <task-id> "new description"
```

**删除任务：**
```bash
scripts/shortcut-delete-task.sh <story-id> <task-id>
```

使用`shortcut-show-story.sh`查看任务ID。

### 管理评论

**添加评论：**
```bash
scripts/shortcut-add-comment.sh <story-id> "comment text"
```

**更新评论：**
```bash
scripts/shortcut-update-comment.sh <story-id> <comment-id> "new text"
```

**删除评论：**
```bash
scripts/shortcut-delete-comment.sh <story-id> <comment-id>
```

使用`shortcut-show-story.sh`查看评论ID。

## 工作流程

1. 列出现有故事以了解当前看板状态
2. 创建具有描述性名称和适当类型的新故事
3. 随着工作的进展更新故事状态

## 注意事项

- 脚本使用`SHORTCUT_API_TOKEN`环境变量，或回退到`~/.config/shortcut/api-token`
- 故事默认创建为“未开始”状态（工作流状态ID：500000006）
- 如果你的工作空间使用不同的工作流状态ID，可能需要调整脚本
- 令牌必须具有你想要管理的工作空间的访问权限