---
name: agent-otc-trade
description: >-
  Facilitate over-the-counter trades between agents using Uniswap as the
  settlement layer. Use when user wants to trade tokens directly with another
  agent, settle an agent-to-agent trade through Uniswap, or execute an OTC
  swap with a specific counterparty agent. Verifies counterparty identity via
  ERC-8004, negotiates terms, and settles through Uniswap pools.
model: opus
allowed-tools:
  - Task(subagent_type:trade-executor)
  - Task(subagent_type:identity-verifier)
  - mcp__uniswap__get_quote
  - mcp__uniswap__get_token_price
  - mcp__uniswap__get_pool_info
  - mcp__uniswap__get_agent_balance
  - mcp__uniswap__execute_swap
  - mcp__uniswap__submit_cross_chain_intent
  - mcp__uniswap__check_safety_status
---

# 代理场外交易（Agent OTC Trade）

## 概述

该功能利用 Uniswap 作为无信任的结算层，促进代理之间的场外交易。与传统方式（代理通过临时渠道手动协调交易、验证对方身份、协商价格并独立处理结算）不同，该功能提供了一套结构化的流程：通过 ERC-8004 标准验证交易对手方的身份，以 Uniswap 的池价格作为参考价格达成交易条款，并通过 Uniswap 池实现原子级结算。

**为什么这比传统的代理间交易好十倍：**

1. **交易对手方验证**：在任何交易之前，都会通过链上的 ERC-8004 注册表验证交易对手方的身份。如果没有这一环节，代理们将盲目地进行交易，只能信任那些他们从未有过交互的地址。该功能会检查对方的身份、信誉分数和信任等级，拒绝与未经验证的代理进行交易。
2. **公平定价**：场外交易使用 Uniswap 的池价格作为参考价格，防止任何一方提出不公平的条件。该功能会显示当前的池价格、提议的场外价格以及溢价/折扣，确保双方都能完全透明地了解交易情况。
3. **原子级结算**：交易通过 Uniswap 池在单次交易中完成。不存在托管风险、对手方违约风险或部分成交的风险。池会以约定的价格提供有保障的流动性。
4. **跨链支持**：对于不同链上的代理，结算过程使用 ERC-7683 跨链协议。如果没有这一功能，跨链场外交易需要手动协调桥梁服务，这可能导致交易卡住或时间不匹配的问题。
5. **审计追踪**：每笔场外交易都会记录交易对手方的身份、约定的条款、结算交易和费用等信息，为建立信誉和解决纠纷提供了可验证的历史记录。

## 适用场景

当用户提出以下请求时，激活该功能：

- “直接与另一代理交易代币”
- “通过 Uniswap 结算代理间的交易”
- “与代理 0x... 执行场外交易”
- “使用 Uniswap 从代理 0x... 购买代币”
- “与交易对手方建立直接交易”
- “用 1000 USDC 与代理 0x... 进行场外交易（交易 UNI）”
- “通过 Uniswap 与另一代理结算服务费用”

**不适用场景**

- 当用户仅需要进行常规的代币交换（此时应使用 `execute-swap` 功能）；
- 当用户需要提供流动性（此时应使用 `manage-liquidity` 功能）；
- 当用户希望寻找交易机会（此时应使用 `scan-opportunities` 功能）。

## 参数

| 参数                | 是否必填 | 默认值       | 获取方式                                      |
|-------------------|--------|------------|-------------------------------------------|
| counterpartyAgent     | 是     | --          | 交易对手方的地址（0x...）或 ERC-8004 身份信息                |
| tokenSell         | 是     | --          | 卖出的代币："USDC", "UNI" 或代币的地址                   |
| tokenBuy          | 是     | --          | 购买的代币："ETH", "UNI" 或代币的地址                   |
| amount            | 是     | --          | 卖出数量："1000 USDC", "50 UNI", "价值 $5,000"                   |
| chain            | 否      | "ethereum"     | 结算链："ethereum", "base", "arbitrum"                   |
| settlementMethod     | 否      | "direct-swap"     | 结算方式（"direct-swap" 或 "intent" [跨链协议]                |
| maxPremium        | 否      | 1%          | 可接受的最大溢价/折扣比例（相对于池价格）                   |
| requireVerified       | 否      | true        | 是否要求验证交易对手方的 ERC-8004 身份                   |

