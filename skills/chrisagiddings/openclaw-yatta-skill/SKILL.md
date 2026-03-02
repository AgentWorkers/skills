---
name: yatta
description: Personal productivity system for task and capacity management. Create and organize tasks with rich attributes (priority, effort, complexity, tags), track time and streaks, manage capacity across projects and contexts, view Eisenhower Matrix prioritization, sync calendar subscriptions, handle delegation and follow-ups, and get AI-powered insights. Supports batch operations, multi-project workflows, and real-time capacity planning to prevent overcommitment. Security: v0.2.0 eliminates RCE vulnerability from v0.1.3 (shell/JSON injection in examples), adds endpoint verification, safe jq patterns throughout.
homepage: https://github.com/chrisagiddings/openclaw-yatta-skill
disable-model-invocation: true
metadata: {"openclaw":{"emoji":"✅","requires":{"env":["YATTA_API_KEY","YATTA_API_URL"],"bins":["curl","jq"],"anyBins":["openssl","dig"]},"primaryEnv":"YATTA_API_KEY","disable-model-invocation":true,"capabilities":["task-management","project-management","context-management","comment-management","calendar-management","destructive-operations"],"credentials":{"type":"env","variables":[{"name":"YATTA_API_KEY","description":"Yatta! API key (yatta_...)","required":true},{"name":"YATTA_API_URL","description":"Yatta! API base URL","required":false,"default":"https://zunahvofybvxpptjkwxk.supabase.co/functions/v1"}]}}}
---

# Yatta! 技能

通过 API 与 Yatta! 任务管理系统进行交互。需要使用您的 Yatta! 账户生成的 API 密钥。

## ⚠️ 安全警告

**此技能可能对您的 Yatta! 账户执行破坏性操作：**

- **任务管理：** 创建、更新、归档和批量修改任务
- **项目管理：** 创建、更新和归档项目
- **上下文管理：** 创建上下文并将其分配给任务
- **评论管理：** 添加、更新和删除任务评论
- **日历管理：** 创建、同步和修改日历订阅
- **跟进管理：** 更新跟进计划并标记为已完成
- **容量管理：** 触发容量计算

**操作类型：**

**只读操作**（✅ 安全）：
- 列出任务、项目、上下文和评论
- 获取分析数据、洞察和统计信息
- 查看容量和日历数据
- 获取艾森豪威尔矩阵视图
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
1. **运行前查看命令** - 确认 API 调用会执行什么操作
2. **删除操作不可撤销** - 归档的任务可以恢复，但某些操作是永久性的
3. **先在非关键数据上测试** - 创建测试任务/项目以验证行为
4. **批量操作会影响多个项目** - 对批量更新要格外小心
5. **实时同步** - 更改会立即显示在 Yatta! 用户界面中

有关详细的 API 操作文档，请参阅 [API-REFERENCE.md](API-REFERENCE.md)。

## 设置

### ⚠️ API 密钥安全

**您的 Yatta! API 密钥可提供对您账户的完全访问权限：**
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
5. 安全地存储它

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

### ⚠️ API 端点验证

**默认 API 端点托管在 Supabase 上：**

- **默认 URL：** `https://zunahvofybvxpptjkwxk.supabase.co/functions/v1`
- **项目：** Yatta! 生产后端
- **所有者：** Chris Giddings (chris@chrisgiddings.net)
- **应用：** https://yattadone.com

**为什么选择 Supabase？**
- Yatta! 使用 Supabase 作为其后端基础设施
- 该 URL 是 Supabase 项目的直接端点
- 品牌化 URL（api.yattadone.com）正在规划中

**验证步骤：**

1. **验证应用所有权：**
   - 访问 https://yattadone.com
   - 检查设置 → 关于或页脚以确认 API 端点

2. **检查 SSL 证书：**
   ```bash
   openssl s_client -connect zunahvofybvxpptjkwxk.supabase.co:443 \
     -servername zunahvofybvxpptjkwxk.supabase.co < /dev/null 2>&1 \
     | openssl x509 -noout -subject -issuer
   ```

3. **运行验证脚本：**
   ```bash
   # Automated endpoint verification
   bash scripts/verify-endpoint.sh
   ```

4. **如有疑问，请联系支持：**
   - 电子邮件：support@yattadone.com
   - 仅将 API 密钥发送到经过验证的端点

**品牌化 URL（即将推出）：**
- 未来：`https://api.yattadone.com/v1`
- 当品牌化 URL 上线后，此技能将自动更新

