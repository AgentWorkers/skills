---
name: x402-layer
version: 1.1.3
description: 此技能适用于以下场景：用户请求“创建 x402 终端点”、“部署可盈利的 API”、“使用 USDC 支付 API 费用”、“检查 x402 信用点数”、“消耗 API 信用点数”、“在市场上列出终端点”、“购买 API 信用点数”、“为终端点充值”、“浏览 x402 市场”、使用“Coinbase Agentic 钱包（AWAL）”，或在 Base 或 Solana 网络上管理 x402 Singularity Layer 操作。
homepage: https://studio.x402layer.cc/docs/agentic-access/openclaw-skill
metadata:
  clawdbot:
    emoji: "⚡"
    homepage: https://studio.x402layer.cc
    os:
      - linux
      - darwin
    requires:
      bins:
        - python3
      env:
        # Core credentials (required for payments)
        - WALLET_ADDRESS
        - PRIVATE_KEY
        # Solana payments (required for Solana network)
        - SOLANA_SECRET_KEY
        # Provider operations (required for endpoint management)
        - X_API_KEY
        - API_KEY
        # AWAL mode (optional - for Coinbase Agentic Wallet)
        - X402_USE_AWAL
        - X402_AUTH_MODE
        - X402_PREFER_NETWORK
        - AWAL_PACKAGE
        - AWAL_BIN
        - AWAL_FORCE_NPX
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
- 📊 管理 API 端点及剩余信用额度

**支持的网络：** Base（EVM）• Solana  
**货币：** USDC  
**协议：** HTTP 402（要求支付）

---

## 快速入门

### 1. 安装依赖项
```bash
pip install -r {baseDir}/requirements.txt
```

### 2. 设置钱包（选择一种模式）

#### 选项 A：私钥（现有模式）
```bash
# For Base (EVM)
export PRIVATE_KEY="0x..."
export WALLET_ADDRESS="0x..."

# For Solana (optional)
export SOLANA_SECRET_KEY="[1,2,3,...]"  # JSON array
```

#### 选项 B：Coinbase Agentic 钱包（AWAL）

对于不需要暴露私钥的 Base 网络支付，可以使用 Coinbase Agentic 钱包：
```bash
# First, install and set up AWAL (one-time setup)
npx skills add coinbase/agentic-wallet-skills

# Then enable AWAL mode for this skill
export X402_USE_AWAL=1
```

