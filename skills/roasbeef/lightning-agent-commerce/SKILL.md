---
name: commerce
description: 基于 Lightning Network 的端到端代理商业工作流程：当代理需要搭建完整的支付体系（包括 lnd、lnget 和 aperture），通过 L402 买卖数据，或实现代理之间的微支付时，可使用该流程。
user-invocable: false
---

# Agentic Commerce Toolkit

该插件为基于代理的Lightning Network商务应用提供了完整的工具集。三个核心功能协同工作，使代理能够使用L402协议在Lightning Network上发送和接收微支付。

## 组件

| 功能 | 用途 |
|-------|---------|
| **lnd** | 运行Lightning Terminal（包含litd、loop、pool和tapd组件） |
| **lnget** | 获取受L402保护的资源（数据购买） |
| **aperture** | 托管付费API端点（数据销售） |

## 完整设置流程

### 第1步：安装所有组件

```bash
# Install litd (Lightning Terminal — bundles lnd + loop + pool + tapd)
skills/lnd/scripts/install.sh

# Install lnget (Lightning HTTP client)
skills/lnget/scripts/install.sh

# Install aperture (L402 reverse proxy)
skills/aperture/scripts/install.sh
```

### 第2步：配置Lightning节点

```bash
# Start litd container (testnet by default)
skills/lnd/scripts/start-lnd.sh

# Create an encrypted wallet
skills/lnd/scripts/create-wallet.sh --mode standalone

# Verify node is running
skills/lnd/scripts/lncli.sh getinfo
```

### 第3步：为钱包充值

```bash
# Generate a Bitcoin address
skills/lnd/scripts/lncli.sh newaddress p2tr

# Send BTC to this address from an exchange or another wallet

# Verify balance
skills/lnd/scripts/lncli.sh walletbalance
```

### 第4步：打开通道

```bash
# Connect to a well-connected node (e.g., ACINQ, Bitfinex)
skills/lnd/scripts/lncli.sh connect <pubkey>@<host>:9735

# Open a channel
skills/lnd/scripts/lncli.sh openchannel --node_key=<pubkey> --local_amt=1000000

# Wait for channel to confirm (6 blocks)
skills/lnd/scripts/lncli.sh listchannels
```

### 第5步：配置lnget

```bash
# Initialize lnget config (auto-detects local lnd)
lnget config init

# Verify connection
lnget ln status
```

### 第6步：获取付费资源

```bash
# Fetch an L402-protected resource
lnget --max-cost 1000 https://api.example.com/paid-data

# Preview without paying
lnget --no-pay https://api.example.com/paid-data

# Check cached tokens
lnget tokens list
```

### 第7步：托管付费API端点（可选）

```bash
# Start your backend service
python3 -m http.server 8080 &

# Configure aperture to protect it
skills/aperture/scripts/setup.sh --insecure --port 8081

# Start the L402 paywall
skills/aperture/scripts/start.sh

# Other agents can now pay to access your endpoints
# lnget --max-cost 100 https://your-host:8081/api/data
```

## 代理之间的商务交易

自主代理商务交易的完整流程：

```
Agent A (buyer)                    Agent B (seller)
─────────────                      ─────────────
lnd node running                   lnd node running
  ↓                                  ↓
lnget fetches URL ──────────────→ aperture receives request
                                     ↓
                                   Returns 402 + invoice
  ↓
lnget pays invoice ─────────────→ lnd receives payment
  ↓                                  ↓
lnget retries with token ───────→ aperture validates token
                                     ↓
                                   Proxies to backend
  ↓                                  ↓
Agent A receives data ←──────────  Backend returns data
```

### 买家代理设置

```bash
# One-time setup
skills/lnd/scripts/install.sh
skills/lnget/scripts/install.sh
skills/lnd/scripts/start-lnd.sh
skills/lnd/scripts/create-wallet.sh --mode standalone
lnget config init

# Fund wallet and open channels (one-time)
skills/lnd/scripts/lncli.sh newaddress p2tr
# ... send BTC ...
skills/lnd/scripts/lncli.sh openchannel --node_key=<pubkey> --local_amt=500000

# Ongoing: fetch paid resources
lnget --max-cost 100 -q https://seller-api.example.com/api/data | jq .
```

### 卖家代理设置

```bash
# One-time setup
skills/lnd/scripts/install.sh
skills/aperture/scripts/install.sh
skills/lnd/scripts/start-lnd.sh
skills/lnd/scripts/create-wallet.sh --mode standalone

# Configure and start paywall
skills/aperture/scripts/setup.sh --port 8081 --insecure

# Start backend with content to sell
mkdir -p /tmp/api-data
echo '{"market_data": "..."}' > /tmp/api-data/data.json
cd /tmp/api-data && python3 -m http.server 8080 &

# Start aperture
skills/aperture/scripts/start.sh

# Buyers can now access:
# https://your-host:8081/api/data.json (100 sats per request)
```

## 成本管理

代理应始终控制自己的支出：

```bash
# Set a hard limit per request
lnget --max-cost 500 https://api.example.com/data

# Check cost before paying
lnget --no-pay --json https://api.example.com/data | jq '.invoice_amount_sat'

# Track spending via token list
lnget tokens list --json | jq '[.[] | .amount_paid_sat] | add'
```

## 安全性概述

| 组件 | 安全模型 |
|-----------|---------------|
| **钱包密码** | 存储在`~/.lnget/lnd/wallet-password.txt`文件中（权限设置为0600） |
| **种子助记词** | 存储在`~/.lnget/lnd/seed.txt`文件中（权限设置为0600） |
| **L402代币** | 按域名存储在`~/.lnget/tokens/<domain>/`目录下 |
| **lnd相关文件** | 标准的lnd文件存储在`~/.lnd/data/chain/...`目录下 |
| **Aperture数据库** | 使用SQLite数据库，存储在`~/.aperture/aperture.db`文件中 |

对于涉及大量资金的生产环境，建议使用仅查看模式的远程签名器容器。详情请参阅`lightning-security-module`组件。

## 停止所有服务

```bash
skills/aperture/scripts/stop.sh
skills/lnd/scripts/stop-lnd.sh
```