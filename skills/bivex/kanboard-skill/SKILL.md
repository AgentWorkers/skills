---
name: kanboard
version: 1.0.0
description: 通过 JSON-RPC API 与 Kanboard 项目管理工具进行交互。适用于处理 Kanboard 的任务、项目、看板、列、泳道、评论、子任务和用户等对象。支持的 API 操作包括：`create task`（创建任务）、`move task`（移动任务）、`show board`（查看看板）、`list projects`（列出项目）、`add comment`（添加评论）等。该接口支持两种认证方式：应用程序 API（使用令牌）和用户 API（需要登录/输入密码）。
metadata:
  clawdbot:
    env:
      - KANBOARD_URL        # e.g. https://kanboard.example.com
      - KANBOARD_API_TOKEN  # from Settings → API, used as password with user "jsonrpc"
      # Optional: use personal credentials instead of app token
      # - KANBOARD_USER     # your Kanboard username
      # - KANBOARD_PASS     # your Kanboard password or personal API token
    requires:
      - curl
      - jq
---
# Kanboard 技能

## 概述

Kanboard 使用基于 HTTP POST 的 **JSON-RPC 2.0** 协议进行通信。所有请求都发送到同一个端点。

### 认证模式

| 认证模式 | 用户名 | 密码       |
|--------|---------|-----------|
| 应用程序 API | `jsonrpc`   | `$KANBOARD_API_TOKEN` |
| 用户 API | `$KANBOARD_USER` | `$KANBOARD_PASS` |

应用程序 API 不会进行权限检查，也不使用会话机制，适用于自动化操作。  
用户 API 会尊重项目权限设置，是执行“我的…”相关操作（如查看个人任务）所必需的。

---

## 核心辅助函数

始终使用以下 shell 函数来调用 API：

```bash
kb() {
  local method="$1"
  local params="${2:-{}}"
  local user="${KANBOARD_USER:-jsonrpc}"
  local pass="${KANBOARD_PASS:-$KANBOARD_API_TOKEN}"

  curl -s -X POST \
    -u "$user:$pass" \
    -H "Content-Type: application/json" \
    -d "{\"jsonrpc\":\"2.0\",\"method\":\"$method\",\"id\":1,\"params\":$params}" \
    "${KANBOARD_URL}/jsonrpc.php" | jq .
}
```

在每个响应中检查是否存在错误：
```bash
# Always verify result is not null/false
result=$(kb getMe | jq '.result')
if [ "$result" = "null" ] || [ "$result" = "false" ]; then
  echo "Error: $(kb getMe | jq -r '.error.message // "unknown error"')"
fi
```

---

## 项目（Projects）

```bash
# List all projects
kb getAllProjects

# Get single project by ID
kb getProjectById '{"project_id": 1}'

# Get project by name
kb getProjectByName '{"name": "My Project"}'

# Create project
kb createProject '{"name": "New Project", "description": "Optional description"}'

# Update project
kb updateProject '{"id": 1, "name": "Renamed", "description": "Updated"}'

# Remove project (irreversible)
kb removeProject '{"project_id": 1}'

# Enable / disable project
kb enableProject  '{"project_id": 1}'
kb disableProject '{"project_id": 1}'

# Get project activity feed
kb getProjectActivity '{"project_id": 1}'
```

---

## 甘特板（Boards）与列（Columns）

```bash
# Get full board (columns + tasks) for a project
kb getBoard '{"project_id": 1}'

# List columns
kb getColumns '{"project_id": 1}'

# Get single column
kb getColumn '{"column_id": 5}'

# Create column
kb addColumn '{"project_id": 1, "title": "In Review", "task_limit": 3}'

# Update column
kb updateColumn '{"column_id": 5, "title": "Review", "task_limit": 5}'

# Remove column
kb removeColumn '{"column_id": 5}'

# Change column position
kb changeColumnPosition '{"project_id": 1, "column_id": 5, "position": 2}'
```

---

## 任务（Tasks）

```bash
# Create task (minimum required: title + project_id)
kb createTask '{
  "title":      "Fix login bug",
  "project_id": 1,
  "column_id":  2,
  "swimlane_id": 1,
  "color_id":   "red",
  "priority":   2,
  "due_date":   "2025-12-31",
  "description": "Detailed description here",
  "owner_id":   3,
  "tags":       ["bug", "urgent"]
}'

# Get task by ID
kb getTask '{"task_id": 42}'

# Get task by reference (external ref)
kb getTaskByReference '{"project_id": 1, "reference": "EXT-123"}'

# List all tasks in a project (status: 1=open, 2=closed)
kb getAllTasks '{"project_id": 1, "status_id": 1}'

# Search tasks with advanced query
kb searchTasks '{"project_id": 1, "query": "assignee:me status:open"}'

# Update task
kb updateTask '{
  "id":         42,
  "title":      "Fix login bug (updated)",
  "column_id":  3,
  "color_id":   "green",
  "priority":   1,
  "due_date":   "2025-11-30"
}'

# Move task to another column/swimlane/position
kb moveTaskToColumn '{
  "project_id":  1,
  "task_id":     42,
  "column_id":   3,
  "position":    1,
  "swimlane_id": 1
}'

# Move task to another project
kb moveTaskToProject '{
  "task_id":        42,
  "project_id":     2,
  "swimlane_id":    1,
  "column_id":      1,
  "category_id":    0
}'

# Duplicate task to another project
kb duplicateTaskToProject '{
  "task_id":    42,
  "project_id": 2
}'

# Close / Open task
kb closeTask '{"task_id": 42}'
kb openTask  '{"task_id": 42}'

# Remove task (irreversible)
kb removeTask '{"task_id": 42}'

# Get task color list
kb getTaskColors
```

