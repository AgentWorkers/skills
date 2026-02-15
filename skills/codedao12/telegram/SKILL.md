---
name: telegram
description: OpenClaw技能：用于设计Telegram机器人的API工作流程以及基于命令的对话系统，支持通过直接的HTTPS请求进行通信（无需使用任何SDK）。
---

# Telegram机器人高级技能

## 目的
本文档提供了一份简洁、面向实际应用的指南，用于通过Telegram机器人API构建机器人工作流程。重点介绍命令交互设计、更新处理方式以及使用纯HTTPS协议的安全操作方法。

## 适用场景
- 需要一个以命令为中心、行为专业的Telegram机器人。
- 需要一个可靠的更新机制（Webhook或轮询）。
- 偏好使用直接的HTTP请求，而非依赖第三方库。

## 不适用场景
- 需要完整的SDK或框架集成。
- 需要在程序内部处理复杂的媒体上传和流媒体传输。

## 快速入门
- 请参阅`references/telegram-bot-api.md`以了解API端点、更新类型和请求格式。
- 请参阅`references/telegram-commands-playbook.md`以了解命令交互设计和消息发送格式。
- 请参阅`references/telegram-update-routing.md`以了解更新数据的标准化处理及路由规则。
- 请参阅`references/telegram-request-templates.md`以了解HTTP请求数据的模板格式。
- 本文档内容较为简略，具体细节请参考相关参考资料。

## 必需输入信息
- 机器人令牌（Bot Token）和基础API地址。
- 更新策略：Webhook或长时间轮询（Long Polling）。
- 命令列表及对话风格。
- 允许的更新类型及请求速率限制策略。

## 预期输出
- 明确的命令设计、更新处理流程及操作检查清单。

## 操作注意事项
- 建议使用规范的命令路径，例如：`/start`、`/help`、`/settings`、`/status`。
- 必须验证所有传入的更新数据及聊天上下文信息。
- 遇到429错误时，请采用重试机制（Backoff）并避免短时间内发送大量消息。

## 安全注意事项
- 绝不要记录机器人令牌（Bot Token）。
- 尽可能使用带有秘密令牌头（Secret Token Header）的Webhook进行通信。