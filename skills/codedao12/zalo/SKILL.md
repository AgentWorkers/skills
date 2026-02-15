---
name: zalo
description: OpenClaw技能：用于Zalo Bot API工作流程（包括获取机器人令牌），并提供关于非官方个人自动化工具的参考指南。
---

# Zalo机器人技能（高级版）

## 目的  
本文档为基于Zalo机器人API（基于令牌的方式）的工作流程提供实用指导，并为非官方的个人自动化工具设立了单独的、明确标记的分支。

## 适用场景  
- 您正在使用Zalo机器人平台及相应的机器人令牌机制。  
- 需要处理Webhook请求或长轮询（long-polling）逻辑。  
- 希望获得专业的对话用户体验指导。  

## 不适用场景  
- 需要官方支持的、针对个人账户的自动化功能。  
- 需要实现富媒体流传输或高级文件处理功能。  

## 快速入门  
- 请阅读`references/zalo-bot-overview.md`以了解平台范围和限制。  
- 请阅读`references/zalo-bot-token-and-setup.md`以了解令牌设置及连接流程。  
- 请阅读`references/zalo-bot-messaging-capabilities.md`以了解机器人功能清单。  
- 请阅读`references/zalo-bot-ux-playbook.md`以了解用户体验和对话模式。  
- 请阅读`references/zalo-bot-webhook-routing.md`以了解Webhook请求的处理方式。  
- 请阅读`references/zalo-personal-zca-js.md`以了解非官方的个人账户自动化相关内容。  
- 请阅读`references/zalo-n8n-automation.md`以获取自动化相关的注意事项和警告。  

## 必需输入  
- 机器人令牌（Bot Token）和机器人配置信息。  
- 目标工作流程（通知、支持、广播等）。  
- 数据传输方式（Webhook或长轮询）。  

## 预期输出  
- 明确的机器人工作流程方案、方法清单以及操作规范。  

## 操作注意事项  
- 验证传入事件并确保安全地处理重试请求。  
- 保持回复简洁；对发出的消息实施速率限制。  
- 对于任何自动化流程，建议使用明确的允许列表（allowlist）。  

## 安全提示  
- 绝不要记录令牌或凭据信息。  
- 将所有状态文件和cookie视为机密信息进行严格管理。