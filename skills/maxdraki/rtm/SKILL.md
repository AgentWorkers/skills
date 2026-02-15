---
name: rtm
description: 管理 Remember The Milk 任务：可以列出任务、添加新任务、完成任务、删除任务、搜索任务、为任务设置优先级、给任务添加标签、移动任务位置，以及为任务添加备注。当用户询问有关任务、待办事项列表、提醒功能或 Remember The Milk 的相关信息时，可以使用该工具。
metadata:
  {
    "openclaw":
      {
        "emoji": "🐄",
        "requires":
          {
            "env": ["RTM_API_KEY", "RTM_SHARED_SECRET"],
          },
        "credentials":
          {
            "env": ["RTM_API_KEY", "RTM_SHARED_SECRET"],
            "files": ["~/.rtm_token"],
          },
      },
  }
---

# Remember The Milk

`scripts/rtm.py` 是一个用于全面管理 RTM（Remember The Milk）任务的命令行工具。该工具仅依赖 Python 标准库，无需安装任何额外的第三方库（如 pip）。

## 设置

1. 在 [https://www.rememberthemilk.com/services/api/keys.rtm](https://www.rememberthemilk.com/services/api/keys.rtm) 获取 API 密钥。
2. 设置环境变量 `RTM_API_KEY` 和 `RTM_SHARED_SECRET`（通过 OpenClaw 的配置文件 `skills.entries.rtm.env`）。
3. 运行 `scripts/rtm.py auth` 命令进行身份验证，按照提示操作后，授权信息会保存到 `~/.rtm_token` 文件中。

**子代理（Sub-agents）：** 这些子代理的配置信息不会从主配置文件中继承，需要手动传递相应的环境变量：
```bash
RTM_API_KEY=... RTM_SHARED_SECRET=... python3 scripts/rtm.py <command>
```

## 安全性

- **环境变量：** `RTM_API_KEY` 和 `RTM_SHARED_SECRET` 在运行时是必需的。请通过 OpenClaw 的技能配置文件进行设置，切勿硬编码。
- **授权令牌：** 经过身份验证后，令牌会以明文形式保存在 `~/.rtm_token` 文件中。该文件会授予对关联 RTM 账户的完全访问权限。请妥善保护该文件（使用 `chmod 600` 限制文件权限），或在不再需要时立即删除它。
- **网络连接：** 所有的 API 请求仅发送到 `api.rememberthemilk.com` 和 `www.rememberthemilk.com`，不会建立其他外部连接。
- **权限要求：** 身份验证过程需要 `delete` 权限（RTM 的最高权限级别）以支持任务删除操作。如果可能，请使用具有最小权限范围的专用 API 密钥。

## 命令列表

```bash
# Auth (interactive, one-time)
scripts/rtm.py auth

# Lists
scripts/rtm.py lists              # show active lists
scripts/rtm.py lists --all        # include archived

# Tasks
scripts/rtm.py tasks                          # all incomplete
scripts/rtm.py tasks --list LIST_ID           # filter by list
scripts/rtm.py tasks --filter "priority:1"    # RTM filter syntax
scripts/rtm.py tasks --no-notes               # hide notes

# Add (--parse enables Smart Add for dates/tags/priority)
scripts/rtm.py add "Buy groceries" --list LIST_ID --parse
# Smart Add: "Buy milk ^tomorrow #shopping !1" sets due, tag, priority

# Complete / Delete
scripts/rtm.py complete LIST_ID SERIES_ID TASK_ID
scripts/rtm.py delete LIST_ID SERIES_ID TASK_ID

# Priority (1=high, 2=medium, 3=low, N=none)
scripts/rtm.py set-priority LIST_ID SERIES_ID TASK_ID 1

# Due date (natural language parsed by RTM)
scripts/rtm.py set-due LIST_ID SERIES_ID TASK_ID "next friday"

# Move between lists
scripts/rtm.py move FROM_LIST_ID TO_LIST_ID SERIES_ID TASK_ID

# Tags
scripts/rtm.py add-tags LIST_ID SERIES_ID TASK_ID "tag1,tag2"

# Search (RTM filter syntax)
scripts/rtm.py search "tag:work AND status:incomplete"

# Notes
scripts/rtm.py notes-add LIST_ID SERIES_ID TASK_ID "text" --title "Title"
scripts/rtm.py notes-delete NOTE_ID
```

## 任务输出格式

任务输出会包含用于后续写入操作的唯一标识符：
```
  Task Name [P1] (due: 2025-03-15) #tag1 #tag2
    list=12345 series=67890 task=11111
    📝 Note Title (note_id=99999)
    Note body text here
```

## RTM 过滤语法

常用的过滤条件包括：`status:incomplete`（任务未完成）、`priority:1`（任务优先级为 1）、`tag:tagname`（任务标签为指定值）、`due:today`（任务截止日期为今天）、`dueBefore:tomorrow`（任务截止日期为明天）、`list:Inbox`（显示收件箱中的任务）、`isTagged:true`（任务已被标记）、`addedWithin:"1 week"`（任务创建时间在 1 周内）。这些条件可以通过 `AND`、`OR`、`NOT` 等逻辑运算符组合使用。

更多详细信息请参考：[https://www.rememberthemilk.com/help/answers/search/advanced.rtm](https://www.rememberthemilk.com/help/answers/search/advanced.rtm)

## 可靠性

- 所有 API 请求都有 15 秒的超时限制，并支持自动重试（最多尝试 3 次，每次尝试之间有延迟）。
- 对于短暂的网络问题，系统会自动重试；如果遇到永久性的 API 错误，程序会立即终止。
- 写入操作（如添加、完成、删除等）会自动生成任务时间线记录。