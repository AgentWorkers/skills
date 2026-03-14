---
name: cold-email-engine
description: 自动化冷电话外联系统，具备潜在客户信息丰富化功能、个性化模板、逐步发送邮件序列（drip sequences）以及符合反垃圾邮件法规（CAN-SPAM）的要求。适用于构建外向销售流程、寻找潜在客户、自动化邮件营销活动、补充潜在客户的联系信息、设置逐步跟进邮件机制，或大规模管理冷电话外联工作。支持与 Resend、SendGrid 或任何 SMTP 服务提供商集成使用。
---
# 冷邮件发送系统 (Cold Email Engine)

自动化的外发邮件流程：寻找潜在客户 → 丰富联系人信息 → 发送个性化邮件 → 进行定时跟进。

## 流程 (Pipeline)

1. **获取潜在客户** — 从 CSV 文件、Google Sheets、API 数据抓取或手动输入中获取。
2. **丰富联系人信息** — 通过网站抓取、Hunter.io 或 Apollo 工具获取电子邮件地址。
3. **个性化邮件内容** — 在邮件模板中使用变量（如 `{name}`、`{company}`、`{pain_point}`）进行个性化处理。
4. **发送邮件** — 可通过 Resend、SendGrid 或原始 SMTP 协议发送，同时支持发送频率限制。
5. **定时跟进** — 在发送后的第 3 天和第 7 天自动发送跟进邮件。
6. **跟踪发送结果** — 将所有发送记录、邮件退回情况以及客户回复记录保存到 CSV 文件或 Google Sheets 中。

## 必备条件

- **邮件服务提供商的 API 密钥** — 用于 Resend（`RESEND_API_KEY`）、SendGrid 或 SMTP 服务。
- **经过验证的发送域名** — 配置了 SPF、DKIM 和 DMARC 等安全机制。
- **潜在客户来源** — 可以是 CSV 文件、Google Sheets ID 或 API 端点。

## 快速入门

```bash
# Set environment
export RESEND_API_KEY=your_key

# Send from CSV
node scripts/cold-email-engine.js --source leads.csv --template templates/default.txt --from "Name <hello@yourdomain.com>"

# Dry run (no emails sent)
node scripts/cold-email-engine.js --source leads.csv --template templates/default.txt --dry-run

# Run drip follow-ups
node scripts/cold-email-engine.js --drip --days 3
```

## 配置 (Configuration)

编辑 `scripts/config.json` 文件：
- `maxPerDay`：每个域名的每日发送上限（默认值：25 封邮件）。
- `delayBetweenMs`：每封邮件之间的延迟时间（单位：毫秒，默认值：3000 毫秒）。
- `dripDays`：初次发送后的跟进时间间隔（3 天或 7 天）。
- `suppressionFile`：用于存储被屏蔽/取消订阅用户列表的文件路径。
- `trackingFile`：用于存储发送日志的文件路径。

## 模板 (Templates)

模板使用 `{variable}` 语法。可用的变量包括：
- `{first_name}`、`{last_name}`、`{email}`、`{company}`、`{website}`、`{city}`、`{state}`。
- `{pain_point}`：根据网站分析自动生成的潜在客户痛点。
- `{sender_name}`、`{sender_title}`：发送邮件的发件人名称和职位。

### 模板示例
```
Subject: {company} — quick question

Hi {first_name},

I noticed {company} {pain_point}. We help businesses like yours 
fix that in under a week.

Would it make sense to chat for 10 minutes this week?

{sender_name}
{sender_title}
```

## 合规性要求 (Compliance)

- **CAN-SPAM 规则**：邮件底部需包含发件人物理地址，并提供取消订阅的途径。
- **GDPR 规则**：仅针对企业间（B2B）发送邮件；尊重用户的退订请求。
- **发送频率限制**：每个域名每天最多发送 25 封邮件，每封邮件之间有 3 秒的延迟。
- **发送前检查屏蔽列表**：每次发送前会检查用户是否在屏蔽列表中。

## 相关脚本 (Scripts)

- `scripts/cold-email-engine.js`：主要的邮件发送脚本。
- `scripts/enrich-leads.js`：用于从网站或域名中获取电子邮件地址的脚本。
- `scripts/config.json`：配置文件。

## 参考资料 (References)

- 请参阅 `references/deliverability.md` 了解域名预热和邮件送达率优化方法。
- 请参阅 `references/templates.md` 查看适用于不同行业的模板示例。