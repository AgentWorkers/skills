---
name: jb-terminal-selection
description: |
  Dynamic terminal selection for Juicebox V5 payments. Use when: (1) building payment UIs that support
  multiple tokens (ETH/USDC), (2) encountering JBMultiTerminal_TokenNotAccepted error, (3) paying a
  project that uses ETH-only accounting with non-ETH tokens, (4) implementing cross-token payments
  where the project may not directly accept the user's payment token. Covers JBDirectory.primaryTerminalOf()
  querying, JBSwapTerminal fallback logic, and permit2 integration with correct terminal addresses.
---

# Juicebox V5 支付中的动态终端选择机制

## 问题

在为 Juicebox V5 项目进行支付时，用户可能希望使用项目在其会计系统中不直接支持的代币（例如 USDC）进行支付。如果将此类支付发送到 `JBMultiTerminal`，将会导致 `JBMultiTerminal_TokenNotAccepted(token)` 错误。

**常见症状**：在完成 permit2 签名后，交易模拟会显示“可能失败”，并且在 Tenderly 或其他模拟工具中会出现 `TokenNotAccepted` 错误。

## 使用场景 / 触发条件**

在以下情况下应用此机制：
- 构建支持多种代币（如 ETH、USDC 等）的支付界面；
- 项目使用 ETH 作为会计系统，但用户希望使用 USDC 进行支付；
- 在交易模拟中看到 `JBMultiTerminal_TokenNotAccepted` 错误；
- MetaMask 在完成 permit2 签名后显示“此交易可能失败”；
- 需要在运行时确定使用哪个支付终端。

## 解决方案

### 核心概念

通过调用 `JBDirectory.primaryTerminalOf(projectId, tokenAddress)` 来查询接受特定代币支付的终端。如果没有任何终端被注册（返回空地址），则使用 `JBSwapTerminal`，它会自动将支付代币转换为项目支持的格式。

### 实现方式

```typescript
import { type PublicClient, type Address, zeroAddress } from 'viem'

// JBSwapTerminal addresses (same via CREATE2 across chains)
const JB_SWAP_TERMINAL: Record<number, Address> = {
  1: '0x259385b97dfbd5576bd717dc7b25967ec8b145dd',      // Ethereum
  10: '0x73d04584bde126242c36c2c7b219cbdec7aad774',     // Optimism
  8453: '0x4fd73d8b285e82471f08a4ef9861d6248b832edd',   // Base
  42161: '0x483c9b12c5bd2da73133aae30642ce0008c752ad',  // Arbitrum
}

// JBDirectory address (same on all chains via CREATE2)
const JB_DIRECTORY = '0x0061e516886a0540f63157f112c0588ee0651dcf'

const JB_DIRECTORY_ABI = [
  {
    name: 'primaryTerminalOf',
    type: 'function',
    stateMutability: 'view',
    inputs: [
      { name: 'projectId', type: 'uint256' },
      { name: 'token', type: 'address' },
    ],
    outputs: [{ name: '', type: 'address' }],
  },
] as const

type TerminalType = 'multi' | 'swap'

interface PaymentTerminal {
  address: Address
  type: TerminalType
}

/**
 * Determines which terminal to use for a payment.
 *
 * 1. Query JBDirectory.primaryTerminalOf(projectId, tokenAddress)
 * 2. If zero address → project doesn't accept this token directly → use SwapTerminal
 * 3. If non-zero → use the returned terminal (could be Multi or Swap)
 */
async function getPaymentTerminal(
  client: PublicClient,
  chainId: number,
  projectId: bigint,
  paymentToken: Address
): Promise<PaymentTerminal> {
  // Query directory for the primary terminal that accepts this token
  const terminal = await client.readContract({
    address: JB_DIRECTORY,
    abi: JB_DIRECTORY_ABI,
    functionName: 'primaryTerminalOf',
    args: [projectId, paymentToken],
  })

  const swapTerminal = JB_SWAP_TERMINAL[chainId]

  // No terminal registered for this token → use swap terminal
  if (terminal === zeroAddress) {
    return { address: swapTerminal, type: 'swap' }
  }

  // Check if the returned terminal IS the swap terminal
  const isSwapTerminal = terminal.toLowerCase() === swapTerminal?.toLowerCase()

  return {
    address: terminal,
    type: isSwapTerminal ? 'swap' : 'multi'
  }
}
```

