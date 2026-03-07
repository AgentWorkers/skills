---
name: x402-layer
version: 1.3.3
description: >
  **x402-layer** 功能帮助代理使用 USDC 支付 API 使用费，部署可盈利的 API 端点，管理信用额度、Webhook 以及市场列表，并在 Base/Solana 上处理 ERC-8004 相关的注册和信誉管理。  
  当用户需要执行以下操作时，请使用此功能：  
  - 创建 x402 API 端点  
  - 部署可盈利的 API  
  - 使用 USDC 支付 API 使用费  
  - 查看 x402 信用额度  
  - 消耗 API 信用额度  
  - 将 API 端点发布到市场  
  - 购买 API 信用额度  
  - 为 API 端点充值  
  - 浏览 x402 相关市场  
  - 设置 Webhook  
  - 接收支付通知  
  - 管理 API 端点的 Webhook  
  - 验证 Webhook 支付  
  - 验证支付的真实性  
  - 注册 ERC-8004 代理  
  - 注册 Solana 8004 代理  
  - 在链上提交信誉反馈  
  - 为 ERC-8004 代理打分  
  - 使用 Coinbase Agentic Wallet (AWAL)  
  - 在 Base 或 Solana 网络上管理 x402 相关操作。
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
        - WALLET_ADDRESS
        - PRIVATE_KEY
        - SOLANA_SECRET_KEY
        - X_API_KEY
        - API_KEY
        - WORKER_FEEDBACK_API_KEY
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
---
# x402 单点层（Singularity Layer）

x402 是一个 Web3 支付层，允许人类和代理出售/消费 API 和产品。  
本文档涵盖了整个单点层的生命周期，包括：  
- 支付/消费服务  
- 创建/管理/列出端点（endpoints）  
- 接收并验证 Webhook 支付事件  
- 注册代理并提交链上声誉反馈  

**支持的网络：** Base（EVM）、Solana  
**货币：** USDC  
**协议：** HTTP 402（需要支付）  

---

## 意图路由（Intent Routing）  
请先使用以下路由规则，然后再查阅相关参考文档。  

| 用户意图 | 主要脚本 | 参考文档 |  
|---|---|---|  
| 支付/消费端点或产品 | `pay_base.py`、`pay_solana.py`、`consume_credits.py`、`consume_product.py` | `references/pay-per-request.md`、`references/credit-based.md` |  
| 发现/搜索市场 | `discover_marketplace.py` | `references/marketplace.md` |  
| 创建/编辑/列出端点 | `create_endpoint.py`、`manage_endpoint.py`、`list_on_marketplace.py`、`topup_endpoint.py` | `references/agentic-endpoints.md`、`references/marketplace.md` |  
| 配置/验证 Webhook | `manage_webhook.py`、`verify_webhook_payment.py` | `references/webhooks-verification.md` |  
| 注册/评估代理（ERC-8004/Solana-8004） | `register_agent.py`、`submit_feedback.py` | `references/agent-registry-reputation.md` |  

---

## 快速入门  

### 1) 安装技能依赖项  
```bash
pip install -r {baseDir}/requirements.txt
```  

### 2) 选择钱包模式  
**选项 A：** 使用私钥  
```bash
export PRIVATE_KEY="0x..."
export WALLET_ADDRESS="0x..."
# Solana optional
export SOLANA_SECRET_KEY="[1,2,3,...]"
```  
**选项 B：** 使用 Coinbase AWAL（预付费模式）  
```bash
# Install Coinbase AWAL skill (shortcut)
npx skills add coinbase/agentic-wallet-skills
export X402_USE_AWAL=1
```  
**安全提示：** 脚本仅读取显式设置的环境变量。`.env` 文件不会被自动加载。  

---

## 脚本清单  
### 消费者（Consumers）  
| 脚本 | 功能 |  
|---|---|  
| `pay_base.py` | 在 Base 网络上支付 |  
| `pay_solana.py` | 在 Solana 网络上支付 |  
| `consume_credits.py` | 使用信用点数进行消费 |  
| `consume_product.py` | 购买数字产品/文件 |  
| `check_credits.py` | 检查信用余额 |  
| `recharge_credits.py` | 购买信用点数包 |  
| `discover_marketplace.py` | 浏览/搜索市场 |  
| `awal_cli.py` | 运行预付费相关的命令（认证/支付/搜索） |  

### 提供者（Providers）  
| 脚本 | 功能 |  
|---|---|  
| `create_endpoint.py` | 部署端点（一次费用 1 美元，包含 4,000 个信用点数） |  
| `manage_endpoint.py` | 列出/更新端点设置 |  
| `topup_endpoint.py` | 为端点充值信用点数 |  
| `list_on_marketplace.py` | 在市场上列出/取消列出端点 |  
| `manage_webhook.py` | 设置/删除/验证 Webhook URL |  
| `verify_webhook_payment.py` | 验证 Webhook 签名及交易收据的真实性（PyJWT/JWKS） |  

### 代理注册与声誉系统（Agent Registry + Reputation）  
| 脚本 | 功能 |  
|---|---|  
| `register_agent.py` | 注册 ERC-8004/Solana-8004 代理 |  
| `submit_feedback.py` | 提交链上声誉反馈 |  

---

## 核心安全要求  
### 原始服务器的 API 密钥验证（强制要求）  
当 x402 将流量代理到您的原始服务器时，必须进行以下验证：  
```http
x-api-key: <YOUR_API_KEY>
```  
如果缺少或验证不通过，请拒绝请求。  