> **注意**：请参阅 [Coinbase AWAL 文档](https://docs.cdp.coinbase.com/agentic-wallet/welcome) 以获取完整的设置说明。您需要使用 USDC 为 AWAL 钱包进行身份验证并充值。

配置完成后，所有 Base 网络的支付脚本将自动使用该钱包，而不再使用私钥。

---

## ⚠️ 安全提示

> **重要提示**：此功能涉及处理用于签署区块链交易的私钥。
>
- **切勿使用您的主托管钱包**——请创建一个仅用于存储少量资金的专用钱包。
- **私钥仅在本地使用**——它们仅用于本地签名交易，不会被传输。
- **签名后的数据会被发送到 `api.x402layer.cc`——支付签名和钱包地址会用于完成支付。
- **测试时**：请使用临时钱包，并确保其中包含至少 1-5 美元的 USDC。
- **API 密钥**：创建 API 端点后，请妥善保管返回的 API 密钥。
- **代码审核**：所有脚本均位于 `scripts/` 目录中，可供审核。

---

## 脚本概览

### 🛒 消费者模式（购买服务）

| 脚本 | 功能 |
|--------|---------|
| `pay_base.py` | 在 Base 网络上支付 API 端点的费用 |
| `pay_solana.py` | 在 Solana 网络上支付 API 端点的费用 |
| `consume_credits.py` | 使用预购买的信用额度（快速支付） |
| `consume_product.py` | 购买数字产品（文件） |
| `awal_cli.py` | 运行 Coinbase Agentic 钱包的 CLI 命令（身份验证、浏览市场、支付、发现服务） |
| `check_credits.py` | 检查您的信用额度余额 |
| `recharge_credits.py | 为 API 端点充值信用额度 |
| `discover_marketplace.py` | 浏览可用服务 |

### 🏭 提供者模式（出售服务）

| 脚本 | 功能 |
|--------|---------|
| `create_endpoint.py` | 部署新的可盈利 API 端点（费用为 1 美元） |
| `manage_endpoint.py` | 查看/更新您的 API 端点 |
| `topup_endpoint.py | 为 API 端点充值信用额度 |
| `list_on_marketplace.py` | 在市场上更新您的服务列表 |

---

## 安全性：API 密钥验证

> **重要提示**：创建 API 端点时，x402 会作为您的代理服务器。您必须确保所有请求都来自 x402。
1. **获取 API 密钥**：通过运行 `create_endpoint.py` 生成。
2. **验证请求头**：您的服务器必须在每个请求中检查以下头部信息：
   ```http
   x-api-key: <YOUR_API_KEY>
   ```
   如果头部信息缺失或错误，请求将被拒绝（返回 401 Unauthorized 错误）。

---

## 信用额度系统的工作原理

> **警告**：**请注意**，这些信用额度是不可用于测试的！每次 API 请求都会消耗信用额度。

### 流程示意图
```
User pays $0.01 → Your wallet receives payment → 1 credit deducted from your endpoint
```

### 经济模型

| 项目 | 价格 |
|------|-------|
| **创建费用** | 1 美元（一次性费用） |
| **初始信用额度** | 4,000 信用额度 |
| **充值费率** | 每 1 美元充值 500 信用额度 |
| **消耗规则** | 每次 API 请求消耗 1 信用额度 |
| **收益** | 您自行设定的每次调用价格 |

### 示例

1. **创建 API 端点**：支付 1 美元，获得 4,000 信用额度。
2. **设置价格**：每次调用 0.01 美元。
3. **用户调用 1,000 次**：您将获得 10 美元的收益，同时消耗 1,000 信用额度。
4. **剩余信用额度**：19,000 信用额度 + 10 美元的收益。
5. **信用额度不足？** 使用 `topup_endpoint.py` 进行充值。

### 信用额度耗尽时会发生什么？

API 端点将 **停止服务** 并返回错误。用户需要重新充值才能继续使用。

---

## 消费者流程

### A. 按次付费（推荐方式）
```bash
# Pay with Base (EVM) - 100% reliable
python {baseDir}/scripts/pay_base.py https://api.x402layer.cc/e/weather-data

# Pay with Solana - includes retry logic
python {baseDir}/scripts/pay_solana.py https://api.x402layer.cc/e/weather-data

# Pay with Coinbase Agentic Wallet (AWAL)
python {baseDir}/scripts/awal_cli.py pay-url https://api.x402layer.cc/e/weather-data
```

### B. 基于信用额度的访问（最快方式）

预先购买信用额度，以实现无延迟的即时访问：
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

# AWAL bazaar discovery
python {baseDir}/scripts/awal_cli.py run bazaar list
```

---

## 提供者流程

### A. 创建 API 端点（一次性费用 1 美元）

部署您的可盈利 API：
**基本模式（不显示在市场上）：**
```bash
python {baseDir}/scripts/create_endpoint.py my-api "My AI Service" https://api.example.com 0.01 --no-list
```

**在市场上展示（推荐模式）：**
```bash
python {baseDir}/scripts/create_endpoint.py my-api "My AI Service" https://api.example.com 0.01 \
    --category ai \
    --description "AI-powered data analysis API" \
    --logo https://example.com/logo.png \
    --banner https://example.com/banner.jpg
```

**可用类别：** `ai`、`data`、`finance`、`utility`、`social`、`gaming`

> **注意**：请保存 `API 密钥**，并使用它来保护您的服务器安全。

> ⚠️ **重要说明**：
- **创建费用**：1 美元（一次性费用），包含 4,000 信用额度（非测试信用额度！）
- **消耗规则**：每次调用您的 API 会消耗 1 信用额度。
- **信用额度耗尽**：API 端点将停止服务，需要重新充值。
- **充值方式**：使用 `topup_endpoint.py` 为 API 端点充值信用额度（1 美元可充值 500 信用额度）。
- **收益**：用户的支付金额会直接进入您的钱包，然后从信用额度中扣除 1 信用额度。

### B. 管理 API 端点

```bash
# List your endpoints
python {baseDir}/scripts/manage_endpoint.py list

# View stats
python {baseDir}/scripts/manage_endpoint.py stats my-api

# Update price
python {baseDir}/scripts/manage_endpoint.py update my-api --price 0.02
```

### C. 为 API 端点充值（保持服务运行）

您的 API 端点每次请求会消耗 1 信用额度。当信用额度耗尽时，服务将停止。请使用 `topup_endpoint.py` 进行充值。

> ⚠️ **注意**：`topup_endpoint.py` 专供提供者使用，用于为自己的 API 端点充值。
`recharge_credits.py` 用于消费者为其他人的 API 端点充值信用额度。

### D. 在市场上展示服务

您可以在创建 API 端点时**立即**或在之后**单独进行市场展示：
**选项 1：创建时展示**（推荐）：
```bash
python {baseDir}/scripts/create_endpoint.py my-api "My API" https://api.example.com 0.01 \
    --category ai \
    --description "AI-powered analysis" \
    --logo https://example.com/logo.png \
    --banner https://example.com/banner.jpg
```

**选项 2：创建后展示**（后续更新）：
```bash
# List or update marketplace listing
python {baseDir}/scripts/list_on_marketplace.py my-api \
    --category ai \
    --description "AI-powered analysis" \
    --logo https://example.com/logo.png \
    --banner https://example.com/banner.jpg

# Unlist from marketplace
python {baseDir}/scripts/list_on_marketplace.py my-api --unlist
```

> **提示**：可以使用 `list_on_marketplace.py` 随时更新服务信息（更改类别、描述或图片），无需重新创建 API 端点。

---

## 支付技术细节

### Base（EVM） - 使用 EIP-712 签名

- 支持使用 USDC 和 `TransferWithAuthorization`（EIP-3009）协议；
- 对支付方来说无需支付 gas 费用；
- 由第三方中介在链上完成结算，可靠性高达 100%。

### Solana - 使用版本化交易（Versioned Transactions）

- 使用 `VersionedTransaction` 和 `MessageV0` 协议；
- 由中介支付 gas 费用（费用来自 `extra.feePayer`）；
- 成功率约为 75%（包含重试机制）。

---

## 环境配置参考

| 变量 | 必需条件 | 说明 |
|----------|--------------|-------------|
| `PRIVATE_KEY` | Base 网络支付（私钥模式） | EVM 私钥（格式：0x...） |
| `WALLET_ADDRESS` | 所有操作 | 您的钱包地址 |
| `SOLANA_SECRET_KEY` | Solana 网络支付 | Solana 的秘密密钥（JSON 字符串格式） |
| `X402_USE_AWAL` | AWAL 模式 | 设置为 1 以启用 Coinbase Agentic 钱包 |
| `X402_AUTH_MODE` | 认证方式（可选） | `auto`、`private-key` 或 `awal`（默认：auto） |
| `X402_PREFER_NETWORK` | 支持的网络（可选） | `base` 或 `solana`（默认：base） |
| `AWAL_PACKAGE` | AWAL 模式（可选） | AWAL CLI 的 NPM 包/版本（默认：`awal@1.0.0`） |
| `AWAL_BIN` | AWAL 模式（可选） | 预安装的 AWAL 执行文件路径/名称 |
| `AWAL_FORCE_NPX` | AWAL 模式（可选） | 设置为 1 以强制使用 npx 命令行工具 |

---

## API 基础地址

- **API 端点**：`https://api.x402layer.cc/e/{slug}` |
- **市场**：`https://api.x402layer.cc/api/marketplace` |
- **信用额度**：`https://api.x402layer.cc/api/credits/*` |
- **代理 API**：`https://api.x402layer.cc/agent/*`

---

## 相关资源

- 📖 **文档**：[studio.x402layer.cc/docs/agentic-access/openclaw-skill](https://studio.x402layer.cc/docs/agentic-access/openclaw-skill)
- 💻 **GitHub 文档**：[github.com/ivaavimusic/SGL_DOCS_2025](https://github.com/ivaavimusic/SGL_DOCS_2025)
- 🐦 **OpenClaw**：[x.com/openclaw](https://x.com/openclaw)
- 🌐 **x402 Studio**：[studio.x402layer.cc](https://studio.x402layer.cc)

---

## 已知问题

⚠️ 由于中介方的费用处理问题，Solana 网络的支付成功率约为 75%。`pay_solana.py` 脚本中包含了重试逻辑。建议在生产环境中使用 Base（EVM）网络进行支付，因为其可靠性为 100%。