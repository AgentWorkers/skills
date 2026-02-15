---
name: setup-local-testnet
description: >-
  Spin up a local Anvil testnet with Uniswap deployed and pre-seeded liquidity.
  One command gives you a full development environment with funded accounts,
  real Uniswap pools, and zero gas costs. Use when developing, testing, or
  demoing Uniswap agent workflows.
model: sonnet
allowed-tools:
  - mcp__uniswap__setup_local_testnet
  - mcp__uniswap__fund_test_account
  - mcp__uniswap__get_supported_chains
---

# 设置本地测试网

## 概述

该功能会创建一个基于Anvil的本地测试网，该测试网是从实际运行中的以太坊链分叉而来的，包含所有Uniswap合约、预先资助的测试账户以及真实的交易池状态。这是所有本地测试的基础——其他所有本地测试功能都依赖于这个测试网。

**为什么这种方式比手动操作好10倍：**

1. **一键完成**：无需编写30多行的Shell脚本来启动Anvil、模拟大资金持有者的操作、为账户充值或验证合约，只需输入“设置本地测试网”，即可完成所有设置。
2. **预资助的账户**：每个测试账户都会获得10,000 ETH、100万USDC、100万USDT、1万DAI和1万UNI，适用于各种测试场景。
3. **真实的交易池状态**：采用分叉模式，因此可以访问具有真实流动性和价格的Uniswap交易池，无需进行任何模拟操作。
4. **合约地址自动获取**：会返回所有相关的Uniswap合约地址（如V3Factory、NonfungiblePositionManager、UniversalRouter、Permit2、QuoterV2），便于立即进行交互。
5. **端口自动管理**：工具会自动选择可用端口，处理端口冲突，并清理之前的测试网残留数据。
6. **后续集成便捷**：生成的测试环境可以直接用于`create-test-pool`和`time-travel`等功能。

## 适用场景

当用户提出以下请求时，可以使用此功能：
- “设置一个本地测试网”
- “启动一个基于Anvil的本地测试网”
- “我需要一个用于Uniswap的测试环境”
- “在本地分叉以太坊链”
- “创建一个开发环境”
- “我想在不消耗真实Gas的情况下进行测试”
- “启动包含Uniswap功能的Anvil测试环境”
- “为我的测试代理创建一个测试环境”

**不适用场景**：
- 如果用户已经运行了测试网，但只是想添加新的交易池（请使用`create-test-pool`功能）或回溯时间（请使用`time-travel`功能）。

## 参数

| 参数                | 是否必填 | 默认值            | 获取方式                                                                                                                         |
|------------------|--------|------------------|-------------------------------------------------------------------------------------------------------------------------|
| mode                | 否       | fork             | “fork”或“mock”（默认推荐模式）                                                                                              |
| forkFrom             | 否       | ethereum         | “ethereum”、“base”、“arbitrum”、“optimism”、“polygon”                                                                                         |
| blockNumber          | 否       | latest            | 如果用户指定了具体的区块号                                                                                                      |
| seedLiquidity        | 否       | true             | 仅当用户请求“空测试网”或“不使用代币”时设置为false                                                                                         |
| fundedAccounts        | 否       | 3               | 用户指定的账户数量（1-5个）                                                                                                      |
| port                | 否       | auto             | 如果用户指定了具体的端口，则使用该端口                                                                                                   |

## 工作流程

### 第1步：检查前提条件

在调用`mcp`工具之前，请确认以下条件：
1. **Anvil是否已安装**：如果未安装Anvil，工具会返回错误提示。如果看到`TESTNET_ANVIL_NOT_FOUND`，请告知用户：
   ```
   Anvil (Foundry) is required but not installed.
   Install: curl -L https://foundry.paradigm.xyz | bash && foundryup
   ```

2. **网络连接**：分叉模式需要能够访问以太坊链的RPC接口。如果看到`TESTNET_STARTUP_TIMEOUT`，请检查网络连接或尝试其他以太坊链。

### 第2步：解析用户请求

根据用户的输入，提取相关参数：
- 选择的以太坊链：例如“fork Base” → 设置`forkFrom: "base"`
- 特定区块号：例如“从区块19000000开始分叉” → 设置`blockNumber: 19000000`
- 账户数量：例如“创建5个测试账户” → 设置`fundedAccounts: 5`
- 是否需要预资助：例如“创建空测试网” → 设置`seedLiquidity: false`