### 任务颜色代码：
`yellow`（黄色）、`blue`（蓝色）、`green`（绿色）、`purple`（紫色）、`red`（红色）、`orange`（橙色）、`grey`（灰色）、`brown`（棕色）、`deep_orange`（深橙色）、`dark_grey`（深灰色）、`pink`（粉色）、`teal`（青色）、`cyan`（青绿色）、`lime`（浅绿色）、`light_green`（浅绿色）、`amber`（琥珀色）

---

## 子任务（Subtasks）

```bash
# List subtasks for a task
kb getAllSubtasks '{"task_id": 42}'

# Create subtask
kb createSubtask '{
  "task_id":  42,
  "title":    "Write unit tests",
  "user_id":  3,
  "time_estimated": 4
}'

# Update subtask (status: 0=todo, 1=in-progress, 2=done)
kb updateSubtask '{
  "id":      10,
  "task_id": 42,
  "status":  1,
  "time_spent": 2
}'

# Remove subtask
kb removeSubtask '{"subtask_id": 10}'
```

---

## 评论（Comments）

```bash
# List comments for a task
kb getAllComments '{"task_id": 42}'

# Create comment
kb createComment '{
  "task_id": 42,
  "user_id": 1,
  "content": "This is a **markdown** comment."
}'

# Update comment
kb updateComment '{"id": 7, "content": "Updated comment text."}'

# Remove comment
kb removeComment '{"comment_id": 7}'
```

---

## 浮动泳道（Swimlanes）

```bash
# List swimlanes for a project
kb getSwimlanes '{"project_id": 1}'

# Get active swimlanes only
kb getActiveSwimlanes '{"project_id": 1}'

# Create swimlane
kb addSwimlane '{"project_id": 1, "name": "Team Alpha"}'

# Update swimlane
kb updateSwimlane '{"swimlane_id": 3, "name": "Team Beta"}'

# Remove swimlane
kb removeSwimlane '{"project_id": 1, "swimlane_id": 3}'

# Change swimlane position
kb changeSwimlanePosition '{"project_id": 1, "swimlane_id": 3, "position": 1}'
```

---

## 分类（Categories）

```bash
# List categories for a project
kb getAllCategories '{"project_id": 1}'

# Create category
kb createCategory '{"project_id": 1, "name": "Backend"}'

# Update category
kb updateCategory '{"id": 5, "name": "Backend & API"}'

# Remove category
kb removeCategory '{"category_id": 5}'
```

---

## 用户（Users）

```bash
# List all users (Application API only)
kb getAllUsers

# Get user by ID
kb getUserById '{"user_id": 3}'

# Get user by username
kb getUserByName '{"username": "alice"}'

# Create user
kb createUser '{
  "username": "bob",
  "password": "S3cur3P@ss",
  "name":     "Bob Smith",
  "email":    "bob@example.com",
  "role":     "app-user"
}'
# Roles: app-admin | app-manager | app-user

# Update user
kb updateUser '{"id": 3, "name": "Bob Jones", "email": "bob.jones@example.com"}'

# Disable / Enable user
kb disableUser '{"user_id": 3}'
kb enableUser  '{"user_id": 3}'

# Remove user
kb removeUser '{"user_id": 3}'

# Current user (User API only)
kb getMe
kb getMyProjects
kb getMyDashboard
kb getMyActivityStream
kb getMyCalendar
kb getMyNotifications
```

---

## 项目权限（Project Permissions）

```bash
# List project users
kb getProjectUsers '{"project_id": 1}'

# Add user to project
kb addProjectUser '{
  "project_id": 1,
  "user_id":    3,
  "role":       "project-member"
}'
# Roles: project-manager | project-member | project-viewer

# Change user role in project
kb changeProjectUserRole '{"project_id": 1, "user_id": 3, "role": "project-manager"}'

# Remove user from project
kb removeProjectUser '{"project_id": 1, "user_id": 3}'

# Add/remove group to project
kb addProjectGroup    '{"project_id": 1, "group_id": 2, "role": "project-member"}'
kb removeProjectGroup '{"project_id": 1, "group_id": 2}'
```

---

## 标签（Tags）

```bash
# Get all tags for a project
kb getTagsByProject '{"project_id": 1}'

# Create tag
kb createTag '{"project_id": 1, "tag": "urgent"}'

# Update tag
kb updateTag '{"id": 4, "tag": "critical"}'

# Remove tag
kb removeTag '{"tag_id": 4}'

# Get tags for a task
kb getTaskTags '{"task_id": 42}'

# Assign tags to a task (replaces existing tags)
kb setTaskTags '{"project_id": 1, "task_id": 42, "tags": ["bug", "urgent"]}'
```

