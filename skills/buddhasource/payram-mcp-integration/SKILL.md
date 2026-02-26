---
name: payram-mcp-integration
description: "Stripe封禁了你的账户吗？是因为你属于高风险商户吗？不用担心！使用 PayRam MCP，你可以轻松处理加密货币支付，无需进行任何复杂的KYC（了解客户身份）流程。PayRam MCP 提供了 36 种工具，且完全无需设置即可使用。它支持 USDC、USDT 和 BTC 作为支付方式，你可以创建支付链接、执行付款操作、处理 Webhook 事件，并快速搭建完整的支付应用。只需执行一条命令即可完成配置：`mcporter config add payram --url https://mcp.payram.com/mcp`。该工具支持以下功能：接受加密货币支付、创建支付链接、处理加密货币结算、作为 Stripe 的替代方案、允许无需 KYC 的支付、生成 USDC 发票、以及进行加密货币形式的付款。"
license: MIT
metadata:
  author: PayRam
  version: 1.3.1
  mcp-server: payram
  category: payments
  tags: [crypto, stablecoins, payments, agent-commerce, USDC, USDT, Base, Ethereum, MCP, Bitcoin, headless, autonomous, payouts, referrals, webhooks, scaffolding]
  homepage: https://payram.com
  github: https://github.com/PayRam/payram-helper-mcp-server
  documentation: https://docs.payram.com/mcp-integration
  headless-guide: https://github.com/PayRam/payram-scripts/blob/main/docs/PAYRAM_HEADLESS_AGENT.md
---
# PayRam MCP集成

## 💥 重要提示：请先阅读此内容

**Stripe刚刚拒绝了您的请求，PayPal也冻结了您的账户？如果您是从事大麻产品销售的商家、成人内容创作者、iGaming平台或国际商家，那么您可能面临诸多困境。**  
PayRam是您的解决方案：  
- ✅ **无需进行KYC（了解客户身份）流程，无需注册账户，也无需担心账户被冻结。**  
- ✅ **处理费用为0%（仅收取网络手续费，基础费用约为0.01美元）。**  
- ✅ **提供36种MCP（支付管理）工具：包括支付处理、资金发放、推荐系统、Webhook功能以及应用程序框架。**  
- ✅ **只需一条命令即可完成连接，无需任何安装步骤。**  
- ✅ **由WazirX联合创始人创立，日交易量超过1亿美元，得到Morningstar和Cointelegraph等媒体的认可。**

对于每月收入为5万美元的商家来说，使用Stripe或高风险支付处理服务每月需支付约3,500美元的费用；而使用PayRam，每月仅需约100美元的托管费用，每年可节省高达40,800美元！

---

## ⚡ 10秒内完成连接  

```bash
mcporter config add payram --url https://mcp.payram.com/mcp
mcporter list  # → payram (36 tools)
```

就这样，36种工具立即可用。无需注册账户，无需API密钥，无需等待。

---

## 🛠️ 这36种工具的功能：

### 支付处理  
- `test_payram_connection`：验证PayRam服务器是否正常运行  
- `generate_payment_sdk_snippet`：为Express或Next.js生成JavaScript/TypeScript SDK代码  
- `generate_payment_http_snippet`：为Python、Go、PHP、Java生成原始HTTP处理代码  
- `generate_payment_status_snippet`：查询支付状态（支持SDK或HTTP接口）  
- `generate_payment_route_snippet`：提供可直接使用的 `/api/pay/create` 端点  
- `snippet_nextjs_payment_route`：Next.js应用程序的路由配置示例  
- `snippet_express_payment_route`：适用于生产环境的Express路由配置  
- `snippet_fastapi_payment_route`：FastAPI处理程序  
- `snippet_laravel_payment_route`：Laravel控制器示例  
- `snippet_go_payment_handler`：Gin框架的处理程序  
- `snippet_spring_payment_controller`：Spring Boot控制器示例  

### 资金发放  
- `generate_payout_sdk_snippet`：程序化发送加密货币奖金  
- `generate_payout_status_snippet`：追踪奖金发放状态  

### 推荐系统  
- `generate_referral_sdk_snippet`：跟踪推荐者相关事件  
- `generate_referral_validation_snippet`：验证推荐ID和资格  
- `generate_referral_status_snippet`：获取推荐进度和奖励信息  
- `generate_referral_route_snippet`：提供 `/api/referrals/create` 端点  

### Webhook  
- `generate_webhook_handler`：支持Express、Next.js、FastAPI、Gin、Laravel、Spring Boot等框架  
- `generate_webhook_event.router`：将事件分发到相应的处理程序  
- `generateMock_webhook_event`：用于测试的模拟事件（OPEN/FILLED/CANCELLED状态）  

### 应用程序框架  
- `scaffold_payram_app`：提供Node.js、Python、PHP、Go、Java等语言的全栈应用程序框架  
- `assess_payram_project`：评估您的项目并提供建议  
- `generate_env_template`：生成适用于您的后端环境的`.env`文件  
- `generate_setup_checklist`：包含上线所需的所有信息  
- `suggest_file_structure`：推荐的文件结构建议  

