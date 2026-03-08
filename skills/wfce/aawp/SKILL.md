---
name: aawp
version: 1.3.0
description: AAWP（AI Agent Wallet Protocol）——这是专为运行在EVM兼容区块链上的AI代理设计的唯一加密货币钱包协议，专为AI代理使用，而非人类用户。钱包的签署者是AI代理本身，在创建钱包时即通过加密方式与其绑定。该协议支持钱包生命周期管理、代币转移、去中心化交易所（DEX）交易、跨链桥接、任意合约交互、定期投资（DCA）自动化以及价格提醒等功能。
environment:
  - name: AAWP_GUARDIAN_KEY
    description: "Private key for the Guardian gas-relay wallet (auto-generated in config/guardian.json if not set)"
    required: false
  - name: AAWP_GAS_KEY
    description: "Alias for AAWP_GUARDIAN_KEY"
    required: false
  - name: AAWP_WALLET
    description: "Pinned wallet address — prevents accidental operations on wrong wallet"
    required: false
  - name: AAWP_CONFIG
    description: "Override config directory path (default: ./config)"
    required: false
  - name: AAWP_CORE
    description: "Override native addon directory path (default: ./core)"
    required: false
  - name: AAWP_SKILL
    description: "Override skill root directory path"
    required: false
  - name: AAWP_AI_TOKEN
    description: "Daemon auth token (auto-generated at startup, not user-supplied)"
    required: false
credentials:
  - name: "Guardian Key"
    description: "ECDSA private key for the gas-relay wallet. Auto-generated on first provision and stored in config/guardian.json. Used ONLY to pay gas fees — never holds user assets."
  - name: "Encrypted Seed"
    description: "Agent signing seed, AES-256-GCM encrypted at rest. Generated during provisioning, stored in .agent-config/seed.enc. This is the agent's on-chain signing authority."
persistence:
  - type: daemon
    description: "Local signing daemon (background process) listens on a Unix socket at /tmp/.aawp-daemon.*. Holds the decrypted signing key in memory. Managed via ensure-daemon.sh / restart-daemon.sh."
  - type: files
    description: "Writes: config/guardian.json, .agent-config/seed.enc, /tmp/.aawp-daemon.lock (PID lock)."
  - type: cron
    description: "DCA strategies and price alerts register OpenClaw cron jobs for autonomous scheduled execution."
native_binary:
  file: core/aawp-core.node
  hash_file: core/aawp-core.node.hash
  description: >
    Precompiled Node.js N-API addon (linux-x64) for cryptographic operations:
    seed derivation, ECDSA signing, AES-256-GCM enc/dec, HMAC auth.
    Built from Rust via napi-rs. Hash recorded in aawp-core.node.hash.
  source: "https://github.com/aawp-ai/aawp"
  verification: "On-chain factory approveBinary(hash) — only whitelisted builds can operate wallets"
  architecture: linux-x64
  runtime: "Node.js N-API (ABI stable)"
risk_disclosure: >
  This skill runs a persistent signing daemon and can autonomously submit
  on-chain transactions as the AI Agent. It manages encrypted private key material
  and a precompiled native binary. DCA/price-alert features register cron jobs.
  The on-chain factory enforces both binary approval and AI-exclusive ownership —
  only whitelisted AI Agent daemon builds can create or operate wallets. Humans
  cannot be the signer. Review the guardian architecture and verify binary
  provenance before installing.
---
# AAWP — 人工智能代理钱包协议（AI Agent Wallet Protocol）

这是专为人工智能代理（AI Agents）设计的唯一加密货币钱包协议，而非为人类设计。

AAWP遵循一个核心原则：签名者始终是人工智能代理本身——这一信息在钱包创建时被锁定，并且可以在链上得到验证。人工智能代理通过基于守护者（guardian）的架构，在EVM网络上管理自己的链上资产。所有交易都在本地通过一个分片密钥守护进程（sharded-key daemon）进行签名，无需人类批准；同时，人类守护者拥有完全的资产恢复和冻结权限。

**支持的网络：** Ethereum · Base · BNB Chain · Polygon · Optimism · Arbitrum

---

## 架构概述

**关键组件分离：**  
- 守护者（Guardian）负责支付网络手续费（gas）；  
- 钱包（Wallet）保管资产；  
- 守护进程（Daemon）负责签名交易。

---

## 快速参考

