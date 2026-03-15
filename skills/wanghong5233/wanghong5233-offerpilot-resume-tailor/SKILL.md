---
name: resume-tailor
description: 生成、审核并导出定制的应用程序材料。
---
# 定制简历功能

## 触发条件

当用户提出以下请求时，该功能将被激活：
- “为这份工作生成定制简历”
- “帮助我准备申请材料”
- “批准/拒绝这份材料草稿”
- “导出已批准的材料”

## 工作流程

1. 如果用户提供了 `job_id`，则调用材料生成 API：
   - `POST http://127.0.0.1:8010/api/material/generate`
   - 请求体：`{"job_id":"<job_id>","resume_version":"resume_v1"}`

2. 解析 JSON 响应：
   - 如果 `status` 为 `skipped_low_match`，说明匹配度较低，询问用户是否希望继续处理其他工作。
   - 如果 `status` 为 `pending_review`，则显示以下内容：
     - `thread_id`
     - 简历内容
     - 封面信
     - 问候信息

3. 请求用户给出审核决定：
   - `approve` / `reject` / `regenerate`（可选的反馈信息）

4. 执行审核请求：
   - `POST http://127.0.0.1:8010/api/material/review`
   - 请求体示例：
     - `{"thread_id":"<thread_id>","decision":"regenerate","feedback":"请强调可量化的成果"}`

5. 如果审核通过，导出文件：
   - `POST http://127.0.0.1:8010/api/material/export`
   - 请求体：`{"thread_id":"<thread_id>","format":"pdf"}`
   - 将文件名或下载链接提供给用户。

## 命令模板（使用 `curl` 工具）

- 生成简历：
  - `curl -sS -X POST "http://127.0.0.1:8010/api/material/generate" -H "Content-Type: application/json" -d '{"job_id":"<job_id>","resume_version":"resume_v1"}'`

- 审核简历：
  - `curl -sS -X POST "http://127.0.0.1:8010/api/material/review" -H "Content-Type: application/json" -d '{"thread_id":"<thread_id>","decision":"approve"}`

- 导出简历：
  - `curl -sS -X POST "http://127.0.0.1:8010/api/material/export" -H "Content-Type: application/json" -d '{"thread_id":"<thread_id>","format":"pdf"}`

## 限制条件

- 严禁自动提交外部申请。
- 对于任何批准或拒绝的操作，都必须获得用户的明确确认。
- 如果 API 出现错误或 JSON 数据无效，必须向用户明确显示错误信息，并询问用户是否需要重试。