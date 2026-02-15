---
name: self-funding-setup
description: >-
  Set up a complete self-funding agent lifecycle in one command. Orchestrates
  5 agents to take an agent from zero to self-sustaining: provisions wallet,
  optionally deploys token with V4 pool, configures treasury management,
  registers identity on ERC-8004, and sets up x402 micropayments. Use when
  user wants to make their agent self-funding, earn and manage its own
  revenue, or configure autonomous agent operations end-to-end.
model: opus
allowed-tools:
  - Task(subagent_type:wallet-provisioner)
  - Task(subagent_type:token-deployer)
  - Task(subagent_type:treasury-manager)
  - Task(subagent_type:identity-verifier)
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - mcp__uniswap__get_supported_chains
  - mcp__uniswap__get_agent_balance
  - mcp__uniswap__check_safety_status
---

# 自筹资金设置

## 概述

这是系统中最为复杂的复合技能。它通过依次协调5个专用代理，将一个代理从无基础设施的状态转变为一个完全自给自足的经济实体——包括钱包、可选的代币、资金管理、链上身份验证以及支付功能——所有这些操作都通过一个命令完成。

**为什么这比手动设置每个组件要好10倍：**

1. **5个功能整合到一个命令中**：钱包配置、代币部署、资金管理、身份注册和支付配置每个都需要不同的专业知识和工具。手动协调这些步骤需要花费数小时，并且需要对Privy/Turnkey API、Uniswap V4池创建、DCA策略、ERC-8004注册以及x402协议有深入的了解。而这个技能可以同时处理所有这些功能。
2. **阶段间的信息传递**：每个代理都会接收到前一个代理的输出结果。资金管理者会知道第一步创建的钱包地址，以及第二步生成的代币地址。身份验证器会使用第二步和第三步提供的信息来注册钱包。如果没有这个技能，你就需要手动在五个不同的工具之间复制和粘贴地址及配置信息。
3. **条件化的流程**：代币部署（第二步）是可选的——对于通过服务而非代币经济模式盈利的代理，可以跳过这一步。该技能会根据所选择的收入模型自动调整后续步骤。
4. **容错机制**：如果第三步失败，第一步和第二步仍然有效且会被保留。该技能会准确报告哪些步骤成功了，哪些步骤失败了，这样你就可以修复问题并从失败点重新开始。
5. **实时反馈**：你可以实时看到每个阶段的完成情况，并获得详细的总结。最终，你会得到一个完整的“代理身份卡”，显示出自筹资金基础设施的各个组成部分。

## 适用场景

当用户有以下需求时，请激活此技能：

- “设置我的代理以实现自筹资金”
- “让我的代理能够自主盈利并管理自己的收入”
- “端到端配置代理的自主运营”
- “我希望我的代理能够实现自我维持”
- “设置完整的代理经济体系”
- “启动我的代理的财务基础设施”
- “从零开始创建一个能够自筹资金的代理”
- “完成代理的全方位设置：钱包、代币、资金管理、身份验证、支付功能”

**不适用场景**

- 当用户只需要其中一个组件时（请分别使用以下技能：`setup-agent-wallet`、`deploy-agent-token`、`manage-treasury`、`verify-agent` 或 `configure-x402`）；
- 当代理已经部分设置完成，只需要补充缺失的部分时。

## 参数

| 参数                | 是否必填 | 默认值 | 获取方式                                      |
|-------------------|--------|-------|------------------------------------------------------|
| walletProvider    | 否      | privy    | "privy"（开发环境）、"turnkey"（生产环境）或 "safe"（最高安全级别）         |
| deployToken       | 否      | false    | 是否部署代理代币："yes"、"with token"、"launch token"           |
| tokenName         | 如果使用代币 | --      | 部署代币时的名称："AgentCoin"、"MyBot Token"                     |
| tokenSymbol       | 如果使用代币 | --      | 部署代币时的符号："AGENT"、"BOT"                               |
| chains            | 否      | base     | 运行链："base"、"ethereum"、"base,ethereum"                   |
| revenueModel       | 否      | x402    | 收入模式："x402"（微支付）、"token-fees"（交易手续费）、"lp-fees" 或 "all"  |
| environment       | 否      | dev     | 环境："dev"（开发环境）、"staging" 或 "production"                         |
| initialFunding     | 否      | --      | 初始资金金额："$100"、"0.1 ETH"                              |

