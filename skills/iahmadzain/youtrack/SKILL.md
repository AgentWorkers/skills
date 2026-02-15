---
name: youtrack
description: 通过 CLI（命令行界面）来管理 YouTrack 的问题、项目和工作流程。适用于创建、更新、搜索或评论 YouTrack 问题、列出项目、检查问题状态，以及自动化问题处理流程等操作。
metadata: {"clawdbot":{"emoji":"🎫","requires":{"bins":["jq","curl"]}}}
---

# YouTrack CLI

使用 `ytctl`（位于 `scripts/` 目录中）来管理 YouTrack 问题跟踪系统。

## 设置

凭据存储在 `~/.config/youtrack/config.json` 文件中：
```json
{
  "url": "https://your-instance.youtrack.cloud",
  "token": "perm:xxx"
}
```

或者通过设置环境变量来配置：`YOUTRACK_URL`、`YOUTRACK_TOKEN`

生成令牌的方法：YouTrack → 账户设置 → 安全 → 新令牌

## 命令

```bash
# List projects
ytctl projects

# List issues (with optional filters)
ytctl issues                           # all issues
ytctl issues SP                        # issues in project SP
ytctl issues SP --query "state: Open"  # filtered
ytctl issues --max 50                  # limit results

# Get issue details
ytctl issue SP-123

# Create issue
ytctl create SP "Bug: Login fails"
ytctl create SP "Feature request" "Detailed description here"

# Update issue
ytctl update SP-123 state "In Progress"
ytctl update SP-123 assignee john.doe
ytctl update SP-123 priority Critical

# Add comment
ytctl comment SP-123 "Investigating this now"

# Search with YouTrack query syntax
ytctl search "project: SP state: Open assignee: me"
ytctl search "created: today"
ytctl search "#unresolved sort by: priority"

# List workflow states for project
ytctl states SP

# List users
ytctl users
ytctl users --query "john"
```

## 查询语法

YouTrack 的查询示例：
- `state: Open` — 按状态查询
- `assignee: me` — 查询分配给当前用户的任务
- `created: today` — 查询今天创建的任务
- `updated: {last week}` — 查询上周更新的任务
- `#unresolved` — 查询所有未解决的任务
- `has: attachments` — 查询包含附件的任务
- `sort by: priority desc` — 按优先级降序排序

组合查询：`project: SP state: Open assignee: me sort by: updated`

## 输出

默认输出格式为表格形式。若需要原始 JSON 格式，可使用 `--json` 选项：
```bash
ytctl issues SP --json
ytctl issue SP-123  # always JSON for single issue
```

## 批量操作

```bash
# Update all matching issues (with dry-run preview)
ytctl bulk-update "project: SP state: Open" state "In Progress" --dry-run
ytctl bulk-update "project: SP state: Open" state "In Progress"

# Comment on all matching issues
ytctl bulk-comment "project: SP state: Open" "Batch update notice"

# Assign all matching issues
ytctl bulk-assign "project: SP #unresolved" john.doe --dry-run
```

## 报告

```bash
# Project summary (default 7 days)
ytctl report SP
ytctl report SP --days 14

# User activity report
ytctl report-user zain
ytctl report-user zain --days 30

# State distribution with bar chart
ytctl report-states SP
```

## 注意事项：

- 项目名称可以是缩写（如 `SP`）或全名
- 可查询的字段包括：状态（state）、摘要（summary）、描述（description）、分配者（assignee）和优先级（priority）
- 可使用 `ytctl states PROJECT` 查看有效的状态名称
- 批量操作支持 `--dry-run` 选项，执行前可进行预览