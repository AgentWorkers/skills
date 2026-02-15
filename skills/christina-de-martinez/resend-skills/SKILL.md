---
name: resend
description: **使用说明：**  
在处理“Resend Email”平台时，这些路由（routes）用于将邮件发送给特定的子技能（sub-skills），以完成发送、接收邮件、管理受众（audiences）或进行广播（broadcasts）等操作。
license: MIT
metadata:
    author: resend
    version: "2.2.0"
---

# 重新发送邮件（Resend Email）

## 概述

“重新发送邮件”（Resend）是一个专为开发者设计的邮件处理平台。该功能通过一系列子功能来实现具体的邮件处理需求。

## 子功能（Sub-Skills）

| 功能          | 技能名称        | 使用场景                |
|----------------|--------------|----------------------|
| **发送邮件**      | `send-email`    | 发送事务性邮件、通知邮件、批量发送邮件   |
| **接收邮件**      | `resend-inbound`  | 处理收到的邮件、设置邮件接收的Webhook、处理附件 |
| **AI代理收件箱**    | `moltbot`     | 为AI代理设置邮件接收功能，并提供防止提示注入攻击的安全措施 |

## 快速使用指南

**需要发送邮件？** 使用 `send-email` 功能：
- 发送单封或批量事务性邮件
- 添加附件、设置发送时间、使用模板
- 监控邮件发送状态（是否被退回、成功送达、是否被打开）

**需要接收邮件？** 使用 `resend-inbound` 功能：
- 设置邮件接收的域名（MX记录）
- 处理 `email.received` Webhook事件
- 获取邮件内容和附件
- 转发收到的邮件

**如何为AI代理设置收件箱？** 使用 `moltbot` 功能：
- 为Moltbot/Clawdbot等AI代理配置邮件接收功能
- 通过ngrok或隧道技术进行本地开发
- 设置安全机制以防止提示注入攻击
- 设置可信发件人列表和内容过滤规则

## 常见设置

### API密钥（API Key）

请将API密钥存储在环境变量中：
```bash
export RESEND_API_KEY=re_xxxxxxxxx
```

### SDK安装（SDK Installation）

有关所有支持语言的SDK安装说明，请参阅 `send-email` 功能的相关文档。

## 资源（Resources）

- [Resend官方文档](https://resend.com/docs)
- [API参考文档](https://resend.com/docs/api-reference)
- [控制面板](https://resend.com/emails)