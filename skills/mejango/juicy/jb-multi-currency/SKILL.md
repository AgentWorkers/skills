---
name: jb-multi-currency
description: |
  Handle Juicebox V5 multi-currency projects (ETH vs USDC accounting).
  Use when: (1) building UI that displays currency labels (ETH vs USDC),
  (2) sending transactions that require currency parameter,
  (3) configuring fund access limits or accounting contexts for new rulesets,
  (4) querying project balance/surplus with correct token,
  (5) debugging "wrong currency" issues in payout or allowance transactions,
  (6) need currency code constants (NATIVE_CURRENCY=61166, USDC varies by chain),
  (7) cash out modal shows wrong return currency (ETH instead of USDC),
  (8) need shared chain constants (names, explorers) across multiple modals.
  Currency in JBAccountingContext is uint32(uint160(tokenAddress)), NOT 1 or 2.
  Covers baseCurrency detection, decimal handling, terminal accounting, currency codes,
  dynamic labels, cash out return display, and shared chain constants patterns.
---

# Juicebox V5 多货币支持

## 问题

Juicebox V5 项目可以使用 ETH（`baseCurrency=1`）或 USD（`baseCurrency=2`）作为货币单位。UI 组件和交易必须使用正确的货币值、代币地址以及显示标签。如果硬编码为 “ETH” 或 `baseCurrency=1`，基于 USDC 的项目将会出现故障。

## 背景/触发条件

- 当项目基于 USDC 时，UI 会显示 “ETH”。
- 支付或津贴交易会无声地失败。
- 资金访问限制设置使用了错误的货币单位。
- 规则集配置与终端会计系统中的货币单位不一致。
- 需要在表单中显示正确的货币符号。

## 解决方案

### 1. 从规则集中检测项目货币单位

```typescript
// baseCurrency is in ruleset metadata
// 1 = ETH, 2 = USD (USDC)
const baseCurrency = ruleset?.metadata?.baseCurrency || 1
const currencyLabel = baseCurrency === 2 ? 'USDC' : 'ETH'
```

### 2. 在交易中使用动态货币单位

在调用终端函数（`sendPayoutsOf`、`useAllowanceOf`）时，使用项目的 `baseCurrency`：

```typescript
// WRONG - hardcoded
args: [projectId, token, amount, 1n, minTokensPaidOut, beneficiary]

// CORRECT - dynamic
args: [projectId, token, amount, BigInt(baseCurrency), minTokensPaidOut, beneficiary]
```

### 3. 资金访问限制的货币单位

在排队新的规则集或显示限制时，确保与项目的实际货币单位一致。
**使用正确的小数位数**：通过 `ERC20.decimals()` 查询，或者对于原生代币使用 18 位小数。

```typescript
import { parseUnits } from 'viem'

// Get currency from existing config
const currency = existingConfig?.baseCurrency || 1

// Get decimals from the token contract (or 18 for native token)
// For USDC: 6 decimals. For native token (ETH): 18 decimals.
const decimals = await getTokenDecimals(tokenAddress, publicClient)

// Use in fund access limit configuration
const payoutLimits = [{
  amount: parseUnits(limitAmount, decimals).toString(),
  currency, // Match project's base currency (1 or 2)
}]
```

### 4. 两个不同的 “货币” 概念（关键点）

Juicebox V5 中存在两个经常被混淆的 “货币” 概念：

| 字段 | 位置 | 值 | 用途 |
|-------|----------|--------|---------|
| `baseCurrency` | 规则集元数据 | 1 = ETH, 2 = USD | 发行率计算 |
| `JBCurrencyAmount(currency` | 资金访问限制 | 1 = ETH, 2 = USD | 支付/津贴限制 |
| `JBAccountingContext(currency` | 终端配置 | `uint32(uint160(token))` | 终端会计系统 |

**`JBAccountingContext` 中的 `currency` 值不是 1 或 2，而是 `uint32(uint160(tokenAddress))`。**

```typescript
// NATIVE_TOKEN (ETH) - same on all chains - from JBConstants.NATIVE_TOKEN
const NATIVE_TOKEN = '0x000000000000000000000000000000000000EEEe'
const NATIVE_CURRENCY = 61166 // uint32(uint160(NATIVE_TOKEN)) = 0x0000EEEe

// USDC addresses and currency codes per chain
const USDC_CONFIG: Record<number, { address: string; currency: number }> = {
  1: {      // Ethereum
    address: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    currency: 909516616,
  },
  10: {     // Optimism
    address: '0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85',
    currency: 3530704773,
  },
  8453: {   // Base
    address: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
    currency: 3169378579,
  },
  42161: {  // Arbitrum
    address: '0xaf88d065e77c8cC2239327C5EDb3A432268e5831',
    currency: 1156540465,
  },
}
```

**如何从任何代币地址计算货币单位：**
```typescript
const calculateCurrency = (tokenAddress: string): number => {
  // Take last 4 bytes of address as uint32
  return Number(BigInt(tokenAddress) & BigInt(0xFFFFFFFF))
}
```

### 5. 小数位数处理

**通用规则**：对于任何代币，从小数位数获取值，使用 `ERC20.decimals()`。原生代币（如 ETH、MATIC 等）始终使用 18 位小数。

**常见情况：**
- 原生代币（ETH）：18 位小数
- USDC：6 位小数
- 大多数 ERC-20 代币：根据实际情况查询 `decimals()`**