**安全提示：**
仅将 API 密钥发送到您信任且已验证的端点。
如果您愿意等待品牌化 API URL，这也是一个有效的安全选择。

### 3. 测试连接
   ```bash
   curl -s "$YATTA_API_URL/tasks" \
     -H "Authorization: Bearer $YATTA_API_KEY" \
     | jq '.[:3]'  # Show first 3 tasks
   ```

## 🔒 安全：输入验证

**⚠️ 重要提示：** 如果用户输入未经过适当清理，此技能容易受到 shell 和 JSON 注入攻击。**

### 安全编码模式（必需）

**此技能中的所有示例都使用安全模式：**
- ✅ **JSON 载荷：** 使用 `jq -n --arg` 构建（防止 JSON 注入）
- ✅ **URL 参数：** 使用 `jq -sRr @uri` 进行编码（防止 shell 注入）
- ✅ **不在 JSON 或 URL 中直接插入字符串**

### 快速参考

```bash
# ✅ SAFE: JSON construction
PAYLOAD=$(jq -n --arg title "$TITLE" '{title: $title}')
curl -d "$PAYLOAD" ...

# ✅ SAFE: URL encoding
TASK_ID_ENCODED=$(printf %s "$TASK_ID" | jq -sRr @uri)
curl "$API_URL/tasks/$TASK_ID_ENCODED" ...

# ✅ BEST: Use wrapper functions
source scripts/yatta-safe-api.sh
yatta_create_task "Finish report" "high"
```

### 为什么这很重要

**不安全的编码模式可能导致：**
- API 密钥泄露
- 任意命令执行（RCE）
- 数据被篡改或损坏

**请参阅 [SECURITY.md] 以获取：**
- 详细的漏洞示例
- 攻击场景和影响
- 安全编码模式
- 测试指南

**请参阅 [scripts/yatta-safe-api.sh](scripts/yatta-safe-api.sh) 以获取：**
- 预构建的安全包装函数
- 可直接使用的示例
- 无样板代码

---

## 🎯 调用政策

**此技能仅允许手动调用。**

### 政策详情

**设置：`disable-model-invocation: true`

**这意味着：**
- 代理将**不会** 自动执行 Yatta! 操作
- **用户必须明确请求** 每个操作
- 不会创建或修改后台任务
- 所有操作都需要明确的用户意图

### 为什么只能手动调用？

**安全原因：**

1. **完全的账户访问权限：** Yatta! API 密钥授予完全的账户访问权限
- **没有只读权限：** 无法限制 API 密钥的权限
- **破坏性操作：** 可能永久删除/归档/修改数据
- **需要用户监督：** 所有更改在执行前都应经过审核

### 示例

**❌ 自动调用（不允许）：**
```
User: "I should probably archive old tasks"
Agent: *silently archives tasks without confirmation*
```

**✅ 手动调用（必需）：**
```
User: "Please archive tasks older than 30 days"
Agent: *executes explicit request, shows results*
```

### 政策执行

**工作原理：**
1. 技能元数据声明 `disable-model-invocation: true`
2. OpenClaw 将遵守此设置
3. 代理需要明确的用户命令
4. 不会自动执行后台操作

**验证：**
```bash
# Check package.json
jq '.openclaw["disable-model-invocation"]' package.json
# Should output: true

# Check SKILL.md frontmatter
grep "disable-model-invocation" SKILL.md
# Should show: "disable-model-invocation":true
```

### 如果出现意外操作

**如果 Yatta! 操作在您未明确请求的情况下发生：**

1. **立即停止** - 这表明违反了政策
2. **撤销 API 密钥** - 在 Yatta! 设置 → API 密钥中创建新密钥
3. **提交问题** - 至 https://github.com/chrisagiddings/openclaw-yatta-skill/issues
4. **报告给 OpenClaw** - 报告政策执行错误

**这种情况不应发生** - 手动调用是安全要求。

---

## 任务 API

### 列出任务

**列出所有任务：**
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

# Get tasks for that project (URL-encode query parameter)
PROJECT_ID_ENCODED=$(printf %s "$PROJECT_ID" | jq -sRr @uri)
curl -s "$YATTA_API_URL/tasks?project_id=$PROJECT_ID_ENCODED" \
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

