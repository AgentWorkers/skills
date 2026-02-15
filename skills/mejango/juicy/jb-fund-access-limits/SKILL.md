---
name: jb-fund-access-limits
description: |
  Query and display Juicebox V5 fund access limits (payout limits, surplus allowances).
  Use when: (1) surplusAllowancesOf or payoutLimitsOf returns empty but values exist,
  (2) need to detect "unlimited" values which can be various max integers not just uint256,
  (3) fund access limits show as zero for USDC-based projects when querying with ETH token,
  (4) REVDeployer stageOf or configurationOf reverts, (5) CONFIGURING project deployment
  and need unlimited payouts - CRITICAL: empty fundAccessLimitGroups means ZERO payouts
  not unlimited, must use uint224.max for unlimited. Covers JBFundAccessLimits querying,
  multi-token support (ETH/USDC), ruleset chain walking, unlimited value detection, and
  proper configuration for project deployment.
---

# Juicebox V5 的资金访问限制

## 问题

资金访问限制存在两个主要问题：

1. **配置**：在部署项目时，如果 `fundAccessLimitGroups: []`（空数组），则表示**不允许任何资金支出**，而不是“无限支出”。这是一个常见的错误。要允许无限支出，必须明确使用 `uint224.max` 来设置 `payoutLimits`。

2. **查询**：在查询 JBFundAccessLimits 以获取支出限制或剩余额度时，即使合约中已经设置了相关值，查询结果也可能为空。此外，由于协议使用了多种不同的最大整数值，因此很难判断某个值是否表示“无限”。

## 上下文/触发条件

**配置（部署时）**：
- 用户选择“我将自行管理”或“无限支出”，但实际上无法提取资金。
- 生成了 `fundAccessLimitGroups: []`（这是错误的配置，会导致无法支出资金）。
- 项目所有者希望能够提取资金，但配置却限制了这一操作。

**查询（读取时）**：
- `surplusAllowancesOf` 或 `payoutLimitsOf` 返回空数组。
- 资金访问状态显示为“None”，而实际上应该是“Unlimited”。
- 项目使用 USDC 作为基础货币，而不是 ETH。
- `REVDeployer` 的 `stageOf` 或 `configurationOf` 函数可能导致配置回退。
- 显示的数值为较大的数字，而不是“Unlimited”字样。

## 解决方案

### 0. 关键点：配置无限支出（部署时）

**空的 `fundAccessLimitGroups: []` 表示不允许任何支出（并非无限支出！**  
要允许无限支出，必须使用 `uint224.max` 来设置支出限制：

```typescript
// uint224.max - the maximum value the JBFundAccessLimits registry accepts
const UINT224_MAX = '26959946667150639794667015087019630673637144422540572481103610249215'

// WRONG - this means ZERO payouts allowed
const wrongConfig = {
  fundAccessLimitGroups: []
}

// CORRECT - unlimited payouts for ETH
const correctConfigETH = {
  fundAccessLimitGroups: [{
    terminal: '0x3f75f7e52ed15c2850b0a6a49c234d5221576dbe', // JBMultiTerminal (ETH)
    token: '0x000000000000000000000000000000000000EEEe',    // Native token
    payoutLimits: [{
      amount: UINT224_MAX,
      currency: 1  // ETH currency
    }],
    surplusAllowances: []
  }]
}

// CORRECT - unlimited payouts for USDC (Ethereum mainnet)
const correctConfigUSDC = {
  fundAccessLimitGroups: [{
    terminal: '0x52869db3d61dde1e391967f2ce5039ad0ecd371c', // JBMultiTerminal5_1
    token: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',    // USDC on Ethereum
    payoutLimits: [{
      amount: UINT224_MAX,
      currency: 909516616  // USDC currency (from accounting context)
    }],
    surplusAllowances: []
  }]
}
```

**何时使用支出限制**：
- 用户希望提取已被预留的资金（这些资金不可用于提现）。
- 捐赠/筹款项目，项目所有者需要确保能够随时提取资金。
- 支出限制在每个规则集周期结束时重置——适用于定期分配的情况。

**何时使用剩余额度（所有者可提取资金且支持者也可提现）**：
- 所有者可以提取资金，同时支持者也可以提现。
- 剩余额度来自同一个资金池，支持者可以从中提取资金。
- 在所有者实际使用剩余额度之前，支持者仍然可以提取全部余额。
- 每个规则集仅适用一次，不会在每个周期内重置。

**关键区别**：
- 支出限制会减少可提取的资金金额（预留的资金不属于剩余额度）。
- 剩余额度会保留可提取的资金金额，直到所有者使用为止。
- **所有者和支持者共享剩余额度的使用权**——按先到先得的原则分配。

**何时使用零支出和零剩余额度**：
- 在 Revnets 中，使用剩余额度进行贷款。
- 项目中的资金仅用于支持者的赎回。

### 1. 多种代币的查询

