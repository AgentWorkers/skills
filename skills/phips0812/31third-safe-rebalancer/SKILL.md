---
name: 31third-safe-rebalancer
description: 基于策略的安全投资组合再平衡辅助工具，适用于31Third ExecutorModule。
homepage: https://31third.com
---
# 31Third 安全再平衡器（Safe Rebalancer）

该技能可帮助您监控投资组合的变动情况，并通过 31Third 的 `ExecutorModule` 在 Gnosis Safe 平台上执行符合政策要求的再平衡操作。

**最佳使用实践：**
- 默认情况下，建议使用一步式执行命令：`npm run cli -- rebalance-now`。
- 仅当您完全了解每个执行步骤并希望进行手动控制时，才使用单独的工具（如 `check_drift`、`plan_rebalance`、`execute_rebalance` 等）。
- 如果不确定如何使用，请先运行 `help` 命令（`npm run cli -- help`），然后按照提示操作。

## 先决条件
- Node.js 22 及更高版本
- npm

## 本地环境配置
（具体配置内容见下方代码块）

## 开始使用
如果您尚未部署策略堆栈，请先完成部署：
<https://app.31third.com/safe-policy-deployer>

请设置以下环境变量：
（具体环境变量设置内容见下方代码块）

`TOT_API_KEY`（31Third API 密钥）可通过 <https://31third.com/contact> 获取，或发送电子邮件至 `dev@31third.com` 申请。

**钱包模型与密钥管理：**
- **Safe 所有者钱包**：用于控制 Safe 的所有权和管理操作。切勿将此私钥共享给该技能。
- **执行器钱包**：在向导中配置为 `ExecutorModule` 的执行器。该私钥是执行 `execute_rebalance` 功能所必需的。
- 31Third 向导的最终步骤会提供所有所需环境变量的详细信息，请以此作为配置该技能的依据。

## 该技能的功能：
- 从 `ExecutorModule` 读取当前链上的策略信息。
- 计算当前投资组合与目标投资组合之间的差异（`check_drift`）。
- 根据资产范围（Asset Universe）和滑点限制（Slippage boundaries）验证交易（`validate_trade`）。
- 运行可配置的心跳监控机制（`automation`），并在差异超过阈值时发送警报。
- 模拟并执行已批准的再平衡操作（`execute_rebalance`），在执行前会进行 `checkPoliciesVerbose` 验证，并在遇到执行失败时尝试重试一次。
- 直接接收 SDK 提供的再平衡计划输出（`txData` 和 `requiredAllowances`），并在内部解码批量交易数据。
- 如果 `ExecutorModule` 中的 `scheduler` 与 `registry` 不匹配，会立即终止执行并显示两个地址的信息。
- 根据当前 Safe 的余额（在存在资产范围限制的情况下）生成基于策略的交易计划（`plan_rebalance`）。
- 为非技术用户提供一键式执行功能（`rebalance_now`）：先检查投资组合差异，再生成再平衡计划，最后执行再平衡操作。
- 提供相关设置和操作指南（`help`）。

## 执行安全性
在执行前，该技能会提供明确的提示信息，例如：
“BTC 的当前占比为 54.00%，目标占比为 50.00%（差异为 400 bps），需要执行再平衡。”

**技术实现细节：**
- 该技能使用 Viem 的 `publicClient` 进行所有数据读取操作。
- 使用 Viem 的 `walletClient` 进行交易执行。

## 执行合约注意事项（重要）
在使用 SDK 或交易 API 进行再平衡操作时，必须遵循以下规则：
1. 从 `requiredAllowances` 中构建交易批准信息（格式为 `(tokenAddress, neededAllowance)`）。
2. 将 `txData` 解码为 `batchTrade(trades, config)` 格式。
3. 将解码后的交易数据重新编码为 ABI 格式（格式如下）：
   ```
   tuple(string, address, uint256, address, uint256, bytes, bytes)[]
   tuple(bool, bool)
   ```
4. 在提交交易前，先运行 `checkPoliciesVerbose(tradesInput, configInput)` 验证。
5. 从 `ExecutorModule` 中读取 `scheduler` 和 `registry` 的信息。
6. 确保执行器钱包的地址与 `registry` 的地址一致（这是 `onlyRegistry` 规则的要求）。
7. 仅当 `scheduler` 等于 `registry` 时，才执行交易（`executeTradeNow(approvals, encodedTradeData)`）。
8. 如果 `scheduler` 与 `registry` 不匹配，立即终止执行并显示两个地址的信息。

**命令行界面（CLI）**
请运行捆绑提供的 CLI 工具：
（具体 CLI 使用方法见下方代码块）

**测试说明：**
- 该技能仅用于自动化流程，不提供投资建议。
- 在正式生产环境中使用前，请先在测试或 staging 环境中验证其功能是否正常。

## 注意事项：
- 该技能属于自动化工具，不提供投资建议。
- 在正式生产环境中使用前，请确保其在测试或 staging 环境中的行为符合预期。