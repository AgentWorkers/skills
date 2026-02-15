---
name: vikunja-fast
description: 通过 Vikunja API 管理 Vikunja 项目及其任务（包括逾期、到期或今日需完成的任务），标记任务为“已完成”，并快速获取任务概要。
homepage: https://vikunja.io/
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":["curl","jq"],"env":["VIKUNJA_URL"],"optionalEnv":["VIKUNJA_TOKEN","VIKUNJA_USERNAME","VIKUNJA_PASSWORD"]},"primaryEnv":"VIKUNJA_TOKEN"}}
---

# ✅ Vikunja 快速技能

使用 Vikunja 作为任务和完成情况的权威信息来源，并通过 Clawdbot 与之进行交互。

## 设置

您可以通过环境变量 **或** Clawdbot 的技能配置来提供凭据。

### 选项 A：环境变量

在运行网关的同一环境中设置这些环境变量：

```bash
export VIKUNJA_URL="https://vikunja.xyz"

# Recommended: use a JWT (starts with "eyJ")
export VIKUNJA_TOKEN="<jwt>"

# Alternative: login with username/password (the helper CLI will request a JWT)
export VIKUNJA_USERNAME="<username>"
export VIKUNJA_PASSWORD="<password>"
```

### 选项 B：Clawdbot 技能配置（推荐给代理）

编辑 `~/.clawdbot/clawdbot.json`：

```json5
{
  skills: {
    entries: {
      "vikunja-fast": {
        enabled: true,
        env: {
          VIKUNJA_URL: "https://vikunja.xyz",
          VIKUNJA_TOKEN: "<jwt>"
        }
      }
    }
  }
}
```

**注意：**
- `VIKUNJA_URL` 可以是基础 URL；辅助工具会将其规范化为 `/api/v1`。
- Vikunja 的身份验证要求大多数 API 调用使用 JWT 承载令牌（`Authorization: Bearer <jwt>`）。
- 如果您只有非 JWT 令牌（通常以 `tk_...` 开头），请使用 `/login` 来获取 JWT。

## 快速检查

### 登录（获取 JWT）
```bash
curl -fsS -X POST "$VIKUNJA_URL/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"YOUR_USERNAME","password":"YOUR_PASSWORD","long_token":true}' | jq
```

### 我是谁？（需要 JWT）
```bash
curl -fsS "$VIKUNJA_URL/user" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq
```

### 列出项目
```bash
curl -fsS "$VIKUNJA_URL/projects" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" | jq '.[] | {id, title}'
```

## 命令

此技能附带了一个简单的辅助命令行工具：

- `{baseDir}/vikunja.sh`

**示例：**

```bash
# Overdue across all projects
{baseDir}/vikunja.sh overdue

# Due today
{baseDir}/vikunja.sh due-today

# Arbitrary filter (Vikunja filter syntax)
{baseDir}/vikunja.sh list --filter 'done = false && due_date < now'

# Show / complete a task
{baseDir}/vikunja.sh show 123
{baseDir}/vikunja.sh done 123
```

**注意：**
- 输出格式：
  - 每个任务应格式化为：`<EMOJI> <截止日期> - #<ID> <任务>`
  - 如果项目标题以表情符号开头，则使用该表情符号；否则使用 `🔨`
  - 截止日期显示为 `Mon/D`（时间+年份被省略）
- 该技能使用 `GET /tasks/all` 来获取所有项目中的任务

## 标记任务已完成
```bash
TASK_ID=123

curl -fsS -X POST "$VIKUNJA_URL/tasks/$TASK_ID" \
  -H "Authorization: Bearer $VIKUNJA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"done": true}' | jq
```