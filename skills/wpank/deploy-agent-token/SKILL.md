---
name: deploy-agent-token
description: 部署一个代理令牌（agent token），该令牌与 Uniswap V4 池（pool）集成。该方案支持配置自定义的钩子（hooks）来管理池的创建过程（包括防止恶意抢购、动态费用设置、收益分配机制），同时涵盖初始流动性的注入、LP（ Liquidity Provider）的锁定机制以及部署后的监控功能。适用于用户希望在 Uniswap 平台上发行代币的场景。
model: opus
allowed-tools: [Task(subagent_type:token-deployer)]
---

# 部署代理令牌（Deploy Agent Token）

## 概述

该功能自动化了在Uniswap V4平台上部署令牌的整个生命周期，包括配置可定制的钩子（hooks）来创建池（pool）、启动初始流动性、锁定LP（liquidity pool）令牌，以及部署后的监控。这些操作由`token-deployer`代理负责执行，确保令牌在上线初期能够得到有效的保护（如防止恶意抢购）、维持合理的初始价格、足够的流动性，并锁定LP令牌。

这类功能的存在，是因为像Clanker（拥有超过58.5万个令牌、交易量超过50亿美元）和BankrBot这样的代理平台需要自动化且安全的池创建流程。配置错误的池、缺失的防抢购机制或流动性不足都可能导致部署失败。

## 使用场景

当用户提出以下请求时，可激活此功能：
- “为我的代理部署一个令牌”
- “为我的令牌创建一个Uniswap V4池”
- “以防抢购保护的方式部署令牌”
- “设置具有动态费用的池”
- “在Base平台上部署带有锁定流动性的令牌”
- “像Clanker那样部署我的代理令牌”
- “创建具有收益分享机制的池”
- “为新令牌启动流动性”

## 参数

| 参数                          | 是否必填 | 默认值    | 说明                                                                                          |
| --------------------------- | -------- | ---------- | ------------------------------------------------------------------------------------------- |
| tokenAddress       | 是      | --         | 需要创建池的ERC-20令牌合约地址                                                                                   |
| pairedToken        | 否       | WETH       | 用于配对的报价令牌（WETH、USDC或地址）                                                                                   |
| chain              | 否       | base       | 部署的目标链（必须支持Uniswap V4）                                                                                   |
| initialPrice       | 否       | --         | 每个令牌的期望价格（或根据`targetMarketCap`计算）                                                                         |
| targetMarketCap    | 否       | --         | 目标市场市值（以美元计），用于根据总供应量计算初始价格                                                                         |
| initialLiquidity   | 是      | --         | 用于初始化池的每个令牌的数量（例如：“100万个AGENT令牌 + 10万WETH”                                                                         |
| hooks              | 否       | anti-snipe | 钩子配置：“anti-snipe”、“dynamic-fees”、“revenue-share”或这些配置的组合     |
| antiSnipeDelay     | 否       | 2个区块     | 防抢购延迟时间（基于ClankerHook模型）                                                                                   |
| revenueSharePct    | 否       | --         | 交易费用中分配给令牌创建者的比例（如果启用了收益分享机制）                                                                     |
| lpLockDuration     | 否       | 10年       | LP令牌的锁定期限（例如：“10年”、“1年”、“6个月”                                                                                   |
| vestingSchedule    | 否       | --         | 令牌分配的可选解锁时间表                                                                                         |

### 钩子配置指南

- **Anti-snipe**（默认推荐）：通过2个区块的延迟来防止机器人抢购（基于ClankerHook模型）。如果没有这个延迟，机器人可能在几秒钟内耗尽初始流动性。
- **Dynamic fees**：根据波动性或交易量调整池费用。适用于早期交易模式不可预测的令牌。
- **Revenue share**：将部分交易费用分配给令牌创建者，从而产生持续的收入流。
- **TWAMM**：时间加权平均做市（Time-Weighted Average Market Making），帮助在部署期间逐步发现合理价格。

## 工作流程

1. **从用户请求中提取参数**：确定令牌地址、配对令牌、目标链、初始价格或市场市值、流动性数量、钩子配置以及LP锁定期限。验证是否提供了必需的参数（令牌地址、初始流动性）。如果未指定初始价格但指定了目标市场市值，系统会根据总供应量计算价格。
2. **委托给`token-deployer`代理**：使用提取的参数调用`Task(subagent_type:token-deployer)`。代理会执行7个步骤的流程：
   - **验证令牌**：通过元数据（名称、符号、小数位数、供应量、风险标志）检查令牌合约。如果检测到恶意代码，将拒绝创建池。
   - **配置钩子**：选择并验证V4兼容的钩子，确认它们已部署在目标链上，并计算钩子的地址要求。
   - **创建池**：计算`sqrtPriceX96`，构建池密钥，通过`safety-guardian`进行模拟，然后执行初始化操作。
   - **启动流动性**：委托给`lp-strategist`确定最佳费用范围，并通过`position manager`添加流动性。
   - **锁定LP**：将相关NFT转移到时间锁定的保险库中，并设置锁定期限。
   - **监控**：在关键的上线初期阶段跟踪价格、交易量、总价值（TVL）和异常情况。
   - **生成报告**：为用户生成详细的部署报告。

