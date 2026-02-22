---
name: clankerkit
description: Monad平台为AI代理提供了自主的钱包管理功能：支持交换（swap）、质押（stake）、部署钱包（deploy wallets）、交易memecoins（memecoins），以及通过自然语言界面管理支出策略（manage spending policies）。
license: MIT
metadata:
  openclaw:
    requires:
      env:
        - AGENT_WALLET_ADDRESS
        - POLICY_ENGINE_ADDRESS
        - AGENT_PRIVATE_KEY
        - OWNER_ADDRESS
      primaryEnv: AGENT_PRIVATE_KEY
---
# ClankerKit – 为Monad上的AI代理提供的自主钱包

ClankerKit为您的AI代理在Monad区块链上提供了自主的财务管理能力。您可以部署智能合约钱包，设置支出策略，通过Kuru DEX进行代币交换，质押MON，使用策略交易memecoins，并执行跨链交换。

## 快速入门

```bash
# Install the skill
claw skill install clankerkit
```

## 环境变量

| 变量 | 是否必需 | 描述 |
|---|---|---|
| `AGENT_WALLET_ADDRESS` | 是 | 部署的AgentWallet合约地址 |
| `POLICY_engine_ADDRESS` | 是 | 部署的PolicyEngine合约地址 |
| `AGENT_PRIVATE_KEY` | 是 | 代理的私钥（以0x前缀开头） |
| `OWNER_ADDRESS` | 是 | 人类所有者地址 |
| `MONAD_RPC_URL` | 否 | Monad RPC地址（默认：testnet） |
| `MONAD_NETWORK` | 否 | `testnet`或`mainnet`（默认：testnet） |
| `ZEROX_API_KEY` | 否 | 0x Swap API密钥（仅用于`zerox_swap`） |

## 工具（共32个）

### 钱包管理

#### `get_wallet_info`  
获取钱包地址、所有者信息、代理信息、MON余额和策略状态。

#### `get_token_balance`  
获取代理钱包中的ERC-20代币余额。  
- **token**：代币符号（WMON、USDC、CHOG、DAK、YAKI）或合约地址  

#### `send_tokens`  
从钱包发送MON代币。  
- **to**：接收者地址  
- **amount**：以人类可读的形式表示的金额（例如“0.5”）  

#### `send_token`  
从钱包发送ERC-20代币。  
- **token**：代币合约地址  
- **to**：接收者地址  
- **amount**：以人类可读的形式表示的金额  

#### `execute_transaction`  
通过钱包执行任意合约调用。  
- **target**：目标合约地址  
- **value**：要发送的MON数量（wei，默认为“0”）  
- **data**：编码后的调用数据（hex格式）  

#### `ensure_gas`  
确保代理的EOA（Externally Owned Account）有足够的MON作为gas费用。如果EOA余额低于最低阈值，系统会自动从AgentWallet合约中向EOA转账MON。用户只需为钱包合约提供资金，代理会自行补充gas费用。  
- **minBalance**：EOA的最低可接受MON余额（以人类可读的形式表示，默认为“0.01”）  
- **topUpAmount**：如果余额低于最低阈值，则需要补充的MON金额（以人类可读的形式表示，默认为“0.05”）  

### 策略与安全  

#### `get_policy`  
查看当前的支出限制（每日/每周）、使用情况以及允许的交易列表。  

#### `create_policy`  
创建支出策略。在启用保护性交易之前必须先调用此函数。  
- **dailyLimit**：每日最大支出限额（以人类可读的形式表示，例如“1.0”）  
- **weeklyLimit**：每周最大支出限额（默认为每日7倍）  
- **allowedTokens**：可选的ERC-20代币允许列表  
- **allowedContracts**：可选的合约地址允许列表  
- **requireApprovalAbove**：需要所有者批准的MON金额阈值  

#### `update_daily_limit`  
更新每日支出限额。  
- **newLimit**：新的每日支出限额（以人类可读的形式表示）  

### 代币交换（Kuru DEX）  

#### `swap_tokens`  
通过Kuru Flow聚合器在Monad上进行代币交换。支持以下代币/合约地址：MON、USDC、WMON、CHOG、DAK、AUSD、WETH、WBTC。  
- **tokenIn**：源代币（符号或地址）  
- **tokenOut**：目标代币（符号或地址）  
- **amount**：以人类可读的形式表示的金额（例如“0.01”）  
- **slippage**：滑点（以bps为单位，默认为50 = 0.5%）  

#### `get_swap_quote`  
获取交换报价（不执行实际交换）。  
- **tokenIn**、**tokenOut**、**amount**：与`swap_tokens`参数相同  

### 质押  

#### `stake_mon`  
将MON质押给验证者以获得奖励。  
- **amount**：要质押的MON数量（以人类可读的形式表示）  
- **validatorId**：验证者ID（可选，使用默认值）  

#### `unstake_mon`  
开始从验证者处取回质押的MON。  
- **amount**：要取回的MON数量（以人类可读的形式表示）  
- **validatorId**：验证者ID（可选）  
- **withdrawId**：取回操作的ID（默认为0）  

#### `claim_staking_rewards`  
领取累积的质押奖励。  
- **validatorId**：可选  

#### `compound_rewards`  
重新质押累积的奖励。  
- **validatorId**：可选  

