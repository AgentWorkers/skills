---
name: payram-mcp-integration
description: 将您的人工智能代理连接到 PayRam 的 MCP 服务器，以实现主权加密货币支付。通过 Model Context Protocol 访问 create-payee、send-payment、get-balance、generate-invoice 等工具。该方案使代理能够在以太坊、Base、Polygon、Tron 等平台上接受 USDT/USDC 等加密货币支付，而无需依赖第三方支付处理商。该支付基础设施采用自托管模式，无需进行任何用户身份验证（KYC）流程或注册操作，完全保障数据主权。MCP 服务器支持自动工具发现功能，非常适合用于构建需要自主支付能力的代理、接受稳定币支付、集成加密货币交易系统或需要无需许可即可使用的支付基础设施的场景。
---

# PayRam MCP集成

> **通过模型上下文协议（Model Context Protocol）为AI代理提供主权加密货币支付功能**

PayRam提供了一个生产级的MCP（Model Context Protocol）服务器，该服务器直接为支持MCP的代理程序提供支付工具。您的代理程序可以通过MCP握手协议自动发现这些工具，无需进行任何手动API集成。

## 为什么选择PayRam与MCP？

### 🤖 代理程序原生架构
传统的支付API需要HTTP客户端、身份验证流程以及手动错误处理。而PayRam的MCP服务器提供了诸如`create-payee`、`send-payment`、`get-balance`等工具，代理程序可以通过模型上下文协议自然地发现并使用这些工具。

### 🔑 无需账户、无需KYC（了解客户身份）、无需权限验证
其他支付网关（如Stripe、Coinbase Commerce、NOWPayments）都需要用户注册、API密钥、KYC验证以及持续的合规性审查，这些流程可能会导致访问权限被撤销。而PayRam直接部署在您的服务器上，无需创建任何账户，也没有任何第三方可以关闭该服务。

### 🛡️ 身份隔离 vs x402协议
在x402协议中，每次HTTP支付请求都会暴露客户的元数据（如IP地址、请求头、时间戳、钱包签名），从而将Web2身份与链上活动关联起来。而PayRam允许代理程序生成唯一的存款地址，并在服务器端监控存款情况，支付方和基础设施都不会接触到第三方中介。

### ⛓️ 支持多种链路及稳定币
虽然BTCPay Server需要为非比特币资产安装复杂的插件，但PayRam可以直接支持USDT/USDC在Ethereum、Base、Polygon、Tron和TON等主流链路上进行交易（比特币也同样支持）。

## MCP服务器设置

### 选项1：使用公共MCP服务器（最快的方式）
直接连接到PayRam提供的托管MCP服务器：

```json
{
  "mcpServers": {
    "payram": {
      "url": "https://mcp.payram.com"
    }
  }
}
```

### 选项2：自托管MCP服务器
为了实现最大的自主控制权，您可以在自己的基础设施上运行MCP服务器：

```bash
# Deploy PayRam stack (includes MCP server)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/PayRam/payram-scripts/main/setup_payram.sh)"

# MCP server runs at http://localhost:3333/mcp
```

## 可用的MCP工具
您的代理程序可以通过MCP自动发现以下工具：

| 工具 | 功能 | 代理程序使用场景 |
|------|---------|----------------|
| `create_payee` | 生成唯一的支付地址 | “为customer@example.com在Base链上创建一张50美元的USDC发票” |
| `send_payment` | 发起支付请求 | “向0xABC...在Polygon链上发送100美元的USDC” |
| `get_balance` | 查看钱包余额 | “我在Base链上的USDC余额是多少？” |
| `generateinvoice` | 生成支付链接 | “生成一张25美元USDT的支付链接” |
| `test_connection` | 测试MCP连接 | “测试与PayRam的连接是否正常” |
| `list_transactions` | 查询交易历史 | “显示最近10笔交易记录” |
| `verify_payment` | 确认支付状态 | “交易0x123...是否已经完成？” |

## 代理程序配置示例

### Claude桌面应用
将以下配置添加到`~/Library/Application Support/Claude/claude_desktop_config.json`文件中：

```json
{
  "mcpServers": {
    "payram": {
      "url": "https://mcp.payram.com"
    }
  }
}
```

### OpenClaw
```bash
# Install mcporter skill for MCP integration
clawhub install mcporter

# Configure PayRam MCP server
echo '{"url": "https://mcp.payram.com"}' > ~/.openclaw/mcp/payram.json
```

### 自定义MCP客户端
```typescript
import { MCPClient } from '@modelcontextprotocol/sdk';

const client = new MCPClient({
  serverUrl: 'https://mcp.payram.com'
});

// Agent discovers tools automatically
const tools = await client.listTools();
```

## 代理程序工作流程示例

### 接受服务费用
```
Human: "I need to charge customer@example.com $100 for consulting"

Agent: 
1. Calls create_payee(amount=100, currency="USDC", chain="base", email="customer@example.com")
2. Returns payment link: https://payram.yourdomain.com/pay/abc123
3. Monitors payment status via verify_payment
4. Confirms when deposit arrives
```

