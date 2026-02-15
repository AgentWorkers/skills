---
name: nadfunagent
description: Nad.fun的自主交易代理：该代理负责扫描市场、分析代币价格、执行交易，并将利润分配给MMIND代币持有者。它依赖于nadfun-trading、nadfun-indexer和nadfun-agent-api这三个组件来完成其功能。
user-invocable: true
argument-hint: [action] [options]
---

**关键通信规则：**  
1. **语言**：始终使用与用户问题相同的语言进行回复。如果是英文，请用英文回复。  
2. **数据加载**：在执行任何操作之前，首先从用户或配置文件中请求并加载所有所需的数据。使用 OpenClaw 的内存/会话存储来保存加载的数据，这样就不需要再次请求了。  
3. **Telegram 集成**：  
   - 在每个交易周期结束后，向 Telegram 发送详细报告。  
   - 如果无法建立与 Telegram 机器人的连接，请要求用户先与机器人开始对话。  
   - 包括持仓状态、盈亏（P&L）、发现的新机会、执行的交易等信息。  

**初始设置：**  
首次调用时，询问用户以下信息：  
   - `MMIND_TOKEN_ADDRESS`（或从 `.env` 文件中加载）  
   - `MONAD_PRIVATE_KEY`（或从 `.env` 文件中加载）  
   - `MONAD_RPC_URL`（或从 `.env` 文件中加载）  
   - `MONAD_NETWORK`（或从 `.env` 文件中加载）  
   - 用于接收通知的 Telegram 用户 ID。  
   将所有这些数据保存在 OpenClaw 内存中以供将来使用。  

# Nad.fun 自动交易代理  

该代理会扫描 Nad.fun 市场，使用动量策略分析代币，执行交易，并将利润分配给 MMIND 代币持有者。  

## 先决条件：  
- 安装了 `monad-development` 技能（用于钱包和 RPC 设置）  
- 安装了 `nadfun-trading` 技能（用于买入/卖出操作），或使用此仓库中的 `trading/` 文件夹  
- 安装了 `nadfun-indexer` 技能（用于查询事件）  
- 安装了 `nadfun-agent-api` 技能（用于市场数据）  
- 配置了网络（仅适用于主网）  
- 配置了 MMIND 代币地址  

**路径（干净安装）：**  
如果设置了 `NADFUN_ENV_PATH`，则从该路径读取配置文件；否则从 `$HOME/nadfunagent/.env` 中读取。  
持仓报告路径：`POSITIONS_REPORT_PATH` 或 `$HOME/nadfunagent/positions_report.json`。  
`nadfun-trading` 中的脚本可能位于 `~/.openclaw/workspace/skills/nadfun-trading` 或 `<this-repo>/trading`。请参阅 `DEPENDENCIES.md`。  

## 配置  

**关键**：从 `.env` 文件中加载环境变量（默认路径：`$HOME/nadfunagent/.env`；可以通过 `NADFUN_ENV_PATH` 覆盖）：  
- `MMIND_TOKEN_ADDRESS`：用于利润分配的 MMIND 代币地址（必需）  
- `MONAD_PRIVATE_KEY`：交易钱包的私钥（必需）  
- `MONAD_RPC_URL`：RPC 端点 URL（必需）  
- `MONAD_NETWORK`：网络类型（“mainnet” 或 “testnet”）（必需）  
- `MAX_POSITION_SIZE`：最大持仓规模（默认：0.1 MON）  
- `PROFIT_TARGET_PERCENT`：止盈阈值（默认：20%）  
- `STOP_LOSS_PERCENT`：止损阈值（默认：10%）  
- `PNL_DISTRIBUTION_PERCENT`：分配的利润百分比（默认：30%）  

**在开始交易周期之前：**  
1. 读取 `.env` 文件（路径：`NADFUN_ENV_PATH` 或 `$HOME/nadfunagent/.env`）。如果文件缺失或任何必需的变量（`MONAD_PRIVATE_KEY`、`MONAD_RPC_URL`、`MMIND_TOKEN_ADDRESS`、`MONAD_NETWORK`）未设置，请**要求用户提供这些信息**，然后再进行买入/卖出或执行 `bonding-v2` 操作。  

### Nad.fun 自动交易代理  

**功能概述：**  
- 自动扫描 Nad.fun 市场  
- 使用动量策略分析代币  
- 执行交易  
- 将利润分配给 MMIND 代币持有者  

### 先决条件（续）：  
- 安装了 `monad-development`、`nadfun-trading`、`nadfun-indexer`、`nadfun-agent-api` 技能  
- 配置了网络（主网）  
- 配置了 MMIND 代币地址  

### 配置文件说明：  
- 请确保 `.env` 文件存在，并且包含所有必要的环境变量。  

### 2. 代币分析（关键步骤）：**  
使用方法 6 和 7 直接获取代币数据。这些方法已经返回了包含 `market_info` 的完整代币数据，因此请直接使用这些数据进行分析，无需额外的 API 调用。  

### 3. 交易决策（关键步骤）：**  
在分析新代币之前，必须先检查和管理现有持仓！  

#### 步骤 1：获取当前持仓：**  
1. 从 `.env` 文件中获取交易钱包地址。  
2. 使用代理 API 查询当前持仓：`/agent/holdings/${walletAddress}?limit=100`。  
3. 过滤余额大于 0 的代币。  

#### 步骤 2：计算每个持仓的盈亏（关键步骤）：**  
使用 `check-pnl.js` 脚本计算盈亏。