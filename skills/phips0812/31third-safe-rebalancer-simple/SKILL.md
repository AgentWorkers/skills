---
name: 31third-safe-rebalancer-simple
description: 基于链上31Third策略的一步式安全再平衡器。
homepage: https://31third.com
---
# 31Third 安全再平衡器（Simple）

此功能专为非技术用户设计，其功能被刻意简化。

最佳实践：仅使用一个命令/一个工具：
- `rebalance_now`
- `verify_deployment_config`（部署后的故障排查）

如果您不确定如何操作，请先使用帮助命令：
- `npm run cli -- help`

## 先决条件
- Node.js 22 及更高版本
- npm

## 本地设置
```bash
npm install
npm run build
```

## 设置步骤
1. 使用 31Third 的策略部署工具来部署您的 Safe 及相关策略：
   <https://app.31third.com/safe-policy-deployer>
2. 您至少需要两个钱包：
   - Safe 所有者钱包：切勿分享此私钥。
   - 执行者钱包：在策略部署工具中的 `ExecutorModule` 部分进行配置；此私钥将用于执行再平衡操作。
3. 复制策略部署工具最终页面显示的环境变量。

所需的环境变量：
```bash
SAFE_ADDRESS=0xYourSafe
EXECUTOR_MODULE_ADDRESS=0xYourExecutorModule
EXECUTOR_WALLET_PRIVATE_KEY=0x...
TOT_API_KEY=your_31third_api_key
RPC_URL=https://mainnet.base.org
CHAIN_ID=8453
```

`TOT_API_KEY` 可以通过 <https://31third.com/contact> 获取，或发送电子邮件至 `dev@31third.com` 请求。

## `rebalance_now` 的功能
1. 从 `ExecutorModule` 读取 `AssetUniverse` 和 `StaticAllocation` 策略的状态。
2. 根据当前 Safe 账户中的余额，生成用于 AssetUniverse 代币的 `baseEntries`。
3. 根据链上的 `StaticAllocation` 配置生成 `targetEntries`。
4. 调用 SDK 的 `calculateRebalancing()` 函数。
5. 使用 ethers钱包的签名功能执行 `executeRebalancing()` 函数。
6. 等待交易确认并返回交易哈希值。

安全检查：
- 如果 `scheduler` 与 `registry` 不匹配，则操作失败。
- 如果执行者钱包与 `registry` 不一致，则操作失败。
- 如果缺少所需的策略，则操作失败。
- 从 `StaticAllocation` 中读取 `driftThresholdBps`；如果漂移率低于阈值，则跳过再平衡操作。
- 从 `SlippagePolicy` 中读取 `maxSlippageBps`，并使用以下公式计算最大滑点：
  - `maxSlippage = policySlippage - 0.1%`
  - `maxPriceImpact = policySlippage - 0.1%`
- 默认的 `minTradeValue` 为 0.1。

### 部分策略未部署时的处理方式
- 如果 `AssetUniverse` 策略未部署，`baseEntries` 将默认为空数组（`[]`）。
- 如果 `SlippagePolicy` 未部署，将使用配置的默认滑点值。
- 如果 `StaticAllocation` 未部署，则无法自动查找交易目标；此时需要手动提供 `targetEntries`。请仅在确实有意不部署 `StaticAllocation` 策略时使用此方法。
  CLI 示例：
  `npm run cli -- rebalance-now --target-entries '[{"tokenAddress":"0x...","allocation":0.5},{"tokenAddress":"0x...","allocation":0.5}]'`

## 命令行界面（CLI）
```bash
npm run cli -- help
npm run cli -- rebalance-now
npm run cli -- rebalance-now --target-entries '[{"tokenAddress":"0x...","allocation":0.5},{"tokenAddress":"0x...","allocation":0.5}]'
npm run cli -- verify-deployment --troubleshooting-file ./summary.txt
npm run cli -- verify-deployment --troubleshooting-summary "Safe=0x..."
```

## 故障排查与最佳实践
如果再平衡操作失败，请检查以下常见问题：

### 1. 部署的合约与您的环境配置不匹配
使用 `verify-deployment` 工具来验证部署的合约是否符合您的环境配置。
请参考 Safe 策略部署工具中的故障排查信息（步骤 4 或步骤 5）。

### 2. 错误提示：“Policy failed: to token not allowed”
您的 `AssetUniverse` 策略禁止了某些代币的交易。
- **解决方法：** 仅使用策略允许的交易代币进行再平衡操作。

### 3. 错误提示：“Policy failed: minToReceive below...”
交易滑点过高。
- **原因：** 相关代币对的流动性较低（常见于 Aave 的 `aTokens` 或新链上的封装资产）。
- **解决方法：** 在调用再平衡函数时尝试降低 `maxSlippage` 和 `maxPriceImpact` 的值。

### 4. 错误提示：“Missing StaticAllocation policy”
脚本无法在链上找到目标分配信息。
- **解决方法：** 运行 `verify-deployment` 工具；如果策略确实是故意未部署的，您可以任意选择一个 `AssetUniverse` 内的分配方案进行再平衡操作。