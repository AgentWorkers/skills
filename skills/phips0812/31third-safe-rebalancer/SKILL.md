---
name: safe-rebalancer
description: 通过 31Third，在 EVM 链上执行受策略保护的代币交换操作以及投资组合的再平衡操作。
homepage: https://31third.com
metadata: {"openclaw":{"skillKey":"31third-safe-rebalancer","homepage":"https://31third.com","requires":{"env":["RPC_URL","CHAIN_ID","TOT_API_KEY","SAFE_ADDRESS","EXECUTOR_MODULE_ADDRESS","EXECUTOR_WALLET_PRIVATE_KEY"],"bins":["node"]},"primaryEnv":"TOT_API_KEY"}}
---

# 31Third 安全再平衡器（Safe Rebalancer）

该技能通过 31Third 的基础设施执行链上交易，并在交易执行前进行一系列策略检查（如每日交易限额、白名单设置、滑点控制等）。

## 代理所有者（Agent Owners）的设置步骤

首先，将 31Third 的执行环境部署到您的 Safe 系统中：
- 部署向导：<https://app.31third.com/safe-policy-deployer>
1. 从 <https://31third.com> 获取 API 密钥。
2. 使用向导部署 Safe 的策略执行器（Policy Executor）。
3. 设置环境变量：

```bash
RPC_URL=https://mainnet.base.org
CHAIN_ID=8453
TOT_API_KEY=your_api_key_here
SAFE_ADDRESS=your_safe_address
EXECUTOR_MODULE_ADDRESS=deployed_module_address
EXECUTOR_WALLET_PRIVATE_KEY=agent_hot_wallet_private_key
```

## 功能概述

- **代币兑换**（例如：USDC -> WETH）
- **投资组合再平衡**（将投资组合调整至目标权重）
- **策略检查**（确保交易符合预设规则）

## 使用方法

### 简单代币兑换

```bash
node {baseDir}/scripts/trade.js --action swap --from 0xUSDC... --to 0xWETH... --amount 1000000 --chain base
```

### 投资组合再平衡

```bash
node {baseDir}/scripts/trade.js --action rebalance --targets '{"0xWETH...": 0.5, "0xUSDC...": 0.5}' --chain-id 8453
```

### 策略检查

```bash
node {baseDir}/scripts/trade.js --action checkPolicy
node {baseDir}/scripts/inspect_policies_advanced.js
node {baseDir}/scripts/check_target_executor.js
```

## 必需的配置参数

- `RPC_URL`：用于与 31Third 服务器通信的 API 地址
- `CHAIN_ID`（可选，默认值为 `8453`）
- `TOT_API_KEY`：全局 API 密钥
- `SAFE_ADDRESS`：Safe 系统的地址
- `EXECUTOR_MODULE_ADDRESS`：策略执行器的模块地址
- `EXECUTOR_WALLET_PRIVATE_KEY`：策略执行器的钱包私钥

## 免责声明

- 本技能仅作为基础设施工具提供，并不提供财务、投资、法律或税务方面的建议。
- 操作者需完全负责策略的配置、签名者的安全设置、交易执行的审批以及合规性检查。
- 在启用实时交易之前，请在非生产环境中验证该技能的运行效果。

## 参考资料

- 有关 SDK 的详细信息，请参阅 `references/SDK.md`。