如果用户没有指定具体参数，将使用默认值（使用以太坊链、创建3个账户、启用资金支持）。

### 第3步：调用`setup_local_testnet`函数

使用提取到的参数调用`mcp__uniswap__setup_local_testnet`函数。

### 第4步：展示结果

以易于理解的格式呈现测试网设置结果：
```text
Local Testnet Ready

  RPC URL:    http://127.0.0.1:8545
  Chain ID:   31337
  Mode:       Fork of Ethereum at block 19,234,567

  Funded Accounts:
  ┌──────────────────────────────────────────────────────────────────────┐
  │ #  Address                                    ETH       USDC        │
  │ 1  0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 10,000    1,000,000  │
  │ 2  0x70997970C51812dc3A010C7d01b50e0d17dc79C8 10,000    1,000,000  │
  │ 3  0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC 10,000    1,000,000  │
  └──────────────────────────────────────────────────────────────────────┘

  Key Contracts:
    V3Factory:                      0x1F98431c8aD98523631AE4a59f267346ea31F984
    NonfungiblePositionManager:     0xC36442b4a4522E871399CD717aBDD847Ab11FE88
    UniversalRouter:                0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD
    Permit2:                        0x000000000022D473030F116dDEE9F6B43aC78BA3
    QuoterV2:                       0x61fFE014bA17989E743c5F6cB21bF9697530B21e

  Available Pools (from fork):
    USDC/WETH 0.05% (V3)  — 0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640
    USDC/WETH 0.30% (V3)  — 0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8
    USDT/WETH 0.30% (V3)  — 0x4e68Ccd3E89f51C3074ca5072bbAC773960dFa36
    WBTC/WETH 0.30% (V3)  — 0xCBCdF9626bC03E24f779434178A73a0B4bad62eD

  Private Keys (for wallet config):
    Account #1: 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
    Account #2: 0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d
    Account #3: 0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a
```

### 第5步：提供后续操作建议

最后，给出具体的下一步操作建议：
```text
  Next Steps:
  - Create a custom pool: "Create a WETH/DAI pool with thin liquidity"
  - Test time-dependent logic: "Advance time by 7 days"
  - Test a swap: "Get a quote for 1 WETH → USDC on the local testnet"
  - Fund more tokens: "Fund account #1 with 10,000 WBTC"
  - Configure your MCP server: Set RPC_URL_1=http://127.0.0.1:8545 in .env
```

## 重要注意事项

- **必须安装Anvil**：此功能依赖于Foundry提供的Anvil工具。如果未安装，请提供安装命令。
- **分叉模式需要网络连接**：工具会从实际链的RPC接口下载初始数据，后续操作均在本地环境中进行。
- **端口冲突会自动处理**：如果端口8545已被占用，工具会自动选择其他可用端口。
- **会清理之前的测试网残留数据**：启动新测试网时会清除所有旧的测试网数据。
- **使用的私钥为预设的测试密钥**：这些密钥仅用于测试环境，切勿在主网上使用。
- **测试网会持续运行，直到`mcp`服务器进程结束或新的测试网启动**。

## 错误处理

| 错误类型                | 显示给用户的提示信息                                      | 建议采取的措施                                                                                                      |
|------------------|--------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| `TESTNET_ANVIL_NOT_FOUND`      | “Anvil（Foundry提供的工具）未安装。”                                      | 安装Anvil：`curl -L https://foundry.paradigm.xyz \| bash && foundryup`                         |
| `TESTNET_STARTUP_TIMEOUT`      | “Anvil未能在30秒内启动。可能是网络问题或RPC接口不可用。”                        | 检查网络连接或尝试其他以太坊链                         |
| `TESTNET_INVALID_FORK_chain`   | “当前链不支持分叉操作。”                                      | 选择支持的以太坊链（如ethereum、base、arbitrum、optimism或polygon）                   |
| `TESTNET_MOCK_NOTImplemented` | “模拟模式尚未实现。”                                      | 使用分叉模式（fork）                                                                                         |
| `TESTNET_setup_FAILED`         | “设置测试网失败：{错误原因}”                                    | 检查Anvil的安装情况和网络连接                         |