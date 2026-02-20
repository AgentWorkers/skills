---
name: pylon-support
description: 通过 Pylon 的 REST API 来处理工单。当您需要列出或检查问题、添加内部备注/客户回复，或执行任何自定义的 Pylon API 调用时，请使用该接口。
---
# Pylon 支持操作

本技能包提供了轻量级的工具，用于与 Pylon 的 REST API 进行交互，使您能够在不离开终端的情况下审核工单、跟进处理或发布更新。

## 设置

1. 创建一个具有所需权限（如查看问题、消息、联系人等）的 Pylon API 令牌。
2. 在运行任何脚本之前，先导出该令牌：
   ```bash
   export PYLON_API_TOKEN="<token>"
   ```
3. 可选：使用 `PYLON_API_BASE` 替换基础 URL（适用于测试环境）。

有关端点概述和示例请求体的详细信息，请参阅 [`references/pylon_api.md`](references/pylon_api.md)。

## 脚本

### `scripts/pylon_list_issues.py`
该脚本可以快速列出 `/issues` 中的数据，并提供常见的过滤选项，帮助您快速找到需要处理的工单。

```bash
python3 scripts/pylon_list_issues.py --state waiting_on_you --limit 25
python3 scripts/pylon_list_issues.py --assignee-id usr_123 --team-id team_9
```

脚本会打印 API 的响应结果；如果适用，还会显示下一页的查询游标。您可以通过 `--page-cursor` 参数继续查询下一页的数据。

### `scripts/pylon_request.py`
这是一个通用脚本，用于调用 Pylon 的任意端点。您需要提供端点路径、请求方法以及可选的参数或请求体。

```bash
# Update a ticket state
python3 scripts/pylon_request.py /issues/iss_123 \
  --method PATCH \
  --data '{"state":"waiting_on_customer"}'

# Add an internal note
python3 scripts/pylon_request.py /issues/iss_123/messages \
  --method POST \
  --data '{"message_html":"<p>Looping product...</p>","is_private":true}'

# Fetch issue messages (GET is default)
python3 scripts/pylon_request.py /issues/iss_123/messages
```

**参数说明**：
- `--param key=value`：用于添加查询参数（可重复使用）。
- `--data '{...}'` 或 `--data-file payload.json`：用于指定请求体内容。

### `scripts/pylon_client.py`
这是一个通用的辅助脚本，负责处理身份验证、基础 URL 的设置以及 JSON 数据的解析。如果您需要编写更具体的任务脚本，请导入此脚本。

## 工作流程建议

1. **每天早上进行工单分类**：运行 `pylon_list_issues.py --state waiting_on_you` 可以查看团队尚未回复的工单列表。
2. **深入查看工单详情**：使用 `pylon_request.py /issues/<id>` 获取工单的元数据，再通过 `/issues/<id>/messages` 查看工单的交流记录。
3. **快速更新工单状态**：使用 `--method PATCH` 来修改工单状态或设置工单的提醒时间。
4. **在交接过程中添加上下文信息**：在通过 Slack 标记团队成员之前，可以使用 `is_private=true` 选项发布内部备注。

有关所有可用端点（如用户、联系人、标签等）的详细信息，请参阅 [`references/pylon_api.md`](references/pylon_api.md)。如果需要未在此文档中提及的字段，请参考官方文档。