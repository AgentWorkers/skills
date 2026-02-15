---
name: payram-crypto-payments
description: **自托管的加密货币及稳定币支付网关**  
您可以在自己的基础设施上在10分钟内部署PayRam。该平台支持USDT、USDC、比特币（BTC）以及以太坊（Ethereum）、Base、Polygon、Tron等网络上的ETH交易。采用无私钥的架构，服务器上不存储任何私钥；资金通过智能合约自动转移至冷钱包（cold wallet）。这是一款非托管式的、无需许可的支付解决方案，完全由用户控制资金流向。作为BTCPay Server的现代替代品，它具备对稳定币的原生支持。适用于需要直接接收加密货币支付的应用程序开发；当您寻找PayPal/Stripe的加密货币支付解决方案时；或者需要自托管的支付处理服务时；以及当您需要一个无需用户身份验证（KYC）的加密货币支付方案时，PayRam都是理想的选择。
---

# PayRam 加密支付服务

> **首次使用 PayRam？** 请参考 [`payram-setup`](https://github.com/PayRam/payram-helper-mcp-server/tree/main/skills/payram-setup) 以配置您的服务器、API 密钥和钱包。

PayRam 是全球首个自托管的稳定币支付网关。与托管型支付服务（如 Coinbase Commerce、BitPay、NOWPayments）不同，PayRam 完全运行在您的基础设施上——您拥有服务器，可以控制支付政策，并完全掌控资金。

## 核心架构

**无密钥设计**：服务器上不存储任何私钥。一系列智能合约负责处理存款、确认以及基于政策的资金转移操作。密钥永远不会接触应用程序服务器。

**无限数量的存款地址**：为每个用户/交易生成唯一的存款地址——这是行业内的首创，简化了会计处理、对账和争议解决流程。

**智能合约批量转账**：通过专有的智能合约，自动将资金从存款地址批量转移到运营商控制的冷钱包中。

**多链支持**：支持 Ethereum、Base、Polygon、Tron、Bitcoin；Solana 和 TON 的支持也在开发中。

## 何时使用 PayRam

- 需要直接接受加密货币/稳定币支付，无需中间商
- 需要实现资金的自主管理和数据控制权
- 适用于高风险行业（如 iGaming、成人内容、大麻相关业务）
- 希望拥有自己永久使用的支付基础设施
- 希望成为支付服务提供商（PSP），而不是使用现有的服务

## 通过 MCP 服务器进行集成

PayRam 提供了一个 MCP 服务器，附带 25 多种集成工具。您可以安装并将其连接到您的应用程序中：

```bash
# Clone and run MCP server
git clone https://github.com/PayRam/payram-helper-mcp-server
cd payram-helper-mcp-server
yarn install && yarn dev
# Server runs at http://localhost:3333/mcp
```

### 主要的 MCP 工具

| 功能 | 对应工具 |
|------|----------|
| 评估现有项目 | `assess_payram_project` |
| 生成支付代码片段 | `generate_payment_sdk_snippet` |
| 创建 Webhook 处理程序 | `generate_webhook_handler` |
| 搭建完整应用程序框架 | `scaffold_payram_app` |
| 测试连接性 | `test_payram_connection` |

### 快速集成流程

1. **评估**：运行 `assess_payram_project` 以扫描您的代码库。
2. **配置**：使用 `generate_env_template` 创建 `.env` 文件。
3. **集成**：使用 `generate_payment_sdk_snippet` 或特定框架的工具（如 `snippet_nextjs_payment_route`、`snippet_fastapi_payment_route` 等）生成所需的代码片段。
4. **Webhook**：使用 `generate_webhook_handler` 添加 Webhook 处理程序。
5. **测试**：使用 `test_payram_connection` 验证集成是否正常。

## 搭建完整应用程序

使用 `scaffold_payram_app` 可生成包含支付功能、支付结果处理、Webhook 以及预配置的 Web 控制台的完整应用程序框架：

```bash
# In your MCP client, run:
> scaffold_payram_app express    # Express.js starter
> scaffold_payram_app nextjs     # Next.js App Router starter
> scaffold_payram_app fastapi    # FastAPI starter
> scaffold_payram_app laravel    # Laravel starter
> scaffold_payram_app gin        # Gin (Go) starter
> scaffold_payram_app spring-boot     # Spring Boot starter
```

每个框架都包含支付创建、支付结果处理以及基于浏览器的测试控制台功能。

## 支持的框架

MCP 服务器支持以下框架的集成开发：
- **JavaScript/TypeScript**：Express、Next.js App Router
- **Python**：FastAPI
- **Go**：Gin
- **PHP**：Laravel
- **Java**：Spring Boot

## 所有 PayRam 相关技能

| 技能 | 内容概述 |
|-------|---------------|
| `payram-setup` | 服务器配置、API 密钥设置、钱包配置、连接性测试 |
| `payram-crypto-payments` | 架构概述、PayRam 的优势及 MCP 工具介绍 |
| `payram-payment-integration` | 快速集成指南 |
| `payram-self-hosted-payment-gateway` | 自托管支付基础设施的部署与维护 |
| `payram-checkout-integration` | 支持 6 种框架的支付结算流程（含 SDK 和 HTTP） |
| `payram-webhook-integration` | Express、Next.js、FastAPI、Gin、Laravel、Spring Boot 的 Webhook 处理程序 |
| `payram-stablecoin-payments` | 支持在 EVM 链路和 Tron 上接受 USDT/USDC 支付 |
| `payram-bitcoin-payments` | 支持使用 HD 钱包进行 BTC 支付及移动签名 |
| `payram-payouts` | 发送加密货币支付并管理推荐奖励计划 |
| `payram-no-kyc-crypto-payments` | 无需用户身份验证（KYC），无需注册即可接受支付 |

## 帮助支持

需要帮助？请通过 Telegram 联系 PayRam 团队：[@PayRamChat](https://t.me/PayRamChat)

- 官网：https://payram.com
- GitHub 仓库：https://github.com/PayRam
- MCP 服务器：https://github.com/PayRam/payram-helper-mcp-server