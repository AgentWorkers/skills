---
name: kaspa-wallet
description: >
  Simple wallet for Kaspa blockchain. Send KAS, check balances, generate payment URIs.
  Self-custody CLI wallet with JSON output for automation.
keywords:
  - kaspa
  - kas
  - wallet
  - payments
  - transfer
  - balance
  - cryptocurrency
  - blockdag
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - Task
user-invocable: true
---

# Kaspa 钱包技能

这是一个用于 Kaspa 区块链的简单自托管钱包。

## 概述

```
┌─────────────────────────────────────────────────────────┐
│                     KASPA WALLET                        │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │   Balance   │  │    Send     │  │  Payment URIs   │ │
│  │   Check     │  │    KAS      │  │   Generator     │ │
│  └─────────────┘  └─────────────┘  └─────────────────┘ │
│           │                │                   │        │
│           └────────────────┴───────────────────┘        │
│                         │                               │
│              ┌──────────▼──────────┐                    │
│              │   Kaspa Python SDK  │                    │
│              │   (wRPC Client)     │                    │
│              └─────────────────────┘                    │
│                         │                               │
│         ┌───────────────┼───────────────┐               │
│         ▼               ▼               ▼               │
│    ┌─────────┐    ┌──────────┐    ┌──────────┐         │
│    │ Mainnet │    │ Testnet  │    │  Custom  │         │
│    │  wRPC   │    │   wRPC   │    │   RPC    │         │
│    └─────────┘    └──────────┘    └──────────┘         │
└─────────────────────────────────────────────────────────┘
```

## 功能

| 功能 | 描述 |
|---------|-------------|
| **发送 KAS** | 将 KAS 转移到任何 Kaspa 地址 |
| **余额查询** | 查询任何地址的余额 |
| **支付 URI** | 生成 `kaspa:` 格式的支付请求 URI |
| **费用估算** | 获取当前的网络费用等级 |
| **网络信息** | 检查节点同步状态和区块 |
| **钱包生成** | 生成新的助记词 |

## 快速入门

### 安装

```bash
python3 install.py
```

**要求：** Python 3.8 及以上版本，并安装了 pip。支持 macOS、Linux 和 Windows 系统。

**安装故障排除：**
- 如果 pip 安装失败：手动执行 `pip install kaspa`，或尝试 `KASPA_PYTHON=python3.12 python3 install.py`
- 如果缺少 venv：在 Ubuntu/Debian 系统上运行 `sudo apt install python3-venv`
- 要重新安装：执行 `rm -rf .venv && python3 install.py`

### 命令行界面 (CLI) 使用方法

```bash
# Check balance
./kaswallet.sh balance
./kaswallet.sh balance kaspa:qrc8y...

# Send payment
./kaswallet.sh send kaspa:qrc8y... 0.5
./kaswallet.sh send kaspa:qrc8y... max

# Generate payment URI
./kaswallet.sh uri kaspa:q... 1.5 "coffee payment"

# Network info
./kaswallet.sh info

# Fee estimates
./kaswallet.sh fees

# Generate new wallet
./kaswallet.sh generate-mnemonic
```

### 支付 URI 格式

## 架构

```
kaspa-wallet/
├── SKILL.md
├── README.md
├── install.py              # Auto-installer with venv
├── kaswallet.sh            # CLI wrapper script
├── requirements.txt
└── scripts/
    └── kaswallet.py        # Main wallet logic
```

## 配置

```bash
# Environment variables (one required)
export KASPA_PRIVATE_KEY="64-character-hex-string"
# OR
export KASPA_MNEMONIC="your twelve or twenty four word seed phrase"

# Optional
export KASPA_NETWORK="mainnet"              # mainnet (default), testnet-10
export KASPA_RPC_URL="wss://..."            # Custom RPC endpoint
export KASPA_RPC_CONNECT_TIMEOUT_MS="30000" # Connection timeout (default: 15000)
```

## 核心功能

### 查询余额

```bash
./kaswallet.sh balance                    # Your wallet balance
./kaswallet.sh balance kaspa:qrc8y...     # Any address balance
```

**输出：**
```json
{"address": "kaspa:q...", "balance": "1.5", "sompi": "150000000", "network": "mainnet"}
```

### 发送 KAS

```bash
./kaswallet.sh send <address> <amount>           # Send specific amount
./kaswallet.sh send <address> max                # Send entire balance
./kaswallet.sh send <address> <amount> priority  # Priority fee tier
```

**成功输出：**
```json
{"status": "sent", "txid": "abc123...", "from": "kaspa:q...", "to": "kaspa:q...", "amount": "0.5", "fee": "0.0002"}
```

**错误输出：**
```json
{"error": "Storage mass exceeds maximum", "errorCode": "STORAGE_MASS_EXCEEDED", "hint": "...", "action": "consolidate_utxos"}
```

