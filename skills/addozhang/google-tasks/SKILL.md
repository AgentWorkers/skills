---
name: google-tasks
version: 1.0.0
description: 使用 Google Tasks API 来获取、显示、创建和删除 Google 任务。当用户需要查看、列出、获取、添加、创建或删除他们的 Google 任务、待办事项列表或任务项时，可以使用该功能。该功能通过 bash 脚本结合 curl 和 jq 自动处理 OAuth 认证。
author: OpenClaw Community
keywords: [google-tasks, tasks, todo, productivity, bash, oauth]
license: MIT
---

# Google Tasks Skill

通过轻量级的 Bash 脚本，可以从所有任务列表中管理 Google 任务。

## 快速入门

### 查看任务
```bash
bash scripts/get_tasks.sh
```

### 创建任务
```bash
# Using default list (configured in google-tasks-config.sh)
bash scripts/create_task.sh "Task title" ["due-date"] ["notes"]

# Specifying list name
bash scripts/create_task.sh "List Name" "Task title" ["due-date"] ["notes"]
```

示例：
```bash
# Simple task (uses default list)
bash scripts/create_task.sh "Buy groceries"

# Task with due date (uses default list)
bash scripts/create_task.sh "Finish report" "2026-02-10"

# Task with specific list
bash scripts/create_task.sh "Work" "Finish report" "2026-02-10"

# Task with list, due date, and notes
bash scripts/create_task.sh "Personal" "Call mom" "2026-02-05" "Ask about her health"
```

**默认列表配置：**
编辑 `google-tasks-config.sh` 以设置您的默认列表：
```bash
DEFAULT_LIST="Private"  # Change to your preferred default
```

### 删除任务
```bash
bash scripts/delete_task.sh "List Name" <task-number-or-title>
```

示例：
```bash
# Delete by task number (position in list)
bash scripts/delete_task.sh "Work" 2

# Delete by task title
bash scripts/delete_task.sh "Inbox" "Buy groceries"
```

## 所需软件

- `jq` - JSON 处理工具（通常已预安装）
- `curl` - HTTP 客户端（通常已预安装）
- 包含 OAuth 访问令牌的 `token.json` 文件
- **所需权限：** `https://www.googleapis.com/auth/tasks`（读取 + 写入）

## 首次设置

如果 `token.json` 文件不存在：

1. 用户需要 OAuth 凭据（`credentials.json` 文件）——请参阅 [setup.md](references/setup.md)
2. 先运行 Node.js 认证流程以生成 `token.json` 文件
3. 之后就可以使用这些 Bash 脚本来执行所有操作了

## 输出格式

```
📋 Your Google Tasks:

📌 List Name
──────────────────────────────────────────────────
  1. ⬜ Task title (due: YYYY-MM-DD)
     Note: Task notes if present
  2. ⬜ Another task

📌 Another List
──────────────────────────────────────────────────
  (no tasks)
```

## 文件位置

- `token.json` - 访问/刷新令牌（工作区根目录）
- `google-tasks-config.sh` - 配置文件（默认列表设置）
- `scripts/get_tasks.sh` - 查看任务的 Bash 脚本
- `scripts/create_task.sh` - 创建任务的 Bash 脚本
- `scripts/delete_task.sh` - 删除任务的 Bash 脚本
- `references/setup.md` - 详细的设置指南

## 实现方式

这些 Bash 脚本直接使用 Google Tasks 的 REST API，通过 `curl` 发送 HTTP 请求，并使用 `jq` 进行 JSON 解析。脚本采用基于令牌（Bearer token）的认证方式，因此不需要依赖 Python。

## 故障排除

**令牌过期：**
```
Error: Invalid credentials
```
删除 `token.json` 文件并重新进行认证。

**找不到 jq：**
```
bash: jq: command not found
```
安装 `jq`：`apt-get install jq` 或 `brew install jq`

更多详细信息，请参阅 [setup.md](references/setup.md)。