如果用户选择了“with token”或“launch a token”，则将`deployToken`设置为`true`，并询问`tokenName`和`tokenSymbol`（如果未提供的话）。

## 工作流程

```
                     SELF-FUNDING SETUP PIPELINE
  ┌──────────────────────────────────────────────────────────────────────┐
  │                                                                      │
  │  Step 1: WALLET PROVISIONING (wallet-provisioner)                    │
  │  ├── Determine provider: privy (dev) / turnkey (prod) / safe (max)   │
  │  ├── Provision wallet with signing capabilities                      │
  │  ├── Configure spending policies                                     │
  │  ├── Fund with gas (2x estimated need)                               │
  │  └── Output: Wallet address, provider, policies                      │
  │          │                                                           │
  │          ▼ wallet address feeds into all subsequent steps             │
  │                                                                      │
  │  Step 2: TOKEN DEPLOYMENT (token-deployer) [OPTIONAL]                │
  │  ├── Deploy ERC-20 token contract                                    │
  │  ├── Create Uniswap V4 pool with anti-snipe hooks                   │
  │  ├── Bootstrap initial liquidity                                     │
  │  ├── Lock LP tokens (10 years default)                               │
  │  └── Output: Token address, pool address, LP position                │
  │          │                                                           │
  │          ▼ token + pool info feeds into treasury config               │
  │                                                                      │
  │  Step 3: TREASURY MANAGEMENT (treasury-manager)                      │
  │  ├── Configure auto-conversion of earned fees to stablecoins         │
  │  ├── Set up DCA strategy for volatile holdings                       │
  │  ├── Configure yield optimization for idle capital                   │
  │  ├── Set circuit breaker thresholds                                  │
  │  └── Output: Treasury config, burn rate, runway projection           │
  │          │                                                           │
  │          ▼ wallet + capabilities feed into identity registration      │
  │                                                                      │
  │  Step 4: IDENTITY REGISTRATION (identity-verifier)                   │
  │  ├── Register agent on ERC-8004 Identity Registry                    │
  │  ├── Set capabilities metadata (trading, LP, services)               │
  │  ├── Initialize reputation score                                     │
  │  └── Output: ERC-8004 identity, trust tier, registry tx              │
  │          │                                                           │
  │          ▼ identity + wallet feed into payment config                 │
  │                                                                      │
  │  Step 5: PAYMENT CONFIGURATION (direct)                              │
  │  ├── Configure x402 micropayment acceptance                          │
  │  ├── Set per-tool pricing                                            │
  │  ├── Generate .well-known/x402-manifest.json                         │
  │  ├── Verify USDC balance for pay mode                                │
  │  └── Output: x402 config, pricing, manifest                          │
  │                                                                      │
  │  ═══════════════════════════════════════════════════════════          │
  │  FINAL: AGENT IDENTITY CARD                                          │
  │  ├── Wallet, token, treasury, identity, payments -- all linked       │
  │  └── Complete self-funding infrastructure report                     │
  │                                                                      │
  └──────────────────────────────────────────────────────────────────────┘
```

### 第一步：钱包配置

将任务委托给`Task(subagent_type:wallet-provisioner)`：

```
Provision an agent wallet for self-funding operations:
- Provider: {walletProvider}
- Chains: {chains}
- Environment: {environment}
- Spending limit: $10,000/day (default for self-funding agents)
- Initial funding: {initialFunding} (or 2x estimated gas need)

This wallet will be used for:
- Token deployment (if enabled)
- Treasury management (fee conversion, LP)
- x402 payment settlement
- General agent operations

Configure appropriate spending policies for a self-funding agent.
```

