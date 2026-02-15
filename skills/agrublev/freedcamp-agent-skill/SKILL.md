---
name: freedcamp
description: "通过 HMAC-SHA1 API 凭据来管理 Freedcamp 的任务、项目、组、评论、通知以及任务列表。"
homepage: https://freedcamp.com
user-invocable: true
metadata: {"openclaw":{"requires":{"env":["FREEDCAMP_API_KEY","FREEDCAMP_API_SECRET"]},"primaryEnv":"FREEDCAMP_API_KEY","homepage":"https://freedcamp.com"}}
---

# Freedcamp

此技能提供了一个不依赖任何外部库的 Node.js 命令行工具（CLI），它使用 **HMAC-SHA1 加密机制**（API 密钥 + API 秘密密钥）来调用 Freedcamp 的 REST API（v1）。

- 脚本路径：`{baseDir}/scripts/freedcamp.mjs`
- 认证方式：`FREEDCAMP_API_KEY` + `FREEDCAMP_API_SECRET`
- 输出格式：**仅限 JSON**（标准输出），适用于自动化脚本或代理程序。

## 设置

1. 从您的 Freedcamp 账户设置中获取 API 密钥和秘密密钥。
2. 将这两个值设置为环境变量。

### 常见的配置方式

- **Shell 环境变量**（用于本地测试）：

  ```
  export FREEDCAMP_API_KEY="..."
  export FREEDCAMP_API_SECRET="..."
  ```

- **OpenClaw 配置**（推荐方式）：设置 `skills.entries.freedcamp.apiKey` 和 `skills.entries.freedcamp.env.FREEDCAMP_API_SECRET`，这样这些密钥仅在代理程序运行时才会被使用。

### 通过 OpenClaw CLI 进行配置（推荐方式）

```bash
openclaw config set skills.entries.freedcamp.enabled true
openclaw config set skills.entries.freedcamp.apiKey "YOUR_API_KEY"
openclaw config set skills.entries.freedcamp.env.FREEDCAMP_API_SECRET "YOUR_API_SECRET"
```

**验证已保存的配置信息：**

```bash
openclaw config get skills.entries.freedcamp
```

**删除已保存的凭据：**

```bash
openclaw config unset skills.entries.freedcamp.apiKey
openclaw config unset skills.entries.freedcamp.env.FREEDCAMP_API_SECRET
```

## 初始操作（用于验证功能）

- 获取用户信息/会话状态：

  `node {baseDir}/scripts/freedcamp.mjs me`

- 列出所有组、项目和应用：

  `node {baseDir}/scripts/freedcamp.mjs groups-projects`

## ID 的解析

当用户提供项目名称时，系统会将其解析为对应的 ID：

- `groups-projects` 会返回包含项目名称和 ID 的所有组。
- 其他命令应使用输出中的 `project_name` 来指定项目。

**注意**：如果存在多个匹配项，请避免手动猜测项目 ID。

## 核心功能：任务管理

### 列出项目中的任务

`node {baseDir}/scripts/freedcamp.mjs tasks --project <project_id> --all`

### 带过滤条件的任务列表

`node {baseDir}/scripts/freedcamp.mjs tasks --project <project_id> --status in_progress,not_started --assigned_to 2,-1`

**常用的过滤参数：**
- `--status`：`not_started`, `completed`, `in_progress`, `invalid`, `review`（用逗号分隔）
- `--assigned_to`：用户 ID（用逗号分隔，`0` 表示未分配，`-1` 表示所有人）
- `--due_from YYYY-MM-DD` / `--due_to YYYY-MM-DD`：任务截止日期
- `--created_from YYYY-MM-DD` / `--created_to YYYY-MM-DD`：任务创建日期
- `--list_status active|archived|all`：显示任务状态（active, archived, all）
- `--with_archived true`：包括已归档项目的任务
- `--limit <n>`：每页显示的任务数量（默认为 200 个）
- `--offset <n>`：用于分页

### 获取单个任务（包含评论和文件）

`node {baseDir}/scripts/freedcamp.mjs task <task_id>`

### 创建任务

`node {baseDir}/scripts/freedcamp.mjs create-task --project <project_id> --title "任务标题"`

**可选参数：**
- `--description`：任务描述
- `--task_group <task_group_id>`：任务所属的组 ID

### 更新任务

`node {baseDir}/scripts/freedcamp.mjs update-task <task_id> --title "新标题" --status in_progress`

**任务状态代码：**
- `not_started`（0）
- `completed`（1）
- `in_progress`（2）
- `invalid`（3）
- `review`（4）

### 按项目名称创建任务

`node {baseDir}/scripts/freedcamp.mjs create-task-by-name --project_name "我的项目" --app_name "任务" --title "新任务"`

系统会使用会话数据自动解析项目名称对应的 ID。目前仅支持 “Tasks” 应用。

## 任务列表（按组分类）

- 列出某个项目的任务列表：

`node {baseDir}/scripts/freedcamp.mjs task-lists --project <project_id>`

- 指定应用（默认为 “Tasks”）：

`node {baseDir}/scripts/freedcamp.mjs task-lists --project <project_id> --app_id 2`

## 评论功能

- 为任何任务添加评论：

`node {baseDir}/scripts/freedcamp.mjs comment <item_id> --app_name "任务" --text "我的评论"`

评论内容会自动被包裹在 `<p>` 标签中。您也可以直接传递 HTML 格式的评论内容：

`node {baseDir}/scripts/freedcamp.mjs comment <item_id> --app_name "任务" --html "<p><b>粗体文本</b></p>"`

### 评论对应的应用名称

添加评论时，必须指定 `--app_name` 的值，例如：“Tasks”, “Discussions” 等。

## 通知功能

- 获取最近 60 天内的通知：

`node {baseDir}/scripts/freedcamp.mjs notifications`

- 将通知标记为已读：

`node {baseDir}/scripts/freedcamp.mjs mark-read <notification_uid>`

## 数据模型说明

### 任务状态

| 状态 | 对应的 CLI 参数 |
|---|---|
| 未开始 | `not_started` |
| 完成 | `completed` |
| 进行中 | `in_progress` |
| 无效 | `invalid` |
| 审核中 | `review` |

### 任务优先级

| 优先级 | 对应的 CLI 参数 |
|---|---|
| 无 | `0` |
| 低 | `1` |
| 中等 | `2` |
| 高 | `3` |

### 应用类型

| 应用 ID | 应用名称 | 关键字 |
|---|---|
| 2 | Tasks | TODOS |
| 3 | Discussions | DISCUSSIONS |
| 4 | Milestones | MILESTONES |
| 5 | Time | TIME |
| 6 | Files | FILES |
| 13 | Issue Tracker | BUGTRACKER |
| 14 | Wikis | WIKI |
| 16 | CRM | CRM |
| 17 | Passwords | PASSMAN |
| 19 | Calendar | CALENDAR |
| 47 | Planner | PLANNER |
| 48 | Translations | TRANSLATIONS |

## 其他注意事项：

- 评论内容必须包含 HTML 格式；通过 `--text` 传递的纯文本会自动被转换为 `<p>` 标签。
- 每次请求最多只能获取 200 条任务信息；使用 `--offset` 参数可以分页获取更多数据。
- 会话信息会存储在本地，并在遇到 401 错误时自动刷新。
- 使用 `--all` 参数可以获取所有任务信息。

## 不支持的功能

- 该工具不提供 “Invoices” 和 “Invoices Plus” 相关的 API。
- 该工具不包含内置的 “Bot 行为” 功能；您需要自行在代理程序中配置相关逻辑。