**归档的任务：**
```bash
curl -s "$YATTA_API_URL/tasks?archived=true" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### 创建任务

**创建简单任务：**
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

**创建包含详细信息的任务：**
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

**创建带有跟进任务的委托任务：**
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

**创建重复任务：**
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
# ✅ SAFE: Use jq to build JSON payload
TASK_ID="uuid-of-task"
PAYLOAD=$(jq -n \
  --arg id "$TASK_ID" \
  --arg status "done" \
  --arg completed_at "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  '{id: $id, status: $status, completed_at: $completed_at}')

curl -s -X PUT "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
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
# ✅ SAFE: Use jq to build JSON payload
TASK_ID="uuid-of-task"
PAYLOAD=$(jq -n --arg id "$TASK_ID" '{id: $id}')

curl -s -X DELETE "$YATTA_API_URL/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  | jq '.'
```

## 项目 API

### 列出项目**

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

### 创建项目**

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

### 更新项目**

```bash
# ✅ SAFE: Use jq to build JSON payload
PROJECT_ID="uuid-of-project"
PAYLOAD=$(jq -n \
  --arg id "$PROJECT_ID" \
  --arg name "Website Redesign v2" \
  --argjson archived false \
  '{id: $id, name: $name, archived: $archived}')

curl -s -X PUT "$YATTA_API_URL/projects" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  | jq '.'
```

### 获取项目任务**

```bash
# ✅ SAFE: URL-encode path parameter
PROJECT_ID="uuid-of-project"
PROJECT_ID_ENCODED=$(printf %s "$PROJECT_ID" | jq -sRr @uri)

curl -s "$YATTA_API_URL/projects/$PROJECT_ID_ENCODED/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

## 上下文 API

### 列出上下文**

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

### 创建上下文**

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

### 将上下文分配给任务**

```bash
# ✅ SAFE: Use jq to build JSON payload with arrays
TASK_ID="uuid-of-task"
CONTEXT_ID="uuid-of-context"

PAYLOAD=$(jq -n \
  --arg task_id "$TASK_ID" \
  --arg context_id "$CONTEXT_ID" \
  '{task_id: $task_id, context_ids: [$context_id]}')

curl -s -X POST "$YATTA_API_URL/contexts/assign" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  | jq '.'
```

### 获取任务上下文**

```bash
# ✅ SAFE: URL-encode path parameter
TASK_ID="uuid-of-task"
TASK_ID_ENCODED=$(printf %s "$TASK_ID" | jq -sRr @uri)

curl -s "$YATTA_API_URL/tasks/$TASK_ID_ENCODED/contexts" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### 获取带有上下文的任务**

```bash
# ✅ SAFE: URL-encode path parameter
CONTEXT_ID="uuid-of-context"
CONTEXT_ID_ENCODED=$(printf %s "$CONTEXT_ID" | jq -sRr @uri)

curl -s "$YATTA_API_URL/contexts/$CONTEXT_ID_ENCODED/tasks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

## 评论 API

### 列出任务评论**

```bash
# ✅ SAFE: URL-encode path parameter
TASK_ID="uuid-of-task"
TASK_ID_ENCODED=$(printf %s "$TASK_ID" | jq -sRr @uri)

curl -s "$YATTA_API_URL/tasks/$TASK_ID_ENCODED/comments" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### 添加评论**

```bash
# ✅ SAFE: URL-encode path + jq for JSON
TASK_ID="uuid-of-task"
TASK_ID_ENCODED=$(printf %s "$TASK_ID" | jq -sRr @uri)
PAYLOAD=$(jq -n \
  --arg content "Waiting on client feedback before proceeding" \
  '{content: $content}')

curl -s -X POST "$YATTA_API_URL/tasks/$TASK_ID_ENCODED/comments" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  | jq '.'
```

### 更新评论**

```bash
# ✅ SAFE: Use jq to build JSON payload
COMMENT_ID="uuid-of-comment"
PAYLOAD=$(jq -n \
  --arg id "$COMMENT_ID" \
  --arg content "Client responded, moving forward" \
  '{id: $id, content: $content}')

curl -s -X PUT "$YATTA_API_URL/task-comments" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  | jq '.'
```

### 删除评论**

```bash
# ✅ SAFE: Use jq to build JSON payload
COMMENT_ID="uuid-of-comment"
PAYLOAD=$(jq -n --arg id "$COMMENT_ID" '{id: $id}')

curl -s -X DELETE "$YATTA_API_URL/task-comments" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  | jq '.'
```

## 跟进 API

### 获取今天的跟进事项**

```bash
curl -s "$YATTA_API_URL/follow-ups" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.[] | {title, delegated_to, follow_up_date}'
```

### 获取指定日期的跟进事项**

