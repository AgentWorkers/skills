---
name: "unitask-task-agent"
description: "在 Unitask (unitask.app) 中，可以通过带有作用域的 API 令牌（CLI 或 MCP）来管理任务和时间块。"
homepage: https://unitask.app
read_when:
  - User wants to manage Unitask tasks from an AI agent
  - User wants to time-block today using Unitask scheduled_start + duration_minutes
metadata: {"clawdbot":{"emoji":"✅"}}
---

# Unitask任务代理

## 目的

该功能允许AI代理使用**受限的API令牌**安全地管理用户的Unitask账户。  
它专为在**unitask.app**上托管使用而设计，因此最终用户无需运行任何本地服务器代码。  

**支持的操作：**  
- 列出任务  
- 获取单个任务  
- 创建任务  
- 更新任务状态  
- 删除任务（软删除）  
- 读取/更新设置（可选的一次性设置）  
- 规划每日时间块（预览/应用时间限制）  

**子任务：**  
- 子任务被视为具有`parent_id`的任务。  
- 通过创建`parent_id=<父任务ID>`的任务来创建子任务。  

## 适用场景  

当用户提出以下请求时，请使用此功能：  
- “列出我的任务”  
- “为X创建一个任务”  
- “将这些任务标记为已完成”  
- “将我的时间从上午9点到下午5点设置为时间限制”  

## 必要的设置  

1. 用户需在“Unitask -> 仪表板 -> 设置 -> API”中生成Unitask API令牌。  
2. 将该令牌作为`UNITASK_API_KEY=<token>`存储在代理/应用程序中的`secret/env`变量中。  

**注意：**  
切勿要求用户在聊天记录中粘贴完整的API令牌，而是让他们设置环境变量。  

## 权限模型  

- `read`：用于读取/列出任务。  
- `write`：用于创建/更新任务。  
- `delete`：用于删除任务。  
- 如果授予了`write`或`delete`权限，则必须同时授予`read`权限。  

## 托管MCP（unitask.app，HTTPS）  

使用托管的MCP端点：  
`https://unitask.app/api/mcp`  

**推荐的认证头：**  
`Authorization: Bearer <UNITASK_API_KEY>`  

## MCP工具  

**提供的API接口：**  
- `list_tasks` — 按`status`（待办|已完成|已归档）过滤任务，支持`limit`（1-500）、`offset`和`parent_id`参数  
- `get_task` — 通过ID获取单个任务  
- `create_task` — 需提供标题；可选参数：描述、parent_id、状态、优先级、截止日期、开始日期、重复频率、计划开始时间、持续时间（分钟）  
- `update_task_status` — 更改任务状态（待办|已完成|已归档）  
- `delete_task` — 软删除任务及其所有子任务  
- `get_settings` — 获取用户设置和测验偏好  
- `update_settings` — 部分更新设置/测验  
- `plan_day_timeblocks` — 在指定时间段内规划时间块  

**时间规划建议：**  
- 先使用`plan_day_timeblocks`并设置`apply=false`进行预览。  
- 用户确认计划后，再使用`apply=true`进行应用。  

## 安全规则：**  
- 仅为请求的操作授予最低必要的权限范围。  
- 除非用户明确要求，否则不要执行具有破坏性的操作（如删除）。  
- 当用户的意图是完成任务而非删除任务时，优先选择`status=done`。  
- 对于`plan_day_timeblocks`，建议先使用`apply=false`进行预览，用户确认后再应用。