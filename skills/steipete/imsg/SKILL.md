---
name: imsg
description: iMessage/SMS 命令行工具（CLI）：用于查看聊天记录、历史信息、监控聊天状态以及发送消息。
homepage: https://imsg.to
metadata: {"clawdbot":{"emoji":"📨","os":["darwin"],"requires":{"bins":["imsg"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/imsg","bins":["imsg"],"label":"Install imsg (brew)"}]}}
---

# imsg

使用 `imsg` 在 macOS 上读取和发送 Messages.app 的 iMessage/SMS 消息。

**使用要求：**
- Messages.app 已登录。
- 终端具有完整的磁盘访问权限。
- 需要自动化权限以控制 Messages.app（用于发送操作）。

**常用命令：**
- 列出聊天记录：`imsg chats --limit 10 --json`
- 查看聊天历史：`imsg history --chat-id 1 --limit 20 --attachments --json`
- 监控聊天状态：`imsg watch --chat-id 1 --attachments`
- 发送消息：`imsg send --to "+14155551212" --text "hi" --file /path/pic.jpg`

**注意事项：**
- 参数 `--service imessage|sms|auto` 用于指定消息的发送方式（iMessage 或 SMS）。
- 发送前会确认收件人和消息内容。