**配置完成后向用户展示：**

```text
Step 1/5: Wallet Provisioned

  Address:    0xABCD...1234
  Provider:   Privy (development)
  Chain:      Base (8453)
  Funded:     0.05 ETH ($98.00)
  Policies:   $10,000/day, Router + Permit2 approved

  Proceeding to token deployment...
```

**如果钱包已经存在**，通过`mcp__uniswap__get_agent_balance`检测到钱包的存在，直接跳到第二步：

```text
Step 1/5: Wallet Already Configured (skipped)

  Address:    0xABCD...1234
  Balance:    0.12 ETH + 500 USDC
  Status:     Active

  Skipping to next step...
```

### 第二步：代币部署（可选）

**仅当`deployToken=true`时执行。否则跳到第三步。**

将任务委托给`Task(subagent_type:token-deployer)`：

```
Deploy an agent token for self-funding:
- Token name: {tokenName}
- Token symbol: {tokenSymbol}
- Chain: {chains[0]} (primary chain)
- Wallet: {wallet address from Step 1}
- Paired token: WETH
- Hooks: anti-snipe (2-block delay) + revenue-share (5%)
- LP lock: 10 years
- Initial liquidity: {derive from initialFunding or suggest minimum}

This token is part of a self-funding agent setup. The revenue-share hook
directs 5% of swap fees to the agent wallet for treasury management.
```

**配置完成后向用户展示：**

```text
Step 2/5: Token Deployed

  Token:      AgentCoin (AGENT)
  Address:    0x5678...efgh
  Chain:      Base (8453)
  Pool:       AGENT/WETH V4 (0.3%, anti-snipe + revenue-share)
  LP Lock:    10 years (unlocks 2036-02-10)
  Revenue:    5% of swap fees -> agent wallet

  Proceeding to treasury management...
```

**如果`deployToken=false`：**

```text
Step 2/5: Token Deployment (skipped)

  No token deployment requested.
  Revenue model: {revenueModel} (no token economics)

  Proceeding to treasury management...
```

### 第三步：资金管理

将任务委托给`Task(subagent_type:treasury-manager)`：

```
Configure treasury management for a self-funding agent:
- Wallet: {wallet address from Step 1}
- Chains: {chains}
- Action: assess + configure (initial setup, not full operations)

Revenue sources:
{if deployToken: "- Token swap fees (5% revenue share from AGENT/WETH pool)"}
{if revenueModel includes x402: "- x402 micropayments (USDC on Base)"}
{if revenueModel includes lp-fees: "- LP fee earnings"}

Configure:
- Auto-convert non-stablecoin earnings to USDC
- Conversion threshold: $10 minimum
- DCA enabled for large conversions
- Circuit breaker: halt if treasury drops below $100
- Operating reserve: 30 days of estimated burn rate
```

**配置完成后向用户展示：**

```text
Step 3/5: Treasury Configured

  Treasury Value: $98.00 (initial funding)
  Auto-Convert:   Enabled (non-stables -> USDC, threshold: $10)
  DCA:            Enabled for conversions > 0.1% pool TVL
  Circuit Breaker: $100 minimum (INACTIVE -- above threshold)
  Burn Rate:      ~$0/day (no operations yet)
  Runway:         Indefinite (no burn rate established)

  Proceeding to identity registration...
```

### 第四步：身份注册

将任务委托给`Task(subagent_type:identity-verifier)`：

```
Register this agent on ERC-8004:
- Agent address: {wallet address from Step 1}
- Chain: ethereum (ERC-8004 registries are on mainnet)

Capabilities to register:
{if deployToken: "- Token deployment and pool management"}
{if revenueModel includes x402: "- x402 service provider"}
- Uniswap trading and LP management
- Treasury management

After registration, query the trust tier to confirm.
```

**配置完成后向用户展示：**

