---
name: local-lead-gen
description: >
  自动化本地商业潜在客户生成及冷电话/邮件推广流程：  
  该系统按行业细分和地理位置对目标企业进行扫描，评估其网站的性能（如SSL安全性、移动设备兼容性、加载速度、设计质量），识别存在问题或过时的网站，并补充相应的联系信息。随后，系统会发送个性化的邮件，主动推广相关服务。  
  适用于构建潜在客户生成流程、开拓本地企业市场、寻找网站质量不佳的公司、自动化开展冷电话/邮件推广活动，或建立定期业务开发工作流程。
---
# 本地潜在客户开发——自动化商业拓展与联系

寻找网站质量较差的本地企业，对其进行评估，并自动发送个性化的推销邮件。

## 流程概述

1. **扫描**：通过 Brave Search API 按行业和城市搜索企业。
2. **评估**：检查每个网站的 SSL 证书、移动设备兼容性、加载速度、设计质量以及页面中的错误元素（评分范围：0-100）。
3. **筛选**：将评分低于 40 的网站标记为潜在联系对象。
4. **提取信息**：使用 DeepCrawl 或直接爬取技术从企业的联系页面中提取电子邮件地址。
5. **发送邮件**：通过 Resend（或其他 SMTP 服务）发送个性化的推销邮件。
6. **跟踪**：将所有潜在客户信息记录到 Google Sheets 或 CSV 文件中，并跟踪其状态。

## 所需资源

- **Brave Search API 密钥**：用于企业信息查询（免费 tier 可用）。
- **Resend API 密钥**（或 SMTP 账户信息）：用于发送邮件。
- **DeepCrawl API 密钥**（可选）：用于更准确地解析联系页面信息。
- **Google Sheets OAuth**（可选）：用于跟踪潜在客户信息。

## 快速入门

```bash
# Set environment variables
export BRAVE_API_KEY=your_key
export RESEND_API_KEY=your_key

# Run the scanner
node scripts/bad-website-hunter.js --niche "restaurants" --city "Austin TX" --limit 20
```

## 配置

编辑 `scripts/config.json` 以自定义以下内容：
- 目标行业和城市。
- 评估标准（用于筛选潜在客户）。
- 邮件模板和发件人信息。
- 邮件过滤列表（已退订的用户）。

## 脚本

- `scripts/bad-website-hunter.js`：主要流程脚本：扫描 → 评估 → 信息提取 → 发送邮件。
- `scripts/config.json`：流程配置文件。

## 邮件模板

默认的推销邮件模板用于推广网页设计/开发服务。您可以在 `config.json` 中自定义邮件内容。

```
Subject: Quick question about {business_name}'s website

Hi {first_name},

I was looking at {business_name}'s website and noticed a few things 
that might be costing you customers: {issues_found}.

I help local businesses in {city} modernize their online presence. 
Would you be open to a quick chat about what an upgrade could look like?

Best,
{sender_name}
```

## 扩展策略

- **小城镇**（人口 5,000–30,000 人）的网站质量较差的比例较高。
- **最佳目标行业**：餐厅、汽车维修、美发沙龙、承包商、律师事务所。
- 每个域名每天发送 10–25 封邮件，以避免被标记为垃圾邮件。
- 如果每天发送邮件数量超过 50 封，请轮换发送域名。
- 添加跟进邮件（例如在第 3 天和第 7 天发送再次联系的邮件）。

## 参考资料

- 请参阅 `references/scoring-criteria.md` 以了解网站评估方法。
- 请参阅 `references/email-best-practices.md` 以获取关于邮件发送效果的优化建议。