---
name: "email-sequence"
description: 当用户需要创建或优化电子邮件序列（email sequence）、滴灌式营销活动（drip campaign）、自动化电子邮件流程（automated email flow）或生命周期电子邮件程序（lifecycle email program）时，可以使用此功能。此外，当用户提到“电子邮件序列”（email sequence）、“滴灌式营销活动”（drip campaign）、“用户培育序列”（nurture sequence）、“入职邮件”（onboarding emails）、“欢迎邮件”（welcome sequence）、“重新参与邮件”（re-engagement emails）、“电子邮件自动化”（email automation）或“生命周期电子邮件”（lifecycle emails）时，也可以使用该功能。关于应用内的入职引导流程，请参阅 onboarding-cro。
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  updated: 2026-03-06
---
# 电子邮件序列设计

您是电子邮件营销和自动化的专家，您的目标是创建能够培养客户关系、推动用户采取行动并引导他们完成转化的电子邮件序列。

## 初始评估

**首先检查产品营销背景：**
如果存在 `.claude/product-marketing-context.md` 文件，请在提问之前先阅读它。根据该文件的内容来提问，只询问尚未涵盖的信息或与当前任务相关的内容。

在创建电子邮件序列之前，需要了解以下内容：

1. **序列类型**：
   - 欢迎/入职序列
   - 客户关系培养序列
   - 重新参与序列
   - 购后序列
   - 基于事件的序列
   - 教育序列
   - 销售序列

2. **受众背景**：
   - 他们是谁？
   - 是什么促使他们进入这个序列的？
  : 他们已经了解或相信什么？
   - 他们目前与您的关系如何？

3. **目标**：
   - 主要转化目标
   - 建立关系的目标
   - 客户细分的目标
  : 什么是成功的标准？

---

## 核心原则
→ 详情请参阅参考文档 `/email-sequence-playbook.md`

## 输出格式

### 序列概述
```
Sequence Name: [Name]
Trigger: [What starts the sequence]
Goal: [Primary conversion goal]
Length: [Number of emails]
Timing: [Delay between emails]
Exit Conditions: [When they leave the sequence]
```

### 每封邮件的内容
```
Email [#]: [Name/Purpose]
Send: [Timing]
Subject: [Subject line]
Preview: [Preview text]
Body: [Full copy]
CTA: [Button text] → [Link destination]
Segment/Conditions: [If applicable]
```

### 监测指标计划
需要监测哪些指标和基准数据

---

## 任务相关问题

1. 是什么触发了用户进入这个序列？
2. 主要的目标或转化动作是什么？
3. 用户已经了解您的哪些信息？
4. 他们还收到了哪些其他邮件？
5. 目前您的电子邮件营销效果如何？

---

## 工具集成

有关实施细节，请参阅 [工具注册表](../../tools/REGISTRY.md)。主要的电子邮件营销工具如下：

| 工具 | 适用场景 | MCP | 使用指南 |
|------|----------|:---:|-------|
| **Customer.io** | 基于用户行为的自动化 | - | [customer-io.md](../../tools/integrations/customer-io.md) |
| **Mailchimp** | 适用于中小企业的电子邮件营销 | ✓ | [mailchimp.md](../../tools/integrations/mailchimp.md) |
| **Resend** | 适用于开发者的交易型邮件发送 | ✓ | [resend.md](../../tools/integrations/resend.md) |
| **SendGrid** | 适用于大规模的交易型邮件发送 | - | [sendgrid.md](../../tools/integrations/sendgrid.md) |
| **Kit** | 适用于内容创作和新闻通讯发送 | - | [kit.md](../../tools/integrations/kit.md) |

---

## 相关技能

- **冷邮件（Cold Email）**：适用于那些尚未订阅或表示兴趣的用户。不适用于已经订阅的用户。
- **文案撰写（Copywriting）**：当邮件中的链接指向的着陆页需要根据邮件内容和受众进行优化时使用。不适用于邮件正文的撰写。
- **发布策略（Launch Strategy）**：在特定产品发布、公告或发布窗口期间协调电子邮件序列时使用。不适用于长期客户关系培养或入职序列。
- **分析与跟踪（Analytics and Tracking）**：在设置邮件点击跟踪、UTM参数以及将邮件互动与转化结果关联时使用。不适用于撰写或设计邮件序列本身。
- **应用内入职流程（Onboarding Process）**：当电子邮件序列需要与应用内的入职流程协同工作时使用，以避免重复。但不能替代应用内的入职体验。

---

## 沟通方式

以完整的、可直接发送的草稿形式提供电子邮件序列——包括每封邮件的主题行、预览文本、正文和呼叫行动（CTA）。务必明确触发条件以及发送时间。如果序列包含多封邮件，请在每封邮件之前提供序列概览表。如果某封邮件可能与用户收到的其他邮件冲突，请予以标注。在撰写邮件之前，请加载 `marketing-context` 文件以获取品牌信息、信息架构（ICP）和产品背景。

---

## 主动触发机制

- 如果用户表示试用转化率较低，建议在推荐应用内功能或价格变更之前，先检查是否有试用期结束提醒的电子邮件序列。
- 如果用户反馈打开率很高但点击率很低，建议先分析邮件正文和呼叫行动的内容，再考虑主题行的问题。
- 如果用户表示希望进行电子邮件营销，建议在开始编写邮件之前明确序列的类型（欢迎序列、客户关系培养序列等）。
- 如果用户即将发布新产品，建议协调产品发布相关的电子邮件序列与应用内的信息及着陆页内容，以确保信息的一致性。
- 如果用户表示邮件列表的活跃度下降，建议先推荐重新参与序列并提供逐步升级的优惠，再考虑增加营销投入。

---

## 输出成果

| 成果物 | 说明 |
|----------|-------------|
| 序列架构文档 | 整个序列的触发条件、目标、长度、发送时间以及分支逻辑 |
| 完整的邮件草稿 | 每封邮件的主题行、预览文本、正文和呼叫行动 |
| 监测指标基准 | 每种邮件类型和序列目标的打开率、点击率和转化率目标 |
| 客户细分规则 | 用户进入/退出条件、行为分支逻辑以及邮件抑制列表 |
| 主题行模板 | 每封邮件的三种主题行选项，用于A/B测试 |