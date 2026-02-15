---
name: locu
description: 通过 Locu 的公共 API 来管理任务和项目。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎯",
        "requires": { "env": ["LOCU_API_TOKEN"] },
        "primaryEnv": "LOCU_API_TOKEN",
      },
  }
---

# Locu Skill

使用 Locu 公共 API 来与您的工作空间进行交互。

## 认证
- `LOCU_API_TOKEN`：您的个人访问令牌（Personal Access Token，简称 PAT）。

## 命令

### 用户信息
- 获取我的信息：`curl -X GET "https://api.locu.app/api/v1/me" -H "Authorization: Bearer $LOCU_API_TOKEN"`

### 任务
- 列出任务：`curl -X GET "https://api.locu.app/api/v1/tasks" -H "Authorization: Bearer $LOCU_API_TOKEN"`

### 项目
- 列出项目：`curl -X GET "https://api.locu.app/api/v1/projects" -H "Authorization: Bearer $LOCU_API_TOKEN"`

## 使用说明
请始终解析 JSON 输出内容，以获取任务的详细信息（ID、名称、完成状态、类型）。Locu 的任务可以是本地的，也可以是从 Linear/Jira 集成的。