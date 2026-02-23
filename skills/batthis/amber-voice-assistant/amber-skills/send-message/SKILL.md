---
name: send-message
version: 1.0.0
description: "为操作员留言——该留言会保存在通话记录中，并通过操作员偏好的消息传递渠道发送给操作员。"
metadata: {"amber": {"capabilities": ["act"], "confirmation_required": true, "confirmation_prompt": "Would you like me to leave that message?", "timeout_ms": 5000, "permissions": {"local_binaries": [], "telegram": true, "openclaw_action": true, "network": false}, "function_schema": {"name": "send_message", "description": "Leave a message for the operator. The message will be saved to the call log and sent to the operator via their messaging channel. IMPORTANT: Always confirm with the caller before calling this function — ask 'Would you like me to leave that message?' and only proceed after they confirm.", "parameters": {"type": "object", "properties": {"message": {"type": "string", "description": "The caller's message to leave for the operator"}, "caller_name": {"type": "string", "description": "The caller's name if they provided it"}, "callback_number": {"type": "string", "description": "A callback number if the caller provided one"}, "urgency": {"type": "string", "enum": ["normal", "urgent"], "description": "Whether the caller indicated this is urgent"}}, "required": ["message"]}}}}
---
# 发送消息

该功能允许来电者给客服人员留言。该功能实现了电话助手中常见的“留言”操作模式。

## 流程

1. 来电者表示他们想要留言。
2. Amber 会确认：“您希望我帮您留言吗？”
3. 确认后，留言会：
   - **首先**被保存到通话记录中（作为审计痕迹）；
   - **然后**通过客服人员配置的消息传递渠道发送给他们。

## 安全性

- 收件人由客服人员的配置决定，绝不会根据来电者的输入来决定。
- 数据模型中没有任何参数用于指定消息的接收者或发送渠道。
- 在发送留言之前必须进行确认（通过大语言模型（LLM）的功能描述来实现）。
- 消息内容会经过清洗处理（限制最长长度，并删除特殊字符）。

## 传递失败处理

- 如果消息传递失败，通话记录会被标记为 `delivery_failed`。
- 客服人员的助手可以在定期检查中查看未送达的留言。
- Amber 会告诉来电者：“我已经收到了您的留言”，但不会承诺具体的传递渠道。