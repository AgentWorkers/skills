# Vikunja 卡诺邦（Kanban）技能

通过 API 管理 Vikunja 卡诺邦看板。可以读取任务状态、创建/移动/完成任务，并与心跳（heartbeat）和问题分类（triage）定时任务集成。

## 配置

凭据存储在 `secrets/vikunja.env` 文件中：
```
VIKUNJA_URL=https://your-vikunja-instance
VIKUNJA_TOKEN=${VIKUNJA_TOKEN}
VIKUNJA_PROJECT_ID=1
VIKUNJA_VIEW_ID=4
```

## 认证

所有脚本使用一个 **长期有效的 API 令牌**（有效期至 2030-01-01）。无需 JWT 登录。
- 权限：任务（读取所有、更新、创建、删除），项目（读取所有、更新、创建）
- JWT 登录凭据存储在 `secrets/vikunja.env` 文件中，仅用于参考

## 仓库 ID（Bucket IDs）

| ID | 名称 | 用途 |
|----|------|---------|
| 1 | 🔴 紧急（Urgent） | 需立即处理 |
| 2 | ⏳ 待处理（Waiting On） | 已发送/请求，等待回复 |
| 7 | ⚠️ 系统问题（System Issues） | 基础设施/系统故障 |
| 8 | 🚧 进行中（Active Projects） | 任务正在进行中 |
| 9 | 📅 即将进行（Upcoming） | 已安排的未来任务 |
| 10 | 📥 收件箱（Inbox） | 新任务，未分类 |
| 3 | ✅ 已完成（Done） | 任务已完成 |

## 脚本

所有脚本位于技能的 `scripts/` 目录中。请从技能根目录运行这些脚本。

### 读取看板信息
```bash
bash scripts/vikunja-status.sh              # All buckets
bash scripts/vikunja-status.sh "Urgent"     # Filter by bucket name
```

### 添加任务
```bash
bash scripts/vikunja-add-task.sh "Title" "Description" BUCKET_ID [PRIORITY]
# Priority: 0=unset, 1=low, 2=medium, 3=high, 4=urgent
# Example: bash scripts/vikunja-add-task.sh "Fix DNS" "Check records" 1 4
```

### 在不同仓库之间移动任务
```bash
bash scripts/vikunja-move-task.sh TASK_ID BUCKET_ID
# Example: bash scripts/vikunja-move-task.sh 15 3  # Move to Done
```

### 完成任务
```bash
bash scripts/vikunja-complete-task.sh TASK_ID
```

## 心跳集成（Heartbeat Integration）

心跳定时任务会从 Vikunja 读取数据：
```bash
bash scripts/vikunja-status.sh
```
- 检查 🔴 紧急任务中超过 1 小时未处理的项
- 如果无法连接到 Vikunja，则回退到 `scripts/nc-status-board.sh read` 脚本进行读取

## 邮件问题分类集成（Email Triage Integration）

邮件问题分类功能会将需要处理的任务添加到 “收件箱” 仓库中：
```bash
bash scripts/vikunja-add-task.sh "Email subject" "Brief description" 10 3
```

## API 参考

- **基础 URL：** https://your-vikunja-instance/api/v1
- **认证：** 使用用户名/密码进行 POST 请求 → 使用 JWT 令牌（有效期较短）
- **任务操作：**  
  - `PUT /projects/{id}/tasks` （创建任务）  
  - `POST /tasks/{id}` （更新任务）  
- **仓库操作：**  
  - `POST /projects/{id}/views/{view}/buckets/{bucket}/tasks` （移动任务）  
  - `GET /projects/{id}/views/{view}/tasks` （按仓库列出任务）  
- **项目操作：**  
  - `POST /projects/{id}` （更新项目标题/设置）  
  - `GET /projects` （列出所有项目）  
- **共享操作：**  
  - `PUT /projects/{id}/users` （添加用户）  
- **用户操作：**  
  - `GET /users?s(query)` （搜索用户）  
  - `POST /user/password` （用户自行更改密码）

## 已知的 API 错误与注意事项

### 共享权限在创建用户时被忽略
`PUT /projects/{id}/users` 操作会忽略 `right` 字段，始终创建用户的权限为 0（仅读）。
**解决方法：** 直接在 PostgreSQL 中设置用户权限：
```sql
UPDATE users_projects SET permission = 2 WHERE user_id = X AND project_id = Y;
```
权限值：0=仅读，1=读写，2=管理员

### 默认的 “收件箱” 项目无法删除
每个新用户都会自动创建一个名为 “收件箱” 的项目。尝试删除该项目时（`DELETE /projects/{id}`）会返回错误 3012。
**解决方法：** 通过 `POST /projects/{id}` 并传入 `{"title":"新名称"}` 来重命名该项目

### 密码更改只能通过用户自行操作
没有管理员端点可以更改其他用户的密码。必须以目标用户的身份登录：
`POST /api/v1/user/password`，传入 `{"old_password":"...", "new_password":"..."`

### 创建 API 令牌需要同时具备任务和项目的权限
仅具有 `tasks` 权限的令牌无法查看卡诺邦看板的信息（会返回 401 错误）。
创建令牌时必须包含以下权限：`{"permissions":{"tasks":["read_all","update","create","delete"],"projects":["read_all","update","create"]}`

### 令牌创建端点
`PUT /api/v1/tokens` 用于创建令牌，`GET /api/v1/tokens` 用于查看令牌列表，`DELETE /api/v1/tokens/{id}` 用于删除令牌。
必填字段：`title`（令牌名称）、`expires_at`（ISO-8601 格式的过期时间）、`permissions`（权限对象）

## 其他注意事项

- 使用 **长期有效的 API 令牌**（有效期至 2030 年），无需 JWT 登录
- Vikunja 使用 `PUT` 方法进行任务创建，使用 `POST` 方法进行任务更新（这可能不太常见）
- 仓库 ID 与具体的卡诺邦视图相关联（`view_id=4`）
- 项目名称已从默认的 “收件箱” 更改为 “Kit Operations”
- 项目共享设置：  
  - Kit（ID：1，管理员/所有者）  
  - Alex（ID：2，通过数据库修复后可以设置为管理员）  
- 令牌包含任务和项目的权限，支持所有卡诺邦操作  
- 每个用户都有一个默认项目，该项目无法被删除——建议重命名以避免混淆