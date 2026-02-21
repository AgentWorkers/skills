---
name: pylon-support
description: 通过 Pylon 的 REST API 来处理工单。当您需要列出或检查问题、添加内部备注/客户回复，或执行任何自定义的 Pylon API 调用时，可以使用该 API。
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["PYLON_API_TOKEN"] },
        "primaryEnv": "PYLON_API_TOKEN",
      },
  }
---
# Pylon 支持操作

此技能包提供了用于与 Pylon 的 REST API 交互的轻量级工具，使您能够在不离开终端的情况下审核工单、跟进进度或发布更新。

## 设置

1. 创建一个具有所需权限（如问题处理、消息发送、联系人管理等）的 Pylon API 令牌。
2. 在运行任何脚本之前导出该令牌：
   ```bash
   export PYLON_API_TOKEN="<token>"
   ```
3. （可选）使用 `PYLON_API_BASE` 替换基础 URL（用于测试环境）。
4. （可选）在 `~/.pylonrc` 文件中创建一个配置文件来缓存您的用户 ID 或自定义设置。使用 `pylon_env.py` 来管理这些设置。

有关端点概述和示例请求体的详细信息，请参阅 [`references/pylon_api.md`](references/pylon_api.md)。

## 脚本

### `scripts/pylon_list_issues.py`
快速列出 `/issues` 中的工单，并应用常见的过滤条件，以便您能够快速找到需要处理的工单。

```bash
python3 scripts/pylon_list_issues.py --state waiting_on_you --limit 25
python3 scripts/pylon_list_issues.py --team-id team_9
```

如果您希望脚本将结果过滤到指定的所有者名下，请设置 `--assignee-id <user-id>`（这很有用，因为 API 有时会忽略服务器端的过滤条件）。您可以通过以下命令获取自己的用户 ID：`python3 scripts/pylon_request.py /users --param search=jordan`。

该脚本会打印 API 的响应结果，并在适用的情况下提供下一页的查询指针（`cursor`）。您可以通过 `--page-cursor` 参数继续查询。

### `scripts/pylon_env.py`
一个轻量级的配置辅助工具，用于将您的用户 ID 或自定义设置缓存到 `~/.pylonrc` 文件中（路径可以通过 `PYLON_CONFIG_FILE` 进行修改）。

```bash
# Discover and cache your /me user id
python3 scripts/pylon_env.py --refresh-user-id

# Set a default window size and view summary
env PYLON_CONFIG_FILE=~/.pylonrc python3 scripts/pylon_env.py --set-window-days 7
python3 scripts/pylon_env.py --show
```

### `scripts/pylon_my_queue.py`
生成一个易于阅读的工单队列摘要：按状态统计工单数量，并显示每个工作单的详细信息（标题、优先级、最后更新时间等）。

```bash
# Quick view using cached user id
python3 scripts/pylon_my_queue.py

# Override assignee or window, limit API fetches
python3 scripts/pylon_my_queue.py --assignee-id usr_123 --window-days 14 --limit 400
```

### `scripts/pylon_triage_report.py`
高级分类报告：一次性获取多个工单的信息，按状态分组，并显示每种状态下更新时间最早的 N 个工单。

```bash
# My queue, 30-day window, top 10 per state
python3 scripts/pylon_triage_report.py --top 10

# Team view for multiple assignees, 14-day window
python3 scripts/pylon_triage_report.py \
  --assignee-id usr_kody --assignee-id usr_skyler --window-days 14 --top 5
```

### `scripts/pylon_update_issue.py`
无需打开用户界面即可快速更新工单的状态、标签、分配者或自定义字段。

```bash
# Move a ticket to waiting_on_customer and tag it
python3 scripts/pylon_update_issue.py iss_123 --state waiting_on_customer --tags followup pending_ops

# Set priority custom field
python3 scripts/pylon_update_issue.py iss_456 --priority high
```

### `scripts/pylon_add_note.py`
添加内部备注或对客户可见的回复。

```bash
# Internal note from inline text
python3 scripts/pylon_add_note.py iss_123 --text "Looping engineering for root cause" --private

# Customer reply from an HTML snippet
python3 scripts/pylon_add_note.py iss_123 --file reply.html --html
```

### `scripts/pylon_request.py`
一个通用的脚本封装，用于调用任何 Pylon 端点。您需要提供端点路径、方法以及可选的参数和请求体。

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

参数说明：
- `--param key=value`（可重复使用）：用于添加查询参数。
- `--data '{...}'` 或 `--data-file payload.json`：用于指定请求体内容。

### `scripts/pylon_client.py`
一个共享的辅助脚本，负责处理身份验证、基础 URL 和 JSON 解析。如果您需要编写更多特定任务的脚本，请导入此脚本。

## 工作流程建议

1. **每天早上进行分类处理**：运行 `pylon_list_issues.py --state waiting_on_you` 可以查看团队需要回复的工单列表。
2. **深入查看工单**：使用 `pylon_request.py /issues/<id>` 获取工单的元数据，然后通过 `/issues/<id>/messages` 查看对话记录。
3. **快速更新工单状态**：使用 `--method PATCH` 方法更新工单状态或设置延迟处理时间。
4. **在交接工作时提供上下文**：在通过 Slack 标记团队成员之前，先添加内部备注（`is_private=true`）。

有关所有可用端点（如用户、联系人、标签等）的完整信息，请参阅 [`references/pylon_api.md`]。如果需要此处未涵盖的字段，请参考官方文档。