如果用户未提供 `counterpartyAgent`、`tokenSell`/`tokenBuy` 或 `amount` 参数，请务必询问用户这些信息——切勿自行猜测。

## 工作流程

```
                        AGENT OTC TRADE PIPELINE
  ┌──────────────────────────────────────────────────────────────────────┐
  │                                                                      │
  │  Step 1: VERIFY COUNTERPARTY                                         │
  │  ├── Check ERC-8004 identity registry                                │
  │  ├── Query reputation score                                          │
  │  ├── Determine trust tier (unverified/basic/verified/trusted)        │
  │  └── Output: Identity report + trust decision                        │
  │          │                                                           │
  │          ▼ IDENTITY GATE                                             │
  │  ┌───────────────────────────────────────────┐                       │
  │  │  trusted/verified  -> Proceed              │                       │
  │  │  basic             -> Warn, ask user       │                       │
  │  │  unverified        -> STOP (if required)   │                       │
  │  └───────────────────────────────────────────┘                       │
  │          │                                                           │
  │          ▼                                                           │
  │                                                                      │
  │  Step 2: PRICE DISCOVERY                                             │
  │  ├── Get current Uniswap pool price for the token pair               │
  │  ├── Get quote at the OTC trade size                                 │
  │  ├── Calculate fair OTC price (pool price + spread)                  │
  │  └── Output: Reference price + OTC terms                             │
  │          │                                                           │
  │          ▼                                                           │
  │                                                                      │
  │  Step 3: TERMS AGREEMENT                                             │
  │  ├── Present terms to user: price, amounts, fees, settlement method  │
  │  ├── Compare OTC price vs pool price (premium/discount)              │
  │  ├── Show total cost including gas and slippage                      │
  │  └── User must explicitly confirm                                    │
  │          │                                                           │
  │          ▼                                                           │
  │                                                                      │
  │  Step 4: SETTLEMENT                                                  │
  │  ├── Check wallet balance and approvals                              │
  │  ├── Execute swap via trade-executor (or cross-chain intent)         │
  │  ├── Verify settlement on-chain                                      │
  │  └── Output: Settlement confirmation + tx hash                       │
  │          │                                                           │
  │          ▼                                                           │
  │                                                                      │
  │  Step 5: RECORD & REPORT                                             │
  │  ├── Record trade in OTC history                                     │
  │  ├── Log counterparty, terms, settlement tx                          │
  │  └── Output: Full OTC trade report                                   │
  │                                                                      │
  └──────────────────────────────────────────────────────────────────────┘
```

### 第一步：验证交易对手方

将任务委托给 `Task(subagent_type:identity-verifier)`：

```
Verify the identity and reputation of this agent:
- Agent address: {counterpartyAgent}
- Chain: {chain}

Check the ERC-8004 Identity Registry, Reputation Registry, and Validation
Registry. Return the trust tier (unverified/basic/verified/trusted),
reputation score, registration date, and any flags.
```

**向用户展示：**

```text
Step 1/5: Counterparty Verification

  Agent:       0x1234...abcd
  ERC-8004:    Registered (verified tier)
  Reputation:  78/100 (good)
  Registered:  2025-11-15 (87 days ago)
  Trades:      142 completed, 0 disputes
  Trust Tier:  VERIFIED

  Proceeding to price discovery...
```

**身份验证逻辑：**

| 信任等级 | 操作                                      |
|---------|-----------------------------------------|
| **受信任**  | 自动进入第二步                                  |
| **已验证** | 自动进入第二步                                  |
| **基本信任** | 警告用户：“交易对手方仅经过基本验证。是否继续？”请求确认。           |
| **未验证** | 如果 `requireVerified` 为 true：**停止操作**。说明原因，并建议先进行验证。     |
|         | 如果 `requireVerified` 为 false：强烈警告用户，并请求明确确认。         |