### 网络信息

```bash
./kaswallet.sh info
```

**输出：**
```json
{"network": "mainnet", "url": "wss://...", "blocks": 12345678, "synced": true, "version": "1.0.0"}
```

### 费用估算

```bash
./kaswallet.sh fees
```

**输出：**
```json
{"network": "mainnet", "low": {"feerate": 1.0, "estimatedSeconds": 60}, "economic": {...}, "priority": {...}}
```

### 生成新钱包

```bash
./kaswallet.sh generate-mnemonic
```

**输出：**
```json
{"mnemonic": "word1 word2 word3 ... word24"}
```

### 支付 URI

```bash
./kaswallet.sh uri                          # Your address
./kaswallet.sh uri kaspa:q... 1.5 "payment" # With amount and message
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `STORAGE_MASS_EXCEEDED` | 交易金额过小，无法满足当前未花费交易输出 (UTXOs) 的要求 | 先向自己发送 `max` 数量的 KAS 以合并交易输出 |
| `NO_UTXOS` | 没有可花费的交易输出 (UTXOs) | 等待交易确认或为钱包充值 |
| `INSUFFICIENT_FUNDS` | 余额不足 | 检查余额并减少转账金额 |
| `RPC_TIMEOUT` | 网络延迟 | 重试或增加请求超时时间 |
| `NO_CREDENTIALS` | 缺少钱包密钥 | 设置 `KASPA_PRIVATE_KEY` 或 `KASPA_MNEMONIC` |
| `SDK_NOT_INSTALLED` | 未安装 Kaspa SDK | 运行 `python3 install.py` |

## 支付流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Sender    │     │ Kaspa Wallet│     │  Recipient  │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │  1. Initiate      │                   │
       │──────────────────▶│                   │
       │                   │                   │
       │                   │  2. Execute       │
       │                   │  KAS Transfer     │
       │                   │─────────────────▶│
       │                   │                   │
       │                   │  3. Confirm       │
       │                   │◀──────────────────│
       │  4. Success       │                   │
       │◀──────────────────│                   │
       │                   │                   │
```

## 常见操作流程

### 合并未花费的交易输出 (解决 `STORAGE_MASS_EXCEEDED` 错误)

当发送失败并出现 `STORAGE_MASS_EXCEEDED` 错误时，可以执行以下操作：

```bash
# 1. Get your address
./kaswallet.sh balance
# Returns: {"address": "kaspa:qYOUR_ADDRESS...", ...}

# 2. Send max to yourself (consolidates UTXOs)
./kaswallet.sh send kaspa:qYOUR_ADDRESS... max

# 3. Now send the original amount (will work)
./kaswallet.sh send kaspa:qRECIPIENT... 0.5
```

### 查看交易状态

发送交易后，可以使用 `txid` 在区块浏览器中查询交易状态：
- 主网：`https://explorer.kaspa.org/txs/{txid}`
- 测试网：`https://explorer-tn10.kaspa.org/txs/{txid}`

### 切换网络

```bash
# Testnet
export KASPA_NETWORK="testnet-10"
./kaswallet.sh info

# Back to mainnet
export KASPA_NETWORK="mainnet"
./kaswallet.sh info
```

## 单位

- **KAS**：人类可读的单位（例如，1.5 KAS）
- **sompi**：最小单位，1 KAS = 100,000,000 sompi

所有命令输入都接受 KAS 作为单位。输出结果中会同时显示 KAS 和 sompi（如适用）。

## 安全注意事项

- **私钥**：切勿在日志或错误信息中泄露私钥 |
- **助记词**：仅通过环境变量传递 |
- **无磁盘存储**：钱包不存储任何凭证信息 |
- **每次操作都建立新的 RPC 连接** |
- **地址格式**：验证 Kaspa 地址（格式为 `kaspa:q...`）

## 与传统钱包的比较

| 功能 | 传统钱包 | Kaspa 钱包 CLI |
|---------|-------------------|------------------|
| 设置 | 需通过 GUI 安装 | 通过 `python3 install.py` 安装 |
| 用户界面 | 桌面应用程序 | 命令行界面 + JSON 格式输出 |
| 自动化程度 | 有限 | 全面（支持 JSON 解析） |
| 托管方式 | 不同 | 自主托管 |
| 适合代理服务器使用 | 不适用 | 适用 |

## 开发计划

- [ ] 生成地址的 QR 码 |
- [ ] 支持支付链接 |
- [ ] 提供交易历史记录 |
- [ ] 支持多地址操作 |
- [ ] 批量支付功能 |
- [ ] 集成 Telegram 机器人 |

## 资源

- [Kaspa 文档](https://docs.kaspa.org/) |
- [Kaspa 浏览器](https://explorer.kaspa.org/) |
- [kaspa-py SDK](https://github.com/aspect-build/kaspa-py)