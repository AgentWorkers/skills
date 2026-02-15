---
name: clickup
description: 通过 REST API 与 ClickUp 项目管理平台进行交互。适用于处理任务、项目空间、列表、分配者以及任何 ClickUp 工作流程自动化相关操作。该 API 支持分页功能、子任务处理以及常见的查询模式，可用于任务管理、报告生成、自动化操作或任何与 ClickUp 相关的查询需求。
---

# ClickUp 技能

该技能用于与 ClickUp 的 REST API 进行交互，以实现任务管理、报告生成和工作流程自动化。

## 配置

在使用此技能之前，请确保在 `TOOLS.md` 中配置了以下内容：

- **API 密钥：** `CLICKUP_API_KEY`
- **团队/工作区 ID：** `CLICKUP_TEAM_ID`
- **空间 ID**（可选，用于过滤）
- **列表 ID**（可选，用于创建任务）

## 快速入门

### 使用辅助脚本

查询 ClickUp 数据的最快方法是使用辅助脚本：

```bash
# Set environment variables
export CLICKUP_API_KEY="pk_..."
export CLICKUP_TEAM_ID="90161392624"

# Get all open tasks
./scripts/clickup-query.sh tasks

# Get task counts (parent vs subtasks)
./scripts/clickup-query.sh task-count

# Get assignee breakdown
./scripts/clickup-query.sh assignees

# Get specific task
./scripts/clickup-query.sh task <task-id>
```

### 直接调用 API

对于辅助脚本未覆盖的自定义查询或操作，可以直接调用 API：

```bash
# Get all open tasks (with subtasks and pagination)
curl "https://api.clickup.com/api/v2/team/{team_id}/task?include_closed=false&subtasks=true" \
  -H "Authorization: {api_key}"
```

## 重要规则

### 1. **务必包含子任务**

**绝对不要** 在不设置 `subtasks=true` 的情况下查询任务：

```bash
# ✅ CORRECT
?subtasks=true

# ❌ WRONG
(no subtasks parameter)
```

**原因：** 如果不设置此参数，你可能会遗漏 70% 以上的实际任务。父任务只是任务的容器，真正的工作内容都在子任务中完成。

### 2. 处理分页

ClickUp API 每页最多返回 100 个任务。**必须** 一直循环查询，直到 `last_page: true` 为 true：

```bash
page=0
while true; do
    result=$(curl -s "...&page=$page" -H "Authorization: $CLICKUP_API_KEY")
    
    # Process tasks
    echo "$result" | jq '.tasks[]'
    
    # Check if done
    is_last=$(echo "$result" | jq -r '.last_page')
    [ "$is_last" = "true" ] && break
    
    ((page++))
done
```

**原因：** 如果工作区中有 300 个以上的任务，可能需要查询 3-4 页才能获取所有数据。遗漏页面会导致数据不完整。

### 3. 区分父任务和子任务

```bash
# Parent tasks have parent=null
jq '.tasks[] | select(.parent == null)'

# Subtasks have parent != null
jq '.tasks[] | select(.parent != null)'
```

## 常见操作

### 获取任务数量

```bash
# Using helper script (recommended)
./scripts/clickup-query.sh task-count

# Direct API with jq
curl -s "https://api.clickup.com/api/v2/team/{team_id}/task?subtasks=true" \
  -H "Authorization: {api_key}" | \
jq '{
    total: (.tasks | length),
    parents: ([.tasks[] | select(.parent == null)] | length),
    subtasks: ([.tasks[] | select(.parent != null)] | length)
}'
```

### 获取任务分配者信息

```bash
# Using helper script (recommended)
./scripts/clickup-query.sh assignees

# Direct API
curl -s "https://api.clickup.com/api/v2/team/{team_id}/task?subtasks=true" \
  -H "Authorization: {api_key}" | \
jq -r '.tasks[] | 
    if .assignees and (.assignees | length) > 0 
    then .assignees[0].username 
    else "Unassigned" 
    end' | sort | uniq -c | sort -rn
```