#### `get_staking_info`  
获取质押信息（质押金额、未领取的奖励）。  
- **validatorId**：可选  

### Kuru CLOB订单簿交易  

#### `get_kuru_markets`  
列出Monad主网上的Kuru CLOB订单簿市场。  

#### `get_order_book`  
获取Kuru CLOB市场的实时订单簿（买价/卖价）。  
- **marketAddress**：订单簿合约地址  

#### `get_market_price`  
获取Kuru CLOB市场的最佳买价、卖价和中价。  
- **marketAddress**：订单簿合约地址  

#### `kuru_market_order`  
在Kuru CLOB市场上放置市场订单（IOC订单）。代理的EOA必须持有相应代币。  
- **marketAddress**：订单簿合约地址  
- **amount**：以人类可读的浮点数表示的金额  
- **isBuy**：true表示买入，false表示卖出  
- **minAmountOut**：最小输出金额（默认为0）  
- **slippageBps**：滑点（以bps为单位，默认为100）  

#### `kuru_limit_order`  
在Kuru CLOB市场上放置限价（GTC）订单。  
- **marketAddress**：订单簿合约地址  
- **price**：报价资产中的价格（浮点数）  
- **size**：基础资产的数量（浮点数）  
- **isBuy**：true表示买入，false表示卖出  
- **postOnly**：如果价格超出价差范围则拒绝执行（默认为false）  

#### `cancel_kuru_orders`  
取消Kuru CLOB市场上的未成交订单。  
- **marketAddress**：订单簿合约地址  
- **orderIds**：订单ID字符串数组  

### Memecoin交易  

#### `get_meme_tokens`  
获取所有已知Monad memecoins（DAK、CHOG、YAKI）的实时价格信息。使用Kuru Flow作为备用方案。  

#### `get_token_price`  
根据代币符号或合约地址获取特定代币的实时价格。  
- **token**：代币符号（DAK、CHOG、YAKI）或合约地址  

#### `smart_trade`  
评估或执行自动交易策略。  
- **token**：代币符号  
- **strategyType**：`dca`、`momentum`、`scalp`或`hodl`  
- **budgetMon**：总预算（MON单位）  
- **stopLoss**：止损比例（默认为0.1 = -10%）  
- **takeProfit**：止盈比例（默认为0.3 = +30%）  
- **dcaIntervals**：DCA购买间隔（默认为5次）  
- **momentumThreshold**：动量变化的最低阈值（默认为0.05%）  
- **autoExecute**：是否自动执行交易（默认为false）  

### 跨链交换  

#### `kyber_swap`  
通过KyberSwap在Ethereum/Polygon/Arbitrum/Optimism/Base/BSC/Avalanche上进行代币交换。无需API密钥，使用代理的EOA（而非钱包合约）。  
- **chain**：目标链名称  
- **tokenIn**、**tokenOut**：目标链上的代币地址  
- **amountIn**：以最小单位（wei）表示的金额  
- **slippageBps**：滑点（默认为50%）  
- **recipient**：接收者地址（默认为代理的EOA）  

#### `zerox_swap`  
通过0x Swap API v2进行交换。需要`ZEROX_API_KEY`。  
- **chain**、**tokenIn**、**tokenOut**、**amountIn**、**slippageBps**：与`kyber_swap`参数相同  

### 支付与身份验证  

#### `pay_for_service`  
为支持x402协议的API端点支付费用。  
- **endpoint**：API端点URL  
- **amount**：支付金额（USDC单位）  

#### `register_agent`  
在ERC-8004身份注册表中注册代理。  
- **name**：代理名称  
- **description**：代理描述  

### 部署  

#### `deploy_policy_engine`  
部署新的PolicyEngine合约。部署者将成为该合约的所有者。无需参数。  

#### `deploy_agent_wallet`  
部署新的AgentWallet合约。可选择同时部署PolicyEngine合约。  
- **owner**：钱包的所有者地址  
- **agent**：允许调用`execute()`函数的代理EOA地址  
- **policyEngine**：可选的现有PolicyEngine合约地址  

## 安全特性  

- **支出限制**：对代理的每日和每周支出设置上限  
- **代币允许列表**：限制代理可以转移的代币类型  
- **合约白名单**：仅允许调用已批准的合约  
- **审批阈值**：超过指定金额时需要人类批准  
- **紧急控制**：所有者可以随时暂停或提取资金  
- **访问控制**：`PolicyEngine`的`recordExecution()`函数仅能由钱包合约调用  

## 示例会话  

```
User: Check my gas and fund up if needed

Agent: [calls ensure_gas]
EOA already has sufficient gas balance. EOA: 0.221 MON, Wallet: 0.075 MON.

User: Set a daily limit of 2 MON

Agent: [calls create_policy with dailyLimit="2.0"]
Policy created: 2 MON daily, 14 MON weekly.

User: Swap 0.1 MON for CHOG

Agent: [calls swap_tokens with tokenIn="MON", tokenOut="CHOG", amount="0.1"]
Swapped 0.1 MON -> 2.71 CHOG via Kuru Flow.

User: What's my portfolio?

Agent: [calls get_wallet_info, get_meme_tokens, get_staking_info]
Wallet: 1.9 MON
CHOG: 2.71 (worth ~0.1 MON)
Staked: 0.5 MON with validator #1
```

## 许可证  

MIT