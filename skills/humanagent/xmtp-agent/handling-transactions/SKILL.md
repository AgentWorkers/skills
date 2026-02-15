---
name: handling-transactions
description: XMTP代理的令牌交易和钱包集成功能。适用于发送USDC、创建交易请求或处理交易确认等场景。该功能会在USDC转账、钱包操作或交易引用发生时被触发。
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# XMTP交易

使用`wallet_sendCalls`（EIP-5792）规范发送和接收代币交易。

## 适用场景

在以下情况下请参考这些指南：
- 发送USDC或其他代币
- 创建交易请求
- 处理交易确认
- 检查代币余额
- 使用智能合约钱包

## 规则类别（按优先级排序）

| 优先级 | 类别 | 影响程度 | 前缀 |
|----------|----------|--------|--------|
| 1 | 发送 | 关键 | `send-` |
| 2 | 接收 | 关键 | `receive-` |
| 3 | 余额 | 高 | `balance-` |

## 快速参考

### 发送（关键）
- `send-usdc-transfer` - 创建USDC转账请求
- `send-wallet-calls` - 发送`wallet_sendCalls`消息

### 接收（关键）
- `receive-transaction-reference` - 处理交易确认

### 余额（高）
- `balance-check` - 检查USDC余额

## 支持的网络

| 网络 | 链路ID | USDC地址 |
|---------|----------|--------------|
| Base Sepolia | 84532 | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |
| Base Mainnet | 8453 | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |

## 快速入门

```typescript
import { validHex } from "@xmtp/agent-sdk";

// Check balance using viem
const balance = await getUSDCBalance("base-sepolia", validHex(address));

// Create USDC transfer calls (EIP-5792)
const calls = createUSDCTransferCalls(
  "base-sepolia",
  validHex(fromAddress),
  validHex(toAddress),
  1000000 // 1 USDC (6 decimals)
);
await ctx.conversation.sendWalletSendCalls(calls);
```

## 实现示例

**USDC代币配置：**

```typescript
const USDC_TOKENS: Record<string, { address: string; decimals: number }> = {
  "base-sepolia": { address: "0x036CbD53842c5426634e7929541eC2318f3dCF7e", decimals: 6 },
  "base-mainnet": { address: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", decimals: 6 },
};
```

**获取USDC余额：**

```typescript
import { createPublicClient, formatUnits, http } from "viem";
import { baseSepolia, base } from "viem/chains";

const getUSDCBalance = async (networkId: string, address: HexString): Promise<string> => {
  const token = USDC_TOKENS[networkId];
  const client = createPublicClient({
    chain: networkId === "base-mainnet" ? base : baseSepolia,
    transport: http(),
  });
  const balance = await client.readContract({
    address: token.address as HexString,
    abi: [{ inputs: [{ name: "account", type: "address" }], name: "balanceOf", outputs: [{ type: "uint256" }], stateMutability: "view", type: "function" }],
    functionName: "balanceOf",
    args: [address],
  });
  return formatUnits(balance, token.decimals);
};
```

**创建USDC转账请求：**

```typescript
import { toHex } from "viem";

const createUSDCTransferCalls = (
  networkId: string, from: HexString, to: string, amount: number
): WalletSendCalls => {
  const token = USDC_TOKENS[networkId];
  const data = `0xa9059cbb${to.slice(2).padStart(64, "0")}${BigInt(amount).toString(16).padStart(64, "0")}`;
  return {
    version: "1.0",
    from,
    chainId: toHex(networkId === "base-mainnet" ? 8453 : 84532),
    calls: [{ to: token.address as HexString, data: validHex(data) }],
  };
};
```

## 使用方法

如需详细说明，请阅读相应的规则文件：

```
rules/send-usdc-transfer.md
rules/receive-transaction-reference.md
rules/balance-check.md
```