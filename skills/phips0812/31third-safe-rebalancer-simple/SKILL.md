---
name: 31third-safe-rebalancer-simple
description: 基于链上31Third策略的一键式安全再平衡器。
homepage: https://31third.com
---
# 31Third Safe Rebalancer Simple

此功能专为非技术用户设计，其功能被刻意简化。

最佳实践：仅使用一个命令/一个工具：

- `rebalance_now`

如果您不确定如何操作，请先使用帮助命令：

- `npm run cli -- help`

## 设置

1. 使用 31Third 的策略向导来部署您的 Safe 及相关策略：
   <https://app.31third.com/safe-policy-deployer>
2. 您至少需要两个钱包：
   - Safe 所有者钱包：切勿分享此私钥。
   - 执行者钱包：在向导的 `ExecutorModule` 部分进行配置；此私钥将用于执行此功能。
3. 从向导的最终概述中复制环境变量（env vars）。

所需的环境变量：

```bash
SAFE_ADDRESS=0xYourSafe
EXECUTOR_MODULE_ADDRESS=0xYourExecutorModule
EXECUTOR_WALLET_PRIVATE_KEY=0x...
TOT_API_KEY=your_31third_api_key
RPC_URL=https://mainnet.base.org
CHAIN_ID=8453
```

`TOT_API_KEY` 可以通过 <https://31third.com> 获取，或发送电子邮件至 `dev@31third.com` 请求。

## `rebalance_now` 的功能

1. 从 `ExecutorModule` 读取 `AssetUniverse` 和 `StaticAllocation` 策略的状态。
2. 根据当前的 Safe 持有量，生成 `AssetUniverse` 代币的 `baseEntries`。
3. 根据链上的 `StaticAllocation` 配置生成 `targetEntries`。
4. 调用 SDK 的 `calculateRebalancing()` 函数。
5. 使用 ethers 钱包签名器执行 `executeRebalancing()` 函数。
6. 等待确认并返回交易哈希（tx hash）。

安全检查：

- 如果 `scheduler` 与 `registry` 不匹配，则操作失败。
- 如果执行者钱包与 `registry` 不相同，则操作失败。
- 如果缺少必要的策略，则操作失败。
- 从 `StaticAllocation` 中加载 `driftThresholdBps`；如果漂移率低于阈值，则跳过执行。
- 从 `SlippagePolicy` 中加载 `maxSlippageBps`，并使用以下公式计算最大允许的滑点：
  - `maxSlippage = policySlippage - 0.1%`
  - `maxPriceImpact = policySlippage - 0.1%`
- 使用默认的 `minTradeValue` 值（0.1）。

### 部分策略未部署时的处理方式：

- 如果 `AssetUniverse` 没有部署，`baseEntries` 将默认为空数组（`[]`）。
- 如果 `SlippagePolicy` 未部署，将使用配置的默认滑点值。
- 如果 `StaticAllocation` 未部署，则无法自动获取目标地址；此时需要手动提供 `targetEntries`。
  仅当 `StaticAllocation` 策略被故意未部署时才使用此方式。
  CLI 示例：
  `npm run cli -- rebalance-now --target-entries '[{"tokenAddress":"0x...","allocation":0.5},{"tokenAddress":"0x...","allocation":0.5}]'`

## 命令行界面（CLI）

```bash
npm run cli -- help
npm run cli -- rebalance-now
npm run cli -- rebalance-now --target-entries '[{"tokenAddress":"0x...","allocation":0.5},{"tokenAddress":"0x...","allocation":0.5}]'
```