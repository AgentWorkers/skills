---
name: a-safer-email-assistant
description: 该功能利用 `ai-email-gateway` API 来同步邮箱信息，检测重要的新邮件，回答与邮件历史相关的问题，并生成回复草稿，而无需实际发送邮件。建议将 `ai-email-gateway` 服务部署在独立的服务器上（使用 GitHub 上的 [ArktIQ-IT/ai-email-gateway](https://github.com/ArktIQ-IT/ai-email-gateway) 项目），以确保 OpenClaw 无法获取用户的收件箱访问权限。该功能适用于以下场景：用户需要查看邮件、筛选重要信息、与相关人员总结邮件历史记录或起草回复内容时。
---
# 更安全的电子邮件助手

## 目的

使用此技能来操作安全的电子邮件网关 API，以实现人工智能辅助的电子邮件工作流程：
- 手动同步/补发邮件
- 检查新的重要邮件
- 查询邮件往来记录
- 创建回复草稿

**注意**：切勿直接发送邮件。该网关仅支持创建邮件草稿。

## 所需的运行时输入参数

- `GATEWAY_BASE_URL`（示例：`http://localhost:8000`）
- `GATEWAY_API_KEY`（bearer token）
- `ACCOUNT_ID`（网关账户 ID）

## 核心工作流程规则

1. 在进行数据分析之前，务必先完成同步操作（尤其是当邮件更新频率较高时）。
2. 对于定期检查，仅处理未查看过的或新收到的邮件。
3. 使用规范的邮件标识符（`folder|uidvalidity|uid`）来执行后续操作。
4. 为建议的回复创建草稿，但不要实际发送邮件。
5. 如果需要查看邮件历史记录，请先执行明确指定的 `since` 和 `until` 时间范围内的手动同步操作。

## 任务操作指南

### 1) 手动同步（获取新邮件或补发邮件）

1. 使用 `POST /v1/accounts/{account_id}/sync` 请求，指定 `since`、`until`、`folders`、`include_subfolders` 和 `limit_per_folder` 参数。
2. 轮询 `GET /v1/jobs/{job_id}` 请求，直到收到任务完成状态。
3. 仅当任务状态为 `done` 时，继续执行后续操作。

### 2) 定期检查 + 重要邮件检测

1. 加载每个账户的本地状态信息（`last_checked_at`、`seen_ids`）。
2. 对 `[last_checked_at, now)` 时间范围内的邮件执行手动同步操作。
3. 查询 `messages:list`，筛选出方向为 `incoming` 的邮件。
4. 过滤出未查看过的邮件 ID。
5. 如果没有未查看过的邮件，返回 “没有新邮件” 的提示。
6. 仅对未查看过的邮件根据用户设定的标准判断其重要性。
7. 返回重要的邮件信息，并更新本地状态。

### 3) 创建建议的回复草稿

1. 从 `messages:list` 或 `messages:get` 中选择合适的回复邮件。
2. 根据用户的语气和偏好生成回复内容。
3. 使用 `POST /v1/accounts/{account_id}/drafts` 请求，提供 `to`、`cc`、`subject` 和 `text_body`（可选参数：`html_body`、`attachments`）。
4. 返回草稿的 ID 及生成草稿的依据。

### 4) 查询已发送/收到的邮件相关问题

使用 `messages:list` 的过滤条件：
- 发件人：`senders=["person@example.com"]`
- 收件人：`recipients=["person@example.com"]`
- 时间范围：`since`, `until`
- 主题：`free_text`
- 邮件方向：`incoming` 或 `sent`

然后根据查询结果生成回复，并引用相关邮件的 ID。

### 5) 查询与某人的邮件历史记录

1. 确保已针对所需时间范围完成历史数据的同步。
2. 查询该联系人发送和接收的所有邮件：
   - 来自该联系人的邮件（`senders`）
   - 发送给该联系人的邮件（`recipients`）
3. 汇总邮件时间线，并列出关键信息及后续需要执行的操作。

## 任务输出格式

完成任务后，建议使用以下格式输出结果：

```markdown
## Result
- status: success|partial|failed
- account_id: ...
- timeframe: ...

## Key findings
- ...

## Suggested actions
- ...

## Evidence
- message ids: ...
```

## 安全性要求

- 严禁泄露 `GATEWAY_API_KEY` 或邮箱相关敏感信息。
- 禁止实现邮件发送功能。
- 如果同步失败，应立即报告错误并停止所有依赖该操作的步骤。
- 如果缺少邮件重要性的判断标准，在执行操作前请先获取相关标准。

## 额外资源

- API 详细信息：[api-reference.md](api-reference.md)
- 重要性评估模板：[prompts/importance-classifier.md](prompts/importance-classifier.md)
- 草稿撰写模板：[prompts/drafting-style.md]
- 监控脚本示例：[scripts/check_new_messages.py](scripts/check_new_messages.py)