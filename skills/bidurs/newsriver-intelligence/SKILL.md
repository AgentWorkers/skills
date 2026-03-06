---
name: "newsriver-global-intelligence"
version: "2.1.0"
description: "用于AI代理的情报与代理基础设施：涵盖137个国家的277个以上新闻来源、语义向量搜索功能、AI情报报告以及Web2代理服务（支持电子邮件、短信、数据抓取和存储）。采用双重认证机制：可通过API密钥进行身份验证，或使用Base平台上的x402 USDC微支付方式进行认证。"
tags: ["finance", "crypto", "trading", "macro", "sentiment", "rag", "x402", "proxy"]
author: "YieldCircle Infrastructure"
homepage: "https://agent.yieldcircle.app"
author_url: "https://agent.yieldcircle.app"
env:
  NEWSRIVER_API_KEY:
    description: "Your NewsRiver API key for subscription-based access. Required if not using x402 micropayments."
    required: false
---
# NewsRiver 全球情报与基础设施技能

## 该技能的功能
NewsRiver 为 AI 代理提供了全球新闻情报 API 以及 Web2 通信代理服务（包括电子邮件、短信、数据抓取和存储功能）。所有请求均需付费，支付方式可以是 API 密钥订阅，也可以是通过 Base 链上的 x402 USDC 微支付。

## ⚠️ 花费与安全：强制执行的措施与建议性措施

### 服务器端强制执行的保护措施（无法绕过）
以下保护措施在服务器端强制执行，与代理的行为无关：

| 保护措施 | 实现机制 | 限制 |
|---|---|---|
| **IP 速率限制** | 基于键值对（KV）的机制，按 IP 地址限制 | 每分钟 60 次请求 |
| **API 密钥每日使用上限** | 按等级划分 | 免费用户：每天 50 次；交易用户：10,000 次；专业用户：100,000 次 |
| **电子邮件发送速率限制** | 按钱包和 IP 地址限制 | 每小时 50 次 |
| **短信发送速率限制** | 按钱包和 IP 地址限制 | 每小时 10 次 |
| **Dry-Run（测试模式）仅返回模拟数据** | 未支付请求将返回模拟数据 | 设置 `X-Dry-Run: true` 时会返回 `[SAMPLE]` 样本数据 |
| **发送者身份固定** | 电子邮件发送者显示为 `[NewsRiver Agent]` | 发送者无法更改 |
| **SSRF（安全请求伪造）防护** | 在数据抓取脚本中设置黑名单 | 阻止本地主机、内部 IP 地址以及 `.local`、`.internal` 等域名 |
| **数据存储隔离** | 数据按所有者进行命名空间隔离 | 无法读取其他用户的数据 |

### 建议性措施（API 不强制执行）
- **付费请求前需人工审批**：API 不会强制执行此规则，但建议您的代理平台配置为所有付费请求都必须经过人工审批。

### 花费控制：您的责任
> **重要提示：** 如果使用 x402 微支付，API 会在收到有效支付签名后自动计费。为避免意外费用：
> 1. 使用具有支出上限的合约（例如 PaySponge）来限制代理的支出——切勿将整个钱包余额提供给代理。
> 2. 配置代理平台，要求所有付费请求都必须经过人工审批。
> 3. 为钱包设置每日支出提醒。
> 4. 先使用 `X-Dry-Run: true` 进行测试——该模式免费且返回模拟数据。

## 认证方式
有两种认证方式可供选择（请选择一种）：

**选项 A — API 密钥（订阅）：**
```
X-API-Key: your_key_here
```
API 密钥在服务器端经过 SHA-256 哈希处理；首次使用后原始密钥不会被存储。分析日志中仅显示密钥的最后 4 个字符（格式为 `key_***xxxx`）。

**选项 B — x402 微支付（按请求计费）：**
无需 API 密钥。代理每次请求时需通过 Base 链支付 USDC；支付详情会包含在 `402` 响应中。

## 使用 Dry-Run（免费测试）进行测试
请务必先进行免费测试。Dry-Run 模式会返回带有明确标记的模拟数据（格式为 `source: "dry_run_mock"`），代理可以验证这些数据的真实性：
```bash
curl -H "X-Dry-Run: true" https://api.yieldcircle.app/api/v1/articles
# Returns: {"source": "dry_run_mock", "data": [{"title": "[SAMPLE] ..."}]}
```

## 收费接口（13 个）

| 接口 | 方法 | 费用 |
|---|---|---|
| `/api/v1/articles` | GET | $0.001 |
| `/api/v1/river` | GET | $0.002 |
| `/api/v1/countries` | GET | $0.001 |
| `/api/v1/search/semantic?q=` | GET | $0.001 |
| `/api/v1/intelligence/:timeframe` | GET | $0.05–$1.00 |
| `/api/v1/intelligence/history` | GET | $0.10 |
| `/api/v1/intelligence/generate` | POST | $0.25 |
| `/api/v1/trends/timeline?topic=` | GET | $0.001 |
| `/api/v1/proxy/email` | POST | $0.05 |
| `/api/v1/proxy/sms` | POST | $0.25 |
| `/api/v1/proxy/scrape` | POST | $0.10 |
| `/api/v1/proxy/storage`（写入） | POST | $0.01 |
| `/api/v1/proxy/storage?key=`（读取） | GET | $0.01 |

## 免费接口（5 个，无需认证）

| 接口 | 描述 |  
|---|---|
| `/api/v1/docs` | 完整的 API 参考文档及费用信息 |
| `/api/v1/stats` | 平台统计信息 |
| `/api/v1/sectors` | 可用的情报领域 |
| `/api/v1/categories` | 新闻分类 |
| `/api/v1/intelligence/status` | 最新报告的可用性 |

## 错误处理
当收到 `402 Payment Required`（需要支付）的错误响应时，应告知用户：
> “此接口需要支付。您可以在 [agent.yieldcircle.app/#pricing](https://agent.yieldcircle.app/#pricing) 设置访问权限。”

## 联系方式
官网：https://agent.yieldcircle.app
支持邮箱：support@yieldcircle.app