### 第二步：价格确认

1. 调用 `mcp__uniswap__get_token_price` 获取两种代币的美元价格。
2. 调用 `mcp__uniswap__get_pool_info` 获取该代币对的当前池价格。
3. 调用 `mcp__uniswap__get_quote` 根据场外交易规模确定实际成交价格（包括滑点）。

```text
Step 2/5: Price Discovery

  Token Pair:    USDC / UNI
  Pool Price:    1 UNI = $7.10 (USDC/UNI 0.3% V3)
  Pool TVL:      $42M
  Quote at Size: 1000 USDC -> 140.65 UNI (impact: 0.08%)

  OTC Reference Rate: $7.10 per UNI
  Your Trade:         1000 USDC -> ~140.85 UNI

  Proceeding to terms agreement...
```

### 第三步：协商交易条款

向用户展示完整的交易条款以获取确认：

```text
OTC Trade Terms

  You Sell:     1,000 USDC
  You Receive:  ~140.85 UNI ($999.90)
  Counterparty: 0x1234...abcd (VERIFIED, rep: 78/100)

  Pricing:
    Pool Rate:  $7.10 per UNI
    OTC Rate:   $7.10 per UNI (0.00% premium)
    Slippage:   ~0.08%
    Gas Est:    ~$5.00

  Settlement:
    Method:     Direct swap via Uniswap V3
    Chain:      Ethereum
    Pool:       USDC/UNI 0.3%

  Proceed with this OTC trade? (yes/no)
```

**只有当用户明确同意后，才能进入第四步。**

如果场外价格与池价格的偏差超过 `maxPremium`，请警告用户：

```text
  WARNING: OTC rate ($7.25/UNI) is 2.1% above pool rate ($7.10/UNI).
  This exceeds your max premium of 1%. Proceed anyway? (yes/no)
```

### 第四步：结算

将任务委托给 `Task(subagent_type:trade-executor)`：

**对于直接交换结算：**

```
Execute this OTC trade settlement:
- Sell: {amount} {tokenSell}
- Buy: {tokenBuy}
- Chain: {chain}
- Slippage tolerance: based on OTC terms
- Context: This is an OTC trade with counterparty {counterpartyAgent}
  (ERC-8004 verified, reputation {score}/100). Settle through the
  {fee}% pool.
```

**对于跨链交易结算：**

使用 `mcp__uniswap__submit_cross_chain(intent`，参数如下：
- `tokenIn`：源链上的卖出代币
- `tokenOut`：目标链上的买入代币
- `sourceChain`：你的链
- `destinationChain`：交易对手方的链

### 第五步：记录与报告

```text
Step 5/5: OTC Trade Complete

  Settlement:
    Sold:       1,000 USDC
    Received:   140.85 UNI ($999.90)
    Slippage:   0.07%
    Gas:        $4.80
    Tx:         https://etherscan.io/tx/0x...

  Counterparty:
    Agent:      0x1234...abcd
    Trust:      VERIFIED (78/100)

  OTC Terms vs Market:
    Pool Rate:  $7.10/UNI
    Actual:     $7.10/UNI (0.00% premium)
```

## 输出格式

### 交易成功

```text
Agent OTC Trade Complete

  Trade:
    Sold:         1,000 USDC
    Received:     140.85 UNI ($999.90)
    Counterparty: 0x1234...abcd (VERIFIED)
    Settlement:   Direct swap via USDC/UNI 0.3% (V3)
    Chain:        Ethereum
    Tx:           https://etherscan.io/tx/0x...

  Pricing:
    Pool Rate:    $7.10/UNI
    Actual Rate:  $7.10/UNI
    Premium:      0.00%
    Slippage:     0.07%
    Gas:          $4.80

  Counterparty Verification:
    ERC-8004:     Registered, VERIFIED tier
    Reputation:   78/100
    Trade History: 142 completed, 0 disputes
```

