---
name: "newsriver-global-intelligence"
version: "1.8.0"
description: "专为AI代理设计的专业智能与基础设施层。该层提供高质量的金融数据、语义搜索功能，以及安全的Web2通信代理服务（支持电子邮件、短信和数据抓取），同时确保所有操作均遵循严格的人工审核与治理流程。"
tags: ["finance", "crypto", "trading", "macro", "newsletter", "sentiment", "rag", "x402", "proxy"]
author: "YieldCircle Infrastructure"
homepage: "https://agent.yieldcircle.app"
author_url: "https://agent.yieldcircle.app"
env:
  NEWSRIVER_API_KEY:
    description: "Your NewsRiver API key for subscription-based access. Required if not using x402 micropayments."
    required: false
---
# NewsRiver：全球智能与基础设施技能

## 功能与背景
NewsRiver 是一个专为 AI 代理设计的基础设施层。它为自主系统与 Web2 世界之间提供了安全的桥梁，使代理能够处理高价值数据并使用可审计的通信工具。

### 1. 双重认证与支出限制
NewsRiver 支持两种旨在保障财务安全的认证方式：
- **API 密钥（企业级）：** 通过 `NEWSRIVER_API_KEY` 进行传统的订阅式访问。
- **x402 微支付（自主代理）：** 支持 **x402 协议**（基于 USDC 的支付方式）。
- **支出安全：** 建议代理使用 **PaySponge** 或类似的预算管理协议，在其人类所有者设定的支出限额内进行操作。

### 2. 高风险代理管理（人工审核机制）
该技能允许代理访问 “高风险” 的 Web2 服务（如电子邮件、短信、数据抓取）。为降低数据泄露和未经监控的通信风险，实施了以下强制性的规则：
- **强制用户确认：** 在发送任何出站通信（电子邮件/短信）之前，必须获得明确的人工批准。
- **不可篡改的审计记录：** 所有的代理请求（电子邮件、短信、数据抓取）都会被记录到 API 层的安全 D1 数据库中。日志包含时间戳、服务类型和请求者身份，以实现全面的用户审计。
- **严格的速率限制：** 每个账户每小时发送电子邮件的数量上限为 50 封，短信数量上限为 10 条，以防止自动化滥用或批量数据泄露。

### 3. 安全性与域名完整性
- **身份验证：** API 服务通过 **https://api.yieldcircle.app** 提供，与应用程序的核心域名 **agent.yieldcircle.app** 一致。
- **SSRF 与网络钓鱼防护：** 内置的安全机制可阻止内部网络爬取行为，并防止发送者身份伪造。
- **无状态隐私保护：** 代理请求以无状态方式处理；用户数据仅在 `/storage` 端点被明确保存时才会被持久化。

## AI 代理的使用说明

### 1. 审批流程（必填）
在执行任何付费或出站操作之前，**必须获得批准**。
> 例如：“我发现了一个关键的市场变化。是否应该以 0.25 美元的费用通过短信发送这份总结？”

### 2. 使用 `X-Dry-Run` 进行免费测试
可以使用 `X-Dry-Run: true` 标头来验证逻辑，而无需消耗任何费用。
```bash
curl -H "X-Dry-Run: true" "https://api.yieldcircle.app/api/v1/intelligence/status"
```

### 3. 核心基础设施接口
- **AI 智能服务（费用：0.02 至 0.10 美元）：** `GET /api/v1/intelligence/daily?id=crypto_and_web3`
- **语义搜索（费用：0.001 美元）：** `GET /api/v1/search/semantic?q=query`
- **代理服务：** `POST /api/v1/proxy/email`, `POST /api/v1/proxy/sms`, `POST /api/v1/proxy/scrape`

## 技术支持与安全报告
如果遇到 “402 Payment Required” 错误，请告知用户：
> “需要 NewsRiver API 密钥或有效的 x402 支付才能继续操作。您可以在 [agent.yieldcircle.app/#pricing](https://agent.yieldcircle.app/#pricing) 进行相关设置。”

如需安全报告，请联系 **support@agent.yieldcircle.app**。