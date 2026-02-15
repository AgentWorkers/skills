---
name: clickup
displayName: ClickUp Integration
description: 与 ClickUp API 进行交互以实现任务管理功能。该 API 可用于列出任务、创建任务、更新任务状态以及管理工作空间。基础 URL 为：https://api.clickup.com/api/v2
version: 1.0.0
tags:
  - productivity
  - task-management
  - api
---

# ClickUp 集成

## 凭据
**注意：** 请在 `TOOLS.md` 中配置您的凭据，或通过设置环境变量来配置：
- `CLICKUP_API_TOKEN` - 您的 ClickUp API 令牌
- `CLICKUP_WORKSPACE_ID` - 您的 ClickUp 工作区 ID

## 用户分配指南
在分配任务时，请根据任务的执行者选择正确的电子邮件地址：

| 电子邮件 | 执行者 | 适用场景 |
|-------|-----|----------|
| `your-email@example.com` | **人工** | 需要您手动完成的任务 |
| `ai-assistant@example.com` | **AI 助手** | 需要 AI 执行的任务 |
| 两个电子邮件地址 | **人工 + AI** | 需要 AI 进行研究/写作、人工进行审核/决策的协作任务 |

### 示例
- **仅由 AI 完成的任务**：「研究趋势检测工具」 → 分配给 AI 的电子邮件地址
- **仅由人工完成的任务**：「为 YouTube 录制视频」 → 分配给您的电子邮件地址
- **协作任务**：「制定内容策略」 → 分配给两个电子邮件地址

## 常见操作

### 列出任务列表
```http
GET https://api.clickup.com/api/v2/list/{list_id}/task
Authorization: {your_api_token}
```

### 获取工作区中的所有任务
```http
GET https://api.clickup.com/api/v2/team/{workspace_id}/task
Authorization: {your_api_token}
```

### 创建任务
```http
POST https://api.clickup.com/api/v2/list/{list_id}/task
Authorization: {your_api_token}
Content-Type: application/json

{
  "name": "Task name",
  "description": "Task description",
  "status": "active"
}
```

### 更新任务状态
```http
PUT https://api.clickup.com/api/v2/task/{task_id}
Authorization: {your_api_token}
Content-Type: application/json

{
  "status": "done"
}
```

### 获取任务详情
```http
GET https://api.clickup.com/api/v2/task/{task_id}
Authorization: {your_api_token}
```

## 所有请求的请求头
```
Authorization: {your_api_token}
Content-Type: application/json
```

## 状态值
常见状态：`active`（活动）、`pending`（待处理）、`review`（审核中）、`completed`（已完成）、`done`（已完成）

## 错误处理
- 401：检查 API 令牌
- 404：验证 `list_id` 或 `task_id` 是否存在
- 429：达到请求限制 - 请稍后重试