### permit2 的集成

在使用 permit2 进行代币审批时，元数据 ID 的计算必须使用正确的终端地址作为支付方：

```typescript
// Permit2 metadata ID = bytes4(bytes20(terminal) ^ bytes20(keccak256("permit2")))
function computePermit2MetadataId(terminalAddress: Address): `0x${string}` {
  const permit2Hash = keccak256(toBytes('permit2'))
  const terminalBytes = terminalAddress.slice(0, 42) // 0x + 40 hex chars
  const hashBytes = permit2Hash.slice(0, 42)

  // XOR the first 20 bytes
  const xorResult = BigInt(terminalBytes) ^ BigInt(hashBytes)
  const bytes4 = (xorResult >> 128n) & 0xffffffffn

  return `0x${bytes4.toString(16).padStart(8, '0')}`
}
```

### 在支付流程中的使用方式

```typescript
async function pay(projectId: string, amount: string, token: 'ETH' | 'USDC') {
  const tokenAddress = token === 'ETH'
    ? '0x000000000000000000000000000000000000EEEe'  // Native token
    : USDC_ADDRESSES[chainId]

  // 1. Detect correct terminal
  const terminal = await getPaymentTerminal(
    publicClient,
    chainId,
    BigInt(projectId),
    tokenAddress
  )

  // 2. For ERC20, sign permit2 with terminal as spender
  if (token !== 'ETH') {
    const permit = await signPermit2({
      spender: terminal.address,  // CRITICAL: use detected terminal
      token: tokenAddress,
      amount,
      // ...
    })
  }

  // 3. Call pay on the correct terminal
  await walletClient.writeContract({
    address: terminal.address,
    abi: terminal.type === 'swap' ? JB_SWAP_TERMINAL_ABI : JB_MULTI_TERMINAL_ABI,
    functionName: 'pay',
    args: [projectId, tokenAddress, amount, beneficiary, minTokens, memo, metadata],
  })
}
```

## 验证方法

1. 对于 ETH，调用 `primaryTerminalOf` 应返回 `JBMultiTerminal` 的地址；
2. 对于仅支持 ETH 的项目，调用 `primaryTerminalOf` 应返回空地址；
3. 如果返回空地址，则使用 `SwapTerminal`；
4. 交易模拟不应再显示 `TokenNotAccepted` 错误。

## 示例

**场景**：用户希望在 Base 平台上使用 USDC 为 NANA（项目 ID 1）进行支付，但 NANA 仅支持 ETH 作为支付方式。

```typescript
// Query: What terminal accepts USDC for NANA?
const terminal = await getPaymentTerminal(
  publicClient,
  8453,  // Base
  1n,    // NANA project ID
  '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'  // USDC on Base
)

// Result: { address: '0x4fd73d8b285e82471f08a4ef9861d6248b832edd', type: 'swap' }
// The SwapTerminal will swap USDC → ETH before paying NANA
```

## 注意事项

- `JBSwapTerminal` 会在将代币记入项目账户之前通过 Uniswap 进行代币转换；
- 该转换过程使用 TWAP 价格机制，并提供滑点保护；
- 项目可以明确注册它们希望支持的代币对应的 `JBSwapTerminal`；
- 有些项目会同时注册多个代币对应的 `JBMultiTerminal`（例如 ETH 和 USDC）；
- 始终在运行时进行查询，因为终端的注册信息可能会发生变化。

## 相关技能

- `/jb-v5-impl`：深入研究终端机制和支付流程的内部实现；
- `/jb-terminal-wrapper`：用于封装终端功能的自定义逻辑框架；
- `/jb-v5-api`：核心的终端接口接口；
- `/jb-query`：用于从区块链中查询项目状态。

## 参考资料

- [revnet-app 的终端检测功能](https://github.com/rev-net/revnet-app/blob/main/src/lib/paymentTerminal.ts)
- [JBSwapTerminal 的实现](https://github.com/Bananapus/nana-swap-terminal)
- [JBDirectory 合同](https://github.com/Bananapus/nana-core-v5/blob/main/src/JBDirectory.sol)