```text
Step 4/5: Identity Registered

  ERC-8004:    Registered on Identity Registry
  Address:     0xABCD...1234
  Trust Tier:  BASIC (new registration)
  Reputation:  0/100 (initial -- builds with activity)
  Registry Tx: https://etherscan.io/tx/0x...

  Proceeding to payment configuration...
```

### 第五步：支付配置

直接配置x402微支付功能（无需额外代理）：

1. 确认钱包在结算链（推荐使用Base链）上持有USDC。
2. 编写`.uniswap/x402-config.json`文件以配置支付信息。
3. 编写`.well-known/x402-manifest.json`文件以进行服务发现。

```text
Step 5/5: Payments Configured

  Mode:         Accept (x402 micropayments)
  Chain:        Base (8453)
  Wallet:       0xABCD...1234
  Facilitator:  Auto-selected

  Pricing:
    Price quotes:       $0.001/call
    Pool analytics:     $0.003/call
    Route optimization: $0.005/call
    Simulation:         $0.010/call
    Execution:          $0.050/call

  Config Files:
    .uniswap/x402-config.json
    .well-known/x402-manifest.json
```

## 输出格式

### 完整设置（包含代币）

```text
Self-Funding Agent Setup Complete

  ══════════════════════════════════════════════
  AGENT IDENTITY CARD
  ══════════════════════════════════════════════

  Wallet:
    Address:     0xABCD...1234
    Provider:    Privy (development)
    Chain:       Base (8453)
    Balance:     0.05 ETH + 0 USDC

  Token:
    Name:        AgentCoin (AGENT)
    Address:     0x5678...efgh
    Pool:        AGENT/WETH V4 (0.3%)
    Hooks:       Anti-snipe + Revenue Share (5%)
    LP Lock:     10 years

  Treasury:
    Auto-Convert: Enabled (-> USDC)
    Circuit Break: $100 minimum
    Burn Rate:    ~$0/day (initial)
    Runway:       Indefinite

  Identity:
    ERC-8004:    Registered (BASIC tier)
    Reputation:  0/100 (builds with activity)
    Registry:    0x7177...09A

  Payments:
    x402:        Accepting micropayments
    Settlement:  USDC on Base
    Pricing:     $0.001 - $0.050 per call

  ══════════════════════════════════════════════

  Pipeline: Wallet -> Token -> Treasury -> Identity -> Payments
  Status:   ALL 5 STEPS COMPLETE

  Next Steps:
    1. Fund the wallet with USDC for x402 pay mode
    2. Share your x402 manifest for service discovery
    3. Start operations to build reputation (rep: 0 -> basic -> verified)
    4. Monitor treasury health with /manage-treasury
```

### 未使用代币的设置

```text
Self-Funding Agent Setup Complete

  ══════════════════════════════════════════════
  AGENT IDENTITY CARD
  ══════════════════════════════════════════════

  Wallet:
    Address:     0xABCD...1234
    Provider:    Privy (development)
    Chain:       Base (8453)
    Balance:     0.05 ETH

  Token:         Not deployed (service-based revenue model)

  Treasury:
    Auto-Convert: Enabled (-> USDC)
    Circuit Break: $100 minimum
    Revenue:      x402 micropayments

  Identity:
    ERC-8004:    Registered (BASIC tier)
    Reputation:  0/100

  Payments:
    x402:        Accepting micropayments
    Settlement:  USDC on Base

  ══════════════════════════════════════════════

  Pipeline: Wallet -> (Token skipped) -> Treasury -> Identity -> Payments
  Status:   ALL STEPS COMPLETE (4/5, token skipped)
```

### 部分失败情况