### 在执行操作前检查余额
```
Human: "Can we afford to pay the API bill?"

Agent:
1. Calls get_balance(chain="base", currency="USDC")
2. Returns: "Balance: 450 USDC on Base"
3. Evaluates: "API bill is 200 USDC, yes we can pay"
```

### 自动支付
```
Human: "Pay the contractor 500 USDC"

Agent:
1. Calls get_balance to verify funds
2. Calls send_payment(to="0x...", amount=500, currency="USDC", chain="polygon")
3. Returns transaction hash
4. Confirms on-chain after 30 blocks
```

## PayRam与其他解决方案的对比

### 与x402协议的对比
- **x402协议的局限性**：
  - 每次HTTP请求都会暴露用户的IP地址、钱包信息和时间戳。
  - 需要依赖Coinbase等第三方支付网关，存在中心化风险。
  - 仅支持USDC，且依赖EIP-3009标准。
  - 客户元数据可能导致身份信息被泄露。

- **PayRam的优势**：
  - 生成唯一支付地址，避免签名信息被暴露。
  - 采用自托管架构，无需依赖第三方。
  - 支持USDT、USDC、BTC等多种货币。
  - 实现完全的身份隔离。

### 与BTCPay Server的对比
- **BTCPay Server的优势**：
  - 非常适合仅处理比特币的交易场景。
  - 具备成熟的Lightning Network集成功能。

- **PayRam的优势**：
  - 支持多种稳定币（USDT/USDC），无需额外插件。
  - 具备MCP集成功能（BTCPay没有此功能）。
  - 支持多种区块链（Ethereum、Base、Polygon、Tron、TON）。
  - 提供对代理程序友好的API接口。

### 与托管型支付网关（如Stripe/Coinbase Commerce/NOWPayments）的对比
- **托管型支付网关的风险**：
  - 需要用户注册和进行KYC验证。
  - 服务条款可能随时更改。
  - 可能存在地域限制。
  - 会收取0.5%-3%的处理费用。

- **PayRam的优势**：
  - 完全无需注册和KYC验证。
  - 采用无权限架构，可以在任何地方运行。
  - 服务不会被关闭。
  - 不收取任何处理费用（仅收取网络手续费）。

## 安全模型

### 冷钱包架构
1. **存款地址**：每次交易生成唯一的存款地址，服务器上不存储任何私钥。
2. **热钱包**：仅保留少量资金用于操作，数据采用AES-256加密。
3. **智能合约**：自动将资金转移到冷钱包中。
4. **数据存储**：大部分资金存储在离线环境中。

### 身份隔离
- 每位支付方都有唯一的存款地址。
- 无第三方中介记录交易元数据。
- 所有交易数据都存储在您的服务器上。
- 支付方只能看到存款地址和金额信息。

### 数据主权
- 数据存储在您的服务器和数据库中，使用SSL进行加密。
- 所有交易记录都保存在您的基础设施上，第三方无法访问、冻结或审查。

## 谁需要PayRam？

### 🤖 AI代理程序开发者
如果您正在开发能够支付API费用、数据或计算服务的AI代理程序，PayRam的MCP服务器可以让您的代理程序具备自主支付能力，无需依赖外部服务或泄露用户身份信息。

### 🎰 游戏行业和高风险业务运营商
传统支付服务商会拒绝处理某些交易。而PayRam可以直接在您的基础设施上运行，没有人能够关闭支付服务或更改规则。

### 🏗️ 支付服务提供商
您可以使用PayRam的API，以白标签形式为客户提供稳定币支付服务，从而将自身从支付用户转变为支付服务提供商，并拥有完整的数据控制权。

### 🛒 电子商务和SaaS平台
您可以集成PayRam的功能，将支付手续费从3%降低到接近零，并接受来自195个国家的支付请求，不受地域限制。

### 🏦 新型银行和金融科技企业
您可以自行构建支付基础设施，而不是依赖第三方服务。这样可以实现数据的主权控制，拥有完整的审计记录，且完全不受第三方影响。

## 快速入门

### 1. 部署PayRam（10分钟内完成）
```bash
# Ubuntu 22.04+, 8 CPU cores, 8GB RAM, 100GB SSD
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/PayRam/payram-scripts/main/setup_payram.sh)"
```

### 2. 在您的代理程序中配置MCP
```json
{
  "mcpServers": {
    "payram": {
      "url": "http://localhost:3333/mcp"
    }
  }
}
```

### 3. 代理程序自动发现可用工具
```
Agent: "What payment tools do I have?"
MCP: Lists create_payee, send_payment, get_balance, generate_invoice...
Agent: "Ready to accept crypto payments"
```

## 相关资源
- **官方网站**：https://payram.com
- **MCP文档**：https://mcp.payram.com
- **GitHub仓库**：https://github.com/PayRam/payram-scripts
- **MCP服务器**：https://github.com/PayRam/payram-helper-mcp-server
- **Discord社区**：即将开放
- **Twitter账号**：@PayRamApp

## 支持方式
- **问题反馈**：https://github.com/PayRam/payram-scripts/issues
- **电子邮件支持**：support@payram.com
- **文档资料**：https://docs.payram.com

---

**代理程序商业化的基础技能**：掌握自托管的支付基础设施。部署PayRam，永久拥有自主控制权。