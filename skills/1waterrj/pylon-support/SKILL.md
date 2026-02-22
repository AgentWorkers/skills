---
name: pylon-support
description: 通过 Pylon 的 REST API 来处理工单。当您需要列出或查看问题、添加内部备注/客户回复，或执行任何自定义的 Pylon API 调用时，可以使用此方法。
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

本技能包提供了一组轻量级的工具，用于与 Pylon 的 REST API 进行交互，使您能够在不离开终端的情况下审核工单、跟进进度或发布更新信息。

## 设置

1. 创建一个具有所需权限（如查看问题、消息、联系信息等）的 Pylon API 令牌。
2. 在运行任何脚本之前，先导出该令牌：
   ```bash
   export PYLON_API_TOKEN="<token>"
   ```

3. （可选）使用 `PYLON_API_BASE` 替换基础 URL（适用于测试环境）。
4. （可选）在 `~/.pylonrc` 文件中创建一个配置文件以缓存您的用户 ID 或自定义设置。可以使用 `pylon_env.py` 来管理这些设置。

有关端点概述和示例请求体的详细信息，请参阅 [`references/pylon_api.md`](references/pylon_api.md)。

## 脚本

### `scripts/pylon_list_issues.py`
快速列出 `/issues` 中的工单，并提供常见的过滤选项，帮助您识别需要处理的工单。

```bash
python3 scripts/pylon_list_issues.py --state waiting_on_you --limit 25
python3 scripts/pylon_list_issues.py --team-id team_9
```

如果您希望脚本将结果过滤到指定的所有者名下，请设置 `--assignee-id <user-id>` 参数（此方法很有用，因为 API 有时会忽略服务器端的过滤设置）。您可以通过以下命令查询自己的用户 ID：`python3 scripts/pylon_request.py /users --param search=jordan`。

该脚本会打印 API 的响应结果，并在适用的情况下提供下一页的查询指针（`cursor`）。您可以通过 `--page-cursor` 参数继续查询后续页面。

### `scripts/pylon_env.py`
一个轻量级的配置辅助工具，用于将您的用户 ID 或自定义设置缓存到 `~/.pylonrc` 文件中（该文件的路径可以通过 `PYLON_CONFIG_FILE` 进行修改）。

```bash
# Discover and cache your /me user id
python3 scripts/pylon_env.py --refresh-user-id

# Set a default window size and view summary
env PYLON_CONFIG_FILE=~/.pylonrc python3 scripts/pylon_env.py --set-window-days 7
python3 scripts/pylon_env.py --show
```

### `scripts/pylon_my_queue.py`
生成工单队列的可视化摘要：按状态统计工单数量，并显示每张工单的详细信息（标题、优先级、最后更新时间等）。

```bash
# Quick view using cached user id
python3 scripts/pylon_my_queue.py

# Override assignee or window, limit API fetches
python3 scripts/pylon_my_queue.py --assignee-id usr_123 --window-days 14 --limit 400
```

### `scripts/pylon_triage_report.py`
高级分类报告功能：一次性获取多个工单的信息，按状态分组，并显示每种状态下更新时间最早的 N 张工单。

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
用于添加内部备注或向客户显示的回复信息。

```bash
# Internal note from inline text
python3 scripts/pylon_add_note.py iss_123 --text "Looping engineering for root cause" --private

# Customer reply from an HTML snippet
python3 scripts/pylon_add_note.py iss_123 --file reply.html --html
```

### `scripts/pylon_followups.py`
查找 N 天内没有更新的工单，以便您能够及时跟进。

```bash
# My queue, flag anything idle >2 days
python3 scripts/pylon_followups.py

# Team view, 4-day threshold
python3 scripts/pylon_followups.py --assignee-id usr_kody --assignee-id usr_phil --threshold-days 4
```

### `scripts/pylon_team_summary.py`
为多个团队成员提供汇总视图。通过传递 `NAME=ID` 的参数对，可以查看他们的工单数量及需要关注的工单。

```bash
python3 scripts/pylon_team_summary.py \
  --assignee kody=usr_kody \
  --assignee phil=usr_phil \
  --assignee skyler=usr_skyler \
  --stale-days 3
```

### `scripts/pylon_morning_digest.py`
一次性生成 Markdown 格式的摘要，包含您的工单队列和团队动态。默认显示 Jordan 及核心团队的相关信息。

```bash
python3 scripts/pylon_morning_digest.py --stale-days 3 --limit 800
```

### `scripts/pylon_request.py`
这是一个通用脚本，用于调用任何 Pylon 端点。您需要提供端点的路径、方法以及可选的参数和请求体。

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
一个共享的辅助脚本，负责处理身份验证、基础 URL 和 JSON 数据的解析。如果您需要编写更多特定任务的脚本，请导入此脚本。

## 工作流程建议

1. **每天早上进行分类处理**：运行 `pylon_list_issues.py --state waiting_on_you` 可以查看团队需要回复的工单列表。
2. **深入查看工单详情**：使用 `pylon_request.py /issues/<id>` 获取工单的元数据，然后通过 `/issues/<id>/messages` 查看对话记录。
3. **快速更新工单状态**：使用 `--method PATCH` 方法修改工单状态或设置提醒时间。
4. **在交接工作时添加上下文信息**：在通过 Slack 标记团队成员之前，使用 `is_private=true` 选项添加内部备注。

有关所有可用端点（如用户、联系信息、标签等）的完整信息，请参阅 [`references/pylon_api.md`](references/pylon_api.md)。如果需要未在此文档中涵盖的字段，请参考官方文档。