### 验证失败

```text
Agent OTC Trade -- Blocked

  Counterparty: 0x5678...efgh
  ERC-8004:     NOT REGISTERED
  Trust Tier:   UNVERIFIED

  Trade blocked: Counterparty is not ERC-8004 verified.
  Your policy requires verified counterparties (requireVerified=true).

  Suggestions:
    - Ask the counterparty to register on ERC-8004
    - Use /verify-agent to check their status
    - Set requireVerified=false to trade with unverified agents (not recommended)
```

## 重要说明

- **交易对手方验证是关键的安全机制。** ERC-8004 身份验证可以防止与恶意或未知的代理进行交易。建议将 `requireVerified` 设置为 `true`。
- **结算通过 Uniswap 池完成，而非点对点交易。** 两个代理都独立地与 Uniswap 池进行交互，因此交易是原子级的且无信任风险的——任何一方都无法违约。
- **交易对手方无需同时在线。** 由于结算通过池完成，你的代理可以独立执行自己的交易部分。这里的“场外交易”指的是双方约定的条款和对手方身份的验证，而不是真正的点对点原子交换。
- **价格参考防止不公平条款。** Uniswap 池价格作为客观的参考标准。`maxPremium` 参数（默认为 1%）可防止接受远低于市场价格的交易。
- **跨链场外交易使用 ERC-7683 协议。** 对于不同链上的代理，该功能使用 `submit_cross_chain(intent` 进行结算。这会增加一些延迟，但支持跨链交易。
- **所有场外交易都会被记录。** 交易详情（交易对手方、条款、结算交易）会被记录下来，用于建立信誉和审计。
- **该功能仅负责执行你方的交易部分。** 交易对手方需自行完成他们的交易部分。实际上，两个代理都可以独立使用该功能，通过同一个 Uniswap 池完成各自的交易。

## 对 MCP 服务器的依赖

该功能依赖于 Uniswap MCP 工具来获取价格、池数据、报价、余额和跨链信息。
在单独使用该功能时（例如，从技能目录中调用），请确保 Agentic Uniswap MCP 服务器正在运行：

- 仓库：[`Agentic-Uniswap` MCP 服务器](https://github.com/wpank/Agentic-Uniswap/tree/main/packages/mcp-server)
- 包：`@agentic-uniswap/mcp-server`

## 错误处理

| 错误类型                | 显示给用户的消息                                      | 建议的操作                                      |
|-------------------|-------------------------------------------------|-----------------------------------------------|
| 交易对手方未验证           | “交易对手方未通过 ERC-8004 验证。”                                      | 请求交易对手方进行注册，或关闭此验证功能                   |
| 交易对手方未找到           | “无法在地址 {addr} 找到对应的代理。”                                      | 确认地址是否正确                         |
| 未找到对应的池             | “在链 {chain} 上找不到 {tokenSell}/{tokenBuy} 的 Uniswap 池。”                   | 尝试其他链或使用其他代币                     |
| 溢价过高             | “场外交易价格与池价格的偏差超过 {X}%，超出 {maxPremium} 的限制。”                   | 重新协商条款或调整最大溢价                     |
| 账户余额不足             | “{tokenSell} 的余额不足：当前余额为 {X}，需要 {Y}。”                         | 充值或减少交易金额                         |
| 结算失败             | “通过 Uniswap 的场外交易失败：原因：{reason}。”                             | 检查流动性、Gas 费用并重试                         |
| 跨链交易失败             | “跨链交易失败：原因：{reason}。”                                      | 检查桥接服务状态并重试                         |
| 安全检查失败             | “交易超出安全限制。”                                      | 使用 `check-safety` 功能检查交易限额                 |
| 未配置钱包             | “未配置钱包。无法执行场外交易。”                                      | 使用 `setup-agent-wallet` 功能配置钱包                 |
| 身份验证服务不可用           | “无法访问 ERC-8004 注册表。无法验证交易对手方。”                         | 稍后重试或谨慎操作                         |