资金访问限制是根据 `(projectId, rulesetId, terminal, token)` 来确定的。基于 USDC 的项目在使用 ETH 代币进行查询时将不会得到结果：

```typescript
const NATIVE_TOKEN = '0x000000000000000000000000000000000000EEEe'

// USDC addresses per chain
const USDC_ADDRESSES: Record<number, string> = {
  1: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',    // Ethereum
  10: '0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85',   // Optimism
  8453: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913', // Base
  42161: '0xaf88d065e77c8cC2239327C5EDb3A432268e5831', // Arbitrum
}

// Try ETH first, then USDC
let limits = await fetchLimitsForToken(rulesetId, NATIVE_TOKEN)
if (!limits) {
  const usdcToken = USDC_ADDRESSES[chainId]
  if (usdcToken) {
    limits = await fetchLimitsForToken(rulesetId, usdcToken)
  }
}
```

### 2. 回溯规则集链

如果当前 `rulesetId` 没有找到相应的限制信息，系统会回溯到 `basedOnId` 进行查找：

```typescript
let currentRsId = BigInt(rulesetId)
while (attempts < maxAttempts) {
  const ruleset = await publicClient.readContract({
    address: JB_CONTRACTS.JBRulesets,
    abi: JB_RULESETS_ABI,
    functionName: 'getRulesetOf',
    args: [BigInt(projectId), currentRsId],
  })

  const basedOnId = BigInt(ruleset.basedOnId)
  if (basedOnId === 0n || basedOnId === currentRsId) break

  const limits = await fetchLimitsForRuleset(basedOnId)
  if (limits) return limits

  currentRsId = basedOnId
}
```

### 3. 使用阈值判断“无限”状态

协议使用了多种不同的最大整数值（如 `uint256`, `uint224`, `uint128` 等）。可以使用阈值来判断是否为“无限”状态：

```typescript
const isUnlimited = (amount: string | undefined): boolean => {
  if (!amount) return false
  try {
    // Any value > 10^30 is effectively unlimited
    return amount.length > 30 || BigInt(amount) > BigInt('1000000000000000000000000000000')
  } catch {
    return false
  }
}
```

### 4. 处理不同版本的 REVDeployer

并非所有版本的 `REVDeployer` 都支持 `stageOf` 函数。可以通过时间戳来计算当前版本：

```typescript
// Instead of calling stageOf (may not exist)
try {
  const config = await publicClient.readContract({
    address: REV_DEPLOYER,
    abi: REV_DEPLOYER_ABI,
    functionName: 'configurationOf',
    args: [BigInt(projectId)],
  })

  // Calculate current stage from timestamps
  const now = Math.floor(Date.now() / 1000)
  let currentStage = 1
  for (let i = 0; i < stageConfigs.length; i++) {
    if (Number(stageConfigs[i].startsAtOrAfter) <= now) {
      currentStage = i + 1
    }
  }
} catch {
  // configurationOf may revert on older deployments - handle gracefully
}
```

## 验证

- 对于 Revnets，剩余额度会显示为“Unlimited”，而不是显示原始的巨大数值。
- 基于 USDC 的项目会显示正确的资金访问信息。
- 在较旧的项目上调用 `REVDeployer` 函数时，控制台不会出现错误。

## 示例

以 Artizen 项目（位于 Base 链 8453 上）为例：
- 该项目使用 USDC 作为货币，因此必须使用 USDC 代币地址进行查询。
- 剩余额度返回 `26959946667150640000000000000000000000000`，表示“无限”。
- `REVDeployer` 的 `configurationOf` 函数可能会导致配置回退，需要优雅地处理这种情况。

## 注意事项

- **关键点**：空的 `fundAccessLimitGroups` 表示不允许任何支出，并非无限支出。配置时务必使用 `uint224.max` 来设置无限支出。
- `uint224.max` 的示例值为 `26959946667150639794667015087019630673637144422540572481103610249215`。
- USDC 地址因链而异（请参考上述表格）。
- JBMultiTerminal5_1 的地址（`0x52869db3d61dde1e391967f2ce5039ad0ecd371c`）在所有链上都是相同的。
- 结果中的货币字段可能不符合标准格式，不要依赖它来显示资金信息。
- 对于 Revnets，支出限制始终为 0，剩余额度始终是无限的（用于贷款）。
- `fundAccessLimitGroups` 中的终端地址必须与接收支付的终端地址相匹配。

## 合约函数

```solidity
// JBFundAccessLimits
function payoutLimitsOf(
  uint256 projectId,
  uint256 rulesetId,
  address terminal,
  address token
) external view returns (JBCurrencyAmount[] memory);

function surplusAllowancesOf(
  uint256 projectId,
  uint256 rulesetId,
  address terminal,
  address token
) external view returns (JBCurrencyAmount[] memory);
```

## 参考资料

- JBFundAccessLimits 合约
- JBMultiTerminal5_1：`0x52869db3d61dde1e391967f2ce5039ad0ecd371c`