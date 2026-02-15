---
name: yatta
description: 这是一款用于任务管理和能力规划的个人生产力工具。它支持创建和整理具有丰富属性（如优先级、所需努力程度、复杂性、标签）的任务，能够记录任务完成的时间和连续完成任务的状态（即“连续完成的任务 streaks”），帮助用户跨项目和不同工作场景管理自己的能力分配。用户可以查看基于艾森豪威尔矩阵的任务优先级排序结果，同步日历订阅信息，处理任务委派和后续跟进工作，并获得人工智能提供的分析建议。该工具还支持批量操作、多项目工作流程以及实时能力规划功能，从而有效防止过度承诺（即用户承担超出自身能力的任务）。
homepage: https://github.com/chrisagiddings/openclaw-yatta-skill
metadata: {"openclaw":{"emoji":"✅","requires":{"env":["YATTA_API_KEY","YATTA_API_URL"],"bins":["curl","jq"]},"primaryEnv":"YATTA_API_KEY","disable-model-invocation":true,"capabilities":["task-management","project-management","context-management","comment-management","calendar-management","destructive-operations"],"credentials":{"type":"env","variables":[{"name":"YATTA_API_KEY","description":"Yatta! API key (yatta_...)","required":true},{"name":"YATTA_API_URL","description":"Yatta! API base URL","required":false,"default":"https://zunahvofybvxpptjkwxk.supabase.co/functions/v1"}]}}}
---

# Yatta! 技能

通过 API 与 Yatta! 任务管理系统进行交互。需要使用您的 Yatta! 账户生成的 API 密钥。

## ⚠️ 安全警告

**此技能可以对您的 Yatta! 账户执行破坏性操作：**

- **任务管理：** 创建、更新、归档和批量修改任务
- **项目管理：** 创建、更新和归档项目
- **上下文管理：** 创建上下文并将其分配给任务
- **评论管理：** 添加、更新和删除任务评论
- **日历管理：** 创建、同步和修改日历订阅
- **跟进管理：** 更新跟进计划并标记任务为已完成
- **容量管理：** 触发容量计算

**操作类型：**

**只读操作**（✅ 安全）：
- 列出任务、项目、上下文和评论
- 获取分析数据、洞察和任务完成情况
- 查看容量和日历数据
- 查看艾森豪威尔矩阵视图
- 所有 GET 请求

**破坏性操作**（⚠️ 修改或删除数据）：
- 创建/更新/归档任务（POST、PUT、DELETE）
- 批量更新任务
- 创建/更新项目
- 创建/分配上下文
- 添加/更新/删除评论
- 添加/同步日历订阅
- 更新跟进计划
- 所有 POST、PUT、DELETE 请求

**最佳实践：**
1. **运行前查看命令** - 确认 API 调用将执行的操作
2. **删除操作不可撤销** - 归档的任务可以恢复，但某些操作是不可逆的
3. **先在非关键数据上测试** - 创建测试任务/项目以验证功能
4. **批量操作会影响多个项目** - 对批量更新要格外小心
5. **实时同步** - 更改会立即显示在 Yatta! 用户界面中

有关详细的 API 操作文档，请参阅 [API-REFERENCE.md](API-REFERENCE.md)。

## 设置

### ⚠️ API 密钥安全

**您的 Yatta! API 密钥可提供对账户的完全访问权限：**
- 可以创建、读取、更新和删除所有任务、项目和上下文
- 可以修改日历订阅和跟进计划
- 可以归档数据并触发容量计算
- **没有只读权限** - 密钥具有全部权限

**安全最佳实践：**
- 将密钥存储在安全的密码管理器中（推荐使用 1Password CLI）
- 使用环境变量，切勿在脚本中硬编码密钥
- 定期轮换密钥（建议每 90 天更换一次）
- 为不同的集成创建单独的密钥
- 立即撤销未使用的密钥
- **切勿将密钥提交到版本控制系统中**

### 1. 获取您的 API 密钥

1. 登录 Yatta! 应用程序
2. 转到设置 → API 密钥
3. 创建新密钥（例如：“OpenClaw Integration”）
4. 复制 `yatta_...` 密钥
5. 安全地存储该密钥

### 2. 配置技能

**选项 A：环境变量（推荐）**
```bash
# Add to your shell profile (~/.zshrc, ~/.bashrc)
export YATTA_API_KEY="yatta_your_key_here"
export YATTA_API_URL="https://zunahvofybvxpptjkwxk.supabase.co/functions/v1"  # Default
```

