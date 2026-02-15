---
name: jb-query
description: 从区块链中查询 Juicebox V5 项目的状态。可以使用 cast 或 ethers.js 读取项目配置、规则集、终端余额、代币持有者数据以及代币分配情况。支持主网（mainnet）和测试网（testnet）。
---

# Juicebox V5 连链查询

用于查询 Juicebox V5 项目的链上状态。

## 快速参考 - 合约函数

### JBProjects (ERC-721)
```solidity
count() → uint256                    // Total projects created
ownerOf(projectId) → address         // Project owner
tokenURI(projectId) → string         // Project metadata URI
```

### JBDirectory
```solidity
controllerOf(projectId) → address              // Project's controller (CRITICAL for version detection!)
terminalsOf(projectId) → IJBTerminal[]         // All terminals
primaryTerminalOf(projectId, token) → address  // Primary terminal for token
isTerminalOf(projectId, terminal) → bool       // Check terminal validity
```

**重要提示**：`controllerOf()` 是确定项目使用哪个合约版本的唯一权威方法。将返回的地址与已知的 V5/V5.1 控制器地址进行比较：
- V5.0: `0x27da30646502e2f642be5281322ae8c394f7668a`
- V5.1: `0xf3cc99b11bd73a2e3b8815fb85fe0381b29987e1`

一些非 Revnet 项目使用 V5.0 合约。切勿仅根据所有权来判断合约版本。

### JBController
```solidity
currentRulesetOf(projectId) → (JBRuleset, JBRulesetMetadata)
getRulesetOf(projectId, rulesetId) → (JBRuleset, JBRulesetMetadata)
upcomingRulesetOf(projectId) → (JBRuleset, JBRulesetMetadata)
latestQueuedRulesetOf(projectId) → (JBRuleset, JBRulesetMetadata, approvalStatus)
totalTokenSupplyWithReservedTokensOf(projectId) → uint256
pendingReservedTokenBalanceOf(projectId) → uint256
```

### JBTokens
```solidity
tokenOf(projectId) → address         // ERC-20 token address
totalBalanceOf(holder, projectId) → uint256   // Holder's token balance
totalCreditSupplyOf(projectId) → uint256      // Unclaimed credits
```

### JBMultiTerminal
```solidity
currentSurplusOf(projectId, accountingContexts, decimals, currency) → uint256
```

### JBSplits
```solidity
splitsOf(projectId, rulesetId, groupId) → JBSplit[]
```

### JBFundAccessLimits
```solidity
payoutLimitOf(projectId, rulesetId, terminal, token, currency) → uint256
usedPayoutLimitOf(projectId, terminal, token, rulesetCycleNumber) → uint256
surplusAllowanceOf(projectId, rulesetId, terminal, token, currency) → uint256
usedSurplusAllowanceOf(projectId, terminal, token, rulesetId) → uint256
```

## Cast 命令（Foundry）

### 获取项目所有者
```bash
cast call $JB_PROJECTS "ownerOf(uint256)(address)" $PROJECT_ID --rpc-url $RPC_URL
```

### 获取当前规则集
```bash
cast call $JB_CONTROLLER "currentRulesetOf(uint256)" $PROJECT_ID --rpc-url $RPC_URL
```

### 获取项目代币
```bash
cast call $JB_TOKENS "tokenOf(uint256)(address)" $PROJECT_ID --rpc-url $RPC_URL
```

### 获取终端余额
```bash
cast call $JB_TERMINAL "currentSurplusOf(uint256,address[],uint256,uint256)" \
    $PROJECT_ID \
    "[$NATIVE_TOKEN]" \
    18 \
    $NATIVE_TOKEN \
    --rpc-url $RPC_URL
```

### 获取分配份额
```bash
# Reserved token splits (groupId = 1, JBSplitGroupIds.RESERVED_TOKENS)
cast call $JB_SPLITS "splitsOf(uint256,uint256,uint256)" \
    $PROJECT_ID $RULESET_ID 1 \
    --rpc-url $RPC_URL

# Payout splits - groupId = uint256(uint160(token))
# For ETH payouts: groupId = uint256(uint160(0x000000000000000000000000000000000000EEEe))
# The payout split group is derived from the token address being paid out
NATIVE_TOKEN="0x000000000000000000000000000000000000EEEe"
ETH_PAYOUT_GROUP=$(cast --to-uint256 $NATIVE_TOKEN)
cast call $JB_SPLITS "splitsOf(uint256,uint256,uint256)" \
    $PROJECT_ID $RULESET_ID $ETH_PAYOUT_GROUP \
    --rpc-url $RPC_URL

# For USDC payouts (example on mainnet):
USDC_ADDRESS="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
USDC_PAYOUT_GROUP=$(cast --to-uint256 $USDC_ADDRESS)
cast call $JB_SPLITS "splitsOf(uint256,uint256,uint256)" \
    $PROJECT_ID $RULESET_ID $USDC_PAYOUT_GROUP \
    --rpc-url $RPC_URL
```

