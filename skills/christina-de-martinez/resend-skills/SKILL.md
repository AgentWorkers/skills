---
name: resend
description: >
  **使用说明：**  
  在处理“Resend Email”平台时，这些路由（routes）用于将邮件发送至特定的子技能（sub-skills），以完成邮件发送、接收、目标受众（audiences）或广播（broadcasts）等操作。
license: MIT
metadata:
    author: resend
    version: "2.5.0"
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

| 功能        | 技能                | 使用场景                |
|------------|------------------|----------------------|
| **发送电子邮件**   | `send-email`         | 发送交易性邮件、通知邮件、批量发送邮件   |
| **接收电子邮件**   | `resend-inbound`        | 处理收到的电子邮件、设置邮件接收的Webhook、处理附件   |
| **AI代理收件箱**   | `agent-email-inbox`       | 为AI代理设置电子邮件接收功能；确保系统能够安全处理不可信的邮件内容（包括防止提示注入攻击） |

## 快速导航

- **需要发送电子邮件？** 使用 `send-email` 功能：
  - 发送单封或批量交易性邮件
  - 添加附件、设置发送时间、使用模板
  - 监控邮件发送状态（是否被退回、成功送达、是否被打开）

- **需要接收电子邮件？** 使用 `resend-inbound` 功能：
  - 设置邮件接收的域名（MX记录）
  - 处理 `email.received` Webhook事件
  - 获取邮件内容和附件
  - 转发收到的邮件

- **为AI代理设置收件箱？** 使用 `agent-email-inbox` 功能：
  - 为Moltbot/Clawdbot等AI代理配置邮件接收功能
  - 使用ngrok或隧道技术进行本地开发
  - 设置安全策略以防止提示注入攻击
  - 设置受信任的发件人列表和内容过滤规则

- **系统自动处理不可信的邮件内容并执行相应操作？** 仍然使用 `agent-email-inbox` 功能：
  - 即使没有AI或大型语言模型（LLM）的参与，任何需要解析外部发件人的自由格式邮件内容并触发操作的系统都需要采取安全措施。不可信的输入可能构成攻击途径。

- **同时需要发送和接收邮件？** 需要同时使用 `resend-inbound` 和 `send-email` 功能：
  - 自动回复、邮件转发等操作都需要这两个功能
  - 先设置邮件接收功能，再执行发送操作
  *注意：批量发送不支持添加附件或设置发送时间；在转发邮件时需要单独发送每封邮件*

- **发送营销邮件或新闻通讯？** 使用 [Resend Broadcasts](https://resend.com/broadcasts)：
  - 上述子功能适用于处理交易性邮件。针对大量订阅者的营销活动（包含退订链接和互动跟踪）应使用 Resend Broadcasts，而非批量发送功能。

## 常见设置

### API密钥（API Key）

将API密钥存储在环境变量中：
```bash
export RESEND_API_KEY=re_xxxxxxxxx
```

### SDK安装（SDK Installation）

请参阅 `send-email` 功能的文档，了解在所有支持的语言中的安装说明。

## 资源（Resources）

- [Resend官方文档](https://resend.com/docs)
- [API参考文档](https://resend.com/docs/api-reference)
- [控制面板](https://resend.com/emails)