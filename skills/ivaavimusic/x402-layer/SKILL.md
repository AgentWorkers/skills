---
name: x402-layer
version: 1.4.0
description: >
  **x402-layer** 功能帮助代理使用 USDC 为 API 支付费用，部署可盈利的 API 端点（monetized endpoints），管理信用点（credits）、Webhook 以及市场列表（marketplace listings），并在 Base、Ethereum、Polygon、BSC、Monad 和 Solana 网络上处理基于钱包的 ERC-8004 标准的注册、发现、管理和声誉管理（registration/discovery/reputation）相关操作。  
  当用户需要执行以下操作时，请使用此功能：  
  - 创建 x402 API 端点  
  - 部署可盈利的 API  
  - 使用 USDC 支付 API 费用  
  - 查看 x402 信用点余额  
  - 消耗 API 信用点  
  - 将 API 端点发布到市场  
  - 购买 API 信用点  
  - 为 API 端点充值  
  - 浏览 x402 API 市场  
  - 设置 Webhook  
  - 接收支付通知  
  - 管理 API 端点的 Webhook  
  - 验证 Webhook 支付  
  - 验证支付真实性  
  - 注册 ERC-8004 代理  
  - 注册 Solana 8004 代理  
  - 提交链上声誉反馈（on-chain reputation feedback）  
  - 为 ERC-8004 代理打分  
  - 使用 Coinbase Agentic Wallet (AWAL)  
  - 管理 Base、Ethereum、Polygon、BSC、Monad 或 Solana 网络上的 x402 Singularity Layer 相关操作。
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
# x402 单点智能层（Singularity Layer）

x402 是一个基于 Web3 的支付层，允许人类用户和代理出售/消费 API 服务及产品。本文档涵盖了整个单点智能层的生命周期，包括以下功能：
- 支付/消费服务
- 创建/管理/列出服务端点
- 接收并验证 Webhook 支付事件
- 注册代理并提交链上声誉反馈

**支持的网络**：Base、Ethereum、Polygon、BSC、Monad、Solana  
**货币**：USDC  
**协议**：HTTP 402（要求支付）

---

## 意图路由（Intent Routing）

请先使用以下路由脚本，然后再查阅相关参考文档。

| 用户意图 | 主要脚本 | 参考文档 |
|---|---|---|
| 支付/消费服务端点或产品 | `pay_base.py`, `pay_solana.py`, `consume_credits.py`, `consume_product.py` | `references/pay-per-request.md`, `references/credit-based.md` |
| 发现/搜索市场 | `discover_marketplace.py` | `references/marketplace.md` |
| 创建/编辑/列出服务端点 | `create_endpoint.py`, `manage_endpoint.py`, `list_on_marketplace.py`, `topup_endpoint.py` | `references/agentic-endpoints.md`, `references/marketplace.md` |
| 配置/验证 Webhook | `manage_webhook.py`, `verify_webhook_payment.py` | `references/webhooks-verification.md` |
| 注册/发现/管理代理（ERC-8004/Solana-8004） | `register_agent.py`, `listAgents.py`, `list_my_endpoints.py`, `update_agent.py`, `submit_feedback.py` | `references/agent-registry-reputation.md` |

---

## 快速入门

### 1) 安装所需依赖项
```bash
pip install -r {baseDir}/requirements.txt
```

### 2) 选择钱包模式

**选项 A**: 使用私钥  
```bash
export PRIVATE_KEY="0x..."
export WALLET_ADDRESS="0x..."
# Solana optional
export SOLANA_SECRET_KEY="base58-or-[1,2,3,...]"
```

**选项 B**: 使用 Coinbase 的 AWAL（预付费模式）  
```bash
# Install Coinbase AWAL skill (shortcut)
npx skills add coinbase/agentic-wallet-skills
export X402_USE_AWAL=1
```

对于首次使用 ERC-8004 协议的代理注册，建议使用私钥模式。AWAL 模式也适用于 x402 的支付流程。

**安全提示**：脚本仅读取显式配置的环境变量，`.env` 文件不会被自动加载。

---

## 脚本清单

### 消费者（Consumer）  
| 脚本 | 功能 |
|---|---|
| `pay_base.py` | 在 Base 网络上执行支付 |
| `pay_solana.py` | 在 Solana 网络上执行支付 |
| `consume_credits.py` | 使用信用额度进行消费 |
| `consume_product.py` | 购买数字产品或文件 |
| `check_credits.py` | 检查信用余额 |
| `recharge_credits.py` | 购买信用额度包 |
| `discover_marketplace.py` | 浏览/搜索市场 |
| `awal_cli.py` | 运行与 AWAL 相关的授权/支付/发现命令 |

