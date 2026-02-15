---
name: browser-use
version: 1.0.0
description: 通过 `Browser Use API` 实现云浏览器自动化。当您需要人工智能驱动的网页浏览、数据抓取、表单填写或多步骤网页任务（且无需使用本地浏览器）时，可以使用该功能。该功能会在以下情况下被触发：`browser use`、`cloud browser`、`scrape website`、`automate web task`，或者当本地浏览器不可用/不合适时。
metadata: {"clawdbot":{"emoji":"🌐","requires":{"env":["BROWSER_USE_API_KEY"]}}}
---

# 浏览器使用

基于云的AI浏览器自动化工具。您可以使用简单的英语指令来发起任务，并获得结构化的数据结果。

## 快速入门

```bash
# Submit task
curl -s -X POST https://api.browser-use.com/api/v2/tasks \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task": "Go to example.com and extract the main heading"}'

# Poll for result (replace TASK_ID)
curl -s "https://api.browser-use.com/api/v2/tasks/TASK_ID" \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY"
```

## 辅助脚本

使用 `scripts/browser-use.sh` 可以更便捷地执行任务：

```bash
# Run task and wait for result
./scripts/browser-use.sh "Go to hacker news and get the top 3 stories"

# Just submit (don't wait)
./scripts/browser-use.sh --no-wait "Search Google for AI news"
```

## API参考

### 创建任务
```
POST https://api.browser-use.com/api/v2/tasks
```

任务执行过程：
```json
{
  "task": "Plain English description of what to do",
  "llm": "gemini-3-flash-preview"  // optional, default is fast model
}
```

任务结果：
```json
{
  "id": "task-uuid",
  "sessionId": "session-uuid"
}
```

### 获取任务状态
```
GET https://api.browser-use.com/api/v2/tasks/{taskId}
```

响应字段：
- `status`: `pending` | `started` | `finished` | `failed`
- `output`: 任务完成后的结果文本
- `steps`: 执行的步骤列表（包含截图）
- `cost`: 任务成本（以美元为单位，例如：“0.02”）
- `isSuccess`: 任务是否成功的布尔值

### 停止任务
```
POST https://api.browser-use.com/api/v2/tasks/{taskId}/stop
```

## 价格

根据任务复杂度，费用约为0.01至0.05美元。请查看您的账户余额：

```bash
curl -s https://api.browser-use.com/api/v2/credits \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY"
```

## 适用场景

- 复杂的多步骤网页操作
- 阻止简单数据抓取的网站
- 表单填写与提交
- 需要步骤截图的情况
- 无法使用本地浏览器控制时

## 不适用场景

- 简单的页面获取（请使用 `web_fetch` 工具）
- 可以使用本地浏览器时（请使用 `browser` 工具）
- 需要快速或大量数据抓取时（请使用其他自动化工具或本地抓取方法）