---

## 任务链接（Internal Task Links）

```bash
# Get link types
kb getAllLinks

# Get links for a task
kb getAllTaskLinks '{"task_id": 42}'

# Create task link
kb createTaskLink '{
  "task_id":        42,
  "opposite_task_id": 55,
  "link_id":        1
}'
# Common link_id: 1=relates to, 2=blocks, 3=is blocked by, 4=duplicates, 5=is duplicated by

# Remove task link
kb removeTaskLink '{"task_link_id": 8}'
```

---

## 应用程序相关操作（Application Operations）

```bash
# Get app version
kb getVersion

# Get app timezone
kb getTimezone

# Get app default language
kb getDefaultLanguage

# Get current datetime
kb now

# Get available board column types
kb getDefaultTaskColors
```

---

## 常见工作流程（Common Workflows）

### 创建包含完整设置的项目
```bash
# 1. Create project
project_id=$(kb createProject '{"name":"Sprint 1"}' | jq '.result')

# 2. Add columns
kb addColumn "{\"project_id\": $project_id, \"title\": \"Backlog\"}"
kb addColumn "{\"project_id\": $project_id, \"title\": \"In Progress\", \"task_limit\": 3}"
kb addColumn "{\"project_id\": $project_id, \"title\": \"Review\"}"
kb addColumn "{\"project_id\": $project_id, \"title\": \"Done\"}"

# 3. Add swimlane
kb addSwimlane "{\"project_id\": $project_id, \"name\": \"Team Alpha\"}"

# 4. Show board
kb getBoard "{\"project_id\": $project_id}"
```

### 将任务推进到工作流程中
```bash
task_id=42
project_id=1

# Get column IDs first
columns=$(kb getColumns "{\"project_id\": $project_id}" | jq '.result')
in_progress_col=$(echo $columns | jq '[.[] | select(.title=="In Progress")][0].id')

# Move task
kb moveTaskToColumn "{
  \"project_id\": $project_id,
  \"task_id\":    $task_id,
  \"column_id\":  $in_progress_col,
  \"position\":   1
}"
```

### 创建包含子任务的任务
```bash
# Create parent task
task_id=$(kb createTask '{
  "title":      "Implement feature X",
  "project_id": 1,
  "priority":   2
}' | jq '.result')

# Add subtasks
kb createSubtask "{\"task_id\": $task_id, \"title\": \"Write spec\"}"
kb createSubtask "{\"task_id\": $task_id, \"title\": \"Implement\"}"
kb createSubtask "{\"task_id\": $task_id, \"title\": \"Write tests\"}"
kb createSubtask "{\"task_id\": $task_id, \"title\": \"Code review\"}"
```

### 批量关闭已完成的任务
```bash
project_id=1

# Get all open tasks, close those tagged "done"
kb getAllTasks "{\"project_id\": $project_id, \"status_id\": 1}" \
  | jq -r '.result[] | select(.tags[]? == "done") | .id' \
  | while read task_id; do
      kb closeTask "{\"task_id\": $task_id}"
      echo "Closed task $task_id"
    done
```

---

## 错误处理（Error Handling）

```bash
# Robust call wrapper
kb_safe() {
  local result
  result=$(kb "$@")
  local error=$(echo "$result" | jq -r '.error // empty')
  if [ -n "$error" ]; then
    echo "❌ API Error: $(echo "$result" | jq -r '.error.message')" >&2
    return 1
  fi
  echo "$result" | jq '.result'
}

# Usage
kb_safe getAllProjects
kb_safe getTask '{"task_id": 99999}'  # returns error if not found
```

---

## 设置与配置（Setup & Configuration）

请将以下内容添加到您的 OpenClaw 环境中：

```bash
# Required
export KANBOARD_URL="https://kanboard.example.com"
export KANBOARD_API_TOKEN="your_token_from_settings_page"

# Optional (for User API / "My…" procedures)
export KANBOARD_USER="your_username"
export KANBOARD_PASS="your_password_or_personal_token"
```

**获取 API 令牌：**
1. 以管理员身份登录 Kanboard。
2. 转到 **设置 → API**。
3. 复制显示的 API 令牌。

**个人 API 令牌（用户 API）：**
1. 点击个人资料头像 → **我的资料**。
2. 在 API 部分点击 **“生成新的 API 令牌”**。
3. 将生成的令牌作为 `$KANBOARD_PASS`，用户名作为 `$KANBOARD_USER` 使用。

---

## 注意事项：

- 所有日期均使用 `YYYY-MM-DD` 格式或 Unix 时间戳。
- 任务优先级：0=低优先级，1=普通优先级，2=高优先级，3=紧急优先级。
- Kanboard 支持 **批量请求**——在一个 HTTP 请求中发送多个 JSON-RPC 请求（适用于批量操作）。
- 任务的状态代码：1=未完成，2=已完成。
- API 端点始终为 `<KANBOARD_URL>/jsonrpc.php`。