### 提供者（Provider）  
| 脚本 | 功能 |
|---|---|
| `create_endpoint.py` | 部署服务端点（费用为 1 USDC，包含 4,000 个信用额度） |
| `manage_endpoint.py` | 列出/更新服务端点设置 |
| `topup_endpoint.py | 为服务端点充值信用额度 |
| `list_on_marketplace.py` | 在市场上列出/取消列出服务端点 |
| `manage_webhook.py` | 设置/删除/验证服务端点的 Webhook 链接 |
| `verify_webhook_payment.py` | 验证 Webhook 签名及支付凭证的真实性（使用 PyJWT/JWKS） |

### 代理注册与声誉管理  
| 脚本 | 功能 |
|---|---|
| `register_agent.py` | 注册 ERC-8004/Solana-8004 代理，支持添加图片、版本信息及绑定服务端点 |
| `list_agents.py` | 列出由当前钱包或关联的仪表板用户拥有的 ERC-8004 代理 |
| `list_my_endpoints.py` | 查看可绑定到 ERC-8004 代理的平台服务端点 |
| `update_agent.py` | 更新 ERC-8004/Solana-8004 代理的元数据、可见性及服务端点绑定信息 |
| `submit_feedback.py` | 提交链上声誉反馈 |

---

## 核心安全要求

### 原始服务器的 API 密钥验证（强制要求）
当 x402 将请求代理到您的原始服务器时，必须进行以下验证：
```http
x-api-key: <YOUR_API_KEY>
```
如果缺少或验证失败的请求将被拒绝。

### 信用额度机制（提供者端）
- 创建服务端点的费用：1 USDC
- 初始信用额度：4,000 个信用额度
- 充值费率：每 1 USDC 可充值 500 个信用额度
- 每次请求消耗 1 个信用额度
- 信用额度耗尽后，服务端点将停止服务，直至重新充值

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

### C) 创建和管理服务端点  
```bash
python {baseDir}/scripts/create_endpoint.py my-api "My API" https://api.example.com 0.01
python {baseDir}/scripts/manage_endpoint.py list
python {baseDir}/scripts/manage_endpoint.py update my-api --price 0.02
python {baseDir}/scripts/topup_endpoint.py my-api 10
```

### D) 在市场上列出/更新服务端点  
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

**Webhook 验证辅助工具**：
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
python {baseDir}/scripts/list_my_endpoints.py

python {baseDir}/scripts/register_agent.py \
  "My Agent" \
  "Autonomous service agent" \
  --network baseSepolia \
  --image https://example.com/agent.png \
  --version 1.4.0 \
  --tag finance \
  --tag automation \
  --endpoint-id <ENDPOINT_UUID> \
  --custom-endpoint https://api.example.com/agent

python {baseDir}/scripts/list_agents.py --network baseSepolia

python {baseDir}/scripts/update_agent.py \
  --network baseSepolia \
  --agent-id 123 \
  --version 1.4.1 \
  --tag finance \
  --tag automation \
  --endpoint-id <ENDPOINT_UUID> \
  --public

# The same EVM flow also supports:
#   --network ethereum
#   --network polygon
#   --network bsc
#   --network monad

python {baseDir}/scripts/submit_feedback.py \
  --network base \
  --agent-id 123 \
  --rating 5 \
  --comment "High quality responses"
```

---

## 参考文档

仅加载用户任务所需的相关文档：
- `references/pay-per-request.md`：EIP-712/Solana 的支付流程及底层签名细节。
- `references/credit-based.md`：信用额度的购买与消费规则及示例。
- `references/marketplace.md`：市场端点的搜索、列出及取消列表功能。
- `references/agentic-endpoints.md`：服务端点的创建、充值及状态管理 API。
- `references/webhooks-verification.md`：Webhook 事件的验证方法及签名真实性检查。
- `references/agent-registry-reputation.md`：ERC-8004/Solana-8004 代理的注册、发现、管理及反馈规则。
- `references/payment-signing.md`：签名域、签名类型及头部数据格式的详细信息。

---

## 环境配置变量

| 变量 | 必需条件 | 备注 |
|---|---|---|
| `PRIVATE_KEY` | 使用私钥模式时必需 | EVM 签名所需的私钥 |
| `WALLET_ADDRESS` | 大多数操作必需 | 主要钱包地址 |
| `SOLANA_SECRET_KEY` | 使用 Solana 私钥模式时必需 | 以 base58 编码的秘密密钥或 JSON 数组形式 |
| `SOLANA_WALLET_ADDRESS` | Solana 网络的备用地址 | 可选 |
| `WALLET_ADDRESS_secondARY` | 需要跨链操作时使用 | 可选 |
| `X402_USE_AWAL` | 是否使用 AWAL 模式 | 设置为 `1` |
| `X402_AUTH_MODE` | 授权方式 | `auto`, `private-key`, `awal` |
| `X402_PREFER_NETWORK` | 优先使用的网络 | `base`, `solana` |
| `X402_API_BASE` | API 基础地址 | 默认为 `https://api.x402layer.cc` |
| `X_API_KEY` / `API_KEY` | 服务端点/Webhook 管理所需的密钥 | 请根据实际情况设置 |
| `WORKER_FEEDBACK_API_KEY` | 用于处理声誉反馈的密钥 | 仅用于工作进程 |

---

## API 基本路径

- 服务端点：`https://api.x402layer.cc/e/{slug}`  
- 市场：`https://api.x402layer.cc/api/marketplace`  
- 信用额度相关 API：`https://api.x402layer.cc/api/credits/*`  
- 代理相关 API：`https://api.x402layer.cc/agent/*`

---

## 相关资源

- 文档：https://studio.x402layer.cc/docs/agentic-access/openclaw-skill  
- SDK 文档：https://studio.x402layer.cc/docs/developer/sdk-receipts  
- GitHub 代码仓库：https://github.com/ivaavimusic/SGL_DOCS_2025  
- x402 开发工具：https://studio.x402layer.cc  

---

## 注意事项

由于 Solana 网络的支付机制依赖于第三方支付处理方，其可靠性相对较低。在 `pay_solana.py` 脚本中请使用重试逻辑；在生产环境中建议优先使用 Base 网络。