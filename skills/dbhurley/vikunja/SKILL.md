---
name: vikunja
description: 在 Vikunja（一个开源的项目管理工具）中管理和安排项目与任务。您可以创建项目、设置任务期限、优先级，并跟踪任务的完成情况。
homepage: https://vikunja.io
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":["uv"],"env":["VIKUNJA_URL","VIKUNJA_USER","VIKUNJA_PASSWORD"]},"primaryEnv":"VIKUNJA_URL"}}
---

# Vikunja 项目管理

在 [Vikunja](https://vikunja.io) 中管理和安排项目及任务。Vikunja 是一个开源的、可自行托管的项目管理工具。

## 设置

配置以下环境变量：
- `VIKUNJA_URL`：您的 Vikunja 实例 URL（例如：`https://vikunja.example.com`）
- `VIKUNJA_USER`：用户名或电子邮件地址
- `VIKUNJA_PASSWORD`：密码

## 命令

### 项目
```bash
# List all projects
uv run {baseDir}/scripts/vikunja.py projects

# Get project details
uv run {baseDir}/scripts/vikunja.py project <ID>

# Create a project
uv run {baseDir}/scripts/vikunja.py create-project "Project Name" -d "Description"
```

### 任务
```bash
# List all tasks
uv run {baseDir}/scripts/vikunja.py tasks

# List tasks in a specific project
uv run {baseDir}/scripts/vikunja.py tasks --project <PROJECT_ID>

# Create a task
uv run {baseDir}/scripts/vikunja.py create-task "Task title" --project <ID> --due 2026-01-15 --priority 3

# Mark task complete
uv run {baseDir}/scripts/vikunja.py complete <TASK_ID>
```

### 选项
- `--json`：以 JSON 格式输出结果（适用于程序化使用）

## 优先级级别
- 0：无
- 1：低
- 2：中等
- 3：高
- 4：紧急
- 5：关键

## 示例
```bash
# Create a project for Q1 planning
uv run {baseDir}/scripts/vikunja.py create-project "Q1 2026 Planning" -d "Quarterly planning tasks"

# Add a high-priority task
uv run {baseDir}/scripts/vikunja.py create-task "Review budget" --project 5 --due 2026-01-20 --priority 3

# Check what's due
uv run {baseDir}/scripts/vikunja.py tasks --project 5 --json
```