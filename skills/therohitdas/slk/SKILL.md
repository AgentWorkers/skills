---
name: slack-personal
description: 通过 `slk CLI` 来读取、发送、搜索和管理 Slack 消息及私信（DMs）。当用户需要查看 Slack 消息、阅读频道内容或私信、发送 Slack 消息、在 Slack 中搜索信息、查看未读消息、管理草稿、查看已保存的内容，或与 Slack 工作空间进行交互时，可以使用该工具。此外，它还用于执行定期的 Slack 状态检查（即“heartbeat”检查）。触发条件包括：“check slack”、“any slack messages”、“send on slack”、“slack unreads”、“search slack”、“slack threads”、“draft on slack”、“read slack dms”以及 “message on slack”。
homepage: https://www.npmjs.com/package/slkcli
user-invocable: true
metadata: {"openclaw":{"emoji":"💬","requires":{"bins":["slk"]},"install":[{"id":"npm","kind":"node","package":"slkcli","bins":["slk"],"label":"Install slk (npm)"}],"os":["darwin"]}}
---

# slk — Slack 命令行工具（Slack CLI）

这是一个基于会话的 Slack 命令行工具，专为 macOS 设计。它能够自动从 Slack 桌面应用中进行身份验证，无需使用令牌或 OAuth，也无需安装任何额外的应用程序。该工具会以你的用户身份（`xoxc-` 会话令牌）执行操作。

## 命令

```bash
# Auth
slk auth                              # Test authentication, show user/team

# Read
slk channels                          # List channels (alias: ch)
slk dms                               # List DM conversations with IDs (alias: dm)
slk read <channel> [count]            # Read recent messages, default 20 (alias: r)
slk read @username [count]            # Read DMs by username
slk read <channel> --threads          # Auto-expand all threads
slk read <channel> --from 2026-02-01  # Date range filter
slk thread <channel> <ts> [count]     # Read thread replies, default 50 (alias: t)
slk search <query> [count]            # Search messages across workspace
slk users                             # List workspace users (alias: u)

# Activity
slk activity                          # All channels with unread/mention counts (alias: a)
slk unread                            # Only unreads, excludes muted (alias: ur)
slk starred                           # VIP users + starred items (alias: star)
slk saved [count] [--all]             # Saved for later items (alias: sv)
slk pins <channel>                    # Pinned items in a channel (alias: pin)

# Write
slk send <channel> <message>          # Send a message (alias: s)
slk react <channel> <ts> <emoji>      # React to a message

# Drafts (synced to Slack editor UI)
slk draft <channel> <message>         # Draft a channel message
slk draft thread <ch> <ts> <message>  # Draft a thread reply
slk draft user <user_id> <message>    # Draft a DM
slk drafts                            # List active drafts
slk draft drop <draft_id>             # Delete a draft
```

`channel` 参数可以接受以下值：
- 名称（例如：`general`）
- ID（例如：`C08A8AQ2AFP`）
- `@username`（用于发送私信）
- 用户 ID（例如：`U07RQTFCLUC`）

## 身份验证

slk 会自动从 Slack 桌面应用的 LevelDB 数据库中获取会话令牌，并从 macOS 的 Keychain 中解密相应的 cookie 文件来完成身份验证。

**首次使用时的提示：** macOS 系统会弹出一个 Keychain 对话框，询问是否允许访问 “Slack 安全存储”：
- **允许**：仅允许一次访问，下次使用时会再次提示；
- **始终允许**：永久允许访问，之后不会再提示；
- **拒绝**：将阻止访问，slk 无法完成身份验证。

**令牌缓存：** 令牌信息存储在 `~/.local/slk/token-cache.json` 文件中。当身份验证失败（例如令牌过期或 Slack 用户登出时），slk 会自动重新获取令牌。

**注意：** 如果 Slack 桌面应用未安装或未登录，slk 无法正常工作。不过，即使令牌已缓存，Slack 桌面应用也可以在后台运行。

## 读取聊天记录

读取聊天记录时需要 Slack 的时间戳。可以使用 `--ts` 参数来获取时间戳，然后使用 `slk read <channel>` 命令来读取指定频道的聊天记录。

## 代理工作流程示例：

- **检查未读消息**：`slk unread` → `slk read <channel>`（用于查看需要处理的频道中的未读消息）；
- **保存聊天记录**：当用户将聊天记录标记为 “稍后处理” 时，代理会使用 `slk saved` 命令保存这些记录；
- **每日频道摘要**：`slk read <channel> 100`（遍历多个频道，提取决策、待办事项等关键信息）→ `slk send daily-digest "📋 ..."`（发送每日摘要）；
- **每周私信汇总**：`slk read @boss 200 --from 2026-02-01 --threads`（提取指定用户的私信中的待办事项和决策）；
- **监控特定聊天记录**：监视特定聊天记录中的新回复（例如事故报告、代码审查结果等）；
- **草稿发送**：`slk draft <channel> "..."`（将草稿发送到 Slack 的编辑器界面供用户审核）；
- **基于搜索的上下文获取**：`slk search "deployment process"` 或 `slk pins <channel>`（在回答问题前获取相关上下文信息）。

## 限制：

- **仅支持 macOS**：该工具依赖于 macOS 的 Keychain 和 Electron 技术；
- **基于会话的身份验证**：slk 会以你的用户身份执行操作，请注意发送的内容；
- 如果 Slack 当前正在处理相同的对话，`slk draft` 命令可能会失败（因为存在冲突）；
- 会话令牌会在用户登出后失效，请确保 Slack 桌面应用保持运行状态，或者使用缓存的令牌。

## 缺失的功能和问题：

如需提交 PR 或报告问题，请访问：https://github.com/therohitdas/slkcli