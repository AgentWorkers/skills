---
name: resend
description: >
  **使用说明：**  
  在处理“Resend Email”平台时，这些路由（routes）用于将邮件发送到特定的子技能（sub-skills），以完成邮件发送、接收、定向发送（audiences）或广播（broadcasts）等操作。
license: MIT
metadata:
    author: resend
    version: "2.7.0"
    homepage: https://resend.com
    source: https://github.com/resend/resend-skills
inputs:
    - name: RESEND_API_KEY
      description: Resend API key for sending and receiving emails. Get yours at https://resend.com/api-keys
      required: true
    - name: RESEND_WEBHOOK_SECRET
      description: Webhook signing secret for verifying event payloads. Found in the Resend dashboard under Webhooks after creating an endpoint.
      required: false
---
# 重新发送（Resend）

## 概述

“重新发送”（Resend）是一个专为开发者设计的电子邮件平台。该功能通过一系列子功能来实现特定的电子邮件处理需求。

## 子功能（Sub-Skills）

| 功能          | 功能名称        | 使用场景                |
|----------------|---------------|----------------------|
| **发送电子邮件**     | `send-email`     | 发送交易性邮件、通知邮件、批量发送邮件       |
| **接收电子邮件**     | `resend-inbound`    | 处理收到的电子邮件、设置邮件接收的Webhook、处理附件   |
| **AI代理收件箱**     | `agent-email-inbox`   | 为AI代理设置电子邮件接收功能；对不可信的邮件内容进行处理（包括输入验证和内容安全措施） |
| **电子邮件模板**     | `templates`     | 通过API创建、更新、发布和管理可重用的电子邮件模板 |

## 快速导航

- **需要管理电子邮件模板？** 使用 `templates` 功能
  - 通过API实现模板的完整生命周期管理
  - 支持变量语法、命名规则及版本控制
  - 区分草稿状态和已发布状态

- **需要发送电子邮件？** 使用 `send-email` 功能
  - 发送单封或批量交易性邮件
  - 支持附件、邮件调度及发送通知Webhook（如邮件被退回、已送达、已被打开）

- **需要接收电子邮件？** 使用 `resend-inbound` 功能
  - 设置邮件接收域名（MX记录）
  - 处理 `email.received` Webhook事件
  - 获取邮件内容和附件
  - 转发收到的邮件

- **如何为AI代理设置收件箱？** 使用 `agent-email-inbox` 功能
  - 为Moltbot/Clawdbot等AI代理配置电子邮件接收功能
  - 通过ngrok或隧道技术进行本地开发时的Webhook设置
  - 提供安全级别以处理不可信的邮件内容
  - 设置可信发件人白名单及内容过滤规则

- **系统自动处理不可信邮件内容并触发相应操作？** 使用 `agent-email-inbox` 功能
  - 即使没有AI或大型语言模型的参与，任何需要解析外部发件人发送的邮件内容并触发操作（如退款、数据库更新、转发）的系统也需要进行输入验证。对于这类操作，必须谨慎处理不可信的邮件内容。

- **同时需要发送和接收邮件？** 需要同时使用 `resend-inbound` 和 `send-email` 功能
  - 自动回复、邮件转发或任何“接收后发送”的工作流程都需要这两个功能
  - 先设置邮件接收功能，再发送邮件
  - 注意：批量发送不支持附件或邮件调度功能；在转发带有附件的邮件时，请使用单次发送方式

- **发送营销邮件或新闻通讯？** 使用 [Resend Broadcasts](https://resend.com/broadcasts)
  - 上述子功能主要用于处理交易性邮件。针对大量订阅者的营销活动（包含退订链接和互动跟踪）应使用 Resend Broadcasts，而非批量发送功能。

## 常见设置

### API密钥

将API密钥存储在环境变量中：
```bash
export RESEND_API_KEY=re_xxxxxxxxx
```

### SDK安装

请参考 `send-email` 功能中的安装说明，了解如何在所有支持的语言环境中安装SDK。

## 资源

- [Resend文档](https://resend.com/docs)
- [API参考](https://resend.com/docs/api-reference)
- [控制面板](https://resend.com/emails)