**选项 B：1Password CLI（最安全）**
```bash
# Store key in 1Password
op item create --category=API_CREDENTIAL \
  --title="Yatta API Key" \
  api_key[password]="yatta_your_key_here"

# Use in commands
export YATTA_API_KEY=$(op read "op://Private/Yatta API Key/api_key")
```

**注意：** 目前直接使用 Supabase 的 API 地址。品牌化的 URL（yattadone.com/api）将在未来版本中提供。

### 3. 测试连接
   ```bash
   curl -s "$YATTA_API_URL/tasks" \
     -H "Authorization: Bearer $YATTA_API_KEY" \
     | jq '.[:3]'  # Show first 3 tasks
   ```

## 任务 API

### 列出任务

**所有任务：**
```bash
curl -s "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

**按状态筛选：**
```bash
# TODO tasks only
curl -s "$YATTA_API_URL/tasks?status=todo" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'

# Doing (active) tasks
curl -s "$YATTA_API_URL/tasks?status=doing" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'

# Completed tasks
curl -s "$YATTA_API_URL/tasks?status=done" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

**按优先级筛选：**
```bash
# High priority tasks
curl -s "$YATTA_API_URL/tasks?priority=high" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.[] | {title, due_date, priority}'
```

**按项目筛选：**
```bash
# Get project ID first
PROJECT_ID=$(curl -s "$YATTA_API_URL/projects" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq -r '.[] | select(.name=="Website Redesign") | .id')

# Get tasks for that project
curl -s "$YATTA_API_URL/tasks?project_id=$PROJECT_ID" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

**按矩阵状态筛选：**
```bash
# Delegated tasks
curl -s "$YATTA_API_URL/tasks?matrix_state=delegated" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.[] | {title, delegated_to, follow_up_date}'

# Waiting tasks
curl -s "$YATTA_API_URL/tasks?matrix_state=waiting" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

**日期范围查询：**
```bash
# Tasks due this week
WEEK_END=$(date -v+7d "+%Y-%m-%d")
curl -s "$YATTA_API_URL/tasks?due_date_lte=$WEEK_END" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.[] | {title, due_date}'

# Overdue tasks
TODAY=$(date "+%Y-%m-%d")
curl -s "$YATTA_API_URL/tasks?due_date_lte=$TODAY&status=todo" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.[] | {title, due_date}'
```

**分页：**
```bash
# First 50 tasks
curl -s "$YATTA_API_URL/tasks?limit=50&offset=0" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'

# Next 50 tasks
curl -s "$YATTA_API_URL/tasks?limit=50&offset=50" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

**归档任务：**
```bash
curl -s "$YATTA_API_URL/tasks?archived=true" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### 创建任务

**简单任务：**
```bash
curl -s "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Finish report",
    "priority": "high"
  }' \
  | jq '.'
```

**包含详细信息的任务：**
```bash
curl -s "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Review Q1 numbers",
    "description": "Go through revenue, costs, and projections",
    "priority": "high",
    "due_date": "2026-02-15",
    "effort_points": 5,
    "project_id": "uuid-of-project",
    "matrix_state": "active"
  }' \
  | jq '.'
```

**带有跟进任务的委派任务：**
```bash
curl -s "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Website redesign",
    "delegated_to": "Dev Team",
    "matrix_state": "delegated",
    "follow_up_schedule": {
      "type": "weekly",
      "day_of_week": "monday",
      "next_follow_up": "2026-02-17"
    }
  }' \
  | jq '.'
```

**重复任务：**
```bash
curl -s "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team standup",
    "recurrence_rule": {
      "frequency": "daily",
      "interval": 1,
      "days_of_week": ["monday", "tuesday", "wednesday", "thursday", "friday"]
    },
    "effort_points": 1
  }' \
  | jq '.'
```

### 更新任务

**更新单个任务：**
```bash
TASK_ID="uuid-of-task"
curl -s -X PUT "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "'$TASK_ID'",
    "status": "done",
    "completed_at": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"
  }' \
  | jq '.'
```

**批量更新任务：**
```bash
curl -s -X PUT "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "ids": ["uuid-1", "uuid-2", "uuid-3"],
    "priority": "high",
    "project_id": "project-uuid"
  }' \
  | jq '.'
```

### 归档任务**

```bash
TASK_ID="uuid-of-task"
curl -s -X DELETE "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "'$TASK_ID'"
  }' \
  | jq '.'
```

## 项目 API

### 列出项目

```bash
# All projects
curl -s "$YATTA_API_URL/projects" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'

# With task counts
curl -s "$YATTA_API_URL/projects?with_counts=true" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.[] | {name, task_count, open_count}'
```

### 创建项目

```bash
curl -s "$YATTA_API_URL/projects" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Website Redesign",
    "description": "Complete overhaul of company site",
    "color": "#3b82f6",
    "icon": "🌐"
  }' \
  | jq '.'
```

