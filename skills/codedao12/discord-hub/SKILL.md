---
name: discord-hub
description: OpenClaw 技能用于 Discord 机器人 API 工作流程，涵盖通过直接 HTTPS 请求进行的交互、命令执行、消息发送以及各种操作。
---

# Discord Bot API技能（高级）

## 目的
本文档提供了一套面向生产环境的指南，用于通过REST API和交互功能构建Discord机器人。重点介绍专业的命令用户界面（UX）、安全的操作方式以及直接使用HTTPS（无需依赖任何SDK）。

## 适用场景
- 希望机器人以命令驱动的方式运行，并且交互流程清晰明了。
- 偏好直接使用HTTP请求，而不依赖任何第三方库。
- 需要一个结构化的Discord API接口映射。

## 不适用场景
- 需要完整的SDK或网关客户端实现。
- 计划直接上传大型媒体文件。

## 快速入门
- 请阅读`references/discord-api-overview.md`以了解基础URL、版本控制和接口映射。
- 请阅读`references/discord-auth-and-tokens.md`以了解令牌类型和安全限制。
- 请阅读`references/discord-interactions.md`以了解交互生命周期和响应模式。
- 请阅读`references/discord-app-commands.md`以了解斜杠命令（slash commands）、用户命令和消息命令。
- 请阅读`references/discord-messages-components.md`以了解消息、嵌入内容（embeds）和组件（components）的相关信息。
- 请阅读`references/discord-gateway-webhooks.md`以了解网关（gateway）与Webhook之间的区别。
- 请阅读`references/discord-rate-limits.md`以了解请求速率限制和基于HTTP头部的处理方式。
- 请阅读`references/discord-request-templates.md`以了解HTTP请求体的模板格式。
- 请阅读`references/discord-feature-map.md`以获取完整的API接口列表。

## 必需输入
- 机器人令牌（bot token）和应用程序ID（application ID）。
- 如果使用交互Webhook（interaction webhooks），则需要交互端点的公钥（interaction endpoint public key）。
- 命令列表（command list）和命令的用户界面风格（UX tone）。
- 允许的意图（allowed intents）和事件范围（event scope）。

## 预期输出
- 一份清晰的机器人工作流程计划、命令设计方案以及操作检查清单。

## 操作注意事项
- 相对于前缀解析（prefix parsing），优先使用交互功能（interactions）和斜杠命令（slash commands）。
- 必须始终验证传入的交互签名（interaction signatures）。
- 保持请求体（payloads）的大小较小，并快速响应用户的交互请求。

## 安全注意事项
- 绝不要记录令牌或敏感信息。
- 请使用最小权限（least-privilege）和相应的权限范围（scopes）进行操作。