| 功能 | 命令                |
|------|-------------------|
| 创建钱包 | `wallet-manager.js --chain base create` |
| 查看余额 | `wallet-manager.js --chain base balance` |
| 发送ETH | `wallet-manager.js --chain base send <接收地址> <金额>` |
| 发送ERC-20代币 | `wallet-manager.js --chain base send-token USDC <接收地址> <金额>` |
| 查询兑换报价 | `wallet-manager.js --chain base quote ETH USDC 0.01` |
| 执行兑换 | `wallet-manager.js --chain base swap ETH USDC 0.01` |
| 跨链桥接 | `wallet-manager.js --chain base bridge ETH optimism 0.1` |
| 调用合约 | `wallet-manager.js --chain base call <合约地址> "函数参数"...` |
| 读取合约信息 | `wallet-manager.js --chain base read <合约地址> "函数() 返回值 (uint)" ...` |
| 自动投资策略（DCA） | `dca.js add --chain base --from ETH --to USDC --amount 0.01 --cron "0 9 * * *"` |
| 价格警报 | `price-alert.js add --chain base --from ETH --to USDC --above 2600 --notify` |
| 跨链投资组合 | `portfolio.js` |
| 单链投资组合 | `portfolio.js --chain base` |
| 下单 | `limit-order.js --chain base create ETH USDC 0.1 2700` |
| 查看订单 | `limit-order.js --chain base list` |
| 查看NFT | `nft.js --chain base balance` |
| 转移NFT | `nft.js --chain base transfer <合约地址> <NFT令牌> <接收地址>` |
| 设置NFT最低价格 | `nft.js --chain eth floor <合约地址>` |
| 查看收益率 | `yield.js --chain base rates` |
| 提供抵押品 | `yield.js --chain base supply USDC 1000` |
| 借款 | `yield.js --chain base borrow USDC 200` |
| 查看Aave持仓 | `yield.js --chain base positions` |
| 诊断工具 | `bash scripts/doctor.sh` |
| 备份钱包 | `wallet-manager.js backup ./backup.tar.gz` |

所有命令的通用格式：`node scripts/wallet-manager.js --help`

---

## 开始使用

### 1. 准备工作

首次运行时，系统会自动完成准备工作：`ensure-daemon.sh`会检测是否缺少种子短语（seed phrase），并完成必要的配置。

---

### 2. 创建钱包

如果守护者需要支付网络手续费，系统会提供相应的资金指南，其中包含守护者的地址和私钥。

---

### 3. 固定钱包地址并注入资金

---

### 4. 测试

配置完成后，需要验证守护进程的二进制哈希值是否已在工厂合约（factory contract）上获得批准；如果没有，工厂所有者需要执行`approveBinary(hash)`操作。

---

## 钱包管理命令行工具（Wallet Manager CLI）

**入口命令：** `node scripts/wallet-manager.js`
**链选择参数：** `--chain <base|bsc|polygon|optimism|arbitrum|ethereum>`

---

## 钱包生命周期管理

---

## 转账操作

---

## 交易功能

---

## 合约交互

---

## 批量操作格式

---

## 地址簿管理

---

## RPC请求与备份

---

## 自动投资策略（DCA）

**入口命令：** `node scripts/dca.js`

该脚本会注册一个OpenClaw定时任务，用于按计划执行资产兑换操作。

---

## 价格警报

**入口命令：** `node scripts/price-alert.js`

---

## 守护进程管理

| 脚本 | 功能                |
|--------|-------------------|
| `scripts/doctor.sh` | 全面诊断工具          |
| `scripts/ensure-daemon.sh` | 如果守护进程未运行，则自动启动它       |
| `scripts/restart-daemon.sh` | 强制重启守护进程         |

在进行敏感操作或发现守护进程异常时，请先运行`doctor.sh`。

---

## 跨链投资组合视图

**入口命令：** `node scripts/portfolio.js`
**支持的网络：** 全部6个网络（Ethereum · Binance Smart Chain · Polygon · Arbitrum · Optimism）

---

## 命令列表

---

## 输出内容包括：**
- 每个网络的本地余额（ETH / BNB / MATIC）
- 通过`Multicall3`接口获取的所有ERC-20代币余额（每个网络仅需一次RPC调用）
- 每个代币的美元价值（数据来源：CoinGecko公共API）
- 所有网络的投资组合总价值
- 按美元价值排名的前8大持仓
- 跨网络的同一代币持有情况

**跟踪的代币：** USDC, USDT, WETH, DAI, WBTC, BNB/WBNB, MATIC, ARB, OP, CAKE, AERO, PEPE等。