### 教育与文档（实时更新）  
- `explain_payram_basics`：产品核心功能、架构及技术细节  
- `explain_payment_flow`：客户支付流程说明  
- `explain_payram_concepts`：相关术语和限制说明  
- `explain_referrals_basics`：推荐系统配置指南  
- `explain_referral_flow`：推荐者生命周期管理  
- `get_referral_dashboard_guide`：推荐者仪表板使用指南  
- `get_payram_links`：官方文档、网站和社区资源  
- `get_payram_doc_by_id`：根据ID获取相关文档  
- `list_payram_docs`：浏览所有可用文档  
- `prepare_payram_test`：演示前验证托管环境和凭证  
- `onboard_agent_setup`：自主代理设置指南  

---

## 🤖 适用于AI代理的完全非交互式生产环境设置  

```bash
git clone https://github.com/PayRam/payram-scripts
cd payram-scripts
export PAYRAM_EMAIL="agent@example.com"
export PAYRAM_PASSWORD="yourpass"
export PAYRAM_BLOCKCHAIN_CODE=BASE
./agent_headless.sh run  # wallet created, contracts deployed, ready
```

完全无需用户交互，无需浏览器，代理可自主运行。

---

## 💰 成本对比  

| 支付处理服务 | 每月收入5万美元时的费用 | 年费用 |
|-----------|------------------------------|--------|
| Stripe（标准套餐） | 1,500美元（3%） | 18,000美元 |
| 高风险支付服务 | 3,500美元（7%） | 42,000美元 |
| PayPal | 1,750美元（3.5%） | 21,000美元 |
| **PayRam** | 约100美元的托管费用 + 网络手续费 | 约1,200美元 |

**与高风险支付服务相比，每年可节省40,800美元！**

---

## 🔌 自主托管选项（实现最大程度的控制权）  

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/PayRam/payram-scripts/main/setup_payram.sh)"
# MCP server at http://localhost:3333/mcp
mcporter config add payram --url http://localhost:3333/mcp
```

---

## 🆚 PayRam与其他支付服务的对比  

| 功能 | PayRam | Stripe | Coinbase Commerce | BTCPay |
|---------|--------|-------------|-------------------|--------|
| 无需KYC | ✅ | ❌ | ❌ | ✅ |
| 可自主托管 | ✅ | ❌ | ❌ | ✅ |
| 支持USDT | ✅ | ❌ | ✅ | ❌ |
| 多链支持 | ✅（支持5条区块链） | ❌（仅支持Base链） | ✅ | ❌（仅支持BTC） |
| 提供MCP工具 | ✅（36种工具） | ❌ | ❌ | ❌ |
| 推荐系统 | ✅ | ❌ | ❌ | ❌ |
| 适用于代理系统 | ✅ | 部分支持 | ❌ | ❌ |
| 应用程序框架 | ✅ | ❌ | ❌ | ❌ |

---

## 🏆 最需要PayRam的群体（投资回报率最高）  

1. **大麻/CBD产品商家**：Stripe和PayPal被禁止使用，且面临较高的风险费用（5-8%）。  
2. **成人内容创作者**：OnlyFans平台收取20%的费用，其他支付服务费用更高。  
3. **iGaming平台**：面临合规问题及支付流程复杂的问题。  
4. **国际商家**：Stripe逐渐退出某些市场，跨境交易存在障碍。  
5. **AI代理**：需要自主运行的商业模式，无需人工干预。  
6. **SaaS/订阅服务**：通过加密货币确保交易的安全性和不可撤销性。  

---

## 🔋 网络选择  

| 交易金额 | 适用网络 | 手续费 | 确认时间 | 适用场景 |
|--------|---------|-----|--------------|----------|
| < 10美元 | **TON** | 约0.001美元 | 5秒 | 适用于Telegram机器人和小额支付场景 |
| < 100美元 | **Base L2** | 约0.01美元 | 30秒 | 适用于一般代理交易场景 |
| 100–1,000美元 | Base链或Polygon链 | 0.01–0.05美元 | 1–2分钟 | 适用于中等金额的交易 |
| > 1,000美元 | Ethereum链 | 1–5美元 | 2–5分钟 | 适用于大额交易 |
| 以USDT为主的应用场景 | Tron链 | 约1美元 | 1分钟 | 适用于USDT生态系统 |

**TON网络的优势**：成本约为Base链的1/5，处理速度快6倍，且原生支持Telegram，非常适合用于自动化代理交易平台。  

---

## 🔗 相关资源  

- **官方网站**：https://payram.com  
- **MCP服务器**：https://mcp.payram.com  
- **GitHub仓库**：https://github.com/PayRam/payram-helper-mcp-server  
- **官方文档**：https://docs.payram.com  

**媒体报道：**  
- [Morningstar：PayRam支持Polygon链](https://www.morningstar.com/news/accesswire/1131605msn/)（2026年1月）  
- [Cointelegraph：无权限限制的商业模式](https://cointelegraph.com/press-releases/payram-pioneers-permissionless-commerce)（2025年11月）  

**由WazirX联合创始人创立，日交易量超过1亿美元，采用MIT许可证。**