### 更新项目

```bash
PROJECT_ID="uuid-of-project"
curl -s -X PUT "$YATTA_API_URL/projects" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "'$PROJECT_ID'",
    "name": "Website Redesign v2",
    "archived": false
  }' \
  | jq '.'
```

### 获取项目任务

```bash
PROJECT_ID="uuid-of-project"
curl -s "$YATTA_API_URL/projects/$PROJECT_ID/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

## 上下文 API

### 列出上下文

```bash
# All contexts
curl -s "$YATTA_API_URL/contexts" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'

# With task counts
curl -s "$YATTA_API_URL/contexts?with_counts=true" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.[] | {name, task_count}'
```

### 创建上下文

```bash
curl -s "$YATTA_API_URL/contexts" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "@deep-focus",
    "color": "#8b5cf6",
    "icon": "🧠"
  }' \
  | jq '.'
```

### 将上下文分配给任务

```bash
TASK_ID="uuid-of-task"
CONTEXT_ID="uuid-of-context"

curl -s -X POST "$YATTA_API_URL/contexts/assign" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "'$TASK_ID'",
    "context_ids": ["'$CONTEXT_ID'"]
  }' \
  | jq '.'
```

### 获取任务上下文

```bash
TASK_ID="uuid-of-task"
curl -s "$YATTA_API_URL/tasks/$TASK_ID/contexts" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### 获取包含上下文的任务

```bash
CONTEXT_ID="uuid-of-context"
curl -s "$YATTA_API_URL/contexts/$CONTEXT_ID/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

## 评论 API

### 列出任务评论

```bash
TASK_ID="uuid-of-task"
curl -s "$YATTA_API_URL/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### 添加评论

```bash
TASK_ID="uuid-of-task"
curl -s -X POST "$YATTA_API_URL/tasks/$TASK_ID/comments" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Waiting on client feedback before proceeding"
  }' \
  | jq '.'
```

### 更新评论

```bash
COMMENT_ID="uuid-of-comment"
curl -s -X PUT "$YATTA_API_URL/task-comments" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "'$COMMENT_ID'",
    "content": "Client responded, moving forward"
  }' \
  | jq '.'
```

### 删除评论

```bash
COMMENT_ID="uuid-of-comment"
curl -s -X DELETE "$YATTA_API_URL/task-comments" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "'$COMMENT_ID'"
  }' \
  | jq '.'
```

## 进展管理 API

### 获取今天的跟进任务

```bash
curl -s "$YATTA_API_URL/follow-ups" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.[] | {title, delegated_to, follow_up_date}'
```

### 获取指定日期的跟进任务

```bash
DATE="2026-02-15"
curl -s "$YATTA_API_URL/follow-ups?date=$DATE" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### 标记跟进任务为已完成

```bash
TASK_ID="uuid-of-task"
curl -s -X POST "$YATTA_API_URL/tasks/$TASK_ID/follow-up" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}' \
  | jq '.'
```

### 更新跟进计划

```bash
TASK_ID="uuid-of-task"
curl -s -X PUT "$YATTA_API_URL/tasks/$TASK_ID/follow-up-schedule" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "every_n_days",
    "interval": 3,
    "next_follow_up": "2026-02-12"
  }' \
  | jq '.'
```

## 日历 API

### 列出日历订阅

```bash
curl -s "$YATTA_API_URL/calendar/subscriptions" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### 添加日历订阅

```bash
curl -s -X POST "$YATTA_API_URL/calendar/subscriptions" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Work Calendar",
    "ical_url": "https://calendar.google.com/calendar/ical/...",
    "default_context_id": "context-uuid"
  }' \
  | jq '.'
```

### 触发日历同步

```bash
SUBSCRIPTION_ID="uuid-of-subscription"
curl -s -X POST "$YATTA_API_URL/calendar/subscriptions/$SUBSCRIPTION_ID/sync" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### 列出日历事件

```bash
# Events for date range
START="2026-02-10"
END="2026-02-17"
curl -s "$YATTA_API_URL/calendar/events?start=$START&end=$END" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

## 容量 API

### 获取今天的容量信息

```bash
curl -s "$YATTA_API_URL/capacity/today" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '{date, utilization_percent, status, used_minutes, total_minutes}'
```

### 获取指定日期范围的容量信息

```bash
START="2026-02-10"
END="2026-02-17"
curl -s "$YATTA_API_URL/capacity?start=$START&end=$END" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.[] | {date, status, utilization_percent}'
```

### 触发容量计算

