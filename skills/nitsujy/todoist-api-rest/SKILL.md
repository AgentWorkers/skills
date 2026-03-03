---
name: todoist-api-rest
description: 通过 curl/jq 直接集成 Todoist API。该集成方式轻量级、可靠，并支持使用 v1/v2 版本的 API 端点。
homepage: https://developer.todoist.com
metadata:
  clawdbot:
    emoji: "✅"
    requires:
      bins: ["curl", "jq"]
      env: ["TODOIST_API_TOKEN"]
---
# Todoist API（REST v2 & API v1）

此技能提供了对 Todoist 的直接 API 访问。当 CLI 不可用或出现故障时，可以使用此方法。

## 设置
确保 `TODOIST_API_TOKEN` 已设置，或者使用来自 `~/.openclaw/.secrets/todoist_token.json` 的令牌。

## 核心命令（REST v2）

### 列出活跃任务
```bash
curl -H "Authorization: Bearer $TODOIST_API_TOKEN" https://api.todoist.com/rest/v2/tasks | jq .
```
*注意：如果 REST v2 返回 410 错误，请使用 `api/v1/tasks`（见下文）。*

### 创建任务
```bash
curl -X POST -H "Authorization: Bearer $TODOIST_API_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"content": "New Task", "due_string": "today"}' \
     https://api.todoist.com/rest/v2/tasks
```

### 完成（关闭）任务
```bash
curl -X POST -H "Authorization: Bearer $TODOIST_API_TOKEN" https://api.todoist.com/rest/v2/tasks/<task_id>/close
```

## 备用/旧版命令（API v1）

当 REST v2 端点返回 `410 Gone` 错误时，可以使用这些命令。

### 列出任务（v1）
```bash
curl -H "Authorization: Bearer $TODOIST_API_TOKEN" https://api.todoist.com/api/v1/tasks | jq .results
```

### 创建任务（v1）
```bash
curl -X POST -H "Authorization: Bearer $TODOIST_API_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"content": "v1 Task", "project_id": "6g382hF2W96x2hvr"}' \
     https://api.todoist.com/api/v1/tasks
```

### 完成任务（v1）
```bash
curl -H "Authorization: Bearer $TODOIST_API_TOKEN" \
     "https://api.todoist.com/api/v1/tasks/completed/by_completion_date?since=2026-03-01T00:00:00Z&until=2026-03-04T23:59:59Z" | jq .items
```

## 项目与分类

### 列出项目
```bash
curl -H "Authorization: Bearer $TODOIST_API_TOKEN" https://api.todoist.com/rest/v2/projects
```

### 列出分类
```bash
curl -H "Authorization: Bearer $TODOIST_API_TOKEN" "https://api.todoist.com/rest/v2/sections?project_id=<project_id>"
```