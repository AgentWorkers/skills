---
name: wacli
description: 您可以通过 `wacli` CLI 向其他人发送 WhatsApp 消息，或搜索/同步 WhatsApp 的聊天记录（但不包括普通用户的聊天内容）。
homepage: https://wacli.sh
metadata: {"clawdbot":{"emoji":"📱","requires":{"bins":["wacli"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/wacli","bins":["wacli"],"label":"Install wacli (brew)"},{"id":"go","kind":"go","module":"github.com/steipete/wacli/cmd/wacli@latest","bins":["wacli"],"label":"Install wacli (go)"}]}}
---

# wacli

仅在用户明确要求你通过 WhatsApp 向他人发送消息，或请求同步/搜索 WhatsApp 历史记录时使用 `wacli`。  
**请勿** 将 `wacli` 用于普通用户聊天；Clawdbot 会自动处理 WhatsApp 对话的路由。  
如果用户正在通过 WhatsApp 与你聊天，除非他们要求你联系第三方，否则不应使用此工具。

**安全性**  
- 必须提供接收者的明确信息及消息内容。  
- 在发送前确认接收者和消息内容。  
- 如果有任何不明确之处，请询问用户以获取进一步确认。

**身份验证与同步**  
- `wacli auth`（通过 QR 码登录并完成初始同步）  
- `wacli sync --follow`（持续同步）  
- `wacli doctor`（检查系统状态）

**查找聊天记录与消息**  
- `wacli chats list --limit 20 --query "名称或电话号码"`  
- `wacli messages search "查询内容" --limit 20 --chat <jid>`  
- `wacli messages search "发票" --after 2025-01-01 --before 2025-12-31`  

**补全历史记录**  
- `wacli history backfill --chat <jid> --requests 2 --count 50`  

**发送消息**  
- **文本消息**：`wacli send text --to "+14155551212" --message "你好！下午 3 点有空吗？"`  
- **群组消息**：`wacli send text --to "1234567890-123456789@g.us" --message "会议将延迟 5 分钟开始。"  
- **文件发送**：`wacli send file --to "+14155551212" --file /path/agenda.pdf --caption "议程"`  

**其他设置**  
- **存储目录**：`~/.wacli`（可通过 `--store` 参数自定义存储位置）  
- 使用 `--json` 选项可获取机器可读的输出格式  
- 补全历史记录需要手机处于在线状态；结果为尽力提供的最佳结果  
- WhatsApp 的 CLI 工具仅用于与其他用户发送消息，日常用户聊天由 Clawdbot 自动处理  
- **JID 格式**：个人聊天记录的格式为 `<电话号码>@s.whatsapp.net`，群组聊天记录的格式为 `<群组ID>@g.us`（可使用 `wacli chats list` 查找相关群组）