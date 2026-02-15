---
name: vikunja
description: 在自托管的Vikunja实例上管理任务和项目。适用于用户需要创建、查看、完成任务、管理任务状态（如已到期或未到期）、列出项目列表，或接收任务通知的场景。同时也可用于创建待办事项列表、设置提醒以及进行任务跟踪。
---

# Vikunja 任务管理器

通过 REST API 在自托管的 Vikunja 实例上管理任务和项目。

## 设置

请设置以下环境变量：

```bash
export VIKUNJA_URL="https://your-vikunja-instance.com"
export VIKUNJA_TOKEN="your-api-token"
```

获取您的 API 令牌：Vikunja → 设置 → API 令牌 → 创建令牌。

## 命令

### 列出任务

```bash
{baseDir}/scripts/vikunja.sh tasks --count 10
{baseDir}/scripts/vikunja.sh tasks --project "Shopping" --count 5
{baseDir}/scripts/vikunja.sh tasks --search "groceries"
{baseDir}/scripts/vikunja.sh tasks --sort priority --order desc
```

### 过期任务

```bash
{baseDir}/scripts/vikunja.sh overdue
```

### 即将到期的任务（接下来的 N 小时）

```bash
{baseDir}/scripts/vikunja.sh due --hours 24
{baseDir}/scripts/vikunja.sh due --hours 48
```

### 创建任务

```bash
{baseDir}/scripts/vikunja.sh create-task --project "Tasks" --title "Buy milk" --due "2026-02-01" --priority 3
```

优先级：1（低）到 5（紧急）。截止日期格式：YYYY-MM-DD。

### 完成任务

```bash
{baseDir}/scripts/vikunja.sh complete --id 123
```

### 获取任务详情

```bash
{baseDir}/scripts/vikunja.sh task --id 123
```

### 列出项目

```bash
{baseDir}/scripts/vikunja.sh projects
```

### 创建项目

```bash
{baseDir}/scripts/vikunja.sh create-project --title "New Project" --description "Optional description"
```

### 获取通知

```bash
{baseDir}/scripts/vikunja.sh notifications
```

## 截止日期监控

要接收关于到期/过期任务的主动通知，请设置一个 cron 作业：

```bash
clawdbot cron add \
  --name "Task due check" \
  --cron "0 9,14 * * *" \
  --tz "America/Denver" \
  --session isolated \
  --message "Check Vikunja for overdue and upcoming tasks (next 24 hours). If any are found, notify me with the list." \
  --deliver \
  --channel telegram
```

## 注意事项

- `--project` 参数中的项目名称不区分大小写
- 过滤表达式遵循 Vikunja 的过滤语法（请参阅 https://vikunja.io/docs/filters）
- 所有时间均以美国/丹佛时区为准