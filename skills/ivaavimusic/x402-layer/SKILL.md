---
name: x402-layer
version: 1.0.1
description: |
  x402 Singularity Layer - Enable AI agents to deploy monetized API endpoints,
  consume paid services via USDC payments, manage credits, and participate
  in a self-sustaining agent economy. Supports Base and Solana networks.
metadata:
  clawdbot:
    emoji: "⚡"
    os:
      - linux
      - darwin
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
---

# x402 单点层（Singularity Layer）

x402 是一个 **Web3 支付层**，它支持 AI 代理执行以下操作：
- 💰 使用 USDC 支付 API 访问费用
- 🚀 部署可盈利的 API 端点
- 🔍 通过市场发现服务
- 📊 管理 API 端点及信用额度

**支持的网络：** Base（EVM）• Solana  
**货币：** USDC  
**协议：** HTTP 402（需要支付）

---

## 快速入门

### 1. 安装依赖项
```bash
pip install -r {baseDir}/requirements.txt
```

### 2. 设置钱包
```bash
# For Base (EVM)
export PRIVATE_KEY="0x..."
export WALLET_ADDRESS="0x..."

# For Solana (optional)
export SOLANA_SECRET_KEY="[1,2,3,...]"  # JSON array
```

---

## 脚本概述

### 🛒 消费者模式（购买服务）

| 脚本 | 功能 |
|--------|---------|
| `pay_base.py` | 在 Base 网络上为 API 端点支付费用 |
| `pay_solana.py` | 在 Solana 网络上为 API 端点支付费用 |
| `consume_credits.py` | 使用预购买的信用额度（快速支付） |
| `consume_product.py` | 购买数字产品（文件） |
| `check_credits.py` | 查看信用额度余额 |
| `recharge_credits.py` | 为 API 端点购买信用额度包 |
| `discover_marketplace.py` | 浏览可用服务 |

### 🏭 提供者模式（出售服务）

| 脚本 | 功能 |
|--------|---------|
| `create_endpoint.py` | 部署新的可盈利 API 端点（费用为 5 美元） |
| `manage_endpoint.py` | 查看/更新你的 API 端点 |
| `topup_endpoint.py` | 为你的 API 端点充值信用额度 |
| `list_on_marketplace.py` | 公开发布你的 API 端点 |

---

## 消费者操作流程

### A. 按请求付费（推荐方式）

```bash
# Pay with Base (EVM) - 100% reliable
python {baseDir}/scripts/pay_base.py https://api.x402layer.cc/e/weather-data

# Pay with Solana - includes retry logic
python {baseDir}/scripts/pay_solana.py https://api.x402layer.cc/e/weather-data
```

### B. 基于信用额度的访问（最快方式）

预先购买信用额度，实现即时访问（无需等待区块链处理时间）：
```bash
# Check your balance
python {baseDir}/scripts/check_credits.py weather-data

# Buy credits (consumer purchasing credits)
python {baseDir}/scripts/recharge_credits.py weather-data pack_100

# Use credits for instant access
python {baseDir}/scripts/consume_credits.py https://api.x402layer.cc/e/weather-data
```

### C. 发现服务

```bash
# Browse all services
python {baseDir}/scripts/discover_marketplace.py

# Search by keyword
python {baseDir}/scripts/discover_marketplace.py search weather
```

---

## 提供者操作流程

### A. 创建 API 端点（一次性费用 5 美元）

部署你自己的可盈利 API：
```bash
python {baseDir}/scripts/create_endpoint.py my-api "My AI Service" https://api.example.com 0.01
```

包含 20,000 个测试信用额度。

### B. 管理你的 API 端点

```bash
# List your endpoints
python {baseDir}/scripts/manage_endpoint.py list

# View stats
python {baseDir}/scripts/manage_endpoint.py stats my-api

# Update price
python {baseDir}/scripts/manage_endpoint.py update my-api --price 0.02
```

### C. 为你的 API 端点充值信用额度

为你的 API 端点补充信用额度：
```bash
python {baseDir}/scripts/topup_endpoint.py my-api 10  # Add $10 worth
```

> 注意：此操作与 `recharge_credits.py` 的功能不同，`recharge_credits.py` 是为消费者设计的。

### D. 在市场上发布你的 API 端点

让你的 API 端点被公众发现：
```bash
python {baseDir}/scripts/list_on_marketplace.py my-api --category ai --description "AI-powered analysis"
```

---

## 支付技术细节

### Base（EVM） - 使用 EIP-712 签名

使用 USDC 的 `TransferWithAuthorization`（EIP-3009）：
- 对付款方来说无需支付网络费用（无需支付“Gas”）
- 由中介在链上完成结算
- 100% 可靠

### Solana - 使用版本化交易（Versioned Transactions）

使用 `VersionedTransaction` 和 `MessageV0` 协议：
- 由中介支付网络费用（费用来自 `extra.feePayer`）
- 使用 SPL 令牌的 `TransferChecked` 指令
- 成功率约为 75%（包含重试机制）

---

## 环境配置参考

| 变量 | 必需条件 | 说明 |
|----------|--------------|-------------|
| `PRIVATE_KEY` | Base 网络支付 | EVM 私钥（格式：0x...） |
| `WALLET_ADDRESS` | 所有操作 | 你的钱包地址 |
| `SOLANA_SECRET_KEY` | Solana 网络支付 | Solana 的秘密密钥（JSON 字符串格式） |

---

## API 基本地址

- **API 端点：** `https://api.x402layer.cc/e/{slug}` |
- **市场：** `https://api.x402layer.cc/api/marketplace` |
- **信用额度：** `https://api.x402layer.cc/api/credits/*` |
- **代理 API：** `https://api.x402layer.cc/agent/*`

---

## 参考资源

- 📖 **文档：** [studio.x402layer.cc/docs/agentic-access/openclaw-skill](https://studio.x402layer.cc/docs/agentic-access/openclaw-skill) |
- 💻 **GitHub 文档：** [github.com/ivaavimusic/SGL_DOCS_2025](https://github.com/ivaavimusic/SGL_DOCS_2025) |
- 🐦 **OpenClaw：** [x.com/openclaw](https://x.com/openclaw) |
- 🌐 **x402 Studio：** [studio.x402layer.cc](https://studio.x402layer.cc)

---

## 已知问题

⚠️ **Solana 网络的支付成功率约为 75%，这主要是由于中介方的费用结算系统存在问题。`pay_solana.py` 脚本中包含了重试逻辑。**Base（EVM）网络的支付方式 100% 可靠**，建议在生产环境中使用。