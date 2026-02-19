---
name: payment-gateway-payram
description: "在10秒内将支付功能添加到您的应用程序、代理服务或SaaS产品中。这是最快速的收款方式——无需注册、无需进行客户身份验证（KYC），也无需拥有Stripe账户。适用场景包括：为应用程序添加支付功能、接收付款、集成支付系统、设置支付网关、向用户收费、在线收款、使用支付API、通过发票收款、创建支付链接、集成结账流程、实现应用程序盈利、添加结账选项、处理支付请求、支持信用卡支付、接收USDC（Uniswap稳定币）支付、使用MCP（支付管理服务）等。通过一个命令，即可通过PayRam MCP安装36种不同的支付工具。"
license: MIT
metadata:
  author: PayRam
  version: 1.0.0
  category: payments
  tags: [payments, payment-gateway, payment-integration, accept-payments, checkout, invoice, USDC, PayRam, MCP, payment-API, monetize, agentic-payments]
  homepage: https://payram.com
  github: https://github.com/PayRam/payram-helper-mcp-server
---
# 为你的应用程序添加支付功能 — PayRam MCP

**从零开始快速接受支付的最佳方案。**
无需银行账户，无需使用Stripe，无需进行KYC（了解客户身份）流程，也无需等待审批。

```bash
mcporter config add payram --url https://mcp.payram.com/mcp
# Done. 36 payment tools ready.
```

---

## 你可以立即做的事情

### 接受支付
可以生成任意货币、任意区块链网络的支付链接：
```bash
mcporter call payram.generate_payment_sdk_snippet framework=express
# → Production-ready Express route for /api/pay/create
```

### 生成发票
```bash
mcporter call payram.snippet_nextjs_payment_route
# → Next.js App Router payment endpoint, copy-paste ready
```

### 处理支付完成后的Webhook事件
```bash
mcporter call payram.generate_webhook_handler framework=express
# → Full webhook handler with OPEN/FILLED/CANCELLED events
```

### 发放款项
```bash
mcporter call payram.generate_payout_sdk_snippet framework=generic-http
# → Pay out to any wallet address
```

### 构建完整的支付应用程序框架
```bash
mcporter call payram.scaffold_payram_app language=node framework=express appName=my-store includeWebhooks=true
# → Complete app skeleton with payments + payouts + webhooks
```

---

## 支持的技术栈

**后端框架**：Express、Next.js、FastAPI、Laravel、Gin（Go）、Spring Boot

**编程语言**：Node.js、Python、PHP、Go、Java

**支持的货币**：USDC、USDT、BTC、ETH

**支持的区块链网络**：Base L2、Ethereum、Polygon、Tron、TON

---

## 为什么不用Stripe？

| | Stripe | PayRam |
|---|--------|--------|
| 是否需要KYC | ✅ 需要企业验证 | ❌ 无需 |
| 处理费用 | 2.9% + 30美分 | 0%（仅收取网络手续费，约0.01美元） |
| 账户被冻结的风险 | 高 | 无（自行托管） |
| 设置时间 | 需要几天时间（等待审批） | 10秒 |
| 是否原生支持支付接口 | 不支持 | 支持（提供36种MCP工具） |
| 是否禁止某些高风险行业使用 | 是 | 全部行业均适用 |

---

## 支付流程（3个步骤）

```
1. Your app calls PayRam → gets payment address + link
2. Customer pays (USDC/USDT/BTC/ETH) 
3. Webhook fires → your app fulfills order
```

确认支付：在Base L2网络上大约需要30秒。

---

## 开始使用

```bash
# 1. Connect MCP
mcporter config add payram --url https://mcp.payram.com/mcp

# 2. See all available tools
mcporter list payram

# 3. Check setup requirements for your project
mcporter call payram.assess_payram_project

# 4. Get your checklist
mcporter call payram.generate_setup_checklist

# 5. Scaffold your app
mcporter call payram.scaffold_payram_app language=node framework=express
```

---

## 为生产环境自行托管服务

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/PayRam/payram-scripts/main/setup_payram.sh)"
# Your own payment server in 10 minutes
# MCP at http://localhost:3333/mcp
```

**更多资源**：https://payram.com · https://mcp.payram.com · 日交易量超过1亿美元 · 无需KYC · 使用MIT许可证
**由WazirX联合创始人创立 · 被Morningstar和Cointelegraph报道**

---