```bash
DATE="2026-02-15"
curl -s "$YATTA_API_URL/follow-ups?date=$DATE" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### 标记跟进事项为已完成**

```bash
# ✅ SAFE: URL-encode path parameter
TASK_ID="uuid-of-task"
TASK_ID_ENCODED=$(printf %s "$TASK_ID" | jq -sRr @uri)

curl -s -X POST "$YATTA_API_URL/tasks/$TASK_ID_ENCODED/follow-up" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}' \
  | jq '.'
```

### 更新跟进计划**

```bash
# ✅ SAFE: URL-encode path + jq for JSON
TASK_ID="uuid-of-task"
TASK_ID_ENCODED=$(printf %s "$TASK_ID" | jq -sRr @uri)

PAYLOAD=$(jq -n \
  --arg type "every_n_days" \
  --argjson interval 3 \
  --arg next_follow_up "2026-02-12" \
  '{type: $type, interval: $interval, next_follow_up: $next_follow_up}')

curl -s -X PUT "$YATTA_API_URL/tasks/$TASK_ID_ENCODED/follow-up-schedule" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  | jq '.'
```

## 日历 API

### 列出日历订阅**

```bash
curl -s "$YATTA_API_URL/calendar/subscriptions" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### 添加日历订阅**

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

### 触发日历同步**

```bash
# ✅ SAFE: URL-encode path parameter
SUBSCRIPTION_ID="uuid-of-subscription"
SUBSCRIPTION_ID_ENCODED=$(printf %s "$SUBSCRIPTION_ID" | jq -sRr @uri)

curl -s -X POST "$YATTA_API_URL/calendar/subscriptions/$SUBSCRIPTION_ID_ENCODED/sync" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### 列出日历事件**

```bash
# Events for date range
START="2026-02-10"
END="2026-02-17"
curl -s "$YATTA_API_URL/calendar/events?start=$START&end=$END" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

## 容量 API

### 获取今天的容量**

```bash
curl -s "$YATTA_API_URL/capacity/today" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '{date, utilization_percent, status, used_minutes, total_minutes}'
```

### 获取指定日期范围的容量**

```bash
START="2026-02-10"
END="2026-02-17"
curl -s "$YATTA_API_URL/capacity?start=$START&end=$END" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.[] | {date, status, utilization_percent}'
```

### 触发容量计算**

```bash
curl -s -X POST "$YATTA_API_URL/capacity/compute" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

## 分析 API

### 获取汇总洞察**

```bash
curl -s "$YATTA_API_URL/analytics/summary" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### 获取速度指标**

```bash
curl -s "$YATTA_API_URL/analytics/velocity" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### 获取任务分布**

```bash
curl -s "$YATTA_API_URL/analytics/distribution" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '{by_status, by_priority, by_matrix_state}'
```

### 获取统计信息**

```bash
curl -s "$YATTA_API_URL/analytics/streaks" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

### 获取 AI 洞察**

```bash
curl -s "$YATTA_API_URL/analytics/insights" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '.'
```

## 矩阵 API

### 获取艾森豪威尔矩阵视图**

```bash
curl -s "$YATTA_API_URL/tasks/matrix" \
  -H "Authorization: Bearer $YATTA_API_KEY" \
  | jq '{do_first, schedule, delegate, eliminate}'
```

## 常见模式

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

### 从电子邮件创建任务**

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

### 周期性计划报告**

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

## 提示**

- **安全存储 API 密钥：** 使用 1Password CLI、环境变量或秘密管理器
- **使用 jq 进行过滤：** 通过 `jq` 处理响应以获得清晰的结果
- **批量操作：** 尽可能一次更新多个任务
- **速率限制：** 每个 API 密钥每分钟 100 次请求
- **日期格式：** 始终使用 ISO 8601 格式（日期格式为 YYYY-MM-DD，时间戳格式为 YYYY-MM-DDTHH:MM:SSZ）
- **错误响应：** 包含带有描述的 `error` 字段

## 资源

- **API 文档：** [Yatta! API 文档](https://yattadone.com/docs/api)（即将发布）
- **GitHub 仓库：** https://github.com/chrisagiddings/openclaw-yatta-skill
- **报告问题：** https://github.com/chrisagiddings/openclaw-yatta-skill/issues

## API URL 注意

目前使用直接的 Supabase Edge Functions URL 以确保可靠性：
```
https://zunahvofybvxpptjkwxk.supabase.co/functions/v1
```

品牌化 URL（`yattadone.com/api`）将在未来版本中提供，届时将解决与托管提供商的代理配置问题。