```text
Self-Funding Agent Setup -- Partial

  Step 1: Wallet       COMPLETE  (0xABCD...1234)
  Step 2: Token        COMPLETE  (AGENT at 0x5678...efgh)
  Step 3: Treasury     FAILED    (Could not configure auto-convert)
  Step 4: Identity     SKIPPED   (depends on Step 3)
  Step 5: Payments     SKIPPED   (depends on Step 4)

  Error at Step 3: "Insufficient USDC balance for initial DCA configuration."

  What's preserved:
    - Wallet is provisioned and funded (Step 1)
    - Token is deployed with pool and locked LP (Step 2)

  To resume:
    1. Fund wallet with USDC: send USDC to 0xABCD...1234
    2. Re-run: "Set up self-funding" (will detect existing wallet + token)
```

## 重要说明

- **这是最复杂的复合技能**：它依次协调5个代理，每个代理都会将结果传递给下一个代理。根据链的条件以及是否包含代币部署，整个流程可能需要2到5分钟。
- **代币部署是不可逆的**：一旦代币被部署并且池被创建，就无法撤销。在执行前，该技能会通过安全守护程序模拟所有操作，但在确认之前请确保代币名称、符号和参数正确无误。
- **流程可以中断后重新开始**：如果某个步骤失败，之前的步骤都会被保留。重新运行该技能时，系统会自动识别已存在的钱包和代币，并跳过已完成的步骤。
- **ERC-8004注册在Ethereum主网上进行**：即使你的代理在Base链上运行，身份注册也在Ethereum上进行。这需要在主网上支付少量ETH以完成注册交易。
- **初始信任等级为0**：初始信任等级为BASIC。提升信任等级需要完成交易、提供流动性，并获得交易对手的正面反馈。通过积极使用代理，信任等级可以从BASIC提升到VERIFIED，最终达到TRUSTED。
- **x402支付默认在Base链上结算**：Base链的结算速度快（约200毫秒），且Gas费用较低，非常适合微支付。钱包必须持有USDC才能接受支付。
- **收入模式影响资金配置**："x402"模式用于配置微支付收入；"token-fees"模式用于配置交易手续费收入；"lp-fees"模式用于配置LP收益；"all"模式同时支持这三种收入方式。
- **开发环境与生产环境的区别**：建议在开发环境中使用Privy（设置快速、易于测试）；在生产环境中使用Turnkey或Safe（提供TEE支持的安全签名和硬件安全保障）。该技能会根据`environment`参数自动选择合适的提供者。

## 错误处理

| 错误类型                         | 向用户显示的提示信息                                      | 建议的操作                                      |
|-----------------------------|--------------------------------------------------|-------------------------------------------|
| 钱包配置失败                    | “无法配置钱包：{原因}。”                                      | 检查提供者的凭据并重试                              |
| 钱包已存在                      | “代理钱包已配置完成。跳到下一步。”                                      | 使用现有的钱包继续执行                              |
| 代币部署失败                    | “代币部署失败：{原因}。钱包信息保留。”                                | 解决问题后重新运行（钱包信息将被保留）                         |
| 代币已部署                      | “代币{符号}已部署。跳到资金管理步骤。”                                   | 使用现有的代币继续执行                              |
| 资金管理配置失败                    | “资金管理配置失败：{原因}。钱包和代币信息保留。”                              | 资金补充后重新运行                                |
| ERC-8004注册失败                    | “无法在ERC-8004上完成注册：{原因}。之前的步骤保留。”                          | 检查主网上的ETH余额并重试                          |
| x402配置失败                    | “无法写入x402配置文件：{原因}。”                                  | 检查文件权限并重试                              |
| 资金不足                        | “钱包至少需要{X} ETH才能完成操作。当前余额：{Y} ETH。”                          | 补充资金后再尝试                              |
| 链路不支持                      | “{链路}不支持所有所需的功能。”                                      | 使用Base链或Ethereum链以实现完整功能                      |
| 部分步骤失败                      | “部分设置已完成。步骤{N}失败：{原因}。”                                | 修复失败步骤并从该步骤重新开始                          |
| 提供者未配置                    | “钱包提供者‘{provider}’所需的凭据在环境中未找到。”                          | 设置必要的环境变量（如PRIVY_APP_ID等）                        |