### 获取代币余额
```bash
cast call $JB_TOKENS "totalBalanceOf(address,uint256)(uint256)" \
    $HOLDER_ADDRESS $PROJECT_ID \
    --rpc-url $RPC_URL
```

## TypeScript 示例（ethers.js）

### 设置
```typescript
import { ethers } from 'ethers';

const provider = new ethers.JsonRpcProvider(process.env.RPC_URL);

// Contract ABIs (simplified)
const PROJECTS_ABI = ['function ownerOf(uint256) view returns (address)'];
const CONTROLLER_ABI = ['function currentRulesetOf(uint256) view returns (tuple, tuple)'];
const TOKENS_ABI = ['function tokenOf(uint256) view returns (address)'];

const projects = new ethers.Contract(JB_PROJECTS, PROJECTS_ABI, provider);
const controller = new ethers.Contract(JB_CONTROLLER, CONTROLLER_ABI, provider);
const tokens = new ethers.Contract(JB_TOKENS, TOKENS_ABI, provider);
```

### 查询项目信息
```typescript
async function getProjectInfo(projectId: number) {
    const owner = await projects.ownerOf(projectId);
    const [ruleset, metadata] = await controller.currentRulesetOf(projectId);
    const tokenAddress = await tokens.tokenOf(projectId);

    return {
        owner,
        ruleset: {
            cycleNumber: ruleset.cycleNumber,
            weight: ruleset.weight,
            duration: ruleset.duration,
        },
        metadata: {
            reservedRate: metadata.reservedRate,
            cashOutTaxRate: metadata.cashOutTaxRate,
            dataHook: metadata.dataHook,
        },
        tokenAddress,
    };
}
```

### 查询代币持有者
```typescript
async function getTokenBalance(holder: string, projectId: number) {
    const balance = await tokens.totalBalanceOf(holder, projectId);
    return ethers.formatEther(balance);
}
```

## 常见查询

### “项目 X 使用的是哪个合约版本？”
**在进行任何涉及版本化合约的查询之前，** **务必先从这里开始**。
```bash
# Check JBDirectory.controllerOf() - the authoritative source
cast call 0x0061e516886a0540f63157f112c0588ee0651dcf \
  "controllerOf(uint256)(address)" $PROJECT_ID --rpc-url $RPC_URL

# V5.0 controller: 0x27da30646502e2f642be5281322ae8c394f7668a
# V5.1 controller: 0xf3cc99b11bd73a2e3b8815fb85fe0381b29987e1
```
然后使用相应的版本化合约（终端、规则集等）进行后续查询。

### “项目 X 的当前状态是什么？”
1. **首先**：通过 `JBDirectory.controllerOf(projectId)` 获取控制器版本——以确定使用哪些合约
2. 获取所有者：`JBProjects.ownerOf(projectId)`
3. 获取规则集：使用正确的版本化 `JBController.currentRulesetOf(projectId)`
4. 获取代币：`JBTokens.tokenOf(projectId)`
5. 获取终端：`JBDirectory.terminalsOf(projectId)`
6. 获取剩余资金：使用正确的版本化 `JBMultiTerminal.currentSurplusOf(...)`

### “分配份额的接收者是谁？”
1. 从 `currentRulesetOf` 获取当前规则集 ID
2. 查询预留的分配份额：`JBSplits.splitsOf(projectId, rulesetId, 1)`（group 1 = RESERVED_TOKENS）
3. 查询支付份额：`JBSplits.splitsOf(projectId, rulesetId, uint256(uint160(token)))`
   - 对于原生代币（ETH）：group = uint256(uint160(JBConstants.NATIVE_TOKEN))
   - 对于 USDC：group = uint256(uint160(USDC_ADDRESS))

### “可以支付多少？”
1. 获取支付限额：`JBFundAccessLimits.payoutLimitOf(...)`
2. 获取已使用金额：`JBFundAccessLimits.usedPayoutLimitOf(...)`
3. 剩余金额 = 限额 - 已使用金额

### “配置了哪些钩子？”
1. 从 `currentRulesetOf` 获取规则集元数据
2. 检查 `useDataHookForPay` 和 `useDataHookForCashOut`
3. 从 `dataHook` 获取钩子地址

## 网络 RPC 地址

| 网络 | RPC 地址 |
|---------|---------|
| Ethereum | `https://eth.llamarpc.com` |
| Sepolia | `https://rpc.sepolia.org` |
| Optimism | `https://mainnet.optimism.io` |
| Arbitrum | `https://arb1.arbitrum.io/rpc` |
| Base | `https://mainnet.base.org` |

## 生成指南

1. **确定用户问题所需的数据**
2. **确定需要查询的合约**
3. **提供用于快速 CLI 查询的 Cast 命令**
4. **提供 TypeScript 代码以实现程序化访问**
5. **使用 /jb-docs 技能获取当前的合约地址**

## 示例提示

- “项目 123 的当前规则集是什么？”
- “项目 456 的所有者是谁？”
- “项目 789 的剩余资金是多少？”
- “列出项目 42 的所有支付份额”
- “我在项目 100 中的代币余额是多少？”