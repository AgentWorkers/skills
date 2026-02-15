---
name: discord-hub-my
description: OpenClaw 技能用于 Discord 机器人 API 工作流程，涵盖了通过直接 HTTPS 请求进行的交互、命令执行、消息发送以及各种操作。
---

# Discord Bot API高级教程

## 目的  
本教程旨在提供通过REST API和交互功能构建Discord机器人的实用指南，重点介绍专业的命令用户界面设计、安全操作方式以及直接使用HTTPS（无需依赖任何SDK）的方法。

## 适用场景  
- 希望机器人的行为以命令为主，并且交互流程清晰明了。  
- 偏好不依赖任何库的直接HTTP请求方式。  
- 需要一个结构化的Discord API接口映射表。  

## 不适用场景  
- 需要完整的SDK或网关客户端实现。  
- 计划直接上传大文件到Discord。  

## 快速入门  
- 阅读`references/discord-api-overview.md`以了解基础URL、版本信息及API接口结构。  
- 阅读`references/discord-auth-and-tokens.md`以了解令牌类型及安全规范。  
- 阅读`references/discord-interactions.md`以了解交互流程和响应模式。  
- 阅读`references/discord-app-commands.md`以了解斜杠（/）命令、用户相关命令及消息处理方式。  
- 阅读`references/discord-messages-components.md`以了解消息、嵌入内容及组件使用方法。  
- 阅读`references/discord-gateway-webhooks.md`以了解网关与Webhook的优缺点。  
- 阅读`references/discord-rate-limits.md`以了解请求速率限制及头部信息处理规则。  
- 阅读`references/discord-request-templates.md`以了解HTTP请求数据模板。  
- 阅读`references/discord-feature-map.md`以获取完整的API接口列表。  

## 必需输入信息  
- 机器人令牌（Bot Token）和应用程序ID（Application ID）。  
- （如使用交互Webhook）交互端点的公钥（Interaction Endpoint Public Key）。  
- 命令列表及命令的用户界面设计风格。  
- 允许使用的意图（Intents）和事件范围（Event Scope）。  

## 预期输出  
- 一份清晰的机器人工作流程计划、命令设计方案以及操作检查清单。  

## 操作注意事项  
- 建议优先使用交互功能（Interactions）和斜杠命令（Slash Commands），而非前缀解析（Prefix Parsing）方式。  
- 必须验证所有传入的交互请求签名（Interaction Signatures）。  
- 保持请求数据量较小，并尽快响应用户的交互请求。  

## 安全提示  
- 绝不要记录令牌或敏感信息。  
- 请使用最小权限（Least Privilege Principle）进行权限设置。