代理内部会委托`safety-guardian`（负责交易验证）和`lp-strategist`（负责流动性策略）来执行这些操作。

## 代理委托（Agent Delegation）

```
Task(subagent_type:token-deployer)
  tokenAddress: <0x...>
  pairedToken: <WETH|USDC|address>
  chain: <base|ethereum|...>
  initialPrice: <price in paired token>
  targetMarketCap: <USD value>
  initialLiquidity: <amounts>
  hooks: <anti-snipe,dynamic-fees,revenue-share>
  antiSnipeDelay: <2 blocks>
  revenueSharePct: <percentage>
  lpLockDuration: <10 years>
  vestingSchedule: <schedule>
```

## 输出格式

```text
Token Deployment Complete

  Pool:
    Address:    0x1234...abcd
    Chain:      Base (8453)
    Version:    V4
    Pair:       AGENT / WETH
    Fee:        0.30% (tick spacing: 60)
    Hooks:      Anti-snipe (2-block delay) + Dynamic fees
    Init Price: 0.001 WETH per AGENT

  Liquidity:
    Position:   #12345
    Amount:     1,000,000 AGENT + 10 WETH
    Range:      Full range
    Status:     Active

  LP Lock:
    Vault:      0x5555...6666
    Duration:   10 years (unlocks 2036-02-10)
    Position:   #12345

  Early Monitoring (1h):
    Price:      0.00105 WETH (+5.0%)
    Volume:     $45,000
    TVL:        $20,000
    Anomalies:  None detected

  Next Steps:
    - Monitor pool health over the first 24 hours
    - Consider adding more liquidity if TVL grows
    - Share pool address for community trading
```

## 重要说明

- 池的创建是不可逆的。每次创建池的交易都会在广播前通过`safety-guardian`进行模拟。
- 防抢购钩子默认是启用的，强烈建议使用。如果不使用，机器人可能会在几秒钟内耗尽初始流动性。
- 所有钩子合约必须在目标链上部署并验证后才能应用于池中。未经验证的钩子可能会导致资金损失。
- 如果该令牌对已经存在具有足够流动性的池，系统会警告用户并建议将其添加到现有池中。
- LP令牌的锁定有助于建立市场信心。默认的10年锁定期限遵循Clanker模型。虽然可以设置更短的锁定期限，但可能会降低交易者的信心。
- 初始价格的计算非常重要。代理会核对价格与令牌供应量和目标市场市值，以防止配置错误。
- 部署后的监控会在最初几个小时内持续进行，以检测异常情况（如中间人攻击、异常交易、流动性流失等）。

## 错误处理

| 错误类型                         | 向用户显示的消息                                                                 | 建议的操作                                                                                                 |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| 令牌验证失败                        | “无法在[地址]验证令牌：[原因]。”                                                                 | 检查令牌合约地址和目标链                                                                                   |
| 检测到恶意代码                         | “令牌存在恶意代码，拒绝创建池。”                                                                 | 审查令牌合约是否存在恶意代码                                                                                   |
| 已存在池                         | “该令牌对已经存在一个TVL为[X]的池。建议添加流动性。”                                                                 | 使用`manage-liquidity`功能将令牌添加到现有池中                                                                                   |
| 钩子未部署                         | “[类型]钩子未在[链]上部署。”                                                                 | 先部署钩子或选择其他类型的钩子                                                                                   |
| 不支持Uniswap V4                     | “[链]不支持Uniswap V4。”                                                                 | 选择支持V4的链                                                                                         |
| 流动性不足                         | “用于初始化池的[令牌]数量不足：当前有[X]个，需要[Y]个。”                                                                 | 获取更多令牌或减少初始流动性                                                                                   |
| 安全保护机制拒绝交易                     | “交易被安全保护机制拒绝：[原因]。”                                                                 | 查看拒绝原因并调整参数                                                                                         |
| LP锁定失败                         | “无法锁定LP令牌：[原因]。”                                                                 | 检查目标链上的保险库合约可用性                                                                                   |
| 无法估算交易费用                         | “无法估算在[链]上创建池所需的气体费用。”                                                                 | 重试或检查链的状态                                                                                         |