### 创建任务

```bash
curl "https://api.clickup.com/api/v2/list/{list_id}/task" \
  -X POST \
  -H "Authorization: {api_key}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Task Name",
    "description": "Description here",
    "assignees": [user_id],
    "status": "to do",
    "priority": 3
  }'
```

### 更新任务

```bash
curl "https://api.clickup.com/api/v2/task/{task_id}" \
  -X PUT \
  -H "Authorization: {api_key}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "status": "in progress",
    "priority": 2
  }'
```

### 获取特定任务

```bash
# Using helper script
./scripts/clickup-query.sh task {task_id}

# Direct API
curl "https://api.clickup.com/api/v2/task/{task_id}" \
  -H "Authorization: {api_key}"
```

## 高级查询

### 按空间过滤

```bash
curl "https://api.clickup.com/api/v2/team/{team_id}/task?space_ids[]={space_id}&subtasks=true" \
  -H "Authorization: {api_key}"
```

### 按列表过滤

```bash
curl "https://api.clickup.com/api/v2/list/{list_id}/task?subtasks=true" \
  -H "Authorization: {api_key}"
```

### 包含已关闭的任务

```bash
curl "https://api.clickup.com/api/v2/team/{team_id}/task?include_closed=true&subtasks=true" \
  -H "Authorization: {api_key}"
```

## 参考文档

有关详细的 API 文档、查询模式和故障排除方法，请参阅：

**阅读：** `references/api-guide.md`

文档内容包括：
- 完整的 API 端点参考
- 响应结构详情
- 常见问题及解决方法
- 速率限制和最佳实践
- 任务对象结构

## 工作流程示例

### 日常站会报告

```bash
# Get all open tasks grouped by assignee
./scripts/clickup-query.sh assignees

# Get specific team member's tasks (use user ID, not username!)
curl "https://api.clickup.com/api/v2/team/{team_id}/task?subtasks=true&assignees[]={user_id}" \
  -H "Authorization: {api_key}"
```

### 任务审核

```bash
# Count tasks by status
./scripts/clickup-query.sh tasks | \
  jq -r '.tasks[].status.status' | sort | uniq -c | sort -rn

# Find unassigned tasks
./scripts/clickup-query.sh tasks | \
  jq '.tasks[] | select(.assignees | length == 0)'
```

### 任务优先级分析

```bash
# Count by priority
./scripts/clickup-query.sh tasks | \
  jq -r '.tasks[] | .priority.priority // "none"' | sort | uniq -c | sort -rn
```

## 提示

- **优先使用辅助脚本：** 对于常见操作，使用 `scripts/clickup-query.sh` 脚本。
- **需要自定义查询或更新时使用直接 API：** 当需要特定过滤条件或更新时，可以使用 `curl`。
- **务必阅读 api-guide.md：** 包含完整的 API 端点参考和故障排除方法。
- **查看 TOOLS.md：** 了解与工作区相关的 ID 和配置信息。
- **使用小规模查询进行测试：** 在不确定如何操作时，可以先使用 `| head -n 5` 进行测试。
- **按用户 ID 过滤任务：** 使用 `assignees[]={user_id}` 参数进行过滤，而不是使用 `jq` 进行文本匹配。

## 故障排除

- **任务缺失？** → 确保设置了 `subtasks=true`。
- **只返回了 100 个任务？** → 实现分页查询。
- **收到 401 Unauthorized 错误？** → 检查 `CLICKUP_API_KEY` 是否设置正确。
- **遇到速率限制错误？** → 等待 1 分钟（每分钟最多 100 次请求）。
- **分配者数组为空？** → 可能是因为任务尚未分配给任何用户（这不是错误）。
- **按分配者过滤后返回的任务数量少于预期？** → 使用 `assignees[]` 参数中的用户 ID 进行过滤，而不是使用 `jq` 进行文本匹配。