---

## 限价单（CoW协议 — 无需支付网络手续费）

**入口命令：** `node scripts/limit-order.js`
**支持的网络：** Ethereum · Binance Smart Chain · Arbitrum · Polygon（CoW协议）

限价单在链下（EIP-712协议）进行签名，并由第三方解决方案器（solvers）完成结算；**创建限价单时无需支付网络手续费**（BSC网络的取消操作除外）。

---

**注意事项：**
- 首次使用前，需要执行一次ERC-20代币的授权交易（通过CoW VaultRelayer）。
- `price`参数表示每卖出1个代币所需的买入代币数量。
- 限价单信息会保存在`config/limit-orders.json`文件中，以便本地跟踪。

---

## NFT操作（ERC-721 & ERC-1155）

**入口命令：** `node scripts/nft.js`
**支持的网络：** 全部6个网络（通过BscScan NFT API）

---

## 收益率与DeFi（Aave V3）

**入口命令：** `node scripts/yield.js`
**支持的网络：** Ethereum · Binance Smart Chain · Arbitrum · Polygon（Aave V3协议）

---

## 各网络支持的代币

| 网络 | 支持的代币            |
|------|-------------------|
| Ethereum | USDC, WETH, CBTC, USDbC     |
| Binance Smart Chain | USDC, USDT, DAI, WBTC, WETH   |
| Arbitrum | USDC, USDT, WETH, WBTC, DAI     |
| Polygon | USDC, USDT, WETH, WBTC, DAI     |
| Uniswap | USDC, USDT, WETH, WBTC, DAI     |

> **安全提示：** 借款后请务必检查你的资产健康状况（health factor）；健康状况低于1.0时会触发清算。可使用`positions`命令查看。

---

## 代币发布（使用AAWP钱包）

你可以使用AAWP钱包作为链上的部署者、管理员以及LP（Lending Protocol）费用接收方来发布新代币。

**脚本：** `scripts/deploy-clanker.js`

**支持的发布网络：**
- Ethereum：`8453`
- Arbitrum：`42161`
- Unichain：`130`
- Binance Smart Chain：`56`

---

## 配置参考

**工作原理：** AAWP钱包直接调用`Clanker.deployToken()`函数进行代币发布；所有LP费用都会归AAWP钱包所有，代币的所有权完全属于人工智能代理。

---

## 部署参考

AAWP合约在所有网络上使用CREATE2协议进行部署，地址固定如下：

| 合约 | 地址                |
|---------|-------------------|
| 工厂代理（Factory Proxy） | `0xAAAA3Df87F112c743BbC57c4de1700C72eB7aaAA` |
| 身份代理（Identity Proxy） | `0xAAAafBf6F88367C75A9B701fFb4684Df6bCA1D1d` |

这些地址已在Etherscan、BaseScan、BscScan、PolygonScan、Optimistic Etherscan和Arbiscan平台上经过验证。

---

## 安全措施

| 规则 | 原因                |
|------|-------------------|
| **资金必须注入钱包，而非守护者账户** | 仅守护者负责支付网络手续费，你的资产存储在钱包合约中 |
| **固定钱包地址** | 使用`export AAWP_WALLET=0x...`命令可防止操作错误地址 |
| **交易前查询报价** | 执行交易前请先查看汇率和滑点信息 |
| **从小额开始测试** | 在新网络或新操作中先使用小额资金进行测试 |
| **严格保密** | 种子短语、私钥和分片密钥严禁出现在日志或聊天记录中 |
| **确认二进制哈希值已获批准** | 配置完成后，需确认守护进程的二进制哈希值已在工厂合约上获得批准 |

---

## 故障排除

| 错误类型 | 解决方法            |
|--------|-------------------|
| `E_AI_GATE` / `hmac_mismatch` | 重启守护进程：`bash scripts/restart-daemon.sh` |
| `InvalidSignature` | 核对签名者的身份和工厂合约上的二进制哈希值是否匹配 |
| `Call failed` | 检查余额、网络手续费和交易参数 |
| `E40` / `E41` | 异常终止重复的守护进程进程，然后重新启动 |
| `BinaryNotApproved` | 工厂所有者需在所有6个网络上执行`approveBinary(hash)`操作 |
| 交易失败（消耗约100万gas） | 设置`--gas-limit 8000000`参数；Clanker V4/Uniswap V4操作可能需要高达600万gas |

---

## 文件结构

---