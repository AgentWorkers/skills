---
name: email-best-practices
description: **使用场景：**  
- 在构建电子邮件功能时；  
- 当邮件被归类为垃圾邮件（spam）时；  
- 面对高退信率（high bounce rates）时；  
- 设置 SPF/DKIM/DMARC 认证机制时；  
- 实现邮件捕获（email capture）功能时；  
- 确保合规性（如 CAN-SPAM、GDPR、CASL 等法规要求）时；  
- 处理 Webhook 事件时；  
- 实现重试逻辑（retry logic）时；  
- 判断邮件属于交易类（transactional）还是营销类（marketing）时。
---

# 电子邮件最佳实践

本指南旨在帮助您构建可交付、符合规范且用户友好的电子邮件系统。

## 架构概述

```
[User] → [Email Form] → [Validation] → [Double Opt-In]
                                              ↓
                                    [Consent Recorded]
                                              ↓
[Suppression Check] ←──────────────[Ready to Send]
        ↓
[Idempotent Send + Retry] ──────→ [Email API]
                                       ↓
                              [Webhook Events]
                                       ↓
              ┌────────┬────────┬─────────────┐
              ↓        ↓        ↓             ↓
         Delivered  Bounced  Complained  Opened/Clicked
                       ↓        ↓
              [Suppression List Updated]
                       ↓
              [List Hygiene Jobs]
```

## 快速参考

| 需要完成的任务 | 参考资料 |
|------------|-----|
| 设置 SPF/DKIM/DMARC，解决垃圾邮件问题 | [邮件送达性](./resources/deliverability.md) |
| 创建密码重置、一次性密码（OTP）及确认邮件 | [交易类邮件](./resources/transactional-emails.md) |
| 确定应用程序需要发送的邮件类型 | [交易类邮件目录](./resources/transactional-email-catalog.md) |
| 创建新闻通讯注册功能并验证用户邮箱地址 | [邮件捕获](./resources/email-capture.md) |
| 发送新闻通讯和促销邮件 | [营销邮件](./resources/marketing-emails.md) |
| 确保符合 CAN-SPAM/GDPR/CASL 法规要求 | [合规性](./resources/compliance.md) |
| 判断邮件类型（交易类邮件还是营销邮件） | [邮件类型](./resources/email-types.md) |
| 处理重试、幂等性及错误 | [发送可靠性](./resources/sending-reliability.md) |
| 处理邮件送达事件并设置 Webhook | [Webhook 与事件](./resources/webhooks-events.md) |
| 管理邮件退回、用户投诉及邮件抑制机制 | [列表管理](./resources/list-management.md) |

## 从这里开始

**新开发的应用程序？**
首先参考 [交易类邮件目录](./resources/transactional-email-catalog.md)，确定应用程序需要发送的邮件类型（如密码重置、验证邮件等），然后设置 [邮件送达性](./resources/deliverability.md)（包括 DNS 认证），再发送第一封邮件。

**遇到垃圾邮件问题？**
请先查看 [邮件送达性](./resources/deliverability.md)——认证问题是导致邮件被拒绝的最常见原因。Gmail 和 Yahoo 会拒绝未经认证的邮件。

**发送营销邮件？**
按照以下步骤操作：[邮件捕获](./resources/email-capture.md)（收集用户同意信息）→ [合规性](./resources/compliance.md)（满足法律要求）→ [营销邮件](./resources/marketing-emails.md)（最佳实践）。

**准备投入生产环境？**
提升邮件发送的可靠性：[发送可靠性](./resources/sending-reliability.md)（实现重试和幂等性）→ [Webhook 与事件](./resources/webhooks-events.md)（跟踪邮件送达情况）→ [列表管理](./resources/list-management.md)（处理邮件退回问题）。