```typescript
import { erc20Abi } from 'viem'

// For native token
const NATIVE_DECIMALS = 18

// For ERC-20 tokens - query the contract
const getTokenDecimals = async (tokenAddress: string, publicClient: PublicClient) => {
  if (tokenAddress === NATIVE_TOKEN) return NATIVE_DECIMALS
  return await publicClient.readContract({
    address: tokenAddress as `0x${string}`,
    abi: erc20Abi,
    functionName: 'decimals',
  })
}

// Shortcut for known tokens (use with caution)
const KNOWN_DECIMALS: Record<string, number> = {
  [NATIVE_TOKEN]: 18,
  // USDC on all chains uses 6 decimals
}
```

### 6. 终端会计系统中的货币单位

在配置终端时，确保会计系统使用的货币单位与项目的实际货币单位一致。
**错误做法**：对于 ETH 使用 `currency: 1`，对于 USD 使用 `currency: 2`。
**正确做法**：使用从代币地址计算出的 `uint32` 值。

## 组件模式

对于处理多种货币的 React 组件：

```typescript
interface ChainData {
  chainId: number
  projectId: number
  baseCurrency: number // 1 = ETH, 2 = USD
  // ... other fields
}

function MyComponent({ chainData }: { chainData: ChainData }) {
  const baseCurrency = chainData?.baseCurrency || 1
  const currencyLabel = baseCurrency === 2 ? 'USDC' : 'ETH'

  return (
    <div>
      <span>Amount: {amount} {currencyLabel}</span>
      {/* Use currencyLabel throughout, never hardcode "ETH" */}
    </div>
  )
}
```

### 7. 现金提取模态框中的货币显示

在提取现金时，用户会燃烧项目代币并收到 **项目的基础货币**。模态框必须显示正确的货币单位：

```typescript
interface CashOutModalProps {
  projectId: string
  tokenAmount: string      // Tokens being burned
  tokenSymbol: string      // e.g., "NANA", "REV"
  estimatedReturn: number  // Amount user will receive
  currencySymbol: 'ETH' | 'USDC'  // CRITICAL: matches project's base currency
}

function CashOutModal({
  tokenAmount,
  tokenSymbol,
  estimatedReturn,
  currencySymbol = 'ETH',  // Default to ETH for backwards compatibility
}: CashOutModalProps) {
  // Format decimals based on currency
  const decimals = currencySymbol === 'USDC' ? 2 : 4

  return (
    <div>
      <div>Burning: {tokenAmount} {tokenSymbol}</div>
      <div>You receive: ~{estimatedReturn.toFixed(decimals)} {currencySymbol}</div>
    </div>
  )
}
```

**关键点**：接收提取数据的组件必须根据项目的 `baseCurrency` 传递 `currencySymbol`，而不能硬编码为 “ETH”。对于基于 USDC 的项目，应显示 “~5.00 USDC” 而不是 “~0.002 ETH”。

### 8. 共享链信息常量模式

避免在各个模态框中重复存储链信息。创建一个共享的常量文件：

```typescript
// constants/index.ts
export const CHAINS: Record<number, {
  name: string
  shortName: string
  explorerTx: string
  explorerAddress: string
}> = {
  1: {
    name: 'Ethereum',
    shortName: 'ETH',
    explorerTx: 'https://etherscan.io/tx/',
    explorerAddress: 'https://etherscan.io/address/',
  },
  10: {
    name: 'Optimism',
    shortName: 'OP',
    explorerTx: 'https://optimistic.etherscan.io/tx/',
    explorerAddress: 'https://optimistic.etherscan.io/address/',
  },
  8453: {
    name: 'Base',
    shortName: 'BASE',
    explorerTx: 'https://basescan.org/tx/',
    explorerAddress: 'https://basescan.org/address/',
  },
  42161: {
    name: 'Arbitrum',
    shortName: 'ARB',
    explorerTx: 'https://arbiscan.io/tx/',
    explorerAddress: 'https://arbiscan.io/address/',
  },
}

export const NATIVE_TOKEN = '0x000000000000000000000000000000000000EEEe' as const
```

然后在各个模态框中导入这些常量：
```typescript
import { CHAINS, NATIVE_TOKEN } from '../constants'

const chainInfo = CHAINS[chainId] || CHAINS[1]
const explorerLink = `${chainInfo.explorerTx}${txHash}`
```

## 验证

- 基于 USDC 的项目会显示 “USDC” 作为货币单位。
- 现金提取模态框会以正确的货币单位显示返回金额（ETH 或 USDC）。
- 交易使用正确的货币参数。
- 资金访问限制存储正确的货币单位。
- 平衡查询使用正确的代币地址。

## 示例

以 Artizen（Base 上的第 6 个项目）为例：
- `baseCurrency = 2`（USD）
- 所有标签中均显示 “USDC”。
- 平衡查询使用 USDC 代币地址：`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`。
- 资金访问限制使用货币单位：2。

## 常见错误

1. **硬编码标签**：使用 “ETH” 字符串而不是 `currencyLabel`。
2. **硬编码货币单位**：使用 `1n` 而不是 `BigInt(baseCurrency)`。
3. **小数位数错误**：对于 USDC 使用 18 位小数（应为 6）。
4. **代币不匹配**：在查询 USDC 项目时使用错误的代币类型。

## 注意事项

- 如果未指定，默认使用 ETH（`baseCurrency=1`）。
- JBSwapTerminal 可以接受任何代币，并将其兑换为项目的基础货币。
- 现金提取时返回项目的基础货币。
- 价格信息会根据需要在不同货币之间进行转换。

## 参考资料

- JBMultiTerminal5_1: `0x52869db3d61dde1e391967f2ce5039ad0ecd371c`
- JBSwapTerminal: `0x0c02e48e55f4451a499e48a53595de55c40f3574`
- JBPrices: `0x6e92e3b5ce1e7a4344c6d27c0c54efd00df92fb6`