```bash
curl -s -X POST "$YATTA_API_URL/capacity/compute" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

## 分析 API

### 获取汇总洞察

```bash
curl -s "$YATTA_API_URL/analytics/summary" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### 获取任务分布情况

```bash
curl -s "$YATTA_API_URL/analytics/velocity" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### 获取任务完成情况

```bash
curl -s "$YATTA_API_URL/analytics/distribution" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '{by_status, by_priority, by_matrix_state}'
```

### 获取任务完成趋势

```bash
curl -s "$YATTA_API_URL/analytics/streaks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### 获取 AI 洞察

```bash
curl -s "$YATTA_API_URL/analytics/insights" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

## 艾森豪威尔矩阵 API

### 获取艾森豪威尔矩阵视图

```bash
curl -s "$YATTA_API_URL/tasks/matrix" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '{do_first, schedule, delegate, eliminate}'
```

## 常见用法

### 日常工作流程自动化

**晨间简报：**
```bash
#!/bin/bash
echo "=== Today's Tasks ==="
curl -s "$YATTA_API_URL/tasks?status=todo&due_date_lte=$(date +%Y-%m-%d)" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq -r '.[] | "- [\(.priority)] \(.title)"'

echo ""
echo "=== Follow-Ups Due ==="
curl -s "$YATTA_API_URL/follow-ups" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq -r '.[] | "- \(.title) (delegated to: \(.delegated_to))"'

echo ""
echo "=== Capacity Status ==="
curl -s "$YATTA_API_URL/capacity/today" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq -r '"Utilization: \(.utilization_percent)% - \(.status)"'
```

### 从电子邮件创建任务

```bash
#!/bin/bash
# Extract email subject and body
SUBJECT="$1"
BODY="$2"

curl -s "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "'"$SUBJECT"'",
    "description": "'"$BODY"'",
    "priority": "medium",
    "import_source": "email"
  }' \
  | jq -r '"Task created: \(.title)"'
```

### 周度计划报告

```bash
#!/bin/bash
WEEK_START=$(date -v+mon "+%Y-%m-%d")
WEEK_END=$(date -v+sun "+%Y-%m-%d")

echo "=== Week of $WEEK_START ==="
curl -s "$YATTA_API_URL/capacity?start=$WEEK_START&end=$WEEK_END" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq -r '.[] | "\(.date): \(.status) (\(.utilization_percent)%)"'

echo ""
echo "=== Tasks Due This Week ==="
curl -s "$YATTA_API_URL/tasks?due_date_gte=$WEEK_START&due_date_lte=$WEEK_END" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq -r '.[] | "[\(.due_date)] \(.title)"'
```

## 错误处理

**检查响应状态：**
```bash
RESPONSE=$(curl -s -w "\n%{http_code}" "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY")

STATUS=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$STATUS" -eq 200 ]; then
  echo "$BODY" | jq '.'
else
  echo "Error: HTTP $STATUS"
  echo "$BODY" | jq '.error'
fi
```

**速率限制处理：**
```bash
RESPONSE=$(curl -s -i "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY")

# Check X-RateLimit headers
REMAINING=$(echo "$RESPONSE" | grep -i "X-RateLimit-Remaining" | cut -d' ' -f2)
RESET=$(echo "$RESPONSE" | grep -i "X-RateLimit-Reset" | cut -d' ' -f2)

if [ "$REMAINING" -lt 10 ]; then
  echo "Warning: Only $REMAINING requests remaining"
  echo "Rate limit resets at: $(date -r $RESET)"
fi
```

## 提示：

- **安全存储 API 密钥：** 使用 1Password CLI、环境变量或 secrets manager
- **使用 jq 进行数据过滤：** 通过 `jq` 处理响应以获得清晰的输出
- **批量操作：** 尽可能一次更新多个任务
- **速率限制：** 每个 API 密钥每分钟 100 次请求
- **日期格式：** 始终使用 ISO 8601 格式（日期格式为 YYYY-MM-DD，时间戳格式为 YYYY-MM-DDTHH:MM:SSZ）
- **错误响应：** 响应中包含错误信息

## 资源

- **API 文档：** [Yatta! API 文档](https://yattadone.com/docs/api)（即将发布）
- **GitHub 仓库：** https://github.com/chrisagiddings/openclaw-yatta-skill
- **报告问题：** https://github.com/chrisagiddings/openclaw-yatta-skill/issues

## API 地址说明

目前为了确保可靠性，直接使用 Supabase Edge Functions 的 API 地址：
```
https://zunahvofybvxpptjkwxk.supabase.co/functions/v1
```

品牌化的 URL（`yattadone.com/api`）将在解决与托管提供商的代理配置问题后提供。