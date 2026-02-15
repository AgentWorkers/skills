---
name: messenger
description: OpenClaw技能适用于Facebook Messenger平台的工作流程，包括发送消息、使用Webhooks以及通过直接的HTTPS请求操作页面收件箱等功能。
---

# Facebook Messenger API 技能（高级）

## 目的
提供一份面向生产环境的指南，介绍如何在 Messenger 平台上发送消息、处理 Webhook 以及通过直接 HTTPS 调用管理页面消息的功能。

## 适用场景
- 需要在 Facebook Messenger 中实现类似机器人的消息交互功能。
- 希望 Webhook 处理过程简洁明了，且消息用户体验良好。
- 更倾向于使用直接 HTTP 请求而非 SDK。

## 不适用场景
- 需要使用高级的 Graph API 广告或营销功能。
- 必须使用复杂的基于浏览器的 OAuth 流程。

## 快速入门
- 阅读 `references/messenger-api-overview.md` 以了解基础 URL 和核心对象映射。
- 阅读 `references/webhooks.md` 以了解验证和签名验证的流程。
- 阅读 `references/messaging.md` 以了解发送消息的 API 字段和消息类型。
- 阅读 `references/permissions-and-tokens.md` 以了解令牌获取流程和所需权限。
- 阅读 `references/request-templates.md` 以了解具体的 HTTP 请求格式。
- 阅读 `references/conversation-patterns.md` 以了解用户体验流程（如开始对话、菜单操作、备用方案等）。
- 阅读 `references/webhook-event-map.md` 以了解事件类型和路由规则。

## 所需输入
- Facebook 应用程序 ID 和应用程序密钥。
- 页面 ID 及页面访问令牌。
- Webhook URL 及验证令牌。
- 消息交互方式及允许的操作类型。

## 预期输出
- 一份清晰的消息交互工作流程计划、权限检查清单以及操作规范。

## 操作注意事项
- 对所有 Webhook 事件进行签名验证。
- 回复要简洁明了，并及时给予回应。
- 遵循速率限制策略，并在请求失败时采用重试机制。

## 安全注意事项
- 绝不要记录令牌或应用程序密钥。
- 仅使用最低权限级别的访问权限。