### 信用点数经济模型（Provider Side）  
- 创建端点：一次性费用 1 美元  
- 初始信用点数：4,000  
- 充值费率：每 1 美元可充 500 个信用点数  
- 每次请求消耗 1 个信用点数  
- 信用点数归零后，端点将停止服务，直至重新充值  

---

## 快速操作指南  
### A) 支付与消费  
```bash
python {baseDir}/scripts/pay_base.py https://api.x402layer.cc/e/weather-data
python {baseDir}/scripts/pay_solana.py https://api.x402layer.cc/e/weather-data
python {baseDir}/scripts/consume_credits.py https://api.x402layer.cc/e/weather-data
```  

### B) 发现/搜索市场  
```bash
python {baseDir}/scripts/discover_marketplace.py
python {baseDir}/scripts/discover_marketplace.py search weather
```  

### C) 创建和管理端点  
```bash
python {baseDir}/scripts/create_endpoint.py my-api "My API" https://api.example.com 0.01
python {baseDir}/scripts/manage_endpoint.py list
python {baseDir}/scripts/manage_endpoint.py update my-api --price 0.02
python {baseDir}/scripts/topup_endpoint.py my-api 10
```  

### D) 在市场上列出/更新端点  
```bash
python {baseDir}/scripts/list_on_marketplace.py my-api \
  --category ai \
  --description "AI-powered analysis" \
  --logo https://example.com/logo.png \
  --banner https://example.com/banner.jpg
```  

### E) 设置 Webhook 及验证其真实性  
```bash
python {baseDir}/scripts/manage_webhook.py set my-api https://my-server.com/webhook
python {baseDir}/scripts/manage_webhook.py info my-api
python {baseDir}/scripts/manage_webhook.py remove my-api
```  
**Webhook 验证辅助工具：**  
```bash
python {baseDir}/scripts/verify_webhook_payment.py \
  --body-file ./webhook.json \
  --signature 't=1700000000,v1=<hex>' \
  --secret '<YOUR_SIGNING_SECRET>' \
  --required-source-slug my-api \
  --require-receipt
```  

### F) 代理注册与声誉管理  
```bash
python {baseDir}/scripts/register_agent.py \
  "My Agent" \
  "Autonomous service agent" \
  "https://api.example.com/agent" \
  --network baseSepolia

python {baseDir}/scripts/submit_feedback.py \
  --network base \
  --agent-id 123 \
  --rating 5 \
  --comment "High quality responses"
```  

---

## 参考文档  
仅加载用户任务所需的内容：  
- `references/pay-per-request.md`：EIP-712/Solana 的支付流程及底层签名细节  
- `references/credit-based.md`：信用点数的购买与消费规则及示例  
- `references/marketplace.md`：市场端点的搜索/列出/取消列出功能  
- `references/agentic-endpoints.md`：端点的创建、充值及状态管理 API  
- `references/webhooks-verification.md`：Webhook 事件、签名验证及交易收据核对  
- `references/agent-registry-reputation.md`：ERC-8004/Solana-8004 代理的注册与反馈规则  
- `references/payment-signing.md`：签名域、签名类型及头部负载的详细信息  

---

## 环境变量参考  
| 变量 | 必需条件 | 备注 |  
|---|---|---|  
| `PRIVATE_KEY` | 使用 Base 网络时 | EVM 网络的私钥 |  
| `WALLET_ADDRESS` | 大多数操作 | 主钱包地址 |  
| `SOLANA_SECRET_KEY` | 使用 Solana 网络时 | Solana 网络的私钥（JSON 字符串形式） |  
| `SOLANA_WALLET_ADDRESS` | Solana 网络的备用地址 | 可选 |  
| `WALLET_ADDRESS_secondARY` | 使用双链模式时 | 可选 |  
| `X402_USE_AWAL` | 是否使用预付费模式 | 设置为 `1` |  
| `X402_AUTH_MODE` | 认证方式 | `auto`、`private-key`、`awal` |  
| `X402_PREFER_NETWORK` | 优先使用的网络 | `base` 或 `solana` |  
| `X402_API_BASE` | API 基本地址 | 默认为 `https://api.x402layer.cc` |  
| `X_API_KEY` / `API_KEY` | 提供者端点/Webhook 管理所需的密钥 |  
| `WORKER_REGISTRATION_API_KEY` | 代理注册所需的密钥 |  
| `WORKER_FEEDBACK_API_KEY` | 用于处理声誉反馈的密钥 |  

---

## API 基本路径  
- 端点：`https://api.x402layer.cc/e/{slug}`  
- 市场：`https://api.x402layer.cc/api/marketplace`  
- 信用点数：`https://api.x402layer.cc/api/credits/*`  
- 代理相关 API：`https://api.x402layer.cc/agent/*`  

---

## 相关资源  
- 文档：`https://studio.x402layer.cc/docs/agentic-access/openclaw-skill`  
- SDK 文档：`https://studio.x402layer.cc/docs/developer/sdk-receipts`  
- GitHub 文档仓库：`https://github.com/ivaavimusic/SGL_DOCS_2025`  
- x402 Studio：`https://studio.x402layer.cc`  

---

## 已知问题  
由于 Solana 网络的支付系统依赖于第三方费用支付服务，其可靠性相对较低。在 `pay_solana.py` 脚本中请使用重试逻辑；在生产环境中建议优先使用 Base 网络。