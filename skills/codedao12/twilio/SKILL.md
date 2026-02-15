---
name: twilio
description: OpenClaw技能：支持Twilio的多种API功能，包括消息发送、WhatsApp通信、语音通话、对话管理、用户验证，以及Studio、Lookup、Proxy、Sync、TaskRouter等服务。此外，还支持Segment/Engage功能，用于用户分组与互动管理。
---

# Twilio API 技能（高级）

## 目的  
提供一份面向生产环境的指南，介绍如何使用直接的 HTTPS 请求来处理 Twilio API 的各种消息传递和通信渠道相关的工作流程。

## 适用场景  
- 需要使用 SMS/MMS、WhatsApp、语音服务或进行用户验证（Verify）的场景。  
- 希望实现可靠的 Webhook 处理机制和操作安全保障。  
- 更倾向于使用直接的 HTTP 请求而非 SDK。  

## 不适用场景  
- 需要完整的 SDK 或复杂的多服务协调机制。  
- 需要对多个短信服务提供商（ESP）进行高级的营销活动管理。  

## 快速入门  
- 阅读 `references/twilio-api-overview.md` 以了解核心接口和基础端点。  
- 阅读 `references/twilio-auth-and-webhooks.md` 以了解身份验证和 Webhook 验证的相关内容。  
- 阅读 `references/twilio-messaging-sms-mms.md` 以了解 SMS/MMS 的工作流程。  
- 阅读 `references/twilio-whatsapp.md` 以了解 WhatsApp 消息传递的详细信息。  
- 阅读 `references/twilio-voice.md` 以了解电话/IVR 的基础知识。  
- 阅读 `references/twilio-conversations.md` 以了解多渠道会话管理。  
- 阅读 `references/twilio-verify.md` 以了解 OTP/验证流程。  
- 阅读 `references/twilio-sendgrid.md` 以了解电子邮件发送功能。  
- 阅读 `references/twilio-studio.md` 以了解低代码流程编排。  
- 阅读 `references/twilio-lookup.md` 以了解电话相关信息。  
- 阅读 `references/twilio-proxy.md` 以了解加密通信功能。  
- 阅读 `references/twilio-sync.md` 以了解实时状态管理。  
- 阅读 `references/twilio-taskrouter.md` 以了解请求路由和队列管理。  
- 阅读 `references/twilio-segment-engage.md` 以了解客户数据平台（CDP）和受众激活功能。  

## 必需输入  
- 账户 SID 和认证令牌（或 API 密钥/Secret）。  
- 发件人身份（电话号码、消息服务提供商、WhatsApp 发件人）。  
- 用于回调的 Webhook URL。  
- 合规性要求（如用户同意、地区法规）。  

## 预期输出  
- 明确的工作流程计划、方法检查清单以及操作安全准则。  

## 操作注意事项  
- 对每个传入的请求都要验证 Webhook 签名。  
- 注意出站请求的速率限制，并确保安全地重试请求。  
- 将敏感信息存储在安全库中并定期更换。  

## 安全提示  
- 绝不要记录任何认证凭证。  
- 尽可能使用权限最小的 API 密钥。