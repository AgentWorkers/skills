---
name: supabase
description: 查询 Supabase 项目：统计用户数量、列出注册用户信息、查看各项统计数据。适用于数据库查询和用户数据分析。
user-invocable: true
disable-model-invocation: true
triggers:
  - supabase
  - database
  - how many users
  - new signups
  - user count
metadata:
  clawdbot:
    emoji: "⚡"
    primaryEnv: SUPABASE_SERVICE_KEY
    requires:
      bins: [python3]
      env: [SUPABASE_URL, SUPABASE_SERVICE_KEY]
---

# Supabase ⚡

您可以直接通过聊天功能查询您的 Supabase 项目信息。

## 设置

### 1. 获取您的凭证

请访问 **Supabase 仪表板 → 项目设置 → API**

您将看到两个选项卡：
- **“可公开的和私有的 API 密钥”** - 新格式（功能有限）
- **“旧版匿名用户/服务角色 API 密钥”** - JWT 格式（功能齐全）

**⚠️ 请使用旧版 JWT 密钥以获得完整访问权限！**

`service_role` JWT 密钥（以 `eyJ...` 开头）提供完整的管理员权限，包括：
- 列出用户信息
- 统计注册用户数量
- 访问 `auth.users` 数据

新的 `sb_secret_...` 密钥功能有限，无法访问管理员 API。

### 2. 查找您的密钥

1. 访问：**项目设置 → API**
2. 点击 **“旧版匿名用户/服务角色 API 密钥”** 选项卡
3. 找到标记为红色的 “secret” 标签的 `service_role` 密钥
4. 点击 **显示** 并复制 `eyJ...` 令牌

直接链接：`https://supabase.com/dashboard/project/YOUR_PROJECT_REF/settings/api`

### 3. 配置

**选项 A：交互式设置**
```bash
python3 {baseDir}/scripts/supabase.py auth
```

**选项 B：手动配置**
创建 `~/.supabase_config.json` 文件：
```json
{
  "url": "https://xxxxx.supabase.co",
  "service_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**选项 C：环境变量**
```bash
export SUPABASE_URL="https://xxxxx.supabase.co"
export SUPABASE_SERVICE_KEY="eyJhbG..."
```

## 命令

### 用户分析
```bash
# Count total users
python3 {baseDir}/scripts/supabase.py users

# Count new users (24h)
python3 {baseDir}/scripts/supabase.py users-today

# Count new users (7 days)  
python3 {baseDir}/scripts/supabase.py users-week

# List users with details (name, email, provider, signup date)
python3 {baseDir}/scripts/supabase.py list-users

# List new users from last 24h
python3 {baseDir}/scripts/supabase.py list-users-today

# Limit results
python3 {baseDir}/scripts/supabase.py list-users --limit 5
```

### 项目信息
```bash
# Show project info and key type
python3 {baseDir}/scripts/supabase.py info

# List tables exposed via REST API
python3 {baseDir}/scripts/supabase.py tables
```

### JSON 输出
```bash
python3 {baseDir}/scripts/supabase.py list-users --json
```

## 密钥类型说明

| 密钥类型 | 格式 | 是否可以列出用户 | 是否可以统计用户数量 | 是否可以访问 REST 表格 |
|----------|--------|--------------|------------|-------------|
| JWT service_role | `eyJ...` | ✅ 是 | ✅ 是 | ✅ 是 |
| 新型秘密密钥（sb_secret_...） | ❌ 否 | ❌ 否 | ✅ 是 |

**建议：** 在集成 Clawdbot 时，请始终使用 `service_role` JWT 密钥。

## 日报

通过 Clawdbot 的 cron 任务设置自动生成每日用户报告。

### 示例：下午 5 点生成日报

向 Clawdbot 发送请求：
```
Send me a report of how many new users signed up at 5 PM every day, 
show the last 5 signups with their names
```

这将创建一个 cron 作业，如下所示：
```json
{
  "name": "Daily Supabase User Report",
  "schedule": {
    "kind": "cron",
    "expr": "0 17 * * *",
    "tz": "America/Los_Angeles"
  },
  "payload": {
    "message": "Supabase daily report: Count new user signups in the last 24 hours, and list the 5 most recent signups with their name and email."
  }
}
```

### 报告示例输出

```
📊 Supabase Daily Report

New signups (last 24h): 2

Last 5 signups:
• Jane Smith <jane@example.com> (google) - 2026-01-25
• Alex Johnson <alex.j@company.com> (google) - 2026-01-25
• Sam Wilson <sam@startup.io> (email) - 2026-01-24
• Chris Lee <chris.lee@email.com> (google) - 2026-01-23
• Jordan Taylor <jordan@acme.co> (github) - 2026-01-22
```

## GraphQL API (pg_graphql)

⚠️ 自 2025 年底起，新创建的 Supabase 项目默认禁用了 `pg_graphql`。

如果您需要使用 GraphQL API：

### 启用 pg_graphql
```sql
-- Run in SQL Editor
create extension if not exists pg_graphql;
```

### 端点
```
https://<PROJECT_REF>.supabase.co/graphql/v1
```

### 示例查询
```bash
curl -X POST https://<PROJECT_REF>.supabase.co/graphql/v1 \
  -H 'apiKey: <API_KEY>' \
  -H 'Content-Type: application/json' \
  --data-raw '{"query": "{ accountCollection(first: 1) { edges { node { id } } } }"}'
```

注意：GraphQL 会自动反映您的数据库架构。`public` 架构中的表格/视图都可以被查询。有关配置详情，请参阅 [Supabase GraphQL 文档](https://supabase.com/docs/guidesgraphql)。

## 故障排除

### “list-users 需要 JWT service_role 密钥”
您可能使用了 `sb_secret_...` 密钥。请从以下位置获取 JWT 密钥：
**项目设置 → API → 旧版选项卡 → service_role → 显示**

### “请求中未找到 API 密钥”
新的 `sb_secret_` 密钥不支持所有端点，请切换到 JWT 密钥。

### 密钥未显示
请确保您在 **“旧版匿名用户/服务角色 API 密钥”** 选项卡上，而不是新 API 密钥选项卡。

## 安全与权限

`service_role` 密钥具有对数据库的 **完整管理员权限**。此技能需要该密钥来访问管理员 API（列出/统计用户）。

**此技能的功能：**
- 向您的 Supabase 项目的管理员 API 发送 GET 请求
- 读取用户元数据（电子邮件、姓名、提供商、注册日期）
- 所有请求仅限于您的机器和 Supabase 实例之间

**此技能不执行以下操作：**
- 不会写入、修改或删除任何数据
- 不会向任何第三方发送凭证
- 不会访问 Supabase 项目之外的任何端点
- 不能被代理程序自动调用（`disable-model-invocation: true`）

**最低权限替代方案：** 创建一个仅具有 `auth.users` 访问权限的只读 Postgres 角色，并使用 Supabase SQL API 代替管理员 API。

**密钥安全注意事项：**
- 绝不要将密钥提交到 Git
- 不要在客户端代码中暴露密钥
- 仅在可信机器上使用该技能
- 配置文件会自动设置为 600 模式（仅所有者可读写）
- 在首次使用前请查看 `scripts/supabase.py` 文件