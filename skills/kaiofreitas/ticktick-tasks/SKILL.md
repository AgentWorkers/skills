---
name: ticktick
description: TickTick任务管理器集成：支持查看项目与任务列表、创建新任务、完成任务以及删除任务。适用于用户需要管理待办事项、添加提醒、检查未完成的任务或将任务标记为已完成的情况。使用前需通过`ticktick-setup`进行OAuth设置。
---

# TickTick 集成

通过 TickTick 的开放 API（Open API）来管理任务。

## 设置

仅首次使用时需要执行以下步骤：

1. 访问 https://developer.ticktick.com 并创建一个应用程序。
2. 添加回调 URI：`http://127.0.0.1:8765/callback`
3. 运行设置脚本：

```bash
ticktick-setup <client_id> <client_secret>
```

4. 在浏览器中打开授权页面，完成授权操作，然后粘贴回调 URL。

## 使用方法

```bash
# List projects
ticktick projects

# List all tasks
ticktick tasks

# List tasks from specific project
ticktick tasks <project_id>

# Add task (inbox)
ticktick add "Buy milk"

# Add task to project with due date
ticktick add "Buy milk" --project <id> --due 2026-01-30

# Complete task
ticktick complete <project_id> <task_id>

# Delete task
ticktick delete <project_id> <task_id>
```

## API 参考

基础 URL：`https://api.ticktick.com/open/v1`

| 端点（Endpoint） | 方法（Method） | 描述（Description） |
|------------|-------------|---------------------------|
| /project     | GET          | 列出所有项目            |
| /project/{id}/data | GET          | 获取包含任务的项目信息        |
| /task       | POST          | 创建新任务              |
| /task/{id}     | POST          | 更新任务信息              |
| /project/{pid}/task/{tid}/complete | POST          | 完成任务              |
| /task/{pid}/{tid}   | DELETE          | 删除任务              |

## 任务对象（Task Object）

```json
{
  "title": "Task title",
  "content": "Description", 
  "projectId": "project-id",
  "dueDate": "2026-01-25T12:00:00+0000",
  "priority": 0,
  "tags": ["tag1"]
}
```

优先级（Priority）：
0 = 无；1 = 低；3 = 中；5 = 高