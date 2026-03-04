---
name: send-message
version: 1.0.0
description: "为操作员留言——留言内容会保存在通话记录中，并通过操作员偏好的消息传递渠道发送给操作员。"
metadata: {"amber": {"capabilities": ["act"], "confirmation_required": true, "confirmation_prompt": "Would you like me to leave that message?", "timeout_ms": 5000, "permissions": {"local_binaries": [], "telegram": true, "openclaw_action": true, "network": false}, "function_schema": {"name": "send_message", "description": "Leave a message for the operator. The message will be saved to the call log and sent to the operator via their messaging channel. IMPORTANT: Always confirm with the caller before calling this function — ask 'Would you like me to leave that message?' and only proceed after they confirm.", "parameters": {"type": "object", "properties": {"message": {"type": "string", "description": "The caller's message to leave for the operator", "maxLength": 1000}, "caller_name": {"type": "string", "description": "The caller's name if they provided it", "maxLength": 100}, "callback_number": {"type": "string", "description": "A callback number if the caller provided one", "maxLength": 30}, "urgency": {"type": "string", "enum": ["normal", "urgent"], "description": "Whether the caller indicated this is urgent"}, "confirmed": {"type": "boolean", "description": "Must be true — only set after the caller has explicitly confirmed their message and given permission to send it. The router will reject this call if confirmed is not true."}}, "required": ["message", "confirmed"]}}}}
---
# 发送消息

该功能允许来电者给客服人员留下消息。该功能实现了基于电话的助手系统中常见的“留言”功能。

## 流程

1. 来电者表示他们想要留言。
2. Amber 会确认：“您希望我帮您留言吗？”
3. 在得到确认后，消息会：
   - **始终** 首先被保存到通话记录中（作为审计追踪）
   - **随后** 通过客服人员配置的消息渠道发送给他们。

## 安全性

- 收件人由客服人员的配置决定，绝不会根据来电者的输入来设置。
- 数据模型中没有任何参数用于指定消息的接收者。
- 在发送消息之前需要得到确认（这一机制在路由器层面通过编程实现；路由器会检查 `params.confirmed === true` 来确保消息已确认；虽然有大型语言模型的提示引导，但这并非唯一的验证手段）。
- 消息内容会经过清理处理（限制最大长度并去除特殊字符）。

## 交付失败处理

- 如果消息传递失败，通话记录会标记为 `delivery_failed`。
- 客服人员的助手可以在定期检查中查看未送达的消息。
- Amber 会告诉来电者：“我已经收到了您的消息”，但不会承诺具体的消息传递渠道。